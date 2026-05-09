# Signal CGE Development History

This document consolidates the Signal CGE work completed during the current development cycle. It records what was built, why it was added, how it fits into the Signal architecture, how it has been tested, and what remains before Signal becomes a full open-source CGE equilibrium solver.

## 1. Development Goal

The goal was to upgrade Signal from a dashboard with CGE-adjacent functionality into an AI-assisted, chat-driven CGE/SAM workbench that can:

- translate natural-language policy questions into structured simulation scenarios
- run diagnostics before and after simulations
- execute Python SAM multiplier simulations without GAMS
- optionally support GAMS-backed workflows when available
- prepare a formal CGE model-core structure
- calibrate benchmark parameters from a SAM
- generate policy explanations and policy briefs
- remain deployable on Hugging Face Spaces through the root `app.py`

The guiding principle throughout has been:

> AI assists the economist and model user; it does not replace the economic model.

## 2. Major Commits

The main Signal CGE commits in this development sequence are:

| Commit | Message | Purpose |
|---|---|---|
| `a045642` | `Upgrade Signal with AI-assisted CGE workbench` | Created the initial AI-assisted CGE/SAM workbench, Python fallback runner, diagnostics, scenario templates, result explanation, policy brief generator, documentation, and tests. |
| `8b5c356` | `Add AI-native CGE chat studio foundation` | Added deterministic AI-native chat orchestration, intent classification, economic reasoning checks, local simulation memory, mechanism explanations, policy summaries, scenario recommendations, and the first AI CGE Chat Studio tab. |
| `f9f9e8e` | `Stabilize Hugging Face AI CGE Chat Studio deployment` | Verified deployed Hugging Face startup and Chat Studio API paths, improved Markdown UI formatting, added invalid-SAM fallback handling, and kept dependencies unchanged. |
| `1e17130` | `Review and classify untracked Signal assets` | Audited untracked generated model versions and a Docker installer, documented classifications, and added safe `.gitignore` rules. |
| `082c2f4` | `Add formal Signal CGE model structure` | Added formal model-core modules for production, households, government, investment-savings, trade, factors, prices, market clearing, closures, calibration entry point, and equation registry. |
| `f83f851` | `Add Signal CGE calibration prototype` | Added the first calibration prototype for account classification, benchmark flows, share parameters, diagnostics, documentation, and tests. |
| `7bc1513` | `Add Signal CGE calibration prototype` | Aligned the calibration prototype to the requested final module names and API: `benchmark_extractor.py`, `calibration_pipeline.py`, and `calibrate_signal_cge()`. |

## 3. Current Signal CGE Architecture

Signal now has a layered CGE/SAM architecture:

```text
Signal CGE
├── Data and calibration layer
├── Formal model core
├── Closure system
├── Solver layer
├── Scenario engine
├── AI interface
└── Outputs and policy reporting
```

The implementation is intentionally modular so that the current SAM multiplier fallback can operate immediately while the full CGE solver is developed in later phases.

## 4. AI-Assisted CGE Workbench

The first workbench upgrade created:

```text
cge_workbench/
├── prompts/
├── model_registry/
├── runners/
├── diagnostics/
├── scenarios/
├── interpreters/
├── outputs/
└── tests/
```

### Key Capabilities

- Natural-language scenario parsing.
- Scenario templates for care economy, tax policy, infrastructure, trade policy, and baseline runs.
- Optional GAMS runner.
- Python SAM multiplier fallback.
- Diagnostics-first workflow.
- Plain-language result explanation.
- Markdown policy brief generation.
- Timestamped logs and output artifacts.

### Important Design Decision

The system does not require GAMS. If GAMS is unavailable, the GAMS runner returns a clear message and the Python SAM multiplier fallback remains available.

## 5. Python SAM Multiplier Fallback

The Python fallback currently:

- loads SAM data from CSV or Excel
- validates square matrix structure
- computes column coefficients
- computes `I - A`
- computes the Leontief inverse using a pseudo-inverse
- applies policy shocks
- reports account-level effects
- summarizes activities, commodities, factors, and households where account names allow
- stores logs under `cge_workbench/outputs/`

This is useful for fixed-price multiplier screening. It is not a full CGE equilibrium model.

## 6. AI CGE Chat Studio

The AI CGE Chat Studio added a deterministic local AI layer:

```text
signal_ai/
├── conversation_engine/
├── prompt_router/
├── reasoning/
├── memory/
└── explainability/

policy_ai/
├── policy_brief_service.py
└── scenario_recommender.py
```

### Chat Studio Workflow

`run_chat_simulation(user_prompt, sam_file=None, previous_context=None)`:

