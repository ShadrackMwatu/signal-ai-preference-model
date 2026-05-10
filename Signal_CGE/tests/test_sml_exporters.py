from __future__ import annotations

import unittest

from sml_workbench.exporters.gams_exporter import export_to_gams
from sml_workbench.exporters.pyomo_exporter import export_to_pyomo
from sml_workbench.parser.sml_parser import parse_sml


SML_TEXT = """SETS:
  sectors = [agriculture]
PARAMETERS:
  SAM = "Behavioral_Signals_AI/data/sample_sam.csv"
VARIABLES:
  output[sectors]
EQUATIONS:
  market_clearing[sectors]
SHOCKS:
  productivity_growth = productivity[agriculture] + 0.05
SOLVE:
  model = kenya_cge
  backend = gams
  solver = path
"""


class SMLExporterTests(unittest.TestCase):
    def test_gams_exporter_returns_model_text(self) -> None:
        parsed = parse_sml(SML_TEXT)
        exported = export_to_gams(parsed)

        self.assertIn("MODEL kenya_cge", exported)
        self.assertIn("VARIABLES", exported)

    def test_pyomo_exporter_returns_model_text(self) -> None:
        parsed = parse_sml(SML_TEXT)
        exported = export_to_pyomo(parsed)

        self.assertIn("ConcreteModel", exported)
        self.assertIn("Constraint", exported)


if __name__ == "__main__":
    unittest.main()
