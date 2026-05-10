from __future__ import annotations

import unittest

import pandas as pd

from ml.anomaly_detection import SignalAnomalyDetector


class AnomalyDetectionTests(unittest.TestCase):
    def test_isolation_forest_marks_anomaly_fields(self) -> None:
        frame = pd.DataFrame(
            {
                "likes": [10, 12, 11, 13, 900],
                "comments": [2, 3, 2, 4, 300],
                "shares": [1, 1, 2, 1, 120],
                "searches": [8, 9, 7, 10, 850],
                "views": [200, 220, 210, 230, 5000],
            }
        )
        output = SignalAnomalyDetector(contamination=0.2).fit(frame).detect(frame)

        self.assertIn("is_anomaly", output.columns)
        self.assertIn("anomaly_score", output.columns)
        self.assertEqual(output["prediction_source"].iloc[0], "anomaly detection")
        self.assertEqual(len(output), len(frame))


if __name__ == "__main__":
    unittest.main()
