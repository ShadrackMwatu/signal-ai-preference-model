"""Outcome-based learning for Behavioral Signals AI.

This module compares past aggregate signal predictions with later aggregate or
analyst-authorized evidence. It never stores individual-level data and only
keeps lightweight cluster-level learning summaries.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

OUTCOME_MEMORY_PATH = Path("Behavioral_Signals_AI/outputs/outcome_learning_memory.json")
FOLLOW_UP_WINDOWS_DAYS = [7, 30, 90, 365]
_ALLOWED_STATUSES = {"confirmed", "partially_confirmed", "not_confirmed", "still_monitoring"}
_PRIVATE_FIELDS = {
    "user_id",
    "email",
    "phone",
    "private_message",
    "exact_location",
    "personal_profile",
    "profile_url",
    "ip_address",
    "device_id",
}


def default_outcome_memory() -> dict[str, Any]:
    return {
        "version": 1,
        "last_updated": None,
        "follow_up_windows_days": FOLLOW_UP_WINDOWS_DAYS[:],
        "clusters": {},
        "privacy_policy": "aggregate_public_or_authorized_evidence_only",
    }


def initialize_outcome_memory(path: str | Path | None = None) -> dict[str, Any]:
    """Create outcome memory if needed and return a valid memory object."""
    target = Path(path) if path is not None else OUTCOME_MEMORY_PATH
    memory = load_outcome_memory(target)
    write_json(target, memory, backup=False)
    return memory


def load_outcome_memory(path: str | Path | None = None) -> dict[str, Any]:
    """Load memory with corruption recovery and required schema fields."""
    target = Path(path) if path is not None else OUTCOME_MEMORY_PATH
    memory = read_json(target, default_outcome_memory())
    if not isinstance(memory, dict):
        memory = default_outcome_memory()
    memory.setdefault("version", 1)
    memory.setdefault("last_updated", None)
    memory.setdefault("follow_up_windows_days", FOLLOW_UP_WINDOWS_DAYS[:])
    memory.setdefault("clusters", {})
    memory.setdefault("privacy_policy", "aggregate_public_or_authorized_evidence_only")
    return memory


def apply_outcome_learning(signal: dict[str, Any], evidence: dict[str, Any] | None = None, path: str | Path | None = None) -> dict[str, Any]:
    """Attach outcome-learning fields and adapt future confidence.

    Explicit evidence can be passed by tests, analysts, or future official-data
    connectors. Without evidence, the signal is registered for monitoring and
    scored using prior outcomes for the same semantic cluster.
    """
    enriched = dict(signal)
    target = Path(path) if path is not None else OUTCOME_MEMORY_PATH
    memory = load_outcome_memory(target)
    cluster_key = _cluster_key(enriched)
    cluster = memory["clusters"].setdefault(cluster_key, _new_cluster(cluster_key, enriched))

    clean_evidence = _sanitize_evidence(evidence or {})
    if clean_evidence:
        _append_outcome_record(cluster, enriched, clean_evidence)
    elif not cluster.get("records"):
        _append_outcome_record(cluster, enriched, {"outcome_status": "still_monitoring"})

    _recompute_cluster_summary(cluster)
    _apply_cluster_adjustment(enriched, cluster)
    memory["last_updated"] = datetime.now(UTC).isoformat()
    write_json(target, memory)
    return enriched


def record_observed_outcome(signal: dict[str, Any], outcome_status: str, observed_outcome: str = "", accuracy_score: float | int | None = None, path: str | Path | None = None) -> dict[str, Any]:
    """Record a later aggregate outcome for a prior signal cluster."""
    evidence = {
        "outcome_status": outcome_status,
        "observed_outcome": observed_outcome,
        "accuracy_score": accuracy_score,
    }
    return apply_outcome_learning(signal, evidence=evidence, path=path)


def recognized_follow_up_windows() -> list[int]:
    return FOLLOW_UP_WINDOWS_DAYS[:]


def _new_cluster(cluster_key: str, signal: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_cluster": cluster_key,
        "first_seen": datetime.now(UTC).isoformat(),
        "last_seen": datetime.now(UTC).isoformat(),
        "records": [],
        "confirmed_count": 0,
        "not_confirmed_count": 0,
        "monitoring_count": 0,
        "average_accuracy_score": 50,
        "outcome_learning_status": "new",
        "lesson_learned": "Outcome evidence is still accumulating.",
        "future_adjustment": "Keep confidence conservative until follow-up evidence confirms the pattern.",
        "example_prediction": _prediction_text(signal),
    }


def _append_outcome_record(cluster: dict[str, Any], signal: dict[str, Any], evidence: dict[str, Any]) -> None:
    status = str(evidence.get("outcome_status") or "still_monitoring")
    if status not in _ALLOWED_STATUSES:
        status = "still_monitoring"
    accuracy = _coerce_score(evidence.get("accuracy_score"), _default_accuracy(status))
    record = {
        "signal_cluster": cluster.get("signal_cluster") or _cluster_key(signal),
        "original_prediction": _prediction_text(signal),
        "predicted_direction": str(signal.get("forecast_direction") or signal.get("predicted_direction") or "Stable").title(),
        "predicted_opportunity": str(signal.get("opportunity_interpretation") or signal.get("business_opportunity") or signal.get("recommended_action") or "Monitor aggregate evidence."),
        "prediction_date": str(signal.get("last_updated") or datetime.now(UTC).date().isoformat()),
        "follow_up_window_days": int(evidence.get("follow_up_window_days") or 7),
        "recognized_follow_up_windows_days": FOLLOW_UP_WINDOWS_DAYS[:],
        "observed_outcome": str(evidence.get("observed_outcome") or _default_observed_outcome(status)),
        "outcome_status": status,
        "accuracy_score": accuracy,
        "lesson_learned": str(evidence.get("lesson_learned") or _lesson_for_status(status, signal)),
        "future_adjustment": str(evidence.get("future_adjustment") or _adjustment_for_status(status)),
        "evidence_sources": _safe_list(evidence.get("evidence_sources") or evidence.get("validation_sources") or []),
        "privacy_level": "aggregate_public_or_authorized",
        "recorded_at": datetime.now(UTC).isoformat(),
    }
    cluster.setdefault("records", []).append(record)
    cluster["last_seen"] = datetime.now(UTC).isoformat()


def _recompute_cluster_summary(cluster: dict[str, Any]) -> None:
    records = list(cluster.get("records", []))
    if not records:
        return
    confirmed = [r for r in records if r.get("outcome_status") == "confirmed"]
    partial = [r for r in records if r.get("outcome_status") == "partially_confirmed"]
    not_confirmed = [r for r in records if r.get("outcome_status") == "not_confirmed"]
    monitoring = [r for r in records if r.get("outcome_status") == "still_monitoring"]
    scores = [_coerce_score(r.get("accuracy_score"), 50) for r in records]
    average = round(sum(scores) / len(scores), 1) if scores else 50
    cluster["confirmed_count"] = len(confirmed) + len(partial)
    cluster["not_confirmed_count"] = len(not_confirmed)
    cluster["monitoring_count"] = len(monitoring)
    cluster["average_accuracy_score"] = average
    if cluster["confirmed_count"] and cluster["confirmed_count"] >= cluster["not_confirmed_count"] and average >= 64:
        status = "historically_confirmed"
        lesson = "Similar aggregate signals have often been followed by observable pressure or opportunity."
        adjustment = "Increase future confidence moderately for similar confirmed signal clusters."
    elif cluster["not_confirmed_count"] > cluster["confirmed_count"] and average <= 45:
        status = "historically_weak"
        lesson = "Similar signals were not consistently confirmed by later aggregate evidence."
        adjustment = "Reduce confidence and treat similar future signals as potentially noisy until confirmed."
    elif monitoring:
        status = "monitoring"
        lesson = "This signal type is still being monitored across follow-up windows."
        adjustment = "Maintain conservative confidence until 7, 30, 90, or 365 day evidence arrives."
    else:
        status = "new"
        lesson = "Outcome learning has not accumulated enough evidence for this cluster."
        adjustment = "Keep learning from future follow-up evidence."
    cluster["outcome_learning_status"] = status
    cluster["lesson_learned"] = lesson
    cluster["future_adjustment"] = adjustment


def _apply_cluster_adjustment(signal: dict[str, Any], cluster: dict[str, Any]) -> None:
    status = str(cluster.get("outcome_learning_status") or "new")
    historical_score = _coerce_score(cluster.get("average_accuracy_score"), 50)
    base_confidence = _coerce_score(signal.get("confidence_score"), 50)
    source_score = _coerce_score(signal.get("source_reliability_score"), 50)
    category_score = _coerce_score(signal.get("category_confidence_score"), 50)
    if status == "historically_confirmed":
        signal["confidence_score"] = min(100, round(base_confidence + 6, 1))
        signal["source_reliability_score"] = min(100, round(source_score + 4, 1))
        signal["category_confidence_score"] = min(100, round(category_score + 3, 1))
        note = "Historically, similar signals have often preceded real-world pressure or opportunity."
    elif status == "historically_weak":
        signal["confidence_score"] = max(0, round(base_confidence - 8, 1))
        signal["source_reliability_score"] = max(0, round(source_score - 3, 1))
        signal["category_confidence_score"] = max(0, round(category_score - 3, 1))
        note = "Similar past signals were not consistently confirmed, so Signal is scoring this conservatively."
    elif status == "monitoring":
        signal["confidence_score"] = round(base_confidence, 1)
        note = "This type of signal is still being monitored; confidence may improve with more evidence."
    else:
        signal["confidence_score"] = round(base_confidence, 1)
        note = "Outcome learning has started for this signal cluster and will adapt as evidence arrives."
    signal["outcome_learning_status"] = status
    signal["historical_accuracy_score"] = historical_score
    signal["outcome_learning_note"] = f"{note} {cluster.get('future_adjustment', '')}".strip()
    signal["outcome_follow_up_windows_days"] = FOLLOW_UP_WINDOWS_DAYS[:]


def _cluster_key(signal: dict[str, Any]) -> str:
    text = str(signal.get("semantic_cluster") or signal.get("signal_cluster") or signal.get("signal_topic") or "kenya aggregate signal")
    return " ".join(text.lower().strip().split())


def _prediction_text(signal: dict[str, Any]) -> str:
    topic = signal.get("signal_topic") or signal.get("semantic_cluster") or "Kenya aggregate signal"
    direction = signal.get("forecast_direction") or signal.get("predicted_direction") or "Stable"
    demand = signal.get("demand_level") or "Moderate"
    opportunity = signal.get("opportunity_level") or "Moderate"
    return f"{topic}: {direction} direction, {demand} demand, {opportunity} opportunity"


def _sanitize_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in evidence.items():
        if str(key).lower() in _PRIVATE_FIELDS:
            continue
        clean[key] = value
    return clean


def _safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def _coerce_score(value: Any, default: float) -> float:
    try:
        number = float(value)
    except Exception:
        number = float(default)
    return max(0.0, min(100.0, number))


def _default_accuracy(status: str) -> float:
    return {
        "confirmed": 86,
        "partially_confirmed": 68,
        "not_confirmed": 28,
        "still_monitoring": 50,
    }.get(status, 50)


def _default_observed_outcome(status: str) -> str:
    return {
        "confirmed": "Later aggregate evidence confirmed the predicted pressure or opportunity.",
        "partially_confirmed": "Later aggregate evidence partially supported the prediction.",
        "not_confirmed": "Later aggregate evidence did not confirm the prediction within the follow-up window.",
        "still_monitoring": "Awaiting aggregate follow-up evidence across 7, 30, 90, and 365 day windows.",
    }.get(status, "Awaiting follow-up evidence.")


def _lesson_for_status(status: str, signal: dict[str, Any]) -> str:
    category = signal.get("signal_category", "this category")
    return {
        "confirmed": f"Aggregate {category} signals deserve higher attention when similar evidence persists.",
        "partially_confirmed": f"Aggregate {category} signals should be monitored with moderate confidence.",
        "not_confirmed": f"Aggregate {category} signals may be noisy unless repeated or confirmed by trusted sources.",
        "still_monitoring": f"Aggregate {category} signals need follow-up evidence before strong conclusions.",
    }.get(status, "Outcome lesson is still developing.")


def _adjustment_for_status(status: str) -> str:
    return {
        "confirmed": "Increase future confidence for similar persistent, multi-source signals.",
        "partially_confirmed": "Raise confidence slightly when similar signals recur across sources.",
        "not_confirmed": "Reduce future confidence unless similar signals persist or gain validation.",
        "still_monitoring": "Keep confidence conservative until later aggregate evidence is available.",
    }.get(status, "Continue monitoring aggregate evidence.")