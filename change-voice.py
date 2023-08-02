import pyttsx3

def change_voice():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Print available voices
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"{voice.id}: {voice.name}")

    # Change the voice (select a voice ID from the list above)
    selected_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    engine.setProperty('voice', selected_voice_id)

    # Say something with the new voice
    engine.say("Hello, I have a different voice now.")

    # Wait for the speech to be spoken
    engine.runAndWait()

if __name__ == "__main__":
    change_voice()
