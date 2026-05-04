# Learning Memory

Signal model execution now supports a local learning loop:

```text
model runs -> errors/results/logs -> learning memory -> improved templates/rules -> better future runs
```

The learning-memory layer stores privacy-safe JSONL records containing:

- run id and timestamp
- requested backend and actual backend
- status and model name
- classified error patterns
- classified result patterns
- aggregate diagnostics
- recommended template or validation-rule improvements

It does not store raw SAM data, uploaded files, PII, usernames, phone numbers,
emails, exact GPS data, or individual-level behavioral records.

The current implementation proposes improvements rather than rewriting source
templates automatically. This keeps the modelling framework auditable.

Typical recommendations include:

- Use explicit GAMS solver choices such as PATH, CONOPT, or IPOPT.
- If GAMS is unavailable, use experimental Python mode only for validation.
- Add SAM balancing steps when row-column imbalance exceeds tolerance.
- Update SML templates when indexed symbols reference undeclared sets.
