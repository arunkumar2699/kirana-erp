# scripts/run_dev.py
"""
Script to run both backend and frontend in development mode
"""
import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_backend():
    """Run the FastAPI backend"""
    print("Starting backend server...")
    os.chdir("backend")
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"])

def run_frontend():
    """Run the React frontend"""
    print("Starting frontend server...")
    os.chdir("frontend")
    subprocess.run(["npm", "start"], shell=True)

def open_browser():
    """Open browser after servers start"""
    time.sleep(5)  # Wait for servers to start
    webbrowser.open("http://localhost:3000")

if __name__ == "__main__":
    # Change to project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Start backend in a thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Open browser
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run frontend in main thread
    run_frontend()