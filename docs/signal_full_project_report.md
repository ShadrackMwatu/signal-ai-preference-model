# Signal Full Project Intelligence Report

Date: 2026-05-04  
Repository: `ShadrackMwatu/signal-ai-preference-model`  
Local project folder: `C:\Users\smwatu\OneDrive - Kenya Institute for Public Policy Research and Analysis\Documents\Signal`

## Report Scope and Evidence Base

This report documents the Signal project from its initial prototype through the current repository state. It combines:

- The project history and instructions discussed during development.
- The current tracked repository structure.
- The current root Gradio app in `app.py`.
- The modular behavioral-signal AI pipeline under `src/`.
- The CGE modelling framework under `signal_modeling_language/`, `signal_execution/`, `backends/gams/`, `solvers/`, `cge_core/`, and `policy_intelligence/`.
- The learning system under `signal_learning/` and `learning_memory/`.
- The current Git workflow, Git LFS configuration, Hugging Face sync workflow, and documentation system.

Status labels used in this report:

- **Implemented**: present in the repository as code, data, tests, documentation, workflow configuration, or tracked model artifacts.
- **Designed**: discussed and represented as architecture, but not necessarily complete for production.
- **Planned but not yet implemented**: requested or conceptually defined, but not fully present in code.

Important clarification: Signal currently has both learned ML components and deterministic helper logic. The deployed demand classifier and modular demand model suite are trained from data. Some synthetic label generation, feature construction, market recommendation templates, and policy interpretation text remain deterministic prototype logic. This is expected for the current prototype stage and is listed under limitations.

## Historical Development Timeline

Signal evolved in several phases:

- **Repository initialization**: The project was initialized locally, connected to GitHub, renamed from `New project 2` to `Signal`, and pushed to the GitHub repository.
- **Initial Signal model**: The first implementation was a small preference model prototype with data ingestion, model training, prediction, and research-friendly outputs.
- **Module 1 data ingestion**: A deterministic synthetic data generator and tests were added for initial preference data ingestion.
- **Research-oriented outputs**: Outputs were extended for interpretability, policy labels, and CGE/SAM export compatibility.
- **Adaptive behavioral-signal AI**: The project was upgraded into a modular system for anonymized behavioral signals, feature engineering, ML demand prediction, clustering, opportunity intelligence, drift detection, and retraining.
- **Hugging Face Gradio deployment**: The root `app.py` became the Hugging Face entry point. The app uses a saved scikit-learn demand classifier and returns a demand class, aggregate demand score, and opportunity score.
- **CGE modelling framework**: A second, complementary policy-modelling layer was added. It includes Signal Modelling Language, an execution environment, GAMS-compatible generation, solver abstraction, CGE core modules, and policy intelligence.
- **Learning system**: Signal was extended to observe model runs, diagnose issues, store lessons, recommend improvements, validate changes, implement low-risk fixes as versioned adaptations, re-test, and remember.
- **Project structure and documentation system**: Folders were created for data, documents, models, outputs, docs, knowledge base, and learning versions.
- **Hugging Face dependency fix**: `requirements.txt` at the project root was simplified to the exact Hugging Face runtime dependencies:

```text
gradio
numpy
pandas
scikit-learn
joblib
```

Recent Git history includes commits such as:

```text
7ded542 Fix Hugging Face dependencies (joblib issue)
da4893f Fix Hugging Face dependencies
bceb045 Initialize Signal structure, documentation system, and Hugging Face sync
acf0e11 Connect Signal UI to ML model
a50da58 Upgrade Signal to ML-based behavioral demand model
835651d Upgrade Signal into adaptive behavioral signals AI model with NLP, demand prediction, and opportunity intelligence
c05e9a7 Implement adaptive Signal AI revealed demand intelligence system
8f094ae Initial Signal model
```

## Section 1: Project Origin and Vision

### Initial Concept

Signal began as an AI preference and demand-intelligence prototype. The core idea was to infer meaningful aggregate preferences from observable behavioral traces without tracking individuals.

The earliest technical form was a Python model that loaded structured preference data, trained a scikit-learn model, produced interpretable scores, and exposed results through an API. The project then moved beyond preference scoring into behavioral market intelligence and policy modelling.

### Core Idea

Signal is designed as:

```text
privacy-preserving AI for analyzing anonymized and aggregated behavioral signals
```

The system is intended to convert behavioral activity into aggregate intelligence:

```text
behavioral data -> feature extraction -> model training -> prediction -> recommendation -> feedback -> retraining
```

### Intellectual Foundations

Signal draws from four main intellectual traditions:

- **Behavioral economics**: Observed actions can reveal constraints, preferences, urgency, dissatisfaction, and demand intensity.
- **Revealed preference theory**: What people do can be more informative than what they say they want, especially when behavior is repeatedly observed and aggregated.
- **Computational social science**: Large-scale, anonymized digital traces can be transformed into social, economic, and policy insights when handled ethically.
- **Policy intelligence for Kenya**: County-level and sector-level insights can inform public policy, market access, infrastructure planning, supplier strategy, and CGE/SAM scenario design.

### Intended Outputs

The intended Signal output family includes:

- Topic-level preference and demand insights.
- County-level demand and market opportunity insights.
- Time-based preference intelligence.
- Category preference indices.
- National aggregate demand indices.
- Market gap and opportunity scores.
- Policy-ready summaries for CGE/SAM workflows.
- Exportable outputs for dashboards, reports, and scenario models.

## Section 2: Conceptual Framework

### Behavioral Signals

A behavioral signal is an observable cue produced by an action, interaction, delay, omission, complaint, search, or repeated engagement pattern.

Examples include:

- Clicks.
- Likes.
- Comments.
- Shares.
- Saves.
- Views.
- Searches.
- Hashtags.
- Mentions.
- Complaints.
- Purchase-intent phrases.
- Repeated engagement.
- Ignored content.
- Delayed responses.

Signal treats these actions as aggregate behavioral evidence. It does not treat them as individual psychological profiles.

### Data, Signals, and Intelligence

