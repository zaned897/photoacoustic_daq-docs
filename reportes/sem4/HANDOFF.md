# HANDOFF / ESTADO — Reporte Sem 4

> **Fuente única de verdad para trabajar entre máquinas (Windows ↔ Mac).**
> Las sesiones de Claude Code NO se comparten entre computadoras; este archivo SÍ.
> **Léelo al iniciar cada sesión; actualízalo al terminar.** (Para Claude: este doc
> reemplaza la memoria que no viaja entre máquinas.)

## Protocolo de cada sesión (ambas máquinas)
1. `git pull` en este repo (y en `photoacoustic_daq` si tocas firmware).
2. Lee este archivo: **Estado** + **Pendientes** + **Bitácora**.
3. Trabaja. Haz commits pequeños y frecuentes.
4. Actualiza **Pendientes** (marca casillas) y añade una línea a **Bitácora**.
5. `git commit` + `git push` al terminar, o **antes de cambiar de máquina**.

> **Regla anti-conflicto:** una máquina a la vez sobre los mismos archivos. Si
> trabajan en paralelo, dividir por área (ver abajo) y hacer `push` seguido.

## Repos
- **Reportes (este):** `photoacoustic_daq-docs` → github.com/zaned897/photoacoustic_daq-docs (rama `main`).
- **Código/firmware:** `photoacoustic_daq` → github.com/zaned897/photoacoustic_daq (ramas `main`, `feature/...`). Independiente de este.

## Estado actual (2026-06-24)
- `avances_sem4.tex` — **16 pág**, enfoque **DAQ-central**, detección → trabajo futuro. Compila limpio.
- `presentacion/presentacion_sem4.tex` — **21 láminas** (tema metropolis).
- Figuras técnicas reales: generadas por `figuras/scripts/gen_figs.py` (matplotlib) — ya incluidas.
- Figuras de foto: **PLACEHOLDERS pendientes** (el macro `\figph` compila igual). Lista de
  trabajo detallada en `figuras/CAPTURAS-PENDIENTES.md` (Grupos A/B/C + procedimientos).
- Herramienta `tools/scope_capture.py` (SCPI/USB-TMC): captura pantalla+CSV del osciloscopio.
- `Pipfile` con deps Python (numpy, matplotlib, pyvisa/pyvisa-py/pyusb) para banco+figuras.

## Pendientes para terminar
- [ ] **9 figuras** en `figuras/` (nombres con guion `-`, PNG). Lista de trabajo y
      procedimientos en **`figuras/CAPTURAS-PENDIENTES.md`**. Resumen:
      - **A (foto):** `placa-acrilico`, `montaje`.
      - **B (osciloscopio, usar `tools/scope_capture.py`):** `pulsos-corriente`,
        `ringing-falso`, `ruido-em`.
      - **C (datos crudos → Claude grafica):** `daq-captura`, `bringup-etapas`,
        `potencia-laser`, `daq-fpga-etapas`.
- [ ] Confirmar **periodo/fechas** → actualizar título y cronograma.
- [ ] (opcional) **D0** capacitancia del piezo (LCR) + **D1** toque sin láser.
- [ ] **Pulido final** reporte + presentación (proofreading, refs LNA/EMI opcionales).
- [ ] **Subir a Overleaf** (1 vez) + exportar PDFs finales.

## Convenciones
- Figuras: nombres con guion `-`, PNG, en `figuras/`. Las generadas NO se editan a mano (editar `gen_figs.py` y reejecutar).
- `.gitignore` cubre artefactos LaTeX y `.vscode/` — **no commitear** esos. El `.vscode` es **por-máquina** (rutas MiKTeX/MacTeX distintas).
- Commits descriptivos; incluir co-author de Claude.

## Build
- **Windows:** `cd reportes/sem4; pwsh -File build.ps1` (MiKTeX + Biber). Presentación: `pdflatex presentacion_sem4.tex` ×2.
- **Mac:** `cd reportes/sem4; latexmk -pdf avances_sem4.tex` (MacTeX; latexmk corre Biber solo). Presentación: `latexmk -pdf presentacion/presentacion_sem4.tex`. Alternativa: **Overleaf**.
- El toolchain es por-máquina (no se versiona). Para regenerar figuras: `python figuras/scripts/gen_figs.py` (necesita numpy + matplotlib).

## División de trabajo sugerida (si trabajan en paralelo)
- **Mac (junto al banco):** capturar/procesar las 9 fotos; mediciones D0/D1.
- **Windows:** integración LaTeX, figuras generadas, pulido del texto.
- Push frecuente; evitar editar el mismo `.tex` a la vez.

