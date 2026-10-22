# Lens A (fidelity) reproductions for the miss-reading prereg r2 round1. Synthetic data only; no target is opened.
# Imports the reviewed freeze module v003g by path (no bytecode written, -B) and calls its own scoring helpers on
# synthetic members. Reads two target-free records (slots V003 query block; the NGC K32 N-test compare output).
# After those reads an audit hook refuses every further open, so the reproductions run with no file access.
import hashlib, importlib.util, json, math, sys

FREEZE = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py'
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
K32 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json'
BAD = ('rotmod', 'vobs', 'massmodels', 'sparc')
for p in (FREEZE, SLOTS, K32):
    assert not any(b in p.lower() for b in BAD)

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

out = {'inputs': {'freeze_module': sha(FREEZE), 'slots_v003': sha(SLOTS), 'k32_compare': sha(K32)}}
assert out['inputs']['freeze_module'] == '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
assert out['inputs']['slots_v003'] == 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
spec = importlib.util.spec_from_file_location('freeze_v003g_lensA', FREEZE)
fz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fz)
slots = json.load(open(SLOTS))
k32 = json.load(open(K32))

def _hook(event, args):
    if event == 'open':
        raise PermissionError('lens A: no file access after setup: %r' % (args[0],))
sys.addaudithook(_hook)

# ---------- R1: NEAR (band_overlaps_error_bar) holds although no PRIMARY member is within error -------------
ids = ['Q%02d' % i for i in range(1, 4)]
v, s = 100.0, 5.0                                   # synthetic target pair
bound = [(v, s)] * 3
mk = lambda mid, li, speeds: {'member_id': mid, 'log_index': li, 'role': 'interior', 'evaluated': True,
                              'member_valid': True, 'speeds_km_s': speeds, 'row_valid': [True] * 3,
                              'row_registration': [None] * 3}
members = [mk('m_ref', 7, [v + 3 * s] * 3), mk('m_lo', 3, [v - 2 * s] * 3), mk('m_hi', 9, [v + 2 * s] * 3)]
scored = fz._score_members(members, ids, bound)
env = fz._pointwise_envelope(members, ids)
erows, eov, _ = fz._band_rows(env, 'band_low_km_s', 'band_high_km_s', ids, bound)
out['R1_near_without_member_within_error'] = {
    'member_within_error_q1': {m['member_id']: m['rows'][0]['within_error'] for m in scored},
    'reference_score_status_q1': scored[0]['rows'][0]['score_status'],
    'envelope_q1': [erows[0]['band_low_km_s'], erows[0]['band_high_km_s']],
    'band_overlaps_error_bar_q1': erows[0]['band_overlaps_error_bar'],
    'any_member_within_error_q1': any(m['rows'][0]['within_error'] for m in scored),
}

# ---------- R2: a root-listed gate reason gives INVALID_AS_MISS (not one of the three built-ins);
#                and a gate-listed row the producer reports valid is scored normally -----------------------
gate_pin = {'path': '/synthetic/gate.json', 'sha256': 'a' * 64}
roster = {'required': {'Q01': {'status': 'INVALID', 'reason': 'QUERY_INSIDE_INNERMOST_NODE', 'registration': None}},
          'cut_mode': 'NONE', 'contexts': [], 'radii': {'Q01': 0.32, 'Q02': 5.0, 'Q03': 11.0},
          'gates': {('Q02', 'SYNTHETIC_GATE_REASON'): gate_pin, ('Q03', 'SYNTHETIC_GATE_REASON'): gate_pin}}
req = fz._row_contract(roster, {})
reg_q2 = fz._authorized_row_registration(roster, req, 'Q02', 'SYNTHETIC_GATE_REASON')
member = {'member_id': 'm_ref', 'log_index': 7, 'role': 'interior', 'evaluated': True, 'member_valid': True,
          'forward_valid_flag': True, 'theta_ngc': {},
          'row_valid': [False, False, True], 'speeds_km_s': [None, None, v + 0.5 * s],
          'row_registration': [dict(req['Q01']), reg_q2, None]}
fz._root_frozen_rows(member, ids, roster)            # raises if the frozen rows break the roster contract
sc = fz._score_members([member], ids, bound)[0]['rows']
out['R2_gate_rows'] = {
    'Q02_gate_listed_reported_invalid': {k: sc[1][k] for k in ('score_status', 'registered_reason', 'tier')},
    'Q02_reason_in_REGISTERED_INVALID_REASONS': sc[1]['registered_reason'] in fz.REGISTERED_INVALID_REASONS,
    'Q03_gate_listed_reported_valid': {k: sc[2][k] for k in ('score_status', 'registered_reason', 'tier')},
    'root_frozen_rows_accepted': True,
}

