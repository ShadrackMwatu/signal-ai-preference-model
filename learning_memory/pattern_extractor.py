"""Extract reusable learning patterns from Signal run outputs."""

from __future__ import annotations

from typing import Any

from backends.gams.gams_runner import GAMS_UNAVAILABLE_MESSAGE


def extract_error_patterns(run_result: dict[str, Any]) -> list[str]:
    """Classify errors and warnings without storing raw sensitive inputs."""

    message = str(run_result.get("message", "")).lower()
    validation = run_result.get("validation", {}) or {}
    errors = [str(error).lower() for error in validation.get("errors", [])]
    warnings = [str(warning).lower() for warning in validation.get("warnings", [])]
    patterns: list[str] = []

    if GAMS_UNAVAILABLE_MESSAGE.lower() in message:
        patterns.append("gams_unavailable")
    if any("unknown set" in error for error in errors):
        patterns.append("unknown_set_reference")
    if any("sam" in error and "missing" in error for error in errors):
        patterns.append("missing_sam_parameter")
    if validation.get("sam_balanced") is False:
        patterns.append("sam_imbalance")
    if any("default solver" in warning for warning in warnings):
        patterns.append("unspecified_production_solver")
    if "not production-grade" in message:
        patterns.append("experimental_solver_used")
    return sorted(set(patterns))


def extract_result_patterns(run_result: dict[str, Any]) -> list[str]:
    """Classify useful outcome patterns from model metrics."""

    metrics = run_result.get("metrics", {}) or {}
    patterns: list[str] = []
    gdp = float(metrics.get("gdp_impact", 0.0))
    welfare = float(metrics.get("household_welfare_impact", 0.0))
    revenue = float(metrics.get("government_revenue_impact", 0.0))

    patterns.append("positive_gdp_response" if gdp >= 0 else "negative_gdp_response")
    patterns.append("positive_welfare_response" if welfare >= 0 else "negative_welfare_response")
    patterns.append("positive_revenue_response" if revenue >= 0 else "negative_revenue_response")
    if abs(gdp) < 0.01:
        patterns.append("near_zero_macro_response")
    return sorted(set(patterns))


def extract_diagnostics(run_result: dict[str, Any]) -> list[str]:
    validation = run_result.get("validation", {}) or {}
    diagnostics: list[str] = []
    diagnostics.extend(str(error) for error in validation.get("errors", []))
    diagnostics.extend(str(warning) for warning in validation.get("warnings", []))
    if validation.get("sam_balanced") is True:
        diagnostics.append("SAM balance passed selected tolerance.")
    elif validation.get("sam_balanced") is False:
        diagnostics.append("SAM balance failed selected tolerance.")
    return diagnostics
