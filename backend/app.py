from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

model = load_model("model/lstm_model.h5")

with open("model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_len = model.input_shape[1]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data["text"].lower()

    seq = tokenizer.texts_to_sequences([text])[0]
    seq = pad_sequences([seq], maxlen=max_len, padding="pre")

    preds = model.predict(seq)[0]
    top_indices = preds.argsort()[-4:][::-1]

    suggestions = []
    for i in top_indices:
        word = tokenizer.index_word.get(i)
        if word:
            suggestions.append(word)

    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
