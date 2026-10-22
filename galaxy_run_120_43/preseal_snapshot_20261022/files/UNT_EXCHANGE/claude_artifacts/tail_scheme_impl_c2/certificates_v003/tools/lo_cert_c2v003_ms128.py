"""LO (DDO) certificate V003 at the production gas M_s 128 (root A57.1: "the LO certificate recomputed with the M_s 128 source.
The transfer of the M_s 64 LO bound is UNTESTED, so it is not relied on"; Codex3 0591 CX3-C3).  Successor of
certificates_v002 gates/LO_CERT_V002.json (M_s 64, fd4fa52b), which stays unedited.  Replay only; no launch.

Same object, method, shells and rho search as LO_CERT_V002 (certificates_v002 tools/lo_cert_c2v002.py, 1ad8504e, whose
functions are imported read-only; its method text is kept in method_v002):
  |dv_i,s| <= (v_i R_i / 4) rho_s B1_s,  rho_used = max(rho_sampled, rho_envelope);
  B1_s = the module's own shell integral (int_{D cap s} |k| T_inf |S_T|) from ONE build of the saved C4R3 le3 roster with the
  gas columns at M_s = 128 (tail config gas.M_s = 128), O = cylinder 256, kept cube 4 (TEST_ONLY certificate sentinels, as a
  replay must be); I1-T on that state recorded.
Only S_T (hence B1) depends on M_s.  rho_s is a function of the symbol alone (QINF evaluator route, no source enters); it is
recomputed here with the same seeded search and compared with LO_CERT_V002 (rho_equal_v002 per shell).
Shells: (4,5] .. (32,64] (the seven V007 shells), (64,128], (128,256], and (256,363] = D cap {|k| > 256} for O = cylinder 256
(the module's last unit-shell edge is ceil(sqrt2 x 256) = 363 because node |k| reaches 362.04; the commission's "(256,362]"
would leave the nodes in (362, 362.04] uncovered, so 363 is used, as in V002).
envelope_bound: {rule A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS, coverage_max_inverse_kpc} names the rho envelope
(sup over direction x |k| x the cardinal torus, a numerical search, not a proof; A57.4 / CX3-C2).
Usage: python3 -I -B lo_cert_c2v003_ms128.py"""
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certs3_common_c2v003 as C3  # noqa: E402

CC = C3.CC; C2 = C3.C2
import lo_cert_c2v002 as LO2  # noqa: E402  (functions only; on sys.path via certs3_common)

PIN_LO2 = '1ad8504e5d13af4b62c2d59aa30d603ba6f64e1662710169c41e645a2e4e8975'
K_BIG = 256.0
EPS_ENVELOPE_RULE = 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS'


