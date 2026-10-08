"""Preserved schedule-decision excerpt from Datasets/crawler/crawl.py.

Source commit: 75c3056c840f09582244b44a72e43de18e163ef3
Source blob: baf1d65878490f0280d4278123cd7668dd3a803d
Copyright and license: no file-local notice observed. Repository-level licensing is
unresolved; preservation here is for provenance and analysis, not a license grant.
"""
import os
import re
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def read_schedule():
    """Parse schedule.txt -> (rule dict, timezone). Raises ValueError on anything unclear."""
    tz_name, rule = "UTC", None
    for line in open(os.path.join(HERE, "schedule.txt"), encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.lower().startswith("timezone:"):
            tz_name = line.split(":", 1)[1].strip()
            continue
        line = line.lower()
        if rule is not None:
            raise ValueError("schedule.txt has more than one schedule line")
        if line == "off":
            rule = {"kind": "off"}
        elif re.fullmatch(r"every (\d+) hours?", line):
            n = int(line.split()[1])
            if not 1 <= n <= 168:
                raise ValueError("'every N hours' needs N from 1 to 168")
            rule = {"kind": "every", "hours": n}
        elif line == "daily":
            rule = {"kind": "every", "hours": 24}
        elif re.fullmatch(r"daily at (\d{1,2})", line):
            h = int(line.split()[-1])
            if h > 23:
                raise ValueError("hour must be 0-23")
            rule = {"kind": "daily", "hour": h}
        elif re.fullmatch(r"weekly on (\w+)(?: at (\d{1,2}))?", line):
            m = re.fullmatch(r"weekly on (\w+)(?: at (\d{1,2}))?", line)
            if m.group(1) not in DAYS:
                raise ValueError(f"unknown day '{m.group(1)}'")
            h = int(m.group(2) or 0)
            if h > 23:
                raise ValueError("hour must be 0-23")
            rule = {"kind": "weekly", "day": DAYS.index(m.group(1)), "hour": h}
        else:
            raise ValueError(f"could not read schedule line: '{line}'")
    if rule is None:
        raise ValueError("schedule.txt has no schedule line")
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(tz_name)
    except Exception:
        raise ValueError(f"unknown timezone '{tz_name}' (use a name like America/Chicago)")
    return rule, tz


def is_due(rule, tz, last_started, now=None):
    """Return (due, reason)."""
    now = now or datetime.now(timezone.utc)
    if rule["kind"] == "off":
        return False, "schedule is off"
    if last_started is None:
        return True, "no previous run"
    last = datetime.fromisoformat(last_started)
    grace = 10 * 60
    if rule["kind"] == "every":
        gap = (now - last).total_seconds()
        due = gap >= rule["hours"] * 3600 - grace
        return due, f"last run {gap / 3600:.1f} h ago; interval {rule['hours']} h"
    local_now, local_last = now.astimezone(tz), last.astimezone(tz)
    if rule["kind"] == "daily":
        due = local_now.hour >= rule["hour"] and local_last.date() < local_now.date()
        return due, f"daily at {rule['hour']}:00 {tz}; last run {local_last:%Y-%m-%d %H:%M}"
    if rule["kind"] == "weekly":
        this_week_slot = (local_now - timedelta(days=(local_now.weekday() - rule["day"]) % 7)).replace(
            hour=rule["hour"], minute=0, second=0, microsecond=0
        )
        if this_week_slot > local_now:
            this_week_slot -= timedelta(days=7)
        due = local_last < this_week_slot <= local_now
        return due, f"weekly on {DAYS[rule['day']]} at {rule['hour']}:00 {tz}; last run {local_last:%Y-%m-%d %H:%M}"
    return False, "unknown rule"
