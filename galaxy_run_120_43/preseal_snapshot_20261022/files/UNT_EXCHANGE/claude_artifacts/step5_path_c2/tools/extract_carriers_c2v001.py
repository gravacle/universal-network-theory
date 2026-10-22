"""Extract target-free pre-freeze carriers from pinned saved records; never launch.

c2v001 = extract_carriers_cx3v005 (50c7db5f) with one change (RI45-08 (a), A103): POLICY_SHA names
POLICY_CARRIERS_C2V001, whose driver, registry and adoption review are cx3r008 (577f8c94, 2c3f421d,
7ff20c1d). Every other byte is unchanged.

The request SHA must come from the root caller. Optional carrier contracts need
root registration. Missing records remain UNAVAILABLE; no scientific inference
or post-target selection is performed.
"""
import argparse
import datetime
import hashlib
import json
import math
from pathlib import Path

POLICY_SHA = 'aa50c752329b383758d09b1c2ab9724b4db29fd5121881167a6ae2745141362a'
MAX_BYTES = 128 * 1024**2
ROLES = ('model_readout', 'original_k_readout', 'ntest_compare', 'tsr_support', 'newtonian_reference', 'a17_c3_record')


class Refusal(ValueError):
    pass


def require(test, code):
    if not test:
        raise Refusal(code)


def fields(obj, names, where):
    require(type(obj) is dict and set(obj) == set(names), 'EXACT_FIELDS ' + where)


def finite(v, where):
    require(type(v) in (int, float), 'FINITE_REAL ' + where)
    try:
        f = float(v)
    except (OverflowError, ValueError):
        raise Refusal('FINITE_REAL ' + where) from None
    require(math.isfinite(f), 'FINITE_REAL ' + where)
    return f


def hexsha(v, where):
    require(type(v) is str and len(v) == 64 and all(c in '0123456789abcdef' for c in v), 'SHA256 ' + where)


def safe_path(s):
    require(type(s) is str and Path(s).is_absolute(), 'ABSOLUTE_PATH')
    p = Path(s)
    def check(x):
        t = str(x).lower()
        require('/runs_ext/uvt_' not in t and 'kmax_a2f10_c5h_run_v001' not in t, 'PROTECTED_RUN_PATH')
        require('/.codex/' not in t and '/.codex-alt/' not in t, 'SESSION_PATH')
        if 'ngc3198' in t:
            t = t.replace('target_free', '').replace('target-free', '')
            require(not any(k in t for k in ('observed', 'velocit', 'rotmod', 'target')), 'NGC_TARGET_PATH')
    check(p)  # Lexical rejection before touching even path metadata.
    check(p.resolve())
    return p


def sha(b):
    return hashlib.sha256(b).hexdigest()


