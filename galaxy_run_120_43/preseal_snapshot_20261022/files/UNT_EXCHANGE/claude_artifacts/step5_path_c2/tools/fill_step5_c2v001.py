"""Target-free, exclusive step-5 spec filler (c2v001). Does not launch or infer admission.

Successor of fill_step5_cx3v003 (2348974f). The expected handoff digest must come from Claude2 (RI45-09), never
from this tool. A synthetic handoff exercises custody only and is never admitted. Changes, each tied to one item:

  RI45-02 (a)  The native three-u fixed-distance mode.  The policy binds the coordinate mode name
               DDO154_DISTANCE_FIXED_AT_REGISTERED, the coordinate addendum and the admitted (coordinate spec,
               addendum) pairs.  The engine coordinates are the policy coordinates with ONLY the role of distance_Mpc
               changed from nuisance to fixed (the orchestrator's _apply_coordinate_mode rule), so u has three
               entries and theta_natural.distance_Mpc must equal the fixed 4.04 Mpc.  A Phase-1 source names its
               campaign config; that config must name an admitted pair.  theta_natural stays the mapping input.
  RI45-08 (a)  Driver cx3r008 (577f8c94) only, with its registry (2c3f421d) and its accepted review (7ff20c1d) as
               the acceptance pin of every non-synthetic handoff.  r006 and r007 are not in the policy and refuse.
  RI45-12 (a)  Interface A only.  The policy's templates are the call of record (route_a.column_workers 1) and its
               identity twin (route_a.column_workers 8, A132/A133 1.4); the two emitted specs must differ only in
               that leaf, or nothing is written.
  A133 1.4     A second handoff schema for Phase-1 points that are not admitted points: the S0 set
               (PHASE1_S0_C2V001, from phase1_c2v001 fdplan --s0-only) and the FD points F (PHASE1_FDPLAN_C2V001).
               The point is selected by its theta key, recomputed here from theta_natural.
  A133 3       The label is 'step5 <template> theta_key=<key>': it no longer carries the handoff sha or mode (both
               are in the receipt), so the same theta and certificates give the same spec sha in Phase 1 and
               Phase 2 (the A133 section-3 re-binding rule).
Everything else (pins checked from bytes, exact fields, finite numbers, the certificate sentinel, exclusive output,
launch_authorized false) is cx3v003's.
"""
import argparse
import copy
import datetime
import hashlib
import json
import math
from pathlib import Path

POLICY_SHA = '0c781a17548150831a7e10b8dd9d27897b856ab21398ee277fab3d2bbc4287e9'
PENDING = 'PENDING_UV_TAIL_CERTIFICATE'
EXPORT_HANDOFF = 'UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001'
PHASE1_HANDOFF = 'UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001'
THETA_KEY_SCHEMA = 'DDO154_CALIBRATION_THETA_KEY_C2V001'   # orchestrator c2v005 SCHEMA_THETA_KEY (theta_key)
DISTANCE_NAME, DISTANCE_MPC = 'distance_Mpc', 4.04
COMMON_FIELDS = ('schema', 'mode', 'policy_pin', 'driver_branch', 'driver_acceptance_pin', 'v007_adoption_pin',
                 'root_admission', 'certificate_pins')


class Refusal(ValueError):
    pass


def need(ok, reason):
    if not ok:
        raise Refusal(reason)


def safe_path(value):
    need(isinstance(value, str) and Path(value).is_absolute(), 'ABSOLUTE_PATH_REQUIRED')
    p = Path(value)
    for q in (p, p.resolve()):
        s = str(q).lower()
        need('/runs_ext/uvt_' not in s and 'kmax_a2f10_c5h_run_v001' not in s,
             'PROTECTED_RUN_PATH')
        need('/.codex/' not in s and '/.codex-alt/' not in s, 'SESSION_PATH')
        if 'ngc3198' in s:
            s = s.replace('target_free', '').replace('target-free', '')
            need(not any(x in s for x in ('observed', 'velocit', 'rotmod', 'target')), 'NGC_TARGET_PATH')
    return p


