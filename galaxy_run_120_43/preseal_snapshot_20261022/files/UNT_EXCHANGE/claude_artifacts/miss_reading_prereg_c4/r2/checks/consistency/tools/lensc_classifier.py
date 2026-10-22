"""Lens C independent classifier for PREREG_MISS_READING_R2.md (sha256 6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143).

Written from the r2 text (sections 0-6) alone, without reading Claude4's tools. It consumes a
score_after_freeze-shaped dict (v003g format) and returns the classification, zone summaries,
patterns, reading statuses, the alternative (twin) readings and the STAGE0 comparison.

Where the text gives no unique answer, or two clauses conflict, the classifier does NOT choose
silently: it records an AMBIGUITY event {tag, case, options}. Where the rules produce an answer
that contradicts another clause or a cited source, it records a CONFLICT event. Coverage holes
(a reachable outcome no pattern covers) are recorded as GAP events.

Synthetic inputs only. This module reads no file; the caller passes the radii (target-free query
block) and the flag record.
"""
import math

ZONES = ('INNER', 'TRANSITION', 'OUTER')
QIDS = ['NGC3198-Q%02d' % i for i in range(1, 44)]
ZONE_TABLE = {q: ('INNER' if i <= 24 else 'TRANSITION' if i <= 35 else 'OUTER')
              for i, q in ((int(q[-2:]), q) for q in QIDS)}          # C-1.3 membership table
UNDEF = 'UNDEFINED'
BUILTIN_REASONS = ('QUERY_INSIDE_INNERMOST_NODE', 'QUERY_BEYOND_OUTER_GAS_CUT', 'QUERY_OUTSIDE_RETAINED_SUPPORT')
NOT_EVAL_NAMES_62 = ('ML_3p6_0.4', 'ML_3p6_0.6', 'GL10_SOURCE_GAUSS_ORDER', 'STAGE0_GRID_OUTER')


class Stop(Exception):
    """A fail-closed stop named by the text (CLASSIFICATION_INPUT_DEFECT, ZONE_TABLE_MISMATCH)."""


class Events:
    def __init__(self):
        self.items = []

    def add(self, kind, tag, case, options=None, detail=None):
        e = {'kind': kind, 'tag': tag, 'case': case}
        if options is not None:
            e['options'] = options
        if detail is not None:
            e['detail'] = detail
        if e not in self.items:
            self.items.append(e)


def zone_of(r_kpc):                       # C-1.3 cuts
    if r_kpc < 10.0:
        return 'INNER'
    if r_kpc < 30.0:
        return 'TRANSITION'
    return 'OUTER'


