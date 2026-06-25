# Capturas crudas del osciloscopio

Datos crudos exportados del osciloscopio (CSV) que alimentan las figuras del reporte.
El procesamiento a figuras finales lo hace `../figuras/scripts/plot_capturas.py`
(salida → `../figuras/*.png`, que es donde el reporte las lee).

## Formato CSV (validado)
Cabecera `Time (us|ms),Voltage (v)` + filas `t,v`. El parser detecta la unidad de
tiempo automáticamente (µs o ms). Referencia validada: `cal_1kHz_ch2.csv`
(cuadrada de calibración, ~1 kHz, 1 MS/s, 3200 pts) — confirma que el pipeline sirve.

## Convención de nombres
Usa nombres descriptivos (NO `scope_CHn.csv` — ese patrón está en `.gitignore`):
- `cal_1kHz_ch2.csv` — validación del pipeline (referencia).
- `ringing_ch1.csv` / `ringing_ch2.csv` — pickup: CH1 láser + CH2 sensor.
- `ringing_sensordesc_ch2.csv` — control clave (sensor desconectado).
- `pulsos_corriente.csv` — Driver V2.0.
- `daq_rafaga.csv` — ráfaga del DAQ (54 MSPS / 12 bit).

## Inventario actual
| Archivo | Adquisición | Observado | Estado |
|---|---|---|---|
| `cal_1kHz_ch2.csv` | cuadrada de calibración, 1 MS/s, 3200 pts | ~1 kHz, Vpp ~7.2 V | ✓ valida el pipeline |
| `laser_wave.csv` | 200 MS/s, 2560 pts útiles (12.8 µs) | base ~50 V, pico negativo agudo (~−47 V) en t≈−2.8 µs, escalón en t=0 | ⚠️ confirmar qué nodo mide (¿monitor del driver?) · screenshot en `../evidencia/screenshots/firstwave.bmp` |

## Generar una figura
```bash
cd ../figuras/scripts
# una traza:
python plot_capturas.py ../../capturas/cal_1kHz_ch2.csv -o ../cal.png -t "Cal 1 kHz"
# dos canales superpuestos (p. ej. ringing-falso):
python plot_capturas.py ../../capturas/ringing_ch1.csv ../../capturas/ringing_ch2.csv \
   -o ../ringing-falso.png -t "CH1 laser + CH2 (pickup)" --labels "CH1 (laser)" "CH2 (sensor)"
```
Mapa de figuras del reporte: ver `../figuras/CAPTURAS-PENDIENTES.md` (grupos A/B/C).
