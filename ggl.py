import speech_recognition as sr

# Define the wake word
WAKE_WORD = "juicy"

# Initialize the recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

print("Calibrating microphone for ambient noise. Please wait...")
with mic as source:
    r.adjust_for_ambient_noise(source, duration=2)
print("Calibration complete. Listening for the wake word...")

# Continuous listening loop
while True:
    try:
        with mic as source:
            # Listen for audio input
            audio = r.listen(source)
        # Convert the captured audio to text using Google's speech recognition
        text = r.recognize_google(audio)
        print("Heard:", text)
        # Check if the wake word is present in the recognized text
        if WAKE_WORD.lower() in text.lower():
            print("wake word detected")
    except sr.UnknownValueError:
        # Speech was unintelligible
        print("Could not understand audio")
    except sr.RequestError as e:
        # Handle API errors (like connection issues)
        print(f"Could not request results; {e}")
