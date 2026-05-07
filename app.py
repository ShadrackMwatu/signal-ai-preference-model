"""Hugging Face app entrypoint for Signal AI Dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

import gradio as gr


ADVANCED_IMPORT_ERROR = ""

try:
    from src.cge.framework import DEFAULT_SCENARIO, run_policy_scenario
    from signal_execution.runner import SignalRunner
    from signal_learning.adaptation_engine import propose_adaptations
    from signal_learning.implementation_engine import implement_adaptation, rollback_adaptation
    from signal_learning.learning_store import LearningStore
    from signal_learning.pattern_extractor import recurring_issue_summary
    from signal_modeling_language.parser import parse_sml_text
    from signal_modeling_language.validator import validate_model

    ADVANCED_AVAILABLE = True
except Exception as exc:  # pragma: no cover - exercised in constrained Space runtimes.
    ADVANCED_AVAILABLE = False
    ADVANCED_IMPORT_ERROR = str(exc)
    DEFAULT_SCENARIO = "Baseline policy scenario"


SML_EXAMPLE_PATH = Path("signal_modeling_language/examples/basic_cge.sml")
DEFAULT_SML_TEXT = SML_EXAMPLE_PATH.read_text(encoding="utf-8") if SML_EXAMPLE_PATH.exists() else ""
ROOT_DIR = Path(__file__).resolve().parent
PRIMARY_MODEL_PATH = ROOT_DIR / "models" / "model.pkl"
LEGACY_MODEL_PATH = ROOT_DIR / "model.pkl"
PRIMARY_MODEL_METADATA_PATH = ROOT_DIR / "models" / "metadata.json"


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
            "prediction_source": "error",
            "explanation_note": f"Prediction pipeline failed: {exc}",
        }


def predict_demand(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float]:
    """Backward-compatible Gradio callback with model-first behavior."""

    result = predict_demand_details(
        likes,
        comments,
        shares,
        searches,
        engagement_intensity,
        purchase_intent_score,
        trend_growth,
    )
    return (
        str(result["demand_classification"]),
        round(float(result["aggregate_demand_score"]), 2),
        round(float(result["opportunity_score"]), 2),
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

    label, aggregate_score, opportunity_score = predict_demand(
        likes,
        comments,
        shares,
        searches,
        engagement_intensity,
        purchase_intent_score,
        trend_growth,
    )
    legacy_label = {
        "High Demand": "High",
        "Moderate Demand": "Moderate",
        "Low Demand": "Low",
    }.get(label, label)
    legacy_aggregate_score = max(0.0, min(100.0, float(aggregate_score)))
    legacy_opportunity_score = float(opportunity_score) * 100 if opportunity_score <= 1 else float(opportunity_score)
    return legacy_label, legacy_aggregate_score, max(0.0, min(100.0, legacy_opportunity_score))


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


def validate_sml_dashboard(sml_text: str, sml_file: Any | None = None) -> str:
    """Validate SML from dashboard text or upload."""

    try:
        if not ADVANCED_AVAILABLE:
            raise RuntimeError(f"Advanced Signal modules unavailable: {ADVANCED_IMPORT_ERROR}")

        text = _uploaded_text(sml_file) or sml_text or DEFAULT_SML_TEXT
        validation = validate_model(parse_sml_text(text))
        status = "Valid" if validation.valid else "Invalid"
        parts = [f"Status: {status}"]
        if validation.errors:
            parts.append("Errors:\n" + "\n".join(f"- {error}" for error in validation.errors))
        if validation.warnings:
            parts.append("Warnings:\n" + "\n".join(f"- {warning}" for warning in validation.warnings))
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
    return "Low Demand"


def _safe_float(value: Any) -> float:
    return float(value or 0)


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
    prediction = _map_demand_label(model.predict(frame)[0])
    probabilities = model.predict_proba(frame)[0] if hasattr(model, "predict_proba") else np.array([1.0])
    classes = [str(label) for label in getattr(model, "classes_", ["Low Demand", "Moderate Demand", "High Demand"])]
    class_probabilities = {label: float(prob) for label, prob in zip(classes, probabilities)}
    confidence_score = float(max(class_probabilities.values(), default=1.0))
    aggregate_demand_score = float(
        np.clip(
            (
                class_probabilities.get("High Demand", 0.0) * 1.0
                + class_probabilities.get("Moderate Demand", 0.0) * 0.6
                + class_probabilities.get("Low Demand", 0.0) * 0.25
            )
            * 100,
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
        "demand_classification": prediction,
        "confidence_score": round(confidence_score, 4),
        "aggregate_demand_score": round(aggregate_demand_score, 2),
        "opportunity_score": round(opportunity_score, 2),
        "unmet_demand_probability": round(unmet_probability, 4),
        "emerging_trend_probability": round(emerging_probability, 4),
        "prediction_source": "trained model",
        "explanation_note": "Primary prediction produced by the trained local Signal model.",
    }


def _predict_with_fallback(features: dict[str, float]) -> dict[str, Any]:
    latent = np.clip(
        features["engagement_intensity"] * 0.28
        + features["trend_growth"] * 0.2
        + features["urgency_score"] * 0.16
        + features["repetition_score"] * 0.1
        + features["opportunity_index"] * 0.26,
        0,
        1,
    )
    if latent >= 0.68:
        demand = "High Demand"
    elif latent >= 0.42:
        demand = "Moderate Demand"
    else:
        demand = "Low Demand"

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
        "demand_classification": demand,
        "confidence_score": round(confidence_score, 4),
        "aggregate_demand_score": round(aggregate_demand_score, 2),
        "opportunity_score": round(opportunity_score, 2),
        "unmet_demand_probability": round(unmet_probability, 4),
        "emerging_trend_probability": round(emerging_probability, 4),
        "prediction_source": "fallback model",
        "explanation_note": "Fallback scoring used because the trained model artifact was unavailable.",
    }


def _apply_guardrails(result: dict[str, Any], features: dict[str, float]) -> dict[str, Any]:
    demand = str(result["demand_classification"])
    opportunity = float(result["opportunity_score"])
    unmet_probability = float(result["unmet_demand_probability"])
    emerging_probability = float(result["emerging_trend_probability"])
    notes = [str(result["explanation_note"])]

    if demand == "High Demand" and opportunity >= 70:
        interpretation = "Strong Investment Opportunity"
    elif demand == "Moderate Demand" and opportunity >= 55:
        interpretation = "Emerging Opportunity"
    elif demand == "Low Demand" and opportunity >= 55:
        interpretation = "Investigate Anomaly / Possible Unmet Demand"
        unmet_probability = max(unmet_probability, float(np.clip(features["unmet_need_signal"], 0, 1)))
        notes.append("Guardrail flagged a contradiction between low demand and elevated opportunity.")
    else:
        interpretation = "Weak Signal"

    if features["noise_score"] >= 0.75:
        notes.append("High noise score suggests more data quality review before acting.")
    if demand == "Moderate Demand" and emerging_probability >= 0.6:
        notes.append("Guardrail marked this as a near-term emerging trend candidate.")

    result = dict(result)
    result["investment_opportunity_interpretation"] = interpretation
    result["unmet_demand_flag"] = bool(unmet_probability >= 0.6)
    result["emerging_trend_flag"] = bool(emerging_probability >= 0.55)
    result["explanation_note"] = " ".join(notes)
    if len(notes) > 1:
        result["prediction_source"] = f"{result['prediction_source']} + rule-based guardrail"
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


with gr.Blocks(title="Signal AI Market Intelligence") as demo:
    gr.Markdown("# Signal")
    gr.Markdown(
        "Behavioral Signals AI for revealed demand intelligence, plus a Signal CGE "
        "Modelling Framework for policy simulation and GAMS-compatible exports."
    )

    with gr.Tab("Behavioral Signals AI"):
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
                demand_output = gr.Markdown(label="Demand Classification")
                aggregate_output = gr.Number(label="Aggregate Demand Score")
                opportunity_output = gr.Number(label="Opportunity Score")

        predict_button.click(
            fn=predict_demand,
            inputs=[
                likes,
                comments,
                shares,
                searches,
                engagement_intensity,
                purchase_intent_score,
                trend_growth,
            ],
            outputs=[
                demand_output,
                aggregate_output,
                opportunity_output,
            ],
        )

    with gr.Tab("Signal CGE Framework"):
        scenario_input = gr.Textbox(label="CGE Scenario", value=DEFAULT_SCENARIO, lines=8)
        run_cge_button = gr.Button("Run CGE Scenario")
        with gr.Row():
            cge_summary_output = gr.Textbox(label="CGE Simulation Summary", lines=9)
            cge_policy_output = gr.Code(label="Policy Intelligence", language="json", lines=14)
        gams_output = gr.Code(label="GAMS Compatibility Preview", language="python", lines=18)
        run_cge_button.click(
            fn=cge_model,
            inputs=[scenario_input],
            outputs=[cge_summary_output, cge_policy_output, gams_output],
        )

    with gr.Tab("SML CGE Workbench"):
        sam_upload = gr.File(label="Upload SAM CSV/XLSX", file_types=[".csv", ".xlsx", ".xls"])
        sml_upload = gr.File(label="Upload SML Model", file_types=[".sml", ".txt"])
        sml_editor = gr.Textbox(label="Signal Modelling Language", value=DEFAULT_SML_TEXT, lines=20)
        validate_sml_button = gr.Button("Validate Model")
        run_sml_button = gr.Button("Run Scenario")
        validation_output = gr.Textbox(label="Validation", lines=8)
        balance_output = gr.Markdown(label="Balance Check")
        sml_results_output = gr.Code(label="Results", language="json", lines=16)
        report_download = gr.File(label="Download Policy Report")
        validate_sml_button.click(
            fn=validate_sml_dashboard,
            inputs=[sml_editor, sml_upload],
            outputs=[validation_output],
        )
        run_sml_button.click(
            fn=run_sml_dashboard,
            inputs=[sml_editor, sml_upload, sam_upload],
            outputs=[validation_output, balance_output, sml_results_output, report_download],
        )

    with gr.Tab("Learning"):
        refresh_learning_button = gr.Button("Refresh Learning")
        with gr.Row():
            recent_lessons_output = gr.Code(label="Recent Lessons", language="json", lines=16)
            recurring_issues_output = gr.Code(label="Recurring Issues", language="json", lines=16)
        recommended_fixes_output = gr.Code(label="Recommended Fixes", language="json", lines=14)
        apply_learning_button = gr.Button("Apply Latest Low-Risk Fix")
        ignore_learning_button = gr.Button("Ignore Latest Recommendation")
        learning_action_output = gr.Code(label="Learning Action Result", language="json", lines=10)
        rollback_version_input = gr.Textbox(label="Rollback Version", value="v001")
        rollback_learning_button = gr.Button("Rollback")
        refresh_learning_button.click(
            fn=refresh_learning_dashboard,
            inputs=[],
            outputs=[recent_lessons_output, recurring_issues_output, recommended_fixes_output],
        )
        apply_learning_button.click(fn=apply_latest_learning_dashboard, inputs=[], outputs=[learning_action_output])
        ignore_learning_button.click(fn=ignore_latest_learning_dashboard, inputs=[], outputs=[learning_action_output])
        rollback_learning_button.click(
            fn=rollback_learning_dashboard,
            inputs=[rollback_version_input],
            outputs=[learning_action_output],
        )


if __name__ == "__main__":
    demo.launch()
