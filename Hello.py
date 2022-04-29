import nltk
import speech_recognition as sr
# nltk.download('punkt')
# print("Hello world")


recognizer = sr.Recognizer()    # recognize the speech from audio source
mic = sr.Microphone()   # device_index=1   # sr.Microphone.list_microphone_names()
with mic as source:   # invoke microphone on the SR package with an alias named as source
    print('start speaking....')
    recognizer.pause_threshold = 0.5    #
    recognizer.adjust_for_ambient_noise(source)
    # recognizer.energy_threshold = 20000
    voice = recognizer.listen(source,timeout=8,phrase_time_limit=8) # recognizer.listen(source,timeout=8,phrase_time_limit=8) # recognizer.listen(source)
    # listen method on the recognizer instant will record as transcribes from source as long as user speaks
    try:
        query = recognizer.recognize_google(voice).lower()
        # passing the voice through Google search,or,bing,etc
        # also convert the transcribed text into lower case
        print('you said....', query)
    except Exception as ex:
        print('No clue what you said: An exception', ex)

