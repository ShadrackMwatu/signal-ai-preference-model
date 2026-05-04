# CGE Workflow

Workflow:

1. Read an `.sml` model file.
2. Validate SML syntax and model references.
3. Load SAM data from CSV or Excel.
4. Check SAM row-column balance.
5. Calibrate account totals and shares.
6. Generate GAMS-compatible code.
7. Call GAMS when installed.
8. Otherwise use experimental Python backend or validation-only mode.
9. Save outputs under `outputs/<run_id>/`.
10. Generate policy intelligence and a Markdown report.

Balance exports:

- `balance_check.xlsx`
- `balance_check.md`

Execution logs:

- `execution.log`
