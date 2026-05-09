"""Run generated GAMS models when a local GAMS installation is available."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .lst_parser import parse_lst


GAMS_UNAVAILABLE_MESSAGE = "GAMS backend unavailable; using experimental Python backend or validation-only mode."


def is_gams_available() -> bool:
    return shutil.which("gams") is not None


def run_gams(gms_path: str | Path, workdir: str | Path = "outputs") -> dict[str, object]:
    """Run GAMS without pretending success when GAMS is absent."""

    if not is_gams_available():
        return {
            "status": "unavailable",
            "message": GAMS_UNAVAILABLE_MESSAGE,
            "returncode": None,
            "lst": None,
        }
    gms = Path(gms_path)
    destination = Path(workdir)
    destination.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        ["gams", str(gms)],
        cwd=destination,
        capture_output=True,
        text=True,
        check=False,
    )
    lst_path = destination / f"{gms.stem}.lst"
    return {
        "status": "ok" if process.returncode == 0 else "failed",
        "message": process.stdout[-1000:] or process.stderr[-1000:],
        "returncode": process.returncode,
        "lst": parse_lst(lst_path),
    }
