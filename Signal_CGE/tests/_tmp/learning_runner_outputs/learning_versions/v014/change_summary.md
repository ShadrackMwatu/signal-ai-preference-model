# Learning Version v014

Change summary: Recommend explicit fallback mode when GAMS is unavailable.
Reason for change: Observed 5 occurrence(s) of gams_unavailable.
Affected templates/rules: solvers/solver_registry.py, knowledge_base/solver_diagnostics.md
Confidence score: 0.95
Risk level: low
Evidence runs: 44f262ee756f, 4fae4d18a0ac, 6f05287c4e6e, a95bf7bb8f80, c18820f0d68d

Rollback instructions:
Restore files from the rollback copy in this learning version folder.
