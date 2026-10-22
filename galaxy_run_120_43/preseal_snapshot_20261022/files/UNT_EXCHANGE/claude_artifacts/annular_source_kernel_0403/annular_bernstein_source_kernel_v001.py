"""UNT task 0403 -- inert annular-mean quadratic Bernstein source kernel, v001.

Author: Claude helper (author role), from the root specification in
/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0403_2026-10-16_annular_source_kernel_reuse.md
and the mathematics of section 1 of PLANAR_DENSITY_CONSTRUCTION_REVIEW.md
(halogas_source_candidate). Written statically; never imported or executed by its
author. Standard-library math only. Module-level code is limited to this docstring,
the math import, string constants and function definitions: no work at import, no
I/O, no printing, no subprocesses, no CLI.

Specification (root 0403, binding)
  Inputs, all explicit and required:
    s_edges           s[0..n], strictly increasing, nonnegative squared-radius edges;
    annular_means     m[0..n-1], finite nonnegative area means of the n annuli;
    boundary_controls d[0..n], one control per edge; internal edges are shared, so
                      d[i] is used by bin i-1 (right end) and bin i (left end).
  n >= 1. For every bin i both d[i] and d[i+1] lie in [0, m[i]], checked by exact
  comparison with no tolerance. In bin i, with w_i = s[i+1] - s[i],
      t      = (s - s[i]) / w_i,
      b[i]   = 3*m[i] - d[i] - d[i+1],
      Sigma  = d[i]*(1-t)**2 + 2*b[i]*t*(1-t) + d[i+1]*t**2.
  The subinterval area integral is pi * integral Sigma ds. With the antiderivative
      F_i(t) = d[i]*t*(1-t)**2 + (3*m[i] - d[i+1])*t**2*(1-t) + m[i]*t**3
  (dF_i/dt is the quadratic above; 3*m[i] - d[i+1] = d[i] + b[i]; F_i(0) = 0 and
  F_i(1) = m[i]), the integral of Sigma over [s_a, s_b] inside bin i is
  w_i * (F_i(t_b) - F_i(t_a)), and a whole bin gives pi * w_i * m[i].

Properties holding by inspection (no other property is claimed)
  * Bin area mean: each quadratic Bernstein basis function integrates to 1/3 on
    [0, 1], so the bin mean of Sigma in s is (d[i] + b[i] + d[i+1]) / 3 = m[i].
  * C0: Sigma(s[i]) = d[i] from both adjacent bins, because the control is shared.
  * Nonnegativity: d[i], d[i+1] in [0, m[i]] gives b[i] in [m[i], 3*m[i]], so all
    three Bernstein coefficients are >= 0 and 0 <= Sigma <= 3*m[i] in bin i.
  * A zero-mean bin has all three of its coefficients zero (admissibility forces
    d[i] = d[i+1] = 0 and then b[i] = 0); nothing is interpolated into it.
  No monotonicity, C1 smoothness, unique reconstruction, deconvolution, physical
  completeness or observational-error claim is made. The bound 3*m[i] is not a
  precision statement. Intra-bin curvature is a representation choice.

Domain
  ONLY the closed supplied interval [s[0], s[n]]. A query or an integration limit
  outside it is rejected (ok False, no value). Nothing is returned as zero outside
  the edges, no tail or exterior is invented, and the first and last controls are
  whatever the caller supplied (nonzero values are supported). Internal-edge bin
  rule for evaluation: a query equal to an internal edge s[k] (0 < k < n) is
  evaluated in bin k (the bin on its right); s[n] is evaluated in bin n-1. Because
  t = 0 at s[k] in bin k gives exactly d[k], and C0 holds, the value does not
  depend on this rule.

Units
  The caller's, used consistently: Sigma has the units of m and d; s has the units
  of squared radius; pi * integral Sigma ds has (units of m) * (units of s). No
  1e6, helium, distance, mass-to-light, inclination or any other physical
  conversion is applied. Conversions belong to the caller's source layer.

Applicability
  Declared area means over disjoint annuli with explicit edges in s = R**2.
  Stellar medians, nodal or ring-centre samples, overlapping or correlated ring
  samples, or values without declared annulus edges are NOT silently admitted as
  annular means; that declaration belongs to the caller. Unknown geometry, vertical
  shape, unsampled source, outer material and calibration stay with the caller.

Admission (fail-closed)
  Sequences must be built-in list or tuple; elements must be built-in int or float
  (exact types: bool, None, str, numpy scalars and other subclasses are rejected;
  convert explicitly). Values must be finite, and an int must be exactly
  representable as a float. NaN, inf, wrong lengths, n < 1, negative or
  non-strictly-increasing s, negative m and any d outside [0, m] for either
  adjacent bin are rejected. Missing values stay missing: nothing is filled,
  clipped, renormalized or defaulted. Every public argument is keyword-only and
  required. Floating-point rounding is reported as computed, never corrected.

Public callables
  annular_bernstein_sigma(*, s_edges, annular_means, boundary_controls, s_query)
  annular_bernstein_area_integral(*, s_edges, annular_means, boundary_controls,
                                  s_lo, s_hi)
Each returns a plain dict with "ok", "stage_reached" and "failures". When ok is
False every populated field is failure evidence only.
"""

