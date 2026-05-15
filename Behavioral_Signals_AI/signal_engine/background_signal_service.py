"""Background polling service for Kenya aggregate signal cache updates."""

from __future__ import annotations

import os
import threading
import time
from typing import Any

from Behavioral_Signals_AI.signal_engine.signal_cache import initialize_signal_cache, refresh_signal_cache

_SERVICE_LOCK = threading.Lock()
_SERVICE_THREAD: threading.Thread | None = None
_STOP_EVENT = threading.Event()


def start_background_signal_service() -> bool:
    """Start a single cache-refresh worker thread if enabled."""
    global _SERVICE_THREAD
    enabled = os.getenv("SIGNAL_BACKGROUND_SERVICE_ENABLED", "true").lower() not in {"0", "false", "no", "off"}
    if not enabled:
        initialize_signal_cache()
        return False
    with _SERVICE_LOCK:
        if _SERVICE_THREAD and _SERVICE_THREAD.is_alive():
            return False
        initialize_signal_cache()
        _STOP_EVENT.clear()
        _SERVICE_THREAD = threading.Thread(target=_poll_loop, name="signal-kenya-background-poller", daemon=True)
        _SERVICE_THREAD.start()
        return True


def service_status() -> dict[str, Any]:
    thread = _SERVICE_THREAD
    return {
        "enabled": os.getenv("SIGNAL_BACKGROUND_SERVICE_ENABLED", "true").lower() not in {"0", "false", "no", "off"},
        "running": bool(thread and thread.is_alive()),
        "thread_name": thread.name if thread else None,
    }


def stop_background_signal_service() -> None:
    _STOP_EVENT.set()


def _poll_loop() -> None:
    seconds = _poll_seconds()
    while not _STOP_EVENT.is_set():
        try:
            refresh_signal_cache("Kenya")
        except Exception:
            pass
        _STOP_EVENT.wait(seconds)


def _poll_seconds() -> int:
    try:
        return max(15, int(float(os.getenv("SIGNAL_BACKGROUND_POLL_SECONDS", "60"))))
    except Exception:
        return 60