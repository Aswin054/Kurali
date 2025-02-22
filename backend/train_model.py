from datasets import load_dataset
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

# Load the Thirukkural dataset
print("Loading dataset...")
dataset = load_dataset("Selvakumarduraipandian/Thirukural")

# Extract the "train" split
kural_data = dataset['train']

# Ensure the correct key is used (case-sensitive)
texts = [entry['Kural'] for entry in kural_data]  # Use 'Kural' (capitalized)

print(f"Loaded {len(texts)} Thirukkurals")

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)

# Convert texts to sequences
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, padding='post')

# Define a simple model (LSTM-based chatbot)
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=padded_sequences.shape[1]),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(tokenizer.word_index) + 1, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Convert sequences for training (predicting next word)
X = padded_sequences[:, :-1]  # Input sequences
y = padded_sequences[:, -1]   # Target word (last token of each sequence)

# Print shapes to debug
print("X shape:", X.shape)  # Expected: (1330, sequence_length - 1)
print("y shape:", y.shape)  # Expected: (1330,)

# Train the model
model.fit(X, y, epochs=10, batch_size=32)


# Save the model
model.save("chatbot_model.keras")
print("Model saved successfully!")

# Save tokenizer for later use
with open("tokenizer.pkl", "wb") as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)

print("Tokenizer saved successfully!")

