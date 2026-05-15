"""County matching and geospatial classification for Kenya aggregate signals."""

from __future__ import annotations

import json
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
COUNTY_REGISTRY_PATH = BASE_DIR / "county_code_registry.json"
COUNTY_ALIASES_PATH = BASE_DIR / "county_aliases.json"


@lru_cache(maxsize=1)
def load_county_registry() -> dict[str, str]:
    return json.loads(COUNTY_REGISTRY_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_county_aliases() -> dict[str, str]:
    return json.loads(COUNTY_ALIASES_PATH.read_text(encoding="utf-8"))


def county_names() -> list[str]:
    return list(load_county_registry().values())


def county_dropdown_choices() -> list[str]:
    return ["Global", "Kenya"] + county_names()


def county_code_for_name(name: str) -> str:
    normalized = _normalize(name)
    for code, county in load_county_registry().items():
        if _normalize(county) == normalized:
            return code
    return ""


def canonical_county_name(name: str) -> str:
    normalized = _normalize(name)
    for county in county_names():
        if _normalize(county) == normalized:
            return county
    aliases = load_county_aliases()
    return aliases.get(normalized, "")


def detect_county_from_text(text: str) -> dict[str, str]:
    normalized_text = _normalize(text)
    if not normalized_text:
        return {"county_name": "Kenya-wide", "county_code": "", "geographic_scope": "Kenya-wide"}
    aliases = load_county_aliases()
    for alias, county in aliases.items():
        if _word_contains(normalized_text, alias):
            code = county_code_for_name(county)
            return {"county_name": county, "county_code": code, "geographic_scope": county}
    for code, county in load_county_registry().items():
        if _word_contains(normalized_text, _normalize(county)):
            return {"county_name": county, "county_code": code, "geographic_scope": county}
    return {"county_name": "Kenya-wide", "county_code": "", "geographic_scope": "Kenya-wide"}


def signal_matches_location(signal: dict[str, Any], location: str) -> bool:
    if location in {"", "All", "Kenya"}:
        return True
    if location == "Global":
        return True
    target = canonical_county_name(location) or location
    target_norm = _normalize(target)
    fields = [
        signal.get("county_name", ""),
        signal.get("geographic_scope", ""),
        signal.get("signal_topic", ""),
        signal.get("geospatial_insight", ""),
    ]
    haystack = _normalize(" ".join(str(field) for field in fields))
    return _word_contains(haystack, target_norm)


def enrich_signal_geography(signal: dict[str, Any]) -> dict[str, Any]:
    text = " ".join(str(signal.get(key, "")) for key in ["signal_topic", "geographic_scope", "source_summary", "interpretation"])
    detected = detect_county_from_text(text)
    county_name = signal.get("county_name") or detected["county_name"]
    county_code = signal.get("county_code") or county_code_for_name(str(county_name))
    scope = str(signal.get("geographic_scope") or detected["geographic_scope"] or "Kenya-wide")
    enriched = dict(signal)
    enriched["county_name"] = county_name
    enriched["county_code"] = county_code
    enriched["geographic_scope"] = scope
    enriched.setdefault("spread_risk", _spread_risk(scope, float(signal.get("geographic_spread_score", 0) or 0)))
    enriched.setdefault("forecast_direction", str(signal.get("predicted_direction", "Stable")).title())
    enriched.setdefault("geospatial_insight", geospatial_interpretation(enriched))
    enriched.setdefault("ml_rank_score", _ml_rank_score(enriched))
    return enriched


def geospatial_interpretation(signal: dict[str, Any]) -> str:
    county = str(signal.get("county_name") or signal.get("geographic_scope") or "Kenya-wide")
    category = str(signal.get("signal_category", "aggregate demand"))
    if county == "Kenya-wide":
        return f"This is currently a Kenya-wide aggregate {category} signal; county specificity may strengthen as more local evidence appears."
    return f"This signal matters in {county} because recurring county-level aggregate evidence may indicate localized {category}, stress, or opportunity."


def _spread_risk(scope: str, spread_score: float) -> str:
    if scope != "Kenya-wide" and spread_score >= 65:
        return "High"
    if scope != "Kenya-wide" or spread_score >= 45:
        return "Moderate"
    return "Low"


def _ml_rank_score(signal: dict[str, Any]) -> float:
    confidence = float(signal.get("confidence_score", 50) or 50)
    priority = float(signal.get("priority_score", signal.get("behavioral_intelligence_score", 50)) or 50)
    spread = float(signal.get("geographic_spread_score", 35) or 35)
    recurrence = float(signal.get("historical_recurrence_score", 20) or 20)
    return round(min(100.0, confidence * 0.35 + priority * 0.35 + spread * 0.15 + recurrence * 0.15), 2)


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    return " ".join(normalized.lower().replace("'", "").replace("-", " ").split())


def _word_contains(haystack: str, needle: str) -> bool:
    if not needle:
        return False
    return f" {needle} " in f" {haystack} "