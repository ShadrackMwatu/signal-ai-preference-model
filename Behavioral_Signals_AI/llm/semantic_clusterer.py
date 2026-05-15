"""Optional LLM-assisted semantic clustering helpers."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.llm.llm_client import complete_json
from Behavioral_Signals_AI.llm.prompt_templates import SEMANTIC_CLUSTER_TEMPLATE
from Behavioral_Signals_AI.llm.safety_guardrails import sanitize_llm_signals


def llm_cluster_label(records: list[dict[str, Any]], fallback_label: str) -> str:
    safe_records = sanitize_llm_signals(records, limit=6)
    result = complete_json(SEMANTIC_CLUSTER_TEMPLATE, {"records": safe_records}, fallback={"cluster_label": fallback_label})
    label = str(result.get("cluster_label") or fallback_label).strip()
    return label[:90] if label else fallback_label