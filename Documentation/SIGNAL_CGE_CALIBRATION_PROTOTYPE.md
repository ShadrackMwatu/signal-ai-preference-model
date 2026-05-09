# Signal CGE Calibration Prototype

This prototype builds the first open-source calibration layer for the Signal CGE Model. It does not require GAMS, Pyomo, SciPy, or any heavy solver dependency. It converts a SAM-like pandas DataFrame into account classifications, benchmark flows, share parameters, and calibration diagnostics.

## What It Implements

The package `cge_workbench/calibration/` provides:

- SAM account classification.
- Benchmark flow extraction.
- Production share calibration.
- Household demand share calibration.
- Government demand share calibration.
- Investment demand share calibration.
- Trade import/export share calibration.
- Factor payment share calibration.
- Calibration diagnostics and placeholder-equation warnings.

## Account Classification

Accounts are classified into:

- activities
- commodities
- factors
- households
- government
- investment
- taxes
- imports
- exports
- rest of world
- Kenya gender-care factor suffixes

The Kenya gender-care suffixes are:

`fcp`, `fcu`, `fnp`, `fnu`, `mcp`, `mcu`, `mnp`, `mnu`

## Benchmark Flow Extraction

The calibration layer extracts:

- row totals
- column totals
- intermediate flows
- factor payments
- household consumption
- government demand
- investment demand
- imports
- exports
- tax payments
- total absorption
- total activity cost

These flows are transparent SAM slices, not solved model results.

## Share Parameters

The prototype computes fixed benchmark shares for:

- production: factor and commodity input shares by activity
- household demand: commodity budget shares by household account
- government demand: commodity shares in government demand
- investment demand: commodity shares in investment demand
- trade imports: import/rest-of-world row shares across commodities
- trade exports: commodity export shares
- factor payments: factor payment shares by activity

## Diagnostics

Diagnostics include:

- square SAM validation
- row-column account matching
- row-column balance
- zero-column accounts
- negative value warnings
- missing activity/factor warnings
- Kenya gender-care factor coverage warnings
- clear notice that full CGE behavioural equations remain placeholders

## Relationship To The Current SAM Multiplier

The current Python SAM multiplier remains the operational fallback for screening simulations. This calibration prototype prepares the data structures needed for a future full open-source equilibrium solver, but it does not yet solve endogenous prices, substitution, closure-dependent macro balances, or market-clearing residuals.

## Relationship To Full CGE

A full Signal CGE implementation will use this calibration dataset to parameterize formal model blocks in `cge_workbench/model_core/`, then pass variables, equations, closures, and residuals into an optional open-source solver pathway.
