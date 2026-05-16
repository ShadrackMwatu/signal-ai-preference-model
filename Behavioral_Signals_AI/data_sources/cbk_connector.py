"""CBK public macro connector placeholder.

TODO: activate CBK public rates, inflation, exchange-rate, and credit indicators through documented sources.
"""

from Behavioral_Signals_AI.data_sources._aggregate_connector_utils import sample_record


def collect(source=None):
    return [sample_record("Credit and exchange rate pressure", "finance", "CBK", "macro", 84, "Public macro indicators can contextualize credit, liquidity, and price pressure signals.", "https://www.centralbank.go.ke/")]
