"""Scenario helper routes."""

from __future__ import annotations

from fastapi import APIRouter

from signal_execution.runner import SignalRunner


router = APIRouter()


@router.get("/scenarios/example")
def example_scenario() -> dict[str, str]:
    text = SignalRunner().config.resolve("signal_modeling_language/examples/basic_cge.sml").read_text(encoding="utf-8")
    return {"sml_text": text}
