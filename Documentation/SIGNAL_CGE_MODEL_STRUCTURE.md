# Signal CGE Model Structure

This document defines the formal architecture for the Signal CGE Model. The current repository already includes a Python SAM multiplier fallback and an optional GAMS runner. The new `cge_workbench/model_core/` package formalizes the full CGE design in transparent Python modules so future solver work can be implemented without hiding equations or assumptions.

## 1. Data Layer

The data layer prepares the model benchmark:

- SAM loader: reads square SAM data from CSV or Excel.
- Account mapper: classifies activities, commodities, factors, households, government, investment, trade, and tax accounts.
- Balance checker: verifies row-column balance and reports suspicious accounts.
- Calibration dataset builder: converts SAM flows into benchmark totals and share parameters.
- Kenya gender-care SAM support: preserves factor suffixes `fcp`, `fcu`, `fnp`, `fnu`, `mcp`, `mcu`, `mnp`, and `mnu` where available.

## 2. Model Core

The model core is organized into explicit blocks:

- Production block: activity output, intermediate demand, and factor demand.
- Household block: household income, consumption, savings, and transfers.
- Government block: tax revenue, expenditure, transfers, and government savings.
- Investment-savings block: savings pool and investment demand.
- Trade block: import prices, export supply, and external balance channels.
- Factor market block: factor income, factor demand, and factor supply closure.
- Price block: price linkages and numeraire choice.
- Market-clearing block: commodity, factor, and macro balance conditions.

Each block currently contains placeholder equations and deterministic validation logic. These placeholders are not hard-coded results. They are a transparent contract for future full-equilibrium implementation.

## 3. Closure Rules

The closure registry supports the following formal choices:

- Savings-driven investment.
- Government deficit closure.
- Foreign savings / exchange-rate closure.
- Consumer price numeraire.
- Fixed factor supply with factor prices clearing markets.

Closure validation is handled in `cge_workbench/model_core/closure_system.py`.

## 4. Calibration Flow

`calibrate_from_sam()` accepts a SAM-like pandas DataFrame and returns:

- accounts
- activities
- commodities
- factors
- households
- government accounts
- row totals
- column totals
- total flows
- column share parameters
- balance diagnostics
- Kenya gender-care support flag

This calibration layer is the bridge between SAM data and future equation parameters.

## 5. Solver Strategy

Signal uses a layered solver strategy:

1. Current Python SAM multiplier fallback for transparent screening simulations.
2. Optional GAMS runner when a configured GAMS model and runtime are available.
3. Future open-source equilibrium prototype using optional Pyomo, SciPy, or another solver pathway.
4. Diagnostics when full CGE execution is unavailable.

The formal model core does not require GAMS, Pyomo, or external APIs.

## 6. Recursive Dynamics Plan

The recursive dynamic module should be added after the static equilibrium prototype. It will update:

- capital accumulation
- labour growth
- productivity growth
- baseline projection
- annual scenario shocks
- annual SAM/account updates where appropriate

The first implementation should keep annual updating deterministic and auditable before adding advanced calibration features.

## 7. AI Interface

The AI interface assists with:

- natural-language scenario compilation
- economic reasoning checks
- closure explanation
- diagnostics interpretation
- results interpretation
- policy brief generation
- learning assistant guidance

AI does not replace the economic model. It helps users configure, run, explain, and document model workflows.

## 8. SAM Multiplier Fallback vs Full CGE

The current Python SAM multiplier fallback computes fixed-price linear multiplier effects. It is useful for screening and transparent sensitivity analysis, but it is not a full CGE equilibrium solution.

A full CGE model adds:

- endogenous prices
- substitution behavior
- market-clearing equations
- closure-dependent macro balances
- calibrated production, consumption, trade, and factor-market equations
- solver diagnostics for equilibrium residuals

The new model-core package defines the structure required to move from the current fallback toward a full open-source equilibrium implementation.
