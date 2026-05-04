"""Result retrieval routes for Signal CGE runs."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from signal_execution.runner import RUN_STORE


router = APIRouter()


@router.get("/results/{run_id}")
def get_result(run_id: str) -> dict[str, object]:
    if run_id not in RUN_STORE:
        raise HTTPException(status_code=404, detail=f"Result not found: {run_id}")
    return RUN_STORE[run_id]


@router.get("/results/{run_id}/report", response_class=PlainTextResponse)
def get_report(run_id: str) -> str:
    if run_id not in RUN_STORE:
        raise HTTPException(status_code=404, detail=f"Result not found: {run_id}")
    report_path = Path(str(RUN_STORE[run_id].get("report_path", "")))
    if not report_path.exists():
        raise HTTPException(status_code=404, detail=f"Report not found for run: {run_id}")
    return report_path.read_text(encoding="utf-8")
