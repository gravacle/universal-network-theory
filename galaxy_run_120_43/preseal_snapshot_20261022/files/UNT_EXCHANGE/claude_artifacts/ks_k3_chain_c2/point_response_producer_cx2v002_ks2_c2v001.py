"""KS2 (ks_k3_chain_c2 c2v001; root A160): point_response_producer_cx2v002 (a1dcdea8) with the shell lower edge at the
spec's kept K, for S1_UA_C3T only (KS1's gate: the C3T label AND the CB C3T grid, bitwise).

For S1_UA_C3T (kept K = max(breaks_inverse_kpc) = 3): EPS has 179 unit shells [3,4]..[181,182]; rho has the 10-shell
partition [3,4],[4,5],[5,6],[6,8],[8,12],[12,16],[16,32],[32,64],[64,128],[128,182]; required_coverage_inverse_kpc is
[3, 182]; the rho sampled levels keep the k outside the K=3 cube (a1dcdea8 L347 kept those outside the K=4 cube, which
leaves the [3,4] shell empty); audit shells (AUDIT_LO) unchanged. Custody is KS1. Every other spec is handed to the
unchanged a1dcdea8 module object (P, by path and sha): its records, producer and custody pins included, are a1dcdea8's.

Independent point-scoped numerical EPS/rho producer; static replay only.

No scientific run or solver is launched. The registered EPS discrete rule is
kept distinct from the cardinal-torus numerical search. All finite/search
maxima are estimates (lower bounds on the continuous supremum), never a
rigorous enclosure. A smoke/subset result cannot become an admission proof.
Input is the actual DDO154 forward-call spec. Output creation is exclusive.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time

import numpy as np

HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # KS2: a1dcdea8's folder
ART = HERE.parent.parent
CUSTODY_PATH = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/custody_cx2v002_ks1_c2v001.py')   # KS2: KS1 (it hands every other spec to 6810b7c3)
CUSTODY_SHA = 'ad020470aee354201ab6c68926784d75d3ebe2e16628323d49280bd2eb18aea6'
PREDECESSOR = (HERE / 'point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231')
C2_PATH = HERE / 'certs2_common_r5_cx2v001.py'
C2_SHA = 'f8f422f034153b4551e5fd5f89740cb594cb9d877e54b467c617206d2fcd6d8c'
LWR_SHA = '758740ebf6caeb80876497674c3ee844f0ec8a9d0fae5d1fb8d491376e3aff48'
EPS_SCHEMA = 'UNT_POINT_EPS_NUMERICAL_CX2V001'
RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'
AUDIT_LO = (4, 5, 6, 8, 12, 16, 19, 32, 45, 63, 64, 100, 128, 181)
SETTINGS = {
    'registered': dict(torus=12, directions=200, starts=8, candidates=48,
                       iterations=120, actual_dirs=2000, dense_dirs=8000,
                       audit_torus=20, audit_dirs=400, audit_starts=16),
    'smoke': dict(torus=4, directions=16, starts=3, candidates=12,
                  iterations=20, actual_dirs=32, dense_dirs=64,
                  audit_torus=6, audit_dirs=24, audit_starts=4),
}


def _module(path, name, expected):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('dependency byte pin mismatch: ' + str(path))
    sp = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(sp)
    sys.modules[name] = obj
    sp.loader.exec_module(obj)
    return obj


P = _module(PREDECESSOR[0], 'ks2_predecessor_point_response_cx2v002', PREDECESSOR[1])   # KS2: a1dcdea8, unchanged
CU = _module(CUSTODY_PATH, 'ks2_response_custody_ks1', CUSTODY_SHA)
C2 = _module(C2_PATH, 'ks2_response_c2', C2_SHA)
CC = C2.CC


def kept_k(spec):
    """KS2: the spec's kept K, max(breaks_inverse_kpc) (procedure section 2). Only S1_UA_C3T reaches it: 3."""
    k = max(spec['numerics']['composite_grid_spec']['breaks_inverse_kpc'])
    if k != CU.S1_C3T_KEPT_K:
        raise ValueError('S1_UA_C3T kept K must be 3')
    return int(k)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def finite(a, name, *, positive=False, nonnegative=False):
    a = np.asarray(a)
    if a.dtype.hasobject or not np.isfinite(a).all():
        raise ValueError('non-finite ' + name)
    if positive and np.any(a <= 0):
        raise ValueError('non-positive ' + name)
    if nonnegative and np.any(a < 0):
        raise ValueError('negative ' + name)
    return a


