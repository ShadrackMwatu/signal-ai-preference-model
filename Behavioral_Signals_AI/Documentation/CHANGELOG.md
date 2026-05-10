# Signal Changelog

All notable milestones are summarized here. Dates use the local project timeline where known.

## 2026-05-08

### Added

- Comprehensive documentation system under `Documentation/`.
- README navigation for architecture, deployment, live trends, behavioral AI, SML/CGE, learning, privacy, and roadmap.
- Visible static `Live Trend Intelligence` card in the Behavioral Signals AI tab for immediate page-load visibility.

### Fixed

- Removed circular dependency from `trend_intelligence.py` to `app.py`.
- Added a local lightweight trend-intelligence fallback to avoid Gradio re-import failures.
- Confirmed app startup with a non-blocking Gradio launch smoke test.

## 2026-05-07

### Added

- Live trend data model using public aggregate X/Twitter topics and demo fallback trends.
- Trend proxy conversion into demand-intelligence features.
- Privacy validation for public aggregate trend records.
- SML CGE Workbench tab with parser, validator, GAMS export, Pyomo export, and report download wiring.
- Learning tab with AI teaching explanations and adaptive-learning action outputs.

### Improved

- Behavioral Signals AI dashboard with additional visual components:
  - confidence gauge
  - signal strength gauge
  - momentum indicator
  - opportunity radar
  - key driver cards

## 2026-05-04 to 2026-05-06

### Added

- SML parser, validator, grammar, schema, and examples.
- CGE core modules for SAM handling, calibration, accounts, closures, shocks, equations, and validation.
- Signal execution runner, diagnostics, workflow, logs, and output generation.
- Solver abstraction for GAMS, Python NLP, and fixed-point fallback.
- Policy intelligence report and interpretation layers.
- Adaptive learning workflow, feedback collection, learning store, and adaptation proposals.

## Earlier Milestones

### Added

- Initial Signal AI dashboard.
- Behavioral demand prediction model.
- Training pipeline and saved model artifacts.
- FastAPI endpoints for health, demand prediction, counties, opportunities, segments, and market access.
- Synthetic data generation and privacy-preserving data pipeline helpers.

