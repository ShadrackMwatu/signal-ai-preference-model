# Experiment Workflow

## Scenario Initialization

Each experiment starts from a named baseline, selected model type, selected closure rule, target account, shock type, shock size, and expected outputs.

## Shock Containers

Shock containers store structured changes such as tax-rate changes, government spending increases, productivity changes, trade facilitation shocks, care-economy expansion, and investment shocks.

## Loop Structure

Static experiments run a baseline and one or more policy shocks. Recursive experiments repeat baseline updates and policy simulations by year.

## Baseline and Reference Simulations

The baseline establishes the calibrated benchmark or fallback multiplier reference. Reference results should be retained for comparison.

## Policy Experiments

Policy experiments apply shocks after validation. Unsupported accounts, closures, or shock types should generate warnings before execution.

## Reporting Outputs

Reports should include scenario definition, model setup, closure assumptions, baseline validation, simulation results, distributional effects, gender-care effects, interpretation, risks, limitations, and recommendations.