def point_context(spec):
    """Derive trusted custody and a new Binder at THIS point, not the anchor."""
    if not CU.s1_c3t_spec(spec):
        return P.point_context(spec)                          # KS2: a1dcdea8's own code path
    details = CU.derive_details(spec=spec)
    if CU.sha(CC.PINS['lwr_common'][0]) != LWR_SHA:
        raise ValueError('lwr dependency changed')
    L, anchor, anchor_info, (grid, cb, mu) = CC.qinf_binder()
    rep = CC.repro_qinf_anchor(L, anchor)
    if not rep['bitwise_equal'] or not rep['gamma_equal']:
        raise ValueError('anchor evaluator reproduction failed')
    p = spec['physical']
    finite(list(p.values()), 'physical', positive=True)
    s = float(p['common_scale_s'])
    binder = L.Binder(grid, cb, mu, Eref=s * p['Eref_J'],
                      ell=p['ell_F_m'], gam=s * p['gamma'])
    env = C2.Envelope(L, binder)
    ev, vec = np.linalg.eigh(cb)
    finite(ev, 'Cbar eigenvalues', positive=True)
    isq = (vec / np.sqrt(ev)) @ vec.T
    # Sparse independent reference path uses the original pinned symbol modules.
    directions = CC.direction_sets(L)
    probe = directions[0][[0, 4, 8, 12]] * np.array([4.25, 5.5, 16.5, 64.5])[:, None] / L.KPC
    q = CC.q_of(binder, probe)
    qe = env.q(probe, env.t_of(probe))
    qr = np.array([4 * binder.gam * np.dot(k, k) * L.T_module(
        k, grid, cb, mu, Eref=binder.Eref, ell=binder.ell, gam=binder.gam)[0] for k in probe])
    rel = float(np.max(np.abs(q - qr) / np.maximum(1.0, np.abs(qr))))
    if rel > 2e-8 or not np.array_equal(q, qe):
        raise ValueError('point symbol reference/envelope self-check failed')
    source_pins = {k: v for k, v in anchor_info['pins'].items()}
    source_pins.update(custody=CU.pin(CUSTODY_PATH), envelope=CU.pin(C2_PATH),
                       producer=CU.pin(__file__))
    for name, pin in L.MODS.items():
        source_pins['reference_' + name] = CU.pin(pin['path'])
    return dict(L=L, B=binder, E=env, cb=cb, isq=isq, D=directions,
                details=details, spec=spec, source_pins=source_pins,
                checks=dict(anchor_bitwise=True, envelope_actual_bitwise=True,
                            original_symbol_nodes=4, max_relative_q_reference=rel), cache={})


