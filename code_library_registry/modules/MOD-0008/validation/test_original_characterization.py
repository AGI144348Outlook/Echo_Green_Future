import importlib.util
import pathlib
import unittest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

SOURCE = pathlib.Path(__file__).parents[1] / "original" / "schedule_excerpt.py"
spec = importlib.util.spec_from_file_location("original_schedule", SOURCE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class OriginalCharacterizationTests(unittest.TestCase):
    def test_first_run_is_due(self):
        self.assertTrue(module.is_due({"kind": "every", "hours": 1}, ZoneInfo("UTC"), None)[0])

    def test_daily_slot_runs_once_per_date_after_hour(self):
        rule = {"kind": "daily", "hour": 8}
        now = datetime(2026, 10, 8, 14, tzinfo=timezone.utc)
        self.assertTrue(module.is_due(rule, ZoneInfo("America/Chicago"), "2026-10-07T14:00:00+00:00", now)[0])
        self.assertFalse(module.is_due(rule, ZoneInfo("America/Chicago"), "2026-10-08T13:30:00+00:00", now)[0])

    def test_unknown_rule_is_not_due(self):
        self.assertFalse(module.is_due({"kind": "unsupported"}, ZoneInfo("UTC"), "2026-10-07T00:00:00+00:00")[0])


if __name__ == "__main__":
    unittest.main()
