"""EPS certificate V005 (successor of certificates_v001 eps_cert_c2v004.py / gates/EPS_CERT_V004.json, which stay unedited).
Root A52 ruling 5 and certificates_v001 CHECK F1/F5.  Replay only; no launch.

Per unit shell (n, n+1], n = 2 .. 362  (coverage DDO [2, 363] >= sqrt2 x 256 = 362.04; NGC [2, 46] >= sqrt2 x 32 = 45.25;
one symbol for both galaxies, galaxy independence TESTED in certificates_v001 EPS_SAMPLES_V002):
  (1) the REGISTERED RULE exactly as certificates_v001 (eps_cert_c2v002.certify: base 13+13 dirs x 64/decade, refined
      26+26 x 128/decade, one further 104 x 256/decade refinement allowed; 2 failures -> EPS_UNCERTIFIED): eps_base,
      eps_refined, refinements -- kept alongside, and they alone decide the record verdict (CERTIFIED / EPS_UNCERTIFIED);
  (2) the ENVELOPE sup (certs2_common Envelope): sup over direction x |k| in the shell x the cardinal torus t in T^3 of
      |1 - q_env(k, t)|.  It dominates the actual shell because F(k) is the convex combination at t = t(k).  Computed by a
      global product grid (torus 12^3 incl. the vertices 0, pi; 200 hemisphere directions; |k| = lo, mid, hi) and a
      batched local maximization from the 8 best distinct grid points plus the previous shell's optimum; its convergence
      is audited on 17 shells with a denser grid (torus 20^3, 400 directions, 16 starts);
  (3) ACTUAL-SET values: the 10000-direction dense audit of V004 (recomputed, reproduction vs V004 recorded), and a
      local maximization over the actual shell (direction x |k|) from the 6 best of 2000 directions x 64/decade plus the
      dense and rule argmaxima (a LOWER bound of the actual sup above ~5 /kpc, where the actual set is oscillatory in t);
      the cache / stored-operator node maxima are carried from EPS_CERT_V004 (shells 2..6), and the independent check's
      own sup (certificates_v001 check/out/EPS_SUP_SUPP.json 0ddec5a7, 12 shells) is folded in where it exists.
Per-shell eps (field_bound): shells with lo >= 5: eps = max(envelope, every actual-set value) (the envelope; the max only
guards the search); shells (2,3] (3,4] (4,5]: eps = max(actual-set values) (directional sup converged there, CHECK F1
own sup / record 1.0005, 0.9995, 1.0011), with eps_envelope recorded.  eps_max = max over shells of eps.
|1 - q| is the complex modulus for (2)/(3)-local (>= |1 - Re q|; |Im q| <= 1e-15); the rule and dense audit keep Re q.
Usage: python3 -I -B eps_cert_c2v005.py  (writes out/EPS_SAMPLES_V005.json, gates/EPS_CERT_V005.json)"""
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
import eps_cert_c2v002 as E2  # noqa: E402  (functions only)
import eps_cert_c2v004 as E4  # noqa: E402  (functions only)

PIN_E2 = 'e41548099df88f3622892e0342597482d8e3df5b4230a0b87e600286071ef62a'
PIN_E4 = 'c62f2e6eb25ff06c8da4bfd91f99833ff57c92b6d9c01bff89c32b47857f1162'
CHECK_SUP = (C2.V001 / 'check/out/EPS_SUP_SUPP.json', '0ddec5a7b7d5d5e74b9a2874ea1a3d2d44a638757cb4a862209a2c7c5151747c')
N_LO, N_HI = 2, 363
AUDIT_SHELLS = (2, 3, 4, 5, 6, 8, 12, 16, 19, 32, 45, 63, 64, 100, 128, 181, 256, 362)


