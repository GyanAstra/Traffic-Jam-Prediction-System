"""
Traffic Jam Prediction Using RNN
=================================
train_model.py  —  REAL DATA VERSION
Dataset : Metro Interstate Traffic Volume (UCI / Kaggle)
          48,204 hourly readings from I-94 highway, Minneapolis
          
Run this FIRST before starting the Flask app.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Dropout, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

# ── Reproducibility ──────────────────────────────────────────
np.random.seed(42)
tf.random.set_seed(42)

SEQ_LEN    = 24   # 24 hours of history → predict next hour's congestion
N_FEATURES = 9

print("=" * 60)
print("  Traffic Jam Prediction - Model Training")
print("  Dataset: Metro Interstate Traffic Volume (Real Data)")
print("=" * 60)

# ════════════════════════════════════════════════════════════
# 1.  Load & Preprocess Real Dataset
# ════════════════════════════════════════════════════════════
print("\n[1/6] Loading real dataset ...")

CSV_PATH = "dataset/Metro_Interstate_Traffic_Volume.csv"
df = pd.read_csv(CSV_PATH)
print(f"   Loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")

# ── Parse datetime ───────────────────────────────────────────
df["date_time"] = pd.to_datetime(df["date_time"])
df = df.sort_values("date_time").reset_index(drop=True)

# ── Feature Engineering ──────────────────────────────────────
df["hour"]       = df["date_time"].dt.hour
df["day_of_week"] = df["date_time"].dt.dayofweek   # 0=Mon
df["month"]      = df["date_time"].dt.month
df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

# Holiday: NaN means no holiday → 0; any string → 1
df["holiday_flag"] = df["holiday"].notna().astype(int)

# Temperature: Kelvin → Celsius
df["temp_c"] = df["temp"] - 273.15

# Weather encoding
weather_map = {
    "Clear": 0, "Clouds": 1, "Rain": 2, "Drizzle": 2,
    "Thunderstorm": 2, "Snow": 3, "Fog": 4, "Mist": 4,
    "Haze": 4, "Smoke": 4, "Squall": 2
}
df["weather_code"] = df["weather_main"].map(weather_map).fillna(1).astype(int)

# Clean up
df["rain_1h"]   = df["rain_1h"].fillna(0).clip(0, 50)
df["snow_1h"]   = df["snow_1h"].fillna(0).clip(0, 10)
df["clouds_all"] = df["clouds_all"].fillna(0)
df["traffic_volume"] = df["traffic_volume"].fillna(method="ffill")

# ── Label: traffic severity ───────────────────────────────────
# Based on real I-94 data distribution:
# Low    < 1500   (night, off-peak)
# Medium 1500–4500 (moderate flow)
# High   > 4500   (rush hour congestion)
def classify(vol):
    if vol < 1500:  return 0   # Low
    if vol < 4500:  return 1   # Medium
    return 2                   # High

df["label"] = df["traffic_volume"].apply(classify)

print(f"\n   Class distribution:")
vc = df["label"].value_counts().rename({0:"Low",1:"Medium",2:"High"})
print(vc.to_string())

# ── Select features ───────────────────────────────────────────
FEATURE_COLS = [
    "hour", "day_of_week", "month", "is_weekend",
    "holiday_flag", "weather_code", "temp_c",
    "rain_1h", "clouds_all",
]

# Save clean CSV
clean_cols = FEATURE_COLS + ["traffic_volume", "label", "date_time"]
df[clean_cols].to_csv("dataset/traffic_data_real.csv", index=False)
print(f"\n   Clean dataset saved -> dataset/traffic_data_real.csv")

# ════════════════════════════════════════════════════════════
# 2.  Scale Features
# ════════════════════════════════════════════════════════════
print("\n[2/6] Scaling features ...")

X_raw = df[FEATURE_COLS].values.astype(np.float32)
y_raw = df["label"].values.astype(int)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

os.makedirs("model", exist_ok=True)
joblib.dump(scaler, "model/scaler.pkl")
print("   Scaler saved -> model/scaler.pkl")

# ════════════════════════════════════════════════════════════
# 3.  Create Sequences  (sliding window of SEQ_LEN hours)
# ════════════════════════════════════════════════════════════
print(f"\n[3/6] Creating sequences (window = {SEQ_LEN} hours) ...")

def create_sequences(X, y, seq_len):
    Xs, ys = [], []
    for i in range(len(X) - seq_len):
        Xs.append(X[i : i + seq_len])
        ys.append(y[i + seq_len])          # label = next timestep
    return np.array(Xs), np.array(ys)

X_seq, y_seq = create_sequences(X_scaled, y_raw, SEQ_LEN)
print(f"   Sequences: X={X_seq.shape}, y={y_seq.shape}")

# ── Balance classes via undersampling ────────────────────────
# Find minority class count
unique, counts = np.unique(y_seq, return_counts=True)
min_count = counts.min()
balanced_idx = []
for cls in unique:
    idx = np.where(y_seq == cls)[0]
    chosen = np.random.choice(idx, min_count, replace=False)
    balanced_idx.extend(chosen)

np.random.shuffle(balanced_idx)
X_seq = X_seq[balanced_idx]
y_seq = y_seq[balanced_idx]

print(f"   After balancing: {X_seq.shape[0]:,} sequences ({min_count:,} per class)")

# ════════════════════════════════════════════════════════════
# 4.  Train / Test Split
# ════════════════════════════════════════════════════════════
X_train, X_test, y_train, y_test = train_test_split(
    X_seq, y_seq, test_size=0.2, random_state=42, stratify=y_seq
)
y_train_cat = to_categorical(y_train, num_classes=3)
y_test_cat  = to_categorical(y_test,  num_classes=3)

print(f"\n   Train: {X_train.shape[0]:,}  |  Test: {X_test.shape[0]:,}")

# ════════════════════════════════════════════════════════════
# 5.  Build RNN Model
# ════════════════════════════════════════════════════════════
print("\n[4/6] Building RNN model ...")

model = Sequential([
    Input(shape=(SEQ_LEN, len(FEATURE_COLS))),
    SimpleRNN(64, activation="tanh", return_sequences=True),
    Dropout(0.2),
    SimpleRNN(32, activation="tanh"),
    Dropout(0.2),
    Dense(16, activation="relu"),
    Dense(3,  activation="softmax"),
], name="TrafficRNN_RealData")

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)
model.summary()

early_stop = EarlyStopping(monitor="val_loss", patience=3,
                           restore_best_weights=True)

print("\n[5/6] Training ...")
history = model.fit(
    X_train, y_train_cat,
    epochs=15,
    batch_size=64,
    validation_split=0.15,
    callbacks=[early_stop],
    verbose=1,
)

model.save("model/traffic_rnn.keras")
print("\n   Model saved -> model/traffic_rnn.keras")

# ════════════════════════════════════════════════════════════
# 6.  Evaluate
# ════════════════════════════════════════════════════════════
print("\n[6/6] Evaluating ...")

y_pred_prob = model.predict(X_test, verbose=0)
y_pred      = np.argmax(y_pred_prob, axis=1)
acc         = accuracy_score(y_test, y_pred)

print(f"\n   Test Accuracy : {acc*100:.2f}%")
print("\n   Classification Report:")
print(classification_report(y_test, y_pred,
      labels=[0,1,2], target_names=["Low","Medium","High"],
      zero_division=0))

# ════════════════════════════════════════════════════════════
# 7.  Evaluation Graphs
# ════════════════════════════════════════════════════════════
os.makedirs("graphs", exist_ok=True)
DARK_BG = "#0f172a"
plt.style.use("dark_background")

# Accuracy
fig, ax = plt.subplots(figsize=(9, 5), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)
ax.plot(history.history["accuracy"],     color="#38bdf8", lw=2.5, label="Train", marker="o", ms=4)
ax.plot(history.history["val_accuracy"], color="#a78bfa", lw=2.5, label="Val",   marker="s", ms=4)
ax.set_title("Model Accuracy  (Real I-94 Data)", fontsize=15, color="white", pad=12)
ax.set_xlabel("Epoch", color="#94a3b8"); ax.set_ylabel("Accuracy", color="#94a3b8")
ax.tick_params(colors="#94a3b8"); ax.legend(framealpha=0.15, labelcolor="white")
ax.grid(alpha=0.15)
for sp in ax.spines.values(): sp.set_edgecolor("#1e293b")
plt.tight_layout(); plt.savefig("graphs/accuracy.png", dpi=150, bbox_inches="tight"); plt.close()

# Loss
fig, ax = plt.subplots(figsize=(9, 5), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)
ax.plot(history.history["loss"],     color="#f472b6", lw=2.5, label="Train", marker="o", ms=4)
ax.plot(history.history["val_loss"], color="#fb923c", lw=2.5, label="Val",   marker="s", ms=4)
ax.set_title("Model Loss  (Real I-94 Data)", fontsize=15, color="white", pad=12)
ax.set_xlabel("Epoch", color="#94a3b8"); ax.set_ylabel("Loss", color="#94a3b8")
ax.tick_params(colors="#94a3b8"); ax.legend(framealpha=0.15, labelcolor="white")
ax.grid(alpha=0.15)
for sp in ax.spines.values(): sp.set_edgecolor("#1e293b")
plt.tight_layout(); plt.savefig("graphs/loss.png", dpi=150, bbox_inches="tight"); plt.close()

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(7, 6), facecolor=DARK_BG); ax.set_facecolor(DARK_BG)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Low","Medium","High"],
            yticklabels=["Low","Medium","High"],
            ax=ax, linewidths=0.5, linecolor="#1e293b",
            annot_kws={"size":14,"color":"white"}, cbar_kws={"shrink":0.8})
ax.set_title("Confusion Matrix  (Real I-94 Data)", fontsize=15, color="white", pad=12)
ax.set_xlabel("Predicted", color="#94a3b8", fontsize=12)
ax.set_ylabel("Actual",    color="#94a3b8", fontsize=12)
ax.tick_params(colors="#94a3b8")
plt.tight_layout(); plt.savefig("graphs/confusion_matrix.png", dpi=150, bbox_inches="tight"); plt.close()

print("   Saved: graphs/accuracy.png")
print("   Saved: graphs/loss.png")
print("   Saved: graphs/confusion_matrix.png")

print("\n" + "=" * 60)
print("  [OK] Training complete!  Run: python app.py")
print("=" * 60)
