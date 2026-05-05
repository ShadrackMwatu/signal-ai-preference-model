"""Hugging Face app entrypoint for Signal AI Dashboard."""

from __future__ import annotations

import json
from pathlib import Path

import gradio as gr

ADVANCED_IMPORT_ERROR = ""

try:
    from joblib import load

    from src.cge.framework import DEFAULT_SCENARIO, run_policy_scenario
    from src.models.signal_demand_model import FEATURE_COLUMNS, MODEL_PATH, train_signal_model
    from signal_learning.adaptation_engine import propose_adaptations
    from signal_learning.implementation_engine import implement_adaptation, rollback_adaptation
    from signal_learning.learning_store import LearningStore
    from signal_learning.pattern_extractor import recurring_issue_summary
    from signal_execution.runner import SignalRunner
    from signal_modeling_language.parser import parse_sml_text
    from signal_modeling_language.validator import validate_model

    ADVANCED_AVAILABLE = True

except Exception as exc:
    ADVANCED_AVAILABLE = False
    ADVANCED_IMPORT_ERROR = str(exc)

if not ADVANCED_AVAILABLE:
    FEATURE_COLUMNS = [
        "likes",
        "comments",
        "shares",
        "searches",
        "engagement_intensity",
        "purchase_intent_score",
        "trend_growth",
    ]
    MODEL_PATH = "model.pkl"
    DEFAULT_SCENARIO = "Baseline policy scenario"

    def train_signal_model(*args, **kwargs):
        return None

def fallback_signal_dashboard(topic, county):
    return (
        f"Signal AI Dashboard is running.\n\n"
        f"Topic: {topic}\n"
        f"County: {county}\n\n"
        f"Advanced Signal modules are not fully available yet.\n"
        f"Import issue: {ADVANCED_IMPORT_ERROR}"
    )


if False:
    with gr.Blocks(title="Signal AI Dashboard") as demo:
        gr.Markdown("# Signal AI Dashboard")
        gr.Markdown(
            "The basic dashboard is running. Advanced model/CGE modules will load once all project files and dependencies are available."
        )

        topic = gr.Textbox(label="Topic", value="Cost of living")
        county = gr.Textbox(label="County", value="Nairobi")
        output = gr.Textbox(label="Signal output", lines=8)

        btn = gr.Button("Run Signal")
        btn.click(fallback_signal_dashboard, inputs=[topic, county], outputs=output)

else:

    def _load_deployed_model():
        model_path = Path(MODEL_PATH)
        try:
            if not model_path.exists():
                raise FileNotFoundError(f"Trained model not found: {model_path}")

            loaded_model = load(model_path)

            if isinstance(loaded_model, dict) and "model" in loaded_model:
                loaded_model = loaded_model["model"]

            if getattr(loaded_model, "n_features_in_", len(FEATURE_COLUMNS)) != len(FEATURE_COLUMNS):
                train_signal_model(model_path=model_path)
                loaded_model = load(model_path)

            return loaded_model, ""

        except Exception as exc:
            return None, str(exc)


    model, MODEL_LOAD_ERROR = _load_deployed_model()

    SML_EXAMPLE_PATH = Path("signal_modeling_language/examples/basic_cge.sml")
    DEFAULT_SML_TEXT = (
        SML_EXAMPLE_PATH.read_text(encoding="utf-8")
        if SML_EXAMPLE_PATH.exists()
        else ""
    )

