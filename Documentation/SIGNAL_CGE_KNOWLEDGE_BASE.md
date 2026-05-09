# Signal CGE Knowledge Base

This file is the permanent high-level knowledge base for the Signal CGE system. The adapted Signal CGE user guide stored under `Documentation/signal_cge_reference/user_guides/` is treated as the authoritative reference framework for future model, documentation, and AI workflow development.

## Signal CGE Philosophy

Signal CGE is designed as a transparent, SAM-driven economic simulation framework. AI assists with setup, validation, scenario design, interpretation, and documentation, but does not replace the economic model. Equations, assumptions, closures, data requirements, and diagnostics remain visible to users.

## SAM-Driven Architecture

The Social Accounting Matrix is the organizing dataset for calibration and fallback simulations. Signal uses the SAM to classify accounts, validate row-column balance, extract benchmark flows, calibrate shares, and prepare the benchmark state for future equilibrium solving.

## Calibration Workflow

The calibration workflow loads a SAM, validates dimensions and labels, checks balance, classifies accounts, extracts benchmark transactions, calculates share parameters, initializes model quantities, and reports readiness. The current implementation supports a calibration prototype and SAM multiplier fallback. A full equilibrium calibration will require equation-specific parameterization and replication checks.

## Closure System

Signal closure rules define which macroeconomic variables adjust after a shock. The canonical closure families are savings-investment closure, government deficit or tax closure, foreign savings or exchange-rate closure, numeraire choice, and factor-market closure. Closure assumptions must be shown in reports and validated before simulation.

## Recursive Dynamics

Recursive dynamics are planned as annual updates to capital stocks, labor supply, productivity, and baseline projections. Each model year should solve or simulate from the prior year state, then update stocks and exogenous trends before the next year.

## Experiment Workflow

Experiments start with a validated baseline, then define a scenario shock container, apply closure assumptions, run the baseline or fallback simulation, run the policy scenario, compare results, validate plausibility, and generate a policy report.

## Reporting Pipeline

Signal reporting includes diagnostics, macro effects, sectoral output, factor income, household income, gender-care effects, fiscal implications, risks, caveats, recommendations, and downloadable policy briefs.

## MCP vs NLP Structure

Signal distinguishes mathematical complementarity problem structure from natural language processing. The model core and solver layer are responsible for equation systems, closures, and numerical execution. Natural-language processing compiles user prompts into structured scenarios and explanations, but the scenario must pass model diagnostics before execution.

## Solver Architecture

The current operational pathway is the Python SAM multiplier fallback. Optional GAMS execution is guarded by availability checks. Future open-source equilibrium solving can be added through a modular solver interface without making deployment depend on heavy optimization packages.

## Scenario Framework

Supported scenario families include fiscal policy, care economy, infrastructure, trade policy, productivity, and custom natural-language prompts. Each scenario should identify the shock account, shock type, shock size, target outputs, closure rule, diagnostics, and reporting expectations.

## AI-Assisted Policy Workflow

The AI CGE Chat Studio routes user prompts through intent classification, deterministic scenario compilation, economic reasoning checks, model or fallback execution, explanation, policy summary, and recommended next simulations. No external API key is required for the current deterministic implementation.

## SML Relationship

Signal CGE is the economic model engine. SML is the readable model specification and export layer. SML should help define model blocks, closures, scenarios, and solver exports while relying on Signal CGE for canonical economic architecture.

## Learning Integration

The learning modules explain SAMs, CGE concepts, calibration, closures, diagnostics, SML, and scenario interpretation. Learning content should reference the canonical Signal CGE documentation and avoid conflicting terminology.

## Diagnostics and Validation System

Diagnostics run before and after simulations. Pre-run diagnostics include SAM balance, account classification, closure checks, baseline consistency, and shock validity. Post-run diagnostics include plausibility, multiplier size, sector ranking, household and factor consistency, and warnings for suspicious results.