1. Classifies user intent.
2. Compiles a natural-language prompt into a structured scenario.
3. Runs economic reasoning checks.
4. Executes the existing workbench/Python fallback.
5. Explains mechanisms and warnings.
6. Generates a policy summary.
7. Stores a local simulation memory record.

### Supported Prompt Examples

- `double care infrastructure`
- `increase government spending on care services by 10 percent`
- `simulate VAT increase`
- `run infrastructure investment shock`
- `compare unpaid care and paid care scenarios`

### No External API Requirement

The Chat Studio uses deterministic Python logic only. It does not require API keys or paid LLM services.

## 7. Hugging Face Deployment Stabilization

The app remains deployed through root-level:

- `app.py`
- `requirements.txt`
- README Space metadata

Deployment stabilization included:

- confirming the deployed Space returns HTTP `200`
- confirming the Gradio config contains the AI CGE Chat Studio tab
- testing the deployed no-SAM simulation path
- testing the deployed SAM-upload simulation path
- rendering scenario JSON, diagnostics, policy summaries, and recommendations
- adding graceful fallback if an uploaded SAM is invalid
- improving UI formatting with Markdown diagnostics and summary blocks
- keeping `requirements.txt` unchanged because no new dependencies were needed

## 8. Formal Model Core

The formal model-core package was added under:

```text
cge_workbench/model_core/
├── production_block.py
├── household_block.py
├── government_block.py
├── investment_savings_block.py
├── trade_block.py
├── factor_market_block.py
├── price_block.py
├── market_clearing_block.py
├── closure_system.py
├── calibration.py
└── model_equations.py
```

Each block contains:

- placeholder equations
- function stubs
- docstrings explaining the economic role
- deterministic validation logic where possible

### Model-Core Blocks

| Block | Economic Role |
|---|---|
| Production | Activity output, intermediate inputs, and factor demand. |
| Household | Household income, consumption, savings, and transfers. |
| Government | Tax revenue, expenditure, transfers, and government savings. |
| Investment-savings | Savings pool and investment demand allocation. |
| Trade | Imports, exports, external balance, and exchange-rate channels. |
| Factor market | Factor income, factor supply, factor demand, and factor-market closure. |
| Price | Price indices, numeraire, and price-link equations. |
| Market clearing | Commodity, factor, and macro balance conditions. |

### Closure System

The initial closure registry supports:

- savings-driven investment
- government deficit closure
- foreign savings / exchange-rate closure
- consumer price numeraire
- fixed factor supply

The closure system validates selected rules before future solver execution.

## 9. Calibration Prototype

The first open-source calibration prototype now lives under:

```text
cge_workbench/calibration/
├── __init__.py
├── account_classifier.py
├── benchmark_extractor.py
├── share_parameters.py
├── calibration_diagnostics.py
└── calibration_pipeline.py
```

### Main API

```python
from cge_workbench.calibration import calibrate_signal_cge

result = calibrate_signal_cge(sam_df, account_map=None, tolerance=1e-6)
```

### Returned Object

The calibration pipeline returns:

- `account_classification`
- `benchmark_flows`
- `share_parameters`
- `diagnostics`
- `warnings`
- `cge_readiness_status`

### Account Classification

The classifier groups SAM accounts into:

- activities
- commodities
- factors
- households
- government
- taxes
- savings_investment
- rest_of_world
- unknown

It also recognizes care-factor suffixes:

`fcp`, `fcu`, `fnp`, `fnu`, `mcp`, `mcu`, `mnp`, `mnu`

### Benchmark Extraction

The benchmark extractor validates the SAM and computes:

- row totals
- column totals
- imbalance
- activity output
- commodity demand
- factor payments
- household income
- government demand
- investment demand
- imports and exports where rest-of-world accounts exist

### Share Parameters

The prototype computes:

- production input shares
- household expenditure shares
- government demand shares
- investment demand shares
- export shares
- import shares
- factor income shares

Zero denominators are handled gracefully. The calibration layer returns finite `0.0` values instead of `NaN` or infinite values.

### Calibration Diagnostics

Diagnostics report:

- SAM balance tolerance
- zero-row accounts
- zero-column accounts
- negative values
- missing account categories
- readiness for SAM multiplier analysis
- readiness for prototype CGE calibration
- readiness for full equilibrium CGE solving

Diagnostics also warn clearly that full CGE behavioural equations remain placeholders.

## 10. Model-Core Calibration Integration

`cge_workbench/model_core/calibration.py` now delegates to the new calibration pipeline. This avoids duplicated calibration logic and keeps the formal model core connected to the open-source calibration prototype.

## 11. Documentation Added

Key Signal CGE documents now include:

