"""Adaptive category learning for Open Signals aggregate intelligence."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

MEMORY_PATH = Path("Behavioral_Signals_AI/outputs/category_learning_memory.json")

DEFAULT_CATEGORIES = [
    "All",
    "Ceramics",
    "food and agriculture",
    "jobs and labour market",
    "housing",
    "health",
    "transport",
    "energy",
    "technology",
    "education",
    "finance",
    "public services",
    "water and sanitation",
    "climate and environment",
    "cost of living",
    "trade and business",
    "security and governance",
    "other",
]

LEARNABLE_CATEGORY_RULES: dict[str, list[str]] = {
    "care economy": ["care work", "childcare", "daycare", "elder care", "caregiver", "domestic care"],
    "digital services": ["digital service", "online service", "internet service", "app service", "platform", "e citizen", "ecitizen"],
    "household affordability": ["cheap", "affordable", "low cost", "discount", "pay later", "installment", "household prices"],
    "construction materials": ["cement", "mabati", "steel", "hardware", "building materials", "sand", "ballast"],
    "transport logistics": ["logistics", "delivery", "freight", "courier", "truck", "cargo", "last mile"],
    "healthcare access": ["hospital near me", "clinic near me", "pharmacy near me", "medicine access", "doctor appointment"],
    "youth employment": ["youth jobs", "internship", "graduate jobs", "entry level jobs", "attachment", "hustle"],
    "agricultural inputs": ["fertilizer", "seeds", "animal feed", "agrovet", "farm inputs", "pesticide"],
    "retail demand": ["supermarket", "shop near me", "mall", "retail", "wholesale", "duka"],
    "mobility pressure": ["traffic", "bus fare", "matatu", "bus station", "commute", "congestion"],
    "county services": ["county services", "county permit", "county hospital", "county bursary", "county office"],
    "water access": ["water shortage", "borehole", "water point", "water rationing", "clean water"],
    "SME finance": ["sme loan", "business loan", "working capital", "small business finance", "merchant loan"],
}

_DEFAULT_DUPLICATE_TERMS: dict[str, list[str]] = {
    "food and agriculture": ["food", "maize", "unga", "fertilizer", "seed", "agriculture", "farm"],
    "jobs and labour market": ["jobs", "employment", "labour", "salary", "internship"],
    "housing": ["rent", "housing", "landlord", "bedsitter", "apartment"],
    "health": ["hospital", "clinic", "pharmacy", "medicine", "doctor"],
    "transport": ["transport", "matatu", "bus", "traffic", "fuel", "fare"],
    "energy": ["electricity", "tokens", "power", "fuel", "solar"],
    "technology": ["smartphone", "internet", "digital", "app", "software"],
    "education": ["school", "university", "fees", "student", "teacher"],
    "finance": ["loan", "credit", "bank", "sacco", "mpesa", "m-pesa"],
    "public services": ["public service", "permit", "bursary", "county office", "government service"],
    "water and sanitation": ["water", "sanitation", "sewer", "borehole"],
    "climate and environment": ["drought", "flood", "rainfall", "climate", "environment"],
    "cost of living": ["cost of living", "prices", "expensive", "cheap", "affordable", "high cost"],
    "trade and business": ["business", "retail", "wholesale", "market", "shop", "sme"],
    "security and governance": ["security", "crime", "governance", "police", "protest"],
    "Ceramics": ["ceramic", "tiles", "pottery", "sanitary ware"],
}

FORBIDDEN_PERSONAL_PATTERNS = [
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"\b(?:\+?254|0)?7\d{8}\b"),
    re.compile(r"\b(?:user_id|device_id|phone|email|private_message|personal_profile|exact address|id number)\b", re.IGNORECASE),
]

MIN_PROMOTION_APPEARANCES = 2
MIN_PROMOTION_CONFIDENCE = 70.0


def default_category_memory() -> dict[str, Any]:
    return {"last_updated": None, "categories": {}, "privacy_level": "aggregate_category_learning_only"}


def load_category_memory(path: str | Path | None = None) -> dict[str, Any]:
    payload = read_json(Path(path) if path else MEMORY_PATH, default_category_memory())
    if not isinstance(payload, dict):
        return default_category_memory()
    payload.setdefault("categories", {})
    payload.setdefault("privacy_level", "aggregate_category_learning_only")
    return payload


def learn_categories_from_signals(signals: list[dict[str, Any]], path: str | Path | None = None) -> dict[str, Any]:
    memory_path = Path(path) if path else MEMORY_PATH
    memory = load_category_memory(memory_path)
    now = datetime.now(UTC).isoformat()
    changed = False

    for signal in signals or []:
        text = _signal_text(signal)
        if not text or _has_personal_data(text):
            continue
        suggestion = suggest_category(text)
        if not suggestion:
            continue
        category, terms = suggestion
        duplicate = matching_default_category(category, terms)
        if duplicate and _normalize(duplicate) != _normalize(category):
            # Keep defaults canonical; do not create noisy aliases as new visible categories.
            continue
        entry = memory["categories"].setdefault(category, {
            "category_name": category,
            "first_seen": now,
            "last_seen": now,
            "appearance_count": 0,
            "related_terms": [],
            "example_signals": [],
            "confidence_score": 0.0,
            "status": "candidate",
        })
        entry["last_seen"] = now
        entry["appearance_count"] = int(entry.get("appearance_count", 0)) + 1
        _extend_unique(entry["related_terms"], terms, 16)
        _extend_unique(entry["example_signals"], [str(signal.get("signal_topic") or signal.get("topic") or text)[:120]], 8)
        entry["confidence_score"] = _category_confidence(entry)
        entry["status"] = _category_status(category, entry)
        changed = True

    if changed:
        memory["last_updated"] = now
        write_json(memory_path, memory)
    elif not memory_path.exists():
        write_json(memory_path, memory, backup=False)
    return memory


def get_active_learned_categories(path: str | Path | None = None) -> list[str]:
    memory = load_category_memory(path)
    active = []
    for category, entry in memory.get("categories", {}).items():
        if entry.get("status") == "active" and not matching_default_category(category, entry.get("related_terms", [])):
            active.append(str(category))
    return sorted(set(active), key=str.lower)


def get_category_options(path: str | Path | None = None) -> list[str]:
    options = list(DEFAULT_CATEGORIES)
    for category in get_active_learned_categories(path):
        if not any(_normalize(category) == _normalize(existing) for existing in options):
            options.append(category)
    return _dedupe_keep_order(options)


def category_matches_signal(signal: dict[str, Any], selected_category: str, path: str | Path | None = None) -> bool:
    if selected_category in {"", "All", None}:
        return True
    selected = str(selected_category)
    signal_category = str(signal.get("signal_category", ""))
    if _normalize(signal_category) == _normalize(selected):
        return True
    text = _normalize(_signal_text(signal))
    selected_norm = _normalize(selected)
    if selected_norm and selected_norm in text:
        return True
    memory = load_category_memory(path)
    entry = memory.get("categories", {}).get(selected, {})
    terms = entry.get("related_terms", []) if isinstance(entry, dict) else []
    return any(_normalize(term) in text for term in terms if term)


def suggest_category(text: str) -> tuple[str, list[str]] | None:
    normalized = _normalize(text)
    if not normalized or _has_personal_data(text):
        return None
    best_category = ""
    best_terms: list[str] = []
    best_score = 0
    for category, terms in LEARNABLE_CATEGORY_RULES.items():
        matched = [term for term in terms if _normalize(term) in normalized]
        if len(matched) > best_score:
            best_category = category
            best_terms = matched
            best_score = len(matched)
    if not best_category:
        return None
    return best_category, best_terms or [best_category]


def matching_default_category(category: str, terms: list[str] | None = None) -> str:
    category_norm = _normalize(category)
    for default in DEFAULT_CATEGORIES:
        if category_norm == _normalize(default):
            return default
    haystack = _normalize(" ".join([category, *(terms or [])]))
    for default, default_terms in _DEFAULT_DUPLICATE_TERMS.items():
        if _normalize(default) == "all" or _normalize(default) == "other":
            continue
        if _normalize(default) in haystack:
            return default
        if any(_normalize(term) in haystack for term in default_terms):
            return default
    return ""


def reject_personal_category_text(text: str) -> None:
    if _has_personal_data(text):
        raise ValueError("Category learning only accepts aggregate, anonymized signal text.")


def _signal_text(signal: dict[str, Any]) -> str:
    fields = [
        signal.get("signal_topic", ""),
        signal.get("topic", ""),
        signal.get("signal_category", ""),
        signal.get("interpretation", ""),
        signal.get("source_summary", ""),
    ]
    return " ".join(str(field) for field in fields if field)


def _category_confidence(entry: dict[str, Any]) -> float:
    appearances = int(entry.get("appearance_count", 0))
    term_count = len(entry.get("related_terms", []))
    examples = len(entry.get("example_signals", []))
    return round(min(95.0, 45.0 + appearances * 18.0 + term_count * 3.0 + examples * 2.0), 2)


def _category_status(category: str, entry: dict[str, Any]) -> str:
    if _has_personal_data(category):
        return "rejected"
    if matching_default_category(category, entry.get("related_terms", [])):
        return "rejected"
    if int(entry.get("appearance_count", 0)) >= MIN_PROMOTION_APPEARANCES and float(entry.get("confidence_score", 0) or 0) >= MIN_PROMOTION_CONFIDENCE:
        return "active"
    return "candidate"


def _extend_unique(target: list[str], values: list[str], limit: int) -> None:
    for value in values:
        cleaned = str(value).strip()
        if cleaned and cleaned not in target and not _has_personal_data(cleaned):
            target.append(cleaned)
    del target[:-limit]


def _dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        key = _normalize(value)
        if key not in seen:
            seen.add(key)
            output.append(value)
    return output


def _has_personal_data(text: str) -> bool:
    return any(pattern.search(str(text or "")) for pattern in FORBIDDEN_PERSONAL_PATTERNS)


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())
