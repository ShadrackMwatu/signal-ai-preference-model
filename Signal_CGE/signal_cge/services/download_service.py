"""Download/export service for Signal CGE."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any



def export_results(payload: dict[str, Any], output_root: str = "outputs/signal_cge_service") -> dict[str, str]:
    """Export canonical Signal CGE outputs."""

    output_dir = Path(output_root) / datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "signal_cge_results.json"
    md_path = output_dir / "signal_cge_summary.md"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(_markdown_summary(payload), encoding="utf-8")

    return {
        "json": str(json_path),
        "markdown": str(md_path),
    }



def _markdown_summary(payload: dict[str, Any]) -> str:
    return "\n\n".join(
        [
            "# Signal CGE Export",
            "## Backend\n" + str(payload.get("backend", "unknown")),
            "## Interpretation\n```json\n" + json.dumps(payload.get("interpretation", {}), indent=2) + "\n```",
            "## Diagnostics\n```json\n" + json.dumps(payload.get("diagnostics", {}), indent=2) + "\n```",
        ]
    )
