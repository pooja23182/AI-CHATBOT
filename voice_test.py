import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate',150)

engine.say("Hello. The voice chatbot is working.")
engine.runAndWait()