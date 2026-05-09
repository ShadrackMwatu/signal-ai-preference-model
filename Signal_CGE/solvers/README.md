# Solver Abstraction Layer

Signal separates modelling language and execution environment concerns from
mathematical solver engines.

Backends:

- `gams`: production-oriented execution through a local GAMS installation.
- `python_nlp`: experimental SciPy nonlinear solver path.
- `fixed_point`: experimental fallback for validation and demos.

The Python solvers are explicitly experimental and are not production-grade
replacements for GAMS plus established solvers such as PATH, CONOPT, or IPOPT.
