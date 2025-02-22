import numpy as np
import tensorflow as tf
import pickle

# Load the trained model
model = tf.keras.models.load_model("chatbot_model.keras")  # Use "chatbot_model.h5" if needed

# Load the saved tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Function to generate a response from the chatbot
def generate_response(input_text):
    # Convert input text to sequence
    sequence = tokenizer.texts_to_sequences([input_text])
    
    # Pad sequence to match training input size
    max_length = model.input_shape[1]  # Get input size from model
    padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=max_length, padding="post")

    # Make a prediction
    predicted_token = np.argmax(model.predict(padded_sequence), axis=-1)[0]
    
    # Convert token to word
    response_word = tokenizer.index_word.get(predicted_token, "???")  # Default to "???" if not found
    return response_word

# Test the chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye! 👋")
        break

    response = generate_response(user_input)
    print("Chatbot:", response)
