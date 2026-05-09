"""Lightweight repo knowledge graph for Signal CGE references."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .reference_index import build_reference_index


KEYWORD_NODES = {
    "trade": ["trade", "import", "export", "tariff"],
    "tax": ["tax", "vat", "revenue"],
    "government": ["government", "fiscal", "deficit"],
    "prices": ["price", "wedge", "numeraire"],
    "households": ["household", "welfare", "income"],
    "factors": ["factor", "labour", "labor", "capital"],
    "calibration": ["calibration", "benchmark", "share"],
    "closures": ["closure", "savings", "foreign", "numeraire"],
    "dynamics": ["dynamic", "recursive", "capital accumulation", "growth"],
}


def build_knowledge_graph() -> dict[str, Any]:
    """Build a deterministic graph from indexed reference paths."""

    index = build_reference_index()
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []
    grouped: dict[str, list[str]] = defaultdict(list)
    for source in index.get("repo_knowledge_sources", []):
        path = str(source.get("path", ""))
        lower = path.lower()
        node_id = path.replace("\\", "/")
        tags = [tag for tag, keywords in KEYWORD_NODES.items() if any(keyword in lower for keyword in keywords)]
        nodes[node_id] = {"path": node_id, "tags": tags, "section": source.get("section")}
        for tag in tags:
            grouped[tag].append(node_id)
            edges.append({"source": tag, "target": node_id, "relationship": "documents"})
    return {
        "nodes": nodes,
        "edges": edges,
        "topic_index": dict(grouped),
        "source_count": len(nodes),
    }


def get_topic_references(topic: str) -> list[str]:
    """Return reference paths connected to a broad CGE topic."""

    graph = build_knowledge_graph()
    return graph["topic_index"].get(topic, [])
