"""verify_consistency_1: independent re-derivation of the r2 section-2 pattern rules for finding L-C01.

Object: PREREG_MISS_READING_R2.md, sha256 6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143.
Written from the r2 text only (L134-L161 for section 2; L79-L82 for the tiers; L195-L207 for the R-MF rows).
It does not import or read the Lens C tools.

Synthetic data only. Each row is given a synthetic sigma ratio r and, optionally, a synthetic NEAR flag
(standing in for band_overlaps_error_bar). No file is read. No NGC3198 target, observed velocity or radius
value is used: only the ORDER of the OUTER rows by radius matters here (for the outer trend), and the r2
membership table (L110-L114) gives Q36..Q43 in ascending radius, so synthetic ascending radii are used.

Usage: python3 -I -B vc1_patterns.py OUT_JSON   (OUT_JSON is created exclusively; it must not exist)
"""
import itertools
import json
import sys

QIDS = ['Q%02d' % i for i in range(1, 44)]
ZONE = {q: ('INNER' if i <= 24 else 'TRANSITION' if i <= 35 else 'OUTER')
        for i, q in ((int(q[1:]), q) for q in QIDS)}            # r2 L110-L114
RSYN = {q: float(i) for i, q in enumerate(QIDS, start=1)}         # synthetic, ascending: order only
INVALID_DEFAULT = {'Q01', 'Q02'}                                  # r2 L222 (QUERY_INSIDE_INNERMOST_NODE)
OUTER_IDS = [q for q in QIDS if ZONE[q] == 'OUTER']
UND = 'UNDEFINED'


def tier(q, r, near, invalid):                                    # r2 L79-L82, in order
    if q in invalid:
        return 'INVALID'
    if abs(r) <= 1.0:
        return 'HIT'
    if near:
        return 'NEAR'
    return 'MISS'


def median(xs):                                                   # r2 L136
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return UND
    return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def sclass(m):                                                    # r2 L137
    if m == UND:
        return UND
    return 'DEFICIT' if m < -1.0 else ('EXCESS' if m > 1.0 else 'CENTERED')


