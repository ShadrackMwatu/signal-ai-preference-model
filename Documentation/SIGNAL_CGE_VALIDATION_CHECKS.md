# Signal CGE Validation Checks

## SAM Row-Column Balance Check

Signal checks whether each SAM account row total matches its column total within tolerance.

## Zero Row/Column Check

Zero rows or columns are flagged because they may indicate inactive accounts, missing data, or mapping problems.

## Negative Entry Check

Negative values are reported for review because they may represent adjustments, taxes, subsidies, or data errors.

## Account Mapping Check

Signal verifies that activities, commodities, factors, households, government, taxes, savings-investment, and rest-of-world accounts are identified where possible.

## Macro Consistency Check

Signal checks whether available macro totals are consistent with SAM totals and benchmark flows.

## Calibration Replication Check

Signal reports whether the calibrated benchmark can reproduce base-year values before policy shocks.

## Walras-Style Balance Check Placeholder

Signal reserves this check for economy-wide market balance as the full equation system expands.

## Homogeneity/Numeraire Check Placeholder

Signal fixes a numeraire and reserves homogeneity checks for the full price system.

## Solver Convergence Diagnostics

Signal reports convergence status, residual norm, function evaluations, variables solved, equations solved, closure used, and failed equations where applicable.
