let video = null;
let registerVideo = null;
let capturedImage = null;
let currentStream = null;

const API_BASE_URL = 'http://127.0.0.1:5000';

let allStudents = [];
let allCourses = [];
let selectedCourses = [];
let editingCourseId = null;

window.addEventListener('DOMContentLoaded', () => {
    initializeCameras();
    initializeNavigation();
    loadStudentsList();
    loadCourses();
    setTodayDate();
    setupEventListeners();
});

function initializeNavigation() {
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            switchTab(tabName);
            
            navBtns.forEach(b => b.classList.remove('active', 'bg-primary-container/20', 'text-mint-green', 'scale-110', 'rounded-xl', 'px-3', 'py-1'));
            b.classList.add('text-on-surface-variant/70');
            
            btn.classList.add('active', 'bg-primary-container/20', 'text-mint-green', 'scale-110', 'rounded-xl', 'px-3', 'py-1');
        });
    });
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-pane').forEach(tab => {
        tab.classList.add('hidden');
        tab.classList.remove('active');
    });
    
    // Show selected tab
    const tabEl = document.getElementById(`${tabName}-tab`);
    if (tabEl) {
        tabEl.classList.remove('hidden');
        tabEl.classList.add('active');
    }
    
    if (tabName === 'records') {
        loadAttendanceRecords();
    } else if (tabName === 'manage') {
        loadStudentsList();
    } else if (tabName === 'admin') {
        loadCourses();
    } else if (tabName === 'stats') {
        loadStatistics();
    }
}

function setupEventListeners() {
    const searchInput = document.getElementById('student-search');
    if (searchInput) {
        searchInput.addEventListener('input', filterStudents);
    }
    
    const dateInput = document.getElementById('attendance-date');
    if (dateInput) {
        dateInput.addEventListener('change', loadAttendanceRecords);
    }
    
    const courseFilter = document.getElementById('records-course-filter');
    if (courseFilter) {
        courseFilter.addEventListener('change', loadAttendanceRecords);
    }
}

async function initializeCameras() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } }
        });
        currentStream = stream;
        
        const videoEl = document.getElementById('video');
        if (videoEl) {
            videoEl.srcObject = stream;
            videoEl.onloadedmetadata = () => videoEl.play();
        }
        
        const registerVideoEl = document.getElementById('register-video');
        if (registerVideoEl) {
            registerVideoEl.srcObject = stream;
            registerVideoEl.onloadedmetadata = () => registerVideoEl.play();
        }
        
        showResult('attendance-result', '✅ Camera ready', 'success');
    } catch (err) {
        console.error('Camera error:', err);
        const message = err.name === 'NotAllowedError'
            ? '❌ Camera permission denied'
            : '❌ Camera not available';
        showResult('attendance-result', message, 'error');
    }
}

function setTodayDate() {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('attendance-date');
    if (dateInput) {
        dateInput.value = today;
    }
}

