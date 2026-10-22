"""S4-R-C1 LO slot proof c3v003 (A134: Q5, Q9a and (a)4). Claude3 builds it; Codex1 reviews it in one pass (FROM_CODEX/0688).

c3v003 is the erratum-class successor of lo_slot_proof_c3v002 (398d988e; root ruling A138, FROM_CODEX/0703). It changes only:
- V03: the (a)4 bitwise rho comparison (the anchor pair, and the anchor slot against the pair) is wrapper v002's 10-key
  canonical comparison (7a6af535 L177-179 and L189-191; core dc895f8a canonical L34-35): rho_bitwise_canonical().
  The c3v002 projection (partition plus rho_used bits) stays in the proof as a recorded diagnostic only.
No threshold, scope or normalization changes. The proof format is unchanged.

c3v002 is the erratum-class successor of lo_slot_proof_c3v001 (2935a78f; A134 Q2 rule; FROM_CODEX/0696). It changes only:
- F4: the s4rc1_common Refusal and every writer refusal are caught in _prove and in main(): a structured BLOCKED
  result, never a crash;
- F5: check_rho_record reads the rho record's producer bytes and verifies them against a1dcdea8;
- F9: main() runs the root-ruling gate before it reads any pin (args, spec, rho records).
No threshold, scope or normalization changes. The proof format is unchanged.

This module binds the driver lo_certificate slot to the point's REGISTERED rho record. It emits a PROOF_SCHEMA
proof with gate LO_RHO_SLOT and status TESTED/PASS, in the form that wrapper r10_c4 L145-161 accepts once Q5's
stated change is applied (INTERFACE_C3V001 section 1).
- The proof certifies no LO. LO is decided per consumed state at post-run acceptance (Q2, Q3, Q5).
- The proof NEVER carries covers_all_consumed_states (Q5).
- rho binds the slot only after two registered rho runs at the anchor key agree bitwise ((a)4).
- The rho record is read, never produced: no rho, LO or per-state number is computed here.

Root gate: the A134 text of record (56774ba7) and FROM_CODEX/0688 (bcb6df8e) are pinned, and both are re-read
from bytes before anything else. The module refuses to act unless its own sha is in the caller's
approved-producer list (C1, root), and it emits a producer pin only from a canonical __file__ (R4).
Writes are exclusive create through s4rc1_common_c3v002.write_new (fa48b1a1), loaded read-only by path and sha.
"""
import datetime
import hashlib
import importlib.util
import json
import math
import os
import struct
import sys
import types

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
COMMON = (ART + '/s4rc1_c3/build_c3v002/s4rc1_common_c3v002.py',
          'fa48b1a16d26ff14445f6823bd7c15554e50bd0f75b882e0564c4e40980055ce')
