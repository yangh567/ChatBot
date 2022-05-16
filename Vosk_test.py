#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import os
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
    user_not_speaking_duration = []
    unaccept_time = []
    user_not_speaking_but_accepting_empty_str = 0
    print("listening...")
    while True:
        # Start collecting voice
        data = stream.read(4096, exception_on_overflow=False)
        # if data is there
        if len(data) > 0:
            # if it is recognized as waveform
            if recognizer.AcceptWaveform(data):
                # if it is not first time user speak
                if end_time > 0:
                    # if the first letter of spoken word is noise or empty string,
                    # it means that user did not speak,
                    # so calculate the duration between showing of this noise and last properly spoken word's time
                    # if the duration is greater than 10 seconds, break
                    if len(user_speak_dur) == 0:
                        user_not_speaking_duration.append(time.time())
                        user_not_speaking_but_accepting_empty_str = user_not_speaking_duration[-1] - user_not_speaking_duration[0]
                        # print("User empty Paused: ", user_not_speaking_but_accepting_empty_str, "Seconds")
                    # else, it means that user has speaked something properly
                    # print out the word user says
                    # update the last last properly speaked word's time
                    # remove the time when the first letter of this word/sentence is spoken
                    else:
                        print("User Paused: ", user_speak_dur[0] - end_time, "Seconds")
                        txt = recognizer.Result()[14:-3]
                        text += (txt + ".")
                        # print(txt)
                        user_speak_dur = []
                        end_time = time.time()
                        user_not_speaking_duration.append(end_time)

                # if it is first time user speak
                else:
                    # if there is no letter in list, means the noise is accepted as waveform, just pass
                    if len(user_speak_dur) == 0:
                        # print("empty string and 'the' accepted as waveform")
                        # print("Accepted", recognizer.Result()[14:-3])
                        pass
                    # if user spoke something, print out what user said.
                    # update the last last properly spoken word's time
                    # remove the time when the first letter of this word/sentence is spoken
                    else:
                        txt = recognizer.Result()[14:-3]
                        text += (txt + ".")
                        # print(txt)
                        user_speak_dur = []
                        end_time = time.time()
            else:
                dict = json.loads(recognizer.PartialResult())
                txts = str(dict["partial"])
                # when text is not waveform and are empty string and "the" (ambient noise)
                # That means this is the start alpha of a word. Then, record the time when received it
                if txts != "" and txts !="the":
                    os.system("cls")
                    print(txts)
                    start_time = time.time()
                    user_speak_dur.append(start_time)
                    user_not_speaking_duration = []
                # Otherwise, user did not speak (there are noises) and thus if user have already spoken once,
                # then record the time when noises is going in background
                # if the noise is lasting longer than 10 seconds after last properly ended word's time
                # break
                else:
                    if end_time > 0:
                        unaccept_time.append(time.time())
                        user_not_speaking_but_accepting_empty_str = unaccept_time[-1] - end_time
                    # print("not accepted", txts)
                    pass
        # if no data, keep listening
        else:
            pass

        if user_not_speaking_but_accepting_empty_str >= 10:
            print(user_not_speaking_but_accepting_empty_str)
            break

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