async function captureAndMark() {
    const videoEl = document.getElementById('video');
    if (!videoEl || !videoEl.srcObject) {
        showResult('attendance-result', '❌ Camera not ready', 'error');
        return;
    }
    
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;
    context.drawImage(videoEl, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    
    showResult('attendance-result', '⏳ Processing face recognition...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/mark_attendance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        });
        
        const result = await response.json();
        
        if (result.success) {
            let message = '';
            result.recognized.forEach(student => {
                if (student.status === 'marked') {
                    message += `✅ ${student.name}: Marked present at ${student.time}<br>`;
                } else if (student.status === 'already_marked') {
                    message += `⚠️ ${student.name}: Already marked today<br>`;
                }
            });
            showResult('attendance-result', message || '✅ Attendance marked successfully!', 'success');
            loadRecentActivity();
        } else {
            showResult('attendance-result', '❌ ' + (result.error || 'Recognition failed'), 'error');
        }
    } catch (err) {
        console.error('Error:', err);
        showResult('attendance-result', '❌ Network error', 'error');
    }
}

async function loadRecentActivity() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/get_attendance`);
        const data = await response.json();
        
        const container = document.getElementById('recent-activity');
        let html = '';
        
        data.attendance.slice(0, 5).forEach(student => {
            if (student.status === 'present') {
                html += `
                    <div class="flex items-center gap-4 p-4 rounded-lg bg-glass-surface backdrop-blur-xl border border-glass-border glass-inner-glow hover:bg-surface-container-highest transition-colors duration-200">
                        <div class="relative">
                            <div class="w-12 h-12 rounded-full bg-surface-container-highest flex items-center justify-center border border-mint-green/30">
                                <span class="material-symbols-outlined text-mint-green">person</span>
                            </div>
                            <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-mint-green rounded-full border-2 border-surface flex items-center justify-center">
                                <span class="material-symbols-outlined text-[8px] text-surface font-bold">check</span>
                            </div>
                        </div>
                        <div class="flex-grow">
                            <p class="font-body-md font-semibold text-on-surface">${student.name}</p>
                            <p class="font-label-xs text-on-surface-variant/70 uppercase">${student.student_id || ''}</p>
                        </div>
                        <div class="text-right">
                            <p class="font-label-sm text-mint-green">${student.time || ''}</p>
                        </div>
                    </div>
                `;
            }
        });
        
        container.innerHTML = html || '<p class="text-center text-on-surface-variant/60">No recent activity</p>';
        
    } catch (err) {
        console.error('Error:', err);
    }
}

async function captureForRegistration() {
    const registerVideoEl = document.getElementById('register-video');
    if (!registerVideoEl || !registerVideoEl.srcObject) {
        showResult('register-result', '❌ Camera not ready', 'error');
        return;
    }
    
    const canvas = document.createElement('canvas');
    canvas.width = registerVideoEl.videoWidth;
    canvas.height = registerVideoEl.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(registerVideoEl, 0, 0, canvas.width, canvas.height);
    
    capturedImage = canvas.toDataURL('image/jpeg', 0.8);
    
    document.getElementById('register-btn').classList.remove('hidden');
    showResult('register-result', '✅ Photo captured!', 'success');
}

async function registerStudent() {
    const studentId = document.getElementById('student-id').value.trim();
    const name = document.getElementById('student-name').value.trim();
    const email = document.getElementById('student-email').value.trim();
    
    if (!studentId) {
        showResult('register-result', 'Please enter student ID', 'error');
        return;
    }
    if (!name) {
        showResult('register-result', 'Please enter student name', 'error');
        return;
    }
    if (!capturedImage) {
        showResult('register-result', 'Please capture a photo first', 'error');
        return;
    }
    
    showResult('register-result', 'Registering student...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/register_student`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: studentId,
                name: name,
                email: email,
                image: capturedImage,
                courses: selectedCourses
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showResult('register-result', `✅ ${result.message}`, 'success');
            document.getElementById('student-id').value = '';
            document.getElementById('student-name').value = '';
            document.getElementById('student-email').value = '';
            capturedImage = null;
            selectedCourses = [];
            document.getElementById('register-btn').classList.add('hidden');
            
            const checkboxes = document.querySelectorAll('#courses-checkboxes input[type="checkbox"]');
            checkboxes.forEach(cb => cb.checked = false);
            
            loadStudentsList();
        } else {
            showResult('register-result', `❌ ${result.error}`, 'error');
        }
    } catch (err) {
        console.error('Error:', err);
        showResult('register-result', 'Network error', 'error');
    }
}

