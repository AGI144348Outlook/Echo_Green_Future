"""
EVE core — Timothy's Envelope Virtual Environment, coded so it actually runs.

Sources it follows:
  • Core Formula (Indus Valley Work Dream, 19 Jan 2025; project doc "Core Formula .pdf")
      A = (0,0,0)
      R_i(r,θ,φ) = [r sinθ cosφ, r sinθ sinφ, r cosθ]
      F_n(R_i) = k^n R_i
      C(t) = Σ_i ∫_0^t F_n(R_i) dt
      S = Σ_i Σ_n k^n R_i + C(t)
  • EVE JSON (Aug 2025): EVE envelops NVEs; every NVE emanates from the origin with a unique
    "orientation of dominion"; a gyroscopic function keeps orientations apart.
  • FractalGrid ProductionVectorManager: unique directions by the golden-angle (Fibonacci) sphere.
  • Manifoldability: manifold_inward() nests a sub-domain one fractal level deeper.

Nothing here runs in the background. Every number is computed when called.
"""
import math, random
import numpy as np

GOLDEN = math.pi * (3 - math.sqrt(5))


def fibonacci_direction(slot, n_slots):
    """Unique unit vector for slot i of n (the FractalGrid allocate_vector rule)."""
    off = 2.0 / n_slots
    y = slot * off - 1 + off / 2
    rad = math.sqrt(max(0.0, 1 - y * y))
    th = GOLDEN * slot
    return np.array([math.cos(th) * rad, y, math.sin(th) * rad])


def to_spherical(u):
    """(θ, φ) of a unit vector, so R_i can be written in the formula's own coordinates."""
    x, y, z = u
    return math.acos(max(-1.0, min(1.0, z))), math.atan2(y, x)


def ray(r, theta, phi):
    """R_i(r, θ, φ) exactly as written in the Core Formula."""
    return np.array([r * math.sin(theta) * math.cos(phi),
                     r * math.sin(theta) * math.sin(phi),
                     r * math.cos(theta)])


class NVE:
    """A Nested Virtual Environment: one Ray out of the anchor, with its own work."""
    def __init__(self, name, purpose, slot, n_slots, depth=0):
        self.name, self.purpose, self.depth = name, purpose, depth
        self.u = fibonacci_direction(slot, n_slots)          # orientation of dominion
        self.theta, self.phi = to_spherical(self.u)
        self.r = 0.0                                         # ray magnitude = evidence weight (set by work)
        self.children = {}
        self.journal = []                                    # the SmartJournal: what this NVE measured

    def R(self):
        return ray(self.r, self.theta, self.phi)

    def manifold_inward(self, name, purpose, n_slots=12):
        """Manifoldability: nest a child NVE one level deeper (its own local sphere of directions)."""
        if name not in self.children:
            self.children[name] = NVE(name, purpose, len(self.children), n_slots, self.depth + 1)
        return self.children[name]

    def log(self, **entry):
        self.journal.append(entry)
        return entry


class EVE:
    """The envelope. Holds NVEs, checks the gyroscopic rule, and evaluates the Core Formula."""
    def __init__(self, n_slots=720):
        self.A = np.zeros(3)                  # Dimensional Anchor
        self.n_slots = n_slots                # the 720 Rays codex: 720 available orientations
        self.nves = {}

    def open(self, name, purpose):
        nve = NVE(name, purpose, len(self.nves), self.n_slots)
        self.nves[name] = nve
        return nve

    def gyroscopic_check(self):
        """No two NVEs may share an orientation. Returns the smallest angle between any two (degrees)."""
        us = [n.u for n in self.nves.values()]
        best = 180.0
        for i in range(len(us)):
            for j in range(i + 1, len(us)):
                best = min(best, math.degrees(math.acos(max(-1, min(1, float(us[i] @ us[j]))))))
        return best

    # ---- the Core Formula ------------------------------------------------------------
    def unified_state(self, k=0.5, t=1.0, n_terms=None, k_feedback=None):
        """
        S = Σ_i Σ_{n=0}^{∞} k^n R_i + C(t)

        The inner sum is a geometric series. It only converges when |k| < 1, and then
            Σ_n k^n = 1/(1-k).
        C(t) = Σ_i ∫_0^t F_n(R_i) dt. F_n depends on the iteration n, not on t, so for a fixed n
        the integral is t·k^n·R_i. Here n is taken as the iteration reached by time t (n = floor(t)),
        which is one reading of the formula; it is stated so it can be changed.
        Returns S (a 3-vector), its magnitude, and the share of each NVE in it.
        """
        if abs(k) >= 1 and n_terms is None:
            raise ValueError("Σ k^n diverges for |k| ≥ 1 — S is infinite unless the series is cut off (pass n_terms).")
        geo = (1 - k ** n_terms) / (1 - k) if n_terms else 1 / (1 - k)
        Rsum = sum((n.R() for n in self.nves.values()), np.zeros(3))
        n_t = int(math.floor(t))
        kf = k if k_feedback is None else k_feedback
        C = t * (kf ** n_t) * Rsum
        S = geo * Rsum + C
        share = {}
        mag = float(np.linalg.norm(S)) or 1.0
        for name, n in self.nves.items():
            share[name] = round(float((geo + t * kf ** n_t) * n.R() @ S) / (mag ** 2), 4)
        return dict(S=[round(float(x), 6) for x in S], magnitude=round(float(np.linalg.norm(S)), 6),
                    geometric_factor=round(geo, 6), C_t=[round(float(x), 6) for x in C], share=share)


def null_model_note():
    return ("With every r_i equal, rays spread evenly over the sphere nearly cancel, so |S| is small. "
            "S only grows in a direction when the NVEs pointing that way carry more evidence. "
            "S is therefore a weighted resultant: it says which rays dominate, not how much was decoded.")
