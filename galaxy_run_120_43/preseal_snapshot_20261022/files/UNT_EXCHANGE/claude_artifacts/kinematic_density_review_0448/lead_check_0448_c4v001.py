import sys; sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')
import numpy as np
# lead_check_0448_c4v001.py -- Claude4 lead check for 0448 on the frozen 0447 module (synthetic only).
import copy, hashlib, importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(HERE, 'lead_copy_a8b2d578', 'kinematic_density_c3v001.py'); K_SHA = 'a8b2d578fbb0c41a02dac6a5fcfb3e5333ef3a998090cc1fc97c1117b1aaea22'
E = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/c3_snapshot_8632bda6/weak_euler_assembly_c3v001.py'; E_SHA = '8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
assert sha(K) == K_SHA and sha(E) == E_SHA
kin = load(K, 'kin0447').kinematic_density_map; eul = load(E, 'eul0439').assemble_weak_euler
rep = {'python': sys.version.split()[0], 'numpy': np.__version__, 'checks': []}
def add(name, ok, **kw): rep['checks'].append(dict(check=name, ok=bool(ok), **kw))
relerr = lambda a, b: float(np.max(np.abs(a - b)) / max(float(np.max(np.abs(b))), 1e-300))

# C1 analytic nonconstant density vs 4th-order FD of -div(rho xi) (cylindrical, exp(+i m phi))
worst = 0.0
for m in range(1, 7):
    rng = np.random.default_rng(100 + m); n, k = 9, 3
    R = rng.uniform(0.6, 2.0, n); z = rng.uniform(-0.7, 0.7, n)
    r0, a, h2 = 1.3, 0.4, 0.5
    rho_f = lambda R, z: r0 * (1 + a * R ** 2) * np.exp(-z ** 2 / h2)
    cR = rng.normal(size=(3, k)) + 1j * rng.normal(size=(3, k)); cP = rng.normal(size=(2, k)) + 1j * rng.normal(size=(2, k)); cZ = rng.normal(size=(3, k)) + 1j * rng.normal(size=(3, k))
    xR = lambda R, z: (cR[0] + cR[1] * z[:, None] + cR[2] * R[:, None]) * R[:, None] ** (m - 1)
    xP = lambda R, z: 1j * (cP[0] + cP[1] * (R * z)[:, None]) * R[:, None] ** (m - 1)
    xZ = lambda R, z: (cZ[0] + cZ[1] * R[:, None] + cZ[2] * z[:, None] ** 2) * R[:, None] ** m
    hh = 1e-3
    d = lambda f, dR, dz: (-f(R + 2 * dR, z + 2 * dz) + 8 * f(R + dR, z + dz) - 8 * f(R - dR, z - dz) + f(R - 2 * dR, z - 2 * dz)) / (12 * hh)
    Rc = R[:, None]
    divxi = d(lambda R, z: R[:, None] * xR(R, z), hh, 0) / Rc + 1j * m * xP(R, z) / Rc + d(xZ, 0, hh)
    rho = rho_f(R, z); rho_R = r0 * 2 * a * R * np.exp(-z ** 2 / h2); rho_z = -2 * z / h2 * rho
    exact = -(d(lambda R, z: R[:, None] * rho_f(R, z)[:, None] * xR(R, z), hh, 0) / Rc + 1j * m * rho[:, None] * xP(R, z) / Rc
              + d(lambda R, z: rho_f(R, z)[:, None] * xZ(R, z), 0, hh))
    G = kin(rho=rho, rho_R=rho_R, rho_z=rho_z, U_R=xR(R, z), U_z=xZ(R, z), divU=divxi)
    worst = max(worst, relerr(G, exact))
add('C1_analytic_nonconstant_density_vs_FD_minus_div_rho_xi', worst < 1e-9, max_rel_err=worst, cases='m=1..6, 9 points x 3 columns, 4th-order FD h=1e-3')

