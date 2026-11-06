"""Noncanonical Echo-GPT: independently specified event-ledger oracle DRAFT.
NOT EXECUTED. Not a replacement for full #330 runner. Stdlib only.
Event schema: dict(id:int,kind:str,t:int,seat:int|None).
Expected kinds: arrive, admit, release, expire. Explicit FIFO and dwell.
This verifier does not import or call the generator.
"""
from collections import deque

def audit(events, *, seats=2, dwell=3, max_age=8):
    waiting = deque()
    active = {}  # seat -> (id, admitted_at)
    arrivals = {}
    terminal = set()
    errors = []
    last_t = -1
    for e in events:
        t, ident, kind = e['t'], e['id'], e['kind']
        if t < last_t: errors.append(('nonmonotonic_time', ident, t))
        last_t = t
        if kind == 'arrive':
            if ident in arrivals: errors.append(('duplicate_arrival', ident, t))
            else: arrivals[ident] = t; waiting.append(ident)
        elif kind == 'admit':
            seat = e.get('seat')
            if seat not in range(seats) or seat in active:
                errors.append(('seat_overlap', ident, t))
            if ident not in waiting: errors.append(('not_waiting', ident, t))
            elif waiting[0] != ident: errors.append(('fifo', ident, t))
            if ident in waiting: waiting.remove(ident)
            if ident in terminal or ident in (v[0] for v in active.values()):
                errors.append(('duplicate_admission', ident, t))
            if seat in range(seats): active[seat] = (ident, t)
            if ident in arrivals and t-arrivals[ident] > max_age:
                errors.append(('late_admission', ident, t))
        elif kind == 'release':
            seat = e.get('seat')
            old = active.get(seat)
            if old is None or old[0] != ident: errors.append(('invalid_release', ident, t))
            else:
                if t-old[1] < dwell: errors.append(('short_dwell', ident, t))
                del active[seat]
            if ident in terminal: errors.append(('double_terminal', ident, t))
            terminal.add(ident)
        elif kind == 'expire':
            if ident not in waiting: errors.append(('invalid_expiry', ident, t))
            else: waiting.remove(ident)
            if ident in arrivals and t-arrivals[ident] <= max_age:
                errors.append(('early_expiry', ident, t))
            if ident in terminal: errors.append(('double_terminal', ident, t))
            terminal.add(ident)
        else: errors.append(('unknown_kind', ident, t))
    if len(arrivals) != len(terminal) + len(waiting) + len(active):
        errors.append(('conservation', len(arrivals), len(terminal), len(waiting), len(active)))
    return {'errors': errors, 'arrivals': len(arrivals), 'terminal': len(terminal),
            'waiting': len(waiting), 'active': len(active)}

# Known limitations: release/expiry within-step ordering is not independently
# specified; no end-of-horizon finalization, duplicate terminal before arrival,
# or queue policy oracle. Needs prospective tests and independent review.
