"""Synthetic score_after_freeze outputs in the v003g format (prediction_freeze_c2v003g_cx3v001.py, 48a1e48a...).

The functions below are replicas written from reading v003g's _ladder_row, _score_members, _score_members_on_rows,
_pointwise_envelope and _band_rows. crosscheck() compares them with the module's own pure helpers on synthetic
inputs (the module is imported read-only; nothing in it that reads a file is called).

No target is read. Every velocity and sigma here is a synthetic number generated in this file.
"""
import copy
import hashlib
import importlib.util
import json
import math

import numpy as np

QIDS = ['NGC3198-Q%02d' % i for i in range(1, 44)]
V003G = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py'
V003G_SHA = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
ENV_LABEL = 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE'
NOTE_NE = 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'


def load_radii():
    """Target-free query radii (kpc) bound by query id, from the slots V003 query block (sha checked)."""
    raw = open(SLOTS, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == SLOTS_SHA, 'slots sha mismatch'
    d = json.loads(raw)
    rows = d['query_block']['rows']
    assert all(r['Rad_unit'] == 'kpc' for r in rows)
    radii = {r['query_id']: float(r['Rad_text']) for r in rows}
    assert list(radii) == QIDS
    alts = d['alternatives']
    return radii, alts


# ---------------------------------------------------------------- replicas of the v003g format functions
def ladder_row(q, predicted, row_valid, observed, sigma):
    residual = sigma_ratio = fractional = None
    notes = []
    if predicted is not None:
        residual = predicted - observed
        r = residual / sigma
        if math.isfinite(r):
            sigma_ratio = r
        else:
            notes.append('NON_FINITE_SIGMA_RATIO')
        if observed != 0.0:
            f = residual / observed
            if math.isfinite(f):
                fractional = f
            else:
                notes.append('NON_FINITE_FRACTIONAL_ERROR')
    valid = bool(row_valid and predicted is not None)
    within = bool(valid and sigma_ratio is not None and abs(sigma_ratio) <= 1.0)
    return {'id': q, 'observed_speed_km_s': observed, 'predicted_speed_km_s': predicted,
            'quoted_sigma_km_s': sigma, 'signed_residual_km_s': residual, 'sigma_ratio': sigma_ratio,
            'fractional_error': fractional, 'valid': valid, 'within_error': within, 'row_notes': notes}


def score_members(members, ids, bound):
    scored = []
    for m in members:
        rows = []
        for j, q in enumerate(ids):
            row = ladder_row(q, m['speeds_km_s'][j], m['row_valid'][j], bound[j][0], bound[j][1])
            reg = m['row_registration'][j]
            if reg is not None:
                row.update(status='INVALID', prediction=None, registered_reason=reg['reason'],
                           score_status='INVALID_AS_MISS', tier='MISS_WORST_TIER')
                row['row_notes'].append('INVALID_AS_MISS')
            else:
                row.update(status='VALID' if row['valid'] else 'UNEVALUATED_OR_REFUSED',
                           prediction=row['predicted_speed_km_s'], registered_reason=None,
                           score_status='HIT' if row['within_error'] else 'MISS',
                           tier='WITHIN_ERROR' if row['within_error'] else 'MISS_WORST_TIER')
            rows.append(row)
        inv = [r['id'] for r in rows if r['score_status'] == 'INVALID_AS_MISS']
        scored.append({'member_id': m['member_id'], 'log_index': m['log_index'], 'role': m['role'],
                       'evaluated': m['evaluated'], 'member_valid': m['member_valid'],
                       'within_error_count': sum(r['within_error'] for r in rows),
                       'invalid_count': sum(not r['valid'] for r in rows), 'n_rows': len(rows),
                       'invalid_as_miss': inv, 'invalid_as_miss_count': len(inv), 'rows': rows})
    return scored


def score_members_on_rows(members, ids, bound, selected_ids):
    idx = [ids.index(q) for q in selected_ids]
    sub = []
    for m in members:
        n = dict(m)
        for k in ('speeds_km_s', 'row_valid', 'row_registration'):
            n[k] = [m[k][j] for j in idx]
        sub.append(n)
    return score_members(sub, selected_ids, [bound[j] for j in idx])


def pointwise_envelope(members, ids, label=ENV_LABEL):
    rows = []
    n = len(members)
    n_uneval = sum(1 for m in members if not m['evaluated'])
    for j, q in enumerate(ids):
        vals = [m['speeds_km_s'][j] for m in members if m['row_valid'][j]]
        nv = len(vals)
        n_excl = sum(1 for m in members if m['evaluated'] and not m['row_valid'][j])
        rows.append({'id': q, 'band_low_km_s': (min(vals) if nv else None),
                     'band_high_km_s': (max(vals) if nv else None), 'n_members': n, 'n_valid': nv,
                     'n_excluded_invalid': n_excl, 'n_unevaluated': n_uneval,
                     'valid': bool(n >= 1 and n_uneval == 0 and nv >= 1), 'label': label})
    return rows


def band_rows(rows_in, low_key, high_key, ids, bound):
    rows = []
    n_overlap = n_invalid = 0
    for j, q in enumerate(ids):
        r = rows_in[j]
        obs, sig = bound[j]
        lo, hi, valid = r[low_key], r[high_key], r['valid']
        overlaps = bool(valid and lo is not None and hi is not None and lo <= obs + sig and hi >= obs - sig)
        n_overlap += overlaps
        n_invalid += (not valid)
        rows.append({'id': q, 'band_low_km_s': lo, 'band_high_km_s': hi, 'valid': bool(valid),
                     'band_overlaps_error_bar': overlaps, 'label': r['label'],
                     'score_status': 'BAND_OVERLAP' if overlaps else 'BAND_MISS' if valid else 'INVALID_AS_MISS',
                     'tier': 'WITHIN_ERROR' if overlaps else 'MISS_WORST_TIER'})
    return rows, n_overlap, n_invalid


def member_contract_valid(m):
    return bool(m['evaluated'] and m['forward_valid_flag'] is True and any(m['row_valid'])
                and all(rv or reg is not None for rv, reg in zip(m['row_valid'], m['row_registration'])))


# ---------------------------------------------------------------- synthetic builders
def synthetic_bound(seed=0, sigma_override=None):
    """Synthetic (velocity, sigma) pairs; arbitrary numbers, not any target."""
    rng = np.random.default_rng(seed)
    v = [float(40.0 + 3.0 * i + rng.uniform(-1.0, 1.0)) for i in range(43)]
    s = [float(3.0 + rng.uniform(0.0, 2.0)) for i in range(43)]
    if sigma_override:
        for q, val in sigma_override.items():
            s[QIDS.index(q)] = val
    return list(zip(v, s))


def make_member(member_id, log_index, rmap, invalid, bound, *, evaluated=True, forward_valid=True, role='interior',
                abs_offset=None):
    speeds, rv, regs = [], [], []
    for j, q in enumerate(QIDS):
        if not evaluated or not forward_valid:
            speeds.append(None); rv.append(False); regs.append(None)
        elif q in invalid:
            speeds.append(None); rv.append(False)
            regs.append({'status': 'INVALID', 'reason': invalid[q], 'registration': None})
        else:
            v, s = bound[j]
            if abs_offset and q in abs_offset:
                speeds.append(float(v + abs_offset[q])); rv.append(True); regs.append(None)
            else:
                speeds.append(float(v + rmap[q] * s)); rv.append(True); regs.append(None)
    m = {'member_id': member_id, 'point_index': int(member_id[1:]), 'role': role, 'log_index': log_index,
         'evaluated': evaluated, 'forward_valid_flag': (forward_valid if evaluated else None),
         'row_valid': rv, 'speeds_km_s': speeds, 'row_registration': regs}
    m['member_valid'] = member_contract_valid(m)
    return m


DEFAULT_INVALID = {'NGC3198-Q01': 'QUERY_INSIDE_INNERMOST_NODE', 'NGC3198-Q02': 'QUERY_INSIDE_INNERMOST_NODE'}
LOG_INDICES = [5, 17, 23, 31]          # member order M000..M003; the reference is M001 (log_index 17)


def build_score(spec):
    """spec keys: ref_r (q->r), others (list of q->r, len 3), invalid (q->reason, PRIMARY), uneval_other (bool),
    sens (q->(lo_r, hi_r)), alts (name->dict), freeze_status, incomplete_reasons, mode_d_fixed, sigma_override."""
    bound = synthetic_bound(spec.get('seed', 0), spec.get('sigma_override'))
    radii, slot_alts = load_radii()
    inv = dict(DEFAULT_INVALID)
    inv.update(spec.get('invalid', {}))
    for q in spec.get('valid_override', []):
        inv.pop(q, None)
    ref_r = spec['ref_r']
    others = spec.get('others') or [{q: (None if ref_r[q] is None else ref_r[q] + d) for q in ref_r}
                                    for d in (-0.3, 0.2, 0.4)]
    mems = []
    for k, li in enumerate(LOG_INDICES):
        if k == 1:
            mems.append(make_member('M%03d' % k, li, ref_r, inv, bound, role='centroid_nearest',
                                    abs_offset=spec.get('abs_offset')))
        else:
            o = others[k if k == 0 else k - 1]
            ev = not (spec.get('uneval_other') and k == 3)
            mems.append(make_member('M%03d' % k, li, o, inv, bound, evaluated=ev))
    members = score_members(mems, QIDS, bound)
    env = pointwise_envelope(mems, QIDS)
    erows, eov, einv = band_rows(env, 'band_low_km_s', 'band_high_km_s', QIDS, bound)
    sens = spec.get('sens', {})
    per_query = []
    for j, q in enumerate(QIDS):
        rv = mems[1]['row_valid'][j]
        v, s = bound[j]
        if q in sens and rv:
            lo, hi = v + sens[q][0] * s, v + sens[q][1] * s
        else:
            lo = hi = mems[1]['speeds_km_s'][j]
        per_query.append({'id': q, 'reference_speed_km_s': mems[1]['speeds_km_s'][j],
                          'box_limited_band_low_km_s': lo, 'box_limited_band_high_km_s': hi,
                          'max_abs_delta_km_s': (None if lo is None else float(max(abs(lo - (lo if hi is None else hi)), 0.0))),
                          'n_planned': 2, 'n_valid': 2 if rv else 0, 'valid': bool(rv), 'label': 'SENS'})
    srows, sov, sinv = band_rows(per_query, 'box_limited_band_low_km_s', 'box_limited_band_high_km_s', QIDS, bound)
    alts_out = []
    for a in slot_alts['declared']:
        rec = {'name': a['name'], 'kind': a['kind'], 'status': a['status'],
               'role': 'PRIMARY' if a['name'] == slot_alts['primary'] else 'NON_PRIMARY'}
        cfg = spec.get('alts', {}).get(a['name']) or {}
        status = cfg.get('status', a['status'])
        rec['status'] = status
        if rec['role'] == 'PRIMARY':
            rec.update({'scored': True, 'headline': True})
        elif status == 'EVALUATED_BEFORE_FREEZE':
            ainv = dict(inv)
            ainv.update(cfg.get('invalid', {}))
            twin_r = cfg.get('twin_r', ref_r)
            amems = []
            lis = cfg.get('log_indices', LOG_INDICES)
            for k, li in enumerate(lis):
                if k == 1:
                    amems.append(make_member('M%03d' % k, li, twin_r, ainv, bound,
                                             forward_valid=cfg.get('twin_forward_valid', True)))
                else:
                    amems.append(make_member('M%03d' % k, li, {q: (None if twin_r[q] is None else twin_r[q] + 0.5) for q in twin_r}, ainv, bound))
            if a['name'] == 'STAGE0_GRID_OUTER':
                sel = list(a['scoring_scope']['query_ids'])
                am = score_members_on_rows(amems, QIDS, bound, sel)
                rec['scoring_scope'] = {'zone': 'OUTER', 'radius_min_kpc': 30.0, 'radius_min_inclusive': True,
                                        'query_ids': sel, 'registered_query_ids': sel, 'n_rows': len(sel),
                                        'coefficient_grid_pin': dict(a['coefficient_grid_pin']), 'headline': False}
            else:
                am = score_members(amems, QIDS, bound)
            cnt = [m['within_error_count'] for m in am]
            rec.update({'scored': True, 'headline': False,
                        'member_within_error_counts': {'n': len(cnt), 'min': min(cnt), 'max': max(cnt)},
                        'members': am, 'member_evaluation_status': 'COMPLETE'})
        else:
            rec.update({'scored': False, 'headline': False, 'note': NOTE_NE})
        alts_out.append(rec)
    if spec.get('mode_d_fixed'):
        alts_out.append({'name': 'DDO154_DISTANCE_NUISANCE', 'kind': 'calibration_coordinate',
                         'status': 'NOT_EVALUATED_BEFORE_FREEZE', 'role': 'NON_PRIMARY', 'scored': False,
                         'headline': False, 'note': NOTE_NE + ' (A13)'})
    fs = spec.get('freeze_status', 'FREEZE_COMPLETE')
    out = {'ok': True, 'refused': False, 'n_rows': 43, 'freeze_status': fs,
           'incomplete_reasons': spec.get('incomplete_reasons', []),
           'headline': {'reference_member_id': 'M001', 'reference_member_log_index': 17,
                        'reference_within_error_count': members[1]['within_error_count'], 'freeze_status': fs},
           'members': members,
           'pointwise_envelope': {'label': ENV_LABEL, 'rows': erows, 'band_overlap_count': eov,
                                  'invalid_count': einv, 'headline': False},
           'sensitivity': {'label': 'SENS', 'status': 'COMPLETE', 'rows': srows, 'band_overlap_count': sov,
                           'invalid_count': sinv, 'headline': False},
           'alternatives': alts_out}
    return out, radii


# ---------------------------------------------------------------- cross-check against the v003g module
def crosscheck(n_trials=40):
    raw = open(V003G, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == V003G_SHA, 'v003g sha mismatch'
    spec = importlib.util.spec_from_file_location('v003g_readonly_lensc', V003G)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rng = np.random.default_rng(12345)
    mism = 0
    checks = 0
    for t in range(n_trials):
        bound = synthetic_bound(t, {'NGC3198-Q30': 5e-324} if t % 7 == 3 else None)
        inv = dict(DEFAULT_INVALID)
        if t % 3 == 0:
            for q in QIDS[38:]:
                inv[q] = 'QUERY_BEYOND_OUTER_GAS_CUT'
        mems = []
        for k, li in enumerate(LOG_INDICES):
            rmap = {q: float(rng.normal(0, 2)) for q in QIDS}
            if t % 5 == 0 and k == 2:
                rmap['NGC3198-Q10'] = 0.0
            mems.append(make_member('M%03d' % k, li, rmap, inv, bound, evaluated=not (t % 4 == 1 and k == 3),
                                    forward_valid=not (t % 6 == 2 and k == 0)))
        a = score_members(copy.deepcopy(mems), QIDS, bound)
        b = mod._score_members(copy.deepcopy(mems), QIDS, bound)
        checks += 1; mism += (json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True))
        sel = QIDS[35:]
        a = score_members_on_rows(copy.deepcopy(mems), QIDS, bound, sel)
        b = mod._score_members_on_rows(copy.deepcopy(mems), QIDS, bound, sel)
        checks += 1; mism += (json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True))
        ea = pointwise_envelope(copy.deepcopy(mems), QIDS)
        eb = mod._pointwise_envelope(copy.deepcopy(mems), QIDS)
        checks += 1; mism += (json.dumps(ea, sort_keys=True) != json.dumps(eb, sort_keys=True))
        ra = band_rows(ea, 'band_low_km_s', 'band_high_km_s', QIDS, bound)
        rb = mod._band_rows(eb, 'band_low_km_s', 'band_high_km_s', QIDS, bound)
        checks += 1; mism += (json.dumps(ra, sort_keys=True) != json.dumps(rb, sort_keys=True))
        checks += 1; mism += any(member_contract_valid(m) != mod._member_contract_valid(m) for m in mems)
    return {'module_sha256': V003G_SHA, 'trials': n_trials, 'comparisons': checks, 'mismatches': mism}
