from __future__ import annotations

import unittest

from sml_workbench.validators.sml_validator import validate_sml


class SMLValidatorTests(unittest.TestCase):
    def test_validator_reports_missing_required_sections(self) -> None:
        result = validate_sml(
            """SETS:
  sectors = [agriculture]
PARAMETERS:
  SAM = "data/sample_sam.csv"
VARIABLES:
  output[sectors]
"""
        )

        self.assertFalse(result["valid"])
        self.assertTrue(any("Missing required section" in error for error in result["errors"]))

    def test_validator_returns_clear_success_message(self) -> None:
        result = validate_sml(
            """SETS:
  sectors = [agriculture]
PARAMETERS:
  SAM = "data/sample_sam.csv"
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
        )

        self.assertTrue(result["valid"])
        self.assertEqual(result["message"], "SML validation passed.")


if __name__ == "__main__":
    unittest.main()
