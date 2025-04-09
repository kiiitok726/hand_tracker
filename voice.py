import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Load Whisper model
model = whisper.load_model("base")

def record_audio(duration=3, fs=16000):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until recording finishes
    return recording.flatten()

def detect_wake_word(audio):
    # Save temporary audio file
    wav.write("temp.wav", 16000, (audio * 32767).astype(np.int16))

    # Transcribe audio using Whisper
    result = model.transcribe("temp.wav", fp16=False)
    transcription = result["text"].lower().strip()

    print(f"Transcribed Text: {transcription}")
    
    return "hello world" in transcription

def your_function():
    print("Wake word detected! Running your function...")

if __name__ == "__main__":
    while True:
        audio = record_audio(duration=3)
        if detect_wake_word(audio):
            your_function()