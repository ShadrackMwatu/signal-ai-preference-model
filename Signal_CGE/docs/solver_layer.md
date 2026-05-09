# Solver Layer

Signal uses a solver abstraction:

```python
class BaseSolver:
    def solve(model_spec, data, options):
        ...
```

Available backends:

- `gams`: production-oriented GAMS execution when installed.
- `python_nlp`: experimental SciPy nonlinear solver backend.
- `fixed_point`: experimental fixed-point iteration fallback.

The Signal Python solver path is not production-grade. Established solvers
through GAMS remain the trusted production option for serious CGE work.
