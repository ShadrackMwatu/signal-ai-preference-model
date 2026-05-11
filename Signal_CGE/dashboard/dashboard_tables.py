import pandas as pd

try:
    from Signal_CGE.results.gdx_numeric_reader import read_all_numeric_results
except Exception:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(ROOT))

    from Signal_CGE.results.gdx_numeric_reader import read_all_numeric_results

MACRO_KEYWORDS = {
    "GDP": ["stQGDPTOT", "stQGDTOT"],
    "Consumption": ["stQCDTOT"],
    "Investment": ["stQINVTOT"],
    "Absorption": ["stQABSORP"],
    "Exports": ["EXP", "EXPORT"],
    "Imports": ["IMP", "IMPORT"],
}


def _find_matches(df: pd.DataFrame, keywords: list[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    mask = df["raw_line"].astype(str).str.contains(
        "|".join(keywords),
        case=False,
        na=False,
    )

    return df[mask].copy()


def build_macro_dashboard() -> pd.DataFrame:
    df = read_all_numeric_results(max_lines_per_file=500)

    dashboard_rows = []

    for indicator, keywords in MACRO_KEYWORDS.items():
        subset = _find_matches(df, keywords)

        if subset.empty:
            dashboard_rows.append(
                {
                    "indicator": indicator,
                    "value": None,
                    "status": "Not detected",
                }
            )
            continue

        value = pd.to_numeric(
            subset["numeric_value"],
            errors="coerce",
        ).dropna()

        dashboard_rows.append(
            {
                "indicator": indicator,
                "value": float(value.mean()) if len(value) else None,
                "status": "Detected",
            }
        )

    return pd.DataFrame(dashboard_rows)


def build_welfare_dashboard() -> pd.DataFrame:
    df = read_all_numeric_results(max_lines_per_file=500)

    welfare = df[
        df["category"].astype(str).str.contains(
            "welfare",
            case=False,
            na=False,
        )
    ].copy()

    if welfare.empty:
        return pd.DataFrame(
            [
                {
                    "group": "none",
                    "value": None,
                    "status": "No welfare results detected",
                }
            ]
        )

    welfare["numeric_value"] = pd.to_numeric(
        welfare["numeric_value"],
        errors="coerce",
    )

    grouped = (
        welfare.groupby("source_file")["numeric_value"]
        .mean()
        .reset_index()
    )

    grouped.columns = ["group", "value"]

    grouped["status"] = "Detected"

    return grouped


def build_trade_dashboard() -> pd.DataFrame:
    df = read_all_numeric_results(max_lines_per_file=500)

    trade = df[
        df["raw_line"].astype(str).str.contains(
            "EXP|IMP|trade|export|import",
            case=False,
            na=False,
        )
    ].copy()

    if trade.empty:
        return pd.DataFrame(
            [
                {
                    "trade_indicator": "none",
                    "value": None,
                    "status": "No trade indicators detected",
                }
            ]
        )

    trade["numeric_value"] = pd.to_numeric(
        trade["numeric_value"],
        errors="coerce",
    )

    return trade[
        [
            "raw_line",
            "numeric_value",
        ]
    ].rename(
        columns={
            "raw_line": "trade_indicator",
            "numeric_value": "value",
        }
    )


def build_care_dashboard() -> pd.DataFrame:
    df = read_all_numeric_results(max_lines_per_file=500)

    care = df[
        df["raw_line"].astype(str).str.contains(
            "fcp|fcu|fnp|fnu|mcp|mcu|mnp|mnu",
            case=False,
            na=False,
        )
    ].copy()

    if care.empty:
        return pd.DataFrame(
            [
                {
                    "care_group": "none",
                    "value": None,
                    "status": "No care-economy indicators detected",
                }
            ]
        )

    care["numeric_value"] = pd.to_numeric(
        care["numeric_value"],
        errors="coerce",
    )

    return care[
        [
            "raw_line",
            "numeric_value",
        ]
    ].rename(
        columns={
            "raw_line": "care_group",
            "numeric_value": "value",
        }
    )


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
    print(build_trade_dashboard().head(20))

    print()
    print("CARE ECONOMY DASHBOARD")
    print(build_care_dashboard().head(20))