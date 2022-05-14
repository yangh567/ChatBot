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
    end_time = 0
    user_speak_dur = []
    print("listening...")
    while True:
        # Start collecting voice
        start_speak = time.time()
        data = stream.read(4096, exception_on_overflow=False)
        if len(data) > 0:
            if recognizer.AcceptWaveform(data):
                if end_time > 0:
                    print("User Paused: ", user_speak_dur[0] - end_time, "Seconds")
                txt = recognizer.Result()[14:-3]
                text += (txt + ".")
                print(txt)
                user_speak_dur = []
                end_time = time.time()
            else:
                dict = json.loads(recognizer.PartialResult())
                txts = str(dict["partial"])
                if txts != "" and txts !="the":
                    # print(txts)
                    start_time = time.time()
                    user_speak_dur.append(start_time)
        else:
            pass

        if keyboard.is_pressed("q"):
            print("Listening End\n")
            break

        if "finished" in text:
            print("Listening End\n")
            break

    return text

# model_speech = vosk.Model("model")
# device_info = sd.query_devices(None, 'input')
# model_speech = vosk.KaldiRecognizer(model_speech, int(device_info['default_samplerate']))
# return_text(model_speech, device_info)
