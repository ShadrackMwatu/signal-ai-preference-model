from __future__ import annotations

import unittest

from ml.nlp_signal_extractor import build_text_embeddings, extract_text_signals, optional_deep_learning_status


class NLPSignalExtractorTests(unittest.TestCase):
    def test_text_signal_extraction_and_embedding_fallback(self) -> None:
        texts = [
            "Urgent solar battery repair now, ready to buy from trusted supplier",
            "Complaints about delivery delay and expensive farm inputs",
        ]
        features = extract_text_signals(texts)
        embeddings = build_text_embeddings(texts)
        status = optional_deep_learning_status()

        self.assertIn("sentiment_score", features.columns)
        self.assertIn("purchase_intent_score", features.columns)
        self.assertGreater(features.loc[0, "purchase_intent_score"], 0)
        self.assertIn("embeddings", embeddings)
        self.assertIn("embedding_source", embeddings)
        self.assertIn("torch_available", status)


if __name__ == "__main__":
    unittest.main()
