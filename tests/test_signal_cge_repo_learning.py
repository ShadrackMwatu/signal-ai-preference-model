from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from app_routes.signal_cge_route import run_signal_cge_prompt
from Signal_CGE.signal_cge.learning.learning_registry import summarize_learning_memory
from Signal_CGE.signal_cge.learning.model_gap_detector import generate_model_gap_report
from Signal_CGE.signal_cge.learning.scenario_pattern_learning import find_similar_simulations, learn_prompt_patterns
from Signal_CGE.signal_cge.learning.simulation_memory import (
    load_simulation_memory,
    record_simulation_learning_event,
)


def test_learning_memory_stores_metadata_only_event() -> None:
    memory_path = Path(f"Signal_CGE/outputs/signal_cge_learning/test_memory_{uuid4().hex}.jsonl")
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    event = record_simulation_learning_event(
        {
            "prompt": "reduce import tariffs on cmach by 10%",
            "scenario": {"shock_type": "import_tariff", "target_account": "cmach", "shock_size": -10},
            "backend_used": "python_sam_multiplier",
        },
        path=memory_path,
    )
    events = load_simulation_memory(path=memory_path)

    assert event["event_id"]
    assert events[0]["target_account"] == "cmach"
    assert "uploaded" not in events[0]


def test_run_signal_cge_prompt_is_knowledge_aware() -> None:
    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["result_type"] == "open_source_equilibrium_cge_prototype"
    assert result["knowledge_context"]["reference_labels"]
    assert result["model_gap_report"]
    assert "prior_learning_used" in result["interpretation"]
    assert "Full equilibrium effects require the future solver." in result["interpretation"]["caveats"]


def test_model_gap_report_and_pattern_learning_generate() -> None:
    report = generate_model_gap_report(write=False)
    patterns = learn_prompt_patterns(limit=10)
    similar = find_similar_simulations(
        "reduce import tariffs on cmach by 10%",
        {"shock_type": "import_tariff", "target_account": "cmach"},
    )
    summary = summarize_learning_memory(limit=10)

    assert "solver_limitations" in report
    assert "common_prompt_terms" in patterns
    assert isinstance(similar, list)
    assert "event_count" in summary


def test_app_imports_successfully_after_repo_learning() -> None:
    import app

    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]
