"""Account mapping helpers for Signal CGE."""

from __future__ import annotations


def normalize_account_name(account: object) -> str:
    """Normalize account labels for mapping and comparison."""

    return str(account).strip().lower().replace(" ", "_").replace("-", "_")


def apply_account_map(accounts: list[str], account_map: dict[str, str] | None = None) -> dict[str, str]:
    """Return normalized account-to-group mappings with optional overrides."""

    mapping = account_map or {}
    return {account: mapping.get(account, mapping.get(normalize_account_name(account), "unknown")) for account in accounts}
