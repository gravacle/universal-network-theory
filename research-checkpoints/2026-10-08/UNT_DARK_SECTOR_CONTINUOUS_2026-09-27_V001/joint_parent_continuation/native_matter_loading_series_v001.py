"""Exact rational polynomial audit of native N=1 matter/formation onset.

New initial-series calculation, not a propagated history or a fitted model.
Variables h,g,k,eps,lam,j,t mean link flip, writer copy, blank link gap,
record energy, record feedback, current-square and carrier hopping.
Time variable x=tau/hbar. Full original baseline is retained physically;
subtracting its constant here only removes an unobservable common phase.
All carriers are native hard-core qutrit transfers, NOT fermionic CAR.
P0/P2 differ only by a constant carrier energy; P1 is checked both by
full 16D matrices and the two exact carrier-X bands. No files are written.
"""
import sys
sys.dont_write_bytecode = True
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import resource
import time

NAMES = ('h', 'g', 'k', 'eps', 'lam', 'j', 't')
Z = (0,)*len(NAMES)
ONE = {Z: F(1)}

def add(*parts):
    out = {}
    for p in parts:
        for key, val in p.items():
            out[key] = out.get(key, F(0))+val
    return {k: v for k, v in out.items() if v}

def scale(p, a):
    return {k: v*a for k, v in p.items() if v*a}

def mul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x+y for x, y in zip(ka, kb))
            out[key] = out.get(key, F(0))+va*vb
    return {k: v for k, v in out.items() if v}

def power(a, n):
    out = ONE
    for _ in range(n):
        out = mul(out, a)
    return out

def var(index):
    key = tuple(int(i == index) for i in range(len(NAMES)))
    return {key: F(1)}

h, g, k, eps, lam, j, t = [var(i) for i in range(len(NAMES))]

def substitute(p, index, value):
    out = {}
    for key, coeff in p.items():
        base = list(key)
        base[index] = 0
        out = add(out, mul({tuple(base): coeff}, power(value, key[index])))
    return out

def divide_variable(p, index):
    out = {}
    for key, coeff in p.items():
        if key[index] == 0:
            raise ValueError('Non-polynomial division')
        new = list(key)
        new[index] -= 1
        out[tuple(new)] = coeff
    return out

def show(p):
    return [{'coefficient': str(v), 'powers': dict(zip(NAMES, key))}
            for key, v in sorted(p.items())]

