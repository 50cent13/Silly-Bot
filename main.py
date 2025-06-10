import os
import time
import threading
from dotenv import load_dotenv

load_dotenv()

def python_bot():
    """Simple Python bot that writes to shared file"""
    print("Python bot started. Sending periodic messages...")

    counter = 1
    while True:
        try:
            message = f"Python bot message #{counter} at {time.strftime('%H:%M:%S')}"

            # Write to shared file
            with open("shared.txt", "w") as f:
                f.write(message)

            print(f"Python bot sent: {message}")
            counter += 1

            # Wait a bit, then check for Rust response
            time.sleep(3)

            # Read Rust response
            try:
                with open("shared.txt", "r") as f:
                    response = f.read()
                    if response.startswith("Rust bot processed:"):
                        print(f"Python bot received: {response}")
                        # Clear the file for next cycle
                        with open("shared.txt", "w") as f:
                            f.write("")
            except FileNotFoundError:
                pass

            time.sleep(5)  # Wait before next message

        except Exception as e:
            print(f"Python bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    python_bot()