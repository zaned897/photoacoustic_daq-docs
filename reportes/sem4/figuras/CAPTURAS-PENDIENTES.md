# Capturas pendientes — figuras del reporte Sem 4

> Lista de trabajo para el banco. Los nombres de archivo son **exactos** (guion `-`,
> PNG) y deben quedar en `figuras/`. El reporte compila con placeholders hasta entonces.
> Para las capturas de osciloscopio usa `tools/scope_capture.py` (SCPI/USB-TMC).

## 🟥 Grupo A — Fotos físicas (cámara)
| Archivo | Qué fotografiar |
|---|---|
| `placa-acrilico.png` | Placa de acrílico con **todas las PCBs atornilladas** (vista cenital, buena luz, que se distingan las etapas). |
| `montaje.png` | **Montaje de banco** del intento de detección: transductor Yushi 2.5 MHz, cable BNC–SMA al AD9226, osciloscopio en paralelo, Driver V2.0. |

## 🟧 Grupo B — Capturas de osciloscopio (`tools/scope_capture.py` o foto de pantalla)
| Archivo | Qué mostrar | Ajustes sugeridos |
|---|---|---|
| `pulsos-corriente.png` | Pulsos de corriente del **Driver V2.0** (shunt/monitor de corriente). | Base de tiempo que muestre el pulso completo; trigger en el disparo. |
| `ringing-falso.png` | **CH1** = pulso láser; **CH2** = onda ~150 mV pp del transductor (*ringing* ~2.6 MHz). | CH2 ~50 mV/div; base ~0.5–1 µs/div; trigger en CH1. Capturar **también con el sensor desconectado** (control clave). |
| `ruido-em.png` | **Frame del video** del transitorio EM sincronizado con la descarga de alto voltaje. | Screenshot nítido del momento del disparo. |

## 🟦 Grupo C — Datos crudos → Claude genera la figura (matplotlib, estilo `gen_figs.py`)
No requieren foto: entregar los **datos**.
| Figura objetivo | Qué entregar | Resultado |
|---|---|---|
| `daq-captura.png` | **Dump/CSV de una ráfaga** (54 MSPS, 12 bits) — p. ej. `scope_CHn.csv`. | Señal reconstruida (tiempo/voltaje), estilo `fig-timing-fsm`. |
| `bringup-etapas.png` | Resultados de cada etapa de validación (números/tabla o capturas por etapa). | Figura-resumen de validación por etapas. |
| `potencia-laser.png` | **V medida** del monitor óptico (fotodiodo+TIA) + **curva de responsividad** del fotodiodo. | Conversión V→I→P + gráfica de estimación de potencia. |
| `daq-fpga-etapas.png` | Screenshots del diseño FPGA (Vivado block design / sim de trigger, ADC, captura BRAM, UART), **o** pedir diagrama por bloques. | Figura por etapas. |

## 🔧 Procedimientos / decisiones (no son figuras)
- **Fechas del periodo Sem 4** → actualizar título y cronograma (`% TODO` en `avances_sem4.tex`).
- **(Opcional) D0** — capacitancia del piezo con medidor LCR (un número).
- **(Opcional) D1** — toque sin láser (Hsu–Nielsen). *El texto ya lo describe como hecho y sin señal*; si se repite, solo aportar el resultado.
- **(Opcional) Tabla de preamplificador** — candidatos LNA (AD8331/AD8332…), otro `% TODO`.