Signal distinguishes three layers:

- **Data**: Raw or structured observations, such as counts of likes, comments, searches, or complaints.
- **Signals**: Interpreted behavioral cues, such as engagement intensity, urgency, dissatisfaction, or purchase intent.
- **Intelligence**: Decision-ready outputs, such as demand classification, opportunity score, market gap, value proposition, or policy message.

The conceptual chain is:

```text
observable cue -> interpreted meaning -> behavioral outcome
```

For example:

```text
repeated searches + complaint terms + low supplier coverage
-> unmet need signal
-> opportunity for county-level supplier/logistics intervention
```

### Relationship to CGE Modelling, SAM Frameworks, and Policy Advisory Systems

Signal has two complementary modules:

1. **Behavioral Signals AI**
   - Infers revealed aggregate demand from anonymized behavioral data.
   - Produces county/category/time/segment demand intelligence.
   - Supports market opportunity analysis.

2. **Signal CGE Modelling Framework**
   - Parses and validates CGE model specifications.
   - Loads and checks SAM data.
   - Generates GAMS-compatible code.
   - Runs through GAMS if available, or through experimental Python backends for prototype execution.
   - Generates policy reports and learning feedback.

The strategic connection is that behavioral demand intelligence can inform CGE shocks, scenario design, sector priorities, and SAM account interpretation.

## Section 3: Naming and Brand Development

### Meaning of "Signal"

The name "Signal" was selected because it is short, technical, internationally legible, and conceptually precise. A signal is not merely data. A signal is data that carries meaning.

In the project context:

```text
Signal = a privacy-preserving system that extracts meaning from aggregate behavior
```

The name supports both project modules:

- Behavioral Signals AI.
- Signal CGE Modelling Framework.

### Swahili Equivalents

Possible Swahili equivalents and related meanings:

- **Ishara**: sign, indication, signal.
- **Dalili**: sign, symptom, indicator.
- **Kiashiria**: indicator or index.
- **Mwenendo**: trend, pattern, movement, or direction.

Brand interpretation:

- `Ishara` emphasizes sign and interpretation.
- `Dalili` emphasizes diagnostic evidence.
- `Kiashiria` emphasizes index-building and measurement.
- `Mwenendo` emphasizes movement, trends, and behavioral direction.

### Global Translations

Representative global equivalents:

- English: Signal.
- French: signal or signe.
- Spanish: senal.
- Portuguese: sinal.
- German: Signal.
- Arabic: ishara.
- Hindi: sanket.
- Chinese: xinhao.
- Japanese: shingo.
- Korean: sinho.

The global pattern is that the idea travels well across languages because it links to signs, indicators, cues, and encoded meaning.

### Proposed Brand Names

Names discussed for possible brand/product variants:

- **Signalyx**
- **Signalyst**
- **Isharix**
- **SignaCore**
- **Signalynx**

### Branding Strategy Insight

Recommended brand structure:

- Keep **Signal** as the master brand.
- Use sub-brands for modules or editions:
  - Signal Behavioral Signals AI.
  - Signal CGE.
  - Signal SML.
  - Signal Learning.
  - Signal Policy Intelligence.

This avoids fragmenting the project too early while preserving room for future specialized products.

## Section 4: System Architecture (Full)

Signal is designed as a layered intelligence system. The current repository includes all major layers in modular form.

### 1. Signal Modelling Language (SML)

Status: **Implemented as a prototype**

Folder:

```text
signal_modeling_language/
```

Files:

- `grammar.py`
- `parser.py`
- `schema.py`
- `validator.py`
- `examples/basic_cge.sml`
- `README.md`

Purpose:

- Provide an internal modelling language for CGE models.
- Support high-level sections such as sets, parameters, variables, equations, shocks, closure rules, solve commands, and outputs.
- Parse model files into structured Python schema objects.
- Validate syntax and model completeness before execution.

### 2. Signal Execution Environment

Status: **Implemented as a prototype**

Folder:

```text
signal_execution/
```

Files:

- `runner.py`
- `workflow.py`
- `config.py`
- `logger.py`
- `diagnostics.py`
- `README.md`

Purpose:

- Read SML files or SML text.
- Validate syntax and model requirements.
- Load SAM data.
- Check SAM balance.
- Calibrate shares.
- Generate GAMS-compatible code.
- Select a solver backend.
- Save outputs under `outputs/<run_id>/`.
- Capture execution logs.
- Trigger learning-memory and Signal Learning workflows.

### 3. GAMS Integration Layer

Status: **Implemented as a compatibility layer**

Folder:

```text
backends/gams/
```

Files:

- `gams_generator.py`
- `gams_runner.py`
- `gams_templates.py`
- `gdx_reader.py`
- `lst_parser.py`
- `README.md`

Purpose:

- Generate `.gms` files from SML model specifications.
- Produce GAMS blocks for sets, parameters, variables, equations, model declaration, solve commands, display, and unload.
- Call local GAMS only if installed.
- Parse `.lst` logs for common GAMS errors.
- Provide best-effort GDX handling.

Important rule:

```text
Do not fake successful GAMS execution.
```

If GAMS is unavailable, Signal returns:

```text
GAMS backend unavailable; using experimental Python backend or validation-only mode.
```

### 4. Solver Layer

Status: **Implemented as a prototype abstraction**

Folder:

```text
solvers/
```

Files:

- `base_solver.py`
- `gams_solver.py`
- `python_nlp_solver.py`
- `fixed_point_solver.py`
- `solver_registry.py`
- `README.md`

Purpose:

- Separate model specification from numeric computation.
- Provide a common solver interface.
- Route execution to GAMS, an experimental Python nonlinear solver, or an experimental fixed-point fallback.

Current solver backends:

- `gams`: production-oriented path when GAMS is installed.
- `python_nlp`: experimental SciPy-style nonlinear optimization path.
- `fixed_point`: experimental fallback for validation and demonstrations.

### 5. CGE Core

Status: **Implemented as a prototype**

Folder:

```text
cge_core/
```

Files:

- `sam.py`
- `calibration.py`
- `accounts.py`
- `closures.py`
- `shocks.py`
- `equations.py`
- `validation.py`
- `results.py`
- `README.md`

Purpose:

- Load SAM data from CSV or Excel.
- Convert long-format or matrix-format SAM files into a square matrix.
- Reject PII columns in SAM files.
- Check row-column balance.
- Classify accounts.
- Calibrate shares.
- Validate closure logic.
- Summarize model results.

### 6. Policy Intelligence Layer

Status: **Implemented as a prototype**

Folder:

```text
policy_intelligence/
```

Files:

- `interpreter.py`
- `report_generator.py`
- `scenario_comparison.py`
- `kenya_policy_templates.py`
- `README.md`

Purpose:

- Convert model results into policy language.
- Generate Markdown reports.
- Summarize GDP, welfare, sectoral, trade, government revenue, and distributional effects.
- Provide Kenya-oriented policy templates.

### 7. Learning System

Status: **Implemented as an early-stage learning loop**

Folders:

```text
signal_learning/
learning_memory/
knowledge_base/
learning_versions/
```

Purpose:

- Store structured lessons from model runs, validation failures, solver messages, GAMS logs, and user corrections.
- Identify recurring issues.
- Recommend adapted validation rules, templates, and guidance.
- Apply only low-risk fixes as versioned adapted templates.
- Preserve rollback information.

### 8. API Layer

Status: **Implemented**

Folder:

```text
api/
```

Files:

- `app.py`
- `main.py`
- `routes_models.py`
- `routes_scenarios.py`
- `routes_results.py`
- `routes_learning.py`
- `schemas.py`
- `README.md`

Purpose:

- Serve modular Signal endpoints through FastAPI.
- Parse, validate, run, and retrieve SML/CGE results.
- Expose behavioral demand, county demand, opportunities, segments, and market access outputs.
- Expose learning feedback, lessons, apply, and rollback endpoints.

Note: The root Hugging Face app uses Gradio. The FastAPI layer exists for local/API deployment and may require API-specific dependencies if deployed separately.

### 9. Dashboard (Hugging Face / UI)

Status: **Implemented through Gradio in root `app.py`**

Current tabs:

- Behavioral Signals AI.
- Signal CGE Framework.
- SML CGE Workbench.
- Learning.

Purpose:

- Provide a Hugging Face-compatible entry point.
- Load the saved ML classifier safely.
- Provide CGE scenario running and SML validation.
- Display learning lessons, recurring issues, recommended fixes, apply/ignore actions, and rollback.

### 10. GitHub Data Layer

Status: **Implemented as repository structure plus Git LFS and Hugging Face sync**

Purpose:

- Store code, sample data, documentation, model artifacts, and project logs.
- Track large Excel workbook files through Git LFS.
- Sync GitHub `main` to the Hugging Face Space through GitHub Actions.

Current Git LFS configuration in `.gitattributes`:

```text
*.xlsx filter=lfs diff=lfs merge=lfs -text
*.xlsm filter=lfs diff=lfs merge=lfs -text
```

## Section 5: CGE and SAM Integration

### SAM Structure

Signal includes a sample long-format SAM:

```text
data/sample_sam.csv
```

Current sample accounts include:

- `agriculture`
- `manufacturing`
- `services`
- `transport`
- `households`
- `government`
- `investment`
- `rest_of_world`

The current sample SAM is a small demonstration dataset, not a full official Kenya 2024 SAM.

### Kenya 2024 Context

Status: **Designed / planned**

The project target is Kenya policy intelligence. The CGE framework is structured so a Kenya SAM can be loaded, checked, calibrated, shocked, solved, and interpreted.

Planned production use would require:

- Official or validated Kenya SAM data.
- Correct national accounts mapping.
- Sector disaggregation appropriate to the policy question.
- Household, factor, government, trade, savings-investment, and tax accounts.
- Documentation of data sources, balancing assumptions, and calibration methods.

### Gender-Care Disaggregation

Status: **Planned but not yet implemented**

The project has identified gender-care CGE analysis as a future area. Potential disaggregation includes:

- Paid care services.
- Unpaid care work.
- Gender-disaggregated labor factors.
- Rural and urban households.
- Care infrastructure.
- Public care expenditure.
- Time-use constraints.

The current sample SAM does not yet include these accounts.

### Endogenous and Exogenous Accounts

In CGE and multiplier modelling, accounts may be treated as endogenous or exogenous depending on closure rules.

Examples:

- Endogenous accounts can include activities, commodities, factors, and households.
- Exogenous accounts can include government, rest of world, investment, or savings, depending on the closure.

Current Signal support:

- SML closure declarations.
- Closure validation.
- Scenario-level closure selection in the simpler `src/cge` scenario DSL.

### Multiplier Modelling Logic

Status: **Designed / partly represented**

The project uses SAM structure and policy-scenario logic to support multiplier-style reasoning:

```text
shock -> direct account effect -> sectoral response -> household/factor/fiscal/trade interpretation
```

The current CGE runner is a prototype. Production multiplier or CGE analysis would require deeper equation systems, calibrated behavioral functions, and validated closure choices.

### Calibration Principles

Implemented calibration principles include:

- Load SAM into a square account matrix.
- Ensure values are numeric and non-negative.
- Compute account row totals and column totals.
- Check balance by account.
- Estimate account shares from SAM totals.
- Use calibrated shares in generated model summaries and GAMS-compatible code.

SAM balance formula:

```text
imbalance = row_total - column_total
percentage_imbalance = imbalance / max(row_total, column_total)
```

### Closure Rules

Implemented closure support includes SML closure declarations such as:

```text
CLOSURE:
  government_savings = endogenous
  exchange_rate = fixed
  numeraire = consumer_price_index
```

Designed closure issues include:

- Government savings endogenous versus fixed.
- Exchange rate fixed versus flexible.
- Savings-driven versus investment-driven closure.
- Numeraire selection.
- External balance handling.
- Government balance handling.

### Scenario Design

