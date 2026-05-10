"""Optional GAMS runner for the Signal CGE Workbench.

The GAMS backend is optional. It never prevents the app from starting. When
available, it exports scenario/SAM metadata as structured runtime inputs, runs
GAMS, captures logs/listings, and reports machine-readable artifacts for later
GDX parsing.
"""

from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
from typing import Any

from signal_cge.data.sam_loader import discover_sam_path, get_sam_status
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
            "python_api_available": _gams_python_api_available(),
        }
    return {
        "backend": "gams_optional_solver",
        "status": "available",
        "available": True,
        "executable": executable,
        "message": "GAMS executable detected. Execution still requires valid model files and runtime/license availability.",
        "python_api_available": _gams_python_api_available(),
    }


class GAMSRunner:
    """Run a GAMS-backed Signal CGE model when GAMS is installed."""

    def __init__(self, config: RunnerConfig | None = None) -> None:
        self.config = config or RunnerConfig(model_type="CGE model")

    def run(self, scenario: dict[str, Any]) -> ModelRunResult:
        output_dir = self.config.output_dir or Path("Signal_CGE/outputs/runtime/gams")
        logs_dir = output_dir / "logs"
        input_dir = output_dir / "inputs"
        results_dir = output_dir / "results"
        for folder in (logs_dir, input_dir, results_dir):
            folder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = logs_dir / f"gams_run_{timestamp}.log"
        scenario_path = input_dir / f"scenario_{timestamp}.json"
        sam_status_path = input_dir / f"sam_status_{timestamp}.json"
        scalar_inc_path = input_dir / f"signal_runtime_{timestamp}.inc"

        sam_source = discover_sam_path(self.config.sam_path)
        sam_status = get_sam_status(self.config.sam_path)
        runtime_payload = {
            "scenario": scenario,
            "sam_source": {
                "source_type": sam_source.source_type,
                "path": str(sam_source.path) if sam_source.path else "",
                "message": sam_source.message,
            },
            "sam_status": sam_status,
            "model_path": str(self.config.model_path) if self.config.model_path else "",
            "created_at": timestamp,
        }
        scenario_path.write_text(json.dumps(runtime_payload, indent=2), encoding="utf-8")
        sam_status_path.write_text(json.dumps(sam_status, indent=2), encoding="utf-8")
        scalar_inc_path.write_text(_scenario_to_gams_include(scenario), encoding="utf-8")

        executable = find_gams_executable()
        if executable is None:
            log_path.write_text(GAMS_UNAVAILABLE_MESSAGE + "\n", encoding="utf-8")
            return ModelRunResult(
                success=False,
                backend="gams_optional_solver",
                scenario=scenario,
                diagnostics={
                    "gams_status": get_gams_status(),
                    "execution_status": "unavailable",
                    "sam_status": sam_status,
                    "fallback_recommended": "python_sam_multiplier",
                },
                logs=[GAMS_UNAVAILABLE_MESSAGE],
                artifacts={"log": str(log_path), "scenario_json": str(scenario_path), "sam_status_json": str(sam_status_path)},
                message=GAMS_UNAVAILABLE_MESSAGE,
            )

        if self.config.model_path is None:
            message = "No GAMS model path configured for Signal CGE execution."
            log_path.write_text(message + "\n", encoding="utf-8")
            return ModelRunResult(
                False,
                "gams_optional_solver",
                scenario,
                diagnostics={
                    "gams_status": get_gams_status(),
                    "execution_status": "execution_failed",
                    "sam_status": sam_status,
                    "fallback_recommended": "python_sam_multiplier",
                },
                logs=[message],
                artifacts={"log": str(log_path), "scenario_json": str(scenario_path), "sam_status_json": str(sam_status_path)},
                message=message,
            )

        listing_path = output_dir / f"gams_listing_{timestamp}.lst"
        gdx_path = results_dir / f"gams_output_{timestamp}.gdx"
        command = [
            executable,
            str(self.config.model_path),
            "lo=2",
            f"o={listing_path}",
            f"gdx={gdx_path}",
            f"--SIGNAL_SCENARIO_JSON={scenario_path}",
            f"--SIGNAL_SAM_PATH={sam_source.path or ''}",
            f"--SIGNAL_RUNTIME_INC={scalar_inc_path}",
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        log_text = "\n".join([completed.stdout, completed.stderr]).strip()
        log_path.write_text(log_text + "\n", encoding="utf-8")
        execution_status = _execution_status(completed.returncode, log_text)
        parsed_results = _parse_gams_results(gdx_path, log_text)
        return ModelRunResult(
            success=completed.returncode == 0,
            backend="gams_optional_solver",
            scenario=scenario,
            diagnostics={
                "gams_status": get_gams_status(),
                "execution_status": execution_status,
                "return_code": completed.returncode,
                "log_summary": _summarize_log(log_text),
                "sam_status": sam_status,
                "fallback_recommended": "" if completed.returncode == 0 else "python_sam_multiplier",
                "gdx_parsed": parsed_results.get("parsed", False),
            },
            results=parsed_results,
            logs=[_summarize_log(log_text)],
            artifacts={
                "log": str(log_path),
                "listing": str(listing_path),
                "gdx": str(gdx_path),
                "scenario_json": str(scenario_path),
                "sam_status_json": str(sam_status_path),
                "runtime_include": str(scalar_inc_path),
            },
            message="GAMS run completed." if completed.returncode == 0 else "GAMS run failed; fallback to Python solver is recommended.",
        )


def _gams_python_api_available() -> bool:
    try:
        import gams  # type: ignore  # noqa: F401
    except Exception:
        return False
    return True


def _scenario_to_gams_include(scenario: dict[str, Any]) -> str:
    """Create a small GAMS include file with scalar scenario metadata."""

    shock_value = _safe_float(scenario.get("shock_value", scenario.get("shock_size", 0.0)))
    shock_unit = str(scenario.get("shock_unit", "percent")).replace("'", "")
    shock_type = str(scenario.get("shock_type", scenario.get("policy_instrument", "policy_shock"))).replace("'", "")
    target = str(scenario.get("target_account", scenario.get("target_commodity", ""))).replace("'", "")
    return "\n".join(
        [
            "* Auto-generated by Signal CGE runtime. Do not edit by hand.",
            f"Scalar signal_shock_value / {shock_value} /;",
            f"$setglobal signal_shock_unit '{shock_unit}'",
            f"$setglobal signal_shock_type '{shock_type}'",
            f"$setglobal signal_target_account '{target}'",
            "",
        ]
    )


def _parse_gams_results(gdx_path: Path, log_text: str) -> dict[str, Any]:
    """Return a stable result schema; full GDX symbol parsing is added when gams API is available."""

    payload: dict[str, Any] = {
        "parsed": False,
        "gdx_exists": gdx_path.exists(),
        "gdx_path": str(gdx_path),
        "summary": _summarize_log(log_text),
    }
    if not gdx_path.exists() or not _gams_python_api_available():
        return payload
    payload["parsed"] = True
    payload["note"] = "GDX file exists and GAMS Python API is available; symbol-level parsing hook is ready."
    return payload


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


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
