import sys; sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')
import numpy as np
# lead_check_0451_c4v001.py -- Claude4 lead execution check of the frozen 0450 module on SYNTHETIC geometry.
# Pinned project helper modules are loaded by path only as pure-function dependencies (import-inert, verified by AST).
import hashlib, importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
CM = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/'
PINS = {'mod': (os.path.join(HERE, 'lead_copy_23bb22fb', 'annular_knot_maps_c3v001.py'), '23bb22fb94c3a6b39b84479a1c5e03812fbcdeaf6180ca85ddad083a3d3d92c4'),
        'scal1': (CM + 'owned_free_surface_32q8trial_maps_v001.py', '3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943'),
        'hel1': (CM + 'owned_32q8_regular_helicity_maps_v001.py', '280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6'),
        'bind': (CM + 'owned_body_fitted_displacement_binding_v002.py', '87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462')}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
for k, (p, h) in PINS.items(): assert sha(p) == h, k
mod, scal1, hel1, bind = (load(PINS[k][0], 'c4_' + k) for k in ('mod', 'scal1', 'hel1', 'bind'))
rep = {'python': sys.version.split()[0], 'numpy': np.__version__, 'checks': []}
def add(name, ok, **kw): rep['checks'].append(dict(check=name, ok=bool(ok), **kw))

def natural_cardinal(knots, at):
    """Independent natural cubic cardinal spline: values and d/dx at points `at` (own tridiagonal system)."""
    n = len(knots); h = np.diff(knots); V = np.zeros((len(at), n)); D = np.zeros((len(at), n))
    for j in range(n):
        y = np.zeros(n); y[j] = 1.0
        A = np.zeros((n, n)); r = np.zeros(n); A[0, 0] = A[-1, -1] = 1.0
        for i in range(1, n - 1):
            A[i, i - 1], A[i, i], A[i, i + 1] = h[i - 1] / 6, (h[i - 1] + h[i]) / 3, h[i] / 6
            r[i] = (y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]
        M = np.linalg.solve(A, r)  # second derivatives
        for q, x in enumerate(at):
            i = int(np.clip(np.searchsorted(knots, x) - 1, 0, n - 2)); t = x - knots[i]; u = knots[i + 1] - x
            V[q, j] = (M[i] * u ** 3 + M[i + 1] * t ** 3) / (6 * h[i]) + (y[i] / h[i] - M[i] * h[i] / 6) * u + (y[i + 1] / h[i] - M[i + 1] * h[i] / 6) * t
            D[q, j] = (-M[i] * u ** 2 + M[i + 1] * t ** 2) / (2 * h[i]) - (y[i] / h[i] - M[i] * h[i] / 6) + (y[i + 1] / h[i] - M[i + 1] * h[i] / 6)
    return V, D

def geometry(seed, L):
    rng = np.random.default_rng(seed)
    cuts = np.sort(rng.uniform(0, 1, 17)); edges = np.concatenate(([0.0], cuts, [1.0]))
    while np.min(np.diff(edges)) < 0.01:
        cuts = np.sort(rng.uniform(0, 1, 17)); edges = np.concatenate(([0.0], cuts, [1.0]))
    x4, w4 = np.polynomial.legendre.leggauss(4)
    s = ((edges[:-1] + edges[1:]) / 2)[:, None] + ((edges[1:] - edges[:-1]) / 2)[:, None] * x4[None, :]
    wr = (L * L / 2) * ((edges[1:] - edges[:-1]) / 2)[:, None] * w4[None, :]
    R = L * np.sqrt(s.ravel()); wr = wr.ravel()
    center = 0.05 * L * np.sin(R / L * 3); height = L * (0.1 + 0.03 * np.cos(R / L * 2))
    roots = np.stack((center - height, center + height), axis=-1)
    x32, w32 = np.polynomial.legendre.leggauss(32)
    z = center[:, None] + height[:, None] * x32[None, :]; wz = height[:, None] * w32[None, :]
    old = scal1.build(radial_nodes_m=R, radial_RdR_weights_m2=wr, radial_domain_m=(0.0, L), roots_m=roots,
                      z_nodes_m=z, z_weights_m=wz, binding_module=bind)
    return edges, R, wr, old

