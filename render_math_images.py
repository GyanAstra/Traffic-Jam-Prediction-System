"""
render_math_images.py
=====================
Renders high-resolution, transparent LaTeX mathematical equations
for inclusion in reports, documentation, and slides.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def render_equation(latex_str, filename, fontsize=16, dpi=300):
    fig = plt.figure(figsize=(0.1, 0.1), dpi=dpi)
    text = fig.text(0, 0, latex_str, fontsize=fontsize, usetex=False,
                    color="#1F2A44", fontfamily="sans-serif")
    
    # Render without axes
    fig.patch.set_alpha(0.0)
    plt.axis("off")
    
    # Save with tight bounding box
    fig.canvas.draw()
    bbox = text.get_window_extent(fig.canvas.get_renderer())
    bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())
    
    # Add a slight padding
    pad = 0.08
    bbox_expanded = matplotlib.transforms.Bbox.from_bounds(
        bbox_inches.x0 - pad, bbox_inches.y0 - pad,
        bbox_inches.width + 2*pad, bbox_inches.height + 2*pad
    )
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, dpi=dpi, bbox_inches=bbox_expanded, transparent=True)
    plt.close()
    print(f"[OK] Rendered -> {filename}")

def main():
    equations = [
        (r"$z = \frac{x - \mu}{\sigma}$", "graphs/equations/eq_zscore.png", 18),
        (r"$h_t = \tanh\left(W_{ih} \cdot x_t + b_{ih} + W_{hh} \cdot h_{t-1} + b_{hh}\right)$", "graphs/equations/eq_rnn_cell.png", 18),
        (r"$P(y = c \mid X) = \frac{e^{z_c}}{\sum_{j=1}^{C} e^{z_j}}$", "graphs/equations/eq_softmax.png", 18),
        (r"$\mathcal{L} = -\sum_{c=1}^{C} y_c \log(\hat{y}_c)$", "graphs/equations/eq_loss.png", 18),
        (r"$\text{F1-Score} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$", "graphs/equations/eq_f1.png", 18),
        (r"$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$", "graphs/equations/eq_accuracy.png", 18),
    ]
    
    for latex, path, fs in equations:
        render_equation(latex, path, fontsize=fs)

if __name__ == "__main__":
    main()
