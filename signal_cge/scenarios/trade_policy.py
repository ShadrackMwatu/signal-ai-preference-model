"""Trade policy scenario helpers."""


def export_facilitation_prompt(percent: float = 10) -> str:
    return f"Run a trade facilitation shock for exports of {percent}%"
