# Real-Time Intelligence Runtime

Open Signals is moving from a request-response dashboard toward a continuously learning intelligence system. The runtime layer refreshes aggregate/public sources, updates live signal cache state, detects signal movement, and prepares backend intelligence for chat and feed rendering without redesigning the UI.

## Runtime Architecture

The runtime flow is:

aggregate/public source ingestion -> live signal cache -> trajectory classification -> alert and event detection -> adaptive refresh interval -> historical/outcome/geospatial memory update -> evaluation metrics -> render cache refresh -> chat/feed grounding

The main entry point is `run_open_signals_runtime_cycle()` in `Behavioral_Signals_AI/runtime/signal_runtime_manager.py`.

## Adaptive Refresh Logic

Open Signals no longer assumes every signal needs the same refresh speed. High-volatility topics such as fuel prices, sudden price pressure, shortages, or labor unrest receive faster refresh hints. Stable or seasonal signals such as drought and agriculture-cycle signals can refresh more slowly.

The runtime does not call external APIs every second. It updates backend intelligence periodically and leaves the green UI heartbeat dot as a visual indicator only.

## Signal Trajectory Engine

`Behavioral_Signals_AI/signal_engine/signal_trajectory.py` classifies signals as:

- emerging
- strengthening
- persistent
- accelerating
- stabilizing
- weakening
- fading

Classification uses momentum, ranking movement, confidence movement, persistence, source agreement, recurrence, outcome validation, and forecast direction when available.

## Alert and Threshold Detection

The runtime stores internal alerts for:

- rapid signal spikes
- unusual county spread
- sudden affordability stress
- emerging market opportunities
- high-confidence persistent signals

These alerts are backend-only for now and are written to runtime output files. Public alert UI can be added later if needed.

## Event Detection

Runtime event clustering groups signals into interpretable clusters such as:

- fuel price pressure event
- drought or water stress cluster
- transport disruption cluster
- healthcare stress cluster
- food affordability pressure event

The event layer uses topic keywords, category recurrence, geographic scope, source agreement, and trajectory labels.

## Continuous Learning Loop

Each runtime cycle can:

1. Ingest enabled aggregate/public sources.
2. Update the live signal cache.
3. Detect emerging and weakening signals.
4. Update historical, outcome, and geospatial memories.
5. Update evaluation metrics.
6. Refresh render cache without full-feed flicker.
7. Keep the app running if a source fails.

## Evaluation Metrics

The runtime writes or updates metrics including:

- trajectory accuracy placeholder
- emerging signal confirmation rate placeholder
- false spike rate placeholder
- county spread prediction accuracy placeholder
- runtime source uptime
- source freshness
- runtime alert count
- runtime event count
- adaptive refresh interval
- emerging and weakening signal counts

## Privacy Principles

Open Signals remains aggregate-only. It must never track individuals, expose personal behavior, store personal identifiers, infer private identities, or reconstruct routes. Runtime intelligence uses public, aggregate, anonymized, or user-authorized records only.

## Future Multimodal Roadmap

The runtime includes inactive placeholders for:

- image trend understanding
- map overlays
- chart generation
- document ingestion
- speech/audio trend ingestion

These are architecture stubs only. Heavy models are not activated in this phase.
