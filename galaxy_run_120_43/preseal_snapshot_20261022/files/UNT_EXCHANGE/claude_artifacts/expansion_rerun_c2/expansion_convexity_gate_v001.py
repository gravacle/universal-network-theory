"""Estimator-convexity gate for the capture-adiabatic expansion continuation. V001.

Inert module: no sampling, no launch, no repair. numpy only.

WHICH OBJECTS ARE GATED (derived from the continuation code pinned by
CAPTURE_ADIABATIC_EXACT_RESUME_RUN_V001; line numbers of the pinned files):

  resume stepper  owned_capture_adiabatic_resume_v001.py (ef3d22ce)
    L72   data = evaluator.evaluate(capture, candidate, statistics)      [estimator call]
    L82   F = data.native_per_cell.F_hessian ; L83 congruence F00*=Eref, Fjj/=Eref
    L84   rhs(y=n.y, u=Eref*n.U_F_n, F_hessian=F, beta=x0/Eref, j=Eref*x[1:10], ...)
    L88   tangent_observer(x, data, r)   -> root L91-L111 THERMAL_BRANCH_SIGN_GUARD [the sign test]
  evaluator      owned_uniform_capture_thermodynamics_v001.py (df80228a)
    L87   covariance = Cov_w(uniform scores)          (PSD for every sample: plug-in)
    L89   contact[0,0] = <bare NN contact>_w = -<n>   (only NN nonzero)
    L92   F_hessian = -(covariance + contact)/(beta*n_cells)
    L117-L118 returns covariance and contact separately
  RHS V003       owned_adiabatic_equilibrium_bianchi_rhs_v003.py (d7b81d45)
    L55   F_jj admitted by upper-triangle copy ; L60 F_jn := F_nj
    L79-L81 tangent built from the ADMITTED F ; L90 entropy row

  So the estimator object consumed by the expansion RHS is the per-cell
  10x10 F_hessian (source order: uniform lapse n, j_R[3], j_S Mandel[6]),
  as admitted by RHS V003 L55/L60. y, U and C carry no exact-sign constraint
  from convexity (C SPD is already a stepper check, L77, and is not gated here).

EXACT CONSTRAINT (premise P, from code text, not saved data): the capture target
is Z(N,j) = Tr exp(-beta N H0 + beta j.R) with H0 real symmetric and R diagonal
(statistics L117-L120 weight; operator a04f8795 reverse = conjugate forward), so
ln Z is convex in (N,j) and F = -(1/(beta nc)) d2 lnZ is negative semidefinite.
For the plug-in estimator, F <= 0  <=>  G = Cov + contact >= 0, and because the
read-read block of G is a pure covariance (PSD for any sample) a violation can
only appear through the lapse row: Schur_N = G_nn - G_nj G_jj^-1 G_jn
= Var_w(s0 | s_j) - <n> < 0 (when G_jj > 0).

GATE (per evaluated candidate): lambda_max(F_admitted) <= tol for the POOLED
estimate, EACH CHAIN, and EACH leave-one-batch-out JACKKNIFE replicate
(partition = capture all_momentum.partition). tol = 1e-10*max(1, ||F||_2)
classifies roundoff only. Any violation -> status ESTIMATOR_CONVEXITY_VIOLATION.
The gate never modifies F, never clips, never ridges, never retries.
Reported also: Schur_N (= Var_w(s0|s_j) - <n>) with jackknife SE and bias.
"""
import json
import math

import numpy as np

STATUS_PASS = 'PASS'
STATUS_VIOLATION = 'ESTIMATOR_CONVEXITY_VIOLATION'
REL_TOL = 1e-10


def admit_native(F):
    """Re-typed RHS V003 L55 (jj upper copied to lower) and L60 (jn := nj).
    The native->physical map at stepper L83 is a diagonal congruence, so the
    inertia (hence the sign test) is identical in native and physical units."""
    F = np.array(F, dtype=float, copy=True)
    Fjj = F[1:, 1:].copy()
    F[1:, 1:] = np.triu(Fjj) + np.triu(Fjj, 1).T
    F[1:, 0] = F[0, 1:]
    return F


# ---------------------------------------------------------------- capture pooling

def _canon(v):
    return json.dumps(v, sort_keys=True, allow_nan=False)


def reduce_capture(doc):
    """Keep only the fields the pinned evaluator (L36-L77) and the gate read, with feature
    rows converted once to float64 numpy rows (values unchanged). Memory only."""
    sr = doc['sampler_result']
    rs = sr['reweighting_statistics']
    am = sr['all_momentum']
    return {'sampler_result': {
        'status': sr.get('status'), 'ok': sr.get('ok'), 'mixing': sr.get('mixing'), 'flags': sr.get('flags'),
        'reweighting_statistics': {'metadata': rs['metadata'], 'series': [
            {'chain': s['chain'], 'chain_ids': list(s['chain_ids']), 'measurement_ids': list(s['measurement_ids']),
             'features': [np.asarray(r, dtype=float) for r in s['features']]} for s in rs['series']]},
        'all_momentum': {'metadata': am['metadata'], 'partition': am['partition'],
                         'status': am.get('status'), 'mixing': am.get('mixing')}},
        'source_pins': doc.get('source_pins')}


