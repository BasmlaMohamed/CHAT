from flask import Flask, request, jsonify
from flask_cors import CORS  # Add CORS support
import pickle
import nltk
import difflib
import json
from typing import Dict, Any

# Initialize Flask app with CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load configuration
with open('intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)['content']

try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
except FileNotFoundError as e:
    print(f"Model loading error: {e}")
    # Handle missing model files

def get_response(user_input: str) -> str:
    """Generate response based on user input"""
    try:
        X_input = vectorizer.transform([user_input.lower()])
        tag = model.predict(X_input)[0]
        print(f"Predicted tag: {tag}")

        for intent in intents:
            if intent['tag'] == tag:
                patterns = [sub_intent['pattern'].lower() 
                          for sub_intent in intent['intents']]
                
                matches = difflib.get_close_matches(
                    user_input.lower(), 
                    patterns, 
                    n=1, 
                    cutoff=0.6
                )
                
                if matches:
                    closest_pattern = matches[0]
                    for sub_intent in intent['intents']:
                        if sub_intent['pattern'].lower() == closest_pattern:
                            return sub_intent['response']
                
                return intent['intents'][0]['response']
                
    except Exception as e:
        print(f"Error generating response: {e}")
    
    return "Hmm, I didn't catch that. Could you tell me more about your baby's needs? 😊"

@app.route('/predict', methods=['POST', 'GET'])  # Allow both methods
def predict():
    """Handle prediction requests"""
    try:
        if request.method == 'GET':
            return jsonify({
                "response": "Please use POST method with JSON body containing 'message'"
            })
            
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field"}), 400
            
        message = data['message']
        response = get_response(message)
        return jsonify({"response": response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Download NLTK data if not present
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        nltk.download('punkt_tab')
    
    app.run(host='0.0.0.0', port=3000, debug=True)