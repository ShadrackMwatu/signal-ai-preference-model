# Signal Platform Architecture

## Overview

Signal is an integrated AI platform composed of behavioral intelligence, live trend monitoring, SML-based CGE and SAM modeling support, economic simulation layers, and an educational learning layer.

It is designed as one ecosystem rather than separate tools.

## 1. Behavioral Intelligence Layer

This layer includes:

- behavioral signals
- demand scoring
- opportunity analysis

Core responsibilities:

- interpret aggregate user behavior
- classify demand conditions
- estimate opportunity and unmet-demand patterns
- provide investment and policy-facing summaries

## 2. Live Trends Intelligence Layer

This layer includes:

- X/Twitter trends
- topic-level intelligence
- public aggregate signals only

Core responsibilities:

- fetch or simulate public aggregate topic trends
- convert trend rank and volume proxies into Signal-compatible intelligence inputs
- feed those signals into the shared AI engine

Privacy rule:

- no usernames
- no user IDs
- no personal profiles
- no private messages

## 3. SML Modeling Layer

This layer includes:

- SML parser
- equation engine
- CGE translator
- scenario runner

Core repositories and packages:

- `sml_workbench/`
- `signal_modeling_language/`
- `signal_execution/`

Responsibilities:

- parse structured model text
- validate model completeness
- export GAMS-ready text
- export Pyomo-ready text
- prepare future simulation workflows

## 4. Economic Data Layer

This layer includes:

- SAMs
- IO tables
- GTAP mappings
- elasticities
- calibration data

Core repositories and packages:

- `data/`
- `cge_core/`

Responsibilities:

- store and validate economic data
- support calibration and simulation inputs
- prepare consistent economic structures for policy scenarios

## 5. Learning Layer

This layer includes:

- tutorials
- AI explanations
- model interpretation
- economics learning support

Core repositories and packages:

- `learning/`
- `signal_learning/`
- `adaptive_learning.py`

Responsibilities:

- explain platform concepts clearly
- support teaching and onboarding
- surface lessons from model runs and validation cycles

## 6. Shared AI Engine

This layer supports:

- trend intelligence
- CGE scenario interpretation
- educational explanations
- policy recommendations

It connects the behavioral layer, live trends layer, SML workbench, and learning layer into one platform.

## Integrated Workflow

```text
Behavioral Signals
      ↓
AI detects rising demand for solar products
      ↓
SML Workbench converts this into a sector shock
      ↓
CGE/SAM simulation estimates GDP, employment, sectoral output, and welfare effects
      ↓
Learning Module explains the economics and policy meaning
```

## Deployment Stability

Signal keeps the Hugging Face Gradio deployment stable by:

- using `app.py` as the root entry point
- keeping dependencies lightweight
- using fallback logic for optional services such as live X/Twitter integration
- preserving backward compatibility in the behavioral prediction layer