async function loadAttendanceRecords() {
    const date = document.getElementById('attendance-date').value || new Date().toISOString().split('T')[0];
    const courseFilter = document.getElementById('records-course-filter').value;
    
    try {
        let url = `${API_BASE_URL}/api/get_attendance?date=${date}`;
        if (courseFilter) url += `&course_id=${courseFilter}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        const rateEl = document.getElementById('summary-rate');
        const presentEl = document.getElementById('summary-present');
        const absentEl = document.getElementById('summary-absent');
        
        const rate = data.total_students > 0 ? ((data.present_count / data.total_students) * 100).toFixed(1) : 0;
        rateEl.textContent = `${rate}%`;
        presentEl.textContent = data.present_count;
        absentEl.textContent = data.total_students - data.present_count;
        
        const container = document.getElementById('records-list');
        let html = '';
        
        data.attendance.forEach(student => {
            html += `
                <div class="glass-panel p-4 rounded-lg flex items-center gap-4 hover:bg-surface-container-highest transition-colors">
                    <div class="w-12 h-12 rounded-full bg-surface-container-highest flex items-center justify-center border border-glass-border">
                        <span class="material-symbols-outlined text-on-surface-variant">person</span>
                    </div>
                    <div class="flex-1 min-w-0">
                        <h4 class="font-body-md text-on-surface font-semibold truncate">${student.name}</h4>
                        <span class="font-label-sm text-label-sm text-on-surface-variant font-medium">${student.student_id || ''} • ${student.time || ''}</span>
                    </div>
                    <div class="px-3 py-1 rounded-full ${student.status === 'present' ? 'bg-secondary-container/20 border border-secondary-container/30' : 'bg-error-container/20 border border-error-container/30'}">
                        <span class="font-label-xs text-label-xs ${student.status === 'present' ? 'text-mint-green' : 'text-status-critical'} uppercase">${student.status}</span>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html || '<p class="text-center text-on-surface-variant/60">No records</p>';
        
    } catch (err) {
        console.error('Error:', err);
    }
}

async function loadStudentsList() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/get_students`);
        const data = await response.json();
        allStudents = data.students;
        displayStudents(allStudents);
    } catch (err) {
        console.error('Error:', err);
    }
}

function displayStudents(students) {
    const container = document.getElementById('students-list');
    let html = '';
    
    students.forEach(student => {
        html += `
            <div class="glass-card p-4 rounded-lg flex items-center gap-4 hover:scale-[1.02] active:opacity-80 active:scale-95 transition-all cursor-pointer">
                <div class="relative">
                    <div class="w-16 h-16 rounded-full bg-surface-container-highest flex items-center justify-center border-2 border-mint-green/30">
                        <span class="material-symbols-outlined text-mint-green text-2xl">person</span>
                    </div>
                    <div class="absolute bottom-0 right-0 w-4 h-4 bg-mint-green border-2 border-surface rounded-full"></div>
                </div>
                <div class="flex-grow">
                    <h3 class="font-headline-md text-[18px] text-on-surface">${student.name}</h3>
                    <p class="font-label-sm text-label-sm text-on-surface-variant/70">${student.student_id || ''}</p>
                </div>
                <span class="material-symbols-outlined text-on-surface-variant/40">chevron_right</span>
            </div>
        `;
    });
    
    if (html === '') {
        html = '<p class="text-center text-on-surface-variant/60 py-8">No students registered</p>';
    }
    
    container.innerHTML = html;
}

function filterStudents() {
    const searchTerm = document.getElementById('student-search').value.toLowerCase();
    const filtered = allStudents.filter(student =>
        student.name.toLowerCase().includes(searchTerm) ||
        (student.student_id && student.student_id.toLowerCase().includes(searchTerm))
    );
    displayStudents(filtered);
}

function showCourseForm() {
    editingCourseId = null;
    document.getElementById('form-title').textContent = 'Add New Course';
    document.getElementById('course-name').value = '';
    document.getElementById('course-code').value = '';
    document.getElementById('course-instructor').value = '';
    document.getElementById('course-form').classList.remove('hidden');
}

function cancelCourseForm() {
    document.getElementById('course-form').classList.add('hidden');
}

async function loadCourses() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses`);
        const data = await response.json();
        allCourses = data.courses;
        displayCoursesForRegistration();
        displayCoursesInAdmin();
        populateCourseFilters();
    } catch (err) {
        console.error('Error loading courses:', err);
    }
}

function populateCourseFilters() {
    const recordsFilter = document.getElementById('records-course-filter');
    if (recordsFilter) {
        recordsFilter.innerHTML = '<option value="">All Courses</option>';
        allCourses.forEach(course => {
            recordsFilter.innerHTML += `<option value="${course.id}">${course.name} (${course.code})</option>`;
        });
    }
}

