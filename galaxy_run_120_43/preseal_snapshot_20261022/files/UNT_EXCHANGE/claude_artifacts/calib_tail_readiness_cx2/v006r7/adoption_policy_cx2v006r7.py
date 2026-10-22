"""0540 F1: inert verification of a sealed V007 ADOPT_TAIL report; never runs the comparator."""
import ast
import copy
import hashlib
import json
import math


# No final V007 seal has been supplied. A root-reviewed immutable successor
# must register (compare_sha256, prereg_sha256, addendum_sha256, report_schema, verdict_sha256).
# Config declarations and the comparator's own literals cannot create trust.
APPROVED_V007_SEALS = frozenset()


def constants(raw):
    out = {}
    for node in ast.parse(raw).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        out[target.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        pass
    return out


def check_numerics(ncfg, template_numerics, deciding_route_a_n, *, O, validate_block, driver_sha, synthetic=False):
    if synthetic:
        raise O.OrchestratorError('real tail driver cannot use a synthetic adoption bypass')
    if not isinstance(ncfg, dict) or not isinstance(ncfg.get('block'), dict):
        raise O.OrchestratorError('numerics.block must be an object')
    block = copy.deepcopy(ncfg['block'])
    validate_block(block)
    g = {'ok': False, 'reasons': [], 'adopted': None, 'grid_case_inputs': {}, 'u_i_km_s': None}
    R = g['reasons']
    required = ('verdict_artifact', 'block_source', 'compare', 'sealed_prereg', 'adopted_result')
    if any(not isinstance(ncfg.get(k), dict) for k in required):
        R.append('V007_SEALED_ADOPT_TAIL_PENDING: require ' + ','.join(required))
        return block, g
    try:
        def doc(ref, name):
            value = json.loads(O.read_pinned(ref, name))
            if not isinstance(value, dict):
                raise ValueError(name + ' is not an object')
            return value
        art, src, cmpref, preref = (ncfg[k] for k in required[:4])
        rep = doc(art, 'V007 report')
        source = doc(src, 'C4T call spec')
        c = constants(O.read_pinned(cmpref, 'sealed compare source'))
        pre = doc(preref, 'sealed V007 prereg')
        if not isinstance(c.get('V007_PREREG_SHA256'), str) or len(c['V007_PREREG_SHA256']) != 64:
            R.append('V007_COMPARE_NOT_SEALED')
        if c.get('V007_PREREG_SHA256') != preref['sha256'] or rep.get('prereg') != preref:
            R.append('V007_SEALED_PREREG_MISMATCH')
        add=c.get('PIN_ADDENDUM_V005')
        if not isinstance(add,(list,tuple)) or len(add)!=2 or not all(isinstance(v,str) for v in add):
            raise ValueError('V007_ADDENDUM_EXACT_BYTE_PIN_REQUIRED')
        O.read_pinned({'path':add[0],'sha256':add[1]},'sealed V005 addendum')
        seal=(cmpref['sha256'],preref['sha256'],add[1],c.get('SCHEMA_REPORT'),art['sha256'])
        if seal not in APPROVED_V007_SEALS:
            R.append('V007_SEAL_NOT_IN_REVIEWED_ALLOWLIST')
        if (rep.get('pins_verified') or {}).get('V005_addendum') not in (list(add),tuple(add)):
            R.append('V007_REPORT_ADDENDUM_PIN_MISMATCH')
        if c.get('PRODUCTION_K_BIG_A55') != 128.0:
            R.append('V007_COMPARE_NOT_P128')
        if rep.get('schema') != c.get('SCHEMA_REPORT') or not str(rep.get('schema', '')).startswith('UNT_KMAX_TAIL_COMPARISON_C2V007'):
            R.append('V007_REPORT_SCHEMA_MISMATCH')
        if rep.get('script_sha256') != cmpref['sha256']:
            R.append('V007_COMPARE_SHA_MISMATCH')
        dec = rep.get('decision') or {}
        if dec.get('outcome') != 'ADOPT_TAIL' or dec.get('tests_read') is not True or rep.get('test_mode') is not False:
            R.append('V007_READING_NOT_SEALED_ADOPT_TAIL')
        cbref = rep.get('case_block')
        cb = doc(cbref, 'V007 case block')
        if (pre.get('binding_inputs') or {}).get('case_block') != cbref:
            R.append('V007_CASE_BLOCK_NOT_BOUND_BY_SEALED_PREREG')
        reg = (cb.get('cases') or {}).get('C4T') or {}
        if reg.get('tail') is not True or driver_sha not in (reg.get('drivers_allowed') or []):
            R.append('V007_C4T_DRIVER_OR_TAIL_MISMATCH')
        if (rep.get('validity', {}).get('C4T') or {}).get('valid_all') is not True:
            R.append('V007_C4T_NOT_VALID')
        result = doc(ncfg['adopted_result'], 'C4T result')
        if (rep.get('inputs', {}).get('C4T') or {}).get('result_sha256') != ncfg['adopted_result']['sha256']:
            R.append('V007_C4T_RESULT_NOT_VERDICT_INPUT')
        if result.get('call_spec_sha256') != src['sha256'] or result.get('driver_sha256') != driver_sha:
            R.append('V007_C4T_SPEC_OR_DRIVER_NOT_BOUND')
        if result.get('status') != 'COMPLETED' or result.get('valid') is not True:
            R.append('V007_C4T_RESULT_NOT_COMPLETED_VALID')
        if source.get('numerics') != block:
            R.append('V007_BLOCK_DIFFERS_FROM_ADOPTED_C4T')
        if source.get('admit') != {}:
            R.append('V007_ADOPTED_SOURCE_NOT_FRESH')
        # Compare normalized numerics, because the driver adds deterministic defaults.
        registered_num = (reg.get('normalized_spec_equal') or {}).get('/numerics')
        if not isinstance(registered_num, dict) or (result.get('normalized_spec') or {}).get('numerics') != registered_num:
            R.append('V007_C4T_REGISTERED_NORMALIZED_BLOCK_MISMATCH')
        if block.get('route_a', {}).get('column_workers') != deciding_route_a_n:
            R.append('V007_ROUTE_A_WORKERS_NOT_DECIDING_VERIFIED')
        bound = block.get('picard', {}).get('speed_change_bound_km_s')
        if type(bound) not in (int, float) or not math.isfinite(bound) or bound <= 0:
            R.append('V007_FINITE_POSITIVE_PICARD_BOUND_REQUIRED')
        g['adopted'] = {'case_id': 'C4T', 'shape': 'cube', 'grid': reg.get('grid'),
                        'call_spec_sha256': src['sha256'], 'verdict_sha256': art['sha256'],
                        'prereg_sha256': preref['sha256'], 'compare_sha256': cmpref['sha256']}
        g['grid_case_inputs']['C4T'] = {'call_spec_sha256': src['sha256'], 'driver_sha256': driver_sha,
                                      'result_sha256': ncfg['adopted_result']['sha256']}
        seen = {'C4T'}
        for entry in ncfg.get('source_results', []):
            cid = entry['case_id']
            if cid in seen or (cb.get('cases', {}).get(cid) or {}).get('grid') != reg.get('grid'):
                raise ValueError('source receipt input case duplicate or outside adopted grid')
            seen.add(cid)
            rr = doc(entry['result'], 'timing source result')
            if (rep.get('inputs', {}).get(cid) or {}).get('result_sha256') != entry['result']['sha256']:
                raise ValueError('timing source result not verdict input')
            if (rep.get('validity', {}).get(cid) or {}).get('valid_all') is not True or rr.get('driver_sha256') != driver_sha:
                raise ValueError('timing source result invalid or foreign driver')
            g['grid_case_inputs'][cid] = {'call_spec_sha256': rr.get('call_spec_sha256'), 'driver_sha256': driver_sha,
                                         'result_sha256': entry['result']['sha256']}
        u = dec.get('carried_numerical_uncertainty_km_s')
        if not isinstance(u, dict) or not u or any(type(x) not in (int,float) or not math.isfinite(x) or x < 0 for x in u.values()):
            R.append('V007_CARRIED_UNCERTAINTY_REQUIRED')
        else:
            g['u_i_km_s'] = copy.deepcopy(u)
        g.update(verdict_artifact=art, block_source=src, compare=cmpref, sealed_prereg=preref)
    except (O.OrchestratorError, OSError, ValueError, TypeError, KeyError, AttributeError, SyntaxError) as exc:
        R.append(type(exc).__name__ + ': ' + str(exc))
    g['ok'] = not R
    return block, g
