from __future__ import annotations

import unittest

import app


class VisualIntelligenceTests(unittest.TestCase):
    def test_display_label_mapping_uses_professional_language(self) -> None:
        self.assertEqual(app._display_label("High Demand"), "Strong Demand Momentum")  # noqa: SLF001
        self.assertEqual(app._display_label("Low Demand"), "Limited Demand Signal")  # noqa: SLF001
        self.assertEqual(  # noqa: SLF001
            app._display_label("Investigate Anomaly / Possible Unmet Demand"),
            "Potential Unmet Demand Opportunity",
        )

    def test_structured_explanation_contains_expected_sections(self) -> None:
        details = app.predict_demand_details(180, 50, 35, 220, 0.68, 0.82, 0.6)
        brief = app._format_panel_explanation(details)  # noqa: SLF001

        self.assertIn("AI Intelligence Brief", brief)
        self.assertIn("1. Classification", brief)
        self.assertIn("2. Key Drivers", brief)
        self.assertIn("3. Risk / Validation Signals", brief)
        self.assertIn("4. Strategic Interpretation", brief)
        self.assertIn("5. Model Source", brief)

    def test_intelligence_scores_are_generated(self) -> None:
        details = app.predict_demand_details(180, 50, 35, 220, 0.68, 0.82, 0.6)

        for key in (
            "signal_strength_score",
            "momentum_score",
            "volatility_noise_score",
            "persistence_score",
            "adoption_probability",
            "viral_probability",
        ):
            self.assertIn(key, details)
            self.assertGreaterEqual(float(details[key]), 0.0)
            self.assertLessEqual(float(details[key]), 100.0)

    def test_visual_component_payload_contains_html(self) -> None:
        details = app.predict_demand_details(180, 50, 35, 220, 0.68, 0.82, 0.6)
        visuals = app._build_visual_components(details)  # noqa: SLF001

        self.assertIn("<div", visuals["confidence_gauge_html"])
        self.assertIn("<div", visuals["signal_strength_gauge_html"])
        self.assertIn("<div", visuals["momentum_indicator_html"])
        self.assertIn("<svg", visuals["opportunity_radar_html"])
        self.assertIn("Key Driver Summary Cards", visuals["key_driver_cards_html"])


if __name__ == "__main__":
    unittest.main()
