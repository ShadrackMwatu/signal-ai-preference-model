"""Turn run memories into better future modelling rules and template advice."""

from __future__ import annotations

from collections import Counter

from .schema import RunMemory


RULE_RECOMMENDATIONS = {
    "gams_unavailable": "When GAMS is unavailable, default new draft runs to backend = python_nlp and mark results experimental.",
    "experimental_solver_used": "For publication or policy-grade runs, require a GAMS-backed solver check before final reporting.",
    "sam_imbalance": "Add a pre-solve SAM balancing step and review accounts with percentage imbalance above tolerance.",
    "unknown_set_reference": "Update SML templates so every indexed symbol references a declared SETS entry.",
    "missing_sam_parameter": "Ensure every SML template includes PARAMETERS: SAM = \"Behavioral_Signals_AI/data/sample_sam.csv\" or an uploaded SAM path.",
    "unspecified_production_solver": "For GAMS runs, prefer explicit solver choices: PATH, CONOPT, or IPOPT.",
    "near_zero_macro_response": "Review shock magnitudes and equation linkage when macro response is near zero.",
}


def recommendations_for_patterns(patterns: list[str]) -> list[str]:
    return [RULE_RECOMMENDATIONS[pattern] for pattern in patterns if pattern in RULE_RECOMMENDATIONS]


def summarize_memory(memories: list[RunMemory]) -> dict[str, object]:
    """Summarize recurring patterns to guide template and validation improvements."""

    error_counts = Counter(pattern for memory in memories for pattern in memory.error_patterns)
    result_counts = Counter(pattern for memory in memories for pattern in memory.result_patterns)
    top_patterns = [pattern for pattern, _ in error_counts.most_common(5)]
    recommendations = recommendations_for_patterns(top_patterns)
    return {
        "runs_observed": len(memories),
        "error_pattern_counts": dict(error_counts),
        "result_pattern_counts": dict(result_counts),
        "recommended_template_rules": recommendations,
    }