import math


_UNITS = (
    "caller's consistent units: Sigma carries the units of annular_means and "
    "boundary_controls; s carries squared-radius units; the area integral "
    "pi * integral Sigma ds carries (units of m) * (units of s). No 1e6, helium, "
    "distance, mass-to-light, inclination or other physical conversion is applied."
)

_SCOPE = (
    "quadratic Bernstein representation of declared annular area means on the "
    "closed supplied edge interval [s[0], s[n]] only; C0, nonnegative, exact bin "
    "area mean m[i]. No monotonicity, C1, unique-reconstruction, deconvolution, "
    "physical-completeness or observational-error claim. Not applicable by default "
    "to stellar medians, nodal or ring-centre samples or overlapping rings. Outside "
    "the edges nothing is defined: no zero exterior, no tail."
)

_DOMAIN = (
    "closed interval [s[0], s[n]] of the supplied edges; any query or integration "
    "limit outside it is rejected and no value is returned"
)

_BIN_RULE = (
    "a query q is evaluated in the largest bin i (0 <= i <= n-1) with s[i] <= q: an "
    "internal edge s[k] uses bin k (its right bin) and s[n] uses bin n-1. Because "
    "t = 0 at s[k] in bin k gives exactly d[k] and C0 holds, the value does not "
    "depend on this rule."
)


def _scalar(name, value, failures):
    """Admit a finite built-in int or float as float, or record a failure and return None."""
    kind = type(value)
    if kind is bool:
        failures.append(f"input {name}: a boolean is not an admitted real value")
        return None
    if kind is not int and kind is not float:
        failures.append(
            f"input {name}: type {kind.__name__} is not an admitted real value "
            "(built-in int or float only; missing values are not filled)"
        )
        return None
    try:
        out = float(value)
    except (OverflowError, ValueError, TypeError):
        failures.append(f"input {name}: not representable as a float value")
        return None
    if not math.isfinite(out):
        failures.append(f"input {name}: not finite ({out!r})")
        return None
    if kind is int and out != value:
        failures.append(f"input {name}: int {value!r} is not exactly representable as a float")
        return None
    return out


def _sequence(name, value, failures):
    """Admit a built-in list or tuple of finite reals as a list of float, else None."""
    kind = type(value)
    if kind is not list and kind is not tuple:
        failures.append(
            f"input {name}: type {kind.__name__} is not a built-in list or tuple"
        )
        return None
    out = [_scalar(f"{name}[{j}]", value[j], failures) for j in range(len(value))]
    if any(v is None for v in out):
        return None
    return out


def _admit_profile(s_edges, annular_means, boundary_controls, failures):
    """Admit (s, m, d) exactly per the 0403 specification; return lists or None."""
    start = len(failures)
    s = _sequence("s_edges", s_edges, failures)
    m = _sequence("annular_means", annular_means, failures)
    d = _sequence("boundary_controls", boundary_controls, failures)
    if s is None or m is None or d is None:
        return None
    n = len(m)
    if n < 1:
        failures.append("input annular_means: at least one annulus is required (n >= 1)")
        return None
    if len(s) != n + 1:
        failures.append(f"input s_edges: length {len(s)} is not n + 1 = {n + 1}")
    if len(d) != n + 1:
        failures.append(f"input boundary_controls: length {len(d)} is not n + 1 = {n + 1}")
    if len(failures) > start:
        return None
    if not s[0] >= 0.0:
        failures.append(f"input s_edges[0]: {s[0]!r} is negative")
    for j in range(n):
        if not s[j + 1] > s[j]:
            failures.append(
                f"input s_edges: s[{j + 1}] = {s[j + 1]!r} is not greater than "
                f"s[{j}] = {s[j]!r} (strictly increasing required)"
            )
    for i in range(n):
        if not m[i] >= 0.0:
            failures.append(f"input annular_means[{i}]: {m[i]!r} is negative (rejected, not clipped)")
    for j in range(n + 1):
        if not d[j] >= 0.0:
            failures.append(f"input boundary_controls[{j}]: {d[j]!r} is negative")
    for i in range(n):
        for j in (i, i + 1):
            if not d[j] <= m[i]:
                failures.append(
                    f"input boundary_controls[{j}]: {d[j]!r} exceeds annular_means[{i}] "
                    f"= {m[i]!r} of adjacent bin {i} (required d in [0, m])"
                )
    if len(failures) > start:
        return None
    return s, m, d


