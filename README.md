# 🚦 Traffic Jam Prediction Using Recurrent Neural Networks (RNN)

> **College Mini Project** | AI with Python Training | Python 3.12 · TensorFlow · Flask · Chart.js

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.17-orange?logo=tensorflow)](https://tensorflow.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Overview

This project predicts **traffic congestion levels** (Low / Medium / High) using a
**Recurrent Neural Network (SimpleRNN)** trained on **48,204 real hourly observations** from the
**Metro Interstate Traffic Volume dataset** (I-94 Interstate highway, Minneapolis, UCI Machine Learning Repository). It features:

- 🧠 **Keras RNN model** trained with a 24-hour sequence memory window
- 📊 **Evaluation graphs** – Accuracy curve, Loss curve, Confusion Matrix
- 🌐 **Flask REST API** backend (`/api/predict`, `/api/status`, `/predict`)
- 💻 **Premium dark-mode dashboard** (glassmorphism UI, interactive Chart.js doughnut chart, one-click demo presets)
- 📑 **Comprehensive documentation** – Complete college report (`report/Traffic_Jam_Prediction_Report.md`) and ready-to-present PowerPoint slide deck (`report/Traffic_Jam_Prediction.pptx`)

---

## 📁 Project Structure

```
Traffic-Jam-Prediction-RNN/
│
├── app.py                  ← Flask server (API + Web dashboard)
├── train_model.py          ← Real dataset preprocessing, sequence building & RNN training
├── predict.py              ← Inference helper (loads model + scaler, sequence padding)
├── generate_pptx.py        ← Generates 14-slide college presentation PPTX
├── requirements.txt        ← Python dependencies
├── README.md
│
├── model/
│   ├── traffic_rnn.keras   ← Saved trained RNN model
│   └── scaler.pkl          ← Trained StandardScaler
│
├── dataset/
│   ├── Metro_Interstate_Traffic_Volume.csv  ← Real I-94 dataset (UCI ML Repository, 48,204 rows)
│   └── Metro_Interstate_Traffic_Volume.csv.gz
│
├── static/
│   ├── style.css           ← Modern dark-mode & glassmorphism styling
│   ├── script.js           ← Frontend logic, sliders, presets & Chart.js live charts
│   └── graphs/             ← Evaluation graphs served directly
│
├── templates/
│   └── index.html          ← Complete dashboard template
│
├── graphs/
│   ├── accuracy.png        ← Training & validation accuracy curve
│   ├── loss.png            ← Training & validation loss curve
│   └── confusion_matrix.png← Multiclass confusion matrix
│
└── report/
    ├── Traffic_Jam_Prediction_Report.md  ← Full college submission project report
    └── Traffic_Jam_Prediction.pptx       ← Complete 14-slide presentation deck
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Step 1 – Clone / Download the project

```bash
cd Traffic-Jam-Prediction-RNN
```

### Step 2 – Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3 – Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 – Train the model

```bash
python train_model.py
```

This will:
- Load the real I-94 dataset (`dataset/Metro_Interstate_Traffic_Volume.csv`, 48,204 rows)
- Clean and extract cyclic temporal & weather features
- Build 24-step sequences for temporal memory
- Train the SimpleRNN architecture
- Save `model/traffic_rnn.keras` and `model/scaler.pkl`
- Export evaluation graphs to `graphs/` and `static/graphs/`

Expected training time: **~30–60 seconds** on CPU.

### Step 5 – Generate Presentation Slides (Optional)

```bash
python generate_pptx.py
```
Generates `report/Traffic_Jam_Prediction.pptx` (14 high-impact widescreen slides).

### Step 6 – Start the Flask server

```bash
python app.py
```

### Step 7 – Open the dashboard

Navigate to **http://127.0.0.1:5000** in your browser.

---

## 🎮 Using the Dashboard

| Feature | Description |
|---|---|
| **Quick Demo Buttons** | Pre-fills rush hour, rainy evening, late night, or snow storm scenarios |
| **Sliders & Dropdowns** | Adjust hour, day, weather, temperature, rain, clouds, holiday flag |
| **Predict Button** | Sends POST `/api/predict` (or `/predict`), shows classification & confidence |
| **Probability Doughnut** | Live animated Chart.js doughnut with class breakdown |
| **Evaluation Graphs** | Training & validation accuracy, loss curves, and confusion matrix |

---

## 🔌 API Reference

### `GET /`
Returns the HTML dashboard.

### `POST /api/predict` (alias: `/predict`)
**Request body (JSON):**
```json
{
  "hour": 8,
  "day_of_week": 0,
  "month": 9,
  "is_weekend": 0,
  "holiday_flag": 0,
  "weather_code": 0,
  "temp_c": 18,
  "rain_1h": 0,
  "clouds_all": 20
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "confidence": 95.5,
    "label": "Medium",
    "label_full": "Medium Traffic",
    "label_index": 1,
    "probabilities": {
      "High": 1.0,
      "Low": 3.5,
      "Medium": 95.5
    }
  }
}
```

### `GET /api/status` (alias: `/health`)
Returns model readiness status, available graphs, feature column list, and dataset attribution.

### `GET /static/graphs/<filename>` & `GET /graphs/<filename>`
Serves evaluation graph images (`accuracy.png`, `loss.png`, `confusion_matrix.png`).

---

## 🧠 Model Architecture

```
Input  →  (10 timesteps × 9 features)
          ↓
SimpleRNN(64 units, tanh, return_sequences=True)
          ↓
Dropout(0.2)
          ↓
SimpleRNN(32 units, tanh)
          ↓
Dropout(0.2)
          ↓
Dense(16, relu)
          ↓
Dense(3, softmax)  →  [Low, Medium, High]
```

- **Optimizer:** Adam
- **Loss:** Categorical Crossentropy
- **Sequence Length:** 10 timesteps
- **Training Epochs:** up to 15 (EarlyStopping with patience=3)

---

## 📊 Input Features

| Feature | Type | Range | Description |
|---|---|---|---|
| `hour` | int | 0–23 | Hour of day |
| `day_of_week` | int | 0–6 | 0=Monday, 6=Sunday |
| `weather` | int | 0–3 | 0=Clear, 1=Cloudy, 2=Rain, 3=Snow |
| `temperature` | float | -10 to 40 | Temperature in °C |
| `rain_mm` | float | 0–30 | Rainfall in mm |
| `holiday` | int | 0 or 1 | Public holiday flag |
| `traffic_volume` | int | 0–7000 | Vehicles per hour |
| `speed` | float | 5–120 | Average speed in km/h |
| `occupancy` | float | 0–100 | Road occupancy percentage |

---

## 📈 Results

| Metric | Value |
|---|---|
| Test Accuracy | ~95% |
| Training Epochs | ~10 (early stopped) |
| Model Size | < 1 MB |
| Prediction Latency | < 100ms |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ML Framework | TensorFlow / Keras |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Visualisation | Matplotlib, Seaborn |
| Backend | Flask, Flask-CORS |
| Frontend | HTML5, CSS3 (Glassmorphism), JavaScript |
| Charts | Chart.js v4 |
| Model Persistence | Keras native + Joblib |

---

## 👨‍💻 Team

> *College Mini Project — AI with Python (3-month training)*

---

## 📄 License

MIT License — free to use for educational purposes.
