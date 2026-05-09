import unittest

from src.data_pipeline.data_loader import load_behavioral_signals
from src.features.feature_engineering import build_feature_table
from src.models.clustering_model import SegmentClusterer


class ClusteringTests(unittest.TestCase):
    def test_kmeans_clusters_aggregate_segments(self) -> None:
        raw = load_behavioral_signals("Behavioral_Signals_AI/data/sample_behavioral_signals.csv")
        features = build_feature_table(raw)
        clusterer = SegmentClusterer(n_clusters=4).fit(features)
        clustered = clusterer.predict(features)

        self.assertIn("segment_cluster", clustered.columns)
        self.assertIn("county", clustered.columns)
        self.assertNotIn("signal_id", clustered.columns)
        self.assertGreaterEqual(clustered["segment_cluster"].nunique(), 2)


if __name__ == "__main__":
    unittest.main()
