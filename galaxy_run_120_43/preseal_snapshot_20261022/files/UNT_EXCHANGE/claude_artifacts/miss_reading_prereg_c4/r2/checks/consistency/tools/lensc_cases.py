"""Lens C case driver: synthetic score outputs (v003g format) through the independent r2 classifier.

Writes CASES_RESULTS.json (exclusive create) in the lens folder. Synthetic data only; no target is read.
Each case states what the r2 text makes the answer, and which AMBIGUITY / CONFLICT / GAP events must fire.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lensc_classifier as C   # noqa: E402
import lensc_synth as Y        # noqa: E402

Q = Y.QIDS
INNER = Q[2:24]          # Q03-Q24 (Q01/Q02 INVALID by default)
TRANS = Q[24:35]         # Q25-Q35
OUTER = Q[35:43]         # Q36-Q43


def rm(inner=0.3, trans=0.3, outer=0.3, **over):
    d = {}
    for q in Q:
        d[q] = inner if q in Q[:24] else trans if q in TRANS else outer
    for k, v in over.items():
        d['NGC3198-' + k] = v
    return d


def with_outer(base, vals):
    d = dict(base)
    for q, v in zip(OUTER, vals):
        d[q] = v
    return d


def flags(radii, lo, hi):
    """M-7 recommended rule: q flagged iff r_lo <= R_q <= r_hi (closed), synthetic ring ordinal 15."""
    return [{'query_id': q, 'ordinal': 15, 'support_kpc': [lo, hi], 'S_over_theta': 1.0148}
            for q in Q if lo <= radii[q] <= hi]


RADII, _ = Y.load_radii()
DEF_OUT = [-2.0, -2.5, -3.0, -3.5, -4.0, -4.5, -5.0, -5.5]
CASES = []


def case(name, spec, *, expect, events=(), no_events=(), radii=None, flag=None, auth=False, post=None):
    CASES.append({'name': name, 'spec': spec, 'expect': expect, 'events': list(events), 'no_events': list(no_events),
                  'radii': radii, 'flag': flag, 'auth': auth, 'post': post})


# 1 baseline expected outcome (A15 E2): P1 with growing deficit
base_r = with_outer(rm(trans=0.5, Q33=-1.5, Q34=-1.5, Q35=-1.5), DEF_OUT)
case('C01_baseline_P1_P1g', {'ref_r': base_r},
     expect={'patterns_eq': ['P0', 'P1', 'P1g'], 'sum': {'OUTER': {'m': -3.75, 'S': 'DEFICIT', 'M': 8}},
             'trend_delta': -2.0, 'tested_negative': True},
     events=[('AMBIGUITY', 'C-3/C-8', 'R-UT1'), ('AMBIGUITY', 'C-3/C-8', 'R-HIST')],
     flag=(10.04, 11.04))
# 2 odd count in OUTER (one gate-INVALID row): median and half split
case('C02_odd_outer_trend', {'ref_r': with_outer(base_r, [None, -2.5, -3.0, -3.5, -4.0, -4.5, -5.0, -5.5]),
                              'invalid': {'NGC3198-Q36': 'ROOT_GATE_X'}},
     expect={'patterns_eq': ['P0', 'P1', 'P1g'], 'sum': {'OUTER': {'m': -4.0, 'N_v': 7, 'I': 1}}, 'trend_delta': -1.75,
             'invalid_reason': {'NGC3198-Q36': 'ROOT_GATE_X'}})
# 3 every OUTER row INVALID (outer cut) -> P9
case('C03_all_outer_invalid_P9', {'ref_r': base_r, 'invalid': {q: 'QUERY_BEYOND_OUTER_GAS_CUT' for q in OUTER}},
     expect={'patterns_eq': ['P0', 'P7', 'P9'], 'sum': {'OUTER': {'N_v': 0, 'm': 'UNDEFINED', 'S': 'UNDEFINED'}},
             'growing_reported': 'UNDEFINED'})
# 4 every TRANSITION row INVALID (gate): m(TRANSITION) undefined while P1g is evaluated
case('C04_transition_all_invalid', {'ref_r': with_outer(rm(), DEF_OUT), 'invalid': {q: 'ROOT_GATE_T' for q in TRANS}},
     expect={'patterns_eq': ['P0', 'P1'], 'growing_reported': 'UNDEFINED', 'sum': {'TRANSITION': {'N_v': 0}}})
# 5 zero residual
case('C05_zero_residual', {'ref_r': rm(Q10=0.0)}, expect={'tier': {'NGC3198-Q10': 'HIT'}, 'sign': {'NGC3198-Q10': 0},
                                                           'patterns_eq': ['P0', 'P8']})
# 6 NEAR rows: Q40 straddle (no member within), Q41 a member within
r6 = rm(Q40=-2.0, Q41=-2.0)
o6 = [dict(r6, **{'NGC3198-Q40': -2.3, 'NGC3198-Q41': -0.5}), dict(r6, **{'NGC3198-Q40': 2.0, 'NGC3198-Q41': -2.2}),
      dict(r6, **{'NGC3198-Q40': 2.4, 'NGC3198-Q41': -2.1})]
case('C06_near_straddle', {'ref_r': r6, 'others': o6},
     expect={'tier': {'NGC3198-Q40': 'NEAR', 'NGC3198-Q41': 'NEAR'}, 'sum': {'OUTER': {'N': 2, 'M': 0}},
             'patterns_eq': ['P0', 'P8']},
     events=[('CONFLICT', 'C-1.1 / M-1', 'NGC3198-Q40')], no_events=[('CONFLICT', 'C-1.1 / M-1', 'NGC3198-Q41')])
# 7 sensitivity band overlaps where the envelope does not
r7 = rm(Q42=-3.0)
case('C07_sensitivity_only_overlap', {'ref_r': r7, 'others': [dict(r7, **{'NGC3198-Q42': v}) for v in (-3.2, -2.8, -3.1)],
                                      'sens': {'NGC3198-Q42': (-3.5, -0.5)}},
     expect={'tier': {'NGC3198-Q42': 'MISS'}, 'patterns_eq': ['P0', 'P7']},
     events=[('AMBIGUITY', 'C-1.1 vs C-8', None)])
# 8 OUTER all MISS with mixed signs: CENTERED -> no pattern, no R-MF verdict
case('C08_outer_mixed_centered', {'ref_r': with_outer(rm(), [-3.0, 3.0, -2.5, 2.5, -2.0, 2.0, -1.5, 1.5]),
                                  'others': [with_outer(rm(), [-3.0, 3.0, -2.5, 2.5, -2.0, 2.0, -1.5, 1.5])] * 3},
     expect={'patterns_eq': ['P0'], 'sum': {'OUTER': {'M': 8, 'S': 'CENTERED', 'm': 0.0}}},
     events=[('GAP', 'C-2', 'OUTER'), ('CONFLICT', 'C-P vs C-3.2', None)])
# 9 TRANSITION-only miss dominance -> no pattern
case('C09_transition_only_misses', {'ref_r': rm(trans=-2.0), 'others': [rm(trans=-2.0)] * 3},
     expect={'patterns_eq': ['P0'], 'sum': {'TRANSITION': {'M': 11, 'S': 'DEFICIT'}}},
     events=[('GAP', 'C-2', 'TRANSITION')])
# 10 exact half: OUTER 4 HIT + 4 MISS -> both hit- and miss-dominated; P1 (TESTED-NEGATIVE) with 4/8 hits
r10 = with_outer(rm(), [0.2, 0.2, 0.2, 0.2, -3.0, -4.0, -5.0, -6.0])
case('C10_exact_half_tie', {'ref_r': r10, 'others': [r10] * 3},
     expect={'patterns_inc': ['P1'], 'sum': {'OUTER': {'H': 4, 'M': 4, 'miss_dominated': True, 'hit_dominated': True,
                                                      'm': -1.4}}, 'tested_negative': True},
     events=[('CONFLICT', 'C-2/M-3', 'OUTER')])
# 11 INNER split 11/11 with median > 1: P3 and P5 together
inner11 = {q: (0.99 if i % 2 == 0 else 1.2) for i, q in enumerate(INNER)}
r11 = with_outer(rm(trans=-1.5), DEF_OUT)
r11.update(inner11)
case('C11_P3_and_P5', {'ref_r': r11, 'others': [r11] * 3},
     expect={'patterns_inc': ['P1', 'P3', 'P5'], 'sum': {'INNER': {'S': 'EXCESS', 'H': 11, 'M': 11}}},
     events=[('CONFLICT', 'C-2/C-3.2', None), ('CONFLICT', 'C-2/M-3', 'INNER')])
# 12 OUTER excess: P2
r12 = with_outer(rm(), [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5])
case('C12_P2_outer_excess', {'ref_r': r12, 'others': [r12] * 3},
     expect={'patterns_eq': ['P0', 'P2'], 'tested_negative': False},
     events=[('CONFLICT', 'C-P vs C-3.2', None), ('CONFLICT', 'C-3.2', None), ('AMBIGUITY', 'C-3.2', 'R-GRID'),
             ('CONFLICT', 'C-I6 vs C-3.2', None)])
# 13 OUTER clean, a few INNER misses: P8 global differs from OUTER no-miss
r13 = rm(Q05=-2.0, Q06=-2.0, Q07=-2.0)
case('C13_P8_global_vs_outer', {'ref_r': r13, 'others': [r13] * 3},
     expect={'patterns_eq': ['P0', 'P7']}, events=[('AMBIGUITY', 'C-5.2', None), ('AMBIGUITY', 'C-3.2', None)])
# 14 FREEZE_INCOMPLETE, root authorizes, one PRIMARY member unevaluated -> every envelope row invalid
r14 = rm(Q40=-2.0)
o14 = [dict(r14, **{'NGC3198-Q40': 2.0})] * 3
case('C14_incomplete_uneval_member', {'ref_r': r14, 'others': o14, 'uneval_other': True,
                                      'freeze_status': 'FREEZE_INCOMPLETE',
                                      'incomplete_reasons': ['PRIMARY_MEMBER_EVALUATION_BUDGET_EXHAUSTED']},
     auth=True, expect={'tier': {'NGC3198-Q40': 'MISS'}, 'label_prefix': 'PROVISIONAL (FREEZE_INCOMPLETE)'},
     events=[('AMBIGUITY', 'C-1.1/C-I7', 'NGC3198-Q40')])
# 15 FREEZE_INCOMPLETE without authorization
case('C15_incomplete_unauthorized', {'ref_r': rm(), 'freeze_status': 'FREEZE_INCOMPLETE',
                                     'incomplete_reasons': ['SENSITIVITY_BUDGET_EXHAUSTED']},
     expect={'stop_contains': 'FREEZE_INCOMPLETE'})
# 16 flagged rows: hit, miss, INVALID
r16 = rm(Q26=-2.0)
case('C16_flagged_hit_miss_invalid', {'ref_r': r16, 'others': [r16] * 3, 'invalid': {'NGC3198-Q27': 'ROOT_GATE_F'}},
     flag=(10.04, 12.05),
     expect={'patterns_inc': ['P10'], 'tier': {'NGC3198-Q25': 'HIT', 'NGC3198-Q26': 'MISS',
                                               'NGC3198-Q27': 'INVALID_AS_MISS'}},
     events=[('CONFLICT', 'C-2 P10 / C-4', None), ('AMBIGUITY', 'C-3/C-8', 'R-TSR'), ('CONFLICT', 'C-1.1 vs C-4', 'Q27')])
# 17 ORIGINAL_K twin exists but is not valid (forward valid:false)
case('C17_originalk_twin_invalid', {'ref_r': base_r, 'alts': {'ORIGINAL_K': {'status': 'EVALUATED_BEFORE_FREEZE',
                                                                              'twin_forward_valid': False}}},
     expect={'alt_reading': {'ORIGINAL_K': 'NO_TWIN (twin member_valid false)'}},
     events=[('AMBIGUITY', 'C-6.1', 'ORIGINAL_K')])
# 18 ORIGINAL_K with no member at the reference log_index (unreachable under v003g D2)
case('C18_originalk_no_twin', {'ref_r': base_r, 'alts': {'ORIGINAL_K': {'status': 'EVALUATED_BEFORE_FREEZE',
                                                                         'log_indices': [6, 18, 24, 32]}}},
     expect={'alt_reading': {'ORIGINAL_K': 'NO_TWIN (no member at the reference log_index)'}})
# 19 ORIGINAL_K twin valid; flags present -> P10 applicability unstated
case('C19_originalk_twin_valid_flags', {'ref_r': base_r, 'alts': {'ORIGINAL_K': {'status': 'EVALUATED_BEFORE_FREEZE',
                                                                                  'twin_r': rm(trans=-2.0)}}},
     flag=(10.04, 11.04), expect={'alt_patterns_inc': {'ORIGINAL_K': ['P10']}},
     events=[('AMBIGUITY', 'C-1.4/C-6.1', 'ORIGINAL_K'), ('GAP', 'C-2', 'ORIGINAL_K TRANSITION')])
# 20-27 STAGE0_GRID_OUTER evaluated (through a hypothetical successor), comparison boundaries
pr = with_outer(rm(), [-3.0] * 8)


def s0(twin_outer, invalid=None, fv=True, prim=pr):
    return {'ref_r': prim, 'others': [prim] * 3,
            'alts': {'STAGE0_GRID_OUTER': {'status': 'EVALUATED_BEFORE_FREEZE', 'twin_r': with_outer(rm(), twin_outer),
                                           'invalid': invalid or {}, 'twin_forward_valid': fv}}}


case('C20_s0_consistent', s0([0.5] + [-3.0] * 7), expect={'s0': 'CONSISTENT', 's0_HP_HS': (0, 1)},
     events=[('CONFLICT', 'C-6.1 vs C-1.1', 'STAGE0_GRID_OUTER')])
case('C21_s0_against_equal_hits', s0([-2.0] * 8), expect={'s0': 'AGAINST', 's0_HP_HS': (0, 0)})
case('C22_s0_signflip_not_decided', s0([3.0] * 8), expect={'s0': 'NOT_DECIDED'})
case('C23_s0_fewer_hits_same_sign', s0([-3.0] * 8, prim=with_outer(rm(), [0.5] + [-3.0] * 7)),
     expect={'s0': 'AGAINST', 's0_HP_HS': (1, 0)})
case('C24_s0_no_joint_rows', s0([-3.0] * 8, invalid={q: 'QUERY_BEYOND_OUTER_GAS_CUT' for q in OUTER}),
     expect={'s0': 'NOT_DECIDED'}, events=[('GAP', 'C-2', 'STAGE0_GRID_OUTER')])
case('C25_s0_twin_invalid', s0([-3.0] * 8, fv=False), expect={'s0': 'NOT_DECIDED'},
     events=[('AMBIGUITY', 'C-6.3', None)])
case('C26_s0_not_evaluated', {'ref_r': pr, 'others': [pr] * 3}, expect={'s0': 'NOT_EVALUATED'})
# 27 DDO154 distance alternative appended by v003g in the fixed-distance mode
case('C27_seventh_alternative', {'ref_r': base_r, 'mode_d_fixed': True},
     expect={'patterns_inc': ['P1']}, events=[('AMBIGUITY', 'C-I4/C-6.2', 'DDO154_DISTANCE_NUISANCE')])
# 28 null sigma_ratio on a VALID row (v003g NON_FINITE_SIGMA_RATIO, finite sigma > 0)
case('C28_null_sigma_ratio', {'ref_r': rm(), 'sigma_override': {'NGC3198-Q30': 5e-324},
                              'abs_offset': {'NGC3198-Q30': 1.0}},
     expect={'sum': {'TRANSITION': {'m': 'UNDEFINED'}}},
     events=[('AMBIGUITY', 'C-1.1', 'PRIMARY NGC3198-Q30')])
# 29 zone table mismatch (synthetic radius moved)
rad29 = dict(RADII)
rad29['NGC3198-Q24'] = 10.5
case('C29_zone_mismatch', {'ref_r': rm()}, radii=rad29, expect={'stop_contains': 'ZONE_TABLE_MISMATCH'})


# 30 reference rows out of order; 31 a reference row UNEVALUATED_OR_REFUSED
def swap_rows(score):
    rows = score['members'][1]['rows']
    rows[3], rows[4] = rows[4], rows[3]


def uneval_row(score):
    score['members'][1]['rows'][10]['status'] = 'UNEVALUATED_OR_REFUSED'


case('C30_ids_out_of_order', {'ref_r': rm()}, post=swap_rows, expect={'stop_contains': 'not Q01-Q43 in order'})
case('C31_unevaluated_reference_row', {'ref_r': rm()}, post=uneval_row, expect={'stop_contains': 'UNEVALUATED_OR_REFUSED'})
# 32 global excess: P6 with P2 and P3
r32 = rm(inner=2.0, trans=2.0, outer=2.0)
case('C32_P6_global_excess', {'ref_r': r32, 'others': [r32] * 3}, expect={'patterns_inc': ['P2', 'P3', 'P6']})
# 33 scattered misses: P7
r33 = rm(Q05=-2.0, Q27=2.0, Q40=-2.0)
case('C33_P7_scattered', {'ref_r': r33, 'others': [r33] * 3}, expect={'patterns_eq': ['P0', 'P7']},
     events=[('AMBIGUITY', 'C-3.2', None)])
# 34 inner deficit: P4
r34 = rm(inner=-2.0)
case('C34_P4_inner_deficit', {'ref_r': r34, 'others': [r34] * 3}, expect={'patterns_inc': ['P4']},
     events=[('AMBIGUITY', 'C-3.2', 'R-ML')])
# 35 onset: P5 with P1
r35 = with_outer(rm(trans=0.3, Q30=-1.5, Q31=-1.5, Q32=-1.5, Q33=-1.5, Q34=-1.5, Q35=-1.5), DEF_OUT)
case('C35_P5_onset', {'ref_r': r35, 'others': [r35] * 3}, expect={'patterns_inc': ['P1', 'P5']},
     events=[('AMBIGUITY', 'C-3.2', 'P5-onset')])

# 36 one valid OUTER row (7 cut): P1 and R-MF TESTED-NEGATIVE rest on a single row
r36 = with_outer(rm(), [-3.0] + [None] * 7)
case('C36_single_outer_row_P1', {'ref_r': r36, 'others': [r36] * 3,
                                 'invalid': {q: 'QUERY_BEYOND_OUTER_GAS_CUT' for q in OUTER[1:]}},
     expect={'patterns_inc': ['P1'], 'sum': {'OUTER': {'N_v': 1, 'M': 1}}, 'tested_negative': True})
# 37 STAGE0 twin flips the deficit to an excess; one row crosses the error bar -> CONSISTENT
case('C37_s0_signflip_one_crossing', s0([0.5] + [3.0] * 7), expect={'s0': 'CONSISTENT', 's0_HP_HS': (0, 1)})
# 38 STAGE0 twin shrinks every deficit from -6 to -1.5 but gains no hit -> AGAINST
case('C38_s0_shrinking_deficit_against', s0([-1.5] * 8, prim=with_outer(rm(), [-6.0] * 8)),
     expect={'s0': 'AGAINST', 's0_HP_HS': (0, 0)})


def check(res, cs):
    fails = []
    ex = cs['expect']
    if 'stop_contains' in ex:
        if res.get('ok') or ex['stop_contains'] not in res.get('stop', ''):
            fails.append('expected stop containing %r, got %r' % (ex['stop_contains'], res.get('stop')))
        return fails
    if not res.get('ok'):
        return ['unexpected stop: %s' % res.get('stop')]
    pats = res['patterns']
    if 'patterns_eq' in ex and pats != ex['patterns_eq']:
        fails.append('patterns %s != %s' % (pats, ex['patterns_eq']))
    for p in ex.get('patterns_inc', []):
        if p not in pats:
            fails.append('pattern %s missing (have %s)' % (p, pats))
    for Z, kv in ex.get('sum', {}).items():
        for k, v in kv.items():
            got = res['summaries'][Z][k]
            if isinstance(v, float) and isinstance(got, float):
                ok = abs(got - v) < 1e-12
            else:
                ok = got == v
            if not ok:
                fails.append('%s.%s = %r, expected %r' % (Z, k, got, v))
    rows = {c['id']: c for c in res['rows']}
    for q, t in ex.get('tier', {}).items():
        if rows[q]['tier'] != t:
            fails.append('%s tier %s != %s' % (q, rows[q]['tier'], t))
    for q, sg in ex.get('sign', {}).items():
        if rows[q]['sign'] != sg:
            fails.append('%s sign %r != %r' % (q, rows[q]['sign'], sg))
    for q, rs in ex.get('invalid_reason', {}).items():
        if rows[q]['reason'] != rs:
            fails.append('%s reason %r != %r' % (q, rows[q]['reason'], rs))
    if 'trend_delta' in ex and abs(res['trend']['delta_out'] - ex['trend_delta']) > 1e-12:
        fails.append('delta_out %r != %r' % (res['trend']['delta_out'], ex['trend_delta']))
    if 'growing_reported' in ex and res['trend']['GROWING_reported_as'] != ex['growing_reported']:
        fails.append('GROWING reported %r' % res['trend']['GROWING_reported_as'])
    if 'tested_negative' in ex:
        tn = res['readings'].get('R-MF', {}).get('TESTED_NEGATIVE_per_C32', False)
        if tn != ex['tested_negative']:
            fails.append('R-MF TESTED-NEGATIVE %r != %r' % (tn, ex['tested_negative']))
    if 'label_prefix' in ex and not (res.get('label') or '').startswith(ex['label_prefix']):
        fails.append('label %r' % res.get('label'))
    alts = {a['name']: a for a in res['alternatives']}
    for nm, rd in ex.get('alt_reading', {}).items():
        if alts[nm].get('reading') != rd:
            fails.append('%s reading %r != %r' % (nm, alts[nm].get('reading'), rd))
    for nm, ps in ex.get('alt_patterns_inc', {}).items():
        for p in ps:
            if p not in alts[nm].get('patterns', []):
                fails.append('%s pattern %s missing (have %s)' % (nm, p, alts[nm].get('patterns')))
    if 's0' in ex and (res['stage0'] or {}).get('comparison') != ex['s0']:
        fails.append('stage0 %r != %r' % (res['stage0'], ex['s0']))
    if 's0_HP_HS' in ex and (res['stage0'].get('H_P'), res['stage0'].get('H_S')) != ex['s0_HP_HS']:
        fails.append('stage0 H_P/H_S %r' % ((res['stage0'].get('H_P'), res['stage0'].get('H_S')),))
    return fails


def has_event(res, kind, tag, detail_sub):
    for e in res['events']:
        if e['kind'] == kind and e['tag'] == tag:
            if detail_sub is None or detail_sub in json.dumps(e.get('detail')):
                return True
    return False


def run():
    results = []
    n_fail = 0
    for cs in CASES:
        score, radii = Y.build_score(copy.deepcopy(cs['spec']))
        if cs['post']:
            cs['post'](score)
        if cs['radii']:
            radii = cs['radii']
        fl = flags(radii, *cs['flag']) if cs['flag'] else []
        res = C.classify(score, radii, fl, root_authorizes_incomplete=cs['auth'])
        fails = check(res, cs)
        for kind, tag, sub in cs['events']:
            if not has_event(res, kind, tag, sub):
                fails.append('missing event %s %s %s' % (kind, tag, sub))
        for kind, tag, sub in cs['no_events']:
            if has_event(res, kind, tag, sub):
                fails.append('unexpected event %s %s %s' % (kind, tag, sub))
        n_fail += bool(fails)
        results.append({'case': cs['name'], 'pass': not fails, 'fails': fails,
                        'patterns': res.get('patterns'), 'stop': res.get('stop'),
                        'stage0': res.get('stage0'), 'label': res.get('label'),
                        'flagged': [f['query_id'] for f in fl],
                        'summaries': res.get('summaries'), 'trend': res.get('trend'),
                        'readings': res.get('readings'),
                        'alternatives': [{k: v for k, v in a.items() if k not in ('rows',)} for a in res.get('alternatives', [])],
                        'events': res['events']})
    return results, n_fail


if __name__ == '__main__':
    results, n_fail = run()
    summary = {'n_cases': len(results), 'n_fail': n_fail,
               'event_counts': {}}
    for r in results:
        for e in r['events']:
            k = '%s | %s' % (e['kind'], e['tag'])
            summary['event_counts'][k] = summary['event_counts'].get(k, 0) + 1
    for r in results:
        print('%-34s %s %s %s' % (r['case'], 'PASS' if r['pass'] else 'FAIL', r['patterns'] or r['stop'],
                                  '; '.join(r['fails'])))
    print(json.dumps(summary, indent=1))
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'x') as f:
            json.dump({'summary': summary, 'cases': results}, f, indent=1, default=str)