# ---------- R3: the M-7 closed-interval rule on the actual K32 radial_support record ---------------------
rings = k32['failing_TRUNCATION_SHAPE_rings']
rad = {r['query_id']: float(r['Rad_text']) for r in slots['query_block']['rows']}
r3 = {'k32_outcome': k32['outcome'], 'n_route_ab_gate': k32['n_route_ab_gate'],
      'reason_codes': k32['n_route_ab_reason_codes'], 'rings': rings}
ring = rings[0]
rs = ring['radial_support']
r3['support_has_r_lo_r_hi'] = all(k in rs for k in ('r_lo', 'r_hi'))
lo = hi = rs['R_kpc']                                 # the only reading of a point support as [r_lo, r_hi]
r3['flagged_closed_interval_point'] = [q for q, R in rad.items() if lo <= R <= hi]
qs = sorted(rad, key=lambda q: rad[q])
below = max((q for q in qs if rad[q] <= rs['R_kpc']), key=lambda q: rad[q])
above = min((q for q in qs if rad[q] > rs['R_kpc']), key=lambda q: rad[q])
mid = 0.5 * (rad[below] + rad[above])
r3['neighbours'] = {below: rad[below], above: rad[above], 'midpoint_kpc': mid,
                    'ring_minus_midpoint_kpc': rs['R_kpc'] - mid,
                    'nearest_query': min((below, above), key=lambda q: abs(rad[q] - rs['R_kpc']))}
out['R3_m7_rule_on_actual_record'] = r3

# ---------- R4: zone table and STAGE0 scope from the target-free query block -----------------------------
zones = {'INNER': [q for q in qs if rad[q] < 10.0], 'TRANSITION': [q for q in qs if 10.0 <= rad[q] < 30.0],
         'OUTER': [q for q in qs if rad[q] >= 30.0]}
st0 = next(a for a in slots['alternatives']['declared'] if a['name'] == 'STAGE0_GRID_OUTER')
out['R4_zones'] = {z: [l[0], l[-1], len(l), rad[l[0]], rad[l[-1]]] for z, l in zones.items()}
out['R4_outer_equals_stage0_scope'] = zones['OUTER'] == st0['scoring_scope']['query_ids']
print(json.dumps(out, indent=1, sort_keys=True))

# ---------- R5: an OUTER-row failure that no §2 pattern (P1-P9) reports (independent implementation of §2) --------
def _median(x):
    x = sorted(x); n = len(x)
    if n == 0:
        return None
    return x[n // 2] if n % 2 else 0.5 * (x[n // 2 - 1] + x[n // 2])
def _zone(rs, near=()):
    hits = sum(1 for r in rs if abs(r) <= 1); miss = len(rs) - hits   # no NEAR rows in this example
    m = _median(rs); nv = len(rs)
    S = None if m is None else ('DEFICIT' if m < -1 else 'EXCESS' if m > 1 else 'CENTERED')
    return {'N_v': nv, 'H': hits, 'M': miss, 'm': m, 'S': S,
            'miss_dom': nv >= 1 and miss >= nv / 2, 'hit_dom': nv >= 1 and hits >= nv / 2}
Z = {'INNER': _zone([0.2] * 14 + [1.5] * 10), 'TRANSITION': _zone([0.3] * 8 + [-1.5] * 3),
     'OUTER': _zone([-3.0, -2.5, -2.0, -0.5, 0.5, 2.0, 2.5, 3.0])}
I, T, O = Z['INNER'], Z['TRANSITION'], Z['OUTER']
pat = {'P1': O['miss_dom'] and O['S'] == 'DEFICIT', 'P2': O['miss_dom'] and O['S'] == 'EXCESS',
       'P3': I['miss_dom'] and I['S'] == 'EXCESS', 'P4': I['miss_dom'] and I['S'] == 'DEFICIT',
       'P5': I['hit_dom'] and O['miss_dom'] and T['N_v'] >= 1 and not T['hit_dom'],
       'P6': I['S'] == T['S'] == O['S'] != 'CENTERED',
       'P7': (I['M'] + T['M'] + O['M']) >= 1 and not any(z['miss_dom'] for z in Z.values()),
       'P8': (I['M'] + T['M'] + O['M']) == 0, 'P9': O['N_v'] == 0}
print(json.dumps({'R5_outer_failure_without_pattern': {'zones': Z, 'patterns_P1_P9': pat,
                  'any_pattern': any(pat.values())}}, indent=1, sort_keys=True))
