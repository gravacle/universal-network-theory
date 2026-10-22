"""Lens R2-B (regressions and new defects): an independent classifier written from the text of
PREREG_MISS_READING_R2.md round 2 (97d5ce33...) alone, sections 0-6 (C-I1..C-6.3).

It never chooses silently. Where the text gives no unique answer it records an AMBIGUITY event and
carries every admissible option; where two clauses disagree it records a CONFLICT; where a reachable
outcome is covered by no rule it records a GAP. Pure functions only: no file, network or process access.
Input: one dict in the v003g score_after_freeze output format plus a target-free context dict.
"""
import math

IDS = ['NGC3198-Q%02d' % i for i in range(1, 44)]
ZONE_OF = {}
for _i, _q in enumerate(IDS, start=1):
    ZONE_OF[_q] = 'INNER' if _i <= 24 else ('TRANSITION' if _i <= 35 else 'OUTER')   # C-1.3 table, by id
ZONES = ('INNER', 'TRANSITION', 'OUTER')
CUT_INNER, CUT_OUTER = 10.0, 30.0                                                      # C-1.3 cut numbers
BUILTIN = ('QUERY_INSIDE_INNERMOST_NODE', 'QUERY_BEYOND_OUTER_GAS_CUT', 'QUERY_OUTSIDE_RETAINED_SUPPORT')
ENV_PREFIX = 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE'                               # C-I3
TSR_FLAGGED_R2 = ('NGC3198-Q25',)                                                      # C-1.4 "fixed here by id"
ZONE_PATTERNS = ('P1', 'P2', 'P11', 'P3', 'P4', 'P12', 'P13')                          # C-2 coverage set

# C-3.1 deciding tests and their status at writing
DT_STATUS = {'DT-UT1': 'NOT SCHEDULED', 'DT-BHD': 'NOT SCHEDULED', 'DT-U12': 'NOT SCHEDULED',
             'DT-T1a': 'registered', 'DT-GEO': 'NOT_EVALUATED_BEFORE_FREEZE', 'DT-ALT': 'as stated',
             'DT-NAX': 'not run', 'DT-S1': 'UNTESTED', 'DT-S0G': None, 'DT-TSR': 'NOT SCHEDULED',
             'SCORE': 'the score itself, for this scope only'}

# C-3.2, one entry per (row, reading): (row id, trigger patterns, reading, against id, prior, deciding tests)
READING_ROWS = [
    ('R01', ('P1', 'P1g', 'P2', 'P11'), 'R-MF', 'OUTER_NOT_MISS_DOMINATED', 'for: A15 E2, A41', ('SCORE',)),
    ('R02', ('P1', 'P1g'), 'R-UT1', None, 'against: A41 item 3', ('DT-UT1',)),
    ('R03', ('P1', 'P1g'), 'R-HIST', None, '', ('DT-BHD',)),
    ('R04', ('P1', 'P1g'), 'R-REACH', None, '', ('DT-U12',)),
    ('R05', ('P1', 'P1g', 'P2', 'P11'), 'R-DRIFT', 'DT_S0G_AGAINST', 'for: A63 SUPPORTED; against: A65 R-3 UNTESTED', ('DT-S0G',)),
    ('R06', ('P2', 'P11'), 'R-S1', None, '', ('DT-S1',)),
    ('R07', ('P2', 'P11'), 'R-GRID', None, 'against: A27, A90', ()),
    ('R08', ('P11',), 'R-NAX', None, '', ('DT-NAX',)),
    ('R09', ('P3', 'P4', 'P12'), 'R-GEFF', None, '', ('DT-S1',)),
    ('R10', ('P3', 'P4', 'P12'), 'R-ML', 'ML_ALTS', '', ('DT-ALT', 'DT-T1a')),
    ('R11', ('P3', 'P4', 'P12'), 'R-SPEC', None, '', ('DT-T1a',)),
    ('R12', ('P3', 'P4', 'P12', 'P6'), 'R-GEO', None, '', ('DT-GEO',)),
    ('R13', ('P3', 'P4', 'P12', 'P7', 'P13'), 'R-NAX', None, '', ('DT-NAX',)),
    ('R14', ('P5',), 'AS_P1', 'AS_P1', 'as P1', ('AS_P1', 'DT-NAX')),
    ('R15', ('P13',), 'R-NAX+R-TSR(via P10)', None, '', ('DT-NAX', 'DT-TSR')),
    ('R16', ('P6',), 'R-S1,R-GEO,R-MF(all radii)', None, '', ('DT-S1', 'DT-GEO')),
    ('R17', ('P7',), 'R-NAX,R-MF(row level)', None, '', ('DT-NAX',)),
    ('R18', ('P8',), 'P8_REPORT', None, '', ()),
    ('R19', ('P9',), 'P9_OUTER_UNAVAILABLE(R-DRIFT stays OPEN)', None, '', ()),
    ('R20', ('P10',), 'R-TSR', None, 'against: A66.2; A42', ('DT-TSR',)),
]


