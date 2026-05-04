# Signal Development Log

## Initialization
- Project structure created
- Hugging Face integration in progress

## Codex Instructions
- Create Signal project folders for SAM data, raw data, processed data, documents, GAMS models, SML models, and outputs.
- Initialize a development log for coding instructions, code changes, files created/updated, and key decisions.
- Ensure deployment requirements include Gradio, NumPy, pandas, scikit-learn, and joblib.
- Create GitHub Actions sync workflow from GitHub main branch to the Hugging Face Space.
- Add a safe guard so missing model artifacts do not break `app.py`.

## Code Changes Made
- Added tracked placeholder files for required project folders.
- Added Hugging Face sync workflow using `actions/checkout@v4`.
- Updated `app.py` model loading to fail safely when the trained model is unavailable.

## Files Created/Updated
- `.github/workflows/sync-to-huggingface.yml`
- `app.py`
- `data/sams/.gitkeep`
- `data/raw/.gitkeep`
- `data/processed/.gitkeep`
- `documents/cge_frameworks/.gitkeep`
- `documents/policy_notes/.gitkeep`
- `documents/coding_logs/development_log.md`
- `models/gams/.gitkeep`
- `models/sml/.gitkeep`
- `outputs/.gitkeep`

## Key Decisions
- Existing files and current app functionality are preserved.
- `requirements.txt` already contains the requested dependencies, so existing pinned runtime requirements were kept.
- Missing or invalid model loading now returns `Model not loaded` with zero scores instead of crashing.
