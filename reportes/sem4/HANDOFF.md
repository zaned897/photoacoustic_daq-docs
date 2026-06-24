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

## Estado actual (2026-06-23)
- `avances_sem4.tex` — **16 pág**, enfoque **DAQ-central**, detección → trabajo futuro. Compila limpio.
- `presentacion/presentacion_sem4.tex` — **21 láminas** (tema metropolis).
- Figuras técnicas reales: generadas por `figuras/scripts/gen_figs.py` (matplotlib) — ya incluidas.
- Figuras de foto: **PLACEHOLDERS pendientes** (el macro `\figph` compila igual).

## Pendientes para terminar
- [ ] **9 fotos/capturas** en `figuras/` (nombres con guion `-`, PNG): `ringing-falso`,
      `ruido-em`, `pulsos-corriente`, `potencia-laser`, `placa-acrilico`, `montaje`,
      `daq-fpga-etapas`, `daq-captura`, `bringup-etapas`. (Detalle en `README.md`.)
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
