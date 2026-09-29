"""
generate_block_diagram.py
=========================
Renders a publication-quality architectural block diagram for the
Traffic Jam Prediction RNN System using Matplotlib.
Saved as: graphs/block_diagram.png (High Resolution 300 DPI)
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_block_diagram():
    fig, ax = plt.subplots(figsize=(11, 14), dpi=300)
    fig.patch.set_facecolor("#FAF9F6")
    ax.set_facecolor("#FAF9F6")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Colors
    c_navy      = "#1F2A44"
    c_blue      = "#2E74B5"
    c_orange    = "#E8730A"
    c_card_bg   = "#FFFFFF"
    c_card_edge = "#D1D5DB"
    c_accent_bg = "#F3EFEA"
    c_text_main = "#1A202C"
    c_text_sub  = "#4A5568"

    # Title Banner
    ax.text(50, 97, "TRAFFIC JAM PREDICTION SYSTEM USING RNN",
            ha="center", va="center", fontsize=15, weight="bold", color=c_navy, fontfamily="sans-serif")
    ax.text(50, 94.8, "End-to-End Deep Learning Architecture & Dataflow Pipeline · GyanAstra Technologies",
            ha="center", va="center", fontsize=9.5, color=c_orange, weight="bold", fontfamily="sans-serif")

    # Helper function to draw rounded card
    def draw_card(x, y, w, h, title, lines, icon="◈", badge=None, border_color=c_blue, bg_color="#FFFFFF"):
        # Shadow
        shadow = patches.FancyBboxPatch(
            (x + 0.4, y - 0.4), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.2",
            facecolor="#E2E8F0", edgecolor="none", zorder=1
        )
        ax.add_patch(shadow)

        # Main Box
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.2",
            facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=2
        )
        ax.add_patch(card)

        # Header Pill
        header_y = y + h - 1.8
        ax.text(x + 2, header_y, f"{icon}  {title}",
                ha="left", va="center", fontsize=10.5, weight="bold", color=c_navy, zorder=3, fontfamily="sans-serif")

        if badge:
            badge_box = patches.FancyBboxPatch(
                (x + w - len(badge) * 1.05 - 2, header_y - 0.9), len(badge) * 1.05 + 1.2, 1.8,
                boxstyle="round,pad=0.2,rounding_size=0.5",
                facecolor="#FEF3EB", edgecolor=c_orange, linewidth=1, zorder=3
            )
            ax.add_patch(badge_box)
            ax.text(x + w - 1.4, header_y, badge,
                    ha="right", va="center", fontsize=7.5, weight="bold", color=c_orange, zorder=4, fontfamily="sans-serif")

        # Separator line
        ax.plot([x + 1.5, x + w - 1.5], [y + h - 3.2, y + h - 3.2], color="#E2E8F0", lw=1, zorder=3)

        # Content lines
        start_y = y + h - 4.6
        line_spacing = (h - 5.0) / max(len(lines), 1)
        for i, line in enumerate(lines):
            ax.text(x + 2.5, start_y - (i * line_spacing), line,
                    ha="left", va="center", fontsize=8.5, color=c_text_sub, zorder=3, fontfamily="sans-serif")

    # Helper for flow arrows
    def draw_arrow(x1, y1, x2, y2, label=None):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=c_blue,
                lw=2,
                mutation_scale=14,
                shrinkA=2, shrinkB=2
            ),
            zorder=5
        )
        if label:
            mid_x = (x1 + x2) / 2 + 1.5
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y, label, ha="left", va="center", fontsize=7.5, color=c_blue, weight="bold", zorder=6)

    # ─────────────────────────────────────────────────────────────
    # Tier 1: Data Ingestion
    # ─────────────────────────────────────────────────────────────
    draw_card(
        x=15, y=81, w=70, h=9.5,
        title="TIER 1: RAW SENSOR TELEMETRY & INGESTION",
        badge="48,204 Observations",
        icon="[T1]",
        border_color="#3B82F6",
        lines=[
            "• Data Source: Metro Interstate Traffic Volume Dataset (UCI Machine Learning Repository)",
            "• Collection: Minnesota DOT ATR 301 Sensor on Westbound Interstate 94 (I-94, 2012–2018)",
            "• Raw Attributes: date_time, traffic_volume, weather_main, temp, rain_1h, clouds_all, holiday"
        ]
    )

    draw_arrow(50, 81, 50, 74.5, "Raw Telemetry")

    # ─────────────────────────────────────────────────────────────
    # Tier 2: Feature Engineering & Preprocessing
    # ─────────────────────────────────────────────────────────────
    draw_card(
        x=15, y=65, w=70, h=9.5,
        title="TIER 2: MULTI-MODAL FEATURE ENGINEERING & CLEANING",
        badge="9 Features",
        icon="[T2]",
        border_color="#10B981",
        lines=[
            "• Temporal Extraction: Hour of Day (0–23), Day of Week (0–6), Month (1–12), Weekend Flag",
            "• Weather Mapping: Clear (0), Cloudy (1), Rainy/Storm (2), Snow (3), Fog/Mist (4)",
            "• Cleaning: Rain clipping (0–50mm/h), Kelvin to Celsius (temp_c), Forward-fill sequential gaps"
        ]
    )

    draw_arrow(50, 65, 50, 58.5, "Clean Numerical Features")

    # ─────────────────────────────────────────────────────────────
    # Tier 3: Sequential Windowing & Normalization
    # ─────────────────────────────────────────────────────────────
    draw_card(
        x=15, y=49, w=70, h=9.5,
        title="TIER 3: NORMALIZATION & 24-HOUR SEQUENTIAL TENSOR",
        badge="Window = 24h",
        icon="[T3]",
        border_color="#F59E0B",
        lines=[
            "• StandardScaler Normalization: z = (x - μ) / σ for zero mean and unit variance",
            "• Sliding Window Transformation: 24 consecutive hours fed into each temporal step",
            "• Sequential Input Tensor: Shape (Batch_Size, 24 Timesteps, 9 Multi-Variate Features)"
        ]
    )

    draw_arrow(50, 49, 50, 42.5, "3D Tensor: (N, 24, 9)")

    # ─────────────────────────────────────────────────────────────
    # Tier 4: Deep Recurrent Neural Network (RNN)
    # ─────────────────────────────────────────────────────────────
    draw_card(
        x=15, y=24, w=70, h=18.5,
        title="TIER 4: DEEP RECURRENT NEURAL NETWORK (SimpleRNN)",
        badge="Keras / TensorFlow",
        icon="[T4]",
        border_color="#8B5CF6",
        bg_color="#FFFFFF",
        lines=[
            "  Layer 1: SimpleRNN (64 Units, Tanh Activation, return_sequences=True)",
            "  ↳ Captures low-level diurnal temporal dynamics across all 24 sequence steps",
            "  Regularization 1: Dropout (p = 0.2) to prevent co-adaptation and overfitting",
            "  Layer 2: SimpleRNN (32 Units, Tanh Activation, return_sequences=False)",
            "  ↳ Compresses sequence dynamics into a dense 32-dimensional state vector",
            "  Regularization 2: Dropout (p = 0.2)",
            "  Layer 3: Dense Feature Combination (16 Units, ReLU Activation)",
            "  Output Layer: Dense Softmax (3 Units) → Categorical Congestion Probabilities"
        ]
    )

    draw_arrow(50, 24, 50, 18.5, "Softmax Probabilities: [P_Low, P_Med, P_High]")

    # ─────────────────────────────────────────────────────────────
    # Tier 5: Output Classification & Full-Stack Deployment
    # ─────────────────────────────────────────────────────────────
    # Left Box: Classification Targets
    draw_card(
        x=8, y=4.5, w=39, h=14,
        title="PREDICTIVE CLASSIFICATION",
        badge="3 Classes",
        icon="[T5a]",
        border_color="#E8730A",
        lines=[
            "• Low Traffic:    < 1,500 veh/hr",
            "    (Free-flowing speeds > 55 mph)",
            "• Medium Traffic: 1,500–4,500 veh/hr",
            "    (Steady flow with light braking)",
            "• High Traffic:   > 4,500 veh/hr",
            "    (Rush hour stop-and-go delays)"
        ]
    )

    # Right Box: Deployment & Dashboard
    draw_card(
        x=53, y=4.5, w=39, h=14,
        title="DEPLOYMENT & USER DASHBOARD",
        badge="Sub-50ms CPU",
        icon="[T5b]",
        border_color="#0EA5E9",
        lines=[
            "• Flask REST API: POST /api/predict",
            "• High-Speed Inference: < 50ms per run",
            "• Soft-Light Modern Dashboard",
            "• Live Animated Chart.js Doughnut",
            "• Contextual Smart Travel Advice"
        ]
    )

    # Sub-arrows from Tier 4 to Tier 5
    draw_arrow(40, 24, 27.5, 18.5)
    draw_arrow(60, 24, 72.5, 18.5)

    plt.tight_layout()
    os.makedirs("graphs", exist_ok=True)
    out_file = "graphs/block_diagram.png"
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] Block diagram created successfully -> {out_file}")

if __name__ == "__main__":
    create_block_diagram()
