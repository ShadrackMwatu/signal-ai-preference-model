# Signal Learning

Signal Learning extends the CGE workflow so it learns from model files, SAM
structures, GAMS logs, solver outcomes, validation errors, scenario results, and
user corrections.

The core workflow is:

```text
Observe -> Diagnose -> Store -> Recommend -> Validate -> Implement -> Re-test -> Remember
```

Default mode: `recommend`.

Modes:

- `observe_only`: records lessons but changes nothing.
- `recommend`: records lessons and recommends improvements.
- `safe_apply`: applies low-risk fixes only as versioned adapted templates.

Every learned rule must link to evidence:

- source run
- observed error/result
- correction made
- validation status

Signal never silently overwrites core templates. Adaptations are versioned under
`learning_versions/`.