CUSTODY = (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377')
RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
ROOT_RULINGS = (
    {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
             'CLAUDE2/S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md',
     'sha256': '56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82'},
    {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0688_2026-10-19_A134_S4RC1_LO_route_ruled_owners.md',
     'sha256': 'bcb6df8e9cbd7d01c7c10e4673fb6ca60ecf6c4a439be4db6140ed521689b30d'},
)
RESULT_SCHEMA = 'S4RC1_LO_SLOT_PROOF_RESULT_C3V001'
PROOF_SCHEMA = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'          # guard v003 L14
GATE = 'LO_RHO_SLOT'                                          # wrapper successor L148 (INTERFACE OPEN-8)
RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'                # response producer a1dcdea8 L30
RHO_GATE = 'RHO_G'
RHO_VERDICT = 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED'            # response producer L360
RHO_COVERAGE = [4.0, 182.0]                                   # [4, ceil(sqrt(2) * 128)]
RHO_PARTITION = [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0],
                 [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]  # response producer shell_plan(unit=False) L112-121
ANCHOR_KEY = '8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8'   # TAIL_REANCHOR (common POINTS[0])
FORBIDDEN_PROOF_KEYS = ('covers_all_consumed_states', 'cover_all_consumed_states')  # A134 Q5
RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')   # V03: wrapper v002 L177-178
SLOT_RULE = 'A134_Q5_LO_SLOT_IS_THE_POINTS_REGISTERED_RHO_RECORD'
LO_ROUTE = 'PER_STATE_POST_RUN_ACCEPTANCE_ALL_CONSUMED_STATES'
THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')   # single-thread BLAS: rho bitwise reproducibility


class Refusal(Exception):
    """Fail-closed refusal with a stable code."""


CAUGHT = (Refusal, ValueError, KeyError, TypeError, OSError, OverflowError, AttributeError)   # c3v001 _prove tuple


def _common_refusals():
    """F4: the Refusal class of every loaded copy of the pinned s4rc1_common module (COMMON). It subclasses Exception,
    not ValueError, so it is named here: a writer or path-policy refusal then gives a structured result, never a crash."""
    out = []
    for m in list(sys.modules.values()):
        try:
            if getattr(m, '__file__', None) == COMMON[0] and isinstance(getattr(m, 'Refusal', None), type):
                out.append(m.Refusal)
        except Exception:
            continue
    return tuple(out)


def _gate_reader(ref):
    """F9: the CLI root gate's own exact-bytes reader, so no module is loaded and no pin is read before the gate."""
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'} or not isinstance(ref['path'], str) \
            or not os.path.isabs(ref['path']):
        raise Refusal('ROOT_RULING_PIN_MALFORMED')
    with open(ref['path'], 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise Refusal('byte pin mismatch')
    return raw


def _load_exact(path, sha, name):
    """Import a pinned module from its canonical absolute path and the exact hashed bytes."""
    if not isinstance(path, str) or not os.path.isabs(path) or os.path.realpath(path) != path:
        raise Refusal('NONCANONICAL_MODULE_PATH: ' + str(path))
    with open(path, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise Refusal('MODULE_PIN_MISMATCH: ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


_COMMON = {}


def common():
    """s4rc1_common_c3v002 (fa48b1a1), read-only, loaded once by exact path and sha."""
    if 'C' not in _COMMON:
        _COMMON['C'] = _load_exact(COMMON[0], COMMON[1], 's4rc1_proofside_common_c3v002_slot')
    return _COMMON['C']


def _self_pin():
    """R4: the producer pin comes from the canonical __file__ only (the wrapper matches whole dicts, L158)."""
    p = __file__
    if not isinstance(p, str) or not os.path.isabs(p) or os.path.realpath(p) != p:
        raise Refusal('NONCANONICAL_PRODUCER_FILE (R4): ' + str(p))
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def _is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def _is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and _is_sha(x['sha256'])


def _float(x, name):
    if type(x) not in (int, float) or not math.isfinite(x):
        raise Refusal('NONFINITE_OR_NONNUMERIC: ' + name)
    return float(x)


def bits(x):
    """IEEE-754 binary64 bit pattern (little-endian hex) of a finite number: the 'bitwise' comparison unit."""
    return struct.pack('<d', _float(x, 'rho_used')).hex()


def rho_projection(rec):
    """INTERFACE section 0: [(range_inverse_kpc, bits(rho_used)) per shell], in record order."""
    shells = rec.get('shells') if isinstance(rec, dict) else None
    if not isinstance(shells, list) or not shells:
        raise Refusal('RHO_SHELL_TABLE_MISSING')
    out = []
    for s in shells:
        if not isinstance(s, dict):
            raise Refusal('RHO_SHELL_ROW_INVALID')
        rng = s.get('range_inverse_kpc')
        if not isinstance(rng, list) or len(rng) != 2:
            raise Refusal('RHO_SHELL_RANGE_INVALID')
        rho = _float(s.get('rho_used'), 'rho_used')
        if rho < 0:
            raise Refusal('RHO_NEGATIVE')
        out.append([[_float(rng[0], 'range'), _float(rng[1], 'range')], bits(rho)])
    return out


def rho_bitwise_canonical(rec):
    """V03 (A138): wrapper v002's bitwise rho comparison, exactly (7a6af535 L177-179 and L189-191): the canonical JSON
    (core dc895f8a L34-35, the same as canonical() here) of the 10 RHO_COMPARE_KEYS, an absent key read as None. Two rho
    records are bitwise equal iff these bytes are identical. JSON floats round-trip exactly, so a 1-ulp change in any
    compared field differs, a diagnostic such as rho_envelope.estimate included, and +0.0 differs from -0.0. Run metadata
    (utc, seconds, peak_rss_bytes) and provenance pins are not compared (wrapper L176)."""
    if not isinstance(rec, dict):
        raise Refusal('RHO_RECORD_NOT_AN_OBJECT')
    return canonical({k: rec.get(k) for k in RHO_COMPARE_KEYS})


def check_rho_record(rec, *, read_raw, identity=None, custody=None, point_sha256=None):
    """Read-only checks of a registered rho record (response producer a1dcdea8 produce_rho L332-364).

    F5 (c3v002): the record's producer bytes are read through read_raw (an exact {path, sha256} reader that hashes
    the bytes) and must be the a1dcdea8 bytes; the sha string alone is not accepted."""
    if not isinstance(rec, dict):
        raise Refusal('RHO_RECORD_NOT_AN_OBJECT')
    if rec.get('schema') != RHO_SCHEMA or rec.get('gate') != RHO_GATE:
        raise Refusal('RHO_SCHEMA_OR_GATE_MISMATCH')
    if rec.get('status') != 'TESTED' or rec.get('verdict') != RHO_VERDICT:
        raise Refusal('RHO_STATUS_OR_VERDICT_MISMATCH')
    if rec.get('settings') != 'registered' or rec.get('full_registered_search_executed') is not True:
        raise Refusal('RHO_SETTINGS_NOT_REGISTERED_FULL_SEARCH (no smoke or partial rho)')
    if rec.get('coverage_complete') is not True or rec.get('required_coverage_inverse_kpc') != RHO_COVERAGE:
        raise Refusal('RHO_COVERAGE_NOT_4_TO_182')
    if [s.get('range_inverse_kpc') for s in rec.get('shells') or [] if isinstance(s, dict)] != RHO_PARTITION:
        raise Refusal('RHO_PARTITION_NOT_REGISTERED')
    producer = rec.get('producer')
    if not _is_pin(producer) or producer['sha256'] != RESPONSE_SHA:
        raise Refusal('RHO_PRODUCER_NOT_RESPONSE_A1DCDEA8')
    try:
        read_raw(dict(producer))                                  # F5: the producer's bytes are read (sha from bytes)
    except Exception as exc:
        raise Refusal('RHO_PRODUCER_BYTES_NOT_A1DCDEA8 (F5: %s: %s: %s)' % (producer['path'], type(exc).__name__, exc))
    if not isinstance(rec.get('identity'), dict) or rec.get('point_sha256') != digest(rec['identity']):
        raise Refusal('RHO_IDENTITY_POINT_SHA_INCONSISTENT')
    if identity is not None and (rec.get('identity') != identity or rec.get('custody') != custody
                                 or rec.get('point_sha256') != point_sha256):
        raise Refusal('RHO_POINT_CUSTODY_MISMATCH')
    return rho_projection(rec)


def root_gate(root_ruling_refs, read_raw):
    """A134 root gate: whole-dict equality with the pinned rulings, in order, then bytes re-read (sha)."""
    refs = list(root_ruling_refs) if isinstance(root_ruling_refs, (list, tuple)) else None
    if refs is None or len(refs) != len(ROOT_RULINGS) or any(a != b for a, b in zip(refs, ROOT_RULINGS)):
        raise Refusal('ROOT_RULING_A134_NOT_PINNED (S4RC1 text of record 56774ba7 and FROM_CODEX/0688 bcb6df8e '
                      'are required, in that order)')
    for ref in refs:
        try:
            read_raw(dict(ref))
        except Exception as exc:
            raise Refusal('ROOT_RULING_UNREADABLE_OR_CHANGED: %s: %s' % (ref['path'], exc))
    return [dict(r) for r in refs]


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _real_env():
    """Lazy: nothing is loaded until a function is called (and never before the root gate)."""
    state = {}

    def cu():
        if 'cu' not in state:
            state['cu'] = _load_exact(CUSTODY[0], CUSTODY[1], 's4rc1_proofside_slot_custody_cx2v002')
        return state['cu']

    return types.SimpleNamespace(
        derive_details=lambda spec: cu().derive_details(spec=spec),
        read_pin=lambda ref: cu().read_pin(ref),
        read_raw=lambda ref: cu().read_pin(ref, document=False),
        self_pin=_self_pin, utc=_utc)


def _in_list(pin, pins):
    return isinstance(pins, (list, tuple)) and any(_is_pin(p) and p == pin for p in pins)


def _prove(spec, rho_ref, *, registered_rho_records, anchor_rho_pair, root_ruling_refs,
           approved_producer_sha256, env):
    out = {'schema': RESULT_SCHEMA, 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'BLOCKED', 'blockers': [],
           'proof': None, 'driver_certificate': None}
    try:
        # 1. Root gate before anything is derived, loaded or read.
        out['root_rulings'] = root_gate(root_ruling_refs, env.read_raw)
        me = env.self_pin()
        if not isinstance(approved_producer_sha256, (list, tuple, set, frozenset)) or me['sha256'] not in set(approved_producer_sha256):
            raise Refusal('LO_SLOT_PROOF_PRODUCER_NOT_APPROVED (C1 approved_certificate_producers; review first)')
        # 2. Registered rho only, by exact pin (whole dict: path and sha).
        if not _is_pin(rho_ref):
            raise Refusal('RHO_REF_NOT_AN_EXACT_PIN')
        if not _in_list(rho_ref, registered_rho_records):
            raise Refusal('RHO_NOT_REGISTERED (root registered_rho_records; whole-dict match)')
        # 3. The driver slot is this rho pin.
        slot = ((spec or {}).get('numerics') or {}).get('uv_tail', {}).get('lo_certificate')
        if slot != rho_ref:
            raise Refusal('LO_SLOT_NOT_BOUND_TO_REGISTERED_RHO (spec numerics.uv_tail.lo_certificate)')
        # 4. Independent custody; 5. the rho record itself.
        details = env.derive_details(spec)
        rho = env.read_pin(rho_ref)
        proj = check_rho_record(rho, read_raw=env.read_raw, identity=details['identity'], custody=details['custody'],
                                point_sha256=details['point_sha256'])
        # 6. (a)4: two registered rho runs at the anchor key agree bitwise.
        pair = list(anchor_rho_pair) if isinstance(anchor_rho_pair, (list, tuple)) else []
        if len(pair) != 2 or not all(_is_pin(p) for p in pair):
            raise Refusal('ANCHOR_RHO_REPRODUCIBILITY_UNPROVEN ((a)4: two registered anchor rho runs required)')
        if not all(_in_list(p, registered_rho_records) for p in pair):
            raise Refusal('ANCHOR_RHO_RUN_NOT_REGISTERED')
        if pair[0]['sha256'] == pair[1]['sha256'] or pair[0]['path'] == pair[1]['path']:
            raise Refusal('ANCHOR_RHO_PAIR_NOT_TWO_RUNS (distinct records required)')
        anchors = [env.read_pin(p) for p in pair]
        aproj = [check_rho_record(a, read_raw=env.read_raw) for a in anchors]
        if any(a.get('point_sha256') != ANCHOR_KEY for a in anchors):
            raise Refusal('ANCHOR_RHO_RUN_NOT_AT_ANCHOR_KEY')
        if anchors[0].get('custody') != anchors[1].get('custody') or anchors[0].get('identity') != anchors[1].get('identity'):
            raise Refusal('ANCHOR_RHO_RUNS_DIFFER_IN_POINT_OR_CUSTODY')
        if rho_bitwise_canonical(anchors[0]) != rho_bitwise_canonical(anchors[1]):      # V03: wrapper v002 L177-191
            raise Refusal('ANCHOR_RHO_NOT_BITWISE_EQUAL ((a)4 fails; rho may not bind any lo slot)')
        if details['point_sha256'] == ANCHOR_KEY and rho_bitwise_canonical(rho) != rho_bitwise_canonical(anchors[0]):
            raise Refusal('ANCHOR_SLOT_RHO_NOT_BITWISE_EQUAL_TO_REPRODUCED_PAIR')
        full_same = canonical(anchors[0].get('shells')) == canonical(anchors[1].get('shells'))
        proof = {'schema': PROOF_SCHEMA, 'gate': GATE, 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'PASS',
                 'point_sha256': details['point_sha256'], 'custody_sha256': details['custody_sha256'],
                 'producer': me, 'driver_certificate': dict(rho_ref), 'rho_record': dict(rho_ref),
                 'rho_bitwise_projection': proj, 'rho_bitwise_projection_sha256': digest(proj),
                 'anchor_rho_reproducibility': {
                     'records': [dict(p) for p in pair], 'anchor_point_sha256': ANCHOR_KEY, 'bitwise_equal': True,
                     'projection_sha256': digest(aproj[0]),
                     'full_shell_records_identical_diagnostic_only': full_same},
                 'slot_rule': SLOT_RULE, 'lo_route': LO_ROUTE, 'lo_certified': False,
                 'root_rulings': out['root_rulings'],
                 'scope': ('Binds the driver lo_certificate slot to the point\'s registered rho record only. It '
                           'certifies no LO: LO is decided per consumed state at post-run acceptance (A134 Q2/Q3/Q5). '
                           'rho is a numerical maximum estimate, not a rigorous supremum.')}
        _refuse_forbidden(proof)
        out.update(verdict='READY_FOR_MANIFEST', proof=proof, driver_certificate=dict(rho_ref))
    except (CAUGHT + _common_refusals()) as exc:                  # F4
        out['blockers'].append(type(exc).__name__ + ': ' + str(exc))
    return out


def _refuse_forbidden(proof):
    bad = [k for k in FORBIDDEN_PROOF_KEYS if k in proof]
    if bad:
        raise Refusal('LO_SLOT_PROOF_MUST_NOT_CARRY ' + ','.join(bad) + ' (A134 Q5)')


def prove_lo_slot(spec, rho_ref, *, registered_rho_records=(), anchor_rho_pair=(), root_ruling_refs=None,
                  approved_producer_sha256=()):
    """Public entry. BLOCKED unless the A134 root gate, approval, registration, slot and (a)4 all hold."""
    return _prove(spec, rho_ref, registered_rho_records=registered_rho_records, anchor_rho_pair=anchor_rho_pair,
                  root_ruling_refs=root_ruling_refs, approved_producer_sha256=approved_producer_sha256,
                  env=_real_env())


def write_proof(result, out_root, name=None):
    """Exclusive-create the proof of a READY_FOR_MANIFEST result under out_root. Returns its exact pin."""
    proof = (result or {}).get('proof')
    if (result or {}).get('verdict') != 'READY_FOR_MANIFEST' or not isinstance(proof, dict):
        raise Refusal('NO_PROOF_TO_WRITE (verdict %s)' % (result or {}).get('verdict'))
    _refuse_forbidden(proof)
    if proof.get('schema') != PROOF_SCHEMA or proof.get('gate') != GATE or proof.get('status') != 'TESTED' or proof.get('verdict') != 'PASS':
        raise Refusal('PROOF_SHAPE_INVALID')
    C = common()
    name = name or 'LO_RHO_SLOT_PROOF_%s.json' % proof['point_sha256'][:16]
    return C.write_new(os.path.join(out_root, name), proof, out_root)


def main(argv=None):
    """CLI: refusals first (taskpolicy -b; python3 -I -B), then one pinned JSON argument file."""
    C = None
    if not _background_qos():
        print('REFUSED: BACKGROUND_QOS_REQUIRED (run under taskpolicy -b)', flush=True)
        return 2
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B)', flush=True)
        return 2
    import argparse
    ap = argparse.ArgumentParser(description='LO slot proof (A134 Q5)')
    ap.add_argument('--args', required=True, help='JSON file: spec_ref, rho_ref, registered_rho_records, '
                    'anchor_rho_pair, root_ruling_refs, approved_producer_sha256')
    ap.add_argument('--args-sha256', required=True)
    ap.add_argument('--out-root', required=True)
    a = ap.parse_args(argv)
    try:
        root_gate(ROOT_RULINGS, _gate_reader)          # F9: the root-ruling gate runs before any pin is read
    except (CAUGHT + _common_refusals()) as exc:
        print(json.dumps({'verdict': 'BLOCKED', 'blockers': [type(exc).__name__ + ': ' + str(exc)], 'proof': None,
                          'result': None}), flush=True)
        return 3
    try:                                               # F4: a refusal is a structured result, never a crash
        C = common()
        args = C.read_json_pinned({'path': a.args, 'sha256': a.args_sha256}, (ART,), 'args')
        env = _real_env()
        spec = env.read_pin(args['spec_ref'])
        res = _prove(spec, args.get('rho_ref'), registered_rho_records=args.get('registered_rho_records', ()),
                     anchor_rho_pair=args.get('anchor_rho_pair', ()), root_ruling_refs=args.get('root_ruling_refs'),
                     approved_producer_sha256=args.get('approved_producer_sha256', ()), env=env)
        pin = write_proof(res, a.out_root) if res['verdict'] == 'READY_FOR_MANIFEST' else None
        res_pin = C.write_new(os.path.join(a.out_root, 'LO_RHO_SLOT_RESULT_%s.json' % C.utc_compact()), res, a.out_root)
    except (CAUGHT + _common_refusals()) as exc:
        print(json.dumps({'verdict': 'BLOCKED', 'blockers': [type(exc).__name__ + ': ' + str(exc)], 'proof': None,
                          'result': None}), flush=True)
        return 3
    print(json.dumps({'verdict': res['verdict'], 'blockers': res['blockers'], 'proof': pin, 'result': res_pin}), flush=True)
    return 0 if pin else 3


def _background_qos():
    """True only under taskpolicy -b (PRIO_DARWIN_BG): getpriority(PRIO_DARWIN_PROCESS=4, 0) == 1."""
    try:
        return os.getpriority(4, 0) == 1
    except Exception:
        return False


if __name__ == '__main__':
    for _k in THREAD_ENV:          # before numpy is imported (all numpy imports are lazy)
        os.environ[_k] = '1'
    sys.exit(main())
