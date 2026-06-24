# Proyecto: Reportes de tesis — Tomografía Fotoacústica e IA (LUMAT–UAZ)

Repositorio de los **reportes de avance por semestre** (LaTeX) del doctorado de
Eduardo Santos Mena (asesores: Dr. Samuel Pérez Huerta, Dr. Augusto David Ariza
Flores). Separado del repo de firmware `photoacoustic_daq`.

## Antes de trabajar (importante)
**Lee `reportes/sem4/HANDOFF.md`** — es la fuente única de verdad del estado, los
pendientes y el protocolo de sincronización entre máquinas (Windows ↔ Mac). Las
sesiones de Claude Code NO se comparten entre computadoras; ese archivo SÍ.
Protocolo: `git pull` → leer HANDOFF → trabajar → actualizar HANDOFF → commit → push.

## Contexto clave (Sem 4)
- Enfoque del reporte: **el DAQ (sistema de adquisición) es el avance central**; la
  detección ultrasónica pasa a **trabajo futuro** (la etapa crítica anticipada).
- Documento: `reportes/sem4/avances_sem4.tex`. Presentación:
  `reportes/sem4/presentacion/presentacion_sem4.tex` (Beamer, tema metropolis).
- Figuras técnicas reales: generadas por `reportes/sem4/figuras/scripts/gen_figs.py`
  (matplotlib). Las fotos del experimento van como placeholders hasta capturarlas.
- Plan/diagnóstico de fondo: `PLAN_ARGUMENTATIVO_SEM4.md`.

## Convenciones
- Figuras: nombres con guion `-` (no `_`), PNG, en `figuras/`. No editar a mano las
  generadas (editar `gen_figs.py` y reejecutar).
- No commitear artefactos LaTeX ni `.vscode/` (ya en `.gitignore`; `.vscode` es
  específico de cada máquina por las rutas del toolchain).
- Build: Windows `pwsh -File reportes/sem4/build.ps1`; Mac `latexmk -pdf` (MacTeX) o
  Overleaf. Detalle en `reportes/sem4/HANDOFF.md`.
- Commits descriptivos, con `Co-Authored-By: Claude`.
