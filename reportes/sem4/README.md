# Reporte de Avance — Semestre 4 (LaTeX)

Proyecto LaTeX del reporte de avance del 4.º semestre. Enfoque: **el DAQ es el
avance central**; la cadena de detección pasa a *trabajo futuro*.

## Compilar

- **Local (recomendado mientras se itera):** `pwsh -File build.ps1` (MiKTeX + Biber).
- **VS Code:** abrir la carpeta, abrir `avances_sem4.tex`, Ctrl+S (receta de biber en
  `.vscode/settings.json`).
- **Overleaf:** subir la carpeta `sem4/` completa. Motor: pdfLaTeX + Biber.
- Compila **con o sin imágenes**: el macro `\figph` dibuja un recuadro *PLACEHOLDER*
  si el archivo aún no existe (recompilar 1 vez al añadir los PNG).

## Figuras

**Generadas en el documento (TikZ/tabla, NO requieren archivo):**
- Arquitectura del DAQ por etapas y subetapas — se dibuja sola.
- Máquina de estados (FSM) del núcleo de adquisición — se dibuja sola.
- Tabla de *bring-up* (etapas 0–8) — se genera sola.

**Generadas por script (matplotlib, YA incluidas en `figuras/`):**
Producidas por `figuras/scripts/gen_figs.py` (`python gen_figs.py`):
`fig-muestreo-nyquist`, `fig-niveles-codificacion`, `fig-memoria`,
`fig-timing-fsm`, `fig-impedancia`. Edita el script y reejecútalo para regenerarlas.

**Placeholders — dejar el PNG en `figuras/` con EXACTAMENTE estos nombres**
(con guion `-`, no guion bajo `_`):

| Archivo | Contenido | Sección |
|---|---|---|
| `placa-acrilico.png`   | Placa de acrílico con las PCBs de todas las etapas | Metodología |
| `daq-fpga-etapas.png`  | Etapa de adquisición del FPGA **por partes** (trigger, ADC, captura, UART) | Metodología |
| `montaje.png`          | Foto del montaje de banco del intento de detección | Metodología |
| `bringup-etapas.png`   | Resultados de la validación por etapas del FPGA | Resultados (DAQ) |
| `daq-captura.png`      | Datos resultantes: evidencia de captura a 54 MSPS y 12 bits | Resultados (DAQ) |
| `pulsos-corriente.png` | Pulsos de corriente del Driver V2.0 | Resultados (Driver) |
| `potencia-laser.png`   | Estimación de potencia óptica (monitor: V→I por responsividad) | Resultados (Driver) |
| `ruido-em.png`         | Evidencia del ruido EM durante el disparo (frame del video) | Resultados (detección) |
| `ringing-falso.png`    | Osc: CH1 láser + CH2 los ~150 mV pp (pickup); idealmente con sensor desconectado | Resultados (detección) |

> Formato preferido PNG. Si usas otro, ajustar la extensión en `avances_sem4.tex`.

## Pendientes de contenido (`% TODO` en el `.tex`)
- Confirmar **periodo/fechas** (título y cronograma).
- Tabla de candidatos a **preamplificador** (p. ej. AD8331/AD8332).
