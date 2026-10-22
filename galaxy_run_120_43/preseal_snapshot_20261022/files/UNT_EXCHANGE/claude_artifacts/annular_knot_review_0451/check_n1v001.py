"""check_n1v001 -- Claude4 review lane, dispatch 0451, helper N1. Synthetic analytic fixtures only.

Run: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 <root python3> -I -B check_n1v001.py [c3_path c3_sha256]
(optional arguments re-pin section 6 to other frozen c3 bytes). Prints one JSON summary. Writes nothing. Loads by path, after sha256 verification: the oracle
(this directory), the pinned import-inert spline helper (binding v002) and, for section 6 only,
the c3v001 pre-freeze bytes (skipped if the hash differs). No project data, run or search.
"""
import sys

sys.dont_write_bytecode = True
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
HELPERS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
               'FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method')
BINDING = (HELPERS / 'owned_body_fitted_displacement_binding_v002.py',
           '87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462')
C3 = (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_knot_maps_0450/annular_knot_maps_c3v001.py'),
      '23bb22fb94c3a6b39b84479a1c5e03812fbcdeaf6180ca85ddad083a3d3d92c4')
EPS = float(np.finfo(float).eps)
KPC = 3.0856775814913673e19


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(name, path, pin=None):
    digest = sha(path)
    if pin is not None and digest != pin:
        raise ValueError(f'pin mismatch {path}: {digest}')
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, digest


def g3(x):
    return float(f'{float(x):.3e}')


