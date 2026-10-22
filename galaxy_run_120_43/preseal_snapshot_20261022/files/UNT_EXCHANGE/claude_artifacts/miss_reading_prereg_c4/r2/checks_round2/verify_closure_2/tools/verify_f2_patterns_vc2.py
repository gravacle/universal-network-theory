# verify_closure_2: an independent re-implementation of PREREG_MISS_READING_R2 (round 2, sha 97d5ce33...) [C-1.1] L109-L119,
# [C-1.2], [C-2] L189-L229, [C-3] L236-L250 (R-MF tuple and verdict), [C-4] L322-L325 (LATE gates) and [C-5.3] L357-L360,
# written from the round-2 text only (not from the closure lens's tool). SYNTHETIC rows only: dimensionless r values, row
# kinds, and synthetic radii R_q = q (manifest order is radius order). No target, no project data, no file read.
#
# Row kinds:  'B' built-in INVALID (QUERY_INSIDE_INNERMOST_NODE / cut / gap)     -> INVALID for patterns
#             'G' root-gate INVALID registered ON TIME (before any step-5 output) -> INVALID for patterns
#             'L' root-gate INVALID registered LATE ([C-4] L322-L324)            -> non-INVALID MISS, sign UNDEFINED
#             'N' VALID row with null sigma_ratio ([C-1.1] L119)                 -> non-INVALID MISS, sign UNDEFINED
#             float r: VALID row with sigma_ratio r: HIT iff |r| <= 1, else MISS
# Rules 'R2' = the round-2 text as written. Rules 'FIX' = the F2 fix, both halves together (counts-only OUTER_FAILURE plus
# P14 OUTER_UNSIGNED and P15 INNER_UNSIGNED), to test whether the fix closes the holes without new ones.
import json, statistics, sys
import numpy as np

OUT = sys.argv[1]

def _fence(event, args):
    # audit-hook fence: after setup, the only file this process may open is its own output, created exclusively.
    if event == 'open':
        path, mode = args[0], args[1]
        if not (isinstance(path, str) and path == OUT and isinstance(mode, str) and 'x' in mode):
            raise PermissionError('verify_closure_2 fence: refused open of %r mode %r' % (path, mode))
    if event in ('os.remove', 'os.rename', 'os.rmdir', 'os.mkdir', 'os.symlink', 'os.truncate', 'os.chmod',
                 'shutil.rmtree', 'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'socket.connect',
                 'os.listdir', 'os.scandir'):
        raise PermissionError('verify_closure_2 fence: refused %s' % event)

ZONE_OF = {}
for q in range(1, 44):
    ZONE_OF[q] = 'INNER' if q <= 24 else ('TRANSITION' if q <= 35 else 'OUTER')   # [C-1.3] membership table L153-L155
ZONES = ('INNER', 'TRANSITION', 'OUTER')
TSR_FLAGGED = {25}                                                                     # [C-1.4] L179: Q25 only

def row_view(kind):
    """(invalid_for_patterns, tier, r_defined) per [C-1.1], [C-4]."""
    if kind in ('B', 'G'):
        return True, 'INVALID', None
    if kind in ('L', 'N'):
        return False, 'MISS', None
    r = float(kind)
    return False, ('HIT' if abs(r) <= 1.0 else 'MISS'), r

def median_or_none(xs):
    return statistics.median(xs) if xs else None          # even count: mean of the two middle values ([C-2] L195)

def sign_class(m):
    if m is None:
        return None                                        # UNDEFINED ([C-2] L196)
    return 'DEFICIT' if m < -1 else ('EXCESS' if m > 1 else 'CENTERED')

def summarize(rows):
    s = {}
    for z in ZONES:
        zr = [(q, k) for q, k in rows if ZONE_OF[q] == z]
        views = [(q,) + row_view(k) for q, k in zr]
        nv = [v for v in views if not v[1]]
        H = sum(1 for v in nv if v[2] == 'HIT')
        M = sum(1 for v in nv if v[2] == 'MISS')
        I = sum(1 for v in views if v[1])
        defined = [v[3] for v in nv if v[3] is not None]
        m = median_or_none(defined)
        Nv = len(nv)
        s[z] = {'Nv': Nv, 'H': H, 'M': M, 'I': I, 'n_defined': len(defined), 'm': m, 'S': sign_class(m),
                'miss_dom': Nv >= 1 and M >= Nv / 2.0, 'hit_dom': Nv >= 1 and H > Nv / 2.0}
    # outer trend ([C-2] L204-L207): defined OUTER rows by R_q (= q), near/far halves, odd middle to far
    od = [(q, row_view(k)[2]) for q, k in rows if ZONE_OF[q] == 'OUTER' and not row_view(k)[0] and row_view(k)[2] is not None]
    od.sort()
    if len(od) >= 2:
        h = len(od) // 2
        near, far = [r for _, r in od[:h]], [r for _, r in od[h:]]
        d_out = statistics.median(far) - statistics.median(near)
    else:
        d_out = None
    o, t = s['OUTER'], s['TRANSITION']
    growing = (o['S'] == 'DEFICIT' and d_out is not None and d_out < 0 and t['m'] is not None and o['m'] is not None
               and t['m'] > o['m'])
    tsr_miss = any((q in TSR_FLAGGED) and (not row_view(k)[0]) and row_view(k)[1] == 'MISS' for q, k in rows)
    return s, d_out, growing, tsr_miss

