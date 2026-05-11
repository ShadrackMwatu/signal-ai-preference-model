import pandas as pd

try:
    from Signal_CGE.results.gdx_numeric_reader import read_all_numeric_results
except Exception:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(ROOT))

    from Signal_CGE.results.gdx_numeric_reader import read_all_numeric_results


def _load_numeric_results() -> dict:
    try:
        data = read_all_numeric_results(max_lines_per_file=500)
        if isinstance(data, dict):
            return data
        return {}
    except Exception:
        return {}


def _records_to_dataframe(records, columns: list[str]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame(columns=columns)

    frame = pd.DataFrame(records)

    for column in columns:
        if column not in frame.columns:
            frame[column] = None

    return frame[columns]


def build_macro_dashboard() -> pd.DataFrame:
    data = _load_numeric_results()
    records = data.get("macro", [])

    frame = _records_to_dataframe(records, ["metric", "value"])

    if frame.empty:
        return pd.DataFrame(
            [
                {
                    "indicator": "none",
                    "value": None,
                    "status": "No macro indicators detected",
                }
            ]
        )

    frame = frame.rename(columns={"metric": "indicator"})
    frame["status"] = "GDX pipeline ready"

    return frame[["indicator", "value", "status"]]


def build_welfare_dashboard() -> pd.DataFrame:
    data = _load_numeric_results()
    records = data.get("welfare", [])

    frame = _records_to_dataframe(records, ["metric", "value"])

    if frame.empty:
        return pd.DataFrame(
            [
                {
                    "group": "none",
                    "value": None,
                    "status": "No welfare indicators detected",
                }
            ]
        )

    frame = frame.rename(columns={"metric": "group"})
    frame["status"] = "GDX pipeline ready"

    return frame[["group", "value", "status"]]


def build_trade_dashboard() -> pd.DataFrame:
    data = _load_numeric_results()
    records = data.get("trade", [])

    frame = _records_to_dataframe(records, ["metric", "value"])

    if frame.empty:
        return pd.DataFrame(
            [
                {
                    "trade_indicator": "none",
                    "value": None,
                    "status": "No trade indicators detected",
                }
            ]
        )

    frame = frame.rename(columns={"metric": "trade_indicator"})
    frame["status"] = "GDX pipeline ready"

    return frame[["trade_indicator", "value", "status"]]


if __name__ == "__main__":
    print("Signal CGE Dashboard Tables")
    print("===========================")

    print()
    print("MACRO DASHBOARD")
    print(build_macro_dashboard())

    print()
    print("WELFARE DASHBOARD")
    print(build_welfare_dashboard())

    print()
    print("TRADE DASHBOARD")
    print(build_trade_dashboard())