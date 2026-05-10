# Learning Version v032

Change summary: Recommend explicit fallback mode when GAMS is unavailable.
Reason for change: Observed 11 occurrence(s) of gams_unavailable.
Affected templates/rules: solvers/solver_registry.py, knowledge_base/solver_diagnostics.md
Confidence score: 0.95
Risk level: low
Evidence runs: 01eb602be033, 149f32ce3cd8, 2820220f0a5f, 4a7a556425e6, 66d7e4d748ba, 84bbbd663333, ad49c4605afa, b2062092ed2e, d3101de01812, ed4c33e01468, f14b5b137141

Rollback instructions:
Restore files from the rollback copy in this learning version folder.
