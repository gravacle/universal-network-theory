"""Delimit the evenness caution: odd tau coefficients with (a) complex kappa/epsB and
phases 1 (expected zero: diagonal gauge), (b) C2-symmetric complex Born conjugate-pair
phases (allowed by the generalized symmetry). Own code."""
import json, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p47_c2sham_0114_model import G, params, U
from p47_c2sham_0114_exact_series import series, S0, S1
N = 7
z = G(F(3, 5), F(4, 5)); w = G(F(5, 13), F(-12, 13))
cases = {
 'phases1_complex_kappa_epsB': params(),
 'C2sym_complex_Born_pairs': params(born_phase=[z, z.conj(), w, w.conj(), G(0, 1), G(0, -1), G(1), G(1)],
                                    old_phase=[G(1), G(-1), G(-1), G(1)]),
}
out = {}
for k, P in cases.items():
    A, sizes = series(S0, P, N); A1, _ = series(S1, P, N)
    D = {o: [a - (a + b) / 2 for a, b in zip(A[o], A1[o])] for o in ('q0', 'S0')}
    out[k] = dict(sizes=sizes,
                  armA_q0_odd={j: str(A['q0'][j]) for j in (1, 3, 5, 7)},
                  armA_S0_odd={j: str(A['S0'][j]) for j in (1, 3, 5, 7)},
                  Dq0_odd={j: str(D['q0'][j]) for j in (1, 3, 5, 7)},
                  DS0_odd={j: str(D['S0'][j]) for j in (1, 3, 5, 7)},
                  Dq0_c2=str(D['q0'][2]), Dq0_c4=str(D['q0'][4]))
    print(k, json.dumps(out[k]))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p47_c2sham_0114_odd_terms_out.json'), 'w'), indent=1)
