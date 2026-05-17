# Open Signals Tool Calling Architecture

## Purpose

Tool calling lets Open Signals decide when it needs internal aggregate evidence before answering. The chat does not execute arbitrary code or external user-provided tools. It can only call a closed registry of privacy-safe internal tools that retrieve interpreted Open Signals data.

## Registered Tools

- `get_live_signals`: reads current interpreted aggregate signals.
- `get_top_signal`: returns the strongest signal for active filters.
- `get_county_signals`: retrieves county-relevant aggregate signals.
- `compare_counties`: compares the strongest signals across two counties.
- `get_category_signals`: retrieves signals for a category such as transport, health, jobs, or cost of living.
- `get_historical_pattern`: retrieves aggregate historical memory.
- `get_outcome_learning`: retrieves aggregate outcome-learning evidence.
- `get_geospatial_context`: summarizes county/geospatial signal context.
- `get_forecast_context`: summarizes forecast direction and spread risk.
- `get_source_freshness`: reports cache/source freshness.
- `get_evaluation_metrics`: reads aggregate evaluation metrics.
- `summarize_opportunities`: summarizes opportunity signals.
- `summarize_risks`: summarizes risk, stress, and pressure signals.
- `privacy_check`: blocks private or individual-level requests.

## Deterministic Routing

The deterministic router maps prompts to tool calls before synthesis.

Examples:

- “What is happening in Nairobi transport demand?” calls `privacy_check`, `get_county_signals`, `get_geospatial_context`, `get_category_signals`, and `get_forecast_context`.
- “Compare Makueni and Nakuru” calls `privacy_check` and `compare_counties`.
- “What is the strongest signal now?” calls `privacy_check` and `get_top_signal`.
- “Are you sure?” calls `privacy_check`, `get_live_signals`, `get_source_freshness`, and `get_evaluation_metrics`.
- “What opportunities exist in Kisumu?” calls opportunity and county tools.

## LLM-Assisted Routing Readiness

When LLM mode is enabled, Open Signals can pass tool descriptions and executed tool results into the LLM context. The LLM may reason over available tools, but only registered tools can be executed by the Python runtime. Arbitrary code execution is not allowed.

## Privacy Rules

All tools must return aggregate, anonymized, public, or user-authorized data only.

Open Signals must never expose or store:

- names
- phone numbers
- emails
- device IDs
- private messages
- raw private searches
- exact personal locations
- personal routes
- individual profiles

The `privacy_check` tool runs before other tool results are used. Tool outputs are also checked for private fields before being returned.

## Failure Behavior

Tool failures return structured fallback objects. Stack traces are not exposed to the chat response. If a tool fails, Open Signals continues with existing aggregate context and cautious language.

## Future Signal CGE Bridge

Signal CGE is intentionally not touched in this pass. A future bridge could register a separate read-only tool that summarizes aggregate CGE scenario outputs for policy interpretation, with explicit boundaries and tests.
