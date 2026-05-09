from __future__ import annotations

from Signal_CGE.signal_cge.knowledge.document_loader import (
    load_model_profile,
    load_repo_knowledge_bundle,
    list_repo_knowledge_sources,
)
from Signal_CGE.signal_cge.knowledge.knowledge_graph import build_knowledge_graph
from Signal_CGE.signal_cge.knowledge.reference_index import build_reference_index
from Signal_CGE.signal_cge.knowledge.scenario_context import get_scenario_context
from Signal_CGE.signal_cge.knowledge.semantic_mapping import infer_account_type, map_prompt_semantics


def test_repo_docs_and_canonical_profile_load() -> None:
    profile = load_model_profile()
    sources = list_repo_knowledge_sources()
    bundle = load_repo_knowledge_bundle()

    assert profile
    assert any("Signal_CGE/models/canonical" in source["path"] for source in sources)
    assert "SIGNAL_CGE_KNOWLEDGE_BASE.md" in bundle


def test_reference_index_categorizes_knowledge_sources() -> None:
    index = build_reference_index()

    assert index["repo_knowledge_sources"]
    assert "equations" in index["knowledge_categories"]
    assert "calibration" in index["knowledge_categories"]


def test_scenario_context_returns_trade_references() -> None:
    context = get_scenario_context(
        {
            "prompt": "reduce import tariffs on cmach by 10%",
            "shock_type": "import_tariff",
            "target_account": "cmach",
        }
    )

    assert context["scenario_type"] == "import_tariff"
    assert any("Trade Block" in label for label in context["reference_labels"])
    assert "semantic_hints" in context


def test_semantic_mapping_and_knowledge_graph() -> None:
    mapping = map_prompt_semantics("reduce import tariffs on cmach by 10%")
    graph = build_knowledge_graph()

    assert mapping["policy_instrument"] == "import_tariff"
    assert infer_account_type("cmach") == "commodity"
    assert graph["source_count"] > 0
    assert "trade" in graph["topic_index"]
