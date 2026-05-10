# Signal CGE Safe Adaptation Policy

Signal CGE may learn from repository documents, prompts, parsed scenarios, diagnostics, prototype results, policy interpretations, and repeated user behavior. The purpose is to improve deterministic interpretation, diagnostics, recommendations, and model-development planning.

## Allowed Adaptation

- Improve prompt interpretation using deterministic mapping rules.
- Retrieve more relevant repo references for each scenario type.
- Summarize repeated warnings, targets, and scenario requests.
- Recommend account mappings, scenario templates, documentation additions, calibration checks, and solver upgrades.
- Generate model-gap reports for developer review.

## Not Allowed Without Developer Approval

Signal CGE must not automatically rewrite:

- model equations,
- closure rules,
- calibration formulas,
- solver core logic,
- GAMS/Pyomo/open-source solver implementations,
- canonical model profiles that change economic assumptions.

## Runtime Memory

Learning memory is metadata-only and stored under `Signal_CGE/outputs/`. It must not store uploaded SAMs, private user data, large solver outputs, GDX files, logs, checkpoints, or temporary runtime artifacts.

## Review Path

Approved improvements should be made through normal Git workflow: inspect the recommendation, edit the relevant source or documentation, run tests, commit, and push after review.
