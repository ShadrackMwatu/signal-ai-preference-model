# Signal Execution Environment

The execution environment reads SML files, validates syntax, loads SAM data,
checks SAM balance, calibrates shares, generates GAMS-compatible code, calls
GAMS when installed, and otherwise falls back to an experimental Python backend
or validation-only mode.

Outputs are written under `outputs/<run_id>/`, including:

- generated `.gms`
- `balance_check.xlsx`
- `balance_check.md`
- `policy_report.md`
- `execution.log`

GAMS is not a solver. It is a modelling language and execution environment.
Solvers such as PATH, CONOPT, and IPOPT are mathematical engines.
