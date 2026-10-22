import sys; sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')
import numpy as np
# crosscheck_frozen_c4lead_v002_signs.py -- Claude4 lead: closes the two coverage notes from
# CROSSCHECK_C4_V001 on the frozen module: mixed/negative-sign Omega VALUE checks, and npoints>1 with nfree=1.
import hashlib, importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, 'c3_snapshot_8632bda6', 'weak_euler_assembly_c3v001.py'); MOD_SHA = '8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
assert sha(MOD) == MOD_SHA
mod = load(MOD, 'c3'); ora = load(os.path.join(HERE, 'algebra_oracle_h1v001.py'), 'ora'); ref = load(os.path.join(HERE, 'reference_weak_euler_h2v001.py'), 'ref')
def rel(a, b):
    a = np.asarray(a); b = np.asarray(b); return float(np.max(np.abs(a - b)) / max(float(np.max(np.abs(b))), 1e-300))
worst = {'ref': 0.0, 'ora': 0.0}; n_cases = 0
for seed in range(8):
    for (n, k) in [(7, 1), (16, 1), (5, 3), (4, 4)]:
        for m in range(1, 7):
            rng = np.random.default_rng(90000 + 100 * seed + 10 * n + k)
            sgn = {0: 1.0, 1: -1.0}.get(seed % 3, None)
            Om = rng.uniform(0.3, 1.5, n) * (sgn if sgn is not None else rng.choice([-1.0, 1.0], n))  # all+, all-, mixed
            R = rng.uniform(0.5, 3.0, n); rho = rng.uniform(0.5, 2.0, n); K = rng.uniform(0.5, 2.0, n)
            c = lambda: rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k))
            kw = dict(R=R, rho=rho, P=K * rho ** (5 / 3), K_R=rng.uniform(-1, 1, n), K_z=rng.uniform(-1, 1, n),
                      P_R=rng.uniform(-1, 1, n), P_z=rng.uniform(-1, 1, n), Omega=Om,
                      Omega_R=rng.uniform(-0.8, 0.8, n), Omega_z=rng.uniform(-0.8, 0.8, n), volume_weights=rng.uniform(0.1, 1, n),
                      U_R=c(), U_phi=c(), U_z=c(), divU=c(), G=c(),
                      f_R=rng.normal(size=n) + 1j * rng.normal(size=n), f_phi=rng.normal(size=n) + 1j * rng.normal(size=n),
                      f_z=rng.normal(size=n) + 1j * rng.normal(size=n), m=m, gamma=5 / 3, normalization_scale=float(rng.uniform(0.5, 4)),
                      provenance='claude4-sign-coverage')
            got = mod.assemble_weak_euler(**kw); exp = ref.reference_assemble(**kw)
            worst['ref'] = max(worst['ref'], max(rel(got[key], exp[key]) for key in ('A', 'b', 'E', 'PM', 'VR', 'VP', 'VZ')))
            A0, b0 = ora.oracle_A_b(**{q: v for q, v in kw.items() if q not in ('normalization_scale', 'provenance')})
            s = kw['normalization_scale']; worst['ora'] = max(worst['ora'], rel(got['A'], A0 / s), rel(got['b'], b0 / s))
            assert got['A'].shape == (k, k) and got['b'].shape == (k,) and got['VP'].shape == (n, k)
            n_cases += 1
out = {'python': sys.version.split()[0], 'numpy': np.__version__, 'cases': n_cases, 'omega_sign_modes': 'seed%3: 0 all-positive, 1 all-negative, 2 mixed',
       'shapes': '(7,1),(16,1),(5,3),(4,4)', 'max_rel_err_vs_H2_reference_all_outputs': worst['ref'], 'max_rel_err_vs_H1_oracle_A_b': worst['ora'],
       'module_sha256_after': sha(MOD), 'pass': bool(worst['ref'] <= 1e-12 and worst['ora'] <= 1e-12 and sha(MOD) == MOD_SHA)}
json.dump(out, open(sys.argv[sys.argv.index('--out') + 1], 'w'), indent=1); print(json.dumps(out, indent=1))