def _middle_controls(m, d, failures):
    """b[i] = 3*m[i] - d[i] - d[i+1]; a non-finite b is a failure (no value kept)."""
    b = []
    for i in range(len(m)):
        value = 3.0 * m[i] - d[i] - d[i + 1]
        if not math.isfinite(value):
            failures.append(f"coefficients: b[{i}] is not representable ({value!r})")
            return None
        b.append(value)
    return b


def _bin_of(s, q):
    """Largest i in [0, n-1] with s[i] <= q, for s[0] <= q <= s[n] (binary search)."""
    lo = 0
    hi = len(s) - 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if s[mid] <= q:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _sigma_in_bin(s, d, b, i, q):
    """Sigma at q inside bin i: d[i]*(1-t)^2 + 2*b[i]*t*(1-t) + d[i+1]*t^2."""
    t = (q - s[i]) / (s[i + 1] - s[i])
    u = 1.0 - t
    return d[i] * (u * u) + 2.0 * (b[i] * (t * u)) + d[i + 1] * (t * t)


def _primitive(m, d, i, t):
    """F_i(t) = d[i] t (1-t)^2 + (3 m[i] - d[i+1]) t^2 (1-t) + m[i] t^3; F_i(0)=0, F_i(1)=m[i]."""
    u = 1.0 - t
    return d[i] * (t * u * u) + (3.0 * m[i] - d[i + 1]) * (t * t * u) + m[i] * (t * t * t)


def _new_result():
    return {
        "ok": False,
        "stage_reached": None,
        "failures": [],
        "inputs": None,
        "middle_controls": None,
        "units": _UNITS,
        "domain": _DOMAIN,
        "scope": _SCOPE,
    }


def annular_bernstein_sigma(*, s_edges, annular_means, boundary_controls, s_query):
    """Evaluate Sigma at caller-supplied squared radii inside [s[0], s[n]].

    Arguments (keyword-only, required, no defaults):
      s_edges: list/tuple s[0..n], nonnegative, strictly increasing.
      annular_means: list/tuple m[0..n-1], finite, >= 0; n >= 1.
      boundary_controls: list/tuple d[0..n]; d[i], d[i+1] in [0, m[i]] for each bin i.
      s_query: non-empty list/tuple of finite reals, each in [s[0], s[n]].
    Any query outside the closed interval rejects the whole call: no value is
    returned for any query, and nothing outside the edges is reported as zero.

    Returns a dict with keys: ok, stage_reached ('inputs', 'coefficients',
    'evaluation' or 'complete'), failures, inputs (admitted s_edges, annular_means,
    boundary_controls, s_query as floats, n_bins), middle_controls (b list),
    bin_rule, bin_index (list, one per query), sigma (list, one per query, caller's
    units), units, domain, scope. sigma and bin_index are None unless ok.
    """
    result = _new_result()
    result["bin_rule"] = _BIN_RULE
    result["bin_index"] = None
    result["sigma"] = None
    failures = result["failures"]

    # ---- Stage 1: admission ---------------------------------------------------
    result["stage_reached"] = "inputs"
    profile = _admit_profile(s_edges, annular_means, boundary_controls, failures)
    queries = _sequence("s_query", s_query, failures)
    if queries is not None and len(queries) == 0:
        failures.append("input s_query: at least one query value is required")
    if failures:
        return result
    s, m, d = profile
    n = len(m)
    for k in range(len(queries)):
        q = queries[k]
        if not (s[0] <= q <= s[n]):
            failures.append(
                f"input s_query[{k}]: {q!r} is outside the domain [{s[0]!r}, {s[n]!r}]; "
                "Sigma is undefined there (not zero)"
            )
    result["inputs"] = {
        "s_edges": s,
        "annular_means": m,
        "boundary_controls": d,
        "s_query": queries,
        "n_bins": n,
    }
    if failures:
        return result

    # ---- Stage 2: middle Bernstein controls b[i] ------------------------------
    result["stage_reached"] = "coefficients"
    b = _middle_controls(m, d, failures)
    if b is None:
        return result
    result["middle_controls"] = b

    # ---- Stage 3: evaluation --------------------------------------------------
    result["stage_reached"] = "evaluation"
    bins = []
    values = []
    for k in range(len(queries)):
        i = _bin_of(s, queries[k])
        value = _sigma_in_bin(s, d, b, i, queries[k])
        if not math.isfinite(value):
            failures.append(f"evaluation: Sigma at s_query[{k}] is not representable ({value!r})")
        bins.append(i)
        values.append(value)
    if failures:
        return result
    result["bin_index"] = bins
    result["sigma"] = values
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result