def _median(vals):
    v = sorted(vals)
    n = len(v)
    if n == 0:
        return None
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])


def _sign(r):
    if r is None:
        return 'UNDEFINED'
    return -1 if r < 0 else (1 if r > 0 else 0)


def _sclass(m):
    if m is None:
        return 'UNDEFINED'
    return 'DEFICIT' if m < -1 else ('EXCESS' if m > 1 else 'CENTERED')


class Events:
    def __init__(self):
        self.items = []

    def add(self, kind, clause, detail, options=None):
        e = {'kind': kind, 'clause': clause, 'detail': detail}
        if options is not None:
            e['options'] = options
        if e not in self.items:
            self.items.append(e)


def stop_checks(score, ctx):
    """C-1.1 pre-score stop conditions; target-free; any one -> CLASSIFICATION_INPUT_DEFECT."""
    reasons = []
    try:
        ref_id = score['headline']['reference_member_id']
        ref = [m for m in score['members'] if m['member_id'] == ref_id]
        if len(ref) != 1:
            reasons.append('reference member not unique in members')
            return reasons
        rows = ref[0]['rows']
        ids = [r['id'] for r in rows]
        if ids != IDS:
            reasons.append('reference member ids are not Q01..Q43 in order')
        for r in rows:
            for f in ('score_status', 'within_error', 'sigma_ratio', 'registered_reason', 'status'):
                if f not in r:
                    reasons.append('missing field %s' % f)
                    break
            if r.get('status') == 'UNEVALUATED_OR_REFUSED':
                reasons.append('reference row %s UNEVALUATED_OR_REFUSED' % r.get('id'))
        env = score['pointwise_envelope']
        if not isinstance(env.get('label'), str) or not env['label'].startswith(ENV_PREFIX):
            reasons.append('envelope label prefix differs')
        if [e['id'] for e in env['rows']] != IDS or any('band_overlaps_error_bar' not in e for e in env['rows']):
            reasons.append('envelope rows missing or out of order')
        radii = ctx['radii']
        for q in IDS:
            R = radii[q]
            z = 'INNER' if R < CUT_INNER else ('TRANSITION' if R < CUT_OUTER else 'OUTER')
            if z != ZONE_OF[q]:
                reasons.append('zone table differs at %s' % q)
    except (KeyError, TypeError, IndexError) as exc:
        reasons.append('missing field: %r' % (exc,))
    return reasons


