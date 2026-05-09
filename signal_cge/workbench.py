"""High-level chat-driven orchestration for Signal CGE Workbench."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from signal_cge.diagnostics.calibration_checks import validate_calibration, validate_shock
from signal_cge.diagnostics.closure_checks import validate_closure
from signal_cge.reporting.policy_brief_generator import generate_policy_brief
from signal_cge.reporting.result_explainer import explain_results
from signal_cge.scenarios.scenario_schema import parse_scenario_prompt
from signal_cge.solvers.gams_runner import GAMSRunner
from signal_cge.solvers.python_runner import PythonSAMRunner
from signal_cge.solvers.runner_interface import RunnerConfig


def run_chat_scenario(
    prompt: str,
    model_type: str = "SAM multiplier",
    shock_size: float | None = None,
    target_account: str | None = None,
    sam_path: str | None = None,
) -> dict[str, Any]:
    scenario = parse_scenario_prompt(prompt).to_dict()
    if shock_size is not None:
        scenario["shock_value"] = float(shock_size)
    if target_account:
        scenario["target_accounts"] = [target_account]

    output_dir = Path("cge_workbench/outputs") / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    config = RunnerConfig(model_type=model_type, output_dir=output_dir, sam_path=Path(sam_path) if sam_path else None)

    preflight = {
        "closure": validate_closure(scenario),
        "calibration": validate_calibration(None),
        "shock": validate_shock(scenario),
    }
    if model_type == "CGE model":
        run_result = GAMSRunner(config).run(scenario)
        if not run_result.success:
            fallback = PythonSAMRunner(config).run(scenario)
            fallback.logs = run_result.logs + fallback.logs
            fallback.message = run_result.message + " Fallback executed with Python SAM multiplier."
            run_result = fallback
    elif model_type == "Recursive dynamic model - placeholder":
        run_result = PythonSAMRunner(config).run(scenario)
        run_result.message = "Recursive dynamic model is a placeholder; Python SAM multiplier fallback was executed."
    else:
        run_result = PythonSAMRunner(config).run(scenario)

    result_dict = {
        "success": run_result.success,
        "backend": run_result.backend,
        "scenario": run_result.scenario,
        "diagnostics": {"preflight": preflight, **run_result.diagnostics},
        "results": run_result.results,
        "logs": run_result.logs,
        "artifacts": run_result.artifacts,
        "message": run_result.message,
    }
    explanation = explain_results(result_dict)
    brief = generate_policy_brief(result_dict)
    brief_path = output_dir / "policy_brief.md"
    brief_path.write_text(brief, encoding="utf-8")
    result_dict["explanation"] = explanation
    result_dict["policy_brief"] = brief
    result_dict["artifacts"]["policy_brief"] = str(brief_path)
    return result_dict
