"""Downloadable report payload builders for Signal CGE."""

from __future__ import annotations

import json
from typing import Any


def build_downloadable_report(payload: dict[str, Any]) -> str:
    return "\n\n".join(
        [
            "# Signal CGE Results Report",
            "## Result Type\n" + str(payload.get("result_type", "prototype_directional_indicator")),
            "## Results\n```json\n" + json.dumps(payload.get("results", {}), indent=2) + "\n```",
            "## Model Status\n```json\n" + json.dumps(payload.get("full_cge_status", {}), indent=2) + "\n```",
        ]
    )
