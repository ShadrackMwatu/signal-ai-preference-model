import unittest

from api.app import app


class ApiTests(unittest.TestCase):
    def test_required_api_routes_exist(self) -> None:
        routes = {route.path for route in app.routes}

        self.assertIn("/health", routes)
        self.assertIn("/predict-demand", routes)
        self.assertIn("/county-demand", routes)
        self.assertIn("/opportunities", routes)
        self.assertIn("/segments", routes)
        self.assertIn("/market-access", routes)
        self.assertIn("/models/parse", routes)
        self.assertIn("/models/validate", routes)
        self.assertIn("/models/run", routes)
        self.assertIn("/results/{run_id}", routes)
        self.assertIn("/results/{run_id}/report", routes)
        self.assertIn("/learning/feedback", routes)
        self.assertIn("/learning/report/{run_id}", routes)
        self.assertIn("/learning/lessons", routes)
        self.assertIn("/learning/apply", routes)
        self.assertIn("/learning/rollback", routes)


if __name__ == "__main__":
    unittest.main()
