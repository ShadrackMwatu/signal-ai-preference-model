"""API routes for SML parsing, validation, and execution."""

from __future__ import annotations

from fastapi import APIRouter

from signal_execution.runner import SignalRunner
from signal_modeling_language.parser import parse_sml_text
from signal_modeling_language.validator import validate_model

from .schemas import ParseResponse, SMLRunRequest, SMLTextRequest, ValidationResponse


router = APIRouter()


@router.post("/models/parse", response_model=ParseResponse)
def parse_model(request: SMLTextRequest) -> dict[str, object]:
    model = parse_sml_text(request.sml_text)
    return {
        "sets": model.sets,
        "parameters": model.parameters,
        "variables": [{"name": symbol.name, "indices": list(symbol.indices)} for symbol in model.variables],
        "equations": [{"name": symbol.name, "indices": list(symbol.indices)} for symbol in model.equations],
        "closure": model.closure,
        "shocks": [
            {"name": shock.name, "target": shock.target, "operator": shock.operator, "value": shock.value}
            for shock in model.shocks
        ],
        "solve": {"model": model.solve.model, "backend": model.solve.backend, "solver": model.solve.solver},
        "output": {
            "gdx": model.output.gdx,
            "excel": model.output.excel,
            "report": model.output.report,
            "gams": model.output.gams,
        },
    }


@router.post("/models/validate", response_model=ValidationResponse)
def validate_sml_model(request: SMLTextRequest) -> dict[str, object]:
    validation = validate_model(parse_sml_text(request.sml_text))
    return {"valid": validation.valid, "errors": validation.errors, "warnings": validation.warnings}


@router.post("/models/run")
def run_model(request: SMLRunRequest) -> dict[str, object]:
    runner = SignalRunner()
    return runner.run(request.sml_path, sml_text=request.sml_text)
