# Behavioral Signals AI Module Inventory

## Repository And Local Synchronization

| Area | GitHub `origin/main` | Local Windows folder | Sync status |
|---|---|---|---|
| `Behavioral_Signals_AI/` | Present | Present | In sync before this documentation update |
| `Behavioral_Signals_AI/app/` | Present | Present | In sync |
| `Behavioral_Signals_AI/models/` | Present | Present | In sync, includes committed binary artifacts |
| `Behavioral_Signals_AI/Documentation/` | Present | Present | In sync, but contains mixed Behavioral and Signal CGE docs |
| `Behavioral_Signals_AI/tests/` | Not present in inspected tree | Not present | Tests currently live mainly under `Signal_CGE/tests/` |
| Runtime outputs | Not a formal Behavioral domain | No active `Behavioral_Signals_AI/outputs/` inspected | Missing as a first-class runtime area |

The public GitHub page was available and showed the normalized repository with `Behavioral_Signals_AI/`, `Signal_CGE/`, root `app_routes/`, and root deployment files. Local `HEAD` and `origin/main` matched at `87c8b4a`.

## Top-Level Behavioral Folders

| Folder | Purpose | Runtime status | Notes |
|---|---|---|---|
| `adaptive_learning/` | Privacy-safe feedback logging and future retraining support | Partially active | Uses `data/feedback/feedback_log.csv`, which should be normalized to `Behavioral_Signals_AI/utils/data/feedback/` or `Behavioral_Signals_AI/outputs/feedback/`. |
| `api/_merged/` | FastAPI-style merged API implementation | Not public runtime | Useful future API base, but imports still rely on `src...`. |
| `app/routes/` | Product route hooks | Active | `behavioral_route.py` is the cleanest Behavioral public route. `signal_cge_route.py` does not belong here long-term. |
| `app/src/` | Rich behavioral pipeline implementation | Active in tests and future pipeline | Contains data pipeline, features, models, intelligence, evaluation, and historical CGE helpers. |
| `behavioral_ai/_merged/` | Package marker / migrated placeholder | Mostly placeholder | Should become the future public behavioral service namespace or be retired. |
| `Documentation/` | Documentation | Active but mixed | Contains Behavioral docs and many Signal CGE docs. Needs domain cleanup. |
| `explainability/` | Driver explanations and privacy notice | Active | `__init__.py` exports explanation, but privacy is nested under `explainability/privacy.py` while app tries `Behavioral_Signals_AI.privacy`. |
| `live_trends/` | X/Twitter trend fetch and proxy scoring | Partially active | Has demo fallback and aggregate privacy guard, but import paths are currently fragile. |
| `ml/_merged/` | Generic ML toolkit from earlier architecture | Experimental | Contains useful tools but duplicates `app/src/models` and `app/src/features`. |
| `models/` | Committed behavioral model artifacts | Active but needs governance | Includes `.pkl` and `.joblib` artifacts. Consider Git LFS/model registry discipline. |
| `training/` | Standalone training script | Partially active | Path roots point to `training/data` and `training/models`, not current domain data/model folders. |
| `utils/data/` | Sample and synthetic datasets | Active for development | Contains aggregate sample data, feedback log, training CSVs, and synthetic generator. |
| `utils/docs/` | Utility docs | Low activity | Keep for data-asset documentation or merge into `Documentation/`. |

## Key Runtime Modules

| Module | Role | Works now | Issues |
|---|---|---:|---|
| `app/routes/behavioral_route.py` | Deterministic aggregate predictor route | Yes | Uses rule weights, not model artifact. |
| `explainability/explainability.py` | Driver explanation and policy note | Yes | Simple rule-based explanation; no SHAP/permutation support yet. |
| `explainability/privacy.py` | Privacy notice and trend sanitization | Yes as nested module | Not exposed as `Behavioral_Signals_AI.privacy`. |
| `live_trends/x_trends.py` | Fetch live public trends or demo fallback | Partially | `from privacy import ...` is brittle. |
| `live_trends/trend_intelligence.py` | Convert trend records into proxy demand outputs | Partially | Uses local fallback predictor rather than shared demand model. |
| `app/src/data_pipeline/privacy_filter.py` | PII and k-anonymity checks | Yes | Good foundation; should become canonical privacy module. |
| `app/src/features/feature_engineering.py` | Converts aggregate records to feature table | Yes | Assumes specific raw columns and `time_period` shape. |
| `app/src/features/text_features.py` | Keyword NLP signal extraction | Yes | Rule-based; good baseline for future transformer pathway. |
| `app/src/models/signal_demand_model.py` | Deployed RandomForest classifier | Yes | Uses four core features; less rich than full feature pipeline. |
| `app/src/models/train_demand_model.py` | Multi-model demand suite | Yes in principle | Uses `src...` imports; needs path normalization. |
| `app/src/models/predict_demand.py` | DemandPredictor over trained bundle | Yes in principle | Depends on `src...` import root. |
| `app/src/intelligence/opportunity_engine.py` | Value proposition and revenue model | Yes | Deterministic and useful, but not county-calibrated. |
| `adaptive_learning/adaptive_learning.py` | Feedback logging and aggregation | Yes | Path should move away from root `data/`. |
| `training/train_model.py` | Broader model training script | Partially | Import and path roots are inconsistent. |

## Model Artifacts

| Artifact | Purpose | Risk |
|---|---|---|
| `models/model.pkl` | Primary deployed model candidate | Binary artifact in Git; verify size and provenance. |
| `models/signal_model.joblib` | Alternate trained artifact | Duplication risk. |
| `models/saved_models/demand_model_bundle.joblib` | Rich multi-model bundle | Useful but should have metadata and versioning policy. |
| `models/saved_models/signal_demand_classifier.joblib` | Deployed classifier | Active candidate. |
| `models/versions/v1/model.pkl` | Versioned model | Good concept, needs registry discipline. |

## Duplicated Or Overlapping Logic

- `app/routes/behavioral_route.py` and root `app_routes/behavioral_route.py` overlap.
- `app/src/models/signal_demand_model.py`, `training/train_model.py`, and `app/src/models/train_demand_model.py` all define training/prediction pathways.
- `app/src/features/feature_engineering.py` and `ml/_merged/feature_engineering.py` overlap.
- `app/src/models/predict_demand.py` and `ml/_merged/prediction_engine.py` overlap.
- `explainability/privacy.py` and `app/src/data_pipeline/privacy_filter.py` overlap on privacy responsibilities.
- `live_trends/trend_intelligence.py` contains a local prediction fallback that should eventually call a shared prediction service.

## Missing Or Fragile Package Initializers

The following folders do not currently contain `__init__.py` and should be reviewed before treating them as regular packages:

- `Behavioral_Signals_AI/api/`
- `Behavioral_Signals_AI/app/`
- `Behavioral_Signals_AI/behavioral_ai/`
- `Behavioral_Signals_AI/live_trends/`
- `Behavioral_Signals_AI/ml/`
- `Behavioral_Signals_AI/models/`
- `Behavioral_Signals_AI/training/`
- `Behavioral_Signals_AI/utils/`

Some nested documentation, config, artifact, and cache folders do not need `__init__.py`.

## Orphaned Or Not Connected To Runtime

- `api/_merged/` is not part of the Hugging Face public app path.
- `ml/_merged/` is useful but not clearly wired into `app.py`.
- `behavioral_ai/_merged/` is mostly a marker and migration copy.
- `app/src/cge/` appears to be historical CGE-adjacent code and should move to Signal_CGE or be documented as historical if still needed.
- Signal CGE documentation under `Behavioral_Signals_AI/Documentation/` is out of domain.