def patterns(rows, rules):
    s, d_out, growing, tsr_miss = summarize(rows)
    i, t, o = s['INNER'], s['TRANSITION'], s['OUTER']
    P = set()
    if any(s[z]['I'] > 0 for z in ZONES): P.add('P0')
    if o['miss_dom'] and o['S'] == 'DEFICIT': P.add('P1')
    if 'P1' in P and growing: P.add('P1g')
    if o['miss_dom'] and o['S'] == 'EXCESS': P.add('P2')
    if o['miss_dom'] and o['S'] == 'CENTERED': P.add('P11')
    if i['miss_dom'] and i['S'] == 'EXCESS': P.add('P3')
    if i['miss_dom'] and i['S'] == 'DEFICIT': P.add('P4')
    if i['miss_dom'] and i['S'] == 'CENTERED': P.add('P12')
    if t['miss_dom']: P.add('P13')
    if i['hit_dom'] and o['miss_dom'] and t['Nv'] >= 1 and not t['hit_dom']: P.add('P5')
    if all(s[z]['Nv'] >= 1 for z in ZONES) and i['S'] is not None and i['S'] == t['S'] == o['S'] and i['S'] != 'CENTERED': P.add('P6')
    any_miss = any(s[z]['M'] > 0 for z in ZONES)
    if any_miss and not any(s[z]['miss_dom'] for z in ZONES): P.add('P7')
    if sum(s[z]['Nv'] for z in ZONES) >= 1 and sum(s[z]['M'] for z in ZONES) == 0: P.add('P8')
    if o['Nv'] == 0: P.add('P9')
    if tsr_miss: P.add('P10')
    if rules == 'FIX':
        if o['miss_dom'] and o['S'] is None: P.add('P14')    # OUTER_UNSIGNED
        if i['miss_dom'] and i['S'] is None: P.add('P15')    # INNER_UNSIGNED
    # OUTER_FAILURE, both sentences of [C-2] L209
    of_def1 = bool(o['miss_dom'])                             # "OUTER is miss-dominated, whatever its sign class"
    of_def2 = bool(P & {'P1', 'P2', 'P11'})                    # "It holds exactly when one of P1, P2 or P11 holds"
    if rules == 'FIX':
        of_def2 = bool(P & {'P1', 'P2', 'P11', 'P14'})
    def e3(of):                                               # [C-5.3] L357-L360
        if o['Nv'] == 0: return 'NOT_TESTABLE'
        return 'TESTED-NEGATIVE' if of else 'NOT_NEGATIVE_AT_OUTER'
    # R-MF status tuple part 1 ([C-3] L238-L241; [C-3.2] L271, L286, L287): patterns P1/P1g/P2/P11, P6, P7 (+P14 under FIX)
    rmf_pats = {'P1', 'P2', 'P11', 'P6', 'P7'} | ({'P14'} if rules == 'FIX' else set())
    rmf_against = (o['Nv'] >= 1 and not o['miss_dom'])
    if not (P & rmf_pats): rmf_rel = 'NOT_ADDRESSED'
    elif rmf_against: rmf_rel = 'INCONSISTENT'
    else: rmf_rel = 'CONSISTENT'
    cover_list = {'P1', 'P2', 'P11', 'P3', 'P4', 'P12', 'P13', 'P7'} | ({'P14', 'P15'} if rules == 'FIX' else set())
    coverage_literal = (not any_miss) or bool(P & cover_list)            # [C-2] L212 as written
    zone_pats = {'OUTER': {'P1', 'P2', 'P11', 'P14'}, 'INNER': {'P3', 'P4', 'P12', 'P15'}, 'TRANSITION': {'P13'}}
    uncovered_md_zones = [z for z in ZONES if s[z]['miss_dom'] and not (P & zone_pats[z])]
    return {'patterns': sorted(P, key=lambda p: (len(p), p)), 'OF_def1_missdom': of_def1, 'OF_def2_patterns': of_def2,
            'E3_def1': e3(of_def1), 'E3_def2': e3(of_def2), 'RMF_relation': rmf_rel,
            'RMF_verdict_def1': 'TESTED-NEGATIVE' if (o['Nv'] >= 1 and of_def1) else 'not TESTED-NEGATIVE',
            'coverage_literal_L212': coverage_literal, 'miss_dominated_zones_without_zone_pattern': uncovered_md_zones,
            'summaries': s, 'delta_out': d_out, 'growing': growing}

