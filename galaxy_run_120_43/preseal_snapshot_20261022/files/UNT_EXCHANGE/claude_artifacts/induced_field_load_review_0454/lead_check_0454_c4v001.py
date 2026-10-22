import sys; sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')
import numpy as np
# lead_check_0454_c4v001.py -- Claude4 lead: exact equivalence of the 0453 induced load with the frozen 0439 forcing slice.
import copy, hashlib, importlib.util, json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
MOD = glob.glob(os.path.join(HERE, 'lead_copy_*', 'induced_field_weak_load_c3v001.py'))
MOD = sorted(MOD, key=os.path.getmtime)[-1] if len(sys.argv) < 4 else sys.argv[3]
E = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/c3_snapshot_8632bda6/weak_euler_assembly_c3v001.py'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
assert sha(E) == '8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da'
mod_sha = sha(MOD); f = load(MOD, 'c3_0453').induced_field_weak_load; eul = load(E, 'eul0439').assemble_weak_euler
rep = {'python': sys.version.split()[0], 'numpy': np.__version__, 'module': MOD, 'module_sha256': mod_sha, 'checks': []}
def add(name, ok, **kw): rep['checks'].append(dict(check=name, ok=bool(ok), **kw))
bit_all, max_diff, n_cases, mut_ok, alias_ok, comp_ok = True, 0.0, 0, True, True, True
for structure in ('general', 'root'):
    for (n, k) in [(7, 3), (4, 4), (9, 1), (1, 1), (16, 5)]:
        for m in range(1, 7):
            rng = np.random.default_rng(1000 + 10 * n + k + 100 * m + (0 if structure == 'general' else 5000))
            c = lambda: rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k))
            if structure == 'general': U_R, U_phi, U_z = c(), c(), c()
            else: U_R, U_phi, U_z = rng.normal(size=(n, k)), 1j * rng.normal(size=(n, k)), rng.normal(size=(n, k))
            rho = rng.uniform(0.5, 2, n); w = rng.uniform(0.1, 1, n); s = float(rng.uniform(0.5, 4))
            grad = rng.normal(size=(n, 3)) + 1j * rng.normal(size=(n, 3))
            kw = dict(m=m, U_R=U_R, U_phi=U_phi, U_z=U_z, rho=rho, volume_weights=w, grad=grad, normalization_scale=s)
            before = copy.deepcopy(kw); out = f(**kw)
            mut_ok &= all(np.array_equal(kw[q], before[q]) if isinstance(kw[q], np.ndarray) else kw[q] == before[q] for q in kw)
            alias_ok &= not any(np.shares_memory(out[key], kw[q]) for key in ('delta_b', 'load_R', 'load_phi', 'load_z') for q in kw if isinstance(kw[q], np.ndarray))
            # the 0439 b for matching inputs (all other Euler inputs arbitrary but valid; b does not depend on them)
            R = rng.uniform(0.5, 3, n); P = rng.uniform(0.5, 2, n)
            e = eul(R=R, rho=rho, P=P, K_R=np.zeros(n), K_z=np.zeros(n), P_R=np.zeros(n), P_z=np.zeros(n), Omega=np.ones(n),
                    Omega_R=np.zeros(n), Omega_z=np.zeros(n), volume_weights=w, U_R=U_R, U_phi=U_phi, U_z=U_z,
                    divU=np.zeros((n, k)), G=np.zeros((n, k)), f_R=grad[:, 0], f_phi=grad[:, 1], f_z=grad[:, 2],
                    m=m, gamma=5 / 3, normalization_scale=s, provenance='claude4-0454-synthetic')
            bit = bool(np.array_equal(out['delta_b'], e['b'])); bit_all &= bit
            max_diff = max(max_diff, float(np.max(np.abs(out['delta_b'] - e['b'])) / np.max(np.abs(e['b']))))
            lit = -(U_R.conj().T @ (w * rho * grad[:, 0]) + U_phi.conj().T @ (w * rho * grad[:, 1]) + U_z.conj().T @ (w * rho * grad[:, 2])) / s
            comp = out['load_R'] + out['load_phi'] + out['load_z']
            comp_ok &= bool(np.allclose(comp, out['delta_b'], rtol=1e-13, atol=0) and np.allclose(lit, out['delta_b'], rtol=1e-13, atol=0)
                            and out['delta_b'].shape == (k,) and out['delta_b'].dtype == np.complex128)
            n_cases += 1
