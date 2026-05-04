import unittest
from pathlib import Path

from cge_core.sam import balance_check, export_balance_check, is_balanced, load_sam


class SAMBalanceTests(unittest.TestCase):
    def test_sample_sam_balance_checks_work(self) -> None:
        matrix = load_sam("data/sample_sam.csv")
        check = balance_check(matrix)

        self.assertTrue(is_balanced(matrix))
        self.assertEqual(set(check["account"]), set(matrix.index))
        self.assertTrue((check["percentage_imbalance"].abs() <= 0.01).all())

    def test_balance_check_exports_markdown_and_xlsx(self) -> None:
        matrix = load_sam("data/sample_sam.csv")
        paths = export_balance_check(balance_check(matrix), "tests/_tmp/sam_balance")

        self.assertTrue(Path(paths["markdown"]).exists())
        self.assertTrue(Path(paths["excel"]).exists())
        self.assertGreater(Path(paths["excel"]).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
