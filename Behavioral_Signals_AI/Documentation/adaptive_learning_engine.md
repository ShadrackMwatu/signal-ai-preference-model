# Adaptive Learning Engine

Behavioral Signals AI now includes a lightweight adaptive learning loop that improves aggregate demand and opportunity predictions over time without collecting personal data.

## Learning Flow

```text
live aggregate signals
  -> provider normalization and deduplication
  -> revealed preference inference
  -> market demand prediction
  -> opportunity scoring
  -> prediction memory snapshot
  -> feedback and follow-up signal comparison
  -> accuracy tracking
  -> online calibration weights
  -> improved future predictions
```

## What Is Stored

Prediction memory stores aggregate metadata only:

- timestamp;
- signal name;
- category;
- source;
- predicted demand level;
- predicted opportunity;
- confidence;
- follow-up aggregate signal strength when available;
- persistence score;
- accuracy result.

No usernames, user IDs, raw posts, private messages, personal profiles, emails, phone numbers, or individual behavior are stored.

## Calibration Logic

The online calibrator adjusts predictions using:

- source reliability;
- signal persistence;
- cross-provider confirmation;
- historical accuracy;
- volatility/noise;
- trend growth;
- search intensity.

This is intentionally rule-based and statistical for now. It avoids heavy dependencies and remains compatible with Hugging Face Spaces.

## Demo vs Live Mode

Demo fallback exists only for reliability when live credentials are missing. Live mode combines configured providers in priority order: search trends, X aggregate trends, and public news context.