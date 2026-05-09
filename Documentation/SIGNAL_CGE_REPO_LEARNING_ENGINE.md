# Signal CGE Repo Learning Engine

The repo learning engine connects the public Signal CGE prompt interface to the repository's canonical knowledge and runtime learning memory.

## Knowledge Sources

- `Signal_CGE/models/canonical/`
- `Documentation/signal_cge_reference/`
- `Documentation/SIGNAL_CGE_KNOWLEDGE_BASE.md`
- `Documentation/SIGNAL_CGE_MODEL_STRUCTURE.md`
- `Documentation/SIGNAL_CGE_REORGANIZATION_PLAN.md`
- `Documentation/SIGNAL_CGE_REPO_KNOWLEDGE_INTEGRATION.md`

## Runtime Memory

Simulation events are stored as JSONL metadata in:

`Signal_CGE/outputs/signal_cge_learning/simulation_memory.jsonl`

Learning summaries are written to:

`Signal_CGE/outputs/learning_summaries/`

Model gap reports are written to:

`Signal_CGE/outputs/model_improvement_reports/`

Generated JSON files are ignored by Git. `.gitkeep` files preserve the folder structure.

## What Is Stored

- prompt text,
- parsed scenario metadata,
- scenario type,
- target account,
- backend used,
- readiness status,
- diagnostics summary,
- result summary,
- interpretation summary,
- references used,
- recommended next simulations.

## What Is Not Stored

- uploaded SAM files,
- private user data,
- large runtime artifacts,
- GDX/G00/listing files,
- temporary logs,
- solver checkpoints.
