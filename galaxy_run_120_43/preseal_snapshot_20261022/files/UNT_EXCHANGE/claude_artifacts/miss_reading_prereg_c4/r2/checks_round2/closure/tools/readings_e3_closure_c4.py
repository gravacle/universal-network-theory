# R2-A closure lens: which readings does round-2 PREREG [C-3.2] register for each OUTER_FAILURE pattern, and are the binding
# A15 E3 / A12.3 three readings (R-MF, R-REACH, R-HIST) and the A20 two readings (R-UT1, R-HIST) among them?
# Pattern logic: the independent round-2 implementation in patterns_r2_closure_c4.py. Synthetic dimensionless r only.
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('pat', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patterns_r2_closure_c4.py'))
src = open(spec.origin).read().split('\nHITS = ')[0]       # reuse only the definitions, not the case table / output
ns = {}
exec(compile(src, spec.origin, 'exec'), ns)
patterns, zones = ns['patterns'], ns['zones']
# round-2 C-3.2 registered readings per pattern (rows L271-L290 of PREREG_MISS_READING_R2.md 97d5ce33)
TABLE = [
    (('P1', 'P1g', 'P2', 'P11'), ['R-MF', 'R-DRIFT']),
    (('P1', 'P1g'), ['R-UT1', 'R-HIST', 'R-REACH']),
    (('P2', 'P11'), ['R-S1', 'R-GRID']),
    (('P11',), ['R-NAX']),
    (('P3', 'P4', 'P12'), ['R-GEFF', 'R-ML', 'R-SPEC']),
    (('P3', 'P4', 'P12', 'P6'), ['R-GEO']),
    (('P3', 'P4', 'P12', 'P7', 'P13'), ['R-NAX']),
    (('P5',), ['R-MF', 'R-UT1', 'R-HIST', 'R-REACH', 'R-DRIFT', 'R-NAX']),
    (('P13',), ['R-NAX', 'R-TSR']),
    (('P6',), ['R-S1', 'R-GEO', 'R-MF']),
    (('P7',), ['R-NAX', 'R-MF']),
    (('P10',), ['R-TSR']),
]
def readings(P):
    s = set()
    for pats, rs in TABLE:
        if any(p in P for p in pats):
            s.update(rs)
    return sorted(s)
H = lambda n: [0.2] * n
cases = {
    'P1_outer_deficit': zones(['I', 'I'] + H(22), H(11), [-3, -2.5, -2, -3.5, -4, -2, 0.5, -3]),
    'P2_outer_excess': zones(['I', 'I'] + H(22), H(11), [3, 2.5, 2, 3.5, 4, 2, 0.5, 3]),
    'P11_E2_shaped_crossing': zones(['I', 'I'] + H(22), H(11), [3, 2, 1.5, 0.5, -0.5, -1.5, -2, -3]),
    'P11_alternating': zones(['I', 'I'] + H(22), H(11), [-3, 3, -2.5, 2.5, -2, 2, -1.5, 1.5]),
}
out = {}
for k, z in cases.items():
    r = patterns(z)
    regs = readings(r['patterns'])
    out[k] = {'patterns': r['patterns'], 'OUTER_FAILURE': r['OUTER_FAILURE_def1_missdom'], 'E3_line': r['E3_line_under_def1'],
              'registered_readings': regs,
              'A15_E3_three_readings_registered': {x: x in regs for x in ('R-MF', 'R-REACH', 'R-HIST')},
              'A20_two_readings_registered': {x: x in regs for x in ('R-UT1', 'R-HIST')}}
    print('%-24s %-14s E3=%-16s readings=%s  E3-three=%s  A20-two=%s' % (k, ','.join(r['patterns']), out[k]['E3_line'], ','.join(regs),
          out[k]['A15_E3_three_readings_registered'], out[k]['A20_two_readings_registered']))
with open(sys.argv[1], 'x') as f:
    f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
