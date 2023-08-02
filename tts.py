import os
import pyttsx3
import sys
import time
import threading

def text_to_speech_from_file(input_file, progress_event):
    try:
        input_file = os.path.abspath(input_file)

        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read().replace('\n', ' ')

        # Initialize the text-to-speech engine
        engine = pyttsx3.init()

        # Set properties (optional)
        # engine.setProperty('rate', 150)  # Speed of speech
        # engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

        # Get the filename without extension
        filename_base = os.path.splitext(input_file)[0]

        # Create the final output file
        output_file = f"{filename_base}.mp3"

        # Save the speech as an MP3 file
        engine.save_to_file(text, output_file)

        # Wait for the speech to be saved
        engine.runAndWait()

        print(f'\nSuccess! The speech has been saved as {output_file}')

        # Set the progress event to notify the main thread that speech creation is complete
        progress_event.set()

    except Exception as e:
        print("\nError:", e)

def track_progress(output_file, progress_event):
    # Get the initial file size
    file_size = 0

    while not progress_event.is_set():
        try:
            # Get the updated size of the MP3 file
            new_file_size = os.path.getsize(output_file)
        except FileNotFoundError:
            # Wait for the file to be created if not found (yet)
            time.sleep(0.1)
            continue

        if new_file_size != file_size:
            file_size = new_file_size
            # Move the cursor back to the start of the line after printing 'Creating speech...'
            sys.stdout.write('\r')
            # Print the growing file size in bytes
            sys.stdout.write(f"Creating speech... {file_size} bytes")
            sys.stdout.flush()

        # Wait for a short period to avoid excessive updates
        time.sleep(0.1)

    # Move the cursor to the next line after the progress update
    sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == "__main__":
    try:
        input_file = input("Enter the path to the input text file: ")

        # Normalize the file path for the current OS
        input_file = os.path.normpath(input_file)

        # Check if the input file exists
        if not os.path.exists(input_file):
            print("Error: Input file not found.")
        else:
            print("Creating speech... ", end='', flush=True)

            # Create an event to signal progress completion
            progress_event = threading.Event()

            # Start the thread for tracking progress
            output_file = f"{os.path.splitext(input_file)[0]}.mp3"
            progress_thread = threading.Thread(target=track_progress, args=(output_file, progress_event))
            progress_thread.start()

            # Start the thread for text-to-speech conversion
            speech_thread = threading.Thread(target=text_to_speech_from_file, args=(input_file, progress_event))
            speech_thread.start()

            # Wait for both threads to complete
            speech_thread.join()
            progress_thread.join()

            print("Speech creation completed!")

    except Exception as e:
        print("\nError:", e)