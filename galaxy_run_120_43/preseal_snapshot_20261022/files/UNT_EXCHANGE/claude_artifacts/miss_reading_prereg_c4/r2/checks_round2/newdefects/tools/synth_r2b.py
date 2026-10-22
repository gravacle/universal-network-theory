"""Lens R2-B: synthetic score outputs in the v003g score_after_freeze format.

All velocities and sigmas are synthetic and deliberately implausible (1000 + 10*j km/s, sigma 2 km/s);
no target value is read or reproduced. Rows are produced by the v003g module's own pure helpers
(_score_members, _score_members_on_rows, _pointwise_envelope, _band_rows, _distribution), passed in
as a module object, and are cross-checked against independent replicas written here (rep_*).
"""
import math

IDS = ['NGC3198-Q%02d' % i for i in range(1, 44)]
ENV_LABEL_FIXED = 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE; conditional on DDO154 D=4.04 and i=66 (A13/A23)'


def bound_rows(null_ratio_ids=()):
    b = []
    for j, q in enumerate(IDS):
        v = 1000.0 + 10.0 * j
        s = 5e-324 if q in null_ratio_ids else 2.0
        b.append((v, s))
    return b


def member_from_r(member_id, log_index, rmap, bound, role='hull_vertex', evaluated=True, forward_valid=True):
    """rmap: qid -> float r, or ('INV', reason), or ('NULL',) for a valid row whose ratio overflows."""
    speeds, rv, regs = [], [], []
    for j, q in enumerate(IDS):
        x = rmap.get(q, 0.0)
        v, s = bound[j]
        if isinstance(x, tuple) and x[0] == 'INV':
            speeds.append(None); rv.append(False)
            regs.append({'status': 'INVALID', 'reason': x[1], 'registration': None})
        elif isinstance(x, tuple) and x[0] == 'NULL':
            speeds.append(v + 1.0); rv.append(True); regs.append(None)
        else:
            speeds.append(v + float(x) * s); rv.append(True); regs.append(None)
    if not evaluated:
        speeds = [None] * 43; rv = [False] * 43; regs = [None] * 43
    m = {'member_id': member_id, 'log_index': log_index, 'role': role, 'evaluated': evaluated,
         'forward_valid_flag': True if (evaluated and forward_valid) else (None if not evaluated else False),
         'speeds_km_s': speeds, 'row_valid': rv, 'row_registration': regs}
    m['member_valid'] = bool(evaluated and m['forward_valid_flag'] is True and any(rv)
                             and all(a or b is not None for a, b in zip(rv, regs)))
    if evaluated and not forward_valid:
        m['speeds_km_s'] = [None] * 43; m['row_valid'] = [False] * 43; m['row_registration'] = [None] * 43
        m['member_valid'] = False
    return m


# ---------------- independent replicas (cross-check only) ----------------
def rep_ladder(q, predicted, row_valid, observed, sigma):
    residual = ratio = None
    if predicted is not None:
        residual = predicted - observed
        r = residual / sigma
        ratio = r if math.isfinite(r) else None
    valid = bool(row_valid and predicted is not None)
    within = bool(valid and ratio is not None and abs(ratio) <= 1.0)
    return residual, ratio, valid, within


def rep_score(members, ids, bound):
    out = []
    for m in members:
        rows = []
        for j, q in enumerate(ids):
            res, ratio, valid, within = rep_ladder(q, m['speeds_km_s'][j], m['row_valid'][j], bound[j][0], bound[j][1])
            reg = m['row_registration'][j]
            if reg is not None:
                st, ss, rr = 'INVALID', 'INVALID_AS_MISS', reg['reason']
            else:
                st = 'VALID' if valid else 'UNEVALUATED_OR_REFUSED'
                ss = 'HIT' if within else 'MISS'
                rr = None
            rows.append({'id': q, 'sigma_ratio': ratio, 'within_error': within, 'status': st, 'score_status': ss,
                         'registered_reason': rr})
        out.append({'member_id': m['member_id'], 'rows': rows})
    return out


def rep_envelope_overlap(members, ids, bound):
    n_uneval = sum(1 for m in members if not m['evaluated'])
    out = []
    for j, q in enumerate(ids):
        vals = [m['speeds_km_s'][j] for m in members if m['row_valid'][j]]
        valid = bool(len(members) >= 1 and n_uneval == 0 and vals)
        lo, hi = (min(vals), max(vals)) if vals else (None, None)
        o, s = bound[j]
        out.append({'id': q, 'valid': valid,
                    'band_overlaps_error_bar': bool(valid and lo <= o + s and hi >= o - s)})
    return out


