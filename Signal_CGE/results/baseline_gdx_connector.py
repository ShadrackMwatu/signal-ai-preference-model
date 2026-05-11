from pathlib import Path
import subprocess


GAMS_DIR = Path("Signal_CGE/models/gams")
BASELINE_GDX = GAMS_DIR / "baseline.gdx"
BASELINE_DUMP = GAMS_DIR / "baseline_dump.txt"


def baseline_exists() -> bool:
    return BASELINE_GDX.exists()


def dump_baseline_gdx() -> dict:
    if not BASELINE_GDX.exists():
        return {
            "ok": False,
            "message": f"Baseline GDX not found: {BASELINE_GDX}",
            "dump_file": None,
        }

    cmd = ["gdxdump", str(BASELINE_GDX)]

    with BASELINE_DUMP.open("w", encoding="utf-8") as f:
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
            "dump_file": None,
        }

    return {
        "ok": True,
        "message": "Baseline GDX dumped successfully.",
        "dump_file": str(BASELINE_DUMP),
    }


if __name__ == "__main__":
    print(dump_baseline_gdx())