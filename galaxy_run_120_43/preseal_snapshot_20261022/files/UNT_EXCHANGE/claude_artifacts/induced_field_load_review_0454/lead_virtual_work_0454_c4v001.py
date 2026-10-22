import sys; sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')
import numpy as np
# lead_virtual_work_0454_c4v001.py -- Claude4 lead: direct REAL virtual-work fixture for the frozen 0453 load.
# Real potential dPhi(R,phi,z) = sum_m' 2 Re[Phi_m'(R,z) exp(i m' phi)] on 16 angles; analytic gradient incl. (1/R) d_phi;
# root-style inputs grad_c = fft(g_c)[m]/16. Check W_real = sum_p w_p sum_j (2pi/16) xi.F == 4 pi Re(y^H delta_b * s).
import hashlib, importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, 'lead_copy_7f68fba1', 'induced_field_weak_load_c3v001.py'); MOD_SHA = '7f68fba13d93d506b7d1db1e7818f247992d56bb7930190da7d6f3524f0cfb64'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); assert sha(MOD) == MOD_SHA
s_ = importlib.util.spec_from_file_location('c3_0453', MOD); M = importlib.util.module_from_spec(s_); s_.loader.exec_module(M)
f = M.induced_field_weak_load
phi = 2 * np.pi * np.arange(16) / 16
rep = {'python': sys.version.split()[0], 'numpy': np.__version__, 'cases': []}
worst_vw, worst_alt_gap = 0.0, np.inf
for structure in ('general', 'root'):
    for m in range(1, 7):
        for seed in range(3):
            rng = np.random.default_rng(31 + 100 * m + 7 * seed + (0 if structure == 'general' else 999)); n, k = 11, 4
            R = rng.uniform(0.4, 2.5, n); z = rng.uniform(-0.6, 0.6, n); w = rng.uniform(0.05, 1, n); rho = rng.uniform(0.3, 2, n)
            modes = sorted(set([m, 1, 3, 7]))
            coef = {mm: rng.normal(size=4) + 1j * rng.normal(size=4) for mm in modes}
            Phi = lambda mm: coef[mm][0] + coef[mm][1] * R ** 2 + coef[mm][2] * z + coef[mm][3] * R * z
            dPhi_R = lambda mm: 2 * coef[mm][1] * R + coef[mm][3] * z
            dPhi_z = lambda mm: coef[mm][2] + coef[mm][3] * R
            E = lambda mm: np.exp(1j * mm * phi)[None, :]
            gR = sum(2 * np.real(dPhi_R(mm)[:, None] * E(mm)) for mm in modes)                 # (n,16) real
            gP = sum(2 * np.real((1j * mm / R * Phi(mm))[:, None] * E(mm)) for mm in modes)     # (1/R) d_phi, real
            gZ = sum(2 * np.real(dPhi_z(mm)[:, None] * E(mm)) for mm in modes)
            grad = np.stack([np.fft.fft(g, axis=1)[:, m] / 16 for g in (gR, gP, gZ)], axis=1)   # root-style (n,3)
            if structure == 'general':
                c = lambda: rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k)); U = [c(), c(), c()]
            else:
                U = [rng.normal(size=(n, k)), 1j * rng.normal(size=(n, k)), rng.normal(size=(n, k))]
            s = float(rng.uniform(0.5, 3))
            out = f(m=m, U_R=U[0], U_phi=U[1], U_z=U[2], rho=rho, volume_weights=w, grad=grad, normalization_scale=s)
            db = out['delta_b']
            y = rng.normal(size=k) + 1j * rng.normal(size=k)
            xi = [2 * np.real((Uc @ y)[:, None] * E(m)) for Uc in U]                                # real displacement (n,16)
            F = [-rho[:, None] * g for g in (gR, gP, gZ)]                                            # real force density
            W_real = float(np.sum(w[:, None] * (2 * np.pi / 16) * sum(xc * Fc for xc, Fc in zip(xi, F))))
            pred = float(4 * np.pi * np.real(np.vdot(y, db) * s))
            err = abs(W_real - pred) / max(abs(W_real), 1e-300); worst_vw = max(worst_vw, err)
            # alternative conventions that must NOT match (each changes W prediction materially)
            alts = {'factor2': 2 * pred, 'two_pi': 2 * np.pi * pred, 'no_conj': float(4 * np.pi * np.real(np.vdot(y, -(U[0].T @ (w * rho * grad[:, 0]) + U[1].T @ (w * rho * grad[:, 1]) + U[2].T @ (w * rho * grad[:, 2]))))),
                    'extra_1_over_R': float(4 * np.pi * np.real(np.vdot(y, -(U[0].conj().T @ (w * rho * grad[:, 0]) + U[1].conj().T @ (w * rho * grad[:, 1] / R) + U[2].conj().T @ (w * rho * grad[:, 2]))))),
                    'sign': -pred}
            gap = min(abs(v - W_real) / abs(W_real) for v in alts.values()); worst_alt_gap = min(worst_alt_gap, gap)
            rep['cases'].append(dict(structure=structure, m=m, seed=seed, rel_err=err, min_alt_gap=gap))
rep['max_rel_err_virtual_work'] = worst_vw; rep['min_alternative_gap'] = worst_alt_gap; rep['n_cases'] = len(rep['cases'])
rep['module_sha256_after'] = sha(MOD); rep['pass'] = bool(worst_vw < 1e-12 and worst_alt_gap > 1e-3 and rep['module_sha256_after'] == MOD_SHA)
json.dump(rep, open(sys.argv[sys.argv.index('--out') + 1], 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k != 'cases'}, indent=1))
