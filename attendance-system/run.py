#!/usr/bin/env python3
import os
import sys
import subprocess

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Face Recognition Attendance System")
    print("="*60)
    print("\n📋 System Information:")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Directory: {os.getcwd()}")
    
    print("\n💡 Quick Start Guide:")
    print("   1. Go to 'Register Student' tab")
    print("   2. Take a clear photo of a student")
    print("   3. Enter their name and click Register")
    print("   4. Switch to 'Mark Attendance' tab")
    print("   5. Student looks at camera and clicks 'Mark Attendance'")
    
    print("\n⚠️  Important Notes:")
    print("   • Ensure faces are well-lit and clearly visible")
    print("   • First startup may take longer (model download)")
    print("   • Allow camera permissions when prompted")
    
    print("\n" + "="*60)
    print("✅ Starting server...")
    print("📱 Open your browser: http://localhost:5000")
    print("="*60 + "\n")
    
    # Run the Flask app directly from backend
    sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
    from app import app, load_data
    
    load_data()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)