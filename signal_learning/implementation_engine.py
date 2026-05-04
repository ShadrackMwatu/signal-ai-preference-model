"""Implement, recommend, or roll back learned adaptations safely."""

from __future__ import annotations

import shutil
from pathlib import Path

from .adaptation_engine import write_adaptation_version
from .memory_schema import AdaptationProposal, ImplementationResult, LearningMode


def implement_adaptation(
    proposal: AdaptationProposal,
    mode: LearningMode = "recommend",
    version_root: str | Path = "learning_versions",
) -> ImplementationResult:
    """Suggest or apply low-risk changes; high-risk changes require review."""

    manifest_path = write_adaptation_version(proposal, version_root)
    if mode == "observe_only":
        return ImplementationResult(
            status="suggested",
            mode=mode,
            version_id=proposal.version_id,
            message="Observe-only mode recorded the lesson without suggesting implementation.",
            validation_status="not_applied",
            applied_files=[],
        )
    if mode == "recommend" or proposal.risk_level != "low":
        return ImplementationResult(
            status="suggested",
            mode=mode,
            version_id=proposal.version_id,
            message="Recommendation saved for user review; core templates were not overwritten.",
            validation_status="requires_user_review",
            applied_files=[manifest_path],
        )
    return _safe_apply(proposal, manifest_path, version_root)


def rollback_adaptation(version_id: str, version_root: str | Path = "learning_versions") -> ImplementationResult:
    """Roll back files from a version folder when rollback copies exist."""

    version_dir = Path(version_root) / version_id
    rollback_dir = version_dir / "rollback"
    if not rollback_dir.exists():
        return ImplementationResult(
            status="blocked",
            mode="safe_apply",
            version_id=version_id,
            message="No rollback copy found for this version.",
            validation_status="not_available",
        )
    restored: list[str] = []
    for file_path in rollback_dir.rglob("*"):
        if file_path.is_file():
            relative = file_path.relative_to(rollback_dir)
            destination = Path(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, destination)
            restored.append(str(destination))
    return ImplementationResult(
        status="rolled_back",
        mode="safe_apply",
        version_id=version_id,
        message="Rollback files restored.",
        validation_status="restored_from_copy",
        applied_files=restored,
    )


def _safe_apply(
    proposal: AdaptationProposal,
    manifest_path: str,
    version_root: str | Path,
) -> ImplementationResult:
    version_dir = Path(version_root) / proposal.version_id
    adapted_template = version_dir / "adapted_rule.md"
    rollback_dir = version_dir / "rollback"
    rollback_dir.mkdir(parents=True, exist_ok=True)
    adapted_template.write_text(
        "\n".join(
            [
                f"# Adapted Rule {proposal.version_id}",
                "",
                proposal.change_summary,
                "",
                f"Evidence runs: {', '.join(proposal.evidence_run_ids)}",
                f"Confidence: {proposal.confidence_score}",
                "",
                "This is a versioned adapted template. Core templates were not overwritten.",
            ]
        ),
        encoding="utf-8",
    )
    return ImplementationResult(
        status="applied",
        mode="safe_apply",
        version_id=proposal.version_id,
        message="Low-risk adaptation applied as a versioned adapted template only.",
        validation_status="versioned_template_created",
        applied_files=[manifest_path, str(adapted_template)],
        rollback_files=[str(rollback_dir)],
    )
