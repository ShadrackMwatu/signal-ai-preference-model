# Signal Two-Tab Public Interface

Signal's public Hugging Face interface now exposes only two sections:

1. Behavioral Signals AI
2. Signal CGE

Backend modules for the framework, AI chat studio, SML workbench, and learning remain in the repository. They are hidden from the public app surface so users have one clear behavioral workflow and one clear CGE simulation workflow.

## Why Two Tabs

The earlier public app exposed several overlapping CGE-related surfaces. The simplified interface reduces confusion by keeping:

- Behavioral intelligence in one tab.
- Prompt-driven CGE/SAM simulation in one tab.

Advanced modules remain available internally for development and future expansion.

## Signal CGE Prompt Flow

The Signal CGE tab accepts a natural-language simulation prompt and runs directly from the repository-stored canonical model profile by default. Uploading a SAM or experiment workbook is optional and hidden in a collapsed accordion for custom runs. The public callable is:

```python
run_signal_cge_prompt(prompt, uploaded_file=None)
```

The workflow:

1. Loads the canonical model profile from `models/canonical/signal_cge_master/model_profile.yaml`.
2. Loads the Signal CGE reference index from `Documentation/signal_cge_reference/`.
3. Parses the policy prompt into a structured scenario.
4. Detects policy instruments, targets, directions, and magnitudes.
5. Checks model readiness.
6. Runs the currently available backend.
7. Retrieves scenario-specific model references.
8. Records a lightweight learning event.
9. Produces diagnostics, summary cards, a results table, chart-ready data, structured results, policy interpretation, and downloadable files.

## Tariff Prompt Handling

Prompts such as:

```text
reduce import tariffs on cmach by 10%
```

are interpreted as:

- policy instrument: `import_tariff`
- target commodity: `cmach`
- shock direction: decrease
- shock magnitude: `10 percent`
- closure assumption: external account adjusts

## Canonical Repo Model Files

When no upload is provided, the public app uses repository-stored canonical references:

- `models/canonical/signal_cge_master/model_profile.yaml`
- `Documentation/signal_cge_reference/`
- `signal_cge/knowledge/`

The Hugging Face app does not require the local Windows model workspace.

## Current Solver Limitations

If validated static equilibrium solving is unavailable or does not pass validation for a specific run, Signal clearly reports:

```text
Validated static equilibrium solving was unavailable or did not pass validation for this run. Signal is using the available SAM multiplier/prototype backend and canonical repo model profile.
```

The current public backend is suitable for deterministic scenario parsing, SAM multiplier fallback runs, prototype calibration checks, diagnostics, and policy explanation. It should not be described as a full equilibrium CGE solver.

## Model Reference Used

Each Signal CGE run shows the canonical references used for interpretation, such as trade block, government block, price block, macro closure, experiment workflow, and the Signal CGE knowledge base.

## Future Solver Pathway

Future work can expand the validated static solver into a full recursive-dynamic solver behind the same prompt-driven public interface. The public contract should remain stable while backend readiness expands.
