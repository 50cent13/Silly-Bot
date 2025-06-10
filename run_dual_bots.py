
import subprocess
import threading
import time
import os

def run_python_bot():
    """Run the Python Discord bot"""
    print("Starting Python bot...")
    try:
        subprocess.run(["python3", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Python bot error: {e}")
    except KeyboardInterrupt:
        print("Python bot stopped by user")

def run_rust_bot():
    """Run the Rust Discord bot"""
    print("Starting Rust bot...")
    try:
        # Build and run the Rust bot
        subprocess.run(["cargo", "run"], cwd=".", check=True)
    except subprocess.CalledProcessError as e:
        print(f"Rust bot error: {e}")
    except KeyboardInterrupt:
        print("Rust bot stopped by user")

def main():
    print("Starting dual Discord bot system...")
    
    # Check if tokens are set
    if not os.getenv("BOT_TOKEN_PY"):
        print("Error: BOT_TOKEN_PY not found in environment!")
        return
    
    if not os.getenv("BOT_TOKEN_RS"):
        print("Error: BOT_TOKEN_RS not found in environment!")
        return
    
    # Create threads for both bots
    python_thread = threading.Thread(target=run_python_bot, daemon=True)
    rust_thread = threading.Thread(target=run_rust_bot, daemon=True)
    
    # Start both bots
    python_thread.start()
    time.sleep(2)  # Give Python bot a moment to start
    rust_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down both bots...")

if __name__ == "__main__":
    main()
