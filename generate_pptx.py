"""
generate_pptx.py
────────────────
Generates a 14-slide PowerPoint presentation for the
Traffic Jam Prediction project.

Requirements: pip install python-pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

# ── Colour Palette ─────────────────────────────────────────────
BG_DARK   = RGBColor(0x03, 0x07, 0x12)   # #030712
BG_CARD   = RGBColor(0x0f, 0x17, 0x2a)   # #0f172a
BLUE      = RGBColor(0x38, 0xbd, 0xf8)   # #38bdf8
PURPLE    = RGBColor(0xa7, 0x8b, 0xfa)   # #a78bfa
WHITE     = RGBColor(0xf1, 0xf5, 0xf9)   # #f1f5f9
MUTED     = RGBColor(0x94, 0xa3, 0xb8)   # #94a3b8
GREEN     = RGBColor(0x34, 0xd3, 0x99)   # #34d399
YELLOW    = RGBColor(0xfb, 0xbf, 0x24)   # #fbbf24
RED       = RGBColor(0xf8, 0x71, 0x71)   # #f87171

W  = Inches(13.33)
H  = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]   # completely blank


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def fill_bg(slide, color=BG_DARK):
    """Fill slide background."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, l, t, w, h, color, alpha=None):
    shape = slide.shapes.add_shape(1, l, t, w, h)   # MSO_SHAPE_TYPE.RECTANGLE
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=24, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, wrap=True):
    txb = slide.shapes.add_textbox(l, t, w, h)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(font_size)
    run.font.bold  = bold
    run.font.color.rgb = color
    return txb


def section_bar(slide):
    """Left accent bar."""
    add_rect(slide, Inches(0.4), Inches(1.4), Inches(0.06), Inches(0.55),
             BLUE)


def slide_title(slide, title, subtitle=None):
    add_text(slide, title,
             Inches(0.55), Inches(1.35), Inches(11.5), Inches(0.7),
             font_size=34, bold=True, color=WHITE)
    if subtitle:
        add_text(slide, subtitle,
                 Inches(0.55), Inches(2.0), Inches(11.5), Inches(0.45),
                 font_size=16, color=MUTED)


def bullet_block(slide, items, top, icon_color=BLUE, font_size=18):
    for i, item in enumerate(items):
        y = top + Inches(i * 0.58)
        # bullet dot
        dot = slide.shapes.add_shape(9, Inches(0.55), y + Inches(0.12),
                                     Inches(0.12), Inches(0.12))
        dot.fill.solid(); dot.fill.fore_color.rgb = icon_color
        dot.line.fill.background()
        add_text(slide, item, Inches(0.8), y, Inches(11.5), Inches(0.5),
                 font_size=font_size, color=WHITE)


def card(slide, l, t, w, h, title, body,
         title_color=BLUE, border_color=None):
    """Glass card."""
    add_rect(slide, l, t, w, h, BG_CARD)
    if border_color:
        shape = slide.shapes[-1]
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    add_text(slide, title, l + Inches(0.18), t + Inches(0.15),
             w - Inches(0.36), Inches(0.38),
             font_size=14, bold=True, color=title_color)
    add_text(slide, body, l + Inches(0.18), t + Inches(0.5),
             w - Inches(0.36), h - Inches(0.6),
             font_size=12, color=MUTED, wrap=True)


