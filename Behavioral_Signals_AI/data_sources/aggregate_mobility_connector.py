"""Aggregate mobility/place intelligence connector placeholder.

This connector never tracks people, routes, devices, or private location histories.
TODO: activate only with authorized aggregate place/category indicators.
"""

import os
from Behavioral_Signals_AI.data_sources._aggregate_connector_utils import sample_record


def collect(source=None):
    configured = bool(os.getenv("GOOGLE_MAPS_API_KEY"))
    confidence = 72 if configured else 55
    return [sample_record("Retail and market place activity pressure", "trade and business", "aggregate mobility placeholder", "mobility_aggregate", confidence, "Aggregate place-category activity can reinforce retail demand and service pressure signals without surveillance.", "authorized aggregate place intelligence" if configured else "sample aggregate place signal")]
