# R2-A closure lens: an independent implementation of round-2 PREREG [C-1.1]/[C-2]/[C-4]/[C-5.3], written from the round-2 text only,
# run on SYNTHETIC rows (dimensionless r values; 'U' = a non-INVALID MISS with UNDEFINED sign, i.e. a null sigma_ratio row or a
# LATE-gate row; 'I' = an INVALID row). No target, no project data. Output: exclusive create.
import json, statistics, sys

ZONES = ('INNER', 'TRANSITION', 'OUTER')
NZ = {'INNER': 24, 'TRANSITION': 11, 'OUTER': 8}

def tier(x):
    if x == 'I': return 'INVALID'
    if x == 'U': return 'MISS'
    return 'HIT' if abs(x) <= 1 else 'MISS'

def summ(rows):
    nv = [x for x in rows if x != 'I']
    H = sum(1 for x in nv if tier(x) == 'HIT'); M = sum(1 for x in nv if tier(x) == 'MISS')
    defined = [x for x in nv if x != 'U']
    m = statistics.median(defined) if defined else None
    S = None if m is None else ('DEFICIT' if m < -1 else 'EXCESS' if m > 1 else 'CENTERED')
    Nv = len(nv)
    return {'Nv': Nv, 'H': H, 'M': M, 'I': sum(1 for x in rows if x == 'I'), 'm': m, 'S': S,
            'miss_dom': Nv >= 1 and M >= Nv / 2, 'hit_dom': Nv >= 1 and H > Nv / 2}

def patterns(z):
    s = {k: summ(v) for k, v in z.items()}
    o, i, t = s['OUTER'], s['INNER'], s['TRANSITION']
    P = []
    if any(s[k]['I'] > 0 for k in ZONES): P.append('P0')
    if o['miss_dom'] and o['S'] == 'DEFICIT': P.append('P1')
    if o['miss_dom'] and o['S'] == 'EXCESS': P.append('P2')
    if o['miss_dom'] and o['S'] == 'CENTERED': P.append('P11')
    if i['miss_dom'] and i['S'] == 'EXCESS': P.append('P3')
    if i['miss_dom'] and i['S'] == 'DEFICIT': P.append('P4')
    if i['miss_dom'] and i['S'] == 'CENTERED': P.append('P12')
    if t['miss_dom']: P.append('P13')
    if i['hit_dom'] and o['miss_dom'] and t['Nv'] >= 1 and not t['hit_dom']: P.append('P5')
    if all(s[k]['Nv'] >= 1 for k in ZONES) and i['S'] is not None and i['S'] == t['S'] == o['S'] != 'CENTERED': P.append('P6')
    anymiss = any(s[k]['M'] > 0 for k in ZONES)
    if anymiss and not any(s[k]['miss_dom'] for k in ZONES): P.append('P7')
    if sum(s[k]['Nv'] for k in ZONES) >= 1 and sum(s[k]['M'] for k in ZONES) == 0: P.append('P8')
    if o['Nv'] == 0: P.append('P9')
    of_def1 = o['miss_dom']                                   # "OUTER is miss-dominated, whatever its sign class"
    of_def2 = any(p in P for p in ('P1', 'P2', 'P11'))         # "It holds exactly when one of P1, P2 or P11 holds"
    covered = (not anymiss) or any(p in P for p in ('P1', 'P2', 'P11', 'P3', 'P4', 'P12', 'P13', 'P7'))
    def e3(of):
        if o['Nv'] == 0: return 'NOT_TESTABLE'
        return 'TESTED-NEGATIVE' if of else 'NOT_NEGATIVE_AT_OUTER'
    return {'patterns': P, 'OUTER_FAILURE_def1_missdom': of_def1, 'OUTER_FAILURE_def2_P1P2P11': of_def2,
            'E3_line_under_def1': e3(of_def1), 'E3_line_under_def2': e3(of_def2),
            'coverage_property_holds': covered, 'summaries': s}

def zones(inner, trans, outer):
    assert len(inner) == 24 and len(trans) == 11 and len(outer) == 8
    return {'INNER': inner, 'TRANSITION': trans, 'OUTER': outer}

HITS = lambda n: [0.2] * n
cases = {
 # U1: every non-INVALID OUTER row has an undefined sign (null ratio, or LATE-gate rows counted as MISS with sign UNDEFINED)
 'U1_outer_all_undefined_sign': zones(['I', 'I'] + HITS(22), HITS(11), ['U'] * 8),
 # U2: INNER-only, all non-INVALID INNER rows undefined sign
 'U2_inner_all_undefined_sign': zones(['I', 'I'] + ['U'] * 22, HITS(11), HITS(8)),
 # U3 control: OUTER 5 undefined + 3 hits -> P11 (consistent)
 'U3_control_outer_5U_3hit': zones(['I', 'I'] + HITS(22), HITS(11), ['U'] * 5 + HITS(3)),
 # L1/L2: the same producer-INVALID INNER rows read with an on-time gate (INVALID) versus a LATE gate (MISS, sign UNDEFINED)
 'L1_inner_12_gate_rows_on_time_INVALID': zones(['I', 'I'] + ['I'] * 12 + HITS(10), [1.5] * 6 + HITS(5), [-3] * 8),
 'L2_inner_12_gate_rows_LATE_as_MISS': zones(['I', 'I'] + ['U'] * 12 + HITS(10), [1.5] * 6 + HITS(5), [-3] * 8),
 # L3/L4: P8 removed by a late gate (all valid rows hit; 3 producer-INVALID OUTER rows gated)
 'L3_outer_3_gate_rows_on_time_INVALID': zones(['I', 'I'] + HITS(22), HITS(11), ['I'] * 3 + HITS(5)),
 'L4_outer_3_gate_rows_LATE_as_MISS': zones(['I', 'I'] + HITS(22), HITS(11), ['U'] * 3 + HITS(5)),
}
out = {k: patterns(v) for k, v in cases.items()}
for k, v in out.items():
    print('%-42s %-28s OF1=%-5s OF2=%-5s E3(def1)=%-22s E3(def2)=%-22s coverage=%s' % (
        k, ','.join(v['patterns']), v['OUTER_FAILURE_def1_missdom'], v['OUTER_FAILURE_def2_P1P2P11'],
        v['E3_line_under_def1'], v['E3_line_under_def2'], v['coverage_property_holds']))
with open(sys.argv[1], 'x') as f:
    f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
