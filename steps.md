# 1. Create project folder
mkdir attendance-system
cd attendance-system

# 2. Create all the files above in their respective folders
mkdir backend frontend student_photos

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install dlib (required for face_recognition)
# On Windows:
pip install dlib-bin
# On Mac:
brew install dlib
pip install dlib
# On Linux:
sudo apt-get install build-essential cmake
pip install dlib

# 5. Run the application
python run.py