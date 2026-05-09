"""Hugging Face app entrypoint for Signal AI Dashboard."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

for _mpl_candidate in [
    Path(os.environ.get("TEMP", "")) / f"signal_ai_matplotlib_{os.getpid()}",
    Path(os.environ.get("LOCALAPPDATA", "")) / "SignalAI" / "matplotlib",
    Path(__file__).resolve().parent / ".cache" / "matplotlib",
    Path(__file__).resolve().parent / "outputs" / "matplotlib",
]:
    try:
        if str(_mpl_candidate):
            _mpl_candidate.mkdir(parents=True, exist_ok=True)
            os.environ.setdefault("MPLCONFIGDIR", str(_mpl_candidate))
            break
    except OSError:
        continue

import gradio as gr

from app_routes.behavioral_route import run_behavioral_signal_prediction
from app_routes.signal_cge_route import run_signal_cge_prompt as route_run_signal_cge_prompt
from app_routes.signal_cge_route import FULL_CGE_FALLBACK_MESSAGE
from explainability import generate_prediction_explanation
from privacy import PRIVACY_NOTICE
from trend_intelligence import analyze_trend_batch, summarize_trend_batch
from x_trends import fetch_x_trends, get_demo_trends
from sml_workbench.exporters.gams_exporter import export_to_gams
from sml_workbench.exporters.pyomo_exporter import export_to_pyomo
from sml_workbench.parser.sml_parser import load_sml_text as load_sml_workbench_text
from sml_workbench.parser.sml_parser import parse_sml
from sml_workbench.validators.sml_validator import validate_sml
from learning.ai_teaching.explainer import explain_concept


ADVANCED_IMPORT_ERROR = ""

try:
    from src.cge.framework import DEFAULT_SCENARIO, run_policy_scenario
    from signal_execution.runner import SignalRunner
    from signal_learning.adaptation_engine import propose_adaptations
    from signal_learning.implementation_engine import implement_adaptation, rollback_adaptation
    from signal_learning.learning_store import LearningStore
    from signal_learning.pattern_extractor import recurring_issue_summary

    ADVANCED_AVAILABLE = True
except Exception as exc:  # pragma: no cover - exercised in constrained Space runtimes.
    ADVANCED_AVAILABLE = False
    ADVANCED_IMPORT_ERROR = str(exc)
    DEFAULT_SCENARIO = "Baseline policy scenario"

try:
    from signal_cge.solvers.gams_runner import find_gams_executable
    from signal_cge.workbench import run_chat_scenario
    from signal_cge.diagnostics.model_readiness import get_model_readiness
    from signal_cge.knowledge.document_loader import load_model_profile
    from signal_cge.knowledge.reference_index import build_reference_index
    from signal_ai.conversation_engine.chat_orchestrator import run_chat_simulation
    from signal_ai.conversation_engine.response_formatting import (
        format_diagnostics,
        format_policy_explanation,
        format_recommendations,
        format_results_summary,
    )

    AI_CGE_WORKBENCH_AVAILABLE = True
    AI_CGE_WORKBENCH_IMPORT_ERROR = ""
except Exception as exc:  # pragma: no cover - keep dashboard usable in minimal runtimes.
    AI_CGE_WORKBENCH_AVAILABLE = False
    AI_CGE_WORKBENCH_IMPORT_ERROR = str(exc)


SML_EXAMPLE_PATH = Path("sml_workbench/examples/kenya_basic_cge_example.sml")
DEFAULT_SML_TEXT = load_sml_workbench_text(SML_EXAMPLE_PATH) if SML_EXAMPLE_PATH.exists() else ""
ROOT_DIR = Path(__file__).resolve().parent
PRIMARY_MODEL_PATH = ROOT_DIR / "models" / "model.pkl"
LEGACY_MODEL_PATH = ROOT_DIR / "model.pkl"
PRIMARY_MODEL_METADATA_PATH = ROOT_DIR / "models" / "metadata.json"
LIVE_TREND_FEATURE_PLUGINS = [
    "Sentiment analysis",
    "Anomaly detection",
    "Emerging issue detection",
    "County heatmaps",
    "Election intelligence",
    "Market pulse indicators",
]
PUBLIC_TABS = ["Behavioral Signals AI", "Signal CGE"]
HIDDEN_PUBLIC_TABS = ["Signal CGE Framework", "AI CGE Chat Studio", "SML CGE Workbench", "Learning"]
SIGNAL_DASHBOARD_CSS = """
.signal-trend-shell {
    border: 1px solid var(--border-color-primary, #dbe3ef);
    border-radius: 8px;
    background: var(--background-fill-primary, #ffffff);
    padding: 14px;
}
.signal-trend-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.signal-trend-kicker {
    color: var(--body-text-color-subdued, #64748b);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0;
    text-transform: uppercase;
}
.signal-trend-title {
    color: var(--body-text-color, #0f172a);
    font-size: 20px;
    font-weight: 800;
    line-height: 1.2;
    margin-top: 2px;
}
.signal-trend-count {
    min-width: 132px;
    border: 1px solid var(--border-color-primary, #dbe3ef);
    border-radius: 8px;
    padding: 10px 12px;
    text-align: right;
    background: var(--background-fill-secondary, #f8fafc);
}
.signal-trend-count strong {
    display: block;
    color: #16a34a;
    font-size: 30px;
    line-height: 1;
}
.signal-trend-count span {
    color: var(--body-text-color-subdued, #64748b);
    font-size: 12px;
    font-weight: 600;
}
.signal-trend-viewport {
    height: 360px;
    overflow: hidden;
    border: 1px solid var(--border-color-primary, #dbe3ef);
    border-radius: 8px;
    background: linear-gradient(180deg, rgba(15,23,42,0.04), rgba(22,163,74,0.06));
    position: relative;
}
.signal-trend-viewport::before,
.signal-trend-viewport::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    height: 56px;
    z-index: 2;
    pointer-events: none;
}
.signal-trend-viewport::before {
    top: 0;
    background: linear-gradient(180deg, var(--background-fill-primary, #ffffff), rgba(255,255,255,0));
}
.signal-trend-viewport::after {
    bottom: 0;
    background: linear-gradient(0deg, var(--background-fill-primary, #ffffff), rgba(255,255,255,0));
}
.signal-trend-rail {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 12px;
    animation: signalTrendScroll var(--signal-trend-duration, 24s) linear infinite;
}
.signal-trend-viewport:hover .signal-trend-rail {
    animation-play-state: paused;
}
.signal-trend-card {
    border: 1px solid var(--border-color-primary, #dbe3ef);
    border-radius: 8px;
    background: var(--background-fill-primary, #ffffff);
    padding: 12px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}
.signal-trend-issue {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    border: 1px solid var(--border-color-primary, #dbe3ef);
    border-radius: 8px;
    background: var(--background-fill-primary, #ffffff);
    padding: 14px 16px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}
.signal-trend-issue-name {
    color: var(--body-text-color, #0f172a);
    font-size: 17px;
    font-weight: 800;
    line-height: 1.25;
}
.signal-trend-issue-meta {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 6px;
}
.signal-trend-card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
}
.signal-trend-name {
    color: var(--body-text-color, #0f172a);
    font-size: 16px;
    font-weight: 800;
    line-height: 1.25;
}
.signal-trend-meta,
.signal-trend-tags,
.signal-trend-intel {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}
.signal-trend-pill {
    border: 1px solid var(--border-color-primary, #dbe3ef);
    border-radius: 999px;
    color: var(--body-text-color-subdued, #475569);
    background: var(--background-fill-secondary, #f8fafc);
    font-size: 12px;
    font-weight: 650;
    padding: 4px 8px;
}
.signal-trend-confidence {
    min-width: 116px;
    text-align: right;
    color: var(--body-text-color, #0f172a);
    font-size: 12px;
    font-weight: 700;
}
.signal-trend-bar {
    height: 7px;
    width: 116px;
    margin-top: 5px;
    border-radius: 999px;
    background: var(--background-fill-secondary, #e2e8f0);
    overflow: hidden;
}
.signal-trend-bar span {
    display: block;
    height: 100%;
    width: var(--confidence-width, 0%);
    border-radius: 999px;
    background: linear-gradient(90deg, #2563eb, #16a34a);
}
.signal-trend-classification {
    color: var(--body-text-color, #0f172a);
    font-size: 13px;
    line-height: 1.45;
    margin-top: 8px;
}
.signal-trend-plugins {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 12px;
}
.signal-trend-debug {
    display: none;
}
@keyframes signalTrendScroll {
    0% { transform: translateY(48%); }
    100% { transform: translateY(-54%); }
}
"""

DISPLAY_LABELS = {
    "Validate Signal Quality": "Emerging Signal — Further Monitoring Recommended",
    "Monitor Further": "Emerging Signal — Further Monitoring Recommended",
    "Weak Signal": "Limited Market Momentum",
    "Possible Noise": "Signal Volatility Detected",
    "Investigate Anomaly / Possible Unmet Demand": "Potential Unmet Demand Opportunity",
    "Moderate Demand": "Developing Market Interest",
    "High Demand": "Strong Demand Momentum",
    "Low Demand": "Limited Demand Signal",
    "Emerging Demand": "Emerging Demand Signal",
    "Declining Demand": "Limited Market Momentum",
    "Unmet Demand": "Potential Unmet Demand Opportunity",
}


def predict_demand_details(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> dict[str, Any]:
    """Return the full Signal demand interpretation while staying crash-resistant."""

    try:
        features = _build_signal_features(
            likes,
            comments,
            shares,
            searches,
            engagement_intensity,
            purchase_intent_score,
            trend_growth,
        )
        model_result = _predict_with_model(features)
        guarded = _apply_guardrails(model_result, features)
        explanation = generate_prediction_explanation(features, guarded)
        guarded["key_drivers"] = explanation["key_drivers"]
        guarded["key_driver_summary"] = explanation["driver_summary"]
        guarded["policy_note"] = explanation["policy_note"]
        guarded["risk_signals"] = _build_risk_signals(features, guarded)
        guarded.update(_calculate_intelligence_scores(features, guarded))
        guarded["why_this_matters"] = _build_why_this_matters(features, guarded)
        guarded["product_domain_route"] = run_behavioral_signal_prediction(
            likes,
            comments,
            shares,
            searches,
            engagement_intensity,
            purchase_intent_score,
            trend_growth,
        )["route_domain"]
        return guarded
    except Exception as exc:
        return {
            "demand_classification": f"Error: {exc}",
            "confidence_score": 0.0,
            "aggregate_demand_score": 0.0,
            "opportunity_score": 0.0,
            "investment_opportunity_interpretation": "Prediction failed",
            "unmet_demand_flag": False,
            "emerging_trend_flag": False,
            "demand_band": "Low Demand",
            "prediction_source": "Error",
            "model_source_label": "Error",
            "explanation_note": f"Prediction pipeline failed: {exc}",
            "key_drivers": ["prediction error"],
            "key_driver_summary": f"Signal could not complete the prediction: {exc}",
            "risk_signals": ["Prediction pipeline failed before validation could complete."],
            "policy_note": "Check model availability and input validity before interpreting this signal.",
            "why_this_matters": "Signal could not complete the assessment, so the current output should not be used for decision-making.",
            "signal_strength_score": 0.0,
            "momentum_score": 0.0,
            "volatility_noise_score": 0.0,
            "persistence_score": 0.0,
            "adoption_probability": 0.0,
            "viral_probability": 0.0,
            "model_version": "unavailable",
        }


def predict_demand(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float, float, float, float, str, str]:
    """Primary Gradio callback for both live updates and button-triggered refresh."""

    result = predict_demand_details(
        likes,
        comments,
        shares,
        searches,
        engagement_intensity,
        purchase_intent_score,
        trend_growth,
    )
    explanation = _format_panel_explanation(result)
    return (
        str(result["demand_classification"]),
        round(float(result["confidence_score"]) * 100, 2),
        round(float(result["aggregate_demand_score"]), 2),
        round(float(result["opportunity_score"]), 2),
        round(float(result["emerging_trend_probability"]) * 100, 2),
        round(float(result["unmet_demand_probability"]) * 100, 2),
        str(result["investment_opportunity_interpretation"]),
        explanation,
    )


def signal_model(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float]:
    """Backward-compatible wrapper used by existing tests and callers."""

    result = predict_demand_details(
        likes,
        comments,
        shares,
        searches,
        engagement_intensity,
        purchase_intent_score,
        trend_growth,
    )
    label = str(result["demand_band"])
    aggregate_score = float(result["aggregate_demand_score"])
    opportunity_score = float(result["opportunity_score"])
    legacy_label = {
        "High Demand": "High",
        "Moderate Demand": "Moderate",
        "Low Demand": "Low",
    }.get(label, label)
    legacy_aggregate_score = max(0.0, min(100.0, float(aggregate_score)))
    legacy_opportunity_score = float(opportunity_score) * 100 if opportunity_score <= 1 else float(opportunity_score)
    return legacy_label, legacy_aggregate_score, max(0.0, min(100.0, legacy_opportunity_score))


def update_behavioral_dashboard(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[Any, ...]:
    """Return the full live dashboard payload for the Behavioral Signals AI tab."""

    try:
        result = predict_demand_details(
            likes,
            comments,
            shares,
            searches,
            engagement_intensity,
            purchase_intent_score,
            trend_growth,
        )
        visuals = _build_visual_components(result)
        return (
            str(result["demand_classification"]),
            round(float(result["confidence_score"]) * 100, 2),
            round(float(result["aggregate_demand_score"]), 2),
            round(float(result["opportunity_score"]), 2),
            round(float(result["emerging_trend_probability"]) * 100, 2),
            round(float(result["unmet_demand_probability"]) * 100, 2),
            str(result["investment_opportunity_interpretation"]),
            _format_panel_explanation(result),
            round(float(result["signal_strength_score"]), 2),
            round(float(result["momentum_score"]), 2),
            round(float(result["volatility_noise_score"]), 2),
            round(float(result["persistence_score"]), 2),
            round(float(result["adoption_probability"]), 2),
            round(float(result["viral_probability"]), 2),
            str(result["why_this_matters"]),
            visuals["confidence_gauge_html"],
            visuals["signal_strength_gauge_html"],
            visuals["momentum_indicator_html"],
            visuals["opportunity_radar_html"],
            visuals["key_driver_cards_html"],
        )
    except Exception as exc:
        message = f"Prediction temporarily unavailable: {exc}"
        return (
            "Prediction unavailable",
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            "Signal could not complete the current prediction. Adjust inputs and try again.",
            message,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            "No decision should be made from this failed run.",
            _render_gauge_card("Confidence Gauge", 0.0, "#2563eb"),
            _render_gauge_card("Signal Strength Gauge", 0.0, "#16a34a"),
            _render_gauge_card("Trend Momentum Indicator", 0.0, "#d97706"),
            _render_radar_chart({"Opportunity": 0, "Momentum": 0, "Adoption": 0, "Persistence": 0, "Viral": 0}),
            _render_key_driver_cards(["Prediction error"], [message]),
        )


def cge_model(scenario_text: str) -> tuple[str, str, str]:
    """Run the Signal CGE framework and return dashboard-ready outputs."""

    try:
        if not ADVANCED_AVAILABLE:
            raise RuntimeError(f"Advanced Signal modules unavailable: {ADVANCED_IMPORT_ERROR}")

        result = run_policy_scenario(scenario_text or DEFAULT_SCENARIO)
        macro = result["macro_results"]
        intelligence = result["policy_intelligence"]
        summary = (
            f"{intelligence['summary']}\n\n"
            f"Baseline GDP index: {macro['baseline_gdp']}\n"
            f"Simulated GDP index: {macro['simulated_gdp']}\n"
            f"GDP change: {macro['gdp_change_percent']}%\n"
            f"Household welfare change: {macro['household_welfare_change_percent']}%\n"
            f"Price index change: {macro['price_index_change_percent']}%"
        )
        policy_output = {
            "priority_sectors": intelligence["priority_sectors"],
            "recommended_policy_actions": intelligence["recommended_policy_actions"],
            "risks": intelligence["risks"],
            "diagnostics": result["diagnostics"],
            "publication_note": intelligence["publication_note"],
        }
        gams_preview = "\n".join(str(result["gams_model"]).splitlines()[:32])
        return summary, json.dumps(policy_output, indent=2), gams_preview
    except Exception as exc:
        return f"CGE run failed: {exc}", "{}", ""


def ai_cge_workbench_model(
    model_type: str,
    scenario_family: str,
    custom_prompt: str,
    shock_size: float,
    target_account: str,
    sam_file: Any | None = None,
) -> tuple[str, str, str, str | None]:
    """Run the chat-driven Signal CGE Workbench from dashboard controls."""

    try:
        if not AI_CGE_WORKBENCH_AVAILABLE:
            raise RuntimeError(f"AI-CGE Workbench unavailable: {AI_CGE_WORKBENCH_IMPORT_ERROR}")
        prompt = custom_prompt.strip() if custom_prompt else _prompt_from_controls(scenario_family, shock_size, target_account)
        sam_path = _uploaded_path(sam_file)
        result = run_chat_scenario(
            prompt=prompt,
            model_type=model_type,
            shock_size=shock_size,
            target_account=target_account.strip() if target_account else None,
            sam_path=sam_path,
        )
        gams_path = find_gams_executable()
        summary = "\n\n".join(
            [
                result["message"],
                result["explanation"]["executive_summary"],
                f"GAMS execution available: {'Yes - ' + gams_path if gams_path else 'No'}",
                f"Policy brief: {result['artifacts'].get('policy_brief', '')}",
            ]
        )
        scenario_json = json.dumps(result["scenario"], indent=2)
        results_json = json.dumps(
            {
                "diagnostics": result["diagnostics"],
                "results": result["results"],
                "artifacts": result["artifacts"],
            },
            indent=2,
        )
        return summary, scenario_json, results_json, result["artifacts"].get("policy_brief")
    except Exception as exc:
        return f"AI-CGE Workbench run failed: {exc}", "{}", "{}", None


def ai_cge_chat_studio_model(user_prompt: str, sam_file: Any | None = None) -> tuple[str, str, str, str, str]:
    """Run the deterministic AI CGE Chat Studio orchestration."""

    try:
        if not AI_CGE_WORKBENCH_AVAILABLE:
            raise RuntimeError(f"AI-CGE Workbench unavailable: {AI_CGE_WORKBENCH_IMPORT_ERROR}")
        sam_path = _uploaded_path(sam_file)
        result = run_chat_simulation(user_prompt, sam_file=sam_path)
        scenario_json = json.dumps(result["scenario"], indent=2)
        diagnostics_json = format_diagnostics(result)
        result_summary = format_results_summary(result)
        explanation = format_policy_explanation(result)
        recommendations = format_recommendations(result)
        return scenario_json, diagnostics_json, result_summary, explanation, recommendations
    except Exception as exc:
        message = f"AI CGE Chat Studio failed gracefully: {exc}"
        return "{}", f"## Diagnostics\n- {message}", "## Results Summary\n- No results were produced.", message, ""


def run_signal_cge_prompt(prompt: str, uploaded_file: Any | None = None) -> dict[str, Any]:
    """Run the single public Signal CGE prompt-driven workflow."""

    if not AI_CGE_WORKBENCH_AVAILABLE:
        return _signal_cge_error_response(
            prompt,
            f"Signal CGE backend unavailable: {AI_CGE_WORKBENCH_IMPORT_ERROR}",
        )
    return route_run_signal_cge_prompt(prompt, uploaded_file)


def signal_cge_prompt_ui(prompt: str, uploaded_file: Any | None = None) -> tuple[str, pd.DataFrame, pd.DataFrame, str, str, str, str | None, str | None, str | None]:
    """Return display-ready Signal CGE sections for the public Gradio tab."""

    result = run_signal_cge_prompt(prompt, uploaded_file)
    downloads = result.get("downloads", {})
    return (
        _render_results_cards(result),
        pd.DataFrame(result.get("chart_data", [])),
        _results_table_dataframe(result.get("results", {})),
        _render_model_reference_used(result),
        _render_policy_interpretation(result.get("interpretation", {})),
        "\n\n".join(
            [
                _render_interpreted_scenario(result),
                _render_diagnostics(result.get("diagnostics", {})),
                _render_readiness(result.get("readiness", {})),
            ]
        ),
        downloads.get("policy_brief_md"),
        downloads.get("results_json"),
        downloads.get("results_csv"),
    )


def get_public_tab_labels() -> list[str]:
    """Return the public Gradio tab labels."""

    return PUBLIC_TABS.copy()


def _signal_cge_error_response(prompt: str, message: str) -> dict[str, Any]:
    scenario = {
        "scenario_name": prompt or "Signal CGE prompt",
        "policy_shock": "unavailable",
        "shock_account": "",
        "shock_magnitude": "",
        "closure_assumption": "",
        "model_backend_used": "unavailable",
    }
    return {
        "scenario": scenario,
        "readiness": get_model_readiness() if "get_model_readiness" in globals() else {},
        "diagnostics": {"solver_warnings": [message], "fallback_explanation": FULL_CGE_FALLBACK_MESSAGE},
        "results": {},
        "interpretation": {"caveats": [message]},
        "downloads": {},
        "backend_used": "unavailable",
        "fallback_message": FULL_CGE_FALLBACK_MESSAGE,
    }


def _signal_cge_interpreted_scenario(scenario: dict[str, Any], results: dict[str, Any]) -> dict[str, Any]:
    policy_shock = scenario.get("policy_instrument") or scenario.get("shock_type", "policy shock")
    return {
        "policy_shock": str(policy_shock).replace("_", " "),
        "policy_instrument": scenario.get("policy_instrument", scenario.get("shock_type", "")),
        "target_account": scenario.get("target_account", scenario.get("target_commodity", scenario.get("shock_account", ""))),
        "target_account_sector": scenario.get("target_account", scenario.get("target_commodity", scenario.get("shock_account", ""))),
        "shock_direction": scenario.get("shock_direction", "increase" if float(scenario.get("shock_size", 0) or 0) >= 0 else "decrease"),
        "shock_magnitude_percent": abs(float(scenario.get("shock_size", scenario.get("shock_value", 0)) or 0)),
        "shock_magnitude": f"{scenario.get('shock_size', scenario.get('shock_value', 0))} {scenario.get('shock_unit', 'percent')}",
        "simulation_type": scenario.get("simulation_type", "sam_multiplier"),
        "closure_assumption": scenario.get("closure", scenario.get("closure_rule", "standard_sam_multiplier")),
        "model_backend_used": results.get("backend", "python_sam_multiplier"),
        "raw_scenario": scenario,
    }


def _signal_cge_structured_results(results: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    accounts = results.get("accounts", {}) if isinstance(results, dict) else {}
    account_total = sum(float(value) for value in accounts.values()) if accounts else 0.0
    household_effect = sum(float(value) for account, value in accounts.items() if "household" in account.lower())
    trade_effect = sum(float(value) for account, value in accounts.items() if account.lower() in {"imports", "exports", "cmach"})
    government_effect = sum(float(value) for account, value in accounts.items() if "government" in account.lower())
    factor_effect = sum(
        float(value)
        for account, value in accounts.items()
        if any(term in account.lower() for term in ["labour", "labor", "capital", "fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"])
    )
    care_effect = sum(float(value) for account, value in accounts.items() if "care" in account.lower())
    return {
        "GDP/output effect": round(account_total, 6),
        "factor income effect": round(factor_effect, 6),
        "household income effect": round(household_effect, 6),
        "government balance effect": round(government_effect, 6),
        "trade effect": round(trade_effect, 6),
        "welfare/proxy welfare effect": round(household_effect or account_total, 6),
        "gender-care impact": round(care_effect, 6) if _is_care_scenario(scenario) else "Not a care-focused scenario.",
        "account_effects": accounts,
        "backend": results.get("backend", "python_sam_multiplier") if isinstance(results, dict) else "python_sam_multiplier",
    }


def _signal_cge_chart_data(results: dict[str, Any]) -> list[dict[str, Any]]:
    """Return chart-ready scenario effect rows for Gradio's native bar plot."""

    metric_map = {
        "GDP/output": results.get("GDP/output effect", 0.0),
        "Household income": results.get("household income effect", 0.0),
        "Government balance": results.get("government balance effect", 0.0),
        "Imports": _account_effect(results, "imports"),
        "Exports": _account_effect(results, "exports"),
        "Welfare/proxy welfare": results.get("welfare/proxy welfare effect", 0.0),
    }
    return [{"metric": metric, "effect": _safe_float(value)} for metric, value in metric_map.items()]


def _account_effect(results: dict[str, Any], account_name: str) -> float:
    accounts = results.get("account_effects", {})
    return float(accounts.get(account_name, 0.0)) if isinstance(accounts, dict) else 0.0


def _signal_cge_policy_interpretation(result: dict[str, Any]) -> dict[str, Any]:
    summary = result.get("policy_summary", {})
    return {
        "transmission_mechanism": summary.get("expected_transmission_channel", ""),
        "winners_and_losers": {
            "likely_winners": summary.get("likely_winners", []),
            "likely_losers": ["Accounts facing higher relative costs or reduced demand, subject to SAM mapping."],
        },
        "risks": summary.get("likely_risks", []),
        "caveats": [
            summary.get("interpretation_caveat", ""),
            FULL_CGE_FALLBACK_MESSAGE,
        ],
        "recommended_next_simulations": summary.get("suggested_next_simulations", []),
    }


def _is_care_scenario(scenario: dict[str, Any]) -> bool:
    text = json.dumps(scenario).lower()
    return "care" in text or any(suffix in text for suffix in ["fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"])


def _write_signal_cge_downloads(
    scenario: dict[str, Any],
    readiness: dict[str, Any],
    diagnostics: dict[str, Any],
    results: dict[str, Any],
    interpretation: dict[str, Any],
    model_profile: dict[str, Any],
) -> dict[str, str]:
    output_dir = Path("outputs") / "signal_cge_public" / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "scenario": scenario,
        "readiness": readiness,
        "diagnostics": diagnostics,
        "results": results,
        "interpretation": interpretation,
        "model_profile": model_profile,
    }
    md_path = output_dir / "signal_cge_policy_brief.md"
    json_path = output_dir / "signal_cge_results.json"
    csv_path = output_dir / "signal_cge_results.csv"
    md_path.write_text(_policy_brief_markdown(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    pd.DataFrame(
        [{"account": account, "effect": value} for account, value in results.get("account_effects", {}).items()]
    ).to_csv(csv_path, index=False)
    return {
        "policy_brief_md": str(md_path),
        "results_json": str(json_path),
        "results_csv": str(csv_path),
    }


def _render_results_cards(result: dict[str, Any]) -> str:
    results = result.get("results", {})
    cards = [
        ("GDP/output effect", results.get("GDP/output effect", 0.0)),
        ("Household income effect", results.get("household income effect", 0.0)),
        ("Trade effect", results.get("trade effect", 0.0)),
        ("Welfare/proxy welfare effect", results.get("welfare/proxy welfare effect", 0.0)),
        ("Model backend used", result.get("backend_used", "python_sam_multiplier")),
        ("Result type", result.get("result_type", "prototype_directional_indicator")),
    ]
    card_html = "".join(
        (
            "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#fff;'>"
            f"<div style='font-size:12px;color:#64748b;font-weight:700;'>{escape(label)}</div>"
            f"<div style='font-size:20px;font-weight:800;color:#0f172a;margin-top:4px;'>{escape(str(value))}</div>"
            "</div>"
        )
        for label, value in cards
    )


def _results_table_dataframe(results: dict[str, Any]) -> pd.DataFrame:
    rows = [
        {"metric": "GDP/output", "effect": results.get("GDP/output effect", 0.0)},
        {"metric": "Factor income", "effect": results.get("factor income effect", 0.0)},
        {"metric": "Household income", "effect": results.get("household income effect", 0.0)},
        {"metric": "Government balance", "effect": results.get("government balance effect", 0.0)},
        {"metric": "Trade", "effect": results.get("trade effect", 0.0)},
        {"metric": "Welfare/proxy welfare", "effect": results.get("welfare/proxy welfare effect", 0.0)},
        {"metric": "Gender-care impact", "effect": results.get("gender-care impact", "Not applicable to this scenario.")},
    ]
    return pd.DataFrame(rows)
    return (
        "<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:10px 0;'>"
        f"{card_html}</div>"
    )


def _policy_brief_markdown(payload: dict[str, Any]) -> str:
    return "\n\n".join(
        [
            "# Signal CGE Policy Simulation Brief",
            "## Interpreted Scenario\n```json\n" + json.dumps(payload["scenario"], indent=2) + "\n```",
            "## Model Readiness\n```json\n" + json.dumps(payload["readiness"], indent=2) + "\n```",
            "## Diagnostics\n```json\n" + json.dumps(payload["diagnostics"], indent=2) + "\n```",
            "## Simulation Results\n```json\n" + json.dumps(payload["results"], indent=2) + "\n```",
            "## Policy Interpretation\n```json\n" + json.dumps(payload["interpretation"], indent=2) + "\n```",
        ]
    )


def _render_interpreted_scenario(result: dict[str, Any]) -> str:
    scenario = result.get("scenario", {})
    return "\n".join(
        [
            "## Interpreted Scenario",
            f"- Policy shock: `{scenario.get('policy_shock', '')}`",
            f"- Target account/sector: `{scenario.get('target_account_sector', '')}`",
            f"- Shock magnitude: `{scenario.get('shock_magnitude', '')}`",
            f"- Closure assumption: `{scenario.get('closure_assumption', '')}`",
            f"- Model backend used: `{result.get('backend_used', '')}`",
        ]
    )


def _render_readiness(readiness: dict[str, Any]) -> str:
    labels = [
        "sam_multiplier_readiness",
        "calibration_readiness",
        "prototype_cge_readiness",
        "full_cge_solver_readiness",
        "recursive_dynamic_readiness",
    ]
    return "\n".join(["## Model Readiness", *[f"- {label.replace('_', ' ').title()}: `{readiness.get(label, 'unknown')}`" for label in labels]])


def _render_diagnostics(diagnostics: dict[str, Any]) -> str:
    pre_run = diagnostics.get("pre_run", {})
    calibration = diagnostics.get("preflight", {}).get("calibration", {})
    closure = diagnostics.get("preflight", {}).get("closure", {})
    lines = [
        "## Diagnostics",
        f"- SAM balance status: `{pre_run.get('balanced', pre_run.get('is_balanced', 'not available'))}`",
        "- Calibration status: Prototype calibration available; full equilibrium calibration not yet active.",
        f"- Closure warnings: {_format_warning_text(closure.get('warnings', []) if isinstance(closure, dict) else [])}",
        f"- Solver warnings: `{diagnostics.get('fallback_explanation', FULL_CGE_FALLBACK_MESSAGE)}`",
        f"- Fallback explanation: {diagnostics.get('fallback_explanation', FULL_CGE_FALLBACK_MESSAGE)}",
    ]
    return "\n".join(lines)


def _render_simulation_results(results: dict[str, Any]) -> str:
    lines = ["## Simulation Results"]
    for key in [
        "GDP/output effect",
        "factor income effect",
        "household income effect",
        "government balance effect",
        "trade effect",
        "welfare/proxy welfare effect",
        "gender-care impact",
    ]:
        lines.append(f"- {key}: `{results.get(key, 'not available')}`")
    return "\n".join(lines)


def _render_policy_interpretation(interpretation: dict[str, Any]) -> str:
    winners = interpretation.get("winners_and_losers", {}).get("likely_winners", [])
    losers = interpretation.get("winners_and_losers", {}).get("likely_losers", [])
    return "\n".join(
        [
            "## Policy Interpretation",
            f"- Transmission mechanism: {interpretation.get('transmission_mechanism', '')}",
            f"- Winners: {', '.join(winners) if winners else 'None identified.'}",
            f"- Losers: {', '.join(losers) if losers else 'None identified.'}",
            f"- Risks: {', '.join(interpretation.get('risks', [])) or 'No major warning raised.'}",
            f"- Caveats: {', '.join(item for item in interpretation.get('caveats', []) if item)}",
            f"- Recommended next simulations: {', '.join(interpretation.get('recommended_next_simulations', []))}",
        ]
    )


def _render_model_reference_used(result: dict[str, Any]) -> str:
    references = result.get("knowledge_context", {}).get("reference_labels", [])
    lines = ["## Model Reference Used"]
    if references:
        lines.extend(f"- {reference} loaded" for reference in references)
    else:
        lines.append("- Canonical model profile loaded")
    lines.append("- Solver limitation note loaded")
    return "\n".join(lines)


def _format_warning_text(warnings: list[Any]) -> str:
    return "; ".join(str(warning) for warning in warnings) if warnings else "No closure warnings."


def _prompt_from_controls(scenario_family: str, shock_size: float, target_account: str) -> str:
    target = target_account.strip() if target_account else "selected account"
    templates = {
        "Care economy": f"Increase public investment in care infrastructure by {shock_size}%",
        "Tax policy": f"Simulate a {abs(shock_size)}% VAT reduction on {target}",
        "Infrastructure": f"Increase transport productivity by {shock_size}%",
        "Trade policy": f"Run a trade facilitation shock for exports of {shock_size}%",
        "Productivity": f"Increase {target} productivity by {shock_size}%",
        "Custom prompt": f"Apply a {shock_size}% shock to {target}",
    }
    return templates.get(scenario_family, templates["Custom prompt"])


def validate_sml_dashboard(sml_text: str, sml_file: Any | None = None) -> str:
    """Validate SML from dashboard text or upload."""

    try:
        text = _uploaded_text(sml_file) or sml_text or DEFAULT_SML_TEXT
        parsed = parse_sml(text)
        validation = validate_sml(parsed)
        status = "Valid" if validation["valid"] else "Invalid"
        parts = [f"Status: {status}"]
        if validation["errors"]:
            parts.append("Errors:\n" + "\n".join(f"- {error}" for error in validation["errors"]))
        if validation["warnings"]:
            parts.append("Warnings:\n" + "\n".join(f"- {warning}" for warning in validation["warnings"]))
        return "\n\n".join(parts)
    except Exception as exc:
        return f"Invalid\n\nErrors:\n- {exc}"


def run_sml_dashboard(
    sml_text: str,
    sml_file: Any | None = None,
    sam_file: Any | None = None,
) -> tuple[str, str, str, str | None]:
    """Run SML from the dashboard and return validation, balance, results, and report file."""

    try:
        if not ADVANCED_AVAILABLE:
            raise RuntimeError(f"Advanced Signal modules unavailable: {ADVANCED_IMPORT_ERROR}")

        text = _uploaded_text(sml_file) or sml_text or DEFAULT_SML_TEXT
        parsed = parse_sml(text)
        workbench_validation = validate_sml(parsed)
        sam_path = _uploaded_path(sam_file)
        result = SignalRunner().run(sml_text=text, sam_override=sam_path)
        validation = result["validation"]
        balance_text = _balance_rows_to_markdown(validation["balance_check"][:12])
        result_view = {
            "run_id": result["run_id"],
            "status": result["status"],
            "backend": result["backend"],
            "requested_backend": result["requested_backend"],
            "message": result["message"],
            "gams_message": result["gams_message"],
            "metrics": result["metrics"],
            "gams_file": result["gams_file"],
            "balance_check_paths": result["balance_check_paths"],
            "learning_memory": result["learning_memory"],
            "workbench_validation": workbench_validation,
            "gams_export_preview": export_to_gams(parsed),
            "pyomo_export_preview": export_to_pyomo(parsed),
        }
        validation_text = "Status: Valid" if validation["valid"] else "Status: Invalid"
        if validation["warnings"]:
            validation_text += "\n\nWarnings:\n" + "\n".join(f"- {warning}" for warning in validation["warnings"])
        return validation_text, balance_text, json.dumps(result_view, indent=2), str(result["report_path"])
    except Exception as exc:
        return f"Status: Failed\n\nErrors:\n- {exc}", "", "{}", None


def refresh_learning_dashboard() -> tuple[str, str, str]:
    """Return recent lessons, recurring issues, and recommended fixes."""

    try:
        if not ADVANCED_AVAILABLE:
            raise RuntimeError(f"Advanced Signal modules unavailable: {ADVANCED_IMPORT_ERROR}")

        store = LearningStore()
        data = store.load()
        lessons = store.lessons()[-10:]
        recurring = recurring_issue_summary(data)
        proposals = propose_adaptations(data)
        recommended = [
            {
                "version_id": proposal.version_id,
                "change_summary": proposal.change_summary,
                "risk_level": proposal.risk_level,
                "confidence_score": proposal.confidence_score,
                "evidence_run_ids": proposal.evidence_run_ids,
            }
            for proposal in proposals[-10:]
        ]
        return json.dumps(lessons, indent=2), json.dumps(recurring, indent=2), json.dumps(recommended, indent=2)
    except Exception as exc:
        return "[]", "{}", json.dumps({"error": str(exc)}, indent=2)


def refresh_live_trends(location: str, trend_limit: float) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """Fetch public aggregate X/Twitter trends and convert them into Signal intelligence."""

    try:
        records = fetch_x_trends(location=location, limit=int(trend_limit))
    except Exception as exc:
        fallback_location = location if location in {"Kenya", "Nairobi", "Global"} else "Kenya"
        records = get_demo_trends(location=fallback_location, limit=int(trend_limit))
        location = fallback_location
        fallback_note = f"Live API unavailable — displaying demo aggregate trends. Details: {exc}"
    else:
        fallback_note = (
            "Live API unavailable — displaying demo aggregate trends."
            if any("Demo fallback" in str(record.get("source", "")) for record in records)
            else ""
        )

    analyses = analyze_trend_batch(records)
    raw_frame = pd.DataFrame(records)
    intelligence_frame = pd.DataFrame(analyses)
    trends_frame = _build_hidden_trends_frame(raw_frame, intelligence_frame)
    summary = summarize_trend_batch(location, analyses)
    if fallback_note:
        summary = f"{summary}\n\n{fallback_note}"
    return trends_frame, intelligence_frame, summary


def refresh_live_trend_intelligence(location: str, trend_limit: float) -> tuple[pd.DataFrame, str, int, str, pd.DataFrame]:
    """Return embedded Live Trend Intelligence values for Behavioral Signals AI."""

    try:
        trends_frame, intelligence_frame, summary = refresh_live_trends(location, trend_limit)
        active_count = _active_trend_count(trends_frame)
        ticker_html = build_live_trend_html(trends_frame)
        return trends_frame, ticker_html, active_count, summary, intelligence_frame
    except Exception as exc:
        fallback_records = get_demo_trends(location="Kenya", limit=max(3, int(trend_limit or 5)))
        fallback_frame = pd.DataFrame(fallback_records)
        fallback_intelligence = pd.DataFrame(analyze_trend_batch(fallback_records))
        fallback_summary = f"Live API unavailable — displaying demo aggregate trends. Details: {exc}"
        return (
            fallback_frame,
            _fallback_live_trend_html(fallback_summary),
            len(fallback_records),
            fallback_summary,
            fallback_intelligence,
        )


def explain_learning_topic(topic: str) -> str:
    """Return a readable learning note for the selected concept."""

    return explain_concept(topic)


def apply_latest_learning_dashboard() -> str:
    """Apply the latest low-risk adaptation as a versioned template."""

    try:
        if not ADVANCED_AVAILABLE:
            raise RuntimeError(f"Advanced Signal modules unavailable: {ADVANCED_IMPORT_ERROR}")

        data = LearningStore().load()
        proposals = propose_adaptations(data)
        if not proposals:
            return "No recommended fixes are available yet."
        low_risk = [proposal for proposal in proposals if proposal.risk_level == "low"]
        proposal = low_risk[-1] if low_risk else proposals[-1]
        result = implement_adaptation(proposal, mode="safe_apply" if proposal.risk_level == "low" else "recommend")
        LearningStore().add_implementation(result)
        return json.dumps(result.to_dict(), indent=2)
    except Exception as exc:
        return json.dumps({"error": str(exc)}, indent=2)


def ignore_latest_learning_dashboard() -> str:
    return "Latest recommendation ignored for now. No files were changed."


def rollback_learning_dashboard(version_id: str) -> str:
    """Roll back a learning version."""

    try:
        if not ADVANCED_AVAILABLE:
            raise RuntimeError(f"Advanced Signal modules unavailable: {ADVANCED_IMPORT_ERROR}")

        if not str(version_id).strip():
            return "Enter a learning version id such as v001."
        result = rollback_adaptation(str(version_id).strip())
        LearningStore().add_implementation(result)
        return json.dumps(result.to_dict(), indent=2)
    except Exception as exc:
        return json.dumps({"error": str(exc)}, indent=2)


def _map_demand_label(prediction: Any) -> str:
    text = str(prediction).strip().lower()
    if prediction == 2 or text in {"2", "high", "high demand"}:
        return "High Demand"
    if prediction == 1 or text in {"1", "moderate", "moderate demand"}:
        return "Moderate Demand"
    if text in {"emerging", "emerging demand"}:
        return "Emerging Demand"
    if text in {"declining", "declining demand"}:
        return "Declining Demand"
    if text in {"unmet", "unmet demand"}:
        return "Unmet Demand"
    return "Low Demand"


def _normalize_demand_band(label: str) -> str:
    mapping = {
        "High Demand": "High Demand",
        "Moderate Demand": "Moderate Demand",
        "Emerging Demand": "Moderate Demand",
        "Low Demand": "Low Demand",
        "Declining Demand": "Low Demand",
        "Unmet Demand": "Low Demand",
    }
    return mapping.get(label, "Low Demand")


def _safe_float(value: Any) -> float:
    return float(value or 0)


def _display_label(label: str) -> str:
    return DISPLAY_LABELS.get(label, label)


def _build_signal_features(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> dict[str, float]:
    likes = _safe_float(likes)
    comments = _safe_float(comments)
    shares = _safe_float(shares)
    searches = _safe_float(searches)
    engagement_intensity = _safe_float(engagement_intensity)
    purchase_intent_score = _safe_float(purchase_intent_score)
    trend_growth = _safe_float(trend_growth)

    total_engagement = likes + comments + shares + searches
    mentions_count = comments + (shares * 0.5)
    sentiment_score = np.clip((purchase_intent_score * 0.75) - 0.15 + trend_growth * 0.2, -1, 1)
    urgency_score = np.clip((searches / max(total_engagement, 1)) * 1.5 + trend_growth * 0.45, 0, 1)
    repetition_score = np.clip(searches / max(likes + comments + 1, 1), 0, 1)
    location_relevance = 0.55
    price_sensitivity = np.clip(0.65 - purchase_intent_score * 0.35 + (1 - engagement_intensity) * 0.15, 0, 1)
    noise_score = np.clip(1 - min((comments + shares + 1) / max(likes + searches + 1, 1), 1), 0, 1)
    engagement_rate = np.clip(total_engagement / max(total_engagement + 100, 1), 0, 1)
    weighted_engagement_score = np.clip(
        (likes + comments * 1.8 + shares * 2.4 + searches * 1.6 + mentions_count) / 100,
        0,
        10,
    )
    trend_momentum = np.clip(trend_growth * 0.6 + urgency_score * 0.4, 0, 1)
    unmet_need_signal = np.clip(urgency_score * 0.45 + price_sensitivity * 0.25 + (1 - sentiment_score) * 0.1, 0, 1)
    opportunity_index = np.clip(
        engagement_intensity * 0.22
        + purchase_intent_score * 0.22
        + trend_growth * 0.18
        + urgency_score * 0.14
        + repetition_score * 0.08
        + unmet_need_signal * 0.12
        + location_relevance * 0.06
        - noise_score * 0.08,
        0,
        1,
    )

    return {
        "engagement_intensity": round(float(np.clip(engagement_intensity, 0, 1)), 4),
        "mentions_count": round(float(max(mentions_count, 0)), 4),
        "comments_count": round(float(max(comments, 0)), 4),
        "shares_count": round(float(max(shares, 0)), 4),
        "likes_count": round(float(max(likes, 0)), 4),
        "searches_count": round(float(max(searches, 0)), 4),
        "likes": round(float(max(likes, 0)), 4),
        "comments": round(float(max(comments, 0)), 4),
        "shares": round(float(max(shares, 0)), 4),
        "searches": round(float(max(searches, 0)), 4),
        "purchase_intent_score": round(float(np.clip(purchase_intent_score, 0, 1)), 4),
        "sentiment_score": round(float(sentiment_score), 4),
        "urgency_score": round(float(urgency_score), 4),
        "trend_growth": round(float(np.clip(trend_growth, -1, 1)), 4),
        "repetition_score": round(float(repetition_score), 4),
        "location_relevance": round(float(location_relevance), 4),
        "price_sensitivity": round(float(price_sensitivity), 4),
        "noise_score": round(float(noise_score), 4),
        "engagement_rate": round(float(engagement_rate), 4),
        "weighted_engagement_score": round(float(weighted_engagement_score), 4),
        "trend_momentum": round(float(trend_momentum), 4),
        "unmet_need_signal": round(float(unmet_need_signal), 4),
        "opportunity_index": round(float(opportunity_index), 4),
    }


def _predict_with_model(features: dict[str, float]) -> dict[str, Any]:
    artifact = _load_prediction_artifact()
    if artifact is None:
        return _predict_with_fallback(features)

    feature_columns = artifact.get("feature_columns") or list(features.keys())
    model = artifact.get("model", artifact)
    frame = pd.DataFrame([{column: float(features.get(column, 0.0)) for column in feature_columns}])
    raw_prediction = _map_demand_label(model.predict(frame)[0])
    probabilities = model.predict_proba(frame)[0] if hasattr(model, "predict_proba") else np.array([1.0])
    classes = [_map_demand_label(label) for label in getattr(model, "classes_", ["Low Demand", "Moderate Demand", "High Demand"])]
    class_probabilities = {label: float(prob) for label, prob in zip(classes, probabilities)}
    confidence_score = float(max(class_probabilities.values(), default=1.0))
    demand_weights = {
        "High Demand": 1.0,
        "Moderate Demand": 0.62,
        "Low Demand": 0.2,
        "Emerging Demand": 0.58,
        "Declining Demand": 0.16,
        "Unmet Demand": 0.52,
    }
    aggregate_demand_score = float(
        np.clip(
            sum(class_probabilities.get(label, 0.0) * weight for label, weight in demand_weights.items()) * 100,
            0,
            100,
        )
    )

    unmet_model = artifact.get("unmet_model")
    emerging_model = artifact.get("emerging_model")
    unmet_probability = _positive_probability(unmet_model, frame)
    emerging_probability = _positive_probability(emerging_model, frame)
    opportunity_score = float(
        np.clip(
            (
                aggregate_demand_score * 0.5
                + features["opportunity_index"] * 100 * 0.25
                + unmet_probability * 100 * 0.15
                + emerging_probability * 100 * 0.1
            ),
            0,
            100,
        )
    )

    return {
        "raw_demand_classification": raw_prediction,
        "demand_classification": _display_label(raw_prediction),
        "demand_band": _normalize_demand_band(raw_prediction),
        "confidence_score": round(confidence_score, 4),
        "aggregate_demand_score": round(aggregate_demand_score, 2),
        "opportunity_score": round(opportunity_score, 2),
        "unmet_demand_probability": round(unmet_probability, 4),
        "emerging_trend_probability": round(emerging_probability, 4),
        "prediction_source": "Trained ML Model",
        "model_source_components": ["Trained ML Model"],
        "model_source_label": "Trained ML Model",
        "explanation_note": "Primary prediction produced by the trained local Signal model.",
        "model_version": str(artifact.get("model_version", _metadata_value("model_version", "legacy"))),
    }


def _predict_with_fallback(features: dict[str, float]) -> dict[str, Any]:
    latent = np.clip(
        features["engagement_intensity"] * 0.28
        + features["purchase_intent_score"] * 0.18
        + features["trend_growth"] * 0.2
        + features["urgency_score"] * 0.16
        + features["repetition_score"] * 0.1
        + features["opportunity_index"] * 0.26,
        0,
        1,
    )
    if features["searches"] >= 160 and features["engagement_intensity"] < 0.45 and features["purchase_intent_score"] >= 0.6:
        raw_demand = "Unmet Demand"
    elif features["trend_growth"] <= -0.08 and features["engagement_intensity"] < 0.5:
        raw_demand = "Declining Demand"
    elif features["trend_growth"] >= 0.48 and features["engagement_intensity"] >= 0.46:
        raw_demand = "Emerging Demand"
    elif latent >= 0.68:
        raw_demand = "High Demand"
    elif latent >= 0.42:
        raw_demand = "Moderate Demand"
    else:
        raw_demand = "Low Demand"

    unmet_probability = float(np.clip(features["unmet_need_signal"], 0, 1))
    emerging_probability = float(np.clip(features["trend_momentum"], 0, 1))
    confidence_score = float(np.clip(0.52 + abs(latent - 0.5) * 0.4, 0, 0.95))
    aggregate_demand_score = float(np.clip(latent * 100, 0, 100))
    opportunity_score = float(
        np.clip(
            aggregate_demand_score * 0.58
            + unmet_probability * 100 * 0.22
            + emerging_probability * 100 * 0.2,
            0,
            100,
        )
    )
    return {
        "raw_demand_classification": raw_demand,
        "demand_classification": _display_label(raw_demand),
        "demand_band": _normalize_demand_band(raw_demand),
        "confidence_score": round(confidence_score, 4),
        "aggregate_demand_score": round(aggregate_demand_score, 2),
        "opportunity_score": round(opportunity_score, 2),
        "unmet_demand_probability": round(unmet_probability, 4),
        "emerging_trend_probability": round(emerging_probability, 4),
        "prediction_source": "Fallback Logic — trained model not available.",
        "model_source_components": ["Fallback Logic"],
        "model_source_label": "Fallback Logic — trained model not available.",
        "explanation_note": "Fallback scoring used because the trained model artifact was unavailable.",
        "model_version": "unavailable",
    }


def _apply_guardrails(result: dict[str, Any], features: dict[str, float]) -> dict[str, Any]:
    raw_demand = str(result.get("raw_demand_classification", result["demand_classification"]))
    demand_band = str(result.get("demand_band", _normalize_demand_band(raw_demand)))
    opportunity = float(result["opportunity_score"])
    confidence = float(result["confidence_score"])
    unmet_probability = float(result["unmet_demand_probability"])
    emerging_probability = float(result["emerging_trend_probability"])
    notes = [str(result["explanation_note"])]
    source_components = list(result.get("model_source_components", []))

    if demand_band == "High Demand" and opportunity >= 70:
        raw_interpretation = "Strong Investment Opportunity"
    elif demand_band == "Moderate Demand" and opportunity >= 55:
        raw_interpretation = "Emerging Opportunity"
    elif demand_band == "Low Demand" and opportunity >= 55:
        raw_interpretation = "Investigate Anomaly / Possible Unmet Demand"
        unmet_probability = max(unmet_probability, float(np.clip(features["unmet_need_signal"], 0, 1)))
        notes.append("Guardrail flagged a contradiction between low demand and elevated opportunity.")
    else:
        raw_interpretation = "Weak Signal"

    if demand_band == "High Demand" and confidence < 0.62:
        raw_interpretation = "Monitor Further"
        notes.append("High-demand classification arrived with low confidence and should be monitored further.")
    if features.get("searches", 0) >= 160 and features.get("engagement_intensity", 0) < 0.45:
        unmet_probability = max(unmet_probability, 0.72)
        notes.append("High searches with low engagement suggest a possible unmet demand pocket.")
        if "Anomaly / Unmet Demand Detection" not in source_components:
            source_components.append("Anomaly / Unmet Demand Detection")
    if features.get("noise_score", 0) >= 0.75:
        raw_interpretation = "Validate Signal Quality" if opportunity >= 45 else raw_interpretation
        notes.append("High noise score suggests more data quality review before acting.")
    if features.get("engagement_intensity", 0) >= 0.72 and features.get("noise_score", 0) >= 0.6:
        notes.append("High engagement is present, but signal quality should be validated because noise is also elevated.")
    if demand_band == "Moderate Demand" and emerging_probability >= 0.6:
        notes.append("Guardrail marked this as a near-term emerging trend candidate.")
    if len(notes) > 1 and "Guardrail Adjustment" not in source_components:
        source_components.append("Guardrail Adjustment")

    result = dict(result)
    result["raw_demand_classification"] = raw_demand
    result["demand_classification"] = _display_label(raw_demand)
    result["raw_investment_opportunity_interpretation"] = raw_interpretation
    result["investment_opportunity_interpretation"] = _display_label(raw_interpretation)
    result["unmet_demand_flag"] = bool(unmet_probability >= 0.6)
    result["emerging_trend_flag"] = bool(emerging_probability >= 0.55)
    result["explanation_note"] = " ".join(notes)
    result["demand_band"] = demand_band
    result["unmet_demand_probability"] = round(unmet_probability, 4)
    result["model_source_components"] = source_components
    result["prediction_source"] = " | ".join(source_components) if source_components else str(result["prediction_source"])
    result["model_source_label"] = result["prediction_source"].replace("â€”", "—")
    return result


def _load_prediction_artifact() -> dict[str, Any] | None:
    for candidate in (PRIMARY_MODEL_PATH, LEGACY_MODEL_PATH):
        resolved = candidate.resolve()
        try:
            resolved.relative_to(ROOT_DIR)
        except ValueError:
            continue
        if resolved.exists():
            artifact = joblib.load(resolved)
            if isinstance(artifact, dict):
                return artifact
            return {"model": artifact, "feature_columns": ["likes", "comments", "shares", "searches"]}
    return None


def _positive_probability(model: Any | None, vector: pd.DataFrame) -> float:
    if model is None or not hasattr(model, "predict_proba"):
        return 0.0
    probabilities = model.predict_proba(vector)[0]
    if len(probabilities) == 1:
        return float(probabilities[0])
    return float(probabilities[-1])


def _metadata_value(key: str, default: str) -> str:
    if not PRIMARY_MODEL_METADATA_PATH.exists():
        return default
    try:
        payload = json.loads(PRIMARY_MODEL_METADATA_PATH.read_text(encoding="utf-8"))
    except Exception:
        return default
    return str(payload.get(key, default))

def _format_panel_explanation(result: dict[str, Any]) -> str:
    key_drivers = result.get("key_drivers", [])[:3]
    risk_signals = result.get("risk_signals", [])[:3]
    lines = [
        "AI Intelligence Brief",
        "",
        "1. Classification",
        f"Demand classification: {result['demand_classification']}",
        f"Confidence level: {float(result['confidence_score']) * 100:.1f}%",
        f"Aggregate demand score: {float(result['aggregate_demand_score']):.2f}",
        f"Opportunity score: {float(result['opportunity_score']):.2f}",
        "",
        "2. Key Drivers",
    ]
    lines.extend(f"- {driver}" for driver in key_drivers or ["No dominant drivers identified."])
    lines.extend(["", "3. Risk / Validation Signals"])
    lines.extend(f"- {risk}" for risk in risk_signals or ["No major validation risks were detected."])
    lines.extend(
        [
            "",
            "4. Strategic Interpretation",
            str(result["why_this_matters"]),
            "",
            "5. Model Source",
            str(result["model_source_label"]),
        ]
    )
    return "\n".join(lines)


def _calculate_intelligence_scores(features: dict[str, float], result: dict[str, Any]) -> dict[str, float]:
    weighted_engagement_normalized = float(np.clip(features["weighted_engagement_score"] / 10, 0, 1))
    signal_strength = np.clip(
        (
            features["engagement_intensity"] * 0.28
            + features["purchase_intent_score"] * 0.22
            + features["engagement_rate"] * 0.14
            + weighted_engagement_normalized * 0.14
            + max(features["sentiment_score"], 0) * 0.08
            + float(result["confidence_score"]) * 0.14
        )
        * 100,
        0,
        100,
    )
    momentum_score = np.clip(
        (
            features["trend_momentum"] * 0.48
            + max(features["trend_growth"], 0) * 0.24
            + float(result["emerging_trend_probability"]) * 0.18
            + features["urgency_score"] * 0.1
        )
        * 100,
        0,
        100,
    )
    volatility_noise_score = np.clip(
        (
            features["noise_score"] * 0.7
            + abs(features["trend_growth"] - features["engagement_intensity"]) * 0.2
            + max(-features["sentiment_score"], 0) * 0.1
        )
        * 100,
        0,
        100,
    )
    persistence_score = np.clip(
        (features["repetition_score"] * 0.65 + features["engagement_intensity"] * 0.2 + features["engagement_rate"] * 0.15)
        * 100,
        0,
        100,
    )
    adoption_probability = np.clip(
        signal_strength * 0.3
        + momentum_score * 0.18
        + features["purchase_intent_score"] * 100 * 0.2
        + float(result["aggregate_demand_score"]) * 0.16
        + float(result["confidence_score"]) * 100 * 0.16,
        0,
        100,
    )
    viral_probability = np.clip(
        (
            min(features["shares_count"] / max(features["likes_count"] + 1, 1), 1) * 0.26
            + min(features["comments_count"] / max(features["likes_count"] + 1, 1), 1) * 0.12
            + min(features["searches_count"] / max(features["likes_count"] + 1, 1), 1) * 0.16
            + max(features["trend_growth"], 0) * 0.24
            + features["engagement_intensity"] * 0.12
            + features["urgency_score"] * 0.1
        )
        * 100,
        0,
        100,
    )
    return {
        "signal_strength_score": round(float(signal_strength), 2),
        "momentum_score": round(float(momentum_score), 2),
        "volatility_noise_score": round(float(volatility_noise_score), 2),
        "persistence_score": round(float(persistence_score), 2),
        "adoption_probability": round(float(adoption_probability), 2),
        "viral_probability": round(float(viral_probability), 2),
    }


def _build_risk_signals(features: dict[str, float], result: dict[str, Any]) -> list[str]:
    risks: list[str] = []
    if float(result["confidence_score"]) < 0.6:
        risks.append("Low confidence means this signal should be monitored before large commitments.")
    if features["noise_score"] >= 0.7:
        risks.append("Signal Volatility Detected: elevated noise suggests additional validation is needed.")
    if bool(result.get("unmet_demand_flag")):
        risks.append("Potential unmet demand may reflect access, delivery, or affordability gaps.")
    if features["sentiment_score"] < 0:
        risks.append("Soft sentiment may limit conversion even if attention remains elevated.")
    if features["price_sensitivity"] >= 0.68:
        risks.append("High price sensitivity suggests affordability could slow adoption.")
    if not risks:
        risks.append("No major validation risks were detected in the current aggregate signal.")
    return risks[:3]


def _build_why_this_matters(features: dict[str, float], result: dict[str, Any]) -> str:
    classification = str(result["demand_classification"])
    interpretation = str(result["investment_opportunity_interpretation"])
    confidence = float(result["confidence_score"]) * 100
    if result.get("unmet_demand_flag"):
        return (
            "Rising search activity and uneven engagement suggest latent demand that may not yet be fully served. "
            "This can point to delivery, pricing, or access gaps that deserve targeted market validation or policy support. "
            f"The current signal is classified as {classification.lower()} with {confidence:.1f}% confidence."
        )
    if features["trend_growth"] >= 0.45:
        return (
            "Momentum is building quickly, which can signal a near-term opening for investment, product positioning, or targeted outreach. "
            f"Signal currently reads as {classification.lower()}, and the dashboard interpretation is {interpretation.lower()}. "
            "This is useful for prioritizing early action while monitoring conversion quality."
        )
    return (
        "Current activity shows the market is moving, but the strength and quality of participation still matter. "
        f"Signal currently reads as {classification.lower()}, which helps frame whether this is a scaling opportunity, a monitoring case, or a policy watchpoint. "
        "Use this view alongside sector context and follow-on evidence before making large commitments."
    )


def _build_visual_components(result: dict[str, Any]) -> dict[str, str]:
    return {
        "confidence_gauge_html": _render_gauge_card("Confidence Gauge", float(result["confidence_score"]) * 100, "#2563eb"),
        "signal_strength_gauge_html": _render_gauge_card("Signal Strength Gauge", float(result["signal_strength_score"]), "#16a34a"),
        "momentum_indicator_html": _render_gauge_card("Trend Momentum Indicator", float(result["momentum_score"]), "#d97706"),
        "opportunity_radar_html": _render_radar_chart(
            {
                "Opportunity": float(result["opportunity_score"]),
                "Momentum": float(result["momentum_score"]),
                "Adoption": float(result["adoption_probability"]),
                "Persistence": float(result["persistence_score"]),
                "Viral": float(result["viral_probability"]),
            }
        ),
        "key_driver_cards_html": _render_key_driver_cards(
            result.get("key_drivers", []),
            result.get("risk_signals", []),
        ),
    }


def _render_gauge_card(title: str, value: float, color: str) -> str:
    safe_title = escape(title)
    width = max(0.0, min(float(value), 100.0))
    return (
        "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#ffffff;'>"
        f"<div style='font-size:13px;font-weight:600;color:#1f2937;margin-bottom:8px;'>{safe_title}</div>"
        f"<div style='font-size:24px;font-weight:700;color:#111827;margin-bottom:8px;'>{width:.1f}</div>"
        "<div style='height:12px;background:#eef2f7;border-radius:999px;overflow:hidden;'>"
        f"<div style='height:12px;width:{width:.1f}%;background:{color};border-radius:999px;'></div>"
        "</div>"
        "</div>"
    )


def _render_radar_chart(values: dict[str, float]) -> str:
    labels = list(values.keys())
    points: list[tuple[float, float]] = []
    center_x = 120.0
    center_y = 120.0
    radius = 84.0
    for index, label in enumerate(labels):
        angle = (-np.pi / 2) + (2 * np.pi * index / len(labels))
        scale = max(0.0, min(float(values[label]), 100.0)) / 100
        x = center_x + np.cos(angle) * radius * scale
        y = center_y + np.sin(angle) * radius * scale
        points.append((x, y))
    polygon = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    axis_labels = []
    for index, label in enumerate(labels):
        angle = (-np.pi / 2) + (2 * np.pi * index / len(labels))
        outer_x = center_x + np.cos(angle) * 102
        outer_y = center_y + np.sin(angle) * 102
        axis_labels.append(
            f"<text x='{outer_x:.1f}' y='{outer_y:.1f}' text-anchor='middle' font-size='11' fill='#334155'>{escape(label)}</text>"
        )
    return (
        "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#ffffff;'>"
        "<div style='font-size:13px;font-weight:600;color:#1f2937;margin-bottom:8px;'>Opportunity Radar Chart</div>"
        "<svg viewBox='0 0 240 240' width='100%' height='240'>"
        "<circle cx='120' cy='120' r='84' fill='none' stroke='#e2e8f0' stroke-width='1' />"
        "<circle cx='120' cy='120' r='56' fill='none' stroke='#e2e8f0' stroke-width='1' />"
        "<circle cx='120' cy='120' r='28' fill='none' stroke='#e2e8f0' stroke-width='1' />"
        f"<polygon points='{polygon}' fill='rgba(37,99,235,0.25)' stroke='#2563eb' stroke-width='2' />"
        + "".join(axis_labels)
        + "</svg></div>"
    )


def _render_key_driver_cards(drivers: list[str], risks: list[str]) -> str:
    driver_cards = []
    for driver in (drivers or ["Balanced aggregate demand profile"])[:3]:
        driver_cards.append(
            "<div style='flex:1;min-width:140px;border:1px solid #dbe3ef;border-radius:8px;padding:10px;background:#f8fafc;'>"
            f"<div style='font-size:12px;color:#475569;'>Key Driver</div><div style='font-size:14px;font-weight:600;color:#0f172a;'>{escape(driver)}</div></div>"
        )
    risk_markup = "".join(f"<li>{escape(risk)}</li>" for risk in (risks or [])[:2])
    return (
        "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#ffffff;'>"
        "<div style='font-size:13px;font-weight:600;color:#1f2937;margin-bottom:8px;'>Key Driver Summary Cards</div>"
        f"<div style='display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;'>{''.join(driver_cards)}</div>"
        "<div style='font-size:12px;color:#475569;'>Validation Signals</div>"
        f"<ul style='margin:6px 0 0 18px;color:#0f172a;font-size:13px;'>{risk_markup}</ul>"
        "</div>"
    )


def _build_hidden_trends_frame(raw_frame: pd.DataFrame, intelligence_frame: pd.DataFrame) -> pd.DataFrame:
    """Combine raw trend rows with Signal intelligence for hidden backend use."""

    if raw_frame.empty:
        raw_frame = pd.DataFrame(get_demo_trends("Kenya", limit=5))
    if intelligence_frame.empty:
        intelligence_frame = pd.DataFrame(analyze_trend_batch(raw_frame.to_dict(orient="records")))

    intelligence_columns = [
        "trend_name",
        "demand_classification",
        "confidence_score",
        "aggregate_demand_score",
        "opportunity_score",
        "emerging_trend_probability",
        "unmet_demand_probability",
        "investment_policy_interpretation",
        "model_source_explanation",
    ]
    available_columns = [column for column in intelligence_columns if column in intelligence_frame.columns]
    return raw_frame.merge(
        intelligence_frame[available_columns],
        on="trend_name",
        how="left",
        suffixes=("", "_signal"),
    )


def _active_trend_count(trends_df: pd.DataFrame) -> int:
    if trends_df.empty or "trend_name" not in trends_df.columns:
        return 0
    names = trends_df["trend_name"].fillna("").astype(str).str.strip()
    return int(((names != "") & (names.str.lower() != "unavailable")).sum())


def build_live_trend_html(trends_df: pd.DataFrame) -> str:
    """Convert the hidden trends dataframe into the public animated trend feed."""

    if trends_df.empty or "trend_name" not in trends_df.columns:
        trends_df = _build_hidden_trends_frame(
            pd.DataFrame(get_demo_trends("Kenya", limit=5)),
            pd.DataFrame(),
        )

    records = [
        record
        for record in trends_df.to_dict(orient="records")
        if str(record.get("trend_name", "")).strip().lower() not in {"", "unavailable"}
    ]
    if not records:
        records = get_demo_trends("Kenya", limit=5)

    active_count = len(records)
    location = records[0].get("location", "Kenya")
    fallback_note = (
        "<div class='signal-trend-classification'>Live API unavailable — displaying demo aggregate trends.</div>"
        if any("Demo fallback" in str(record.get("source", "")) for record in records)
        else ""
    )
    cards = [_render_public_trend_issue(record) for record in records]
    duration = max(18, min(40, len(cards) * 5))
    rail_markup = "".join(cards + cards)
    return (
        "<div class='signal-trend-shell'>"
        "<div class='signal-trend-header'>"
        "<div>"
        "<div class='signal-trend-kicker'>Behavioral Signals AI</div>"
        "<div class='signal-trend-title'>Live Trend Intelligence</div>"
        f"<div class='signal-trend-meta'><span class='signal-trend-pill'>Location: {escape(str(location))}</span>"
        f"<span class='signal-trend-pill'>Updated: {escape(_utc_timestamp())}</span></div>"
        "</div>"
        f"<div class='signal-trend-count'><strong>{active_count}</strong><span>active trends</span></div>"
        "</div>"
        f"{fallback_note}"
        f"<div class='signal-trend-viewport' style='--signal-trend-duration:{duration}s;'>"
        f"<div class='signal-trend-rail'>{rail_markup}</div>"
        "</div>"
        "</div>"
    )


def _render_public_trend_issue(record: dict[str, Any]) -> str:
    trend_name = escape(str(record.get("trend_name", "Monitoring trend")))
    source = escape(str(record.get("source", "Aggregate trend feed")))
    location = escape(str(record.get("location", "Kenya")))
    confidence = _safe_float(record.get("confidence_score"), 0.0)
    confidence_label = f"Confidence {confidence:.1f}%" if confidence > 0 else "Confidence pending"
    return (
        "<div class='signal-trend-issue'>"
        f"<div class='signal-trend-issue-name'>{trend_name}</div>"
        "<div class='signal-trend-issue-meta'>"
        f"<span class='signal-trend-pill'>{location}</span>"
        f"<span class='signal-trend-pill'>{escape(confidence_label)}</span>"
        f"<span class='signal-trend-pill'>{source}</span>"
        "</div>"
        "</div>"
    )


def _format_volume(value: Any) -> str:
    if isinstance(value, (int, float)) and not pd.isna(value):
        return f"{int(value):,} posts"
    return "Volume unavailable"


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _format_timestamp(value: Any) -> str:
    if not value:
        return _utc_timestamp()
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return str(value)


def _utc_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")


def _uploaded_path(file_obj: Any | None) -> str | None:
    if file_obj is None:
        return None
    return str(getattr(file_obj, "name", file_obj))


def _uploaded_text(file_obj: Any | None) -> str:
    path = _uploaded_path(file_obj)
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8")


def _balance_rows_to_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Account | Row Total | Column Total | Imbalance | Percentage Imbalance |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['account']} | {row['row_total']} | {row['column_total']} | "
            f"{row['imbalance']} | {row['percentage_imbalance']} |"
        )
    return "\n".join(lines)


def _dashboard_status_banner() -> str:
    mode = "Live API available" if os.getenv("X_BEARER_TOKEN", "").strip() else "Demo fallback"
    return (
        "<div style='border:1px solid #cbd5e1;border-radius:10px;padding:14px 16px;margin:0 0 12px 0;"
        "background:#f8fafc;color:#0f172a;'>"
        "<div style='font-size:22px;font-weight:800;margin-bottom:8px;'>Signal AI Dashboard</div>"
        "<div style='display:flex;gap:8px;flex-wrap:wrap;'>"
        "<span style='border:1px solid #bbf7d0;background:#ecfdf5;border-radius:999px;padding:5px 10px;font-weight:700;'>Status: Running</span>"
        f"<span style='border:1px solid #bfdbfe;background:#eff6ff;border-radius:999px;padding:5px 10px;font-weight:700;'>Mode: {escape(mode)}</span>"
        "<span style='border:1px solid #e2e8f0;background:#ffffff;border-radius:999px;padding:5px 10px;font-weight:700;'>Privacy: Aggregate signals only, no individual tracking</span>"
        "</div>"
        "</div>"
    )


def _behavioral_section_intro() -> str:
    return (
        "## Behavioral Signals AI\n"
        "Estimate demand, opportunity, confidence, unmet demand, and market signal strength from aggregate behavioural inputs."
    )


def _how_to_use_signal_markdown() -> str:
    return (
        "1. Adjust behavioural signal inputs.\n"
        "2. Click **Predict Demand**.\n"
        "3. Review demand classification and opportunity score.\n"
        "4. Use Live Trend Intelligence to compare current topical issues."
    )


def _model_interpretation_markdown() -> str:
    return (
        "- **Demand Classification:** Overall demand band inferred from aggregate signal quality.\n"
        "- **Confidence Score:** How strongly Signal trusts the current classification.\n"
        "- **Aggregate Demand Score:** Combined demand intensity from engagement and search proxies.\n"
        "- **Opportunity Score:** Estimated market or policy action potential.\n"
        "- **Unmet Demand Probability:** Likelihood that attention reflects access, affordability, or delivery gaps.\n"
        "- **Emerging Trend Probability:** Likelihood that the signal is gaining early momentum.\n"
        "- **Volatility / Noise Score:** Risk that the signal is unstable, noisy, or not yet decision-ready."
    )


def _fallback_live_trend_html(message: str = "Live API unavailable — displaying demo aggregate trends.") -> str:
    return f"""
<div style="border:1px solid #ddd; border-radius:12px; padding:14px; margin:10px 0; background:#fff;">
  <h3 style="margin:0 0 6px 0;">Live Trend Intelligence</h3>
  <div style="font-weight:600; margin-bottom:4px;">8 active trends</div>
  <div style="font-size:13px; color:#475569; margin-bottom:8px;">{escape(message)}</div>

  <style>
    .signal-trend-box {{
      height: 140px;
      overflow: hidden;
      position: relative;
      border-radius: 10px;
      background: #f8f9fa;
      padding: 8px;
    }}
    .signal-trend-scroll {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      animation: signal-scroll-up 10s linear infinite;
    }}
    .signal-trend-item {{
      padding: 8px 10px;
      border-radius: 8px;
      background: white;
      border: 1px solid #eee;
      font-weight: 600;
    }}
    @keyframes signal-scroll-up {{
      0% {{ transform: translateY(100%); }}
      100% {{ transform: translateY(-100%); }}
    }}
  </style>

  <div class="signal-trend-box">
    <div class="signal-trend-scroll">
      <div class="signal-trend-item">Cost of living</div>
      <div class="signal-trend-item">Fuel prices</div>
      <div class="signal-trend-item">Finance Bill</div>
      <div class="signal-trend-item">Jobs and youth employment</div>
      <div class="signal-trend-item">School fees</div>
      <div class="signal-trend-item">Healthcare access</div>
      <div class="signal-trend-item">Electricity prices</div>
      <div class="signal-trend-item">Agriculture prices</div>
    </div>
  </div>
</div>
"""


with gr.Blocks(title="Signal AI Dashboard", css=SIGNAL_DASHBOARD_CSS) as demo:
    gr.HTML(value=_dashboard_status_banner())
    gr.Markdown(
        "Behavioral intelligence and AI-native CGE simulation for policy analysis."
    )

    with gr.Tab("Behavioral Signals AI"):
        gr.Markdown(_behavioral_section_intro())
        with gr.Accordion("How to Use Signal", open=False):
            gr.Markdown(_how_to_use_signal_markdown())
        with gr.Accordion("Model Interpretation Guide", open=False):
            gr.Markdown(_model_interpretation_markdown())
        live_trend_feed = gr.HTML(value=_fallback_live_trend_html())
        with gr.Row():
            with gr.Column():
                likes = gr.Number(label="Likes", value=120, precision=0)
                comments = gr.Number(label="Comments", value=35, precision=0)
                shares = gr.Number(label="Shares", value=24, precision=0)
                searches = gr.Number(label="Searches", value=160, precision=0)
                engagement_intensity = gr.Slider(0, 1, value=0.55, label="Engagement Intensity")
                purchase_intent_score = gr.Slider(0, 1, value=0.7, label="Purchase Intent Score")
                trend_growth = gr.Slider(0, 1, value=0.35, label="Trend Growth")
                predict_button = gr.Button("Predict Demand")

            with gr.Column():
                with gr.Row():
                    demand_output = gr.Textbox(label="Demand Classification", interactive=False)
                    confidence_output = gr.Number(label="Confidence Score (%)", interactive=False)
                with gr.Row():
                    aggregate_output = gr.Number(label="Aggregate Demand Score", interactive=False)
                    opportunity_output = gr.Number(label="Opportunity Score", interactive=False)
                with gr.Row():
                    emerging_output = gr.Number(label="Emerging Trend Probability (%)", interactive=False)
                    unmet_output = gr.Number(label="Unmet Demand Probability (%)", interactive=False)
                interpretation_output = gr.Textbox(label="Investment / Policy Interpretation", lines=2, interactive=False)
                with gr.Row():
                    signal_strength_output = gr.Number(label="Signal Strength Score", interactive=False)
                    momentum_score_output = gr.Number(label="Momentum Score", interactive=False)
                    volatility_output = gr.Number(label="Volatility / Noise Score", interactive=False)
                with gr.Row():
                    persistence_output = gr.Number(label="Persistence Score", interactive=False)
                    adoption_output = gr.Number(label="Adoption Probability", interactive=False)
                    viral_output = gr.Number(label="Viral Probability", interactive=False)
                why_matters_output = gr.Textbox(label="Why This Matters", lines=4, interactive=False)
                with gr.Accordion("Technical Model Source and Explanation", open=False):
                    source_output = gr.Textbox(label="Model Source and Explanation", lines=16, interactive=False)

        with gr.Row():
            confidence_gauge_output = gr.HTML(label="Confidence Gauge")
            signal_strength_gauge_output = gr.HTML(label="Signal Strength Gauge")
            momentum_indicator_output = gr.HTML(label="Trend Momentum Indicator")

        with gr.Row():
            opportunity_radar_output = gr.HTML(label="Opportunity Radar Chart")
            key_driver_cards_output = gr.HTML(label="Key Driver Summary Cards")

        with gr.Row():
            trends_location = gr.Dropdown(
                label="Trend Location",
                choices=["Kenya", "Nairobi", "Global"],
                value="Kenya",
            )
            trends_limit = gr.Slider(label="Number of Trends", minimum=3, maximum=10, step=1, value=5)
            refresh_trends_button = gr.Button("Refresh Trends")
        live_trend_ticker_output = gr.HTML(label="Live Trend Intelligence", visible=False)
        active_trends_output = gr.Number(label="Active Trends", precision=0, interactive=False, visible=False)
        trends_table = gr.Dataframe(
            label="Hidden Trends Table",
            headers=[
                "trend_name",
                "rank",
                "tweet_volume",
                "location",
                "fetched_at",
                "source",
                "demand_classification",
                "confidence_score",
                "aggregate_demand_score",
                "opportunity_score",
                "emerging_trend_probability",
                "unmet_demand_probability",
                "investment_policy_interpretation",
                "model_source_explanation",
            ],
            interactive=False,
            visible=False,
        )
        trend_intelligence_table = gr.Dataframe(
            label="Hidden Signal Intelligence Table",
            headers=[
                "trend_name",
                "location",
                "rank",
                "tweet_volume",
                "source",
                "fetched_at",
                "demand_classification",
                "confidence_score",
                "aggregate_demand_score",
                "opportunity_score",
                "emerging_trend_probability",
                "unmet_demand_probability",
                "investment_policy_interpretation",
                "model_source_explanation",
            ],
            interactive=False,
            visible=False,
        )
        trends_summary = gr.Textbox(label="Interpretation Summary", lines=6, interactive=False, visible=False)
        trend_outputs = [
            trends_table,
            live_trend_feed,
            active_trends_output,
            trends_summary,
            trend_intelligence_table,
        ]
        trend_timer = gr.Timer(value=6, active=True)
        refresh_trends_button.click(
            fn=refresh_live_trend_intelligence,
            inputs=[trends_location, trends_limit],
            outputs=trend_outputs,
            show_api=False,
        )
        trends_location.change(
            fn=refresh_live_trend_intelligence,
            inputs=[trends_location, trends_limit],
            outputs=trend_outputs,
            show_api=False,
        )
        trends_limit.change(
            fn=refresh_live_trend_intelligence,
            inputs=[trends_location, trends_limit],
            outputs=trend_outputs,
            show_api=False,
        )
        trend_timer.tick(
            fn=refresh_live_trend_intelligence,
            inputs=[trends_location, trends_limit],
            outputs=trend_outputs,
            show_api=False,
        )
        demo.load(
            fn=refresh_live_trend_intelligence,
            inputs=[trends_location, trends_limit],
            outputs=trend_outputs,
            show_api=False,
        )

        live_inputs = [
            likes,
            comments,
            shares,
            searches,
            engagement_intensity,
            purchase_intent_score,
            trend_growth,
        ]
        live_outputs = [
            demand_output,
            confidence_output,
            aggregate_output,
            opportunity_output,
            emerging_output,
            unmet_output,
            interpretation_output,
            source_output,
            signal_strength_output,
            momentum_score_output,
            volatility_output,
            persistence_output,
            adoption_output,
            viral_output,
            why_matters_output,
            confidence_gauge_output,
            signal_strength_gauge_output,
            momentum_indicator_output,
            opportunity_radar_output,
            key_driver_cards_output,
        ]
        for input_component in live_inputs:
            input_component.change(
                fn=update_behavioral_dashboard,
                inputs=live_inputs,
                outputs=live_outputs,
                show_api=False,
            )
        predict_button.click(
            fn=update_behavioral_dashboard,
            inputs=live_inputs,
            outputs=live_outputs,
            show_api=False,
        )
        demo.load(
            fn=update_behavioral_dashboard,
            inputs=live_inputs,
            outputs=live_outputs,
            show_api=False,
        )

    with gr.Tab("Signal CGE"):
        gr.Markdown(
            "## Signal CGE\n"
            "AI-native CGE simulation engine for policy prompts, SAM calibration, scenario execution, diagnostics, and policy interpretation."
        )
        signal_cge_prompt = gr.Textbox(
            label="Enter simulation prompt",
            placeholder=(
                "reduce import tariffs on cmach by 10%\n"
                "Simulate a 10 percent increase in government spending on care infrastructure.\n"
                "Run a VAT increase scenario and show household welfare effects.\n"
                "Double investment in care services and report GDP, employment, and household income effects.\n"
                "Simulate an import tariff reduction and explain trade, prices, and welfare impacts."
            ),
            value="reduce import tariffs on cmach by 10%",
            lines=6,
        )
        with gr.Accordion("Optional: Upload custom SAM/workbook", open=False):
            gr.Markdown(
                "No upload is required. Signal CGE uses the canonical model stored in the repository unless a custom file is uploaded."
            )
            signal_cge_upload = gr.File(
                label="Upload SAM or experiment workbook",
                file_types=[".xlsx", ".csv"],
            )
        run_signal_cge_button = gr.Button("Run Signal CGE Simulation")
        signal_cge_summary_cards = gr.HTML(label="Results Summary")
        signal_cge_results_table = gr.Dataframe(label="Results Table", interactive=False)
        signal_cge_effect_chart = gr.BarPlot(
            label="Scenario effects",
            x="metric",
            y="effect",
            title="Signal CGE Scenario Effects",
            tooltip=["metric", "effect"],
            vertical=False,
        )
        signal_cge_reference_output = gr.Markdown(label="Model Reference Used")
        signal_cge_interpretation_output = gr.Markdown(label="Scenario Interpretation")
        signal_cge_diagnostics_output = gr.Markdown(label="Diagnostics")
        with gr.Row():
            signal_cge_json_download = gr.File(label="Download JSON results")
            signal_cge_csv_download = gr.File(label="Download CSV results")
            signal_cge_brief_download = gr.File(label="Download Markdown policy brief")
        run_signal_cge_button.click(
            fn=signal_cge_prompt_ui,
            inputs=[signal_cge_prompt, signal_cge_upload],
            outputs=[
                signal_cge_summary_cards,
                signal_cge_effect_chart,
                signal_cge_results_table,
                signal_cge_reference_output,
                signal_cge_interpretation_output,
                signal_cge_diagnostics_output,
                signal_cge_brief_download,
                signal_cge_json_download,
                signal_cge_csv_download,
            ],
            show_api=False,
        )

    gr.Markdown(
        "Signal is a privacy-preserving AI dashboard for aggregate behavioural signal intelligence, "
        "policy insight, and market demand analysis."
    )


if __name__ == "__main__":
    demo.launch(show_api=False)
