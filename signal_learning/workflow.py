"""Explicit Signal learning cycle.

Observe -> Diagnose -> Store -> Recommend -> Validate -> Implement -> Re-test -> Remember
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .adaptation_engine import generate_learning_report, propose_adaptations
from .feedback_collector import build_run_snapshot, collect_run_feedback
from .implementation_engine import implement_adaptation
from .learning_store import LearningStore
from .memory_schema import AdaptationProposal, ImplementationResult, LearningMode
from .pattern_extractor import recurring_issue_summary


LEARNING_STAGES = (
    "observe",
    "diagnose",
    "store",
    "recommend",
    "validate",
    "implement",
    "retest",
    "remember",
)


def run_learning_cycle(
    run_result: dict[str, Any],
    *,
    store_path: str | Path,
    output_dir: str | Path,
    version_root: str | Path,
    mode: LearningMode = "recommend",
) -> dict[str, Any]:
    """Run the full learning cycle for a completed model run."""

    store = LearningStore(store_path)

    observed = observe(run_result)
    diagnostic = diagnose(observed, store.load())
    store_result = store_observations(store, observed)
    recommendations = recommend(store.load(), version_root)
    validation = validate_recommendations(recommendations, mode)
    implementation_results = implement(recommendations, validation, mode, version_root)
    retest_result = retest(implementation_results, validation)
    remember_result = remember(
        store,
        run_result,
        observed,
        recommendations,
        implementation_results,
        output_dir,
    )
    return {
        "cycle": list(LEARNING_STAGES),
        "mode": mode,
        "store_path": str(store_path),
        "observe": observed,
        "diagnose": diagnostic,
        "store": store_result,
        "recommend": [proposal.to_dict() for proposal in recommendations],
        "validate": validation,
        "implement": [result.to_dict() for result in implementation_results],
        "retest": retest_result,
        "remember": remember_result,
        # Backward-compatible fields used by the dashboard and earlier tests.
        "learning_report_path": remember_result["learning_report_path"],
        "feedback_entries": [entry.to_dict() for entry in observed["feedback_entries"]],
        "adaptation_proposals": [proposal.to_dict() for proposal in recommendations],
        "implementation_results": [result.to_dict() for result in implementation_results],
    }


def observe(run_result: dict[str, Any]) -> dict[str, Any]:
    """Observe run outputs without storing raw SAM cells or uploaded files."""

    return {
        "run_id": str(run_result.get("run_id", "")),
        "snapshot": build_run_snapshot(run_result),
        "feedback_entries": collect_run_feedback(run_result),
    }


def diagnose(observed: dict[str, Any], existing_store_data: dict[str, Any]) -> dict[str, Any]:
    """Diagnose immediate and recurring patterns from current plus past evidence."""

    feedback_dicts = [entry.to_dict() for entry in observed["feedback_entries"]]
    combined = dict(existing_store_data)
    combined["feedback"] = list(existing_store_data.get("feedback", [])) + feedback_dicts
    return recurring_issue_summary(combined)


def store_observations(store: LearningStore, observed: dict[str, Any]) -> dict[str, Any]:
    """Persist observations before recommendations are generated."""

    store.add_run_snapshot(observed["snapshot"])
    for entry in observed["feedback_entries"]:
        store.add_feedback(entry)
    return {
        "stored": True,
        "feedback_count": len(observed["feedback_entries"]),
        "snapshot_run_id": observed["run_id"],
    }


def recommend(store_data: dict[str, Any], version_root: str | Path) -> list[AdaptationProposal]:
    """Recommend versioned adaptations from stored evidence."""

    return propose_adaptations(store_data, version_root)


def validate_recommendations(
    proposals: list[AdaptationProposal],
    mode: LearningMode,
) -> dict[str, Any]:
    """Validate evidence and safety before implementation."""

    checks: list[dict[str, Any]] = []
    for proposal in proposals:
        has_evidence = bool(proposal.evidence_run_ids)
        confidence_ok = proposal.confidence_score > 0
        risk_ok = mode != "safe_apply" or proposal.risk_level == "low"
        checks.append(
            {
                "version_id": proposal.version_id,
                "has_evidence": has_evidence,
                "confidence_ok": confidence_ok,
                "risk_ok_for_mode": risk_ok,
                "valid": has_evidence and confidence_ok and risk_ok,
            }
        )
    return {
        "valid": all(check["valid"] for check in checks) if checks else True,
        "checks": checks,
        "mode": mode,
    }


def implement(
    proposals: list[AdaptationProposal],
    validation: dict[str, Any],
    mode: LearningMode,
    version_root: str | Path,
) -> list[ImplementationResult]:
    """Implement only proposals that passed validation for the selected mode."""

    valid_by_version = {
        check["version_id"]: bool(check["valid"])
        for check in validation.get("checks", [])
    }
    results: list[ImplementationResult] = []
    for proposal in proposals:
        if not valid_by_version.get(proposal.version_id, True):
            results.append(
                ImplementationResult(
                    status="blocked",
                    mode=mode,
                    version_id=proposal.version_id,
                    message="Adaptation blocked because evidence, confidence, or risk validation failed.",
                    validation_status="failed_pre_implementation_validation",
                )
            )
            continue
        results.append(implement_adaptation(proposal, mode=mode, version_root=version_root))
    return results


def retest(
    implementation_results: list[ImplementationResult],
    validation: dict[str, Any],
) -> dict[str, Any]:
    """Re-test implementation artifacts with lightweight safety checks."""

    checks: list[dict[str, Any]] = []
    for result in implementation_results:
        files_exist = all(Path(path).exists() for path in result.applied_files)
        high_risk_not_applied = not (
            result.status == "applied" and result.validation_status == "requires_user_review"
        )
        checks.append(
            {
                "version_id": result.version_id,
                "files_exist": files_exist,
                "high_risk_not_applied": high_risk_not_applied,
                "passed": files_exist and high_risk_not_applied,
            }
        )
    return {
        "passed": bool(validation.get("valid", True)) and all(check["passed"] for check in checks),
        "checks": checks,
        "note": "Runtime re-test checks versioned artifacts and safety status; repository tests are run separately.",
    }


def remember(
    store: LearningStore,
    run_result: dict[str, Any],
    observed: dict[str, Any],
    proposals: list[AdaptationProposal],
    implementation_results: list[ImplementationResult],
    output_dir: str | Path,
) -> dict[str, Any]:
    """Persist adaptations, implementations, and a learning report."""

    for proposal in proposals:
        store.add_adaptation(proposal)
    for result in implementation_results:
        store.add_implementation(result)
    report_path = generate_learning_report(
        run_result,
        [entry.to_dict() for entry in observed["feedback_entries"]],
        proposals,
        [result.to_dict() for result in implementation_results],
        output_dir,
    )
    store.add_report(
        str(run_result.get("run_id", "")),
        report_path,
        {
            "feedback_entries": len(observed["feedback_entries"]),
            "adaptation_proposals": len(proposals),
            "mode": run_result.get("learning_mode", "recommend"),
        },
    )
    return {
        "remembered": True,
        "learning_report_path": report_path,
        "adaptations_recorded": len(proposals),
        "implementations_recorded": len(implementation_results),
    }