def env_search(E, L, Nt, T, dirs, Ed, kref, lo, hi, rng, n_starts=8, extra=None, ks_frac=(0.0, 0.5, 1.0)):
    ks = np.array([lo + f * (hi - lo) for f in ks_frac]) / L.KPC
    D = E.dev_grid(Nt, Ed, ks, kref)                                   # [nk, nd, nt]
    flat = D.reshape(-1); nk, nd, nt = D.shape
    ik, idd, it = np.unravel_index(np.arange(flat.size), D.shape)
    keys = np.concatenate([T[it] / np.pi, dirs[idd]], axis=1)
    # coarse prefilter for speed: top 4000 then distinct
    pre = np.argpartition(flat, -4000)[-4000:]
    sel = [pre[i] for i in C2.distinct_top(flat[pre], keys[pre], n_starts, 0.15)]
    starts_t = [T[it[s]] for s in sel]; starts_n = [dirs[idd[s]] for s in sel]; starts_s = [ks_frac[ik[s]] for s in sel]
    if extra is not None:
        starts_t.append(np.asarray(extra['t'])); starts_n.append(np.asarray(extra['dir'])); starts_s.append(float(np.clip((extra['k'] - lo) / (hi - lo), 0, 1)))
    n0, e1, e2 = C2.tangent_basis(np.array(starts_n))
    p0 = np.concatenate([np.array(starts_t), np.zeros((len(starts_t), 2)), np.array(starts_s)[:, None]], axis=1)

    def f(si, P):
        n = n0[si] + P[:, 3:4] * e1[si] + P[:, 4:5] * e2[si]; n /= np.linalg.norm(n, axis=1)[:, None]
        k = (lo + (hi - lo) * P[:, 5]) / L.KPC
        return np.abs(1.0 - E.q(n * k[:, None], P[:, :3]))
    p, fv, its = C2.refine(f, p0, (0.3, 0.3, 0.3, 0.15, 0.15, 0.3), [5], rng)
    j = int(np.argmax(fv)); P = p[j]
    n = n0[j] + P[3] * e1[j] + P[4] * e2[j]; n /= np.linalg.norm(n)
    kbest = lo + (hi - lo) * P[5]
    qx = E.q((n * kbest / L.KPC)[None], P[None, :3])[0]
    return dict(eps_envelope=float(abs(1 - qx)), grid_max=float(flat.max()), n_grid=int(flat.size), n_starts=len(p0),
                start_values=[float(x) for x in fv], iterations=int(its), t_at=np.remainder(P[:3], 2 * np.pi).tolist(), dir_at=n.tolist(),
                k_at_inverse_kpc=float(kbest), max_abs_imag_q_at=float(abs(qx.imag)))


