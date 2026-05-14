# Behavioral Signals AI Cleanup Recommendations

## Cleanup Principles

1. Do not delete working code until the runtime path and tests prove it is unused.
2. Keep Hugging Face startup stable.
3. Normalize imports before moving files.
4. Preserve aggregate-only privacy behavior.
5. Separate source, model artifacts, runtime outputs, documentation, and historical material.

## Highest Priority Cleanup

### 1. Normalize Behavioral Imports

Current fragile imports:

- `from privacy import ...` in `live_trends/`
- `from src...` in `app/src/` and `api/_merged/`
- `from data.synthetic...` in `training/train_model.py`

Recommended fix:

- expose `Behavioral_Signals_AI/explainability/privacy.py` through a stable package path or move privacy utilities into `app/src/data_pipeline/privacy_filter.py`;
- update modules to import from `Behavioral_Signals_AI.app.src...`;
- update training imports to `Behavioral_Signals_AI.utils.data.synthetic...`.

### 2. Decide The Canonical ML Pipeline

There are at least three model paths:

- root `app.py` model loading/fallback logic;
- `app/src/models/signal_demand_model.py`;
- `app/src/models/train_demand_model.py` and `predict_demand.py`;
- `ml/_merged/prediction_engine.py`.

Recommended fix:

- make `app/src/models/signal_demand_model.py` the lightweight deployed classifier service;
- make `app/src/models/train_demand_model.py` the richer training suite;
- turn `ml/_merged/` into archived or experimental modules after tests are adjusted.

### 3. Move Signal CGE Documentation Out Of Behavioral

`Behavioral_Signals_AI/Documentation/` contains many `SIGNAL_CGE_*` files and `signal_cge_reference/`. These belong under `Signal_CGE/Documentation/`.

Do this only after:

- updating documentation links;
- updating knowledge loaders;
- confirming GitHub and Hugging Face startup;
- keeping any shared platform docs in a clearly named shared location.

### 4. Add Missing `__init__.py` Files Where Needed

Review and add package initializers to active source folders:

- `Behavioral_Signals_AI/app/`
- `Behavioral_Signals_AI/live_trends/`
- `Behavioral_Signals_AI/training/`
- `Behavioral_Signals_AI/utils/`

Do not add initializers to pure data/model/doc folders unless a Python package import requires it.

### 5. Separate Runtime Outputs

Create explicit ignored folders:

- `Behavioral_Signals_AI/outputs/feedback/`
- `Behavioral_Signals_AI/outputs/predictions/`
- `Behavioral_Signals_AI/outputs/retraining/`
- `Behavioral_Signals_AI/outputs/trend_cache/`

Then move runtime feedback logs out of committed data folders unless intentionally used as a sample fixture.

## Medium Priority Cleanup

### API Layer

`api/_merged/` should become either:

- `Behavioral_Signals_AI/api/` active FastAPI code, or
- archived documentation/legacy material.

Before activating it, normalize imports and write a small import smoke test.

### Model Artifact Governance

Current binary artifacts should be reviewed:

- keep one deployed lightweight model artifact;
- keep one versioned model registry entry;
- move experimental binaries to ignored or Git LFS-managed storage;
- document model provenance and feature schema.

### Live Trend Service

Replace the local trend fallback predictor with a shared call to the canonical demand prediction service. Keep demo trend fallback for hosted environments without credentials.

## Lower Priority Cleanup

- Consolidate duplicated README files.
- Move historical CGE-adjacent `app/src/cge/` code out of Behavioral or label it as historical.
- Move `_merged` folders into an explicit `legacy/` or `experimental/` namespace after test coverage is updated.
- Add architectural tests that enforce Behavioral does not import Signal_CGE internals.

## Files Not Connected To Runtime Execution

Likely not directly connected to public Gradio runtime:

- `api/_merged/`
- `ml/_merged/`
- `behavioral_ai/_merged/`
- `utils/docs/`
- most `Documentation/SIGNAL_CGE_*` files
- `app/src/cge/`

These should be retained until a formal migration confirms no tests or imports depend on them.

