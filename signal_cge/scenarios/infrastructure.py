"""Infrastructure scenario helpers."""


def transport_productivity_prompt(percent: float = 5) -> str:
    return f"Increase transport productivity by {percent}%"
