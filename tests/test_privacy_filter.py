import unittest

from src.data_pipeline.data_loader import load_behavioral_signals
from src.data_pipeline.privacy_filter import filter_private_data, validate_no_pii


class PrivacyFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = load_behavioral_signals("data/sample_behavioral_signals.csv", apply_privacy_filter=False)

    def test_blocks_pii_columns_and_patterns(self) -> None:
        with_user = self.frame.copy()
        with_user["user_id"] = "person_001"
        with_email = self.frame.copy()
        with_email.loc[0, "text"] = "contact buyer@example.com"
        with_gps = self.frame.copy()
        with_gps["latitude"] = -1.286389

        with self.assertRaises(ValueError):
            validate_no_pii(with_user)
        with self.assertRaises(ValueError):
            validate_no_pii(with_email)
        with self.assertRaises(ValueError):
            validate_no_pii(with_gps)

    def test_suppresses_small_groups(self) -> None:
        small = self.frame.copy()
        small.loc[0, "observation_count"] = 4

        safe = filter_private_data(small, min_group_size=30)

        self.assertEqual(len(safe), len(small) - 1)
        self.assertGreaterEqual(safe["observation_count"].min(), 30)


if __name__ == "__main__":
    unittest.main()
