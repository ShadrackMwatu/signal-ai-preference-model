from pathlib import Path
import json


BASELINE_SUMMARY = Path("Signal_CGE/outputs/baseline/baseline_summary.json")


def load_baseline_summary() -> dict:
    if not BASELINE_SUMMARY.exists():
        return {
            "status": "missing",
            "baseline_name": "Baseline not available",
            "solver_status": "Not available",
            "model_status": "Not available",
            "recommended_next_symbols": [],
            "description": "Run the baseline GAMS model and exporter first.",
        }

    with BASELINE_SUMMARY.open("r", encoding="utf-8") as f:
        return json.load(f)


def baseline_dashboard_markdown() -> str:
    data = load_baseline_summary()

    indicators = data.get("recommended_next_symbols", [])
    indicators_text = "\n".join([f"- {x}" for x in indicators]) or "- No indicators mapped yet"

    return f"""
## Signal CGE Baseline Economy

**Baseline:** {data.get("baseline_name", "N/A")}

**Baseline status:** {data.get("status", "N/A")}

**Solver status:** {data.get("solver_status", "N/A")}

**Model status:** {data.get("model_status", "N/A")}

### Description

{data.get("description", "")}

### Available / Planned Indicators

{indicators_text}

### Architecture

GAMS → baseline.gdx → Python exporter → JSON summary → Signal dashboard → AI policy interpretation
"""


if __name__ == "__main__":
    print(baseline_dashboard_markdown())