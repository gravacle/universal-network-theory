"""Exact Gaussian-rational short-time series of diagonal reads for the 0114 arms.
Own code; imports only the reviewer's own model file in this directory."""
import json, sys, os
from fractions import Fraction as F
from math import factorial
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p47_c2sham_0114_model import G, params, column, U, pc

S0 = (0, 3, 1, 3, 0, 3)
S1 = U(S0)
assert S1 == (0, 3, 2, 3, 0, 3), S1

OBS = {
    'q0': lambda s: (s[3] >> 0) & 1, 'q1': lambda s: (s[3] >> 1) & 1,
    'q2': lambda s: (s[3] >> 2) & 1, 'q3': lambda s: (s[3] >> 3) & 1,
    'S0': lambda s: (s[5] >> 0) & 1, 'S1': lambda s: (s[5] >> 1) & 1,
    'R0': lambda s: (s[4] >> 0) & 1, 'p0': lambda s: (s[2] >> 0) & 1,
    'p1': lambda s: (s[2] >> 1) & 1, 'Nc': lambda s: pc(s[2]),
    'Born': lambda s: s[0],
}


def apply(vec, P, cache):
    out = {}
    for st, w in vec.items():
        col = cache.get(st)
        if col is None:
            col = cache[st] = column(st, P)
        for tg, a in col.items():
            out[tg] = out.get(tg, G()) + a * w
    return {k: v for k, v in out.items() if v}


def series(z, P, N):
    cache = {}
    vs = [{z: G(1)}]
    for _ in range(N):
        vs.append(apply(vs[-1], P, cache))
    hb = P['hbar']
    ipow = [G(1), G(0, 1), G(-1), G(0, -1)]
    res = {}
    for name, f in OBS.items():
        cs = []
        for k in range(N + 1):
            tot = G()
            for m in range(k + 1):
                n = k - m
                a, b = vs[m], vs[n]
                small, big = (a, b) if len(a) < len(b) else (b, a)
                inner = G()
                for w in small:
                    if w in big:
                        o = f(w)
                        if o:
                            inner = inner + a[w].conj() * b[w] * o
                coef = ipow[m % 4] * ipow[(3 * n) % 4] * G(F(1, factorial(m) * factorial(n)))
                tot = tot + coef * inner
            tot = tot * G(1 / hb ** k)
            assert tot.im == 0, (name, k, tot)
            cs.append(tot.re)
        res[name] = cs
    return res, [len(v) for v in vs]


def run(label, P, N=6):
    A, sizes = series(S0, P, N)
    A1, _ = series(S1, P, N)
    B = {k: [(x + y) / 2 for x, y in zip(A[k], A1[k])] for k in A}
    D = {k: [x - y for x, y in zip(A[k], B[k])] for k in A}
    g, hb = P['g'], P['hbar']
    k0 = P['kappa'][0]
    pred_q = -g * g / (2 * hb * hb)
    pred_S = -(k0.re ** 2 + k0.im ** 2) / (2 * hb * hb)
    out = dict(label=label, sizes_H_power_support=sizes,
               g=str(g), hbar=str(hb), kappa0=repr(k0), epsilon_B=repr(P['epsilon_B']),
               armA={k: [str(x) for x in v] for k, v in A.items()},
               armB={k: [str(x) for x in v] for k, v in B.items()},
               Delta={k: [str(x) for x in v] for k, v in D.items()},
               predicted_Dq0_tau2=str(pred_q), predicted_DS0_tau2=str(pred_S),
               checks=dict(
                   Dq0_c1_zero=D['q0'][1] == 0,
                   Dq0_c2_matches=D['q0'][2] == pred_q,
                   Dq1_c2_opposite=D['q1'][2] == -pred_q,
                   DS0_c2_matches=D['S0'][2] == pred_S,
                   DS1_c2_opposite=D['S1'][2] == -pred_S,
                   Dq0_plus_Dq1_all_orders_zero=all(D['q0'][k] + D['q1'][k] == 0 for k in range(N + 1)),
                   Dq2_plus_Dq3_all_orders_zero=all(D['q2'][k] + D['q3'][k] == 0 for k in range(N + 1)),
                   Dq0_c3=str(D['q0'][3]), DS0_c3=str(D['S0'][3]),
                   Dq0_c5=str(D['q0'][5]) if N >= 5 else None,
                   DS0_c5=str(D['S0'][5]) if N >= 5 else None,
                   armA_q1_c2=str(A['q1'][2]), armA_S1_c2=str(A['S1'][2]),
                   R0_plus_S0_constant=all((A['R0'][k] + A['S0'][k]) == (1 if k == 0 else 0) for k in range(N + 1)),
               ))
    return out


if __name__ == '__main__':
    results = []
    results.append(run('complex_kappa_epsB_hbar3/2', params()))
    results.append(run('real_params_hbar3/2', params(real_only=True)))
    results.append(run('complex_alt_g-2_hbar1/3', params(g=F(-2), hbar=F(1, 3),
                       kappa01=G(F(-3, 5), F(7, 4)), kappa23=G(F(1, 2), F(-1, 3)), epsB=G(F(-5, 6), F(1, 4)))))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p47_c2sham_0114_exact_series_out.json')
    with open(out, 'w') as fh:
        json.dump(results, fh, indent=1)
    for r in results:
        print(r['label'], r['sizes_H_power_support'])
        print('  Dq0', r['Delta']['q0'][:6], 'pred c2', r['predicted_Dq0_tau2'])
        print('  DS0', r['Delta']['S0'][:6], 'pred c2', r['predicted_DS0_tau2'])
        print('  checks', r['checks'])
