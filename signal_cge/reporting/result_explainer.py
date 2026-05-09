"""Plain-language interpretation of Signal model results."""

from __future__ import annotations

from typing import Any


def explain_results(run_result: dict[str, Any]) -> dict[str, Any]:
    scenario = run_result.get("scenario", {})
    results = run_result.get("results", {})
    diagnostics = run_result.get("diagnostics", {})
    accounts = results.get("accounts", {})
    top = sorted(accounts.items(), key=lambda item: abs(float(item[1])), reverse=True)[:5]
    warnings = _collect_warnings(diagnostics)
    return {
        "executive_summary": (
            f"Signal tested '{scenario.get('scenario_name', 'the selected scenario')}' using "
            f"{run_result.get('backend', 'the selected backend')}. The largest modeled effects are concentrated in "
            f"{', '.join(account for account, _ in top) if top else 'the targeted accounts'}."
        ),
        "key_macro_results": "The SAM multiplier reports direct and indirect account effects, not a full equilibrium GDP forecast.",
        "sectoral_output_effects": _format_effects(results.get("activities", {})),
        "factor_income_effects": _format_effects(results.get("factors", {})),
        "household_income_effects": _format_effects(results.get("households", {})),
        "gender_care_effects": _gender_care_text(results),
        "fiscal_implications": _fiscal_text(scenario),
        "policy_risks": warnings or ["No critical warning was raised by the screening diagnostics."],
        "caveats": [
            "Python SAM multipliers are linear and fixed-price; they do not replace a calibrated CGE closure.",
            "Results depend on SAM quality, account mapping, and the stated closure rule.",
        ],
        "recommended_next_steps": [
            "Review diagnostics before using results in policy advice.",
            "Run the same scenario in the GAMS-backed CGE model when the model files and GAMS runtime are available.",
            "Document all account mappings and closure assumptions in the run archive.",
        ],
    }


def explanation_to_markdown(explanation: dict[str, Any]) -> str:
    sections = [
        ("Executive summary", explanation.get("executive_summary", "")),
        ("Key macro results", explanation.get("key_macro_results", "")),
        ("Sectoral output effects", explanation.get("sectoral_output_effects", "")),
        ("Factor income effects", explanation.get("factor_income_effects", "")),
        ("Household income effects", explanation.get("household_income_effects", "")),
        ("Gender-care effects", explanation.get("gender_care_effects", "")),
        ("Fiscal implications", explanation.get("fiscal_implications", "")),
        ("Policy risks", _bullets(explanation.get("policy_risks", []))),
        ("Caveats", _bullets(explanation.get("caveats", []))),
        ("Recommended next steps", _bullets(explanation.get("recommended_next_steps", []))),
    ]
    return "\n\n".join(f"## {title}\n\n{body}" for title, body in sections).strip() + "\n"


def _format_effects(effects: dict[str, float]) -> str:
    if not effects:
        return "No matching accounts were identified in this result group."
    ordered = sorted(effects.items(), key=lambda item: abs(float(item[1])), reverse=True)[:8]
    return "; ".join(f"{account}: {float(value):,.3f}" for account, value in ordered)


def _gender_care_text(results: dict[str, Any]) -> str:
    factors = results.get("factors", {})
    care_hits = {key: value for key, value in factors.items() if key.lower() in {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"}}
    if not care_hits:
        return "Gender-care factor suffixes were not found in the active SAM results."
    return _format_effects(care_hits)


def _fiscal_text(scenario: dict[str, Any]) -> str:
    if scenario.get("shock_type") == "tax":
        return "The scenario directly changes tax rates; revenue and government savings assumptions should be reviewed."
    if scenario.get("shock_type") == "public_investment":
        return "The scenario requires a visible financing assumption for public investment."
    return "No direct fiscal instrument was specified."


def _collect_warnings(diagnostics: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for block in diagnostics.values():
        if isinstance(block, dict):
            warnings.extend(str(item) for item in block.get("warnings", []))
    return warnings


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None"
