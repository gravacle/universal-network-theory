"""Exact symbolic verification of the local cause of the saved sixth-order contrast.

One eight-dimensional block, no evolution, fit, spectrum or parameter scan.
Variables: t, V=Vv-Vu, a=delta_u, b=delta_v, w=g_writer, g=g_carrier.
The prospective identity checked is the g-dependent, detuning-dependent part
of P6: t^2/360 * [g^2*(a^2+b^2+V*(4*b-14*a))+18*V*w*g*(b-a)].
This is an independently coded symbolic check of the hand derivation. The
dynamic-link cancellation is a separate path-counting argument, not simulated
by this block. Compare only feedback/copy contrasts with the saved full parent.
All polynomials have rational coefficients; no numerical tolerance is used.
The common graph energy cancels from probabilities, not from physical work.
The reference clock is absent here; use its independently saved full result.
Root only; 120 seconds and 256 MiB; fail on existing output or altered input.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import resource
import tempfile
import time

HERE = Path(__file__).resolve().parent
SAVED = HERE / "native_active_record_density_response_v001_results.json"
PIN = "243064c9d85f8c78e780e2410e0b3d1d019679073ecb46d68096a41dbe3f9671"
OUT = HERE / "native_record_local_mechanism_v001_results.json"
NAMES = ("t", "V", "a", "b", "w", "g")
ZERO = (0,) * 6


def plus(*polys):
    out = {}
    for p in polys:
        for k, c in p.items():
            out[k] = out.get(k, F(0)) + c
    return {k: c for k, c in out.items() if c}


def scale(p, c):
    return {k: v * c for k, v in p.items() if v * c}


def mul(p, q):
    out = {}
    for a, c in p.items():
        for b, d in q.items():
            k = tuple(x + y for x, y in zip(a, b))
            out[k] = out.get(k, F(0)) + c * d
    return {k: c for k, c in out.items() if c}


def var(i):
    return {tuple(int(j == i) for j in range(6)): F(1)}


t, V, a, b, w, g = [var(i) for i in range(6)]


def action(vector):
    out = [{} for _ in range(8)]
    for index, p in enumerate(vector):
        pos, bits = divmod(index, 4)
        diagonal = plus(V if pos else {}, a if bits & 1 else {}, b if bits & 2 else {})
        out[index] = plus(out[index], mul(diagonal, p))
        out[index ^ 4] = plus(out[index ^ 4], scale(mul(t, p), -1))
        for record in (0, 1):
            amplitude = plus(w, g if pos == record else {})
            dest = index ^ (1 << record)
            out[dest] = plus(out[dest], mul(amplitude, p))
    return out


def target_dot(x, y):
    return plus(*(mul(x[k], y[k]) for k in range(4, 8)))


def evaluate(p, values):
    total = F(0)
    for powers, c in p.items():
        term = c
        for v, power in zip(values, powers):
            term *= v ** power
        total += term
    return total


def encode(p):
    return [{"powers": dict(zip(NAMES, powers)), "coefficient": str(c)}
            for powers, c in sorted(p.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", required=True)
    parser.parse_args()
    start = time.monotonic()
    if OUT.exists():
        raise FileExistsError("Preserve completed evidence; no replay.")
    if hashlib.sha256(SAVED.read_bytes()).hexdigest() != PIN:
        raise ValueError("Saved full-parent result changed.")
    checks = []
    def check(name, passed):
        checks.append(dict(name=name, passed=bool(passed)))
    def guard():
        if time.monotonic() - start > 120 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 268435456:
            raise RuntimeError("Frozen resource ceiling exceeded.")
    vectors = [[{ZERO: F(1)}] + [{} for _ in range(7)]]
    for _ in range(5):
        vectors.append(action(vectors[-1]))
        guard()
    p2 = target_dot(vectors[1], vectors[1])
    p4 = plus(scale(target_dot(vectors[2], vectors[2]), F(1, 4)),
              scale(target_dot(vectors[1], vectors[3]), F(-1, 3)))
    p6 = plus(scale(target_dot(vectors[3], vectors[3]), F(1, 36)),
              scale(target_dot(vectors[1], vectors[5]), F(1, 60)),
              scale(target_dot(vectors[2], vectors[4]), F(-1, 24)))
    tt, gg = mul(t, t), mul(g, g)
    expected4 = scale(mul(tt, plus(mul(V, V), scale(gg, 2), scale(tt, 4))), F(-1, 12))
    isolated = {k: c for k, c in p6.items() if k[5] and (k[2] or k[3])}
    expected = scale(mul(tt, plus(
        mul(gg, plus(mul(a, a), mul(b, b), mul(V, plus(scale(b, 4), scale(a, -14))))),
        scale(mul(mul(mul(V, w), g), plus(b, scale(a, -1))), 18))), F(1, 360))
    check("P2=t^2", p2 == tt)
    check("complete local P4", p4 == expected4)
    check("general detuning and copy part of P6", isolated == expected)
    off = {k: c for k, c in p6.items() if not k[5]}
    omega2 = plus(mul(V, V), scale(tt, 4))
    check("copy-off factorizes for all detunings and writer strengths",
          off == scale(mul(tt, mul(omega2, omega2)), F(1, 360)))
    for label, poly, degree in (("P2", p2, 2), ("P4", p4, 4), ("P6", p6, 6)):
        check(label + " energy homogeneity", all(sum(k) == degree for k in poly))
    full = json.loads(SAVED.read_text())
    rows = {(r["graph"], r["feedback"], r["copy"]): F(r["P6"]["exact"]) for r in full["rows"]}
    comparisons = []
    changes = {}
    for graph, du, dv in ((13, 1, 2), (15, 2, 2)):
        local = {}
        for feedback in (False, True):
            lam = F(1, 2) if feedback else F(0)
            for copy in (False, True):
                values = (F(1, 2), F(dv-du, 4), 1-lam*du, 1-lam*dv, F(1), F(int(copy)))
                local[feedback, copy] = evaluate(p6, values)
        delta = local[True, True] - local[True, False] - local[False, True] + local[False, False]
        actual = rows[graph, True, True] - rows[graph, True, False] - rows[graph, False, True] + rows[graph, False, False]
        check(f"G{graph} local and full-parent feedback-copy contrast", delta == actual)
        changes[graph] = delta
        comparisons.append(dict(graph=graph, local_P6={str(k): str(v) for k, v in local.items()},
                                local_contrast=str(delta), full_parent_contrast=str(actual)))
    triple = changes[15] - changes[13]
    check("triple contrast agrees with full parent", triple == F(full["three_factor_contrast"]["P6"]["exact"]))
    guard()
    passed = all(c["passed"] for c in checks)
    result = dict(status="COMPLETE" if passed else "EXACT_CHECK_FAILURE",
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), input_sha256=PIN,
        variables=NAMES, P2=encode(p2), P4=encode(p4), P6=encode(p6),
        copy_and_detuning_P6=encode(isolated), comparisons=comparisons, triple_P6=str(triple),
        checks=checks, check_counts=dict(passed=sum(c["passed"] for c in checks), total=len(checks)),
        qualifications=["Local contrast only; full P6 and reference clock are not replaced",
                        "Path cancellation requires definite initial graph and blank records",
                        "Analytic interference mechanism, not a collective criticality or gravitational-force test"],
        runtime=dict(wall_seconds=time.monotonic()-start, peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    with tempfile.NamedTemporaryFile(mode="w", dir=HERE, prefix=".local-record-", delete=False) as f:
        temporary = Path(f.name)
        f.write(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary, OUT)
    finally:
        temporary.unlink()
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
