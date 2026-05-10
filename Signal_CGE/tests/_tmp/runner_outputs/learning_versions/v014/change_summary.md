# Learning Version v014

Change summary: Recommend explicit fallback mode when GAMS is unavailable.
Reason for change: Observed 5 occurrence(s) of gams_unavailable.
Affected templates/rules: solvers/solver_registry.py, knowledge_base/solver_diagnostics.md
Confidence score: 0.95
Risk level: low
Evidence runs: 01eb602be033, 4a7a556425e6, ad49c4605afa, b2062092ed2e, ed4c33e01468

Rollback instructions:
Restore files from the rollback copy in this learning version folder.
