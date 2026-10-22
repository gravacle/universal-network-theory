"""S4-R-C1 SRB-ROT adapter c3v003 (A134 Q10). Claude3 builds it; Codex1 reviews it in one pass (FROM_CODEX/0688).

c3v003 is the erratum-class successor of srb_rot_adapter_c3v002 (d69e5449; root ruling A138, FROM_CODEX/0703). It changes
only:
- V02: the inventory enumerator pin is the b1 enumerator consumed_states_b1_c2v001 (4ca7f364; the C1 state_enumerator)
  in place of consumed_states_cx2v010 (e48cca3c). A v010 inventory is refused.
No threshold, scope or normalization changes. The record formats are unchanged.

c3v002 is the erratum-class successor of srb_rot_adapter_c3v001 (e74c6f5e; A134 Q2 rule; FROM_CODEX/0696). It changes only:
- F4: the s4rc1_common Refusal and every writer refusal are caught in _adapt and in main(): a structured
  UNAVAILABLE result, never a crash;
- F8: monitor_status M_T_NOT_NORMALIZED with flags [] reads UNFLAGGED, exactly as r14 raw_flag L4587-4590 does
  (the flag is TAIL_SOURCE_UNDERCONVERGED in flags). The FLAGGED <-> TAIL_SOURCE_UNDERCONVERGED check is kept, and
  any other status stays UNAVAILABLE;
- F9: main() runs the root-ruling gate before it reads any pin.
No threshold, scope or normalization changes. The record formats are unchanged.

It runs on the call's accepted final-rotation state ONLY: the own_source_state of stage le{final_pass}_rotation,
stage_kind le_rotation.
- It is a thin format adapter. It feeds the pinned library owned_uv_tail_lapse_v002 (2026f2b6): field_bound
  L847 and srb_rot L860-871.
- Inputs: the call's own rows and the point's cx2 EPS record over [4,182]. The input field is 'eps', the larger
  recorded value (guard v003 L139); eps_envelope is never fed.
- The pass rule is V007's frozen <= tau_i/10, read from the library's pass_tau_over_10. No threshold is declared
  here, and no bare EPS magnitude gate exists.
- AMB-04 is r14's own apply_flag (L4099-4109, used at L4617), extracted from the pinned f3f9ba7e bytes by AST and
  executed alone:
  - on a call flagged TAIL_SOURCE_UNDERCONVERGED, a pass reads PASS_FLAGGED and a fail UNDECIDABLE_FLAGGED;
  - an unflagged fail reads BOUND_INSUFFICIENT, is preserved, and its rows are not model output.
- The C4T-locked V007 producer is not used. The optional RB-FP(p) screen is not computed in v001; it is never a gate.

Root gate: A134 text of record 56774ba7 and FROM_CODEX/0688 bcb6df8e, pinned and re-read from bytes. The
module's own sha must be in root's C1 list. Producer pins come from a canonical __file__ (R4). Writes are
exclusive create. The builder ran it on synthetic TailStates and records only.
"""
import ast
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

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
COMMON = (ART + '/s4rc1_c3/build_c3v002/s4rc1_common_c3v002.py',
          'fa48b1a16d26ff14445f6823bd7c15554e50bd0f75b882e0564c4e40980055ce')
