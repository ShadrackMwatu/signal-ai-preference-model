# CGE Core

The CGE core handles SAM loading, balance diagnostics, account classification,
calibration, closure validation, shock tables, equation inventories, and result
summaries.

SAM balance for each account is computed as:

```text
imbalance = row_total - column_total
percentage_imbalance = imbalance / max(row_total, column_total)
```

Balance checks can be exported to `outputs/balance_check.xlsx` and
`outputs/balance_check.md`.
