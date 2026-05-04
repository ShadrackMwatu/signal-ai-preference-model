import unittest

from solvers.fixed_point_solver import FixedPointSolver
from solvers.gams_solver import GamsSolver
from solvers.python_nlp_solver import PythonNLPSolver
from solvers.solver_registry import available_solvers, get_solver


class SolverRegistryTests(unittest.TestCase):
    def test_registry_selects_backends(self) -> None:
        self.assertIsInstance(get_solver("gams"), GamsSolver)
        self.assertIsInstance(get_solver("python_nlp"), PythonNLPSolver)
        self.assertIsInstance(get_solver("fixed_point"), FixedPointSolver)
        self.assertIn("gams", available_solvers())

    def test_unknown_backend_fails_clearly(self) -> None:
        with self.assertRaises(ValueError):
            get_solver("unknown")


if __name__ == "__main__":
    unittest.main()
