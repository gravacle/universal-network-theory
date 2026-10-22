"""verify_targetfree_2: independent recomputation of the TRUNCATION_SHAPE_RESIDUAL flag set
under candidate radial-support definitions (finding B-2 of lens targetfree).

Reads only target-free inputs, each verified by sha256 from bytes:
  - N-test compare of record (K32_COMPARE_COMPLETE_V001.json)
  - N1 record (K32_RECORDS_COMPLETE_V001_N1.json)
  - slots V003 query block (ids and radii only)
  - registered GL4 route-B node artifact
No target, observed velocity or sigma is read. Writes one JSON into this check's runs/ folder
with an exclusive create (open mode 'x').
"""
import hashlib, json, sys, random
from pathlib import Path

PINS = {
    'compare': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json',
                '6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9'),
    'n1': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json',
           '8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70'),
    'slots': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json',
              'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'),
    'gl_nodes': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json',
                 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'),
}

def load(key):
    path, want = PINS[key]
    raw = Path(path).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != want:
        raise SystemExit('SHA_MISMATCH %s %s' % (key, got))
    return json.loads(raw)

def main(out_path):
    cmp_ = load('compare'); n1 = load('n1'); slots = load('slots'); gl = load('gl_nodes')
    rings = n1['ring_radii_kpc']
    kpc_m = gl['kpc_m']
    assert len(rings) == 100 and all(a < b for a, b in zip(rings, rings[1:]))
    assert all(gl['orders']['4']['radii_m'][i] / kpc_m == rings[i] for i in range(100)), 'rings != GL4 nodes'
    fail = cmp_['failing_TRUNCATION_SHAPE_rings']
    assert len(fail) == 1 and cmp_['failing_non_TRUNCATION_SHAPE_rings'] == []
    f = fail[0]; i = f['ordinal']; R = f['R_kpc']
    assert rings[i] == R and f['radial_support'] == {'kind': 'sampled_ring', 'R_kpc': R}
    stored_keys = sorted(f['radial_support'].keys())
    rows = slots['query_block']['rows']
    assert len(rows) == 43
    q = []
    for r in rows:
        assert r['Rad_unit'] == 'kpc' and float(r['Rad_text']) == r['radius_kpc']
        q.append((r['query_id'], float(r['Rad_text'])))
    # candidate definitions: (lo, hi, closed_lo, closed_hi)
    cands = {
        'A_point_as_stored_closed': (R, R, True, True),
        'B_midpoints_to_neighbour_rings_closed': ((rings[i-1] + R) / 2, (R + rings[i+1]) / 2, True, True),
        'C_neighbour_rings_closed': (rings[i-1], rings[i+1], True, True),
        'C2_linear_interpolation_footprint_open': (rings[i-1], rings[i+1], False, False),
        'D_two_rings_each_side_closed': (rings[i-2], rings[i+2], True, True),
        'E_pm_0p25_kpc_closed': (R - 0.25, R + 0.25, True, True),
        'F_pm_0p5_kpc_closed': (R - 0.5, R + 0.5, True, True),
        'G_pm_1p0_kpc_closed': (R - 1.0, R + 1.0, True, True),
    }
    def inside(x, lo, hi, cl, ch):
        a = (x >= lo) if cl else (x > lo)
        b = (x <= hi) if ch else (x < hi)
        return a and b
    res = {}
    min_margin = None
    for name, (lo, hi, cl, ch) in cands.items():
        kpc = [qid for qid, x in q if inside(x, lo, hi, cl, ch)]
        met = [qid for qid, x in q if inside(x * kpc_m, lo * kpc_m, hi * kpc_m, cl, ch)]
        margins = [min(abs(x - lo), abs(x - hi)) for _, x in q]
        m = min(margins)
        min_margin = m if min_margin is None else min(min_margin, m)
        res[name] = {'interval_kpc': [lo, hi], 'closed': [cl, ch], 'flagged_kpc_arithmetic': kpc,
                     'flagged_metre_arithmetic': met, 'kpc_equals_metre': kpc == met,
                     'min_abs_distance_any_query_to_an_endpoint_kpc': m}
    # rows whose piecewise-linear interpolated value uses node i with nonzero weight (registered observation rule)
    interp_dep = []
    for qid, x in q:
        if x < rings[0] or x > rings[-1]:
            continue
        j = max(k for k in range(100) if rings[k] <= x)
        if rings[j] == x:
            used = {j}
        else:
            used = {j, j + 1}
        if i in used:
            interp_dep.append(qid)
    # nearest node of each nearby query
    near = {}
    for qid, x in q:
        if 9.0 <= x <= 12.5:
            k = min(range(100), key=lambda k: abs(rings[k] - x))
            near[qid] = {'R_q_kpc': x, 'nearest_ring_ordinal': k, 'nearest_ring_R_kpc': rings[k], 'distance_kpc': abs(rings[k] - x)}
    # synthetic P10 check: random synthetic tiers, never a target
    rng = random.Random(20261018)
    tiers = ('HIT', 'NEAR', 'MISS', 'INVALID_AS_MISS')
    p10 = {}
    for name in ('A_point_as_stored_closed', 'C_neighbour_rings_closed', 'F_pm_0p5_kpc_closed'):
        flagged = set(res[name]['flagged_kpc_arithmetic'])
        cnt = 0
        for _ in range(20000):
            t = {qid: rng.choice(tiers) for qid, _ in q}
            if any(t[qid] == 'MISS' for qid in flagged):
                cnt += 1
        p10[name] = {'draws': 20000, 'P10_true_count': cnt}
    out = {
        'schema': 'VT2_TSR_FLAGSET_RECOMPUTE_V001',
        'pins_verified': {k: v[1] for k, v in PINS.items()},
        'failing_ring': {'ordinal': i, 'R_kpc': R, 'stored_radial_support_keys': stored_keys,
                         'has_r_lo_r_hi_keys': ('r_lo' in f['radial_support'] and 'r_hi' in f['radial_support']),
                         'neighbours_kpc': {str(i-2): rings[i-2], str(i-1): rings[i-1], str(i+1): rings[i+1], str(i+2): rings[i+2]}},
        'n1_record_has_radial_support_key': 'radial_support' in n1,
        'rings_equal_registered_GL4_nodes_bitwise': True,
        'kpc_m': kpc_m,
        'query_ids_with_R_equal_to_failing_ring': [qid for qid, x in q if x == R],
        'candidates': res,
        'linear_interpolation_dependence_on_ring_15': interp_dep,
        'nearest_ring_of_queries_9_to_12p5_kpc': near,
        'min_margin_over_all_candidates_kpc': min_margin,
        'synthetic_P10_reachability': p10,
    }
    with open(out_path, 'x') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: (v['flagged_kpc_arithmetic'], v['kpc_equals_metre']) for k, v in res.items()}, indent=1))
    print('interp_dep', interp_dep, 'min_margin', min_margin, 'p10', p10)

if __name__ == '__main__':
    main(sys.argv[1])
