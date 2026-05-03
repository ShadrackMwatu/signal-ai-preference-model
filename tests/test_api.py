import unittest
from pathlib import Path

from api.main import BatchPreferencePayload, CgeSamExportPayload, PreferencePayload, create_app


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
        self.assertTrue(response.drivers)
        self.assertEqual(response.cge_sam_account, "DIGITAL_SERVICES")
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

    def test_cge_sam_export_endpoint(self) -> None:
        endpoint = _route_endpoint(self.app, "/export/cge-sam")
        response = endpoint(
            CgeSamExportPayload(
                scenario_id="policy_scenario_1",
                items=[
                    PreferencePayload(
                        user_id="user_001",
                        item_id="dashboard_plus",
                        category="analytics",
                        price=24.0,
                        rating=4.7,
                        popularity=0.8,
                    )
                ],
            )
        )

        self.assertEqual(response.rows[0].scenario_id, "policy_scenario_1")
        self.assertEqual(response.rows[0].sam_account, "DIGITAL_SERVICES")

    def test_cge_sam_export_endpoint_accepts_dict_payload(self) -> None:
        payload = CgeSamExportPayload.model_validate(
            {
                "scenario_id": "policy_scenario_1",
                "items": [
                    {
                        "user_id": "user_001",
                        "item_id": "dashboard_plus",
                        "category": "analytics",
                        "price": 24.0,
                        "rating": 4.7,
                        "popularity": 0.8,
                    }
                ]
            }
        )
        endpoint = _route_endpoint(self.app, "/export/cge-sam")
        response = endpoint(payload)

        self.assertEqual(response.rows[0].scenario_id, "policy_scenario_1")
        self.assertEqual(response.rows[0].sam_account, "DIGITAL_SERVICES")

    def test_market_intelligence_dashboard_endpoint(self) -> None:
        endpoint = _route_endpoint(self.app, "/market-intelligence/dashboard")
        response = endpoint()

        self.assertIn("dashboard", response)
        self.assertIn("national_aggregate_demand_index", response["dashboard"])
        self.assertIn("market_opportunities", response["dashboard"])

    def test_market_intelligence_evaluation_endpoint(self) -> None:
        endpoint = _route_endpoint(self.app, "/market-intelligence/evaluation")
        response = endpoint()

        self.assertIn("classification", response)
        self.assertIn("accuracy", response["classification"])

    def test_market_intelligence_retrain_endpoint_reports_version_logs(self) -> None:
        endpoint = _route_endpoint(self.app, "/market-intelligence/retrain")
        response = endpoint()

        self.assertEqual(response["status"], "retrained")
        self.assertGreaterEqual(response["model_version"], 2)
        self.assertTrue(response["retraining_logs"])

    def test_dashboard_html_endpoint(self) -> None:
        endpoint = _route_endpoint(self.app, "/dashboard")
        response = endpoint()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Signal Market Intelligence Dashboard", response.body.decode("utf-8"))


def _route_endpoint(app, path: str):
    for route in app.routes:
        if getattr(route, "path", None) == path:
            return route.endpoint
    raise AssertionError(f"route not found: {path}")


if __name__ == "__main__":
    unittest.main()