CUSTODY = (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377')
LIBRARY = (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
           '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')
R14 = (ART + '/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py',
       'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7')
APPLY_FLAG_LINES = (4099, 4109)
APPLY_FLAG_SOURCE_SHA256 = '9bbb3835d25a745d7665b96c3faf564d8227e8039f9bd6ef409ac10d4a1ff926'
ENUMERATOR_SHA = '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'   # V02: b1 enumerator consumed_states_b1_c2v001
ROOT_RULINGS = (
    {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
             'CLAUDE2/S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md',
     'sha256': '56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82'},
    {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0688_2026-10-19_A134_S4RC1_LO_route_ruled_owners.md',
     'sha256': 'bcb6df8e9cbd7d01c7c10e4673fb6ca60ecf6c4a439be4db6140ed521689b30d'},
)
RESULT_SCHEMA = 'S4RC1_SRB_ROT_RESULT_C3V001'
PROOF_SCHEMA = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'
GATE = 'SRB_ROT'
INVENTORY_SCHEMA = 'DDO154_CONSUMED_STATE_JOIN_CX2V010'
STATE_INPUT_SCHEMA = 'UNT_POINT_LO_STATE_INPUT_CX2V001'
ROWS_INPUT_SCHEMA = 'S4RC1_SRB_ROT_ROWS_INPUT_C3V001'
EPS_SCHEMA = 'UNT_POINT_EPS_NUMERICAL_CX2V001'                 # response producer a1dcdea8 L29
EPS_COVERAGE = (4.0, 182.0)                                   # [K, ceil(sqrt(2) * 128)]
FINAL_ROTATION_KIND = 'le_rotation'                           # discovery v005 KINDS['rotation_v005']
FLAG_TSU = 'TAIL_SOURCE_UNDERCONVERGED'                       # r14 L412; route-A controller L537
MONITOR_STATUSES = ('FLAGGED', 'M_T_WITHIN_THRESHOLD', 'M_T_NOT_NORMALIZED')   # route-A controller c2v001 result_record
MT_NOT_NORMALIZED = 'M_T_NOT_NORMALIZED'     # F8: controller c2v001 L534-535 (flags []); r14 raw_flag L4587-4590 unflagged
READING = {'PASS': 'PASS', 'PASS_FLAGGED': 'PASS_FLAGGED', 'UNDECIDABLE_FLAGGED': 'UNDECIDABLE_FLAGGED',
           'FAIL': 'BOUND_INSUFFICIENT'}
RB_FP_SCREEN = 'NOT_COMPUTED_IN_C3V001 (optional; never a gate; UNTESTED off the anchor; A134 Q10)'
STATE_KEYS = {'state_sha256', 'source_sha256', 'stage_kind', 'nonnegative_masses'}
THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')   # single-thread BLAS: rho bitwise reproducibility
CAUGHT = (ValueError, KeyError, TypeError, OSError, OverflowError, AttributeError, IndexError,
          ZeroDivisionError, FloatingPointError, SyntaxError)


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
        _COMMON['C'] = _load_exact(COMMON[0], COMMON[1], 's4rc1_proofside_common_c3v002_srb')
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


def _bits(x, name):
    return struct.pack('<d', _float(x, name)).hex()


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


def extract_apply_flag(raw):
    """r14's own apply_flag: from the exact pinned bytes, AST-isolated, executed with only `sorted` available."""
    if hashlib.sha256(raw).hexdigest() != R14[1]:
        raise Refusal('R14_BYTES_NOT_F3F9BA7E')
    src = raw.decode('utf-8')
    tree = ast.parse(src)
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'apply_flag']
    if len(fns) != 1 or (fns[0].lineno, fns[0].end_lineno) != APPLY_FLAG_LINES:
        raise Refusal('R14_APPLY_FLAG_NOT_AT_L4099_L4109')
    seg = ast.get_source_segment(src, fns[0])
    if hashlib.sha256(seg.encode('utf-8')).hexdigest() != APPLY_FLAG_SOURCE_SHA256:
        raise Refusal('R14_APPLY_FLAG_SOURCE_CHANGED')
    ns = {'__builtins__': {'sorted': sorted}}
    exec(compile(ast.Module(body=[fns[0]], type_ignores=[]), R14[0], 'exec'), ns)
    return ns['apply_flag']


# ----------------------------------------------------------------------------------------------- inputs
def check_inventory(inventory, details):
    if not isinstance(inventory, dict) or inventory.get('schema') != INVENTORY_SCHEMA or inventory.get('complete') is not True:
        raise Refusal('COMPLETE_V010_INVENTORY_REQUIRED')
    prod = inventory.get('producer')
    if not _is_pin(prod) or prod['sha256'] != ENUMERATOR_SHA:
        raise Refusal('INVENTORY_PRODUCER_NOT_B1_4CA7F364')         # V02
    if inventory.get('point_sha256') != details['point_sha256'] or inventory.get('custody_sha256') != details['custody_sha256']:
        raise Refusal('INVENTORY_POINT_OR_CUSTODY_MISMATCH')
    states = inventory.get('states')
    if not isinstance(states, list) or not states or any(not isinstance(s, dict) or set(s) != STATE_KEYS for s in states):
        raise Refusal('INVENTORY_STATE_IDENTITY_INVALID')
    return states


