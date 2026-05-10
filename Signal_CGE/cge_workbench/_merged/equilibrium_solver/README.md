# Signal Static CGE Solver

This package provides the production-facing open-source static equilibrium CGE
solver API for Signal CGE.

It calibrates a compact benchmark system from a balanced SAM, builds equilibrium
equations, solves the baseline and counterfactual with SciPy, validates
convergence, and exports diagnostics and results. The SAM multiplier remains
available as a separate screening backend, and GAMS remains optional for local
users with a valid installation.