Current implemented sample scenarios include:

- Aggregate demand and transport productivity scenario.
- Services market access expansion.

Example from `data/sample_cge_scenarios.csv`:

```text
shock demand agriculture by 6%
shock productivity transport by 3%
shock tax manufacturing by -1%
```

Planned care-economy scenarios:

- Care services expansion.
- Care infrastructure investment.
- Paid care versus unpaid care reallocation.
- Public care subsidy scenarios.
- Gender-disaggregated labor supply response.

These care-economy scenarios are not yet fully implemented in the sample SAM or equation system.

## Section 6: GAMS Understanding

### What GAMS Is

GAMS means **General Algebraic Modeling System**.

GAMS is:

- A modelling language.
- An execution environment.
- A system for expressing sets, parameters, variables, equations, models, solve statements, and outputs.

GAMS is not the mathematical solver itself.

### What a Solver Is

A solver is the mathematical engine that solves a specific class of optimization or equilibrium problem.

Examples:

- **PATH**: Often used for mixed complementarity problems and equilibrium models.
- **CONOPT**: Used for nonlinear programming problems.
- **IPOPT**: Used for nonlinear optimization.
- **CPLEX**: Used for linear programming, mixed-integer programming, and related optimization classes.
- **GUROBI**: Used for linear, quadratic, and mixed-integer optimization.

### Role Separation

The clean conceptual separation is:

```text
model specification -> execution environment -> mathematical solver -> results
```

In the GAMS ecosystem:

```text
GAMS model code -> GAMS execution environment -> PATH/CONOPT/IPOPT/CPLEX/GUROBI -> solution output
```

In Signal:

```text
SML model specification -> Signal execution environment -> GAMS or Python backend -> policy intelligence output
```

## Section 7: Signal-GAMS Relationship

### Why Signal Does Not Replace GAMS Initially

Signal does not try to replace GAMS at the current stage because:

- GAMS is mature and trusted for economic modelling workflows.
- GAMS already supports established solver integrations.
- Production-grade CGE solving requires robust numerical infrastructure.
- Many CGE researchers and policy institutions already use GAMS.

### Signal as Orchestration and Intelligence Layer

Signal initially acts as:

- A modelling-language front end.
- A validation layer.
- A SAM diagnostics layer.
- A GAMS code generation layer.
- A policy interpretation layer.
- A learning and memory layer.

This lets Signal help users build, validate, run, interpret, and improve models without pretending to replace proven solvers prematurely.

### GAMS as Computational Backend

For production-grade CGE solving, the intended trusted path remains:

```text
Signal SML -> generated GAMS code -> GAMS -> solver such as PATH or CONOPT -> results -> Signal policy intelligence
```

### Long-Term Signal-Native Solver Plan

Status: **Planned but not yet production-grade**

Signal includes experimental Python solver backends, but they are not production replacements for GAMS plus established solvers.

Long-term development could include:

- A Signal-native model compiler.
- Stronger equation system representation.
- Automatic differentiation.
- Solver diagnostics.
- Calibration validation.
- Robust nonlinear and complementarity solving.
- Reproducible benchmark tests against GAMS models.

## Section 8: Signal Modelling Language (SML)

### Purpose

Signal Modelling Language is a compact internal language for specifying CGE model structure.

It supports:

- `SETS`
- `PARAMETERS`
- `VARIABLES`
- `EQUATIONS`
- `CLOSURE`
- `SHOCKS`
- `SOLVE`
- `OUTPUT`

### Syntax Definition

The syntax is section-based:

```text
SECTION:
  key = value
  symbol[index]
  shock_name = target + value
```

SML is intended to be easier to inspect and learn than full GAMS while still being translatable into GAMS-compatible model code.

### Example SML Model

Current example file:

```text
signal_modeling_language/examples/basic_cge.sml
```

Example:

```text
SETS:
  sectors = [agriculture, manufacturing, services]
  factors = [labour, capital]
  households = [rural, urban]

PARAMETERS:
  SAM = "data/sample_sam.csv"
  elasticity_armington = 2.0
  elasticity_cet = 2.0

VARIABLES:
  output[sectors]
  price[sectors]
  consumption[households,sectors]
  imports[sectors]
  exports[sectors]

EQUATIONS:
  market_clearing[sectors]
  household_income[households]
  armington_demand[sectors]
  cet_supply[sectors]
  government_balance
  savings_investment_balance

CLOSURE:
  government_savings = endogenous
  exchange_rate = fixed
  numeraire = consumer_price_index

SHOCKS:
  increase_vat = tax_rate + 0.02
  productivity_growth = productivity[agriculture] + 0.05

SOLVE:
  model = kenya_cge
  backend = gams
  solver = path

OUTPUT:
  gdx = "outputs/results.gdx"
  excel = "outputs/results.xlsx"
  report = "outputs/policy_report.md"
  gams = "outputs/kenya_cge.gms"
```

### Current SML Capabilities

Implemented:

- Parse SML text and files.
- Represent parsed models in schema objects.
- Validate required sections.
- Validate model structure enough for prototype execution.
- Generate GAMS-compatible code.
- Run through SignalRunner.

Planned but not yet implemented:

- Full GAMS-equivalent expression parsing.
- Complete algebraic equation bodies.
- MPSGE-style model declarations.
- Full complementarity syntax.
- Rich include/import system.

## Section 9: Execution Environment

### Workflow

The execution environment follows:

```text
parse -> validate -> calibrate -> generate -> solve -> interpret -> output
```

Current `SignalRunner` workflow:

1. Read SML file or SML text.
2. Parse into an SML model schema.
3. Validate the model.
4. Create a unique run ID.
5. Create `outputs/<run_id>/`.
6. Resolve the SAM path.
7. Load SAM data.
8. Run diagnostics and balance checks.
9. Export `balance_check.md` and `balance_check.xlsx`.
10. Calibrate from SAM.
11. Generate GAMS-compatible `.gms` code.
12. Select solver backend.
13. Run solver backend.
14. Generate policy report.
15. Summarize results.
16. Capture learning memory.
17. Run Signal Learning cycle.
18. Store run result in the in-memory run store.
19. Write execution log.

