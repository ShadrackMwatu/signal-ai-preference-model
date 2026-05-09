# Signal Local Model Workspace

Signal separates the local persistent model workspace from the synchronized GitHub repository.

## Local Workspace Role

The local workspace is:

```text
C:/Users/smwatu/OneDrive - Kenya Institute for Public Policy Research and Analysis/Documents/Signal/models/Model
```

It is the persistent canonical workspace for large model files, solver runtime outputs, checkpoints, archives, local SAM storage, and experiment runs.

Expected structure:

```text
models/Model/
  canonical/
  calibration/
  closures/
  experiments/
  scenarios/
  sam/
  outputs/
  checkpoints/
  archives/
  runtime/
```

## GitHub Role

GitHub remains the canonical synchronized repository for:

- source code
- tests
- documentation
- model architecture
- equation references
- calibration logic
- templates
- YAML configuration
- lightweight reference data

The synchronized repository should not contain large runtime solver artifacts.

## Synchronization Policy

The policy is stored in:

```text
signal_cge/config/sync_policy.yaml
```

Files that may sync include source code, templates, YAML configs, docs, equations, calibration logic, and lightweight reference data.

Files that should not sync include `.gdx`, `.g00`, `.lst`, `.log`, `.tmp`, `.bak`, large outputs, runtime checkpoints, temporary solver artifacts, cached runs, logs, archives, and runtime folders.

## Runtime Artifact Handling

Runtime artifacts stay local under:

- `models/Model/outputs/`
- `models/Model/checkpoints/`
- `models/Model/archives/`
- `models/Model/runtime/`

The repository `.gitignore` protects these files from accidental commits. Signal code should read metadata and paths by default rather than loading large binary artifacts.

## Hugging Face Limitations

Hugging Face deployment uses the lightweight repository layer. It should not depend on the local Windows path, large local model files, GAMS runtime outputs, or checkpoint artifacts. If local paths are unavailable in deployment, the app should continue using lightweight docs, configs, tests, and Python fallback logic.

## AI Access Layer

AI CGE Chat Studio, policy AI, and learning modules can reference:

- `signal_cge/config/local_model_paths.yaml`
- `signal_cge/config/sync_policy.yaml`
- `signal_cge/local_workspace/`
- `models/canonical/`
- `Documentation/signal_cge_reference/`

They should not load `.gdx`, `.g00`, solver logs, checkpoints, or runtime outputs unless a user explicitly asks for a local diagnostic workflow.

## Future Cloud Synchronization

Future cloud synchronization can add a reviewed artifact store for selected model outputs. Any cloud sync should keep the same rule: source and lightweight references sync by default; runtime artifacts sync only through explicit reviewed export workflows.
