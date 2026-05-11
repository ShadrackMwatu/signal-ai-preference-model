from pathlib import Path
from typing import Any
import subprocess
import pandas as pd


RESULT_DIR = Path("Signal_CGE/models/gams/70_Result")

GDX_FILES = {
    "macro": "sta_TEST_resmacro.gdx",
    "welfare": "sta_TEST_reswelf.gdx",
    "level": "sta_TEST_resLevel.gdx",
    "level_aggregated": "sta_TEST_resLevelAggr.gdx",
    "difference_from_base": "sta_TEST_resDiffBase.gdx",
    "percentage_from_base": "sta_TEST_resPerBase.gdx",
    "percentage_from_base_aggregated": "sta_TEST_resPerBaseAggr.gdx",
    "structure": "sta_TEST_resstruct.gdx",
}


def _safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def _run_gdxdump(gdx_path: Path) -> str:
    """
    Use gdxdump to convert a GDX file into readable text.

    This works when GAMS tools are available on PATH.
    If gdxdump is not available, the function returns an empty string.
    """

    try:
        result = subprocess.run(
            ["gdxdump", str(gdx_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            return ""

        return result.stdout

    except Exception:
        return ""


def read_gdx_as_text(category: str) -> dict[str, Any]:
    """
    Read one GDX result file as raw text using gdxdump.

    This is the first practical numerical extraction layer.
    """

    file_name = GDX_FILES.get(category)

    if not file_name:
        return {
            "success": False,
            "category": category,
            "message": f"Unknown GDX category: {category}",
            "text": "",
        }

    gdx_path = RESULT_DIR / file_name

    if not gdx_path.exists():
        return {
            "success": False,
            "category": category,
            "file_name": file_name,
            "message": f"GDX file not found: {gdx_path}",
            "text": "",
        }

    text = _run_gdxdump(gdx_path)

    if not text:
        return {
            "success": False,
            "category": category,
            "file_name": file_name,
            "path": str(gdx_path),
            "message": (
                "GDX file exists, but gdxdump could not extract text. "
                "Confirm that GAMS tools are on PATH."
            ),
            "text": "",
        }

    return {
        "success": True,
        "category": category,
        "file_name": file_name,
        "path": str(gdx_path),
        "message": "GDX text extracted successfully using gdxdump.",
        "text": text,
    }


def extract_numeric_lines(category: str, max_lines: int = 200) -> pd.DataFrame:
    """
    Extract readable numeric-looking rows from a GDX dump.

    This is intentionally generic because GDX symbol structures vary.
    Later we can specialize this for GDP, welfare, trade, prices, employment, etc.
    """

    payload = read_gdx_as_text(category)

    if not payload.get("success"):
        return pd.DataFrame(
            [
                {
                    "category": category,
                    "source_file": payload.get("file_name", ""),
                    "raw_line": "",
                    "numeric_value": None,
                    "message": payload.get("message", ""),
                }
            ]
        )

    rows = []

    for line in payload["text"].splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        parts = stripped.replace(",", " ").replace("=", " ").split()

        numeric_values = [_safe_float(part) for part in parts]
        numeric_values = [value for value in numeric_values if value is not None]

        if numeric_values:
            rows.append(
                {
                    "category": category,
                    "source_file": payload["file_name"],
                    "raw_line": stripped[:300],
                    "numeric_value": numeric_values[-1],
                    "message": "numeric line detected",
                }
            )

        if len(rows) >= max_lines:
            break

    if not rows:
        rows.append(
            {
                "category": category,
                "source_file": payload["file_name"],
                "raw_line": "",
                "numeric_value": None,
                "message": "No numeric lines detected in gdxdump output.",
            }
        )

    return pd.DataFrame(rows)


def read_all_numeric_results(max_lines_per_file: int = 100) -> pd.DataFrame:
    """
    Read all available GDX result files and return numeric-looking rows.
    """

    frames = []

    for category in GDX_FILES:
        frame = extract_numeric_lines(category, max_lines=max_lines_per_file)
        frames.append(frame)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def summarize_numeric_results() -> pd.DataFrame:
    """
    Produce a compact dashboard summary by category.
    """

    df = read_all_numeric_results(max_lines_per_file=100)

    if df.empty:
        return pd.DataFrame(
            [
                {
                    "category": "none",
                    "rows_detected": 0,
                    "first_value": None,
                    "mean_detected_value": None,
                    "message": "No numerical GDX data detected.",
                }
            ]
        )

    summary_rows = []

    for category, group in df.groupby("category"):
        numeric = pd.to_numeric(group["numeric_value"], errors="coerce").dropna()

        summary_rows.append(
            {
                "category": category,
                "rows_detected": len(group),
                "first_value": float(numeric.iloc[0]) if len(numeric) else None,
                "mean_detected_value": float(numeric.mean()) if len(numeric) else None,
                "message": "Initial numerical extraction from GDX dump.",
            }
        )

    return pd.DataFrame(summary_rows)


if __name__ == "__main__":
    print("Signal CGE Numerical GDX Reader")
    print("===============================")

    summary = summarize_numeric_results()
    print(summary)

    detail = read_all_numeric_results(max_lines_per_file=10)
    print()
    print("Sample extracted rows:")
    print(detail.head(30))