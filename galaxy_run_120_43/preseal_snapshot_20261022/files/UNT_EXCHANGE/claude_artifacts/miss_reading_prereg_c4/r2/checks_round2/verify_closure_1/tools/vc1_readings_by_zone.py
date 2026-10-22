# verify_closure_1 (round 2): independent re-implementation, from PREREG_MISS_READING_R2.md 97d5ce33 text only, of
#   [C-1.1] tiers (L105-L119), [C-2] zone summaries and patterns (L187-L229), [C-3] scope rule (L249) and the
#   [C-3.2] reading table (L267-L290),
# to answer: for each synthetic outcome, which registered readings may cite OUTER rows, and are the binding
# A15 E3 / A12.3 readings 2-3 (R-REACH, R-HIST), the A20 readings (R-UT1, R-HIST) and an A10 history/species
# reading (R-HIST or R-SPEC) among them?
# Synthetic dimensionless sigma ratios only. Zone membership by index (INNER 24, TRANSITION 11, OUTER 8), as in [C-1.3].
# Q01, Q02 are INVALID (built-in QUERY_INSIDE_INNERMOST_NODE) in every case, as in [C-4]. No file other than --out is written.
import json, sys

INV = 'INV'          # INVALID_AS_MISS row
NEAR_NONE = None


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return None
    if n % 2:
        return xs[n // 2]
    return 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def zone_summary(rows):
    valid = [r for r in rows if r != INV]
    nv = len(valid)
    defined = [r for r in valid if r is not None]
    hit = sum(1 for r in defined if abs(r) <= 1.0)
    miss = nv - hit                      # NEAR rows stay MISS; a null ratio is a MISS (L119)
    m = median(defined)
    if m is None:
        s = 'UNDEFINED'
    elif m < -1:
        s = 'DEFICIT'
    elif m > 1:
        s = 'EXCESS'
    else:
        s = 'CENTERED'
    missdom = nv >= 1 and miss >= nv / 2.0
    hitdom = nv >= 1 and hit > nv / 2.0
    return dict(Nv=nv, H=hit, M=miss, I=len(rows) - nv, m=m, S=s, missdom=missdom, hitdom=hitdom)


def delta_out(outer):
    d = [r for r in outer if r != INV and r is not None]      # sorted by R: index order is radius order
    if len(d) < 2:
        return None
    k = len(d) // 2                                            # odd count: middle row goes to the far half
    near, far = d[:k], d[k:]
    return median(far) - median(near)


def patterns(inner, trans, outer):
    zi, zt, zo = zone_summary(inner), zone_summary(trans), zone_summary(outer)
    allrows = inner + trans + outer
    nmiss = zi['M'] + zt['M'] + zo['M']
    dout = delta_out(outer)
    growing = (zo['S'] == 'DEFICIT' and dout is not None and dout < 0 and zt['m'] is not None and zo['m'] is not None
               and zt['m'] > zo['m'])
    P = []
    if zi['I'] + zt['I'] + zo['I'] > 0:
        P.append('P0')
    if zo['missdom'] and zo['S'] == 'DEFICIT':
        P.append('P1')
        if growing:
            P.append('P1g')
    if zo['missdom'] and zo['S'] == 'EXCESS':
        P.append('P2')
    if zo['missdom'] and zo['S'] == 'CENTERED':
        P.append('P11')
    if zi['missdom'] and zi['S'] == 'EXCESS':
        P.append('P3')
    if zi['missdom'] and zi['S'] == 'DEFICIT':
        P.append('P4')
    if zi['missdom'] and zi['S'] == 'CENTERED':
        P.append('P12')
    if zt['missdom']:
        P.append('P13')
    if zi['hitdom'] and zo['missdom'] and zt['Nv'] >= 1 and not zt['hitdom']:
        P.append('P5')
    if (zi['Nv'] >= 1 and zt['Nv'] >= 1 and zo['Nv'] >= 1 and zi['S'] == zt['S'] == zo['S']
            and zi['S'] in ('DEFICIT', 'EXCESS')):
        P.append('P6')
    if nmiss >= 1 and not (zi['missdom'] or zt['missdom'] or zo['missdom']):
        P.append('P7')
    if (zi['Nv'] + zt['Nv'] + zo['Nv']) >= 1 and nmiss == 0:
        P.append('P8')
    if zo['Nv'] == 0:
        P.append('P9')
    outer_failure = zo['missdom']                               # [C-2] L209 first sentence
    e3 = 'NOT_TESTABLE' if zo['Nv'] == 0 else ('TESTED-NEGATIVE' if outer_failure else 'NOT_NEGATIVE_AT_OUTER')
    return P, dict(INNER=zi, TRANSITION=zt, OUTER=zo, delta_out=dout, GROWING=growing,
                   OUTER_FAILURE=outer_failure, E3_line=e3)


# [C-3.2] rows L271-L290: (patterns that trigger the row, reading, zones whose rows the reading may cite under [C-3] L249).
# P5 "as P1 for the OUTER rows (including R-DRIFT), and R-NAX for the transition zone" (L284).
# P6 "R-MF at all radii" and P7 "at row level": all zones. P13 R-NAX "for the transition zone". R-TSR: flagged rows only (none here).
TABLE = [
    (('P1', 'P1g', 'P2', 'P11'), 'R-MF', ('OUTER',)),
    (('P1', 'P1g'), 'R-UT1', ('OUTER',)),
    (('P1', 'P1g'), 'R-HIST', ('OUTER',)),
    (('P1', 'P1g'), 'R-REACH', ('OUTER',)),
    (('P1', 'P1g', 'P2', 'P11'), 'R-DRIFT', ('OUTER',)),
    (('P2', 'P11'), 'R-S1', ('OUTER',)),
    (('P2', 'P11'), 'R-GRID', ('OUTER',)),
    (('P11',), 'R-NAX', ('OUTER',)),
    (('P3', 'P4', 'P12'), 'R-GEFF', ('INNER',)),
    (('P3', 'P4', 'P12'), 'R-ML', ('INNER',)),
    (('P3', 'P4', 'P12'), 'R-SPEC', ('INNER',)),
    (('P3', 'P4', 'P12'), 'R-GEO', ('INNER',)),
    (('P6',), 'R-GEO', ('INNER', 'TRANSITION', 'OUTER')),
    (('P3', 'P4', 'P12'), 'R-NAX', ('INNER',)),
    (('P7',), 'R-NAX', ('INNER', 'TRANSITION', 'OUTER')),
    (('P13',), 'R-NAX', ('TRANSITION',)),
    (('P5',), 'R-MF', ('OUTER',)),
    (('P5',), 'R-UT1', ('OUTER',)),
    (('P5',), 'R-HIST', ('OUTER',)),
    (('P5',), 'R-REACH', ('OUTER',)),
    (('P5',), 'R-DRIFT', ('OUTER',)),
    (('P5',), 'R-NAX', ('TRANSITION',)),
    (('P6',), 'R-S1', ('INNER', 'TRANSITION', 'OUTER')),
    (('P6',), 'R-MF', ('INNER', 'TRANSITION', 'OUTER')),
    (('P7',), 'R-MF', ('INNER', 'TRANSITION', 'OUTER')),
]


def readings_citing(P, zone):
    out = {}
    for pats, rd, zones in TABLE:
        trig = [p for p in pats if p in P]
        if trig and zone in zones:
            out.setdefault(rd, set()).update(trig)
    return {k: sorted(v) for k, v in sorted(out.items())}


def case(inner_valid, trans, outer):
    inner = [INV, INV] + inner_valid
    assert len(inner) == 24 and len(trans) == 11 and len(outer) == 8
    return inner, trans, outer


HIT = 0.2
CASES = {
    'V1_P1_outer_deficit_control': case([HIT] * 22, [HIT] * 11, [-3, -2.5, -2, -3.5, -4, -2, 0.5, -3]),
    'V2_P2_outer_excess_alone': case([HIT] * 22, [HIT] * 11, [3, 2.5, 2, 3.5, 4, 2, 0.5, 3]),
    'V3_P11_E2_shaped_crossing': case([HIT] * 22, [HIT] * 11, [3, 2, 1.5, 0.5, -0.5, -1.5, -2, -3]),
    'V4_P11_alternating': case([HIT] * 22, [HIT] * 11, [-3, 3, -2.5, 2.5, -2, 2, -1.5, 1.5]),
    # same OUTER as V2/V3, but TRANSITION not hit-dominated (6 of 11 misses), so P5 holds: does the OUTER reading set change?
    'V5_P2_with_P5': case([HIT] * 22, [HIT] * 5 + [2, 2.5, 3, 2, 2.5, 3], [3, 2.5, 2, 3.5, 4, 2, 0.5, 3]),
    'V6_P11_crossing_with_P5': case([HIT] * 22, [HIT] * 5 + [2, 2.5, 3, 2, 2.5, 3], [3, 2, 1.5, 0.5, -0.5, -1.5, -2, -3]),
    # A10 "every miss read two ways" probes: TRANSITION-only failure (P13), scattered (P7), global offset (P6 with P2, P3, P13)
    'V7_P13_transition_only': case([HIT] * 22, [HIT] * 5 + [2, -2.5, 3, -2, 2.5, -3], [HIT] * 8),
    'V8_P7_scattered': case([HIT] * 18 + [2, -2, 3, -3], [HIT] * 9 + [2, -2], [HIT] * 6 + [-2, 2]),
    'V9_P6_global_excess': case([2.0] * 22, [2.0] * 11, [2.0] * 8),
}

E3_2_3 = ('R-REACH', 'R-HIST')
A20_2 = ('R-UT1', 'R-HIST')
HIST_ANY = ('R-HIST', 'R-SPEC')

res = {}
for name, (inner, trans, outer) in CASES.items():
    P, s = patterns(inner, trans, outer)
    per_zone = {z: readings_citing(P, z) for z in ('INNER', 'TRANSITION', 'OUTER')}
    zone_with_miss = [z for z, rows in (('INNER', inner), ('TRANSITION', trans), ('OUTER', outer))
                      if s[z]['M'] > 0]
    res[name] = {
        'patterns': P,
        'OUTER_FAILURE': s['OUTER_FAILURE'], 'E3_line': s['E3_line'],
        'S': {z: s[z]['S'] for z in ('INNER', 'TRANSITION', 'OUTER')},
        'M_of_Nv': {z: '%d/%d' % (s[z]['M'], s[z]['Nv']) for z in ('INNER', 'TRANSITION', 'OUTER')},
        'delta_out': s['delta_out'], 'GROWING': s['GROWING'],
        'readings_citing_zone': per_zone,
        'OUTER_has_E3_readings_2_3': {x: x in per_zone['OUTER'] for x in E3_2_3},
        'OUTER_has_A20_readings': {x: x in per_zone['OUTER'] for x in A20_2},
        'A10_two_way_per_zone_with_a_miss': {z: {'model_failure_R-MF': 'R-MF' in per_zone[z],
                                                 'history_or_species': any(h in per_zone[z] for h in HIST_ANY)}
                                             for z in zone_with_miss},
    }
    print('%-30s %-22s E3=%-22s OUTER cites=%s' % (name, ','.join(P), s['E3_line'], ','.join(per_zone['OUTER'])))
    print('    E3 2-3 on OUTER: %s   A20 on OUTER: %s   A10 per miss zone: %s' % (
        res[name]['OUTER_has_E3_readings_2_3'], res[name]['OUTER_has_A20_readings'],
        res[name]['A10_two_way_per_zone_with_a_miss']))

with open(sys.argv[1], 'x') as f:
    f.write(json.dumps(res, indent=1, sort_keys=True) + '\n')