def classify(rvals, near=(), invalid=INVALID_DEFAULT, flagged=()):
    rows = []
    for q in QIDS:
        t = tier(q, rvals[q], q in near, invalid)
        rows.append({'q': q, 'zone': ZONE[q], 'tier': t, 'r': (None if t == 'INVALID' else rvals[q])})
    S = {}
    for Z in ('INNER', 'TRANSITION', 'OUTER'):
        zr = [x for x in rows if x['zone'] == Z]
        v = [x for x in zr if x['tier'] != 'INVALID']
        nv = len(v)
        H = sum(x['tier'] == 'HIT' for x in v)
        N = sum(x['tier'] == 'NEAR' for x in v)
        M = sum(x['tier'] == 'MISS' for x in v)
        m = median([x['r'] for x in v])
        S[Z] = {'N_v': nv, 'H': H, 'N': N, 'M': M, 'I': len(zr) - nv, 'm': m, 'S': sclass(m),
                'miss_dom': nv >= 1 and M >= nv / 2.0,            # r2 L138
                'hit_dom': nv >= 1 and H >= nv / 2.0}             # r2 L139
    vo = sorted([x for x in rows if x['zone'] == 'OUTER' and x['tier'] != 'INVALID'], key=lambda x: RSYN[x['q']])
    if len(vo) < 2:
        dout = UND
    else:
        k = len(vo) // 2                                          # odd count: middle row to the far half (L143)
        dout = median([x['r'] for x in vo[k:]]) - median([x['r'] for x in vo[:k]])
    mT, mO = S['TRANSITION']['m'], S['OUTER']['m']
    growing = (S['OUTER']['S'] == 'DEFICIT' and dout != UND and dout < 0
               and mT != UND and mO != UND and mT > mO)           # r2 L145
    Mtot = sum(S[Z]['M'] for Z in S)
    P = {
        'P0': any(S[Z]['I'] > 0 for Z in S),
        'P1': S['OUTER']['miss_dom'] and S['OUTER']['S'] == 'DEFICIT',
        'P2': S['OUTER']['miss_dom'] and S['OUTER']['S'] == 'EXCESS',
        'P3': S['INNER']['miss_dom'] and S['INNER']['S'] == 'EXCESS',
        'P4': S['INNER']['miss_dom'] and S['INNER']['S'] == 'DEFICIT',
        'P5': (S['INNER']['hit_dom'] and S['OUTER']['miss_dom'] and S['TRANSITION']['N_v'] >= 1
               and not S['TRANSITION']['hit_dom']),
        'P6': (all(S[Z]['N_v'] >= 1 for Z in S) and S['INNER']['S'] == S['TRANSITION']['S'] == S['OUTER']['S']
               and S['OUTER']['S'] not in ('CENTERED', UND)),
        'P7': Mtot >= 1 and not any(S[Z]['miss_dom'] for Z in S),
        'P8': Mtot == 0,
        'P9': S['OUTER']['N_v'] == 0,
        'P10': any(x['tier'] == 'MISS' and x['q'] in flagged for x in rows),
    }
    P['P1g'] = P['P1'] and growing
    holds = [p for p in ('P0', 'P1', 'P1g', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10') if P[p]]
    # Verdict triggers, each read literally from its own clause.
    out_fail_miss = sum(1 for x in rows if x['zone'] == 'OUTER' and x['tier'] == 'MISS')
    out_fail_ref = sum(1 for x in rows if x['zone'] == 'OUTER' and x['tier'] in ('MISS', 'NEAR'))
    verdict = {
        # C-3.2 L195: "If P1 holds, this is TESTED-NEGATIVE for exactly this scope."
        'TN_explicit_C32': P['P1'],
        # C-P L17 / A15 E3: "an outer-row failure is TESTED-NEGATIVE", literal reading "at least one failing row".
        # Two literal variants: the reading tier MISS, or the reference member's LADDER failure (MISS or NEAR;
        # r2 L86: "A NEAR row's LADDER tier stays MISS_WORST_TIER").
        'TN_CP_literal_any_MISS': out_fail_miss >= 1,
        'TN_CP_literal_any_ref_failure': out_fail_ref >= 1,
        # Lens fix: "TESTED-NEGATIVE iff OUTER is miss-dominated (N_v(OUTER) >= 1)".
        'TN_fix_miss_dominated': S['OUTER']['miss_dom'],
        # Variant counting the reference member's NEAR rows as failures (not part of the lens fix).
        'TN_fix_variant_nonhit_dominated': (S['OUTER']['N_v'] >= 1
                                            and (S['OUTER']['M'] + S['OUTER']['N']) >= S['OUTER']['N_v'] / 2.0),
    }
    # The R-MF rows reported (C-8 items 4-5: readings only for patterns that hold).
    rmf_rows = [p for p in ('P1', 'P2', 'P6', 'P7') if P[p]]
    # P1-row against-column: "no P1 with N_v(OUTER) >= 1"; and the lens fix's replacement,
    # "OUTER not miss-dominated, with N_v(OUTER) >= 1", both evaluated only where the P1 row is reported.
    against = {
        'current_P1row_against_true_while_P1_reported': P['P1'] and (not P['P1']) and S['OUTER']['N_v'] >= 1,
        'fix_P1row_against_true_while_P1_reported': P['P1'] and (not S['OUTER']['miss_dom']) and S['OUTER']['N_v'] >= 1,
    }
    gap_outer = S['OUTER']['miss_dom'] and not (P['P1'] or P['P2'] or P['P5'] or P['P6'])
    return {'summaries': S, 'delta_out': dout, 'patterns': holds, 'verdict': verdict, 'R_MF_rows_reported': rmf_rows,
            'against': against, 'outer_miss_dominated_but_no_outer_pattern': gap_outer}


def base(inner=0.3, trans=0.3):
    return {q: (inner if ZONE[q] == 'INNER' else trans if ZONE[q] == 'TRANSITION' else 0.3) for q in QIDS}


def with_outer(d, vals):
    d = dict(d)
    for q, v in zip(OUTER_IDS, vals):
        d[q] = v
    return d


def main(out_path):
    cases = {}
    # V1: replica of Lens C C08 (alternating signs, all eight OUTER rows MISS).
    cases['V1_C08_replica_alternating'] = classify(with_outer(base(), [-3.0, 3.0, -2.5, 2.5, -2.0, 2.0, -1.5, 1.5]))
    # V2: a model curve that falls through a flat target inside the OUTER zone (excess near, deficit far), the
    #     E2-shaped outcome; 6/8 OUTER MISS; INNER and TRANSITION all HIT.
    cases['V2_falling_crossing_inside_OUTER'] = classify(
        with_outer(base(), [3.0, 2.0, 1.5, 0.5, -0.5, -1.5, -2.0, -3.0]))
    # V3: as V2, but TRANSITION has 5 HIT and 6 MISS (excess) rows (not hit-dominated), so P5 holds.
    t = base()
    for i, q in enumerate([q for q in QIDS if ZONE[q] == 'TRANSITION']):
        t[q] = 1.6 if i >= 5 else 0.3
    cases['V3_crossing_with_P5'] = classify(with_outer(t, [3.0, 2.0, 1.5, 0.5, -0.5, -1.5, -2.0, -3.0]))
    # V4: replica of Lens C C12 (OUTER excess, P2).
    cases['V4_C12_replica_P2'] = classify(with_outer(base(), [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]))
    # V5: two OUTER deficits of eight (not miss-dominated): literal C-P vs C-3.2 vs the fix.
    cases['V5_two_outer_misses'] = classify(with_outer(base(), [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, -3.0, -3.5]))
    # V6: NEAR dilution: OUTER 3 MISS, 2 NEAR, 3 HIT (the reference member fails 5/8 OUTER rows).
    v6 = with_outer(base(), [0.3, 0.3, 0.3, -2.5, -2.5, -3.0, -3.5, -4.0])
    cases['V6_near_dilution'] = classify(v6, near={'Q39', 'Q40'})
    # V7: the expected P1/P1g outcome; the P1-row against-columns (current and fix) are false.
    v7 = base(trans=0.5)
    for q in ('Q33', 'Q34', 'Q35'):
        v7[q] = -1.5
    cases['V7_P1_P1g'] = classify(with_outer(v7, [-2.0, -2.5, -3.0, -3.5, -4.0, -4.5, -5.0, -5.5]))

    # Enumeration: every OUTER vector over a six-value synthetic grid, INNER and TRANSITION all HIT.
    grid = (-3.0, -2.0, -0.5, 0.5, 2.0, 3.0)
    tally = {'n': 0, 'outer_miss_dominated': 0, 'P1': 0, 'P2': 0, 'CENTERED_miss_dominated_gap': 0,
             'gap_with_all_8_MISS': 0, 'P7': 0, 'P1row_against_reachable_current': 0,
             'P1row_against_reachable_fix': 0, 'P2_and_TN_explicit_C32': 0}
    b = base()
    for vals in itertools.product(grid, repeat=8):
        res = classify(with_outer(b, vals))
        tally['n'] += 1
        S = res['summaries']['OUTER']
        if S['miss_dom']:
            tally['outer_miss_dominated'] += 1
        if 'P1' in res['patterns']:
            tally['P1'] += 1
        if 'P2' in res['patterns']:
            tally['P2'] += 1
            if res['verdict']['TN_explicit_C32']:
                tally['P2_and_TN_explicit_C32'] += 1
        if res['outer_miss_dominated_but_no_outer_pattern']:
            tally['CENTERED_miss_dominated_gap'] += 1
            if S['M'] == 8:
                tally['gap_with_all_8_MISS'] += 1
        if 'P7' in res['patterns']:
            tally['P7'] += 1
        if res['against']['current_P1row_against_true_while_P1_reported']:
            tally['P1row_against_reachable_current'] += 1
        if res['against']['fix_P1row_against_true_while_P1_reported']:
            tally['P1row_against_reachable_fix'] += 1

    out = {'object_sha256': '6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143',
           'synthetic_only': True, 'cases': cases,
           'enumeration': {'grid': list(grid), 'inner_transition': 'all r = 0.3 (HIT)', 'tally': tally}}
    with open(out_path, 'x') as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
    for k, v in cases.items():
        print(k, 'patterns=', v['patterns'], 'S(OUTER)=', v['summaries']['OUTER']['S'],
              'M/N/H/N_v=', (v['summaries']['OUTER']['M'], v['summaries']['OUTER']['N'],
                             v['summaries']['OUTER']['H'], v['summaries']['OUTER']['N_v']),
              'delta_out=', v['delta_out'], 'verdict=', v['verdict'], 'R-MF rows=', v['R_MF_rows_reported'],
              'gap=', v['outer_miss_dominated_but_no_outer_pattern'])
    print('ENUMERATION', json.dumps(tally))


if __name__ == '__main__':
    main(sys.argv[1])