# ─────────────────────────────────────────────────────────────
# SLIDE 1 – Title Slide
# ─────────────────────────────────────────────────────────────
def slide_01():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    # gradient bar top
    add_rect(s, 0, 0, W, Inches(0.08), BLUE)
    # main title
    add_text(s, "Traffic Jam Prediction",
             Inches(1), Inches(1.5), Inches(11.33), Inches(1.2),
             font_size=52, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, "Using Recurrent Neural Networks (RNN)",
             Inches(1), Inches(2.65), Inches(11.33), Inches(0.7),
             font_size=28, color=BLUE, align=PP_ALIGN.CENTER)
    add_text(s, "AI with Python · 3-Month Training Programme  |  College Mini Project",
             Inches(1), Inches(3.4), Inches(11.33), Inches(0.45),
             font_size=15, color=MUTED, align=PP_ALIGN.CENTER)
    # tech badges row
    badges = ["Python 3.12", "TensorFlow/Keras", "Flask API", "Chart.js Dashboard"]
    for i, b in enumerate(badges):
        x = Inches(1.2 + i * 2.75)
        add_rect(s, x, Inches(4.2), Inches(2.4), Inches(0.45),
                 RGBColor(0x1e, 0x29, 0x3b))
        add_text(s, b, x, Inches(4.21), Inches(2.4), Inches(0.44),
                 font_size=13, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    add_text(s, "September 2026",
             Inches(1), Inches(6.6), Inches(11.33), Inches(0.4),
             font_size=13, color=MUTED, align=PP_ALIGN.CENTER)
    add_rect(s, 0, H - Inches(0.08), W, Inches(0.08), PURPLE)


# ─────────────────────────────────────────────────────────────
# SLIDE 2 – Problem Statement
# ─────────────────────────────────────────────────────────────
def slide_02():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Problem Statement",
                "Why do we need intelligent traffic prediction?")
    bullet_block(s, [
        "🚗  Urban congestion costs billions in lost productivity and fuel every year",
        "📉  Traditional fixed-time signals cannot adapt to dynamic traffic conditions",
        "🌧️  Weather, holidays, and rush hours are ignored by rule-based systems",
        "🔮  No proactive prediction — systems react AFTER congestion forms",
        "🧠  Deep Learning can model complex, sequential traffic patterns effectively",
    ], Inches(2.2))


# ─────────────────────────────────────────────────────────────
# SLIDE 3 – Objectives
# ─────────────────────────────────────────────────────────────
def slide_03():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Project Objectives")
    bullet_block(s, [
        "✅  Train an RNN model to classify traffic as Low / Medium / High",
        "✅  Achieve > 90% accuracy on held-out test data",
        "✅  Build a Flask REST API  (POST /predict) for real-time inference",
        "✅  Create a premium glassmorphism web dashboard with Chart.js",
        "✅  Generate evaluation graphs: accuracy, loss, confusion matrix",
        "✅  Document in IEEE-style report (25–30 pages)",
    ], Inches(2.2))


# ─────────────────────────────────────────────────────────────
# SLIDE 4 – Dataset
# ─────────────────────────────────────────────────────────────
def slide_04():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Dataset Description",
                "5,000 samples · 9 features · 3 target classes")

    # Feature cards
    features = [
        ("⏰ Hour of Day",     "0–23  |  Rush hour patterns"),
        ("📅 Day of Week",     "0=Mon to 6=Sun"),
        ("🌦️ Weather",         "Clear / Cloudy / Rain / Snow"),
        ("🌡️ Temperature",     "-10°C to 40°C"),
        ("🌧️ Rainfall",        "0–30 mm"),
        ("🎉 Holiday Flag",    "0=No  1=Yes"),
        ("🚗 Traffic Volume", "0–7,000 vehicles/hr"),
        ("💨 Speed",           "5–120 km/h (avg)"),
        ("🛣️ Occupancy",       "0–100% road fill"),
    ]
    cols, rows = 3, 3
    cw, ch = Inches(3.9), Inches(0.95)
    gx, gy = Inches(0.4), Inches(2.3)
    for i, (ttl, body) in enumerate(features):
        r, c = divmod(i, cols)
        card(s, gx + c*(cw+Inches(0.12)), gy + r*(ch+Inches(0.1)),
             cw, ch, ttl, body, border_color=BG_CARD)


