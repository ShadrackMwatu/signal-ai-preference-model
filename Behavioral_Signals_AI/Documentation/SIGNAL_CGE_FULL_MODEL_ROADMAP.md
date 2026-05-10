# Signal CGE Full Model Roadmap

Signal CGE is moving from a SAM multiplier fallback toward a full single-country CGE model. The current upgrade adds a solver-neutral blueprint for equations, variables, parameters, closures, experiments, recursive dynamics, and reporting.

## Current State

- SAM loading, classification, validation, and multiplier fallback are active.
- Prototype calibration extracts benchmark flows and share parameters.
- Equation, variable, parameter, and closure registries are now available as structured blueprints.
- Prompt-driven experiments can create structured shocks and future solver payloads.

## Next Steps

1. Complete nonlinear equation residual functions.
2. Add elasticities and tax-rate calibration.
3. Implement base-year replication checks.
4. Add an open-source nonlinear solver pathway.
5. Add recursive dynamic period updates.
6. Expand reporting into level results, percentage changes, macro accounts, welfare, trade, factors, households, and structural shifts.

## Guardrails

The current system must label fallback outputs as prototype directional indicators. Full equilibrium results should only be shown after a numerical solver, calibrated elasticities, closure checks, and replication diagnostics are active.
