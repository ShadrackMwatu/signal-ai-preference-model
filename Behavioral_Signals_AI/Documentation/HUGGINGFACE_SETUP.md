# Hugging Face Setup

Last updated: 2026-05-08

## Space Metadata

The repository README contains Hugging Face Space metadata:

```yaml
title: Signal AI Dashboard
sdk: gradio
sdk_version: 5.13.0
app_file: app.py
```

## GitHub Sync

The workflow `.github/workflows/sync-to-huggingface.yml` syncs `main` to:

```text
Signal-ai/signal-ai-dashboard
```

Required GitHub secret:

```text
HF_TOKEN
```

## Runtime Dependencies

Current `requirements.txt`:

```text
gradio==5.13.0
numpy
pandas
scikit-learn
joblib
openpyxl
fastapi<0.116
pydantic<2.11
```

## Operational Notes

- The app must import cleanly from `app.py`.
- Avoid circular imports back into `app.py`.
- Keep optional integrations resilient.
- Use fallback demo trends when X credentials are not configured.
- Use fallback model logic when trained artifacts are missing.