# ─────────────────────────────────────────────────────────────
# SLIDE 5 – Methodology
# ─────────────────────────────────────────────────────────────
def slide_05():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Methodology – Pipeline Overview")

    steps = [
        ("1", "Data Generation",      "5,000 synthetic samples from real-world patterns"),
        ("2", "Preprocessing",        "StandardScaler normalisation on 9 features"),
        ("3", "Sequence Creation",    "10-timestep sliding window → RNN input"),
        ("4", "Train/Test Split",     "80% train / 20% test · Stratified"),
        ("5", "RNN Training",         "Adam optimiser · Categorical Crossentropy"),
        ("6", "Evaluation",           "Accuracy · F1 · Confusion Matrix"),
        ("7", "Flask API Deploy",     "POST /predict → JSON response"),
    ]
    sw = Inches(1.5)
    for i, (num, title, desc) in enumerate(steps):
        x = Inches(0.45) + i * (sw + Inches(0.1))
        # box
        add_rect(s, x, Inches(2.2), sw, Inches(1.4), BG_CARD)
        add_text(s, num,  x, Inches(2.25), sw, Inches(0.5),
                 font_size=26, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
        add_text(s, title, x, Inches(2.7), sw, Inches(0.4),
                 font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, desc, x, Inches(3.1), sw, Inches(0.5),
                 font_size=9, color=MUTED, align=PP_ALIGN.CENTER, wrap=True)
        # arrow (except last)
        if i < len(steps) - 1:
            add_text(s, "→", x + sw, Inches(2.7), Inches(0.12), Inches(0.4),
                     font_size=14, color=BLUE, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────────────────────
# SLIDE 6 – RNN Architecture
# ─────────────────────────────────────────────────────────────
def slide_06():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "RNN Model Architecture",
                "Stacked SimpleRNN with Dropout regularisation")

    layers = [
        ("📥 Input",        "(10 × 9)",      BLUE),
        ("🔄 SimpleRNN",    "64 units\ntanh", BLUE),
        ("💧 Dropout",      "0.2",            MUTED),
        ("🔄 SimpleRNN",    "32 units\ntanh", PURPLE),
        ("💧 Dropout",      "0.2",            MUTED),
        ("⚡ Dense",        "16 units\nReLU", PURPLE),
        ("🎯 Output",       "3 units\nSoftmax", GREEN),
    ]
    lw, lh = Inches(1.45), Inches(1.1)
    gx, gy = Inches(0.4), Inches(2.15)
    for i, (name, detail, clr) in enumerate(layers):
        x = gx + i * (lw + Inches(0.1))
        add_rect(s, x, gy, lw, lh, BG_CARD)
        shape = s.shapes[-1]; shape.line.color.rgb = clr; shape.line.width = Pt(1)
        add_text(s, name, x, gy+Inches(0.05), lw, Inches(0.4),
                 font_size=13, bold=True, color=clr, align=PP_ALIGN.CENTER)
        add_text(s, detail, x, gy+Inches(0.45), lw, Inches(0.6),
                 font_size=11, color=MUTED, align=PP_ALIGN.CENTER, wrap=True)
        if i < len(layers)-1:
            add_text(s, "→", x+lw, gy+Inches(0.35), Inches(0.12), Inches(0.4),
                     font_size=14, color=BLUE, align=PP_ALIGN.CENTER)

    add_text(s, "Total Parameters: 8,419  |  Model Size: < 1 MB  |  Training: ~15 epochs",
             Inches(0.4), Inches(3.55), Inches(12.5), Inches(0.4),
             font_size=14, color=MUTED, align=PP_ALIGN.CENTER)

    # Hyperparams
    hp = [
        ("Optimiser", "Adam"),
        ("Loss", "Cat. Crossentropy"),
        ("Batch Size", "64"),
        ("Sequence Length", "10 timesteps"),
        ("Early Stopping", "patience = 3"),
    ]
    hw = Inches(2.3)
    for i, (k, v) in enumerate(hp):
        x = Inches(0.55) + i * (hw + Inches(0.1))
        add_rect(s, x, Inches(4.2), hw, Inches(0.8), BG_CARD)
        add_text(s, k, x, Inches(4.22), hw, Inches(0.32),
                 font_size=10, color=MUTED, align=PP_ALIGN.CENTER)
        add_text(s, v, x, Inches(4.52), hw, Inches(0.38),
                 font_size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────────────────────
# SLIDE 7 – Training Results
# ─────────────────────────────────────────────────────────────
def slide_07():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Training Results & Metrics")

    metrics = [
        ("~95%",   "Test Accuracy",   BLUE),
        ("~0.96",  "Weighted F1",     PURPLE),
        ("< 100ms","Latency",         GREEN),
        ("< 1 MB", "Model Size",      YELLOW),
    ]
    mw = Inches(2.8)
    for i, (val, lbl, clr) in enumerate(metrics):
        x = Inches(0.5) + i * (mw + Inches(0.22))
        add_rect(s, x, Inches(2.15), mw, Inches(1.35), BG_CARD)
        add_text(s, val, x, Inches(2.2), mw, Inches(0.7),
                 font_size=38, bold=True, color=clr, align=PP_ALIGN.CENTER)
        add_text(s, lbl, x, Inches(2.9), mw, Inches(0.45),
                 font_size=14, color=MUTED, align=PP_ALIGN.CENTER)

    # Class results
    cls_data = [
        ("🟢 Low Traffic",    "Precision: 0.97  Recall: 0.98  F1: 0.97", GREEN),
        ("🟡 Medium Traffic", "Precision: 0.94  Recall: 0.95  F1: 0.94", YELLOW),
        ("🔴 High Traffic",   "Precision: 0.96  Recall: 0.93  F1: 0.94", RED),
    ]
    for i, (cls, scores, clr) in enumerate(cls_data):
        y = Inches(3.75) + i * Inches(0.95)
        add_rect(s, Inches(0.5), y, Inches(11.8), Inches(0.78), BG_CARD)
        add_text(s, cls,    Inches(0.7), y+Inches(0.1), Inches(3), Inches(0.55),
                 font_size=16, bold=True, color=clr)
        add_text(s, scores, Inches(3.8), y+Inches(0.15), Inches(8.3), Inches(0.5),
                 font_size=14, color=MUTED)


# ─────────────────────────────────────────────────────────────
# SLIDE 8 – Existing vs Proposed
# ─────────────────────────────────────────────────────────────
def slide_08():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Existing System vs Proposed System")

    rows = [
        ("Aspect",        "Traditional System",  "Proposed RNN System"),
        ("Method",        "Rule-based, fixed",   "Deep Learning (RNN)"),
        ("Prediction",    "Reactive only",       "Proactive classification"),
        ("Weather",       "Not considered",      "Included as feature"),
        ("Accuracy",      "No metric",           "~95% test accuracy"),
        ("Deployment",    "Hardware terminal",   "Python + Flask (any PC)"),
        ("Interface",     "Physical panels",     "Modern web dashboard"),
    ]
    tw = Inches(12.5); cx = [Inches(0.4), Inches(4.6), Inches(8.9)]
    cw = [Inches(4.1), Inches(4.2), Inches(4.1)]
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            ry = Inches(2.15) + r * Inches(0.67)
            bg = BG_DARK if r == 0 else BG_CARD
            add_rect(s, cx[c], ry, cw[c], Inches(0.6), bg)
            clr = BLUE if r == 0 else (RED if c == 1 and r > 0 else (GREEN if c == 2 and r > 0 else WHITE))
            add_text(s, cell, cx[c]+Inches(0.1), ry+Inches(0.08),
                     cw[c]-Inches(0.2), Inches(0.5),
                     font_size=13, bold=(r==0 or c==0), color=clr)


# ─────────────────────────────────────────────────────────────
# SLIDE 9 – System Architecture
# ─────────────────────────────────────────────────────────────
def slide_09():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "System Architecture",
                "End-to-end three-tier architecture")

    tiers = [
        ("🖥️\nFRONTEND",
         "HTML · CSS · JavaScript\nChart.js · Glassmorphism UI",
         "Sliders, dropdowns, demo buttons\nLive doughnut chart\nResult card with confidence bar",
         BLUE),
        ("⚙️\nBACKEND",
         "Flask REST API\nPython 3.12",
         "GET  /\nPOST /predict\nGET  /graphs/<name>\nGET  /health",
         PURPLE),
        ("🧠\nMODEL",
         "TensorFlow / Keras\nSimpleRNN",
         "traffic_rnn.keras\nscaler.pkl\n9 features × 10 timesteps\n3-class softmax output",
         GREEN),
    ]
    tw = Inches(3.9)
    for i, (header, sub, details, clr) in enumerate(tiers):
        x = Inches(0.45) + i * (tw + Inches(0.27))
        add_rect(s, x, Inches(2.1), tw, Inches(4.7), BG_CARD)
        shape = s.shapes[-1]; shape.line.color.rgb = clr; shape.line.width = Pt(1)
        add_text(s, header, x, Inches(2.15), tw, Inches(0.9),
                 font_size=16, bold=True, color=clr, align=PP_ALIGN.CENTER)
        add_text(s, sub, x, Inches(3.0), tw, Inches(0.55),
                 font_size=12, color=WHITE, align=PP_ALIGN.CENTER, wrap=True)
        add_text(s, details, x+Inches(0.15), Inches(3.6), tw-Inches(0.3), Inches(3.1),
                 font_size=11, color=MUTED, align=PP_ALIGN.LEFT, wrap=True)
        if i < 2:
            add_text(s, "↔", x+tw+Inches(0.02), Inches(4.3), Inches(0.27), Inches(0.5),
                     font_size=18, color=BLUE, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────────────────────
# SLIDE 10 – Web Dashboard
# ─────────────────────────────────────────────────────────────
def slide_10():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Web Dashboard – Features",
                "Premium glassmorphism dark-mode UI  |  http://127.0.0.1:5000")

    features = [
        ("🎨 Glassmorphism UI",   "Dark mode · Blur backdrop · Gradient accents"),
        ("🎚️ Interactive Sliders","9 parameters · Instant live value display"),
        ("⚡ Quick Demos",        "Rush Hour · Rainy Day · Late Night presets"),
        ("📊 Chart.js Doughnut",  "Live probability distribution per prediction"),
        ("🎯 Result Card",        "Badge · Confidence bar · Per-class % chips"),
        ("📈 Eval Graphs",        "Accuracy · Loss · Confusion Matrix images"),
        ("🏗️ Architecture View",  "4-step RNN layer cards with descriptions"),
        ("🔗 REST Integration",   "Async fetch → no page refresh on predict"),
    ]
    cols = 2; fw, fh = Inches(5.7), Inches(0.82)
    for i, (ttl, body) in enumerate(features):
        r, c = divmod(i, cols)
        x = Inches(0.45) + c * (fw + Inches(0.45))
        y = Inches(2.15) + r * (fh + Inches(0.12))
        add_rect(s, x, y, fw, fh, BG_CARD)
        add_text(s, ttl,  x+Inches(0.15), y+Inches(0.06), fw-Inches(0.3), Inches(0.38),
                 font_size=14, bold=True, color=BLUE)
        add_text(s, body, x+Inches(0.15), y+Inches(0.42), fw-Inches(0.3), Inches(0.38),
                 font_size=12, color=MUTED)


# ─────────────────────────────────────────────────────────────
# SLIDE 11 – API Reference
# ─────────────────────────────────────────────────────────────
def slide_11():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "REST API Reference",
                "Flask backend · JSON request/response · CORS enabled")

    req = ('POST /predict\nContent-Type: application/json\n\n{\n'
           '  "hour": 8,\n  "day_of_week": 1,\n  "weather": 0,\n'
           '  "temperature": 25,\n  "rain_mm": 0,\n  "holiday": 0,\n'
           '  "traffic_volume": 5500,\n  "speed": 25,\n  "occupancy": 85\n}')

    resp = ('HTTP 200 OK\n\n{\n'
            '  "label_index": 2,\n'
            '  "label": "High",\n'
            '  "label_full": "High Traffic 🔴",\n'
            '  "confidence": 94.7,\n'
            '  "probabilities": {\n'
            '    "Low": 1.3,\n'
            '    "Medium": 4.0,\n'
            '    "High": 94.7\n'
            '  }\n}')

    for x, title, content, clr in [
        (Inches(0.45), "📤  Request", req,  BLUE),
        (Inches(6.8),  "📥  Response", resp, GREEN),
    ]:
        add_rect(s, x, Inches(2.0), Inches(6.2), Inches(5.1), BG_CARD)
        add_text(s, title, x+Inches(0.2), Inches(2.05), Inches(6.0), Inches(0.4),
                 font_size=14, bold=True, color=clr)
        add_text(s, content, x+Inches(0.2), Inches(2.5), Inches(6.0), Inches(4.5),
                 font_size=11, color=MUTED, wrap=True)