def signal_model(
    likes,
    comments,
    shares,
    searches,
    engagement_intensity,
    purchase_intent_score,
    trend_growth,
):
    try:
        # =========================
        # 1. INPUT PROCESSING
        # =========================
        likes = float(likes)
        comments = float(comments)
        shares = float(shares)
        searches = float(searches)
        engagement_intensity = float(engagement_intensity)
        purchase_intent_score = float(purchase_intent_score)
        trend_growth = float(trend_growth)

        # =========================
        # 2. FEATURE ENGINEERING
        # =========================
        engagement_volume = (likes + comments + shares + searches) / 4

        aggregate_demand_score = round(
            engagement_volume * engagement_intensity,
            2,
        )

        opportunity_score = round(
            ((purchase_intent_score + trend_growth) / 2) * 100,
            2,
        )

        # =========================
        # 3. ML PREDICTION (PRIMARY)
        # =========================
        demand_class = None
        confidence_score = 0.0
        prediction_source = "Fallback"

        if model is not None:
            try:
                features = [[
                    likes,
                    comments,
                    shares,
                    searches,
                    engagement_intensity,
                    purchase_intent_score,
                    trend_growth,
                ]]

                pred = model.predict(features)[0]
                demand_class = str(pred)

                if hasattr(model, "predict_proba"):
                    confidence_score = float(max(model.predict_proba(features)[0]))
                else:
                    confidence_score = 0.6  # default fallback

                prediction_source = "ML Model"

            except Exception:
                demand_class = None

        # =========================
        # 4. FALLBACK LOGIC (SAFE)
        # =========================
        if demand_class is None:
            if purchase_intent_score >= 0.7 and trend_growth >= 0.5:
                demand_class = "High Demand"
            elif purchase_intent_score >= 0.4 or engagement_intensity >= 0.5:
                demand_class = "Moderate Demand"
            else:
                demand_class = "Low Demand"

            confidence_score = 0.5

        # =========================
        # 5. ANOMALY DETECTION
        # =========================
        anomaly_flag = False

        if demand_class == "Low Demand" and opportunity_score > 65:
            anomaly_flag = True

        if engagement_volume < 20 and purchase_intent_score > 0.7:
            anomaly_flag = True

        # =========================
        # 6. GUARDRAIL INTELLIGENCE
        # =========================
        if demand_class == "High Demand" and opportunity_score >= 60:
            signal = "Strong Investment Opportunity"

        elif demand_class == "Moderate Demand" and opportunity_score >= 55:
            signal = "Emerging Opportunity"

        elif demand_class == "Low Demand" and opportunity_score >= 60:
            signal = "Unmet Demand / Market Gap"

        elif demand_class == "Low Demand" and opportunity_score < 50:
            signal = "Weak Signal"

        else:
            signal = "Monitor"

        # =========================
        # 7. POLICY-GRADE INTERPRETATION
        # =========================
        if signal == "Strong Investment Opportunity":
            recommendation = "Scale investment, expand supply, prioritize financing"

        elif signal == "Emerging Opportunity":
            recommendation = "Monitor growth, pilot investments, validate demand"

        elif signal == "Unmet Demand / Market Gap":
            recommendation = "Investigate barriers (pricing, access, awareness)"

        elif signal == "Weak Signal":
            recommendation = "Do not allocate resources, low priority"

        else:
            recommendation = "Collect more data before acting"

        # =========================
        # 8. OUTPUT (CLEAN + POLICY READY)
        # =========================
        output_text = f"""
### 📊 Signal Result

**Demand Level:** {demand_class}  
**Opportunity Classification:** {signal}  
**Recommendation:** {recommendation}  

---

**📈 Aggregate Demand Score:** {aggregate_demand_score}  
**🚀 Opportunity Score:** {opportunity_score}  
**📊 Confidence:** {round(confidence_score * 100, 2)}%  
**⚠️ Anomaly Detected:** {'YES' if anomaly_flag else 'NO'}  
**🧠 Source:** {prediction_source}
"""
    """
   
return output_text, aggregate_demand_score, opportunity_score

    except Exception as e:
        return f"Signal system error: {str(e)}", 0, 0

    def cge_model(scenario_text):
        try:
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


    def _uploaded_path(file_obj):
        if file_obj is None:
            return None
        return str(getattr(file_obj, "name", file_obj))


    def _uploaded_text(file_obj):
        path = _uploaded_path(file_obj)
        if not path:
            return ""
        return Path(path).read_text(encoding="utf-8")


    def _balance_rows_to_markdown(rows):
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


    def validate_sml_dashboard(sml_text, sml_file=None):
        try:
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


    def run_sml_dashboard(sml_text, sml_file=None, sam_file=None):
        try:
            text = _uploaded_text(sml_file) or sml_text or DEFAULT_SML_TEXT
            sam_path = _uploaded_path(sam_file)

            result = SignalRunner().run(sml_text=text, sam_override=sam_path)
            validation = result["validation"]

            balance_rows = validation["balance_check"]
            balance_text = _balance_rows_to_markdown(balance_rows[:12])

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
                validation_text += "\n\nWarnings:\n" + "\n".join(
                    f"- {warning}" for warning in validation["warnings"]
                )

            return validation_text, balance_text, json.dumps(result_view, indent=2), str(result["report_path"])

        except Exception as exc:
            return f"Status: Failed\n\nErrors:\n- {exc}", "", "{}", None


    def refresh_learning_dashboard():
        try:
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

            return (
                json.dumps(lessons, indent=2),
                json.dumps(recurring, indent=2),
                json.dumps(recommended, indent=2),
            )

        except Exception as exc:
            return "[]", "{}", json.dumps({"error": str(exc)}, indent=2)


    def apply_latest_learning_dashboard():
        try:
            data = LearningStore().load()
            proposals = propose_adaptations(data)

            if not proposals:
                return "No recommended fixes are available yet."

            low_risk = [proposal for proposal in proposals if proposal.risk_level == "low"]
            proposal = low_risk[-1] if low_risk else proposals[-1]

            result = implement_adaptation(
                proposal,
                mode="safe_apply" if proposal.risk_level == "low" else "recommend",
            )

            LearningStore().add_implementation(result)

            return json.dumps(result.to_dict(), indent=2)

        except Exception as exc:
            return json.dumps({"error": str(exc)}, indent=2)


    def ignore_latest_learning_dashboard():
        return "Latest recommendation ignored for now. No files were changed."


    def rollback_learning_dashboard(version_id):
        try:
            if not str(version_id).strip():
                return "Enter a learning version id such as v001."

            result = rollback_adaptation(str(version_id).strip())
            LearningStore().add_implementation(result)

            return json.dumps(result.to_dict(), indent=2)

        except Exception as exc:
            return json.dumps({"error": str(exc)}, indent=2)


    with gr.Blocks(title="Signal AI Market Intelligence") as demo:
        gr.Markdown("# Signal")
        gr.Markdown(
            "Behavioral Signals AI for revealed demand intelligence, plus a Signal CGE "
            "Modelling Framework for policy simulation and GAMS-compatible exports."
        )

        with gr.Tab("Behavioral Signals AI"):
            with gr.Row():
                with gr.Column():
                    likes_input = gr.Number(label="Likes", value=120, precision=0)
                    comments_input = gr.Number(label="Comments", value=35, precision=0)
                    shares_input = gr.Number(label="Shares", value=24, precision=0)
                    searches_input = gr.Number(label="Searches", value=160, precision=0)
                    engagement_input = gr.Slider(0, 1, value=0.55, label="Engagement Intensity")
                    intent_input = gr.Slider(0, 1, value=0.7, label="Purchase Intent Score")
                    trend_input = gr.Slider(0, 1, value=0.35, label="Trend Growth")
                    predict_button = gr.Button("Predict Demand")

                with gr.Column():
                    demand_output = gr.Markdown(label="Signal Output")
                    aggregate_output = gr.Number(label="Aggregate Demand Score")
                    opportunity_output = gr.Number(label="Opportunity Score")

            predict_button.click(
                fn=signal_model,
                inputs=[
                    likes_input,
                    comments_input,
                    shares_input,
                    searches_input,
                    engagement_input,
                    intent_input,
                    trend_input,
                ],
                outputs=[demand_output, aggregate_output, opportunity_output],
            )

        with gr.Tab("Signal CGE Framework"):
            scenario_input = gr.Textbox(
                label="CGE Scenario",
                value=DEFAULT_SCENARIO,
                lines=8,
            )

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

            sml_editor = gr.Textbox(
                label="Signal Modelling Language",
                value=DEFAULT_SML_TEXT,
                lines=20,
            )

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

            apply_learning_button.click(
                fn=apply_latest_learning_dashboard,
                inputs=[],
                outputs=[learning_action_output],
            )

            ignore_learning_button.click(
                fn=ignore_latest_learning_dashboard,
                inputs=[],
                outputs=[learning_action_output],
            )

            rollback_learning_button.click(
                fn=rollback_learning_dashboard,
                inputs=[rollback_version_input],
                outputs=[learning_action_output],
            )

try:
    demo
except NameError:
    def _safe_signal_model(likes, comments, shares, searches, engagement, purchase, trend):
        likes = float(likes)
        comments = float(comments)
        shares = float(shares)
        searches = float(searches)
        purchase = float(purchase)
        trend = float(trend)

        aggregate_score = round((likes + comments + shares + searches) / 4, 2)
        opportunity_score = round(((purchase + trend) / 2) * 100, 2)

        if purchase > 0.7 and trend > 0.5:
            demand = "High Demand"
        elif purchase > 0.4:
            demand = "Moderate Demand"
        else:
            demand = "Low Demand"

        return demand, aggregate_score, opportunity_score

    with gr.Blocks(title="Signal AI Market Intelligence") as demo:
        gr.Markdown("# Signal AI Market Intelligence")

        with gr.Tab("Behavioral Signals AI"):
            likes = gr.Number(label="Likes", value=120)
            comments = gr.Number(label="Comments", value=35)
            shares = gr.Number(label="Shares", value=24)
            searches = gr.Number(label="Searches", value=160)
            engagement = gr.Slider(0, 1, value=0.55, label="Engagement Intensity")
            purchase = gr.Slider(0, 1, value=0.7, label="Purchase Intent Score")
            trend = gr.Slider(0, 1, value=0.35, label="Trend Growth")

            btn = gr.Button("Predict Demand")
            demand = gr.Textbox(label="Predicted Demand Class")
            aggregate = gr.Number(label="Aggregate Demand Score")
            opportunity = gr.Number(label="Opportunity Score")

            btn.click(
                fn=_safe_signal_model,
                inputs=[likes, comments, shares, searches, engagement, purchase, trend],
                outputs=[demand, aggregate, opportunity],
            )

        with gr.Tab("Signal CGE Framework"):
            gr.Markdown("CGE framework will load here.")

        with gr.Tab("SML CGE Workbench"):
            gr.Markdown("SML workbench will load here.")

        with gr.Tab("Learning"):
            gr.Markdown("Learning system will load here.")


if __name__ == "__main__":
    demo.launch()