def annular_bernstein_area_integral(*, s_edges, annular_means, boundary_controls, s_lo, s_hi):
    """Exact polynomial area integral pi * integral_{s_lo}^{s_hi} Sigma ds.

    Arguments (keyword-only, required, no defaults):
      s_edges, annular_means, boundary_controls: as in annular_bernstein_sigma.
      s_lo, s_hi: finite reals with s[0] <= s_lo <= s_hi <= s[n].
    Any limit outside the closed edge interval rejects the call; nothing outside
    the edges is integrated as zero and no tail is added. s_lo == s_hi gives 0.

    Per overlapped bin i with [s_a, s_b] = [max(s_lo, s[i]), min(s_hi, s[i+1])],
    s_a < s_b, the contribution is pi * w_i * (F_i(t_b) - F_i(t_a)) with the
    closed-form cubic antiderivative F_i of the module docstring. A whole bin
    (t_a = 0, t_b = 1) gives exactly pi * w_i * m[i] up to the final products.
    Contributions are summed with math.fsum; rounding is reported, not corrected.

    Returns a dict with keys: ok, stage_reached ('inputs', 'coefficients',
    'integration' or 'complete'), failures, inputs (admitted s_edges,
    annular_means, boundary_controls, s_lo, s_hi as floats, n_bins),
    middle_controls (b list), per_bin (list of {bin, s_from, s_to, area_integral}
    for bins with s_from < s_to), area_integral (caller's units of m times units
    of s), units, domain, scope. per_bin and area_integral are None unless ok.
    """
    result = _new_result()
    result["per_bin"] = None
    result["area_integral"] = None
    failures = result["failures"]

    # ---- Stage 1: admission ---------------------------------------------------
    result["stage_reached"] = "inputs"
    profile = _admit_profile(s_edges, annular_means, boundary_controls, failures)
    lo = _scalar("s_lo", s_lo, failures)
    hi = _scalar("s_hi", s_hi, failures)
    if failures:
        return result
    s, m, d = profile
    n = len(m)
    if not lo >= s[0]:
        failures.append(
            f"input s_lo: {lo!r} is below s[0] = {s[0]!r}; outside the domain "
            "(rejected, not integrated as zero)"
        )
    if not hi <= s[n]:
        failures.append(
            f"input s_hi: {hi!r} is above s[n] = {s[n]!r}; outside the domain "
            "(rejected, no tail)"
        )
    if not lo <= hi:
        failures.append(f"input s_lo, s_hi: s_lo = {lo!r} exceeds s_hi = {hi!r}")
    result["inputs"] = {
        "s_edges": s,
        "annular_means": m,
        "boundary_controls": d,
        "s_lo": lo,
        "s_hi": hi,
        "n_bins": n,
    }
    if failures:
        return result

    # ---- Stage 2: middle Bernstein controls b[i] ------------------------------
    result["stage_reached"] = "coefficients"
    b = _middle_controls(m, d, failures)
    if b is None:
        return result
    result["middle_controls"] = b

    # ---- Stage 3: per-bin closed-form integration -----------------------------
    result["stage_reached"] = "integration"
    per_bin = []
    parts = []
    for i in range(n):
        s_a = max(lo, s[i])
        s_b = min(hi, s[i + 1])
        if not s_a < s_b:
            continue
        w = s[i + 1] - s[i]
        t_a = (s_a - s[i]) / w
        t_b = (s_b - s[i]) / w
        value = math.pi * (w * (_primitive(m, d, i, t_b) - _primitive(m, d, i, t_a)))
        if not math.isfinite(value):
            failures.append(f"integration: bin {i} contribution is not representable ({value!r})")
        per_bin.append({"bin": i, "s_from": s_a, "s_to": s_b, "area_integral": value})
        parts.append(value)
    if failures:
        return result
    try:
        total = math.fsum(parts)
    except (OverflowError, ValueError) as exc:
        failures.append(f"integration: total is not representable ({exc})")
        return result
    if not math.isfinite(total):
        failures.append(f"integration: total is not representable ({total!r})")
        return result
    result["per_bin"] = per_bin
    result["area_integral"] = total
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result
