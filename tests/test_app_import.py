from __future__ import annotations

import unittest

import app
import trend_intelligence
import x_trends


class AppImportTests(unittest.TestCase):
    def test_app_imports_and_builds_demo(self) -> None:
        self.assertTrue(hasattr(app, "demo"))
        self.assertTrue(callable(app.predict_demand))
        self.assertTrue(callable(app.predict_demand_details))
        self.assertTrue(callable(app.refresh_live_trends))

    def test_live_trend_modules_import(self) -> None:
        self.assertTrue(callable(x_trends.fetch_x_trends))
        self.assertTrue(callable(trend_intelligence.analyze_trend_signal))


if __name__ == "__main__":
    unittest.main()