- `Documentation/AI_CGE_WORKFLOW.md`
- `Documentation/SIGNAL_CGE_ARCHITECTURE.md`
- `Documentation/CODEX_MODELING_GUIDE.md`
- `Documentation/OPEN_SOURCE_REPLICATION_PLAN.md`
- `Documentation/SCENARIO_LIBRARY.md`
- `Documentation/SIGNAL_AI_CGE_CHAT_STUDIO.md`
- `Documentation/AI_NATIVE_CGE_ROADMAP.md`
- `Documentation/IMPLEMENTATION_LOG.md`
- `Documentation/UNTRACKED_FILES_REVIEW.md`
- `Documentation/SIGNAL_CGE_MODEL_STRUCTURE.md`
- `Documentation/SIGNAL_CGE_CALIBRATION_PROTOTYPE.md`
- `Documentation/SIGNAL_CGE_DEVELOPMENT_HISTORY.md`

## 12. Tests Added

The Signal CGE work added or expanded tests for:

- scenario parsing
- SAM validation
- multiplier computation
- zero-column handling
- GAMS availability handling
- result explanation generation
- policy brief generation
- AI chat intent classification
- chat orchestration
- invalid SAM fallback
- app import stability
- model-core module imports
- closure validation
- equation registry coverage
- calibration account classification
- care suffix classification
- square SAM validation
- share-parameter sums
- zero-denominator handling
- calibration diagnostics
- calibration pipeline output schema

## 13. Current Test Status

The latest full test run passed:

```text
130 passed, 1 warning
```

The warning is from a dependency deprecation notice in `websockets.legacy` and is not specific to the Signal CGE implementation.

## 14. Asset Hygiene

Untracked generated assets were reviewed and classified.

Ignored:

- `docker/*.exe`
- `models/versions/v*/`

Reason:

- local installer binaries should not be committed
- generated model-version artifacts include binary `.pkl` files
- model metadata contained local private filesystem paths
- `.pkl` artifacts should use Git LFS only if a model-version retention policy is adopted

No generated model artifacts or private-path metadata were committed during the CGE work.

## 15. Current Functional State

Signal currently supports:

- Gradio dashboard startup on Hugging Face
- AI CGE Chat Studio tab
- natural-language scenario compilation
- deterministic economic reasoning checks
- Python SAM multiplier fallback
- optional GAMS availability detection
- invalid uploaded SAM fallback
- structured scenario JSON
- diagnostics rendering
- policy explanation rendering
- recommended next simulations
- formal model-core placeholder equation registry
- open-source calibration prototype

## 16. Current Limitations

Signal does not yet have:

- a full nonlinear equilibrium solver
- calibrated behavioural equations
- endogenous price solving
- market-clearing residual functions
- closure-dependent variable selection
- recursive dynamic updating
- full scenario comparison tables
- charts for CGE results
- formal downloadable report bundles beyond Markdown policy briefs and documentation

The current Python SAM multiplier fallback is a screening tool. It should not be presented as a full CGE equilibrium result.

## 17. Roadmap

The agreed development sequence is:

1. Formalize model blocks and equations.
2. Build calibration layer from SAM.
3. Build open-source equilibrium solver prototype.
4. Add recursive dynamics.
5. Add full AI-assisted scenario and policy interpretation.

### Next Recommended Phase

The next technical step is Phase 3:

> Build a lightweight open-source equilibrium solver prototype.

This should start with residual functions and a solver interface, while keeping solver dependencies optional and guarding imports so Hugging Face startup remains stable.

## 18. Practical Usage Today

A user can currently:

1. Open the Signal dashboard.
2. Use the AI CGE Chat Studio.
3. Ask a natural-language policy question.
4. Optionally upload a SAM.
5. Run a deterministic SAM multiplier simulation.
6. Inspect scenario JSON, diagnostics, results summary, policy explanation, and recommended next simulations.

The calibration prototype can be used from Python:

```python
from cge_workbench.calibration import calibrate_signal_cge

calibration = calibrate_signal_cge(sam_df)
```

This prepares the benchmark dataset for future full CGE solving.

## 19. Deployment Notes

No heavy dependencies were added during the CGE work. The root `requirements.txt` remains lean:

- Gradio
- NumPy
- pandas
- scikit-learn
- joblib
- openpyxl
- FastAPI / Pydantic version constraints

GAMS and future open-source solver libraries remain optional.

## 20. Summary

Signal CGE has moved from an initial policy-simulation concept into a structured AI-assisted CGE/SAM workbench with:

- a working Gradio interface
- deterministic chat orchestration
- Python fallback execution
- diagnostics and policy explanation
- formal model-core blocks
- closure validation
- calibration prototype
- tests and documentation

The project is now ready for the next phase: an optional open-source equilibrium solver prototype that uses the calibrated benchmark and formal equation blocks.
