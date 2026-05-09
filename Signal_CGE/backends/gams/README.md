# GAMS Compatibility Layer

This layer converts Signal Modelling Language models into GAMS-compatible
`.gms` files. GAMS is a modelling language and execution environment. It is not
itself the mathematical solver. Numeric computation is delegated to engines such
as PATH, CONOPT, IPOPT, or the default solver configured in GAMS.

The layer includes:

- SETS, PARAMETERS, VARIABLES, EQUATIONS, MODEL, SOLVE, DISPLAY, and
  `execute_unload` generation.
- Solver option support for PATH, CONOPT, IPOPT, and default choices.
- `.lst` error parsing for common GAMS errors.
- Best-effort GDX metadata reading.

If GAMS is not installed, Signal returns:

```text
GAMS backend unavailable; using experimental Python backend or validation-only mode.
```
