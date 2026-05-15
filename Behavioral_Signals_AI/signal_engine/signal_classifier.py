"""Classify topical signals into demand-relevant categories."""

from __future__ import annotations

CATEGORY_KEYWORDS = {
    "Ceramics": ["ceramic", "tiles", "sanitary", "porcelain"],
    "food and agriculture": ["maize", "flour", "food", "fertilizer", "farm", "agriculture", "beans"],
    "jobs and labour market": ["job", "jobs", "hiring", "employment", "salary"],
    "housing": ["rent", "house", "housing", "apartment", "mortgage"],
    "health": ["hospital", "clinic", "medicine", "health", "doctor"],
    "transport": ["matatu", "fare", "transport", "traffic", "bus"],
    "energy": ["fuel", "electricity", "solar", "power", "cooking gas"],
    "technology": ["smartphone", "phone", "internet", "laptop", "digital"],
    "education": ["school", "fees", "training", "course", "university"],
    "finance": ["loan", "credit", "bank", "mpesa", "insurance", "digital lending"],
    "public services": ["passport", "permit", "water", "county", "public service"],
    "climate and environment": ["rain", "drought", "flood", "climate", "environment"],
}


def classify_topic(topic: str, existing_category: str | None = None) -> str:
    text = f"{topic} {existing_category or ''}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return existing_category or "other"