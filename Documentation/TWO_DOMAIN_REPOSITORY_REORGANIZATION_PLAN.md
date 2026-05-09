# Two-Domain Repository Reorganization Plan

Signal is being reorganized around two public product domains:

1. `Behavioral_Signals_AI/`
2. `Signal_CGE/`

The shared root remains the deployment and coordination layer: `app.py`, `requirements.txt`, `README.md`, `tests/`, `app_routes/`, `.github/`, and `.gitignore`.

## Migration Map

| Current folder or file | Assigned domain | Proposed destination | Imported by app.py | Imported by tests | Migration risk |
|---|---|---|---:|---:|---|
| `behavioral_ai/` | Behavioral Signals AI | `Behavioral_Signals_AI/behavioral_ai/` | Via route | Yes | Low; wrapper retained. |
| `adaptive_learning/` | Behavioral Signals AI | `Behavioral_Signals_AI/adaptive_learning/` | Indirect | Limited | Low; documentation package. |
| `adaptive_learning.py` | Behavioral Signals AI | `Behavioral_Signals_AI/adaptive_learning.py` | Via route | Yes | Medium; root wrapper retained. |
| `live_trends/` | Behavioral Signals AI | `Behavioral_Signals_AI/live_trends/` | Via route | Limited | Low; wrapper retained. |
| `explainability/` | Behavioral Signals AI | `Behavioral_Signals_AI/explainability/` | No | No | Low. |
| `explainability.py` | Behavioral Signals AI | `Behavioral_Signals_AI/explainability.py` | Yes | Yes | Medium; root wrapper retained. |
| `trend_intelligence.py` | Behavioral Signals AI | `Behavioral_Signals_AI/trend_intelligence.py` | Yes | Yes | Medium; root wrapper retained. |
| `x_trends.py` | Behavioral Signals AI | `Behavioral_Signals_AI/x_trends.py` | Yes | Yes | Medium; root wrapper retained. |
| `signal_cge/` | Signal CGE | `Signal_CGE/signal_cge/` | Via route | Yes | High; root `signal_cge.py` compatibility package retained. |
| `signal_ai/` | Signal CGE | `Signal_CGE/signal_ai/` | Via route | Yes | Medium; wrapper retained. |
| `policy_ai/` | Signal CGE | `Signal_CGE/policy_ai/` | Via route | Yes | Medium; wrapper retained. |
| `signal_sml/` | Signal CGE | `Signal_CGE/signal_sml/` | No | Limited | Low; wrapper retained. |
| `sml_workbench/` | Signal CGE | `Signal_CGE/sml_workbench/` | Internal imports | Yes | Medium; wrapper retained. |
| `cge_workbench/` | Signal CGE compatibility | `Signal_CGE/cge_workbench/` | No public tab | Yes | Medium; wrapper retained. |
| `cge_core/` | Signal CGE legacy | `Signal_CGE/cge_core/` | No | Yes | Medium; wrapper retained. |
| `cge_engine/` | Signal CGE legacy | `Signal_CGE/cge_engine/` | No | Limited | Low; wrapper retained. |
| `solvers/` | Signal CGE legacy solver prototypes | `Signal_CGE/solvers/` | No | Yes | Medium; wrapper retained. |
| `signal_execution/` | Signal CGE legacy execution | `Signal_CGE/signal_execution/` | Guarded | Yes | Medium; wrapper retained. |
| `signal_modeling_language/` | Signal CGE legacy SML | `Signal_CGE/signal_modeling_language/` | No | Yes | Medium; wrapper retained. |
| `policy_intelligence/` | Signal CGE legacy policy reports | `Signal_CGE/policy_intelligence/` | No | Yes | Medium; wrapper retained. |
| `models/canonical/` | Signal CGE | `Signal_CGE/models/canonical/` | Via route | Yes | Medium; model registry paths updated. |
| `models/` behavioral artifacts | Behavioral Signals AI | deferred root compatibility | Yes | Yes | Medium; not moved yet to avoid breaking trained model paths. |
| `data/` | Shared / mixed | deferred root compatibility | Yes | Yes | Medium; not moved yet to avoid breaking sample-data paths. |

## Move Strategy

This migration moves stable product packages first, updates app routes to use product-domain imports, and keeps root-level wrappers for existing imports. Mixed data and model-artifact paths remain at the root until their consumers can be audited file by file.

## Compatibility Wrappers

Root wrappers are retained for existing imports such as:

- `signal_cge.*`
- `signal_ai.*`
- `policy_ai.*`
- `sml_workbench.*`
- `cge_workbench.*`
- `cge_core.*`
- `solvers.*`
- `adaptive_learning`
- `explainability`

These wrappers should be treated as temporary migration aids, not new development locations.

## Tests Required

- App import check.
- Public two-tab UI check.
- Behavioral route domain import check.
- Signal CGE route domain import check.
- Canonical model profile load check.
- Legacy compatibility import check.
- Full regression test suite.
