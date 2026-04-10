import { useState } from 'react';
import './App.css';

function App() {
  const [imagine, setImagine] = useState(null);
  const [preview, setPreview] = useState(null);
  const [rezultat, setRezultat] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAlegeImagine = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImagine(file);
      setPreview(URL.createObjectURL(file));
      setRezultat(null);
    }
  };

  const handleAnalizeaza = async () => {
    if (!imagine) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", imagine);

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setRezultat(data);
    } catch (error) {
      alert("Eroare de conexiune cu serverul AI (Python)!");
    } finally {
      setLoading(false);
    }
  };

  // Functii ajutatoare pentru a stabili culorile si iconitele in mod dinamic
  const getCardClass = (diagnostic) => {
    if (diagnostic === "SANATOS") return 'healthy';
    if (diagnostic.includes("SUSPECT")) return 'suspect';
    return 'pneumonia';
  };

  const getIcon = (diagnostic) => {
    if (diagnostic === "SANATOS") return '✅';
    if (diagnostic.includes("SUSPECT")) return '⚠️';
    return '🚨';
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI Pneumonia Detector</h1>
        <p>Analiza imagistica pulmonara bazata pe Deep Learning (MobileNetV2)</p>
      </header>

      <main className="card-container">
        {/* Buton Custom pentru Upload */}
        <div className="upload-section">
          <label htmlFor="file-upload" className="custom-upload-btn">
            📁 Alege Radiografia
          </label>
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={handleAlegeImagine}
          />
          <span className="file-name">
            {imagine ? imagine.name : "Niciun fisier selectat"}
          </span>
        </div>

        {/* Zona de previzualizare a imaginii */}
        {preview && (
          <div className="preview-section">
            <img src={preview} alt="Previzualizare radiografie" className="image-preview" />
          </div>
        )}

        {/* Butonul principal de actiune */}
        <button
          className={`analyze-btn ${loading ? 'pulsing' : ''}`}
          onClick={handleAnalizeaza}
          disabled={!imagine || loading}
        >
          {loading ? "⚙️ Analizez tiparele..." : "🔍 Genereaza Diagnostic"}
        </button>

        {/* Cardul cu rezultate (Apare doar dupa predictie) */}
        {rezultat && (
          <div className={`result-card ${getCardClass(rezultat.diagnostic)}`}>
            <div className="result-icon">
              {getIcon(rezultat.diagnostic)}
            </div>
            <div className="result-details">
              <h2>DIAGNOSTIC: {rezultat.diagnostic}</h2>
              <div className="confidence-bar-bg">
                <div
                  className="confidence-bar-fill"
                  style={{ width: `${rezultat.incredere}%` }}
                ></div>
              </div>
              <p>Grad de siguranta AI: <strong>{rezultat.incredere.toFixed(1)}%</strong></p>
            </div>
          </div>
        )}
      </main>

    </div>
  );
}

export default App;