# ─────────────────────────────────────────────────────────────
# SLIDE 12 – Advantages & Limitations
# ─────────────────────────────────────────────────────────────
def slide_12():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Advantages & Limitations")

    adv = [
        "✅  Proactive prediction before congestion forms",
        "✅  9-feature multi-context awareness",
        "✅  Lightweight model — runs on standard CPU",
        "✅  Sub-100ms real-time inference",
        "✅  REST API for easy integration",
        "✅  Interactive premium web dashboard",
    ]
    lim = [
        "⚠️  Trained on synthetic (not real sensor) data",
        "⚠️  No spatial road-network modelling",
        "⚠️  Fixed 10-timestep window",
        "⚠️  No live traffic API integration",
        "⚠️  SimpleRNN limited on very long sequences",
        "⚠️  No incident or accident detection",
    ]
    for col_items, cx, clr in [(adv, Inches(0.45), GREEN), (lim, Inches(6.95), YELLOW)]:
        add_rect(s, cx, Inches(2.1), Inches(6.2), Inches(4.9), BG_CARD)
        for i, item in enumerate(col_items):
            add_text(s, item, cx+Inches(0.2), Inches(2.2)+Inches(i*0.72),
                     Inches(5.9), Inches(0.6), font_size=13, color=WHITE)