def pool_captures(sources):
    """sources: list of (label, parsed result.json). Returns one capture document
    accepted unchanged by the pinned evaluator (L36-L77).

    - reweighting metadata must be identical across sources (same declared target);
    - all_momentum n_cells, n_contact and the unique k=0 block must be identical;
    - chain c of source s is relabelled offset_s + c in 'chain' and 'chain_ids'
      (evaluator L71/L74 forbid duplicate (chain, measurement) ids);
    - feature rows are converted once to float64 numpy rows (values unchanged;
      evaluator/statistics call np.asarray on them, L62-L76 / statistics L91);
    - jackknife partition entries are relabelled the same way.
    With ONE source every pass-through field (mixing, flags, ok, all-k status and
    mixing, source_pins) is copied verbatim, so evaluator output is identical to
    evaluating the original document."""
    if not sources:
        raise ValueError('No capture sources')
    meta0 = None
    am_meta0 = None
    series = []
    partition = []
    offset = 0
    pins = {}
    passthrough = {}
    for label, doc in sources:
        sr = doc['sampler_result']
        if sr.get('status') != 'complete':
            raise ValueError('Complete capture required: ' + label)
        meta = sr['reweighting_statistics']['metadata']
        am = sr['all_momentum']
        if meta0 is None:
            meta0 = meta
            am_meta0 = am['metadata']
        else:
            if _canon(meta) != _canon(meta0):
                raise ValueError('Reweighting metadata differs (not the same declared target): ' + label)
            if am['metadata']['n_cells'] != am_meta0['n_cells'] or am['metadata']['n_contact'] != am_meta0['n_contact']:
                raise ValueError('All-k normalization differs: ' + label)
            z = [b for b in am['metadata']['blocks'] if list(b['k']) == [0, 0, 0]]
            z0 = [b for b in am_meta0['blocks'] if list(b['k']) == [0, 0, 0]]
            if len(z) != 1 or len(z0) != 1 or _canon(z[0]) != _canon(z0[0]):
                raise ValueError('Zero-mode block differs: ' + label)
        chains = sorted({int(s['chain']) for s in sr['reweighting_statistics']['series']})
        if chains != list(range(len(chains))):
            raise ValueError('Non-contiguous chain labels: ' + label)
        for s in sr['reweighting_statistics']['series']:
            c = offset + int(s['chain'])
            if any(int(x) != int(s['chain']) for x in s['chain_ids']):
                raise ValueError('Chain id mismatch in ' + label)
            series.append({'chain': c, 'chain_ids': [c] * len(s['chain_ids']),
                           'measurement_ids': list(s['measurement_ids']),
                           'features': [np.asarray(r, dtype=float) for r in s['features']]})
        for p in am['partition']:
            partition.append({'source': label, 'omission_index': len(partition),
                              'chain': offset + int(p['chain']), 'source_chain': int(p['chain']),
                              'batch': p['batch'],
                              'measurement_id_range_half_open': list(p['measurement_id_range_half_open'])})
        pins[label] = doc.get('source_pins')
        passthrough[label] = dict(mixing=sr.get('mixing'), flags=sr.get('flags'), ok=sr.get('ok'),
                                  allk_status=am.get('status'), allk_mixing=am.get('mixing'))
        offset += len(chains)
    if len(sources) == 1:
        (label, doc), = sources
        pt = passthrough[label]
        src_pins = pins[label]
        mixing, flags, ok, allk_status, allk_mixing = (pt['mixing'], pt['flags'], pt['ok'],
                                                       pt['allk_status'], pt['allk_mixing'])
    else:
        src_pins = pins
        mixing = {k: v['mixing'] for k, v in passthrough.items()}
        flags = {k: v['flags'] for k, v in passthrough.items()}
        ok = {k: v['ok'] for k, v in passthrough.items()}
        allk_status = {k: v['allk_status'] for k, v in passthrough.items()}
        allk_mixing = {k: v['allk_mixing'] for k, v in passthrough.items()}
    cap = {'sampler_result': {'status': 'complete', 'ok': ok, 'mixing': mixing, 'flags': flags,
                              'reweighting_statistics': {'metadata': meta0, 'series': series},
                              'all_momentum': {'metadata': am_meta0, 'partition': partition,
                                               'status': allk_status, 'mixing': allk_mixing}},
           'source_pins': src_pins}
    return cap


