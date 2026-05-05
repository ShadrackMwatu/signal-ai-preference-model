# Signal Machine Learning Extensions

This folder adds a scikit-learn-first ML layer for Signal. It supports demand
classification, regression, clustering, anomaly detection, NLP signal
extraction, adaptive retraining, prediction provenance, and model registry
metadata.

Core modules:

- `data_preprocessing.py`: dataset loading, PII column blocking, numeric cleanup.
- `feature_engineering.py`: behavioral features for demand and anomaly models.
- `model_training.py`: RandomForest, LogisticRegression, KMeans training helpers.
- `model_evaluation.py`: classification and regression metrics.
- `prediction_engine.py`: source-aware predictions with fallback behavior.
- `adaptive_learning.py`: prediction history, observed outcomes, retraining checks.
- `anomaly_detection.py`: IsolationForest anomaly detection.
- `nlp_signal_extractor.py`: spaCy/transformer-ready NLP with TF-IDF fallback.
- `model_registry.py`: local JSON metadata registry for trained models.

PyTorch, TensorFlow, transformers, and sentence-transformers are optional at
runtime. Signal uses lazy imports so the basic dashboard can continue running
with scikit-learn when heavy libraries are unavailable.
