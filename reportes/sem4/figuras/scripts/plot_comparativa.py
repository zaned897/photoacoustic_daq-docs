#!/usr/bin/env python3
"""Figura comparativa: el MISMO transitorio del laser visto por el osciloscopio
(referencia, 200 MS/s) y por el DAQ propio (54 MS/s, 12 bit).

Alinea ambos en el instante del transitorio (t=0 = pico) para comparar timing y
forma. Las amplitudes van en sus propias unidades (miden nodos/escala distintos).

Salida: ../daq-vs-osc.png
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
OUT = os.path.join(BASE, "daq-vs-osc.png")
BLUE, ORANGE = "#2b6cb0", "#dd6b20"


def load_osc(path):
    t, v = [], []
    for ln in open(path, errors="replace").read().splitlines()[1:]:
        p = ln.split(",")
        try:
            t.append(float(p[0])); v.append(float(p[1]))
        except ValueError:
            pass
    t, v = np.array(t), np.array(v)
    bad = np.where(np.diff(t) <= 0)[0]          # recorta relleno 0,0
    if len(bad):
        t, v = t[:bad[0] + 1], v[:bad[0] + 1]
    return t, v                                  # us, V


def load_daq(path):
    t, mv, pm = [], [], []
    for ln in open(path, errors="replace").read().splitlines():
        if ln.startswith("#") or ln.lower().startswith("muestra"):
            continue
        p = ln.split(",")
        try:
            t.append(float(p[2])); mv.append(float(p[4])); pm.append(float(p[5]))
        except (ValueError, IndexError):
            pass
    return np.array(t), np.array(mv), np.array(pm)   # us, mV, prom_mV(x32)


def fwhm(t, y):
    base = np.median(y)
    s = y - base
    k = int(np.argmax(np.abs(s)))
    half = base + s[k] * 0.5
    if s[k] < 0:
        idx = np.where(y <= half)[0]
    else:
        idx = np.where(y >= half)[0]
    return (t[idx[-1]] - t[idx[0]]) * 1e3 if len(idx) > 1 else 0.0  # ns


def save_daq_captura(td, vd, vdp):
    """Figura standalone de la ventana del DAQ (rellena el placeholder daq-captura)."""
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(td, vd, color="0.7", lw=0.9, marker="o", ms=2, label="captura (1 ventana)")
    ax.plot(td, vdp, color=ORANGE, lw=1.6, label="promedio coherente x32")
    ax.set_xlabel("tiempo desde el trigger (µs)")
    ax.set_ylabel("amplitud (mV)")
    ax.set_title("Captura del DAQ: 270 muestras @ 54 MS/s, 12 bit (LSB 2.44 mV)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    out = os.path.join(BASE, "daq-captura.png")
    fig.savefig(out, dpi=150)
    print("OK ->", out)


def main():
    to, vo = load_osc(OSC)
    td, vd, vdp = load_daq(DAQ)
    save_daq_captura(td, vd, vdp)
    # alinear t=0 en el pico (máxima desviación de la base)
    to0 = to - to[int(np.argmax(np.abs(vo - np.median(vo))))]
    td0 = td - td[int(np.argmax(np.abs(vd - np.median(vd))))]
    wo, wd = fwhm(to, vo), fwhm(td, vd)
    print(f"FWHM transitorio  OSC ~{wo:.0f} ns   DAQ ~{wd:.0f} ns")

    fig, ax = plt.subplots(2, 1, figsize=(7.2, 5.2), sharex=True)
    ax[0].plot(to0, vo, color=BLUE, lw=1.0)
    ax[0].set_ylabel("voltaje (V)")
    ax[0].set_title("Osciloscopio (referencia) — 200 MS/s", color=BLUE, fontsize=10, loc="left")
    ax[1].plot(td0, vd, color=ORANGE, lw=1.0, marker="o", ms=2.5)
    ax[1].set_ylabel("amplitud (mV)")
    ax[1].set_xlabel("tiempo relativo al transitorio (µs)")
    ax[1].set_title("DAQ propio — 54 MS/s, 12 bit (LSB 2.44 mV)", color=ORANGE, fontsize=10, loc="left")
    for a in ax:
        a.grid(alpha=0.3)
        a.axvline(0, color="0.6", ls=":", lw=1)
    ax[1].set_xlim(-0.6, 4.8)                     # ventana del DAQ
    fig.suptitle("Mismo transitorio del láser: osciloscopio vs DAQ propio", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
