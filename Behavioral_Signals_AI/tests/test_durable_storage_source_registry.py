from pathlib import Path

from Behavioral_Signals_AI.providers.connector_status import connector_status_report, load_source_registry
from Behavioral_Signals_AI.signal_engine.historical_memory import get_historical_storage_health
from Behavioral_Signals_AI.storage.storage_manager import read_json, storage_health, write_json


def test_atomic_storage_write_and_backup_creation(tmp_path):
    target = tmp_path / "memory.json"
    first = {"records": [1]}
    second = {"records": [1, 2]}
    result1 = write_json(target, first)
    result2 = write_json(target, second)

    assert result1["ok"] is True
    assert result2["ok"] is True
    assert read_json(target, {}) == second
    assert target.with_suffix(".json.bak").exists()


def test_malformed_file_recovery_preserves_app_flow(tmp_path):
    target = tmp_path / "bad.json"
    target.write_text("{bad json", encoding="utf-8")
    recovered = read_json(target, {"safe": True})
    assert recovered == {"safe": True}
    assert list(tmp_path.glob("bad.json.corrupt-*"))


def test_storage_health_check_reports_paths(tmp_path):
    memory = tmp_path / "memory.json"
    history = tmp_path / "history.json"
    forecast = tmp_path / "forecast.json"
    write_json(memory, {})
    write_json(history, {})
    health = storage_health({"memory": memory, "history": history, "forecast": forecast})
    assert health["memory_available"] is True
    assert health["history_available"] is True
    assert health["forecast_memory_available"] is False
    assert health["backend"] == "local_json"


def test_source_registry_loading_and_connector_status(tmp_path, monkeypatch):
    registry = tmp_path / "source_registry.yaml"
    registry.write_text(
        "sources:\n"
        "  - name: live_search\n"
        "    enabled: true\n"
        "    requires_api_key: true\n"
        "    environment_key: TEST_SEARCH_KEY\n"
        "    update_frequency_seconds: 60\n"
        "    reliability_prior: 0.8\n"
        "    kenya_relevance_prior: 0.9\n"
        "  - name: public_news\n"
        "    enabled: true\n"
        "    requires_api_key: false\n"
        "    environment_key: \"\"\n",
        encoding="utf-8",
    )
    sources = load_source_registry(registry)
    status = connector_status_report(registry)
    assert len(sources) == 2
    assert any(row["status"] == "missing credentials" for row in status["sources"])
    assert any(row["status"] == "available" for row in status["sources"])
    monkeypatch.setenv("TEST_SEARCH_KEY", "configured")
    status = connector_status_report(registry)
    assert all(row["status"] == "available" for row in status["sources"])


def test_historical_storage_health_function_imports():
    health = get_historical_storage_health()
    assert "memory_available" in health
    assert "last_successful_write" in health


def test_app_import_and_signal_cge_reference_remains():
    import app

    source = Path("app.py").read_text(encoding="utf-8")
    assert hasattr(app, "demo") or hasattr(app, "app")
    assert "Signal CGE" in source
