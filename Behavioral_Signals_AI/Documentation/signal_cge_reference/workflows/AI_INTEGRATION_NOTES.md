# AI Integration Notes

## AI CGE Chat Studio

The Chat Studio accepts natural-language policy questions, classifies intent, compiles a structured scenario, validates the scenario, calls the Signal CGE workbench or Python fallback, and formats diagnostics and explanations.

## Policy AI

`policy_ai/` generates policy summaries and next-scenario recommendations. It should reference the scenario object, result summaries, diagnostics, and caveats rather than inventing results.

## Signal Reasoning

`signal_ai/reasoning/` checks unsupported shocks, missing accounts, negative shock sizes, unsupported closures, care-economy suffixes, and the distinction between SAM multiplier analysis and full CGE solving.

## Learning Modules

The learning modules explain model concepts and workflows. They should point users toward canonical references under `Documentation/signal_cge_reference/`.

## Scenario Recommendation Engine

The scenario recommender proposes follow-up simulations such as alternate closure rules, sensitivity tests, distributional analysis, and sector-specific shocks.