def actual_search(B, L, lo, hi, dirs2000, rng, seeds):
    ks = CC.shell_k(lo, hi, 64)
    kv = np.concatenate([dirs2000 * (k / L.KPC) for k in ks])
    dev = np.abs(1.0 - CC.q_of(B, kv))
    nd = len(dirs2000)
    keys = np.concatenate([dirs2000[np.arange(len(kv)) % nd], (np.repeat(ks, nd) / hi)[:, None]], axis=1)
    sel = C2.distinct_top(dev, keys, 6, 0.1)
    sn = [dirs2000[s % nd] for s in sel] + [np.asarray(x['dir'], float) for x in seeds]
    ss = [float((ks[s // nd] - lo) / (hi - lo)) for s in sel] + [float(np.clip((x['k'] - lo) / (hi - lo), 0, 1)) for x in seeds]
    n0, e1, e2 = C2.tangent_basis(np.array(sn))
    p0 = np.concatenate([np.zeros((len(sn), 2)), np.array(ss)[:, None]], axis=1)

    def f(si, P):
        n = n0[si] + P[:, 0:1] * e1[si] + P[:, 1:2] * e2[si]; n /= np.linalg.norm(n, axis=1)[:, None]
        k = (lo + (hi - lo) * P[:, 2]) / L.KPC
        return np.abs(1.0 - CC.q_of(B, n * k[:, None]))
    p, fv, its = C2.refine(f, p0, (0.1, 0.1, 0.3), [2], rng)
    j = int(np.argmax(fv)); P = p[j]
    n = n0[j] + P[0] * e1[j] + P[1] * e2[j]; n /= np.linalg.norm(n)
    return dict(eps_actual_local_max=float(fv[j]), grid_max=float(dev.max()), iterations=int(its), dir_at=n.tolist(),
                k_at_inverse_kpc=float(lo + (hi - lo) * P[2]))


def main():
    CC.require_env(); t0 = time.time()
    for p, want in ((C2.V001_TOOLS / 'eps_cert_c2v002.py', PIN_E2), (C2.V001_TOOLS / 'eps_cert_c2v004.py', PIN_E4)):
        if CC.sha(p) != want:
            raise SystemExit('pin ' + str(p))
    L, B, info, (g, Cb, mu) = CC.qinf_binder()
    rep = CC.repro_qinf_anchor(L, B)
    if not (rep['bitwise_equal'] and rep['gamma_equal']):
        raise SystemExit('QINF anchor reproduction failed')
    E = C2.Envelope(L, B)
    # self-test: env_q(k, t(k)) == q_of(k) bitwise
    rng = np.random.default_rng(20261018)
    kv = rng.standard_normal((2000, 3)); kv /= np.linalg.norm(kv, axis=1)[:, None]; kv *= rng.uniform(2, 363, (2000, 1)) / L.KPC
    selftest = dict(n=2000, bitwise_equal=bool(np.array_equal(E.q(kv, E.t_of(kv)), CC.q_of(B, kv))))
    if not selftest['bitwise_equal']:
        raise SystemExit('envelope self-test failed')
    print('self-test', selftest, flush=True)
    D = CC.direction_sets(L)
    dense2 = E4.fib_sphere(2000); dense = np.concatenate([dense2, E4.fib_sphere(8000)])
    v4, v4pin = C2.v001_record('EPS_CERT_V004'); v4k, v4kpin = C2.v001_record('EPS_CERT_K128_V004')
    v4sh = {int(s['lo_inverse_kpc']): s for s in v4k['shells']}
    if CC.sha(CHECK_SUP[0]) != CHECK_SUP[1]:
        raise SystemExit('check sup pin')
    chk = {int(x['shell'][0]): float(x['sup_estimate']) for x in json.loads(Path(CHECK_SUP[0]).read_text())['shells']}
    T12 = C2.torus_grid_v(12); Nt12 = E.native(T12)
    dirs200 = C2.fib_hemi(200); kref = 10.0 / L.KPC; Ed200 = E.eh_dir(dirs200, kref)
    shells = []; prev = None
    for n in range(N_LO, N_HI):
        lo, hi = float(n), float(n + 1); ts = time.time()
        s = E2.certify(B, L, D, lo, hi)
        da = E4.dense_eps(B, L, lo, hi, dense)
        s['dense_audit'] = da
        env = env_search(E, L, Nt12, T12, dirs200, Ed200, kref, lo, hi, rng, extra=prev)
        prev = dict(t=env['t_at'], dir=env['dir_at'], k=env['k_at_inverse_kpc'] + 1.0)
        seeds = [dict(dir=da['dir_at_max'], k=da['k_at_max_inverse_kpc'])] + [dict(dir=v['dir_at_max'], k=v['k_at_max_inverse_kpc']) for v in s['levels'].values()]
        act = actual_search(B, L, lo, hi, dense2, rng, seeds)
        old = v4sh.get(n)
        nodes = old['eps_node_maxima'] if old else {'DDO_C4R3_cache_7b9816ae': None, 'NGC_T120L_stored_operator': None}
        actual_vals = [s['eps_base'], s['eps_refined'], da['eps'], act['eps_actual_local_max']] + [v for v in nodes.values() if v is not None]
        if n in chk:
            actual_vals.append(chk[n])
        eps_actual = float(max(actual_vals))
        if lo >= 5.0:
            eps = float(max(env['eps_envelope'], eps_actual)); src = 'envelope'
        else:
            eps = eps_actual; src = 'actual_set_max (converged: CHECK F1)'
        s.update(envelope=env, actual_local=act, eps_node_maxima_from_V004=nodes, eps_check_own_sup=chk.get(n), eps_actual_set=eps_actual, eps=eps, eps_source=src,
                 envelope_dominates_actual=bool(env['eps_envelope'] >= eps_actual * (1 - 1e-12)),
                 envelope_over_actual=env['eps_envelope'] / eps_actual,
                 v004=None if old is None else dict(eps=old['eps'], eps_dense_audit=old['eps_dense_audit'], eps_base=old['eps_base'], eps_refined=old['eps_refined']),
                 seconds=round(time.time() - ts, 2))
        if old is not None:
            s['v004_rule_reproduced'] = bool(old['eps_base'] == s['eps_base'] and old['eps_refined'] == s['eps_refined'] and old['refinements'] == s['refinements'])
            s['v004_dense_reproduced'] = bool(old['eps_dense_audit'] == da['eps'])
        shells.append(s)
        if n <= 8 or n % 16 == 0 or n in AUDIT_SHELLS or s['refinements'] > 0 or not s['envelope_dominates_actual']:
            print('(%d,%d] rule %.4e/%.4e r%d dense %.4e act %.4e env %.4e env/act %.3f eps %.4e [%s] %.1fs' % (
                n, n + 1, s['eps_base'], s['eps_refined'], s['refinements'], da['eps'], act['eps_actual_local_max'], env['eps_envelope'],
                s['envelope_over_actual'], eps, src[:8], s['seconds']), flush=True)
    # convergence audit of the envelope search (denser grid, more starts)
    T20 = C2.torus_grid_v(20); Nt20 = E.native(T20); dirs400 = C2.fib_hemi(400); Ed400 = E.eh_dir(dirs400, kref)
    audit = []
    for n in AUDIT_SHELLS:
        lo, hi = float(n), float(n + 1)
        a = env_search(E, L, Nt20, T20, dirs400, Ed400, kref, lo, hi, rng, n_starts=16, ks_frac=(0.0, 0.25, 0.5, 0.75, 1.0))
        prod = shells[n - N_LO]['envelope']['eps_envelope']
        audit.append(dict(shell=[lo, hi], production=prod, dense=a['eps_envelope'], dense_over_production=a['eps_envelope'] / prod,
                          dense_t_at=a['t_at'], dense_dir_at=a['dir_at'], dense_k_at=a['k_at_inverse_kpc'], dense_grid_max=a['grid_max']))
        print('audit (%d,%d] prod %.6e dense %.6e ratio %.8f' % (n, n + 1, prod, a['eps_envelope'], a['eps_envelope'] / prod), flush=True)
    me = CC.producer(__file__)
    common = CC.producer(C2.HERE / 'certs2_common_c2v002.py')
    samples = dict(schema='UVT_EPS_SAMPLES_C2V005', producer=me, common=common, evaluator=info, qinf_anchor_reproduction=rep,
                   envelope_self_test=selftest, supersedes={'EPS_CERT_V004': v4pin, 'EPS_CERT_K128_V004': v4kpin},
                   envelope_rule='torus 12^3 (vertices 0, pi included) x 200 Fibonacci hemisphere directions x |k| in {lo, mid, hi}; 8 distinct best + previous optimum -> batched local maximization (t, direction, |k|)',
                   envelope_audit_rule='torus 20^3 x 400 directions x 5 |k| values; 16 distinct starts', envelope_audit=audit,
                   shells=shells, seconds=round(time.time() - t0, 1))
    s_sha = C2.write_new(C2.CERT2 / 'out/EPS_SAMPLES_V005.json', samples)
    ok_rule = all(s['refinements'] <= 1 and s['eps_refined'] <= 1.1 * s['eps_base'] for s in shells)
    keep = ('range_inverse_kpc', 'lo_inverse_kpc', 'hi_inverse_kpc', 'eps_base', 'eps_refined', 'refinements', 'eps', 'eps_source')
    sh = []
    for s in shells:
        e = {k: s[k] for k in keep}
        e.update(eps_envelope=s['envelope']['eps_envelope'], eps_actual_set=s['eps_actual_set'], eps_actual_local_max=s['actual_local']['eps_actual_local_max'],
                 eps_dense_audit=s['dense_audit']['eps'], eps_node_maxima=s['eps_node_maxima_from_V004'], eps_check_own_sup=s['eps_check_own_sup'],
                 eps_v004=None if s['v004'] is None else s['v004']['eps'], envelope_over_actual=s['envelope_over_actual'])
        sh.append(e)
    max_audit = max(a['dense_over_production'] for a in audit)
    rec = dict(schema=CC.GATE_SCHEMA, gate='EPS', verdict='CERTIFIED' if ok_rule else 'EPS_UNCERTIFIED', producer=me,
               eps_max=float(max(s['eps'] for s in shells)),
               eps_max_shell=shells[int(np.argmax([s['eps'] for s in shells]))]['range_inverse_kpc'],
               eps_max_envelope_all_shells=float(max(s['envelope']['eps_envelope'] for s in shells)),
               eps_max_actual_set=float(max(s['eps_actual_set'] for s in shells)),
               evaluator_sha256=CC.PINS['qinf_evaluator'][1], evaluator_path=str(CC.PINS['qinf_evaluator'][0]),
               inverse_cache={'sha256': CC.PINS['inverse_cache'][1], 'node_maxima_folded': True, 'node_maxima_source': v4pin},
               check_own_sup_folded={'path': str(CHECK_SUP[0]), 'sha256': CHECK_SUP[1], 'shells': sorted(chk)},
               coverage_inverse_kpc={'DDO': [float(N_LO), float(N_HI)], 'NGC': [2.0, 46.0]},
               coverage_note='DDO [2,363] >= sqrt2 x 256 = 362.04 (the module unit shells from K end at ceil(sqrt2 K_big)); NGC [2,46] >= sqrt2 x 32 = 45.25; one symbol (galaxy independence TESTED, certificates_v001)',
               shells=sh,
               method=__doc__.split('Usage:')[0].strip(),
               envelope_audit=dict(shells=[a['shell'] for a in audit], max_dense_over_production=max_audit,
                                   min_dense_over_production=min(a['dense_over_production'] for a in audit)),
               envelope_dominates_actual_every_shell=bool(all(s['envelope_dominates_actual'] for s in shells)),
               samples={'path': str(C2.CERT2 / 'out/EPS_SAMPLES_V005.json'), 'sha256': s_sha},
               label=('shells lo >= 5: eps = envelope sup (sup over direction x |k| x cardinal torus; dominates the actual set by '
                      'construction; the sup of the envelope itself is a numerical maximization, audited); shells lo < 5: actual-set '
                      'sampled + locally maximized sup (converged per CHECK F1). Not a proven sup: no Lipschitz certificate of the search.'),
               supersedes={'EPS_CERT_V004': v4pin, 'EPS_CERT_K128_V004': v4kpin},
               decisions=C2.decisions())
    h = C2.write_new(C2.CERT2 / 'gates/EPS_CERT_V005.json', rec)
    print(json.dumps(dict(EPS_CERT_V005=[rec['verdict'], rec['eps_max'], rec['eps_max_shell'], h], eps_max_envelope_all=rec['eps_max_envelope_all_shells'],
                          envelope_dominates=rec['envelope_dominates_actual_every_shell'], audit_max_ratio=max_audit,
                          refinements=[s['range_inverse_kpc'] for s in shells if s['refinements']], seconds=round(time.time() - t0, 1))))


if __name__ == '__main__':
    main()
