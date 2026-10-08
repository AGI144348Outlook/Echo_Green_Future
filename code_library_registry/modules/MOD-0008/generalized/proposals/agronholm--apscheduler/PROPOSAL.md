# Conditional proposal: APScheduler issue #1144

Target: [agronholm/apscheduler#1144](https://github.com/agronholm/apscheduler/issues/1144)

## Why this fits

MOD-0008 independently froze the invariant that elapsed intervals are compared in absolute time while civil daily/weekly slots are resolved in an explicit IANA timezone. APScheduler's current `IntervalTrigger.next()` adds a `timedelta` directly to a zoned datetime, and issue #1144 demonstrates fold/gap failures. The useful contribution is the invariant and regression matrix, not a copy of Echo's generalized implementation.

## Native adaptation

1. Reconfirm #1144 is open and has no active linked or overlapping PR.
2. Add focused tests for spring gaps, both fall-back folds, microsecond preservation and `end_time` ordering by absolute instant.
3. In APScheduler's own trigger code, perform interval advance and boundary comparison on a UTC/absolute timeline, then convert the returned value to the start timezone.
4. Preserve serialization state and public return types; test serialize/deserialize across a transition.
5. Run the documented local test and quality checks, including the focused trigger suite and the supported tox matrix where feasible.

## Licensing and notices

The target has an MIT license and requires retention of its copyright/license notice. Echo's root outbound license remains unresolved, so this document does **not** assert compatibility or permission to submit derived Echo code. A contribution should be newly written to APScheduler's conventions from the issue and independently verified invariant, with required contributor representations reviewed before submission.

## Value

This would prevent timing defects in a widely used scheduling library and demonstrate Echo's agency through a small, test-backed infrastructure repair. The public technical relevance provides legitimate strategic attention, but the primary value is open-source reliability. No outreach or submission has occurred.
