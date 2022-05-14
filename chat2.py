import random
import json
import torch
import csv
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import pyttsx3  # text to speech conversion library
from Vosk_test import return_text
import sounddevice as sd
import vosk

engine = pyttsx3.init()  # this loads a speech engine driver
voices = engine.getProperty('voices')  # grab the current value of the engine property: voices
engine.setProperty('voice', voices[0].id)  # this sets female voice... for male voice, set the index to
engine.setProperty('rate', 140)

# model_speech = vosk.Model("model")
# device_info = sd.query_devices(None, 'input')

model_speech = vosk.Model("model")
device_info = sd.query_devices(None, 'input')
model_speech = vosk.KaldiRecognizer(model_speech, int(device_info['default_samplerate']))


def input_query():  # function to accept a command from the user
    # try:
    query = return_text(model_speech, device_info)
    print('you said....', query)
    return query
    # except Exception as ex:
    #     print('No clue what you said: An exception', ex)


def speak_va(transcribed_query):  # result via voice
    engine.say(transcribed_query)  #
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


for step in range(100):
    sentence = input_query()
    if sentence == "quit":
        break
    # get_response(sentence)
