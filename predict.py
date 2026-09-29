"""
predict.py  —  REAL DATA VERSION
Loads the trained RNN model and scaler, builds a 24-hour sequence
from repeated input (or a provided history list), and returns the
traffic severity classification.
"""

import numpy as np
import joblib
import tensorflow as tf

SEQ_LEN = 24

LABELS       = ["Low Traffic", "Medium Traffic", "High Traffic"]
LABELS_EMOJI = ["Low Traffic Green", "Medium Traffic Yellow", "High Traffic Red"]
LABELS_SHORT = ["Low", "Medium", "High"]

# Real dataset features (9 total)
FEATURE_COLS = [
    "hour", "day_of_week", "month", "is_weekend",
    "holiday_flag", "weather_code", "temp_c",
    "rain_1h", "clouds_all",
]

_model  = None
_scaler = None

def _load():
    global _model, _scaler
    if _model is None:
        _model  = tf.keras.models.load_model("model/traffic_rnn.keras")
    if _scaler is None:
        _scaler = joblib.load("model/scaler.pkl")


def predict_traffic(input_rows: list) -> dict:
    """
    Parameters
    ----------
    input_rows : list of dicts, each with keys matching FEATURE_COLS.
                 If fewer than SEQ_LEN rows are provided, the first row
                 is repeated to pad the sequence.

    Returns
    -------
    dict : label_index, label, label_full, confidence, probabilities
    """
    _load()

    # Pad or trim to SEQ_LEN
    if len(input_rows) < SEQ_LEN:
        pad = [input_rows[0]] * (SEQ_LEN - len(input_rows))
        input_rows = pad + list(input_rows)
    input_rows = input_rows[-SEQ_LEN:]

    X = np.array(
        [[row[c] for c in FEATURE_COLS] for row in input_rows],
        dtype=np.float32,
    )
    X_scaled = _scaler.transform(X)
    X_seq    = X_scaled.reshape(1, SEQ_LEN, len(FEATURE_COLS))

    probs      = _model.predict(X_seq, verbose=0)[0]
    label_idx  = int(np.argmax(probs))
    confidence = float(probs[label_idx]) * 100

    return {
        "label_index":  label_idx,
        "label":        LABELS_SHORT[label_idx],
        "label_full":   LABELS[label_idx],
        "confidence":   round(confidence, 2),
        "probabilities": {
            "Low":    round(float(probs[0]) * 100, 2),
            "Medium": round(float(probs[1]) * 100, 2),
            "High":   round(float(probs[2]) * 100, 2),
        },
    }
