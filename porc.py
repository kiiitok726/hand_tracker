import pvporcupine
import sounddevice as sd
import numpy as np

porcupine = pvporcupine.create(keywords=["porcupine"])

print("Listening...")

def audio_callback(indata, frames, time, status):
    if status:
        print("Status:", status)

    pcm = (indata[:, 0] * 32768).astype(np.int16)
    result = porcupine.process(pcm)
    if result >= 0:
        print("Wake word detected!")

try:
    with sd.InputStream(
        samplerate=porcupine.sample_rate,
        channels=1,
        dtype='float32',
        blocksize=porcupine.frame_length,
        callback=audio_callback
    ):
        while True:
            pass

except KeyboardInterrupt:
    print("Stopping...")
finally:
    porcupine.delete()
