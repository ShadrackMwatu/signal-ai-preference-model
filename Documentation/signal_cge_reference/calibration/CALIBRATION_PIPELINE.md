# Calibration Pipeline

## 1. SAM Loading

Signal loads a SAM from CSV, Excel, or an already prepared pandas DataFrame. The SAM must be square and use matching row and column account labels.

## 2. Validation

Validation checks dimensions, labels, missing values, numeric values, zero rows, zero columns, negative entries, and row-column balance.

## 3. Balancing

The current prototype reports imbalance rather than automatically balancing the SAM. Future balancing should be explicit, reproducible, and documented.

## 4. Scaling

Scaling can normalize the SAM into model units while preserving account identities and row-column relationships. Scaling assumptions should be recorded in the calibration profile.

## 5. Parameter Calibration

The prototype calibrates benchmark shares for production inputs, household demand, government demand, investment demand, trade flows, and factor income. Future equilibrium solving will add equation-specific parameters.

## 6. Initialization

Initialization prepares benchmark activity output, commodity demand, factor payments, household income, government demand, investment demand, imports, exports, and account totals.

## 7. Walras Checks

Future full CGE solving should check market-clearing residuals and macro identities so that one redundant market condition is handled consistently.

## 8. Replication Checks

The calibrated benchmark should reproduce the SAM baseline before policy shocks are applied. Any residuals must be reported.

## 9. Diagnostics

Diagnostics classify readiness for SAM multiplier analysis, prototype CGE calibration, full equilibrium CGE solving, and recursive dynamic extensions.
