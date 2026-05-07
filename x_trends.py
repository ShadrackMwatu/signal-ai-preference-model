"""Public aggregate X/Twitter trend fetching for Signal."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from privacy import assert_privacy_safe_records


ROOT_DIR = Path(__file__).resolve().parent
LOCATIONS_PATH = ROOT_DIR / "config" / "locations.json"
X_TRENDS_ENDPOINT = "https://api.twitter.com/1.1/trends/place.json"


def load_location_config(path: str | Path = LOCATIONS_PATH) -> dict[str, dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fetch_x_trends(location: str = "Kenya", limit: int = 10) -> list[dict[str, Any]]:
    """Fetch public aggregate trends or return a safe demo fallback."""

    bearer_token = os.getenv("X_BEARER_TOKEN", "").strip()
    locations = load_location_config()
    if location not in locations:
        raise ValueError(f"Unsupported location: {location}")

    if not bearer_token:
        return get_demo_trends(location, limit=limit)

    try:
        return _fetch_live_trends(location, locations[location]["woeid"], limit, bearer_token)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return get_demo_trends(location, limit=limit)


def get_demo_trends(location: str = "Kenya", limit: int = 10) -> list[dict[str, Any]]:
    fetched_at = datetime.now(UTC).isoformat()
    demo_catalog = {
        "Kenya": [
            ("#KenyaBudget", 1, 185000),
            ("Nairobi Water", 2, 92000),
            ("Digital Lending", 3, 76000),
            ("Agri Logistics", 4, 61000),
            ("Solar Pumps", 5, 54000),
            ("County Health", 6, 48000),
            ("Matatu Cashless", 7, 43000),
            ("SME Credit", 8, 39000),
        ],
        "Nairobi": [
            ("#NairobiTech", 1, 142000),
            ("Housing Delivery", 2, 81000),
            ("Last Mile Delivery", 3, 69000),
            ("Coffee Shops", 4, 51000),
            ("Ride Hailing", 5, 46000),
            ("Weekend Markets", 6, 41000),
            ("School Transport", 7, 35000),
            ("EV Charging", 8, 29000),
        ],
        "Global": [
            ("#AIWorkflows", 1, 420000),
            ("Climate Insurance", 2, 330000),
            ("Digital Payments", 3, 305000),
            ("Telehealth Growth", 4, 271000),
            ("Supply Chain AI", 5, 244000),
            ("Creator Commerce", 6, 221000),
            ("Food Security", 7, 208000),
            ("EV Fleets", 8, 193000),
        ],
    }
    rows = demo_catalog.get(location, demo_catalog["Kenya"])[: max(1, int(limit))]
    records = [
        {
            "trend_name": trend_name,
            "rank": rank,
            "tweet_volume": tweet_volume,
            "location": location,
            "fetched_at": fetched_at,
            "source": "Demo fallback - X API not connected",
        }
        for trend_name, rank, tweet_volume in rows
    ]
    return assert_privacy_safe_records(records)


def _fetch_live_trends(location: str, woeid: int, limit: int, bearer_token: str) -> list[dict[str, Any]]:
    fetched_at = datetime.now(UTC).isoformat()
    query = urlencode({"id": int(woeid)})
    request = Request(f"{X_TRENDS_ENDPOINT}?{query}")
    request.add_header("Authorization", f"Bearer {bearer_token}")
    request.add_header("User-Agent", "SignalAI/1.0")
    with urlopen(request, timeout=20) as response:  # noqa: S310 - controlled API endpoint
        payload = json.loads(response.read().decode("utf-8"))

    if not isinstance(payload, list) or not payload:
        raise ValueError("Unexpected X trends payload structure")

    trend_items = payload[0].get("trends", [])
    records = []
    for index, trend in enumerate(trend_items[: max(1, int(limit))], start=1):
        records.append(
            {
                "trend_name": trend.get("name", f"Trend {index}"),
                "rank": index,
                "tweet_volume": trend.get("tweet_volume"),
                "location": location,
                "fetched_at": fetched_at,
                "source": "X/Twitter API",
            }
        )
    return assert_privacy_safe_records(records)
