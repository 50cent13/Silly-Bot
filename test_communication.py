
import time
import os

def test_file_communication():
    """Test the shared file communication system"""
    print("Testing file communication system...")
    
    
    test_message = "Test message from communication test"
    with open("shared.txt", "w") as f:
        f.write(test_message)
    print(f"✓ Wrote test message: {test_message}")
    
    
    with open("shared.txt", "r") as f:
        read_message = f.read()
    
    if read_message == test_message:
        print("✓ Read message successfully")
    else:
        print(f"✗ Message mismatch. Expected: {test_message}, Got: {read_message}")
    
    
    with open("shared.txt", "w") as f:
        f.write("")
    print("✓ Cleared shared file")
    
    
    with open("shared.txt", "r") as f:
        content = f.read()
    
    if content == "":
        print("✓ File is properly cleared")
    else:
        print(f"✗ File not empty: {content}")
    
    print("\nFile communication test completed!")

if __name__ == "__main__":
    test_file_communication()
