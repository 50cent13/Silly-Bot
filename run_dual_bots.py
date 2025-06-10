
import subprocess
import threading
import time
import os

def run_python_bot():
    """Run the Python Discord bot"""
    print("Starting Python Discord bot...")
    try:
        subprocess.run(["python3", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Python bot error: {e}")
    except KeyboardInterrupt:
        print("Python bot stopped by user")

def run_rust_bot():
    """Run the Rust Discord bot"""
    print("Starting Rust Discord bot...")
    try:
        # Set up Rust environment
        env = os.environ.copy()
        env["PATH"] = f"{os.path.expanduser('~/.cargo/bin')}:{env.get('PATH', '')}"
        subprocess.run(["cargo", "run"], cwd=".", check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Rust bot error: {e}")
    except FileNotFoundError:
        print("Cargo not found. Please install Rust first.")
    except KeyboardInterrupt:
        print("Rust bot stopped by user")

def main():
    print("Starting dual Discord bot system...")
    print("Make sure you have set BOT_TOKEN_PY and BOT_TOKEN_RS in Secrets!")
    
    # Create shared file if it doesn't exist
    if not os.path.exists("shared.txt"):
        with open("shared.txt", "w") as f:
            f.write("")
    
    # Create threads for both bots
    python_thread = threading.Thread(target=run_python_bot, daemon=True)
    rust_thread = threading.Thread(target=run_rust_bot, daemon=True)
    
    # Start both bots
    python_thread.start()
    time.sleep(3)  # Give Python bot a moment to start
    rust_thread.start()
    
    try:
        print("\nBoth bots are starting up...")
        print("Available commands:")
        print("Python bot: !ping, !check_rust, !dual_status, !hello")
        print("Rust bot: !rust_ping, !check_python")
        print("\nPress Ctrl+C to stop both bots")
        
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down both bots...")

if __name__ == "__main__":
    main()
