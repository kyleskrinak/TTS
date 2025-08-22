import os
import sys
import time
import subprocess
import requests

def animate_console(duration=2):
    """Animate the console for a given duration (default 2 seconds)."""
    end_time = time.time() + duration
    animation_chars = ['|', '/', '-', '\\']

    while time.time() < end_time:
        for char in animation_chars:
            sys.stdout.write(f'\rProcessing {char}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\rDone!            \n')  # clear the line after animation


def tts_macos(file_path):
    """Convert text from given file to speech on macOS using the `say` command."""
    
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Generate output filenames
    output_aiff = os.path.splitext(file_path)[0] + ".aiff"
    output_mp3 = os.path.splitext(file_path)[0] + ".mp3"
    output_done = os.path.splitext(file_path)[0] + ".done"
    
    # Check for empty file
    if os.path.getsize(file_path) == 0:
        print("Error: The provided file is empty.")
        return

    try:
        # Read the file content
        with open(file_path, 'r', encoding="utf-8") as f:
            content = f.read()

            # Replace paragraph breaks with the silence tag for a 1500ms (1.5 second) pause
            spoken_content = content.replace('\n\n', '[[slnc 1500]]')

            # Use the 'say' command to generate the aiff audio
            cmd_say = ['say', spoken_content, '-o', output_aiff]
            subprocess.run(cmd_say, check=True, text=True)

            # Convert aiff to high-quality mp3 using ffmpeg
            cmd_ffmpeg = ['ffmpeg', '-i', output_aiff, '-q:a', '0', output_mp3]
            subprocess.run(cmd_ffmpeg, check=True)

            # Remove the temporary aiff file
            os.remove(output_aiff)

            # Rename the text file to .done extension
            os.rename(file_path, output_done)

        # Animate the console while processing
        animate_console()
        print(f"Audio saved to {output_mp3}!")
        print(f"Text file renamed to {output_done}!")

    except Exception as e:
        print(f"Error: {e}")
    
# Example usage:

if __name__ == "__main__":
    # Check if the file path is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_text_file>")
    else:
        tts_macos(sys.argv[1])
