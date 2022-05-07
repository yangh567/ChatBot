#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import sys
import json
import time

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


def return_text(model, device_info):

    text = ""

    with sd.RawInputStream(samplerate=int(device_info['default_samplerate']), blocksize=8000, device=None,
                           dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, int(device_info['default_samplerate']))

        pre_time = time.time()
        timeout = time.time() + 50  # 5 second from now
        while True:
            print("listening...")
            # print("Passing time", time.time() - pre_time)
            data = q.get()
            if rec.AcceptWaveform(data):
                dict = json.loads(rec.Result())
                txt = dict["text"]
                text += (txt+".")
                print(txt)
            # else:
            #     dict = json.loads(rec.PartialResult())
            #     txt = dict["partial"]
            #  text += append(txt+".")

            if time.time() > timeout:
                print("Listening End")
                break
    return text




# txts = return_text()
#
#
# for txt in txts:
#     print(txt)