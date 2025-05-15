import json
import pickle
import nltk
import difflib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# Load intents
with open('intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)['content']

# Load model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def get_response(user_input):
    # Vectorize input
    X_input = vectorizer.transform([user_input.lower()])
    tag = model.predict(X_input)[0]
    print(f"Predicted tag: {tag}")  # Debug line

    # Find the matching intent
    for intent in intents:
        if intent['tag'] == tag:
            patterns = [sub_intent['pattern'].lower() for sub_intent in intent['intents']]
            matches = difflib.get_close_matches(user_input.lower(), patterns, n=1, cutoff=0.6)
            if matches:
                closest_pattern = matches[0]
                for sub_intent in intent['intents']:
                    if sub_intent['pattern'].lower() == closest_pattern:
                        return sub_intent['response']
            # Fallback if no close match
            return intent['intents'][0]['response']  # Return first response as fallback
    return "Hmm, I didn’t catch that. Could you tell me more about your baby’s needs? 😊"

# Chat loop
# Chat loop
history = []
print("🤖 Type your message. Type 'exit' to end the chat.")
while True:
    user_input = input("🧑 You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("🤖 Bye! Mom Pulse will be here when you need us. 😊")
        break
    response = get_response(user_input)
    print(f"🤖 Bot: {response}")
    history.append({"user": user_input, "bot": response})