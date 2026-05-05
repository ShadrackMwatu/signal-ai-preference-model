"""Hugging Face app entrypoint for Signal AI Dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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


def predict_demand(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float]:
    """Return demand label, aggregate demand score, and opportunity score without crashing."""

    try:
        likes = float(likes or 0)
        comments = float(comments or 0)
        shares = float(shares or 0)
        searches = float(searches or 0)
        engagement_intensity = float(engagement_intensity or 0)
        purchase_intent_score = float(purchase_intent_score or 0)
        trend_growth = float(trend_growth or 0)

        # Step A: Compute engagement score
        engagement_score = (likes + comments + shares + searches) / 4

        # Step B: Prepare feature vector
        features = [[
            float(engagement_score),
            float(engagement_intensity),
            float(purchase_intent_score),
            float(trend_growth),
        ]]

        # Step C: Try loading model
        try:
            import joblib

            model = joblib.load("model.pkl")
            prediction = model.predict(features)[0]
        except Exception:
            # Fallback rule-based logic
            if purchase_intent_score > 0.7 and trend_growth > 0.5:
                prediction = 2
            elif purchase_intent_score > 0.4:
                prediction = 1
            else:
                prediction = 0

        # Step D: Map labels
        demand_label = _map_demand_label(prediction)

        # Step E: Opportunity score
        opportunity_score = (purchase_intent_score + trend_growth) / 2

        return (
            demand_label,
            round(engagement_score, 2),
            round(opportunity_score, 2),
        )

    except Exception as exc:
        return (
            f"Error: {str(exc)}",
            0,
            0,
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
