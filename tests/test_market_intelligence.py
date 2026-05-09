import unittest

from src.data_pipeline.data_loader import load_behavioral_signals


class MarketIntelligenceSmokeTests(unittest.TestCase):
    def test_sample_data_is_aggregate_only(self) -> None:
        frame = load_behavioral_signals("Behavioral_Signals_AI/data/sample_behavioral_signals.csv")

        self.assertIn("signal_id", frame.columns)
        self.assertIn("county", frame.columns)
        self.assertIn("consumer_segment", frame.columns)
        self.assertNotIn("user_id", frame.columns)
        self.assertNotIn("username", frame.columns)


if __name__ == "__main__":
    unittest.main()
