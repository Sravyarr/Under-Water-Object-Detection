import os
import numpy as np

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import tensorflow_hub as hub

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
model = load_model('mobilenet.h5')  # Make sure to provide the correct path to the model file

def model_predict(img_path, model):
    test_image = image.load_img(img_path, target_size=(224,224))
    test_image = image.img_to_array(test_image)
    test_image = test_image / 255
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)

 
    classes = ['Black Sea Sprat','Clams','Corals','Crabs','Dolphin','Eel','Fish','Gilt-Head Bream','Hourse Mackerel','JellyFish','Lobster','Nudibranchs','Octopus','Otter','Penguin','Puffers','Red Mullet','Red Sea Bream','Sea Bass','Sea Rays','Sea Urchins','Seahorse','Seal','Sharks','Shrimp','Squid','Starfish','Striped Red Mullet','Trout','Turtle_Tortoise','Whale']

    # Get the class with the highest probability
    predicted_class_index = np.argmax(result)

    predicted_class = classes[predicted_class_index]
    return predicted_class

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        predicted_class = model_predict(file_path, model)
        result = f"The predicted class is: {predicted_class}"
        return result
    return None

if __name__ == '__main__':
    app.run(debug=False)