def build(records, carrier=False):
    nr, nc = 1 << records, 2 if carrier else 1
    size = 2*nr*nc
    edges = []
    for link in (0, 1):
        for rec in range(nr):
            for c in range(nc):
                row = (link*nr+rec)*nc+c
                diag = add(scale(k, link), scale(eps, rec.bit_count()),
                           scale(lam, -link*rec.bit_count()), scale(j, link if carrier else 0))
                edges.append((row, row, diag))
                edges.append((row, ((1-link)*nr+rec)*nc+c, scale(h, -1)))
                for r in range(records):
                    edges.append((row, (link*nr+(rec ^ (1 << r)))*nc+c, g))
                if carrier and link:
                    edges.append((row, (link*nr+rec)*nc+(1-c), scale(t, -1)))
    vectors = [[ONE]+[{} for _ in range(size-1)]]
    for _ in range(6):
        nxt = [{} for _ in range(size)]
        for row, col, val in edges:
            nxt[row] = add(nxt[row], mul(val, vectors[-1][col]))
        vectors.append(nxt)
    n_op = [(i, i, 1, 0) for i in range(size) if i//(nr*nc)]
    z_op = [(i, i, 1-2*((i//nc) % 2), 0) for i in range(size)]
    x_op = [(i, i ^ nc, 1, 0) for i in range(size)]
    y_op = [(i, i ^ nc, -1 if ((i//nc) % 2) == 0 else 1, 1) for i in range(size)]
    return vectors, (n_op, z_op, x_op, y_op)

def expectation(vectors, order, operator):
    real, imag = {}, {}
    for n in range(order+1):
        m = order-n
        denom = factorial(n)*factorial(m)
        for row, col, coeff, iphase in operator:
            phase = (n-m+iphase) % 4  # i^n (-i)^m times the operator phase.
            term = scale(mul(vectors[n][row], vectors[m][col]), F(coeff, denom))
            if phase == 0: real = add(real, term)
            if phase == 1: imag = add(imag, term)
            if phase == 2: real = add(real, scale(term, -1))
            if phase == 3: imag = add(imag, scale(term, -1))
    if imag:
        raise AssertionError('Non-real expectation for Hermitian observable')
    return real

def main():
    start = time.perf_counter()
    checks = []
    def check(name, got, expected):
        residual = add(got, scale(expected, -1))
        checks.append(dict(name=name, passed=not residual, exact_residual=show(residual)))
    results = {}
    for records, carrier, label in ((1, False, 'one_record'), (2, False, 'P0'), (2, True, 'P1_full')):
        vec, ops = build(records, carrier)
        series = {n: expectation(vec, n, ops[0]) for n in range(7)}
        check(label+':n0', series[0], {})
        for n in (1, 3, 5): check(label+':odd'+str(n), series[n], {})
        check(label+':n2', series[2], power(h, 2))
        if not carrier:
            check(label+':n4', series[4], scale(mul(power(h, 2), add(power(k, 2), scale(power(h, 2), 4))), F(-1, 12)))
        results[label] = dict(series=series)
        if records == 2:
            R2 = add(mul(g, expectation(vec, 2, ops[1])), scale(mul(eps, expectation(vec, 2, ops[2])), F(1, 2)))
            R4 = add(mul(g, expectation(vec, 4, ops[1])), scale(mul(eps, expectation(vec, 4, ops[2])), F(1, 2)))
            I3, I5 = [scale(expectation(vec, n, ops[3]), F(-1, 2)) for n in (3, 5)]
            gap2 = add(power(eps, 2), scale(power(g, 2), 4))
            check(label+':clock_R2', R2, scale(mul(g, gap2), F(-1, 2)))
            check(label+':clock_I3', I3, scale(mul(g, gap2), F(-1, 6)))
            delta_R4 = add(R4, scale(mul(g, power(gap2, 2)), F(-1, 24)))
            delta_I5 = add(I5, scale(mul(g, power(gap2, 2)), F(-1, 120)))
            theta5_over_gap = divide_variable(add(delta_I5, scale(delta_R4, -1)), 1)
            expected = scale(mul(mul(lam, power(h, 2)), add(scale(eps, F(1, 10)), scale(lam, F(1, 15)))), -1)
            check(label+':clock_phase5_over_gap', theta5_over_gap, expected)
            results[label]['theta5_over_gap'] = theta5_over_gap
    p0, p1 = results['P0']['series'], results['P1_full']['series']
    for n in (2, 4, 6):
        bands = scale(add(substitute(p0[n], 2, add(k, j, t)), substitute(p0[n], 2, add(k, j, scale(t, -1)))), F(1, 2))
        check('P1:independent_bands:'+str(n), p1[n], bands)
    contrast4 = add(p1[4], scale(p0[4], -1))
    check('loading_quartic', contrast4, scale(mul(power(h, 2), add(scale(mul(k, j), 2), power(j, 2), power(t, 2))), F(-1, 12)))
    contrast6 = add(p1[6], scale(p0[6], -1))
    double6 = add(contrast6, scale(substitute(contrast6, 4, {}), -1))
    check('feedback_loading_sixth', double6, scale(mul(mul(power(h, 2), power(g, 2)), mul(j, lam)), F(1, 10)))
    r6 = results['one_record']['series'][6]
    check('one_record_feedback_sixth', add(r6, scale(substitute(r6, 4, {}), -1)),
          mul(mul(power(h, 2), power(g, 2)), add(scale(mul(k, lam), F(1, 20)), scale(power(lam, 2), F(-1, 45)))))
    passed = all(c['passed'] for c in checks)
    output = dict(status='COMPLETE' if passed else 'FAILED_IDENTITIES', checks=checks,
                  check_counts=dict(total=len(checks), passed=sum(c['passed'] for c in checks)),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  method='Exact Fraction polynomial identities; no floating point, fits or trajectories',
                  variable_order=NAMES, time_variable='tau/hbar',
                  series={label: {str(n): show(p) for n, p in value['series'].items()} for label, value in results.items()},
                  loading_quartic=show(contrast4), feedback_loading_sixth=show(double6),
                  clock_phase5_over_gap={label: show(results[label]['theta5_over_gap']) for label in ('P0', 'P1_full')},
                  qualifications=dict(local_cell_not_gravity=True, physical_volume=False,
                                      operational_clock_requires_g_nonzero=True, external_q=False,
                                      no_fitted_dark_source=True, finite_time_remainder_bound=False),
                  runtime=dict(wall_seconds=time.perf_counter()-start,
                               max_rss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                               max_rss_units='bytes' if sys.platform == 'darwin' else 'KiB'))
    print(json.dumps(output, separators=(',', ':')))
    return 0 if passed else 1

if __name__ == '__main__':
    if sys.argv[1:] != ['--run']:
        raise SystemExit('Explicit --run required; symbolic coefficients only')
    raise SystemExit(main())
