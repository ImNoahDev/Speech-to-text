import pvporcupine
import pyaudio
import struct
import wave

access_key = "API-KEY" # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
keyword_paths = ['./Wakeword.ppn']
porcupine = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)

# PyAudio configuration
p = pyaudio.PyAudio()
stream = p.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

def wakeword():
    print("Listening for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected!")
                return True

    except KeyboardInterrupt:
        print("Stopping wake word detection")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        porcupine.delete()





            
print(wakeword())

