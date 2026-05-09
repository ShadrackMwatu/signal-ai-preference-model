# Signal CGE Architecture

Signal now has two complementary modules:

1. Behavioral Signals AI for revealed demand and market intelligence.
2. Signal CGE Modelling Framework for AI-assisted CGE model specification,
   execution, GAMS compatibility, solver orchestration, and policy reporting.

Core principle:

- GAMS is a modelling language and execution environment.
- A solver is the mathematical engine.
- Signal is developing its own modelling language and execution environment
  first, while initially relying on GAMS and Python solver backends for numeric
  computation.

Main layers:

- `signal_modeling_language/`: SML grammar, parser, schema, validator, examples.
- `signal_execution/`: runner, workflow, config, logs, diagnostics, outputs.
- `backends/gams/`: GAMS-compatible code generation and execution helpers.
- `solvers/`: solver abstraction for GAMS, SciPy NLP, and fixed-point fallback.
- `cge_core/`: SAM, calibration, accounts, closures, shocks, equations, results.
- `policy_intelligence/`: policy interpretation, reports, scenario comparison.
- `api/`: FastAPI routes for parse, validate, run, and result retrieval.
- `app.py`: Hugging Face-compatible Gradio dashboard entry point.
