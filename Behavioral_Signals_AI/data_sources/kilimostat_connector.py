"""KilimoSTAT agriculture connector placeholder.

TODO: activate public agriculture and food-system APIs when configured.
"""

from Behavioral_Signals_AI.data_sources._aggregate_connector_utils import sample_record


def collect(source=None):
    return [sample_record("Fertilizer and staple crop input pressure", "food and agriculture", "KilimoSTAT", "agriculture", 82, "Agriculture indicators can validate food supply, input-cost, and rural livelihood stress signals.", "https://www.kilimo.go.ke/")]
