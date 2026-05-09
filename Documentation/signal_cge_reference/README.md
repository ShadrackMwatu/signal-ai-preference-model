# Signal CGE Reference Library

This folder is the permanent reference library for the canonical Signal CGE architecture.

## Sections

- `user_guides/`: adapted user guide files.
- `architecture/`: model architecture and package layout.
- `equations/`: model-block equation references.
- `workflows/`: AI, SML, and execution workflows.
- `calibration/`: SAM calibration and benchmark preparation.
- `closures/`: macro and market-closure documentation.
- `experiments/`: policy experiment workflow.
- `historical/`: source-package notes and historical reference material.

Signal AI modules should use `signal_cge/knowledge/` to discover and load these references.

Public app routing for this domain lives in:

```text
app_routes/signal_cge_route.py
```
