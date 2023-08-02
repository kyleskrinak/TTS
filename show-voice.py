import pyttsx3

def get_available_voices():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Get the list of available voices
    voices = engine.getProperty('voices')
    
    # Print the voice details
    for voice in voices:
        print(f"ID: {voice.id}")
        print(f"Name: {voice.name}")
        print(f"Languages: {voice.languages}")
        print(f"Gender: {voice.gender}")
        print(f"Age: {voice.age}")
        print("\n")

if __name__ == "__main__":
    get_available_voices()