for seed, L in ((1, 2.5), (2, 3.1e20)):
    edges, R, wr, old = geometry(seed, L)
    sm = mod.build_annular_scalar_maps(old_scalar_maps=old, old_scalar_map_sha256=PINS['scal1'][1], radial_nodes_m=R,
                                       radial_RdR_weights_m2=wr, outer_radius_m=L, binding_module=bind,
                                       binding_module_sha256=PINS['bind'][1], edge_absolute_tolerance=1e-12,
                                       weight_relative_tolerance=1e-12)
    a = sm['arrays']; tag = f'L={L:g}'
    add(f'edges_match_generator {tag}', np.max(np.abs(a['annular_edges_s'] - edges)) < 1e-14, max_abs=float(np.max(np.abs(a['annular_edges_s'] - edges))))
    s = (R / L) ** 2; Vb, Db = natural_cardinal(edges, s)
    add(f'radial_value_vs_independent_spline {tag}', np.max(np.abs(a['radial_value'] - Vb)) < 1e-12, max_abs=float(np.max(np.abs(a['radial_value'] - Vb))))
    BR = (2 * R / L ** 2)[:, None] * Db
    e = float(np.max(np.abs(a['radial_derivative'] - BR)) / np.max(np.abs(BR)))
    add(f'radial_derivative_equals_(2R/L^2)dB/ds_independent {tag}', e < 1e-11, rel=e)
    oa = old['arrays']
    pres = all(np.array_equal(a[k], oa[k]) for k in ('weights_RdRdz', 'zeta', 'roots_m', 'root_radial_derivatives'))
    add(f'preserved_geometry_bitwise {tag}', pres)
    add(f'outer_trace_exact_kron_e18_I8 {tag}', np.array_equal(a['outer_coefficient_trace'], np.kron(np.eye(19)[-1][None, :], np.eye(8))))
    # chain rule / formula check with the preserved v001 slopes (independent evaluation of the contract formulas)
    zeta = oa['zeta']; roots = oa['roots_m']; cen = roots.mean(1); hgt = (roots[:, 1] - roots[:, 0]) / 2
    cR = (oa['root_radial_derivatives'][:, 0] + oa['root_radial_derivatives'][:, 1]) / 2
    hR = (oa['root_radial_derivatives'][:, 1] - oa['root_radial_derivatives'][:, 0]) / 2
    P = np.polynomial.legendre.legvander(zeta, 7)
    dP = np.zeros_like(P)
    for q in range(8):
        dP[..., q] = np.polynomial.legendre.legval(zeta, np.polynomial.legendre.legder(np.eye(8)[q]))
    V_exp = np.einsum('ij,ila->ilja', Vb, P).reshape(2304, 152)
    VR_exp = (np.einsum('ij,ila->ilja', BR, P) - np.einsum('ij,ila->ilja', Vb, dP * ((cR[:, None] + zeta * hR[:, None]) / hgt[:, None])[:, :, None])).reshape(2304, 152)
    VZ_exp = np.einsum('ij,ila->ilja', Vb, dP / hgt[:, None, None]).reshape(2304, 152)
    for key, ex in (('value', V_exp), ('partial_R', VR_exp), ('partial_z', VZ_exp)):
        r = float(np.max(np.abs(a[key] - ex)) / np.max(np.abs(ex)))
        add(f'scalar_{key}_vs_independent_contract_formula {tag}', r < 1e-11, rel=r, shape=list(a[key].shape))
    add(f'trial_and_quadrature_shapes {tag}', sm['trial_shape'] == [19, 8] and sm['quadrature_shape'] == [72, 32] and a['value'].shape == (2304, 152))
    # fail-closed probes on edge recovery
    def rejects(**chg):
        kw = dict(old_scalar_maps=old, old_scalar_map_sha256=PINS['scal1'][1], radial_nodes_m=R, radial_RdR_weights_m2=wr,
                  outer_radius_m=L, binding_module=bind, binding_module_sha256=PINS['bind'][1],
                  edge_absolute_tolerance=1e-12, weight_relative_tolerance=1e-12); kw.update(chg)
        try: mod.build_annular_scalar_maps(**kw); return False
        except (ValueError, TypeError): return True
    Rp = R.copy(); Rp[37] *= (1 + 1e-9); wp = wr.copy(); wp[10] *= (1 + 1e-9)
    add(f'fail_closed_probes {tag}', all([rejects(radial_nodes_m=Rp), rejects(radial_RdR_weights_m2=wp), rejects(outer_radius_m=L * (1 + 1e-9)),
                                         rejects(old_scalar_map_sha256='0' * 64), rejects(binding_module_sha256='0' * 64),
                                         rejects(edge_absolute_tolerance=-1.0), rejects(edge_absolute_tolerance=float('nan'))]))
    # helicity: dims, shared reduced coordinates, divU identity, hard residual, outer xi_R, equivalence to v001 on old maps
    for m in range(1, 7):
        hm = mod.build_annular_regular_helicity_maps(scalar_maps=sm, radial_nodes_m=R, outer_radius_m=L, m=m,
                                                    rank_relative_tolerance=1e-12, rank_absolute_tolerance=0.0)
        ok_dims = hm['status'] == 'REGULAR_HELICITY_MAPS' and all(hm[k].shape == (2304, 448) for k in
                  ('UR', 'UP', 'UZ', 'partial_R_UR', 'partial_R_UP', 'partial_R_UZ', 'partial_z_UR', 'partial_z_UP', 'partial_z_UZ', 'divU')) \
                  and hm['raw_coefficient_transform'].shape == (456, 448) and hm['regularity_exponents'] == [abs(m + 1), abs(m - 1), abs(m)]
        rr = np.repeat(R, 32); ex = (m + 1, abs(m - 1), m); f = [(rr / L) ** e for e in ex]; T = hm['raw_coefficient_transform']
        pl, mi, ve = T[:152], T[152:304], T[304:]
        UR = (L / 2) * ((f[0][:, None] * a['value']) @ pl + (f[1][:, None] * a['value']) @ mi)
        dRUR = (L / 2) * ((f[0][:, None] * a['partial_R'] + (ex[0] / rr)[:, None] * f[0][:, None] * a['value']) @ pl
                          + (f[1][:, None] * a['partial_R'] + (ex[1] / rr)[:, None] * f[1][:, None] * a['value']) @ mi)
        UZ = L * ((f[2][:, None] * a['value']) @ ve); dzUZ = L * ((f[2][:, None] * a['partial_z']) @ ve)
        UP = (L / 2j) * ((f[0][:, None] * a['value']) @ pl - (f[1][:, None] * a['value']) @ mi)
        div = dRUR + UR / rr[:, None] + 1j * m * UP / rr[:, None] + dzUZ
        sc = lambda x, y: float(np.max(np.abs(x - y)) / max(np.max(np.abs(y)), 1e-300))
        shared = max(sc(hm['UR'], UR), sc(hm['partial_R_UR'], dRUR), sc(hm['UZ'], UZ), sc(hm['partial_z_UZ'], dzUZ), sc(hm['UP'], UP), sc(hm['divU'], div))
        outer_xiR = float(np.max(np.abs(np.kron(np.eye(19)[-1][None, :], np.eye(8)) @ (0.5 * (pl + mi)))))
        add(f'helicity_m{m} {tag}', ok_dims and shared < 1e-12 and hm['hard_nullspace_residual_norm'] < 1e-12 and outer_xiR < 1e-12,
            dims_ok=ok_dims, shared_coordinate_rel=shared, hard_residual=hm['hard_nullspace_residual_norm'], outer_xiR_raw_trace=outer_xiR)
        # generalization check: 0450 core on the OLD v001 scalar maps vs the reviewed v001 helicity module itself
        o = old['arrays']; core = mod._regular_helicity_core(V=o['value'], VR=o['partial_R'], VZ=o['partial_z'], T=o['outer_coefficient_trace'],
                                                           R=R, L=L, m=m, rank_relative_tolerance=1e-12, rank_absolute_tolerance=0.0)
        ref = hel1.build(scalar_maps=old, scalar_map_sha256=PINS['scal1'][1], radial_nodes_m=R, outer_radius_m=L, m=m,
                         rank_relative_tolerance=1e-12, rank_absolute_tolerance=0.0)
        keys = ('UR', 'UP', 'UZ', 'partial_R_UR', 'partial_R_UP', 'partial_R_UZ', 'partial_z_UR', 'partial_z_UP', 'partial_z_UZ', 'divU',
                'normalized_nullspace', 'raw_coefficient_transform', 'column_norms', 'hard_constraint_normalized', 'hard_singular_values')
        add(f'core_on_old_maps_bitwise_equals_v001_helicity_m{m} {tag}', all(np.array_equal(core[k], ref[k]) for k in keys))
rep['module_sha256_after'] = sha(PINS['mod'][0]); rep['all_ok'] = all(c['ok'] for c in rep['checks']) and rep['module_sha256_after'] == PINS['mod'][1]
json.dump(rep, open(sys.argv[sys.argv.index('--out') + 1], 'w'), indent=1, default=float)
print(json.dumps({'python': rep['python'], 'numpy': rep['numpy'], 'all_ok': rep['all_ok'], 'n_checks': len(rep['checks']),
                  'failed': [c for c in rep['checks'] if not c['ok']]}, indent=1, default=float))
