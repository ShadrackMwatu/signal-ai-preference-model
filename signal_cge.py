"""Compatibility wrapper for the Signal CGE product-domain package.

The canonical implementation now lives under `Signal_CGE/signal_cge/`.
This root module keeps imports such as `signal_cge.knowledge` working during
the repository transition.
"""

from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parent / "Signal_CGE" / "signal_cge"
__path__ = [str(_PACKAGE_ROOT)]

from Signal_CGE.signal_cge.model_registry import get_model_registry  # noqa: E402
from Signal_CGE.signal_cge.workbench import run_chat_scenario  # noqa: E402

__all__ = ["get_model_registry", "run_chat_scenario"]