def final_rotation_state(inventory, result):
    """The accepted final-rotation state: own_source_state at stage le{final_pass}_rotation (INTERFACE OPEN-3)."""
    n, passes = result.get('final_pass'), result.get('passes')
    if type(n) is not int or n < 1 or not isinstance(passes, list) or len(passes) != n:
        raise Refusal('FINAL_PASS_UNAVAILABLE')
    stage = 'le%d_rotation' % n
    occ = inventory.get('occurrences') or []
    hits = [o for o in occ if isinstance(o, dict) and o.get('role') == 'own_source_state'
            and o.get('stage') == stage and o.get('stage_kind') == FINAL_ROTATION_KIND]
    if len(hits) != 1:
        raise Refusal('FINAL_ROTATION_STATE_NOT_UNIQUE_IN_INVENTORY: ' + stage)
    js = [j for j in inventory.get('joined_occurrences') or [] if isinstance(j, dict) and j.get('ordinal') == hits[0].get('ordinal')]
    if len(js) != 1 or not isinstance(js[0].get('state'), dict):
        raise Refusal('FINAL_ROTATION_STATE_NOT_JOINED')
    st = js[0]['state']
    if st not in inventory['states'] or st.get('stage_kind') != FINAL_ROTATION_KIND or st.get('state_sha256') != hits[0].get('state_sha256_claimed'):
        raise Refusal('FINAL_ROTATION_STATE_INCONSISTENT')
    return st, stage


def call_flag(result):
    """The call's own TAIL_SOURCE_UNDERCONVERGED flag (result.uv_tail.route_a_record; OPEN-12).

    F8 (c3v002): as r14 raw_flag L4587-4590, the flag is TAIL_SOURCE_UNDERCONVERGED in flags. monitor_status
    M_T_NOT_NORMALIZED (controller c2v001 L534-535) is read unflagged with flags [] only. FLAGGED <-> the flag is
    checked as before, and any other status is UNAVAILABLE."""
    ra = ((result.get('uv_tail') or {}) if isinstance(result, dict) else {}).get('route_a_record')
    if not isinstance(ra, dict):
        raise Refusal('ROUTE_A_FLAG_RECORD_MISSING')
    flags, ms = ra.get('flags'), ra.get('monitor_status')
    if not isinstance(flags, list) or not all(isinstance(f, str) for f in flags):
        raise Refusal('ROUTE_A_FLAGS_INVALID')
    flagged = FLAG_TSU in flags
    if ms not in MONITOR_STATUSES or (ms == 'FLAGGED') != flagged:
        raise Refusal('ROUTE_A_FLAG_RECORD_INCONSISTENT (flags %r, monitor_status %r)' % (flags, ms))
    if ms == MT_NOT_NORMALIZED and flags != []:                    # F8
        raise Refusal('ROUTE_A_FLAG_RECORD_INCONSISTENT (M_T_NOT_NORMALIZED is read unflagged only with flags []; '
                      'flags %r)' % (flags,))
    return flagged


def format_eps(eps_rec, details):
    """Thin format adapter: the point's cx2 EPS record -> library eps_certificate over exactly [4,182], field 'eps'."""
    if not isinstance(eps_rec, dict) or eps_rec.get('schema') != EPS_SCHEMA or eps_rec.get('gate') != 'EPS':
        raise Refusal('EPS_RECORD_SCHEMA')
    if eps_rec.get('identity') != details['identity'] or eps_rec.get('custody') != details['custody'] \
            or eps_rec.get('point_sha256') != details['point_sha256']:
        raise Refusal('EPS_RECORD_POINT_CUSTODY_MISMATCH')
    if eps_rec.get('status') != 'TESTED' or eps_rec.get('settings') != 'registered' \
            or eps_rec.get('full_registered_search_executed') is not True or eps_rec.get('coverage_complete') is not True:
        raise Refusal('EPS_RECORD_NOT_REGISTERED_FULL')
    if eps_rec.get('required_coverage_inverse_kpc') != list(EPS_COVERAGE):
        raise Refusal('EPS_COVERAGE_NOT_4_TO_182')
    shells = eps_rec.get('shells')
    if not isinstance(shells, list) or not shells:
        raise Refusal('EPS_SHELLS_MISSING')
    cursor, out = EPS_COVERAGE[0], []
    for s in shells:
        lo, hi = _float(s.get('lo_inverse_kpc'), 'lo'), _float(s.get('hi_inverse_kpc'), 'hi')
        if s.get('range_inverse_kpc') != [lo, hi] or lo != cursor or hi != lo + 1:
            raise Refusal('EPS_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS_FROM_4')
        eps, env = _float(s.get('eps'), 'eps'), _float(s.get('eps_envelope'), 'eps_envelope')
        if eps < 0 or env < 0 or eps < env:
            raise Refusal('EPS_FIELD_NOT_THE_LARGER_VALUE (guard v003 L139: eps >= eps_envelope)')
        out.append({'lo_inverse_kpc': lo, 'hi_inverse_kpc': hi, 'eps': eps})
        cursor = hi
    if cursor != EPS_COVERAGE[1]:
        raise Refusal('EPS_COVERAGE_NOT_4_TO_182')
    return {'shells': out}


