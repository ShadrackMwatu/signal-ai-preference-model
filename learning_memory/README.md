# Learning Memory

Signal learning memory implements the loop:

```text
model runs -> errors/results/logs -> learning memory -> improved templates/rules -> better future runs
```

The memory is local, append-only JSONL. It stores aggregate run metadata,
diagnostic categories, result patterns, and rule recommendations. It does not
store SAM cells, uploaded files, usernames, emails, phone numbers, exact GPS, or
individual-level behavioral data.

The system does not silently rewrite source code. It proposes safer template and
validation rules that can be reviewed before becoming production defaults.
