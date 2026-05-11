def interpret_shock(prompt: str) -> dict:
    text = prompt.lower()

    if "government spending" in text or "public spending" in text:
        return {
            "shock_type": "government_spending",
            "target": "government_demand",
            "percent_change": extract_percent(text),
        }

    if "tariff" in text or "import duty" in text:
        return {
            "shock_type": "import_tariff",
            "target": "import_tax_rate",
            "percent_change": extract_percent(text),
        }

    if "care infrastructure" in text:
        return {
            "shock_type": "care_infrastructure",
            "target": "care_investment",
            "percent_change": extract_percent(text),
        }

    if "agricultural productivity" in text or "agriculture productivity" in text:
        return {
            "shock_type": "productivity",
            "target": "agriculture",
            "percent_change": extract_percent(text),
        }

    return {
        "shock_type": "unknown",
        "target": None,
        "percent_change": None,
    }


def extract_percent(text: str):
    import re
    match = re.search(r"(\d+(\.\d+)?)\s*%", text)
    if match:
        return float(match.group(1))
    return None


if __name__ == "__main__":
    examples = [
        "increase government spending by 10%",
        "reduce import tariff on machinery by 10%",
        "double care infrastructure investment",
        "increase agricultural productivity by 5%",
    ]

    for e in examples:
        print(e, "=>", interpret_shock(e))