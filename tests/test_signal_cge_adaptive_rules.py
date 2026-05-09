from __future__ import annotations

from Signal_CGE.signal_cge.learning.adaptive_rules import (
    apply_adaptive_prompt_rules,
    evolve_adaptive_rules_from_memory,
)
from Signal_CGE.signal_cge.learning.recommendation_engine import recommend_adaptive_next_simulations


def test_adaptive_rules_map_tariff_prompt() -> None:
    hints = apply_adaptive_prompt_rules("reduce import tariffs on cmach by 10%")

    assert hints["policy_instrument"] == "import_tariff"
    assert hints["shock_direction"] == "decrease"
    assert hints["target_account"] == "cmach"
    assert hints["target_account_type"] == "commodity"


def test_adaptive_rules_cover_vat_care_and_exports() -> None:
    vat = apply_adaptive_prompt_rules("increase VAT by 5 percent")
    care = apply_adaptive_prompt_rules("double care infrastructure")
    exports = apply_adaptive_prompt_rules("boost exports")

    assert vat["policy_instrument"] == "vat_tax"
    assert care["policy_instrument"] == "care_investment"
    assert exports["policy_instrument"] == "export_demand"


def test_rule_evolution_and_recommendations_return_structured_outputs() -> None:
    evolution = evolve_adaptive_rules_from_memory(limit=5)
    recommendations = recommend_adaptive_next_simulations(
        {"shock_type": "import_tariff", "policy_instrument": "import_tariff", "target_account": "cmach"}
    )

    assert "learned_patterns" in evolution
    assert recommendations
