# Signal CGE Validated Static Equilibrium Solver

Signal CGE now includes a validated open-source static equilibrium CGE solver. The solver remains compact, but it must pass explicit validation gates before its outputs receive the `validated_static_equilibrium_cge_solver` label.

## Equations Included

The validated static solver includes:

- production and zero-profit condition,
- intermediate demand,
- factor demand,
- household income,
- household demand,
- government revenue,
- government expenditure,
- investment-savings balance,
- Armington import demand,
- CET/export supply,
- commodity market clearing,
- factor market clearing,
- price system,
- external balance,
- numeraire condition,
- income-expenditure consistency.

## Calibration Requirements

The solver starts from a SAM and requires core account classes:

- activities,
- commodities,
- factors,
- households,
- government,
- investment or savings-investment,
- rest of world.

Signal classifies the accounts, extracts benchmark flows, computes share-style parameters, and generates initial values from the benchmark. If a user uploads a SAM, Signal attempts to calibrate from that file. If no upload is provided, Signal uses a repo-stored default benchmark structure.

## Closure Rules

The static solver activates explicit closure concepts for:

- government balance,
- savings-investment balance,
- external balance,
- factor market clearing,
- numeraire selection.

The current default closure is `base_closure`.

## Validation Tests

Signal only applies the validated label when all checks pass:

- SAM row-column balance,
- no missing core account groups,
- no negative entries,
- no zero columns,
- base-year replication residual below tolerance,
- Walras-style commodity market residual below tolerance,
- homogeneity/numeraire check,
- post-shock solver convergence,
- residual norm below tolerance,
- no NaN or infinite solved values.

## Limitations

The validated static solver is not yet the full recursive-dynamic Signal CGE model. It uses a compact aggregate equation system and prototype elasticities. Full national-scale use still requires richer account coverage, calibrated elasticities, more detailed taxes and margins, stronger base-year replication, and period-by-period dynamics.

## Difference From Recursive Dynamic CGE

The static solver compares one benchmark equilibrium with one shocked equilibrium. A recursive dynamic CGE model will update capital, labor, productivity, and baseline values across multiple periods.
