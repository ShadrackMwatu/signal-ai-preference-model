"""Tests for repo-default Signal CGE execution without uploaded workbooks."""

from __future__ import annotations

from pathlib import Path


def test_repo_default_signal_cge_execution_no_upload() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["diagnostics"]["model_profile_loaded"] is True
    assert result["diagnostics"]["canonical_model_profile"].endswith("model_profile.yaml")
    assert result["diagnostics"]["uploaded_sam"].startswith("not provided")
    assert result["results"]["account_effects"]
    assert result["chart_data"]
    assert result["backend_used"] == "open_source_equilibrium_solver"


def test_repo_default_downloads_are_materialized() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    for key in ["results_json", "results_csv", "policy_brief_md"]:
        path = Path(result["downloads"][key])
        assert path.exists()
        assert path.stat().st_size > 0
