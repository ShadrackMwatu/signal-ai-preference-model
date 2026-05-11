from pathlib import Path
import json
import re
import subprocess


GAMS_DIR = Path("Signal_CGE/models/gams")
BASELINE_GDX = GAMS_DIR / "baseline.gdx"
SCENARIO_GDX = GAMS_DIR / "scenario.gdx"

OUTPUT_DIR = Path("Signal_CGE/outputs/gdx")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def dump_gdx(gdx_path: Path) -> Path:
    dump_path = OUTPUT_DIR / f"{gdx_path.stem}_dump.txt"

    if not gdx_path.exists():
        raise FileNotFoundError(f"GDX file not found: {gdx_path}")

    cmd = f'gdxdump "{gdx_path}"'

    with dump_path.open("w", encoding="utf-8", errors="ignore") as f:
        result = subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return dump_path


def list_gdx_symbols(gdx_path: Path) -> list[str]:
    dump_path = dump_gdx(gdx_path)
    text = dump_path.read_text(encoding="utf-8", errors="ignore")

    symbols = set()

    for pattern in [
        r"Set\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"Parameter\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"Variable\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"Equation\s+([A-Za-z_][A-Za-z0-9_]*)",
    ]:
        symbols.update(re.findall(pattern, text))

    return sorted(symbols)


def build_symbol_inventory() -> dict:
    inventory = {
        "baseline_gdx": str(BASELINE_GDX),
        "baseline_available": BASELINE_GDX.exists(),
        "symbols": [],
    }

    if BASELINE_GDX.exists():
        inventory["symbols"] = list_gdx_symbols(BASELINE_GDX)

    out = OUTPUT_DIR / "baseline_symbol_inventory.json"
    out.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    return inventory


def compare_baseline_scenario() -> dict:
    return {
        "baseline_gdx_available": BASELINE_GDX.exists(),
        "scenario_gdx_available": SCENARIO_GDX.exists(),
        "message": (
            "Baseline GDX is available. Scenario GDX comparison will activate "
            "after Signal creates scenario.gdx from a policy shock."
        ),
        "results": {
            "GDP/output effect": 0.0,
            "household income effect": 0.0,
            "trade effect": 0.0,
        },
        "results_table": [
            {"metric": "GDP/output", "effect": 0.0},
            {"metric": "Household income", "effect": 0.0},
            {"metric": "Trade", "effect": 0.0},
            {"metric": "Result type", "effect": "gdx_ready_pending_symbol_mapping"},
        ],
        "chart_data": [
            {"metric": "GDP/output", "effect": 0.0},
            {"metric": "Household income", "effect": 0.0},
            {"metric": "Trade", "effect": 0.0},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_symbol_inventory(), indent=2))
    print(json.dumps(compare_baseline_scenario(), indent=2))

# =========================================================
# BACKWARD COMPATIBILITY WRAPPER
# =========================================================

def read_all_numeric_results():
    """
    Compatibility wrapper for dashboard modules.

    Returns lightweight dashboard-ready numeric structures
    until full symbol mapping is connected.
    """

    try:
        comparison = compare_baseline_scenario()

        results = comparison.get("results", {})

        return {
            "macro": [
                {
                    "metric": "GDP/output",
                    "value": results.get("GDP/output effect", 0.0),
                },
                {
                    "metric": "Household income",
                    "value": results.get("household income effect", 0.0),
                },
                {
                    "metric": "Trade",
                    "value": results.get("trade effect", 0.0),
                },
            ],

            "welfare": [
                {
                    "metric": "Household income",
                    "value": results.get("household income effect", 0.0),
                }
            ],

            "trade": [
                {
                    "metric": "Trade",
                    "value": results.get("trade effect", 0.0),
                }
            ],
        }

    except Exception:

        return {
            "macro": [],
            "welfare": [],
            "trade": [],
        }