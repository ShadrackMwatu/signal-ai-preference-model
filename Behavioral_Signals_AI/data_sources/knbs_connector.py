"""KNBS public aggregate connector placeholder.

TODO: connect to official KNBS public datasets when endpoint configuration is available.
"""

from Behavioral_Signals_AI.data_sources._aggregate_connector_utils import sample_record


def collect(source=None):
    return [sample_record("Kenya inflation and household cost indicators", "cost of living", "KNBS", "official_statistics", 88, "Public aggregate statistics can validate affordability and household pressure signals.", "https://www.knbs.or.ke/")]