def median(xs):                           # C-2: even count -> mean of the two middle values
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return UNDEF
    if n % 2:
        return xs[n // 2]
    return 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def sign_class(m):                        # C-2
    if m == UNDEF:
        return UNDEF
    if m < -1.0:
        return 'DEFICIT'
    if m > 1.0:
        return 'EXCESS'
    return 'CENTERED'


def lt(a, b):                             # UNDEFINED makes a condition false (C-2 clarification)
    return a != UNDEF and b != UNDEF and a < b


def gt(a, b):
    return a != UNDEF and b != UNDEF and a > b


def sgn(r):
    return UNDEF if r is None else (-1 if r < 0 else (1 if r > 0 else 0))


# ---------------------------------------------------------------- section 1: per-row classification
def classify_rows(rows_by_id, env_by_id, ids, radii, ev, *, allow_near, who):
    """M-T for one member (C-1.1). rows_by_id: q -> LADDER row; env_by_id: q -> envelope row or None."""
    out = []
    for q in ids:
        L = rows_by_id[q]
        if L.get('status') == 'UNEVALUATED_OR_REFUSED':
            raise Stop('CLASSIFICATION_INPUT_DEFECT: %s %s status UNEVALUATED_OR_REFUSED' % (who, q))
        for f in ('score_status', 'registered_reason', 'within_error', 'sigma_ratio', 'status'):
            if f not in L:
                raise Stop('CLASSIFICATION_INPUT_DEFECT: %s %s missing field %s' % (who, q, f))
        if L['score_status'] == 'INVALID_AS_MISS':
            tier = 'INVALID_AS_MISS'
        elif L['within_error'] is True:
            tier = 'HIT'
        elif allow_near:
            E = env_by_id.get(q)
            if E is None or 'band_overlaps_error_bar' not in E:
                raise Stop('CLASSIFICATION_INPUT_DEFECT: %s %s envelope row/field missing' % (who, q))
            if E.get('valid') is False:
                ev.add('AMBIGUITY', 'C-1.1/C-I7', 'non-INVALID row whose PRIMARY envelope row is invalid (e.g. an '
                       'unevaluated member under FREEZE_INCOMPLETE): NEAR cannot be computed, but the text silently '
                       'reads band_overlaps_error_bar = false',
                       ['MISS (literal: band_overlaps_error_bar false)', 'NEAR NOT_AVAILABLE (row reported as such)'],
                       detail=q)
            tier = 'NEAR' if E['band_overlaps_error_bar'] is True else 'MISS'
        else:
            tier = 'MISS'
        r = L['sigma_ratio']
        if tier != 'INVALID_AS_MISS' and r is None:
            ev.add('AMBIGUITY', 'C-1.1', 'non-INVALID row with sigma_ratio null (v003g NON_FINITE_SIGMA_RATIO): '
                   'the field is present but null; the fail-closed list names only a missing field',
                   ['CLASSIFICATION_INPUT_DEFECT (null treated as missing)', 'MISS with r_q UNDEFINED, '
                    'excluded from or poisoning m(Z)'], detail='%s %s' % (who, q))
        if tier == 'INVALID_AS_MISS' and L.get('registered_reason') not in BUILTIN_REASONS:
            ev.add('CONFLICT', 'C-1.1 vs C-4', 'INVALID_AS_MISS row with a root-listed gate reason: C-1.1 says '
                   'score_status INVALID_AS_MISS holds "exactly when the root-pinned roster registers q INVALID with '
                   'one of the three registered reasons"; C-4 and v003g also admit gate reasons',
                   detail='%s %s %s' % (who, q, L.get('registered_reason')))
        out.append({'id': q, 'R': radii[q], 'zone': ZONE_TABLE[q], 'tier': tier,
                    'r': (None if tier == 'INVALID_AS_MISS' else r),
                    'sign': (None if tier == 'INVALID_AS_MISS' else sgn(r)),
                    'reason': (L.get('registered_reason') if tier == 'INVALID_AS_MISS' else None)})
    return out


def zone_check(ids, radii):
    for q in ids:
        if zone_of(radii[q]) != ZONE_TABLE[q]:
            raise Stop('ZONE_TABLE_MISMATCH: %s at %r kpc' % (q, radii[q]))


# ---------------------------------------------------------------- section 2: summaries and patterns
def summaries(cls):
    S = {}
    for Z in ZONES:
        rows = [c for c in cls if c['zone'] == Z]
        val = [c for c in rows if c['tier'] != 'INVALID_AS_MISS']
        rs = [c['r'] for c in val if c['r'] is not None]
        nv = len(val)
        H = sum(c['tier'] == 'HIT' for c in val)
        N = sum(c['tier'] == 'NEAR' for c in val)
        M = sum(c['tier'] == 'MISS' for c in val)
        inv = [c for c in rows if c['tier'] == 'INVALID_AS_MISS']
        by_reason = {}
        for c in inv:
            by_reason[c['reason']] = by_reason.get(c['reason'], 0) + 1
        m = median(rs) if len(rs) == nv else UNDEF      # a null r on a valid row leaves m undefined
        S[Z] = {'n_rows': len(rows), 'N_v': nv, 'H': H, 'N': N, 'M': M, 'I': len(inv), 'I_by_reason': by_reason,
                'm': m, 'S': sign_class(m),
                'miss_dominated': bool(nv >= 1 and M >= nv / 2.0),
                'hit_dominated': bool(nv >= 1 and H >= nv / 2.0)}
    return S


def outer_trend(cls, S):
    val = sorted([c for c in cls if c['zone'] == 'OUTER' and c['tier'] != 'INVALID_AS_MISS'], key=lambda c: c['R'])
    n = len(val)
    if n < 2 or any(c['r'] is None for c in val):
        d = UNDEF
    else:
        near, far = val[:n // 2], val[n // 2:]               # odd count: the middle row goes to the far half
        d = median([c['r'] for c in far]) - median([c['r'] for c in near])
    growing_terms = {'S_OUTER_DEFICIT': S['OUTER']['S'] == 'DEFICIT', 'delta_lt_0': lt(d, 0.0),
                     'mT_gt_mO': gt(S['TRANSITION']['m'], S['OUTER']['m'])}
    growing = all(growing_terms.values())
    undefined = (d == UNDEF or S['TRANSITION']['m'] == UNDEF or S['OUTER']['m'] == UNDEF) and not growing
    return {'delta_out': d, 'GROWING': growing, 'GROWING_reported_as': (UNDEF if undefined else growing),
            'terms': growing_terms}


def patterns(cls, S, trend, flagged):
    P = {}
    P['P0'] = any(S[Z]['I'] > 0 for Z in ZONES)
    P['P1'] = S['OUTER']['miss_dominated'] and S['OUTER']['S'] == 'DEFICIT'
    P['P1g'] = P['P1'] and trend['GROWING']
    P['P2'] = S['OUTER']['miss_dominated'] and S['OUTER']['S'] == 'EXCESS'
    P['P3'] = S['INNER']['miss_dominated'] and S['INNER']['S'] == 'EXCESS'
    P['P4'] = S['INNER']['miss_dominated'] and S['INNER']['S'] == 'DEFICIT'
    P['P5'] = (S['INNER']['hit_dominated'] and S['OUTER']['miss_dominated'] and S['TRANSITION']['N_v'] >= 1
               and not S['TRANSITION']['hit_dominated'])
    s3 = [S[Z]['S'] for Z in ZONES]
    P['P6'] = (all(S[Z]['N_v'] >= 1 for Z in ZONES) and s3[0] == s3[1] == s3[2]
               and s3[0] not in ('CENTERED', UNDEF))
    total_M = sum(S[Z]['M'] for Z in ZONES)
    P['P7'] = total_M >= 1 and not any(S[Z]['miss_dominated'] for Z in ZONES)
    P['P8'] = total_M == 0
    P['P9'] = S['OUTER']['N_v'] == 0 and S['OUTER']['n_rows'] > 0
    P['P10'] = any(c['tier'] == 'MISS' and c['id'] in flagged for c in cls)
    return P


def pattern_events(cls, S, P, flagged, ev, who):
    for Z in ZONES:
        if S[Z]['miss_dominated'] and S[Z]['hit_dominated']:
            ev.add('CONFLICT', 'C-2/M-3', 'a zone is both miss-dominated and hit-dominated (exact half, N(Z)=0); '
                   'M-3 says the r2 clarifications close tie cases', detail='%s %s H=%d M=%d N_v=%d' % (
                       who, Z, S[Z]['H'], S[Z]['M'], S[Z]['N_v']))
    if P['P5'] and (P['P3'] or P['P4']):
        ev.add('CONFLICT', 'C-2/C-3.2', 'P5 (INNER hit-dominated, onset reading) holds together with P3/P4 (INNER '
               'miss-dominated)', detail=who)
    covered = {'OUTER': P['P1'] or P['P2'] or P['P5'] or P['P6'],
               'INNER': P['P3'] or P['P4'] or P['P6'],
               'TRANSITION': P['P5'] or P['P6']}
    for Z in ZONES:
        if S[Z]['miss_dominated'] and not covered[Z]:
            ev.add('GAP', 'C-2', 'zone miss-dominated but no zone pattern (P1-P6) covers it and P7 is excluded '
                   '("no zone miss-dominated"): no pattern and no reading for it',
                   detail='%s %s S=%s M=%d/N_v=%d' % (who, Z, S[Z]['S'], S[Z]['M'], S[Z]['N_v']))
    total_nv = sum(S[Z]['N_v'] for Z in ZONES)
    if P['P8'] and total_nv == 0:
        ev.add('GAP', 'C-2', 'P8 NO_MISS holds vacuously with no non-INVALID row (no N_v >= 1 guard, unlike P5)',
               detail=who)
    inv_flag = [c['id'] for c in cls if c['id'] in flagged and c['tier'] == 'INVALID_AS_MISS']
    if P['P10'] and inv_flag:
        ev.add('CONFLICT', 'C-2 P10 / C-4', 'P10 is "reported with the tier of every flagged row", but C-4 excludes '
               'INVALID rows from every pattern except P0 and P9', detail='%s %s' % (who, inv_flag))


# ---------------------------------------------------------------- section 3: readings
FACT_A41_ITEM3 = True        # registered before the score (V004 A41 item 3, FORMAL + TESTED)
FACT_A66_2_AZIMUTHAL = True  # registered before the score (A66.2; A42 TESTED): route B consumes the azimuthal mean
DT_STATUS = {'DT-UT1': 'NOT SCHEDULED', 'DT-BHD': 'NOT SCHEDULED', 'DT-U12': 'NOT SCHEDULED', 'DT-TSR': 'NOT SCHEDULED',
             'DT-T1a': 'registered', 'DT-GEO': 'NOT_EVALUATED_BEFORE_FREEZE', 'DT-NAX': 'not run', 'DT-S1': 'UNTESTED'}


def reading_status(name, consistent, against, test_run, ev, undefined_against=None):
    """C-3 rules + C-8 item 5 ('each with the status consistent, inconsistent or OPEN')."""
    cands = []
    if consistent:
        cands.append('consistent')
    if against:
        cands.append('inconsistent')
    if not test_run:
        cands.append('OPEN')
    if undefined_against:
        ev.add('AMBIGUITY', 'C-3.2', 'against-condition uses an undefined term, so whether it fires is decided by '
               'the reporter', [undefined_against + ' holds', undefined_against + ' does not hold'], detail=name)
    if len(cands) > 1:
        ev.add('AMBIGUITY', 'C-3/C-8', 'reading meets more than one status condition; C-8 item 5 asks for one of '
               '"consistent, inconsistent or OPEN" and gives no precedence', cands, detail=name)
    return cands


def readings(P, S, s0, ev):
    R = {}
    nvO = S['OUTER']['N_v']
    omd = S['OUTER']['miss_dominated']
    if omd and not P['P1']:
        ev.add('CONFLICT', 'C-P vs C-3.2', 'OUTER miss-dominated without P1: C-P says "under A15 E3 an outer-row '
               'failure is TESTED-NEGATIVE"; C-3.2 grants TESTED-NEGATIVE only "if P1 holds"',
               ['R-MF TESTED-NEGATIVE (C-P, A15 E3)', 'R-MF not TESTED-NEGATIVE (C-3.2 P1 row; C-8 words rule)'],
               detail='S(OUTER)=%s; R-MF row reached=%s' % (S['OUTER']['S'], P['P1'] or P['P2'] or P['P6']))
    if P['P1'] or P['P2'] or P['P6']:
        tn = P['P1']
        against_p1row = (not P['P1']) and nvO >= 1
        if P['P2'] and against_p1row:
            ev.add('CONFLICT', 'C-3.2', 'R-MF is "consistent" under the P2 row and "against" under the P1 row '
                   '("no P1 with N_v(OUTER) >= 1") at once')
        R['R-MF'] = {'cands': reading_status('R-MF', P['P1'] or P['P2'] or P['P6'], against_p1row, True, ev),
                     'TESTED_NEGATIVE_per_C32': tn}
    if P['P1']:
        R['R-UT1'] = {'cands': reading_status('R-UT1', True, FACT_A41_ITEM3, False, ev)}
        R['R-HIST'] = {'cands': reading_status('R-HIST', True, False, False, ev)}
        R['R-REACH'] = {'cands': reading_status('R-REACH', True, False, False, ev)}
    if P['P1'] or P['P2'] or P['P5']:
        consistent = omd
        if s0 is None or s0['comparison'] in (None, 'NOT_EVALUATED'):
            R['R-DRIFT'] = {'cands': reading_status('R-DRIFT', consistent, False, False, ev), 'DT-S0G': 'NOT_EVALUATED'}
        else:
            comp = s0['comparison']
            if comp == 'NOT_DECIDED':
                ev.add('AMBIGUITY', 'C-3.2/C-6.3', 'the text does not map a NOT_DECIDED DT-S0G comparison to an '
                       'R-DRIFT status', ['OPEN', 'consistent (score relation only)'], detail='R-DRIFT')
            R['R-DRIFT'] = {'cands': reading_status('R-DRIFT', consistent or comp == 'CONSISTENT', comp == 'AGAINST',
                                                    comp != 'NOT_DECIDED', ev), 'DT-S0G': comp}
    if P['P2']:
        R['R-S1'] = {'cands': reading_status('R-S1', True, False, False, ev)}
        R['R-GRID'] = {'cands': reading_status('R-GRID', True, False, False, ev,
                                               undefined_against='"ORIGINAL_K shows the same excess"')}
        ev.add('CONFLICT', 'C-I6 vs C-3.2', 'R-GRID (k-grid fidelity, A17 C3) is a numerical reading registered for '
               'P2, but C-I6 says "The only registered numerical reading is R-TSR"')
    if P['P3'] or P['P4']:
        for nm in ('R-GEFF', 'R-SPEC', 'R-NAX'):
            R[nm] = {'cands': reading_status(nm, True, False, False, ev)}
        R['R-ML'] = {'cands': reading_status('R-ML', True, False, False, ev,
                                             undefined_against='"the DT-T1a M/L variants do not move the inner rows '
                                                               'by the miss"')}
        R['R-GEO'] = {'cands': reading_status('R-GEO', True, False, False, ev)}
    if P['P5']:
        R['P5-onset'] = {'cands': reading_status('P5-onset', True, False, False, ev,
                                                 undefined_against='"an onset radius inconsistent with k*"')}
    if P['P7']:
        ev.add('AMBIGUITY', 'C-3.2', 'P7 readings: "R-NAX; otherwise R-MF at row level" - no rule says when '
               '"otherwise" applies', ['R-NAX', 'R-MF at row level', 'both'])
        R['R-NAX'] = {'cands': reading_status('R-NAX', True, False, False, ev)}
    if P['P8']:
        R['P8'] = {'against_E2': nvO >= 1}
        ev.add('AMBIGUITY', 'C-3.2', 'P8 mandatory check "ORIGINAL_K and the A17 C3 grid record agree": agree on '
               'what is undefined, and the disagreement case is not ruled', ['agree', 'disagree'])
    if P['P9']:
        R['P9'] = {'E2': 'NOT_TESTABLE', 'R-DRIFT': 'OPEN'}
    if P['P10']:
        R['R-TSR'] = {'cands': reading_status('R-TSR', True, FACT_A66_2_AZIMUTHAL, False, ev)}
    return R


# ---------------------------------------------------------------- section 6: alternatives
def twin_of(alt, ref_log_index, ev):
    ms = [m for m in alt.get('members', []) if m.get('log_index') == ref_log_index]
    if not ms:
        return None, 'NO_TWIN (no member at the reference log_index)'
    t = ms[0]
    tests = {'member_valid': t.get('member_valid') is True, 'evaluated': t.get('evaluated') is True,
             'no_unevaluated_rows': all(r.get('status') != 'UNEVALUATED_OR_REFUSED' for r in t['rows'])}
    if len(set(tests.values())) > 1:
        ev.add('AMBIGUITY', 'C-6.1', '"the twin is not valid" names no field; candidate validity tests disagree',
               ['%s=%s' % kv for kv in sorted(tests.items())], detail=alt['name'])
    if not tests['member_valid']:
        return t, 'NO_TWIN (twin member_valid false)'
    return t, None


def classify_alternative(alt, ref_log_index, radii, flagged, ev):
    t, why = twin_of(alt, ref_log_index, ev)
    res = {'name': alt['name'], 'twin': None if t is None else t.get('member_id'),
           'member_within_error_counts': alt.get('member_within_error_counts')}
    if why is not None:
        res['reading'] = why
        return res
    ids = [r['id'] for r in t['rows']]
    if ids != QIDS:
        ev.add('CONFLICT', 'C-6.1 vs C-1.1', 'the twin is classified "by M-T", whose fail-closed stop fires when '
               '"the ids in that member\'s rows are not Q01 to Q43 in order"; an evaluated STAGE0 twin has 8 rows',
               ['CLASSIFICATION_INPUT_DEFECT', 'classify the 8 rows (stop applies to the PRIMARY only)'],
               detail=alt['name'])
    rows_by_id = {r['id']: r for r in t['rows']}
    cls = classify_rows(rows_by_id, {}, ids, radii, ev, allow_near=False, who=alt['name'])
    S = summaries(cls)
    tr = outer_trend(cls, S)
    P = patterns(cls, S, tr, flagged)
    if any(q in flagged for q in ids):
        ev.add('AMBIGUITY', 'C-1.4/C-6.1', 'whether the M-7 TRUNCATION_SHAPE_RESIDUAL flags (from the PRIMARY '
               'numerics N-test record) apply to an alternative\'s rows for P10 is not stated',
               ['apply flags', 'do not apply'], detail=alt['name'])
    pattern_events(cls, S, P, flagged, ev, alt['name'])
    res.update({'rows': cls, 'summaries': S, 'trend': tr, 'patterns': [k for k, v in P.items() if v]})
    return res


def stage0_comparison(prim_cls, alt, ref_log_index, ev):
    if alt['status'] != 'EVALUATED_BEFORE_FREEZE':
        return {'comparison': 'NOT_EVALUATED', 'R-DRIFT': 'OPEN'}
    t, why = twin_of(alt, ref_log_index, ev)
    if why is not None:
        ev.add('AMBIGUITY', 'C-6.3', 'STAGE0 evaluated but its twin reads NO_TWIN: C-6.3 covers only '
               '"stays NOT_EVALUATED" and "evaluated"; the comparison needs twin rows',
               ['comparison NOT_DECIDED; R-DRIFT OPEN', 'comparison not performed', 'run on the invalid twin rows'],
               detail=why)
        return {'comparison': 'NOT_DECIDED', 'why': why}
    prim = {c['id']: c for c in prim_cls}
    tw = {r['id']: r for r in t['rows']}
    rows = [q for q in tw if prim[q]['zone'] == 'OUTER' and prim[q]['tier'] != 'INVALID_AS_MISS'
            and tw[q]['score_status'] != 'INVALID_AS_MISS']
    H_P = sum(prim[q]['tier'] == 'HIT' for q in rows)
    H_S = sum(tw[q]['within_error'] is True for q in rows)
    S_P = sign_class(median([prim[q]['r'] for q in rows]))
    S_S = sign_class(median([tw[q]['sigma_ratio'] for q in rows]))
    if H_S > H_P:
        comp = 'CONSISTENT'
    elif H_S <= H_P and S_S != UNDEF and S_S == S_P:
        comp = 'AGAINST'
    else:
        comp = 'NOT_DECIDED'
    return {'comparison': comp, 'rows': rows, 'H_P': H_P, 'H_S': H_S, 'S_P': S_P, 'S_S': S_S}


# ---------------------------------------------------------------- top level
def classify(score, radii, flag_record, *, root_authorizes_incomplete=False):
    ev = Events()
    out = {'events': None}
    try:
        if score.get('freeze_status') == 'FREEZE_INCOMPLETE' and not root_authorizes_incomplete:
            raise Stop('FREEZE_INCOMPLETE without root authorization (C-I7): not classified')
        ref = score['headline']['reference_member_id']
        ref_li = score['headline']['reference_member_log_index']
        member = [m for m in score['members'] if m['member_id'] == ref]
        if len(member) != 1:
            raise Stop('CLASSIFICATION_INPUT_DEFECT: reference member not found once')
        rows = member[0]['rows']
        ids = [r.get('id') for r in rows]
        if ids != QIDS:
            raise Stop('CLASSIFICATION_INPUT_DEFECT: reference member row ids are not Q01-Q43 in order')
        zone_check(ids, radii)
        env = {r['id']: r for r in score['pointwise_envelope']['rows']}
        flagged = {f['query_id'] for f in flag_record}
        cls = classify_rows({r['id']: r for r in rows}, env, ids, radii, ev, allow_near=True, who='PRIMARY')
        # NEAR gloss check (C-1.1 "Some admitted representative member state reaches the error bar")
        for c in cls:
            if c['tier'] == 'NEAR':
                anyhit = any(r['within_error'] for m in score['members'] for r in m['rows'] if r['id'] == c['id'])
                c['some_member_within_error'] = anyhit
                if not anyhit:
                    ev.add('CONFLICT', 'C-1.1 / M-1', 'NEAR row where no PRIMARY member is within error (the '
                           'pointwise min/max band straddles the error bar): the registered meaning "some admitted '
                           'representative member state reaches the error bar" is false', detail=c['id'])
        # sensitivity band: never a tier; "only reported" - but C-8 has no slot for it
        srows = {r['id']: r for r in (score.get('sensitivity') or {}).get('rows', [])}
        sens_only = [c['id'] for c in cls if c['tier'] == 'MISS' and srows.get(c['id'], {}).get('band_overlaps_error_bar')]
        if sens_only:
            ev.add('AMBIGUITY', 'C-1.1 vs C-8', 'MISS rows where the box-limited sensitivity band overlaps the error '
                   'bar: C-1.1 says the band "is only reported", but the C-8 report format has no place for it',
                   ['report per row (unregistered format)', 'report selected rows only', 'do not report'],
                   detail=sens_only)
        S = summaries(cls)
        tr = outer_trend(cls, S)
        P = patterns(cls, S, tr, flagged)
        pattern_events(cls, S, P, flagged, ev, 'PRIMARY')
        # alternatives (C-6)
        alts = []
        s0 = None
        for a in score.get('alternatives', []):
            if a.get('role') == 'PRIMARY':
                continue
            if a.get('status') == 'EVALUATED_BEFORE_FREEZE':
                alts.append(classify_alternative(a, ref_li, radii, flagged, ev))
                if a['name'] == 'STAGE0_GRID_OUTER':
                    s0 = stage0_comparison(cls, a, ref_li, ev)
            else:
                if a['name'] not in NOT_EVAL_NAMES_62:
                    ev.add('AMBIGUITY', 'C-I4/C-6.2', 'the score output lists a NOT_EVALUATED alternative that C-I4 '
                           'and C-6.2 do not name (v003g appends the A13 recorded distance alternative in the fixed-'
                           'distance mode)', ['report under C-6.2', 'omit'], detail=a['name'])
                alts.append({'name': a['name'], 'reading': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never '
                             'scored as the headline'})
                if a['name'] == 'STAGE0_GRID_OUTER':
                    s0 = {'comparison': 'NOT_EVALUATED', 'R-DRIFT': 'OPEN'}
        R = readings(P, S, s0, ev)
        # C-5: comparisons
        e2_p8_global = P['P8']
        e2_outer_nomiss = S['OUTER']['N_v'] >= 1 and S['OUTER']['M'] == 0
        if e2_p8_global != e2_outer_nomiss:
            ev.add('AMBIGUITY', 'C-5.2', '"Report P1/P1g/P2/P8/P9 for OUTER": P8 is a global pattern; its global '
                   'value differs from an OUTER-only no-miss reading here', ['P8 global=%s' % e2_p8_global,
                                                                            'OUTER no-miss=%s' % e2_outer_nomiss])
        provisional = score.get('freeze_status') == 'FREEZE_INCOMPLETE'
        out.update({'ok': True, 'rows': cls, 'summaries': S, 'trend': tr,
                    'patterns': [k for k, v in P.items() if v], 'readings': R, 'alternatives': alts, 'stage0': s0,
                    'invalid_list': [{'id': c['id'], 'zone': c['zone'], 'reason': c['reason']} for c in cls
                                     if c['tier'] == 'INVALID_AS_MISS'],
                    'E1a': {k: S['INNER'][k] for k in ('H', 'N', 'M')},
                    'E1a_subtable': [c for c in cls if 3 <= int(c['id'][-2:]) <= 15],
                    'E1b': 'NOT_AVAILABLE',
                    'label': ('PROVISIONAL (FREEZE_INCOMPLETE) ' + repr(score.get('incomplete_reasons'))
                              if provisional else None)})
    except Stop as e:
        out.update({'ok': False, 'stop': str(e)})
    out['events'] = ev.items
    return out
