import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import sys
import os

model_path = 'model_pneumonie.h5'
image_path = 'radio1.jpg'

if not os.path.exists(model_path):
    print(f"EROARE: Nu gasesc fișierul '{model_path}'. L-ai pus in același folder?")
    sys.exit()

if not os.path.exists(image_path):
    print(f"EROARE: Nu gasesc imaginea '{image_path}'. Verifica numele si extensia!")
    sys.exit()

print("Incarcam reteaua neurala... te rog asteapta.")
# Suprimam avertismentele hardware pentru o consola mai curata
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model = load_model(model_path)


print(f"Analizam radiografia: {image_path}...")
# Redimensionam la 224x224, formatul obligatoriu cu care a fost antrenat modelul
img = image.load_img(image_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0  # Normalizam culorile (aducem pixelii in intervalul 0-1)


# Funcția predict returneaza probabilitatea ca imaginea sa aiba pneumonie
predictie = model.predict(img_array, verbose=0)[0][0]

if predictie > 0.8:
    diagnostic = "PNEUMONIE"
    incredere = predictie * 100
    culoare_grafic = 'red'
else:
    diagnostic = "SANATOS"
    incredere = (1 - predictie) * 100
    culoare_grafic = 'green'

print("\n" + "="*40)
print("             REZULTAT ANALIZA            ")
print("="*40)
print(f" DIAGNOSTIC: {diagnostic}")
print(f" SIGURANȚA:  {incredere:.2f}%")
print("="*40 + "\n")


plt.figure(figsize=(6, 6))
plt.imshow(img, cmap='gray')
plt.axis('off')
titlu = f"Diagnostic AI: {diagnostic}\nSiguranta: {incredere:.1f}%"
plt.title(titlu, color=culoare_grafic, fontsize=14, fontweight='bold')
plt.show()