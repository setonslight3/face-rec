from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import os
import json
from datetime import datetime, timedelta
import pickle
import base64
import logging
from deepface import DeepFace

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Set up paths - use current directory for files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_PHOTOS_DIR = os.path.join(BASE_DIR, "student_photos")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance_logs.json")
FACE_ENCODER_FILE = os.path.join(BASE_DIR, "face_encoder.pkl")
COURSES_FILE = os.path.join(BASE_DIR, "courses.json")
ENROLLMENTS_FILE = os.path.join(BASE_DIR, "enrollments.json")
STUDENT_DETAILS_FILE = os.path.join(BASE_DIR, "student_details.json")
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

known_face_encodings = {}
known_face_names = []
attendance_records = {}
courses = {}
enrollments = {}
student_details = {}  # Store student ID, email, and other details
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def load_data():
    global known_face_encodings, known_face_names, attendance_records, courses, enrollments, student_details
    # Clear existing data to avoid duplicates if reloaded
    known_face_encodings = {}
    known_face_names = []
    attendance_records = {}
    courses = {}
    enrollments = {}
    student_details = {}
    
    try:
        if os.path.exists(ATTENDANCE_FILE):
            with open(ATTENDANCE_FILE, 'r') as f:
                attendance_records = json.load(f)
                logger.info(f"Loaded {len(attendance_records)} attendance records")

        if os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, 'r') as f:
                courses = json.load(f)
                logger.info(f"Loaded {len(courses)} courses")

        if os.path.exists(ENROLLMENTS_FILE):
            with open(ENROLLMENTS_FILE, 'r') as f:
                enrollments = json.load(f)
                logger.info(f"Loaded enrollment data")

        if os.path.exists(STUDENT_DETAILS_FILE):
            with open(STUDENT_DETAILS_FILE, 'r') as f:
                student_details = json.load(f)
                logger.info(f"Loaded {len(student_details)} student details")

        if os.path.exists(FACE_ENCODER_FILE):
            with open(FACE_ENCODER_FILE, 'rb') as f:
                data = pickle.load(f)
                known_face_encodings = data['encodings']
                known_face_names = data['names']
                logger.info(f"Loaded {len(known_face_names)} students from cache")
        else:
            load_students_from_photos()
    except Exception as e:
        logger.error(f"Error loading data: {e}")

def encode_face(image):
    """Extract face embedding from image using DeepFace"""
    try:
        # DeepFace expects RGB images
        if isinstance(image, np.ndarray):
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image

        # Try multiple detectors in order of accuracy
        # RetinaFace is best, MTCNN is good balance, OpenCV is a fallback
        detectors = ["retinaface", "mtcnn", "opencv"]
        
        for detector in detectors:
            try:
                embeddings = DeepFace.represent(
                    img_path=image_rgb,
                    model_name="Facenet",
                    detector_backend=detector,
                    enforce_detection=True,
                    align=True
                )
                if embeddings and len(embeddings) > 0:
                    embedding = np.array(embeddings[0]['embedding'])
                    logger.info(f"Generated embedding using {detector}")
                    return embedding
            except Exception as e:
                logger.debug(f"Detector {detector} failed: {e}")
                continue
                
    except Exception as e:
        logger.warning(f"Error encoding face: {e}")
    return None

def get_face_embedding_from_array(image_array):
    """Extract encoding from image array"""
    return encode_face(image_array)

def load_students_from_photos():
    global known_face_encodings, known_face_names
    if not os.path.exists(STUDENT_PHOTOS_DIR):
        os.makedirs(STUDENT_PHOTOS_DIR)
        return

    count = 0
    for filename in os.listdir(STUDENT_PHOTOS_DIR):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            student_name = os.path.splitext(filename)[0]
            image_path = os.path.join(STUDENT_PHOTOS_DIR, filename)
            try:
                image = cv2.imread(image_path)
                if image is None:
                    continue
                encoding = encode_face(image)
                if encoding is not None:
                    known_face_encodings[student_name] = encoding
                    if student_name not in known_face_names:
                        known_face_names.append(student_name)
                    count += 1
                    logger.info(f"Loaded: {student_name} with embedding shape {encoding.shape}")
            except Exception as e:
                logger.warning(f"Error processing {filename}: {e}")

    if count > 0:
        save_face_embeddings()
        logger.info(f"Saved {count} student embeddings to cache")

def save_face_embeddings():
    data = {'encodings': known_face_encodings, 'names': known_face_names}
    with open(FACE_ENCODER_FILE, 'wb') as f:
        pickle.dump(data, f)

