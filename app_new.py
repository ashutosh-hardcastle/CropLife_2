# Importing essential libraries and modules

import pandas as pd
import numpy as np
import base64
import io
import uvicorn
import urllib
import tensorflow as tf
from flask import Flask, render_template, request, Markup
from fastapi import FastAPI, File, UploadFile
from utils.fertilizer import fertilizer_dic
from utils.disease import disease_dic
from io import BytesIO
from PIL import Image
from tensorflow.keras.models import Sequential, load_model
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import request
from flask import jsonify
# ------------------------------------ FLASK APP -------------------------------------------------


app = FastAPI()

MODEL = tf.keras.models.load_model("C:/Users/lenova/PycharmProjects/MMC/models_old")

# ----------------Loading the Trained Models------------#

disease_classes = ['Apple_Apple_Scab',
                   'Apple_Black_Rot',
                   'Apple_Cedar_Apple_Rust',
                   'Apple_Healthy',
                   'Bell_Pepper_Bacterial_Spot',
                   'Bell_Pepper_Healthy',
                   'Blueberry_Healthy',
                   'Cherry(Including_Sour)_Healthy',
                   'Cherry(Including_Sour)_Powdery_Mildew',
                   'Corn(Maize)_Cercospora_Gray_Leaf_Spot',
                   'Corn(Maize)_Common_Rust',
                   'Corn(Maize)_Healthy',
                   'Corn(Maize)_Northern_Leaf_Blight',
                   'Cotton_Bacterial_Blight',
                   'Cotton_Curl_Virus',
                   'Cotton_Fussarium_Wilt',
                   'Cotton_Healthy',
                   'Grape_Black_Rot',
                   'Grape_Esca(Black_Measles)',
                   'Grape_Healthy',
                   'Grape_Leaf_Blight(Isariopsis_Leaf_Spot)',
                   'Orange_Haunglongbing(Citrus_Greening)',
                   'Peach_Bacterial_Spot',
                   'Peach_Healthy',
                   'Potato_Early_Blight',
                   'Potato_Healthy',
                   'Potato_Late_Blight',
                   'Raspberry_Healthy',
                   'Rice_Bacterial_Leaf_Blight',
                   'Rice_Blast',
                   'Rice_Brown_Spot',
                   'Rice_Healthy',
                   'Rice_Leaf_Smut',
                   'Rice_Sheath_Blight',
                   'Rice_Tungro',
                   'Soybean_Healthy',
                   'Squash_Powdery_Mildew',
                   'Strawberry_Healthy',
                   'Strawberry_Leaf_Scorch',
                   'Sugarcane_Bacterial_Blight',
                   'Sugarcane_Healthy',
                   'Sugarcane_Red_Rot',
                   'Tomato_Bacterial_Spot',
                   'Tomato_Early_Blight',
                   'Tomato_Healthy',
                   'Tomato_Late_Blight',
                   'Tomato_Leaf_Mold',
                   'Tomato_Mosaic_Virus',
                   'Tomato_Septoria_Leaf_Spot',
                   'Tomato_Target_Spot',
                   'Tomato_Two_Spotted_Spider_Mite',
                   'Tomato_Yellow_Leaf_Curl_Virus',
                   'Wheat_Brown_Rust',
                   'Wheat_Healthy',
                   'Wheat_Septoria',
                   'Wheat_Stripe_Rust',
                   'Wheat_Yellow_Rust']

# ------------------------------------ FLASK APP -------------------------------------------------



def predict_image(image):
    image = image.load_img(image, target_size=(256, 256))
    x = image.img_to_array(image)
    x = x / 255
    return np.expand_dims(x, axis=0)


result = model.predict([prepare(x)])
disease = image.load_img(x)
plt.imshow(disease)

class_predicted = Classes[np.argmax(result)]
print(class_predicted)

# def predict_image(img, model=disease_model):
#     """
#     Transforms image to tensor and predicts disease label
#     :params: image
#     :return: prediction (string)
#     """
#     transform = transforms.Compose([
#         transforms.Resize(256),
#         transforms.ToTensor(),
#     ])
#     image = Image.open(io.BytesIO(img))
#     img_t = transform(image)
#     img_u = torch.unsqueeze(img_t, 0)
#
#     # Get predictions from model
#     yb = model(img_u)
#     # Pick index with highest probability
#     _, preds = torch.max(yb, dim=1)
#     prediction = disease_classes[preds[0].item()]
#     # Retrieve the class label
#     return prediction

# def predict_image(image, model = d_model):
#     if image.mode != "RGB":
#         image = image.convert("RGB")
#     image = image.resize(256,256)
# image = img_to_array(image)
# image = np.expand_dims(image, axis=0)
# class_predicted = disease_classes[np.argmax(image)]
# print(class_predicted)
# return class_predicted

print("*Loading the Model. Kindly wait.")
get_model()

#######################################

app = Flask(__name__)


# render home page


@app.route('/')
def home():
    title = 'CropLife'
    return render_template('index.html', title=title)


# render crop recommendation form page


@app.route('/crop-recommend')
def crop_recommend():
    title = 'MMC - Crop Recommendation'
    return render_template('crop.html', title=title)


# render fertilizer recommendation form page


@app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'MMC - Fertilizer Suggestion'

    return render_template('fertilizer.html', title=title)


# render disease prediction input page


# ===============================================================================================

# RENDER PREDICTION PAGES

# render crop recommendation result page


@app.route('/crop-predict', methods=['POST'])
# render fertilizer recommendation result page

@app.route('/fertilizer-result', methods=['POST'])
def fert_recommend():
    title = 'MMC - Fertilizer Suggestion'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])
    # ph = float(request.form['ph'])

    df = pd.read_csv('Data/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K

    if n < 0:
        key1 = "NHigh"
    elif n > 0:
        key1 = "NLow"
    else:
        key1 = "NNo"

    if p < 0:
        key2 = "PHigh"
    elif p > 0:
        key2 = "PLow"
    else:
        key2 = "PNo"

    if k < 0:
        key3 = "KHigh"
    elif k > 0:
        key3 = "KLow"
    else:
        key3 = "KNo"

    abs_n = abs(n)
    abs_p = abs(p)
    abs_k = abs(k)

    response = Markup(str(fertilizer_dic[key1]))
    response1 = Markup(str(fertilizer_dic[key2]))
    response2 = Markup(str(fertilizer_dic[key3]))

    return render_template('fertilizer-result.html', recommendation=response,
                           recommendation1=response1, recommendation2=response2,
                           title=title, diff_n=abs_n, diff_p=abs_p, diff_k=abs_k)


# render disease prediction result page


@app.route('/disease-result', methods=['GET', 'POST'])
def disease_prediction():
    title = 'MMC - Disease Detection'

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('disease.html', title=title)
        try:
            img = file.read()

            prediction = predict_image(img)

            prediction = Markup(str(disease_dic[prediction]))
            return render_template('disease-result.html', prediction=prediction, title=title)
        except:
            pass
    return render_template('disease.html', title=title)


# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=False)