### Logging

Implemented:

- `signal_execution/logger.py`
- Per-run logs under `outputs/<run_id>/execution.log`

### Diagnostics

Implemented diagnostics include:

- SAM balance status.
- Balance-check rows.
- Warnings and errors.
- Backend and solver messages.
- GAMS availability messages.

### Error Handling

Implemented safeguards:

- Missing SAM files produce clear errors.
- Invalid SML raises validation errors.
- GAMS unavailability is explicitly reported.
- Missing deployed ML model in root `app.py` returns:

```text
Model not loaded
```

with zero scores.

## Section 10: Solver Layer

### Solver Abstraction

The solver layer defines a common interface:

```python
class BaseSolver:
    def solve(self, model_spec, data, options):
        pass
```

This lets Signal select backends without hard-coding all execution logic into the runner.

### Available Solvers

Implemented backend categories:

- **GAMS backend**
  - Production-oriented when local GAMS is installed.
  - Generates `.gms` code and calls GAMS through the compatibility layer.

- **Python NLP solver**
  - Experimental nonlinear optimization path.
  - Useful for prototype validation only.

- **Fixed-point solver**
  - Experimental fallback.
  - Useful for simple demonstrations and validation-only runs.

### Limitations of the Internal Solver

The internal Python solver layer is not production-grade. It does not yet replace:

- GAMS execution.
- PATH for complementarity models.
- CONOPT/IPOPT for production nonlinear CGE models.
- Carefully calibrated, benchmarked economic model solving.

## Section 11: Learning System (Critical)

### Core Learning Loop

Signal Learning implements the loop:

```text
Observe -> Diagnose -> Store -> Recommend -> Validate -> Implement -> Re-test -> Remember
```

This extends the earlier learning-memory concept:

```text
model runs -> errors/results/logs -> learning memory -> improved templates/rules -> better future runs
```

### Learning Store

Status: **Implemented**

File:

```text
signal_learning/learning_store.py
```

Default store:

```text
outputs/signal_learning_store.json
```

The store can record:

- Uploaded SAM structure.
- Account classifications.
- Calibration patterns.
- Model equations.
- Closure rules.
- Shock definitions.
- GAMS errors.
- Solver failures.
- Successful model runs.
- User corrections.
- Final reports.

Privacy note: The learning store is designed to keep structural evidence and avoid raw SAM cells, PII, usernames, emails, phone numbers, GPS, or individual-level behavioral records.

### Feedback Collector

Status: **Implemented**

File:

```text
signal_learning/feedback_collector.py
```

Feedback sources:

- User corrections.
- Validation errors.
- Validation warnings.
- SAM imbalance checks.
- GAMS unavailable messages.
- Experimental solver warnings.
- Successful model runs.
- Parsed GAMS `.lst` errors.

Each feedback entry includes:

- `run_id`
- `timestamp`
- `issue_type`
- `source`
- `original_value`
- `corrected_value`
- `lesson_learned`
- `confidence_score`
- Evidence link:
  - source run
  - observed error or result
  - correction made
  - validation status

### Pattern Extractor

Status: **Implemented**

File:

```text
signal_learning/pattern_extractor.py
```

Designed recurring patterns:

- Common SAM imbalance causes.
- Frequently misclassified accounts.
- Repeated GAMS syntax errors.
- Closure inconsistencies.
- Shocks that fail under certain closures.
- Solver convergence problems.

Current implementation summarizes recurring issue types and supports adaptation proposals.

### Adaptation Engine

Status: **Implemented**

File:

```text
signal_learning/adaptation_engine.py
```

The adaptation engine converts recurring patterns into versioned proposals.

It can recommend updates to:

- Validation rules.
- Account classification rules.
- Default closure recommendations.
- Solver selection recommendations.
- GAMS code-generation templates.
- Scenario templates.
- Policy-report interpretation logic.

Important safety rule:

```text
Signal does not silently overwrite core templates.
```

Adaptations are versioned under:

```text
learning_versions/
```

### Implementation Engine

Status: **Implemented**

File:

```text
signal_learning/implementation_engine.py
```

The implementation engine can:

- Suggest a fix.
- Save recommendations for user review.
- Apply low-risk fixes as versioned adapted templates.
- Block high-risk fixes from automatic application.
- Support rollback where rollback copies exist.

Examples of intended learned interventions:

- If a SAM row and column are imbalanced, suggest likely account areas to review.
- If GAMS reports "uncontrolled set entered as constant", explain the indexing issue.
- If PATH fails to converge, suggest initialization, scaling, or solver-option changes.
- If a tax shock causes government balance failure, suggest reviewing closure assumptions.

### Learning Modes

Implemented modes:

- `observe_only`: Records lessons but changes nothing.
- `recommend`: Records lessons and recommends improvements.
- `safe_apply`: Applies low-risk fixes as versioned adapted templates only.

Default mode:

```text
recommend
```

### Learning Reports

Status: **Implemented**

Signal can generate:

```text
outputs/learning_report.md
```

The report includes:

- What Signal observed.
- What failed.
- What worked.
- What was learned.
- Recommended fixes.
- Whether anything was automatically applied.
- Confidence level.

### Versioned Learning

Status: **Implemented**

Current version structure includes:

```text
learning_versions/v001/
```

Each adaptation version is designed to include:

- Change summary.
- Reason for change.
- Affected templates or rules.
- Confidence score.
- Rollback instructions.

## Section 12: GitHub Integration

### GitHub Repository

Project repository:

```text
https://github.com/ShadrackMwatu/signal-ai-preference-model
```

### Git Workflow

The project was initialized and synchronized through local Git commands:

```powershell
git init
git add .
git commit -m "Initial Signal model"
git remote add origin https://github.com/ShadrackMwatu/signal-ai-preference-model.git
git branch -M main
git push -u origin main
```

Recent development used local shell Git commands. The project instruction explicitly avoided GitHub API or GitHub connector writes for local code changes.

