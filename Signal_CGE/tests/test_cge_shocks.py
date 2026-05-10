from cge_workbench.equilibrium_solver.shocks import apply_shock, normalize_shock, parse_policy_shock


def test_tariff_prompt_parses_to_import_tariff_shock():
    shock = parse_policy_shock("reduce import tariffs on cmach by 10%")
    assert shock["shock_type"] == "import_tariff_change"
    assert shock["target_account"] == "cmach"
    assert shock["shock_value"] == -10.0


def test_import_tariff_shock_reduces_tariff_rate():
    params = {
        "tariff_rate": 0.10,
        "world_export_price": 1.0,
        "productivity": 1.0,
        "government_demand_multiplier": 1.0,
        "investment_demand_multiplier": 1.0,
        "household_transfer": 0.0,
        "household_income": 100.0,
        "factor_supply": 1.0,
        "commodity_tax_rate": 0.04,
        "activity_tax_rate": 0.03,
    }
    shocked = apply_shock(params, {"shock_type": "import_tariff_change", "shock_value": -10, "shock_unit": "percent"})
    assert shocked["tariff_rate"] < params["tariff_rate"]


def test_normalize_vat_alias():
    shock = normalize_shock({"policy_instrument": "vat", "target_account": "cfood", "shock_value": 5})
    assert shock["shock_type"] == "commodity_tax_change"
