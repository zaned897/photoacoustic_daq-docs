#!/usr/bin/env python3
"""Genera las figuras explicativas del reporte Sem4 (DAQ).
Salida: PNGs en ../  (reportes/sem4/figuras/).
Uso:  python gen_figs.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 11,
    "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False,
    "axes.spines.right": False,
})
BLUE, ORANGE, GREEN, RED = "#2b6cb0", "#dd6b20", "#2f855a", "#c53030"


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    print("->", name)


# 1) Muestreo del ringing 2.5 MHz a 27 vs 54 MSPS -----------------------------
def fig_muestreo():
    f = 2.5e6
    t = np.linspace(0, 1.2e-6, 2000)
    y = np.sin(2 * np.pi * f * t)
    fig, ax = plt.subplots(2, 1, figsize=(7, 4.6), sharex=True)
    for a, fs, c, lbl in [(ax[0], 27e6, ORANGE, "27 MSPS (10.8 muestras/ciclo)"),
                          (ax[1], 54e6, BLUE, "54 MSPS (21.6 muestras/ciclo)")]:
        ts = np.arange(0, 1.2e-6, 1 / fs)
        a.plot(t * 1e6, y, color="0.6", lw=1, label="señal 2.5 MHz")
        a.stem(ts * 1e6, np.sin(2 * np.pi * f * ts), linefmt=c, markerfmt="o",
               basefmt=" ")
        a.set_ylabel("amplitud")
        a.set_title(lbl, color=c, fontsize=10, loc="left")
        a.set_ylim(-1.4, 1.4)
    ax[1].set_xlabel("tiempo (µs)")
    fig.suptitle("Aumento de la tasa de muestreo (PLL ×2): "
                 "muestreo del ringing del transductor", fontsize=11)
    fig.tight_layout()
    save(fig, "fig-muestreo-nyquist.png")


# 2) Niveles de codificación 8/10/12 bit --------------------------------------
def fig_niveles():
    t = np.linspace(0, 2e-6, 1000)
    # ringing débil de ejemplo (decaimiento) en torno a 0 V, +-0.1 V
    sig = 0.1 * np.exp(-t / 0.8e-6) * np.sin(2 * np.pi * 2.5e6 * t)
    rng = 10.0  # AD9226 +-5 V => 10 Vpp
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(t * 1e6, sig * 1e3, color="0.5", lw=1.4, label="señal analógica")
    for bits, c in [(8, ORANGE), (12, BLUE)]:
        lsb = rng / (2 ** bits)
        q = np.round(sig / lsb) * lsb
        ax.step(t * 1e6, q * 1e3, where="mid", color=c, lw=1.2,
                label=f"{bits} bits  ({2**bits} niveles, LSB {lsb*1e3:.2f} mV)")
    ax.set_xlabel("tiempo (µs)")
    ax.set_ylabel("amplitud (mV)")
    ax.set_title("Niveles de codificación: 8 vs 12 bits sobre el rango ±5 V")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, "fig-niveles-codificacion.png")


# 3) Repercusión en memoria (BRAM) --------------------------------------------
def fig_memoria():
    fs = 54e6
    win = np.linspace(1e-6, 50e-6, 400)          # ventana en s (desde 1 µs)
    n = win * fs
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for bits, c in [(8, ORANGE), (10, GREEN), (12, BLUE)]:
        kbit = n * bits / 1000.0
        ax.plot(win * 1e6, kbit, color=c, lw=1.8, label=f"{bits} bits @ 54 MSPS")
    ax.axhline(468, color=RED, ls="--", lw=1.4, label="BSRAM ≈ 468 Kbit (GW1NR-9C)")
    cur = 5e-6 * fs * 12 / 1000.0
    tgt = 37.7e-6 * fs * 12 / 1000.0
    ax.scatter([5], [cur], color=BLUE, zorder=5)
    ax.scatter([37.7], [tgt], color="0.2", zorder=5)
    ax.annotate(f"actual: 5 µs, 12 bit ({cur:.1f} Kbit)", (5, cur),
                textcoords="offset points", xytext=(10, -4), fontsize=8, color=BLUE)
    ax.annotate(f"objetivo: ~5.8 cm (37.7 µs, {tgt:.0f} Kbit)", (37.7, tgt),
                textcoords="offset points", xytext=(-160, 12), fontsize=8)
    ax.set_yscale("log")
    ax.set_ylim(0.1, 1000)
    ax.set_xlabel("ventana de captura (µs)")
    ax.set_ylabel("memoria por ráfaga (Kbit, escala log)")
    ax.set_title("Memoria por ráfaga vs ventana: el BSRAM holgado no es el límite")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, "fig-memoria.png")


# 4) Sincronización store-and-forward (timing) --------------------------------
def fig_timing():
    baud = 1e6
    n_bytes = 270 * 2
    t_cap_us = 5.0
    t_tx_ms = n_bytes * 10 / baud * 1e3       # ms
    t_tx_us = t_tx_ms * 1e3
    period_us = 200.0                          # trigger 5 kHz
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    # FSM bars
    ax.broken_barh([(0, t_cap_us)], (10, 6), facecolors=BLUE)
    ax.broken_barh([(t_cap_us, t_tx_us)], (10, 6), facecolors=ORANGE)
    ax.annotate("CAPTURE (5 µs)", xy=(t_cap_us, 16), xytext=(450, 17.4),
                fontsize=8, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1))
    ax.text(t_cap_us + t_tx_us / 2, 13, f"SEND  ≈ {t_tx_ms:.1f} ms (UART 1 Mbaud)",
            ha="center", va="center", color="white", fontsize=9)
    # triggers ignored
    n_skip = int(t_tx_us / period_us)
    for k in range(0, n_skip + 2):
        x = k * period_us
        ax.plot([x, x], (2, 6), color=RED, lw=1)
    ax.text(t_tx_us / 2, 0.2, f"≈ {n_skip} disparos omitidos durante la transmisión "
            f"(→ promediado coherente)", ha="center", va="bottom", fontsize=8,
            color=RED)
    ax.set_xlim(-200, t_tx_us * 1.05)
    ax.set_ylim(-1, 18)
    ax.set_yticks([4, 13]); ax.set_yticklabels(["triggers\n(5 kHz)", "FSM"])
    ax.set_xlabel("tiempo (µs)")
    ax.set_title("Sincronización store-and-forward: captura rápida, transmisión lenta")
    ax.grid(False)
    fig.tight_layout()
    save(fig, "fig-timing-fsm.png")


# 5) Acoplamiento de impedancias ----------------------------------------------
def fig_impedancia():
    zin = np.logspace(1, 7, 500)               # 10 Ω .. 10 MΩ
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for zsrc, c in [(300, ORANGE), (3000, BLUE)]:
        retained = zin / (zin + zsrc) * 100
        ax.semilogx(zin, retained, color=c, lw=1.8,
                    label=f"|Z| fuente piezo ≈ {zsrc} Ω")
    for x, lab in [(50, "50 Ω\n(coax/osc.)"), (1e6, "1 MΩ\n(preamp/osc. hi-Z)")]:
        ax.axvline(x, color="0.5", ls=":", lw=1)
        ax.text(x, 5, lab, rotation=90, va="bottom", ha="right", fontsize=8,
                color="0.3")
    ax.set_xlabel("impedancia de entrada del receptor (Ω)")
    ax.set_ylabel("señal retenida (%)")
    ax.set_ylim(0, 105)
    ax.set_title("Acoplamiento de impedancias: por qué se necesita entrada de alta-Z "
                 "(preamplificador)")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, "fig-impedancia.png")


if __name__ == "__main__":
    fig_muestreo()
    fig_niveles()
    fig_memoria()
    fig_timing()
    fig_impedancia()
    print("OK ->", OUT)
