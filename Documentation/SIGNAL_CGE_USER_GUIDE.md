# Signal CGE User Guide

## Introduction To Signal CGE

Signal CGE is a prompt-driven CGE/SAM simulation platform for policy analysis. It starts from a social accounting matrix, validates inputs, calibrates benchmark values, applies policy shocks, runs the available solver backend, and reports results in policy language.

## Signal CGE Folder Structure

- `Signal_CGE/signal_cge/data/`: SAM loading, account mapping, and validation.
- `Signal_CGE/signal_cge/calibration/`: benchmark extraction and share-parameter calibration.
- `Signal_CGE/signal_cge/full_cge/`: equation, variable, parameter, closure, and solver blueprints.
- `Signal_CGE/signal_cge/solvers/`: solver backends and fallback runners.
- `Signal_CGE/signal_cge/experiments/`: experiment registries, shock containers, and simulation loops.
- `Signal_CGE/signal_cge/results/`: result tables, macro results, welfare results, structural results, and reports.
- `Documentation/`: user guides, validation notes, model structure, and workflow references.

## How To Prepare A SAM

Prepare a square matrix with matching row and column accounts. Use consistent account labels for activities, commodities, factors, households, government, taxes, savings-investment, and rest of world. Values should be numeric and measured in a consistent unit.

## Required Model Data

Signal CGE can run from repo-stored canonical model files by default. Stronger simulations require a balanced SAM, account mappings, tax and tariff rates, factor payments, household accounts, government accounts, trade accounts, elasticity assumptions, and closure settings.

## Account Sets And Mappings

Account mappings connect SAM labels to model sets. Clear mappings let Signal identify policy targets, apply shocks correctly, and report household, factor, government, trade, and welfare effects.

## Calibration Workflow

Calibration validates the SAM, classifies accounts, extracts benchmark flows, computes share parameters, prepares initial values, and builds solver payloads.

## Validation Checks Before Simulation

Signal checks SAM balance, zero rows and columns, negative values, missing mappings, calibration sufficiency, closure settings, base-year replication status, and solver readiness.

## Closure Rules

Closure rules define which variables adjust to restore macro balance. Signal CGE supports savings-driven investment, investment-driven savings, fixed government savings, flexible direct tax replacement, fixed foreign savings, flexible exchange rate, factor full employment, and unemployment or fixed wage options.

## How To Enter Simulation Prompts

Use clear policy language, such as:

- `reduce import tariffs on cmach by 10%`
- `increase VAT by 5%`
- `increase government spending on health by 10%`
- `double investment in care infrastructure`
- `increase productivity in agriculture by 8%`

## How Signal Converts Prompts Into Shocks

Signal identifies the policy instrument, target account, shock direction, magnitude, scenario type, expected outputs, and closure assumptions. The result is stored as a structured scenario and shock container.

## How Simulations Are Executed

Signal runs the open-source prototype equilibrium CGE solver when the payload is sufficient. If the solver fails, Signal falls back to the SAM multiplier/prototype pathway and reports the reason.

## How Results Are Reported

Results include levels, differences from baseline where available, percentage changes, macro indicators, welfare or proxy welfare, trade effects, household effects, factor income effects, government balance effects, tables, charts, and downloadable files.

## How To Interpret Results

Review the interpreted scenario, solver used, validation status, diagnostics, caveats, model references, and recommended next simulations. Prototype outputs should be treated as model-based indicators, not final national policy estimates.

## Current Solver Limitations

The current open-source equilibrium solver is a compact static prototype. It does not yet include full sector coverage, complete elasticity datasets, complete closure replacement rules, full base-year replication checks, or recursive dynamics.

## Future Full-Equilibrium Solver Pathway

Future work will expand equations, sector coverage, elasticities, base-year replication, recursive dynamics, and reporting across macro, sectoral, household, factor, fiscal, trade, and welfare outcomes.