### Git LFS for Large Excel Files

Git LFS is configured for large Excel workbook files:

```text
*.xlsx filter=lfs diff=lfs merge=lfs -text
*.xlsm filter=lfs diff=lfs merge=lfs -text
```

Typical Git LFS workflow:

```powershell
git lfs install
git lfs track "*.xlsx"
git lfs track "*.xlsm"
git add .gitattributes
git add data/sams/my_sam.xlsx
git commit -m "Add SAM workbook"
git push origin main
```

### Folder Structure

Implemented root-level structure includes:

```text
data/
  sams/
  raw/
  processed/

documents/
  cge_frameworks/
  policy_notes/
  coding_logs/

models/
  gams/
  saved_models/
  sml/

outputs/

docs/
```

### GitHub as Data Repository

GitHub acts as:

- Code repository.
- Documentation repository.
- Sample data repository.
- Model artifact repository for small tracked artifacts.
- Version history for development decisions.
- Source for Hugging Face Space synchronization.

### Signal as Learning System

Signal acts as:

- Model runner.
- Diagnostics engine.
- Policy intelligence layer.
- Learning memory.
- Recommendation and adaptation system.

The strategic distinction is:

```text
GitHub = versioned storage and collaboration layer
Signal = modelling, intelligence, learning, and execution layer
```

## Section 13: Dashboard Design

### Hugging Face Spaces Deployment

Status: **Implemented**

The deployed app entry point is:

```text
app.py
```

The GitHub Actions workflow is:

```text
.github/workflows/sync-to-huggingface.yml
```

The workflow syncs GitHub `main` to:

```text
Signal-ai/signal-ai-dashboard
```

The Space SDK is:

```text
gradio
```

### Gradio Interface

Current root `app.py` implements a Gradio app with four tabs:

1. **Behavioral Signals AI**
   - Inputs: likes, comments, shares, searches, engagement intensity, purchase intent score, trend growth.
   - Current ML model uses likes, comments, shares, and searches for prediction.
   - Outputs: predicted demand class, aggregate demand score, opportunity score.

2. **Signal CGE Framework**
   - Input: simple scenario text.
   - Outputs: CGE simulation summary, policy intelligence JSON, GAMS compatibility preview.

3. **SML CGE Workbench**
   - Upload SAM CSV/XLSX.
   - Upload or edit SML model file.
   - Validate model.
   - Run scenario.
   - View balance check.
   - View results JSON.
   - Download policy report.

4. **Learning**
   - Refresh recent lessons.
   - View recurring issues.
   - View recommended fixes.
   - Apply latest low-risk fix.
   - Ignore latest recommendation.
   - Roll back a version.

### Designed Dashboard Workflow

The intended user workflow is:

```text
upload -> validate -> run -> view -> download
```

Current implementation supports this workflow for SML/SAM runs through the SML CGE Workbench tab.

### Privacy Notice

Privacy is a core design requirement:

```text
Signal uses anonymized and aggregated behavioral signals only.
It does not track individuals, store PII, usernames, phone numbers, emails, or exact GPS data.
```

The current repository implements privacy validation in the data pipeline and SAM loader. The root Gradio app could make this notice more visible in future UI polish.

## Section 14: API Design

### Behavioral and Market Intelligence Endpoints

Implemented in `api/app.py`:

- `GET /health`
- `GET /predict-demand`
- `GET /county-demand`
- `GET /opportunities`
- `GET /segments`
- `GET /market-access`

### CGE/SML Endpoints

Implemented in `api/routes_models.py`:

- `POST /models/parse`
- `POST /models/validate`
- `POST /models/run`

Implemented in `api/routes_results.py`:

- `GET /results/{run_id}`
- `GET /results/{run_id}/report`

Implemented in `api/routes_scenarios.py`:

- `GET /scenarios/example`

### Learning Endpoints

Implemented in `api/routes_learning.py`:

- `POST /learning/feedback`
- `GET /learning/report/{run_id}`
- `GET /learning/lessons`
- `POST /learning/apply`
- `POST /learning/rollback`

### API Output Principle

The API is designed for aggregate outputs only:

- Country.
- County.
- Category.
- Consumer segment.
- Time period.

It does not expose raw individual-level records.

## Section 15: Output System

### Current Output Locations

Signal writes execution outputs to:

```text
outputs/<run_id>/
```

Implemented output files include:

- Generated `.gms` files.
- `balance_check.xlsx`.
- `balance_check.md`.
- `policy_report.md`.
- `execution.log`.

Signal Learning can also write:

```text
outputs/learning_report.md
outputs/signal_learning_store.json
```

### SML Output Declarations

SML supports declarations such as:

```text
OUTPUT:
  gdx = "outputs/results.gdx"
  excel = "outputs/results.xlsx"
  report = "outputs/policy_report.md"
  gams = "outputs/kenya_cge.gms"
```

Current status:

- `report` output is implemented through Markdown policy reports.
- `gams` output is implemented through generated `.gms` files.
- `balance_check.xlsx` is implemented.
- `results.gdx` depends on GAMS/GDX availability and is not guaranteed.
- `results.xlsx` as a full solved-results workbook is planned but not fully implemented.

### Behavioral Intelligence Outputs

Implemented market-intelligence outputs include:

- `national_aggregate_demand_index`
- `county_demand_index`
- `category_preference_index`
- `behavioral_signal_score`
- `aggregate_demand_score`
- `opportunity_score`
- `demand_classification`
- `trend_direction`
- `demand_forecast`
- `recommended_value_proposition`
- `product_or_service_opportunity`
- `revenue_model`
- `competitor_gap`
- `supplier_recommendation`
- `logistics_recommendation`
- `payment_recommendation`

## Section 16: Terminal and Local Setup

### Creating and Working in the Project Folder

The local project folder is:

```text
C:\Users\smwatu\OneDrive - Kenya Institute for Public Policy Research and Analysis\Documents\Signal
```

Navigate there in PowerShell or Command Prompt:

