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
MODEL_PATH = 'models/a_g1.h5'

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
    test_img = image.load_img(filepath, target_size=(198, 198))
    test_img = image.img_to_array(test_img)
    test_img = np.expand_dims(test_img, axis = 0)
    test_img /= 255
    return test_img


def model_predict(img_path):
    global new_model    
    age_pred, gender_pred = new_model.predict(loadImage(img_path))
    img = image.load_img(img_path)                        

    max=-1
    count=0
    #print('Chances of belonging in any category :')
    xx = list(age_pred[0])
    for i in age_pred[0]:
        if i>max:
            max = i
            temp = count
        count+=1

    if temp==0:
        age = '0-24 yrs old'
    if temp==1:
        age = '25-49 yrs old'
    if temp==2:
        age = '50-74 yrs old'
    if temp==3:
        age = '75-99 yrs old'
    if temp==4:
        age = '91-124 yrs old'

    if gender_pred[0][0]>gender_pred[0][1]:
        gender = 'male'
    else:
        gender = 'female'

    return age, gender


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
        age, gender = model_predict(file_path)

        return ' '+ age + '    ' + ', '+ gender
    return None

if __name__ == '__main__':
    app.run(debug=True)

