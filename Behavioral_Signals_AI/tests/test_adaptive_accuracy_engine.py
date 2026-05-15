from pathlib import Path


def test_noisy_signals_are_down_ranked():
    from Behavioral_Signals_AI.signal_engine.signal_quality import score_signal_quality

    noisy = score_signal_quality({"topic": "!!!", "source_type": "aggregate_public", "category": "other"}, [])
    clean = score_signal_quality({"topic": "maize flour prices Kenya", "source_type": "search_trend", "category": "food and agriculture", "location": "Kenya"}, [])
    assert noisy["quality_score"] < clean["quality_score"]
    assert noisy["accepted"] is False


def test_repeated_signals_gain_persistence(tmp_path, monkeypatch):
    monkeypatch.setenv("SIGNAL_CLUSTER_MEMORY_PATH", str(tmp_path / "signal_memory.json"))
    from Behavioral_Signals_AI.signal_engine.adaptive_learning_engine import update_signal_memory, load_cluster_memory, adapt_signal_scores

    signal = {"signal_topic": "maize flour prices", "signal_category": "food and agriculture", "confidence_score": 50, "priority_score": 60, "momentum": "Rising", "accuracy_confidence": 60}
    update_signal_memory([signal])
    update_signal_memory([signal])
    memory = load_cluster_memory()
    adapted = adapt_signal_scores(dict(signal), memory, {"feedback": []})
    assert adapted["confidence_score"] > 50
    assert adapted["persistence_badge"] in {"Persistent", "Emerging"}


def test_multi_source_signals_gain_confidence():
    from Behavioral_Signals_AI.signal_engine.signal_quality import score_signal_quality

    peers = [
        {"topic": "fuel prices Kenya", "source_type": "search_trend"},
        {"topic": "fuel prices Kenya", "source_type": "news_public"},
    ]
    score = score_signal_quality({"topic": "fuel prices Kenya", "source_type": "search_trend", "category": "energy", "location": "Kenya"}, peers)
    assert score["multi_source_confirmation_score"] >= 70


def test_validation_status_is_assigned():
    from Behavioral_Signals_AI.signal_engine.validation_engine import validate_signal

    validated = validate_signal({"signal_category": "food and agriculture", "source_summary": "WFP food price data"})
    partial = validate_signal({"signal_category": "health", "source_summary": "Search trends + public news"})
    assert validated["validation_status"] == "validated"
    assert partial["validation_status"] in {"partially_validated", "validated"}


def test_analyst_feedback_changes_future_scoring(tmp_path, monkeypatch):
    monkeypatch.setenv("SIGNAL_FEEDBACK_PATH", str(tmp_path / "signal_feedback.json"))
    from Behavioral_Signals_AI.signal_engine.adaptive_learning_engine import analyst_rejects_signal, adapt_signal_scores, load_feedback

    signal = {"signal_topic": "weak topic", "signal_category": "other", "confidence_score": 70, "priority_score": 60, "momentum": "Stable", "accuracy_confidence": 50}
    before = adapt_signal_scores(dict(signal), {"clusters": {}}, {"feedback": []})["confidence_score"]
    analyst_rejects_signal("weak topic")
    after = adapt_signal_scores(dict(signal), {"clusters": {}}, load_feedback())["confidence_score"]
    assert after < before


def test_signal_memory_updates_safely(tmp_path, monkeypatch):
    monkeypatch.setenv("SIGNAL_CLUSTER_MEMORY_PATH", str(tmp_path / "signal_memory.json"))
    from Behavioral_Signals_AI.signal_engine.adaptive_learning_engine import update_signal_memory, load_cluster_memory

    update_signal_memory([{"signal_topic": "jobs in Nairobi", "signal_category": "jobs and labour market", "confidence_score": 75, "urgency": "High", "momentum": "Breakout"}])
    memory = load_cluster_memory()
    assert memory["clusters"]
    cluster = next(iter(memory["clusters"].values()))
    assert cluster["number_of_appearances"] == 1


def test_missing_apis_do_not_crash(monkeypatch):
    for key in ["SERPAPI_KEY", "NEWS_API_KEY", "YOUTUBE_API_KEY", "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "X_BEARER_TOKEN"]:
        monkeypatch.delenv(key, raising=False)
    from Behavioral_Signals_AI.signal_engine.kenya_signal_fusion import fuse_kenya_signals

    assert fuse_kenya_signals("Kenya", "All", "All")


def test_no_raw_personal_fields_are_stored(tmp_path, monkeypatch):
    monkeypatch.setenv("SIGNAL_CLUSTER_MEMORY_PATH", str(tmp_path / "signal_memory.json"))
    from Behavioral_Signals_AI.signal_engine.adaptive_learning_engine import update_signal_memory

    memory = update_signal_memory([{"signal_topic": "hospital near me", "user_id": "abc", "email": "x@y.com", "private_message": "secret"}])
    text = str(memory)
    assert "user_id" not in text
    assert "x@y.com" not in text
    assert "secret" not in text


def test_signal_cge_remains_present():
    source = Path("app.py").read_text(encoding="utf-8")
    assert 'with gr.Tab("Signal CGE")' in source