```powershell
cd "C:\Users\smwatu\OneDrive - Kenya Institute for Public Policy Research and Analysis\Documents\Signal"
```

### File Explorer, Terminal, and Codex

- **File Explorer**: Visual file browser. Useful for seeing folders, opening documents, and confirming files exist.
- **Terminal**: Command-line environment. Used for Git, Python, tests, app launches, and local automation.
- **Codex**: AI coding collaborator operating inside the local workspace. Used to inspect files, edit code/docs, run tests, and help implement requested changes.

### Common Git Commands

```powershell
git status
git add .
git commit -m "Your commit message"
git push origin main
```

### Common Python Commands

Run the Hugging Face Gradio app locally:

```powershell
python app.py
```

Regenerate the deployed ML demand model:

```powershell
python -m src.models.signal_demand_model
```

Generate sample behavioral, competitor, and feedback data:

```powershell
python -m src.data_pipeline.synthetic_data --data-dir data
```

Run the SML example:

```powershell
python -c "from signal_execution.runner import SignalRunner; print(SignalRunner().run('signal_modeling_language/examples/basic_cge.sml')['summary'])"
```

Run the FastAPI API locally:

```powershell
python -m uvicorn api.main:app --reload
```

Run tests:

```powershell
python -m unittest discover -s tests
```

### Dependency Notes

The current root `requirements.txt` is intentionally minimal for Hugging Face:

```text
gradio
numpy
pandas
scikit-learn
joblib
```

The FastAPI API layer may require additional dependencies such as `fastapi`, `pydantic`, and `uvicorn` when deployed as an API service. They are not currently listed because the latest Hugging Face runtime fix required an exact minimal dependency file.

## Section 17: Current Capabilities

### Behavioral Signals AI

Implemented:

- Synthetic Kenya behavioral-signal data generation.
- Sample counties:
  - Nairobi.
  - Mombasa.
  - Kisumu.
  - Nakuru.
  - Machakos.
  - Kiambu.
  - Turkana.
- Behavioral fields:
  - clicks
  - likes
  - comments
  - shares
  - saves
  - views
  - searches
  - hashtags
  - mentions
  - complaints
  - purchase-intent phrases
  - repeated engagement
  - ignored content
  - delayed responses
- Context fields:
  - country
  - county
  - category
  - consumer segment
  - time period
- Rule-based NLP feature extraction:
  - sentiment score
  - purchase intent score
  - complaint score
  - urgency score
  - topic keywords
  - NLP topic
  - topic confidence
- Feature engineering:
  - engagement intensity
  - repetition score
  - trend growth
  - location relevance
  - price sensitivity
  - noise score
  - behavioral signal score
- Privacy filtering:
  - PII column rejection.
  - Email and phone pattern detection.
  - Small-group suppression using `observation_count`.
  - Aggregate-only output columns.

### Machine Learning Demand Models

Implemented:

- Deployed `RandomForestClassifier` for `High`, `Moderate`, and `Low` demand.
- Model artifact:

```text
models/saved_models/signal_demand_classifier.joblib
```

- Synthetic training dataset:

```text
data/signal_training_dataset.csv
```

- Modular model bundle:

```text
models/saved_models/demand_model_bundle.joblib
```

The modular bundle includes:

- RandomForestClassifier for demand classification.
- RandomForestRegressor for aggregate demand score.
- GradientBoostingRegressor for opportunity score.
- LogisticRegression classifiers for emerging-trend probability and unmet-demand probability.
- Feature baseline for drift detection.

### Prediction and Market Intelligence

Implemented:

- Demand prediction from saved models.
- County demand index.
- National aggregate demand index.
- Category preference index.
- Opportunity generation.
- Competitor gap analysis.
- Market access metrics.
- Supplier, logistics, and payment recommendations.

### Clustering

Implemented:

- KMeans clustering over aggregated county/category/segment/time features.
- Output: anonymized segment clusters.

### Feedback and Adaptation

Implemented:

- Drift detection using feature mean/std shift.
- Adaptive retraining trigger.
- Retraining logs in the model bundle.
- Learning store.
- Feedback collector.
- Pattern extractor.
- Adaptation engine.
- Implementation engine.
- Versioned learning outputs.

### CGE Framework

Implemented:

- SML parser and validator.
- SML example model.
- SAM loading from CSV/Excel.
- SAM balance checks.
- Calibration from SAM.
- GAMS-compatible code generation.
- GAMS unavailable fallback messaging.
- Experimental Python solver fallback.
- Fixed-point solver fallback.
- Policy report generation.
- Scenario comparison support.
- Kenya policy templates.

### Dashboard

Implemented:

- Hugging Face-compatible Gradio app in root `app.py`.
- Behavioral ML prediction tab.
- CGE scenario tab.
- SML CGE Workbench tab.
- Learning tab.
- Safe ML model loading fallback.

### API

Implemented:

- Modular FastAPI app under `api/`.
- Behavioral, SML/CGE, result, scenario, and learning endpoints.

### Documentation and Project Structure

Implemented:

- `README.md`.
- Architecture docs under `docs/`.
- Development log under `documents/coding_logs/development_log.md`.
- Knowledge base files for GAMS errors, closure rules, SAM account classification, solver diagnostics, and policy interpretation rules.
- GitHub Actions sync workflow to Hugging Face.
- Git LFS tracking for Excel files.

### Tests

Implemented tests include:

- Data loading.
- Data ingestion.
- Feature engineering.
- Privacy filtering.
- Training pipeline.
- Prediction outputs.
- Clustering.
- Opportunity engine.
- Drift detection.
- Market intelligence.
- Signal demand model.
- CGE framework.
- SML parser.
- SAM balance.
- Calibration.
- GAMS generation.
- Solver registry.
- Policy report.
- Learning store.
- Feedback collector.
- Pattern extractor.
- Adaptation engine.
- Implementation engine.
- Learning workflow.
- API tests.

## Section 18: Limitations

### Dependency on GAMS

Signal can generate GAMS-compatible model code, but production-grade CGE solving still depends on:

