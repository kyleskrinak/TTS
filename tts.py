import os
from gtts import gTTS
import time
import threading
import itertools

# Animation function to show progress in the console
def animate():
    """Create console animation"""
    for c in itertools.cycle(['|', '/', '-', '\\']):  # Loop through the characters for animation
        if done:  # Stop if the conversion is done
            break
        print(f'\rConverting text to speech... {c}', end='', flush=True)  # Print the animation character
        time.sleep(0.1)

def main():
    # Prompt the user for the text file's name
    file_name = input("Enter the name of the text file (with extension): ")

    # Check if the file exists and print an error if not
    if not os.path.isfile(file_name):
        print(f"No such file: {file_name}")
        return

    # Try to open the file with UTF-8 encoding
    try:
        # Open the file and read the content, normalizing line endings
        with open(file_name, 'r', encoding='utf-8', newline=None) as f:
            data = f.read()
    except UnicodeDecodeError:
        print("Error reading the file. Please ensure the file is encoded in UTF-8 or another supported encoding.")
        return

    # If the file is empty, abort the conversion
    if not data.strip():
        print("The file is empty. Aborting conversion.")
        return

    # Replace newline characters to insert pauses
    # Double newlines become a pause; single newlines become a space
    data = data.replace("\n\n", "||pause||").replace("\n", " ").replace("||pause||", "\n\n")

    # Create the output filename by replacing the extension with .mp3
    base_name = os.path.splitext(file_name)[0]
    output_file_name = f"{base_name}.mp3"

    # Global variable to control the animation thread
    global done
    done = False

    # Start the animation thread
    t = threading.Thread(target=animate)
    t.start()

    # Convert the text to speech and save the result
    speech = gTTS(text=data, lang='en')
    speech.save(output_file_name)

    # Stop the animation thread
    done = True

    # Print a completion message with the output file name
    print(f"\rConversion completed! Audio file saved as {output_file_name}.")

if __name__ == "__main__":
    main()