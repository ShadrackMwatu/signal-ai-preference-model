"""Best-effort GDX output reader."""

from __future__ import annotations

from pathlib import Path


def read_gdx(path: str | Path) -> dict[str, object]:
    """Return metadata for GDX files; full parsing requires optional GAMS tools."""

    source = Path(path)
    if not source.exists():
        return {"available": False, "message": f"GDX file not found: {source}"}
    return {
        "available": True,
        "path": str(source),
        "size_bytes": source.stat().st_size,
        "message": "GDX file exists. Install GAMS Python APIs for symbol-level parsing.",
    }
