from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load model and tokenizer
print("Loading chatbot model...")
model = load_model("models/chatbot_model.h5")

with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_len = 20  # Set this to match train_model.py's max_len

# FastAPI setup
app = FastAPI()

class ChatInput(BaseModel):
    message: str

# Chatbot response function
def generate_response(user_input):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding="post")
    
    predicted_index = np.argmax(model.predict(padded_sequence), axis=-1)[0]
    response = tokenizer.index_word.get(predicted_index, "மன்னிக்கவும், புரியவில்லை!")  # Default response

    return response

# API Endpoint
@app.post("/chat")
def chat(input_data: ChatInput):
    response = generate_response(input_data.message)
    return {"response": response}

# Run server: uvicorn main:app --reload