def build(inner, trans, outer):
    assert len(inner) == 24 and len(trans) == 11 and len(outer) == 8
    ks = list(inner) + list(trans) + list(outer)
    return [(q, ks[q - 1]) for q in range(1, 44)]

H = lambda n, r=0.3: [r] * n
CASES = {
    # undefined-sign zones
    'U1N_outer_all_null_ratio': build(['B', 'B'] + H(22), H(11), ['N'] * 8),
    'U1L_outer_all_late_gate': build(['B', 'B'] + H(22), H(11), ['L'] * 8),
    'U1G_outer_all_ontime_gate': build(['B', 'B'] + H(22), H(11), ['G'] * 8),
    'U1Lc_outer_cut4_plus_late4': build(['B', 'B'] + H(22), H(11), ['L'] * 4 + ['B'] * 4),
    'U1Gc_outer_cut4_plus_ontime4': build(['B', 'B'] + H(22), H(11), ['G'] * 4 + ['B'] * 4),
    'U1Lt_outer_late_and_transition_missdom': build(['B', 'B'] + H(22), [2.0] * 6 + H(5), ['L'] * 8),
    'U2L_inner_all_late_gate': build(['B', 'B'] + ['L'] * 22, H(11), H(8)),
    'U2N_inner_all_null_ratio': build(['B', 'B'] + ['N'] * 22, H(11), H(8)),
    'U2G_inner_all_ontime_gate': build(['B', 'B'] + ['G'] * 22, H(11), H(8)),
    'T1L_transition_all_late_gate_control': build(['B', 'B'] + H(22), ['L'] * 11, H(8)),
    # late versus on-time pairs: pattern removal
    'P5G_inner_11_gate_ontime': build(['B', 'B'] + ['G'] * 11 + H(11), [1.8] * 6 + H(5), [-2.5] * 8),
    'P5L_inner_11_gate_late': build(['B', 'B'] + ['L'] * 11 + H(11), [1.8] * 6 + H(5), [-2.5] * 8),
    'P8G_outer_2_gate_ontime': build(['B', 'B'] + H(22), H(11), ['G'] * 2 + H(6)),
    'P8L_outer_2_gate_late': build(['B', 'B'] + H(22), H(11), ['L'] * 2 + H(6)),
    'P7G_outer_1miss_4hit_3gate_ontime': build(['B', 'B'] + H(22), H(11), [-2.5] + H(4) + ['G'] * 3),
    'P7L_outer_1miss_4hit_3gate_late': build(['B', 'B'] + H(22), H(11), [-2.5] + H(4) + ['L'] * 3),
    'P10G_q25_gate_ontime': build(['B', 'B'] + H(22), ['G'] + H(10), H(8)),
    'P10L_q25_gate_late': build(['B', 'B'] + H(22), ['L'] + H(10), H(8)),
    # controls: a defined-sign row in the zone removes the contradiction
    'C1_outer_5late_3hit': build(['B', 'B'] + H(22), H(11), ['L'] * 5 + H(3)),
    'C2_outer_7late_1deficit': build(['B', 'B'] + H(22), H(11), ['L'] * 7 + [-3.0]),
    'C3_outer_all_deficit': build(['B', 'B'] + H(22), H(11), [-3.0] * 8),
}
PAIRS = [('U1G_outer_all_ontime_gate', 'U1L_outer_all_late_gate'), ('U1Gc_outer_cut4_plus_ontime4', 'U1Lc_outer_cut4_plus_late4'),
         ('U2G_inner_all_ontime_gate', 'U2L_inner_all_late_gate'), ('P5G_inner_11_gate_ontime', 'P5L_inner_11_gate_late'),
         ('P8G_outer_2_gate_ontime', 'P8L_outer_2_gate_late'), ('P7G_outer_1miss_4hit_3gate_ontime', 'P7L_outer_1miss_4hit_3gate_late'),
         ('P10G_q25_gate_ontime', 'P10L_q25_gate_late')]

