"""Scenario-aware retrieval from canonical Signal CGE reference documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .document_loader import load_knowledge_base, load_reference_text
from .semantic_mapping import map_prompt_semantics


REFERENCE_RULES = {
    "import_tariff": [
        "equations/TRADE_BLOCK.md",
        "equations/GOVERNMENT_BLOCK.md",
        "equations/PRICE_BLOCK.md",
        "equations/MACRO_CLOSURE.md",
        "experiments/EXPERIMENT_WORKFLOW.md",
    ],
    "trade_facilitation": [
        "equations/TRADE_BLOCK.md",
        "equations/PRICE_BLOCK.md",
        "equations/MARKET_CLEARING.md",
        "experiments/EXPERIMENT_WORKFLOW.md",
    ],
    "tax": [
        "equations/GOVERNMENT_BLOCK.md",
        "equations/HOUSEHOLD_DEMAND_BLOCK.md",
        "equations/PRICE_BLOCK.md",
        "equations/MACRO_CLOSURE.md",
    ],
    "vat_tax": [
        "equations/GOVERNMENT_BLOCK.md",
        "equations/HOUSEHOLD_DEMAND_BLOCK.md",
        "equations/PRICE_BLOCK.md",
        "equations/MACRO_CLOSURE.md",
    ],
    "care_infrastructure": [
        "equations/INVESTMENT_SAVINGS_BLOCK.md",
        "equations/HOUSEHOLD_DEMAND_BLOCK.md",
        "equations/FACTOR_MARKET_BLOCK.md",
        "workflows/AI_INTEGRATION_NOTES.md",
    ],
    "public_investment": [
        "equations/INVESTMENT_SAVINGS_BLOCK.md",
        "equations/GOVERNMENT_BLOCK.md",
        "equations/MARKET_CLEARING.md",
        "experiments/EXPERIMENT_WORKFLOW.md",
    ],
    "government_spending": [
        "equations/GOVERNMENT_BLOCK.md",
        "equations/HOUSEHOLD_DEMAND_BLOCK.md",
        "equations/MACRO_CLOSURE.md",
        "equations/MARKET_CLEARING.md",
    ],
    "productivity": [
        "equations/PRODUCTION_BLOCK.md",
        "equations/FACTOR_MARKET_BLOCK.md",
        "equations/RECURSIVE_DYNAMICS.md",
    ],
}


def get_scenario_context(scenario: dict[str, Any]) -> dict[str, Any]:
    """Return scenario-relevant reference snippets and labels."""

    shock_type = str(scenario.get("shock_type") or scenario.get("policy_instrument") or "").lower()
    prompt_text = str(scenario.get("prompt", "")).lower()
    semantic_hints = map_prompt_semantics(prompt_text, scenario)
    if "tariff" in prompt_text and "import" in prompt_text:
        shock_type = "import_tariff"
    references = REFERENCE_RULES.get(shock_type, ["experiments/EXPERIMENT_WORKFLOW.md", "equations/MACRO_CLOSURE.md"])
    loaded = []
    for relative_path in references:
        text = load_reference_text(relative_path)
        loaded.append(
            {
                "path": f"Documentation/signal_cge_reference/{relative_path}",
                "title": _title_from_path(relative_path),
                "summary": _summarize_reference(text),
            }
        )
    loaded.append(
        {
            "path": "Documentation/SIGNAL_CGE_KNOWLEDGE_BASE.md",
            "title": "Signal CGE Knowledge Base",
            "summary": _summarize_reference(load_knowledge_base()),
        }
    )
    return {
        "scenario_type": shock_type or "general",
        "references": loaded,
        "reference_labels": [item["title"] for item in loaded],
        "semantic_hints": semantic_hints,
    }


def _title_from_path(path: str) -> str:
    return Path(path).stem.replace("_", " ").replace("-", " ").title()


def _summarize_reference(text: str, limit: int = 220) -> str:
    compact = " ".join(line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#"))
    return compact[:limit].rstrip() + ("..." if len(compact) > limit else "")
