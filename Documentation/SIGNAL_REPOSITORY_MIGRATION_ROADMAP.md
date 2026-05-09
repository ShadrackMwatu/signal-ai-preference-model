# Signal Repository Migration Roadmap

This roadmap keeps the deployed Hugging Face app stable while the repository converges on clearer package ownership.

## Phase 1: Document Duplication and Clarify Active Folders

Status: in progress.

- Treat `signal_cge/` as the official CGE/SAM model engine.
- Treat `signal_ai/` as the AI chat, reasoning, memory, and explainability layer.
- Treat `policy_ai/` as the current policy summary and scenario recommendation service.
- Keep `sml_workbench/` as the active SML implementation until migration.
- Keep `learning/` as the active teaching layer until migration.
- Keep `cge_workbench/` as a compatibility wrapper for old CGE imports.
- Mark older overlapping folders with deprecation notes instead of deleting them.

## Phase 2: Move Reusable CGE Code into `signal_cge/`

Target folders for review:

- `cge_core/`
- `cge_engine/`
- `solvers/`
- `signal_execution/`

Migration rule:

- Move only reusable, tested logic.
- Add tests before changing import ownership.
- Keep wrappers in legacy folders until all app and test imports are updated.
- Avoid adding solver dependencies unless they are optional and deployment-safe.

## Phase 3: Move SML Implementation into `signal_sml/`

Current active implementation:

- `sml_workbench/`

Legacy implementation:

- `signal_modeling_language/`

Target:

- `signal_sml/parser/`
- `signal_sml/validators/`
- `signal_sml/exporters/`
- `signal_sml/templates/`
- `signal_sml/simulation_bundles/`

Migration rule:

- Keep `sml_workbench/` imports working for the Gradio app.
- Keep old examples readable.
- Move parser and validator behavior with regression tests.

## Phase 4: Move Learning Implementation into `signal_learning/`

Current teaching implementation:

- `learning/`

Current adaptive implementation:

- `signal_learning/`

Target:

- Use `signal_learning/` as the long-term canonical learning namespace.
- Keep `learning/` as a compatibility package for the app's current teaching tab until the UI imports are migrated.

## Phase 5: Retire Deprecated Folders

Deprecated folders can be retired only after:

- `app.py` no longer imports them.
- `tests/` no longer imports them.
- The Hugging Face app imports successfully.
- Full tests pass.
- A release note documents the removal.

Candidate retirement order:

1. `cge_engine/`, if it remains unused.
2. `policy_intelligence/`, after durable logic moves into `policy_ai/`.
3. `signal_modeling_language/`, after SML examples and parser tests move to `signal_sml/`.
4. `solvers/`, after solver registry behavior moves to `signal_cge/solvers/`.
5. `cge_core/`, after SAM and calibration behavior is fully covered in `signal_cge/`.
6. `signal_execution/`, after execution workflows are split between `signal_cge/` and `signal_sml/`.

## Migration Risks

- Hidden imports in tests or notebooks may still depend on older paths.
- Hugging Face startup can fail if `app.py` imports are changed without fallback guards.
- Moving SML parser behavior too early could break export workflows.
- Solver code may imply unavailable dependencies; optional pathways must remain guarded.
- Generated outputs and model artifacts must remain out of migration commits unless explicitly reviewed.

## Required Tests

Run these before and after each migration phase:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_repository_structure.py -q
.\.venv\Scripts\python.exe -m pytest -q
```
