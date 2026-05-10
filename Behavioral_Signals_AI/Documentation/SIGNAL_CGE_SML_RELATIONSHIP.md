# Signal CGE And SML Relationship

Signal separates the economic model engine, readable model specification, AI chat interface, learning layer, and solver layer.

## Signal CGE

Signal CGE is the economic model engine. It owns:

- SAM validation and calibration
- formal model blocks and equations
- closure rules
- scenario data structures
- diagnostics
- solver interfaces
- reporting outputs

The canonical package is `signal_cge/`.

## SML CGE Workbench

SML is the readable specification language. It helps users describe model structures, validate model text, and prepare exports. It is not the economic solver by itself.

Current implementation remains in `sml_workbench/`. A new `signal_sml/` namespace has been created for gradual migration.

## AI CGE Chat Studio

The AI Chat Studio turns natural-language policy questions into structured scenarios. It calls Signal CGE for simulation and diagnostics. It does not replace equations, calibration, or solvers.

## Learning

The learning layer explains concepts and workflows: SAMs, CGE blocks, calibration, closures, diagnostics, SML syntax, and policy interpretation.

## Solvers

Solvers execute the calibrated model or fallback multiplier:

- Python SAM multiplier fallback is currently ready.
- Optional GAMS runner is detected when available.
- Open-source equilibrium solver is a future placeholder.
- Recursive dynamic solver is a future placeholder.

## Practical Rule

Use SML to specify, Signal CGE to calibrate and solve, AI Chat Studio to configure scenarios conversationally, and Learning to explain what is happening.