def same_pin(resolve, a, b):
    """Same bytes and the same resolved file (consumed_states_cx2v010 same_ref precedent)."""
    if not (_is_pin(a) and _is_pin(b)) or a['sha256'] != b['sha256']:
        return False
    try:
        return str(resolve(a['path'])) == str(resolve(b['path']))
    except CAUGHT:
        return False


def format_rows(rin, details, state, result_pin, trusted_source_producers, resolve=None):
    """The call's own rows -> library srb_rot rows; tau comes from the row contract (prereg V005, 0.25 sigma)."""
    if not isinstance(rin, dict) or rin.get('schema') != ROWS_INPUT_SCHEMA:
        raise Refusal('SRB_ROWS_INPUT_SCHEMA')
    if rin.get('state') != state:
        raise Refusal('SRB_ROWS_INPUT_NOT_THE_FINAL_ROTATION_STATE')
    same = (rin.get('call_result') == result_pin) if resolve is None else same_pin(resolve, rin.get('call_result'), result_pin)
    if not same:
        raise Refusal('SRB_ROWS_INPUT_NOT_THIS_CALL (the call\'s own rows only)')
    prod = rin.get('producer')
    if not _is_pin(prod) or prod['sha256'] not in set(trusted_source_producers):
        raise Refusal('SRB_ROWS_INPUT_PRODUCER_NOT_TRUSTED')
    contract = details['row_contract']
    ids = [r['id'] for r in contract['rows']]
    tau = list(contract['tau_km_s'])
    if rin.get('row_ids') != ids or rin.get('row_contract_sha256') != details['custody']['row_contract_sha256']:
        raise Refusal('SRB_ROWS_INPUT_ROW_CONTRACT_MISMATCH')
    got_tau = rin.get('tau_km_s')
    if not isinstance(got_tau, list) or len(got_tau) != len(tau) or any(_bits(a, 'tau') != _bits(b, 'tau') for a, b in zip(got_tau, tau)):
        raise Refusal('SRB_ROWS_INPUT_TAU_NOT_ROW_CONTRACT_TAU')
    R, v = rin.get('column_R_m'), rin.get('v_c_m_s')
    if not isinstance(R, list) or not isinstance(v, list) or not R or len(R) != len(v):
        raise Refusal('SRB_ROWS_INPUT_COLUMN_SHAPE')
    R = [_float(x, 'column_R_m') for x in R]
    v = [_float(x, 'v_c_m_s') for x in v]
    if any(x <= 0 for x in R) or any(x <= 0 for x in v):
        raise Refusal('SRB_ROWS_INPUT_COLUMN_VALUES_NOT_POSITIVE')
    rc = rin.get('row_columns')
    if not isinstance(rc, list) or len(rc) != len(ids):
        raise Refusal('SRB_ROWS_INPUT_ROW_COLUMNS_SHAPE')
    for ix in rc:
        if not isinstance(ix, list) or not ix or len(set(ix)) != len(ix) or any(
                isinstance(i, bool) or type(i) is not int or not 0 <= i < len(R) for i in ix):
            raise Refusal('SRB_ROWS_INPUT_ROW_COLUMNS_INVALID')
    n_min = _float(rin.get('N_min'), 'N_min')
    if n_min <= 0:
        raise Refusal('SRB_ROWS_INPUT_N_MIN_NOT_POSITIVE')
    return {'column_R_m': R, 'v_c_m_s': v, 'row_columns': [list(ix) for ix in rc], 'N_min': n_min,
            'tau_km_s': [float(x) for x in tau]}


