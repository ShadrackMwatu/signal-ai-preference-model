# Signal AI CGE Chat Studio

The AI CGE Chat Studio is a deterministic, local chat layer for the Signal CGE Workbench. It accepts a natural-language policy question, compiles it into a structured scenario, runs economic reasoning checks, executes the existing Python SAM multiplier fallback, explains the policy mechanism, and recommends next simulations.

The studio does not require API keys, paid services, GAMS, or Pyomo. It does not replace the model. It assists with scenario setup, diagnostics, explanation, memory, and policy summarization.

## How to Use

Open the Hugging Face Gradio app and select **AI CGE Chat Studio**. Enter a policy question such as:

- `double care infrastructure`
- `increase government spending on care services by 10 percent`
- `simulate VAT increase`
- `run infrastructure investment shock`
- `compare unpaid care and paid care scenarios`

Optionally upload a SAM CSV/XLSX. Click **Run chat simulation**.

## Outputs

The tab returns a structured scenario JSON object, diagnostics and warnings, result summaries, a policy explanation, and recommended next simulations.

## Important Limitation

The current execution path uses a Python SAM multiplier fallback unless a full CGE backend is configured. SAM multipliers are fixed-price linear simulations and should be interpreted as screening results, not full equilibrium CGE findings.
