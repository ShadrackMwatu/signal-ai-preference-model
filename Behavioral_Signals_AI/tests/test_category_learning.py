"""Adaptive category learning tests for Open Signals."""

from __future__ import annotations

import pytest

from Behavioral_Signals_AI.signal_engine.category_learning import (
    DEFAULT_CATEGORIES,
    category_matches_signal,
    get_active_learned_categories,
    get_category_options,
    learn_categories_from_signals,
    load_category_memory,
    matching_default_category,
    reject_personal_category_text,
)


def test_default_categories_remain_available() -> None:
    assert DEFAULT_CATEGORIES == [
        "All",
        "Ceramics",
        "food and agriculture",
        "jobs and labour market",
        "housing",
        "health",
        "transport",
        "energy",
        "technology",
        "education",
        "finance",
        "public services",
        "water and sanitation",
        "climate and environment",
        "cost of living",
        "trade and business",
        "security and governance",
        "other",
    ]


def test_learned_category_memory_initializes_safely(tmp_path) -> None:
    memory = load_category_memory(tmp_path / "category_learning_memory.json")

    assert memory["categories"] == {}
    assert memory["privacy_level"] == "aggregate_category_learning_only"


def test_repeated_signals_promote_category(tmp_path) -> None:
    path = tmp_path / "category_learning_memory.json"
    signals = [
        {"signal_topic": "cement prices rising in county markets", "signal_category": "other"},
        {"signal_topic": "mabati and cement demand increasing", "signal_category": "other"},
    ]

    memory = learn_categories_from_signals(signals, path)

    category = memory["categories"]["construction materials"]
    assert category["appearance_count"] == 2
    assert category["status"] == "active"
    assert "construction materials" in get_active_learned_categories(path)


def test_one_off_noisy_signals_do_not_promote_category(tmp_path) -> None:
    path = tmp_path / "category_learning_memory.json"
    learn_categories_from_signals([{"signal_topic": "one random vague meme topic", "signal_category": "other"}], path)

    assert get_active_learned_categories(path) == []


def test_duplicate_categories_are_merged_with_defaults(tmp_path) -> None:
    path = tmp_path / "category_learning_memory.json"
    signals = [
        {"signal_topic": "hospital near me searches rising", "signal_category": "other"},
        {"signal_topic": "clinic near me demand rising", "signal_category": "other"},
    ]

    memory = learn_categories_from_signals(signals, path)

    assert matching_default_category("healthcare access", ["hospital near me"]) == "health"
    assert "healthcare access" not in memory["categories"]
    assert "healthcare access" not in get_active_learned_categories(path)


def test_personal_data_is_rejected() -> None:
    with pytest.raises(ValueError):
        reject_personal_category_text("demand from user_id 123 private_message exact address")


def test_category_dropdown_includes_active_learned_categories(tmp_path) -> None:
    path = tmp_path / "category_learning_memory.json"
    learn_categories_from_signals([
        {"signal_topic": "cement prices rising in county markets", "signal_category": "other"},
        {"signal_topic": "mabati and cement demand increasing", "signal_category": "other"},
    ], path)

    options = get_category_options(path)

    assert options[0] == "All"
    assert "food and agriculture" in options
    assert "construction materials" in options
    assert len(options) == len(set(options))


def test_learned_category_filters_by_related_terms(tmp_path) -> None:
    path = tmp_path / "category_learning_memory.json"
    learn_categories_from_signals([
        {"signal_topic": "cement prices rising in county markets", "signal_category": "other"},
        {"signal_topic": "mabati and cement demand increasing", "signal_category": "other"},
    ], path)

    assert category_matches_signal({"signal_topic": "cement shortage pressure", "signal_category": "other"}, "construction materials", path)
    assert not category_matches_signal({"signal_topic": "school fees pressure", "signal_category": "education"}, "construction materials", path)
