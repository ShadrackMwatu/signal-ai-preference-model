# Solver Diagnostics

GAMS is a modelling language and execution environment. PATH, CONOPT, IPOPT,
and other engines are solvers.

Initial diagnostic rules:

- PATH convergence failure: check MCP formulation, scaling, bounds, and initial values.
- CONOPT/IPOPT failure: check differentiability, scaling, and infeasible constraints.
- Experimental Python backend: validation and prototyping only; not policy-grade.
- Missing GAMS: return an honest unavailable message and use fallback only if requested or allowed.
