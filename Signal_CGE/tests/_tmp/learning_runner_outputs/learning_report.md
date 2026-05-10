# Signal Learning Report

Run ID: `71b2de82c796`
Status: `ok`
Requested backend: `gams`
Actual backend: `python_nlp`

## What Signal Observed

- solver_message: GAMS backend unavailable; using experimental Python backend or validation-only mode. Experimental Python NLP backend; not production-grade.
- solver_message: GAMS backend unavailable; using experimental Python backend or validation-only mode. Experimental Python NLP backend; not production-grade.
- scenario_result: run completed

## What Failed

- gams_unavailable: Install GAMS or explicitly select experimental backend.
- experimental_solver: Do not treat experimental backend as production evidence.

## What Worked

- This model structure produced a successful prototype run.

## What Was Learned

- Flag experimental solver outputs before policy use. Evidence: 019f7a72add4, 03a2af0c6fb2, 043316eebf85, 0d7e10920317, 10f2f0f7e5cb, 15ae9306af57, 16effaff804c, 193a29d65852, 1bb1871bc9fd, 215cfbe597d2, 2658781926ef, 29a4d3ad011e, 2bd3615008d7, 2cf2200f505b, 325e42382741, 380ec7b66075, 39d69e772a4b, 3b4451c1ee3e, 43814d603048, 44f262ee756f, 450968ae6426, 479f7521985d, 48ef1e40ad13, 4accd891d914, 4fae4d18a0ac, 4fda7a69bb30, 58b2d3fe8ece, 5dafba6128f0, 64e3aaa4db7c, 66f85242c663, 6ce74696091a, 6f05287c4e6e, 6f8425872e50, 71b2de82c796, 71d642615997, 7653e84a6d17, 7f7b586644cd, 8ce5879f58d2, 93b2b191ecd9, 95d13ae54c85, 9d6c98046dcf, a45ed9327d83, a95bf7bb8f80, aa86cf42818e, b1aceb48220a, b2bb456dc660, b6b1b034b229, c18820f0d68d, cabe87706c93, d44b1dd72201, d87d04b8b38e, da7617172d40, db2641da3fc0, e1acbdec2676, e3d8a35b0509, e3ebf7641737, e67a32324aa3. Confidence: 0.95.
- Recommend explicit fallback mode when GAMS is unavailable. Evidence: 019f7a72add4, 03a2af0c6fb2, 043316eebf85, 0d7e10920317, 10f2f0f7e5cb, 15ae9306af57, 16effaff804c, 193a29d65852, 1bb1871bc9fd, 215cfbe597d2, 2658781926ef, 29a4d3ad011e, 2bd3615008d7, 2cf2200f505b, 325e42382741, 380ec7b66075, 39d69e772a4b, 3b4451c1ee3e, 43814d603048, 44f262ee756f, 450968ae6426, 479f7521985d, 48ef1e40ad13, 4accd891d914, 4fae4d18a0ac, 4fda7a69bb30, 58b2d3fe8ece, 5dafba6128f0, 64e3aaa4db7c, 66f85242c663, 6ce74696091a, 6f05287c4e6e, 6f8425872e50, 71b2de82c796, 71d642615997, 7653e84a6d17, 7f7b586644cd, 8ce5879f58d2, 93b2b191ecd9, 95d13ae54c85, 9d6c98046dcf, a45ed9327d83, a95bf7bb8f80, aa86cf42818e, b1aceb48220a, b2bb456dc660, b6b1b034b229, c18820f0d68d, cabe87706c93, d44b1dd72201, d87d04b8b38e, da7617172d40, db2641da3fc0, e1acbdec2676, e3d8a35b0509, e3ebf7641737, e67a32324aa3. Confidence: 0.95.
- Preserve successful model structure as scenario-template evidence. Evidence: 019f7a72add4, 03a2af0c6fb2, 043316eebf85, 0d7e10920317, 10f2f0f7e5cb, 15ae9306af57, 16effaff804c, 193a29d65852, 1bb1871bc9fd, 215cfbe597d2, 2658781926ef, 29a4d3ad011e, 2bd3615008d7, 2cf2200f505b, 325e42382741, 380ec7b66075, 39d69e772a4b, 3b4451c1ee3e, 43814d603048, 44f262ee756f, 450968ae6426, 479f7521985d, 48ef1e40ad13, 4accd891d914, 4fae4d18a0ac, 4fda7a69bb30, 58b2d3fe8ece, 5dafba6128f0, 64e3aaa4db7c, 66f85242c663, 6ce74696091a, 6f05287c4e6e, 6f8425872e50, 71b2de82c796, 71d642615997, 7653e84a6d17, 7f7b586644cd, 8ce5879f58d2, 93b2b191ecd9, 95d13ae54c85, 9d6c98046dcf, a45ed9327d83, a95bf7bb8f80, aa86cf42818e, b1aceb48220a, b2bb456dc660, b6b1b034b229, c18820f0d68d, cabe87706c93, d44b1dd72201, d87d04b8b38e, da7617172d40, db2641da3fc0, e1acbdec2676, e3d8a35b0509, e3ebf7641737, e67a32324aa3. Confidence: 0.95.

## Recommended Fixes

- [suggested] Recommendation saved for user review; core templates were not overwritten.
- [suggested] Recommendation saved for user review; core templates were not overwritten.
- [suggested] Recommendation saved for user review; core templates were not overwritten.

## Automatic Application

- No automatic changes were applied.

## Confidence Level

- 0.95
