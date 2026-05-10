# Signal CGE Static Equilibrium Solver

Signal CGE now includes an open-source static equilibrium solver implemented in
Python with NumPy, pandas, and SciPy. The solver calibrates a compact benchmark
equilibrium from a balanced SAM, solves the baseline, applies policy shocks, and
solves a counterfactual equilibrium with simultaneous price, quantity,
institution, trade, fiscal, and macro-closure adjustments.

## What The Solver Does

The solver:

- loads a SAM from CSV, Excel, or an uploaded DataFrame,
- validates row-column balance,
- classifies activities, commodities, factors, households, government, taxes,
  investment, and rest-of-world accounts,
- calibrates benchmark flows, shares, tax rates, elasticities, and normalized
  prices,
- solves the benchmark and counterfactual equilibrium using SciPy,
- reports baseline levels, counterfactual levels, and percentage changes,
- writes diagnostics to `cge_workbench/outputs/latest_diagnostics.json`,
- exports JSON, CSV, and Markdown results.

## Model Blocks

The static equation system includes:

- production output supply,
- production zero-profit condition,
- household income and household demand,
- government revenue and government balance,
- savings-driven investment,
- Armington-style import demand,
- export supply response,
- commodity market demand and supply clearing,
- factor-market clearing,
- fixed commodity-price numeraire.

## Calibration Logic

Calibration starts from a balanced SAM and derives:

- activity output,
- composite commodity demand,
- imports and exports,
- household income and consumption,
- government demand and revenue,
- investment and savings,
- intermediate demand,
- factor payments,
- indirect tax, activity tax, direct tax, and tariff rates,
- benchmark prices normalized to one.

Safe division is used throughout calibration. NaN and infinite values are
rejected.

## Closure Rules

The first supported closure is:

- savings-driven investment,
- fixed government consumption shares,
- fixed foreign savings/external balance handling,
- fixed commodity-price numeraire,
- flexible factor return.

The closure code is modular so additional closures can be added without changing
the app interface.

## Supported Shocks

The shock container supports:

- import tariff changes,
- export price changes,
- productivity changes,
- government demand changes,
- investment demand changes,
- household transfer changes,
- factor supply changes,
- commodity tax changes,
- activity tax changes.

Example:

```json
{
  "shock_type": "import_tariff_change",
  "target_account": "cmach",
  "shock_value": -10,
  "shock_unit": "percent"
}
```

## Results

Signal reports:

- baseline levels,
- counterfactual levels,
- percentage changes from baseline,
- macro indicators,
- household and welfare proxy indicators,
- government balance effects,
- trade effects,
- diagnostics and residuals,
- downloadable JSON, CSV, and Markdown files.

## SAM Multiplier Mode Versus Static CGE Mode

SAM multiplier mode is a fixed-price linear screening tool. It is useful for
quick directional checks and for cases where a full SAM calibration is not
available.

Static CGE mode is a numerical equilibrium solve. Prices, quantities, household
income, fiscal accounts, trade flows, and investment adjust simultaneously under
the selected closure.

## Limitations

This is a static single-period solver. It does not yet include full
recursive-dynamic capital accumulation, detailed nested CES/CET systems by
sector, or a complementarity formulation. These can be added behind the same
solver interface.

## Extension Path

Future extensions can add:

- richer Armington and CET nests,
- sector-specific elasticities,
- explicit factor unemployment closures,
- recursive dynamics,
- a Pyomo backend,
- a Julia/JuMP backend for complementarity-style formulations,
- optional local external solver execution when available.
