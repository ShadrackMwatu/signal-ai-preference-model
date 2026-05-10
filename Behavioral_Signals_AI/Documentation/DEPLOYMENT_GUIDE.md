# Deployment Guide

Last updated: 2026-05-08

## Local Gradio Dashboard

```powershell
.\.venv\Scripts\python.exe app.py
```

The dashboard uses `app.py` as the entry point.

## Local API

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

## Compile Checks

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py
.\.venv\Scripts\python.exe -m py_compile trend_intelligence.py
```

## Test Suite

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Hugging Face Space

The README front matter configures the Space:

```yaml
sdk: gradio
sdk_version: 5.13.0
app_file: app.py
```

## Required Files For Deployment

- `app.py`
- `requirements.txt`
- `README.md`
- `models/` artifacts when available
- `config/locations.json`
- supporting Python packages in repository folders

## Secrets

Use hosted secrets for:

- `X_BEARER_TOKEN`
- `HF_TOKEN` for GitHub-to-Hugging Face sync

Never hard-code tokens in source files.

## Deployment Verification

After deployment:

1. Open the Gradio Space.
2. Confirm the Behavioral Signals AI tab loads.
3. Confirm Live Trend Intelligence is visible immediately.
4. Test prediction inputs.
5. Open SML CGE Workbench and validate the default model.
6. Open Learning tab and confirm explanation output loads.

