"""Create versioned adaptation proposals from learned patterns."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .memory_schema import AdaptationProposal
from .pattern_extractor import extract_patterns


DEFAULT_VERSION_ROOT = Path("learning_versions")


def propose_adaptations(store_data: dict[str, Any], version_root: str | Path = DEFAULT_VERSION_ROOT) -> list[AdaptationProposal]:
    """Convert recurring patterns into versioned adaptation proposals."""

    existing_versions = max(len(store_data.get("adaptations", [])), _max_existing_version(version_root))
    proposals: list[AdaptationProposal] = []
    for index, pattern in enumerate(extract_patterns(store_data), start=existing_versions + 1):
        risk = _risk_for_issue(pattern.issue_type)
        proposals.append(
            AdaptationProposal(
                version_id=f"v{index:03d}",
                change_summary=_change_summary(pattern.issue_type),
                reason_for_change=pattern.description,
                affected_templates_or_rules=_affected_rules(pattern.issue_type),
                confidence_score=pattern.confidence_score,
                risk_level=risk,
                recommended_mode="safe_apply" if risk == "low" else "recommend",
                evidence_run_ids=pattern.evidence_run_ids,
                rollback_instructions="Restore files from the rollback copy in this learning version folder.",
            )
        )
    return proposals


def write_adaptation_version(proposal: AdaptationProposal, version_root: str | Path = DEFAULT_VERSION_ROOT) -> str:
    """Write a versioned adaptation manifest without overwriting core templates."""

    version_dir = Path(version_root) / proposal.version_id
    version_dir.mkdir(parents=True, exist_ok=True)
    manifest = version_dir / "change_summary.md"
    manifest.write_text(
        "\n".join(
            [
                f"# Learning Version {proposal.version_id}",
                "",
                f"Change summary: {proposal.change_summary}",
                f"Reason for change: {proposal.reason_for_change}",
                f"Affected templates/rules: {', '.join(proposal.affected_templates_or_rules)}",
                f"Confidence score: {proposal.confidence_score}",
                f"Risk level: {proposal.risk_level}",
                f"Evidence runs: {', '.join(proposal.evidence_run_ids)}",
                "",
                "Rollback instructions:",
                proposal.rollback_instructions,
                "",
            ]
        ),
        encoding="utf-8",
    )
    return str(manifest)


def generate_learning_report(
    run_result: dict[str, Any],
    feedback_entries: list[dict[str, Any]],
    proposals: list[AdaptationProposal],
    implementation_results: list[dict[str, Any]],
    output_dir: str | Path = "outputs",
) -> str:
    """Write outputs/learning_report.md after each model run."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    report_path = destination / "learning_report.md"
    failed = [entry for entry in feedback_entries if entry["issue_type"] not in {"successful_model_run"}]
    worked = [entry for entry in feedback_entries if entry["issue_type"] == "successful_model_run"]
    lines = [
        "# Signal Learning Report",
        "",
        f"Run ID: `{run_result.get('run_id', 'unknown')}`",
        f"Status: `{run_result.get('status', 'unknown')}`",
        f"Requested backend: `{run_result.get('requested_backend', 'unknown')}`",
        f"Actual backend: `{run_result.get('backend', 'unknown')}`",
        "",
        "## What Signal Observed",
        "",
    ]
    lines.extend(f"- {entry['source']}: {entry['original_value']}" for entry in feedback_entries[:12])
    if not feedback_entries:
        lines.append("- No feedback entries were collected.")
    lines.extend(["", "## What Failed", ""])
    lines.extend(f"- {entry['issue_type']}: {entry['lesson_learned']}" for entry in failed[:12])
    if not failed:
        lines.append("- No failure pattern was detected.")
    lines.extend(["", "## What Worked", ""])
    lines.extend(f"- {entry['lesson_learned']}" for entry in worked[:8])
    if not worked:
        lines.append("- Successful-run evidence was not collected for this run.")
    lines.extend(["", "## What Was Learned", ""])
    for proposal in proposals[:8]:
        lines.append(
            f"- {proposal.change_summary} Evidence: {', '.join(proposal.evidence_run_ids)}. "
            f"Confidence: {proposal.confidence_score}."
        )
    if not proposals:
        lines.append("- No adaptation proposal was produced yet.")
    lines.extend(["", "## Recommended Fixes", ""])
    for result in implementation_results[:8]:
        lines.append(f"- [{result['status']}] {result['message']}")
    if not implementation_results:
        lines.append("- No implementation action was taken.")
    auto_applied = [result for result in implementation_results if result["status"] == "applied"]
    lines.extend(
        [
            "",
            "## Automatic Application",
            "",
            "- Yes" if auto_applied else "- No automatic changes were applied.",
            "",
            "## Confidence Level",
            "",
            f"- {max([proposal.confidence_score for proposal in proposals] or [0.0])}",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return str(report_path)


def _risk_for_issue(issue_type: str) -> str:
    if issue_type in {"gams_unavailable", "experimental_solver", "successful_model_run"}:
        return "low"
    if issue_type in {"sam_imbalance", "gams_error", "validation_error"}:
        return "medium"
    return "high"


def _max_existing_version(version_root: str | Path) -> int:
    root = Path(version_root)
    if not root.exists():
        return 0
    versions: list[int] = []
    for child in root.iterdir():
        if child.is_dir() and child.name.startswith("v") and child.name[1:].isdigit():
            versions.append(int(child.name[1:]))
    return max(versions, default=0)


def _affected_rules(issue_type: str) -> list[str]:
    mapping = {
        "sam_imbalance": ["cge_core.sam.balance_check", "knowledge_base/sam_account_classification.md"],
        "gams_error": ["backends/gams/gams_templates.py", "knowledge_base/gams_common_errors.md"],
        "validation_error": ["signal_modeling_language/validator.py"],
        "gams_unavailable": ["solvers/solver_registry.py", "knowledge_base/solver_diagnostics.md"],
        "experimental_solver": ["docs/solver_layer.md", "knowledge_base/solver_diagnostics.md"],
        "successful_model_run": ["signal_modeling_language/examples/basic_cge.sml"],
    }
    return mapping.get(issue_type, ["manual_review"])


def _change_summary(issue_type: str) -> str:
    mapping = {
        "sam_imbalance": "Add stronger SAM imbalance guidance before solve.",
        "gams_error": "Add GAMS template guidance for recurring syntax/indexing failures.",
        "validation_error": "Tighten SML validation for recurring invalid patterns.",
        "gams_unavailable": "Recommend explicit fallback mode when GAMS is unavailable.",
        "experimental_solver": "Flag experimental solver outputs before policy use.",
        "successful_model_run": "Preserve successful model structure as scenario-template evidence.",
    }
    return mapping.get(issue_type, "Manual learning review required.")