## Bitácora (una línea por sesión, al terminar)
- 2026-06-23 — Windows/Claude: Bloque 0 (sync repos OK, ambos limpios). Creado este HANDOFF. Pendiente: capturar las 9 fotos + fechas.
- 2026-06-24 — Mac/Claude: pull de `scope_capture.py` + `.gitignore`. Creado `figuras/CAPTURAS-PENDIENTES.md` (9 figuras clasificadas A/B/C + procedimientos). `Pipfile` con deps. Pendiente: capturas + datos Grupo C + fechas.
- 2026-06-24 — Windows/Claude: **pipeline de captura validado** (cuadrada cal ~1 kHz; formato `Time (us|ms),Voltage (v)` parseable). Creada carpeta `capturas/` (CSVs crudos) + `figuras/scripts/plot_capturas.py` (CSV→figura, autoescala/2 canales). Referencia: `capturas/cal_1kHz_ch2.csv`. Listos para capturar Grupo B/C con señales reales.
- 2026-06-24 — Windows/Claude: `plot_capturas.py` recorta relleno `0,0` del export. Nueva carpeta `evidencia/` (fotos/screenshots/video/frames) + README. Traídos `capturas/laser_wave.csv` (200 MS/s) y `evidencia/screenshots/firstwave.bmp`. `.gitignore`: videos crudos no se versionan (solo frames). Pendiente: confirmar qué mide `laser_wave`; subir video del ruido EM a `evidencia/video/`; captura del pickup CH1/CH2.
- 2026-06-24 — Mac/Claude: evidencia real del DAQ → `figuras/exports/` (`ventana_20260624_200320.csv` + `captura_20260624_200325.png`). Ventana 270 muestras @54 MSPS, 12 bits, LSB 2.4414 mV, offset 2048; transitorio a t≈0.13 µs, min −349/max −15 mV (Vpp 334 mV). Formato propio del GUI del DAQ (`muestra,t_ns,t_us,codigo,mV,prom_mV`) — distinto al del osciloscopio, no va en `capturas/`. Material para la figura `daq-captura` (Grupo C); falta generarla.
- 2026-06-24 — Windows/Claude: generadas figuras reales **`daq-captura.png`** (ventana DAQ 54 MS/s/12 bit + promedio coherente ×32) y **`daq-vs-osc.png`** (comparativa osciloscopio 200 MS/s vs DAQ del MISMO transitorio láser, alineados; timing coherente, amplitud distinta por medir en nodos distintos). Integradas al reporte (17 pág). Script `figuras/scripts/plot_comparativa.py`. Grupo C restante: `bringup-etapas`, `potencia-laser`, `daq-fpga-etapas`. Grupo B: `ringing`, `pulsos`. Falta confirmar fechas.
- 2026-06-24 — Windows/Claude: figura `daq-muestreo.png` (ventana + stem de muestras, puntos de adquisición) vía `figuras/scripts/plot_muestreo.py`. Añadida cita Jim Williams **AN47** (`williams_an47`) + descripción del transitorio = descarga de avalancha (ns, decenas de A). 18 pág. ⚠️ PENDIENTE atribución: el usuario debe confirmar si 67 W/80 A/ZTX415 son medición propia o de la referencia (video Les's Lab) — NO meter como resultado propio sin confirmar.
- 2026-06-24 — Windows/Claude: atribución corregida (67 W/80 A **ignorados**; osc = tensión en el diodo, DAQ = corriente en shunt 0.1 Ω). Figuras nuevas: `pulsos-corriente` (corriente A), `potencia-laser` (estimación V·I preliminar ~15–144 W), `daq-fpga-etapas` (foto `adc_fpga` + diagrama de bloques). Fotos→figuras: `ringing-falso` (=`ring_osc_con_cursor`), `placa-acrilico`, `montaje`. Subidas fotos/videos a `evidencia/fotos/`. **Presentación: 22 láminas** + frame "[VIDEO]" del ruido EM (se reproduce manual). Scripts `plot_potencia.py`, `plot_daq_fpga.py`. PENDIENTE: descongelar `.tex` para integrar todo + corregir caption de `potencia-laser` (ya no es fotodiodo/responsividad); confirmar fechas; factor sense→A si hay atenuación.
- 2026-06-24 — Windows/Claude: **`.tex` descongelado e integrado**. Reporte **21 pág** con figuras reales (fotos + DAQ); quitada `ruido-em` estática (queda como video en la presentación); caption de `potencia-laser` corregido (V·I, ya no fotodiodo). Añadido el **encuadre del hito** (abstract + conclusiones del reporte; conclusiones de la presentación, **22 láminas**): el objetivo era la prueba PA completa; lograr el DAQ a estas frecuencias y con materiales de bajo costo es un hito. Único placeholder restante: **`bringup-etapas`**. Pendiente: fechas del periodo; factor sense→A si hay atenuación.
- 2026-06-24 — Windows/Claude: **`bringup-etapas.png`** creada (escalera de validación 0–8, `plot_bringup.py`) e integrada → **ya no quedan placeholders**. Fechas fijadas: periodo **enero–junio 2026** (título reporte + presentación); cronograma futuro **jul.–dic. 2026**. Reporte **22 pág** + presentación **22 láminas**, ambos compilan limpio. Queda opcional: factor sense→A; subida final a Overleaf.
- 2026-06-24 — Windows/Claude: pasada de lectura del reporte. Arreglos: unidades **MSPS→MS/s** (reporte+presentación, coincide con figuras), objetivo de potencia alineado (V·I, ya no "óptica vía monitor"), bug `~1 muestra`→`$\sim$1`. **PDFs semifinales** en `reportes/sem4/entregables/` (`Avances_Sem4_semifinal.pdf` 6.1 MB, `Presentacion_Sem4_semifinal.pdf` 2.0 MB). Reporte 22 pág + presentación 22 lám., compilan limpio. Pendiente: subida a Overleaf; factor sense→A (opcional).
- 2026-06-24 — Mac/Claude: renombrado el screenshot del GUI del DAQ → **`figuras/daq-python-software.png`** (`git mv` desde `exports/captura_*`); `exports/` queda con `ventana_20260624_200320.csv`.
- 2026-06-24 — Windows/Claude: **revisión mayor** del reporte (reescrito, **15 pág** desde 22). Añadidos: sección **Materiales** (+ link al repo FPGA), subsección **"El costo del ciclo de lectura completo"** (8→12 bit y 27→54 MS/s → BRAM/UART/sincronía) reflejada en el abstract; **encuadre OBJETIVO** de la detección (4 razones con datos); narrativa EM **"se veía acústica en el osc. pero se perdía al pasar al ADC"** + impedancia como **obstáculo**; **figura de software final** = `daq-python-software.png` (adoptado el rename del Mac). Presentación alineada (**24 lám**). MERGE con la rama del Mac resuelto; PDFs semifinales regenerados.
