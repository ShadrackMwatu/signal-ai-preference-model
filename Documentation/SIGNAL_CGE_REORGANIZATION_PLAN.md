# Signal CGE Reorganization Plan

## Current Structure Problems

Signal has grown through several working layers: `cge_workbench`, `sml_workbench`, `signal_ai`, `policy_ai`, solver utilities, diagnostics, learning modules, and documentation. The system works, but CGE responsibilities are spread across multiple folders:

- formal model blocks live under `cge_workbench/model_core`
- calibration lives under `cge_workbench/calibration`
- diagnostics live under `cge_workbench/diagnostics`
- runners live under `cge_workbench/runners`
- result explanation and policy brief generation live under `cge_workbench/interpreters`
- AI chat orchestration lives under `signal_ai`
- SML parsing/export lives under `sml_workbench`

This creates overlap between the economic model engine, the chat interface, the SML specification layer, and the learning layer.

## Proposed Target Structure

The canonical economic model package is now:

```text
signal_cge/
├── data/
├── calibration/
├── model_core/
├── solvers/
├── scenarios/
├── dynamics/
├── diagnostics/
├── reporting/
├── model_registry.py
└── workbench.py
```

Supporting layers remain:

- `signal_ai/`: conversational scenario interface and reasoning.
- `signal_sml/`: readable model specification namespace.
- `signal_learning/`: teaching, documentation, and guided workflows.
- `policy_ai/`: policy summaries and scenario recommendations.

## Old-To-New Folder Mapping

| Old folder/file | New canonical location | Action |
|---|---|---|
| `cge_workbench/model_core/` | `signal_cge/model_core/` | Mirrored now; old modules are compatibility wrappers. |
| `cge_workbench/calibration/` | `signal_cge/calibration/` | Mirrored now; old modules are compatibility wrappers. |
| `cge_workbench/diagnostics/` | `signal_cge/diagnostics/` | Mirrored now; old modules are compatibility wrappers. |
| `cge_workbench/runners/` | `signal_cge/solvers/` | Mirrored now; old modules are compatibility wrappers. |
| `cge_workbench/interpreters/result_explainer.py` | `signal_cge/reporting/result_explainer.py` | Mirrored now; old module is a compatibility wrapper. |
| `cge_workbench/interpreters/policy_brief_generator.py` | `signal_cge/reporting/policy_brief_generator.py` | Mirrored now; old module is a compatibility wrapper. |
| `cge_workbench/interpreters/natural_language_to_scenario.py` | `signal_cge/scenarios/scenario_schema.py` | Mirrored now; old module is a compatibility wrapper. |
| `cge_workbench/scenarios/` | `signal_cge/scenarios/` | YAML templates copied; Python scenario helpers added. |
| `sml_workbench/` | `signal_sml/` over time | New namespace created; existing implementation remains in place. |

## What Was Moved Now

This phase creates `signal_cge/` and mirrors stable modules into it. It updates app and AI chat imports to use `signal_cge` as the canonical CGE backend.

## Compatibility Wrappers

`cge_workbench` is retained during transition. Existing imports continue to work through thin wrappers that point to `signal_cge`. This avoids breaking the Hugging Face app, tests, and any local notebooks that still import from `cge_workbench`.

## Deprecated Later

After at least one stable release using `signal_cge`, the following can be deprecated:

- direct imports from `cge_workbench/model_core`
- direct imports from `cge_workbench/calibration`
- direct imports from `cge_workbench/runners`
- direct imports from `cge_workbench/diagnostics`

The `cge_workbench` folder should not be removed until all app, test, documentation, and user-facing examples use `signal_cge`.

## Migration Risks

- Broken imports if wrappers are incomplete.
- Divergence if future changes are made in `cge_workbench` instead of `signal_cge`.
- Confusion between SML specification and CGE execution.
- Hugging Face startup failures if app imports become heavy or require optional solver dependencies.

## Required Tests

- `signal_cge` imports.
- Old `cge_workbench` imports still work.
- Calibration pipeline still works.
- Model registry returns expected fields.
- Model readiness dashboard returns expected statuses.
- `app.py` imports successfully.
- AI CGE Chat Studio still runs.
- Full test suite passes.