def classify_rows(member_rows, env_rows, sens_rows, ctx, ev, who, late_assumption):
    """C-1.1/C-1.2/C-1.3/C-1.4/C-4 per-row classification for one member (PRIMARY ref or a twin)."""
    out = []
    flagged = set(ctx.get('tsr_flagged', TSR_FLAGGED_R2))
    late_rows = ctx.get('late_gate_rows')       # set of (qid, reason), or None when unknown
    for j, r in enumerate(member_rows):
        q = r['id']
        row = {'id': q, 'zone': ZONE_OF[q], 'R_q': ctx['radii'][q], 'tsr_flag': q in flagged,
               'invalid_reason': None, 'gate_after_predictions': False}
        if r['score_status'] == 'INVALID_AS_MISS':
            reason = r['registered_reason']
            row['invalid_reason'] = reason
            is_gate = reason not in BUILTIN
            late = False
            if is_gate:
                if late_rows is None:
                    ev.add('GAP', 'C-4 LATE gates', '%s: gate reason %r is a root-listed gate; whether it is LATE (registered '
                           'after any step-5 output value exists) is not carried by any field of the score output, the roster '
                           'or the gate schema; classified under the assumption %s' % (who, reason, late_assumption))
                    late = late_assumption == 'LATE'
                else:
                    late = (q, reason) in late_rows
            if late:
                row.update(tier='MISS', counts_as='NON_INVALID_MISS_SIGN_UNDEFINED', r=None, sign='UNDEFINED',
                           gate_after_predictions=True)
            else:
                row.update(tier='INVALID_AS_MISS', counts_as='INVALID', r=None, sign=None)
        else:
            rq = r['sigma_ratio']
            hit = r['within_error'] is True
            row.update(tier='HIT' if hit else 'MISS', counts_as='HIT' if hit else 'MISS', r=rq, sign=_sign(rq))
        # NEAR flag (C-1.1), PRIMARY only; C-I7 incomplete-freeze clause
        row['near'] = False
        if env_rows is not None and row['tier'] == 'MISS':
            e = env_rows[j]
            if not e['valid']:
                row['near'] = 'NOT_AVAILABLE'
            else:
                row['near'] = bool(e['band_overlaps_error_bar'])
            if row['gate_after_predictions'] and e['valid'] and e['band_overlaps_error_bar']:
                ev.add('AMBIGUITY', 'C-1.1 vs C-4', '%s %s: a LATE-gate row (reference prediction null) gets a NEAR flag from '
                       'the other members\' envelope' % (who, q), ['NEAR true', 'NEAR not applicable'])
        if sens_rows is not None:
            s = sens_rows[j]
            row['sensitivity_overlap'] = 'invalid' if not s['valid'] else ('yes' if s['band_overlaps_error_bar'] else 'no')
        out.append(row)
    return out


def zone_summaries(rows):
    zs = {}
    for Z in ZONES:
        zr = [r for r in rows if r['zone'] == Z]
        nonin = [r for r in zr if r['counts_as'] != 'INVALID']
        H = sum(1 for r in nonin if r['tier'] == 'HIT')
        M = sum(1 for r in nonin if r['tier'] == 'MISS')
        N = sum(1 for r in nonin if r['near'] is True)
        N_na = sum(1 for r in nonin if r['near'] == 'NOT_AVAILABLE')
        inv = {}
        for r in zr:
            if r['counts_as'] == 'INVALID':
                inv[r['invalid_reason']] = inv.get(r['invalid_reason'], 0) + 1
        defined = [r['r'] for r in nonin if r['r'] is not None]
        m = _median(defined)
        Nv = len(nonin)
        zs[Z] = {'n_rows': len(zr), 'N_v': Nv, 'H': H, 'M': M, 'N': N, 'N_not_available': N_na,
                 'I': sum(inv.values()), 'I_by_reason': inv, 'm': m, 'S': _sclass(m),
                 'n_defined_r': len(defined),
                 'miss_dominated': Nv >= 1 and M >= Nv / 2.0, 'hit_dominated': Nv >= 1 and H > Nv / 2.0}
    return zs


def outer_trend(rows, zs):
    o = sorted([r for r in rows if r['zone'] == 'OUTER' and r['counts_as'] != 'INVALID' and r['r'] is not None],
               key=lambda r: r['R_q'])
    if len(o) < 2:
        d = None
    else:
        k = len(o) // 2                      # odd count: the middle row goes to the far half
        near, far = o[:k], o[k:]
        d = _median([r['r'] for r in far]) - _median([r['r'] for r in near])
    mt, mo = zs['TRANSITION']['m'], zs['OUTER']['m']
    growing = (zs['OUTER']['S'] == 'DEFICIT' and d is not None and d < 0 and mt is not None and mo is not None and mt > mo)
    return d, growing


