import unittest

from cge_core.calibration import calibrate_from_sam
from cge_core.sam import load_sam


class CalibrationTests(unittest.TestCase):
    def test_calibration_generates_account_shares(self) -> None:
        calibration = calibrate_from_sam(load_sam("data/sample_sam.csv"))

        self.assertGreater(calibration["total_activity"], 0)
        self.assertIn("output_shares", calibration)
        self.assertIn("agriculture", calibration["output_shares"])
        self.assertIn("sectors", calibration["account_classification"])


if __name__ == "__main__":
    unittest.main()
