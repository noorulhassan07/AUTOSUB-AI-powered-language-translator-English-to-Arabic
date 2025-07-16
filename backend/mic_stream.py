import speech_recognition as sr
import queue
import os
import time

audio_queue = queue.Queue()

def mic_stream():
    print("🟢 mic_stream started")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("🎙️ Listening for speech...")

        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=3)
                
                # Save audio to a temporary file
                filename = f"temp_{int(time.time())}.wav"
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

                # Put file path in the queue
                audio_queue.put(filename)

            except Exception as e:
                print("Mic error:", e)
