"""Higher odd orders (to tau^11) for C2-symmetric complex Born conjugate-pair phases,
arm A diagonal reads q0,S0 from s0, to test whether evenness can fail inside the C2 class."""
import json, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p47_c2sham_0114_model import G, params
from p47_c2sham_0114_exact_series import series, S0, S1
N = 11
z = G(F(3, 5), F(4, 5)); w = G(F(5, 13), F(-12, 13))
P = params(born_phase=[z, z.conj(), w, w.conj(), G(0, 1), G(0, -1), G(1), G(1)])
A, sizes = series(S0, P, N); A1, _ = series(S1, P, N)
res = dict(sizes=sizes, q0={j: str(A['q0'][j]) for j in range(N + 1)}, S0={j: str(A['S0'][j]) for j in range(N + 1)},
           q2={j: str(A['q2'][j]) for j in range(N + 1)}, q3={j: str(A['q3'][j]) for j in range(N + 1)},
           Dq0={j: str(A['q0'][j] - (A['q0'][j] + A1['q0'][j]) / 2) for j in range(N + 1)})
print(json.dumps(res)[:3000])
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p47_c2sham_0114_odd_terms_deep_out.json'), 'w'), indent=1)
