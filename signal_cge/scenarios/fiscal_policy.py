"""Fiscal policy scenario helpers."""

from .scenario_schema import parse_scenario_prompt


def vat_change_prompt(percent: float, target: str = "manufacturing") -> str:
    return f"Simulate a {percent}% VAT change on {target}"
