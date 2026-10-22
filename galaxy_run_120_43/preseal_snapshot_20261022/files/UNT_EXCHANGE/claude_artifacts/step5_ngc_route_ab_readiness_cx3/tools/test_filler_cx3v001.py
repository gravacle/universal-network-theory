"""Synthetic adversarial custody/mapping tests; no scientific drivers are imported."""
import copy
import datetime
import hashlib
import json
from pathlib import Path
import resource
import runpy

D = Path(__file__).resolve().parent.parent
M = runpy.run_path(str(D / 'tools/fill_step5_cx3v002.py'), run_name='cx3_step5_test')
F = D / 'synthetic/negative_fixtures_v001'
F.mkdir(exist_ok=False)
H = json.loads((D / 'synthetic/SYNTHETIC_HANDOFF_CX3V001.json').read_bytes())
E = json.loads((D / 'synthetic/SYNTHETIC_EXPORT_CX3V001.json').read_bytes())
checks = []


def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def wx(name, obj):
    p = F / (name + '.json')
    with p.open('xb') as f:
        f.write(M['encoded'](obj))
    return pin(p)


def record(name, passed, observed):
    checks.append({'name': name, 'passed': bool(passed), 'observed': observed})


def reject(name, mutate_h=None, mutate_e=None, message=None, synthetic=True, expected_override=None):
    h = copy.deepcopy(H)
    if mutate_e:
        e = copy.deepcopy(E); mutate_e(e)
        h['source_export_pin'] = wx(name + '_export', e)
    if mutate_h:
        mutate_h(h)
    p = wx(name + '_handoff', h)
    try:
        M['prepare'](p['path'], expected_override or p['sha256'], synthetic)
        record(name, False, 'ACCEPTED')
    except Exception as exc:
        record(name, isinstance(exc, M['Refusal']) and (message is None or message in str(exc)), type(exc).__name__ + ': ' + str(exc))


hp = pin(D / 'synthetic/SYNTHETIC_HANDOFF_CX3V001.json')
payloads, receipt = M['prepare'](hp['path'], hp['sha256'], True)
record('four_templates_filled', len(receipt['outputs']) == 4, list(payloads))
record('synthetic_launch_fence', receipt['mode'] == 'SYNTHETIC_DRY_ONLY' and receipt['launch_authorized'] is False, receipt['status'])
record('certificates_remain_pending', set(receipt['pending_certificates']) == {'eps_certificate', 'lo_certificate'}, receipt['pending_certificates'])
theta = E['admitted_points'][0]['theta_natural']
for rec in receipt['outputs']:
    spec = json.loads(payloads[rec['file']]); t = M['load_pin'](rec['template_pin'], 'TEST_TEMPLATE')
    original = M['load_pin'](t['source_spec_pin'], 'TEST_SOURCE')
    for obj in (spec, original):
        obj.pop('physical'); obj.pop('label')
    record('fixed_bytes_mapping_' + rec['file'], spec == original, 'All fields other than declared physical mapping and label equal registered source JSON')
    s = json.loads(payloads[rec['file']])
    record('gamma_and_geometry_' + rec['file'], s['physical']['gamma'] == theta['gamma_over_Eref'] * theta['Eref_base_J'] and s['physical']['distance_Mpc'] == 13.8 and s['physical']['inclination_deg'] == 72 and s['physical']['distance_Mpc'] != theta['distance_Mpc'], s['physical'])
    record('point_custody_' + rec['file'], rec['source_point']['export_pin'] == H['source_export_pin'] and rec['source_point']['point_canonical_sha256'] == hashlib.sha256(M['canon'](E['admitted_points'][0])).hexdigest(), rec['source_point'])

