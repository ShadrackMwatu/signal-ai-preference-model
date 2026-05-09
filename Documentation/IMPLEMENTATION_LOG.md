# Implementation Log

## AI-Native CGE Chat Studio Foundation

Added `signal_ai/` and `policy_ai/` packages to support deterministic AI-native CGE workflows without external LLM APIs. The implementation includes prompt routing, scenario compilation, economic reasoning, local memory, mechanism explanation, policy summaries, and recommendations.

Updated `cge_workbench/interpreters/natural_language_to_scenario.py` so compiled scenarios include both existing workbench fields and chat-studio fields:

- `model`
- `simulation_type`
- `shock_account`
- `shock_type`
- `shock_size`
- `target_outputs`
- `closure`
- `notes`
- `validation_warnings`

Updated `app.py` with a new **AI CGE Chat Studio** tab while preserving existing Signal tabs and Hugging Face deployment entrypoints.

## Remaining Limitations

The Python fallback remains a SAM multiplier model, not a full CGE equilibrium solver. GAMS integration remains optional. Pyomo is not required and has not been added to mandatory dependencies.

## Canonical Signal CGE Knowledge System

Added the permanent Signal CGE reference structure under `Documentation/signal_cge_reference/` and stored the adapted user guide in both Word and PDF formats. Added equation references, calibration workflow documentation, closure notes, experiment workflow notes, and AI integration notes.

Added `Documentation/SIGNAL_CGE_KNOWLEDGE_BASE.md` as the high-level canonical knowledge file covering the Signal CGE philosophy, SAM-driven architecture, calibration, closures, recursive dynamics, experiment workflow, reporting, solver pathways, scenarios, AI-assisted policy workflow, SML relationship, learning integration, and diagnostics.

Added `models/canonical/signal_cge_master/model_profile.yaml` and connected it to `signal_cge/model_registry.py`. Added `signal_cge/knowledge/` helpers so Signal AI modules and future LLM integrations can list, load, and index canonical references without adding a YAML dependency.

The canonical layer is documentation and registry infrastructure only. It does not change model execution logic, Hugging Face startup behavior, or the current SAM multiplier fallback.

## Two-Tab Public Interface

Simplified the public Hugging Face app to two tabs: **Behavioral Signals AI** and **Signal CGE**. The existing behavioral prediction workflow remains public. Older public CGE-facing tabs for the framework, AI chat studio, SML workbench, and learning were hidden from the app UI but their backend modules remain available internally.

Added `run_signal_cge_prompt(prompt, uploaded_file=None)` as the public Signal CGE callable. It loads the canonical model profile and reference index from the repository, interprets prompts, checks readiness, runs the available SAM multiplier/prototype calibration backend, and returns display-ready scenario, readiness, diagnostics, results, policy interpretation, and downloadable report paths.

Added explicit import-tariff parsing for prompts such as `reduce import tariffs on cmach by 10%`. Signal now reports the full-solver limitation clearly instead of implying full equilibrium CGE solving.

Updated the Signal CGE tab so no upload is required. The public workflow now defaults to `models/canonical/signal_cge_master/model_profile.yaml` and `Documentation/signal_cge_reference/`, places custom uploads in a collapsed optional accordion, shows result summary cards, returns chart-ready scenario effects, and creates JSON, CSV, and Markdown downloads after every run.

## Signal CGE Repo Knowledge and Adaptive Learning

Added scenario-aware knowledge retrieval from repository-stored Signal CGE reference materials and threaded the knowledge context into Signal CGE outputs, diagnostics, policy interpretation, downloads, and the public UI. Added metadata-only simulation learning memory under `outputs/signal_cge_learning/`, deterministic adaptive prompt rules, learning summaries, and model improvement suggestions. Runtime learning logs are ignored from Git by default.
