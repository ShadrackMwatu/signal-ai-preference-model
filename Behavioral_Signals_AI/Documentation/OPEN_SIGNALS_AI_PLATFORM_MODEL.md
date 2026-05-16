# Open Signals AI Platform Model

Open Signals is evolving from a dashboard feature into a privacy-preserving behavioral economic intelligence platform for Kenya. It combines aggregate public or user-authorized signals, adaptive ranking, historical memory, outcome learning, geospatial context, and optional LLM reasoning to support concise policy and market intelligence.

## Intelligence Stack

AI = the overall intelligence architecture that orchestrates retrieval, safety, reasoning, ranking, memory, and response planning.

ML = the pattern learning and ranking layer. It learns from persistence, source agreement, county spread, historical recurrence, validation, and outcomes.

LLM = the conversational reasoning and explanation layer. It explains what aggregate signals mean, why they matter, and what action may be useful.

Feedback = the continuous improvement mechanism. It compares past signals with later evidence and improves confidence, source reliability, and future ranking.

## Platform Flow

User prompt
-> intent detection
-> retrieval from live signal cache and aggregate memory
-> adaptive memory, history, outcome, geospatial, category, and evaluation context
-> privacy and safety filtering
-> response planning
-> optional LLM interpretation or deterministic fallback
-> concise conversational answer

## Retrieval-Grounded Reasoning

Open Signals grounds answers in:

- `latest_live_signals.json`
- `historical_signal_memory.json`
- `outcome_learning_memory.json`
- `geospatial_signal_memory.json`
- `behavioral_intelligence_memory.json`
- `category_learning_memory.json`
- `evaluation_metrics.json`

If a file is missing or malformed, the platform falls back safely and keeps the app running.

## Response Modes

The response planner supports:

- greeting
- identity
- capability
- clarification
- quick signal answer
- analytical answer
- policy answer
- business opportunity answer
- comparison answer
- privacy refusal

## Tool-Ready Architecture

The retrieval layer exposes internal tools for future agent or LLM tool use:

- `get_top_signal(location, category, urgency)`
- `compare_counties(county_a, county_b)`
- `explain_signal(topic)`
- `summarize_opportunities(location)`
- `summarize_risks(location)`
- `get_historical_pattern(topic_or_county)`
- `get_policy_implications(topic_or_county)`

These tools operate on aggregate interpreted signals only.

## Privacy Principles

Open Signals must never store or expose personal names, emails, phone numbers, device IDs, individual searches, individual likes or comments, private messages, exact personal locations, personal routes, or individual profiles.

It uses only aggregate, anonymized, public, or user-authorized intelligence. The public interface should discuss county, category, sector, and aggregate trend patterns, not individual behavior.

## How Open Signals Differs From Generic Chatbots

Generic chatbots answer from broad language knowledge. Open Signals answers from a domain-specific intelligence stack: live aggregate signals, behavioral taxonomy, adaptive ranking, county context, historical memory, outcome learning, source validation, and privacy guardrails.

The LLM explains the platform's retrieved intelligence. It does not replace the adaptive ranking and evidence layers.

## Continuous Improvement

`run_open_signals_learning_cycle()` updates evaluation metrics from current aggregate signals and available memory. The loop is designed to expand into deeper source reliability learning, analyst validation, outcome confirmation, and model calibration.

## Future Roadmap

1. Activate one real public connector and track source reliability.
2. Expand evaluation metrics into a backend quality report.
3. Add analyst validation hooks for confirmed, rejected, and corrected signals.
4. Add richer county boundary and geospatial pattern support.
5. Expose internal retrieval tools safely to the optional LLM when tool calling is available.
