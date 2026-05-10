---
title: Signal AI Dashboard
emoji: 📊
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.13.0
app_file: app.py
pinned: false
---

# Signal AI Preference Model

Signal is organized into two major product folders:

1. **Signal_CGE** — SAM/CGE/SML economic modeling, solver backends, policy simulation, GAMS integration, diagnostics, reporting, and economic learning services.
2. **Behavioral_Signals_AI** — privacy-preserving behavioral intelligence, aggregate demand prediction, opportunity scoring, live trend intelligence, adaptive learning, API/app support, and explainability.

## Repository Structure

```text
Signal_CGE/
Behavioral_Signals_AI/
app.py
requirements.txt
README.md
pytest.ini
.github/
.gitattributes
.gitignore
```

The root keeps only deployment and repository-control files required by Hugging Face, GitHub Actions, Git LFS, and local testing. Product code should live inside either `Signal_CGE/` or `Behavioral_Signals_AI/`.

<!-- cleanup-trigger: remove any remaining non-domain root items -->
