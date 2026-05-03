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


if __name__ == "__main__":
    unittest.main()
