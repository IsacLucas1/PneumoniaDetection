# 🫁 AI Pneumonia Detector

O aplicație Full-Stack (React + Python) bazată pe Inteligență Artificială, concepută pentru a analiza radiografii pulmonare și a detecta semnele de pneumonie. Proiectul folosește un model de Deep Learning (MobileNetV2) antrenat pe un set de date clinic și este optimizat pentru a funcționa corect pe date din lumea reală.

---

## 💡 Problema pe care o rezolvă (Domain Shift)
În mod frecvent, modelele AI medicale funcționează perfect în mediul controlat de antrenament, dar eșuează când primesc radiografii din surse noi (de pe internet sau de la alte aparate). Această problemă poartă numele de **Domain Shift**. 

Acest proiect rezolvă această provocare printr-un **filtru avansat de pre-procesare**:
* **Auto-Crop:** Elimină automat marginile negre inutile generate de scanere.
* **Grayscale Forțat:** Previne erorile cauzate de imaginile salvate accidental cu profil de culoare RGB.
* **Autocontrast:** Normalizează luminozitatea pentru a aduce radiografia la standardele de vizibilitate clinică înainte de a fi trimisă rețelei neurale.

---

## ✨ Sistemul de Triage Medical pe 3 Niveluri
Pentru a reflecta prudența din medicina reală, AI-ul nu ia decizii absolute de tip "Alb/Negru" (unde pragul clasic de 50% poate fi periculos). Diagnosticul este împărțit astfel:

* 🟢 **SĂNĂTOS:** Risc de boală sub 50%.
* 🟠 **SUSPECT (Necesită verificare):** Zonă de incertitudine (risc 50% - 80%). Semnalează medicului o posibilă anomalie sau o calitate slabă a imaginii, solicitând intervenție umană.
* 🔴 **PNEUMONIE:** Siguranță de peste 80% a prezenței infecției (opacități / consolidări vizibile).

---

## 🛠️ Tehnologii Folosite

**Frontend (Interfața Utilizator):**
* React (via Vite)
* JavaScript / JSX
* CSS3 (Design responsiv și dinamic în funcție de starea diagnosticului)

**Backend & Deep Learning:**
* Python
* FastAPI & Uvicorn (Server REST)
* TensorFlow / Keras (Model: MobileNetV2)
* Pillow (PIL) & NumPy (Pre-procesarea avansată a imaginilor)

---

## 🚀 Cum să rulezi proiectul local

Aplicația are o arhitectură decuplată. Trebuie să pornești simultan serverul de AI (Backend) și interfața web (Frontend) în **două terminale separate**.

### 1. Pornirea Serverului AI (Backend / Python)
Deschide un terminal în folderul principal al proiectului și instalează modulele necesare:
```bash
pip install fastapi uvicorn tensorflow pillow python-multipart numpy matplotlib

Pornește serverul:

uvicorn api:app --reload
(Serverul va rula invizibil pe http://localhost:8000 și va aștepta să proceseze imagini)

Notă pentru Debug: Există și un script main.py pe care îl poți rula în terminal (python main.py) pentru a testa rețeaua neurală strict la nivel de consolă, fără interfața web.

2. Pornirea Interfeței Web (Frontend / React)
Deschide un al doilea terminal și navighează în folderul frontend-ului:

cd frontend_PneumoniaDetector
Instalează pachetele Node:

npm install

Pornește aplicația:

npm run dev
(Dă click pe linkul generat în terminal, de obicei http://localhost:5173, pentru a deschide aplicația direct în browserul tău)

📁 Structura Proiectului
Plaintext
/
├── api.py                     # API-ul REST principal (FastAPI) și logica de filtrare
├── main.py                    # Script de testare locală (CLI)
├── model_pneumonie.h5         # Modelul neural antrenat (Ponderile MobileNetV2)
├── radio1.jpg - radio10.jpg   # Imagini locale de testare
├── .gitignore                 # Fișiere ignorate de sistemul Git
└── frontend_PneumoniaDetector/ # Aplicația interfeței web
    ├── package.json           # Dependențele de UI
    ├── vite.config.js         # Configurarea mediului de dezvoltare Vite
    ├── index.html             # Punctul de intrare HTML
    ├── public/                # Active vizuale și iconițe SVG
    └── src/                   # Codul sursă React
        ├── App.jsx            # Componenta principală (Logica aplicației)
        ├── App.css            # Stilurile UI
        ├── main.jsx           # Punctul de intrare pentru React
        └── index.css          # Setări globale CSS

🛑 Limitări Cunoscute
Fiind antrenat specific pe radiografii clinice standard de tip PA (Postero-Anterior), sistemul prezintă următoarele limitări:

Nu procesează corect radiografii efectuate din profil (lateral).

Poate returna rezultate eronate (Fals Pozitive) dacă imaginea conține editări vizibile (ex: săgeți colorate suprapuse, texte masive sau decupaje nenaturale).

⚠️ Disclaimer
Acesta este un proiect educațional demonstrativ de Machine Learning. Deși folosește tehnologii avansate de recunoaștere a imaginilor, NU este un dispozitiv medical aprobat și nu trebuie folosit pentru diagnosticare în viața reală. Orice decizie medicală trebuie luată exclusiv de un medic specialist.