def patterns(rows, zs, d_out, growing):
    I, T, O = zs['INNER'], zs['TRANSITION'], zs['OUTER']
    nonin = [r for r in rows if r['counts_as'] != 'INVALID']
    M_tot = sum(1 for r in nonin if r['tier'] == 'MISS')
    p = {}
    p['P0'] = any(zs[Z]['I'] > 0 for Z in ZONES)
    p['P1'] = O['miss_dominated'] and O['S'] == 'DEFICIT'
    p['P1g'] = p['P1'] and growing
    p['P2'] = O['miss_dominated'] and O['S'] == 'EXCESS'
    p['P11'] = O['miss_dominated'] and O['S'] == 'CENTERED'
    p['P3'] = I['miss_dominated'] and I['S'] == 'EXCESS'
    p['P4'] = I['miss_dominated'] and I['S'] == 'DEFICIT'
    p['P12'] = I['miss_dominated'] and I['S'] == 'CENTERED'
    p['P13'] = T['miss_dominated']
    p['P5'] = I['hit_dominated'] and O['miss_dominated'] and T['N_v'] >= 1 and not T['hit_dominated']
    p['P6'] = (I['S'] == T['S'] == O['S'] and I['S'] not in ('CENTERED', 'UNDEFINED') and
               all(zs[Z]['N_v'] >= 1 for Z in ZONES))
    p['P7'] = M_tot >= 1 and not any(zs[Z]['miss_dominated'] for Z in ZONES)
    p['P8'] = len(nonin) >= 1 and M_tot == 0
    p['P9'] = O['N_v'] == 0
    p['P10'] = any(r['tier'] == 'MISS' and r['tsr_flag'] for r in nonin)
    return p, M_tot


def dt_s0g(prim_rows, twin_rows):
    """C-6.3 comparison rule on OUTER rows non-INVALID under both with a defined r under both."""
    tw = {r['id']: r for r in twin_rows}
    qual = []
    for r in prim_rows:
        if r['zone'] != 'OUTER' or r['id'] not in tw:
            continue
        s = tw[r['id']]
        if r['counts_as'] == 'INVALID' or s['counts_as'] == 'INVALID' or r['r'] is None or s['r'] is None:
            continue
        qual.append((r, s))
    if not qual:
        return {'n_rows': 0, 'outcome': 'NOT_DECIDED'}
    HP = sum(1 for r, s in qual if r['tier'] == 'HIT')
    HS = sum(1 for r, s in qual if s['tier'] == 'HIT')
    AP = _median([abs(r['r']) for r, s in qual])
    AS = _median([abs(s['r']) for r, s in qual])
    if HS > HP:
        out = 'CONSISTENT'
    elif HS <= HP and AS >= AP:
        out = 'AGAINST'
    else:
        out = 'NOT_DECIDED'
    return {'n_rows': len(qual), 'H_P': HP, 'H_S': HS, 'A_P': AP, 'A_S': AS, 'outcome': out}


def _dt_part2(dt, ctx, s0g):
    if dt == 'SCORE':
        return None   # filled by the caller
    if dt == 'DT-S0G':
        if s0g is None:
            return 'OPEN (STAGE0 NOT_EVALUATED_BEFORE_FREEZE)'
        if s0g in ('TWIN_INVALID', 'TWIN_INPUT_DEFECT'):
            return 'OPEN (%s)' % s0g
        if s0g == 'NOT_DECIDED':
            return 'OPEN (NOT_DECIDED)'
        return 'DT-S0G %s' % s0g
    if dt == 'DT-ALT':
        return 'OPEN (ML_3p6 NOT_EVALUATED_BEFORE_FREEZE)'
    if dt == 'DT-T1a':
        return ctx.get('dt_t1a_outcome') or 'OPEN (not run at classification)'
    st = DT_STATUS[dt]
    if st in ('NOT SCHEDULED', 'not run', 'UNTESTED', 'NOT_EVALUATED_BEFORE_FREEZE'):
        return 'OPEN'
    return st