def shell_plan(spec, shell_ranges=None, *, unit=True):
    if not CU.s1_c3t_spec(spec):
        return P.shell_plan(spec, shell_ranges, unit=unit)    # KS2: a1dcdea8's own code path
    K = kept_k(spec)                                          # KS2: lower edge = the kept K (3), not the literal 4
    end = int(math.ceil(math.sqrt(2) * spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc']))
    full = [[float(n), float(n + 1)] for n in range(K, end)]
    if not unit:
        edges = [K] + [e for e in (4, 5, 6, 8, 12, 16, 32, 64) if e > K]
        if end > 128:
            edges.append(128)
        if edges[-1] != end:
            edges.append(end)
        full = [[float(a), float(b)] for a, b in zip(edges[:-1], edges[1:])]
    selected = full if shell_ranges is None else [[float(x) for x in s] for s in shell_ranges]
    if not selected:
        raise ValueError('empty shell selection')
    for lo, hi in selected:
        if not (math.isfinite(lo) and math.isfinite(hi) and K <= lo < hi <= end):
            raise ValueError('shell outside point domain')
        if unit and (hi != lo + 1 or lo != int(lo)):
            raise ValueError('EPS requires unit shells')
    if len({tuple(s) for s in selected}) != len(selected):
        raise ValueError('duplicate shells')
    if selected != sorted(selected) or any(a[1] > b[0] for a, b in zip(selected[:-1], selected[1:])):
        raise ValueError('unordered/overlapping shells')
    complete = selected[0][0] == K and selected[-1][1] == end and all(
        a[1] == b[0] for a, b in zip(selected[:-1], selected[1:]))
    return selected, complete, end


def discrete_shell(ctx, lo, hi):
    """Exact 26/52/104 direction, 64/128/256-per-decade refinement rule."""
    levels = {}
    for lv in (0, 1, 2):
        ks = CC.shell_k(lo, hi, CC.PER_DECADE[lv])
        dirs = ctx['D'][lv]
        kv = (ks[:, None, None] * dirs[None, :, :] / ctx['L'].KPC).reshape(-1, 3)
        q = CC.q_of(ctx['B'], kv)
        finite(q, 'q discrete')
        dev = np.abs(1 - q.real)
        j = int(np.argmax(dev))
        levels[str(lv)] = dict(eps=float(dev[j]), n_samples=len(kv), n_k=len(ks),
            n_dirs=len(dirs), k_at_max_inverse_kpc=float(ks[j // len(dirs)]),
            dir_at_max=dirs[j % len(dirs)].tolist(), max_abs_imag_q=float(np.max(np.abs(q.imag))))
        if lv == 1 and levels['1']['eps'] <= 1.1 * levels['0']['eps']:
            base, ref, nref = 0, 1, 0
            break
        if lv == 2:
            base, ref = 1, 2
            nref = 1 if levels['2']['eps'] <= 1.1 * levels['1']['eps'] else 2
    return dict(eps_base=levels[str(base)]['eps'], eps_refined=levels[str(ref)]['eps'],
                refinements=nref, certified=nref <= 1, levels=levels)


def mandel(v):
    out = np.zeros(v.shape[:-1] + (3, 3), complex)
    out[..., 0, 0], out[..., 1, 1], out[..., 2, 2] = v[..., 0], v[..., 1], v[..., 2]
    for j, (a, b) in enumerate(((1, 2), (0, 2), (0, 1)), 3):
        out[..., a, b] = out[..., b, a] = v[..., j] / math.sqrt(2)
    return out


def values_from_x(ctx, x, k_m, objective):
    norm = 4 * ctx['B'].gam * np.asarray(k_m) ** 2
    if objective == 'EPS':
        values = np.abs(1 - norm * x[..., 0])
    elif objective == 'RHO_G':
        gh = ctx['isq'] @ mandel(x[..., 1:7]) @ ctx['isq']
        values = np.linalg.norm(gh, ord=2, axis=(-2, -1)) * norm
    else:
        raise ValueError('unsupported objective')
    return finite(values, objective, nonnegative=True)


def search_envelope(ctx, lo, hi, cfg, *, objective='EPS', audit=False, previous=None):
    """Grid + seeded local search over (direction, radius, free cardinal torus).

    Uses all hemisphere directions only because the EH block is even in k;
    free t makes this symmetry exact. Search maxima are NOT sup upper bounds.
    """
    nt = cfg['audit_torus' if audit else 'torus']
    nd = cfg['audit_dirs' if audit else 'directions']
    nstarts = cfg['audit_starts' if audit else 'starts']
    key = (nt, nd)
    if key not in ctx['cache']:
        T = C2.torus_grid_v(nt)
        dirs = C2.fib_hemi(nd)
        kref = 10 / ctx['L'].KPC
        ctx['cache'][key] = (T, dirs, ctx['E'].native(T), ctx['E'].eh_dir(dirs, kref), kref)
    T, dirs, native, eh, kref = ctx['cache'][key]
    fractions = np.array([0, .25, .5, .75, 1.] if audit else [0., .5, 1.])
    # EPS registered radial grid linear; LO registered grid logarithmic.
    radial = lambda f: (lo + (hi - lo) * f if objective == 'EPS'
                        else np.exp(math.log(lo) + math.log(hi / lo) * f))
    ks = radial(fractions) / ctx['L'].KPC
    out = np.empty((len(ks), nd, len(T)))
    e0 = np.zeros((10, 1), complex)
    e0[0, 0] = -1
    step = max(1, 20000 // len(T))
    for ik, k in enumerate(ks):
        for d0 in range(0, nd, step):
            d1 = min(d0 + step, nd)
            matrix = ((native[None] + (k / kref) ** 2 * eh[d0:d1, None]) / ctx['B'].volume).reshape(-1, 10, 10)
            x = np.linalg.solve(matrix, np.broadcast_to(e0, (len(matrix), 10, 1)))[:, :, 0]
            out[ik, d0:d1] = values_from_x(ctx, x, k, objective).reshape(d1 - d0, len(T))
    flat = out.ravel()
    npre = min(4000, len(flat))
    pre = np.argpartition(flat, len(flat) - npre)[-npre:]
    ik, idd, it = np.unravel_index(pre, out.shape)
    keys = np.concatenate([T[it] / math.pi, dirs[idd]], axis=1)
    ix = C2.distinct_top(flat[pre], keys, nstarts, .15)
    starts_t, starts_d, starts_f = T[it[ix]], dirs[idd[ix]], fractions[ik[ix]]
    if previous is not None:
        starts_t = np.concatenate([starts_t, [previous['t_at']]])
        starts_d = np.concatenate([starts_d, [previous['dir_at']]])
        starts_f = np.append(starts_f, np.clip((previous['k_at_inverse_kpc'] + 1 - lo) / (hi - lo), 0, 1))
    n0, e1, e2 = C2.tangent_basis(starts_d)
    p0 = np.concatenate([starts_t, np.zeros((len(starts_t), 2)), starts_f[:, None]], axis=1)

    def evaluate(si, params):
        n = n0[si] + params[:, 3:4] * e1[si] + params[:, 4:5] * e2[si]
        n /= np.linalg.norm(n, axis=1)[:, None]
        k = radial(params[:, 5]) / ctx['L'].KPC
        x = C2.env_full(ctx['E'], n * k[:, None], params[:, :3])
        return values_from_x(ctx, x, k, objective)

    seed = 20261018 + int(lo * 17 + hi * 29) + (100000 if audit else 0) + (200000 if objective != 'EPS' else 0)
    p, fv, iterations = C2.refine(evaluate, p0, (.3, .3, .3, .15, .15, .3), [5],
        np.random.default_rng(seed), M=cfg['candidates'], max_it=cfg['iterations'])
    best = int(np.argmax(fv))
    n = n0[best] + p[best, 3] * e1[best] + p[best, 4] * e2[best]
    n /= np.linalg.norm(n)
    return dict(estimate=float(fv[best]), grid_max=float(flat.max()), n_grid=len(flat),
        torus_m=nt, direction_count=nd, radial_fractions=fractions.tolist(), starts=len(p0),
        iterations=iterations, seed=seed, t_at=np.remainder(p[best, :3], 2 * math.pi).tolist(),
        dir_at=n.tolist(), k_at_inverse_kpc=float(radial(p[best, 5])),
        estimator_scope='finite grid plus local maximum; lower bound on continuous supremum')


def actual_eps_search(ctx, lo, hi, cfg, discrete):
    dirs = np.concatenate([C2.fib_sphere(cfg['actual_dirs']), C2.fib_sphere(cfg['dense_dirs'])])
    ks = CC.shell_k(lo, hi, 256)
    kv = (ks[:, None, None] * dirs[None, :, :] / ctx['L'].KPC).reshape(-1, 3)
    q = CC.q_of(ctx['B'], kv)
    vals = finite(np.abs(1 - q), 'dense actual EPS', nonnegative=True)
    top = np.argsort(vals)[-min(12, len(vals)):][::-1]
    seeds_d = [dirs[i % len(dirs)] for i in top]
    seeds_f = [(ks[i // len(dirs)] - lo) / (hi - lo) for i in top]
    for level in discrete['levels'].values():
        seeds_d.append(level['dir_at_max'])
        seeds_f.append((level['k_at_max_inverse_kpc'] - lo) / (hi - lo))
    n0, e1, e2 = C2.tangent_basis(np.asarray(seeds_d))
    p0 = np.column_stack([np.zeros((len(seeds_d), 2)), seeds_f])

    def evaluate(si, p):
        n = n0[si] + p[:, :1] * e1[si] + p[:, 1:2] * e2[si]
        n /= np.linalg.norm(n, axis=1)[:, None]
        k = (lo + (hi - lo) * p[:, 2]) / ctx['L'].KPC
        return finite(np.abs(1 - CC.q_of(ctx['B'], n * k[:, None])), 'local actual EPS')

    p, fv, its = C2.refine(evaluate, p0, (.1, .1, .3), [2],
        np.random.default_rng(20261018 + int(lo)), M=cfg['candidates'], max_it=cfg['iterations'])
    j = int(np.argmax(fv))
    n = n0[j] + p[j, 0] * e1[j] + p[j, 1] * e2[j]
    n /= np.linalg.norm(n)
    return dict(estimate=float(max(vals.max(), fv.max())), dense_max=float(vals.max()),
                local_max=float(fv[j]), dense_nodes=len(vals), iterations=its,
                dir_at=n.tolist(), k_at_inverse_kpc=float(lo + (hi - lo) * p[j, 2]))


def base_record(ctx, schema, mode):
    return dict(schema=schema, utc=utc(), status='TESTED', identity=ctx['details']['identity'],
        point_sha256=ctx['details']['point_sha256'], custody=ctx['details']['custody'],
        producer=CU.pin(__file__), dependencies=ctx['source_pins'], settings=mode,
        point_symbol_checks=ctx['checks'], rigorous_supremum=False,
        production_admissible=False, covers_all_consumed_states=False,
        limitation='Numerical convention only; independent scientific review/admission remains required.')


def produce_eps(spec, *, settings='registered', shell_ranges=None, context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                              # KS2: a1dcdea8's own code path
        return P.produce_eps(spec, settings=settings, shell_ranges=shell_ranges, context=context, progress=progress)
    K = kept_k(spec)
    start = time.monotonic()
    if settings not in SETTINGS:
        raise ValueError('unknown settings')
    ctx = context or point_context(spec)
    if ctx['details']['identity'] != CU.identity(spec):
        raise ValueError('point context mismatch')
    ranges, complete, end = shell_plan(spec, shell_ranges)
    cfg = SETTINGS[settings]
    rows, audits, previous = [], [], None
    for lo, hi in ranges:
        discrete = discrete_shell(ctx, lo, hi)
        env = search_envelope(ctx, lo, hi, cfg, previous=previous)
        actual = actual_eps_search(ctx, lo, hi, cfg, discrete)
        audit = search_envelope(ctx, lo, hi, cfg, audit=True) if lo in AUDIT_LO else None
        previous = env
        eps = max(discrete['eps_base'], discrete['eps_refined'], env['estimate'], actual['estimate'],
                  0 if audit is None else audit['estimate'])
        row = dict(range_inverse_kpc=[lo, hi], lo_inverse_kpc=lo, hi_inverse_kpc=hi,
            **discrete, eps=eps, eps_envelope=max(env['estimate'], 0 if audit is None else audit['estimate']),
            envelope=env, actual=actual)
        if audit is not None:
            audits.append(dict(range_inverse_kpc=[lo, hi], production=env['estimate'],
                dense=audit['estimate'], dense_over_production=(audit['estimate'] / env['estimate'] if env['estimate'] else None),
                dense_search=audit))
        rows.append(row)
        if progress:
            progress(dict(shell=[lo, hi], eps=eps, refinements=discrete['refinements']))
    passed = all(r['certified'] for r in rows)
    rec = base_record(ctx, EPS_SCHEMA, settings)
    rec.update(gate='EPS', verdict=('NUMERICAL_RULE_PASSED_REVIEW_REQUIRED' if passed and complete and settings == 'registered'
                                  else 'EPS_UNCERTIFIED' if not passed else 'INCOMPLETE_NUMERICAL_DIAGNOSTIC'),
        registered_discrete_verdict='CERTIFIED' if passed else 'EPS_UNCERTIFIED',
        full_registered_search_executed=complete and settings == 'registered', coverage_complete=complete,
        required_coverage_inverse_kpc=[float(K), float(end)], shells=rows, envelope_audit=audits,
        eps_max=max(r['eps'] for r in rows), eps_max_shell=max(rows, key=lambda r: r['eps'])['range_inverse_kpc'],
        envelope_rule='A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS',
        envelope_numerical_rule='12^3 x 200 hemisphere x 3 radii; 8 starts plus previous; 20^3 x 400 x 5 audit, 16 starts',
        shell_value_rule='max of actual, discrete, envelope and dense audit on EVERY shell; no anchor exceptions',
        nodes_from_future_solved_states='UNTESTED; none consumed or claimed',
        seconds=time.monotonic() - start, peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return rec


def produce_rho(spec, *, settings='registered', shell_ranges=None, context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                              # KS2: a1dcdea8's own code path
        return P.produce_rho(spec, settings=settings, shell_ranges=shell_ranges, context=context, progress=progress)
    K = kept_k(spec)
    start = time.monotonic()
    if settings not in SETTINGS:
        raise ValueError('unknown settings')
    ctx = context or point_context(spec)
    if ctx['details']['identity'] != CU.identity(spec):
        raise ValueError('point context mismatch')
    ranges, complete, end = shell_plan(spec, shell_ranges, unit=False)
    rows = []
    for lo, hi in ranges:
        levels = []
        for lv in (1, 2):
            ks = CC.shell_k(lo, hi, CC.PER_DECADE[lv])
            dirs = ctx['D'][lv]
            kv = (ks[:, None, None] * dirs[None, :, :] / ctx['L'].KPC).reshape(-1, 3)
            kv = kv[np.max(np.abs(kv), axis=1) * ctx['L'].KPC > K * (1 + 1e-12)]   # KS2: outside the kept-K cube
            x = CC.full_response(ctx['B'], kv, chunk=2048)
            vals = values_from_x(ctx, x, np.linalg.norm(kv, axis=1), 'RHO_G')
            j = int(np.argmax(vals))
            levels.append(dict(level=lv, estimate=float(vals[j]), n_samples=len(vals),
                               k_argmax_inverse_kpc=(kv[j] * ctx['L'].KPC).tolist()))
        env = search_envelope(ctx, lo, hi, SETTINGS[settings], objective='RHO_G')
        row = dict(range_inverse_kpc=[lo, hi], rho_used=max(env['estimate'], *(x['estimate'] for x in levels)),
                   rho_envelope=env, sampled_levels=levels)
        rows.append(row)
        if progress:
            progress(dict(shell=[lo, hi], rho=row['rho_used']))
    rec = base_record(ctx, RHO_SCHEMA, settings)
    rec.update(gate='RHO_G', verdict='NUMERICAL_ESTIMATE_REVIEW_REQUIRED', shells=rows,
        coverage_complete=complete, required_coverage_inverse_kpc=[float(K), float(end)],
        full_registered_search_executed=complete and settings == 'registered',
        seconds=time.monotonic() - start, peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return rec


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--mode', choices=('eps', 'rho'), default='eps')
    parser.add_argument('--settings', choices=tuple(SETTINGS), default='registered')
    parser.add_argument('--shells', help='JSON list of [lo,hi]; omission covers the full point domain')
    a = parser.parse_args()
    spec = json.loads(CU.allowed_path(a.spec).read_bytes())
    fn = produce_eps if a.mode == 'eps' else produce_rho
    rec = fn(spec, settings=a.settings, shell_ranges=None if a.shells is None else json.loads(a.shells),
             progress=lambda x: print(json.dumps(x), flush=True))
    print(json.dumps(CU.write_new(a.out, rec)))


if __name__ == '__main__':
    main()
