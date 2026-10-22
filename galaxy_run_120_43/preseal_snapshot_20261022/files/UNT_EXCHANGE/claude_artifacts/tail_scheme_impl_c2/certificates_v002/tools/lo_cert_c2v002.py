"""LO (DDO) certificate V002 (successor of certificates_v001 lo_cert_c2v001.py / gates/LO_CERT_V001.json and
LO_CERT_K128_V001.json, which stay unedited).  Root A52 (K_big ruling pending in A53; LO must reach beyond 128, CHECK F5).
Replay only; no launch.

Same object and the same absolute-bound method as V001 (its docstring, kept verbatim in the record's method_v001):
  route-A channel only.  Components 1-9 reach a route-A row through prediction v005 (54136c71) L128-129
  pressure_streaming_speed(d_log_N=m['dlnN_dR'], d_log_R=m['dln_sqrt_gphiphi_dR']) and the proper-volume density
  L144-147 (slogdet g_cylindrical; jac = N exp(logdet/2)).  Route B: none -- rotation v005 uvt successor (aa9992bd) L283
  computes metric.evaluate_point (validity guard, result unused) and L284-288 form N, Phi, Phi_R, Phi_z from f[0], g[0] only.
  |dv_i,s| <= (v_i R_i / 4) rho_s B1_s,  rho_s = sup ||Ghat(k)||_2 4 gamma |k|^2 over the shell (points with |k|_inf > K),
  B1_s = the module's own field-bound shell integral (int_{D cap s} |k| T_inf |S_T|), here from ONE build of the saved C4R3
  le3 roster at O = cylinder 256 (TEST_ONLY certificates; I1-T on that state recorded).
Shells: the seven V007 shells (4,5] .. (32,64], plus (64,128], (128,256] (complete spherical shells inside cyl 256) and
(256,363] = D cap {|k| > 256} for O = cylinder 256 (the K_big = 256 production domain; NOT the complete spherical shell;
its outer edge 363 is the module's last unit-shell edge, ceil(sqrt2 x 256) = 363).
rho_s two ways:  rho_sampled = V001's sampled max (52 dirs x 128/decade and 104 x 256/decade; v001 rho_shell);
rho_envelope = sup over direction x |k| x the cardinal torus (certs2_common Envelope; dominates the actual set) by a global
grid (torus 12^3, 200 hemisphere directions, 3 |k| values) + batched local maximization.  max_over_tau uses
rho_used = max(rho_sampled, rho_envelope); max_over_tau_rho_sampled (the V001 definition) is kept alongside.
Usage: python3 -I -B lo_cert_c2v002.py"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certs2_common_c2v002 as C2  # noqa: E402

CC = C2.CC
sys.path.insert(0, str(C2.V001_TOOLS))
import lo_cert_c2v001 as LO1  # noqa: E402  (functions only)

PIN_LO1 = 'd8a70a5e0b3c933147ac0a7c951c7c4d4f4ba0d442676a7bcfc36a96be2111c5'
SHELLS = ((4, 5), (5, 6), (6, 8), (8, 12), (12, 16), (16, 32), (32, 64), (64, 128), (128, 256), (256, 363))
K_BIG = 256.0
CODE = {
    'route_A_prediction_v005': (CC.UPC / 'helpers/coefficient_method/galaxy_coupled_fourier_hi_prediction_v005.py',
                                '54136c71403c90b82f5b150672bf218577bf837c345798ec5f770adf31ba8c72', 'L128-129 (pressure_streaming_speed d_log_R = dln sqrt g_phiphi/dR), L144-147 (proper-volume density)'),
    'route_B_rotation_v005_uvt': (CC.ART / 'tail_scheme_impl_c2/route_b/stages/ddo_free_surface_rotation_root_v005_gal_c2v005_uvt_c2v001.py',
                                  'aa9992bdbcaa112d79f13446021fc169fb0c31a59703709c1a58820c5d8f2ad0', 'L283 metric result unused; L284-288 N, Phi, Phi_R, Phi_z from f[0], g[0] only'),
    'metric_v002': (CC.UPC / 'helpers/coefficient_method/owned_fourier_physical_metric_evaluator_v002.py',
                    '8f01bd5b352a5ec5f74f6c19ed8ad4295c55ff80ba895dac93628f62bace73a4', 'L76 C = Cbar + mat(dx[1:7]); N = 1 + dx[0]'),
}


def rho_env_grid(E, Nt, Ed, ks_m, kref, isq):
    """sup-candidates of ||Ghat||_2 / T_inf on the product grid: [nk, nd, nt]."""
    B = E.B
    out = np.empty((len(ks_m), Ed.shape[0], Nt.shape[0]))
    e0 = np.zeros((10, 1), complex); e0[0, 0] = 1.0
    step = max(1, 20000 // Nt.shape[0])
    for ik, k in enumerate(ks_m):
        s = (k / kref) ** 2; Tinf = 1.0 / (4.0 * B.gam * k * k)
        for d0 in range(0, Ed.shape[0], step):
            d1 = min(Ed.shape[0], d0 + step)
            tot = ((Nt[None] + s * Ed[d0:d1, None]) / B.volume).reshape(-1, 10, 10)
            x = np.linalg.solve(tot, np.broadcast_to(-e0, (tot.shape[0], 10, 1)))[:, :, 0]
            Gh = isq @ LO1.mandel_mat(x[:, 1:7]) @ isq
            out[ik, d0:d1] = (np.linalg.norm(Gh, ord=2, axis=(1, 2)) / Tinf).reshape(d1 - d0, Nt.shape[0])
    return out


def rho_env_search(E, L, Nt, T, dirs, Ed, kref, isq, lo, hi, rng, n_starts=8):
    ks = np.array([lo, math.sqrt(lo * hi), hi]) / L.KPC
    D = rho_env_grid(E, Nt, Ed, ks, kref, isq)
    flat = D.reshape(-1)
    ik, idd, it = np.unravel_index(np.arange(flat.size), D.shape)
    keys = np.concatenate([T[it] / np.pi, dirs[idd]], axis=1)
    pre = np.argpartition(flat, -4000)[-4000:]
    sel = [pre[i] for i in C2.distinct_top(flat[pre], keys[pre], n_starts, 0.15)]
    fr = (0.0, 0.5, 1.0)
    n0, e1, e2 = C2.tangent_basis(np.array([dirs[idd[s]] for s in sel]))
    p0 = np.concatenate([np.array([T[it[s]] for s in sel]), np.zeros((len(sel), 2)), np.array([[fr[ik[s]]] for s in sel])], axis=1)
    llo, lhi = math.log(lo), math.log(hi)

    def f(si, P):
        n = n0[si] + P[:, 3:4] * e1[si] + P[:, 4:5] * e2[si]; n /= np.linalg.norm(n, axis=1)[:, None]
        k = np.exp(llo + (lhi - llo) * P[:, 5]) / L.KPC
        x = C2.env_full(E, n * k[:, None], P[:, :3])
        Gh = isq @ LO1.mandel_mat(x[:, 1:7]) @ isq
        return np.linalg.norm(Gh, ord=2, axis=(1, 2)) * 4.0 * E.B.gam * k * k
    p, fv, its = C2.refine(f, p0, (0.3, 0.3, 0.3, 0.15, 0.15, 0.3), [5], rng)
    j = int(np.argmax(fv)); P = p[j]
    n = n0[j] + P[3] * e1[j] + P[4] * e2[j]; n /= np.linalg.norm(n)
    return dict(rho_G_envelope=float(fv[j]), grid_max=float(flat.max()), n_grid=int(flat.size), iterations=int(its),
                start_values=[float(v) for v in fv], t_at=np.remainder(P[:3], 2 * np.pi).tolist(), dir_at=n.tolist(),
                k_at_inverse_kpc=float(math.exp(llo + (lhi - llo) * P[5])))


def main():
    CC.require_env(); t0 = time.time()
    if CC.sha(C2.V001_TOOLS / 'lo_cert_c2v001.py') != PIN_LO1:
        raise SystemExit('lo_cert_c2v001 pin')
    code = {}
    for k, (p, want, lines) in CODE.items():
        if CC.sha(p) != want:
            raise SystemExit('code pin ' + k)
        code[k] = dict(path=str(p), sha256=want, lines=lines)
    L, B, info, (g, Cb, mu) = CC.qinf_binder()
    rep = CC.repro_qinf_anchor(L, B)
    if not rep['bitwise_equal']:
        raise SystemExit('QINF anchor reproduction failed')
    D = CC.direction_sets(L); E = C2.Envelope(L, B)
    ev, V = np.linalg.eigh(np.asarray(Cb, float)); isq = (V / np.sqrt(ev)) @ V.T
    U, RS, PV = CC.uvt_modules(); jn = PV.create_provider()
    prof = json.loads(Path(CC.pin('profile')['path']).read_text())
    ids, R_rows, tau = CC.row_radii_and_tau()
    case = CC.SavedR3('C4R3')
    units = dict(kpc_m=case.ni['kpc_m'], solar_mass_kg=case.ni['solar_mass_kg'])
    s_edges = prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    i1t = CC.i1t_on_state(RS, PV, case, prof, s_edges, units, jn)
    print('I1-T', i1t, flush=True)
    stars = RS.stars_registered(prof, 'DDO154', units=units)
    ros = RS.roster_rotation(case.source_rotation_arrays(), stars, s_edges_kpc2=s_edges, kpc_m=units['kpc_m'], M_s=64)
    kept = U.kept_region('fs_rotation', {'shape': 'cube', 'kmax_inverse_kpc': None}, case.K / U.KPC_M)
    cfg = CC.uvt_config(U, K_big=K_BIG)
    # rho first (no build needed), then the build
    rng = np.random.default_rng(20261018)
    T12 = C2.torus_grid_v(12); Nt12 = E.native(T12); dirs200 = C2.fib_hemi(200); kref = 10.0 / L.KPC; Ed200 = E.eh_dir(dirs200, kref)
    rhos = {}
    for lo, hi in SHELLS:
        ts = time.time()
        r = LO1.rho_shell(B, L, D, Cb, lo, hi, case.K)
        re = rho_env_search(E, L, Nt12, T12, dirs200, Ed200, kref, isq, float(lo), float(hi), rng)
        rhos[(lo, hi)] = (r, re)
        print('rho (%g,%g] sampled %.4f envelope %.4f (grid %.4f) %.0fs' % (lo, hi, r['rho_G'], re['rho_G_envelope'], re['grid_max'], time.time() - ts), flush=True)
    st = U.build(config=cfg, kept=kept, roster=ros, gamma_eff=case.gamma, c_m_s=CC.C, eval_radii_m=[], jn_provider=jn, i1t=i1t,
                 stage_kind='fs_rotation')
    edges = np.asarray(st._a['shell_edges_inverse_kpc'])
    print('DDO build K_big 256', st.record['quadrature']['N_perp'], st.record['quadrature']['N_z_plus'], 'edges', edges[0], edges[-1],
          '%.0fs' % (time.time() - t0), flush=True)
    v = case.rows
    old, oldpin = C2.v001_record('LO_CERT_K128_V001')
    oldB1 = {tuple(int(x) for x in s['range_inverse_kpc']): s['B1_per_m'] for s in old['shells']}
    out = []
    for lo, hi in SHELLS:
        r, re = rhos[(lo, hi)]
        B0, B1, B2 = LO1.shell_sum(st, lo, hi)
        rho_used = max(r['rho_G'], re['rho_G_envelope'])
        dv = v * R_rows * rho_used * B1 / 4.0
        dvs = v * R_rows * r['rho_G'] * B1 / 4.0
        e = dict(range_inverse_kpc=[float(lo), float(hi)], max_over_tau=float(np.max(dv / tau)), per_row_over_tau=(dv / tau).tolist(),
                 max_over_tau_rho_sampled=float(np.max(dvs / tau)), rho_used=rho_used, rho_G_sampled=r['rho_G'], rho_G_envelope=re['rho_G_envelope'],
                 rho_envelope_search=re, rho_V_sampled=r['rho_V'], B0=float(B0), B1_per_m=float(B1),
                 volume_channel_bound_dln_sqrtg_rho_V_sampled=float(r['rho_V'] * B0), rho_levels=r['levels'],
                 readout_coupled_route_B_over_tau=0.0,
                 B1_v001_K128_build=oldB1.get((lo, hi)),
                 B1_rel_diff_vs_v001=(None if oldB1.get((lo, hi)) is None else float(abs(B1 - oldB1[(lo, hi)]) / oldB1[(lo, hi)])),
                 domain=('complete spherical shell (inside cylinder 256)' if hi <= 256 else 'D cap {256 < |k|} for O = cylinder 256 (K_big 256 production domain)'))
        out.append(e)
        print('LO (%g,%g] max/tau %.3e (rho_sampled %.3e) rho %.3f/%.3f B1 %.3e' % (lo, hi, e['max_over_tau'], e['max_over_tau_rho_sampled'],
              r['rho_G'], re['rho_G_envelope'], B1), flush=True)
    seven = out[:7]
    ok = all(s['max_over_tau'] <= 0.005 for s in out)
    summ = float(sum(s['max_over_tau'] for s in out))
    rowsum = float(np.max(np.sum([s['per_row_over_tau'] for s in out], axis=0)))
    ok = ok and summ <= 0.05
    me = CC.producer(__file__)
    rec = dict(schema=CC.GATE_SCHEMA, gate='LO', verdict='PASS' if ok else 'NON_LAPSE_TAIL_MATERIAL',
               state_result_sha256=case.result_sha, state='C4R3 le3 (saved; K = 4)', i1t=i1t,
               shells=out, summed_max_over_tau=summ,
               summed_definition='sum over ALL 10 shells (4,5] .. (256,363] of the per-shell max over rows (>= the per-row sum, %.3e); '
                                 'the seven V007 shells alone sum to %.3e' % (rowsum, sum(s['max_over_tau'] for s in seven)),
               summed_seven_v007_shells=float(sum(s['max_over_tau'] for s in seven)), max_row_sum_over_tau=rowsum,
               coverage_inverse_kpc=[4.0, 363.0], valid_for_K_big_up_to=K_BIG,
               v_state_km_s=v.tolist(), tau_km_s=tau.tolist(), row_ids=ids, R_kpc=(R_rows / U.KPC_M).tolist(),
               tail_config_sha256=cfg['sha256'], build=dict(K_big=K_BIG, N_perp=st.record['quadrature']['N_perp'], N_z_plus=st.record['quadrature']['N_z_plus'],
                                                           shell_edges=[float(edges[0]), float(edges[-1])], production_admissible=st.record['production_admissible']),
               producer=me, common=CC.producer(C2.HERE / 'certs2_common_c2v002.py'), method=__doc__.split('Usage:')[0].strip(),
               method_v001=LO1.__doc__.split('Usage:')[0].strip(), evaluator_sha256=CC.PINS['qinf_evaluator'][1],
               qinf_anchor_reproduction_bitwise=rep['bitwise_equal'], code_reading=code,
               label='bound estimate: rho is a sampled / locally maximized sup (the envelope dominates the actual set); B1 is quadrature; not a proven sup',
               supersedes={'LO_CERT_V001': C2.v001_record('LO_CERT_V001')[1], 'LO_CERT_K128_V001': oldpin},
               pins={k: CC.pin(k) for k in ('uvt_lapse', 'uvt_roster', 'uvt_jn', 'profile', 'row_binding', 'prereg_v005')},
               decisions=C2.decisions(), seconds=round(time.time() - t0, 1))
    h = C2.write_new(C2.CERT2 / 'gates/LO_CERT_V002.json', rec)
    print(json.dumps(dict(LO_CERT_V002=[rec['verdict'], summ, h], seconds=round(time.time() - t0, 1))))


if __name__ == '__main__':
    main()
