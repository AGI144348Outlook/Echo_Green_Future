import unittest
from datetime import datetime, timedelta, timezone

from schedule_gate import decide, parse_schedule


class ScheduleGateTests(unittest.TestCase):
    def test_parse_comments_and_interval(self):
        s = parse_schedule("# note\ntimezone: UTC\nevery 6 hours\n")
        self.assertEqual((s.kind, s.hours), ("every", 6))

    def test_rejects_multiple_rules(self):
        with self.assertRaises(ValueError):
            parse_schedule("daily\noff")

    def test_rejects_unknown_timezone(self):
        with self.assertRaises(ValueError):
            parse_schedule("timezone: Mars/Olympus\ndaily at 4")

    def test_interval_grace_boundary(self):
        s = parse_schedule("every 2 hours")
        last = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.assertFalse(decide(s, now=last + timedelta(hours=1, minutes=49), last_started=last).due)
        self.assertTrue(decide(s, now=last + timedelta(hours=1, minutes=50), last_started=last).due)

    def test_future_last_run_fails_closed(self):
        s = parse_schedule("every 1 hour")
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.assertFalse(decide(s, now=now, last_started=now + timedelta(seconds=1)).due)

    def test_naive_datetime_rejected(self):
        with self.assertRaises(ValueError):
            decide(parse_schedule("daily"), now=datetime(2026, 1, 1), last_started=None)

    def test_daily_slot_once(self):
        s = parse_schedule("timezone: America/Chicago\ndaily at 8")
        now = datetime(2026, 6, 1, 14, tzinfo=timezone.utc)
        before = datetime(2026, 5, 31, 14, tzinfo=timezone.utc)
        after = datetime(2026, 6, 1, 13, 30, tzinfo=timezone.utc)
        self.assertTrue(decide(s, now=now, last_started=before).due)
        self.assertFalse(decide(s, now=now, last_started=after).due)

    def test_weekly_slot(self):
        s = parse_schedule("timezone: UTC\nweekly on monday at 9")
        now = datetime(2026, 10, 8, 12, tzinfo=timezone.utc)
        self.assertTrue(decide(s, now=now, last_started=datetime(2026, 10, 4, tzinfo=timezone.utc)).due)

    def test_dst_fall_back_uses_absolute_slot(self):
        s = parse_schedule("timezone: America/Chicago\ndaily at 8")
        now = datetime(2026, 11, 1, 15, tzinfo=timezone.utc)
        d = decide(s, now=now, last_started=datetime(2026, 10, 31, 15, tzinfo=timezone.utc))
        self.assertTrue(d.due)
        self.assertEqual(d.slot_utc, datetime(2026, 11, 1, 14, tzinfo=timezone.utc))


if __name__ == "__main__":
    unittest.main()
