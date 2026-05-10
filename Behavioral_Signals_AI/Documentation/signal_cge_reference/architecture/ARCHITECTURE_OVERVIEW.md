# Signal CGE Architecture Overview

Signal CGE is organized into data, calibration, model core, solver, scenario, dynamics, diagnostics, reporting, and workbench layers.

```text
signal_cge/
  data/          SAM loading, account mapping, validation
  calibration/   benchmark extraction and share parameters
  model_core/    formal model blocks and equation registry
  solvers/       SAM multiplier fallback and optional solver pathways
  scenarios/     policy shock schemas and templates
  dynamics/      recursive baseline and update stubs
  diagnostics/   pre-run and post-run checks
  reporting/     result explanation and policy brief generation
  workbench.py   canonical orchestration entrypoint
```

The architecture separates model economics from AI assistance. AI modules can read references, compile scenarios, and explain results, but the model engine remains explicit and inspectable.
