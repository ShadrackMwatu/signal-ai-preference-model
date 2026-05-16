"""Kenya public news/report connector placeholder.

TODO: activate public RSS or licensed news APIs. Avoid private scraping.
"""

import os
from Behavioral_Signals_AI.data_sources._aggregate_connector_utils import sample_record


def collect(source=None):
    configured = bool(os.getenv("NEWS_API_KEY"))
    confidence = 78 if configured else 66
    return [sample_record("Public reports on water and food affordability", "public services", "Kenya news/public reports", "news", confidence, "Public reports help confirm whether online signals are becoming policy or service concerns.", "NEWS_API_KEY configured" if configured else "sample public report signal")]
