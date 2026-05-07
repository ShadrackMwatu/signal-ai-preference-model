from __future__ import annotations

import unittest

import app
import trend_intelligence
import x_trends
from learning.ai_teaching.explainer import explain_concept
from sml_workbench.parser.sml_parser import parse_sml
from sml_workbench.validators.sml_validator import validate_sml


class AppImportTests(unittest.TestCase):
    def test_app_imports_and_builds_demo(self) -> None:
        self.assertTrue(hasattr(app, "demo"))
        self.assertTrue(callable(app.predict_demand))
        self.assertTrue(callable(app.predict_demand_details))
        self.assertTrue(callable(app.refresh_live_trends))
        self.assertTrue(callable(app.update_behavioral_dashboard))

    def test_live_trend_modules_import(self) -> None:
        self.assertTrue(callable(x_trends.fetch_x_trends))
        self.assertTrue(callable(trend_intelligence.analyze_trend_signal))
        self.assertTrue(callable(parse_sml))
        self.assertTrue(callable(validate_sml))
        self.assertTrue(callable(explain_concept))


if __name__ == "__main__":
    unittest.main()
