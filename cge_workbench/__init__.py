"""Compatibility wrapper for `Signal_CGE/cge_workbench`."""

from pathlib import Path

__path__ = [str(Path(__file__).resolve().parents[1] / "Signal_CGE" / "cge_workbench")]

from Signal_CGE.cge_workbench import *  # noqa: F401,F403,E402
