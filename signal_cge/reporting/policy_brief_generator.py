"""Markdown policy brief generation for Signal CGE Workbench."""

from __future__ import annotations

from typing import Any

from .result_explainer import explain_results


def generate_policy_brief(run_result: dict[str, Any]) -> str:
    scenario = run_result.get("scenario", {})
    diagnostics = run_result.get("diagnostics", {})
    explanation = explain_results(run_result)
    return f"""# Signal CGE Policy Simulation Brief

## 1. Scenario tested

{scenario.get("scenario_name", "Scenario not named")}  
Shock: {scenario.get("shock_type", "not specified")}  
Targets: {", ".join(map(str, scenario.get("target_accounts", [])))}  
Shock size: {scenario.get("shock_value", 0)} {scenario.get("shock_unit", "")}

## 2. Model setup

Backend: {run_result.get("backend", "not specified")}  
AI assistance was used for scenario setup, diagnostics, interpretation, and documentation. The economic model remains the source of simulated results.

## 3. Closure assumptions

{scenario.get("closure_rule", "standard_sam_multiplier")}

## 4. Baseline validation

{_diagnostic_summary(diagnostics.get("pre_run", diagnostics))}

## 5. Simulation results

{explanation["key_macro_results"]}

## 6. Distributional effects

Households: {explanation["household_income_effects"]}  
Factors: {explanation["factor_income_effects"]}

## 7. Gender-care effects

{explanation["gender_care_effects"]}

## 8. Policy interpretation

{explanation["executive_summary"]}

## 9. Risks and limitations

{_bullets(explanation["policy_risks"] + explanation["caveats"])}

## 10. Recommendations

{_bullets(explanation["recommended_next_steps"])}
"""


def _diagnostic_summary(diagnostics: dict[str, Any]) -> str:
    if not diagnostics:
        return "No diagnostics were supplied."
    warnings: list[str] = []
    errors: list[str] = []
    for block in diagnostics.values() if all(isinstance(v, dict) for v in diagnostics.values()) else [diagnostics]:
        if isinstance(block, dict):
            warnings.extend(map(str, block.get("warnings", [])))
            errors.extend(map(str, block.get("errors", [])))
    status = "Passed with warnings" if warnings else "Passed"
    if errors:
        status = "Failed"
    return f"Status: {status}\n\n{_bullets(errors + warnings) if errors or warnings else 'No validation warnings were raised.'}"


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None"
