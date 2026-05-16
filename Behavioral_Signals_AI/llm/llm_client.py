"""Optional LLM client for Behavioral Signals AI.

The app runs without LLM credentials. API calls are attempted only when explicitly
enabled and a key is present in environment variables.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


def llm_config() -> dict[str, Any]:
    enabled = os.getenv("SIGNAL_LLM_ENABLED", "false").strip().lower() in {"1", "true", "yes", "on"}
    return {
        "enabled": enabled,
        "provider": (os.getenv("SIGNAL_LLM_PROVIDER", "local").strip().lower() or "local").replace("-", "_"),
        "api_key": os.getenv("SIGNAL_LLM_API_KEY", "").strip(),
        "model": os.getenv("SIGNAL_LLM_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini",
        "endpoint": os.getenv("SIGNAL_LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions").strip(),
        "max_tokens": int(os.getenv("SIGNAL_LLM_MAX_TOKENS", "700") or "700"),
    }


def is_llm_api_available() -> bool:
    config = llm_config()
    return bool(config["enabled"] and config["api_key"] and config["provider"] not in {"", "local", "fallback"})


def complete_json(system_prompt: str, payload: dict[str, Any], *, fallback: dict[str, Any]) -> dict[str, Any]:
    """Return JSON from optional API mode, otherwise the supplied fallback."""
    if not is_llm_api_available():
        result = dict(fallback)
        result.setdefault("llm_mode", "rule_based_fallback")
        result.setdefault("llm_warning", "LLM API disabled or missing credentials; using deterministic fallback.")
        return result
    config = llm_config()
    try:
        if config["provider"] in {"openai", "openai_compatible"}:
            return _openai_compatible_json(system_prompt, payload, fallback, config)
    except Exception as exc:
        result = dict(fallback)
        result["llm_mode"] = "rule_based_fallback"
        result["llm_warning"] = f"LLM API failed safely: {exc}"
        return result
    result = dict(fallback)
    result["llm_mode"] = "rule_based_fallback"
    result["llm_warning"] = f"Unsupported provider {config['provider']}; using deterministic fallback."
    return result


def _openai_compatible_json(system_prompt: str, payload: dict[str, Any], fallback: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    body = {
        "model": config["model"],
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=True)},
        ],
        "temperature": 0.2,
        "max_tokens": config.get("max_tokens", 700),
    }
    request = urllib.request.Request(
        config["endpoint"],
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(str(exc)) from exc
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")
    parsed = json.loads(content)
    if not isinstance(parsed, dict):
        raise RuntimeError("LLM did not return a JSON object")
    parsed.setdefault("llm_mode", "api")
    parsed.setdefault("llm_provider", config["provider"])
    return parsed