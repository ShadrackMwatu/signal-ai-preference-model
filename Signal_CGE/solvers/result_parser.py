from typing import Any
import pandas as pd

try:
    from Signal_CGE.solvers.gdx_reader import summarize_gdx_results
except Exception:
    from gdx_reader import summarize_gdx_results


def build_results_dataframe() -> pd.DataFrame:
    summary = summarize_gdx_results()
    rows = summary.get("rows", [])

    if not rows:
        return pd.DataFrame(
            [
                {
                    "file_name": "No local GAMS results found",
                    "category": "No results",
                    "status": "Missing",
                    "size_kb": 0,
                    "modified": "",
                    "message": "Run the model locally or upload/export parsed results.",
                }
            ]
        )

    return pd.DataFrame(rows)


def build_diagnostics_dataframe() -> pd.DataFrame:
    summary = summarize_gdx_results()

    return pd.DataFrame(
        [
            {
                "diagnostic": "Result directory",
                "value": summary.get("result_dir", ""),
            },
            {
                "diagnostic": "GDX files found",
                "value": summary.get("files_found", 0),
            },
            {
                "diagnostic": "GDX files missing",
                "value": summary.get("files_missing", 0),
            },
            {
                "diagnostic": "Has local GAMS results",
                "value": summary.get("has_results", False),
            },
        ]
    )


def build_summary_text() -> str:
    summary = summarize_gdx_results()

    if not summary.get("has_results"):
        return (
            "No local GAMS results found. "
            "Run the model locally or upload/export parsed results."
        )

    return (
        "Signal CGE found real GAMS output files in 70_Result. "
        f"{summary.get('files_found', 0)} result files are available for display."
    )


def build_interpretation_text() -> str:
    summary = summarize_gdx_results()

    if not summary.get("has_results"):
        return (
            "The Hugging Face cloud environment does not contain local GAMS outputs. "
            "This is expected unless the model has been run locally or parsed outputs "
            "have been exported into the app environment."
        )

    return (
        "The available GAMS result files indicate that the model has produced "
        "macroeconomic, welfare, level, percentage-change, baseline-difference, "
        "and structural outputs. These files can now feed the Signal CGE Results Window. "
        "Detailed numerical extraction from GDX will require the GAMS Python API or gdxdump."
    )


def parse_signal_cge_results() -> dict[str, Any]:
    return {
        "summary_text": build_summary_text(),
        "results_dataframe": build_results_dataframe(),
        "diagnostics_dataframe": build_diagnostics_dataframe(),
        "interpretation_text": build_interpretation_text(),
    }


if __name__ == "__main__":
    parsed = parse_signal_cge_results()

    print(parsed["summary_text"])
    print()
    print(parsed["results_dataframe"])
    print()
    print(parsed["diagnostics_dataframe"])
    print()
    print(parsed["interpretation_text"])

def parse_signal_results():
    parsed = parse_signal_cge_results()
    return (
        parsed["summary_text"],
        parsed["results_dataframe"],
        parsed["diagnostics_dataframe"],
        parsed["interpretation_text"],
    )