def readings(p, zs, rows, ctx, ev, s0g, outer_failure, provisional):
    out = []
    O = zs['OUTER']
    p1_readings = [x for x in READING_ROWS if 'P1' in x[1]]
    for rid, trig, name, against, prior, dts in READING_ROWS:
        holding = [t for t in trig if p.get(t)]
        if not holding:
            continue
        rec = {'row': rid, 'patterns_holding': holding, 'reading': name, 'prior': prior}
        # score relation (part 1)
        rel = 'CONSISTENT'
        rel_options = None
        if against == 'OUTER_NOT_MISS_DOMINATED':
            if (not O['miss_dominated']) and O['N_v'] >= 1:
                rel = 'INCONSISTENT'
            ev.add('NOTE', 'C-3.2 R01', 'R-MF against-condition "OUTER not miss-dominated, with N_v(OUTER) >= 1" can never '
                   'hold while R01 is reported (its patterns all require OUTER miss-dominated); against-precedence is dead here')
        elif against == 'DT_S0G_AGAINST':
            if s0g == 'AGAINST':
                rel = 'INCONSISTENT'
        elif against == 'ML_ALTS':
            rel_options = ['CONSISTENT (no against-condition holds)', 'NOT_AVAILABLE (the text: "this reads NOT_AVAILABLE")']
            ev.add('AMBIGUITY', 'C-3 vs C-3.2 R-ML', 'R-ML against-condition "reads NOT_AVAILABLE"; part 1 must be one of '
                   'CONSISTENT/INCONSISTENT/NOT_ADDRESSED', rel_options)
        elif against == 'AS_P1':
            if not p['P1']:
                ev.add('AMBIGUITY', 'C-3.2 P5 row', 'P5 holds with S(OUTER)=%s, so P1 does not hold; "as P1" either imports '
                       'the P1 readings (R-MF, R-UT1, R-HIST, R-REACH, R-DRIFT; deficit readings) or the readings of the OUTER '
                       'pattern that does hold, or none' % O['S'],
                       ['P1 readings regardless of sign', 'readings of the holding OUTER pattern (%s)' %
                        [t for t in ('P1', 'P2', 'P11') if p[t]], 'P1 readings NOT_ADDRESSED'])
        rec['part1'] = rel if rel_options is None else rel_options
        # deciding-test status (part 2)
        part2 = []
        for dt in dts:
            if dt == 'SCORE':
                part2.append('TESTED-NEGATIVE (A15 E3 scope)' if outer_failure else 'NOT_NEGATIVE_AT_OUTER')
            elif dt == 'AS_P1':
                part2.append('as P1')
            else:
                part2.append('%s: %s' % (dt, _dt_part2(dt, ctx, s0g)))
        rec['part2'] = part2
        if rid in ('R16', 'R17'):
            ev.add('AMBIGUITY', 'C-3 / C-3.2 %s' % rid, 'R-MF is a reading of %s but the row names no deciding test for R-MF '
                   '(listed: %s); R01 names "the score itself". Part 2 for R-MF is not fixed' % (holding, list(dts)),
                   ['the score itself -> %s' % ('TESTED-NEGATIVE' if outer_failure else 'NOT_NEGATIVE_AT_OUTER'),
                    'OPEN (no test named in this row)'])
            if rid == 'R17' and (not O['miss_dominated']) and O['N_v'] >= 1:
                ev.add('AMBIGUITY', 'C-3 / C-3.2 R17 vs R01', 'under P7 R-MF\'s R01 against-condition holds (OUTER not '
                       'miss-dominated, N_v(OUTER) >= 1) but the P7 row lists no against-condition',
                       ['CONSISTENT (row-level against: none)', 'INCONSISTENT (reading-level against of R01)'])
        if rid == 'R15' and not p['P10']:
            ev.add('AMBIGUITY', 'C-3.2 P13 row', 'P13 holds and P10 does not (flagged rows: %s); R-TSR "for flagged rows (via '
                   'P10)" is either CONSISTENT under P13 or NOT_ADDRESSED' % [(r['id'], r['tier']) for r in rows if r['tsr_flag']],
                   ['R-TSR CONSISTENT (pattern P13 holds)', 'R-TSR NOT_ADDRESSED (P10 does not hold)'])
        if rid == 'R20':
            late_flagged = [r['id'] for r in rows if r['tsr_flag'] and r['gate_after_predictions'] and r['tier'] == 'MISS']
            if late_flagged:
                ev.add('CONFLICT', 'C-2 P10 / C-3 scope / C-4', 'P10 holds on LATE-gate row(s) %s (non-INVALID MISS for counts, '
                       'INVALID_AS_MISS with a null prediction in LADDER); R-TSR would be CONSISTENT on a row with no '
                       'prediction, while "no reading cites an INVALID row"' % late_flagged,
                       ['P10 holds; R-TSR CONSISTENT citing the LATE row', 'P10 does not hold (LATE row is INVALID for citation)'])
        if rid == 'R19':
            ev.add('AMBIGUITY', 'C-3.2 P9 row', 'P9 row says "R-DRIFT stays OPEN": R-DRIFT is reported under P9 with part 1 '
                   'CONSISTENT (pattern holds) or is NOT_ADDRESSED with part 2 OPEN', ['R-DRIFT (CONSISTENT, OPEN)',
                                                                                   'R-DRIFT (NOT_ADDRESSED, OPEN)'])
        if rid == 'R10' and ctx.get('dt_t1a_outcome') is None:
            pass
        if provisional:
            rec['label'] = 'PROVISIONAL (FREEZE_INCOMPLETE)'
        out.append(rec)
    if p['P1g']:
        ev.add('NOTE', 'C-2 / C-3.2', 'P1g is a flag on P1 in the C-2 table but a trigger column entry in C-3.2 rows R01-R05; '
               'a classifier that treats P1g as a pattern reports R-MF, R-UT1, R-HIST, R-REACH and R-DRIFT twice')
    return out


