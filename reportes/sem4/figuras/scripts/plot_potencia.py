#!/usr/bin/env python3
"""Estimación (PRELIMINAR) de la excitación del diodo combinando:
  - V del diodo  (osciloscopio across el diodo, laser_wave.csv)
  - I del shunt  (DAQ en sense 0.1 Ω, ventana_*.csv)
ambas alineadas en el transitorio (el disparo de avalancha es periódico/reproducible).

ADVERTENCIAS (van en el caption del reporte):
  * Capturas NO simultáneas (instrumentos distintos) -> se pierde la fase V-I fina;
    sirve para orden de magnitud, no para P(t) instantánea exacta.
  * La corriente está submuestreada (54 MS/s) -> el pico real es MAYOR (cota inferior).
  * La tensión de conducción real del diodo es ambigua (hay ringing); por eso la
    potencia se da como rango de orden de magnitud, no como cifra exacta.

Salida: ../potencia-laser.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SEM4 = os.path.dirname(BASE)
OSC = os.path.join(SEM4, "capturas", "laser_wave.csv")
DAQ = os.path.join(SEM4, "figuras", "exports", "ventana_20260624_200320.csv")
OUT = os.path.join(BASE, "potencia-laser.png")
BLUE, ORANGE = "#2b6cb0", "#dd6b20"
R_SHUNT = 0.1


def load_osc(path):
    t, v = [], []
    for ln in open(path, errors="replace").read().splitlines()[1:]:
        p = ln.split(",")
        try:
            t.append(float(p[0])); v.append(float(p[1]))
        except ValueError:
            pass
    t, v = np.array(t), np.array(v)
    bad = np.where(np.diff(t) <= 0)[0]
    if len(bad):
        t, v = t[:bad[0] + 1], v[:bad[0] + 1]
    return t, v                                   # us, V


def load_i(path):
    t, mv = [], []
    for ln in open(path, errors="replace").read().splitlines():
        if ln.startswith("#") or ln.lower().startswith("muestra"):
            continue
        p = ln.split(",")
        try:
            t.append(float(p[2])); mv.append(float(p[4]))
        except (ValueError, IndexError):
            pass
    t, mv = np.array(t), np.array(mv)
    base = np.median(mv)                           # quitar offset (off-state ~ 0 A)
    i = (mv - base) / 1000.0 / R_SHUNT            # A
    return t, i


def main():
    tv, v = load_osc(OSC)
    ti, i = load_i(DAQ)
    tv = tv - tv[int(np.argmax(np.abs(v - np.median(v))))]   # alinear transitorio a 0
    ti = ti - ti[int(np.argmax(np.abs(i)))]

    vpk = v[int(np.argmax(np.abs(v - np.median(v))))]
    ipk = i[int(np.argmax(np.abs(i)))]
    # rango de orden de magnitud: Vf de conducción ~5 V (bajo) hasta |V| del swing (alto)
    p_lo = abs(5.0 * ipk)
    p_hi = abs(vpk * ipk)
    print(f"V_pico(diodo)~{vpk:.0f} V   I_pico(muestreada)~{ipk:.2f} A")
    print(f"P_pico estimada: {p_lo:.0f}-{p_hi:.0f} W (cota inf. de I -> potencia mayor)")

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ax.plot(tv, v, color=BLUE, lw=1.0, label="V del diodo (osc.)")
    ax.set_xlabel("tiempo relativo al transitorio (µs)")
    ax.set_ylabel("tensión del diodo (V)", color=BLUE)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax.set_xlim(-0.6, 2.0)
    ax.grid(alpha=0.3)
    ax2 = ax.twinx()
    ax2.plot(ti, i, color=ORANGE, lw=1.2, marker="o", ms=2.5, label="I del shunt (DAQ)")
    ax2.set_ylabel("corriente del diodo (A)", color=ORANGE)
    ax2.tick_params(axis="y", labelcolor=ORANGE)
    ax.set_title("Excitación del diodo: tensión (osc.) y corriente (shunt) — estimación",
                 fontsize=10)
    txt = (f"Estimación PRELIMINAR de potencia pico: ~{p_lo:.0f}–{p_hi:.0f} W\n"
           f"(I muestreada {ipk:.1f} A = cota inferior; capturas no simultáneas)")
    ax.text(0.02, 0.03, txt, transform=ax.transAxes, fontsize=8,
            va="bottom", ha="left",
            bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.9))
    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
