"""Compatibility wrapper for `Signal_CGE/signal_modeling_language`."""

from pathlib import Path

__path__ = [
    str(Path(__file__).resolve().parents[1] / "Signal_CGE" / "signal_modeling_language")
]
