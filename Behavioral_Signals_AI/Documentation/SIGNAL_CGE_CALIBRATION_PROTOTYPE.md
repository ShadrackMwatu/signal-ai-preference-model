# Signal CGE Calibration Prototype

This document describes the first lightweight open-source calibration layer for the Signal CGE Model. The calibration layer prepares a Social Accounting Matrix (SAM) for future full CGE equilibrium solving. It does not require GAMS, Pyomo, SciPy, or any new heavy dependency, and it does not change Hugging Face/Gradio app startup behavior.

## Purpose

The prototype turns a SAM-like pandas DataFrame into a structured calibration package:

- account classification
- benchmark flows
- simple share parameters
- diagnostics and warnings
- readiness status for different modelling pathways

This is not yet a full CGE solver. It prepares transparent benchmark data for future solver work.

## SAM Requirements

The input SAM must be:

- a pandas DataFrame
- non-empty
- square
- numeric or convertible to numeric
- labelled with matching row and column accounts

If these conditions fail, calibration raises a clear validation error.

## Account Classification Logic

`cge_workbench/calibration/account_classifier.py` classifies accounts into:

- `activities`
- `commodities`
- `factors`
- `households`
- `government`
- `taxes`
- `savings_investment`
- `rest_of_world`
- `unknown`

It also identifies care-factor suffixes:

`fcp`, `fcu`, `fnp`, `fnu`, `mcp`, `mcu`, `mnp`, `mnu`

Classification is rule-based and can be overridden with an optional `account_map`, for example:

```python
calibrate_signal_cge(sam_df, account_map={"hh_rural": "households"})
```

## Benchmark Extraction

`benchmark_extractor.py` validates the SAM and extracts:

- row totals
- column totals
- account imbalance
- activity output
- commodity demand
- factor payments
- household income
- government demand
- investment demand
- imports and exports where rest-of-world accounts are available

The extraction avoids hardcoded country assumptions. Kenya gender-care support is limited to recognizing the known factor suffixes when they appear.

## Share Parameters

`share_parameters.py` computes benchmark shares for:

- production input shares
- household expenditure shares
- government demand shares
- investment demand shares
- export shares
- import shares
- factor income shares

Zero denominators are handled safely. The calibration layer returns `0.0` instead of `NaN` or infinite values.

## Diagnostics

`calibration_diagnostics.py` reports:

- SAM balance tolerance checks
- zero-row accounts
- zero-column accounts
- negative values
- missing account categories
- readiness for SAM multiplier analysis
- readiness for prototype CGE calibration
- readiness for full equilibrium CGE solving

Diagnostics also warn that full CGE equations remain placeholders.

## Pipeline

Use:

```python
from cge_workbench.calibration import calibrate_signal_cge

result = calibrate_signal_cge(sam_df, account_map=None, tolerance=1e-6)
```

The result contains:

- `account_classification`
- `benchmark_flows`
- `share_parameters`
- `diagnostics`
- `warnings`
- `cge_readiness_status`

The existing model-core calibration entry point now delegates to this pipeline to avoid duplicated calibration logic.

## What Is Ready Now

The current prototype is ready for:

- SAM screening
- account classification review
- benchmark-flow extraction
- simple share-parameter calibration
- diagnostics before future solver development

## What Remains Before Full CGE Solving

The following are still future work:

- calibrated behavioural equations
- endogenous prices
- market-clearing residual functions
- closure-specific variable selection
- open-source equilibrium solver prototype
- recursive dynamics
- solver diagnostics and convergence reporting

## SAM Multiplier vs Calibrated Benchmark vs Full CGE Solver

The SAM multiplier fallback is a fixed-price linear screening tool.

The calibrated CGE benchmark is a structured dataset of base-year flows and shares prepared from the SAM.

A full equilibrium CGE solver will use the calibrated benchmark, formal model blocks, closure rules, and numerical solving to find endogenous prices, quantities, and macro balances.
