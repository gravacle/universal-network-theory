"""Post-hoc two-mode fit of the saved route-A convergence records (residual/bound per iteration, COMPLETED.json) of the
computed prefixes G2 (K=2), G3 (K=3), G4 (K=4): r_n = A a^n + B b^n (least squares in log r over a grid of (a, b), A, B
by linear least squares).  The fitted (A, a, B, b) are extrapolated linearly in K to K=5, 6 and the first n with r_n <= 1
is reported (iteration index; the solver's loop runs n = 0 .. max_iterations-1).  A model, not a measurement of C5/C6:
it sets the registered route-A iteration budget and is reported, never used by the decision.
Writes analysis/ROUTE_A_PROJECTION2_V001.json (must not exist).  numpy only."""
import json
from pathlib import Path

import numpy as np

R = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
RUNS = {2: 'A2_ANCHOR_F10_RUN_V001', 3: 'KMAX_A2F10_C3_V005_RUN_V001', 4: 'KMAX_A2F10_C4_V005_RUN_V001'}


def seq(run):
    out = []
    for f in sorted((R / run / 'stages/01_route_a/checkpoint').glob('iteration_*/COMPLETED.json')):
        c = json.loads(f.read_text())
        out.append(float.fromhex(c['gas_fourier_residual_J'][1]) / float.fromhex(c['bound_J'][1]))
    return np.array(out)


def fit(r):
    n = np.arange(len(r))
    best = None
    for a in np.linspace(0.30, 0.60, 61):
        for b in np.linspace(0.40, 0.98, 117):
            if b <= a:
                continue
            M = np.stack([a ** n, b ** n], 1)
            coef, *_ = np.linalg.lstsq(M / r[:, None], np.ones(len(r)), rcond=None)  # relative least squares
            if np.any(coef < 0):
                continue
            m = M @ coef
            err = float(np.sum(np.log(m / r) ** 2))
            if best is None or err < best[0]:
                best = (err, float(a), float(b), float(coef[0]), float(coef[1]))
    return {'sse_log': best[0], 'a': best[1], 'b': best[2], 'A': best[3], 'B': best[4]}


def first_converged(A, a, B, b, nmax=64):
    for n in range(nmax):
        if A * a ** n + B * b ** n <= 1:
            return n
    return None


def main():
    data = {K: seq(run) for K, run in RUNS.items()}
    fits = {K: fit(r) for K, r in data.items()}
    out = {'schema': 'UNT_ROUTE_A_PROJECTION2_C2EXT_V001', 'measured': {K: [round(x, 4) for x in r] for K, r in data.items()},
           'fits': fits, 'measured_converged_at': {K: int(np.argmax(r <= 1)) for K, r in data.items()}}
    Ks = np.array([3, 4])
    proj = {}
    for K in (5, 6):
        p = {}
        for key in ('A', 'a', 'B', 'b'):
            y = np.array([fits[k][key] for k in (3, 4)])
            p[key] = float(y[1] + (y[1] - y[0]) * (K - 4))
        p['b'] = min(p['b'], 0.98)
        p['converged_at_iteration'] = first_converged(p['A'], p['a'], p['B'], p['b'])
        p['max_iterations_needed'] = None if p['converged_at_iteration'] is None else p['converged_at_iteration'] + 1
        proj[K] = p
    out['projection_linear_in_K_from_K3_K4'] = proj
    out['self_check_fit_reproduces_measured_convergence'] = {K: first_converged(f['A'], f['a'], f['B'], f['b']) for K, f in fits.items()}
    with open(HERE / 'analysis/ROUTE_A_PROJECTION2_V001.json', 'x') as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