def encode(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()


def strict_json(b, filename):
    class Pairs(list):
        pass
    def constant(v):
        raise Refusal('NONFINITE_JSON file=' + filename + ' token=' + v)
    def walk(x, path):
        if isinstance(x, Pairs):
            out, positions = {}, {}
            for i, (k, v) in enumerate(x):
                if k in out:
                    raise Refusal('DUPLICATE_KEY file=%s path=%s key=%r first_pair=%d second_pair=%d' % (filename, path, k, positions[k], i))
                positions[k] = i
                out[k] = walk(v, path + '[' + json.dumps(k) + ']')
            return out
        if isinstance(x, list):
            return [walk(v, path + '[%d]' % i) for i, v in enumerate(x)]
        return x
    try:
        return walk(json.loads(b, object_pairs_hook=Pairs, parse_constant=constant), '$')
    except (json.JSONDecodeError, UnicodeError, RecursionError) as e:
        raise Refusal('JSON_RECORD file=%s %s' % (filename, type(e).__name__)) from None


def read_pin(pin, where, parse=True):
    fields(pin, ('path', 'sha256'), where + '_PIN')
    hexsha(pin['sha256'], where)
    p = safe_path(pin['path'])
    require(p.stat().st_size <= MAX_BYTES, 'INPUT_SIZE_CAP ' + where)
    b = p.read_bytes()
    require(len(b) <= MAX_BYTES and sha(b) == pin['sha256'], 'BYTE_PIN ' + where)
    return strict_json(b, str(p)) if parse else b


def unavailable(reason, **extra):
    return dict(status='UNAVAILABLE', reason=reason, **extra)


def validate_rows(rows, ids, where, strict_keys=False):
    require(type(rows) is list and len(rows) == len(ids), 'ROW_COUNT ' + where)
    out = []
    for row, ident in zip(rows, ids):
        require(type(row) is dict, 'ROW_OBJECT ' + where)
        if strict_keys:
            fields(row, ('id', 'speed_km_s', 'valid', 'reason'), where + '_ROW')
        require(row.get('id') == ident, 'ROW_ID_ORDER ' + where)
        valid = row.get('valid', True)
        require(type(valid) is bool, 'ROW_VALID_BOOL ' + where)
        speed = row.get('speed_km_s')
        if valid:
            finite(speed, where + '.' + ident)
        else:
            require(speed is None, 'INVALID_SPEED_MUST_BE_NULL ' + where)
            require(type(row.get('reason')) is str and bool(row['reason']), 'INVALID_REASON ' + where)
        out.append({'id': ident, 'speed_km_s': speed, 'valid': valid, 'reason': row.get('reason')})
    return out


def readout(binding, ids, driver, where, mode):
    if binding is None:
        return unavailable('NO_SAVED_ROUTE_B_READOUT', rows=None, call_spec_pin=None), None
    fields(binding, ('result', 'finish', 'call_spec'), where + '_BINDING')
    result = read_pin(binding['result'], where + '_RESULT')
    finish = read_pin(binding['finish'], where + '_FINISH')
    spec = read_pin(binding['call_spec'], where + '_CALL')
    require(type(result) is dict and type(finish) is dict and type(spec) is dict, 'RECORD_OBJECT ' + where)
    require(not result.get('synthetic_fixture') or mode == 'SYNTHETIC', 'SYNTHETIC_RESULT_FENCE ' + where)
    require(spec.get('galaxy') == 'NGC3198', 'CALL_GALAXY ' + where)
    require(spec.get('schema') in ('UNT_GALAXY_M0_FORWARD_CALL_C2V001','UNT_GALAXY_M0_FORWARD_CALL_NGC_C2V002'), 'CALL_SCHEMA ' + where)
    require(type(spec.get('physical')) is dict and type(spec.get('coefficients')) is dict, 'CALL_PHYSICAL_COEFFICIENT_OBJECT ' + where)
    for key in ('Eref_J','gamma','ell_F_m','common_scale_s','distance_Mpc','inclination_deg'):
        finite(spec['physical'].get(key), 'CALL_' + key)
    if 'entropy_K_factor' in spec['physical']:
        finite(spec['physical']['entropy_K_factor'], 'CALL_entropy_K_factor')
    require(result.get('driver_sha256') == driver['sha256'], 'DRIVER_CUSTODY ' + where)
    require(result.get('call_spec_sha256') == binding['call_spec']['sha256'], 'CALL_CUSTODY ' + where)
    require(finish.get('result_sha256') == binding['result']['sha256'], 'FINISH_RESULT_SHA ' + where)
    require(type(result.get('status')) is str and bool(result['status']) and finish.get('status') == result['status'], 'FINISH_STATUS ' + where)
    require(type(result.get('valid')) is bool and finish.get('valid') is result['valid'], 'FINISH_VALIDITY ' + where)
    rows = result.get('rows')
    if rows is not None:
        rows = validate_rows(rows, ids, where)
    available = result['status'] == 'COMPLETED' and result['valid'] is True and rows is not None
    rec = dict(status='AVAILABLE' if available else 'UNAVAILABLE', reason=None if available else 'READOUT_NOT_VALID_COMPLETED',
               source_binding=binding, call_spec_pin=binding['call_spec'], source_status=result['status'], source_valid=result['valid'],
               rows=rows, result_reasons=result.get('reasons', []), native_pointer='/rows',
               scope='Saved conditional model rows only; not calibration admission.')
    return rec, spec


def common_carrier(rec, schema, mode, point, slots_pin):
    require(rec.get('schema') == schema, 'CARRIER_SCHEMA')
    require(rec.get('mode') == mode and rec.get('target_free') is True and rec.get('before_target_access') is True, 'CARRIER_SCOPE')
    require(rec.get('point_key') == point and point is not None, 'CARRIER_POINT_BINDING')
    require(rec.get('slots_pin') == slots_pin, 'CARRIER_SLOTS_BINDING')


def extract(request_path, expected_sha, synthetic=False):
    req_pin = {'path': str(request_path), 'sha256': expected_sha}
    req = read_pin(req_pin, 'REQUEST')
    fields(req, ('schema', 'mode', 'target_free', 'before_target_access', 'policy_pin', 'point_key', 'inputs'), 'REQUEST')
    require(req['schema'] == 'UNT_STEP5_CARRIER_REQUEST_CX3V001', 'REQUEST_SCHEMA')
    mode = 'SYNTHETIC' if synthetic else 'SAVED_TARGET_FREE'
    require(req['mode'] == mode and req['target_free'] is True and req['before_target_access'] is True, 'REQUEST_SCOPE')
    fields(req['policy_pin'], ('path', 'sha256'), 'POLICY_PIN')
    require(req['policy_pin']['sha256'] == POLICY_SHA, 'REGISTERED_POLICY')
    policy = read_pin(req['policy_pin'], 'POLICY')
    read_pin(policy['driver'], 'DRIVER', parse=False)
    read_pin(policy['registry'], 'DRIVER_REGISTRY')
    slots = read_pin(policy['slots'], 'SLOTS')
    queries = slots['query_block']['rows']
    ids = [q['query_id'] for q in queries]
    require(ids == ['NGC3198-Q%02d' % i for i in range(1, 44)], 'REGISTERED_43_IDS')
    radii = {q['query_id']: finite(q['radius_kpc'], 'QUERY_RADIUS') for q in queries}
    fields(req['inputs'], ROLES, 'INPUT_ROLES')
    sources = req['inputs']
    point = req['point_key']
    if point is not None:
        hexsha(point, 'POINT_KEY')
    if any(sources[k] is not None for k in ('model_readout', 'original_k_readout', 'tsr_support', 'newtonian_reference', 'a17_c3_record')):
        require(point is not None, 'POINT_KEY_REQUIRED')
    model, mspec = readout(sources['model_readout'], ids, policy['driver'], 'MODEL', mode)
    original, ospec = readout(sources['original_k_readout'], ids, policy['driver'], 'ORIGINAL_K', mode)
    if mspec is not None:
        require(mspec.get('physical', {}).get('entropy_K_factor', 64/121) == 64/121, 'HEADLINE_ENTROPY')
    if ospec is not None:
        require(ospec.get('physical', {}).get('entropy_K_factor') == 1.0, 'ORIGINAL_K_ENTROPY')
        if mspec is not None:
            mp = {k:v for k,v in mspec['physical'].items() if k != 'entropy_K_factor'}
            op = {k:v for k,v in ospec['physical'].items() if k != 'entropy_K_factor'}
            require(mp == op and mspec['coefficients'] == ospec['coefficients'], 'ORIGINAL_K_SHARED_POINT_GRID')
    compare, rings = None, []
    if sources['ntest_compare'] is not None:
        compare = read_pin(sources['ntest_compare'], 'NTEST_COMPARE')
        require(type(compare) is dict and compare.get('schema') == 'NGC_NTEST_COMPARE_C2V002' and type(compare.get('tests_read')) is bool, 'NTEST_RECORD')
        rows = compare.get('failing_TRUNCATION_SHAPE_rings')
        require(type(rows) is list, 'NTEST_FAILING_RING_LIST')
        # Preserve the exact native evidence. No support interpretation occurs here.
        rings = rows
        ordinals = set()
        for ring in rings:
            require(type(ring) is dict and type(ring.get('ordinal')) is int and ring['ordinal'] >= 0 and ring['ordinal'] not in ordinals, 'NTEST_RING_ORDINAL')
            ordinals.add(ring['ordinal'])
            require(ring.get('classification') == 'TRUNCATION_SHAPE', 'NTEST_RING_CLASS')
            require(finite(ring.get('S_over_theta'), 'RING_S_OVER_THETA') >= 0 and finite(ring.get('R_kpc'), 'RING_RADIUS') >= 0, 'NTEST_RING_NONNEGATIVE')
            require(type(ring.get('radial_support')) is dict, 'NTEST_NATIVE_SUPPORT')
    tsr = unavailable('ROOT_TSR_FLAG_AND_RADIAL_SUPPORT_RULE_NOT_SUPPLIED', source_compare_pin=sources['ntest_compare'],
                      native_failing_rings=rings, support_rule=None, rows=[{'query_id':i, 'radius_kpc':radii[i], 'TRUNCATION_SHAPE_RESIDUAL':None, 'ring_evidence':None} for i in ids])
    if sources['tsr_support'] is not None:
        support = read_pin(sources['tsr_support'], 'TSR_SUPPORT')
        fields(support, ('schema','mode','target_free','before_target_access','point_key','slots_pin','ntest_compare_pin','rule_id','rings'), 'TSR_SUPPORT')
        common_carrier(support, 'UNT_ROOT_TSR_SUPPORT_CX3V001', mode, point, policy['slots'])
        require(compare is not None and support['ntest_compare_pin'] == sources['ntest_compare'], 'TSR_COMPARE_BINDING')
        require(compare['tests_read'] is True, 'TSR_UNREAD_NTEST_RECORD')
        require(type(support['rule_id']) is str and bool(support['rule_id']), 'TSR_RULE_ID_REQUIRED')
        require(type(support['rings']) is list and len(support['rings']) == len(rings), 'TSR_RING_COVERAGE')
        evidence = []
        for s, native in zip(support['rings'], rings):
            fields(s, ('native_ring','lower_kpc','upper_kpc','lower_inclusive','upper_inclusive'), 'TSR_RING')
            require(encode(s['native_ring']) == encode(native), 'TSR_NATIVE_EVIDENCE_BINDING')
            lo, hi = finite(s['lower_kpc'],'SUPPORT_LO'), finite(s['upper_kpc'],'SUPPORT_HI')
            require(0 <= lo <= hi and type(s['lower_inclusive']) is bool and type(s['upper_inclusive']) is bool, 'TSR_SUPPORT_DOMAIN')
            radius = native['R_kpc']
            require((radius >= lo if s['lower_inclusive'] else radius > lo) and (radius <= hi if s['upper_inclusive'] else radius < hi), 'TSR_SUPPORT_EXCLUDES_NATIVE_RING')
            evidence.append(s)
        tsr.update(status='AVAILABLE', reason=None, support_rule={'pin':sources['tsr_support'],'rule_id':support['rule_id']})
        for row in tsr['rows']:
            r = row['radius_kpc']; hit = [s for s in evidence if (r >= s['lower_kpc'] if s['lower_inclusive'] else r > s['lower_kpc']) and (r <= s['upper_kpc'] if s['upper_inclusive'] else r < s['upper_kpc'])]
            row.update(TRUNCATION_SHAPE_RESIDUAL=bool(hit), ring_evidence=hit)
    tsr['disclosure_only_not_INVALID'] = True
    tsr['ntest_state'] = None if compare is None else {k:compare.get(k) for k in ('outcome','tests_read','n_route_ab_gate','n_route_ab_reason_codes')}
    newtonian = unavailable('NO_PRE_FREEZE_BARYONIC_NEWTONIAN_CARRIER', rows=None)
    if sources['newtonian_reference'] is not None:
        n = read_pin(sources['newtonian_reference'], 'NEWTONIAN')
        fields(n, ('schema','mode','target_free','before_target_access','point_key','slots_pin','model_call_spec_pin','units','baryonic_definition','producer_pin','rows'), 'NEWTONIAN')
        common_carrier(n, 'UNT_ROOT_BARYONIC_NEWTONIAN_CX3V001', mode, point, policy['slots'])
        require(model['call_spec_pin'] is not None and n['model_call_spec_pin'] == model['call_spec_pin'], 'NEWTONIAN_CALL_BINDING')
        require(n['units'] == 'km/s' and type(n['baryonic_definition']) is str and bool(n['baryonic_definition']), 'NEWTONIAN_DEFINITION_UNITS')
        read_pin(n['producer_pin'], 'NEWTONIAN_PRODUCER', parse=False)
        nr = validate_rows(n['rows'], ids, 'NEWTONIAN', strict_keys=True)
        newtonian = dict(status='AVAILABLE', reason=None, source_pin=sources['newtonian_reference'], units='km/s',
                         baryonic_definition=n['baryonic_definition'], producer_pin=n['producer_pin'], rows=nr)
    e1b = dict(status='AVAILABLE' if model['status']=='AVAILABLE' and newtonian['status']=='AVAILABLE' else 'UNAVAILABLE',
               model=model, baryonic_newtonian=newtonian, inner_query_ids=ids[:24], comparison=None,
               scope='Per-point raw target-free model pair, not a headline envelope or target residual.')
    if e1b['status'] == 'AVAILABLE':
        e1b['comparison'] = [{'query_id':m['id'], 'status':'AVAILABLE' if m['valid'] and n['valid'] else 'UNAVAILABLE',
                             'model_exceeds_newtonian':m['speed_km_s'] > n['speed_km_s'] if m['valid'] and n['valid'] else None}
                            for m,n in zip(model['rows'][:24],newtonian['rows'][:24])]
    c3 = unavailable('NO_ROOT_PINNED_A17_C3_RECORD', record_pin=None, payload=None)
    if sources['a17_c3_record'] is not None:
        c = read_pin(sources['a17_c3_record'], 'C3_REGISTRATION')
        fields(c, ('schema','mode','target_free','before_target_access','point_key','slots_pin','original_k_call_spec_pin','record_pin'), 'C3_REGISTRATION')
        common_carrier(c, 'UNT_ROOT_A17_C3_REGISTRATION_CX3V001', mode, point, policy['slots'])
        require(original['call_spec_pin'] is not None and c['original_k_call_spec_pin'] == original['call_spec_pin'], 'C3_ORIGINAL_K_CALL_BINDING')
        payload = read_pin(c['record_pin'], 'A17_C3_RECORD')
        require(type(payload) is dict, 'C3_RECORD_OBJECT')
        require(len(encode(payload)) <= 1024**2, 'C3_PAYLOAD_SIZE_CAP')
        c3 = dict(status='AVAILABLE', reason=None, registration_pin=sources['a17_c3_record'], record_pin=c['record_pin'], payload=payload)
    p8 = dict(status='AVAILABLE' if original['status']=='AVAILABLE' and c3['status']=='AVAILABLE' else 'UNAVAILABLE',
              original_k=original, a17_c3=c3, consistency_verdict='UNAVAILABLE_NO_REGISTERED_AGREEMENT_PREDICATE',
              reading='M13: mandatory exact report of both records. Never infer agreement from two PASS strings, unlike quantities, or model-target residuals.',
              trigger_evaluation='NOT_PERFORMED_TARGET_FREE; P8 classification belongs to the sealed later reader.')
    return dict(schema='UNT_STEP5_READING_CARRIERS_CX3V001',date_u=datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),
                mode=mode,target_free=True,before_target_access=True,launch_authorized=False,request_pin=req_pin,policy_pin=req['policy_pin'],
                extractor_pin={'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__).read_bytes())},
                point_key=point,slots_pin=policy['slots'],driver_pin=policy['driver'],registry_pin=policy['registry'],
                carriers={'TSR':tsr,'E1b':e1b,'P8_C3':p8},root_registration_status='REQUIRED_BEFORE_PRODUCTION_FREEZE',
                scope='Proposed carriers; no mutation of v003g, slots, driver, saved records or prior readiness evidence.')


def write_carriers(request_path, expected_sha, output_path, synthetic=False):
    obj = extract(request_path, expected_sha, synthetic)
    p = safe_path(str(output_path))
    require(p.parent.is_dir(), 'OUTPUT_PARENT_REQUIRED')
    b = encode(obj)
    require(len(b) <= 2 * 1024**2, 'OUTPUT_SIZE_CAP')
    with p.open('xb') as f:
        f.write(b)
    return obj


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--request',required=True);p.add_argument('--expected-sha256',required=True)
    p.add_argument('--output',required=True);p.add_argument('--synthetic',action='store_true')
    a=p.parse_args()
    try:
        o=write_carriers(a.request,a.expected_sha256,a.output,a.synthetic)
    except (Refusal,OSError,KeyError,TypeError) as e:
        p.exit(2,'REFUSED: %s\n'%e)
    print(json.dumps({k:v['status'] for k,v in o['carriers'].items()}))


if __name__=='__main__':
    main()
