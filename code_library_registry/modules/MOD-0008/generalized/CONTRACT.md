# Contract

`parse_schedule(text)` accepts comments, one optional IANA timezone declaration and exactly one rule: `off`, `every N hours`, `daily`, `daily at H`, or `weekly on DAY [at H]`. Invalid, ambiguous or unsupported input raises `ValueError`.

`decide(schedule, now=..., last_started=..., grace=...)` is pure and deterministic. Inputs must be timezone-aware. It returns `Decision(due, reason, slot_utc)` and never performs I/O. A future `last_started`, a negative grace, naive datetimes or unsupported rule kind fail closed or raise explicitly.

Assumptions: the caller owns durable state, mutual exclusion, execution, retries and clock quality. The supplied `last_started` represents a consumed start, not a successful completion.
