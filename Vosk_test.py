#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import sys
import json
import time
import keyboard
import pyaudio

q = queue.Queue()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

    # def return_text(model, device_info):
    #
    #     text = ""
    #
    #     with sd.RawInputStream(samplerate=int(device_info['default_samplerate']), blocksize=8000, device=None,
    #                            dtype='int16',
    #                            channels=1, callback=callback):
    #         rec = vosk.KaldiRecognizer(model, int(device_info['default_samplerate']))
    #
    #         pre_time = time.time()
    #         timeout = time.time() + 50  # 5 second from now
    #         print("listening...")
    #         while True:
    #             # print("Passing time", time.time() - pre_time)
    #             data = q.get()
    #             # if len(data) == 0:
    #             #     break
    #             if rec.AcceptWaveform(data):
    #                 dict = json.loads(rec.Result())
    #                 txt = dict["text"]
    #                 text += (txt+".")
    #                 print(txt)
    #             # else:
    #             #     dict = json.loads(rec.PartialResult())
    #             #     txt = dict["partial"]
    #             #  text += append(txt+".")
    #
    #             if time.time() > timeout:
    #                 print("Listening End")
    #                 break
    #
    #             if keyboard.is_pressed("q"):
    #                 print("Listening End")
    #                 break
    #         return text
    #         # return text
    #     # except '':
    #     #     print('\nDone')
    #     #     return text
    #     # except Exception as e:
    #     #     print("Fine")


# User pause time = (time when machine hears user's new speaking - time of the end of last speak accepted as
# waveform) - time when machine try to recognize user new speaking)
def return_text(model, device_info):
    text = ""
    recognizer = model
    cap = pyaudio.PyAudio()
    stream = cap.open(format=pyaudio.paInt16, channels=1, rate=int(device_info['default_samplerate']), input=True,
                      frames_per_buffer=8192)
    stream.start_stream()
    # rec = vosk.KaldiRecognizer(model, int(device_info['default_samplerate']))
    # timeout = time.time() + 50  # 5 second from now
    print("listening...")
    end_time = 0
    pause_time = 0
    while True:

        # Start collecting voice
        start_time = time.time()
        if end_time != 0:
            # user pause time is the time duration between finished speaking and next expected voice
            # (user suppose to speak, but, not yet).

            # (the next expected voice time will not be capture when user speak, instead,
            # the time will be captured after machine recognize user's new speak)
            pause_time = start_time - end_time

        data = stream.read(4096, exception_on_overflow=False)
        start_recognize = time.time()

        # if the speak is done within 10 seconds and accepted
        if pause_time < 10 and recognizer.AcceptWaveform(data) and len(data) > 0:
            txt = recognizer.Result()[14:-3]
            text += (txt + ".")
            print(txt)
            end_recognize = time.time()
            # if he/she delivered expected speak, then, we need to strip off the time that machine listens and predicts
            time_for_recognize = end_recognize - start_recognize
            end_time = time.time()
            if pause_time != 0:
                real_pause_time = pause_time - time_for_recognize
                # print out the real time duration user spent before speaking
                print("User Paused: ", real_pause_time, "Seconds")
        # else:
        #     # dict = json.loads(recognizer.PartialResult())
        #     # txt = dict["partial"]
        #     continue
        # if user pause more than 10 second and nothing detected (haven't deliver supposed speak), break
        if pause_time >= 10:
            if not recognizer.AcceptWaveform(data):
                print("Exceeded time limit for waiting for you to speak")
                break

        if keyboard.is_pressed("q"):
            print("Listening End\n")
            break

        if "finished" in text:
            break

    return text

# model_speech = vosk.Model("model")
# device_info = sd.query_devices(None, 'input')
# model_speech = vosk.KaldiRecognizer(model_speech, int(device_info['default_samplerate']))
# return_text(model_speech, device_info)
