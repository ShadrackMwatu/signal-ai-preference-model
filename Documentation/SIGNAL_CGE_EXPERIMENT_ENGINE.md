# Signal CGE Experiment Engine

The experiment engine converts policy prompts into structured shocks and solver-ready payloads.

## Workflow

1. Read the policy prompt.
2. Identify experiment type, instrument, target account, direction, and magnitude.
3. Produce prototype directional indicators for the active fallback backend.
4. Prepare the future full-equilibrium payload with target equation blocks and instrument variables.
5. Collect macro, trade, government, welfare, factor, and household result summaries.

For an import tariff shock, the engine identifies the target commodity, tariff instrument, shock direction, and future equation blocks covering imports, prices, government balance, and the external balance.
