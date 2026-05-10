"""Optional GAMS runner for the Signal CGE Workbench."""

from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import shutil
import subprocess
from typing import Any

from .runner_interface import ModelRunResult, RunnerConfig


GAMS_UNAVAILABLE_MESSAGE = (
    "GAMS solver backend is configured but not available in this runtime. "
    "Signal is using the open-source/Python backend."
)


def find_gams_executable() -> str | None:
    """Return the path to GAMS from GAMS_PATH or PATH, if available."""

    env_path = os.environ.get("GAMS_PATH", "").strip()
    if env_path:
        candidate = Path(env_path)
        if candidate.is_dir():
            for name in ("gams.exe", "gams"):
                executable = candidate / name
                if executable.exists():
                    return str(executable)
        if candidate.exists():
            return str(candidate)
    return shutil.which("gams") or shutil.which("gams.exe")


def is_gams_available() -> bool:
    return find_gams_executable() is not None


def get_gams_status() -> dict[str, Any]:
    """Return a non-throwing status payload for the optional GAMS backend."""

    executable = find_gams_executable()
    if not executable:
        return {
            "backend": "gams_optional_solver",
            "status": "unavailable",
            "available": False,
            "executable": "",
            "message": GAMS_UNAVAILABLE_MESSAGE,
        }
    return {
        "backend": "gams_optional_solver",
        "status": "available",
        "available": True,
        "executable": executable,
        "message": "GAMS executable detected. Execution still requires valid model files and runtime/license availability.",
    }


class GAMSRunner:
    """Run a GAMS-backed Signal CGE model when GAMS is installed."""

    def __init__(self, config: RunnerConfig | None = None) -> None:
        self.config = config or RunnerConfig(model_type="CGE model")

    def run(self, scenario: dict[str, Any]) -> ModelRunResult:
        output_dir = self.config.output_dir or Path("Signal_CGE/outputs/runtime/gams")
        logs_dir = output_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = logs_dir / f"gams_run_{timestamp}.log"

        executable = find_gams_executable()
        if executable is None:
            log_path.write_text(GAMS_UNAVAILABLE_MESSAGE + "\n", encoding="utf-8")
            return ModelRunResult(
                success=False,
                backend="gams_optional_solver",
                scenario=scenario,
                diagnostics={"gams_status": get_gams_status(), "execution_status": "unavailable"},
                logs=[GAMS_UNAVAILABLE_MESSAGE],
                artifacts={"log": str(log_path)},
                message=GAMS_UNAVAILABLE_MESSAGE,
            )

        if self.config.model_path is None:
            message = "No GAMS model path configured for Signal CGE execution."
            log_path.write_text(message + "\n", encoding="utf-8")
            return ModelRunResult(
                False,
                "gams_optional_solver",
                scenario,
                diagnostics={"gams_status": get_gams_status(), "execution_status": "execution_failed"},
                logs=[message],
                artifacts={"log": str(log_path)},
                message=message,
            )

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
        execution_status = _execution_status(completed.returncode, log_text)
        return ModelRunResult(
            success=completed.returncode == 0,
            backend="gams_optional_solver",
            scenario=scenario,
            diagnostics={
                "gams_status": get_gams_status(),
                "execution_status": execution_status,
                "return_code": completed.returncode,
                "log_summary": _summarize_log(log_text),
            },
            logs=[_summarize_log(log_text)],
            artifacts={"log": str(log_path), "listing": str(listing_path), "gdx": str(gdx_path)},
            message="GAMS run completed." if completed.returncode == 0 else "GAMS run failed; inspect listing and log files.",
        )


def _execution_status(return_code: int, log_text: str) -> str:
    if return_code == 0:
        return "available"
    lowered = log_text.lower()
    if "license" in lowered or "licence" in lowered:
        return "installed_but_unlicensed"
    return "execution_failed"


def _summarize_log(log_text: str, max_lines: int = 12) -> str:
    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    return "\n".join(lines[-max_lines:]) if lines else "No GAMS log output captured."
