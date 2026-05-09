# AI-Native CGE Roadmap

## Implemented

- Deterministic intent classification.
- Natural-language scenario compilation with Signal scenario fields.
- Economic reasoning checks for shock accounts, closures, simulation types, care suffixes, and fallback caveats.
- Local simulation memory stored under `cge_workbench/outputs/simulation_history.json`.
- Plain-English mechanism explanations.
- Policy summary and next-scenario recommendations.
- Gradio **AI CGE Chat Studio** tab.

## Placeholder

- Full CGE equilibrium solving remains a future backend.
- Recursive dynamic CGE workflows remain a placeholder.
- Scenario comparison currently compiles and runs through the same SAM fallback rather than a multi-run comparison table.

## Future Pyomo/Open-Source Pathway

Pyomo can be added as an optional dependency for open-source equilibrium modeling, calibration experiments, and solver-backed replication. It should not be required for `app.py` startup on Hugging Face Spaces until the pathway is stable and optional imports are guarded.

## Future GAMS Pathway

The optional GAMS runner should be connected to the authoritative Signal CGE model files, baseline data, GDX extraction, listing-file diagnostics, and reproducible run folders. If GAMS is unavailable, the app should continue to use the Python fallback.
