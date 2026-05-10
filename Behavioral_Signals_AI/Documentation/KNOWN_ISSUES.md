# Known Issues

Last updated: 2026-05-08

## Temporary Trend Fallback Predictor

`trend_intelligence.py` currently uses a lightweight local fallback predictor to avoid circular imports. A future refactor should move shared prediction logic into a neutral module.

## Visible Static Live Trend Card

The visible Live Trend Intelligence card is currently static fallback HTML to guarantee immediate visibility. It should later be connected to a safe, tested live feed without reintroducing callback or import instability.

## Untracked Generated Artifacts

The local workspace has generated model-version directories and scratch test outputs. These should be reviewed before broad staging commands.

## Hosted Runtime Cache Warnings

Matplotlib cache warnings can appear in restricted local or hosted environments. They have not blocked core app startup.

## Optional X API

X API integration requires credentials and may fail in hosted environments. Fallback trends are required for stable demos.

## SML/CGE Completeness

Some exports and solver integrations are scaffolds or compatibility layers. Production-grade economic simulation requires deeper calibration, solver configuration, and validation.

