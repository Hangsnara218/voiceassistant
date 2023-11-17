import speech_recognition as sr
import pyttsx3 
import os
from dotenv import load_dotenv
load_dotenv()
import openai
#OPENAI_KEY = os.getenv('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')
openai.api_key = 'sk-*****'

#openai.api_key = OPENAI_KEY

# convert text to speech
def SpeakText(command):

    # initialize the engine 
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

#initialize the recognizer
r = sr.Recognizer()

def record_text():
    #loop in case of error
    while(1):
        try:
            # with microphone
            with sr.Microphone() as source2:
                # prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening, Master...")
                #listen for user input
                audio2 = r.listen(source2)
                #using google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
        
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message
messages = []
while(1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    SpeakText(response)

    print(response)
