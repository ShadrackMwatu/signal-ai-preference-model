"""SAM loading, balance checks, and balance-check exports."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd


LONG_FORMAT_COLUMNS = {"row_account", "column_account", "value"}
PII_COLUMNS = {"name", "username", "email", "phone", "user_id", "gps", "latitude", "longitude"}


def load_sam(path: str | Path) -> pd.DataFrame:
    """Load a SAM from CSV or Excel into a square matrix DataFrame."""

    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"SAM file not found: {source}")
    if source.suffix.lower() in {".xlsx", ".xls"}:
        raw = pd.read_excel(source)
    else:
        raw = pd.read_csv(source)
    return sam_to_matrix(raw)


def sam_to_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert long-format or matrix-format SAM data into a square matrix."""

    columns = {str(column).strip().lower() for column in frame.columns}
    pii_hits = columns.intersection(PII_COLUMNS)
    if pii_hits:
        raise ValueError(f"SAM contains disallowed PII column(s): {', '.join(sorted(pii_hits))}")

    if LONG_FORMAT_COLUMNS.issubset(columns):
        normalized = frame.rename(columns={column: str(column).strip().lower() for column in frame.columns})
        normalized["row_account"] = normalized["row_account"].map(_account)
        normalized["column_account"] = normalized["column_account"].map(_account)
        normalized["value"] = pd.to_numeric(normalized["value"], errors="raise").astype(float)
        matrix = normalized.pivot_table(
            index="row_account",
            columns="column_account",
            values="value",
            aggfunc="sum",
            fill_value=0.0,
        )
    else:
        matrix = frame.copy()
        first_column = matrix.columns[0]
        matrix[first_column] = matrix[first_column].map(_account)
        matrix = matrix.set_index(first_column)
        matrix.index = [_account(account) for account in matrix.index]
        matrix.columns = [_account(column) for column in matrix.columns]
        matrix = matrix.apply(pd.to_numeric, errors="raise").astype(float)

    accounts = sorted(set(matrix.index).union(matrix.columns))
    matrix = matrix.reindex(index=accounts, columns=accounts, fill_value=0.0).astype(float)
    if (matrix < 0).any().any():
        raise ValueError("SAM values must be non-negative")
    if matrix.empty:
        raise ValueError("SAM must contain at least one account")
    return matrix


def balance_check(matrix: pd.DataFrame) -> pd.DataFrame:
    """Return row-column balance diagnostics for every SAM account."""

    sam = sam_to_matrix(matrix.reset_index()) if "row_account" in matrix.columns else matrix.astype(float)
    row_total = sam.sum(axis=1)
    column_total = sam.sum(axis=0).reindex(sam.index)
    check = pd.DataFrame(
        {
            "account": sam.index,
            "row_total": row_total.to_numpy(),
            "column_total": column_total.to_numpy(),
        }
    )
    check["imbalance"] = check["row_total"] - check["column_total"]
    denominator = check[["row_total", "column_total"]].max(axis=1).replace(0, 1)
    check["percentage_imbalance"] = check["imbalance"] / denominator
    return check.round(8)


def is_balanced(matrix: pd.DataFrame, tolerance: float = 0.01) -> bool:
    return bool((balance_check(matrix)["percentage_imbalance"].abs() <= tolerance).all())


def export_balance_check(check: pd.DataFrame, output_dir: str | Path = "outputs") -> dict[str, str]:
    """Export balance checks to Markdown and a minimal XLSX workbook."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    markdown_path = destination / "balance_check.md"
    xlsx_path = destination / "balance_check.xlsx"
    markdown_path.write_text(_balance_markdown(check), encoding="utf-8")
    _write_simple_xlsx(check, xlsx_path)
    return {"markdown": str(markdown_path), "excel": str(xlsx_path)}


def _balance_markdown(check: pd.DataFrame) -> str:
    lines = ["# SAM Balance Check", "", "| Account | Row Total | Column Total | Imbalance | Percentage Imbalance |", "|---|---:|---:|---:|---:|"]
    for row in check.to_dict(orient="records"):
        lines.append(
            f"| {row['account']} | {row['row_total']} | {row['column_total']} | "
            f"{row['imbalance']} | {row['percentage_imbalance']} |"
        )
    return "\n".join(lines) + "\n"


def _write_simple_xlsx(frame: pd.DataFrame, path: Path) -> None:
    rows = [list(frame.columns)] + frame.astype(object).values.tolist()
    sheet_rows = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        for column_index, value in enumerate(row, start=1):
            cell_ref = f"{_column_letter(column_index)}{row_index}"
            if isinstance(value, int | float) and not isinstance(value, bool):
                cells.append(f'<c r="{cell_ref}"><v>{value}</v></c>')
            else:
                escaped = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                cells.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{escaped}</t></is></c>')
        sheet_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    with ZipFile(path, "w", ZIP_DEFLATED) as workbook:
        workbook.writestr("[Content_Types].xml", _CONTENT_TYPES)
        workbook.writestr("_rels/.rels", _RELS)
        workbook.writestr("xl/workbook.xml", _WORKBOOK)
        workbook.writestr("xl/_rels/workbook.xml.rels", _WORKBOOK_RELS)
        workbook.writestr(
            "xl/worksheets/sheet1.xml",
            f'<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{"".join(sheet_rows)}</sheetData></worksheet>',
        )


def _column_letter(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def _account(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


_CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>"""
_RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""
_WORKBOOK = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="balance_check" sheetId="1" r:id="rId1"/></sheets></workbook>"""
_WORKBOOK_RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>"""
