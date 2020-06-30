import sys
import os
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/more_data(3).h5'

# Load your trained model
new_model = load_model(MODEL_PATH)
      # Necessary
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')

def loadImage(filepath):
    test_img = image.load_img(filepath, target_size=(180, 180))
    test_img = image.img_to_array(test_img)
    test_img = np.expand_dims(test_img, axis = 0)
    test_img /= 255
    return test_img


def model_predict(img_path):
    global new_model    
    age_pred = new_model.predict(loadImage(img_path))

    x = age_pred[0][0]
    #print('Chances of belonging in any category :')
    
    age = 'About '+ str(x) +' years old'

    return age


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
        age = model_predict(file_path)

        return ' '+ age 

    return None

if __name__ == '__main__':
    app.run(debug=True)