def build_score(mod, members, ref_id, bound, *, freeze_status='FREEZE_COMPLETE', incomplete_reasons=(),
                original_k=None, stage0=None, sens_valid=False, fixed_mode=True):
    """members: PRIMARY member dicts. original_k/stage0: lists of member dicts (evaluated) or None (not evaluated)."""
    ids = list(IDS)
    scored = mod._score_members(members, ids, bound)
    ref = next(m for m in scored if m['member_id'] == ref_id)
    env_in = mod._pointwise_envelope(members, ids, ENV_LABEL_FIXED if fixed_mode else mod.ENVELOPE_LABEL)
    erows, eov, einv = mod._band_rows(env_in, 'band_low_km_s', 'band_high_km_s', ids, bound)
    ref_member = next(m for m in members if m['member_id'] == ref_id)
    sens_in = []
    for j, q in enumerate(ids):
        sp = ref_member['speeds_km_s'][j]
        ok = bool(sens_valid and sp is not None)
        sens_in.append({'id': q, 'reference_speed_km_s': sp, 'box_limited_band_low_km_s': (sp - 3.0) if ok else None,
                        'box_limited_band_high_km_s': (sp + 3.0) if ok else None, 'max_abs_delta_km_s': 3.0 if ok else None,
                        'n_planned': 4, 'n_valid': 4 if ok else 0, 'valid': ok, 'label': 'SENS'})
    srows, sov, sinv = mod._band_rows(sens_in, 'box_limited_band_low_km_s', 'box_limited_band_high_km_s', ids, bound)
    counts = [m['within_error_count'] for m in scored]
    alts = [{'name': 'BR_A_F10_PRIMARY', 'kind': 'state', 'status': 'EVALUATED_BEFORE_FREEZE', 'role': 'PRIMARY',
             'scored': True, 'headline': True}]

    def evaluated_alt(name, kind, mems, scope=None):
        if scope is None:
            am = mod._score_members(mems, ids, bound)
        else:
            am = mod._score_members_on_rows(mems, ids, bound, scope)
        rec = {'name': name, 'kind': kind, 'status': 'EVALUATED_BEFORE_FREEZE', 'role': 'NON_PRIMARY', 'scored': True,
               'headline': False, 'member_within_error_counts': mod._distribution([m['within_error_count'] for m in am]),
               'members': am, 'member_evaluation_status': 'COMPLETE'}
        return rec
    if original_k is not None:
        alts.append(evaluated_alt('ORIGINAL_K', 'state', original_k))
    else:
        alts.append({'name': 'ORIGINAL_K', 'kind': 'state', 'status': 'NOT_EVALUATED_BEFORE_FREEZE', 'role': 'NON_PRIMARY',
                     'scored': False, 'headline': False, 'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'})
    for nm, kd in (('ML_3p6_0.4', 'source'), ('ML_3p6_0.6', 'source'), ('GL10_SOURCE_GAUSS_ORDER', 'approximation')):
        alts.append({'name': nm, 'kind': kd, 'status': 'NOT_EVALUATED_BEFORE_FREEZE', 'role': 'NON_PRIMARY', 'scored': False,
                     'headline': False, 'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'})
    outer = ids[35:]
    scope = {'zone': 'OUTER', 'radius_min_kpc': 30.0, 'radius_min_inclusive': True, 'query_ids': outer,
             'registered_query_ids': outer, 'n_rows': 8, 'coefficient_grid_pin': {'path': 'SYNTH', 'sha256': '0' * 64},
             'headline': False}
    if stage0 is not None:   # successor format assumed equal to v003g's (M-14: only the status changes)
        rec = evaluated_alt('STAGE0_GRID_OUTER', 'approximation', stage0, scope=outer)
        rec['scoring_scope'] = scope
        alts.append(rec)
    else:
        alts.append({'name': 'STAGE0_GRID_OUTER', 'kind': 'approximation', 'status': 'NOT_EVALUATED_BEFORE_FREEZE',
                     'role': 'NON_PRIMARY', 'scoring_scope': scope, 'scored': False, 'headline': False,
                     'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'})
    if fixed_mode:
        alts.append({'name': 'DDO154_DISTANCE_NUISANCE', 'kind': 'calibration_coordinate', 'status': 'NOT_EVALUATED_BEFORE_FREEZE',
                     'role': 'NON_PRIMARY', 'scored': False, 'headline': False,
                     'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline (A13)'})
    score = {'ok': True, 'refused': False, 'n_rows': 43, 'freeze_status': freeze_status,
             'incomplete_reasons': list(incomplete_reasons),
             'headline': {'reference_member_id': ref_id, 'reference_member_log_index': ref['log_index'],
                          'member_within_error_counts': mod._distribution(counts), 'freeze_status': freeze_status},
             'members': scored,
             'pointwise_envelope': {'label': ENV_LABEL_FIXED if fixed_mode else mod.ENVELOPE_LABEL, 'rows': erows,
                                    'band_overlap_count': eov, 'invalid_count': einv, 'headline': False},
             'sensitivity': {'label': 'SENS', 'status': 'COMPLETE', 'rows': srows, 'band_overlap_count': sov,
                             'invalid_count': sinv, 'headline': False},
             'alternatives': alts}
    # cross-check of the module's helpers against the replicas
    mism = 0
    rep = rep_score(members, ids, bound)
    for a, b in zip(scored, rep):
        for ra, rb in zip(a['rows'], b['rows']):
            for k in ('sigma_ratio', 'within_error', 'status', 'score_status', 'registered_reason'):
                if ra[k] != rb[k]:
                    mism += 1
    renv = rep_envelope_overlap(members, ids, bound)
    for a, b in zip(erows, renv):
        if a['valid'] != b['valid'] or a['band_overlaps_error_bar'] != b['band_overlaps_error_bar']:
            mism += 1
    return score, mism