def save_attendance():
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(attendance_records, f, indent=2)

def save_courses():
    with open(COURSES_FILE, 'w') as f:
        json.dump(courses, f, indent=2)

def save_enrollments():
    with open(ENROLLMENTS_FILE, 'w') as f:
        json.dump(enrollments, f, indent=2)

def save_student_details():
    with open(STUDENT_DETAILS_FILE, 'w') as f:
        json.dump(student_details, f, indent=2)

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_match(encoding):
    """Find matching student using cosine similarity"""
    if not known_face_encodings or encoding is None:
        logger.warning("No known encodings or encoding is None")
        return None

    best_match = None
    best_similarity = -1  # Cosine similarity ranges from -1 to 1

    logger.info(f"Looking for match among {len(known_face_encodings)} students")
    logger.info(f"Query encoding shape: {encoding.shape}, dtype: {encoding.dtype}")

    for student_name, known_encoding in known_face_encodings.items():
        # Ensure both encodings are numpy arrays
        if isinstance(known_encoding, np.ndarray):
            similarity = cosine_similarity(encoding, known_encoding)
            logger.info(f"Similarity with {student_name}: {similarity:.4f}")

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = student_name

    # Threshold for Facenet embeddings - typically 0.40 distance for cosine
    # which translates to 0.60 similarity.
    logger.info(f"Best match: {best_match} with similarity: {best_similarity:.4f}")

    if best_similarity > 0.70:  # Using 0.70 for higher confidence
        return best_match
    return None

@app.route('/')
def serve_frontend():
    frontend_dir = os.path.join(BASE_DIR, 'frontend')
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    frontend_dir = os.path.join(BASE_DIR, 'frontend')
    return send_from_directory(frontend_dir, path)

