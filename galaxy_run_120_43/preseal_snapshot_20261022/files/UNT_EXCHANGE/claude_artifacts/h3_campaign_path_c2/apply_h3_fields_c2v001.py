"""Apply the H3 gate fields to a DDO154 calibration RUN_CONFIG (Claude2 h3_campaign_path_c2, c2v001; V006 A188 item 4).

c2v001 = apply_sched_delta_s45_c2v002 (2a18b280) with the allowed set replaced: v002 may set only scheduling leaves, so it
cannot set any gate field (its ALLOWED_SET L25-26).  This successor may set ONLY the fields the five H3 gates and the numerics
gate read (parent c75a889f, core r9/r10_c4, wrapper q5b1), and append to notes:
  {"set": {path: value, ...}, "append": {"notes": " h3 ..."}}
  * numerics gate (policy check_numerics L46-138): numerics.{verdict_artifact, block_source, compare, sealed_prereg,
    adopted_result, source_results}.  numerics.block can NOT change.  With --seal-record (the one record root fills at the
    verdict, regenerate_h3_c2v001.py) verdict_artifact, compare and sealed_prereg are DERIVED from it: the report pin, the
    sealed compare pin, and the report's own prereg object (the policy compares it exactly, L63); a delta that also sets
    them must give the same values;
  * deciding (core L114-197): deciding_test; anchor.{result, receipt, spec_sha256} (anchor.use stays false, L101-102);
  * capability (core L313-340): capability_evidence;
  * certificate policy (wrapper q5b1 L59-77): tail_readiness.{certificate_registry, certificate_policy_review,
    approved_certificate_producers, state_enumerator, custody_deriver};
  * adoption (parent L1828-1926, q5b1 L213-227): adoption_derivation, disk_guard.measured_per_call_bytes;
  * u_i carrier (parent L1797-1826): u_i_carrier.{carrier, declared_by, basis, note}.
Every other path refuses (physics, scheduling, campaign, driver, work dir, ...).  Value rules, all before anything is
written: no null; a pin is exactly {path, sha256} with an absolute path whose bytes hash to sha256 (sealed_prereg may carry
the report's extra keys); approved_certificate_producers is a non-empty list of pins; source_results is a list of
{case_id, result: pin}; anchor.spec_sha256 is 64 lowercase hex; carrier is NOT_CARRIED_DECLARED or FROZEN_BANDS_ONLY
(parent L148-149: ADMISSION_RECTANGLES refuses); declared_by / basis are non-empty text; measured_per_call_bytes is an int > 0.
The output keeps the predecessor's serialization (json, indent 1, sorted keys, trailing newline) and is written by exclusive
create.  The report lists every changed path, the canonical sha256 of every unchanged top-level key, and whether a changed
path is in the wrapper cache key (tail_readiness, q5b1 L52-55: then the cache id changes).
usage: python3 -I -B apply_h3_fields_c2v001.py PREDECESSOR.json DELTA.json OUT.json [REPORT.json]
                                              [--seal-record SEAL.json --seal-record-sha256 H]
"""
import copy
import hashlib
import json
import os
import re
import sys
from pathlib import Path

PIN_PATHS = ('numerics.verdict_artifact', 'numerics.block_source', 'numerics.compare', 'numerics.sealed_prereg',
             'numerics.adopted_result', 'deciding_test', 'anchor.result', 'anchor.receipt', 'capability_evidence',
             'tail_readiness.certificate_registry', 'tail_readiness.certificate_policy_review',
             'tail_readiness.state_enumerator', 'tail_readiness.custody_deriver', 'adoption_derivation')
ALLOWED_SET = PIN_PATHS + ('numerics.source_results', 'anchor.spec_sha256', 'tail_readiness.approved_certificate_producers',
                           'disk_guard.measured_per_call_bytes', 'u_i_carrier.carrier', 'u_i_carrier.declared_by',
                           'u_i_carrier.basis', 'u_i_carrier.note')
ALLOWED_APPEND = ('notes',)
ALLOWED = ALLOWED_SET + ALLOWED_APPEND
CACHE_KEY_PREFIXES = ('tail_readiness',)                 # wrapper q5b1 L52-55; the parent key reads none of ALLOWED_SET
SEAL_SCHEMA = 'H3_V007_SEAL_TUPLE_RECORD_C2V001'
HEX = re.compile(r'[0-9a-f]{64}')


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def get(d, path):
    for k in path.split('.'):
        d = d[k]
    return d


