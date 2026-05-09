# Signal CGE Workbench

Signal CGE Workbench is an AI-assisted interface for running transparent CGE/SAM policy simulations from natural language prompts. It helps users prepare scenarios, validate SAM data, choose execution backends, run diagnostics, interpret outputs, and generate policy briefs without directly operating GAMS, spreadsheets, or model code.

AI assists the workflow; it does not replace the economic model. All assumptions, closure choices, diagnostics, warnings, and generated artifacts remain visible and reproducible.

## Workflow

1. Convert a chat prompt into a structured scenario.
2. Run diagnostics before execution: SAM balance, account classification, closure, baseline consistency, and shock validity.
3. Execute with the selected backend:
   - `SAM multiplier`: open-source Python fallback.
   - `CGE model`: optional GAMS-backed execution when GAMS is installed.
   - `Recursive dynamic model`: placeholder for future implementation.
4. Run post-simulation validation.
5. Generate plain-language interpretation and a Markdown policy brief.
6. Store run artifacts in `cge_workbench/outputs/` with timestamped logs.

## Python SAM Multiplier

The fallback engine loads a square SAM from CSV or Excel, computes column coefficients `A`, builds `I - A`, computes the Leontief inverse, applies the shock vector `x`, and reports `y = (I - A)^-1 x`.

## GAMS Execution

`runners/gams_runner.py` checks for `gams.exe` or `gams` on the system path. If unavailable, the runner returns a clear message and the workbench can continue with the Python SAM multiplier.

## Example Prompts

- Increase public investment in care infrastructure by 20%
- Simulate a 10% VAT reduction on manufacturing
- Increase transport productivity by 5%
- Double paid care services
- Convert 25% of unpaid care work into paid care work
- Run a trade facilitation shock for exports
