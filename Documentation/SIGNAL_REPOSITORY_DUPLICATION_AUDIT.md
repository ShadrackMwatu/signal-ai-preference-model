# Signal Repository Duplication Audit

Date: 2026-05-09

This audit records the package ownership decisions after the `signal_cge/` reorganization. It is intentionally conservative: no folders are removed, and legacy modules remain available until tests and app imports confirm they can be retired.

## Current App Imports

The deployed Gradio app imports these repository layers directly:

- `signal_cge/` through `signal_cge.solvers.gams_runner` and `signal_cge.workbench`
- `signal_ai/` through the AI CGE chat orchestrator and response formatting helpers
- `sml_workbench/` through SML parsing, validation, and export helpers
- `learning/` through the teaching explainer
- `signal_execution/` inside the guarded advanced workflow block
- `signal_learning/` inside the guarded advanced workflow block

The app does not directly import `cge_workbench/`, `cge_core/`, `cge_engine/`, `solvers/`, `signal_modeling_language/`, or `policy_intelligence/`, although several of those folders are still imported by tests and older workflows.

## Ownership Classification

| Folder | Classification | Purpose | Imported by `app.py` | Imported by tests | Duplicated by `signal_cge/` | Recommended action |
|---|---|---|---:|---:|---:|---|
| `signal_cge/` | A. canonical package | Official CGE/SAM model engine: data, calibration, model core, solvers, diagnostics, scenarios, reporting, readiness, and workbench API. | Yes | Yes | No, it is the canonical target | Keep as the source of truth for new CGE development. |
| `signal_ai/` | A. canonical package | AI chat, intent routing, scenario orchestration, reasoning, memory, and explainability. | Yes | Yes | No | Keep as the source of truth for AI-native workflow logic. |
| `policy_ai/` | A. canonical package | Current policy summary and scenario recommendation service used by AI chat flows. | Indirectly | Yes | No | Keep active; consolidate older policy report utilities later if useful. |
| `sml_workbench/` | B. active legacy package | Current deployed SML parser, validator, exporter, examples, and workbench utilities. | Yes | Yes | No | Keep active until migrated into `signal_sml/`. |
| `learning/` | B. active legacy package | Current deployed learning explainer and teaching content. | Yes | Yes | No | Keep active until migrated into `signal_learning/`. |
| `signal_learning/` | B. active migration package | Adaptive learning, implementation proposals, learning store, and pattern extraction. | Yes, guarded | Yes | No | Keep active. Treat as the future canonical learning namespace, but do not remove `learning/` yet. |
| `cge_workbench/` | C. compatibility wrapper | Legacy CGE workbench namespace retained for older imports. Most stable code now mirrors or forwards to `signal_cge/`. | No | Yes | Yes | Keep wrappers during transition. New CGE development should use `signal_cge/`. |
| `signal_sml/` | C. compatibility or future namespace | Placeholder future canonical SML namespace. | No | Limited | No | Keep as migration target. Move `sml_workbench/` code gradually. |
| `cge_core/` | D. deprecated duplicate | Early SAM/CGE account, calibration, closure, equation, result, shock, and validation utilities. | No | Yes | Partly | Mark deprecated. Migrate reusable pieces into `signal_cge/` only after tests cover behavior. |
| `cge_engine/` | D. deprecated duplicate | Historical CGE engine namespace with minimal content. | No | No | Partly | Mark deprecated. Archive later if no imports remain. |
| `solvers/` | D. deprecated duplicate | Early fixed-point, GAMS, Python NLP, and solver registry abstractions. | No | Yes | Yes | Mark deprecated. Migrate reusable solver patterns into `signal_cge/solvers/`. |
| `signal_execution/` | B. active legacy package | Execution configuration, workflow, diagnostics, logging, and runner for SML-based runs. | Yes, guarded | Yes | Partly | Mark legacy but not inactive. Keep until execution responsibilities are clearly moved into `signal_cge/` and `signal_sml/`. |
| `signal_modeling_language/` | D. deprecated duplicate | Earlier SML grammar, parser, schema, validator, and examples. | No | Yes | No | Mark deprecated in favor of `sml_workbench/` now and `signal_sml/` later. |
| `policy_intelligence/` | D. deprecated duplicate | Earlier policy report, templates, interpreter, and scenario comparison utilities. | No | Yes | Partly | Mark deprecated. Migrate durable report patterns into `policy_ai/` or `signal_cge/reporting/`. |

## Production-Active Folders

- `app.py`
- `signal_cge/`
- `signal_ai/`
- `policy_ai/`
- `sml_workbench/`
- `learning/`
- `signal_learning/` for guarded adaptive-learning workflows

## Compatibility and Migration Folders

- `cge_workbench/`
- `signal_sml/`
- `signal_learning/`

## Experimental or Deprecated Folders

- `cge_core/`
- `cge_engine/`
- `solvers/`
- `signal_execution/`
- `signal_modeling_language/`
- `policy_intelligence/`

`signal_execution/` is deprecated as a CGE ownership namespace, but remains active because the app and tests still use it for guarded SML execution workflows.

## Safe Actions Taken

- Added this audit.
- Added explicit deprecation notes to legacy folders.
- Added import-safety tests for the canonical, active, and compatibility namespaces.
- Updated the README structure section so new contributors know where to work first.

No folders were deleted, no generated artifacts were committed, and no dependencies were added.
