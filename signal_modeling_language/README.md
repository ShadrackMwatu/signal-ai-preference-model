# Signal Modelling Language

Signal Modelling Language (SML) is the internal modelling language for Signal
CGE models. GAMS is a modelling language and execution environment, not a solver;
SML follows that same separation by describing the model while delegating numeric
computation to GAMS or an experimental Python backend.

Supported sections:

- `SETS`
- `PARAMETERS`
- `VARIABLES`
- `EQUATIONS`
- `CLOSURE`
- `SHOCKS`
- `SOLVE`
- `OUTPUT`

Run the example:

```powershell
.\.venv\Scripts\python.exe -c "from signal_execution.runner import SignalRunner; print(SignalRunner().run('signal_modeling_language/examples/basic_cge.sml')['status'])"
```
