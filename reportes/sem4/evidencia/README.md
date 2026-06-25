# Evidencia y media — reporte Sem 4

Material visual del experimento. Los **datos numéricos crudos** (CSV del
osciloscopio) van en `../capturas/`; las **figuras finales** del reporte van en
`../figuras/`.

## Estructura
- `fotos/` — fotos de cámara (banco, PCBs, montaje).
- `screenshots/` — capturas de pantalla del osciloscopio (.bmp/.png exportadas).
- `video/` — videos crudos (p. ej. el del ruido EM). ⚠️ **Videos grandes NO se
  versionan** (ver `.gitignore`): déjalos aquí localmente y commitea solo los frames.
- `frames/` — frames extraídos de los videos (para figuras como `ruido-em`).

## Inventario
| Archivo | Qué es | Notas |
|---|---|---|
| `screenshots/firstwave.bmp` | Captura de pantalla del osciloscopio (24-jun) | Probablemente la pantalla del `laser_wave` (a confirmar el nodo medido). |

> Relación con datos: `../capturas/laser_wave.csv` es el export numérico de esa
> misma adquisición (200 MS/s, base ~50 V, pico negativo agudo en t≈−2.8 µs).

## Pendiente
- **Video del ruido EM**: aún no está en el repo. Déjalo en `video/` (o dime la ruta)
  y extraigo el/los frame(s) para la figura `ruido-em`.