def keys(obj, expected, where):
    need(type(obj) is dict and set(obj) == set(expected), 'EXACT_FIELDS_' + where)


def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        need(k not in out, 'DUPLICATE_JSON_KEY_' + k)
        out[k] = v
    return out


def parse(b):
    def bad_constant(s):
        raise Refusal('NONFINITE_JSON_' + s)
    return json.loads(b, object_pairs_hook=unique_pairs, parse_constant=bad_constant)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def encoded(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def theta_key(theta):
    """The orchestrator c2v005 theta_key, verbatim: sha256 of canonical {schema, theta} with float values."""
    th = {str(k): float(v) for k, v in theta.items()}
    need(all(math.isfinite(v) for v in th.values()), 'THETA_KEY_NONFINITE')
    return sha(json.dumps({'schema': THETA_KEY_SCHEMA, 'theta': th}, sort_keys=True, separators=(',', ':'),
                          allow_nan=False).encode('utf-8'))


def is_pin(x):
    return type(x) is dict and set(x) == {'path', 'sha256'}


def load_pin(pin, where, decode=True):
    keys(pin, ('path', 'sha256'), where + '_PIN')
    need(type(pin['sha256']) is str and len(pin['sha256']) == 64 and
         all(c in '0123456789abcdef' for c in pin['sha256']), 'HEX_SHA_' + where)
    b = safe_path(pin['path']).read_bytes()
    need(sha(b) == pin['sha256'], 'BYTE_PIN_' + where)
    return parse(b) if decode else b


def number(x, where):
    need(type(x) in (int, float), 'FINITE_REAL_' + where)
    try:
        value = float(x)
    except (OverflowError, ValueError):
        raise Refusal('FINITE_REAL_' + where) from None
    need(math.isfinite(value), 'FINITE_REAL_' + where)
    return value


def engine_coordinates(policy, coordinates):
    """RI45-02 (a): the native engine coordinates = the policy coordinates with ONLY distance_Mpc's role changed
    (nuisance -> fixed, trial 4.04), as orchestrator c2v005 _apply_coordinate_mode does; the addendum must say so."""
    cm = policy['coordinate_mode']
    keys(cm, ('mode', 'addendum', 'fixed_engine_coordinates', 'free_coordinates', 'rule'), 'COORDINATE_MODE')
    add = load_pin(cm['addendum'], 'COORDINATE_ADDENDUM')
    acm = add.get('coordinate_mode') if type(add) is dict else None
    need(type(acm) is dict and acm.get('mode') == cm['mode'] == 'DDO154_DISTANCE_FIXED_AT_REGISTERED', 'COORDINATE_MODE_NAME')
    need(acm.get('fixed_engine_coordinates') == cm['fixed_engine_coordinates'] == {DISTANCE_NAME: DISTANCE_MPC},
         'COORDINATE_MODE_FIXED_DISTANCE')
    need(acm.get('free_coordinates') == cm['free_coordinates'], 'COORDINATE_MODE_FREE_NAMES')
    need(add.get('applies_to_coordinate_spec_sha256') == policy['coordinates']['sha256'], 'COORDINATE_ADDENDUM_TARGET')
    src = coordinates['engine_coordinates']
    out = copy.deepcopy(src)
    hit = [c for c in out if c.get('name') == DISTANCE_NAME]
    need(len(hit) == 1, 'COORDINATE_MODE_DISTANCE_SLOT')
    c = hit[0]
    need(c.get('role') == 'nuisance' and c.get('scope') == 'DDO154' and c.get('units') == 'Mpc' and
         c.get('trial_value') == DISTANCE_MPC, 'COORDINATE_MODE_DISTANCE_SLOT')
    c['role'] = 'fixed'
    changed = [(a['name'], k) for a, b in zip(src, out) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    need(changed == [(DISTANCE_NAME, 'role')], 'COORDINATE_MODE_CHANGED_MORE_THAN_DISTANCE_ROLE')
    need([x['name'] for x in out if x['role'] != 'fixed'] == cm['free_coordinates'], 'COORDINATE_MODE_VARYING_ORDER')
    return out


def admitted_pair(policy, spec_pin, addendum_pin):
    for pair in policy['admitted_campaign_coordinate_pairs']:
        keys(pair, ('coordinate_spec', 'addendum'), 'ADMITTED_PAIR')
        if pair['coordinate_spec'] == spec_pin and (addendum_pin is None or pair['addendum'] == addendum_pin):
            return True
    return False


def validate_point(point, dims, where):
    """cx3v003 validate_points, per point, on the native engine coordinates (three varying entries)."""
    u = point['u']
    nvary = sum(c['role'] != 'fixed' for c in dims)
    need(type(u) is list and len(u) == nvary, 'VARYING_U_LENGTH')
    for value in u:
        need(0 <= number(value, 'U') <= 1, 'U_BOUNDS')
    theta = point['theta_natural']
    need(type(theta) is dict and set(theta) == {c['name'] for c in dims}, 'EXACT_ENGINE_COORDINATES')
    j = 0
    for c in dims:
        value = number(theta[c['name']], c['name'])
        need(c['lower'] <= value <= c['upper'], 'THETA_BOUNDS_' + c['name'])
        if c['role'] == 'fixed':
            need(value == c['trial_value'], 'FIXED_THETA_CHANGED_' + c['name'])
            expected = c['trial_value']
        else:
            lo, hi = (math.log(c[k]) for k in ('lower', 'upper')) if c['transform'] == 'log' else (c[k] for k in ('lower', 'upper'))
            x = lo + u[j] * (hi - lo)
            expected = min(c['upper'], max(c['lower'], math.exp(x))) if c['transform'] == 'log' else x
            j += 1
        need(math.isclose(value, expected, rel_tol=1e-12, abs_tol=0.0), 'U_THETA_MISMATCH_' + c['name'])
    need(theta[DISTANCE_NAME] == DISTANCE_MPC, 'DISTANCE_NOT_FIXED_4_04')
    return theta_key(theta)


def export_point(h, policy, dims):
    """RI45-10 export path (Phase-2 members, Phase-1 v003g members): the cx3v003 rules on three-u points."""
    keys(h, COMMON_FIELDS + ('source_export_pin', 'log_index'), 'HANDOFF')
    export = load_pin(h['source_export_pin'], 'EXPORT')
    keys(export, ('schema', 'mode', 'target_free', 'coordinate_pin', 'admitted_points'), 'EXPORT')
    need(export['schema'] == 'UNT_STEP4_TARGET_FREE_ADMITTED_EXPORT_CX3V001', 'EXPORT_SCHEMA')
    need(export['mode'] == h['mode'] and export['target_free'] is True, 'EXPORT_TARGET_FREE_MODE')
    need(is_pin(export['coordinate_pin']) and admitted_pair(policy, export['coordinate_pin'], None),
         'EXPORT_COORDINATE_BINDING')
    points = export['admitted_points']
    need(type(points) is list and bool(points), 'NONEMPTY_ADMITTED_POINTS')
    indices, chosen = set(), []
    for point in points:
        keys(point, ('log_index', 'u', 'theta_natural'), 'POINT')
        li = point['log_index']
        need(type(li) is int and li >= 0 and li not in indices, 'UNIQUE_NONNEGATIVE_LOG_INDEX')
        indices.add(li)
        k = validate_point(point, dims, 'EXPORT')
        if li == h['log_index']:
            chosen.append((point, k))
    need(type(h['log_index']) is int, 'POINT_SELECTION_INTEGER')
    need(len(chosen) == 1, 'POINT_NOT_IN_ADMITTED_EXPORT')
    point, k = chosen[0]
    return point, k, {'kind': 'ADMITTED_EXPORT', 'export_pin': h['source_export_pin'], 'log_index': h['log_index']}


def phase1_point(h, policy, dims, synthetic):
    """A133 1.4: an S0 or F point from phase1_c2v001, selected by theta key; the S0 config names an admitted pair."""
    keys(h, COMMON_FIELDS + ('source_pin', 'point_key'), 'HANDOFF')
    src = load_pin(h['source_pin'], 'PHASE1_SOURCE')
    need(type(src) is dict and src.get('schema') in policy['phase1_source_lists'], 'PHASE1_SOURCE_SCHEMA')
    listname = policy['phase1_source_lists'][src['schema']]
    if src['schema'] == 'PHASE1_S0_C2V001':
        keys(src, ('schema', 'module', 'config', 'cache_id', 'points', 'note'), 'PHASE1_S0')
        config = load_pin(src['config'], 'CAMPAIGN_CONFIG')
        need(type(config) is dict and is_pin(config.get('coordinate_spec')) and is_pin(config.get('coordinate_spec_addendum')),
             'CAMPAIGN_CONFIG_COORDINATE_PINS')
        need(admitted_pair(policy, config['coordinate_spec'], config['coordinate_spec_addendum']),
             'CAMPAIGN_CONFIG_COORDINATE_PAIR_NOT_ADMITTED')
        need(type(config.get('synthetic_test')) is bool, 'CAMPAIGN_CONFIG_SYNTHETIC_FLAG')
        need(synthetic or config['synthetic_test'] is False, 'SYNTHETIC_CAMPAIGN_CANNOT_HAND_OFF_A_REAL_POINT')
        binding = {'kind': 'PHASE1_S0', 'source_pin': h['source_pin'], 'campaign_config': src['config']}
    else:
        need(type(src.get('snapshot_sha256')) is str and type(src.get('record_file_sha256')) is str, 'PHASE1_FDPLAN_BINDING')
        binding = {'kind': 'PHASE1_FD', 'source_pin': h['source_pin'], 'snapshot_sha256': src['snapshot_sha256'],
                   'record_file_sha256': src['record_file_sha256']}
    points = src.get(listname)
    need(type(points) is list and bool(points), 'NONEMPTY_PHASE1_POINTS')
    need(type(h['point_key']) is str and len(h['point_key']) == 64, 'POINT_KEY_HEX')
    seen, chosen = set(), []
    for point in points:
        need(type(point) is dict and {'u', 'theta_natural', 'key', 'role'} <= set(point), 'PHASE1_POINT_FIELDS')
        k = validate_point(point, dims, 'PHASE1')
        need(point['key'] == k, 'PHASE1_THETA_KEY_MISMATCH')
        if 'theta_hex' in point:
            need(point['theta_hex'] == {n: float(v).hex() for n, v in point['theta_natural'].items()}, 'PHASE1_THETA_HEX')
        need(k not in seen, 'PHASE1_DUPLICATE_THETA')
        seen.add(k)
        if k == h['point_key']:
            chosen.append(point)
    need(len(chosen) == 1, 'POINT_NOT_IN_PHASE1_SOURCE')
    binding.update(point_key=h['point_key'], role=chosen[0]['role'])
    return chosen[0], h['point_key'], binding


def prepare(handoff_path, expected_sha, synthetic_dry_only=False):
    handoff_pin = {'path': str(handoff_path), 'sha256': expected_sha}
    h = load_pin(handoff_pin, 'HANDOFF')
    need(type(h) is dict and h.get('schema') in (EXPORT_HANDOFF, PHASE1_HANDOFF), 'HANDOFF_SCHEMA')
    need(type(synthetic_dry_only) is bool, 'SYNTHETIC_FLAG_BOOL')
    real_mode = 'ADMITTED' if h['schema'] == EXPORT_HANDOFF else 'PHASE1_POINT'
    need(h.get('mode') == ('SYNTHETIC_DRY_ONLY' if synthetic_dry_only else real_mode), 'MODE_FENCE')
    keys(h.get('policy_pin'), ('path', 'sha256'), 'POLICY_PIN')
    need(h['policy_pin']['sha256'] == POLICY_SHA, 'POLICY_NOT_REGISTERED')
    policy = load_pin(h['policy_pin'], 'POLICY')
    coordinates = load_pin(policy['coordinates'], 'COORDINATES')
    slots = load_pin(policy['slots'], 'SLOTS')
    dims = engine_coordinates(policy, coordinates)
    if h['schema'] == EXPORT_HANDOFF:
        point, key, source = export_point(h, policy, dims)
    else:
        point, key, source = phase1_point(h, policy, dims, synthetic_dry_only)
    branch = h['driver_branch']
    need(type(branch) is str and branch in policy['drivers'], 'UNREGISTERED_DRIVER_BRANCH')
    selection = policy['drivers'][branch]
    keys(selection, ('driver', 'registry', 'acceptance'), 'DRIVER_SELECTION')
    load_pin(selection['driver'], 'DRIVER', decode=False)
    load_pin(selection['registry'], 'DRIVER_REGISTRY')
    if synthetic_dry_only:
        need(h['root_admission'] == 'SYNTHETIC_DRY_ONLY' and h['v007_adoption_pin'] is None and
             h['driver_acceptance_pin'] is None, 'SYNTHETIC_CANNOT_CLAIM_ADOPTION')
    else:
        want = policy['root_admission_required'] if h['schema'] == EXPORT_HANDOFF else policy['phase1_root_admission_required']
        need(h['root_admission'] == want, 'ROOT_ADMISSION_REQUIRED')
        load_pin(h['v007_adoption_pin'], 'V007_ADOPTION', decode=False)
        need(h['driver_acceptance_pin'] == selection['acceptance'], 'DRIVER_ACCEPTANCE_PIN')
        load_pin(h['driver_acceptance_pin'], 'DRIVER_ACCEPTANCE', decode=False)
    certs = h['certificate_pins']
    keys(certs, ('eps_certificate', 'lo_certificate'), 'CERTIFICATES')
    for kind, cert in certs.items():
        if cert != PENDING:
            need(not synthetic_dry_only, 'SYNTHETIC_CERTIFICATE_PROMOTION_REFUSED')
            load_pin(cert, kind, decode=False)
    theta = point['theta_natural']
    geometry = {s['name']: s['trial_value'] for s in slots['ngc3198_slots']}
    values = {'Eref_J': theta['Eref_base_J'], 'ell_F_m': theta['ell_F_m'],
              'gamma': theta['gamma_over_Eref'] * theta['Eref_base_J'],
              'common_scale_s': theta['common_scale_s'],
              'entropy_K_factor': theta['entropy_K_factor'],
              'distance_Mpc': geometry['ngc3198_distance_Mpc'],
              'inclination_deg': geometry['ngc3198_inclination_deg']}
    number(values['gamma'], 'DERIVED_GAMMA')
    payloads, records, specs = {}, [], {}
    for ident, template_pin in policy['templates'].items():
        t = load_pin(template_pin, ident)
        need(t['schema'] == 'UNT_STEP5_PARAMETERIZED_TEMPLATE_C2V001' and t['template_id'] == ident, 'TEMPLATE_ID')
        need(t['route'] == 'A', 'INTERFACE_A_ONLY')
        original = load_pin(t['source_spec_pin'], ident + '_SOURCE')
        load_pin(original['coefficients'], ident + '_GRID', decode=False)
        if 'source_slots' in original:
            for k, p in original['source_slots'].items():
                load_pin(p, k, decode=False)
        spec = copy.deepcopy(t['call_spec'])
        for field in spec['physical']:
            need(field in values, 'UNTRACEABLE_PHYSICAL_FIELD')
            spec['physical'][field] = values[field]
        spec['label'] = 'step5 %s theta_key=%s' % (t['label_template_id'], key)
        spec['numerics']['uv_tail'].update(certs)
        specs[ident] = spec
        name = 'CALL_%s_C2V001.json' % ident
        payloads[name] = encoded(spec)
        records.append({'file': name, 'sha256': sha(payloads[name]), 'template_pin': template_pin,
                        'route_a_column_workers': spec['numerics']['route_a']['column_workers'],
                        'role': t['identity_role'], 'physical_mapping': t['physical_mapping'],
                        'source_point': dict(source, theta_key=key, point_canonical_sha256=sha(canon(point))),
                        'all_other_values_from': {'call_spec': template_pin, 'geometry': policy['slots'], 'certificates': handoff_pin,
                                                  'label': 'template label id + the theta key recomputed from theta_natural'},
                        'outer_query_ids': t['outer_query_ids'], 'alternative_adoption_status': t['adoption_status']})
    pair = policy['identity_pair']
    keys(pair, ('call_of_record', 'twin', 'leaf', 'values'), 'IDENTITY_PAIR')
    need(set(specs) == {pair['call_of_record'], pair['twin']}, 'IDENTITY_PAIR_TEMPLATES')
    stripped = []
    for ident, want in zip((pair['call_of_record'], pair['twin']), pair['values']):
        s = copy.deepcopy(specs[ident])
        node = s
        for k in pair['leaf'][:-1]:
            node = node[k]
        need(node.pop(pair['leaf'][-1]) == want, 'IDENTITY_PAIR_LEAF_VALUE')
        stripped.append(canon(s))
    need(stripped[0] == stripped[1], 'IDENTITY_PAIR_DIFFERS_OUTSIDE_THE_LEAF')
    receipt = {'schema': 'UNT_STEP5_FILLED_SPECS_C2V001', 'date_u': datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),
               'mode': h['mode'], 'status': 'SYNTHETIC_DRY_ONLY' if synthetic_dry_only else 'POINT_BOUND_REQUIRES_CLAUDE2_PREFLIGHT',
               'launch_authorized': False, 'handoff_pin': handoff_pin, 'handoff_schema': h['schema'], 'policy_pin': h['policy_pin'],
               'driver_selection': selection, 'source': source, 'theta_key': key,
               'pending_certificates': [k for k, v in certs.items() if v == PENDING], 'outputs': records,
               'identity_pair': {'call_of_record': 'CALL_%s_C2V001.json' % pair['call_of_record'],
                                 'twin': 'CALL_%s_C2V001.json' % pair['twin'], 'leaf': pair['leaf'], 'values': pair['values'],
                                 'differs_only_in_leaf': True},
               'scope_limit': 'Custody and fixed mapping only; admission and certificate science are not established by this filler. '
                              'Exact dry-plan and root preflight still required. The twin exists only for the A132/A133 serial = '
                              'parallel identity test; its values are never read.'}
    payloads['FILL_RECEIPT_C2V001.json'] = encoded(receipt)
    return payloads, receipt


def fill(handoff_path, expected_sha, output_dir, synthetic_dry_only=False):
    payloads, receipt = prepare(handoff_path, expected_sha, synthetic_dry_only)
    out = safe_path(str(output_dir))
    need(not out.exists(), 'OUTPUT_DIRECTORY_EXISTS')
    need(out.parent.is_dir(), 'OUTPUT_PARENT_REQUIRED')
    out.mkdir(exist_ok=False)
    for name, b in payloads.items():
        with (out / name).open('xb') as f:
            f.write(b)
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--handoff', required=True)
    p.add_argument('--expected-sha256', required=True)
    p.add_argument('--output-dir', required=True)
    p.add_argument('--synthetic-dry-only', action='store_true')
    a = p.parse_args()
    try:
        result = fill(a.handoff, a.expected_sha256, a.output_dir, a.synthetic_dry_only)
    except (Refusal, OSError, KeyError, TypeError, json.JSONDecodeError) as e:
        p.exit(2, 'REFUSED: %s\n' % e)
    print(json.dumps({'status': result['status'], 'launch_authorized': False, 'outputs': len(result['outputs'])}))


if __name__ == '__main__':
    main()