def e3_line(zs, of):
    O = zs['OUTER']
    if O['N_v'] == 0:
        v = 'NOT_TESTABLE'
    elif of:
        v = 'TESTED-NEGATIVE (A15 E3 scope)'
    else:
        v = 'NOT_NEGATIVE_AT_OUTER'
    return v


def classify_member(member_rows, env_rows, sens_rows, ctx, ev, who, late_assumption, s0g=None, provisional=False,
                    with_readings=True):
    rows = classify_rows(member_rows, env_rows, sens_rows, ctx, ev, who, late_assumption)
    zs = zone_summaries(rows)
    d_out, growing = outer_trend(rows, zs)
    p, M_tot = patterns(rows, zs, d_out, growing)
    of_a = zs['OUTER']['miss_dominated']                 # "OUTER is miss-dominated, whatever its sign class"
    of_b = p['P1'] or p['P2'] or p['P11']                 # "It holds exactly when one of P1, P2 or P11 holds"
    res = {'rows': rows, 'zones': zs, 'delta_out': d_out, 'growing': growing, 'patterns': p,
           'patterns_holding': [k for k in ('P0', 'P1', 'P1g', 'P2', 'P11', 'P3', 'P4', 'P12', 'P13', 'P5', 'P6', 'P7',
                                            'P8', 'P9', 'P10') if p[k]],
           'outer_failure_def_miss_dominated': of_a, 'outer_failure_def_P1_P2_P11': of_b}
    if of_a != of_b:
        ev.add('CONFLICT', 'C-2 OUTER_FAILURE', '%s: OUTER miss-dominated=%s with S(OUTER)=%s, so the two registered '
               'definitions of OUTER_FAILURE disagree' % (who, of_a, zs['OUTER']['S']),
               ['OUTER_FAILURE true (miss-dominated)', 'OUTER_FAILURE false (no P1/P2/P11)'])
    if M_tot >= 1 and not any(p[k] for k in ZONE_PATTERNS) and not p['P7']:
        ev.add('GAP', 'C-2 coverage property', '%s: %d MISS row(s) but no zone pattern and no P7 holds; S by zone %s' %
               (who, M_tot, {Z: zs[Z]['S'] for Z in ZONES}))
    if any(r['gate_after_predictions'] for r in rows):
        ev.add('NOTE', 'C-4 LATE gates', '%s: LATE rows present: %s' % (who, [r['id'] for r in rows if r['gate_after_predictions']]))
    res['e3_by_definition'] = {'miss_dominated': e3_line(zs, of_a), 'P1_P2_P11': e3_line(zs, of_b)}
    if res['e3_by_definition']['miss_dominated'] != res['e3_by_definition']['P1_P2_P11']:
        ev.add('CONFLICT', 'C-5.3 E3 verdict line', '%s: the E3 verdict differs between the two OUTER_FAILURE definitions: %s' %
               (who, res['e3_by_definition']))
    if with_readings:
        res['readings'] = readings(p, zs, rows, ctx, ev, s0g, of_a and of_b, provisional)
    mt = [r for r in rows if r['zone'] in ('TRANSITION', 'OUTER') and r['tier'] == 'MISS']
    res['onset_radius_all_MISS'] = min([r['R_q'] for r in mt]) if mt else None
    mt2 = [r for r in mt if not r['gate_after_predictions']]
    res['onset_radius_excluding_LATE'] = min([r['R_q'] for r in mt2]) if mt2 else None
    if res['onset_radius_all_MISS'] != res['onset_radius_excluding_LATE']:
        ev.add('AMBIGUITY', 'C-3.2 onset radius / C-4', '%s: the onset radius depends on whether LATE rows are MISS rows' % who,
               [res['onset_radius_all_MISS'], res['onset_radius_excluding_LATE']])
    if any(r['near'] == 'NOT_AVAILABLE' for r in rows):
        ev.add('AMBIGUITY', 'C-I7 / C-2 N(Z)', '%s: NEAR could not be set on some MISS rows; N(Z) in the zone summaries and '
               'the E3 line is 0 or NOT_AVAILABLE' % who, ['N(Z)=0', 'N(Z)=NOT_AVAILABLE'])
    late_inv = [r for r in rows if r['gate_after_predictions']]
    if late_inv and not res['patterns']['P0']:
        ev.add('AMBIGUITY', 'C-2 P0 vs C-4', '%s: the only roster INVALID rows are LATE-gate rows; P0 ("INVALID rows ... per '
               'registered reason (C-4)") reads false under the counts rule but the rows are INVALID_AS_MISS in LADDER' % who,
               ['P0 false', 'P0 true'])
    return res


