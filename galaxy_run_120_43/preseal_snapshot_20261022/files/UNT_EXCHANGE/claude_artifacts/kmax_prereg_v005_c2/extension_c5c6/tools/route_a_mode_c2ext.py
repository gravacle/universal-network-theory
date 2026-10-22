"""Post-hoc (read-only) analysis of the saved route-A relaxed iterates g_n (iteration_<n>/START.json gas_fourier_J blobs)
of computed prefixes: step d_n = g_{n+1} - g_n (= relaxation * (U(g_n) - g_n), relaxation 0.5), the norm ratio
|d_{n+1}|/|d_n|, the signed projection mu_n = Re<d_n, d_{n+1}> / |d_n|^2 and cos(d_n, d_{n+1}).  For a single dominant real
mode of the relaxed map, mu_n -> its eigenvalue m = 1 - 0.5 (1 - lam) (lam: eigenvalue of the unrelaxed update U);
mu > 0 with cos -> 1: monotone slow mode (more iterations converge it while m < 1); cos -> -1: oscillating mode.
Prints JSON and writes analysis/ROUTE_A_MODE_V001.json (must not exist).  numpy only."""
import json
import sys
from pathlib import Path

import numpy as np

R = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
RUNS = {'G2': 'A2_ANCHOR_F10_RUN_V001', 'G3': 'KMAX_A2F10_C3_V005_RUN_V001', 'G4': 'KMAX_A2F10_C4_V005_RUN_V001', 'GR': 'KMAX_A2F10_R_V005_RUN_V001'}


def main():
    out = {'schema': 'UNT_ROUTE_A_MODE_C2EXT_V001', 'runs': {}}
    for g, run in RUNS.items():
        cp = R / run / 'stages/01_route_a/checkpoint'
        its = sorted(cp.glob('iteration_*'))
        prev_g = prev_d = None
        rows = []
        for it in its:
            st = json.loads((it / 'START.json').read_text())
            gi = np.load(cp / st['gas_fourier_J']['blob'], allow_pickle=False).reshape(-1)
            if prev_g is not None:
                d = gi - prev_g
                if prev_d is not None:
                    nd0, nd1 = np.linalg.norm(prev_d), np.linalg.norm(d)
                    ip = np.vdot(prev_d, d)
                    rows.append({'n': len(rows), 'ratio': float(nd1 / nd0), 'mu': float(ip.real / nd0 ** 2),
                                 'cos': float(ip.real / (nd0 * nd1)), 'imag_over_norms': float(ip.imag / (nd0 * nd1))})
                prev_d = d
            prev_g = gi
            del st
        out['runs'][g] = {'run': run, 'iterations': len(its), 'steps_between_starts': len(its) - 1, 'pairs': rows}
        print(g, [(round(r['ratio'], 3), round(r['mu'], 3), round(r['cos'], 3)) for r in rows], flush=True)
    with open(HERE / 'analysis/ROUTE_A_MODE_V001.json', 'x') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
