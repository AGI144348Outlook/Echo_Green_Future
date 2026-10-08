# Applications

The module separates schedule parsing and due/not-due decisions from file I/O, sleeping, network calls and job execution.

Potential applications:

- an hourly CI wake-up that must run a job only once per local daily or weekly slot;
- dataset refresh, backup, cache-expiry or report-generation gates;
- deterministic schedule previews in a UI;
- replay tests across time zones and daylight-saving transitions.

Non-applications and limits:

- It is not a durable scheduler, lock service or distributed lease. Two workers can both decide “due.”
- It does not persist completion state or retry failed work.
- It supports hour-level interval/daily/weekly syntax only.
- “Daily” without `at` remains a rolling 24-hour interval; this is deliberately distinct from a civil-time daily slot.
- A caller must provide timezone-aware timestamps and atomically persist/lock job state where concurrency matters.

The current Echo crawler is a concrete prospective consumer. MOD-0003 can hold persisted run metadata, while MOD-0001 can gate required state before this decision is evaluated; neither combination itself supplies a distributed lock.
