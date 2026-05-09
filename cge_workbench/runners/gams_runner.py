"""Optional GAMS runner for the Signal CGE Workbench."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import subprocess
from typing import Any

from .runner_interface import ModelRunResult, RunnerConfig


GAMS_UNAVAILABLE_MESSAGE = (
    "GAMS execution is not available in this environment. "
    "The model can still run Python-based SAM multiplier simulations."
)


def find_gams_executable() -> str | None:
    """Return the path to GAMS if available on PATH."""

    return shutil.which("gams") or shutil.which("gams.exe")


def is_gams_available() -> bool:
    return find_gams_executable() is not None


class GAMSRunner:
    """Run a GAMS-backed Signal CGE model when GAMS is installed."""

    def __init__(self, config: RunnerConfig | None = None) -> None:
        self.config = config or RunnerConfig(model_type="CGE model")

    def run(self, scenario: dict[str, Any]) -> ModelRunResult:
        output_dir = self.config.output_dir
        logs_dir = output_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = logs_dir / f"gams_run_{timestamp}.log"

        executable = find_gams_executable()
        if executable is None:
            log_path.write_text(GAMS_UNAVAILABLE_MESSAGE + "\n", encoding="utf-8")
            return ModelRunResult(
                success=False,
                backend="gams",
                scenario=scenario,
                logs=[GAMS_UNAVAILABLE_MESSAGE],
                artifacts={"log": str(log_path)},
                message=GAMS_UNAVAILABLE_MESSAGE,
            )

        if self.config.model_path is None:
            message = "No GAMS model path configured for Signal CGE execution."
            log_path.write_text(message + "\n", encoding="utf-8")
            return ModelRunResult(False, "gams", scenario, logs=[message], artifacts={"log": str(log_path)}, message=message)

        listing_path = output_dir / f"gams_listing_{timestamp}.lst"
        gdx_path = output_dir / f"gams_output_{timestamp}.gdx"
        command = [
            executable,
            str(self.config.model_path),
            f"lo=2",
            f"o={listing_path}",
            f"gdx={gdx_path}",
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        log_text = "\n".join([completed.stdout, completed.stderr]).strip()
        log_path.write_text(log_text + "\n", encoding="utf-8")
        return ModelRunResult(
            success=completed.returncode == 0,
            backend="gams",
            scenario=scenario,
            logs=[log_text],
            artifacts={"log": str(log_path), "listing": str(listing_path), "gdx": str(gdx_path)},
            message="GAMS run completed." if completed.returncode == 0 else "GAMS run failed; inspect listing and log files.",
        )