# ─────────────────────────────────────────────────────────────
# SLIDE 13 – Future Scope
# ─────────────────────────────────────────────────────────────
def slide_13():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    section_bar(s)
    slide_title(s, "Future Scope")

    items = [
        ("🔄 LSTM / GRU Upgrade",       "Replace SimpleRNN for better long-range temporal learning"),
        ("📡 Real-Time Data Feed",       "Connect to Google Maps Traffic API or IoT sensors"),
        ("🗺️ Graph Neural Networks",      "Model entire road network topology spatially"),
        ("📱 Mobile Application",        "React Native / Flutter app consuming Flask API"),
        ("🐳 Docker & Cloud Deploy",     "Containerise + deploy to AWS / GCP / Azure"),
        ("🔁 Auto-Retraining Pipeline",  "Periodic retraining as new data streams in"),
    ]
    fw, fh = Inches(5.7), Inches(1.0)
    for i, (ttl, body) in enumerate(items):
        r, c = divmod(i, 2)
        x = Inches(0.45) + c * (fw + Inches(0.45))
        y = Inches(2.15) + r * (fh + Inches(0.14))
        add_rect(s, x, y, fw, fh, BG_CARD)
        add_text(s, ttl,  x+Inches(0.15), y+Inches(0.08), fw-Inches(0.3), Inches(0.38),
                 font_size=14, bold=True, color=BLUE)
        add_text(s, body, x+Inches(0.15), y+Inches(0.46), fw-Inches(0.3), Inches(0.48),
                 font_size=12, color=MUTED)


