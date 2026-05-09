import unittest
from pathlib import Path

import pandas as pd

from app import cge_model
from src.cge.dsl import parse_scenario, scenario_from_behavioral_signal
from src.cge.framework import DEFAULT_SCENARIO, run_policy_scenario
from src.cge.gams import export_gams_model
from src.cge.sam import calibrate_sam, load_sam, sam_matrix, validate_sam
from src.cge.simulation import run_cge_simulation


SAMPLE_SAM = Path("Behavioral_Signals_AI/data/sample_sam.csv")


class CGEFrameworkTests(unittest.TestCase):
    def test_sample_sam_loads_as_balanced_square_matrix(self) -> None:
        sam = load_sam(SAMPLE_SAM)
        matrix = sam_matrix(sam)
        calibration = calibrate_sam(sam)

        self.assertEqual(set(matrix.index), set(matrix.columns))
        self.assertGreater(calibration["baseline_gdp"], 0)
        self.assertIn("agriculture", calibration["sectors"])
        self.assertIn("SAM account balances are within the 1% tolerance.", run_policy_scenario()["diagnostics"])

    def test_sam_privacy_validation_rejects_pii_columns(self) -> None:
        pii_sam = pd.DataFrame(
            {
                "row_account": ["agriculture"],
                "column_account": ["agriculture"],
                "value": [1],
                "email": ["person@example.com"],
            }
        )

        with self.assertRaises(ValueError):
            validate_sam(pii_sam)

    def test_policy_scenario_language_parses_shocks_and_metadata(self) -> None:
        scenario = parse_scenario(DEFAULT_SCENARIO)

        self.assertEqual(scenario.closure, "savings_driven")
        self.assertEqual(scenario.numeraire, "consumer_price_index")
        self.assertEqual(len(scenario.shocks), 3)
        self.assertEqual(scenario.shocks[0].shock_type, "demand")

    def test_cge_simulation_outputs_policy_metrics(self) -> None:
        sam = load_sam(SAMPLE_SAM)
        scenario = parse_scenario(DEFAULT_SCENARIO)
        result = run_cge_simulation(sam, scenario)

        self.assertGreater(result.simulated_gdp, 0)
        self.assertTrue(result.sector_impacts)
        self.assertIsInstance(result.gdp_change_percent, float)
        self.assertIsInstance(result.household_welfare_change_percent, float)

    def test_gams_export_contains_core_symbols(self) -> None:
        sam = load_sam(SAMPLE_SAM)
        scenario = parse_scenario(DEFAULT_SCENARIO)
        gams_text = export_gams_model(sam, scenario)

        self.assertIn("Parameter SAM(i,j)", gams_text)
        self.assertIn("Model signal_cge", gams_text)
        self.assertIn("shock_1_demand_agriculture", gams_text)

    def test_behavioral_signal_can_become_cge_scenario(self) -> None:
        scenario = scenario_from_behavioral_signal("Nairobi", "agri_inputs", "High", 88)

        self.assertEqual(scenario.shocks[0].target, "agriculture")
        self.assertGreater(scenario.shocks[0].change_percent, 0)

    def test_gradio_cge_wrapper_returns_privacy_safe_outputs(self) -> None:
        summary, policy_json, gams_preview = cge_model(DEFAULT_SCENARIO)
        combined = f"{summary}\n{policy_json}\n{gams_preview}".lower()

        self.assertIn("gdp change", summary.lower())
        self.assertIn("priority_sectors", policy_json)
        self.assertIn("parameter sam", gams_preview.lower())
        self.assertNotIn("email", combined)
        self.assertNotIn("phone", combined)
        self.assertNotIn("username", combined)
        self.assertNotIn("user_id", combined)


if __name__ == "__main__":
    unittest.main()
