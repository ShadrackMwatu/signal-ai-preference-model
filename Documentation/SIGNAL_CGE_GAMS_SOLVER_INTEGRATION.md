# Signal CGE Optional GAMS Solver Integration

Signal CGE recognizes GAMS as an optional solver backend for local environments. GAMS is not required for Hugging Face startup and is not required for the open-source Python solvers.

## Optional Local Use

If GAMS is installed locally and available through `PATH` or `GAMS_PATH`, Signal can detect the executable and report the backend as available. Execution still requires repo-safe model files and a valid local runtime/license.

## Hosted Runtime Behavior

On hosted deployments, GAMS is usually unavailable. In that case Signal reports:

```text
GAMS solver backend is configured but not available in this runtime. Signal is using the open-source/Python backend.
```

The app then continues with the validated static equilibrium solver, open-source prototype solver, or SAM multiplier fallback.

## Detection

Signal checks:

1. `GAMS_PATH` environment variable.
2. `gams` or `gams.exe` on `PATH`.

The status payload can be:

- `available`
- `unavailable`
- `installed_but_unlicensed`
- `execution_failed`

## Runtime Output Policy

Temporary solver outputs must stay in ignored runtime folders. GAMS execution may produce `.gdx`, `.g00`, `.lst`, `.log`, `.pf`, and temporary files. These must not be committed.

## Files That Must Never Be Committed

- GAMS license files
- `gamslice.txt`
- `gamslice.dat`
- installer files
- local shortcuts
- private local paths
- generated `.gdx`, `.g00`, `.lst`, `.log`, `.pf`, `.tmp`, or `.bak` files

## Configuration

To configure a local runtime, set:

```text
GAMS_PATH=C:/path/to/gams
```

This can point to either the GAMS executable or a folder containing the executable.