def rel(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return g3(np.max(np.abs(a - b)) / max(np.max(np.abs(b)), 1e-300))


def fro_rel(defect, *parts):
    return g3(np.linalg.norm(defect) / sum(np.linalg.norm(p) for p in parts))


# ----------------------------------------------------------------- synthetic geometry
def annuli(seed, n=18, min_width=0.02, uniform=False):
    if uniform:
        w = np.full(n, 1.0 / n)
    else:
        w = min_width + (1 - n * min_width) * np.random.default_rng(seed).dirichlet(np.ones(n))
    e = np.concatenate(([0.0], np.cumsum(w)))
    e /= e[-1]
    e[-1] = 1.0
    return e


def radial(edges, L, pipeline='direct', L_kpc=7.3):
    x, w = np.polynomial.legendre.leggauss(4)
    if pipeline == 'direct':                         # GL in s, R = L sqrt(s)
        c, h = (edges[:-1] + edges[1:]) / 2, (edges[1:] - edges[:-1]) / 2
        s = (c[:, None] + h[:, None] * x).ravel()
        return L * np.sqrt(s), (L * L / 2) * (h[:, None] * w).ravel(), L
    if pipeline == 'kpc2':                           # edges stored in kpc^2, converted to metres
        sp = L_kpc ** 2 * edges
        c, h = (sp[:-1] + sp[1:]) / 2, (sp[1:] - sp[:-1]) / 2
        R = np.sqrt((c[:, None] + h[:, None] * x).ravel()) * KPC
        return R, (0.5 * h[:, None] * w).ravel() * KPC * KPC, np.sqrt(sp[-1]) * KPC
    if pipeline == 'gl_in_R':                        # wrong rule: GL in R on the same annuli
        Re = L * np.sqrt(edges)
        c, h = (Re[:-1] + Re[1:]) / 2, (Re[1:] - Re[:-1]) / 2
        R = (c[:, None] + h[:, None] * x).ravel()
        return R, R * (h[:, None] * w).ravel(), L
    raise ValueError(pipeline)


def vertical(R, L):
    x, w = np.polynomial.legendre.leggauss(16)
    zeta = np.concatenate((-0.5 + 0.5 * x, 0.5 + 0.5 * x))
    om = np.concatenate((0.5 * w, 0.5 * w))
    c = 0.05 * L * np.sin(2 * R / L) + 0.01 * L
    h = 0.1 * L * (1 + 0.3 * np.cos(R / L))
    cR = 0.1 * np.cos(2 * R / L)
    hR = -0.03 * np.sin(R / L)
    roots = np.stack((c - h, c + h), axis=-1)
    return dict(roots=roots, z=c[:, None] + h[:, None] * zeta, wz=h[:, None] * om,
                rootR=np.stack((cR - hR, cR + hR), axis=-1))


def center_height(R, L):
    return 0.05 * L * np.sin(2 * R / L) + 0.01 * L, 0.1 * L * (1 + 0.3 * np.cos(R / L))


def main(argv):
    c3_pin = C3 if len(argv) < 3 else (Path(argv[1]), argv[2])
    out = {}
    orc, orc_sha = load('oracle_n1v001', HERE / 'oracle_n1v001.py')
    helper, _ = load('binding_v002', *BINDING)
    out['pins'] = dict(oracle_n1v001=orc_sha, binding_v002=BINDING[1], numpy=np.__version__)
    TOL = orc.RECOMMENDED_EDGE_TOL_S

    # ------------------------------------------------------------ 1. edge recovery
    worst = {k: 0.0 for k in ('node', 'adjacent', 's0', 's_end', 'weight', 'cumulative_weight_edges')}
    edge_err = 0.0
    for seed in range(20):
        e = annuli(seed)
        for pipe in ('direct', 'kpc2'):
            R, wr, L = radial(e, 2.5, pipe)
            rec = orc.recover_annular_edges(radial_nodes_m=R, radial_RdR_weights_m2=wr, outer_radius_m=L,
                                            edge_tolerance_s=TOL, weight_tolerance_s=TOL)
            for k in worst:
                worst[k] = max(worst[k], rec['residuals'][k])
            edge_err = max(edge_err, float(np.max(np.abs(rec['knots'] - e))))
    neg = {}
    e = annuli(0)
    R, wr, L = radial(e, 2.5, 'gl_in_R')
    try:
        orc.recover_annular_edges(radial_nodes_m=R, radial_RdR_weights_m2=wr, outer_radius_m=L,
                                  edge_tolerance_s=TOL, weight_tolerance_s=TOL)
        neg['gl_in_R'] = 'NOT DETECTED'
    except ValueError as exc:
        neg['gl_in_R'] = 'raised: ' + str(exc).split(';')[0][:200]
    R, wr, L = radial(e, 2.5, 'direct')
    R2 = R.copy()
    R2[37] *= 1 + 1e-10
    for name, (RR, ww) in {'node_rel_1e-10': (R2, wr), 'weights_x_(1+1e-9)': (R, wr * (1 + 1e-9)),
                           'groups_shifted_by_one': (np.concatenate((R[1:], [R[-1] * (1 + 1e-6)])), wr)}.items():
        try:
            orc.recover_annular_edges(radial_nodes_m=RR, radial_RdR_weights_m2=ww, outer_radius_m=L,
                                      edge_tolerance_s=TOL, weight_tolerance_s=TOL)
            neg[name] = 'NOT DETECTED'
        except ValueError as exc:
            neg[name] = 'raised'
    out['1_edge_recovery'] = dict(
        tolerance_s=g3(TOL), tolerance_in_eps=TOL / EPS, seeds=20, pipelines=['direct L=2.5', 'kpc^2 -> m'],
        worst_residuals_s={k: g3(v) for k, v in worst.items()}, worst_residual_in_eps=g3(max(worst.values()) / EPS),
        max_abs_knot_error_vs_truth=g3(edge_err), negative_cases=neg)

    # ---------------------------------------------- 2. spline self-check vs pinned helper
    e = annuli(3)
    R, wr, L = radial(e, 2.5, 'direct')
    s = (R / L) ** 2
    at = list(s) + [0.0, 1.0]
    sc = {}
    Hv, Hd = helper._spline_matrices(e, at)
    Ov, Od = orc.evaluate_cardinal(orc.natural_cubic_cardinal(e), at)
    sc['annular_19_knots'] = dict(value_maxabs=g3(np.max(abs(Hv - Ov))), deriv_rel=rel(Od, Hd),
                                  helper_trace_s1_is_e18=bool(np.array_equal(Hv[-1], np.eye(19)[-1])),
                                  oracle_trace_s1_is_e18=bool(np.array_equal(Ov[-1], np.eye(19)[-1])),
                                  oracle_trace_s0_is_e0=bool(np.array_equal(Ov[-2], np.eye(19)[0])))
    Hv, Hd = helper._spline_matrices(s, at)
    Ov, Od = orc.evaluate_cardinal(orc.natural_cubic_cardinal(s), at, allow_extrapolation=True)
    sc['old_72_nodal_knots_with_extrapolated_0_1'] = dict(value_rel=rel(Ov, Hv), deriv_rel=rel(Od, Hd),
                                                         nodal_values_identity=bool(np.array_equal(Ov[:72], np.eye(72))))
    zeta = np.linspace(-1, 1, 41)
    P, dP = orc.legendre(zeta)
    Pn = np.polynomial.legendre.legvander(zeta, 7)
    dPn = np.stack([np.polynomial.legendre.legval(zeta, np.polynomial.legendre.legder(np.eye(8)[a]))
                    for a in range(8)], axis=-1)
    sc['legendre_vs_numpy'] = dict(P_maxabs=g3(np.max(abs(P - Pn))), dP_maxabs=g3(np.max(abs(dP - dPn))))
    sc['gl4_closed_form_vs_leggauss'] = dict(
        nodes=g3(np.max(abs(orc.GL4_X - np.polynomial.legendre.leggauss(4)[0]))),
        weights=g3(np.max(abs(orc.GL4_W - np.polynomial.legendre.leggauss(4)[1]))))
    out['2_spline_selfcheck_vs_pinned_helper'] = sc

    # ------------------------------------------------------------ 3. IBP demonstration
    def bases(edges, L):
        R, wr, L = radial(edges, L, 'direct')
        s = (R / L) ** 2
        what = 2 * wr / L ** 2
        V0, D0 = helper._spline_matrices(s, list(s) + [0.0, 1.0])       # v001-style nodal basis
        old = dict(Bv=np.eye(s.size), Bs=D0[:s.size], t0=V0[-2], t1=V0[-1])
        sp = orc.natural_cubic_cardinal(edges)
        Bv, Bs = orc.evaluate_cardinal(sp, s)
        T, _ = orc.evaluate_cardinal(sp, [0.0, 1.0])
        new = dict(Bv=Bv, Bs=Bs, t0=T[0], t1=T[1])
        return s, what, R, wr, L, old, new

    def metrics(b, s, what, R, wr, L):
        BR = (2 * R / L ** 2)[:, None] * b['Bs']
        lhs_s = b['Bv'].T @ (what[:, None] * b['Bs']) + b['Bs'].T @ (what[:, None] * b['Bv'])
        bnd_s = np.outer(b['t1'], b['t1']) - np.outer(b['t0'], b['t0'])
        lhs_R = (b['Bv'].T @ (wr[:, None] * BR) + BR.T @ (wr[:, None] * b['Bv'])
                 + b['Bv'].T @ ((wr / R)[:, None] * b['Bv']))
        bnd_R = L * np.outer(b['t1'], b['t1'])
        return dict(s_form=fro_rel(lhs_s - bnd_s, lhs_s, bnd_s), root_cylindrical_R_form=fro_rel(lhs_R - bnd_R, lhs_R, bnd_R))

    ibp = {}
    for label, edges in (('uniform_18', annuli(0, uniform=True)), ('random_18_seed7', annuli(7)),
                         ('random_18_seed11', annuli(11))):
        s, what, R, wr, L, old, new = bases(edges, 2.5)
        ibp[label] = dict(old_knots_at_nodes=metrics(old, s, what, R, wr, L),
                          annular_knots=metrics(new, s, what, R, wr, L))
    # axis-term isolation (annular, uniform 18): drop the (wr/R) term and its share of the boundary
    s, what, R, wr, L, old, new = bases(annuli(0, uniform=True), 2.5)
    weighted = {}
    for name, g, dg in (('sqrt_s', np.sqrt(s), 0.5 / np.sqrt(s)),
                        ('(1-s)^1.5', (1 - s) ** 1.5, -1.5 * np.sqrt(1 - s)),
                        ('exp(-s/0.1)', np.exp(-s / 0.1), -10 * np.exp(-s / 0.1))):
        g0, g1 = {'sqrt_s': (0.0, 1.0), '(1-s)^1.5': (1.0, 0.0), 'exp(-s/0.1)': (1.0, np.exp(-10.0))}[name]
        rows = {}
        for lab, b in (('old', old), ('annular', new)):
            lhs = (b['Bv'].T @ ((what * g)[:, None] * b['Bs']) + b['Bs'].T @ ((what * g)[:, None] * b['Bv'])
                   + b['Bv'].T @ ((what * dg)[:, None] * b['Bv']))
            bnd = g1 * np.outer(b['t1'], b['t1']) - g0 * np.outer(b['t0'], b['t0'])
            rows[lab] = fro_rel(lhs - bnd, lhs, bnd)
        weighted[name] = rows
    ibp['s_form_with_weight_g(s)_uniform_18'] = weighted
    parity = {}
    BR = (2 * R / L ** 2)[:, None] * new['Bs']
    for e_ in range(6):
        f = (R / L) ** e_
        trial, dtrial = f[:, None] * new['Bv'], f[:, None] * BR + (e_ / R * f)[:, None] * new['Bv']
        lhs = new['Bv'].T @ (wr[:, None] * dtrial) + BR.T @ (wr[:, None] * trial) + new['Bv'].T @ ((wr / R)[:, None] * trial)
        bnd = L * np.outer(new['t1'], new['t1'])
        parity[f'e={e_}'] = fro_rel(lhs - bnd, lhs, bnd)
    ibp['cylindrical_R_form_trial_times_(R/L)^e_annular_uniform_18'] = parity
    refine = {}
    for N in (18, 36, 72, 144):
        s, what, R, wr, L, old, new = bases(annuli(0, n=N, uniform=True), 2.5)
        refine[f'N={N}'] = metrics(new, s, what, R, wr, L)['root_cylindrical_R_form']
    ibp['annular_root_R_form_vs_uniform_refinement'] = refine
    # attribution (diagnostic only, not a grid proposal): defect share near the axis, and the same
    # R-form with ONLY annulus 0 integrated by 8-point GL in r=sqrt(s) (integrand polynomial in r)
    edges = annuli(0, uniform=True)
    s, what, R, wr, L, old, new = bases(edges, 2.5)
    sp = orc.natural_cubic_cardinal(edges)

    def r_form(s_, what_):
        R_, wr_ = L * np.sqrt(s_), (L * L / 2) * what_
        Bv, Bs = orc.evaluate_cardinal(sp, s_)
        BR_ = (2 * R_ / L ** 2)[:, None] * Bs
        lhs = Bv.T @ (wr_[:, None] * BR_) + BR_.T @ (wr_[:, None] * Bv) + Bv.T @ ((wr_ / R_)[:, None] * Bv)
        bnd = L * np.outer(new['t1'], new['t1'])
        return lhs - bnd, lhs, bnd

    D, lhs, bnd = r_form(s, what)
    x8, w8 = np.polynomial.legendre.leggauss(8)
    r1 = np.sqrt(edges[1])
    rk = r1 / 2 * (1 + x8)
    s_alt = np.concatenate((rk ** 2, s[4:]))
    what_alt = np.concatenate((2 * rk * (r1 / 2) * w8, what[4:]))
    D2, lhs2, bnd2 = r_form(s_alt, what_alt)
    ibp['annular_root_R_form_attribution_uniform_18'] = dict(
        defect_share_leading_3x3=g3(np.linalg.norm(D[:3, :3]) ** 2 / np.linalg.norm(D) ** 2),
        with_annulus0_GL8_in_r=fro_rel(D2, lhs2, bnd2))
    # scaling with the first annular edge t1=(R1/L)^2: 12 random layouts + edges uniform in R
    ratios, d00 = [], []
    for edges in [annuli(seed) for seed in range(12)] + [(np.arange(19) / 18.0) ** 2]:
        s, what, R, wr, L, old, new = bases(edges, 2.5)
        sp = orc.natural_cubic_cardinal(edges)
        D, lhs, bnd = r_form(s, what)
        r = np.linalg.norm(D) / (np.linalg.norm(lhs) + np.linalg.norm(bnd))
        ratios.append(r / np.sqrt(edges[1]))
        d00.append(abs(D[0, 0]) / np.linalg.norm(D))
    ibp['annular_root_R_form_over_sqrt_t1'] = dict(min=g3(min(ratios)), max=g3(max(ratios)),
                                                  uniform_in_R_value=g3(ratios[-1] / 18.0),
                                                  D00_over_frobenius_min=g3(min(d00)))
    u, wu = (1 + orc.GL4_X) / 2, orc.GL4_W / 2
    ibp['gl4_on_[0,1]'] = {'int_u^-1/2_(exact_2)': float(np.sum(wu / np.sqrt(u))),
                           'rel_error_u^-1/2': g3((2 - np.sum(wu / np.sqrt(u))) / 2),
                           'rel_error_u^+1/2': g3((2 / 3 - np.sum(wu * np.sqrt(u))) / (2 / 3))}
    out['3_ibp'] = ibp

    # ------------------------------------------------------------- 4. chain rule (FD)
    e = annuli(5)
    R, wr, L = radial(e, 2.5, 'direct')
    geo = vertical(R, L)
    sm = orc.annular_scalar_maps(radial_nodes_m=R, radial_RdR_weights_m2=wr, outer_radius_m=L, roots_m=geo['roots'],
                                 z_nodes_m=geo['z'], z_weights_m=geo['wz'], edge_tolerance_s=TOL,
                                 weight_tolerance_s=TOL, root_radial_derivatives_m=geo['rootR'])
    a = sm['arrays']
    Rq, zq = np.repeat(R, 32), geo['z'].ravel()
    # FD stencil must stay inside each annulus (spline third derivative jumps at knots)
    Ek = L * np.sqrt(e)
    gap = float(np.min(np.minimum(R - Ek[np.searchsorted(Ek, R) - 1], Ek[np.searchsorted(Ek, R)] - R)))
    d = 1e-4 * L
    assert 2 * d < gap

    def basis(Rp, zp):
        c, h = center_height(Rp, L)
        return orc.scalar_basis_at(spline=sm['spline'], R=Rp, z=zp, outer_radius_m=L, center=c, height=h)

    def fd(fun, x0, step, other, axis):
        def one(dd):
            if axis == 'R':
                return (fun(x0 + dd, other) - fun(x0 - dd, other)) / (2 * dd)
            return (fun(other, x0 + dd) - fun(other, x0 - dd)) / (2 * dd)
        return (4 * one(step) - one(2 * step)) / 3

    chain = dict(fd_step_over_L=d / L, min_node_to_knot_gap_over_L=g3(gap / L),
                 V_partial_R=rel(fd(basis, Rq, d, zq, 'R'), a['partial_R']),
                 V_partial_z=rel(fd(basis, zq, 1e-4 * L, Rq, 'z'), a['partial_z']),
                 V_value_pointwise_vs_map=rel(basis(Rq, zq), a['value']))
    rng = np.random.default_rng(451)
    hel_fd = {}
    for m in range(1, 7):
        hm = orc.regular_helicity_maps(value=a['value'], partial_R=a['partial_R'], partial_z=a['partial_z'],
                                       outer_coefficient_trace=a['outer_coefficient_trace'], radial_nodes_m=R,
                                       outer_radius_m=L, m=m, rank_relative_tolerance=1e-12, rank_absolute_tolerance=0.0)
        y = rng.standard_normal(hm['raw_coefficient_transform'].shape[1])

        def U(Rp, zp, m=m, hm=hm):
            return [u @ y for u in orc.helicity_fields_at(scalar_rows=basis(Rp, zp), R=Rp, outer_radius_m=L, m=m,
                                                           raw_coefficient_transform=hm['raw_coefficient_transform'])]
        dR = [(4 * ((np.array(U(Rq + d, zq)) - np.array(U(Rq - d, zq))) / (2 * d))
               - ((np.array(U(Rq + 2 * d, zq)) - np.array(U(Rq - 2 * d, zq))) / (4 * d))) / 3]
        dR = dR[0]
        dzs = 1e-4 * L
        dZ = (4 * ((np.array(U(Rq, zq + dzs)) - np.array(U(Rq, zq - dzs))) / (2 * dzs))
              - ((np.array(U(Rq, zq + 2 * dzs)) - np.array(U(Rq, zq - 2 * dzs))) / (4 * dzs))) / 3
        U0 = np.array(U(Rq, zq))
        divfd = dR[0] + U0[0] / Rq + 1j * m * U0[1] / Rq + dZ[2]
        ce, he = center_height(np.array([L]), L)
        zL = ce + he * np.linspace(-1, 1, 41)
        URL = U(np.full(41, L), zL)[0]
        hel_fd[f'm={m}'] = dict(
            U_vs_maps=max(rel(U0[k], hm[n] @ y) for k, n in enumerate(('UR', 'UP', 'UZ'))),
            partial_R=max(rel(dR[k], hm[n] @ y) for k, n in enumerate(('partial_R_UR', 'partial_R_UP', 'partial_R_UZ'))),
            partial_z=max(rel(dZ[k], hm[n] @ y) for k, n in enumerate(('partial_z_UR', 'partial_z_UP', 'partial_z_UZ'))),
            divU=rel(divfd, hm['divU'] @ y),
            UR_at_R_eq_L_rel=g3(np.max(np.abs(URL)) / np.max(np.abs(U0[0]))))
    chain['helicity_fd_rel_errors'] = hel_fd
    out['4_chain_rule'] = chain

    # ------------------------------------------------------- 5. dimensions / helicity
    T = a['outer_coefficient_trace']
    dims = dict(value=list(a['value'].shape), trial_shape=sm['trial_shape'], quadrature_shape=sm['quadrature_shape'],
                rank_value=int(np.linalg.matrix_rank(a['value'])),
                outer_trace_is_kron_e18_I8=bool(np.array_equal(T, np.kron(np.eye(19)[-1][None, :], np.eye(8)))))
    per_m = {}
    for m in range(1, 7):
        kw = dict(value=a['value'], partial_R=a['partial_R'], partial_z=a['partial_z'], outer_coefficient_trace=T,
                  radial_nodes_m=R, outer_radius_m=L, m=m, rank_relative_tolerance=1e-12, rank_absolute_tolerance=0.0)
        hq, hs = orc.regular_helicity_maps(**kw, nullspace='qr'), orc.regular_helicity_maps(**kw, nullspace='eigh')
        Zq, Zs = hq['normalized_nullspace'], hs['normalized_nullspace']
        names = ('UR', 'UP', 'UZ', 'partial_R_UR', 'partial_R_UP', 'partial_R_UZ', 'partial_z_UR', 'partial_z_UP',
                 'partial_z_UZ', 'divU', 'raw_coefficient_transform')
        per_m[f'm={m}'] = dict(
            status=hq['status'], exponents=hq['regularity_exponents'], Braw_shape=list(hq['hard_constraint_raw'].shape),
            Z_shape=list(Zq.shape), map_shape=list(hq['UR'].shape), constraint_rank=int(np.sum(hq['hard_singular_values'] > hq['rank_threshold'])),
            BZ_residual=g3(hq['hard_nullspace_residual_norm']), BZ_residual_eigh=g3(hs['hard_nullspace_residual_norm']), ZtZ_minus_I=g3(np.max(abs(Zq.T @ Zq - np.eye(Zq.shape[1])))),
            Braw_raw_transform_rel=g3(np.linalg.norm(hq['hard_constraint_raw'] @ hq['raw_coefficient_transform'])
                                      / (np.linalg.norm(hq['hard_constraint_raw']) * np.linalg.norm(hq['raw_coefficient_transform']))),
            qr_vs_eigh_raw_Z_columns_maxabs=g3(np.max(abs(Zq - Zs))),
            qr_vs_eigh_projected_maps_rel=max(rel(hs[n] @ Zs.T, hq[n] @ Zq.T) for n in names))
    dims['helicity'] = per_m
    out['5_dimensions_helicity'] = dims

    # ---------------------------------------- 6. oracle vs c3v001 pre-freeze bytes (synthetic)
    try:
        c3, c3sha = load('annular_knot_maps_c3v001', *c3_pin)
    except (ValueError, FileNotFoundError) as exc:
        out['6_oracle_vs_c3v001'] = 'SKIPPED: ' + str(exc)[:160]
    else:
        cmp = dict(c3_sha256=c3sha)
        for label, (seed, pipe, Lval) in dict(direct_L2p5=(5, 'direct', 2.5), kpc2_meters=(9, 'kpc2', None)).items():
            e = annuli(seed)
            R, wr, L = radial(e, Lval if Lval else 1.0, pipe)
            geo = vertical(R, L)
            center, height = geo['roots'].mean(axis=1), (geo['roots'][:, 1] - geo['roots'][:, 0]) / 2
            zeta = (geo['z'] - center[:, None]) / height[:, None]
            s = (R / L) ** 2
            _, Ds = helper._spline_matrices(s, list(s) + [0.0, 1.0])
            DR = (2 * R / L ** 2)[:, None] * Ds[:72]
            cR = np.einsum('ij,j->i', DR, center, optimize=False)
            hR = np.einsum('ij,j->i', DR, height, optimize=False)
            Vold = np.zeros((72, 32, 72, 8))
            Pv = np.polynomial.legendre.legvander(zeta, 7)
            for i in range(72):
                Vold[i, :, i, :] = Pv[i]
            old = dict(trial_shape=[72, 8], quadrature_shape=[72, 32], arrays=dict(
                value=Vold.reshape(2304, 576), zeta=zeta, weights_RdRdz=(wr[:, None] * geo['wz']).reshape(-1),
                roots_m=geo['roots'], root_radial_derivatives=np.stack((cR - hR, cR + hR), axis=-1), radial_derivative=DR))
            s3 = c3.build_annular_scalar_maps(old_scalar_maps=old, old_scalar_map_sha256=c3.OLD_SCALAR_MAP_SHA256,
                                              radial_nodes_m=R, radial_RdR_weights_m2=wr, outer_radius_m=L,
                                              binding_module=helper, binding_module_sha256=c3.BINDING_MODULE_SHA256,
                                              edge_absolute_tolerance=1e-12, weight_relative_tolerance=1e-12)
            so = orc.annular_scalar_maps(radial_nodes_m=R, radial_RdR_weights_m2=wr, outer_radius_m=L,
                                         roots_m=geo['roots'], z_nodes_m=geo['z'], z_weights_m=geo['wz'],
                                         edge_tolerance_s=TOL, weight_tolerance_s=TOL,
                                         root_radial_derivatives_m=old['arrays']['root_radial_derivatives'])
            a3, ao = s3['arrays'], so['arrays']
            par = (-1.0) ** np.arange(8)
            row = dict(
                trial_shape=s3['trial_shape'], quadrature_shape=s3['quadrature_shape'],
                edges_maxabs=g3(np.max(abs(a3['annular_edges_s'] - ao['annular_edges_s']))),
                edges_vs_truth_maxabs=g3(np.max(abs(a3['annular_edges_s'] - e))),
                c3_edge_recovery={k: g3(v) for k, v in s3['edge_recovery'].items() if k.startswith(('max_', 's0', 's18', 'weights'))},
                value=rel(a3['value'], ao['value']), partial_R=rel(a3['partial_R'], ao['partial_R']),
                partial_z=rel(a3['partial_z'], ao['partial_z']),
                radial_value=rel(a3['radial_value'], ao['radial_value']),
                radial_derivative=rel(a3['radial_derivative'], ao['radial_derivative']),
                outer_trace_bitwise=bool(np.array_equal(a3['outer_coefficient_trace'], ao['outer_coefficient_trace'])),
                lower_surface_trace=rel(a3['lower_surface_trace'], np.kron(ao['radial_value'], par[None, :])),
                upper_surface_trace=rel(a3['upper_surface_trace'], np.kron(ao['radial_value'], np.ones((1, 8)))),
                preserved_bitwise=all(np.array_equal(a3[k], old['arrays'][k]) for k in ('weights_RdRdz', 'zeta', 'roots_m', 'root_radial_derivatives')))
            hel = {}
            for m in range(1, 7):
                h3 = c3.build_annular_regular_helicity_maps(scalar_maps=s3, radial_nodes_m=R, outer_radius_m=L, m=m,
                                                            rank_relative_tolerance=1e-12, rank_absolute_tolerance=0.0)
                ho = orc.regular_helicity_maps(value=ao['value'], partial_R=ao['partial_R'], partial_z=ao['partial_z'],
                                               outer_coefficient_trace=ao['outer_coefficient_trace'], radial_nodes_m=R,
                                               outer_radius_m=L, m=m, rank_relative_tolerance=1e-12, rank_absolute_tolerance=0.0)
                Z3, Zo = h3['normalized_nullspace'], ho['normalized_nullspace']
                names = ('UR', 'UP', 'UZ', 'partial_R_UR', 'partial_R_UP', 'partial_R_UZ', 'partial_z_UR', 'partial_z_UP',
                         'partial_z_UZ', 'divU', 'raw_coefficient_transform')
                hel[f'm={m}'] = dict(
                    status=h3['status'], shapes=[list(h3['UR'].shape), list(h3['raw_coefficient_transform'].shape)],
                    exponents_equal=h3['regularity_exponents'] == ho['regularity_exponents'],
                    Braw_bitwise=bool(np.array_equal(h3['hard_constraint_raw'], ho['hard_constraint_raw'])),
                    column_norms=rel(h3['column_norms'], ho['column_norms']),
                    projected_maps_rel=max(rel(h3[n] @ Z3.T, ho[n] @ Zo.T) for n in names),
                    raw_Z_columns_maxabs=g3(np.max(abs(Z3 - Zo))),
                    c3_hard_residual=g3(h3['hard_nullspace_residual_norm']),
                    dtypes=[str(h3[n].dtype) for n in ('UR', 'UP', 'UZ', 'divU')])
            row['helicity'] = hel
            cmp[label] = row
        out['6_oracle_vs_c3v001'] = cmp
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main(sys.argv)