function displayCoursesForRegistration() {
    const container = document.getElementById('courses-checkboxes');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (allCourses.length === 0) {
        container.innerHTML = '<p class="text-on-surface-variant/60">No courses available</p>';
        return;
    }
    
    allCourses.forEach(course => {
        const div = document.createElement('div');
        div.className = 'flex items-center gap-3 p-2 rounded-lg hover:bg-surface-container-low';
        div.innerHTML = `
            <input type="checkbox" id="course-${course.id}" value="${course.id}" class="w-4 h-4 text-mint-green bg-surface-container border-glass-border focus:ring-mint-green">
            <label for="course-${course.id}" class="flex-grow cursor-pointer">
                <span class="text-on-surface font-body-md">${course.name}</span>
                <span class="text-on-surface-variant/70 font-label-sm ml-2">${course.code}</span>
            </label>
        `;
        
        const checkbox = div.querySelector('input');
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                if (!selectedCourses.includes(course.id)) {
                    selectedCourses.push(course.id);
                }
            } else {
                selectedCourses = selectedCourses.filter(id => id !== course.id);
            }
        });
        
        container.appendChild(div);
    });
}

function displayCoursesInAdmin() {
    const container = document.getElementById('courses-list');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (allCourses.length === 0) {
        container.innerHTML = '<p class="text-center text-on-surface-variant/60 py-8">No courses yet</p>';
        return;
    }
    
    allCourses.forEach(course => {
        const div = document.createElement('div');
        div.className = 'glass-card p-4 rounded-lg mb-3';
        div.innerHTML = `
            <h4 class="font-headline-md text-on-surface">${course.name}</h4>
            <p class="text-on-surface-variant/70 font-label-sm"><strong>Code:</strong> ${course.code}</p>
            <p class="text-on-surface-variant/70 font-label-sm"><strong>Instructor:</strong> ${course.instructor || 'Not assigned'}</p>
        `;
        container.appendChild(div);
    });
}

async function saveCourse() {
    const name = document.getElementById('course-name').value.trim();
    const code = document.getElementById('course-code').value.trim();
    const instructor = document.getElementById('course-instructor').value.trim();
    
    if (!name || !code) {
        alert('Course name and code are required');
        return;
    }
    
    const courseData = { name, code, instructor, timetable: [] };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(courseData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            cancelCourseForm();
            loadCourses();
        } else {
            alert(result.error);
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Network error');
    }
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/statistics`);
        const data = await response.json();
        
        const overallEl = document.getElementById('stat-overall');
        const presentEl = document.getElementById('stat-present');
        const absentEl = document.getElementById('stat-absent');
        const topCourseEl = document.getElementById('stat-top');
        const rankingContainer = document.getElementById('stat-ranking');
        
        overallEl.textContent = `${data.overall_rate}%`;
        presentEl.textContent = data.total_present;
        absentEl.textContent = data.total_absent;
        topCourseEl.textContent = data.top_course || 'N/A';
        
        let rankingHtml = '';
        data.student_ranking.slice(0, 5).forEach((student, index) => {
            const medal = index < 3 ? ['🥇', '🥈', '🥉'][index] : '';
            rankingHtml += `
                <div class="flex items-center justify-between p-3 glass-card rounded-lg mb-2">
                    <div class="flex items-center gap-3">
                        <span class="text-lg font-bold text-on-surface-variant">${index + 1}</span>
                        <span class="text-on-surface font-semibold">${medal} ${student.name}</span>
                    </div>
                    <span class="font-headline-md text-mint-green">${student.rate}%</span>
                </div>
            `;
        });
        
        rankingContainer.innerHTML = rankingHtml;
        
    } catch (err) {
        console.error('Error loading statistics:', err);
    }
}

function showResult(elementId, message, type) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.innerHTML = message;
    if (type === 'error') {
        element.className = 'p-4 rounded-lg bg-error-container/20 border border-error-container/30 text-error';
    } else if (type === 'success') {
        element.className = 'p-4 rounded-lg bg-glass-surface backdrop-blur-xl border border-glass-border glass-inner-glow';
    } else if (type === 'info') {
        element.className = 'p-4 rounded-lg bg-surface-container-low border border-glass-border';
    }
}
