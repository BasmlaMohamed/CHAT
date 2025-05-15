import json
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle
import random

# Download NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# Load intents file
with open('intents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare training data
X_train = []
y_train = []

for intent in data['content']:
    tag = intent['tag']
    for sub_intent in intent['intents']:
        pattern = sub_intent['pattern'].lower()
        X_train.append(pattern)
        y_train.append(tag)

# Vectorize patterns
vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize)
X_train_vectorized = vectorizer.fit_transform(X_train)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_vectorized, y_train)

# Save model and vectorizer
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ Training complete and model saved.")