- A local GAMS installation.
- Valid GAMS license.
- Correct solver availability.
- Appropriate solver selection.

Signal does not claim GAMS execution succeeded when GAMS is missing.

### Experimental Internal Solver

The Python NLP and fixed-point solvers are experimental. They are useful for:

- Prototype validation.
- Demonstrations.
- Fallback when GAMS is not installed.

They are not yet production-grade CGE solvers.

### Structured Data Requirements

Signal needs structured inputs:

- SAMs must be valid CSV or Excel files.
- Behavioral data must include required aggregate columns.
- Privacy-sensitive columns are rejected.
- Small-cell reporting is suppressed through observation-count thresholds.

### Synthetic Data

The behavioral demand models are trained on synthetic data. This supports prototyping and testability, but production demand intelligence would require:

- Validated real aggregate data sources.
- Data governance approvals.
- Sampling and bias analysis.
- Calibration against observed outcomes.
- Ongoing drift monitoring.

### Rule-Based Prototype Components

The project goal is learned, model-driven intelligence. Current implementation includes both ML and deterministic components:

- The deployed demand classifier is learned from synthetic data.
- The modular demand classifier/regressors are learned from synthetic data.
- Text feature extraction is currently keyword/rule-based.
- Some feature generation and recommendation logic is deterministic.
- Some opportunity and policy text generation uses templates.

These deterministic elements are acceptable for prototype transparency but should be gradually replaced or validated with learned models where appropriate.

### Current Root Gradio Demand Tab

The current root Gradio demand tab exposes numeric behavioral inputs and sliders. The deployed classifier uses:

- likes
- comments
- shares
- searches

Although broader NLP and county/category modules exist, the root demand tab does not currently wire sample social-media text into the deployed classifier output.

### Learning System Early Stage

The learning system is structurally implemented but early-stage. It still needs:

- More real run history.
- More robust pattern evidence.
- Stronger validation before adapting templates.
- Better longitudinal memory review.
- User-facing governance for accepting or rejecting learned rules.

### Results Persistence

`RUN_STORE` is currently in memory for API result lookup. File outputs are persisted, but API result retrieval by run ID may not survive process restarts unless the result is reloaded from disk in a future version.

### Requirements File Tradeoff

The current `requirements.txt` was intentionally reduced to exactly:

```text
gradio
numpy
pandas
scikit-learn
joblib
```

This fixes the Hugging Face Gradio runtime need. The FastAPI service layer may need additional dependencies if deployed independently.

### Privacy Limits

Implemented privacy rules block direct identifiers and suppress small groups. Planned stronger privacy methods include:

- Differential privacy.
- Formal disclosure risk analysis.
- More granular k-anonymity checks.
- Automated output auditing.

These are planned but not yet implemented.

## Section 19: Future Roadmap

### Signal-Native Solver

Planned:

- More complete internal model representation.
- Robust equation parser.
- Complementarity support.
- Automatic differentiation.
- Solver benchmarking against GAMS.
- Clear production-readiness criteria.

### Full AI-Driven CGE Modelling

Planned:

- AI-assisted SML authoring.
- Automatic equation diagnostics.
- Closure recommendation based on policy question.
- SAM account classification suggestions.
- Scenario template generation.
- GAMS error explanation and correction proposals.

### Real-Time Policy Intelligence

Planned:

- Dynamic dashboards.
- Scenario comparison views.
- Automated policy briefs.
- County and sector drilldowns.
- Data-quality warnings.
- Export-ready policy notes.

### Integration with National Data Systems

Planned:

- Kenya SAM integration from validated national sources.
- KNBS and official macro data integration where permitted.
- County-level indicators.
- Sectoral production, trade, tax, employment, and household welfare data.
- Care economy and gender-disaggregated accounts.

### Behavioral Signals Maturity

Planned:

- Real aggregate data ingestion pipelines.
- Transformer-based or LLM-assisted text feature extraction where governance permits.
- Stronger demand forecasting.
- Outcome-based model calibration.
- Drift dashboards.
- Publication-grade validation.

### Privacy and Ethics Expansion

Planned:

- Differential privacy options.
- Stronger no-PII guarantees.
- Automated red-team checks for individual leakage.
- Small-cell suppression across all public outputs.
- Ethics review templates for policy use.

### Reporting and Publication

Planned:

- Academic methods appendix.
- Reproducible experiment logs.
- Model cards.
- Data cards.
- Policy report templates.
- CGE scenario audit trail.

## Appendix A: Current High-Level Repository Map

```text
api/
backends/gams/
cge_core/
data/
docs/
documents/
knowledge_base/
learning_memory/
learning_versions/
models/
outputs/
policy_intelligence/
signal_execution/
signal_learning/
signal_modeling_language/
solvers/
src/
tests/
app.py
README.md
requirements.txt
.github/workflows/sync-to-huggingface.yml
```

## Appendix B: Core Run Commands

Run Hugging Face app locally:

```powershell
python app.py
```

Run FastAPI locally:

```powershell
python -m uvicorn api.main:app --reload
```

Run tests:

```powershell
python -m unittest discover -s tests
```

Run SML example:

```powershell
python -c "from signal_execution.runner import SignalRunner; print(SignalRunner().run('signal_modeling_language/examples/basic_cge.sml')['summary'])"
```

Generate behavioral sample data:

```powershell
python -m src.data_pipeline.synthetic_data --data-dir data
```

Train deployed demand classifier:

```powershell
python -m src.models.signal_demand_model
```

## Appendix C: Core Project Principle

Signal's guiding principle is:

```text
GAMS = modelling language + execution environment
Solver = mathematical engine
Signal = privacy-preserving AI, modelling orchestration, policy intelligence, and learning layer
```

Signal's long-term ambition is to become a trusted AI-assisted policy modelling environment. Its current correct position is as a modular prototype that combines:

- Behavioral revealed-demand intelligence.
- CGE/SAM model orchestration.
- GAMS-compatible execution.
- Experimental Python solver fallback.
- Policy reporting.
- Evidence-linked learning memory.

