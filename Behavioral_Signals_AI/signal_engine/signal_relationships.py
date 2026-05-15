"""Relationship graph for Kenya behavioral-economic signals."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import write_json

GRAPH_PATH = Path(os.getenv("SIGNAL_RELATIONSHIP_GRAPH_PATH", "Behavioral_Signals_AI/outputs/signal_relationship_graph.json"))

RELATION_RULES = [
    ("fuel", "transport", "fuel price pressure may raise transport costs"),
    ("transport", "food", "transport cost pressure may feed into food prices"),
    ("fuel", "food", "fuel price pressure can amplify food affordability pressure"),
    ("drought", "water", "drought signals may intensify water shortage risk"),
    ("water", "crop", "water stress may become crop stress"),
    ("drought", "food", "drought signals may indicate food supply risk"),
    ("jobs", "housing", "job search and housing search together may indicate urban migration pressure"),
    ("rent", "jobs", "housing affordability and job search may indicate urban livelihood stress"),
]


def detect_signal_relationships(signals: list[dict[str, Any]]) -> dict[str, Any]:
    nodes = [_node(signal) for signal in signals]
    edges: list[dict[str, str]] = []
    for left in signals:
        for right in signals:
            if left is right:
                continue
            relation = _relationship(left, right)
            if relation:
                edges.append(relation)
    graph = {"nodes": nodes, "edges": _dedupe_edges(edges)}
    write_relationship_graph(graph)
    return graph


def relationship_summary(graph: dict[str, Any]) -> str:
    edges = graph.get("edges", [])
    if not edges:
        return "No strong cross-signal relationship detected yet."
    examples = [edge["description"] for edge in edges[:3]]
    return "; ".join(examples)


def write_relationship_graph(graph: dict[str, Any], path: str | Path | None = None) -> None:
    write_json(Path(path or GRAPH_PATH), graph)


def related_signals_for_topic(topic: str, signals: list[dict[str, Any]], graph: dict[str, Any]) -> list[dict[str, Any]]:
    connected: set[str] = set()
    for edge in graph.get("edges", []):
        if edge.get("from") == topic:
            connected.add(str(edge.get("to")))
        if edge.get("to") == topic:
            connected.add(str(edge.get("from")))
    return [signal for signal in signals if str(signal.get("signal_topic")) in connected]


def _node(signal: dict[str, Any]) -> dict[str, Any]:
    return {"topic": signal.get("signal_topic"), "category": signal.get("signal_category"), "county": signal.get("geographic_scope")}


def _relationship(left: dict[str, Any], right: dict[str, Any]) -> dict[str, str] | None:
    text_left = f"{left.get('signal_topic', '')} {left.get('signal_category', '')}".lower()
    text_right = f"{right.get('signal_topic', '')} {right.get('signal_category', '')}".lower()
    for cause, effect, description in RELATION_RULES:
        if cause in text_left and effect in text_right:
            return {"from": str(left.get("signal_topic")), "to": str(right.get("signal_topic")), "description": description}
    return None


def _dedupe_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen = set()
    output = []
    for edge in edges:
        key = (edge.get("from"), edge.get("to"), edge.get("description"))
        if key not in seen:
            seen.add(key)
            output.append(edge)
    return output
