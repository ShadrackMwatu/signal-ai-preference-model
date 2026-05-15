"""Early warning labels for Kenya behavioral-economic signals."""

from __future__ import annotations

from typing import Any

PRESSURE_CATEGORIES = {
    "food and agriculture",
    "cost of living",
    "energy",
    "water and sanitation",
    "health",
    "transport",
    "jobs and labour market",
}


def classify_early_warning(signal: dict[str, Any], related_signals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Assign deterministic early-warning labels from aggregate signal evidence."""
    related = related_signals or []
    labels: list[str] = []
    category = str(signal.get("signal_category", "other")).lower()
    momentum = str(signal.get("momentum", "Stable"))
    urgency = str(signal.get("urgency", "Medium"))
    confidence = _num(signal.get("confidence_score"), 50)
    priority = _num(signal.get("priority_score"), confidence)
    source_confirmation = _num(signal.get("multi_source_confirmation_score"), 45)
    related_count = len(related)

    if momentum in {"Breakout", "Rising"} and (urgency == "High" or priority >= 72):
        labels.append("Early warning")
    if urgency == "High" and confidence >= 62:
        labels.append("Escalating pressure")
    if category in PRESSURE_CATEGORIES and (source_confirmation >= 65 or related_count >= 2):
        labels.append("Emerging stress")
    if category in {"food and agriculture", "water and sanitation", "energy", "health"} and urgency in {"High", "Medium"}:
        labels.append("Potential supply gap")
    if category in {"cost of living", "public services", "health", "water and sanitation", "jobs and labour market"} and confidence >= 58:
        labels.append("Potential policy concern")

    if not labels and momentum == "Breakout":
        labels.append("Early warning")
    severity = "High" if any(label in labels for label in ["Escalating pressure", "Potential supply gap"]) else ("Medium" if labels else "Low")
    return {"early_warning_labels": _dedupe(labels), "early_warning_severity": severity}


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output


def _num(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default
