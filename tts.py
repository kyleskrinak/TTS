import os
from gtts import gTTS
import time
import threading
import itertools

def animate():
    """Create console animation"""
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        print(f'\rConverting text to speech... {c}', end='', flush=True)
        time.sleep(0.1)

def main():
    # Get the file name
    file_name = input("Enter the name of the text file (with extension): ")

    # Check if the file exists
    if not os.path.isfile(file_name):
        print(f"No such file: {file_name}")
        return

    try:
        # Open the file and read the content, normalizing line endings
        with open(file_name, 'r', encoding='utf-8', newline=None) as f:
            data = f.read()
    except UnicodeDecodeError:
        print("Error reading the file. Please ensure the file is encoded in UTF-8 or another supported encoding.")
        return

    # If the file is empty, abort conversion
    if not data.strip():
        print("The file is empty. Aborting conversion.")
        return

    # Replace single newline characters with spaces and double newline characters with a string to represent a pause
    data = data.replace("\n\n", "||pause||").replace("\n", " ").replace("||pause||", "\n\n")

    # Prepare the output file name
    base_name = os.path.splitext(file_name)[0]
    output_file_name = f"{base_name}.mp3"

    # Start console animation
    global done
    done = False
    t = threading.Thread(target=animate)
    t.start()

    # Convert text to speech
    speech = gTTS(text=data, lang='en')
    speech.save(output_file_name)

    # Stop console animation
    done = True

    print(f"\rConversion completed! Audio file saved as {output_file_name}.")

if __name__ == "__main__":
    main()
