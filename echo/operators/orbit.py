"""A-177 part 1: Orbit tracer, the `%` spin made measurable.

Apply an operation repeatedly until a state repeats. On anything finite this
always happens (there are only so many states), so recursive inversion ends in a
cycle. A fixed point is a cycle of length 1; an involution pairs things into
cycles of length 2. The cycle length (period) is an invariant of the operation.
"""
from math import gcd


def orbit(x, f, max_steps=10000, key=repr):
    """Trace x, f(x), f(f(x))... Returns tail (states before the cycle) and the cycle."""
    seen, states = {}, []
    cur = x
    for step in range(max_steps + 1):
        k = key(cur)
        if k in seen:
            start = seen[k]
            cycle = states[start:]
            return {"tail": states[:start], "cycle": cycle, "cycle_length": len(cycle),
                    "fixed_point": len(cycle) == 1, "returns_to_start": start == 0, "halted": None}
        seen[k] = step
        states.append(cur)
        nxt = f(cur)
        if nxt is None:  # the operation has no image here: the trace halts
            return {"tail": states, "cycle": [], "cycle_length": 0, "fixed_point": False,
                    "returns_to_start": False, "halted": "no image for " + repr(cur)}
        cur = nxt
    return {"tail": states, "cycle": [], "cycle_length": None, "fixed_point": False,
            "returns_to_start": False, "halted": "no repeat within max_steps"}


def is_involution(f, domain, key=repr):
    return all(key(f(f(x))) == key(x) for x in domain)


def period(f, domain, key=repr):
    """Least n > 0 with f^n = identity on domain (bijections only): lcm of cycle lengths."""
    p = 1
    for x in domain:
        o = orbit(x, f, key=key)
        if not o["returns_to_start"]:
            return None
        p = p * o["cycle_length"] // gcd(p, o["cycle_length"])
    return p


def as_two_involutions(perm):
    """Factor a permutation (dict x -> perm[x]) as r2 . r1 with r1, r2 involutions.

    Each cycle (c0 c1 ... c_{k-1}) is a rotation, and every rotation is two
    reflections: r1(c_i) = c_{-i}, r2(c_i) = c_{1-i}, so r2(r1(c_i)) = c_{i+1}.
    """
    r1, r2, done = {}, {}, set()
    for start in perm:
        if start in done:
            continue
        cyc, cur = [], start
        while cur not in done:
            done.add(cur); cyc.append(cur); cur = perm[cur]
        k = len(cyc)
        for i, c in enumerate(cyc):
            r1[c] = cyc[(-i) % k]
            r2[c] = cyc[(1 - i) % k]
    return r1, r2


def spin(f, domain):
    """Signed cardinality of a transformation over an ordered domain.

    rotation  every element moves the same number of places around the cycle: +k (forward)
              or -k (backward), with period n / gcd(n, k)
    half-turn step n/2: forward and backward coincide, so it has no direction
    reflection an involution that is not a rotation (Atbash): flips, no direction
    identity  step 0
    mixed     none of these (parts move by different amounts)
    """
    n = len(domain)
    pos = {x: i for i, x in enumerate(domain)}
    steps = {(pos[f(x)] - pos[x]) % n for x in domain}
    if len(steps) == 1:
        k = steps.pop()
        if k == 0: return {"kind": "identity", "signed_step": 0, "period": 1}
        signed = k if k < n / 2 else (k - n if k > n / 2 else k)
        per = n // gcd(n, k)
        if k * 2 == n: return {"kind": "half-turn (no direction)", "signed_step": k, "period": per}
        return {"kind": "rotation", "direction": "forward" if signed > 0 else "backward", "signed_step": signed, "period": per}
    if all(f(f(x)) == x for x in domain):
        return {"kind": "reflection (no direction)", "period": 2}
    return {"kind": "mixed", "period": period(f, domain)}
