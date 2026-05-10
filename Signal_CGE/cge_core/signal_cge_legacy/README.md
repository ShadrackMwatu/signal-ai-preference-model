# Signal CGE

`signal_cge/` is the canonical CGE/SAM model engine for Signal.

It owns:

- data loading and validation
- calibration prototypes
- model-core blocks
- solver interfaces and fallback execution
- scenarios
- recursive-dynamics stubs
- diagnostics
- reporting
- knowledge/reference indexing
- local workspace configuration

The public Hugging Face tab routes through:

```text
app_routes/signal_cge_route.py
```

Signal CGE uses repo-stored canonical files by default and does not require local Windows model artifacts for Hugging Face execution.
