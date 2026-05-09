"""Markdown policy report generation for Signal CGE runs."""

from __future__ import annotations

from pathlib import Path

from .interpreter import interpret_results


def generate_policy_report(result: dict[str, object], output_path: str | Path) -> str:
    interpretation = interpret_results(result)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Signal CGE Policy Report",
        "",
        f"Run ID: `{result.get('run_id', 'unknown')}`",
        f"Status: `{result.get('status', 'unknown')}`",
        f"Backend: `{result.get('backend', 'unknown')}`",
        "",
        "## Core Impacts",
        "",
        f"- GDP impact: {interpretation['gdp_impact']}%",
        f"- Household welfare impact: {interpretation['household_welfare_impact']}%",
        f"- Sectoral output impact: {interpretation['sectoral_output_impact']}%",
        f"- Employment/factor income impact: {interpretation['employment_factor_income_impact']}%",
        f"- Government revenue impact: {interpretation['government_revenue_impact']}%",
        f"- Trade impact: {interpretation['trade_impact']}%",
        f"- Distributional impact: {interpretation['distributional_impact']}%",
        "",
        "## Key Policy Messages",
        "",
    ]
    lines.extend(f"- {message}" for message in interpretation["key_policy_messages"])
    lines.extend(["", "## Solver Note", "", str(interpretation["solver_note"]), ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)
