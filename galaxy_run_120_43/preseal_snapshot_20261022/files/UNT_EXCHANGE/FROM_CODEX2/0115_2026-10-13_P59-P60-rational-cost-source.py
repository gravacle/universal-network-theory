"""Codex2 source submission. NOT EXECUTED or independently reviewed.
See packets 0114 and 0116. Exact conditional diagonal parent only.
No import of project code, no jobs, file IO, automatic main, or physical verdict.
"""
from fractions import Fraction


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError("Use int, rational string or Fraction; no float coercion")
    return Fraction(value)


def bit(value):
    if type(value) is not int or value not in (0, 1):
        raise ValueError("Expected literal binary integer")
    return value


def edge_return_energy(D, x_without_q, lam_r, h, n, q_u, q_v):
    """One diagonal second-order return term; positive denominator required."""
    D, x, r, h = map(rational, (D, x_without_q, lam_r, h))
    if D <= 0:
        raise ValueError("D=2Ud must be positive")
    sigma = 1 - 2 * bit(n)
    denominator = D + sigma * (x - r * (bit(q_u) + bit(q_v)))
    if denominator <= 0:
        raise ValueError("No positive separated single-flip denominator")
    return -h * h / denominator


def edge_mixed_cost(D, x_without_q, lam_r, h, n):
    """Return four raw arms and their mixed difference, no phase/mass inference."""
    arms = {(a, b): edge_return_energy(D, x_without_q, lam_r, h, n, a, b)
            for a in (0, 1) for b in (0, 1)}
    return {"arms": arms, "mixed_cost":
            arms[1, 1] - arms[1, 0] - arms[0, 1] + arms[0, 0],
            "scope": "CONDITIONAL_DIAGONAL_RETURN_ORDER_H2"}


def bare_flip_cost(epsilon_r, lam_r, degree, q):
    """Basis diagonal of persistent-site comparator C_v, not a writing rate."""
    if type(degree) is not int or degree not in range(5):
        raise ValueError("q4 degree must be 0..4")
    return (rational(epsilon_r) - rational(lam_r) * degree) * (1 - 2 * bit(q))


def fixed_word_defect_bound(Ud, Delta, dstar, lam_j, lam_r, p_word, q_word):
    """Sufficient diagonal, fixed-word ice bound; NOT a full-H gap.
    On a loopless q4 graph an off-ice configuration has sum |d_v-2| >= 2.
    Caller must separately establish the graph/ice existence and fixed-word parent.
    Nonpositive delta means inconclusive, not absence of a native gap or Gamma.
    """
    Ud, Delta, dstar, j, r = map(rational, (Ud, Delta, dstar, lam_j, lam_r))
    if Ud <= 0 or len(p_word) != len(q_word) or not p_word:
        raise ValueError("Positive Ud and nonempty equal-length words required")
    mu0 = Delta / 2 + 2 * Ud * (2 - dstar)
    mu = tuple(mu0 + j * bit(p) - r * bit(q) for p, q in zip(p_word, q_word))
    delta = min(Ud - abs(m) for m in mu)
    return {"mu": mu, "delta": delta,
            "off_ice_lower_bound": 2 * delta if delta > 0 else None,
            "status": "SUFFICIENT_DIAGONAL_BOUND" if delta > 0 else "INCONCLUSIVE",
            "full_native_gap": "NOT_CERTIFIED"}


def isolated_cluster_sufficient_bound(cluster_upper, complement_lower, perturbation_norm):
    """Weyl sufficient bound with caller-certified ALL-spectrum input bounds.
    Assumes entire reference cluster lies below its complement and V is Hermitian.
    Does not compute, authenticate or assert those inputs or a native ice cluster.
    """
    a, b, v = map(rational, (cluster_upper, complement_lower, perturbation_norm))
    if v < 0 or b <= a:
        raise ValueError("Need nonnegative norm and ordered disjoint reference spectra")
    remaining = b - a - 2 * v
    return {"bound": remaining,
            "status": "CONDITIONAL_SUFFICIENT" if remaining > 0 else "INCONCLUSIVE",
            "input_certification": "CALLER_OWNS_FULL_SPECTRAL_AND_NORM_CERTIFICATES"}
