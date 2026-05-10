# Learning Version v161

Change summary: Recommend explicit fallback mode when GAMS is unavailable.
Reason for change: Observed 54 occurrence(s) of gams_unavailable.
Affected templates/rules: solvers/solver_registry.py, knowledge_base/solver_diagnostics.md
Confidence score: 0.95
Risk level: low
Evidence runs: 0095385aeebc, 01eb602be033, 045af20466ca, 074cce6a89a4, 079434a02859, 08108087d193, 0b5c696c8982, 149f32ce3cd8, 1846ae37d6fc, 18f071423e72, 1e60ba1b4c54, 1ef24d5303b2, 23e7afa459a6, 2820220f0a5f, 291ce792dee4, 2b5982a90f93, 32e5f007d024, 35b24ce91eca, 37b7279401a9, 4a7a556425e6, 4cd69c3585ff, 4f22d2faba9d, 5e24a6fc2ccb, 66d7e4d748ba, 6c05ca280ec5, 6da0f10dcd2a, 6f43f286c4a5, 72a6d46a081e, 73481601bdf8, 78afe7d7e0f6, 84bbbd663333, 91248583c19d, 9f7faecebf8b, a4e719151033, ad49c4605afa, b08cb6abc1b8, b2062092ed2e, b5bef1e96c5d, bef1e82c676a, c7078af1ca83, cdc1c9a8252c, d030cdbd2c0e, d2fbe51b5306, d3101de01812, d9b3cbd01887, dad2d5390bee, dbcd71fbfa72, e30f0ca16efe, ecab4571e9a5, ed4c33e01468, f14b5b137141, f32cdeab473f, f33c46d5ebdb, ff42cea1f231

Rollback instructions:
Restore files from the rollback copy in this learning version folder.
