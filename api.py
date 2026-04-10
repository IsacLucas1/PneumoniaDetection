import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import logging
import tensorflow as tf

tf.get_logger().setLevel('ERROR')
logging.getLogger('absl').setLevel('ERROR')

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import io
from PIL import Image, ImageOps

# Initializam serverul
app = FastAPI()

# Permitem interfetei React (de pe alt port) sa discute cu noi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Incarcam reteaua neurala...")
model = load_model('model_pneumonie.h5')
print("Server activ! Astept radiografii de la React...")


def curata_radiografia(img):
    # 1. O facem strict alb-negru pentru a elimina abaterile de culoare ascunse
    img_gray = img.convert('L')

    # 2. Gasim si taiem automat marginile negre inutile (Auto-Crop)
    bbox = img_gray.getbbox()
    if bbox:
        img_gray = img_gray.crop(bbox)

    # 3. Fortam contrastul (echilibreaza luminozitatea oaselor cu cea a plamanilor)
    img_contrast = ImageOps.autocontrast(img_gray, cutoff=2)

    # 4. O transformam inapoi in RGB pentru ca MobileNetV2 vrea 3 canale de culoare
    return img_contrast.convert('RGB')


@app.post("/predict")
async def predict_pneumonia(file: UploadFile = File(...)):
    # 1. Receptionam imaginea din browser
    contents = await file.read()
    img_bruta = Image.open(io.BytesIO(contents))

    # --- APLICAM FILTRUL DE CURATARE ---
    img_curatata = curata_radiografia(img_bruta)

    # 2. O pregatim pentru model (redimensionare 224x224 si normalizare)
    img_finala = img_curatata.resize((224, 224))
    img_array = keras_image.img_to_array(img_finala)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # 3. Modelul pune diagnosticul
    predictie = model.predict(img_array, verbose=0)[0][0]

    # 4. Trimitem raspunsul inapoi catre React in format JSON
    if predictie >= 0.80:
        return {"diagnostic": "PNEUMONIE", "incredere": float(predictie * 100)}
    elif predictie <= 0.50:
        return {"diagnostic": "SANATOS", "incredere": float((1 - predictie) * 100)}
    else:
        return {"diagnostic": "SUSPECT (Necesita verificare)", "incredere": float(predictie * 100)}