reject('wrong_expected_handoff_pin', expected_override='0'*64, message='BYTE_PIN_HANDOFF')
reject('default_refuses_synthetic_as_admitted', synthetic=False, message='MODE_FENCE')
reject('unknown_handoff_field', lambda h: h.update(gamma=123), message='EXACT_FIELDS_HANDOFF')
reject('missing_handoff_field', lambda h: h.pop('log_index'), message='EXACT_FIELDS_HANDOFF')
reject('wrong_schema', lambda h: h.update(schema='FAKE'), message='HANDOFF_SCHEMA')
reject('unknown_point', lambda h: h.update(log_index=999), message='POINT_NOT_IN_ADMITTED_EXPORT')
reject('boolean_point_selection', lambda h: h.update(log_index=False), message='POINT_SELECTION_INTEGER')
reject('unregistered_driver', lambda h: h.update(driver_branch='r999'), message='UNREGISTERED_DRIVER_BRANCH')
reject('tampered_policy_sha', lambda h: h['policy_pin'].update(sha256='0'*64), message='POLICY_NOT_REGISTERED')
reject('malformed_policy_pin', lambda h: h.update(policy_pin=[]), message='EXACT_FIELDS_POLICY_PIN')
reject('bad_export_pin', lambda h: h['source_export_pin'].update(sha256='0'*64), message='BYTE_PIN_EXPORT')
reject('protected_run_before_read', lambda h: h['source_export_pin'].update(path='/Volumes/External1/prohibited/runs_ext/UVT_NEVER_OPEN/result.json'), message='PROTECTED_RUN_PATH')
reject('observed_target_before_read', lambda h: h['source_export_pin'].update(path='/Users/bgm/NGC3198_observed_velocities.json'), message='NGC_TARGET_PATH')
reject('synthetic_false_adoption', lambda h: h.update(root_admission='STEP4_ADMITTED_UNDER_ADOPTED_V007'), message='SYNTHETIC_CANNOT_CLAIM_ADOPTION')
reject('synthetic_certificate_promotion', lambda h: h['certificate_pins'].update(lo_certificate=h['source_export_pin']), message='SYNTHETIC_CERTIFICATE_PROMOTION_REFUSED')
reject('certificate_extra_field', lambda h: h['certificate_pins'].update(gq_certificate='PASS'), message='EXACT_FIELDS_CERTIFICATES')
reject('export_unknown_field', mutate_e=lambda e: e.update(velocities=[1]), message='EXACT_FIELDS_EXPORT')
reject('export_not_target_free', mutate_e=lambda e: e.update(target_free=False), message='EXPORT_TARGET_FREE_MODE')
reject('export_wrong_coordinate_pin', mutate_e=lambda e: e['coordinate_pin'].update(sha256='0'*64), message='EXPORT_COORDINATE_BINDING')
reject('empty_admitted_points', mutate_e=lambda e: e.update(admitted_points=[]), message='NONEMPTY_ADMITTED_POINTS')
reject('duplicated_admitted_log_index', mutate_e=lambda e: e['admitted_points'].append(copy.deepcopy(e['admitted_points'][0])), message='UNIQUE_NONNEGATIVE_LOG_INDEX')
reject('negative_log_index', mutate_e=lambda e: e['admitted_points'][0].update(log_index=-1), message='UNIQUE_NONNEGATIVE_LOG_INDEX')
reject('point_unknown_field', mutate_e=lambda e: e['admitted_points'][0].update(override=1), message='EXACT_FIELDS_POINT')
reject('missing_coordinate', mutate_e=lambda e: e['admitted_points'][0]['theta_natural'].pop('native_Ud'), message='EXACT_ENGINE_COORDINATES')
reject('boolean_coordinate', mutate_e=lambda e: e['admitted_points'][0]['theta_natural'].update(common_scale_s=True), message='FINITE_REAL_common_scale_s')
reject('non_numeric_coordinate', mutate_e=lambda e: e['admitted_points'][0]['theta_natural'].update(common_scale_s='0.1'), message='FINITE_REAL_common_scale_s')
reject('out_of_bounds_coordinate', mutate_e=lambda e: e['admitted_points'][0]['theta_natural'].update(common_scale_s=10), message='THETA_BOUNDS_common_scale_s')
reject('changed_fixed_coordinate', mutate_e=lambda e: e['admitted_points'][0]['theta_natural'].update(native_Ud=1.5), message='FIXED_THETA_CHANGED_native_Ud')
reject('wrong_u_dimension', mutate_e=lambda e: e['admitted_points'][0]['u'].append(0.5), message='VARYING_U_LENGTH')
reject('out_of_bounds_u', mutate_e=lambda e: e['admitted_points'][0]['u'].__setitem__(0,2), message='U_BOUNDS')
reject('boolean_u', mutate_e=lambda e: e['admitted_points'][0]['u'].__setitem__(0,False), message='FINITE_REAL_U')
reject('untraceable_theta_u_pair', mutate_e=lambda e: e['admitted_points'][0]['u'].__setitem__(0,0.1), message='U_THETA_MISMATCH_common_scale_s')
reject('tiny_gamma_cannot_hide_in_absolute_tolerance', mutate_e=lambda e: e['admitted_points'][0]['u'].__setitem__(1,0.1), message='U_THETA_MISMATCH_gamma_over_Eref')
for name, raw, expected in [('duplicate_json_key', b'{"a":1,"a":2}', 'DUPLICATE_JSON_KEY'), ('nonfinite_json', b'{"a":NaN}', 'NONFINITE_JSON')]:
    try:
        M['parse'](raw); record(name, False, 'ACCEPTED')
    except M['Refusal'] as exc:
        record(name, expected in str(exc), str(exc))

existing = D / 'synthetic/filled_v001'
before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in existing.iterdir()}
try:
    M['fill'](hp['path'], hp['sha256'], str(existing), True); record('exclusive_output_directory', False, 'ACCEPTED')
except M['Refusal'] as exc:
    record('exclusive_output_directory', 'OUTPUT_DIRECTORY_EXISTS' in str(exc), str(exc))
after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in existing.iterdir()}
record('existing_outputs_unchanged', before == after, before)
missing_output = D / 'synthetic/must_not_exist_after_refusal'
try:
    M['fill'](hp['path'], '0'*64, str(missing_output), True)
except M['Refusal']:
    pass
record('validation_before_any_output', not missing_output.exists(), str(missing_output))

result = {'schema': 'UNT_STEP5_FILLER_TESTS_CX3V001', 'date_u': datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),
          'filler_pin': pin(D / 'tools/fill_step5_cx3v002.py'), 'status': 'TESTED_PASS' if all(x['passed'] for x in checks) else 'TESTED_FAIL',
          'checks': checks, 'passed': sum(x['passed'] for x in checks), 'total': len(checks),
          'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'scope': 'All inputs synthetic. Actual step4/V007 admission, certificate truth and scientific launches UNTESTED.'}
with (D / 'FILLER_TESTS_CX3V001.json').open('x') as f:
    json.dump(result, f, indent=2, sort_keys=True); f.write('\n')
print(json.dumps({k: result[k] for k in ('status', 'passed', 'total', 'peak_rss_bytes')}))
assert result['passed'] == result['total']
