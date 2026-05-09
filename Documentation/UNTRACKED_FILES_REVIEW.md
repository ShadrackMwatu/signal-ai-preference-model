# Untracked Files Review

Review date: 2026-05-09

## Commands Run

```bash
git status --short
git ls-files --others --exclude-standard
```

## Summary

The untracked inventory contained one local Docker Desktop installer and generated model-version folders under `models/versions/v2` through `models/versions/v28`. Each generated model-version folder contains one `metadata.json` file and one `model.pkl` file. The already tracked `models/versions/v1/` folder was inspected for context but was not part of the untracked set.

No API keys, tokens, passwords, `.env` files, or credentials were found by text scan. However, generated metadata files contain local machine paths such as `C:\Users\...`, `OneDrive`, `artifact_path`, and `data_path`, so they should not be committed as-is.

Git LFS is configured only for Excel workbook formats (`*.xlsx`, `*.xlsm`). It is not currently configured for `.pkl` model artifacts.

## Inventory and Classification

| Item reviewed | Size / type | Classification | Reason | Action taken |
|---|---:|---|---|---|
| `docker/Docker Desktop Installer.exe` | 647,543,728 bytes, `.exe` | E. Large files that should not be committed directly | Local third-party installer binary; not source code or deployable app configuration. Too large for normal Git. | Ignored with `docker/*.exe`; left on disk. |
| `models/versions/v2/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F. Model artifact, generated runtime output, contains private local paths in metadata | Generated training version artifact. `model.pkl` is binary; `metadata.json` records local scratch paths. | Ignored with `models/versions/v*/`; left on disk. |
| `models/versions/v3/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v4/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v5/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v6/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v7/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v8/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v9/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v10/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v11/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v12/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v13/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v14/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v15/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v16/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v17/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v18/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v19/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v20/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v21/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v22/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v23/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v24/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v25/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v26/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v27/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |
| `models/versions/v28/` | 2 files, ~1.51 MB, `.json` + `.pkl` | C/D/F | Generated model artifact; metadata includes local paths. | Ignored; left on disk. |

## Extension and Size Summary

| Extension | Count | Total size | Assessment |
|---|---:|---:|---|
| `.exe` | 1 | 647,543,728 bytes | Local installer binary; do not commit. |
| `.pkl` | 28 inspected, 27 untracked | 44,662,951 bytes inspected | Binary model artifacts. Use Git LFS only if a model-version retention policy is adopted. |
| `.json` | 28 inspected, 27 untracked | 32,414 bytes inspected | Generated metadata; contains local paths and should be regenerated or sanitized before tracking. |

## Sensitive Content Check

Text scan patterns included API keys, tokens, passwords, secrets, bearer tokens, credentials, licenses, private paths, `.env`, `artifact_path`, and `data_path`.

Findings:

- No API keys, tokens, passwords, `.env` files, or credential files were detected.
- `models/versions/*/metadata.json` contains local private filesystem paths and generated scratch-data paths.
- `docker/Docker Desktop Installer.exe` is a binary installer and was not text-inspected for embedded content.

## Git LFS Recommendation

Do not commit the current untracked model-version artifacts directly. If historical model versions are required later, configure Git LFS for model binaries first, for example:

```bash
git lfs track "*.pkl"
git add .gitattributes
```

Before tracking metadata, sanitize `artifact_path` and `data_path` so local user and organization paths are not committed.

## Actions Taken

- Added `.gitignore` rule: `docker/*.exe`
- Added `.gitignore` rule: `models/versions/v*/`
- Created this review report.
- Did not remove any local files from disk.
- Did not stage model artifacts, installer binaries, generated outputs, caches, or metadata containing local paths.