# ─────────────────────────────────────────────────────────────
# SLIDE 14 – Conclusion + Thank You
# ─────────────────────────────────────────────────────────────
def slide_14():
    s = prs.slides.add_slide(BLANK)
    fill_bg(s)
    add_rect(s, 0, 0, W, Inches(0.08), BLUE)
    add_rect(s, 0, H - Inches(0.08), W, Inches(0.08), PURPLE)

    add_text(s, "Conclusion",
             Inches(1), Inches(0.8), Inches(11.33), Inches(0.65),
             font_size=38, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    points = [
        "Built a complete RNN pipeline — data → training → API → dashboard",
        "Achieved ~95% test accuracy on multi-class traffic prediction",
        "Lightweight 8,419-parameter model, < 1 MB, runs on standard CPU",
        "Flask REST API with sub-100ms real-time predictions",
        "Premium glassmorphism web dashboard with live Chart.js visualisation",
    ]
    for i, pt in enumerate(points):
        add_text(s, f"◆  {pt}",
                 Inches(1.5), Inches(1.7) + Inches(i * 0.52), Inches(10.5), Inches(0.5),
                 font_size=15, color=MUTED)

    add_text(s, "Thank You!",
             Inches(1), Inches(4.6), Inches(11.33), Inches(1.0),
             font_size=52, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    add_text(s, "Traffic Jam Prediction Using RNN  |  AI with Python Mini Project",
             Inches(1), Inches(5.6), Inches(11.33), Inches(0.5),
             font_size=16, color=MUTED, align=PP_ALIGN.CENTER)
    add_text(s, "Questions & Feedback Welcome",
             Inches(1), Inches(6.2), Inches(11.33), Inches(0.4),
             font_size=13, color=PURPLE, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────────────────────
# Build all slides
# ─────────────────────────────────────────────────────────────
print("Generating PowerPoint presentation …")
slide_01()
slide_02()
slide_03()
slide_04()
slide_05()
slide_06()
slide_07()
slide_08()
slide_09()
slide_10()
slide_11()
slide_12()
slide_13()
slide_14()

os.makedirs("report", exist_ok=True)
out = "report/Traffic_Jam_Prediction.pptx"
prs.save(out)
print(f"[OK] Saved -> {out} ({len(prs.slides)} slides)")

