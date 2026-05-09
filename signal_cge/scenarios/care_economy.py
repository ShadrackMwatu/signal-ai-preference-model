"""Care economy scenario helpers."""

CARE_SUFFIXES = ["fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"]


def care_infrastructure_prompt(percent: float = 20) -> str:
    return f"Increase public investment in care infrastructure by {percent}%"
