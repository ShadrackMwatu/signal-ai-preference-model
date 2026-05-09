# Signal CGE Open-Source Prototype Equilibrium Solver

Signal CGE now includes a first open-source prototype equilibrium CGE solver. It is a modest static nonlinear system built with SciPy. It is not yet a complete national CGE model, but it is a real equilibrium solve rather than a generated result table.

## What The Solver Does

The solver uses `scipy.optimize.root` to solve a small calibrated equilibrium system with ten endogenous variables:

- domestic output
- composite commodity demand
- imports
- exports
- commodity price
- activity price
- household income
- government revenue
- investment
- exchange rate

## Equations Included

The prototype system includes:

- zero-profit/activity price condition
- commodity market clearing
- Armington-style import relation
- export transformation relation
- household income-expenditure balance
- government revenue equation
- savings-investment balance
- external balance condition
- numeraire price condition
- activity output supply response

## Tariff Shock Pathway

For a prompt such as `reduce import tariffs on cmach by 10%`, Signal:

1. identifies `cmach` as the target commodity,
2. identifies the policy instrument as an import tariff,
3. reduces the tariff wedge by 10 percent relative to the benchmark tariff rate,
4. solves the post-shock equilibrium,
5. compares the policy equilibrium with the benchmark equilibrium,
6. reports import price, import demand, government tariff revenue, household welfare proxy, output, and trade-balance changes.

## Calibration Requirements

The solver can consume existing Signal SAM calibration outputs. If a complete calibration payload is unavailable, it constructs a small prototype calibrated benchmark from the canonical model profile and labels it accordingly.

## Difference From SAM Multiplier Fallback

The SAM multiplier fallback traces linear accounting effects through the SAM. The prototype equilibrium solver solves nonlinear equations with endogenous prices, trade quantities, government revenue, investment, and external-balance adjustment.

## Difference From Future Full Recursive-Dynamic CGE

The current solver is static and compact. The future full model will add:

- complete sector and commodity sets,
- calibrated elasticities,
- full tax and margin systems,
- base-year replication diagnostics,
- full closure replacement rules,
- recursive dynamic capital, labor, and productivity updates,
- period-by-period scenario loops.

## Remaining Limitations

The results should be labeled `open_source_equilibrium_cge_prototype`. They are simplified equilibrium indicators, not final national CGE results.
