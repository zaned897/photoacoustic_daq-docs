#!/usr/bin/env python3
"""Convierte capturas crudas del osciloscopio (CSV) en figuras del reporte.

Formato CSV esperado: cabecera tipo 'Time (us|ms|s),Voltage (v)' + filas t,v.
La unidad de tiempo se detecta de la cabecera; el eje x se autoescala.

Uso:
  python plot_capturas.py CSV [CSV2 ...] -o ../figura.png -t "Titulo" [--labels L1 L2]

Ejemplos:
  python plot_capturas.py ../../capturas/cal_1kHz_ch2.csv -o ../cal.png -t "Cal 1 kHz"
  python plot_capturas.py ../../capturas/ringing_ch1.csv ../../capturas/ringing_ch2.csv \
      -o ../ringing-falso.png -t "CH1 laser + CH2 (pickup)" --labels "CH1 (laser)" "CH2 (sensor)"
"""
import argparse
import os
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = ["#2b6cb0", "#dd6b20", "#2f855a", "#c53030"]


def load(path):
    raw = open(path, errors="replace").read().splitlines()
    hdr = raw[0].lower() if raw else ""
    unit = "us" if "us" in hdr else ("ms" if "ms" in hdr else "s")
    sc = {"us": 1e-6, "ms": 1e-3, "s": 1.0}[unit]
    rows = []
    for ln in raw:
        p = re.split(r"[;,\t ]+", ln.strip())
        if len(p) < 2:
            continue
        try:
            rows.append([float(p[0]), float(p[1])])
        except ValueError:
            continue  # salta cabecera/líneas no numéricas
    a = np.array(rows, float)
    t = a[:, 0] * sc
    v = a[:, 1]
    # Recorta relleno de exportación: conserva el prefijo de tiempo estrictamente
    # creciente (algunos osciloscopios rellenan el buffer con filas 0,0 al final).
    if len(t) > 1:
        bad = np.where(np.diff(t) <= 0)[0]
        if len(bad):
            cut = bad[0] + 1
            t, v = t[:cut], v[:cut]
    return t, v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+", help="uno o más CSV (se superponen)")
    ap.add_argument("-o", "--out", required=True, help="PNG de salida")
    ap.add_argument("-t", "--title", default="")
    ap.add_argument("--labels", nargs="*", default=None)
    ap.add_argument("--xunit", choices=["auto", "s", "ms", "us"], default="auto")
    args = ap.parse_args()

    t0, _ = load(args.csv[0])
    span = t0.max() - t0.min()
    if args.xunit == "auto":
        xu, xs = ("us", 1e6) if span < 2e-3 else (("ms", 1e3) if span < 2 else ("s", 1))
    else:
        xu, xs = {"s": ("s", 1), "ms": ("ms", 1e3), "us": ("us", 1e6)}[args.xunit]

    fig, ax = plt.subplots(figsize=(8, 3.6))
    for i, c in enumerate(args.csv):
        t, v = load(c)
        lbl = args.labels[i] if (args.labels and i < len(args.labels)) else os.path.basename(c)
        ax.plot(t * xs, v, lw=1.0, color=COLORS[i % 4], label=lbl)
    ax.set_xlabel(f"tiempo ({xu})")
    ax.set_ylabel("voltaje (V)")
    if args.title:
        ax.set_title(args.title)
    if len(args.csv) > 1 or args.labels:
        ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    fig.savefig(args.out, dpi=150)
    print("OK ->", args.out)


if __name__ == "__main__":
    main()
