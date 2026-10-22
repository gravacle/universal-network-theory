# R2-A closure lens: verify the C-1.4 / M-7 facts from target-free bytes only.
# Reads: the K32 compare, the K32 N1 record, the registered GL4 nodes, and the slots V003 query block (ids, Rad_text, Rad_unit only).
# Prints no velocity field. Exclusive-create output into this lens folder.
import json, hashlib, sys, os
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
PINS = {
 'compare': (ART + 'ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json', '6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9'),
 'n1': (ART + 'ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json', '8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70'),
 'nodes': (ART + 'ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json', 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'),
 'slots': (ART + 'freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json', 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'),
}
def strict(b):
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d: raise ValueError('dup %r' % k)
            d[k] = v
        return d
    return json.loads(b.decode('utf-8'), object_pairs_hook=hook)
docs = {}
for k, (p, h) in PINS.items():
    b = open(p, 'rb').read()
    got = hashlib.sha256(b).hexdigest()
    assert got == h, (k, got)
    docs[k] = strict(b)
c, n1, nodes, slots = docs['compare'], docs['n1'], docs['nodes'], docs['slots']
out = {'pins_verified': {k: v[1] for k, v in PINS.items()}}
out['compare'] = {k: c[k] for k in ('outcome', 'tests_read', 'production_K_big', 'n_route_ab_gate', 'n_route_ab_reason_codes', 'n_route_ab_ruling', 'failures', 'checks')}
out['compare']['failing_TRUNCATION_SHAPE_rings'] = c['failing_TRUNCATION_SHAPE_rings']
out['compare']['failing_non_TRUNCATION_SHAPE_rings'] = c['failing_non_TRUNCATION_SHAPE_rings']
out['n1_keys'] = sorted(n1.keys())
rr = n1.get('ring_radii_kpc')
gl = nodes['orders']['4']['radii_kpc']
out['n1_ring_count'] = len(rr)
out['gl4_node_count'] = len(gl)
out['rings_equal_nodes_bitwise'] = (len(rr) == len(gl) and all(float(a).hex() == float(b).hex() for a, b in zip(rr, gl)))
out['rings_12_to_18'] = {i: rr[i] for i in range(12, 19)}
rows = slots['query_block']['rows']
out['rad_units'] = sorted({r['Rad_unit'] for r in rows})
out['n_rows'] = len(rows)
rad = {r['query_id']: float(r['Rad_text']) for r in rows}
out['Q22_to_Q28'] = {q: r['Rad_text'] for r in rows for q in [r['query_id']] if q in ['NGC3198-Q%02d' % i for i in range(22, 29)]}
out['Q34_to_Q37'] = {q: r['Rad_text'] for r in rows for q in [r['query_id']] if q in ['NGC3198-Q%02d' % i for i in range(34, 38)]}
# M-7 derived rule: flagged iff r_{k-1} < R_q < r_{k+1} for failing ring k
flag = {}
for ring in c['failing_TRUNCATION_SHAPE_rings']:
    k = ring.get('ordinal')
    lo, hi = rr[k - 1], rr[k + 1]
    flag[k] = sorted(q for q, R in rad.items() if lo < R < hi)
out['flagged_by_derived_rule'] = flag
# zone membership from Rad_text with cuts 10.0 / 30.0
zones = {'INNER': [], 'TRANSITION': [], 'OUTER': []}
for r in rows:
    R = float(r['Rad_text'])
    z = 'INNER' if R < 10.0 else ('TRANSITION' if R < 30.0 else 'OUTER')
    zones[z].append(r['query_id'])
out['zones'] = {z: [v[0], v[-1], len(v)] for z, v in zones.items()}
out['query_ids_in_order'] = [r['query_id'] for r in rows] == ['NGC3198-Q%02d' % i for i in range(1, 44)]
# slots alternatives and observation rule (metadata only)
alts = slots.get('alternatives', {})
out['slots_top_keys'] = sorted(slots.keys())
out['alternatives_shape'] = type(alts).__name__
dst = sys.argv[1]
with open(dst, 'x') as f:
    f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
print(json.dumps(out, indent=1, sort_keys=True))
