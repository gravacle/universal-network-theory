"""Evaluate the frozen six-point sufficient bound, not a graph simulation."""
import argparse
import decimal
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import tempfile
import time

HERE = Path(__file__).resolve().parent
NOTE = HERE / "NATIVE_CARRIER_CONTROLLED_CLOCK_V001.md"
NOTE_SHA = "55e7514ecdc636bc2817d78d44ca5a50422f8be2002877e96c92fca04636108b"
OUT = HERE / "native_remote_clock_bound_v001_results.json"
CENSUS = (16, 256, 4096, 65536, 1048576, 16777216)
ALLOWANCE = 1e-10


def binary_bound(n):
    d = (n.bit_length() - 1) // 2
    assert n == 4 ** d
    s = 2 * d + 1
    q = math.sinh(1.0 / n)
    a = 8.0 ** (-d) * math.exp(63.0 / 16)
    e = .75 * (math.sqrt(s*n*q*q + (s*n*n+n*s*s)*q**4) + n*a)
    w = math.sqrt(n*q*q+n*(n-1)*q**4)
    p = min(1.0, (a+e)**2)
    f = 2*p+.5*w
    b = .5-f
    return dict(q=q, tail_amplitude=a, state_error_upper=e,
                degree_rms_upper=w, carrier_probability_upper=p,
                forcing_upper=f, amplitude_lower=b, margin=2*b-f)


def decimal_bound(n):
    D = decimal.Decimal
    with decimal.localcontext() as ctx:
        ctx.prec = 60
        d = (n.bit_length()-1)//2
        s = D(2*d+1)
        nd = D(n)
        z = D(1)/nd
        q = (z.exp()-(-z).exp())/2
        a = D(8)**(-d)*(D(63)/16).exp()
        e = D(3)/4*((s*nd*q*q+(s*nd*nd+nd*s*s)*q**4).sqrt()+nd*a)
        w = (nd*q*q+nd*(nd-1)*q**4).sqrt()
        p = min(D(1),(a+e)**2)
        f = 2*p+w/2
        b = D(1)/2-f
        return dict(q=q, tail_amplitude=a, state_error_upper=e,
                    degree_rms_upper=w, carrier_probability_upper=p,
                    forcing_upper=f, amplitude_lower=b, margin=2*b-f)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", required=True)
    parser.parse_args()
    start = time.monotonic()
    if OUT.exists():
        raise FileExistsError("Preserve the completed result; do not rerun.")
    if hashlib.sha256(NOTE.read_bytes()).hexdigest() != NOTE_SHA:
        raise ValueError("Frozen mathematical protocol hash mismatch.")
    checks, rows = [], []
    for n in CENSUS:
        a, b = binary_bound(n), decimal_bound(n)
        for key in a:
            residual = abs(a[key]-float(b[key]))
            checks.append(dict(n=n, field=key, residual=residual,
                               passed=math.isfinite(residual) and residual<=ALLOWANCE))
        qualifies = a["amplitude_lower"]>ALLOWANCE and a["margin"]>ALLOWANCE
        rows.append(dict(n=n, supplied_cycle_vertices=2*n,
                         radius_and_clock_distance=(n.bit_length()-1)//2,
                         binary64=a, decimal60={k:str(v) for k,v in b.items()},
                         sufficient_certificate=qualifies,
                         frequency_lower=(a["margin"]/a["amplitude_lower"]
                                          if a["amplitude_lower"]>ALLOWANCE else None)))
    passed = all(c["passed"] for c in checks)
    result = dict(status="COMPLETE" if passed else "ARITHMETIC_CHECK_FAILURE",
                  scope="Six scalar bounds only; no state propagation or observed clock",
                  input_sha256=NOTE_SHA,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  units="x=tau/hbar", window=[0,1], fixed_census=list(CENSUS),
                  assigned_arithmetic_allowance=ALLOWANCE, rows=rows, checks=checks,
                  check_counts=dict(passed=sum(c["passed"] for c in checks),total=len(checks)),
                  qualifications=["Not directed-rounding certification",
                                  "Uncertified bound does not mean clock failure",
                                  "Supplied graphs and separation; no formation theorem",
                                  "Expectation-level phase, not single-shot readout",
                                  "No physical unit, gravitational or observational claim"],
                  runtime=dict(wall_seconds=time.monotonic()-start,
                               peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    payload = json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n"
    with tempfile.NamedTemporaryFile(mode="w",dir=HERE,prefix=".remote-clock-",delete=False) as f:
        temporary = Path(f.name)
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary,OUT)  # Exclusive publication: never replace evidence.
    finally:
        temporary.unlink()
    print(json.dumps(dict(status=result["status"],check_counts=result["check_counts"],
                          rows=[dict(n=r["n"],certificate=r["sufficient_certificate"],
                                     amplitude_lower=r["binary64"]["amplitude_lower"],
                                     frequency_lower=r["frequency_lower"]) for r in rows],
                          runtime=result["runtime"]),indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