# ----------------------------------------------------------------------------------------------- env
def _real_env():
    state = {}

    def cu():
        if 'cu' not in state:
            state['cu'] = _load_exact(CUSTODY[0], CUSTODY[1], 's4rc1_proofside_srb_custody_cx2v002')
        return state['cu']

    def lib():
        if 'lib' not in state:
            state['lib'] = _load_exact(LIBRARY[0], LIBRARY[1], 's4rc1_proofside_uvt_lapse_v002')
        return state['lib']

    def load_arrays(pin):
        raw = cu().read_pin(pin, document=False)
        import numpy as np
        with np.load(io.BytesIO(raw), allow_pickle=False) as z:
            return {k: z[k] for k in z.files}

    return types.SimpleNamespace(
        derive_details=lambda spec: cu().derive_details(spec=spec),
        read_pin=lambda ref: cu().read_pin(ref),
        read_raw=lambda ref: cu().read_pin(ref, document=False),
        read_bytes=lambda path: cu().allowed_path(path).read_bytes(),
        resolve=lambda path: cu().allowed_path(path),
        lib=lib, load_arrays=load_arrays,
        apply_flag=lambda: extract_apply_flag(cu().read_pin({'path': R14[0], 'sha256': R14[1]}, document=False)),
        write=lambda obj, out_root, name: common().write_new(os.path.join(out_root, name), obj, out_root),
        self_pin=_self_pin, utc=_utc)


