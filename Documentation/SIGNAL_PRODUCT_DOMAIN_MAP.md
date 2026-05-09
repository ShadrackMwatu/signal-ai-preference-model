# Signal Product Domain Map

Signal now has two public product domains:

1. **Behavioral Signals AI**
2. **Signal CGE**

The Hugging Face app exposes only those two public tabs. Backend folders now live primarily under `Behavioral_Signals_AI/` and `Signal_CGE/`; root-level wrappers remain in place for compatibility, tests, and future migration.

## Domain Ownership

## Current Product Roots

| Folder | Purpose | Assigned domain | Used by `app.py` | Used by tests | Recommended action |
|---|---|---|---:|---:|---|
| `Behavioral_Signals_AI/` | Behavioral intelligence product root. | Behavioral Signals AI | Via route | Yes | New canonical home for behavioral-domain code. |
| `Signal_CGE/` | CGE/SAM product root. | Signal CGE | Via route | Yes | New canonical home for CGE-domain code. |
| root compatibility wrappers | Preserve imports such as `signal_cge`, `signal_ai`, `policy_ai`, `sml_workbench`, `cge_core`, `solvers`, `adaptive_learning`, and `explainability`. | Legacy / compatibility | Indirect | Yes | Retain temporarily until imports are fully migrated. |

