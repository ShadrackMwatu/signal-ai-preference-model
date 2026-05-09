"""Markdown formatters for AI CGE Chat Studio responses."""

from __future__ import annotations

from typing import Any


def format_diagnostics(result: dict[str, Any]) -> str:
    diagnostics = result.get("diagnostics", {})
    warnings = result.get("warnings", [])
    intent = diagnostics.get("intent", {})
    validation = diagnostics.get("validation", {})
    lines = [
        "## Diagnostics",
        f"- Intent: `{intent.get('intent', 'unknown')}`",
        f"- Domain: `{intent.get('domain', 'unknown')}`",
        f"- Scenario valid: `{validation.get('valid', False)}`",
    ]
    errors = validation.get("errors", [])
    if errors:
        lines.extend(["", "### Errors", *_bullets(errors)])
    if warnings:
        lines.extend(["", "### Warnings", *_bullets(warnings)])
    else:
        lines.extend(["", "### Warnings", "- No warnings were raised."])
    return "\n".join(lines)


def format_results_summary(result: dict[str, Any]) -> str:
    results = result.get("results", {})
    accounts = results.get("accounts", {})
    ranking = sorted(accounts.items(), key=lambda item: abs(float(item[1])), reverse=True)[:8]
    lines = ["## Results Summary"]
    if not ranking:
        lines.append("- No account-level results were produced.")
    else:
        lines.append("| Account | Effect |")
        lines.append("|---|---:|")
        for account, value in ranking:
            lines.append(f"| `{account}` | {float(value):,.3f} |")
    zero_columns = results.get("zero_columns", [])
    if zero_columns:
        lines.extend(["", "### Zero-column accounts", *_bullets(zero_columns)])
    return "\n".join(lines)


def format_policy_explanation(result: dict[str, Any]) -> str:
    summary = result.get("policy_summary", {})
    channels = result.get("explanation", {}).get("transmission_channels", [])
    lines = [
        "## Policy Summary",
        summary.get("executive_summary", "No executive summary was produced."),
        "",
        "### Transmission Channel",
        summary.get("expected_transmission_channel", ""),
    ]
    if channels:
        lines.extend(["", "### Mechanism Checks", *_bullets(channels)])
    lines.extend(
        [
            "",
            "### Likely Winners",
            *_bullets(summary.get("likely_winners", [])),
            "",
            "### Risks",
            *_bullets(summary.get("likely_risks", [])),
            "",
            "### Caveat",
            summary.get("interpretation_caveat", ""),
        ]
    )
    return "\n".join(lines)


def format_recommendations(result: dict[str, Any]) -> str:
    recommendations = result.get("policy_summary", {}).get("suggested_next_simulations", [])
    return "\n".join(["## Recommended Next Simulations", *_bullets(recommendations)])


def _bullets(items: list[Any]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- None"]
