# Signal AI/ML Engine Phase 2

## Purpose of this upgrade

Phase 2 strengthens Signal’s Hugging Face dashboard so the user receives a fuller intelligence brief instead of a narrow score output. The goal is to keep the existing deployment stable while improving:

- prediction richness
- explainability
- synthetic training data quality
- model versioning
- transparent fallback behavior
- policy and investment interpretation

## Model architecture

Signal uses a scikit-learn-first architecture:

- synthetic training data generator
- feature preparation and derived features
- `RandomForestClassifier` pipeline for demand classification
- auxiliary classifiers for:
  - unmet demand probability
  - emerging trend probability
- Gradio dashboard for inference and presentation

## Training data design

The synthetic dataset is generated at:

`data/training/signal_training_data.csv`

Core columns:

- `topic`
- `county`
- `time_period`
- `likes`
- `comments`
- `shares`
- `searches`
- `engagement_intensity`
- `purchase_intent_score`
- `trend_growth`
- `sentiment_score`
- `urgency_score`
- `repetition_score`
- `location_relevance`
- `price_sensitivity`
- `noise_score`
- `demand_class`
- `opportunity_label`
- `unmet_demand_flag`
- `emerging_trend_flag`

Signal simulates these market states:

- High Demand
- Moderate Demand
- Low Demand
- Emerging Demand
- Declining Demand
- Unmet Demand

## Synthetic data generation

Run:

```bash
python data/synthetic/generate_synthetic_signal_data.py
```

This creates a realistic aggregate dataset for model retraining and testing.

## Prediction flow

The dashboard prediction path is:

1. collect aggregate behavioral inputs
2. build derived features
3. load the trained model if available
4. predict demand class and confidence
5. estimate aggregate demand, opportunity, unmet demand, and emerging trend
6. apply consistency guardrails
7. generate explainability output
8. render a policy-friendly and investor-friendly intelligence brief

## Fallback logic

If `models/model.pkl` is missing or unreadable, Signal still runs using transparent fallback logic.

Fallback computes:

- demand class
- confidence estimate
- aggregate demand score
- opportunity score
- unmet demand probability
- emerging trend probability

The dashboard clearly labels this path as:

`Fallback Logic — trained model not available.`

## Guardrails

Guardrails adjust interpretation after model prediction. They do not replace the model.

Examples:

- High Demand + high opportunity score -> Strong Investment Opportunity
- Moderate Demand + medium/high opportunity score -> Emerging Opportunity
- Low Demand + high opportunity score -> Investigate Anomaly / Possible Unmet Demand
- Low Demand + low opportunity score -> Weak Signal
- High Demand + low confidence -> Monitor Further
- High searches + low engagement -> Possible Unmet Demand
- High engagement + high noise -> Validate Signal Quality

## Explainability

`explainability.py` produces simple transparent narratives using aggregate signals only.

It highlights drivers such as:

- high likes
- high comments
- high shares
- high searches
- strong engagement intensity
- strong purchase intent
- fast trend growth
- weak trend growth
- possible noise
- possible unmet demand

## Privacy safeguards

Signal remains privacy-preserving:

- no individual tracking
- no usernames
- no emails
- no phone numbers
- no exact GPS data
- no user-level behavioral storage
- feedback is stored only at aggregate topic/county/time level

## Retraining

Run:

```bash
python train_model.py
```

Each run:

- loads `data/training/signal_training_data.csv`
- validates required columns
- prepares derived features
- trains the pipeline
- writes latest artifacts:
  - `models/model.pkl`
  - `models/metadata.json`
- writes a versioned copy:
  - `models/versions/vN/model.pkl`
  - `models/versions/vN/metadata.json`

## Running tests

Run:

```bash
python -m pytest
```

## Hugging Face deployment notes

- root `app.py` remains the entry point
- the existing tabs are preserved
- the dashboard still works if the trained model is unavailable
- dependencies remain intentionally lean for Space stability
