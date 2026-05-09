"""Learning API routes for Signal's adaptive CGE layer."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from signal_learning.adaptation_engine import propose_adaptations
from signal_learning.feedback_collector import user_feedback
from signal_learning.implementation_engine import implement_adaptation, rollback_adaptation
from signal_learning.learning_store import LearningStore
from signal_learning.memory_schema import AdaptationProposal
from signal_learning.pattern_extractor import recurring_issue_summary

from .schemas import LearningApplyRequest, LearningFeedbackRequest, LearningRollbackRequest


router = APIRouter()


@router.post("/learning/feedback")
def add_learning_feedback(request: LearningFeedbackRequest) -> dict[str, object]:
    store = LearningStore()
    feedback = user_feedback(
        run_id=request.run_id,
        issue_type=request.issue_type,
        original_value=request.original_value,
        corrected_value=request.corrected_value,
        lesson_learned=request.lesson_learned,
        confidence_score=request.confidence_score,
        source=request.source,
    )
    store.add_feedback(feedback)
    return {"status": "recorded", "feedback": feedback.to_dict()}


@router.get("/learning/report/{run_id}", response_class=PlainTextResponse)
def get_learning_report(run_id: str) -> str:
    data = LearningStore().load()
    for report in reversed(data.get("reports", [])):
        if report.get("run_id") == run_id:
            path = Path(str(report.get("report_path", "")))
            if path.exists():
                return path.read_text(encoding="utf-8")
            return str(report.get("summary", {}))
    raise HTTPException(status_code=404, detail=f"Learning report not found: {run_id}")


@router.get("/learning/lessons")
def get_learning_lessons() -> dict[str, object]:
    store = LearningStore()
    data = store.load()
    patterns = propose_adaptations(data)
    return {
        "lessons": store.lessons(),
        "recurring_issues": recurring_issue_summary(data),
        "recommended_fixes": [proposal.to_dict() for proposal in patterns],
    }


@router.post("/learning/apply")
def apply_learning(request: LearningApplyRequest) -> dict[str, object]:
    store = LearningStore()
    data = store.load()
    proposals = [_proposal_from_dict(item) for item in data.get("adaptations", [])]
    if not proposals:
        proposals = propose_adaptations(data)
    if request.version_id:
        proposals = [proposal for proposal in proposals if proposal.version_id == request.version_id]
    if not proposals:
        raise HTTPException(status_code=404, detail="No matching learning adaptation found")
    result = implement_adaptation(proposals[-1], mode=request.mode)  # type: ignore[arg-type]
    store.add_implementation(result)
    return result.to_dict()


@router.post("/learning/rollback")
def rollback_learning(request: LearningRollbackRequest) -> dict[str, object]:
    result = rollback_adaptation(request.version_id)
    LearningStore().add_implementation(result)
    return result.to_dict()


def _proposal_from_dict(values: dict[str, object]) -> AdaptationProposal:
    return AdaptationProposal(
        version_id=str(values["version_id"]),
        change_summary=str(values["change_summary"]),
        reason_for_change=str(values["reason_for_change"]),
        affected_templates_or_rules=list(values.get("affected_templates_or_rules", [])),
        confidence_score=float(values.get("confidence_score", 0.0)),
        risk_level=str(values.get("risk_level", "high")),  # type: ignore[arg-type]
        recommended_mode=str(values.get("recommended_mode", "recommend")),  # type: ignore[arg-type]
        evidence_run_ids=list(values.get("evidence_run_ids", [])),
        rollback_instructions=str(values.get("rollback_instructions", "")),
    )
