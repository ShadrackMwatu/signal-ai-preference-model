# Signal CGE

This product folder contains the CGE/SAM side of Signal:

- `signal_cge/`: canonical CGE/SAM model engine, calibration, diagnostics, knowledge, solver interfaces, and reporting.
- `signal_ai/`: deterministic prompt orchestration, reasoning, memory, and explainability for CGE workflows.
- `policy_ai/`: policy summaries and scenario recommendations.
- `signal_sml/` and `sml_workbench/`: model specification and export layers.
- `cge_workbench/`, `cge_core/`, `cge_engine/`, `signal_execution/`, `signal_modeling_language/`, `policy_intelligence/`, and `solvers/`: compatibility, legacy, or migration layers.
- `models/canonical/`: repo-stored canonical Signal CGE profile and templates.

The public Hugging Face app exposes Signal CGE through `app_routes/signal_cge_route.py`.
