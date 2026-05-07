# Signal AI/ML Engine Upgrade

## Overview

Signal now uses a trained local machine-learning model as the primary demand engine for the Hugging Face Gradio dashboard. The dashboard still accepts the existing `predict_demand()` inputs and returns the same three values, but the underlying decision logic is now model-first with transparent fallback behavior.

## Core model logic

- Primary engine: `models/model.pkl`
- Training entrypoint: `train_model.py`
- Metadata output: `models/metadata.json`
- Feedback log: `data/feedback/feedback_log.csv`

The trained artifact stores:

- a supervised demand-classification pipeline
- an unmet-demand probability classifier
- an emerging-trend probability classifier
- the exact feature list used during training

## Training data structure

The training dataset lives at:

`data/training/signal_training_data.csv`

Required fields:

- `county`
- `topic`
- `time_period`
- `engagement_intensity`
- `mentions_count`
- `comments_count`
- `shares_count`
- `likes_count`
- `searches_count`
- `sentiment_score`
- `urgency_score`
- `trend_growth`
- `repetition_score`
- `location_relevance`
- `price_sensitivity`
- `noise_score`
- `engagement_rate`
- `weighted_engagement_score`
- `trend_momentum`
- `unmet_need_signal`
- `opportunity_index`
- `demand_classification`
- `opportunity_score`
- `unmet_demand_flag`
- `emerging_trend_flag`

The data is synthetic and privacy-safe. It does not contain names, usernames, emails, phone numbers, GPS points, or user-level identifiers.

## Features used by the model

Primary model features:

- `engagement_intensity`
- `mentions_count`
- `comments_count`
- `shares_count`
- `likes_count`
- `searches_count`
- `sentiment_score`
- `urgency_score`
- `trend_growth`
- `repetition_score`
- `location_relevance`
- `price_sensitivity`
- `noise_score`
- `engagement_rate`
- `weighted_engagement_score`
- `trend_momentum`
- `unmet_need_signal`
- `opportunity_index`

## Adaptive learning design

The adaptive layer is intentionally conservative.

- `adaptive_learning.py` stores only aggregate feedback
- feedback is logged by county, topic, and time period
- blocked fields include user ids, usernames, names, emails, phone numbers, and exact location fields
- feedback can later be aggregated for retraining workflows without introducing individual tracking

## Fallback logic

If `models/model.pkl` is unavailable or fails to load, Signal falls back to a transparent scoring model based on:

- engagement intensity
- trend growth
- urgency
- repetition
- opportunity index

Fallback results are explicitly marked as fallback output.

## Guardrails

Guardrails are applied only after model prediction.

- High Demand + high opportunity score -> `Strong Investment Opportunity`
- Moderate Demand + medium/high opportunity score -> `Emerging Opportunity`
- Low Demand + high opportunity score -> `Investigate Anomaly / Possible Unmet Demand`
- Low Demand + low opportunity score -> `Weak Signal`

These guardrails do not replace the model. They only help prevent contradictory interpretation.

## Retraining

Run:

```bash
python train_model.py
```

This will:

1. create the training dataset if needed
2. validate required columns
3. train the local pipelines
4. save `models/model.pkl`
5. save `models/metadata.json`

## Local testing

Run:

```bash
python -m pytest
python train_model.py
python -c "import app; print('app import OK')"
```

## Hugging Face Spaces deployment

The root `app.py` remains the entry point for the Gradio Space. The app is designed to keep running even if the trained model artifact is missing, which helps avoid hard runtime failures during cold starts or incomplete deployments.

## Limitations

- the current training data is synthetic
- the feedback loop stores lessons but does not yet auto-retrain
- county/topic aggregation is supported, but the Gradio UI still exposes only the original compact prediction inputs
