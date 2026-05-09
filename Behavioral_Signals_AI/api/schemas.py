"""FastAPI request and response schemas for Signal CGE routes."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SMLTextRequest(BaseModel):
    sml_text: str = Field(..., description="Signal Modelling Language text")


class SMLRunRequest(BaseModel):
    sml_text: str | None = Field(None, description="Inline SML text. Uses the default example when omitted.")
    sml_path: str | None = Field(None, description="Optional path to a local SML file.")


class ParseResponse(BaseModel):
    sets: dict[str, list[str]]
    parameters: dict[str, object]
    variables: list[dict[str, object]]
    equations: list[dict[str, object]]
    closure: dict[str, str]
    shocks: list[dict[str, object]]
    solve: dict[str, str]
    output: dict[str, str | None]


class ValidationResponse(BaseModel):
    valid: bool
    errors: list[str]
    warnings: list[str]


class LearningFeedbackRequest(BaseModel):
    run_id: str
    issue_type: str
    source: str = "user_correction"
    original_value: str
    corrected_value: str = ""
    lesson_learned: str
    confidence_score: float = 0.75


class LearningApplyRequest(BaseModel):
    version_id: str | None = None
    mode: str = "recommend"


class LearningRollbackRequest(BaseModel):
    version_id: str
