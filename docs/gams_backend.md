# GAMS Backend

GAMS is not a solver. It is a modelling language and execution environment.
Solvers such as PATH, CONOPT, and IPOPT are mathematical engines called through
GAMS.

Signal's GAMS compatibility layer:

- Generates `.gms` files from SML.
- Emits GAMS `SETS`, `PARAMETERS`, `VARIABLES`, `EQUATIONS`, `MODEL`, `SOLVE`,
  `DISPLAY`, and `execute_unload` blocks.
- Supports solver option choices for PATH, CONOPT, IPOPT, or GAMS defaults.
- Parses `.lst` files for common errors.
- Reads GDX metadata when available.

If GAMS is not installed, Signal does not fake success. It returns:

```text
GAMS backend unavailable; using experimental Python backend or validation-only mode.
```
