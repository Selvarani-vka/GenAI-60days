import os
import sys
from datetime import datetime

def write_input(text):
    filename = "notes.txt"
    file_path = os.path.join(os.getcwd(), filename)

    # Prepare timestamped entry (optional)
    timestamp = datetime.now().strftime("%d-%m-%Y::%H-%M-%S")
    entry = f"{timestamp} - {text}\n"

    # Append or create file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python date_input.py "your text here"')
        sys.exit(1)

    user_text = sys.argv[1]
    write_input(user_text)
    print("Input saved successfully!")
