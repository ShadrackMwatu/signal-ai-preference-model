from __future__ import annotations

import unittest
from unittest.mock import patch

import x_trends


class XTrendsTests(unittest.TestCase):
    def test_missing_bearer_token_returns_demo_fallback(self) -> None:
        with patch.dict("os.environ", {}, clear=False):
            records = x_trends.fetch_x_trends(location="Kenya", limit=3)

        self.assertEqual(len(records), 3)
        self.assertTrue(all(record["source"] == "Demo fallback - X API not connected" for record in records))

    def test_trend_records_have_required_fields(self) -> None:
        records = x_trends.get_demo_trends(location="Nairobi", limit=2)
        required = {"trend_name", "rank", "tweet_volume", "location", "fetched_at", "source"}

        self.assertEqual(len(records), 2)
        for record in records:
            self.assertTrue(required.issubset(record.keys()))

    def test_unsupported_location_fails_clearly(self) -> None:
        with self.assertRaises(ValueError):
            x_trends.fetch_x_trends(location="Mars", limit=2)


if __name__ == "__main__":
    unittest.main()
