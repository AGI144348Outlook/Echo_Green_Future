"""Echo-GPT noncanonical independent ledger oracle v2 DRAFT — NOT EXECUTED.
Schema matches ledger_census_fixture_v1_DRAFT.py. No simulator imports.
This is an untested source artifact, not evidence of a passing experiment.
The independent census is passed as a separate witness; digest is checked.
"""
from collections import deque
import hashlib
import json

PHASE = {"release": 0, "expire": 1, "arrival": 2,
         "admit": 3, "open_wait": 4, "open_seat": 4}

def verify(payload, external_census):
    """Return explicit error records; fail closed on malformed input.
    external_census is immutable pre-generated (id,tick,source) triples,
    not derived from payload.events. The caller must independently source it.
    """
    errors = []
    def err(code, **details):
        errors.append(dict(code=code, **details))
    try:
        horizon = payload["ticks"]
        seats = payload["seats"]
        dwell = payload["dwell"]
        max_wait = payload["max_wait"]
        events = payload["events"]
        assert all(type(x) is int and x > 0 for x in (horizon, seats, dwell))
        assert type(max_wait) is int and max_wait >= 0
        assert isinstance(events, list)
        witness = [dict(id=i, tick=t, source=s) for i,t,s in external_census]
        raw = json.dumps(witness, sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(raw).hexdigest() != payload["census_sha256"]:
            err("census_digest_mismatch")
        if payload.get("census") != witness:
            err("census_payload_mismatch")
    except (KeyError, TypeError, ValueError, AssertionError) as ex:
        return dict(errors=[dict(code="invalid_header", detail=str(ex))])

    expected = {row["id"]: row for row in witness}
    if len(expected) != len(witness):
        err("duplicate_census_id")
    seen_arrival = set()
    waiting = deque()
    occupied = {}
    terminal = set()
    last_order = (-1, -1)
    for index, event in enumerate(events):
        try:
            kind = event["kind"]
            ident = event["id"]
            tick = event["tick"]
            assert type(ident) is int and type(tick) is int
            assert kind in PHASE
            assert 0 <= tick <= horizon
            phase = PHASE[kind]
            if tick == horizon and phase != 4:
                err("post_horizon_event", index=index)
            if (tick, phase) < last_order:
                err("phase_order", index=index)
            last_order = (tick, phase)
            if ident not in expected:
                err("phantom_id", index=index, id=ident)
            if kind == "arrival":
                if ident in seen_arrival:
                    err("duplicate_arrival", id=ident)
                seen_arrival.add(ident)
                if ident in expected and expected[ident]["tick"] != tick:
                    err("arrival_tick", id=ident)
                waiting.append(ident)
            elif kind == "admit":
                seat = event["seat"]
                if type(seat) is not int or not 0 <= seat < seats:
                    err("invalid_seat", id=ident)
                if seat in occupied:
                    err("seat_overlap", id=ident)
                if not waiting or waiting[0] != ident:
                    err("fifo", id=ident)
                if ident in waiting:
                    waiting.remove(ident)
                if ident in terminal or any(v[0] == ident for v in occupied.values()):
                    err("double_admit", id=ident)
                if ident in expected and tick - expected[ident]["tick"] > max_wait:
                    err("late_admit", id=ident)
                occupied[seat] = (ident, tick)
            elif kind == "release":
                seat = event["seat"]
                active = occupied.get(seat)
                if active is None or active[0] != ident:
                    err("invalid_release", id=ident)
                else:
                    if tick - active[1] != dwell:
                        err("dwell_mismatch", id=ident)
                    del occupied[seat]
                if ident in terminal:
                    err("double_terminal", id=ident)
                terminal.add(ident)
            elif kind == "expire":
                if ident not in waiting:
                    err("invalid_expire", id=ident)
                else:
                    waiting.remove(ident)
                if ident in expected and tick - expected[ident]["tick"] <= max_wait:
                    err("early_expire", id=ident)
                if ident in terminal:
                    err("double_terminal", id=ident)
                terminal.add(ident)
            elif kind == "open_wait":
                if tick != horizon or ident not in waiting:
                    err("invalid_open_wait", id=ident)
                elif ident in waiting:
                    waiting.remove(ident)
                if ident in terminal:
                    err("double_terminal", id=ident)
                terminal.add(ident)
            elif kind == "open_seat":
                seat = event["seat"]
                active = occupied.get(seat)
                if tick != horizon or active is None or active[0] != ident:
                    err("invalid_open_seat", id=ident)
                else:
                    if event.get("planned_release") != active[1] + dwell:
                        err("planned_release_mismatch", id=ident)
                    del occupied[seat]
                if ident in terminal:
                    err("double_terminal", id=ident)
                terminal.add(ident)
        except (KeyError, TypeError, ValueError, AssertionError) as ex:
            err("malformed_event", index=index, detail=str(ex))
    missing = set(expected) - seen_arrival
    if missing:
        err("missing_arrivals", count=len(missing), sample=sorted(missing)[:10])
    unclosed = set(expected) - terminal
    if unclosed:
        err("missing_terminal", count=len(unclosed), sample=sorted(unclosed)[:10])
    if waiting:
        err("unfinalized_waiting", count=len(waiting))
    if occupied:
        err("unfinalized_seats", count=len(occupied))
    return dict(errors=errors, census_count=len(expected), event_count=len(events))

if __name__ == "__main__":
    raise SystemExit("DRAFT ONLY: no tests without prospective GitHub registration")