# C2 exact transcription (bitwise), shapes incl. square and nfree=1; C3 dtype; C4 no mutation / fresh array
bit_ok, dtype_ok, mut_ok, alias_ok = True, True, True, True
for (n, k) in [(7, 3), (4, 4), (9, 1), (1, 1)]:
    rng = np.random.default_rng(10 * n + k)
    kw = dict(rho=rng.uniform(0.5, 2, n), rho_R=rng.normal(size=n), rho_z=rng.normal(size=n),
              U_R=rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k)), U_z=rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k)),
              divU=rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k)))
    before = copy.deepcopy(kw); G = kin(**kw)
    lit = -kw['rho'][:, None] * kw['divU'] - kw['rho_R'][:, None] * kw['U_R'] - kw['rho_z'][:, None] * kw['U_z']
    bit_ok &= bool(np.array_equal(G, lit)) and G.dtype == np.complex128 and G.shape == (n, k)
    mut_ok &= all(np.array_equal(kw[q], before[q]) for q in kw)
    alias_ok &= not any(np.shares_memory(G, kw[q]) for q in kw)
    real = dict(kw, U_R=kw['U_R'].real.copy(), U_z=kw['U_z'].real.copy(), divU=kw['divU'].real.astype(np.complex128))
    real_c = dict(real, U_R=real['U_R'].astype(np.complex128), U_z=real['U_z'].astype(np.complex128))
    dtype_ok &= bool(np.array_equal(kin(**real), kin(**real_c)))
add('C2_bitwise_equal_literal_contract_formula', bit_ok); add('C3_real_dtype_maps_bitwise_equal_complex', dtype_ok)
add('C4_inputs_unmodified', mut_ok); add('C4_output_fresh_array_no_aliasing', alias_ok)

# C5 fail-closed probes
n, k = 5, 2; rng = np.random.default_rng(5)
base = dict(rho=rng.uniform(0.5, 2, n), rho_R=rng.normal(size=n), rho_z=rng.normal(size=n),
            U_R=rng.normal(size=(n, k)) + 0j, U_z=rng.normal(size=(n, k)) + 0j, divU=rng.normal(size=(n, k)) + 0j)
def probe(name, expect, **chg):
    kw = dict(base, **chg)
    try: kin(**kw); got = 'accept'
    except (TypeError, ValueError) as e: got = 'reject:' + type(e).__name__
    add('C5_' + name, got.startswith(expect), expected=expect, got=got)
probe('rho_zero', 'reject', rho=np.where(np.arange(n) == 2, 0.0, base['rho']))
probe('rho_negative', 'reject', rho=-base['rho'])
probe('rho_R_negative_accepted', 'accept', rho_R=-np.abs(base['rho_R']) - 1)
probe('rho_z_complex_rejected', 'reject', rho_z=base['rho_z'] + 0j)
probe('U_z_nan', 'reject', U_z=np.where(np.arange(n)[:, None] == 1, np.nan, base['U_z']))
probe('divU_inf', 'reject', divU=np.full((n, k), np.inf + 0j))
probe('divU_shape_mismatch', 'reject', divU=base['divU'][:, :1])
probe('rho_R_wrong_length', 'reject', rho_R=base['rho_R'][:-1])
probe('U_R_bool_dtype', 'reject', U_R=np.ones((n, k), dtype=bool))
probe('overflow_to_nonfinite', 'reject', rho=np.full(n, 1e308), divU=np.full((n, k), 1e308 + 0j))
for name, call in [('positional', lambda: kin(base['rho'], rho_R=base['rho_R'], rho_z=base['rho_z'], U_R=base['U_R'], U_z=base['U_z'], divU=base['divU'])),
                   ('missing_divU', lambda: kin(**{q: v for q, v in base.items() if q != 'divU'})),
                   ('unknown_kwarg', lambda: kin(U_phi=base['U_R'], **base))]:
    try: call(); got = 'accept'
    except TypeError: got = 'reject:TypeError'
    except ValueError: got = 'reject:ValueError'
    add('C5_' + name, got == 'reject:TypeError', expected='reject:TypeError', got=got)

