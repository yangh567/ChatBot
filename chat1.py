import random
import json
import torch
import csv
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import speech_recognition as sr
import pyttsx3         # text to speech conversion library
# import nltk

engine = pyttsx3.init()      # this loads a speech engine driver
voices = engine.getProperty('voices')    # grab the current value of the engine property: voices
engine.setProperty('voice', voices[0].id)   # this sets female voice... for male voice, set the index to
engine.setProperty('rate', 140)

def input_query():     # function to accept a command from the user
    recognizer = sr.Recognizer()    # recognize the speech from audio source
    mic = sr.Microphone()   # device_index=1   # sr.Microphone.list_microphone_names()
    with mic as source:   # invoke microphone on the SR package with an alias named as source
        print('start speaking....')
        # recognizer.pause_threshold = 0.5    #
        recognizer.adjust_for_ambient_noise(source)
        voice = recognizer.listen(source)
        # listen method on the recognizer instant will record as transcribes from source as long as user speaks
        try:
            query = recognizer.recognize_google(voice).lower()
            # passing the voice through Google search,or,bing,etc
            # also convert the transcribed text into lower case
            print('you said....', query)
            return query
        except Exception as ex:
            print('No clue what you said: An exception', ex)


def speak_va(transcribed_query):     # result via voice
    engine.say(transcribed_query)    #
    engine.runAndWait()


def add_tagged_keywords_to_csv(tagged_keywords_list):
    print("at add_tagged_keywords_to_csv()")
    fields = ["Word", "Tag"]
    with open('./tagged_keywords.csv', 'a') as f:
        write = csv.writer(f)
        write.writerow(fields)
        for row in tagged_keywords_list:
            write.writerow(row)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("yes" if torch.cuda.is_available() else "No, it is not")

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sarah"
print("I would like you to think back to the moment when you explored the object.")
speak_va("I would like you to think back to the moment when you explored the object")
print("Would you please describe what do you perceive?")
speak_va("Would you please describe what do you perceive?")


def get_response(msg):
# for step in range(3):
# while True:
#     sentence = input_query()
    # if sentence == "quit":
    #     break

    msg = tokenize(msg)
    X = bag_of_words(msg, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # print(f"{bot_name}: {random.choice(intent['responses'])}")
                kk = random.choice(intent['responses'])
                speak_va(f"{kk}")
                return kk
    else:
        # print(f"{bot_name}: I do not understand... Could you please repeat?")
        speak_va("I do not understand... Could you please repeat?")
        return "I do not understand... Could you please repeat?"


# for step in range(3):
#     sentence = input_query()
#     if sentence == "quit":
#         break
#     get_response(sentence)
