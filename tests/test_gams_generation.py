import unittest

from backends.gams.gams_generator import generate_gams_code
from cge_core.calibration import calibrate_from_sam
from cge_core.sam import load_sam
from signal_modeling_language.parser import parse_sml_file


class GAMSGenerationTests(unittest.TestCase):
    def test_gams_code_is_generated_from_sml(self) -> None:
        model = parse_sml_file("signal_modeling_language/examples/basic_cge.sml")
        calibration = calibrate_from_sam(load_sam("data/sample_sam.csv"))
        gams_code = generate_gams_code(model, calibration)

        self.assertIn("Sets", gams_code)
        self.assertIn("Parameters", gams_code)
        self.assertIn("Variables output", gams_code)
        self.assertIn("Equations market_clearing", gams_code)
        self.assertIn("Model kenya_cge", gams_code)
        self.assertIn('execute_unload "outputs/results.gdx"', gams_code)


if __name__ == "__main__":
    unittest.main()
