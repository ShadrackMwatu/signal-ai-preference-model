"""Compatibility wrapper for $module.

cge_workbench is retained during the Signal CGE package transition.
Use $module for new code.
"""

from importlib import import_module
import sys

_module = import_module("signal_cge.model_core.market_clearing_block")
sys.modules[__name__] = _module
