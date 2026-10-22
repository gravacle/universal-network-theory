"""Apply the H3 gate fields to a DDO154 calibration RUN_CONFIG (Claude2 h3_campaign_path_c2, c2v006; V006 A188 item 4, A192,
A218 (2) S4-R-A1, A221 CX1-S4RA1-01, A222 E_A220_1).

c2v006 against apply_h3_fields_c2v005 (6c6c6d08), and nothing else (V006 A222, under E_A220_1 (A221): every pin-binding
read reads the file once, hashes that buffer against its pin and parses that same buffer).  A sweep of the whole c2v005
module found two places where a pinned file was hashed and then read again for the same use:
  * seal_derived: pin_problem(rp) hashed one read of the seal record's report and json.loads(Path(rp['path']).read_bytes())
    parsed a second read, whose prereg object was written into numerics.sealed_prereg.  Now pin_read(rp) reads the report
    once and applies pin_problem's checks and messages to that buffer, in pin_problem's order; the SAME buffer is parsed;
  * value_problems, numerics.source_results: pin_problem(x['result']) decided and a second pin_problem(x['result']) (a
    second read) gave the refusal text.  Now one call decides and gives the text.
New top-level: pin_read (pin_problem's checks and messages on one read; returns that buffer).  pin_problem, block_derived
(c2v005's one read), apply and main are unchanged (AST-identical).  Whenever no file changes between reads, every output,
report and refusal reason is c2v005's.  Kept, unchanged since c2v003: value_problems re-checks a delta-set
numerics.block_source and the three seal-derived pins numerics.{verdict_artifact, compare, sealed_prereg} with pin_problem.
Each of those re-checks is one read that is hashed and never parsed, and refuses if the bytes changed; the only buffers
parsed are block_derived's one read and seal_derived's one report read (the compare and prereg files are never parsed).
Text below is c2v005's.

c2v005 against apply_h3_fields_c2v004 (b3e8b7d3), and nothing else (V006 A221; Codex1 0162 blocking item CX1-S4RA1-01):
block_derived reads the block_source file ONCE.  c2v004 hashed one read (pin_problem) and parsed a second read, so a second
read that differed at a permitted slot was accepted and reported as derived from the pin.  Now:
  * one read: raw = the block_source file's bytes (the only read block_derived makes);
  * that buffer is checked with pin_problem's checks and messages, in pin_problem's order (shape; absolute path and 64 hex;
    readable; sha256(raw) == the pin's sha256), then the pin must be exactly BLOCK_SOURCE_PIN (path and sha), as in c2v004;
  * the SAME buffer is parsed and the block is derived from it; the file is never read again.
Every other line is c2v004's (AST-identical outside block_derived).  Whenever the file's bytes do not change between reads,
every output, report and refusal reason is c2v004's.  Not part of the derivation and unchanged from c2v003: when the delta
also sets numerics.block_source, value_problems verifies that field's pin with its own read (pin_problem); nothing from that
read is parsed or written, and the derivation still refuses unless its own one buffer hashes to the pin.
Text below is c2v004's.

c2v004 against apply_h3_fields_c2v003 (02addc1d), and nothing else (V006 A218 (2), ruling S4-R-A1): one more operation,
--block-source PATH --block-source-sha256 H, that sets numerics.block to the numerics of the pinned block_source spec.
  * The pin must be exactly BLOCK_SOURCE_PIN: the C4T FILLED call spec de6d7d77 (the only block_source the adoption policy
    93d9c0ac can admit: L98 binds it to the adopted C4T result, L100 needs that result COMPLETED and valid, and driver r5
    refuses PENDING slots in run mode; final-spec producer v004 fcbf1c3e L151-152 and L709-711 pin the same path and
    sha).  Its bytes must hash to it.  A --block-source-sha256 without --block-source refuses (exit 2).
  * The new block is DERIVED: a JSON copy of block_source.numerics, nothing else.  It refuses unless
    strip_slots(new block) == strip_slots(old block) as canonical JSON, where strip_slots removes exactly
    uv_tail.eps_certificate and uv_tail.lo_certificate (the two per-point slots core point_identity strips).  So the only
    leaves that may change are under numerics.block.uv_tail.{eps_certificate, lo_certificate}: a string slot replaced by a
    {path, sha256} pin is 6 flat keys (2 removed, 4 added).
  * If the config's numerics.block_source (after this delta and the seal record) is set, it must equal the pin exactly.
  * The written block must equal block_source.numerics exactly (canonical JSON, re-read from the output bytes).
  * numerics.block is still NOT a settable path in a delta: {"set": {"numerics.block": ...}} refuses as in c2v003.
  * The policy bytes are not touched; policy L102 (`source.get('numerics') != block`) then holds by construction.
  * numerics.block enters the parent base spec (parent c75a889f L1695, L1760, L1765), so base_spec_sha256 changes and
    with it the parent cache id (L1774-1780), the wrapper cache id (q5b1 L52-55) and every document bound to
    base_spec_sha256 (the capability evidence, core r10_c4 L323; the adoption derivation and its timing model, parent
    L1861, L1870).  Apply the block in the same step as the first candidate config, before the HEADLINE11 evidence
    assembly and the adoption derivation.
  * Without --block-source the tool is c2v003: same output bytes, same report.
The report then also carries block_source, the changed block leaves, the canonical sha of the old and new block, and the
paths that enter the parent cache key.  Usable on the W1 candidate config and on the H1 run config alike (any config whose
numerics.block is an object with uv_tail; an empty delta {"set": {}} is allowed).  Text below is c2v003's.

c2v003 against apply_h3_fields_c2v001 (2e4a5393), and nothing else (V006 A192 item 2, the R-C8 ledger policy): one more
settable field, tail_readiness.certificate_ledger, whose value must be exactly
  {"schema": "DDO154_CERTIFICATE_LEDGER_C2V003", "path": <predecessor work_dir>/CERTIFICATE_LEDGER.jsonl}
(the wrapper source calibration_orchestrator_q5b1_ledger_c2v003 requires exactly this; the path is not a pin: the ledger file
need not exist and carries no head sha).  It is the only path that may be ABSENT in the predecessor (v004a has no such key).
It is in the wrapper cache key (tail_readiness).  Text below is c2v001's.

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
usage: python3 -I -B apply_h3_fields_c2v006.py PREDECESSOR.json DELTA.json OUT.json [REPORT.json]
                                              [--seal-record SEAL.json --seal-record-sha256 H]
                                              [--block-source SPEC.json --block-source-sha256 H]
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
                           'u_i_carrier.basis', 'u_i_carrier.note', 'tail_readiness.certificate_ledger')
CREATABLE = ('tail_readiness.certificate_ledger',)      # c2v003: may be absent in the predecessor
LEDGER_SCHEMA = 'DDO154_CERTIFICATE_LEDGER_C2V003'      # wrapper source c2v003 LEDGER_SCHEMA
LEDGER_NAME = 'CERTIFICATE_LEDGER.jsonl'                # wrapper source c2v003 LEDGER_NAME
ALLOWED_APPEND = ('notes',)
ALLOWED = ALLOWED_SET + ALLOWED_APPEND
CACHE_KEY_PREFIXES = ('tail_readiness',)                 # wrapper q5b1 L52-55; the parent key reads none of ALLOWED_SET
SEAL_SCHEMA = 'H3_V007_SEAL_TUPLE_RECORD_C2V001'
HEX = re.compile(r'[0-9a-f]{64}')
BLOCK_SOURCE_PIN = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/'
                            'C4T_P128_MS128_R5_CX1V004.FILLED.json',
                    'sha256': 'de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738'}   # c2v004: A218 (2)
SLOTS = ('eps_certificate', 'lo_certificate')            # c2v004: core point_identity / deciding_numerics_identity strip these
SLOT_PATHS = tuple('numerics.block.uv_tail.' + s for s in SLOTS)
BLOCK_RULE = 'V006 A218 (2) S4-R-A1: numerics.block := block_source.numerics (canonical-equal); policy bytes unchanged'


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
    if ks[-1] not in d and path not in CREATABLE:
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


def pin_read(v, extra_keys_ok=False):
    """c2v006 (V006 A222, E_A220_1): pin_problem's checks and messages, in pin_problem's order, on ONE read of the pinned
    file.  -> (None, raw) when raw (that one read) hashes to the pin, else (problem, None).  The caller parses raw and
    never reads the file again."""
    if not isinstance(v, dict) or not {'path', 'sha256'} <= set(v) or (not extra_keys_ok and set(v) != {'path', 'sha256'}):
        return 'must be {path, sha256}', None
    if not isinstance(v['path'], str) or not os.path.isabs(v['path']) or not isinstance(v['sha256'], str) \
            or HEX.fullmatch(v['sha256']) is None:
        return 'needs an absolute path and a 64-hex sha256', None
    try:
        raw = Path(v['path']).read_bytes()                      # c2v006: the one read of the pinned file
    except OSError as exc:
        return 'unreadable: %s' % exc, None
    if sha_b(raw) != v['sha256']:
        return 'sha256 differs from the file bytes', None
    return None, raw


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
            elif (bad := pin_problem(x['result'])):            # c2v006: one read per pin (c2v005: two)
                out.append('%s[%d].result: %s' % (p, i, bad))
        return out
    if p == 'anchor.spec_sha256':
        return [] if isinstance(v, str) and HEX.fullmatch(v) else ['%s: 64 lowercase hex' % p]
    if p == 'u_i_carrier.carrier':
        return [] if v in ('NOT_CARRIED_DECLARED', 'FROZEN_BANDS_ONLY') else ['%s: NOT_CARRIED_DECLARED or FROZEN_BANDS_ONLY' % p]
    if p in ('u_i_carrier.declared_by', 'u_i_carrier.basis', 'u_i_carrier.note'):
        return [] if isinstance(v, str) and v.strip() else ['%s: non-empty text' % p]
    if p == 'disk_guard.measured_per_call_bytes':
        return [] if type(v) is int and v > 0 else ['%s: an int > 0' % p]
    if p == 'tail_readiness.certificate_ledger':
        if not isinstance(v, dict) or set(v) != {'schema', 'path'} or v.get('schema') != LEDGER_SCHEMA:
            return ['%s: exactly {schema: %s, path}' % (p, LEDGER_SCHEMA)]
        if not isinstance(v['path'], str) or not os.path.isabs(v['path']) or os.path.normpath(v['path']) != v['path']:
            return ['%s: path must be absolute and normalized' % p]
    return []


def seal_derived(seal_raw, seal_sha):
    """numerics.{verdict_artifact, compare, sealed_prereg} from the root-filled seal tuple record (regenerate_h3_c2v001).
    c2v006 (V006 A222, E_A220_1): the report is read ONCE (pin_read: pin_problem's checks and messages on that buffer) and
    the prereg object is parsed from that same buffer; c2v005 hashed one read (pin_problem) and parsed a second."""
    if sha_b(seal_raw) != seal_sha:
        return None, ['seal record bytes do not hash to --seal-record-sha256']
    rec = json.loads(seal_raw)
    if rec.get('schema') != SEAL_SCHEMA or rec.get('status') != 'ROOT_FILLED':
        return None, ['seal record must be %s with status ROOT_FILLED (EMPTY_TUPLE)' % SEAL_SCHEMA]
    t, rp, cp = rec.get('tuple') or {}, rec.get('report') or {}, rec.get('compare') or {}
    rp_bad, rp_raw = pin_read(rp)                               # c2v006: the one read of the report
    reasons = [x for x in (rp_bad, pin_problem(cp)) if x]
    if reasons:
        return None, ['seal record report/compare pin: %s' % reasons]
    if rp['sha256'] != t.get('verdict_sha256') or cp['sha256'] != t.get('compare_sha256'):
        return None, ['seal record pins differ from its tuple (TUPLE_NOT_REPORT_BYTES)']
    rep = json.loads(rp_raw)                                    # c2v006: the buffer that was hashed, not a second read
    pre = rep.get('prereg')
    if not isinstance(pre, dict) or pre.get('sha256') != t.get('prereg_sha256') or pin_problem(pre, extra_keys_ok=True):
        return None, ['the report prereg object is not the tuple P / does not verify']
    return {'numerics.verdict_artifact': {'path': rp['path'], 'sha256': rp['sha256']},
            'numerics.compare': {'path': cp['path'], 'sha256': cp['sha256']},
            'numerics.sealed_prereg': copy.deepcopy(pre)}, []


def strip_slots(block):
    """c2v004: numerics.block without uv_tail.{eps_certificate, lo_certificate} (as core point_identity strips them)."""
    out = copy.deepcopy(block)
    for s in SLOTS:
        out['uv_tail'].pop(s, None)
    return out


def block_derived(pred, sets, pin):
    """c2v004 (A218 (2) S4-R-A1): the new numerics.block, derived from the pinned block_source bytes alone.
    c2v005 (CX1-S4RA1-01): the block_source file is read ONCE; that buffer is checked against the pin (pin_problem's checks
    and messages, in its order), the pin must be exactly BLOCK_SOURCE_PIN, and the SAME buffer is parsed.
    -> (block, []) or (None, reasons).  Reads only the block_source file, once."""
    if not isinstance(pin, dict) or set(pin) != {'path', 'sha256'}:
        return None, ['--block-source: must be {path, sha256}']
    if not isinstance(pin['path'], str) or not os.path.isabs(pin['path']) or not isinstance(pin['sha256'], str) \
            or HEX.fullmatch(pin['sha256']) is None:
        return None, ['--block-source: needs an absolute path and a 64-hex sha256']
    try:
        raw = Path(pin['path']).read_bytes()                    # c2v005: the one read of the block_source file
    except OSError as exc:
        return None, ['--block-source: unreadable: %s' % exc]
    if sha_b(raw) != pin['sha256']:
        return None, ['--block-source: sha256 differs from the file bytes']
    if canon(pin) != canon(BLOCK_SOURCE_PIN):
        return None, ['--block-source: not the pinned block_source %s %s (BLOCK_SOURCE_NOT_PINNED_C4T_FILLED)'
                      % (BLOCK_SOURCE_PIN['path'], BLOCK_SOURCE_PIN['sha256'][:16])]
    try:
        src = json.loads(raw)                                   # c2v005: the buffer that was hashed, not a second read
    except ValueError:
        return None, ['--block-source: not a JSON document']
    new = src.get('numerics') if isinstance(src, dict) else None
    num = pred.get('numerics') if isinstance(pred.get('numerics'), dict) else {}
    old = num.get('block')
    if not isinstance(new, dict) or not isinstance(new.get('uv_tail'), dict):
        return None, ['--block-source: its numerics must be an object with uv_tail (BLOCK_SOURCE_NUMERICS_REQUIRED)']
    if not isinstance(old, dict) or not isinstance(old.get('uv_tail'), dict):
        return None, ['numerics.block must be an object with uv_tail (CONFIG_BLOCK_REQUIRED)']
    reasons = []
    if canon(strip_slots(new)) != canon(strip_slots(old)):
        fo, fn = flat(strip_slots(old)), flat(strip_slots(new))
        diff = sorted(k for k in set(fo) | set(fn) if canon(fo.get(k, '<absent>')) != canon(fn.get(k, '<absent>')))
        reasons.append('BLOCK_DIFFERS_OUTSIDE_THE_TWO_SLOTS: strip_slots(new) != strip_slots(old) at %s' % diff[:8])
    cur = sets['numerics.block_source'] if 'numerics.block_source' in sets else num.get('block_source')
    if cur is not None and canon(cur) != canon(pin):
        reasons.append('numerics.block_source differs from --block-source (BLOCK_SOURCE_FIELD_MISMATCH)')
    return (None, reasons) if reasons else (copy.deepcopy(new), [])


def apply(pred_bytes, delta, seal_raw=None, seal_sha=None, block_source=None):
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
    led = sets.get('tail_readiness.certificate_ledger')
    if isinstance(led, dict) and led.get('path') != os.path.join(str(pred.get('work_dir')), LEDGER_NAME):
        reasons.append('tail_readiness.certificate_ledger: path must be the work dir\'s %s (%s)'
                       % (LEDGER_NAME, os.path.join(str(pred.get('work_dir')), LEDGER_NAME)))
    blk = None
    if block_source is not None:                                # c2v004: the S4-R-A1 block operation, checked before writing
        blk, why = block_derived(pred, sets, block_source)
        reasons += why
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
    if blk is not None:                                         # c2v004
        new['numerics']['block'] = copy.deepcopy(blk)
    if 'disk_guard.per_call_bytes' in sets or 'per_call.output_cap_bytes' in sets:
        if new['disk_guard']['per_call_bytes'] < int(new['per_call']['output_cap_bytes']):
            return None, {'ok': False, 'reasons': ['disk_guard.per_call_bytes < per_call.output_cap_bytes (parent L1748)']}
    out_bytes = (json.dumps(new, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    fp, fn = flat(pred), flat(new)
    changed = sorted(k for k in set(fp) | set(fn) if fp.get(k, '<absent>') != fn.get(k, '<absent>'))
    illegal = [k for k in changed if not any(k == a or k.startswith(a + '.') for a in ALLOWED)]
    if blk is not None:                                         # c2v004: the two slots are the only block leaves that may change
        illegal = [k for k in illegal if not any(k == a or k.startswith(a + '.') for a in SLOT_PATHS)]
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
    if blk is not None:                                         # c2v004: verified on the output bytes, then reported
        written = json.loads(out_bytes)['numerics']['block']
        if canon(written) != canon(blk) or canon(strip_slots(written)) != canon(strip_slots(pred['numerics']['block'])):
            return None, {'ok': False, 'reasons': ['the written numerics.block is not block_source.numerics (BLOCK_NOT_DERIVED)']}
        bl = sorted(k for k in changed if k.startswith('numerics.block.'))
        rep.update({'block_rule': BLOCK_RULE, 'block_source': dict(block_source),
                    'block_derived_equals_block_source_numerics': True, 'block_strip_slots_equal': True,
                    'block_changed_paths': bl, 'changed_paths_in_parent_cache_key': bl,
                    'block_canonical_sha256': {'from': sha_b(canon(pred['numerics']['block']).encode()),
                                               'to': sha_b(canon(written).encode())},
                    'block_note': 'numerics.block enters the parent base spec (parent L1760, L1765): base_spec_sha256, the '
                                  'parent cache id (L1774-1780) and the wrapper cache id change; capability evidence and '
                                  'the adoption derivation must be made under this config'})
    return out_bytes, rep


def main(argv):
    seal_p = seal_s = None
    block_pin = None                                            # c2v004
    if '--seal-record' in argv:
        i = argv.index('--seal-record')
        seal_p, argv = argv[i + 1], argv[:i] + argv[i + 2:]
        j = argv.index('--seal-record-sha256')
        seal_s, argv = argv[j + 1], argv[:j] + argv[j + 2:]
    if '--block-source' in argv:                                # c2v004
        i = argv.index('--block-source')
        block_p, argv = argv[i + 1], argv[:i] + argv[i + 2:]
        j = argv.index('--block-source-sha256')
        block_s, argv = argv[j + 1], argv[:j] + argv[j + 2:]
        block_pin = {'path': block_p, 'sha256': block_s}
    if '--block-source-sha256' in argv:                         # c2v004: a sha without its --block-source is never a path
        print(json.dumps({'ok': False, 'reasons': ['--block-source-sha256 without --block-source']}, indent=1))
        return 2
    pred_p, delta_p, out_p = argv[:3]
    out_bytes, rep = apply(Path(pred_p).read_bytes(), json.loads(Path(delta_p).read_text()),
                           Path(seal_p).read_bytes() if seal_p else None, seal_s, block_source=block_pin)
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