add('delta_b_bitwise_equal_frozen_0439_b', bit_all, cases=n_cases, max_rel_diff=max_diff)
add('component_loads_sum_and_literal_formula', comp_ok)
add('inputs_unmodified', mut_ok); add('outputs_not_aliasing_inputs', alias_ok)
# conjugation / sign / normalization / no-2pi / no-extra-1/R sensitivity on root-structured inputs vs 0439 b
rng = np.random.default_rng(7); n, k = 8, 3
U_R, U_phi, U_z = rng.normal(size=(n, k)), 1j * rng.normal(size=(n, k)), rng.normal(size=(n, k))
rho = rng.uniform(0.5, 2, n); w = rng.uniform(0.1, 1, n); grad = rng.normal(size=(n, 3)) + 1j * rng.normal(size=(n, 3)); R = rng.uniform(0.5, 3, n)
out = f(m=2, U_R=U_R, U_phi=U_phi, U_z=U_z, rho=rho, volume_weights=w, grad=grad, normalization_scale=1.0)['delta_b']
alts = {'no_conj_on_U_phi': -(U_R.T @ (w * rho * grad[:, 0]) + U_phi.T @ (w * rho * grad[:, 1]) + U_z.T @ (w * rho * grad[:, 2])),
        'extra_2pi': -2 * np.pi * (U_R.conj().T @ (w * rho * grad[:, 0]) + U_phi.conj().T @ (w * rho * grad[:, 1]) + U_z.conj().T @ (w * rho * grad[:, 2])),
        'extra_1_over_R_on_grad_phi': -(U_R.conj().T @ (w * rho * grad[:, 0]) + U_phi.conj().T @ (w * rho * grad[:, 1] / R) + U_z.conj().T @ (w * rho * grad[:, 2])),
        'sign_flipped': (U_R.conj().T @ (w * rho * grad[:, 0]) + U_phi.conj().T @ (w * rho * grad[:, 1]) + U_z.conj().T @ (w * rho * grad[:, 2]))}
add('distinguishes_conventions', all(float(np.max(np.abs(out - v))) > 1e-3 * float(np.max(np.abs(out))) for v in alts.values()),
    min_rel_gap=min(float(np.max(np.abs(out - v)) / np.max(np.abs(out))) for v in alts.values()))
# fail-closed probes
base = dict(m=1, U_R=U_R, U_phi=U_phi, U_z=U_z, rho=rho, volume_weights=w, grad=grad, normalization_scale=1.0)
def rej(**chg):
    try: f(**dict(base, **chg)); return False
    except (ValueError, TypeError): return True
probes = {'m0': rej(m=0), 'm7': rej(m=7), 'm_bool': rej(m=True), 'm_npint': rej(m=np.int64(2)), 'rho_zero': rej(rho=np.where(np.arange(n) == 0, 0.0, rho)),
          'w_negative': rej(volume_weights=-w), 'rho_complex': rej(rho=rho + 0j), 'grad_transposed': rej(grad=grad.T), 'grad_nan': rej(grad=np.where(np.arange(n)[:, None] == 1, np.nan, grad)),
          'map_1d': rej(U_R=U_R[:, 0]), 'map_mismatch': rej(U_z=U_z[:, :2]), 'norm_zero': rej(normalization_scale=0.0), 'norm_bool': rej(normalization_scale=True),
          'norm_inf': rej(normalization_scale=float('inf')), 'overflow': rej(grad=np.full((n, 3), 1e308 + 0j), rho=np.full(n, 1e300))}
add('fail_closed_probes', all(probes.values()), probes=probes)
try:
    f(1, U_R=U_R, U_phi=U_phi, U_z=U_z, rho=rho, volume_weights=w, grad=grad, normalization_scale=1.0); pos = False
except TypeError: pos = True
add('positional_rejected_TypeError', pos)
real_ok = bool(np.array_equal(f(**base)['delta_b'], f(**dict(base, U_R=U_R.astype(complex), U_z=U_z.astype(complex)))['delta_b']))
add('real_dtype_maps_bitwise_equal_complex', real_ok)
rep['module_sha256_after'] = sha(MOD); rep['all_ok'] = all(c['ok'] for c in rep['checks']) and rep['module_sha256_after'] == mod_sha
json.dump(rep, open(sys.argv[sys.argv.index('--out') + 1], 'w'), indent=1, default=str)
print(json.dumps({'python': rep['python'], 'numpy': rep['numpy'], 'module_sha256': mod_sha, 'all_ok': rep['all_ok'],
                  'checks': [{k: v for k, v in c.items() if k != 'probes'} for c in rep['checks']]}, indent=1, default=str))
