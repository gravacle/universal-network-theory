"""S4-R-C1 per-state LO proof adapter c3v003 (A134: Q2, Q3, Q4, Q5). Claude3 builds it; Codex1 reviews it in one pass (0688).

c3v003 is the erratum-class successor of lo_state_proof_adapter_c3v002 (8cae0b1a; root ruling A138, FROM_CODEX/0703).
It changes only:
- V02: the inventory enumerator pin is the b1 enumerator consumed_states_b1_c2v001 (4ca7f364; offset_b1 README item 4,
  the C1 state_enumerator) in place of consumed_states_cx2v010 (e48cca3c). A v010 inventory is refused;
- V03: the rho recompute is compared with the slot rho by wrapper v002's 10-key canonical comparison (7a6af535
  L177-179, L189-191): rho_bitwise_canonical(). The c3v002 projection is recorded beside it as a diagnostic only;
- B3: the call reading is exactly FROM_CODEX/0690 OPEN-6. A FAIL at an accepted, inherited or route-B state is decisive
  (NON_LAPSE_TAIL_MATERIAL) even when other states are UNAVAILABLE; LO_UNCERTIFIED_TRANSIENT needs every non-iterate
  state at PASS, so an UNAVAILABLE iterate no longer blocks it; otherwise INCOMPLETE, with the iterate failures recorded.
No threshold, scope or normalization changes. The proof and state-reading formats are unchanged; each call-record
state entry gains one diagnostic key (V03).

c3v002 is the erratum-class successor of lo_state_proof_adapter_c3v001 (495cdf4e; A134 Q2 rule; FROM_CODEX/0696).
It changes only:
- F3: lo_config's certificate_slots_bound is honoured. If it is not True, the state reads UNAVAILABLE with
  ACTUAL_POINT_CERTIFICATE_SLOTS_UNBOUND, exactly as lo_config L85-90 does (after the core; the core record is kept);
- F4: the s4rc1_common Refusal and every writer refusal are caught in the entry points and in main(): a structured
  INCOMPLETE/UNAVAILABLE result, never a crash;
- F5: check_rho_record reads the rho record's producer bytes and verifies them against a1dcdea8;
- F6: lo_producer_cx2v004 L71-78 is re-applied: the row reference's state_files must be non-empty and inside the
  run root (and are read from bytes), with v004's blocker names;
- F9: main() runs the root-ruling gate before it reads any pin.
No threshold, scope or normalization changes. The proof and record formats are unchanged.

At post-run acceptance, for EVERY consumed state in the call's inventory (c3v003, V02: the b1 enumerator
consumed_states_b1_c2v001, 4ca7f364, which writes the v010 join schema), this adapter does the following:
- It runs the UNCHANGED lo_core produce_current_lo (lo_core_r5_cx2v001, 12d36305, L190-267).
- It requires the rho that call recomputes to equal the slot's registered rho BITWISE (Q5; c3v003, V03: wrapper
  v002's 10-key canonical comparison).
- It requires |v_i| to be the maximum over every readout of row i that THIS call recorded (Q4a). A state whose call
  recorded no readout reads UNAVAILABLE, with no substitution.
- It emits, for a PASS state, a guard-format LO proof (guard v003 L205-219). For any other state it emits a reading
  record: the frozen Q5 readings, or UNAVAILABLE.

tau_i = 0.25 sigma_i enters only through row_contract_sha256. The LO thresholds stay in lo_core L171 and guard
L210-215; this module declares no threshold. Before the core it also runs lo_config_r5_cx2v001 (6654d93c, unchanged)
validate_current_config, and re-applies lo_producer v004's own-run rules (L56-70; c3v002 adds L71-78, F6).

Root gate: A134 text of record 56774ba7 and FROM_CODEX/0688 bcb6df8e, pinned and re-read from bytes.
Self-approval: the module's own sha must be in root's C1 list. Producer pins come from a canonical __file__ (R4).
Writes are exclusive create through s4rc1_common_c3v002.write_new (fa48b1a1).
The builder exercised this module on synthetic fixtures only.
"""
import datetime
import hashlib
import importlib.util
import io
import json
import math
import os
import struct
import sys
import types
from pathlib import Path

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
COMMON = (ART + '/s4rc1_c3/build_c3v002/s4rc1_common_c3v002.py',
          'fa48b1a16d26ff14445f6823bd7c15554e50bd0f75b882e0564c4e40980055ce')
