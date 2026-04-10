# AI Pneumonia Detector

O aplicație Full-Stack (React + Python) bazată pe Inteligență Artificială, creată pentru a analiza radiografii pulmonare și a detecta semnele de pneumonie. Proiectul folosește un model de Deep Learning (MobileNetV2) antrenat pe un set de date clinic și dispune de un sistem robust de pre-procesare a imaginilor pentru a funcționa corect pe date din lumea reală.

## ✨ Caracteristici Cheie

* **Arhitectură Decuplată (Full-Stack):** Frontend modern și rapid construit cu React (Vite), care comunică printr-un API REST cu un server de Python (FastAPI).
* **Filtru de Pre-procesare (Domain Shift Mitigation):** Aplicația rezolvă problema clasică de *Domain Shift* (diferența dintre datele de laborator și pozele reale). Backend-ul taie automat marginile negre inutile (Auto-Crop), forțează conversia în tonuri de gri și aplică *Autocontrast* pentru a aduce radiografia la standardele clinice înainte de a o trimite către AI.
* **Sistem de Triage Medical pe 3 Niveluri:** Modelul nu gândește doar în "Alb și Negru". Pentru a imita prudența medicală reală, diagnosticul este împărțit astfel:
  * 🟢 **SĂNĂTOS:** Risc de boală sub 50%.
  * 🟠 **SUSPECT (Necesită verificare):** Zonă de incertitudine (risc 50% - 80%). Semnalează medicului o posibilă anomalie.
  * 🔴 **PNEUMONIE:** Siguranță de peste 80% a prezenței infecției.

## 🛠️ Tehnologii Folosite

**Frontend:**
* React (via Vite)
* JavaScript / JSX
* CSS pur (Design responsiv și dinamic în funcție de diagnostic)

**Backend & AI:**
* Python
* FastAPI & Uvicorn (Server REST rapid)
* TensorFlow / Keras (Modelul Deep Learning MobileNetV2)
* Pillow (PIL) & NumPy (Procesare imagini)

## 🚀 Cum să rulezi proiectul local

Aplicația este formată din două părți care trebuie pornite simultan în două terminale separate.

### 1. Pornirea Serverului AI (Backend / Python)
Deschide un terminal în folderul principal al proiectului și instalează dependențele (dacă nu le ai deja):
```bash
pip install fastapi uvicorn tensorflow pillow python-multipart numpy matplotlib
