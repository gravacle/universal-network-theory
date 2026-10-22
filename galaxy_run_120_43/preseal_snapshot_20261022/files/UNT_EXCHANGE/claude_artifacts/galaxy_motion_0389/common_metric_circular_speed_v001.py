# UNT support task 0389 -- inert author implementation, v001.
# Standard library only (math, numbers). Module level: imports and function
# definitions only; no I/O, no CLI, no work at import, no physical constants.
# Written statically; never executed or imported by its author.

import math
import numbers


def _finite_real(label, value):
    """Return float(value) for a finite real, non-bool number; otherwise raise ValueError."""
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(f"{label}: expected a finite real number, got {type(value).__name__}")
    try:
        out = float(value)
    except (OverflowError, ValueError, TypeError) as exc:
        raise ValueError(f"{label}: not representable as a float ({exc})") from None
    if not math.isfinite(out):
        raise ValueError(f"{label}: not finite ({out!r})")
    return out


def circular_speed_rows(*, metric_rows, c_km_s):
    """Local circular speed read from an input common-metric profile, row by row.

    Sources (read-only): task FROM_CODEX/0389_2026-10-15_common_metric_motion_kernel_
    implementation.md; equation from CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md,
    sections "Existing geometry, gravity and motion" and "Direction-dependent extension".

    Equation (stationary axisymmetric, negligible-shift, equatorial circular branch;
    R = sqrt(h_phi_phi) circumferential radius, N > 0 lapse, both differentiated with
    respect to the SAME declared radial coordinate r):
        ratio        = dlogN_dr / dlogR_dr        (= v_local^2 / c^2, coordinate invariant)
        v_local_km_s = c_km_s * sqrt(ratio)
    In a circumferential coordinate (r = R) this is v^2 = c^2 R d_R ln N.

    Arguments (keyword-only, required, no defaults):
      metric_rows: non-empty list or tuple of dicts, each with exactly the keys
        "id" (non-empty string, unique; e.g. "NGC3198-Q01", the <object>-Q<NN> form of
        the target-free query manifest's query_id; the format is documented, not
        enforced), "R_kpc", "N", "dlogN_dr", "dlogR_dr" (finite real, non-bool).
      c_km_s: finite real > 0, supplied by the caller; no constant is built in.

    Raises ValueError (first violation, with row index and id) unless: every value is
    finite real and not bool; c_km_s > 0; R_kpc > 0; N > 0; dlogR_dr != 0; ids are
    unique non-empty strings; 0 <= ratio < 1. Nothing is clipped, sorted, replaced,
    dropped or inferred; output rows keep input order and ids.

    Returns a dict: "rows" (one dict per input row: id, v_local_km_s, ratio, R_kpc,
    inputs, units "km/s", semantics "LOCAL_CIRCULAR_SPEED"), plus c_km_s, units,
    semantics, equation and scope.

    Scope: local circular speed read from an input metric profile only. NOT
    TOTAL_OBSERVABLE and not a full prediction; observational projection,
    normalization, state and error metadata belong to the existing higher-level
    provider. No gravity law, Poisson solver, mass, halo or Birth-deficit force is
    inserted; no weak-field approximation and no observer/light correction is applied.
    """
    c = _finite_real("c_km_s", c_km_s)
    if not c > 0.0:
        raise ValueError(f"c_km_s must be > 0, got {c!r}")
    if not isinstance(metric_rows, (list, tuple)):
        raise ValueError(f"metric_rows must be a list or tuple, got {type(metric_rows).__name__}")
    if len(metric_rows) == 0:
        raise ValueError("metric_rows is empty")
    fields = ("id", "R_kpc", "N", "dlogN_dr", "dlogR_dr")
    seen = set()
    rows = []
    for index, row in enumerate(metric_rows):
        where = f"metric_rows[{index}]"
        if not isinstance(row, dict):
            raise ValueError(f"{where}: expected a dict, got {type(row).__name__}")
        missing = [k for k in fields if k not in row]
        extra = [k for k in row if k not in fields]
        if missing or extra:
            raise ValueError(f"{where}: missing keys {missing!r}, unexpected keys {extra!r}")
        rid = row["id"]
        if not isinstance(rid, str) or not rid.strip():
            raise ValueError(f"{where}: id must be a non-empty string")
        if rid in seen:
            raise ValueError(f"{where}: duplicate id {rid!r}")
        seen.add(rid)
        where = f"{where} (id {rid!r})"
        R = _finite_real(f"{where} R_kpc", row["R_kpc"])
        N = _finite_real(f"{where} N", row["N"])
        dlogN = _finite_real(f"{where} dlogN_dr", row["dlogN_dr"])
        dlogR = _finite_real(f"{where} dlogR_dr", row["dlogR_dr"])
        if not R > 0.0:
            raise ValueError(f"{where}: R_kpc must be > 0, got {R!r}")
        if not N > 0.0:
            raise ValueError(f"{where}: lapse N must be > 0, got {N!r}")
        if dlogR == 0.0:
            raise ValueError(f"{where}: dlogR_dr is zero (dR/dr = 0); the circular read is undefined")
        try:
            ratio = dlogN / dlogR
        except OverflowError:
            raise ValueError(f"{where}: dlogN_dr / dlogR_dr overflows") from None
        if not math.isfinite(ratio):
            raise ValueError(f"{where}: dlogN_dr / dlogR_dr is not finite ({ratio!r})")
        if not 0.0 <= ratio < 1.0:
            raise ValueError(
                f"{where}: ratio dlogN_dr/dlogR_dr = {ratio!r} is outside [0, 1): "
                "a negative ratio has no circular orbit on this branch and a ratio >= 1 "
                "is not subluminal"
            )
        rows.append(
            {
                "id": rid,
                "v_local_km_s": c * math.sqrt(ratio),
                "ratio": ratio,
                "R_kpc": R,
                "inputs": {"R_kpc": R, "N": N, "dlogN_dr": dlogN, "dlogR_dr": dlogR},
                "units": "km/s",
                "semantics": "LOCAL_CIRCULAR_SPEED",
            }
        )
    return {
        "rows": rows,
        "c_km_s": c,
        "units": "km/s",
        "semantics": "LOCAL_CIRCULAR_SPEED",
        "equation": "ratio = dlogN_dr / dlogR_dr; v_local_km_s = c_km_s * sqrt(ratio)",
        "scope": (
            "local circular speed read from an input metric profile only; NOT "
            "TOTAL_OBSERVABLE or a full prediction; observational projection, "
            "normalization, state and error belong to the existing higher-level "
            "provider; no gravity law, Poisson solver, mass, halo or force insertion; "
            "no weak-field or observer/light correction"
        ),
    }
