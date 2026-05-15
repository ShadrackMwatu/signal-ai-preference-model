"""Kenya-aware aggregate/public data source connectors."""

from .fallback_sample_source import collect as collect_sample_signals

__all__ = ["collect_sample_signals"]