import unittest
from pathlib import Path

from signal_modeling_language.parser import SMLParseError, parse_sml_file, parse_sml_text
from signal_modeling_language.validator import validate_model


EXAMPLE = Path("signal_modeling_language/examples/basic_cge.sml")


class SMLParserTests(unittest.TestCase):
    def test_basic_cge_sml_parses_correctly(self) -> None:
        model = parse_sml_file(EXAMPLE)

        self.assertIn("sectors", model.sets)
        self.assertEqual(model.parameters["sam"], "data/sample_sam.csv")
        self.assertEqual(model.solve.backend, "gams")
        self.assertEqual(model.solve.solver, "path")
        self.assertTrue(any(variable.name == "output" for variable in model.variables))

    def test_invalid_sml_fails_clearly(self) -> None:
        with self.assertRaises(SMLParseError):
            parse_sml_text("SETS:\n  sectors agriculture manufacturing")

    def test_unknown_index_fails_validation(self) -> None:
        model = parse_sml_text(
            """SETS:
  sectors = [agriculture]
PARAMETERS:
  SAM = "data/sample_sam.csv"
VARIABLES:
  output[unknown_set]
EQUATIONS:
  market_clearing[sectors]
SOLVE:
  model = bad_model
  backend = gams
  solver = path
"""
        )
        validation = validate_model(model)

        self.assertFalse(validation.valid)
        self.assertIn("unknown_set", " ".join(validation.errors))


if __name__ == "__main__":
    unittest.main()
