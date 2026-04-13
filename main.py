import subprocess
import time
import sys

def main():
    print("Starting FastAPI Backend...")
    # Start the FastAPI backend via uvicorn
    # using subprocess.Popen so it runs in the background
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api:app", "--host", "localhost", "--port", "8001"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    # Give the backend a bit more time to load Langchain and models
    print("Waiting for backend to initialize (5s)...")
    time.sleep(5)

    print("\nStarting Streamlit Frontend...")
    # Start the Streamlit frontend
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    try:
        # Wait for both processes
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