| Folder | Purpose | Assigned domain | Used by `app.py` | Used by tests | Recommended action |
|---|---|---|---:|---:|---|
| `app.py` | Gradio entrypoint and two-tab public UI. | Shared infrastructure | Yes | Yes | Keep lightweight; route through `app_routes/`. |
| `app_routes/` | Public routing layer for product-domain backends. | Shared infrastructure | Yes | Yes | Keep as the public boundary between UI and backend packages. |
| `behavioral_ai/` | Behavioral intelligence package marker and future behavioral domain code. | Behavioral Signals AI | Via route | Yes | Keep; add behavioral-specific code here over time. |
| `adaptive_learning/` | Adaptive learning package marker for behavioral feedback layer. | Behavioral Signals AI | Via route | Yes | Keep; avoid CGE dependencies. |
| `adaptive_learning.py` | Feedback logging and retraining aggregation utilities. | Behavioral Signals AI | Via route | Yes | Keep as active behavioral support code. |
| `live_trends/` | Live trends package marker. | Behavioral Signals AI | Via route | Limited | Keep; avoid CGE dependencies. |
| `trend_intelligence.py` | Trend enrichment and summarization logic. | Behavioral Signals AI | Yes | Yes | Keep active for Behavioral Signals AI tab. |
| `x_trends.py` | Public aggregate X trend fetch/fallback logic. | Behavioral Signals AI | Yes | Yes | Keep active; no individual tracking. |
| `explainability.py` | Behavioral prediction explanation helpers. | Behavioral Signals AI | Yes | Yes | Keep active for behavioral explanations. |
| `explainability/` | Explainability documentation. | Behavioral Signals AI | No | No | Keep documentation-only. |
| `ml/` | ML training, feature engineering, evaluation, and prediction utilities. | Behavioral Signals AI | Indirect | Yes | Keep active for behavioral model lifecycle. |
| `models/` | Mixed model storage. `models/canonical/` belongs to Signal CGE; behavioral model bundles also live here. | Shared infrastructure | Yes | Yes | Keep split documented; ignore `models/Model/` runtime workspace. |
| `models/canonical/` | Repo-stored canonical Signal CGE model profile and templates. | Signal CGE | Via route | Yes | Keep version-controlled and lightweight. |
| `models/Model/` | Local persistent runtime model workspace. | Generated / ignored | No | No | Keep local-only; do not commit artifacts. |
| `models_ml/` | ML experiment placeholders. | Behavioral Signals AI | No | Limited | Keep lightweight placeholders; avoid large artifacts. |
| `signal_cge/` | Canonical CGE/SAM model engine, knowledge, diagnostics, solvers, local workspace config. | Signal CGE | Via route | Yes | Keep as the official CGE backend. |
| `signal_ai/` | AI CGE prompt routing, reasoning, memory, and explainability. | Signal CGE | Via route | Yes | Keep active for Signal CGE prompt workflow. |
| `policy_ai/` | Policy summaries and scenario recommendations. | Signal CGE | Via route | Yes | Keep active. |
| `signal_sml/` | Future canonical SML namespace. | Signal CGE | No | Limited | Keep migration target. |
| `sml_workbench/` | Current active SML parser/exporter backend. | Signal CGE | Imported for compatibility/internal functions | Yes | Keep internal; not public tab. |
| `cge_workbench/` | Compatibility wrappers and older workbench paths. | Legacy / compatibility | No public tab | Yes | Keep until imports are migrated. |
| `Documentation/signal_cge_reference/` | Canonical Signal CGE reference library. | Signal CGE | Via route | Yes | Keep authoritative. |
| `Documentation/` | Project documentation. | Shared infrastructure | No | Limited | Keep; maintain domain-specific docs. |
| `cge_core/` | Early CGE/SAM core utilities. | Legacy / compatibility | No | Yes | Keep deprecated; migrate useful pieces to `signal_cge/`. |
| `cge_engine/` | Historical CGE engine namespace. | Legacy / compatibility | No | No | Keep deprecated until safe removal. |
| `solvers/` | Early solver registry and solver prototypes. | Legacy / compatibility | No | Yes | Keep deprecated; migrate useful pieces to `signal_cge/solvers/`. |
| `signal_execution/` | Older SML execution workflow. | Legacy / compatibility | Guarded internal import | Yes | Keep until execution routing is migrated. |
| `signal_modeling_language/` | Earlier SML grammar/parser implementation. | Legacy / compatibility | No | Yes | Keep deprecated; migrate to `signal_sml/` later. |
| `policy_intelligence/` | Older policy report utilities. | Legacy / compatibility | No | Yes | Keep deprecated; migrate durable parts to `policy_ai/`. |
| `learning/` | Teaching explainer content. | Legacy / compatibility | Imported internally | Yes | Keep internal; not public tab. |
| `signal_learning/` | Adaptive learning implementation and proposal workflow. | Shared infrastructure | Guarded internal import | Yes | Keep internal; not public tab. |
| `learning_memory/` | Learning memory store utilities. | Shared infrastructure | Indirect | Yes | Keep internal. |
| `learning_versions/` | Historical learning version notes. | Legacy / compatibility | No | No | Keep historical. |
| `src/` | General research, data, ML, and older CGE framework code. | Shared infrastructure | Guarded internal import | Yes | Keep until migrated into clearer packages. |
| `api/` | FastAPI routes and schemas. | Shared infrastructure | No | Yes | Keep separate from Hugging Face UI. |
| `backends/` | Backend adapters, including GAMS support. | Signal CGE | No public dependency | Yes | Keep optional; no deployment requirement. |
| `data/` | Sample and training data. | Shared infrastructure | Yes | Yes | Keep lightweight, non-sensitive data only. |
| `config/` | General app configuration. | Shared infrastructure | Yes | Limited | Keep. |
| `.github/` | CI/deployment workflows. | Shared infrastructure | No | No | Keep. |
| `tests/` | Test suite. | Shared infrastructure | No | Yes | Keep broad regression coverage. |
| `outputs/` | Generated outputs. | Generated / ignored | Writes downloads | Ignored | Keep ignored except `.gitkeep`. |
| `cge_workbench/outputs/` | Generated CGE run outputs. | Generated / ignored | Indirect writes | Ignored | Keep ignored. |
| `docker/` | Local deployment/runtime assets. | Shared infrastructure | No | No | Keep reviewed; ignore binaries. |
| `.venv/`, `.cache/`, `__pycache__/`, `pytest-cache-*` | Local runtime/cache folders. | Generated / ignored | No | No | Keep ignored, do not commit. |

## Public App Routing

- `Behavioral Signals AI` tab routes through `app_routes.behavioral_route` and imports product code from `Behavioral_Signals_AI/`.
- `Signal CGE` tab routes through `app_routes.signal_cge_route` and imports product code from `Signal_CGE/`.
- Signal CGE uses repo-stored canonical files by default:
  - `Signal_CGE/models/canonical/signal_cge_master/model_profile.yaml`
  - `Documentation/signal_cge_reference/`
  - `Signal_CGE/signal_cge/knowledge/`

## Remaining Legacy Folders

The following root imports remain as compatibility wrappers: `cge_core`, `cge_engine`, `solvers`, `signal_execution`, `signal_modeling_language`, `policy_intelligence`, `cge_workbench`, `sml_workbench`, `signal_ai`, `signal_cge`, `policy_ai`, `adaptive_learning`, `explainability`, `trend_intelligence`, and `x_trends`. They should not be deleted until imports and tests are migrated.