def subcaptures(capture):
    """Per-chain captures and leave-one-batch-out jackknife captures (rows shared)."""
    sr = capture['sampler_result']
    series = sr['reweighting_statistics']['series']

    def with_series(new_series):
        s2 = dict(sr)
        s2['reweighting_statistics'] = {'metadata': sr['reweighting_statistics']['metadata'], 'series': new_series}
        out = dict(capture)
        out['sampler_result'] = s2
        return out
    chains = [(int(s['chain']), with_series([s])) for s in series]
    jk = []
    for p in sr['all_momentum']['partition']:
        lo, hi = p['measurement_id_range_half_open']
        new = []
        hit = 0
        for s in series:
            if int(s['chain']) != int(p['chain']):
                new.append(s)
                continue
            keep = [i for i, m in enumerate(s['measurement_ids']) if not (lo <= m < hi)]
            hit += len(s['measurement_ids']) - len(keep)
            new.append({'chain': s['chain'], 'chain_ids': [s['chain_ids'][i] for i in keep],
                        'measurement_ids': [s['measurement_ids'][i] for i in keep],
                        'features': [s['features'][i] for i in keep]})
        if hit != hi - lo:
            raise ValueError('Jackknife batch does not match committed rows')
        jk.append((p, with_series(new)))
    return dict(chains=chains, jackknife=jk)


# ---------------------------------------------------------------- the gate

def _one(evaluator, statistics, capture, candidate, data=None):
    d = data if data is not None else evaluator.evaluate(capture=capture, candidate=candidate, statistics=statistics)
    F = np.asarray(d['native_per_cell']['F_hessian'], dtype=float)
    Fa = admit_native(F)
    lam = np.linalg.eigvalsh(Fa)
    nrm = float(np.linalg.norm(Fa, 2))
    tol = REL_TOL * max(1.0, nrm)
    G = np.asarray(d['uniform_extensive_score_covariance'], float) + np.asarray(d['uniform_extensive_mean_bare_contact'], float)
    Gjj = G[1:, 1:]
    gjj_min = float(np.linalg.eigvalsh(Gjj)[0])
    schur = float(G[0, 0] - G[0, 1:].dot(np.linalg.solve(Gjj, G[1:, 0])))
    return dict(rows=int(d['path_count']), lambda_max=float(lam[-1]), lambda_min=float(lam[0]),
                tol=tol, violates=bool(lam[-1] > tol), schur_N=schur,
                mean_events=float(-G[0, 0] + np.asarray(d['uniform_extensive_score_covariance'], float)[0, 0]),
                G_jj_lambda_min=gjj_min, ESS=float(d['weight_concentration']['ESS']),
                F_symmetry_defect=float(np.linalg.norm(F - F.T)))


def _jk_stats(full, reps):
    reps = np.asarray(reps, dtype=float)
    nb = len(reps)
    m = float(reps.mean())
    se = float(math.sqrt((nb - 1) / nb * float(np.sum((reps - m) ** 2))))
    bias = float((nb - 1) * (m - full))
    return dict(replicates=nb, mean=m, SE=se, bias=bias, bias_corrected=full - bias)


def gate(*, evaluator, statistics, capture, subs, candidate, pooled_data=None):
    """Returns a JSON-able record; record['status'] is PASS or ESTIMATOR_CONVEXITY_VIOLATION.
    pooled_data may be the evaluator output already computed for (capture, candidate)."""
    pooled = _one(evaluator, statistics, capture, candidate, pooled_data)
    chains = []
    for c, sub in subs['chains']:
        r = _one(evaluator, statistics, sub, candidate)
        r['chain'] = c
        chains.append(r)
    jk = []
    for p, sub in subs['jackknife']:
        r = _one(evaluator, statistics, sub, candidate)
        r['omitted'] = dict(chain=p['chain'], range=p['measurement_id_range_half_open'], source=p.get('source'))
        jk.append(r)
    violators = []
    if pooled['violates']:
        violators.append('pooled')
    violators += ['chain%d' % r['chain'] for r in chains if r['violates']]
    violators += ['jk%02d' % i for i, r in enumerate(jk) if r['violates']]
    rec = dict(status=STATUS_VIOLATION if violators else STATUS_PASS,
               beta_native=float(candidate['beta']), j_native=[float(v) for v in candidate['j_mandel']],
               pooled=pooled, chains=chains,
               jackknife=dict(n=len(jk), n_violating=sum(r['violates'] for r in jk),
                              lambda_max=[r['lambda_max'] for r in jk], schur_N=[r['schur_N'] for r in jk],
                              lambda_max_stats=_jk_stats(pooled['lambda_max'], [r['lambda_max'] for r in jk]) if jk else None,
                              schur_N_stats=_jk_stats(pooled['schur_N'], [r['schur_N'] for r in jk]) if jk else None),
               violators=violators,
               max_lambda_max=max([pooled['lambda_max']] + [r['lambda_max'] for r in chains] + [r['lambda_max'] for r in jk]),
               min_schur_N=min([pooled['schur_N']] + [r['schur_N'] for r in chains] + [r['schur_N'] for r in jk]),
               rule='lambda_max(admitted per-cell F) <= 1e-10*max(1,||F||_2) for pooled, every chain, every jackknife replicate; no repair')
    return rec
