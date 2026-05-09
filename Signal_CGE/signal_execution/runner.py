"""Signal execution environment for SML CGE models."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from backends.gams.gams_generator import generate_gams_code
from backends.gams.gams_runner import GAMS_UNAVAILABLE_MESSAGE
from cge_core.calibration import calibrate_from_sam
from cge_core.equations import equation_inventory
from cge_core.results import summarize_results
from cge_core.sam import balance_check, export_balance_check, load_sam
from cge_core.shocks import aggregate_shock_size, shock_table
from learning_memory.memory import capture_run_memory
from policy_intelligence.report_generator import generate_policy_report
from signal_learning.workflow import run_learning_cycle
from signal_modeling_language.parser import parse_sml_file, parse_sml_text
from signal_modeling_language.schema import SMLModel
from signal_modeling_language.validator import validate_model
from solvers.solver_registry import get_solver

from .config import ExecutionConfig
from .diagnostics import build_diagnostics
from .logger import write_log


RUN_STORE: dict[str, dict[str, Any]] = {}


class SignalRunner:
    """Read, validate, translate, execute, and report SML models."""

    def __init__(self, config: ExecutionConfig | None = None) -> None:
        self.config = config or ExecutionConfig(project_root=Path("."))

    def run(
        self,
        sml_source: str | Path | None = None,
        *,
        sml_text: str | None = None,
        sam_override: str | Path | None = None,
    ) -> dict[str, Any]:
        model = self._read_model(sml_source, sml_text)
        validation = validate_model(model)
        validation.raise_for_errors()

        run_id = uuid.uuid4().hex[:12]
        run_dir = self.config.output_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        write_log(run_dir, f"Starting Signal CGE run {run_id}")

        sam_path = self._resolve_sam_path(model, sam_override)
        sam_matrix = load_sam(sam_path)
        diagnostics = build_diagnostics(model, sam_matrix, tolerance=self.config.balance_tolerance)
        balance_paths = export_balance_check(balance_check(sam_matrix), run_dir)
        calibration = calibrate_from_sam(sam_matrix)
        gams_code = generate_gams_code(model, calibration)
        gms_path = run_dir / f"{model.solve.model}.gms"
        gms_path.write_text(gams_code, encoding="utf-8")

        solver = get_solver(model.solve.backend)
        solver_result = solver.solve(
            model,
            {
                "calibration": calibration,
                "shock_table": shock_table(model),
                "shock_size": aggregate_shock_size(model),
            },
            {"gms_path": str(gms_path), "workdir": str(run_dir), "solver": model.solve.solver},
        )
        message = str(solver_result.get("message", ""))
        status = str(solver_result.get("status", "ok"))
        backend = str(solver_result.get("backend", model.solve.backend))
        result: dict[str, Any] = {
            "run_id": run_id,
            "status": status,
            "backend": backend,
            "requested_backend": model.solve.backend,
            "message": message,
            "model_name": model.solve.model,
            "gams_message": GAMS_UNAVAILABLE_MESSAGE if GAMS_UNAVAILABLE_MESSAGE in message else "",
            "validation": diagnostics,
            "closure_rules": model.closure,
            "sam_path": str(sam_path),
            "balance_check_paths": balance_paths,
            "calibration": calibration,
            "equations": equation_inventory(model),
            "shocks": shock_table(model),
            "gams_file": str(gms_path),
            "solver_result": solver_result,
            "metrics": solver_result.get("metrics", {}),
            "learning_mode": self.config.learning_mode,
        }
        report_path = self._report_path(model, run_dir)
        result["report_path"] = generate_policy_report(result, report_path)
        result["summary"] = summarize_results(result)
        result["learning_memory"] = capture_run_memory(result, self.config.memory_path)
        result["signal_learning"] = self._learn_from_result(result)
        RUN_STORE[run_id] = result
        write_log(run_dir, f"Completed Signal CGE run {run_id} with status {status}")
        return result

    def validate(self, sml_text: str) -> dict[str, Any]:
        model = parse_sml_text(sml_text)
        validation = validate_model(model)
        return {"valid": validation.valid, "errors": validation.errors, "warnings": validation.warnings}

    def parse(self, sml_text: str) -> SMLModel:
        return parse_sml_text(sml_text)

    def _read_model(self, sml_source: str | Path | None, sml_text: str | None) -> SMLModel:
        if sml_text:
            return parse_sml_text(sml_text)
        source = Path(sml_source or self.config.default_sml_path)
        return parse_sml_file(source)

    def _resolve_sam_path(self, model: SMLModel, sam_override: str | Path | None = None) -> Path:
        if sam_override is not None:
            candidate = Path(sam_override)
            if candidate.exists():
                return candidate
            raise FileNotFoundError(f"Uploaded SAM file not found: {candidate}")
        sam_value = str(model.parameters.get("sam", "data/sample_sam.csv"))
        candidate = self.config.resolve(sam_value)
        if candidate.exists():
            return candidate
        fallback = self.config.resolve("data/sample_sam.csv")
        if fallback.exists():
            return fallback
        raise FileNotFoundError(f"SAM file not found: {candidate}")

    def _report_path(self, model: SMLModel, run_dir: Path) -> Path:
        requested = model.output.report
        if requested:
            return run_dir / Path(requested).name
        return run_dir / "policy_report.md"

    def _learn_from_result(self, result: dict[str, Any]) -> dict[str, Any]:
        return run_learning_cycle(
            result,
            store_path=self.config.learning_store_path,
            output_dir=self.config.output_dir,
            version_root=self.config.learning_version_root,
            mode=self.config.learning_mode,
        )
