from __future__ import annotations

import unittest

import privacy


class PrivacyTests(unittest.TestCase):
    def test_sanitize_trend_record_removes_individual_fields(self) -> None:
        record = {
            "trend_name": "#NairobiTech",
            "location": "Nairobi",
            "username": "example_user",
            "user_id": "12345",
            "profile_url": "https://x.example/profile",
        }

        sanitized = privacy.sanitize_trend_record(record)

        self.assertNotIn("username", sanitized)
        self.assertNotIn("user_id", sanitized)
        self.assertNotIn("profile_url", sanitized)
        self.assertEqual(sanitized["trend_name"], "#NairobiTech")

    def test_privacy_notice_mentions_blocked_fields(self) -> None:
        self.assertIn("usernames", privacy.PRIVACY_NOTICE)
        self.assertIn("user ids", privacy.PRIVACY_NOTICE)
        self.assertIn("private messages", privacy.PRIVACY_NOTICE)

    def test_assert_privacy_safe_records_strips_blocked_fields(self) -> None:
        records = [{"trend_name": "Food Security", "username": "hidden"}]
        safe_records = privacy.assert_privacy_safe_records(records)

        self.assertEqual(len(safe_records), 1)
        self.assertNotIn("username", safe_records[0])


if __name__ == "__main__":
    unittest.main()
