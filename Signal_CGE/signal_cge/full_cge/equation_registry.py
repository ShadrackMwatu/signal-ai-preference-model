"""Equation registry for the future full Signal CGE model."""

from __future__ import annotations

from typing import Any


EQUATION_BLOCKS: dict[str, dict[str, str]] = {
    "production": {
        "role": "Maps activity output to intermediate inputs and value added.",
        "placeholder": "QA[a] = F(IVA[a], INT[a,*], productivity[a])",
    },
    "intermediate_demand": {
        "role": "Determines commodity inputs per unit of activity output.",
        "placeholder": "QINT[c,a] = io_share[c,a] * QA[a]",
    },
    "value_added": {
        "role": "Combines factor demands into activity-level value added.",
        "placeholder": "QVA[a] = VA(FD[f,a], va_share[f,a], elasticity[a])",
    },
    "household_demand": {
        "role": "Allocates disposable household income across commodities.",
        "placeholder": "QH[c,h] = demand_share[c,h] * YD[h] / PC[c]",
    },
    "government_demand": {
        "role": "Tracks government consumption and public service purchases.",
        "placeholder": "QG[c] = gov_share[c] * GOVEXP / PC[c]",
    },
    "investment_demand": {
        "role": "Allocates investment demand across commodities.",
        "placeholder": "QI[c] = inv_share[c] * INVEST / PC[c]",
    },
    "imports": {
        "role": "Links import demand to import prices and composite demand.",
        "placeholder": "QM[c] = ArmingtonImport(QQ[c], PM[c], PD[c], sigma_m[c])",
    },
    "exports": {
        "role": "Links export supply to world prices and domestic output allocation.",
        "placeholder": "QE[c] = ExportSupply(QX[c], PE[c], PD[c], sigma_e[c])",
    },
    "armington_aggregation": {
        "role": "Combines domestic and imported commodities into composite supply.",
        "placeholder": "QQ[c] = Armington(QD[c], QM[c], delta_m[c], rho_m[c])",
    },
    "cet_transformation": {
        "role": "Allocates output between domestic sales and exports.",
        "placeholder": "QX[c] = CET(QD[c], QE[c], delta_e[c], rho_e[c])",
    },
    "factor_markets": {
        "role": "Clears factor demand and factor supply under selected closure.",
        "placeholder": "sum_a FD[f,a] = FS[f] or wage adjusts by closure",
    },
    "commodity_markets": {
        "role": "Clears composite commodity supply and demand.",
        "placeholder": "QQ[c] = sum_h QH[c,h] + QG[c] + QI[c] + sum_a QINT[c,a]",
    },
    "price_equations": {
        "role": "Defines producer, consumer, import, export, and composite prices.",
        "placeholder": "PC[c] = price_index(PD[c], PM[c], taxes[c])",
    },
    "income_expenditure_balance": {
        "role": "Balances institution incomes, transfers, taxes, savings, and spending.",
        "placeholder": "Y[h] = factor_income[h] + transfers[h]",
    },
    "savings_investment_balance": {
        "role": "Balances total savings and investment according to macro closure.",
        "placeholder": "SAV = INVEST",
    },
    "government_balance": {
        "role": "Balances public revenue, spending, transfers, and savings or taxes.",
        "placeholder": "GOVREV = GOVEXP + GTRANS + GSAV",
    },
    "external_balance": {
        "role": "Balances foreign savings, exports, imports, and exchange rate closure.",
        "placeholder": "FSAV = EXR * (sum_c PWM[c]*QM[c] - sum_c PWE[c]*QE[c])",
    },
    "numeraire_condition": {
        "role": "Fixes one price index to anchor the model price level.",
        "placeholder": "CPI = 1",
    },
}


def get_equation_registry() -> dict[str, Any]:
    """Return the full-equilibrium equation registry."""

    return {
        "model": "Signal CGE",
        "status": "blueprint",
        "blocks": EQUATION_BLOCKS,
        "block_count": len(EQUATION_BLOCKS),
    }


def validate_equation_registry(registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate that all planned full-CGE equation blocks are present."""

    payload = registry or get_equation_registry()
    blocks = payload.get("blocks", {})
    missing = [name for name in EQUATION_BLOCKS if name not in blocks]
    incomplete = [name for name, block in blocks.items() if not block.get("role") or not block.get("placeholder")]
    return {"valid": not missing and not incomplete, "missing": missing, "incomplete": incomplete}