def classify(score, ctx, late_assumption='LATE'):
    ev = Events()
    stop = stop_checks(score, ctx)
    if stop:
        return {'status': 'CLASSIFICATION_INPUT_DEFECT', 'stop_reasons': stop, 'events': ev.items}
    provisional = score['freeze_status'] != 'FREEZE_COMPLETE'
    ref_id = score['headline']['reference_member_id']
    ref = next(m for m in score['members'] if m['member_id'] == ref_id)
    ref_li = ref['log_index']
    alts = {}
    s0g = None
    stage0_twin_rows = None
    for a in score['alternatives']:
        if a.get('role') == 'PRIMARY':
            continue
        rec = {'name': a['name'], 'status': a['status']}
        if a['status'] != 'EVALUATED_BEFORE_FREEZE' or not a.get('scored'):
            rec['reading'] = 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'
            alts[a['name']] = rec
            continue
        twins = [m for m in a['members'] if m['log_index'] == ref_li]
        if len(twins) != 1:
            rec['reading'] = 'NO_TWIN'
            ev.add('GAP', 'C-6.1', '%s: no unique twin (text says one exists by construction)' % a['name'])
            alts[a['name']] = rec
            continue
        tw = twins[0]
        scope = a.get('scoring_scope', {}).get('query_ids') if a['name'] == 'STAGE0_GRID_OUTER' else IDS
        if [r['id'] for r in tw['rows']] != list(scope):
            rec['reading'] = 'TWIN_INPUT_DEFECT'
            if a['name'] == 'STAGE0_GRID_OUTER':
                s0g = 'TWIN_INPUT_DEFECT'
                ev.add('GAP', 'C-6.1 / C-6.3', 'STAGE0 TWIN_INPUT_DEFECT: C-6.3 states R-DRIFT stays OPEN only for TWIN_INVALID '
                       'and NOT_DECIDED; R-DRIFT status under TWIN_INPUT_DEFECT is unstated')
            alts[a['name']] = rec
            continue
        if not tw['member_valid']:
            rec['reading'] = 'TWIN_INVALID'
            rec['member_within_error_counts'] = a.get('member_within_error_counts')
            if a['name'] == 'STAGE0_GRID_OUTER':
                s0g = 'TWIN_INVALID'
            alts[a['name']] = rec
            continue
        sub_ctx = dict(ctx)
        if not ctx.get('tsr_flags_apply_to_alternatives_known'):
            ev.add('AMBIGUITY', 'C-6.1 / C-2 P10', '%s: C-6.1 applies the C-2 rules (N(Z)=0) to the twin, but does not say '
                   'whether the TRUNCATION_SHAPE_RESIDUAL flag applies to an alternative\'s rows (P10 for the twin)' % a['name'],
                   ['flags apply (Q25 flagged)', 'no flags for alternatives'])
        res = classify_member(tw['rows'], None, None, sub_ctx, ev, a['name'] + ' twin', late_assumption,
                              provisional=provisional, with_readings=False)
        rec['twin'] = {'member_id': tw['member_id'], 'log_index': tw['log_index'],
                       'patterns_holding': res['patterns_holding'], 'zones': res['zones'],
                       'outer_failure_defs': [res['outer_failure_def_miss_dominated'], res['outer_failure_def_P1_P2_P11']]}
        rec['_rows'] = res['rows']
        if a['name'] == 'STAGE0_GRID_OUTER':
            stage0_twin_rows = res['rows']
        alts[a['name']] = rec
    # PRIMARY: first pass to get rows for the DT-S0G comparison
    prim = classify_member(ref['rows'], score['pointwise_envelope']['rows'], score['sensitivity']['rows'], ctx, ev,
                           'PRIMARY', late_assumption, s0g=None, provisional=provisional, with_readings=False)
    s0g_detail = None
    if stage0_twin_rows is not None:
        s0g_detail = dt_s0g(prim['rows'], stage0_twin_rows)
        s0g = s0g_detail['outcome']
    prim = classify_member(ref['rows'], score['pointwise_envelope']['rows'], score['sensitivity']['rows'], ctx, ev,
                           'PRIMARY', late_assumption, s0g=s0g, provisional=provisional, with_readings=True)
    for a in alts.values():
        a.pop('_rows', None)
    if provisional:
        ev.add('AMBIGUITY', 'C-I7 / C-5.3', 'FREEZE_INCOMPLETE: every pattern and reading carries PROVISIONAL, but the E3 '
               'verdict line (C-5.3) is neither; whether TESTED-NEGATIVE prints with PROVISIONAL is unstated',
               ['E3 line labelled PROVISIONAL', 'E3 line unlabelled'])
    p8 = None
    if prim['patterns']['P8']:
        ok = alts.get('ORIGINAL_K', {})
        p8 = {'ORIGINAL_K_twin_OUTER': (ok.get('twin', {}).get('zones', {}).get('OUTER') if 'twin' in ok
                                        else ok.get('reading', 'NOT_AVAILABLE')),
              'T120L_C3_record': 'PINNED' if ctx.get('c3_record_pinned') else 'NOT_AVAILABLE'}
    return {'status': 'CLASSIFIED', 'provisional': provisional, 'primary': prim,
            'e3': prim['e3_by_definition'], 'alternatives': alts, 'dt_s0g': s0g_detail if s0g_detail else s0g,
            'p8_report': p8, 'events': ev.items}
