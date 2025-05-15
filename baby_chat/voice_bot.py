import speech_recognition as sr
import pyttsx3
import pickle
import json
import random

# Load trained model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["content"]

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("🤖 Mom Pulse:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("🗣️ You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition is not working right now.")
        return ""

def get_response(user_input):
    X_input = vectorizer.transform([user_input])
    tag = model.predict(X_input)[0]

    for intent in intents:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "I'm not sure how to help with that."

# Run chatbot loop
while True:
    text = listen()
    if not text:
        continue
    if "exit" in text or "stop" in text:
        speak("Goodbye mama! Call me when you need help again.")
        break
    response = get_response(text)
    speak(response)
