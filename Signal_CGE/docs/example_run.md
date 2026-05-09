# Example Run

Run the default SML example:

```powershell
.\.venv\Scripts\python.exe -c "from signal_execution.runner import SignalRunner; result = SignalRunner().run('signal_modeling_language/examples/basic_cge.sml'); print(result['run_id']); print(result['summary'])"
```

Run tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Launch the dashboard:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the Gradio URL shown in the terminal. Use the `SML CGE Workbench` tab to
upload a SAM, edit SML, validate, run, inspect balance diagnostics, and download
the report.
