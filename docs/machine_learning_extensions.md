# Signal Machine Learning Extensions

## Purpose

Signal now includes a modular machine-learning extension layer for demand
classification, regression, clustering, anomaly detection, NLP signal
extraction, adaptive learning, and model registry metadata. The extension is
designed to support the existing behavioral-signals dashboard without making
heavy deep-learning libraries mandatory at runtime.

## Installed ML Libraries

- `numpy`: numerical arrays and vectorized calculations.
- `pandas`: tabular data loading, cleaning, and model-ready data frames.
- `scipy`: scientific computing support used by parts of the Python ML stack.
- `scikit-learn`: stable default engine for classification, regression,
  clustering, anomaly detection, train/test splitting, and metrics.
- `statsmodels`: statistical modelling, diagnostics, and econometric extensions.
- `xgboost`: gradient-boosted tree models for future high-performance demand
  and opportunity prediction.
- `joblib`: model serialization and loading.
- `openpyxl`: Excel workbook support for SAM and training datasets.
- `matplotlib` and `plotly`: model evaluation and dashboard visualizations.
- `spacy`: text preprocessing when available.
- `nltk`: additional NLP preprocessing and lexical tools.
- `transformers`: optional transformer-based NLP models.
- `sentence-transformers`: optional text embeddings.
- `torch`: optional PyTorch deep learning backend.
- `tensorflow`: optional TensorFlow deep learning backend. It is included with
  a Python-version marker because TensorFlow wheels are not available for every
  newest Python version on Windows.
- `datasets` and `evaluate`: dataset management and model evaluation tools.
- `pyyaml`: configuration files for experiments and model metadata.
- `pydantic`, `fastapi`, and `uvicorn`: API schemas and serving infrastructure.
- `gradio==5.13.0`: Hugging Face Space dashboard runtime.

## How ML Supports Signal

The extension supports:

- Classification of demand signals using `RandomForestClassifier` and
  `LogisticRegression`.
- Regression prediction using `RandomForestRegressor`.
- Clustering of counties, topics, households, or aggregate preference patterns
  using `KMeans`.
- Anomaly detection using `IsolationForest`.
- Sentiment, urgency, complaint, topic, and purchase-intent extraction from text.
- Text embeddings through sentence-transformers when explicitly enabled, with a
  TF-IDF fallback.
- Adaptive retraining when labelled data becomes available.
- Model version tracking through a local JSON registry.
- Prediction provenance labels, including:
  - `trained ML model`
  - `fallback rule`
  - `anomaly detection`
  - `adaptive learning update`

## Module Layout

```text
ml/
  data_preprocessing.py
  feature_engineering.py
  model_training.py
  model_evaluation.py
  prediction_engine.py
  adaptive_learning.py
  anomaly_detection.py
  nlp_signal_extractor.py
  model_registry.py
  README.md

models_ml/
  trained_models/
  experiments/
  metadata/
```

## Scikit-Learn Default Engine

Signal uses scikit-learn first because it is stable, lightweight relative to
deep-learning frameworks, and sufficient for the current prototype.

Default algorithms:

- `RandomForestClassifier` for demand classification.
- `RandomForestRegressor` for aggregate demand and opportunity score prediction.
- `LogisticRegression` for interpretable classification baselines.
- `KMeans` for clustering aggregate segments.
- `IsolationForest` for anomaly detection.
- `train_test_split` for evaluation splits.
- `accuracy_score`, `classification_report`, and `mean_squared_error` for
  evaluation.

## Optional Deep Learning Support

PyTorch, TensorFlow, transformers, and sentence-transformers are included in the
requirements for future deep-learning and NLP work. The basic Signal dashboard
does not import these libraries at startup.

The optional NLP path uses lazy imports:

- If spaCy is installed, Signal uses spaCy preprocessing.
- If sentence-transformers is explicitly enabled and available, Signal can
  generate embeddings.
- Otherwise Signal falls back to TF-IDF.

To avoid accidental model downloads in constrained environments,
sentence-transformers are only used when this environment variable is set:

```powershell
$env:SIGNAL_ENABLE_SENTENCE_TRANSFORMERS = "1"
```

## How ML Connects to CGE and SAM Analysis

Signal's behavioral ML layer can inform CGE/SAM workflows by producing:

- Demand classes that help define scenario narratives.
- Aggregate demand scores that can support demand shocks.
- Opportunity scores that can help prioritize sectors or counties.
- County/topic clusters that identify structurally similar policy units.
- Anomaly flags that highlight unusual behavior before model calibration.
- Text-derived urgency and dissatisfaction signals that support policy
  interpretation.

Example connection:

```text
high unmet demand in county/category
-> scenario shock or policy intervention
-> SAM/CGE simulation
-> policy report and learning memory
```

## Training Models

Example classifier training:

```python
import pandas as pd
from ml.model_training import train_demand_classifier

frame = pd.read_csv("data/signal_training_dataset.csv")
result = train_demand_classifier(frame, target_column="demand_class")

print(result["model_path"])
print(result["metrics"]["accuracy"])
```

Example regression training:

```python
from ml.model_training import train_regression_model

result = train_regression_model(frame, target_column="aggregate_demand_score")
print(result["metrics"])
```

## Running Predictions

```python
import pandas as pd
from ml.prediction_engine import PredictionEngine

frame = pd.DataFrame(
    [{"likes": 120, "comments": 30, "shares": 15, "searches": 200, "views": 1000}]
)

engine = PredictionEngine("models_ml/trained_models/signal_demand_classifier.joblib")
print(engine.predict(frame))
```

If the model file is unavailable, the prediction engine returns a fallback rule
prediction and labels the source as `fallback rule`.

## Adaptive Learning

Adaptive learning stores past predictions and later observed outcomes. When
enough labelled data is available, Signal can retrain and record a new model
version.

```python
from ml.adaptive_learning import AdaptiveLearningStore

store = AdaptiveLearningStore()
store.record_prediction({"prediction_id": "p001", "prediction": "High"})
store.record_outcome({"prediction_id": "p001", "observed_outcome": "High"})
```

## Model Registry

The model registry tracks:

- Model name.
- Model type.
- Training date.
- Dataset used.
- Performance.
- Version.
- File path.
- Notes.

Default path:

```text
models_ml/metadata/model_registry.json
```

## Limitations

- Current models use synthetic or user-provided labelled data; production use
  requires validated aggregate datasets.
- Deep-learning libraries are optional and may be heavy for free-tier runtime
  environments.
- The current NLP layer is intentionally conservative and falls back to TF-IDF.
- Adaptive retraining requires labelled observed outcomes.
- CGE/SAM integration remains an orchestration and policy-intelligence bridge;
  production CGE solving still depends on validated SAM data, model equations,
  closures, and solver availability.
