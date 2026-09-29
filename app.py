"""
app.py  —  Flask Backend for Traffic Jam Prediction
Real Dataset: Metro Interstate Traffic Volume (I-94 Highway)
"""

import os
from flask import Flask, jsonify, render_template, request, send_from_directory

from predict import predict_traffic, FEATURE_COLS

app = Flask(__name__)

MODEL_PATH  = "model/traffic_rnn.keras"
SCALER_PATH = "model/scaler.pkl"
GRAPH_DIR   = "graphs"


# ────────────────────────────────────────────────────────────
# Routes
# ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    model_ready = (
        os.path.exists(MODEL_PATH) and
        os.path.exists(SCALER_PATH)
    )
    graphs_exist = (
        os.path.exists(os.path.join(GRAPH_DIR, "accuracy.png")) and
        os.path.exists(os.path.join(GRAPH_DIR, "loss.png")) and
        os.path.exists(os.path.join(GRAPH_DIR, "confusion_matrix.png"))
    )
    return jsonify({
        "model_ready":  model_ready,
        "graphs":       graphs_exist,
        "feature_cols": FEATURE_COLS,
        "dataset":      "Metro Interstate Traffic Volume (I-94, UCI)",
    })


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    Expects JSON with these 9 real-dataset keys:
      hour, day_of_week, month, is_weekend, holiday_flag,
      weather_code, temp_c, rain_1h, clouds_all
    """
    try:
        body = request.get_json(force=True)

        row = {
            "hour":         float(body.get("hour",         8)),
            "day_of_week":  float(body.get("day_of_week",  0)),
            "month":        float(body.get("month",        10)),
            "is_weekend":   float(body.get("is_weekend",    0)),
            "holiday_flag": float(body.get("holiday_flag",  0)),
            "weather_code": float(body.get("weather_code",  0)),
            "temp_c":       float(body.get("temp_c",       15)),
            "rain_1h":      float(body.get("rain_1h",       0)),
            "clouds_all":   float(body.get("clouds_all",   40)),
        }

        result = predict_traffic([row])   # predict.py pads to SEQ_LEN=24
        return jsonify({"success": True, "result": result})

    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": "Model not found. Run train_model.py first.",
        }), 503
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


# ────────────────────────────────────────────────────────────
# Serve graph PNGs
# ────────────────────────────────────────────────────────────

@app.route("/static/graphs/<path:filename>")
@app.route("/graphs/<path:filename>")
def serve_graphs(filename):
    return send_from_directory(os.path.abspath(GRAPH_DIR), filename)


# Aliases for backward compatibility
@app.route("/predict", methods=["POST"])
def predict_alias():
    return api_predict()


@app.route("/health")
def health_alias():
    return status()


if __name__ == "__main__":
    print("\n[*] Traffic Jam Prediction Server")
    print("   Dataset: Metro Interstate Traffic Volume (I-94)")
    print("   URL    : http://127.0.0.1:5000")
    print("   Press CTRL+C to quit\n")
    app.run(debug=True, port=5000)