@app.route('/api/register_student', methods=['POST'])
def register_student():
    global known_face_encodings, known_face_names, enrollments, student_details
    try:
        data = request.json
        student_name = data.get('name', '').strip()
        student_id = data.get('student_id', '').strip()
        email = data.get('email', '').strip()
        image_base64 = data.get('image')
        selected_courses = data.get('courses', [])

        if not student_name or not image_base64:
            return jsonify({'error': 'Missing name or image'}), 400

        if len(student_name) > 100 or len(student_name) < 2:
            return jsonify({'error': 'Name must be 2-100 characters'}), 400

        # Check for duplicate student ID
        if student_id:
            for name, details in student_details.items():
                if details.get('student_id') == student_id:
                    return jsonify({'error': f'Student ID {student_id} already exists'}), 400

        try:
            image_data = base64.b64decode(image_base64.split(',')[1])
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                return jsonify({'error': 'Invalid image'}), 400
        except Exception as e:
            logger.error(f"Decode error: {e}")
            return jsonify({'error': 'Image processing failed'}), 400

        encoding = get_face_embedding_from_array(image)
        if encoding is None:
            return jsonify({'error': 'No face detected'}), 400

        known_face_encodings[student_name] = encoding
        if student_name not in known_face_names:
            known_face_names.append(student_name)

        # Store student details
        student_details[student_name] = {
            'student_id': student_id,
            'email': email,
            'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Enroll student in selected courses
        if student_name not in enrollments:
            enrollments[student_name] = []

        for course_id in selected_courses:
            if course_id not in enrollments[student_name]:
                enrollments[student_name].append(course_id)

        os.makedirs(STUDENT_PHOTOS_DIR, exist_ok=True)
        cv2.imwrite(os.path.join(STUDENT_PHOTOS_DIR, f"{student_name}.jpg"), image)
        save_face_embeddings()
        save_enrollments()
        save_student_details()

        return jsonify({'success': True, 'message': f'{student_name} registered and enrolled in {len(selected_courses)} course(s)'})
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():
    try:
        data = request.json
        image_base64 = data.get('image')
        course_id = data.get('course_id')
        
        if not image_base64:
            return jsonify({'error': 'No image'}), 400
        
        try:
            image_data = base64.b64decode(image_base64.split(',')[1])
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                return jsonify({'error': 'Invalid image'}), 400
        except:
            return jsonify({'error': 'Image processing failed'}), 400
        
        encoding = get_face_embedding_from_array(image)
        if encoding is None:
            return jsonify({'error': 'No face detected'}), 400

        logger.info(f"Generated encoding shape: {encoding.shape}")
        logger.info(f"Known students: {list(known_face_encodings.keys())}")

        student_name = find_match(encoding)
        if student_name:
            today = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Track attendance per course if course_id is provided
            if course_id and course_id in courses:
                record_key = f"{student_name}_{course_id}"
            else:
                record_key = student_name
            
            if record_key not in attendance_records:
                attendance_records[record_key] = []
            
            already_marked = any(r['date'] == today for r in attendance_records[record_key])
            if not already_marked:
                attendance_records[record_key].append({'date': today, 'time': current_time, 'status': 'present', 'course': course_id})
                save_attendance()
                return jsonify({'success': True, 'recognized': [{'name': student_name, 'status': 'marked', 'time': current_time, 'courses': enrollments.get(student_name, [])}]})
            else:
                return jsonify({'success': True, 'recognized': [{'name': student_name, 'status': 'already_marked', 'time': current_time}]})
        else:
            return jsonify({'success': False, 'error': 'Face not recognized'}), 404
    except Exception as e:
        logger.error(f"Attendance error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_attendance', methods=['GET'])
def get_attendance():
    try:
        date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
        course_id = request.args.get('course_id')
        
        if course_id and course_id in courses:
            # Get attendance for specific course
            attendance_today = []
            for student in known_face_names:
                if student in enrollments and course_id in enrollments[student]:
                    record_key = f"{student}_{course_id}"
                    records = attendance_records.get(record_key, [])
                    record = next((r for r in records if r['date'] == date), None)
                    attendance_today.append({
                        'name': student,
                        'status': record['status'] if record else 'absent',
                        'time': record['time'] if record else None
                    })
            
            return jsonify({
                'date': date,
                'course_id': course_id,
                'course_name': courses[course_id]['name'],
                'attendance': attendance_today,
                'total_students': len(attendance_today),
                'present_count': sum(1 for a in attendance_today if a['status'] == 'present')
            })
        else:
            # Get general attendance
            attendance_today = []
            for student in known_face_names:
                records = attendance_records.get(student, [])
                record = next((r for r in records if r['date'] == date), None)
                attendance_today.append({
                    'name': student,
                    'status': record['status'] if record else 'absent',
                    'time': record['time'] if record else None
                })
            
            return jsonify({
                'date': date,
                'attendance': attendance_today,
                'total_students': len(known_face_names),
                'present_count': sum(1 for a in attendance_today if a['status'] == 'present')
            })
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_students', methods=['GET'])
def get_students():
    students_list = []
    for name in known_face_names:
        details = student_details.get(name, {})
        photo_path = os.path.join(STUDENT_PHOTOS_DIR, f"{name}.jpg")
        photo_url = f"/student_photos/{name}.jpg" if os.path.exists(photo_path) else None
        students_list.append({
            'name': name,
            'student_id': details.get('student_id', ''),
            'email': details.get('email', ''),
            'registered_at': details.get('registered_at', ''),
            'photo_url': photo_url,
            'courses': enrollments.get(name, [])
        })
    return jsonify({'students': students_list, 'total': len(students_list)})

@app.route('/api/student_details/<name>', methods=['GET'])
def get_student_details(name):
    try:
        if name not in known_face_names:
            return jsonify({'error': 'Student not found'}), 404

        details = student_details.get(name, {})
        photo_path = os.path.join(STUDENT_PHOTOS_DIR, f"{name}.jpg")

        # Calculate attendance stats
        student_courses = enrollments.get(name, [])
        total_records = 0
        present_count = 0

        for course_id in student_courses:
            record_key = f"{name}_{course_id}"
            records = attendance_records.get(record_key, [])
            total_records += len(records)
            present_count += sum(1 for r in records if r.get('status') == 'present')

        # General attendance records
        general_records = attendance_records.get(name, [])
        total_records += len(general_records)
        present_count += sum(1 for r in general_records if r.get('status') == 'present')

        attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0

        course_details = []
        for course_id in student_courses:
            if course_id in courses:
                course_details.append({
                    'id': course_id,
                    'name': courses[course_id].get('name', ''),
                    'code': courses[course_id].get('code', '')
                })

        return jsonify({
            'name': name,
            'student_id': details.get('student_id', ''),
            'email': details.get('email', ''),
            'registered_at': details.get('registered_at', ''),
            'photo_url': f"/student_photos/{name}.jpg" if os.path.exists(photo_path) else None,
            'courses': course_details,
            'attendance_stats': {
                'total_records': total_records,
                'present_count': present_count,
                'attendance_rate': round(attendance_rate, 1)
            }
        })
    except Exception as e:
        logger.error(f"Error getting student details: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance_range', methods=['GET'])
def get_attendance_range():
    try:
        from_date = request.args.get('from')
        to_date = request.args.get('to')
        course_id = request.args.get('course_id')

        if not from_date or not to_date:
            return jsonify({'error': 'Date range required'}), 400

        # Generate date range
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")
        date_range = []
        current = from_dt
        while current <= to_dt:
            date_range.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        # Get attendance for each date
        range_data = []
        for date_str in date_range:
            day_attendance = []

            if course_id and course_id in courses:
                # Course-specific attendance
                for student in known_face_names:
                    if student in enrollments and course_id in enrollments[student]:
                        record_key = f"{student}_{course_id}"
                        records = attendance_records.get(record_key, [])
                        record = next((r for r in records if r['date'] == date_str), None)
                        details = student_details.get(student, {})
                        day_attendance.append({
                            'name': student,
                            'student_id': details.get('student_id', ''),
                            'status': record['status'] if record else 'absent',
                            'time': record['time'] if record else None
                        })
            else:
                # General attendance
                for student in known_face_names:
                    records = attendance_records.get(student, [])
                    record = next((r for r in records if r['date'] == date_str), None)
                    details = student_details.get(student, {})
                    day_attendance.append({
                        'name': student,
                        'student_id': details.get('student_id', ''),
                        'status': record['status'] if record else 'absent',
                        'time': record['time'] if record else None
                    })

            present = sum(1 for a in day_attendance if a['status'] == 'present')
            range_data.append({
                'date': date_str,
                'total': len(day_attendance),
                'present': present,
                'absent': len(day_attendance) - present,
                'attendance': day_attendance
            })

        return jsonify({
            'from_date': from_date,
            'to_date': to_date,
            'course_id': course_id,
            'course_name': courses.get(course_id, {}).get('name') if course_id else None,
            'range_data': range_data
        })
    except Exception as e:
        logger.error(f"Error getting attendance range: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        days = int(request.args.get('days', 30))
        course_id = request.args.get('course_id')

        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)

        # Get student attendance counts
        student_attendance = {}
        course_attendance = {}

        for student in known_face_names:
            student_attendance[student] = {'present': 0, 'total': 0}

        for course_id_key, course_data in courses.items():
            course_attendance[course_id_key] = {'name': course_data.get('name', ''), 'present': 0, 'total': 0}

        # Count attendance records
        total_present = 0
        total_absent = 0
        daily_stats = {}

        for record_key, records in attendance_records.items():
            for record in records:
                record_date = datetime.strptime(record['date'], "%Y-%m-%d")
                if from_date <= record_date <= to_date:
                    date_str = record['date']
                    if date_str not in daily_stats:
                        daily_stats[date_str] = {'present': 0, 'total': 0}

                    daily_stats[date_str]['total'] += 1
                    if record['status'] == 'present':
                        daily_stats[date_str]['present'] += 1
                        total_present += 1
                    else:
                        total_absent += 1

                    # Extract student name from record key
                    student_name = record_key.split('_')[0]
                    if student_name in student_attendance:
                        student_attendance[student_name]['total'] += 1
                        if record['status'] == 'present':
                            student_attendance[student_name]['present'] += 1

        # Calculate overall rate
        total_records = total_present + total_absent
        overall_rate = (total_present / total_records * 100) if total_records > 0 else 0

        # Sort students by attendance rate
        student_ranking = []
        for name, stats in student_attendance.items():
            if stats['total'] > 0:
                rate = (stats['present'] / stats['total'] * 100)
                student_ranking.append({
                    'name': name,
                    'student_id': student_details.get(name, {}).get('student_id', ''),
                    'present': stats['present'],
                    'total': stats['total'],
                    'rate': round(rate, 1)
                })

        student_ranking.sort(key=lambda x: x['rate'], reverse=True)

        # Find most attended course
        top_course = None
        top_course_rate = 0
        for cid, cdata in course_attendance.items():
            if cdata['total'] > 0:
                rate = (cdata['present'] / cdata['total'] * 100)
                if rate > top_course_rate:
                    top_course_rate = rate
                    top_course = cdata['name']

        # Format daily stats for chart
        trend_data = []
        for date_str in sorted(daily_stats.keys()):
            day_data = daily_stats[date_str]
            rate = (day_data['present'] / day_data['total'] * 100) if day_data['total'] > 0 else 0
            trend_data.append({
                'date': date_str,
                'rate': round(rate, 1),
                'present': day_data['present'],
                'total': day_data['total']
            })

        return jsonify({
            'period': f'Last {days} days',
            'overall_rate': round(overall_rate, 1),
            'total_present': total_present,
            'total_absent': total_absent,
            'total_students': len(known_face_names),
            'top_course': top_course,
            'student_ranking': student_ranking[:10],  # Top 10
            'trend_data': trend_data
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500

# Serve student photos
@app.route('/student_photos/<filename>')
def serve_student_photo(filename):
    return send_from_directory(STUDENT_PHOTOS_DIR, filename)

@app.route('/api/delete_student/<name>', methods=['DELETE'])
def delete_student(name):
    global known_face_encodings, known_face_names, enrollments, student_details
    try:
        if name in known_face_names:
            del known_face_encodings[name]
            known_face_names.remove(name)
            photo_path = os.path.join(STUDENT_PHOTOS_DIR, f"{name}.jpg")
            if os.path.exists(photo_path):
                os.remove(photo_path)
            if name in attendance_records:
                del attendance_records[name]
            if name in enrollments:
                del enrollments[name]
            if name in student_details:
                del student_details[name]
            save_face_embeddings()
            save_attendance()
            save_enrollments()
            save_student_details()
            return jsonify({'success': True, 'message': f'{name} deleted'})
        return jsonify({'error': 'Not found'}), 404
    except Exception as e:
        logger.error(f"Delete error: {e}")
        return jsonify({'error': str(e)}), 500

# Course Management APIs

@app.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        course_list = []
        for course_id, course_data in courses.items():
            course_info = {
                'id': course_id,
                'name': course_data.get('name', ''),
                'code': course_data.get('code', ''),
                'instructor': course_data.get('instructor', ''),
                'timetable': course_data.get('timetable', [])
            }
            course_list.append(course_info)
        return jsonify({'courses': course_list, 'total': len(course_list)})
    except Exception as e:
        logger.error(f"Error getting courses: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses', methods=['POST'])
def create_course():
    global courses
    try:
        data = request.json
        course_name = data.get('name', '').strip()
        course_code = data.get('code', '').strip()
        instructor = data.get('instructor', '').strip()
        timetable = data.get('timetable', [])
        
        if not course_name or not course_code:
            return jsonify({'error': 'Course name and code are required'}), 400
        
        course_id = course_code.replace(' ', '_').lower()
        
        if course_id in courses:
            return jsonify({'error': 'Course already exists'}), 400
        
        courses[course_id] = {
            'name': course_name,
            'code': course_code,
            'instructor': instructor,
            'timetable': timetable
        }
        save_courses()
        
        return jsonify({'success': True, 'message': f'Course {course_name} created', 'course_id': course_id})
    except Exception as e:
        logger.error(f"Course creation error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<course_id>', methods=['PUT'])
def update_course(course_id):
    global courses
    try:
        if course_id not in courses:
            return jsonify({'error': 'Course not found'}), 404
        
        data = request.json
        courses[course_id]['name'] = data.get('name', courses[course_id]['name'])
        courses[course_id]['code'] = data.get('code', courses[course_id]['code'])
        courses[course_id]['instructor'] = data.get('instructor', courses[course_id]['instructor'])
        courses[course_id]['timetable'] = data.get('timetable', courses[course_id]['timetable'])
        
        save_courses()
        return jsonify({'success': True, 'message': 'Course updated'})
    except Exception as e:
        logger.error(f"Course update error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    global courses
    try:
        if course_id not in courses:
            return jsonify({'error': 'Course not found'}), 404
        
        del courses[course_id]
        save_courses()
        return jsonify({'success': True, 'message': 'Course deleted'})
    except Exception as e:
        logger.error(f"Course deletion error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/student_courses/<name>', methods=['GET'])
def get_student_courses(name):
    try:
        student_courses = enrollments.get(name, [])
        course_details = []
        for course_id in student_courses:
            if course_id in courses:
                course_info = {
                    'id': course_id,
                    'name': courses[course_id].get('name', ''),
                    'code': courses[course_id].get('code', ''),
                    'instructor': courses[course_id].get('instructor', ''),
                    'timetable': courses[course_id].get('timetable', [])
                }
                course_details.append(course_info)
        return jsonify({'courses': course_details, 'total': len(course_details)})
    except Exception as e:
        logger.error(f"Error getting student courses: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
