"""Google Trends / SerpAPI aggregate search connector placeholder.

Uses environment variables only. Does not collect individual searches.
TODO: activate via SERPAPI_KEY or a compliant trends provider.
"""

import os
from Behavioral_Signals_AI.data_sources._aggregate_connector_utils import sample_record


def collect(source=None):
    configured = bool(os.getenv("SERPAPI_KEY") or os.getenv("GOOGLE_TRENDS_API_KEY"))
    confidence = 80 if configured else 64
    return [sample_record("Rising Kenya search interest in food prices", "cost of living", "Google Trends / SerpAPI", "search_trends", confidence, "Aggregate search interest can reveal demand pressure without exposing individual searches.", "SERPAPI_KEY configured" if configured else "sample aggregate search signal")]
