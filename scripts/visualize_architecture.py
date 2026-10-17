"""
scripts/visualize_architecture.py
Generates high-resolution 3D volumetric diagram for Power-Monitor:
1. docs/figures/1_power_monitor_distribution_3d.png

Canvas: 16x10 inches, 300 DPI.
Shows Standalone Thick-Client Packaging, Telemetry Flow, and relation to Master-Station.
Does NOT duplicate Master-Station AI diagrams.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

THEMES = {
    "camera": ["#0284C7", "#38BDF8", "#0369A1"],      # Cyan / Sky
    "preprocess": ["#475569", "#94A3B8", "#334155"],  # Slate Gray
    "backend": ["#4F46E5", "#818CF8", "#3730A3"],     # Indigo
    "ui": ["#DB2777", "#F472B6", "#9D174D"],          # Rose / Pink
    "plc": ["#059669", "#34D399", "#047857"],         # Emerald Green
    "dark_bg": "#0B1120",
    "card_bg": "#1E293B",
    "card_border": "#334155",
    "text_white": "#F8FAFC",
    "text_muted": "#94A3B8",
    "text_yellow": "#FEF08A"
}

def draw_3d_block(ax, x, y, w, h, depth=0.35, theme="backend", label="", sublabel="", tensor_shape="", desc=""):
    front_c, top_c, side_c = THEMES[theme]
    dx = depth * 0.7
    dy = depth * 0.7

    side_pts = [[x + w, y], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + w, y + h]]
    ax.add_patch(Polygon(side_pts, closed=True, facecolor=side_c, edgecolor="#0F172A", lw=1.2, zorder=2))

    top_pts = [[x, y + h], [x + dx, y + h + dy], [x + w + dx, y + h + dy], [x + w, y + h]]
    ax.add_patch(Polygon(top_pts, closed=True, facecolor=top_c, edgecolor="#0F172A", lw=1.2, zorder=2))

    front_pts = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
    ax.add_patch(Polygon(front_pts, closed=True, facecolor=front_c, edgecolor="#0F172A", lw=1.2, zorder=3))

    cx = x + w / 2.0
    cy = y + h / 2.0

    if label:
        ax.text(cx, cy + h * 0.22, label, ha="center", va="center", color=THEMES["text_white"], fontsize=9.5, fontweight="bold", zorder=4)
    if sublabel:
        ax.text(cx, cy + h * 0.02, sublabel, ha="center", va="center", color="#F1F5F9", fontsize=8.0, zorder=4)
    if tensor_shape:
        ax.text(cx, cy - h * 0.22, tensor_shape, ha="center", va="center", color=THEMES["text_yellow"], fontsize=8.0, fontweight="bold", family="monospace", zorder=4)
    if desc:
        ax.text(cx + dx/2, y - 0.35, desc, ha="center", va="top", color=THEMES["text_muted"], fontsize=7.8, zorder=4)

def draw_3d_arrow(ax, x1, y1, x2, y2, color="#38BDF8", text=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=color, edgecolor=color, width=1.8, headwidth=6, headlength=7, shrink=0.06), zorder=5)
    if text:
        ax.text((x1 + x2)/2, (y1 + y2)/2 + 0.25, text, ha="center", va="center", color="#FFFFFF", fontsize=7.5, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor=THEMES["card_bg"], edgecolor=THEMES["card_border"], alpha=0.95), zorder=6)

def generate_fig1():
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    fig.patch.set_facecolor(THEMES["dark_bg"])
    ax.set_facecolor(THEMES["dark_bg"])
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(-0.5, 9.5)
    ax.axis("off")

    ax.text(8.0, 8.8, "Power-Monitor: Standalone Desktop Thick-Client Packaging Topology", ha="center", va="center",
            color=THEMES["text_white"], fontsize=18, fontweight="bold")
    ax.text(8.0, 8.35, "Twin Distribution Profile of Master-Station (StationOS) for Air-Gapped Industrial Substation PCs",
            ha="center", va="center", color=THEMES["text_muted"], fontsize=10.5)

    stages = [
        {"x": 0.5, "w": 2.8, "h": 2.8, "theme": "plc", "label": "Telemetry Ingestion", "sub": "Industrial Modbus/S7", "shape": "Power Meters", "desc": "Active / Reactive Power\nVoltage & Current readings"},
        {"x": 4.4, "w": 3.0, "h": 2.8, "theme": "backend", "label": "Local Backend Svc", "sub": "build-thick-client.sh", "shape": "StationOS.Api", "desc": "Self-contained SQLite DB\nBundled C# .NET 8 Runtime"},
        {"x": 8.5, "w": 3.0, "h": 2.8, "theme": "preprocess", "label": "VMAF Media Server", "sub": "go2rtc/model/*.pkl", "shape": "Video Quality", "desc": "Assesses streaming quality\nunder noisy factory network"},
        {"x": 12.6, "w": 3.0, "h": 2.8, "theme": "ui", "label": "Desktop HMI App", "sub": "station-monitor.exe", "shape": "Electron Shell", "desc": "Air-gapped desktop display\nSingle-line diagram & trends"}
    ]

    for s in stages:
        draw_3d_block(ax, s["x"], 3.2, s["w"], s["h"], theme=s["theme"],
                      label=s["label"], sublabel=s["sub"], tensor_shape=s["shape"], desc=s["desc"])

    draw_3d_arrow(ax, 3.3, 4.6, 4.4, 4.6)
    draw_3d_arrow(ax, 7.4, 4.6, 8.5, 4.6)
    draw_3d_arrow(ax, 11.5, 4.6, 12.6, 4.6)

    fig.savefig(OUTPUT_DIR / "1_power_monitor_distribution_3d.png", dpi=300)
    plt.close(fig)
    print("Power-Monitor: Generated 1_power_monitor_distribution_3d.png")

if __name__ == "__main__":
    generate_fig1()
    print("Power-Monitor: 3D figure generated successfully.")
