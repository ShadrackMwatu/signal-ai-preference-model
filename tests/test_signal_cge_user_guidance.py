from __future__ import annotations

from pathlib import Path


DOCS = [
    "Documentation/SIGNAL_CGE_USER_GUIDE.md",
    "Documentation/SIGNAL_CGE_OPERATING_WORKFLOW.md",
    "Documentation/SIGNAL_CGE_SIMULATION_INSTRUCTIONS.md",
    "Documentation/SIGNAL_CGE_VALIDATION_CHECKS.md",
    "Documentation/SIGNAL_CGE_RESULTS_GUIDE.md",
]


def test_signal_cge_guidance_documents_exist() -> None:
    for doc in DOCS:
        path = Path(doc)
        assert path.exists()
        assert path.stat().st_size > 500


def test_user_guide_contains_expected_sections() -> None:
    text = Path("Documentation/SIGNAL_CGE_USER_GUIDE.md").read_text(encoding="utf-8")

    for heading in [
        "Introduction To Signal CGE",
        "Signal CGE Folder Structure",
        "How To Prepare A SAM",
        "Calibration Workflow",
        "Closure Rules",
        "Future Full-Equilibrium Solver Pathway",
    ]:
        assert heading in text


def test_app_imports_and_ui_contains_how_to_use_signal_cge() -> None:
    import app

    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]
    source = Path("app.py").read_text(encoding="utf-8")
    assert "How to use Signal CGE" in source
    assert "Type a policy simulation prompt" in source


def test_policy_brief_contains_operating_trace() -> None:
    from app_routes.signal_cge_route import run_signal_cge_prompt

    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    report = Path(result["downloads"]["policy_brief_md"]).read_text(encoding="utf-8")

    for section in [
        "Prompt Entered",
        "Interpreted Scenario",
        "Model References Used",
        "Solver/Backend Used",
        "Validation Status",
        "Prototype Directional Results",
        "Caveats",
        "Next Recommended Simulations",
    ]:
        assert section in report
