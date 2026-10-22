"""Target-free, exclusive step-5 spec filler. Does not launch or infer admission.

The expected handoff digest must come from Claude2, not from this tool's own
calculation. The synthetic fixture exercises custody only and is never admitted.
"""
import argparse
import copy
import datetime
import hashlib
import json
import math
from pathlib import Path

POLICY_SHA = '4f0d7d039fcee03fc9e2e1c74624919c77b14e19b101389124864219057e5bbf'
PENDING = 'PENDING_UV_TAIL_CERTIFICATE'


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


def validate_points(export, coordinates):
    points = export['admitted_points']
    need(type(points) is list and bool(points), 'NONEMPTY_ADMITTED_POINTS')
    dims = coordinates['engine_coordinates']
    names = {c['name'] for c in dims}
    nvary = sum(c['role'] != 'fixed' for c in dims)
    indices = set()
    for point in points:
        keys(point, ('log_index', 'u', 'theta_natural'), 'POINT')
        li = point['log_index']
        need(type(li) is int and li >= 0 and li not in indices, 'UNIQUE_NONNEGATIVE_LOG_INDEX')
        indices.add(li)
        u = point['u']
        need(type(u) is list and len(u) == nvary, 'VARYING_U_LENGTH')
        for value in u:
            need(0 <= number(value, 'U') <= 1, 'U_BOUNDS')
        theta = point['theta_natural']
        need(type(theta) is dict and set(theta) == names, 'EXACT_ENGINE_COORDINATES')
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
            need(math.isclose(value, expected, rel_tol=1e-12, abs_tol=0.0),
                 'U_THETA_MISMATCH_' + c['name'])
    return points


def prepare(handoff_path, expected_sha, synthetic_dry_only=False):
    handoff_pin = {'path': str(handoff_path), 'sha256': expected_sha}
    h = load_pin(handoff_pin, 'HANDOFF')
    keys(h, ('schema', 'mode', 'source_export_pin', 'log_index', 'policy_pin',
             'driver_branch', 'driver_acceptance_pin', 'v007_adoption_pin',
             'root_admission', 'certificate_pins'), 'HANDOFF')
    need(h['schema'] == 'UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001', 'HANDOFF_SCHEMA')
    need(type(synthetic_dry_only) is bool, 'SYNTHETIC_FLAG_BOOL')
    need(h['mode'] == ('SYNTHETIC_DRY_ONLY' if synthetic_dry_only else 'ADMITTED'), 'MODE_FENCE')
    keys(h['policy_pin'], ('path', 'sha256'), 'POLICY_PIN')
    need(h['policy_pin']['sha256'] == POLICY_SHA, 'POLICY_NOT_REGISTERED')
    policy = load_pin(h['policy_pin'], 'POLICY')
    coordinates = load_pin(policy['coordinates'], 'COORDINATES')
    slots = load_pin(policy['slots'], 'SLOTS')
    export = load_pin(h['source_export_pin'], 'EXPORT')
    keys(export, ('schema', 'mode', 'target_free', 'coordinate_pin', 'admitted_points'), 'EXPORT')
    need(export['schema'] == 'UNT_STEP4_TARGET_FREE_ADMITTED_EXPORT_CX3V001', 'EXPORT_SCHEMA')
    need(export['mode'] == h['mode'] and export['target_free'] is True, 'EXPORT_TARGET_FREE_MODE')
    need(export['coordinate_pin'] == policy['coordinates'], 'EXPORT_COORDINATE_BINDING')
    points = validate_points(export, coordinates)
    need(type(h['log_index']) is int, 'POINT_SELECTION_INTEGER')
    matches = [p for p in points if p['log_index'] == h['log_index']]
    need(len(matches) == 1, 'POINT_NOT_IN_ADMITTED_EXPORT')
    point = matches[0]
    branch = h['driver_branch']
    need(type(branch) is str and branch in policy['drivers'], 'UNREGISTERED_DRIVER_BRANCH')
    selection = policy['drivers'][branch]
    load_pin(selection['driver'], 'DRIVER', decode=False)
    load_pin(selection['registry'], 'DRIVER_REGISTRY')
    if synthetic_dry_only:
        need(h['root_admission'] == 'SYNTHETIC_DRY_ONLY' and h['v007_adoption_pin'] is None and
             h['driver_acceptance_pin'] is None, 'SYNTHETIC_CANNOT_CLAIM_ADOPTION')
    else:
        need(h['root_admission'] == policy['root_admission_required'], 'ROOT_STEP4_ADMISSION_REQUIRED')
        load_pin(h['v007_adoption_pin'], 'V007_ADOPTION', decode=False)
        if branch == 'r007':
            load_pin(h['driver_acceptance_pin'], 'R007_ACCEPTANCE', decode=False)
        else:
            need(h['driver_acceptance_pin'] is None, 'FALLBACK_ACCEPTANCE_FIELD_MUST_BE_NULL')
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
    payloads = {}
    records = []
    for ident, template_pin in policy['templates'].items():
        t = load_pin(template_pin, ident)
        need(t['template_id'] == ident, 'TEMPLATE_ID')
        original = load_pin(t['source_spec_pin'], ident + '_SOURCE')
        load_pin(original['coefficients'], ident + '_GRID', decode=False)
        if 'source_slots' in original:
            for k, p in original['source_slots'].items():
                load_pin(p, k, decode=False)
        spec = copy.deepcopy(t['call_spec'])
        for field in spec['physical']:
            need(field in values, 'UNTRACEABLE_PHYSICAL_FIELD')
            spec['physical'][field] = values[field]
        spec['label'] = 'step5 %s log_index=%d handoff=%s %s' % (ident, h['log_index'], expected_sha[:16], h['mode'])
        spec['numerics']['uv_tail'].update(certs)
        name = 'CALL_%s_CX3V001.json' % ident
        payloads[name] = encoded(spec)
        records.append({'file': name, 'sha256': sha(payloads[name]), 'template_pin': template_pin,
                        'physical_mapping': t['physical_mapping'], 'source_point': {'export_pin': h['source_export_pin'], 'log_index': h['log_index'], 'point_canonical_sha256': sha(canon(point))},
                        'all_other_values_from': {'call_spec': template_pin, 'geometry': policy['slots'], 'certificates': handoff_pin, 'label': 'deterministic template ID + selected log_index + externally supplied handoff SHA + mode'},
                        'outer_query_ids': t['outer_query_ids'], 'alternative_adoption_status': t['adoption_status']})
    receipt = {'schema': 'UNT_STEP5_FILLED_SPECS_CX3V001', 'date_u': datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),
               'mode': h['mode'], 'status': 'SYNTHETIC_DRY_ONLY' if synthetic_dry_only else 'POINT_BOUND_REQUIRES_CLAUDE2_PREFLIGHT',
               'launch_authorized': False, 'handoff_pin': handoff_pin, 'policy_pin': h['policy_pin'], 'driver_selection': selection,
               'pending_certificates': [k for k, v in certs.items() if v == PENDING], 'outputs': records,
               'scope_limit': 'Custody and fixed mapping only; admission and certificate science are not established by this filler. Exact dry-plan and root preflight still required.'}
    payloads['FILL_RECEIPT_CX3V001.json'] = encoded(receipt)
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