def main():
    CC.require_env(); t0 = time.time()
    if CC.sha(C3.V002_TOOLS / 'lo_cert_c2v002.py') != PIN_LO2:
        raise SystemExit('lo_cert_c2v002 pin')
    code = {}
    for k, (p, want, lines) in LO2.CODE.items():
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
    ids, R_rows, tau = CC.row_radii_and_tau()
    case, ros, i1t, units, prof, s_edges = C3.ddo_roster(U, RS, PV, jn, 'C4R3', C3.MS_PROD)
    print('I1-T', i1t, 'gas M_s', ros.gas.M_s, flush=True)
    kept = U.kept_region('fs_rotation', {'shape': 'cube', 'kmax_inverse_kpc': None}, case.K / U.KPC_M)
    cfg = CC.uvt_config(U, K_big=K_BIG, M_s=C3.MS_PROD)
    old, oldpin = C3.v002_record('LO_CERT_V002')
    oldsh = {tuple(float(x) for x in s['range_inverse_kpc']): s for s in old['shells']}
    rng = np.random.default_rng(20261018)
    T12 = C2.torus_grid_v(12); Nt12 = E.native(T12); dirs200 = C2.fib_hemi(200); kref = 10.0 / L.KPC; Ed200 = E.eh_dir(dirs200, kref)
    rhos = {}
    for lo, hi in LO2.SHELLS:
        ts = time.time()
        r = LO2.LO1.rho_shell(B, L, D, Cb, lo, hi, case.K)
        re = LO2.rho_env_search(E, L, Nt12, T12, dirs200, Ed200, kref, isq, float(lo), float(hi), rng)
        rhos[(lo, hi)] = (r, re)
        print('rho (%g,%g] sampled %.4f envelope %.4f %.0fs' % (lo, hi, r['rho_G'], re['rho_G_envelope'], time.time() - ts), flush=True)
    st = U.build(config=cfg, kept=kept, roster=ros, gamma_eff=case.gamma, c_m_s=CC.C, eval_radii_m=[], jn_provider=jn, i1t=i1t,
                 stage_kind='fs_rotation')
    edges = np.asarray(st._a['shell_edges_inverse_kpc'])
    print('DDO build K_big 256 M_s 128', st.record['quadrature']['N_perp'], st.record['quadrature']['N_z_plus'], 'edges', edges[0], edges[-1],
          'roster', st.record['roster_record']['gas'], '%.0fs' % (time.time() - t0), flush=True)
    v = case.rows
    out = []
    for lo, hi in LO2.SHELLS:
        r, re = rhos[(lo, hi)]
        B0, B1, B2 = LO2.LO1.shell_sum(st, lo, hi)
        rho_used = max(r['rho_G'], re['rho_G_envelope'])
        dv = v * R_rows * rho_used * B1 / 4.0
        dvs = v * R_rows * r['rho_G'] * B1 / 4.0
        o = oldsh[(float(lo), float(hi))]
        e = dict(range_inverse_kpc=[float(lo), float(hi)], max_over_tau=float(np.max(dv / tau)), per_row_over_tau=(dv / tau).tolist(),
                 max_over_tau_rho_sampled=float(np.max(dvs / tau)), rho_used=rho_used, rho_G_sampled=r['rho_G'], rho_G_envelope=re['rho_G_envelope'],
                 rho_envelope_search=re, rho_V_sampled=r['rho_V'], B0=float(B0), B1_per_m=float(B1),
                 volume_channel_bound_dln_sqrtg_rho_V_sampled=float(r['rho_V'] * B0), rho_levels=r['levels'],
                 readout_coupled_route_B_over_tau=0.0,
                 B1_ms64_LO_CERT_V002=o['B1_per_m'], B1_ratio_ms128_over_ms64=float(B1 / o['B1_per_m']),
                 max_over_tau_ms64_LO_CERT_V002=o['max_over_tau'],
                 rho_equal_v002=dict(rho_G_sampled=bool(r['rho_G'] == o['rho_G_sampled']), rho_G_envelope=bool(re['rho_G_envelope'] == o['rho_G_envelope']),
                                     rho_V_sampled=bool(r['rho_V'] == o['rho_V_sampled'])),
                 domain=('complete spherical shell (inside cylinder 256)' if hi <= 256 else 'D cap {256 < |k|} for O = cylinder 256 (K_big 256 production domain)'))
        out.append(e)
        print('LO (%g,%g] max/tau %.3e (M_s 64: %.3e) B1 ratio %.9f rho equal %s' % (lo, hi, e['max_over_tau'], o['max_over_tau'],
              e['B1_ratio_ms128_over_ms64'], e['rho_equal_v002']), flush=True)
    seven = out[:7]
    summ = float(sum(s['max_over_tau'] for s in out))
    rowsum = float(np.max(np.sum([s['per_row_over_tau'] for s in out], axis=0)))
    ok = all(s['max_over_tau'] <= 0.005 for s in out) and summ <= 0.05
    rho_env_max = float(max(s['rho_G_envelope'] for s in out))
    rec = dict(schema=CC.GATE_SCHEMA, gate='LO', verdict='PASS' if ok else 'NON_LAPSE_TAIL_MATERIAL',
               state_result_sha256=case.result_sha, state='C4R3 le3 (saved; K = 4)', i1t=i1t,
               gas_M_s=int(C3.MS_PROD), source='C4R3 le3 rotation roster with gas columns at M_s 128 (A57.1)',
               shells=out, summed_max_over_tau=summ,
               summed_definition='sum over ALL 10 shells (4,5] .. (256,363] of the per-shell max over rows (>= the per-row sum, %.3e); '
                                 'the seven V007 shells alone sum to %.3e' % (rowsum, sum(s['max_over_tau'] for s in seven)),
               summed_seven_v007_shells=float(sum(s['max_over_tau'] for s in seven)), max_row_sum_over_tau=rowsum,
               coverage_inverse_kpc=[4.0, 363.0], valid_for_K_big_up_to=K_BIG,
               envelope_bound=dict(rule=EPS_ENVELOPE_RULE, coverage_max_inverse_kpc=363.0, rho_G_envelope_max=rho_env_max,
                                   label='rho envelope = sup over direction x |k| x cardinal torus by numerical search (estimate, not a proven sup; A57.4)'),
               ms64_transfer=dict(record=oldpin, max_B1_rel_change=float(max(abs(s['B1_ratio_ms128_over_ms64'] - 1.0) for s in out)),
                                  max_over_tau_max_abs_change=float(max(abs(s['max_over_tau'] - s['max_over_tau_ms64_LO_CERT_V002']) for s in out)),
                                  note='measured here, not assumed: the M_s 64 record is superseded for the M_s 128 production source'),
               v_state_km_s=v.tolist(), tau_km_s=tau.tolist(), row_ids=ids, R_kpc=(R_rows / U.KPC_M).tolist(),
               tail_config_sha256=cfg['sha256'], tail_config_gas=cfg['gas'],
               build=dict(K_big=K_BIG, N_perp=st.record['quadrature']['N_perp'], N_z_plus=st.record['quadrature']['N_z_plus'],
                          shell_edges=[float(edges[0]), float(edges[-1])], production_admissible=st.record['production_admissible'],
                          roster_gas=st.record['roster_record']['gas'], roster_digest=st.record['roster_digest']),
               producer=CC.producer(__file__), common=CC.producer(C3.HERE / 'certs3_common_c2v003.py'), method=__doc__.split('Usage:')[0].strip(),
               method_v002=LO2.__doc__.split('Usage:')[0].strip(), evaluator_sha256=CC.PINS['qinf_evaluator'][1],
               qinf_anchor_reproduction_bitwise=rep['bitwise_equal'], code_reading=code,
               label='bound estimate: rho is a sampled / locally maximized sup (the envelope dominates the actual set); B1 is quadrature; not a proven sup',
               supersedes_for_ms128={'LO_CERT_V002': oldpin},
               pins={k: CC.pin(k) for k in ('uvt_lapse', 'uvt_roster', 'uvt_jn', 'profile', 'row_binding', 'prereg_v005')},
               decisions=C3.decisions(), seconds=round(time.time() - t0, 1))
    h = C3.write_new(C3.CERT3 / 'gates/LO_CERT_V003_MS128.json', rec)
    print(json.dumps(dict(LO_CERT_V003_MS128=[rec['verdict'], summ, h], seconds=round(time.time() - t0, 1))))


if __name__ == '__main__':
    main()