def put(d, path, v):
    ks = path.split('.')
    for k in ks[:-1]:
        d = d[k]
    if ks[-1] not in d:
        raise KeyError('path absent in predecessor: %s' % path)
    d[ks[-1]] = v


def flat(o, pre=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(flat(v, pre + k + '.') if isinstance(v, dict) and v else {pre + k: v})
        return out
    return {pre[:-1]: o}


def pin_problem(v, extra_keys_ok=False):
    if not isinstance(v, dict) or not {'path', 'sha256'} <= set(v) or (not extra_keys_ok and set(v) != {'path', 'sha256'}):
        return 'must be {path, sha256}'
    if not isinstance(v['path'], str) or not os.path.isabs(v['path']) or not isinstance(v['sha256'], str) \
            or HEX.fullmatch(v['sha256']) is None:
        return 'needs an absolute path and a 64-hex sha256'
    try:
        if sha_b(Path(v['path']).read_bytes()) != v['sha256']:
            return 'sha256 differs from the file bytes'
    except OSError as exc:
        return 'unreadable: %s' % exc
    return None


def value_problems(p, v):
    if v is None:
        return ['%s: null (every H3 field must be filled; pending fields are not applied)' % p]
    if p in PIN_PATHS:
        bad = pin_problem(v, extra_keys_ok=(p == 'numerics.sealed_prereg'))
        return ['%s: %s' % (p, bad)] if bad else []
    if p == 'tail_readiness.approved_certificate_producers':
        if not isinstance(v, list) or not v:
            return ['%s: a non-empty list of pins' % p]
        return ['%s[%d]: %s' % (p, i, b) for i, b in enumerate(pin_problem(x) for x in v) if b]
    if p == 'numerics.source_results':
        if not isinstance(v, list):
            return ['%s: a list of {case_id, result}' % p]
        out = []
        for i, x in enumerate(v):
            if not isinstance(x, dict) or set(x) != {'case_id', 'result'} or not isinstance(x.get('case_id'), str):
                out.append('%s[%d]: must be {case_id, result}' % (p, i))
            elif pin_problem(x['result']):
                out.append('%s[%d].result: %s' % (p, i, pin_problem(x['result'])))
        return out
    if p == 'anchor.spec_sha256':
        return [] if isinstance(v, str) and HEX.fullmatch(v) else ['%s: 64 lowercase hex' % p]
    if p == 'u_i_carrier.carrier':
        return [] if v in ('NOT_CARRIED_DECLARED', 'FROZEN_BANDS_ONLY') else ['%s: NOT_CARRIED_DECLARED or FROZEN_BANDS_ONLY' % p]
    if p in ('u_i_carrier.declared_by', 'u_i_carrier.basis', 'u_i_carrier.note'):
        return [] if isinstance(v, str) and v.strip() else ['%s: non-empty text' % p]
    if p == 'disk_guard.measured_per_call_bytes':
        return [] if type(v) is int and v > 0 else ['%s: an int > 0' % p]
    return []


def seal_derived(seal_raw, seal_sha):
    """numerics.{verdict_artifact, compare, sealed_prereg} from the root-filled seal tuple record (regenerate_h3_c2v001)."""
    if sha_b(seal_raw) != seal_sha:
        return None, ['seal record bytes do not hash to --seal-record-sha256']
    rec = json.loads(seal_raw)
    if rec.get('schema') != SEAL_SCHEMA or rec.get('status') != 'ROOT_FILLED':
        return None, ['seal record must be %s with status ROOT_FILLED (EMPTY_TUPLE)' % SEAL_SCHEMA]
    t, rp, cp = rec.get('tuple') or {}, rec.get('report') or {}, rec.get('compare') or {}
    reasons = [x for x in (pin_problem(rp), pin_problem(cp)) if x]
    if reasons:
        return None, ['seal record report/compare pin: %s' % reasons]
    if rp['sha256'] != t.get('verdict_sha256') or cp['sha256'] != t.get('compare_sha256'):
        return None, ['seal record pins differ from its tuple (TUPLE_NOT_REPORT_BYTES)']
    rep = json.loads(Path(rp['path']).read_bytes())
    pre = rep.get('prereg')
    if not isinstance(pre, dict) or pre.get('sha256') != t.get('prereg_sha256') or pin_problem(pre, extra_keys_ok=True):
        return None, ['the report prereg object is not the tuple P / does not verify']
    return {'numerics.verdict_artifact': {'path': rp['path'], 'sha256': rp['sha256']},
            'numerics.compare': {'path': cp['path'], 'sha256': cp['sha256']},
            'numerics.sealed_prereg': copy.deepcopy(pre)}, []


def apply(pred_bytes, delta, seal_raw=None, seal_sha=None):
    pred = json.loads(pred_bytes)
    reasons = []
    sets = dict(delta.get('set') or {})
    appends = delta.get('append') or {}
    if seal_raw is not None:
        derived, why = seal_derived(seal_raw, seal_sha)
        reasons += why
        for p, v in (derived or {}).items():
            if p in sets and canon(sets[p]) != canon(v):
                reasons.append('%s differs from the value derived from the seal record' % p)
            sets[p] = v
    for p in sets:
        if p not in ALLOWED_SET:
            reasons.append('path not allowed to be set (H3 gate fields only; notes are append-only): %s' % p)
    for p, v in appends.items():
        if p not in ALLOWED_APPEND:
            reasons.append('path not allowed to be appended to: %s' % p)
        elif not isinstance(v, str) or not v:
            reasons.append('append value must be a non-empty string: %s' % p)
    for p, v in sets.items():
        if p in ALLOWED_SET:
            reasons.extend(value_problems(p, v))
    if reasons:
        return None, {'ok': False, 'reasons': reasons}
    new = copy.deepcopy(pred)
    try:
        for p, v in sets.items():
            put(new, p, v)
        for p, v in appends.items():
            cur = get(new, p)
            if not isinstance(cur, str):
                return None, {'ok': False, 'reasons': ['append target is not a string: %s' % p]}
            put(new, p, cur + v)
    except KeyError as exc:
        return None, {'ok': False, 'reasons': [str(exc)]}
    if 'disk_guard.per_call_bytes' in sets or 'per_call.output_cap_bytes' in sets:
        if new['disk_guard']['per_call_bytes'] < int(new['per_call']['output_cap_bytes']):
            return None, {'ok': False, 'reasons': ['disk_guard.per_call_bytes < per_call.output_cap_bytes (parent L1748)']}
    out_bytes = (json.dumps(new, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    fp, fn = flat(pred), flat(new)
    changed = sorted(k for k in set(fp) | set(fn) if fp.get(k, '<absent>') != fn.get(k, '<absent>'))
    illegal = [k for k in changed if not any(k == a or k.startswith(a + '.') for a in ALLOWED)]
    if illegal:
        return None, {'ok': False, 'reasons': ['changed outside ALLOWED: %s' % illegal]}
    kept_prefix = {p: get(new, p).startswith(get(pred, p)) for p in appends}
    top_same = {k: sha_b(canon(pred[k]).encode()) for k in sorted(pred) if canon(pred[k]) == canon(new[k])}
    rep = {'ok': True, 'predecessor_sha256': sha_b(pred_bytes), 'successor_sha256': sha_b(out_bytes),
           'predecessor_serialization_roundtrips': (json.dumps(pred, indent=1, sort_keys=True) + '\n').encode() == pred_bytes,
           'changed_paths': {k: {'from': fp.get(k), 'to': fn.get(k)} for k in changed},
           'appended_paths_keep_predecessor_prefix': kept_prefix,
           'unchanged_top_level_canonical_sha256': top_same,
           'seal_record_sha256': seal_sha,
           'changed_paths_in_wrapper_cache_key': sorted(k for k in changed if k.split('.')[0] in CACHE_KEY_PREFIXES)}
    return out_bytes, rep


def main(argv):
    seal_p = seal_s = None
    if '--seal-record' in argv:
        i = argv.index('--seal-record')
        seal_p, argv = argv[i + 1], argv[:i] + argv[i + 2:]
        j = argv.index('--seal-record-sha256')
        seal_s, argv = argv[j + 1], argv[:j] + argv[j + 2:]
    pred_p, delta_p, out_p = argv[:3]
    out_bytes, rep = apply(Path(pred_p).read_bytes(), json.loads(Path(delta_p).read_text()),
                           Path(seal_p).read_bytes() if seal_p else None, seal_s)
    if out_bytes is None:
        print(json.dumps(rep, indent=1))
        return 2
    with open(out_p, 'xb') as f:
        f.write(out_bytes)
    if len(argv) > 3:
        with open(argv[3], 'x') as f:
            json.dump(rep, f, indent=1)
            f.write('\n')
    print(json.dumps({k: rep[k] for k in ('ok', 'predecessor_sha256', 'successor_sha256', 'changed_paths',
                                          'appended_paths_keep_predecessor_prefix', 'changed_paths_in_wrapper_cache_key')},
                     indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
