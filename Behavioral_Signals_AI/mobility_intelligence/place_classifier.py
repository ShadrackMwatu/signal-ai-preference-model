"""Map public place categories into economic demand categories."""

from __future__ import annotations

CATEGORY_KEYWORDS = {
    "food_household_demand": ["supermarket", "grocery", "market", "food", "bakery", "butcher", "restaurant"],
    "retail_trade_demand": ["mall", "retail", "shop", "wholesale", "store", "outlet"],
    "health_demand": ["pharmacy", "clinic", "hospital", "doctor", "health"],
    "transport_demand": ["bus station", "railway", "train", "matatu", "transport", "airport", "taxi"],
    "construction_demand": ["hardware", "cement", "building", "construction", "paint", "timber"],
    "education_demand": ["school", "university", "college", "academy", "education"],
    "financial_services_demand": ["bank", "sacco", "m-pesa", "mpesa", "microfinance", "atm", "finance"],
    "water_access_pressure": ["water point", "borehole", "water", "sanitation"],
}


def classify_place(place_name: str, place_category: str | list[str]) -> str:
    text = f"{place_name} {' '.join(place_category) if isinstance(place_category, list) else place_category}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "general_place_activity"


def demand_category_to_signal_category(category: str) -> str:
    return {
        "food_household_demand": "food and agriculture",
        "retail_trade_demand": "trade and business",
        "health_demand": "health",
        "transport_demand": "transport",
        "construction_demand": "housing",
        "education_demand": "education",
        "financial_services_demand": "finance and credit",
        "water_access_pressure": "water and sanitation",
    }.get(category, "other")