import os
import sys
import subprocess
import time
import webbrowser
import signal
import json
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    # Check Python dependencies
    backend_requirements = Path("backend/requirements.txt").read_text().splitlines()
    backend_requirements = [req.split("==")[0] for req in backend_requirements if req and not req.startswith("#")]
    
    missing_python_deps = []
    for req in backend_requirements:
        try:
            __import__(req.replace("-", "_"))
        except ImportError:
            missing_python_deps.append(req)
    
    if missing_python_deps:
        print("Missing Python dependencies:")
        for dep in missing_python_deps:
            print(f"  - {dep}")
        print("\nInstalling missing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
    
    # Check if Node.js is installed
    try:
        subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Node.js is not installed or not in PATH. Please install Node.js to run the frontend.")
        sys.exit(1)
    
    # Check if npm is installed
    try:
        subprocess.run(["npm", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("npm is not installed or not in PATH. Please install npm to run the frontend.")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path("backend/.env")
    example_path = Path("backend/.env.example")
    
    if not env_path.exists() and example_path.exists():
        print("Creating .env file from .env.example...")
        env_content = example_path.read_text()
        # Replace the API key placeholder with the actual key
        env_content = env_content.replace("your_google_api_key_here", "AIzaSyDh_bB29TU_ge26Pke-E9LkOrQviWw6Ryo")
        env_path.write_text(env_content)
        print("Created .env file with API key")

def process_sample_data():
    """Process the sample data and load it into the vector database"""
    from scripts.test_rag import load_sample_data
    from backend.app.services.rag_service import RAGService
    import asyncio
    
    async def load_data():
        print("Loading sample data...")
        documents = load_sample_data()
        print(f"Loaded {len(documents)} documents from sample data")
        
        rag_service = RAGService()
        await rag_service.load_documents(documents)
        print("Sample data loaded into vector database")
    
    asyncio.run(load_data())

def run_backend():
    """Run the backend server"""
    os.chdir("backend")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

def run_frontend():
    """Run the frontend development server"""
    os.chdir("frontend")
    # Check if node_modules exists, if not run npm install
    if not os.path.exists("node_modules"):
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=True)
    
    return subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

def main():
    """Main function to run the application"""
    # Store the original directory
    original_dir = os.getcwd()
    
    try:
        print("Starting College Chatbot application...")
        
        # Check dependencies
        print("Checking dependencies...")
        check_dependencies()
        
        # Create .env file if it doesn't exist
        create_env_file()
        
        # Process sample data
        process_sample_data()
        
        # Start the backend server
        print("Starting backend server...")
        os.chdir(original_dir)  # Reset directory
        backend_process = run_backend()
        
        # Give the backend some time to start
        time.sleep(2)
        
        # Start the frontend server
        print("Starting frontend server...")
        os.chdir(original_dir)  # Reset directory
        frontend_process = run_frontend()
        
        # Open the browser
        print("Opening browser...")
        webbrowser.open("http://localhost:3000")
        
        print("\nCollege Chatbot is running!")
        print("Backend: http://localhost:8000")
        print("Frontend: http://localhost:3000")
        print("\nPress Ctrl+C to stop the application")
        
        # Monitor the processes and print their output
        while True:
            backend_line = backend_process.stdout.readline()
            if backend_line:
                print(f"[Backend] {backend_line.strip()}")
            
            frontend_line = frontend_process.stdout.readline()
            if frontend_line:
                print(f"[Frontend] {frontend_line.strip()}")
            
            # Check if processes are still running
            if backend_process.poll() is not None and frontend_process.poll() is not None:
                print("Both processes have terminated. Exiting...")
                break
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    finally:
        # Clean up processes
        os.chdir(original_dir)  # Reset directory
        
        try:
            if 'backend_process' in locals():
                backend_process.terminate()
                backend_process.wait(timeout=5)
        except:
            pass
        
        try:
            if 'frontend_process' in locals():
                frontend_process.terminate()
                frontend_process.wait(timeout=5)
        except:
            pass
        
        print("Application stopped")

if __name__ == "__main__":
    main()
