# Signal CGE Repo Knowledge Integration

Signal CGE reads canonical repository materials before producing public simulation outputs.

## Knowledge Sources

- `models/canonical/signal_cge_master/model_profile.yaml`
- `Documentation/SIGNAL_CGE_KNOWLEDGE_BASE.md`
- `Documentation/signal_cge_reference/`
- `Documentation/signal_cge_reference/equations/`
- `Documentation/signal_cge_reference/calibration/`
- `Documentation/signal_cge_reference/closures/`
- `Documentation/signal_cge_reference/experiments/`
- `signal_cge/knowledge/`

## Scenario-Specific Context

`signal_cge/knowledge/scenario_context.py` maps scenarios to relevant references. For example, an import tariff shock loads trade, government, price, macro closure, experiment workflow, and knowledge base references.

## Simulation Learning Memory

`signal_cge/learning/` records lightweight metadata after each run:

- prompt
- parsed scenario
- backend used
- readiness status
- diagnostics summary
- result summary
- interpretation summary
- caveats
- recommended next simulations
- knowledge references used

Runtime memory is stored under:

```text
outputs/signal_cge_learning/simulation_memory.jsonl
```

The file is ignored by Git. Signal does not store uploaded SAM contents or large artifacts.

## Adaptation

Adaptive rules improve deterministic interpretation. They can map repeated phrases such as `reduce tariffs on cmach` to import-tariff decreases, activate gender-care reporting for care prompts, and infer commodity or activity account types from prefixes.

## Reports and Downloads

Downloadable JSON and Markdown reports include knowledge context, learning event id, result type, readiness, diagnostics, interpretation, limitations, and suggested model improvements.

## Solver Learning Pathway

Current results are prototype directional indicators. Future full CGE solver work can use accumulated diagnostics and scenario patterns to prioritize account mappings, scenario templates, calibration checks, and solver features.