def _adapt(spec, *, call_dir, result, inventory, bundle_ref, state_input_ref, rows_input_ref, root_ruling_refs,
           approved_producer_sha256, trusted_source_producers, env):
    out = {'schema': RESULT_SCHEMA, 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'UNAVAILABLE',
           'amb04_status': None, 'reading': 'UNAVAILABLE', 'blockers': [], 'proof': None, 'rb_fp_screen': RB_FP_SCREEN}
    try:
        out['root_rulings'] = root_gate(root_ruling_refs, env.read_raw)
        me = env.self_pin()
        approved = set(approved_producer_sha256) if isinstance(approved_producer_sha256, (list, tuple, set, frozenset)) else set()
        if me['sha256'] not in approved:
            raise Refusal('SRB_ROT_ADAPTER_NOT_APPROVED (C1 approved_certificate_producers; review first)')
        out['producer'] = me
        out['blas_thread_env'] = {k: os.environ.get(k) for k in THREAD_ENV}
        if not isinstance(trusted_source_producers, (list, tuple)) or not all(_is_sha(x) for x in trusted_source_producers):
            raise Refusal('TRUSTED_SOURCE_PRODUCERS_INVALID')
        rp = os.path.join(str(call_dir), 'out', 'result.json')
        raw = env.read_bytes(rp)
        if json.loads(raw) != result:
            raise Refusal('CALL_RESULT_BYTES_DIFFER_FROM_SUPPLIED_RESULT')
        result_pin = {'path': rp, 'sha256': hashlib.sha256(raw).hexdigest()}
        out['call_result'] = result_pin
        details = env.derive_details(spec)
        out.update(point_sha256=details['point_sha256'], custody_sha256=details['custody_sha256'])
        check_inventory(inventory, details)
        state, stage = final_rotation_state(inventory, result)
        out.update(state=state, stage=stage)
        sin = env.read_pin(state_input_ref)
        if sin.get('schema') != STATE_INPUT_SCHEMA:
            raise Refusal('STATE_INPUT_SCHEMA')
        if sin.get('state') != state:
            raise Refusal('SRB_ROT_FINAL_ROTATION_STATE_ONLY (the supplied state is not the accepted final-rotation state)')
        if sin.get('identity') != details['identity'] or sin.get('custody') != details['custody'] \
                or not same_pin(env.resolve, sin.get('call_result'), result_pin):
            raise Refusal('STATE_INPUT_POINT_CUSTODY_OR_CALL_MISMATCH')
        uv = (spec.get('numerics') or {}).get('uv_tail') or {}
        eps_pin, lo_pin = uv.get('eps_certificate'), uv.get('lo_certificate')
        if not _is_pin(eps_pin):
            raise Refusal('EPS_SLOT_NOT_A_PIN')
        bundle = env.read_pin(bundle_ref)
        if bundle.get('identity') != details['identity'] or bundle.get('custody') != details['custody']:
            raise Refusal('BUNDLE_POINT_OR_CUSTODY_MISMATCH')
        if (bundle.get('driver_certificate_bindings') or {}).get('eps_certificate') != eps_pin:
            raise Refusal('EPS_SLOT_NOT_BOUND_BY_REGISTERED_BUNDLE')
        ep = env.read_pin((bundle.get('prelaunch') or {}).get('EPS'))
        if (ep.get('schema') != PROOF_SCHEMA or ep.get('gate') != 'EPS' or ep.get('status') != 'TESTED'
                or ep.get('verdict') != 'PASS' or ep.get('driver_certificate') != eps_pin
                or ep.get('point_sha256') != details['point_sha256'] or ep.get('custody_sha256') != details['custody_sha256']):
            raise Refusal('EPS_PROOF_NOT_TESTED_PASS_FOR_THIS_SLOT')
        if not _is_pin(ep.get('producer')) or ep['producer']['sha256'] not in approved:
            raise Refusal('EPS_PROOF_PRODUCER_NOT_APPROVED')
        eps_cert = format_eps(env.read_pin(eps_pin), details)
        U = env.lib()
        record = env.read_pin(sin['tail_state']['record'])
        arrays = env.load_arrays(sin['tail_state']['arrays'])
        st = U.TailState.from_arrays(arrays, record, expected_digest=state['state_sha256'])
        if record.get('stage_kind') != FINAL_ROTATION_KIND or record.get('roster_digest') != state['source_sha256']:
            raise Refusal('TAIL_STATE_STAGE_OR_SOURCE_MISMATCH')
        if record.get('eps_certificate') != eps_pin or record.get('lo_certificate') != lo_pin:
            raise Refusal('TAIL_STATE_DID_NOT_RUN_WITH_THESE_CERTIFICATE_SLOTS')
        rows = format_rows(env.read_pin(rows_input_ref), details, state, result_pin, trusted_source_producers,
                           resolve=env.resolve)
        flagged = call_flag(result)
        fb = U.field_bound(st, eps_cert)
        sr = U.srb_rot(st, eps_cert, rows)
        if not isinstance(sr.get('pass_tau_over_10'), bool):
            raise Refusal('LIBRARY_PASS_FLAG_MISSING')
        base = 'PASS' if sr['pass_tau_over_10'] else 'FAIL'
        amb = env.apply_flag()({'status': base}, ['CALL'] if flagged else [])
        status = amb['status']
        if status not in READING:
            raise Refusal('AMB04_STATUS_UNEXPECTED: ' + str(status))
        out.update(verdict='PASS' if status in ('PASS', 'PASS_FLAGGED') else ('FAIL' if status == 'FAIL' else status),
                   amb04_status=status, raw_status=amb['raw_status'], flagged=flagged, flagged_runs=amb['flagged_runs'],
                   reading=READING[status], bound_km_s=sr['bound_km_s'], ratio_to_tau=sr['ratio_to_tau'],
                   pass_tau_over_10=sr['pass_tau_over_10'], field_bound_total=fb.get('total'),
                   field_bound_eps_per_shell=fb.get('eps'), state_empty=bool(st.empty), eps_record=dict(eps_pin),
                   rows_input=dict(rows_input_ref), state_input=dict(state_input_ref),
                   library={'path': LIBRARY[0], 'sha256': LIBRARY[1]},
                   apply_flag_source={'path': R14[0], 'sha256': R14[1], 'lines': list(APPLY_FLAG_LINES),
                                      'segment_sha256': APPLY_FLAG_SOURCE_SHA256},
                   rows_are_model_output_per_srb_rot=status in ('PASS', 'PASS_FLAGGED'),
                   scope='SRB-ROT: static rotation-law channel only; necessary, not sufficient (A134 Q10).')
        if status in ('PASS', 'PASS_FLAGGED'):
            out['proof'] = {'schema': PROOF_SCHEMA, 'gate': GATE, 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'PASS',
                            'amb04_status': status, 'flagged': flagged, 'point_sha256': details['point_sha256'],
                            'custody_sha256': details['custody_sha256'], 'producer': me, 'state': state,
                            'stage': stage, 'eps_record': dict(eps_pin), 'rows_input': dict(rows_input_ref),
                            'bound_km_s': sr['bound_km_s'], 'ratio_to_tau': sr['ratio_to_tau'],
                            'pass_tau_over_10': True, 'call_result': result_pin, 'root_rulings': out['root_rulings'],
                            'library': out['library'], 'apply_flag_source': out['apply_flag_source'],
                            'rb_fp_screen': RB_FP_SCREEN,
                            'scope': 'necessary, not sufficient; RB-FP off the anchor UNTESTED (A134 Q10)'}
    except (CAUGHT + _common_refusals()) as exc:              # F4
        out['blockers'].append(type(exc).__name__ + ': ' + str(exc))
        out.update(verdict='UNAVAILABLE', reading='UNAVAILABLE', proof=None)
    return out


