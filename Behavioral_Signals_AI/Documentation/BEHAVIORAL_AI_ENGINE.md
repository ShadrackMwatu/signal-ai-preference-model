# Behavioral AI Engine

Last updated: 2026-05-08

## Purpose

The Behavioral AI Engine estimates demand and opportunity from aggregate behavioral signals.

## Inputs

- Likes
- Comments
- Shares
- Searches
- Engagement intensity
- Purchase intent score
- Trend growth

## Demand Classification Logic

`app.py` builds normalized features, attempts a trained model prediction, then applies guardrails and explanations. If a model is unavailable, fallback logic estimates classification from aggregate demand, engagement quality, search strength, trend growth, and risk signals.

## Opportunity Scoring

Opportunity score reflects a combination of:

- demand intensity
- purchase intent
- trend growth
- engagement quality
- unmet demand probability
- confidence

## Confidence Scoring

Confidence is derived from model probability when available. Fallback confidence is based on signal strength, noise, and feature consistency.

## Anomaly Detection

Anomaly support exists in `ml/anomaly_detection.py`. The dashboard also computes volatility/noise and risk signals in `app.py`.

## Unmet Demand Detection

Unmet demand is inferred when search and attention are strong but conversion or engagement quality may indicate access, affordability, or delivery gaps.

## Rule-Based Guardrails

Guardrails prevent overconfident outputs when:

- signal strength is weak
- noise is high
- confidence is low
- demand is ambiguous
- trend growth does not support the classification

## Explainability

`explainability.py` and helper functions in `app.py` generate:

- key drivers
- driver summary
- policy note
- risk signals
- why-this-matters text

## Adaptive Learning

The engine is connected to feedback and adaptation modules so future versions can learn from user corrections, model errors, failed runs, and recurring issues.

