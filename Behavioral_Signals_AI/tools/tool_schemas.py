"""Tool schemas for deterministic Open Signals internal tool calling."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class ToolSchema:
    name: str
    description: str
    required_inputs: list[str]
    optional_inputs: list[str]
    output_schema: dict[str, str]
    privacy_level: str = "aggregate_public"
    failure_behavior: str = "return structured fallback without stack traces"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


TOOL_SCHEMAS: dict[str, ToolSchema] = {
    "get_live_signals": ToolSchema(
        "get_live_signals",
        "Retrieve current interpreted aggregate Open Signals from cache.",
        [],
        ["location", "category", "urgency", "limit"],
        {"signals": "list[aggregate_signal]", "source_status": "string"},
    ),
    "get_top_signal": ToolSchema(
        "get_top_signal",
        "Return the strongest current aggregate signal for the active filters.",
        [],
        ["location", "category", "urgency"],
        {"signal": "aggregate_signal"},
    ),
    "get_county_signals": ToolSchema(
        "get_county_signals",
        "Return county-relevant aggregate signals.",
        ["county"],
        ["category", "time_focus", "limit"],
        {"signals": "list[aggregate_signal]", "county": "string"},
    ),
    "compare_counties": ToolSchema(
        "compare_counties",
        "Compare strongest aggregate signals across two counties.",
        ["county_a", "county_b"],
        ["category", "urgency"],
        {"comparison": "list[county_signal_summary]"},
    ),
    "get_category_signals": ToolSchema(
        "get_category_signals",
        "Return aggregate signals matching a demand category.",
        ["category"],
        ["location", "urgency", "limit"],
        {"signals": "list[aggregate_signal]", "category": "string"},
    ),
    "get_historical_pattern": ToolSchema(
        "get_historical_pattern",
        "Retrieve aggregate historical learning memory for a topic, county, or category.",
        [],
        ["topic", "county", "category", "limit"],
        {"patterns": "list[historical_summary]"},
    ),
    "get_outcome_learning": ToolSchema(
        "get_outcome_learning",
        "Retrieve aggregate outcome-learning evidence for similar signals.",
        [],
        ["topic", "county", "category", "limit"],
        {"outcomes": "list[outcome_summary]"},
    ),
    "get_geospatial_context": ToolSchema(
        "get_geospatial_context",
        "Return county/geospatial aggregate context for a county.",
        ["county"],
        ["category"],
        {"context": "geospatial_summary"},
    ),
    "get_forecast_context": ToolSchema(
        "get_forecast_context",
        "Return forecast-related aggregate context for county/category questions.",
        [],
        ["county", "category", "limit"],
        {"forecast": "forecast_summary"},
    ),
    "get_source_freshness": ToolSchema(
        "get_source_freshness",
        "Classify current source freshness and cache status.",
        [],
        [],
        {"freshness": "string", "last_updated": "string", "status": "string"},
    ),
    "get_evaluation_metrics": ToolSchema(
        "get_evaluation_metrics",
        "Retrieve aggregate evaluation metrics for Open Signals.",
        [],
        [],
        {"metrics": "dict"},
    ),
    "summarize_opportunities": ToolSchema(
        "summarize_opportunities",
        "Summarize aggregate market or service opportunity signals.",
        [],
        ["location", "category", "limit"],
        {"opportunities": "list[opportunity_summary]"},
    ),
    "summarize_risks": ToolSchema(
        "summarize_risks",
        "Summarize aggregate risk, stress, and pressure signals.",
        [],
        ["location", "category", "limit"],
        {"risks": "list[risk_summary]"},
    ),
    "privacy_check": ToolSchema(
        "privacy_check",
        "Check whether a prompt or payload requests private or individual-level data.",
        ["text"],
        [],
        {"allowed": "bool", "reason": "string"},
    ),
}
