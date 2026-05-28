# Installation & Setup Guide

## Windows Setup

### 1. Check Python Installation

Open Command Prompt and run:
```bash
python --version
```

If not installed, download from https://www.python.org (version 3.8+)

**During installation, check: ✓ Add Python to PATH**

### 2. Navigate to Project

```bash
cd C:\Users\YourUsername\OneDrive\Documents\facial rec\attendance-system
```

### 3. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

⏳ **First installation will take 5-10 minutes** (downloading DeepFace models)

### 5. Run Application

```bash
python run.py
```

### 6. Open Browser

Navigate to: http://localhost:5000

---

## macOS Setup

### 1. Check Python

```bash
python3 --version
```

### 2. Navigate to Project

```bash
cd ~/Documents/facial\ rec/attendance-system
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Run Application

```bash
python3 run.py
```

### 6. Open Browser

Navigate to: http://localhost:5000

---

## Linux Setup

### 1. Install Python and Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip libsm6 libxext6
```

### 2. Navigate to Project

```bash
cd ~/Documents/facial\ rec/attendance-system
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Run Application

```bash
python3 run.py
```

### 6. Open Browser

Navigate to: http://localhost:5000

---

## Troubleshooting Installation

### Issue: "pip: command not found"

**Solution**: Python is not in PATH. Reinstall Python and check "Add Python to PATH"

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution**: Dependencies not installed properly
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Issue: "No module named 'deepface'"

**Solution**: Specific DeepFace installation
```bash
pip install deepface==0.0.79
```

### Issue: "ImportError: No module named 'cv2'"

**Solution**: OpenCV not installed
```bash
pip install opencv-python==4.8.1.78
```

### Issue: Application won't start

**Solutions**:
1. Kill any existing Flask process:
   - Windows: `taskkill /IM python.exe /F`
   - macOS/Linux: `lsof -ti:5000 | xargs kill -9`

2. Check port 5000 is free:
   - Windows: `netstat -ano | findstr :5000`
   - macOS/Linux: `lsof -i :5000`

3. Try different port in code: Change `port=5000` to `port=5001` in `run.py`

---

## First Run Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Camera/Webcam is connected and working
- [ ] Browser is updated (Chrome, Firefox, Edge, Safari)
- [ ] Firewall allows localhost connection
- [ ] Adequate disk space (~2GB)

## Getting Help

1. **Check error messages** - Terminal output often shows exact issue
2. **Camera permissions** - Browser may need permission (check address bar)
3. **Restart everything** - Close browser, stop server, restart
4. **Check README.md** - Comprehensive troubleshooting guide included

---

**Ready to go!** Start with `python run.py` and open http://localhost:5000
