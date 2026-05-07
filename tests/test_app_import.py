from __future__ import annotations

import unittest

import app


class AppImportTests(unittest.TestCase):
    def test_app_imports_and_builds_demo(self) -> None:
        self.assertTrue(hasattr(app, "demo"))
        self.assertTrue(callable(app.predict_demand))
        self.assertTrue(callable(app.predict_demand_details))


if __name__ == "__main__":
    unittest.main()