# C6 EOS gradients (provider L44-46 form, K_z=0): PM(G=Gkin) == -gamma P divU - (P_R U_R + P_z U_z)
# C7 Hermiticity of A(G=Gkin): A - A^H == U_R^H D(q) U_z - U_z^H D(q) U_R, q = w[2 rho R Om Om_z + (K_R/K) P_z/gamma]
g = 5.0 / 3.0; w6 = w7 = w7h = 0.0
for seed in range(6):
    for m in range(1, 7):
        rng = np.random.default_rng(700 + 10 * seed + m); n, k = 8, 4
        R = rng.uniform(0.5, 3, n); rho = rng.uniform(0.5, 2, n); Kc = rng.uniform(0.5, 2, n); P = Kc * rho ** g
        K_R = rng.normal(size=n); K_z = np.zeros(n); P_R = rng.normal(size=n); P_z = rng.normal(size=n)
        rho_R = (P_R - rho ** g * K_R) / (g * P / rho); rho_z = P_z / (g * P / rho)
        Om = rng.uniform(0.3, 1.5, n) * rng.choice([-1, 1], n); Om_R = rng.normal(size=n)
        c = lambda: rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k))
        U_R, U_phi, U_z, divU = c(), c(), c(), c(); w = rng.uniform(0.1, 1, n)
        Gk = kin(rho=rho, rho_R=rho_R, rho_z=rho_z, U_R=U_R, U_z=U_z, divU=divU)
        for tw in (False, True):
            Om_z = (-(K_R / Kc) * P_z / (g * rho)) / (2 * R * Om) if tw else rng.normal(size=n)
            out = eul(R=R, rho=rho, P=P, K_R=K_R, K_z=K_z, P_R=P_R, P_z=P_z, Omega=Om, Omega_R=Om_R, Omega_z=Om_z,
                      volume_weights=w, U_R=U_R, U_phi=U_phi, U_z=U_z, divU=divU, G=Gk, f_R=np.zeros(n), f_phi=np.zeros(n),
                      f_z=np.zeros(n), m=m, gamma=g, normalization_scale=1.0, provenance='claude4-0448-synthetic')
            PMx = -g * P[:, None] * divU - (P_R[:, None] * U_R + P_z[:, None] * U_z)
            w6 = max(w6, relerr(out['PM'], PMx))
            A = out['A']; q = w * (2 * rho * R * Om * Om_z + (K_R / Kc) * P_z / g)
            pred = U_R.conj().T @ (q[:, None] * U_z) - U_z.conj().T @ (q[:, None] * U_R)
            if tw: w7h = max(w7h, float(np.max(np.abs(A - A.conj().T)) / np.max(np.abs(A))))
            else: w7 = max(w7, relerr(A - A.conj().T, pred))
add('C6_PM_with_Gkin_equals_minus_gammaP_divU_minus_xi_grad_P', w6 < 1e-12, max_rel_err=w6)
add('C7_antiHermitian_part_matches_thermal_wind_imbalance_formula', w7 < 1e-12, max_rel_err=w7)
add('C7_A_Hermitian_when_fixed_K_thermal_wind_holds', w7h < 1e-13, max_rel_antiHermitian=w7h)
rep['module_sha256_after'] = sha(K); rep['euler_sha256_after'] = sha(E)
rep['all_ok'] = all(cc['ok'] for cc in rep['checks']) and rep['module_sha256_after'] == K_SHA
json.dump(rep, open(sys.argv[sys.argv.index('--out') + 1], 'w'), indent=1)
print(json.dumps({'python': rep['python'], 'numpy': rep['numpy'], 'all_ok': rep['all_ok'],
                  'failed': [cc for cc in rep['checks'] if not cc['ok']],
                  'numbers': {cc['check']: cc.get('max_rel_err', cc.get('max_rel_antiHermitian')) for cc in rep['checks'] if ('max_rel_err' in cc or 'max_rel_antiHermitian' in cc)},
                  'n_checks': len(rep['checks'])}, indent=1))
