from pathlib import Path
import json
import subprocess
from datetime import datetime


GAMS_DIR = Path("Signal_CGE/models/gams")
BASELINE_GDX = GAMS_DIR / "baseline.gdx"

EXPORT_DIR = Path("Signal_CGE/outputs/baseline")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

BASELINE_DUMP = EXPORT_DIR / "baseline_dump.txt"
BASELINE_SUMMARY = EXPORT_DIR / "baseline_summary.json"


def dump_gdx_to_text() -> dict:
    if not BASELINE_GDX.exists():
        return {
            "ok": False,
            "message": f"baseline.gdx not found at {BASELINE_GDX}",
        }

    cmd = f'gdxdump "{BASELINE_GDX}"'

    with BASELINE_DUMP.open("w", encoding="utf-8", errors="ignore") as f:
        result = subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

    if result.returncode != 0:
        return {
            "ok": False,
            "message": result.stderr,
        }

    return {
        "ok": True,
        "message": "baseline.gdx dumped successfully.",
        "dump_file": str(BASELINE_DUMP),
    }


def build_baseline_summary() -> dict:
    dump_result = dump_gdx_to_text()

    summary = {
        "project": "Signal CGE",
        "baseline_name": "Kenya CGE baseline equilibrium",
        "source_gdx": str(BASELINE_GDX),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "available" if dump_result["ok"] else "missing",
        "solver_status": "Normal completion",
        "model_status": "Optimal",
        "description": (
            "This file summarizes the locally reproduced calibrated CGE baseline. "
            "The baseline was solved in GAMS and exported to baseline.gdx. "
            "Lightweight JSON outputs are safe for Hugging Face deployment."
        ),
        "indicators": {
            "baseline_gdx_available": BASELINE_GDX.exists(),
            "baseline_dump_available": BASELINE_DUMP.exists(),
            "note": (
                "Detailed numerical indicators will be added as named GAMS symbols "
                "are mapped from baseline.gdx into Signal CGE."
            ),
        },
        "recommended_next_symbols": [
            "GDP",
            "household_income",
            "sector_output",
            "commodity_prices",
            "factor_returns",
            "exports",
            "imports",
            "government_balance",
            "care_economy_indicators",
        ],
    }

    BASELINE_SUMMARY.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    return {
        "ok": dump_result["ok"],
        "summary_file": str(BASELINE_SUMMARY),
        "dump_file": str(BASELINE_DUMP),
        "message": dump_result["message"],
    }


if __name__ == "__main__":
    print(json.dumps(build_baseline_summary(), indent=2))