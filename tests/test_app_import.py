from __future__ import annotations

import unittest

import pandas as pd

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
        self.assertTrue(callable(app.refresh_live_trend_intelligence))
        self.assertTrue(callable(app.build_live_trend_html))
        self.assertTrue(callable(app.update_behavioral_dashboard))

    def test_live_trend_modules_import(self) -> None:
        self.assertTrue(callable(x_trends.fetch_x_trends))
        self.assertTrue(callable(trend_intelligence.analyze_trend_signal))
        self.assertTrue(callable(parse_sml))
        self.assertTrue(callable(validate_sml))
        self.assertTrue(callable(explain_concept))

    def test_embedded_live_trend_callback_returns_hidden_data_and_public_feed(self) -> None:
        trends_df, feed_html, active_count, summary, intelligence_df = app.refresh_live_trend_intelligence("Kenya", 3)

        self.assertIsInstance(trends_df, pd.DataFrame)
        self.assertIsInstance(feed_html, str)
        self.assertIsInstance(active_count, int)
        self.assertIsInstance(summary, str)
        self.assertIsInstance(intelligence_df, pd.DataFrame)
        self.assertGreater(active_count, 0)
        self.assertIn("Live Trend Intelligence", feed_html)
        self.assertIn("signal-trend-rail", feed_html)
        self.assertNotIn("Unavailable", feed_html)
        self.assertIn("demand_classification", trends_df.columns)
        self.assertIn("confidence_score", trends_df.columns)
        self.assertIn("opportunity_score", trends_df.columns)


if __name__ == "__main__":
    unittest.main()
