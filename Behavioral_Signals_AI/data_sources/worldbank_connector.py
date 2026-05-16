"""World Bank Open Data connector placeholder.

TODO: activate selected World Bank country indicators through public API endpoints.
"""

from Behavioral_Signals_AI.data_sources._aggregate_connector_utils import sample_record


def collect(source=None):
    return [sample_record("Kenya macro development indicators", "trade and business", "World Bank Open Data", "macro", 82, "Global public indicators can contextualize national demand and investment opportunity patterns.", "https://data.worldbank.org/country/kenya")]