CUSTODY = (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377')
LO_CONFIG = (CERT + '/lo_config_r5_cx2v001.py', '6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a')
LO_CORE = (CERT + '/lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e')
RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
ENUMERATOR_SHA = '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'   # V02: b1 enumerator consumed_states_b1_c2v001
ROOT_RULINGS = (
    {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
             'CLAUDE2/S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md',
     'sha256': '56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82'},
    {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0688_2026-10-19_A134_S4RC1_LO_route_ruled_owners.md',
     'sha256': 'bcb6df8e9cbd7d01c7c10e4673fb6ca60ecf6c4a439be4db6140ed521689b30d'},
)
PROOF_SCHEMA = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'           # guard v003 L14
STATE_READING_SCHEMA = 'S4RC1_LO_STATE_READING_C3V001'
CALL_SCHEMA = 'S4RC1_LO_CALL_ACCEPTANCE_C3V001'
INVENTORY_SCHEMA = 'DDO154_CONSUMED_STATE_JOIN_CX2V010'
STATE_INPUT_SCHEMA = 'UNT_POINT_LO_STATE_INPUT_CX2V001'        # lo_core L34
ROWS_SCHEMA = 'UNT_POINT_LO_ROWS_CX2V001'                      # lo_core L219
SOURCE_SCHEMA = 'UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001'      # lo_core L236
CORE_SCHEMA = 'UNT_POINT_LO_NUMERICAL_CX2V001'                 # lo_core L36
CORE_KIND = 'CURRENT_SAVED_STATE'                              # lo_core L260
CORE_PASS_VERDICT = 'CURRENT_LO_NUMERICAL_EVIDENCE_REVIEW_REQUIRED'   # lo_core L264
CORE_THRESHOLD_BLOCKER = 'LO_NUMERICAL_INDICATOR_ABOVE_THRESHOLD'    # lo_core L258-259
SLOT_GATE = 'LO_RHO_SLOT'
RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'
RHO_GATE = 'RHO_G'
RHO_VERDICT = 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED'
RHO_COVERAGE = [4.0, 182.0]
RHO_PARTITION = [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0],
                 [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]
ANCHOR_KEY = '8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8'
SPEED_POLICY = 'A134_Q4A_OWN_CALL_MAX_ABS_OVER_EVERY_RECORDED_READOUT'
READOUT_SET = 'RESULT_PASSES_ROWS_SPEED_KM_S (every Picard pass of this call; INTERFACE OPEN-1)'
FORBIDDEN_PROOF_KEYS = ('covers_all_consumed_states', 'cover_all_consumed_states')
RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')   # V03: wrapper v002 L177-178
EXECUTION_KEYS = {'fresh_call': True, 'resumed': False, 'retried': False, 'route_a_completed_normally': True}
# Q5 state classes (from the inventory only) and frozen readings.
ACCEPTED = 'ACCEPTED_ROUTE_A'
INHERITED = 'INHERITED_ROUTE_A'
ROUTE_B = 'ROUTE_B_STAGE'
ITERATE = 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'
CLASS_UNAVAILABLE = 'UNAVAILABLE'
DECISIVE_CLASSES = (ACCEPTED, INHERITED, ROUTE_B)
R_PASS = 'PASS'
R_NLTM = 'NON_LAPSE_TAIL_MATERIAL'
R_TRANSIENT = 'LO_UNCERTIFIED_TRANSIENT'
R_ANCHOR = 'ANCHOR_LO_FAILURE_PRESERVED_STEP4_STOPS_FOR_ROOT'
R_CLASS_GAP = 'LO_FAIL_STATE_CLASS_UNAVAILABLE'
R_INCOMPLETE = 'INCOMPLETE'
ROUTE_A_ITERATE_ROLES = {'current_begin_inferred_from_completion', 'next_built_and_monitor_consumed'}
ROUTE_B_ROLES = {'own_source_state', 'signed_body_minus_route_a'}
STATE_KEYS = {'state_sha256', 'source_sha256', 'stage_kind', 'nonnegative_masses'}
THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')   # single-thread BLAS: rho bitwise reproducibility
CAUGHT = (ValueError, KeyError, TypeError, OSError, OverflowError, AttributeError, IndexError,
          ZeroDivisionError, FloatingPointError)


class Refusal(ValueError):
    """Fail-closed refusal with a stable code."""


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
    if 'C' not in _COMMON:
        _COMMON['C'] = _load_exact(COMMON[0], COMMON[1], 's4rc1_proofside_common_c3v002_state')
    return _COMMON['C']


def _self_pin():
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
    if isinstance(x, bool) or type(x) not in (int, float) or not math.isfinite(x):
        raise Refusal('NONFINITE_OR_NONNUMERIC: ' + name)
    return float(x)


def bits(x, name='value'):
    return struct.pack('<d', _float(x, name)).hex()


def rho_projection(rec):
    """Identical definition to lo_slot_proof_c3v001.rho_projection (INTERFACE section 0; the suite checks parity)."""
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
        out.append([[_float(rng[0], 'range'), _float(rng[1], 'range')], bits(rho, 'rho_used')])
    return out


def rho_bitwise_canonical(rec):
    """Identical definition to lo_slot_proof_c3v003.rho_bitwise_canonical (the suite checks parity).

    V03 (A138): wrapper v002's bitwise rho comparison, exactly (7a6af535 L177-179 and L189-191): the canonical JSON
    (core dc895f8a L34-35, the same as canonical() here) of the 10 RHO_COMPARE_KEYS, an absent key read as None. Two rho
    records are bitwise equal iff these bytes are identical. JSON floats round-trip exactly, so a 1-ulp change in any
    compared field differs, a diagnostic such as rho_envelope.estimate included, and +0.0 differs from -0.0. Run metadata
    (utc, seconds, peak_rss_bytes) and provenance pins are not compared (wrapper L176)."""
    if not isinstance(rec, dict):
        raise Refusal('RHO_RECORD_NOT_AN_OBJECT')
    return canonical({k: rec.get(k) for k in RHO_COMPARE_KEYS})


def check_rho_record(rec, *, read_raw, identity=None, custody=None, point_sha256=None):
    """Identical checks to lo_slot_proof_c3v002.check_rho_record.

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


# ----------------------------------------------------------------------------------------------- Q4a speeds
def own_call_vmax(result, row_ids):
    """Q4a: |v_i| = max over every readout of row i that THIS call recorded (result.passes[*].rows; OPEN-1).

    Returns floats in row-contract order. Raises (state UNAVAILABLE, nothing substituted) when the call recorded
    no pass, a pass row list is not in the exact row-contract order, or any readout is missing or non-finite.
    """
    passes = result.get('passes') if isinstance(result, dict) else None
    if not isinstance(passes, list) or not passes:
        raise Refusal('OWN_CALL_READOUT_UNAVAILABLE: the call recorded no readout (no pass); nothing is substituted')
    vmax = [None] * len(row_ids)
    for p in passes:
        rows = p.get('rows') if isinstance(p, dict) else None
        if not isinstance(rows, list) or [r.get('id') if isinstance(r, dict) else None for r in rows] != list(row_ids):
            raise Refusal('OWN_CALL_READOUT_UNAVAILABLE: pass rows are not the exact row-contract order')
        for i, r in enumerate(rows):
            v = r.get('speed_km_s')
            if isinstance(v, bool) or type(v) not in (int, float) or not math.isfinite(v):
                raise Refusal('OWN_CALL_READOUT_UNAVAILABLE: row %s has a missing or non-finite readout' % row_ids[i])
            a = abs(float(v))
            vmax[i] = a if vmax[i] is None or a > vmax[i] else vmax[i]
    if 'rows' in result and result['rows'] != passes[-1].get('rows'):
        raise Refusal('OWN_CALL_FINAL_ROWS_DIFFER_FROM_FINAL_PASS')
    return vmax


# ----------------------------------------------------------------------------------------------- Q5 classes
def state_classes(inventory):
    """Q5 class per unique consumed state, from the v010 inventory only.

    Returns (classes: {digest(state): (class, roles, stages)}, gap or None, accepted digest or None).
    """
    occ, joined = inventory.get('occurrences'), inventory.get('joined_occurrences')
    if not isinstance(occ, list) or not isinstance(joined, list) or not joined:
        return {}, 'STATE_CLASS_UNAVAILABLE: inventory lacks occurrences/joined_occurrences', None
    by_ord = {}
    for o in occ:
        if not isinstance(o, dict) or type(o.get('ordinal')) is not int or o['ordinal'] in by_ord:
            return {}, 'STATE_CLASS_UNAVAILABLE: occurrence ordinals invalid', None
        by_ord[o['ordinal']] = o
    boundary = [o for o in occ if o.get('role') == 'boundary_at_return']
    if len(boundary) != 1 or not _is_sha(boundary[0].get('state_sha256_claimed')):
        return {}, 'STATE_CLASS_UNAVAILABLE: no unique boundary_at_return (accepted) occurrence', None
    accepted = boundary[0]['state_sha256_claimed']
    roles = {}
    for j in joined:
        o = by_ord.get(j.get('ordinal')) if isinstance(j, dict) else None
        if o is None or not isinstance(j.get('state'), dict):
            return {}, 'STATE_CLASS_UNAVAILABLE: joined occurrence without a discovery occurrence', None
        k = digest(j['state'])
        roles.setdefault(k, (set(), set()))
        roles[k][0].add(o.get('role'))
        roles[k][1].add(o.get('stage'))
    out = {}
    for s in inventory.get('states') or []:
        k = digest(s)
        r, stages = roles.get(k, (set(), set()))
        if not r:
            cls = CLASS_UNAVAILABLE
        elif s.get('state_sha256') == accepted:
            cls = ACCEPTED
        elif 'inherited_route_a' in r:
            cls = INHERITED
        elif r & ROUTE_B_ROLES:
            cls = ROUTE_B
        elif r <= ROUTE_A_ITERATE_ROLES:
            cls = ITERATE
        else:
            cls = CLASS_UNAVAILABLE
        out[k] = (cls, sorted(x for x in r if isinstance(x, str)), sorted(x for x in stages if isinstance(x, str)))
    return out, None, accepted


def check_inventory(inventory, details):
    if not isinstance(inventory, dict) or inventory.get('schema') != INVENTORY_SCHEMA:
        raise Refusal('INVENTORY_SCHEMA_NOT_V010')
    if inventory.get('complete') is not True:
        raise Refusal('COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED')
    prod = inventory.get('producer')
    if not _is_pin(prod) or prod['sha256'] != ENUMERATOR_SHA:
        raise Refusal('INVENTORY_PRODUCER_NOT_B1_4CA7F364')         # V02
    if inventory.get('point_sha256') != details['point_sha256'] or inventory.get('custody_sha256') != details['custody_sha256']:
        raise Refusal('INVENTORY_POINT_OR_CUSTODY_MISMATCH')
    states = inventory.get('states')
    if not isinstance(states, list) or not states:
        raise Refusal('INVENTORY_STATES_EMPTY')
    seen = set()
    for s in states:
        if not isinstance(s, dict) or set(s) != STATE_KEYS or not _is_sha(s['state_sha256']) or not _is_sha(s['source_sha256']):
            raise Refusal('INVENTORY_STATE_IDENTITY_INVALID')
        if not isinstance(s['stage_kind'], str) or not s['stage_kind'] or type(s['nonnegative_masses']) is not bool:
            raise Refusal('INVENTORY_STATE_IDENTITY_INVALID')
        k = digest(s)
        if k in seen:
            raise Refusal('INVENTORY_STATES_NOT_UNIQUE')
        seen.add(k)
    return states


# ----------------------------------------------------------------------------------------------- env
def _real_env():
    """Lazy: nothing is loaded until used; never before the root gate (the entry points call it first)."""
    state = {}

    def cu():
        if 'cu' not in state:
            state['cu'] = _load_exact(CUSTODY[0], CUSTODY[1], 's4rc1_proofside_state_custody_cx2v002')
        return state['cu']

    def stack():
        if 'cfg' not in state:
            cfg = _load_exact(LO_CONFIG[0], LO_CONFIG[1], 's4rc1_proofside_lo_config_r5_cx2v001')
            v1 = cfg.V1
            if getattr(v1, '__file__', None) != LO_CORE[0] or cu().sha(v1.__file__) != LO_CORE[1]:
                raise Refusal('LO_CORE_NOT_THE_UNCHANGED_12D36305')
            state['cfg'] = cfg
        return state['cfg']

    def validate_config(spec, state_input):
        rec = cu().read_pin(state_input['tail_state']['record'])
        raw = cu().read_pin(state_input['tail_state']['arrays'], document=False)
        import numpy as np
        with np.load(io.BytesIO(raw), allow_pickle=False) as z:
            arrays = {k: z[k] for k in ('kp', 'kz', 'wkp', 'wz')}
        U = stack().V1.CC.uvt_modules()[0]
        return stack().validate_current_config(spec, rec, arrays, U)

    return types.SimpleNamespace(
        derive_details=lambda spec: cu().derive_details(spec=spec),
        read_pin=lambda ref: cu().read_pin(ref),
        read_raw=lambda ref: cu().read_pin(ref, document=False),
        read_bytes=lambda path: cu().allowed_path(path).read_bytes(),
        resolve=lambda path: cu().allowed_path(path),
        point_context=lambda spec: stack().V1.PR.point_context(spec),
        produce_current_lo=lambda spec, ref, **kw: stack().V1.produce_current_lo(spec, ref, **kw),
        validate_config=validate_config,
        write=lambda obj, out_root, name: common().write_new(os.path.join(out_root, name), obj, out_root),
        self_pin=_self_pin, utc=_utc)


# ----------------------------------------------------------------------------------------------- call level
def _call_context(spec, call_dir, result, inventory, bundle_ref, approved, env):
    rp = os.path.join(str(call_dir), 'out', 'result.json')
    raw = env.read_bytes(rp)
    if json.loads(raw) != result:
        raise Refusal('CALL_RESULT_BYTES_DIFFER_FROM_SUPPLIED_RESULT')
    result_pin = {'path': rp, 'sha256': hashlib.sha256(raw).hexdigest()}
    details = env.derive_details(spec)
    states = check_inventory(inventory, details)
    bundle = env.read_pin(bundle_ref)
    if bundle.get('identity') != details['identity'] or bundle.get('custody') != details['custody']:
        raise Refusal('BUNDLE_POINT_OR_CUSTODY_MISMATCH')
    slots = {k: ((spec.get('numerics') or {}).get('uv_tail') or {}).get(k) for k in ('eps_certificate', 'lo_certificate')}
    if not _is_pin(slots['lo_certificate']) or (bundle.get('driver_certificate_bindings') or {}).get('lo_certificate') != slots['lo_certificate']:
        raise Refusal('LO_SLOT_NOT_BOUND_BY_REGISTERED_BUNDLE')
    pre = bundle.get('prelaunch') or {}
    if not _is_pin(pre.get(SLOT_GATE)) or not _is_pin(pre.get('GQ')):
        raise Refusal('BUNDLE_PRELAUNCH_LO_RHO_SLOT_OR_GQ_MISSING')
    sp = env.read_pin(pre[SLOT_GATE])
    if any(k in sp for k in FORBIDDEN_PROOF_KEYS):
        raise Refusal('LO_SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES (A134 Q5)')
    if (sp.get('schema') != PROOF_SCHEMA or sp.get('gate') != SLOT_GATE or sp.get('status') != 'TESTED'
            or sp.get('verdict') != 'PASS'):
        raise Refusal('LO_SLOT_PROOF_NOT_TESTED_PASS')
    if sp.get('point_sha256') != details['point_sha256'] or sp.get('custody_sha256') != details['custody_sha256']:
        raise Refusal('LO_SLOT_PROOF_SCOPE_MISMATCH')
    if sp.get('driver_certificate') != slots['lo_certificate']:
        raise Refusal('LO_SLOT_PROOF_DIFFERS_FROM_DRIVER_SLOT')
    prod = sp.get('producer')
    if not _is_pin(prod) or prod['sha256'] not in approved:
        raise Refusal('LO_SLOT_PROOF_PRODUCER_NOT_APPROVED')
    env.read_raw(prod)
    slot_rho = env.read_pin(slots['lo_certificate'])
    slot_proj = check_rho_record(slot_rho, read_raw=env.read_raw, identity=details['identity'], custody=details['custody'],
                                 point_sha256=details['point_sha256'])
    if sp.get('rho_bitwise_projection') != slot_proj:
        raise Refusal('LO_SLOT_PROOF_PROJECTION_DIFFERS_FROM_SLOT_RHO')
    return {'result_pin': result_pin, 'details': details, 'states': states, 'bundle': bundle,
            'slot_rho_pin': dict(slots['lo_certificate']), 'slot_proj': slot_proj, 'slot_proof_pin': dict(pre[SLOT_GATE]),
            'gq_sha256': pre['GQ']['sha256'], 'run_root': os.path.join(str(call_dir), 'out'),
            'slot_rho_bitwise': rho_bitwise_canonical(slot_rho)}            # V03: wrapper v002 L179 (want)


def _same_pin(env, a, b):
    """Same bytes and the same resolved file (consumed_states_cx2v010 same_ref precedent)."""
    if not (_is_pin(a) and _is_pin(b)) or a['sha256'] != b['sha256']:
        return False
    try:
        return Path(env.resolve(a['path'])) == Path(env.resolve(b['path']))
    except CAUGHT:
        return False


def _same_dir(env, a, b):
    try:
        return isinstance(a, str) and Path(env.resolve(a)) == Path(env.resolve(b))
    except CAUGHT:
        return False


def _within(env, path, root):
    p = Path(env.resolve(path))
    r = Path(env.resolve(root))
    return p.is_relative_to(r)


def _state_name(state, tag):
    return 'LO_%s_%s.json' % (tag, digest(state)[:24])


def _one_state(spec, state, cls_info, call, vmax, vmax_error, *, state_inputs, trusted_source_producers,
               trusted_reviews, ctx_box, out_root, me, rulings, env):
    details = call['details']
    cls, roles, stages = cls_info
    st = {'state': state, 'state_class': cls, 'roles': roles, 'stages': stages, 'verdict': 'UNAVAILABLE',
          'reading': None, 'blockers': [], 'core_record': None, 'record': None, 'summed_max_over_tau': None}
    core = None
    try:
        ref = (state_inputs or {}).get(state['state_sha256'])
        if not _is_pin(ref):
            raise Refusal('STATE_INPUT_MISSING')
        obj = env.read_pin(ref)
        if obj.get('schema') != STATE_INPUT_SCHEMA or obj.get('state') != state:
            raise Refusal('STATE_INPUT_SCHEMA_OR_STATE_MISMATCH')
        if obj.get('identity') != details['identity'] or obj.get('custody') != details['custody']:
            raise Refusal('STATE_INPUT_POINT_CUSTODY_MISMATCH')
        if not _same_pin(env, obj.get('call_result'), call['result_pin']):
            raise Refusal('STATE_INPUT_NOT_THIS_CALL (call_result pin)')
        ex = obj.get('execution') or {}
        if any(ex.get(k) is not v for k, v in EXECUTION_KEYS.items()):
            raise Refusal('FRESH_COMPLETED_NO_RESUME_NO_RETRY_CALL_NOT_ESTABLISHED (lo_producer v004 L56-59)')
        if not _same_dir(env, ex.get('run_root'), call['run_root']):
            raise Refusal('STATE_INPUT_RUN_ROOT_NOT_THIS_CALL_OUT')
        src = env.read_pin(obj['source_reconstruction'])
        if src.get('schema') != SOURCE_SCHEMA:
            raise Refusal('SOURCE_RECONSTRUCTION_SCHEMA')
        files = src.get('source_files') or []
        if not files:
            raise Refusal('OWN_RUN_SOURCE_ARCHIVES_UNAVAILABLE')
        for f in files:
            if not _is_pin(f) or not _within(env, f['path'], call['run_root']):
                raise Refusal('CROSS_RUN_SOURCE_SUBSTITUTION_FORBIDDEN (lo_producer v004 L67-69)')
            env.read_raw(f)
        row = env.read_pin(obj['row_reference'])
        ids = [r['id'] for r in details['row_contract']['rows']]
        if row.get('schema') != ROWS_SCHEMA or row.get('state_sha256') != state['state_sha256']:
            raise Refusal('ROW_REFERENCE_SCHEMA_OR_STATE')
        if not _same_pin(env, row.get('call_result'), call['result_pin']):
            raise Refusal('ROW_REFERENCE_NOT_OWN_CALL (another call\'s or no call\'s readouts; Q4a)')
        if row.get('speed_reference_policy') != SPEED_POLICY:
            raise Refusal('ROW_REFERENCE_SPEED_POLICY_NOT_Q4A')
        if row.get('row_ids') != ids:
            raise Refusal('ROW_REFERENCE_ROW_ORDER')
        row_files = row.get('state_files', [])                    # F6: lo_producer v004 L71-78, re-applied
        if not row_files:
            raise Refusal('OWN_RUN_READOUT_STATE_ARCHIVES_UNAVAILABLE (lo_producer v004 L72-74)')
        for f in row_files:
            if not _within(env, f['path'], call['run_root']):
                raise Refusal('CROSS_RUN_READOUT_SUBSTITUTION_FORBIDDEN (lo_producer v004 L75-77)')
            env.read_raw(f)
        if vmax is None:
            raise Refusal(vmax_error or 'OWN_CALL_READOUT_UNAVAILABLE')
        got = row.get('v_reference_km_s')
        if not isinstance(got, list) or len(got) != len(vmax) or any(bits(a, 'v_reference') != bits(b) for a, b in zip(got, vmax)):
            raise Refusal('ROW_SPEED_NOT_OWN_CALL_MAX (Q4a: v_reference_km_s must equal max |own readout| bitwise)')
        st['state_configuration_validation'] = env.validate_config(spec, obj)
        if 'err' in ctx_box:
            raise Refusal('POINT_CONTEXT_UNAVAILABLE: ' + ctx_box['err'])
        if ctx_box.get('ctx') is None:
            try:
                ctx_box['ctx'] = env.point_context(spec)
            except CAUGHT as exc:
                ctx_box['err'] = type(exc).__name__ + ': ' + str(exc)
                raise Refusal('POINT_CONTEXT_UNAVAILABLE: ' + ctx_box['err'])
        core = env.produce_current_lo(spec, ref, expected_state=state,
                                      trusted_source_producers=tuple(trusted_source_producers),
                                      trusted_review_hashes=tuple(trusted_reviews), settings='registered',
                                      shell_ranges=None, context=ctx_box['ctx'])
        st['core_record'] = env.write(core, out_root, _state_name(state, 'CORE'))
        if (core.get('schema') != CORE_SCHEMA or core.get('gate') != 'LO' or core.get('kind') != CORE_KIND
                or core.get('state') != state):
            raise Refusal('CORE_RECORD_SHAPE_OR_STATE_MISMATCH')
        if (core.get('identity') != details['identity'] or core.get('custody') != details['custody']
                or core.get('point_sha256') != details['point_sha256']):
            raise Refusal('CORE_RECORD_POINT_CUSTODY_MISMATCH')
        if (core.get('producer') or {}).get('sha256') != LO_CORE[1] or (core.get('response_producer') or {}).get('sha256') != RESPONSE_SHA:
            raise Refusal('CORE_PRODUCER_NOT_UNCHANGED_12D36305_A1DCDEA8')
        if core.get('v_reference_km_s') != [abs(x) for x in got]:
            raise Refusal('CORE_SPEEDS_DIFFER_FROM_VERIFIED_OWN_CALL_SPEEDS')
        proj = check_rho_record(core.get('rho'), read_raw=env.read_raw, identity=details['identity'],
                                custody=details['custody'],
                                point_sha256=details['point_sha256'])
        st['rho_projection_equal_to_slot_diagnostic_only'] = proj == call['slot_proj']     # V03: the c3v002 form, recorded only
        st['rho_bitwise_equal_to_slot'] = rho_bitwise_canonical(core.get('rho')) == call['slot_rho_bitwise']   # V03: L189-191
        if not st['rho_bitwise_equal_to_slot']:
            raise Refusal('RHO_RECOMPUTE_NOT_BITWISE_EQUAL_TO_SLOT (A134 Q5; preserved for root)')
        if (st['state_configuration_validation'] or {}).get('certificate_slots_bound') is not True:
            # F3: exactly lo_config L85-90. After the core runs, an unbound certificate slot adds
            # ACTUAL_POINT_CERTIFICATE_SLOTS_UNBOUND and the verdict BLOCKED, so the state reads UNAVAILABLE here.
            st['threshold_failed_observation'] = core.get('numerical_thresholds_pass') is False
            raise Refusal('ACTUAL_POINT_CERTIFICATE_SLOTS_UNBOUND (lo_config L88-90: certificate_slots_bound is not True)')
        blockers = core.get('blockers')
        if not isinstance(blockers, list):
            raise Refusal('CORE_BLOCKERS_MISSING')
        clean = core.get('all_nonzero_B1_consumed') is True
        st['core_verdict'], st['core_blockers'] = core.get('verdict'), list(blockers)
        if blockers == [] and core.get('verdict') == CORE_PASS_VERDICT and core.get('numerical_thresholds_pass') is True and clean:
            st['verdict'] = 'PASS'
        elif (blockers == [CORE_THRESHOLD_BLOCKER] and core.get('verdict') == 'BLOCKED'
              and core.get('numerical_thresholds_pass') is False and clean):
            st['verdict'] = 'FAIL'
        else:
            st['threshold_failed_observation'] = core.get('numerical_thresholds_pass') is False
            raise Refusal('CORE_NOT_CLEAN: ' + ','.join(str(b) for b in blockers))
        st['summed_max_over_tau'] = core.get('summed_max_over_tau')
        if st['verdict'] == 'PASS':
            proof = {'schema': PROOF_SCHEMA, 'gate': 'LO', 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'PASS',
                     'point_sha256': details['point_sha256'], 'custody_sha256': details['custody_sha256'],
                     'producer': me, 'state': state, 'shells': core['shells'],
                     'summed_max_over_tau': core['summed_max_over_tau'],
                     'row_contract_sha256': details['custody']['row_contract_sha256'], 'i1t_verdict': 'PASS',
                     'GQ_uniform_proof_sha256': call['gq_sha256'], 'core_record': st['core_record'],
                     'rho_slot': call['slot_rho_pin'], 'rho_bitwise_equal': True,
                     'speed_reference_policy': SPEED_POLICY, 'readout_set': READOUT_SET,
                     'state_class': cls, 'call_result': call['result_pin'], 'root_rulings': rulings,
                     'scope': ('Registered linear readout indicator (numerical rho x node-quadrature B1); not a '
                               'rigorous bound. Per-state post-run acceptance (A134 Q2/Q3/Q5).')}
            st['record'] = env.write(proof, out_root, _state_name(state, 'STATE_PROOF'))
            st['reading'] = R_PASS
            return st
    except (CAUGHT + _common_refusals()) as exc:              # F4
        st['verdict'] = 'UNAVAILABLE'
        st['blockers'].append(type(exc).__name__ + ': ' + str(exc))
    if st['verdict'] == 'FAIL':
        st['reading'] = {ACCEPTED: R_NLTM, INHERITED: R_NLTM, ROUTE_B: R_NLTM, ITERATE: R_TRANSIENT}.get(cls, R_CLASS_GAP)
    else:
        st['reading'] = 'UNAVAILABLE'
    rec = {'schema': STATE_READING_SCHEMA, 'utc': env.utc(), 'status': 'TESTED' if st['verdict'] == 'FAIL' else 'UNTESTED',
           'verdict': st['verdict'], 'reading': st['reading'], 'state': state, 'state_class': cls,
           'blockers': st['blockers'], 'core_record': st['core_record'], 'point_sha256': details['point_sha256'],
           'custody_sha256': details['custody_sha256'], 'producer': me, 'call_result': call['result_pin'],
           'summed_max_over_tau': st['summed_max_over_tau'], 'root_rulings': rulings,
           'threshold_failed_observation': st.get('threshold_failed_observation', False)}
    try:
        st['record'] = env.write(rec, out_root, _state_name(state, 'STATE_READING'))
    except (CAUGHT + _common_refusals()) as exc:              # F4
        st['blockers'].append('READING_RECORD_NOT_WRITTEN: ' + str(exc))
    return st


def call_reading(states, *, is_anchor, class_gap):
    """Q3/Q5 call-level LO reading from the per-state verdicts and classes (INTERFACE section 2, OPEN-5/6).

    B3 (c3v003): exactly FROM_CODEX/0690 OPEN-6, as root's acceptance_handoff_c2v002 L373-391 reads it. A FAIL at an
    accepted, inherited or route-B state is decisive (NON_LAPSE_TAIL_MATERIAL) even when other states are UNAVAILABLE.
    LO_UNCERTIFIED_TRANSIENT needs every non-iterate state at PASS, so an UNAVAILABLE iterate does not block it;
    otherwise the call reads INCOMPLETE, and each iterate failure stays recorded in its own TESTED state record."""
    fails = [s for s in states if s['verdict'] == 'FAIL']
    unav = [s for s in states if s['verdict'] == 'UNAVAILABLE']
    out = {'class_reading': None, 'step4_stop': False, 'class_gap': class_gap}
    if not fails:
        out['reading'] = R_PASS if not unav else R_INCOMPLETE
        return out
    classes = {s['state_class'] for s in fails}
    if classes & set(DECISIVE_CLASSES):
        cr = R_NLTM
    elif CLASS_UNAVAILABLE in classes:
        cr = R_CLASS_GAP
    elif classes == {ITERATE} and all(s['verdict'] == 'PASS' for s in states if s['state_class'] != ITERATE):
        cr = R_TRANSIENT                                  # B3: 0690 OPEN-6 (every non-iterate state at PASS)
    else:
        cr = R_INCOMPLETE
    out['class_reading'] = cr
    if is_anchor:
        out.update(reading=R_ANCHOR, step4_stop=True)
    else:
        out['reading'] = cr
    return out


def _adapt_call(spec, *, call_dir, result, inventory, bundle_ref, state_inputs, root_ruling_refs,
                approved_producer_sha256, trusted_source_producers, trusted_row_policy_review_sha256, out_root, env):
    rec = {'schema': CALL_SCHEMA, 'utc': env.utc(), 'status': 'TESTED', 'call_lo_reading': R_INCOMPLETE,
           'blockers': [], 'states': [], 'lo_rows_for_acceptance_bundle': [], 'summed_lo_for_RC2': None,
           'speed_reference_policy': SPEED_POLICY, 'readout_set': READOUT_SET}
    try:
        rec['root_rulings'] = root_gate(root_ruling_refs, env.read_raw)
        me = env.self_pin()
        approved = set(approved_producer_sha256) if isinstance(approved_producer_sha256, (list, tuple, set, frozenset)) else set()
        if me['sha256'] not in approved:
            raise Refusal('LO_STATE_ADAPTER_NOT_APPROVED (C1 approved_certificate_producers; review first)')
        rec['producer'] = me
        rec['blas_thread_env'] = {k: os.environ.get(k) for k in THREAD_ENV}
        reviews = list(trusted_row_policy_review_sha256) if isinstance(trusted_row_policy_review_sha256, (list, tuple)) else []
        if not reviews or not all(_is_sha(x) for x in reviews) or len(set(reviews)) != len(reviews):
            raise Refusal('ROW_POLICY_REVIEWS_REQUIRED (Q4: the three row-reference policy reviews, by sha)')
        if not isinstance(trusted_source_producers, (list, tuple)) or not all(_is_sha(x) for x in trusted_source_producers):
            raise Refusal('TRUSTED_SOURCE_PRODUCERS_INVALID')
        call = _call_context(spec, call_dir, result, inventory, bundle_ref, approved, env)
        details = call['details']
        rec.update(point_sha256=details['point_sha256'], custody_sha256=details['custody_sha256'],
                   call_result=call['result_pin'], inventory_digest=digest(inventory),
                   lo_slot=call['slot_rho_pin'], lo_slot_proof=call['slot_proof_pin'])
        ids = [r['id'] for r in details['row_contract']['rows']]
        vmax, verr = None, None
        try:
            vmax = own_call_vmax(result, ids)
        except Refusal as exc:
            verr = str(exc)
        rec['own_call_vmax_km_s'] = vmax
        classes, gap, accepted = state_classes(inventory)
        rec['accepted_state_sha256'] = accepted
        if gap:
            rec['blockers'].append(gap)
        ctx_box = {}
        for state in call['states']:
            info = classes.get(digest(state), (CLASS_UNAVAILABLE, [], []))
            rec['states'].append(_one_state(
                spec, state, info, call, vmax, verr, state_inputs=state_inputs,
                trusted_source_producers=trusted_source_producers, trusted_reviews=reviews, ctx_box=ctx_box,
                out_root=out_root, me=me, rulings=rec['root_rulings'], env=env))
        cr = call_reading(rec['states'], is_anchor=details['point_sha256'] == ANCHOR_KEY, class_gap=gap)
        rec['call_lo_reading'] = cr['reading']
        rec['class_reading'] = cr['class_reading']
        rec['step4_stop'] = cr['step4_stop']
        rec['lo_rows_for_acceptance_bundle'] = [{'state': s['state'], 'LO': s['record']} for s in rec['states']
                                                if s['verdict'] == 'PASS']
        sums = [s['summed_max_over_tau'] for s in rec['states'] if s['summed_max_over_tau'] is not None]
        rec['summed_lo_for_RC2'] = {'per_state': [{'state': s['state'], 'summed_max_over_tau': s['summed_max_over_tau']}
                                                  for s in rec['states']],
                                    'max_over_states': max(sums) if sums and len(sums) == len(rec['states']) else None,
                                    'complete': bool(sums) and len(sums) == len(rec['states'])}
        rec['lo_gate_passed_all_states'] = cr['reading'] == R_PASS
    except (CAUGHT + _common_refusals()) as exc:              # F4
        rec['blockers'].append(type(exc).__name__ + ': ' + str(exc))
        rec['call_lo_reading'] = R_INCOMPLETE
        rec['lo_gate_passed_all_states'] = False
    return rec


def adapt_call_lo(spec, *, call_dir, result, inventory, bundle_ref, state_inputs, root_ruling_refs=None,
                  approved_producer_sha256=(), trusted_source_producers=(), trusted_row_policy_review_sha256=(),
                  out_root):
    """Public entry (root operates it at post-run acceptance). INCOMPLETE unless every gate above holds."""
    return _adapt_call(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
                       state_inputs=state_inputs, root_ruling_refs=root_ruling_refs,
                       approved_producer_sha256=approved_producer_sha256,
                       trusted_source_producers=trusted_source_producers,
                       trusted_row_policy_review_sha256=trusted_row_policy_review_sha256, out_root=out_root,
                       env=_real_env())


def write_call_record(rec, out_root):
    return common().write_new(os.path.join(out_root, 'LO_CALL_ACCEPTANCE_%s.json' % common().utc_compact()), rec, out_root)


def _background_qos():
    try:
        return os.getpriority(4, 0) == 1
    except Exception:
        return False


def main(argv=None):
    """CLI: refusals first (taskpolicy -b; python3 -I -B), then one pinned JSON argument file."""
    if not _background_qos():
        print('REFUSED: BACKGROUND_QOS_REQUIRED (run under taskpolicy -b)', flush=True)
        return 2
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B)', flush=True)
        return 2
    import argparse
    ap = argparse.ArgumentParser(description='Per-state LO proof adapter (A134 Q2-Q5)')
    ap.add_argument('--args', required=True, help='JSON: spec_ref, call_dir, inventory_ref, bundle_ref, state_inputs, '
                    'root_ruling_refs, approved_producer_sha256, trusted_source_producers, '
                    'trusted_row_policy_review_sha256')
    ap.add_argument('--args-sha256', required=True)
    ap.add_argument('--out-root', required=True)
    a = ap.parse_args(argv)
    try:
        root_gate(ROOT_RULINGS, _gate_reader)          # F9: the root-ruling gate runs before any pin is read
    except (CAUGHT + _common_refusals()) as exc:
        print(json.dumps({'call_lo_reading': R_INCOMPLETE, 'blockers': [type(exc).__name__ + ': ' + str(exc)],
                          'record': None}), flush=True)
        return 3
    try:                                               # F4: a refusal is a structured result, never a crash
        C = common()
        args = C.read_json_pinned({'path': a.args, 'sha256': a.args_sha256}, (ART,), 'args')
        env = _real_env()
        spec = env.read_pin(args['spec_ref'])
        result = json.loads(env.read_bytes(os.path.join(args['call_dir'], 'out', 'result.json')))
        inventory = env.read_pin(args['inventory_ref'])
        rec = _adapt_call(spec, call_dir=args['call_dir'], result=result, inventory=inventory,
                          bundle_ref=args['bundle_ref'], state_inputs=args.get('state_inputs') or {},
                          root_ruling_refs=args.get('root_ruling_refs'),
                          approved_producer_sha256=args.get('approved_producer_sha256', ()),
                          trusted_source_producers=args.get('trusted_source_producers', ()),
                          trusted_row_policy_review_sha256=args.get('trusted_row_policy_review_sha256', ()),
                          out_root=a.out_root, env=env)
        pin = write_call_record(rec, a.out_root)
    except (CAUGHT + _common_refusals()) as exc:
        print(json.dumps({'call_lo_reading': R_INCOMPLETE, 'blockers': [type(exc).__name__ + ': ' + str(exc)],
                          'record': None}), flush=True)
        return 3
    print(json.dumps({'call_lo_reading': rec['call_lo_reading'], 'blockers': rec['blockers'], 'record': pin}), flush=True)
    return 0 if rec['call_lo_reading'] == R_PASS else 3


if __name__ == '__main__':
    for _k in THREAD_ENV:          # before numpy is imported (all numpy imports are lazy)
        os.environ[_k] = '1'
    sys.exit(main())
