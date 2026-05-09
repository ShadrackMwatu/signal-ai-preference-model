"""SAM loading helpers for Signal CGE."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_sam(path: str | Path) -> pd.DataFrame:
    """Load a SAM matrix from CSV or Excel using the first column as accounts."""

    source = Path(path)
    if source.suffix.lower() in {".xlsx", ".xls"}:
        frame = pd.read_excel(source, index_col=0)
    else:
        frame = pd.read_csv(source, index_col=0)
    frame.index = [str(account).strip() for account in frame.index]
    frame.columns = [str(account).strip() for account in frame.columns]
    return frame.apply(pd.to_numeric, errors="raise").astype(float)
