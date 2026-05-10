# Closure System

Signal closure rules define which variables adjust when the model is shocked. The closure system must be explicit, validated, and reported.

## Supported Closure Families

- Savings-driven investment
- Government deficit closure
- Foreign savings or exchange-rate closure
- Numeraire choice
- Factor-market closure

## Validation Requirements

Each closure should identify fixed variables, flexible variables, macro balance assumptions, and compatibility with the selected solver pathway. Unsupported closures should block full CGE solving and produce a warning for fallback simulations.
