# Signal Modelling Language

Signal Modelling Language (SML) is a compact internal modelling language for
CGE workflows.

Supported blocks:

```text
SETS:
PARAMETERS:
VARIABLES:
EQUATIONS:
CLOSURE:
SHOCKS:
SOLVE:
OUTPUT:
```

Example:

```text
SOLVE:
  model = kenya_cge
  backend = gams
  solver = path
```

SML is not a numeric solver. It describes model structure, data, closure rules,
shocks, solve preferences, and outputs. The execution layer translates SML into
GAMS-compatible code or experimental Python solver inputs.
