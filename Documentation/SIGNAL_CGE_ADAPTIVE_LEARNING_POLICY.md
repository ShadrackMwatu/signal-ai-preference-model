# Signal CGE Adaptive Learning Policy

Signal CGE may learn from prompts, interpreted scenarios, diagnostics, results, policy interpretations, caveats, and recommended follow-up simulations.

## Allowed

- Record lightweight simulation metadata.
- Summarize common scenario types and target accounts.
- Track repeated warnings and backend limitations.
- Improve deterministic prompt interpretation rules.
- Improve policy caveats and recommended next simulations.
- Propose model improvements for developer review.

## Not Allowed Automatically

Signal must not automatically modify:

- core equations
- calibration formulas
- closure rules
- solver logic
- canonical SAM data
- uploaded user data

Any change to model equations, calibration, closures, or solvers requires explicit developer review and normal Git workflow.

## Runtime Logs

Runtime learning logs are ignored from Git by default:

```text
outputs/signal_cge_learning/simulation_memory.jsonl
```

Signal stores metadata and summaries only. It must not store full uploaded SAMs, large binaries, or sensitive user data.

## Approved Improvements

Approved improvements should be implemented as ordinary code or documentation changes, tested, committed, and reviewed through the repository workflow.
