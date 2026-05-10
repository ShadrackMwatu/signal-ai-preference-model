from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import app


class FallbackLogicTests(unittest.TestCase):
    def test_fallback_logic_is_explicit_when_model_is_missing(self) -> None:
        with patch.object(app, "PRIMARY_MODEL_PATH", Path("tests/_tmp/missing_model.pkl")), patch.object(
            app, "LEGACY_MODEL_PATH", Path("tests/_tmp/missing_legacy.pkl")
        ):
            result = app.predict_demand_details(60, 10, 5, 180, 0.38, 0.72, 0.22)

        self.assertIn("Fallback Logic", result["model_source_label"])
        self.assertGreaterEqual(result["aggregate_demand_score"], 0)
        self.assertLessEqual(result["confidence_score"], 1)
        self.assertGreaterEqual(result["unmet_demand_probability"], 0)
        self.assertLessEqual(result["emerging_trend_probability"], 1)


if __name__ == "__main__":
    unittest.main()
