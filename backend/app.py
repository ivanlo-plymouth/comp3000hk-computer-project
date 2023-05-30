import numpy as np
import pickle
import os
import uuid
import pandas as pd
import json
import shutil
from datetime import datetime
from flask import Flask, request
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)
CORS(app)

# Load the trained models
text_model = load_model('text_classifier_model.h5')
image_model = load_model('image_classifier_model.h5')

# Load the tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the max_length
with open('max_length.json', 'r') as f:
    max_length = json.load(f)['max_length']

@app.route('/predict-text', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def predict_text():
    text = request.json['text']
    # Tokenize and pad the text
    sequences = tokenizer.texts_to_sequences([text])
    data = pad_sequences(sequences, maxlen=max_length)
    # Make the prediction with text_model
    predictions = text_model.predict(data)
    predicted_class = (predictions > 0.5).astype("int32")

    # Save the text submission
    df = pd.DataFrame({'body': [text], 'label': [predicted_class[0][0]]})
    # Create a new directory
    date_dir = datetime.now().strftime('%Y-%m-%d')
    os.makedirs(f'text/{date_dir}', exist_ok=True)
    if not os.path.exists(f'text/{date_dir}/submissions.csv'):
        df.to_csv(f'text/{date_dir}/submissions.csv', index=False)
    else:
        df.to_csv(f'text/{date_dir}/submissions.csv', mode='a', header=False, index=False)

    return {"result": "spam" if predicted_class[0] == 1 else "ham"}


@app.route('/predict-image', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def predict_image():
    file = request.files['file']
    # Generate a unique filename
    filename = str(uuid.uuid4()) + '.jpg'
    # Save the image temporarily for prediction
    temp_image_path = "temp.jpg"
    file.save(temp_image_path)
    # Load the image and preprocess it
    img = load_img(temp_image_path, target_size=(256,256))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    # Make the prediction with image_model
    predictions = image_model.predict(x)
    predicted_class = "spam" if (predictions > 0.7)[0] else "ham"
    # Save the image in the respective directory
    date_dir = datetime.now().strftime('%Y-%m-%d')
    target_dir = f'images/{date_dir}/{predicted_class}'
    os.makedirs(target_dir, exist_ok=True)
    # Move the image to the target directory
    shutil.move(temp_image_path, os.path.join(target_dir, filename))
    return {"result": predicted_class}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)