def adapt_call_srb_rot(spec, *, call_dir, result, inventory, bundle_ref, state_input_ref, rows_input_ref,
                       root_ruling_refs=None, approved_producer_sha256=(), trusted_source_producers=()):
    """Public entry (root operates it at post-run acceptance)."""
    return _adapt(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
                  state_input_ref=state_input_ref, rows_input_ref=rows_input_ref, root_ruling_refs=root_ruling_refs,
                  approved_producer_sha256=approved_producer_sha256,
                  trusted_source_producers=trusted_source_producers, env=_real_env())


def write_outputs(out, out_root, env=None):
    """Exclusive-create the result record and, for PASS/PASS_FLAGGED, the SRB_ROT proof. Returns their pins."""
    w = (env.write if env is not None else (lambda o, r, n: common().write_new(os.path.join(r, n), o, r)))
    tag = (out.get('state') or {}).get('state_sha256', 'nostate')[:16]
    pins = {'proof': None}
    if out.get('proof') is not None:
        p = out['proof']
        if p.get('schema') != PROOF_SCHEMA or p.get('gate') != GATE or p.get('verdict') != 'PASS' or \
                out.get('amb04_status') not in ('PASS', 'PASS_FLAGGED'):
            raise Refusal('SRB_ROT_PROOF_SHAPE_INVALID')
        pins['proof'] = w(p, out_root, 'SRB_ROT_PROOF_%s.json' % tag)
    pins['result'] = w(out, out_root, 'SRB_ROT_RESULT_%s.json' % tag)
    return pins


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
    ap = argparse.ArgumentParser(description='SRB-ROT adapter (A134 Q10)')
    ap.add_argument('--args', required=True, help='JSON: spec_ref, call_dir, inventory_ref, bundle_ref, state_input_ref, '
                    'rows_input_ref, root_ruling_refs, approved_producer_sha256, trusted_source_producers')
    ap.add_argument('--args-sha256', required=True)
    ap.add_argument('--out-root', required=True)
    a = ap.parse_args(argv)
    try:
        root_gate(ROOT_RULINGS, _gate_reader)          # F9: the root-ruling gate runs before any pin is read
    except (CAUGHT + _common_refusals()) as exc:
        print(json.dumps({'verdict': 'UNAVAILABLE', 'reading': 'UNAVAILABLE',
                          'blockers': [type(exc).__name__ + ': ' + str(exc)], 'pins': None}), flush=True)
        return 3
    try:                                               # F4: a refusal is a structured result, never a crash
        C = common()
        args = C.read_json_pinned({'path': a.args, 'sha256': a.args_sha256}, (ART,), 'args')
        env = _real_env()
        spec = env.read_pin(args['spec_ref'])
        result = json.loads(env.read_bytes(os.path.join(args['call_dir'], 'out', 'result.json')))
        out = _adapt(spec, call_dir=args['call_dir'], result=result, inventory=env.read_pin(args['inventory_ref']),
                     bundle_ref=args['bundle_ref'], state_input_ref=args['state_input_ref'],
                     rows_input_ref=args['rows_input_ref'], root_ruling_refs=args.get('root_ruling_refs'),
                     approved_producer_sha256=args.get('approved_producer_sha256', ()),
                     trusted_source_producers=args.get('trusted_source_producers', ()), env=env)
        pins = write_outputs(out, a.out_root, env)
    except (CAUGHT + _common_refusals()) as exc:
        print(json.dumps({'verdict': 'UNAVAILABLE', 'reading': 'UNAVAILABLE',
                          'blockers': [type(exc).__name__ + ': ' + str(exc)], 'pins': None}), flush=True)
        return 3
    print(json.dumps({'verdict': out['verdict'], 'reading': out['reading'], 'blockers': out['blockers'], 'pins': pins}), flush=True)
    return 0 if out['verdict'] == 'PASS' else 3


if __name__ == '__main__':
    for _k in THREAD_ENV:          # before numpy is imported (all numpy imports are lazy)
        os.environ[_k] = '1'
    sys.exit(main())