def random_sweep(rules, n, seed):
    rng = np.random.default_rng(seed)
    kinds = np.array(['B', 'G', 'L', 'N', 'V'])
    rvals = np.array([-3.0, -1.5, -1.0, -0.4, 0.0, 0.4, 1.0, 1.5, 3.0])
    tally = {'n': n, 'OF_def1_ne_def2': 0, 'E3_def1_ne_def2': 0, 'coverage_literal_false': 0,
             'missdom_zone_without_zone_pattern': 0, 'RMF_TN_but_NOT_ADDRESSED': 0,
             'OF_mismatch_and_outer_has_defined_row': 0, 'coverage_false_without_undefined_only_zone': 0}
    examples = {}
    for it in range(n):
        p_kind = rng.dirichlet(np.ones(5))
        ks = []
        for q in range(1, 44):
            k = kinds[rng.choice(5, p=p_kind)]
            ks.append(str(k) if k != 'V' else float(rvals[rng.integers(len(rvals))]))
        rows = [(q, ks[q - 1]) for q in range(1, 44)]
        res = patterns(rows, rules)
        s = res['summaries']
        undefined_only = [z for z in ZONES if s[z]['miss_dom'] and s[z]['n_defined'] == 0]
        if res['OF_def1_missdom'] != res['OF_def2_patterns']:
            tally['OF_def1_ne_def2'] += 1
            examples.setdefault('OF_mismatch', ks)
            if s['OUTER']['n_defined'] > 0: tally['OF_mismatch_and_outer_has_defined_row'] += 1
        if res['E3_def1'] != res['E3_def2']: tally['E3_def1_ne_def2'] += 1
        if not res['coverage_literal_L212']:
            tally['coverage_literal_false'] += 1
            examples.setdefault('coverage_false', ks)
            if not undefined_only: tally['coverage_false_without_undefined_only_zone'] += 1
        if res['miss_dominated_zones_without_zone_pattern']:
            tally['missdom_zone_without_zone_pattern'] += 1
            examples.setdefault('zone_uncovered', ks)
        if res['RMF_verdict_def1'] == 'TESTED-NEGATIVE' and res['RMF_relation'] == 'NOT_ADDRESSED':
            tally['RMF_TN_but_NOT_ADDRESSED'] += 1
    return tally, examples

def main():
    results = {'R2': {k: patterns(v, 'R2') for k, v in CASES.items()},
               'FIX': {k: patterns(v, 'FIX') for k, v in CASES.items()}}
    diffs = {}
    for a, b in PAIRS:
        pa, pb = set(results['R2'][a]['patterns']), set(results['R2'][b]['patterns'])
        diffs['%s -> %s' % (a, b)] = {'removed_by_late': sorted(pa - pb), 'added_by_late': sorted(pb - pa),
                                      'E3_ontime_def1/def2': [results['R2'][a]['E3_def1'], results['R2'][a]['E3_def2']],
                                      'E3_late_def1/def2': [results['R2'][b]['E3_def1'], results['R2'][b]['E3_def2']]}
    sweep_r2, ex_r2 = random_sweep('R2', 20000, 20261018)
    sweep_fix, ex_fix = random_sweep('FIX', 20000, 20261018)
    out = {'cases': results, 'late_vs_ontime': diffs, 'sweep_R2': sweep_r2, 'sweep_FIX': sweep_fix,
           'sweep_examples_R2': {k: [str(x) for x in v] for k, v in ex_r2.items()},
           'sweep_examples_FIX': {k: [str(x) for x in v] for k, v in ex_fix.items()}}
    for k in CASES:
        r = results['R2'][k]
        print('%-42s %-30s OF1=%-5s OF2=%-5s E3=%s|%s RMF=%s cov=%s uncov=%s' % (
            k, ','.join(r['patterns']), r['OF_def1_missdom'], r['OF_def2_patterns'], r['E3_def1'], r['E3_def2'],
            r['RMF_relation'], r['coverage_literal_L212'], r['miss_dominated_zones_without_zone_pattern']))
    print('--- late vs on-time')
    for k, v in diffs.items(): print(k, v)
    print('--- sweep R2 ', sweep_r2)
    print('--- sweep FIX', sweep_fix)
    payload = json.dumps(out, indent=1, sort_keys=True, default=str) + '\n'
    sys.addaudithook(_fence)
    with open(OUT, 'x') as f:
        f.write(payload)

if __name__ == '__main__':
    main()
