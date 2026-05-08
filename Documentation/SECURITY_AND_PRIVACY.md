# Security And Privacy

Last updated: 2026-05-08

## Privacy Principle

Signal does not need to track individuals. The platform is designed for aggregate behavioral intelligence.

## What Signal Should Not Store

- usernames
- private messages
- phone numbers
- email addresses
- individual profiles
- precise individual locations
- private account data

## Aggregate-Only Philosophy

Signal should operate on:

- topic-level trends
- aggregate engagement counts
- county-level or group-level data
- synthetic development data
- anonymized feedback
- public policy and market signals

## Current Privacy Helpers

- `privacy.py`
- `src/data_pipeline/privacy_filter.py`

## Security Practices

- Store secrets in environment variables or hosted secrets.
- Do not commit API tokens.
- Keep Hugging Face and GitHub tokens outside source files.
- Avoid exposing raw API payloads in public UI.
- Use hidden components for internal diagnostic data when needed.

## Future Privacy Enhancements

- Formal PII scanning in CI.
- Data retention policy.
- Access controls for enterprise deployments.
- Audit logs.
- Differential privacy review for sensitive aggregate datasets.

