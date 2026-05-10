from pathlib import Path
from datetime import datetime
from typing import Any

RESULT_DIR = Path("Signal_CGE/models/gams/70_Result")

GDX_FILE_CATEGORIES = {
    "sta_TEST_resmacro.gdx": "Macroeconomic results",
    "sta_TEST_reswelf.gdx": "Welfare results",
    "sta_TEST_resLevel.gdx": "Detailed level results",
    "sta_TEST_resLevelAggr.gdx": "Aggregated level results",
    "sta_TEST_resDiffBase.gdx": "Changes from baseline",
    "sta_TEST_resPerBase.gdx": "Percentage changes from baseline",
    "sta_TEST_resPerBaseAggr.gdx": "Aggregated percentage changes",
    "sta_TEST_resstruct.gdx": "Structural/account results",
}


def _format_modified_time(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")


def list_gdx_results(result_dir: Path | str = RESULT_DIR) -> list[dict[str, Any]]:
    """
    List expected GAMS GDX result files from 70_Result.

    This function is safe for Hugging Face:
    if files are absent, it returns an empty list instead of crashing.
    """

    result_dir = Path(result_dir)

    if not result_dir.exists():
        return []

    rows = []

    for file_name, category in GDX_FILE_CATEGORIES.items():
        path = result_dir / file_name

        if path.exists():
            rows.append(
                {
                    "file_name": file_name,
                    "category": category,
                    "path": str(path),
                    "size_kb": round(path.stat().st_size / 1024, 2),
                    "modified": _format_modified_time(path),
                    "status": "Found",
                    "message": "GDX file found. Detailed parsing requires GAMS Python API or gdxdump.",
                }
            )
        else:
            rows.append(
                {
                    "file_name": file_name,
                    "category": category,
                    "path": str(path),
                    "size_kb": 0,
                    "modified": "",
                    "status": "Missing",
                    "message": "GDX file not found. Run the model locally to generate this output.",
                }
            )

    return rows


def summarize_gdx_results(result_dir: Path | str = RESULT_DIR) -> dict[str, Any]:
    rows = list_gdx_results(result_dir)

    found = [row for row in rows if row["status"] == "Found"]
    missing = [row for row in rows if row["status"] == "Missing"]

    return {
        "result_dir": str(Path(result_dir)),
        "files_found": len(found),
        "files_missing": len(missing),
        "rows": rows,
        "has_results": len(found) > 0,
    }


if __name__ == "__main__":
    summary = summarize_gdx_results()

    print("Signal CGE GAMS Result Files")
    print("============================")
    print(f"Result directory: {summary['result_dir']}")
    print(f"Files found: {summary['files_found']}")
    print(f"Files missing: {summary['files_missing']}")

    for row in summary["rows"]:
        print(f"{row['status']}: {row['file_name']} - {row['category']}")