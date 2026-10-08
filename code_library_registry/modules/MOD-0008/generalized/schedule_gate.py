"""Pure parser and decision gate for interval, daily and weekly schedules."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


@dataclass(frozen=True)
class Schedule:
    kind: str
    timezone_name: str = "UTC"
    hours: int | None = None
    hour: int | None = None
    weekday: int | None = None


@dataclass(frozen=True)
class Decision:
    due: bool
    reason: str
    slot_utc: datetime | None = None


def parse_schedule(text: str) -> Schedule:
    """Parse exactly one rule plus at most one `timezone:` declaration."""
    timezone_name = "UTC"
    rule: tuple[str, int | None, int | None] | None = None
    timezone_seen = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.lower().startswith("timezone:"):
            if timezone_seen:
                raise ValueError("schedule has more than one timezone declaration")
            timezone_name = line.split(":", 1)[1].strip()
            if not timezone_name:
                raise ValueError("timezone declaration is empty")
            timezone_seen = True
            continue
        if rule is not None:
            raise ValueError("schedule has more than one rule")
        normalized = line.lower()
        if normalized == "off":
            rule = ("off", None, None)
        elif normalized == "daily":
            rule = ("every", 24, None)
        elif (match := re.fullmatch(r"every (\d+) hours?", normalized)):
            hours = int(match.group(1))
            if not 1 <= hours <= 168:
                raise ValueError("interval must be between 1 and 168 hours")
            rule = ("every", hours, None)
        elif (match := re.fullmatch(r"daily at (\d{1,2})", normalized)):
            hour = int(match.group(1))
            if hour > 23:
                raise ValueError("hour must be between 0 and 23")
            rule = ("daily", hour, None)
        elif (match := re.fullmatch(r"weekly on (\w+)(?: at (\d{1,2}))?", normalized)):
            day = match.group(1)
            if day not in DAYS:
                raise ValueError(f"unknown weekday: {day}")
            hour = int(match.group(2) or 0)
            if hour > 23:
                raise ValueError("hour must be between 0 and 23")
            rule = ("weekly", hour, DAYS.index(day))
        else:
            raise ValueError(f"unrecognized schedule line: {line}")
    if rule is None:
        raise ValueError("schedule has no rule")
    try:
        ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown timezone: {timezone_name}") from exc
    kind, value, weekday = rule
    return Schedule(kind, timezone_name, value if kind == "every" else None,
                    value if kind in {"daily", "weekly"} else None, weekday)


def _aware(value: datetime, label: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware")
    return value


def decide(schedule: Schedule, *, now: datetime, last_started: datetime | None,
           grace: timedelta = timedelta(minutes=10)) -> Decision:
    """Return a deterministic due/not-due decision without I/O or sleeping."""
    now = _aware(now, "now")
    if grace < timedelta(0):
        raise ValueError("grace must not be negative")
    if schedule.kind == "off":
        return Decision(False, "schedule is off")
    if last_started is None:
        return Decision(True, "no previous run")
    last_started = _aware(last_started, "last_started")
    if last_started > now:
        return Decision(False, "last run is in the future")
    if schedule.kind == "every":
        threshold = timedelta(hours=schedule.hours or 0) - grace
        due = now - last_started >= threshold
        return Decision(due, "interval reached" if due else "interval not reached")
    tz = ZoneInfo(schedule.timezone_name)
    local_now = now.astimezone(tz)
    local_last = last_started.astimezone(tz)
    if schedule.kind == "daily":
        slot = local_now.replace(hour=schedule.hour or 0, minute=0, second=0, microsecond=0)
        if slot > local_now:
            slot -= timedelta(days=1)
    elif schedule.kind == "weekly":
        slot = (local_now - timedelta(days=(local_now.weekday() - (schedule.weekday or 0)) % 7)).replace(
            hour=schedule.hour or 0, minute=0, second=0, microsecond=0
        )
        if slot > local_now:
            slot -= timedelta(days=7)
    else:
        raise ValueError(f"unsupported schedule kind: {schedule.kind}")
    slot_utc = slot.astimezone(timezone.utc)
    due = last_started.astimezone(timezone.utc) < slot_utc <= now.astimezone(timezone.utc)
    return Decision(due, "scheduled slot is unconsumed" if due else "scheduled slot already consumed", slot_utc)
