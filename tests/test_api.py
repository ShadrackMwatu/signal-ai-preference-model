import unittest
from pathlib import Path

from api.main import BatchPreferencePayload, PreferencePayload, create_app


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_dir = Path("tests/_tmp")
        temp_dir.mkdir(exist_ok=True)
        self.model_path = temp_dir / "api_model.joblib"
        self.app = create_app(self.model_path)

    def test_health_endpoint(self) -> None:
        endpoint = _route_endpoint(self.app, "/health")

        self.assertEqual(endpoint(), {"status": "ok"})

    def test_predict_endpoint(self) -> None:
        endpoint = _route_endpoint(self.app, "/predict")
        response = endpoint(
            PreferencePayload(
                user_id="user_001",
                item_id="dashboard_plus",
                category="analytics",
                price=24.0,
                rating=4.7,
                popularity=0.8,
            )
        )

        self.assertEqual(response.item_id, "dashboard_plus")
        self.assertGreaterEqual(response.score, 0)
        self.assertLessEqual(response.score, 1)
        self.assertIsInstance(response.preferred, bool)

    def test_batch_predict_endpoint(self) -> None:
        endpoint = _route_endpoint(self.app, "/predict/batch")
        response = endpoint(
            BatchPreferencePayload(
                items=[
                    PreferencePayload(
                        user_id="user_001",
                        item_id="dashboard_plus",
                        category="analytics",
                        price=24.0,
                        rating=4.7,
                        popularity=0.8,
                    ),
                    PreferencePayload(
                        user_id="user_002",
                        item_id="raw_dump",
                        category="research",
                        price=4.0,
                        rating=2.1,
                        popularity=0.1,
                    ),
                ]
            )
        )

        self.assertEqual(len(response.predictions), 2)


def _route_endpoint(app, path: str):
    for route in app.routes:
        if getattr(route, "path", None) == path:
            return route.endpoint
    raise AssertionError(f"route not found: {path}")


if __name__ == "__main__":
    unittest.main()
