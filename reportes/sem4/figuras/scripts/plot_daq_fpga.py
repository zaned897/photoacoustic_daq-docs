#!/usr/bin/env python3
"""Figura `daq-fpga-etapas`: foto del hardware (FPGA + ADC) arriba y un diagrama de
bloques de la cadena de adquisición del FPGA abajo.

Salida: ../daq-fpga-etapas.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SEM4 = os.path.dirname(BASE)
PHOTO = os.path.join(SEM4, "evidencia", "fotos", "adc_fpga.jpeg")
OUT = os.path.join(BASE, "daq-fpga-etapas.png")
BLUE = "#2b6cb0"


def main():
    img = Image.open(PHOTO).convert("RGB")
    fig = plt.figure(figsize=(7.4, 6.0))

    ax1 = fig.add_axes([0.05, 0.40, 0.90, 0.56])
    ax1.imshow(img)
    ax1.axis("off")
    ax1.set_title("Etapa de adquisición: FPGA Tang Nano 9K + módulo AD9226",
                  fontsize=10)

    ax2 = fig.add_axes([0.02, 0.03, 0.96, 0.30])
    ax2.axis("off")
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    blocks = ["Trigger\n(pin 77 / S2)", "ADC AD9226\n12 bit · 54 MSPS",
              "Captura\nFSM + BRAM\n(270 muestras)", "UART\nheader + datos",
              "PC\n(Python)"]
    n = len(blocks)
    xs = [(k + 0.5) / n for k in range(n)]
    for x, b in zip(xs, blocks):
        ax2.text(x, 0.55, b, ha="center", va="center", fontsize=8,
                 bbox=dict(boxstyle="round,pad=0.35", fc="#e8f0fa", ec=BLUE, lw=1.4))
    for k in range(n - 1):
        ax2.annotate("", xy=(xs[k + 1] - 0.075, 0.55), xytext=(xs[k] + 0.075, 0.55),
                     arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6))
    ax2.text(0.5, 0.04, "Cadena de adquisición del FPGA (store-and-forward)",
             ha="center", fontsize=8, color="0.4")

    fig.savefig(OUT, dpi=150)
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
