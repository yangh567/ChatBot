## 0
modify the intents file based on ur application, and run train.py file to train the model

-madhan

## 0
The DeepSpeech model file should be put in DeepSpeech folder

you need to download model files there: https://drive.google.com/drive/folders/11jHbi-ylASIBsmwSCgLU5gLiYHkGwI-B?usp=sharing

you need to install requirement library by pip install -r requirements.txt in your environment

Then, you need to run app1.py

- Zhouyang

## 1
New version avaliable using VOSK

you need to install requirements and download model files and create and put into a new directory called 'model'

The model files can be downloaded here: https://alphacephei.com/vosk/models

Please find the file name -- vosk-model-en-us-0.22

then:
    1. Decompress it and rename the top folder as 'model' and put under ChatBot directory
    2. Done

Run app2.py to see the results

update specification:

    1, new model called VOSK that support English, Indian English,
    German, French, Spanish, Portuguese, Chinese, Russian, Turkish,
    Vietnamese, Italian, Dutch, Catalan, Arabic, Greek, Farsi, Filipino,
    Ukrainian, Kazakh, Swedish, Japanese, Esperanto, Hindi, Czech. More to come.

    2. managed to eliminated delay when access microphone
    3. managed to allow users speak as much long as possible
    4. added model training and testing file train_test.py and enhanced model.
    5. removed unnecessary libraries
