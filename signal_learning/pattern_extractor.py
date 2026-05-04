"""Recurring pattern extraction for Signal learning evidence."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .memory_schema import LearningPattern


PATTERN_ACTIONS = {
    "sam_imbalance": "Suggest likely correction areas from high row-column imbalance accounts before solving.",
    "gams_error": "Attach GAMS common-error guidance and inspect generated indexing/template blocks.",
    "validation_error": "Strengthen SML validation rules for this model pattern.",
    "gams_unavailable": "Recommend installing GAMS for production or selecting experimental backend explicitly.",
    "experimental_solver": "Require a trusted GAMS/solver confirmation before final policy use.",
    "successful_model_run": "Promote this model structure as a candidate scenario template after more evidence.",
}


def extract_patterns(store_data: dict[str, Any], min_occurrences: int = 1) -> list[LearningPattern]:
    """Identify recurring issues/results from evidence-linked feedback."""

    feedback = store_data.get("feedback", [])
    counts = Counter(entry["issue_type"] for entry in feedback)
    runs_by_issue: dict[str, set[str]] = defaultdict(set)
    for entry in feedback:
        runs_by_issue[entry["issue_type"]].add(str(entry["run_id"]))

    patterns: list[LearningPattern] = []
    for issue_type, occurrences in sorted(counts.items()):
        if occurrences < min_occurrences:
            continue
        confidence = min(0.95, 0.45 + 0.1 * occurrences)
        patterns.append(
            LearningPattern(
                pattern_id=f"pattern_{issue_type}",
                issue_type=issue_type,
                description=f"Observed {occurrences} occurrence(s) of {issue_type}.",
                evidence_run_ids=sorted(runs_by_issue[issue_type]),
                occurrences=occurrences,
                confidence_score=confidence,
                recommended_action=PATTERN_ACTIONS.get(issue_type, "Review recurring evidence and update rules manually."),
            )
        )
    return patterns


def recurring_issue_summary(store_data: dict[str, Any]) -> dict[str, Any]:
    patterns = extract_patterns(store_data)
    return {
        "recurring_issues": [pattern.to_dict() for pattern in patterns],
        "top_recommendations": [pattern.recommended_action for pattern in patterns[:5]],
    }
