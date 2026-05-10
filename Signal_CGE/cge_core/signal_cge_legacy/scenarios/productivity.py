"""Productivity scenario helpers."""


def productivity_prompt(target: str, percent: float = 5) -> str:
    return f"Increase {target} productivity by {percent}%"
