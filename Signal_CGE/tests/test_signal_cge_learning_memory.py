"""Tests for repo-safe Signal CGE learning memory."""

from __future__ import annotations

from pathlib import Path
import uuid

from app_routes.signal_cge_route import run_signal_cge_prompt
from signal_cge.learning.adaptive_rules import apply_adaptive_prompt_rules
from signal_cge.learning.learning_registry import summarize_learning_memory
from signal_cge.learning.model_improvement_suggestions import generate_model_improvement_suggestions
from signal_cge.learning.simulation_memory import load_simulation_memory, record_simulation_learning_event


def test_record_simulation_learning_event_creates_metadata_only_event() -> None:
    scratch = Path("tests/_tmp/signal_cge_learning")
    scratch.mkdir(parents=True, exist_ok=True)
    memory_path = scratch / f"simulation_memory_{uuid.uuid4().hex}.jsonl"
    event = record_simulation_learning_event(
        {
            "prompt": "reduce import tariffs on cmach by 10%",
            "scenario": {"shock_type": "import_tariff", "target_account": "cmach", "shock_size": -10},
            "backend_used": "python_sam_multiplier",
            "knowledge_references_used": ["Trade Block"],
        },
        path=memory_path,
    )

    assert event["event_id"]
    assert event["target_account"] == "cmach"
    assert memory_path.exists()
    assert "uploaded" not in memory_path.read_text(encoding="utf-8").lower()


def test_learning_registry_summarizes_prior_events() -> None:
    run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    summary = summarize_learning_memory(limit=10)

    assert summary["event_count"] >= 1
    assert summary["common_scenario_types"]
    assert summary["backend_limitations_observed"]


def test_adaptive_rules_map_reduce_tariffs_prompt() -> None:
    hints = apply_adaptive_prompt_rules("reduce tariffs on cmach by 10%")

    assert hints["policy_instrument"] == "import_tariff"
    assert hints["shock_direction"] == "decrease"
    assert hints["target_account"] == "cmach"
    assert hints["target_account_type"] == "commodity"


def test_model_improvement_suggestions_are_generated() -> None:
    run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    suggestions = generate_model_improvement_suggestions(limit=20)

    assert suggestions["solver_features_needed"]
    assert suggestions["knowledge_docs_to_expand"]
    assert suggestions["suggestions"]


def test_runtime_learning_memory_is_ignored() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    assert "outputs/signal_cge_learning/*.jsonl" in gitignore
    assert Path("outputs/signal_cge_learning/.gitkeep").exists()


def test_app_imports_successfully() -> None:
    import app

    assert hasattr(app, "demo")
