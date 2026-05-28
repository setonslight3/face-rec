 # 📸 Face Recognition Attendance System

A web-based facial recognition system for automated student attendance tracking with real-time face detection and recording.

## Features

✅ **Real-time Face Recognition** - Recognizes registered students via webcam  
✅ **Student Registration** - Register new students with facial photos  
✅ **Automated Attendance** - Mark attendance automatically with face detection  
✅ **Attendance Records** - View daily attendance reports with statistics  
✅ **Student Management** - Add, view, and delete registered students  
✅ **Modern UI** - Clean, responsive web interface  

## System Requirements

- Python 3.8+
- Webcam/Camera device
- Modern web browser (Chrome, Firefox, Edge, Safari)
- 4GB+ RAM (for DeepFace models)
- 2GB+ free disk space

## Installation & Setup

### Step 1: Install Python Dependencies

```bash
cd attendance-system
pip install -r backend/requirements.txt
```

**Note**: First-time installation of DeepFace will download pre-trained models (~350MB). This may take 5-10 minutes.

### Step 2: Run the Application

```bash
python run.py
```

You should see:
```
============================================================
🚀 Face Recognition Attendance System
============================================================

📋 System Information:
   Python: 3.x.x
   Directory: C:\Users\...\attendance-system

💡 Quick Start Guide:
   1. Go to 'Register Student' tab
   2. Take a clear photo of a student
   3. Enter their name and click Register
   4. Switch to 'Mark Attendance' tab
   5. Student looks at camera and clicks 'Mark Attendance'

⚠️  Important Notes:
   • Ensure faces are well-lit and clearly visible
   • First startup may take longer (model download)
   • Allow camera permissions when prompted

============================================================
✅ Starting server...
📱 Open your browser: http://localhost:5000
============================================================
```

### Step 3: Access the Web Interface

Open your browser and navigate to: **http://localhost:5000**

## Usage Guide

### 📋 Registering Students

1. Click **"Register Student"** tab
2. Enter the student's name
3. Click **"Capture Photo"** button
4. Ensure good lighting and face is clearly visible
5. Click **"Register Student"** to save

**Tips for Better Recognition:**
- Use good lighting (natural light or bright indoor lighting)
- Face should be centered in camera
- Avoid glasses or extreme angles
- Head should be straight-on (neutral expression)

### ✅ Marking Attendance

1. Click **"Mark Attendance"** tab
2. Student looks at the camera
3. Click **"Mark Attendance"** button
4. System will recognize the face and mark attendance
5. Success message appears with timestamp

### 📊 Viewing Attendance Records

1. Click **"Attendance Records"** tab
2. Select a date (defaults to today)
3. Click **"Load Records"** to view
4. See attendance summary and detailed list

### 👥 Managing Students

1. Click **"Manage Students"** tab
2. View all registered students
3. Click **"Delete"** to remove a student from the system

## File Structure

```
attendance-system/
├── run.py                    # Main application launcher
├── backend/
│   ├── app.py              # Flask backend server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html          # Web interface
│   ├── script.js           # Frontend logic
│   └── style.css           # Styling
├── student_photos/         # Storage for student photos
└── README.md              # This file
```

## Data Storage

### Files Created by the System:

- **student_photos/** - Folder containing registered student photos
- **attendance_logs.json** - Daily attendance records
- **face_encoder.pkl** - Pre-computed face embeddings (for faster matching)

All data is stored locally on your computer.

## Troubleshooting

### 🚫 Camera Not Working

**Problem**: "Camera access denied" message

**Solution**:
1. Check browser permissions (click camera icon in address bar)
2. Allow camera access for localhost
3. Try a different browser
4. Check if another app is using the camera

### ❌ Face Not Being Recognized

**Problem**: System says "Face not recognized"

**Solutions**:
- Ensure good lighting on the face
- Move closer to the camera
- Try a different angle (face should be front-facing)
- Register a new photo with better lighting
- Ensure face is completely visible (no partial faces)

### 🐌 Slow Performance

**Problem**: System is slow or lags

**Solutions**:
- First run downloads models (~350MB) - this is normal
- Close other applications to free up RAM
- Ensure internet connection is stable
- Check system disk space (need ~2GB)

### 📁 Can't Find Attendance Records

**Problem**: Attendance data lost

**Check these files exist:**
- `attendance_logs.json` (in attendance-system folder)
- `face_encoder.pkl` (in attendance-system folder)

If missing, they will be recreated when you register students again.

## Technical Details

### Face Recognition Technology

- **Model**: DeepFace with FaceNet embeddings
- **Matching Algorithm**: Cosine similarity (threshold: 0.5)
- **Face Detection**: Automatic with facial landmarks

### Backend Stack

- **Framework**: Flask 2.3.3
- **Face Recognition**: DeepFace 0.0.79
- **Image Processing**: OpenCV 4.8
- **Data Storage**: JSON (attendance), Pickle (embeddings)

### Frontend Stack

- **Language**: HTML5, CSS3, JavaScript
- **Media**: WebRTC for camera access
- **APIs**: RESTful Flask endpoints

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register_student` | POST | Register a new student |
| `/api/mark_attendance` | POST | Mark attendance for a student |
| `/api/get_attendance` | GET | Get daily attendance records |
| `/api/get_students` | GET | List all registered students |
| `/api/delete_student/<name>` | DELETE | Remove a student |

## Performance Tips

1. **Better Recognition**: Register students with multiple photos under different lighting
2. **Faster Processing**: Reduce video resolution in settings
3. **More Storage**: Regular attendance data gets large - backup old records

## Security Considerations

⚠️ **Important Security Notes**:

1. **Local Storage Only**: All data is stored locally - no cloud sync
2. **Face Data**: Photos and embeddings are stored on disk
3. **Network**: By default, server is accessible only on localhost
4. **Data Backup**: Manually backup `attendance_logs.json` and `student_photos/`

For production deployment, consider:
- Adding authentication (username/password)
- Using HTTPS instead of HTTP
- Implementing database (PostgreSQL, MongoDB)
- Adding data encryption

## Fixes Applied (v1.1)

✅ Fixed missing `deepface` dependency in requirements.txt  
✅ Fixed syntax error in Flask route definition  
✅ Improved camera initialization with better error handling  
✅ Simplified application startup process  
✅ Enhanced error messages and user feedback  
✅ Better date initialization for records tab  

## Known Limitations

- Single camera support only
- Real-time face detection works best with still faces
- Accuracy depends on lighting and image quality
- No multi-person recognition in single frame

## Future Enhancements

- [ ] Multiple face detection in single frame
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Admin login system
- [ ] Export attendance to Excel/CSV
- [ ] Biometric data encryption
- [ ] Mobile app integration
- [ ] Real-time notifications
- [ ] Attendance reports & analytics

## Support & Issues

If you encounter issues:

1. Check the terminal/console for error messages
2. Review the Troubleshooting section above
3. Ensure all dependencies are installed: `pip install -r backend/requirements.txt`
4. Restart the application and browser

## License

This project is for educational and institutional use.

---

**Last Updated**: May 2026  
**Version**: 1.1  
**Status**: Active Development
