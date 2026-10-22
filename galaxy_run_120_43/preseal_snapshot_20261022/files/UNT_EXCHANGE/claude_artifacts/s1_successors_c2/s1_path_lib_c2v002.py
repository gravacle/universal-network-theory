"""S1 transfer test at u_A (S4-POST-S1): template filler, guarded root launch path and reader.

Claude2 root workflow s1_successors_c2, c2v002 (successor of s1_path_c2 c2v001 b461ac36; A150 R-S1-3 (3)). Built for
root; nothing here is in force until root rules and a distinct lane reviews. Importing this module does nothing: no
file is read, no process starts. Every input is read from a pin (absolute path + sha256 from bytes). The registration
it implements is S1_REGISTRATION_DRAFT_C2V002.md (67b4bd78), in force by V6 A150.

c2v002 applies the c2v001 verifier's B1-B3 and notes 1, 2, 4-13 (see README_S1_SUCCESSORS_C2V001.md) and pins the
successors guard012 / launcher013 (overlap admission) and the S1-only kept-K-3 wrapper successor (control 3 for
S1_UA_C3T).

Three parts, each called by its own CLI wrapper (which loads this file by its sha256):
  fill / dry-plan / plan   the S1 template: the two S1 call specs from the u_A theta bits and the campaign's own
                           u_A call spec (the registered call spec, CHOICE C4), then one POST_S1 plan per call.
  launch                   the root launch path: the S1 checks, then the four 0620 controls through step-4 guard012
                           (adoption / spec_structure / validate, which runs native preflight and, for an overlap
                           admission, the live gate), all before any process; then the sched v003 machine gate's own
                           predicates (hold_check and Gate.decide), the r5 route-A snapshot check, A133's root memory
                           rule and memory_pressure; then, in launch mode only, launcher013.
  read                     the reading tool: the registered statistic and reading from the two S1 results and the
                           campaign's u_A result (K4'), reusing reviewed compare-of-record functions by sha.
Labels: TESTED (synthetic tests of this build), FORMAL (follows from cited text or code), UNTESTED (deciding test named).
"""
import ast
import copy
import hashlib
import json
import math
import os
import re
import stat
import sys
import types
from pathlib import Path

MODULE = 's1_path_lib_c2v002'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
SUCC = ART + '/s1_successors_c2'

# ------------------------------------------------------------------------------------------------ pins (sha256 from bytes)
PINS = {
    'P5': (ART + '/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
           'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174'),
    'CB': (ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
           '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
    'COORD': (ART + '/calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json',
              '50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f'),
    'ORC': (ART + '/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
            'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'),
    'CORE': (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py',
             'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6'),
    'GUARD': (SUCC + '/step4_guard_c2v012.py', 'f4656fecc863acf1df1d440f7eb44295dd1a43a8aa4955c18f8e50f57862eeb0'),
    'LAUNCHER': (SUCC + '/step4_launcher_c2v013.py', '620a44da8c68af5175195653da5eaa4d3e4025b2c8029ea841def2332ebb1c58'),
    'WRAPPER_S1K3': (SUCC + '/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001.py', 'e7f52461c33d45d7e506daf25a8c115161cf5cfe661e31afd5a2b1848443856e'),
    'GUARD011': (ART + '/step4_launch_packet_cx1/impl/step4_guard_c2v011.py',
                 'eb97e303b968dc941e2059ada813be95340662253c327a7b9a9634bb8a2c8033'),
    'REGISTRATION': (ART + '/s1_path_c2/S1_REGISTRATION_DRAFT_C2V002.md',
                     '67b4bd78c88d87ea531af99aac16d98c80a20289eca191d4db1897ba8ca76f00'),
    'MONITOR': (ART + '/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
                'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'),
    'DRIVER': (ART + '/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
               'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'),
    'GATE': (ART + '/sched_s45_c2/v003/machine_gate_s45_c2v003.py',
             '736a3438b0a3af41eb8d7b2c764f25ff0f9e18942320a4542a9893b6b419f811'),
    'DBP': (ART + '/sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003A.json',
            '4adc296bcb0ddcd154ec0dcea820908ac525d1d39ce00d633eecc4d0c95f87e7'),
    'COMPARE_R11': (ART + '/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py',
                    'a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a'),
    'COMPARE_R14': (ART + '/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py',
                    'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
    'COMPARE_V005': (ART + '/kmax_prereg_v005_c2/kmax_compare_c2v005.py',
                     '49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5'),
}
R5_SHA = PINS['DRIVER'][1]
OUTPUT_ROOT = '/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001'    # A124 / G11 L268 (string only)
PYTHON = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'  # launcher012 L12
BLAS = {k: '1' for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')}

# ---- note 1: the registration this library implements and the root file that puts it in force (constants, not inputs)
REGISTRATION_SHA = PINS['REGISTRATION'][1]
V6_PATH = CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'
REGISTRATION_ENTRY_PREFIX = '**Registration in force:**'      # V6 A150 L990, root's entry line form
ATTESTATION_PRODUCER_ENTRY_PREFIX = '**S1 attestation producer (SV7):**'   # note 9: root enters each producer sha
FLAG_RULING_ENTRY_PREFIX = '**S1 flag ruling:**'               # note 13: root enters each flag-ruling record sha

# ---- B2: the Phase-1 snapshot fields (phase1_c2v003 149ed4cb cmd_snapshot L476-495, load_snapshot L515-533)
PHASE1_SNAPSHOT_SCHEMA = 'PHASE1_SNAPSHOT_C2V001'               # phase1_c2v003 L91 S_SNAP
PHASE1_BUDGET_EXHAUSTED = 'BUDGET_EXHAUSTED'                    # A133 L65
PTR_SNAPSHOT_STATUS = '/phase1_status'
PTR_SNAPSHOT_U_A_THETA = '/u_A/theta_natural'                  # = run.exploration.primary_anchor.theta_natural (L491)
PTR_SNAPSHOT_U_A_LOG_INDEX = '/u_A/log_index'
PTR_SNAPSHOT_U_A_U_HEX = '/u_A/u_hex'
PTR_SNAPSHOT_RECORD_FILE = '/record/file'                      # the calibration record, beside the snapshot (L477, L486)
PTR_SNAPSHOT_RECORD_SHA = '/record/record_file_sha256'
PTR_RECORD_STATUS = ('/run/status', '/run/exploration/status')  # check_snapshot_run L390
PTR_RECORD_PRIMARY_ANCHOR_THETA = '/run/exploration/primary_anchor/theta_natural'
PTR_RECORD_PRIMARY_ANCHOR_LOG_INDEX = '/run/exploration/primary_anchor/log_index'
PTR_RECORD_PRIMARY_ANCHOR_U = '/run/exploration/primary_anchor/u'

# ---- B1: the only compare files the reader executes, with the AST digest of every reused function (TESTED from bytes).
# r14 (the compare of record, V6 A116/A117) is admitted because each of its 18 reused-function digests equals r11's
# (TESTED); the transitive closure of the 17 c2v001 functions is AST-identical too, and the closure of check_ro1_record
# differs only in activate_driver_build and check_record_codes (r14's R12 A91 / R13 A102 strictness; disclosed).
REVIEWED_COMPARES = {
    'a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a': {'path': ART + '/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py', 'functions': {
        'read_run': '87d009f8e2e42a9ef65f1f7cc6a91559eb6e4c9c0c4624bef693f47af863e036',
        'pass_rows_ids_code': '6bdd101543061b0456f11e428a6eb359aeaa361df1046266373a35ed43cb9ff1',
        'pass_rows_gap': 'd76e18a5ce85278873a2a1b8b58d2f5d378097fd900ee42c89274d3af9807c6b',
        '_pass_rows': '3670ccdf36d6b8a2f6fdf794f60fcaae8bc8420af4721c7f3afddee6b824113e',
        'picard_noise_detail': '972fafd75f3e481f902f0f884bf4963370a670fe4d54b8bc3d343e3ff1ea3040',
        'route_a_noise': '962c9647bd802496179487b1e7c74c9f4317cd4cde79da77b1345f37babb0869',
        'pair_noise': 'eaaab35dbda5311479141c0b6609573b894d9983ac4d17c57bff28ce8482198e',
        'rpair_branch_row': 'f3422b2aea1958e64d0f3087b1cf28cb196b2dfbf07f963ccc2a9510a3e7f091',
        'row_stat': 'a55a552fd59c2cd96f58ad9ceb354fe3fe6c843870931f28775fb5a34bae3f9b',
        'thresholded': '4d128bf05096533739f31c152cd1c6e6ed991278e4f44a2912d47d9c2fa1ba6f',
        'check_uvt_record': '55220c44e09cb85d599a3b2568dd5465b77652e3c61323832d74bcf235eef074',
        'rows_codes': '4f1c6442ecac5ae500eec8119e282277431e8c1a796245313bb4df589e192145',
        'v2_check': '2816f6a876c685463bec8fc159ae133c1501bcd99649fa49af08a531982bf6d9',
        'classify_failure': 'ae5de19143240aad04792cc2de9a57c96c272088373917b6e4e48977d0149bc9',
        'registered_row_radii': 'f2a72f2ffd95c4f08e69d9d92f7a2632ace9fa3e6ffd683444ff33347120caf5',
        'radii_equal': '220b0301c2cb2aa95e49f6620e29bb4357a00065dbeff79d54aeb88b82294f34',
        'ra4_block_expected': 'c6e383d44d556d641eab65885f34fd60b6f3f4d1fc70582bcc876170b57e10f6',
        'check_ro1_record': 'b45e097b8cadbbffe9ff472d5c3a54f480fbfdf65e478e6d291918d11b11afe8',
        'registered_source_rule_is_nodes': '55765389b393fa7db3a37d2ccfa2bfc740e0e06399b7254d69c96d9c5311fca2',
    }},
    'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7': {'path': ART + '/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py', 'functions': {
        'read_run': '87d009f8e2e42a9ef65f1f7cc6a91559eb6e4c9c0c4624bef693f47af863e036',
        'pass_rows_ids_code': '6bdd101543061b0456f11e428a6eb359aeaa361df1046266373a35ed43cb9ff1',
        'pass_rows_gap': 'd76e18a5ce85278873a2a1b8b58d2f5d378097fd900ee42c89274d3af9807c6b',
        '_pass_rows': '3670ccdf36d6b8a2f6fdf794f60fcaae8bc8420af4721c7f3afddee6b824113e',
        'picard_noise_detail': '972fafd75f3e481f902f0f884bf4963370a670fe4d54b8bc3d343e3ff1ea3040',
        'route_a_noise': '962c9647bd802496179487b1e7c74c9f4317cd4cde79da77b1345f37babb0869',
        'pair_noise': 'eaaab35dbda5311479141c0b6609573b894d9983ac4d17c57bff28ce8482198e',
        'rpair_branch_row': 'f3422b2aea1958e64d0f3087b1cf28cb196b2dfbf07f963ccc2a9510a3e7f091',
        'row_stat': 'a55a552fd59c2cd96f58ad9ceb354fe3fe6c843870931f28775fb5a34bae3f9b',
        'thresholded': '4d128bf05096533739f31c152cd1c6e6ed991278e4f44a2912d47d9c2fa1ba6f',
        'check_uvt_record': '55220c44e09cb85d599a3b2568dd5465b77652e3c61323832d74bcf235eef074',
        'rows_codes': '4f1c6442ecac5ae500eec8119e282277431e8c1a796245313bb4df589e192145',
        'v2_check': '2816f6a876c685463bec8fc159ae133c1501bcd99649fa49af08a531982bf6d9',
        'classify_failure': 'ae5de19143240aad04792cc2de9a57c96c272088373917b6e4e48977d0149bc9',
        'registered_row_radii': 'f2a72f2ffd95c4f08e69d9d92f7a2632ace9fa3e6ffd683444ff33347120caf5',
        'radii_equal': '220b0301c2cb2aa95e49f6620e29bb4357a00065dbeff79d54aeb88b82294f34',
        'ra4_block_expected': 'c6e383d44d556d641eab65885f34fd60b6f3f4d1fc70582bcc876170b57e10f6',
        'check_ro1_record': 'b45e097b8cadbbffe9ff472d5c3a54f480fbfdf65e478e6d291918d11b11afe8',
        'registered_source_rule_is_nodes': '55765389b393fa7db3a37d2ccfa2bfc740e0e06399b7254d69c96d9c5311fca2',
    }},
}

# ---- guard012 overlap admission (A150 R-S1-3 (1)); the replay API this module serves to guard012
S1_REPLAY_API = 'UNT_S1_FILL_REPLAY_C2V002'
S1_OVERLAP_SCHEMA = 'UNT_S1_OVERLAP_ADMISSION_C2V001'
CAMPAIGN_WINDOWS = ('SINGLE_CALL_WAVE_START', 'NO_CAMPAIGN_HEAD_PENDING')   # registration section 11 rule 4 (C14)
MEMORY_FREE_MIN_PERCENT = 25                                              # launcher012 L35-36 (note 4)

# ------------------------------------------------------------------------------------------------ registered constants
S1_C3T, S1_C4T, K4P = 'S1_UA_C3T', 'S1_UA_C4T', 'K4_PRIME'
S1_CASES = (S1_C3T, S1_C4T)
RUNS = (S1_C3T, S1_C4T, K4P)
CASE_K = {S1_C3T: 3, S1_C4T: 4, K4P: 4}
CASE_CB = {S1_C3T: 'C3T', S1_C4T: 'C4T', K4P: 'C4T'}
CASE_TAG = {S1_C3T: 'C3T', S1_C4T: 'C4T'}
DBP_CASE = {S1_C3T: 'ROOT_NAMES_AT_REGISTRATION_K3', S1_C4T: 'ROOT_NAMES_AT_REGISTRATION_K4'}   # DBP L155-168
CERT_SLOTS = ('eps_certificate', 'lo_certificate')
ALLOWED_CHANGED = {S1_C4T: ('label',),
                   S1_C3T: ('label', 'numerics.composite_grid_spec', 'numerics.uv_tail.eps_certificate',
                            'numerics.uv_tail.lo_certificate')}
LABEL_FORMAT = 'S1 transfer test %s at u_A theta %s; base %s'        # registration section 4 (CHOICE C5)
SCHEMA_THETA_KEY = 'DDO154_CALIBRATION_THETA_KEY_C2V001'            # ORC L132
ANCHOR_ALIAS_RTOL = 1e-14                                            # ORC L155
MODE_D_FIXED_DISTANCE = 4.04                                         # ORC L160-162
MAPPED_LEAVES = ('common_scale_s', 'gamma', 'ell_F_m', 'distance_Mpc')
VARYING = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'distance_Mpc')
TH1_MAX_OVER_TAU = 1.0                    # V005 shape_pass first numeric clause (P5 L726)
TH2_MAX_OVER_TAU = 0.5                    # V007 T1_H form (R6 L1636)
DECIDABLE_FRACTION = 1.0 / 8.0            # R6 L1231 decidable_iff
A133_LIMIT_GB = 103.0                     # A133 L114 (75 % of RAM)
A133_S1_TERM_GB = 29.1                    # A133 L123 "27 GB per S1 call" in consistent units (27.1 GiB; A141 L2)
A133_CAMPAIGN_RESERVE_GB = 29.1           # A141 L2 (V6): 27.1 GiB in consistent units
CORE_PRIORITY = {'normal_qos_required': True, 'step2_route_a_inactive': True, 'campaign_inactive': True,
                 'background_noncritical_lanes': True, 'sleep_assertion_required': True}       # G11 L333
CORE_PRIORITY_S1_OVERLAP = dict(CORE_PRIORITY, campaign_inactive=False)                    # guard012
PROTECTED_PARTS = ('ngc3198', 'uvt_', 'c5h_hull_c2', 'kmax_a2f10_c5h_run_v001', '.codex')

SCHEMA_UA_POINT = 'UNT_S1_UA_POINT_C2V002'
SCHEMA_FILL = 'UNT_S1_FILL_RECORD_C2V002'
SCHEMA_PLAN = 'UNT_STEP4_LAUNCH_PLAN_CX1V001'                      # G11 L322
SCHEMA_PLAN_SIDECAR = 'UNT_S1_PLAN_RECORD_C2V002'
SCHEMA_LAUNCH_CFG = 'UNT_S1_LAUNCH_CONFIG_C2V002'
SCHEMA_LAUNCH_RECORD = 'UNT_S1_PRELAUNCH_DECISION_C2V002'
SCHEMA_LAUNCH_OUTCOME = 'UNT_S1_LAUNCH_OUTCOME_C2V002'
SCHEMA_MANIFEST = 'UNT_S1_READING_MANIFEST_C2V002'
SCHEMA_ATTEST = 'UNT_S1_GATE_ATTESTATION_C2V001'
SCHEMA_FLAG_RULING = 'UNT_S1_FLAG_RULING_C2V001'
SCHEMA_READING = 'UNT_S1_READING_C2V002'
ATTESTED_GATES = ('SV7',)                 # note 8: RO1 is computed (R11 check_ro1_record), no longer attested
FLAG_CLEARED = 'FLAG_CLEARED_FOR_S1'


# ================================================================================================ custody helpers
class Refusal(ValueError):
    def __init__(self, code, detail=None):
        ValueError.__init__(self, code if detail is None else '%s: %s' % (code, detail))
        self.code = code
        self.detail = detail


def require(cond, code, detail=None):
    if cond is not True:
        raise Refusal(code, detail)


def _lexical_guard(path):
    """Lexical refusal of protected names (the G11 L57 class, plus .codex, C5H and v003g/slots)."""
    require(isinstance(path, str) and os.path.isabs(path), 'ABSOLUTE_PATH_REQUIRED', repr(path))
    parts = Path(path).parts
    ruling = re.fullmatch(r'ROOT_DECISIONS_NGC3198_CONSTRUCTION_[A-Za-z0-9_-]+\.md', parts[-1]) is not None
    for n, part in enumerate(parts):
        if ruling and n == len(parts) - 1:
            continue                     # the root ruling files only (the G11 L56-57 metadata exception)
        low = part.casefold()
        require(not any(low.startswith(x) if x == 'uvt_' else (x in low) for x in PROTECTED_PARTS),
                'PROTECTED_PATH_REFUSED', path)
    require('v003g/slots' not in path, 'PROTECTED_PATH_REFUSED', path)
    require('..' not in parts, 'PROTECTED_PATH_REFUSED', '.. component: %s' % path)


def guard_path(path):
    """Note 12: the lexical refusal, then a component-by-component walk (guard011 safe_path L60-82) in which every
    symlink target is refused lexically before it is followed; no stat or open of a protected name. Returns Path(path)."""
    _lexical_guard(path)
    todo, cur, links = list(Path(path).parts[1:]), Path('/'), 0
    while todo:
        part = todo.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':                 # only reachable through a relative symlink target (inputs refuse '..')
            cur = cur.parent
            continue
        cand = cur / part
        _lexical_guard(str(cand))
        try:
            info = os.lstat(str(cand))
        except (FileNotFoundError, NotADirectoryError):
            cur = cand
            continue
        except OSError as exc:
            raise Refusal('PATH_UNREADABLE', '%s: %s' % (cand, type(exc).__name__))
        if stat.S_ISLNK(info.st_mode):
            links += 1
            require(links <= 40, 'SYMLINK_LOOP_REFUSED', path)
            target = os.readlink(str(cand))
            tp = Path(target) if os.path.isabs(target) else cur / target
            _lexical_guard(os.path.normpath(str(tp)))
            if os.path.isabs(target):
                cur, todo = Path('/'), list(Path(target).parts[1:]) + todo
            else:
                todo = list(Path(target).parts) + todo
        else:
            cur = cand
    _lexical_guard(os.path.normpath(str(cur)))
    return Path(path)


def read_bytes(path):
    p = guard_path(str(path))
    try:
        fd = os.open(str(p), os.O_RDONLY | os.O_NOFOLLOW)
    except FileNotFoundError:
        raise Refusal('FILE_MISSING', str(p))
    except OSError as exc:
        raise Refusal('FILE_UNREADABLE', '%s: %s' % (p, type(exc).__name__))
    try:
        require(stat.S_ISREG(os.fstat(fd).st_mode), 'REGULAR_FILE_REQUIRED', str(p))
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
        return b''.join(chunks)
    finally:
        os.close(fd)


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def pin_of(path):
    return {'path': str(path), 'sha256': sha256_bytes(read_bytes(path))}


def is_pin(ref):
    return (isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and isinstance(ref['path'], str)
            and isinstance(ref['sha256'], str) and len(ref['sha256']) == 64
            and all(c in '0123456789abcdef' for c in ref['sha256']))


def verify_pin(ref, code='PIN'):
    require(is_pin(ref), code + '_PIN_REQUIRED', repr(ref)[:200])
    raw = read_bytes(ref['path'])
    require(sha256_bytes(raw) == ref['sha256'], code + '_PIN_BYTES_CHANGED', ref['path'])
    return raw


def _pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, 'DUPLICATE_JSON_KEY', k)
        out[k] = v
    return out


def _finite(s):
    v = float(s)
    require(math.isfinite(v), 'NONFINITE_JSON')
    return v


def strict_json(raw):
    try:
        return json.loads(raw, object_pairs_hook=_pairs, parse_float=_finite,
                          parse_constant=lambda s: (_ for _ in ()).throw(Refusal('NONFINITE_JSON')))
    except Refusal:
        raise
    except (ValueError, UnicodeDecodeError) as exc:
        raise Refusal('JSON_UNREADABLE', type(exc).__name__)


def pinned_json(ref, code='PIN'):
    d = strict_json(verify_pin(ref, code))
    require(isinstance(d, dict), code + '_OBJECT_REQUIRED')
    return d


def const_pin(key):
    return {'path': PINS[key][0], 'sha256': PINS[key][1]}


def canonical(obj):
    """G11 L105 / ORC L261 / CORE canonical form."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(obj):
    return sha256_bytes(canonical(obj))


def spec_bytes(obj):
    """ORC json_bytes (L285): the bytes Mapper.build writes for a call spec."""
    return (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def record_bytes(obj):
    return (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def write_exclusive(path, data):
    p = guard_path(str(path))
    try:
        fd = os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    except FileExistsError:
        raise Refusal('OUTPUT_EXISTS', str(p))
    except OSError as exc:
        raise Refusal('OUTPUT_NOT_CREATABLE', '%s: %s' % (p, type(exc).__name__))
    try:
        view = memoryview(data)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'path': str(p), 'sha256': sha256_bytes(data)}


def fhex(x):
    return float(x).hex()


def module_sha256():
    """sha256 of this library's own bytes (the CLI wrappers load it by this sha)."""
    try:
        return sha256_bytes(read_bytes(globals().get('__file__') or ''))
    except Exception:                                                    # noqa: BLE001 -- custody field only
        return None


def load_source_module(ref, name, code):
    """exec a pinned .py from its verified bytes (the launcher012 L7-11 pattern)."""
    raw = verify_pin(ref, code)
    m = types.ModuleType(name)
    m.__file__ = ref['path']
    sys.modules[name] = m
    exec(compile(raw, ref['path'], 'exec'), m.__dict__)
    return m


def extract_definitions(raw, names, filename, prelude=''):
    """Exec only the named top-level functions / classes / assignments of a pinned source, in a fresh namespace.
    Used to replay as-built clauses (CORE validate_block / point_identity, ORC theta_key / diff_paths / Mapper)
    without executing the module's import-time code."""
    tree = ast.parse(raw)
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names:
            keep.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets):
            keep.append(node)
    found = {getattr(n, 'name', None) or n.targets[0].id for n in keep}
    require(found == set(names), 'EXTRACTION_INCOMPLETE', sorted(set(names) - found))
    ns = {}
    exec(compile(prelude, filename + ':prelude', 'exec'), ns)
    exec(compile(ast.Module(body=keep, type_ignores=[]), filename + ':extracted', 'exec'), ns)
    return ns


def function_digests(raw, names):
    """sha256 of ast.dump of each named top-level function (a byte-independent identity of the reused code)."""
    tree = ast.parse(raw)
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            out[node.name] = sha256_bytes(ast.dump(node, include_attributes=False).encode())
    return {n: out.get(n) for n in names}


# ================================================================================================ mapping (ORC / CORE formulas)
def theta_key(theta):
    """ORC L523-529 verbatim formula (TESTED equal to the extracted ORC function)."""
    th = {str(k): float(v) for k, v in theta.items()}
    for k, v in th.items():
        require(math.isfinite(v), 'THETA_NONFINITE', k)
    return sha256_bytes(canonical({'schema': SCHEMA_THETA_KEY, 'theta': th}))


def diff_paths(a, b, prefix=''):
    """ORC L532-543 verbatim (TESTED equal to the extracted ORC function)."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = (prefix + '.' + str(k)) if prefix else str(k)
            if k not in a or k not in b:
                out.append(p)
            else:
                out.extend(diff_paths(a[k], b[k], p))
        return out
    return [] if canonical(a) == canonical(b) else [prefix or '$']


def point_identity(spec):
    """CORE L233-238 (TESTED equal to the extracted CORE function)."""
    n = copy.deepcopy(spec['numerics'])
    for key in CERT_SLOTS:
        n['uv_tail'].pop(key, None)
    return {'driver_sha256': R5_SHA, 'physical': spec['physical'], 'coefficients': spec['coefficients'], 'numerics': n}


def mapped_physical(theta):
    """ORC Mapper.build L2216-2219: the four leaves set from theta (TESTED equal to the extracted Mapper)."""
    return {'common_scale_s': theta['common_scale_s'], 'gamma': theta['gamma_over_Eref'] * theta['Eref_base_J'],
            'ell_F_m': theta['ell_F_m'], 'distance_Mpc': theta['distance_Mpc']}


def strip_certs(numerics):
    n = copy.deepcopy(numerics)
    if isinstance(n.get('uv_tail'), dict):
        for k in CERT_SLOTS:
            n['uv_tail'].pop(k, None)
    return n


def _tf(v, kind):
    return math.log(v) if kind == 'log' else float(v)


def u_value(v, coord):
    """The engine box coordinate u = (T(v) - T(lower)) / (T(upper) - T(lower)), T = ln for log coordinates.
    TESTED: it reproduces the coordinate spec's engine_trial_u from engine_seed_theta (COORD trial_point)."""
    lo, hi = _tf(coord['lower'], coord['transform']), _tf(coord['upper'], coord['transform'])
    return (_tf(v, coord['transform']) - lo) / (hi - lo)


def allowed_path(p, allowed):
    return any(p == a or p.startswith(a + '.') for a in allowed)


# ================================================================================================ static inputs
def load_static():
    p5 = pinned_json(const_pin('P5'), 'P5')
    cb = pinned_json(const_pin('CB'), 'CB')
    coord = pinned_json(const_pin('COORD'), 'COORD')
    ids, tau, sig = p5['row_ids'], p5['tau_km_s'], p5['quoted_sigma_km_s']
    require(isinstance(ids, list) and len(ids) == 12 and len(set(ids)) == 12 and len(tau) == 12 and len(sig) == 12,
            'P5_ROWS')
    return {'p5': p5, 'cb': cb, 'coord': coord, 'ids': ids, 'tau': dict(zip(ids, tau)), 'sigma': dict(zip(ids, sig)),
            'tau_picard': float(p5['criterion']['tau_picard_km_s']), 'anchor_physical': p5['anchor']['physical']}


def cb_numerics(st, cbcase):
    return st['cb']['cases'][cbcase]['normalized_spec_equal']['/numerics']


def core_replay():
    """CORE validate_block, extracted from the pinned bytes (as-built control-3 clause, CORE L213-231)."""
    raw = verify_pin(const_pin('CORE'), 'CORE')
    ns = extract_definitions(raw, ('validate_block', 'HULL'), PINS['CORE'][0],
                             prelude='class Error(Exception):\n    pass\n')
    return ns


def as_built_core_check(spec):
    try:
        core_replay()['validate_block'](spec['numerics'])
        return 'PASS'
    except Exception as exc:
        return 'REFUSED: %s' % exc


_WRAPPER = {}


def wrapper_successor():
    """The S1-only kept-K-3 wrapper successor, executed from its pinned bytes (it loads q5b1 / core unchanged)."""
    if 'm' not in _WRAPPER:
        _WRAPPER['m'] = load_source_module(const_pin('WRAPPER_S1K3'), '_s1_wrapper_s1k3_c2v001', 'WRAPPER_S1K3')
    return _WRAPPER['m']


def successor_core_check(spec):
    """Control-3 clause of the wrapper successor (validate_spec_block): S1_UA_C3T with the CB C3T grid passes; every
    other spec is core dc895f8a's validate_block."""
    try:
        wrapper_successor().validate_spec_block(spec)
        return 'PASS'
    except Refusal:
        raise
    except Exception as exc:
        return 'REFUSED: %s' % exc


# ================================================================================================ part 1: the template
def check_theta(udoc, st):
    require(udoc.get('schema') == SCHEMA_UA_POINT, 'UA_POINT_SCHEMA')
    theta = udoc.get('theta')
    require(isinstance(theta, dict), 'THETA_REQUIRED')
    coords = {c['name']: c for c in st['coord']['engine_coordinates']}
    require(sorted(theta) == sorted(coords), 'THETA_NAMES_NOT_THE_ENGINE_COORDINATES')
    for nm, v in theta.items():
        require(type(v) is float and math.isfinite(v), 'THETA_NOT_A_FINITE_FLOAT', nm)
        c = coords[nm]
        require(c['lower'] <= v <= c['upper'], 'THETA_OUT_OF_BOX', nm)
        if c['role'] == 'fixed':
            require(fhex(v) == fhex(c['trial_value']), 'THETA_FIXED_COORDINATE_MOVED', nm)
    require(fhex(theta['distance_Mpc']) == fhex(MODE_D_FIXED_DISTANCE), 'THETA_DISTANCE_NOT_REGISTERED')
    key = theta_key(theta)
    require(udoc.get('theta_key') == key, 'THETA_KEY_MISMATCH')
    bind_phase1_primary_anchor(udoc.get('phase1_snapshot'), theta, key)
    return theta, key


def json_pointer(doc, ptr, code):
    """RFC 6901 pointer (no escapes are used by the registered pointers); a missing member refuses with code."""
    cur = doc
    for tok in ptr.split('/')[1:]:
        if isinstance(cur, dict) and tok in cur:
            cur = cur[tok]
        elif isinstance(cur, list) and tok.isdigit() and int(tok) < len(cur):
            cur = cur[int(tok)]
        else:
            raise Refusal(code, 'no member at %s' % ptr)
    return cur


def _theta_bits_equal(nat, theta):
    if not isinstance(nat, dict) or sorted(nat) != sorted(theta):
        return False
    for k, v in nat.items():
        if type(v) not in (int, float) or not math.isfinite(float(v)) or fhex(float(v)) != fhex(theta[k]):
            return False
    return True


def bind_phase1_primary_anchor(snap_ref, theta, key):
    """B2: u_A is the Phase-1 snapshot's primary anchor. The snapshot (phase1_c2v003 cmd_snapshot) must be a
    BUDGET_EXHAUSTED PHASE1_SNAPSHOT_C2V001 whose /u_A/theta_natural is fhex-equal to theta on every coordinate (and
    whose theta_key is the u_A key); the calibration record it names (by file and sha, beside it) must read
    BUDGET_EXHAUSTED in run.status and run.exploration.status, and its run.exploration.primary_anchor must carry the
    same theta bits, log index and u bits. Any other point the record mentions (the engine log) does not bind."""
    snap = pinned_json(snap_ref, 'PHASE1_SNAPSHOT')
    require(snap.get('schema') == PHASE1_SNAPSHOT_SCHEMA, 'PHASE1_SNAPSHOT_SCHEMA')
    require(json_pointer(snap, PTR_SNAPSHOT_STATUS, 'PHASE1_SNAPSHOT_FIELD') == PHASE1_BUDGET_EXHAUSTED,
            'PHASE1_STATUS_NOT_BUDGET_EXHAUSTED')
    nat = json_pointer(snap, PTR_SNAPSHOT_U_A_THETA, 'PHASE1_SNAPSHOT_FIELD')
    require(_theta_bits_equal(nat, theta), 'PHASE1_PRIMARY_ANCHOR_NOT_U_A', PTR_SNAPSHOT_U_A_THETA)
    require(theta_key({k: float(v) for k, v in nat.items()}) == key, 'PHASE1_PRIMARY_ANCHOR_NOT_U_A', 'theta_key')
    log_index = json_pointer(snap, PTR_SNAPSHOT_U_A_LOG_INDEX, 'PHASE1_SNAPSHOT_FIELD')
    u_hex = json_pointer(snap, PTR_SNAPSHOT_U_A_U_HEX, 'PHASE1_SNAPSHOT_FIELD')
    fname = json_pointer(snap, PTR_SNAPSHOT_RECORD_FILE, 'PHASE1_SNAPSHOT_FIELD')
    require(isinstance(fname, str) and fname == os.path.basename(fname) and fname not in ('', '.', '..'),
            'PHASE1_RECORD_FILE_NAME')
    rec_ref = {'path': str(Path(snap_ref['path']).parent / fname),
               'sha256': json_pointer(snap, PTR_SNAPSHOT_RECORD_SHA, 'PHASE1_SNAPSHOT_FIELD')}
    rec = pinned_json(rec_ref, 'PHASE1_RECORD')
    for ptr in PTR_RECORD_STATUS:
        require(json_pointer(rec, ptr, 'PHASE1_RECORD_FIELD') == PHASE1_BUDGET_EXHAUSTED,
                'PHASE1_STATUS_NOT_BUDGET_EXHAUSTED', ptr)
    require(_theta_bits_equal(json_pointer(rec, PTR_RECORD_PRIMARY_ANCHOR_THETA, 'PHASE1_RECORD_FIELD'), theta),
            'PHASE1_PRIMARY_ANCHOR_NOT_U_A', PTR_RECORD_PRIMARY_ANCHOR_THETA)
    require(json_pointer(rec, PTR_RECORD_PRIMARY_ANCHOR_LOG_INDEX, 'PHASE1_RECORD_FIELD') == log_index
            and type(log_index) is int, 'PHASE1_PRIMARY_ANCHOR_NOT_U_A', 'log_index')
    u = json_pointer(rec, PTR_RECORD_PRIMARY_ANCHOR_U, 'PHASE1_RECORD_FIELD')
    require(isinstance(u, list) and isinstance(u_hex, list) and len(u) == len(u_hex)
            and all(type(x) in (int, float) and fhex(x) == h for x, h in zip(u, u_hex)),
            'PHASE1_PRIMARY_ANCHOR_NOT_U_A', 'u bits')
    return {'snapshot': snap_ref, 'record': rec_ref, 'log_index': log_index}


def check_base(base, base_sha, theta, key, cfg_block, st):
    require(base.get('galaxy') == 'DDO154', 'BASE_GALAXY')
    require('admit' in base and base['admit'] == {}, 'BASE_ADMIT_NOT_EMPTY_OBJECT')         # G11 L216
    ph = base.get('physical') or {}
    want = dict(mapped_physical(theta), Eref_J=theta['Eref_base_J'], entropy_K_factor=theta['entropy_K_factor'])
    for leaf, v in want.items():
        require(type(ph.get(leaf)) is float and fhex(ph[leaf]) == fhex(v), 'THETA_PHYSICAL_MISMATCH', leaf)
    require(fhex(ph.get('inclination_deg', float('nan'))) == fhex(st['anchor_physical']['inclination_deg']),
            'BASE_INCLINATION')
    require(isinstance(base.get('label'), str) and ('theta ' + key[:16]) in base['label'], 'BASE_LABEL_THETA_MISMATCH')
    require(canonical(base.get('coefficients')) == canonical(st['p5']['anchor']['coefficients']),
            'BASE_COEFFICIENTS_NOT_REGISTERED')                                                  # P5 V3 L712
    n = base.get('numerics')
    require(isinstance(n, dict), 'BASE_NUMERICS')
    require(canonical(strip_certs(n)) == canonical(strip_certs(cfg_block)), 'BASE_NUMERICS_NOT_CAMPAIGN_BLOCK')
    c4 = cb_numerics(st, 'C4T')
    require(canonical(n.get('composite_grid_spec')) == canonical(c4['composite_grid_spec'])
            and n['composite_grid_spec']['breaks_inverse_kpc'][-1] == 4, 'BASE_NOT_C4T_GRID')
    require(canonical(n.get('brackets')) == canonical(c4['brackets']), 'BASE_BRACKETS_NOT_RA4_BLOCK')
    require(n.get('truncation') == {'shape': 'cube'}, 'BASE_TRUNCATION_NOT_CUBE')
    u = n.get('uv_tail') or {}
    require(u.get('enabled') is True, 'BASE_TAIL_NOT_ON')
    for slot in CERT_SLOTS:
        verify_pin(u.get(slot), 'BASE_' + slot.upper())
    return True


def build_case(base, base_sha, key, case, st, certs):
    s = copy.deepcopy(base)
    s['label'] = LABEL_FORMAT % (CASE_TAG[case], key[:16], base_sha[:8])
    if case == S1_C3T:
        s['numerics']['composite_grid_spec'] = copy.deepcopy(cb_numerics(st, 'C3T')['composite_grid_spec'])
        for slot in CERT_SLOTS:
            s['numerics']['uv_tail'][slot] = copy.deepcopy(certs[slot]) if certs else 'PENDING_S1_C3T_POINT_CERTIFICATE'
    changed = diff_paths(base, s)
    require(all(allowed_path(p, ALLOWED_CHANGED[case]) for p in changed), 'S1_UNDECLARED_CHANGE', changed)
    require(s['numerics']['composite_grid_spec']['breaks_inverse_kpc'][-1] == CASE_K[case], 'S1_CASE_K_MISMATCH')
    raw = spec_bytes(s)
    return s, raw, changed


def branch_record(theta, st, physical):
    coords = {c['name']: c for c in st['coord']['engine_coordinates']}
    seed = st['coord']['trial_point']['engine_seed_theta']
    seed_bits = sorted(seed) == sorted(theta) and all(fhex(theta[k]) == fhex(seed[k]) for k in theta)
    anc = st['anchor_physical']
    rel = {k: abs(physical[k] / anc[k] - 1.0) for k in MAPPED_LEAVES}
    alias = all(r <= ANCHOR_ALIAS_RTOL for r in rel.values())
    du, dT = {}, {}
    for nm in VARYING:
        c = coords[nm]
        du[nm] = u_value(theta[nm], c) - u_value(seed[nm], c)
        half = (_tf(c['upper'], c['transform']) - _tf(c['lower'], c['transform'])) / 2.0
        d = _tf(theta[nm], c['transform']) - _tf(c['trial_value'], c['transform'])
        dT[nm] = {'delta_transform': d, 'over_half_width': d / half, 'transform': c['transform']}
    lnl = {k: math.log(physical[k] / anc[k]) for k in MAPPED_LEAVES}
    branch = 'AT_ANCHOR' if (seed_bits or alias) else 'OFF_ANCHOR'
    return {'branch': branch, 'seed_bits_equal': seed_bits, 'anchor_alias_within_rtol': alias,
            'anchor_alias_rtol': ANCHOR_ALIAS_RTOL, 'relative_deviation_from_anchor': rel,
            'u_A_minus_u_seed': du, 'delta_from_trial': dT,
            'max_abs_over_half_width': max(abs(v['over_half_width']) for v in dT.values()),
            'ln_leaf_over_anchor_leaf': lnl,
            'basis': 'u = (T(v)-T(lo))/(T(hi)-T(lo)), T = ln for log coordinates (reproduces COORD engine_trial_u, TESTED); '
                     'seed = COORD trial_point.engine_seed_theta; anchor = P5 anchor.physical; AT_ANCHOR iff seed bits '
                     'equal or every mapped leaf within ANCHOR_ALIAS_RTOL (ORC L155) of the anchor'}


C3T_CHAIN_NOTE = ('S1_UA_C3T: the as-built certificate chain is K=4-only: custody_cx2v002 derive_details L111-113 '
                  '("K4 cube required"), point_response_producer_cx2v002 shell_plan L113-123 (coverage from the literal 4), '
                  'CP-1 runner c3v004 EPS_SHELLS/RHO_COVERAGE (L82-L96) and certificate guard b1 L94 (domain K 4.0 only); '
                  'see S1_C3T_CERT_EXTENSION_PROCEDURE.md')


def c3t_slots_from_registry(registry_ref, spec):
    """Note 10: the C3T certificate slots are the registry entry of point_identity(S1_UA_C3T), with the identity-equality
    check of core dc895f8a Mapper.build L246-258 (canonical, stricter than ==); any two pinned files are not enough."""
    reg = pinned_json(registry_ref, 'C3T_REGISTRY')
    ident = point_identity(spec)
    rec = (reg.get('points') or {}).get(digest(ident)) if isinstance(reg.get('points'), dict) else None
    require(isinstance(rec, dict), 'C3T_REGISTRY_POINT_MISSING', digest(ident)[:16])
    require(canonical(rec.get('identity')) == canonical(ident), 'C3T_REGISTRY_IDENTITY_MISMATCH')
    slots = {}
    for slot in CERT_SLOTS:
        verify_pin(rec.get(slot), 'C3T_' + slot.upper())
        slots[slot] = copy.deepcopy(rec[slot])
    return slots


def fill(u_a_ref, base_ref, config_ref, c3t_registry=None, out_dir=None, dry=False):
    """The S1 template. Returns the fill record; writes the two specs and the record by exclusive create unless dry."""
    st = load_static()
    udoc = pinned_json(u_a_ref, 'UA_POINT')
    theta, key = check_theta(udoc, st)
    base_raw = verify_pin(base_ref, 'BASE_SPEC')
    base = strict_json(base_raw)
    require(isinstance(base, dict), 'BASE_SPEC_OBJECT')
    cfg = pinned_json(config_ref, 'CAMPAIGN_CONFIG')
    cfg_block = (cfg.get('numerics') or {}).get('block')
    require(isinstance(cfg_block, dict), 'CAMPAIGN_CONFIG_NUMERICS_BLOCK')
    check_base(base, base_ref['sha256'], theta, key, cfg_block, st)
    c3t_certs = None
    if c3t_registry is not None:
        pending, _, _ = build_case(base, base_ref['sha256'], key, S1_C3T, st, None)
        c3t_certs = c3t_slots_from_registry(c3t_registry, pending)
    else:
        require(dry, 'C3T_REGISTRY_REQUIRED')
    phys = {k: base['physical'][k] for k in MAPPED_LEAVES}
    rec = {'schema': SCHEMA_FILL, 'module': MODULE, 'module_sha256': module_sha256(), 'dry': bool(dry), 'theta_key': key,
           'u_A_point': u_a_ref, 'phase1_snapshot': udoc['phase1_snapshot'], 'base_spec': base_ref,
           'campaign_config': config_ref, 'c3t_registry': c3t_registry,
           'static_pins': {k: const_pin(k) for k in ('P5', 'CB', 'COORD', 'WRAPPER_S1K3')},
           'base_point_key': digest(point_identity(base)),
           'physical_u_A': {k: {'value': v, 'hex': fhex(v)} for k, v in base['physical'].items()},
           'theta': {k: {'value': v, 'hex': fhex(v)} for k, v in sorted(theta.items())},
           'branch': branch_record(theta, st, phys), 'cases': {}, 'blockers': [], 'notes': [C3T_CHAIN_NOTE]}
    for case in S1_CASES:
        s, raw, changed = build_case(base, base_ref['sha256'], key, case, st, c3t_certs)
        entry = {'k': CASE_K[case], 'cb_case': CASE_CB[case], 'label': s['label'], 'changed_paths': changed,
                 'sha256': sha256_bytes(raw), 'point_key': digest(point_identity(s)),
                 'as_built_core_validate_block': as_built_core_check(s),
                 'successor_validate_spec_block': successor_core_check(s)}
        if case == S1_C4T:
            require(entry['point_key'] == rec['base_point_key'], 'C4T_POINT_KEY_NOT_BASE')
        if entry['successor_validate_spec_block'] != 'PASS':
            rec['blockers'].append('%s: the wrapper successor refuses this spec (%s)'
                                   % (case, entry['successor_validate_spec_block']))
        if case == S1_C3T and c3t_certs is None:
            rec['blockers'].append('S1_UA_C3T: no certificate-registry entry for point key %s yet' % entry['point_key'][:16])
        entry['_raw'] = raw
        rec['cases'][case] = entry
    if not dry:
        require(isinstance(out_dir, str), 'OUT_DIR_REQUIRED')
        d = guard_path(out_dir)
        require(d.is_dir() and not d.is_symlink(), 'OUT_DIR_MUST_EXIST')
        for case in S1_CASES:
            e = rec['cases'][case]
            e['spec'] = write_exclusive(str(d / ('%s_%s.spec.json' % (case, key[:16]))), e['_raw'])
    for case in S1_CASES:
        rec['cases'][case].pop('_raw')
    if not dry:
        rec['record'] = write_exclusive(str(guard_path(out_dir) / ('S1_FILL_RECORD_%s.json' % key[:16])), record_bytes(rec))
    return rec


def replay_specs(fill_rec):
    """Re-derive both S1 spec byte strings from the fill record's own pinned inputs (template replay). The C3T
    certificate slots are looked up again in the pinned registry (note 10), never read back from the spec."""
    require(isinstance(fill_rec, dict) and fill_rec.get('schema') == SCHEMA_FILL and fill_rec.get('dry') is False,
            'FILL_RECORD_NOT_WRITTEN_FILL')
    st = load_static()
    udoc = pinned_json(fill_rec['u_A_point'], 'UA_POINT')
    theta, key = check_theta(udoc, st)
    require(key == fill_rec['theta_key'], 'FILL_RECORD_THETA_KEY')
    require(udoc.get('phase1_snapshot') == fill_rec.get('phase1_snapshot'), 'FILL_RECORD_PHASE1_SNAPSHOT')
    base = strict_json(verify_pin(fill_rec['base_spec'], 'BASE_SPEC'))
    cfg = pinned_json(fill_rec['campaign_config'], 'CAMPAIGN_CONFIG')
    check_base(base, fill_rec['base_spec']['sha256'], theta, key, cfg['numerics']['block'], st)
    pending, _, _ = build_case(base, fill_rec['base_spec']['sha256'], key, S1_C3T, st, None)
    certs = c3t_slots_from_registry(fill_rec.get('c3t_registry'), pending)
    out = {}
    for case in S1_CASES:
        _, raw, _ = build_case(base, fill_rec['base_spec']['sha256'], key, case, st, certs if case == S1_C3T else None)
        out[case] = raw
    return out, st


CP1_PENDING_SLOT = 'PENDING_UV_TAIL_CERTIFICATE'          # core dc895f8a L29 PENDING; the CP-1 dry-plan spec form


def write_c3t_cp1_spec(u_a_ref, base_ref, config_ref, out_dir=None, dry=False):
    """The S1_UA_C3T spec in CP-1's input form (S1_C3T_CERT_EXTENSION_PROCEDURE.md step 2): the S1 template's C3T spec with
    both certificate slots set to core's PENDING marker. point_identity excludes the slots and the label, so its point key
    is the key of the S1_UA_C3T spec the fill writes once the registry entry exists (TESTED). Writes by exclusive create."""
    st = load_static()
    udoc = pinned_json(u_a_ref, 'UA_POINT')
    theta, key = check_theta(udoc, st)
    base = strict_json(verify_pin(base_ref, 'BASE_SPEC'))
    require(isinstance(base, dict), 'BASE_SPEC_OBJECT')
    cfg = pinned_json(config_ref, 'CAMPAIGN_CONFIG')
    check_base(base, base_ref['sha256'], theta, key, (cfg.get('numerics') or {}).get('block') or {}, st)
    s, _, _ = build_case(base, base_ref['sha256'], key, S1_C3T, st, None)
    for slot in CERT_SLOTS:
        s['numerics']['uv_tail'][slot] = CP1_PENDING_SLOT
    raw = spec_bytes(s)
    out = {'case': S1_C3T, 'theta_key': key, 'point_key': digest(point_identity(s)), 'sha256': sha256_bytes(raw),
           'successor_validate_spec_block': successor_core_check(s), 'k': CASE_K[S1_C3T],
           'composite_grid_spec_version': s['numerics']['composite_grid_spec'].get('version')}
    if not dry:
        require(isinstance(out_dir, str), 'OUT_DIR_REQUIRED')
        d = guard_path(out_dir)
        require(d.is_dir() and not d.is_symlink(), 'OUT_DIR_MUST_EXIST')
        out['spec'] = write_exclusive(str(d / ('S1_UA_C3T_%s.cp1.spec.json' % key[:16])), raw)
    return out


def guard_replay(fill_ref):
    """The S1_REPLAY_API guard012 calls (A150 R-S1-3 (1)): {'cases': {case: {'spec': the fill record's spec pin,
    'bytes': the replayed spec bytes}}}. Refuses (raises Refusal) on any pin, binding or replay failure."""
    fill_rec = pinned_json(fill_ref, 'FILL_RECORD')
    replay, _ = replay_specs(fill_rec)
    out = {}
    for case in S1_CASES:
        spec_ref = fill_rec['cases'][case]['spec']
        require(is_pin(spec_ref) and sha256_bytes(replay[case]) == spec_ref['sha256'], 'S1_TEMPLATE_REPLAY_MISMATCH', case)
        out[case] = {'spec': spec_ref, 'bytes': replay[case]}
    return {'api': S1_REPLAY_API, 'fill_record': fill_ref, 'cases': out}


def self_pin():
    """This library's own pin (the guard012 replay module named in an overlap admission)."""
    return {'path': str(globals().get('__file__') or ''), 'sha256': module_sha256()}


def make_plan(fill_ref, case, prelaunch_ref, params_ref=None, attempt=1, out_path=None, output_root=OUTPUT_ROOT,
              dry=False, overlap=False):
    """One POST_S1 plan per S1 call (CHOICE C14: each S1 head passes the machine gate at its own start). overlap=True
    writes guard012's S1 overlap admission fields into the sidecar (campaign active); the plan bytes are the same."""
    require(case in S1_CASES, 'S1_CASE_UNKNOWN', case)
    require(type(overlap) is bool, 'OVERLAP_FLAG_BOOL')
    require(type(attempt) is int and attempt >= 1, 'ATTEMPT_POSITIVE_INT')
    fill_rec = pinned_json(fill_ref, 'FILL_RECORD')
    require(fill_rec.get('schema') == SCHEMA_FILL and fill_rec.get('dry') is False, 'FILL_RECORD_NOT_WRITTEN_FILL')
    spec_ref = fill_rec['cases'][case]['spec']
    spec = strict_json(verify_pin(spec_ref, 'S1_SPEC'))
    params = pinned_json(params_ref or const_pin('DBP'), 'PARAMS')
    post = (params.get('batches') or {}).get('POST_S1')
    require(isinstance(post, dict), 'PARAMS_POST_S1_REQUIRED')
    caps = copy.deepcopy(post['caps_per_case'][DBP_CASE[case]])
    rule = copy.deepcopy(post['route_a_admission'])
    rule['max_active'] = 1
    name = '%s_%s_A%d' % (case, fill_rec['theta_key'][:16], attempt)
    outdir = output_root.rstrip('/') + '/' + name
    call = {'case': case, 'spec': spec_ref, 'driver': const_pin('DRIVER'), 'spec_status': 'ROOT_FINAL', 'pending': [],
            'distance_Mpc': spec['physical']['distance_Mpc'], 'tail_on': True, 'family': 'S4_POST_S1',
            'wall_cap_s': caps['wall_cap_s'], 'rss_cap_bytes': caps['rss_cap_bytes'],
            'output_cap_bytes': caps['output_cap_bytes'], 'prelaunch': prelaunch_ref,
            'outdir': outdir, 'receipt': outdir + '.receipt.json', 'monitor_log': outdir + '.monitor.log'}
    blockers = []
    if prelaunch_ref is None:
        blockers.append('PRELAUNCH_RECORD_REQUIRED (PRELAUNCH005 native preflight record for this spec)')
        call['pending'] = ['PRELAUNCH_RECORD']
    else:
        pre = pinned_json(prelaunch_ref, 'PRELAUNCH')
        require(pre.get('schema') == 'UNT_STEP4_PRELAUNCH_CX1V001' and pre.get('case') == case
                and pre.get('spec') == spec_ref and pre.get('driver') == const_pin('DRIVER')
                and pre.get('adoption_checked') is True, 'PRELAUNCH_RECORD_BINDING')
    plan = {'schema': SCHEMA_PLAN, 'binding_status': 'ROOT_BOUND', 'batch': 'POST_S1',
            'launcher': const_pin('LAUNCHER'), 'guard': const_pin('GUARD'), 'monitor': const_pin('MONITOR'),
            'route_a_admission': rule, 'launcher_log': outdir + '.launcher.log', 'calls': [call],
            's1': {'fill_record': fill_ref, 'theta_key': fill_rec['theta_key'], 'k': CASE_K[case],
                   'branch': fill_rec['branch']['branch'], 'attempt': attempt}}
    fields = {'case_order': [case], 'caps': {case: caps},
              'calls': {case: {'spec': spec_ref, 'driver': const_pin('DRIVER'), 'prelaunch': prelaunch_ref}},
              'route_a_admission': rule, 'core_priority': CORE_PRIORITY_S1_OVERLAP if overlap else CORE_PRIORITY,
              'batch': 'POST_S1', 'context_module': const_pin('WRAPPER_S1K3'),
              'sources_to_add': [const_pin('GUARD'), const_pin('LAUNCHER'), const_pin('WRAPPER_S1K3')]
              + ([self_pin()] if overlap else [])}
    if overlap:
        fields['s1_overlap'] = {'schema': S1_OVERLAP_SCHEMA, 'replay_module': self_pin(), 'fill_record': fill_ref}
    sidecar = {'schema': SCHEMA_PLAN_SIDECAR, 'module': MODULE, 'module_sha256': module_sha256(), 'case': case,
               'blockers': blockers, 'overlap': overlap, 'admission_fields_for_root': fields,
               'caps_basis': 'DBP POST_S1 caps_per_case %s (wall PROVISIONAL until the A140 N4 successor)' % DBP_CASE[case],
               'as_built_core_validate_block': as_built_core_check(spec),
               'successor_validate_spec_block': successor_core_check(spec),
               'notes': [C3T_CHAIN_NOTE] if case == S1_C3T else []}
    if sidecar['successor_validate_spec_block'] != 'PASS':
        blockers.append('the wrapper successor refuses this spec: %s' % sidecar['successor_validate_spec_block'])
    if dry or blockers:
        return {'plan': plan, 'sidecar': sidecar, 'written': None}
    require(isinstance(out_path, str), 'OUT_PATH_REQUIRED')
    raw = (json.dumps(plan, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    w = write_exclusive(out_path, raw)
    sidecar['plan'] = w
    ws = write_exclusive(out_path + '.s1.json', record_bytes(sidecar))
    return {'plan': plan, 'sidecar': sidecar, 'written': {'plan': w, 'sidecar': ws}}


# ================================================================================================ part 2: the root launch path
CONTROL_C1 = ('SEALED_ROOT_BINDING', 'SEALED_R5_BINDING', 'SEALED_ADOPT_TAIL_REQUIRED', 'VERDICT_BYTE_BINDING',
              'PREREG_CASE_BLOCK_REQUIRED', 'REVIEWED_SEAL_TUPLE_PENDING', 'C1_ADOPTION_BINDING',
              'ADOPTED_WORKER_COUNT_REQUIRED')
CONTROL_C4 = ('EXACT_R5_OR_DIII_REFERENCE_DRIVER_REQUIRED', 'TAIL_ON_R5_REQUIRED', 'REFERENCE_DRIVER_SCOPE',
              'S1_DRIVER_NOT_R5', 'S1_TAIL_ON_REQUIRED')
CONTROL_C3 = ('NATIVE_GATE_REFUSED', 'PRELAUNCH_REPLAY_MISMATCH', 'CERTIFICATE_PRODUCERS_REQUIRED',
              'DIRECT_CONTEXT_API_REQUIRED', 'TAIL_ON_SPEC_REQUIRED', 'FRESH_DDO154_SPEC_REQUIRED',
              'PREFLIGHT_PROCESS_OR_NETWORK_REFUSED', 'PREFLIGHT_WRITE_REFUSED', 'PREFLIGHT_COMPILE_HASH_MISMATCH',
              'UNPINNED_PREFLIGHT_SOURCE', 'PREFLIGHT_SOURCE_BUFFER_REQUIRED')
CONTROLS = ('C1_SEALED_V007_ADOPT_TAIL', 'C2_STEP4_ADMISSION', 'C3_PRELAUNCH_CERTIFICATE_SENSITIVITY', 'C4_R5_ALLOWLIST')


def load_guard(ref=None):
    ref = ref or const_pin('GUARD')
    raw = verify_pin(ref, 'GUARD')
    G = types.ModuleType('_s1_step4_guard')
    G.__file__ = ref['path']
    exec(compile(raw, ref['path'], 'exec'), G.__dict__)
    return G


def load_gate():
    return load_source_module(const_pin('GATE'), '_s1_machine_gate_v003', 'GATE')


def _code(exc):
    c = getattr(exc, 'code', None)
    if isinstance(c, str):
        return c
    s = str(exc.args[0]) if getattr(exc, 'args', None) else type(exc).__name__
    return s


def _control_for(code, default):
    if code in CONTROL_C1:
        return CONTROLS[0]
    if code in CONTROL_C4:
        return CONTROLS[3]
    if code in CONTROL_C3:
        return CONTROLS[2]
    return default


def v6_entry_lines(v6_bytes, prefix):
    """The lines of the pinned V006 bytes that begin (after leading spaces and one list marker) with root's prefix."""
    out = []
    for ln in v6_bytes.decode('utf-8', 'strict').splitlines():
        s = re.sub(r'^\s*(?:[-*]\s+|\d+\.\s+)?', '', ln)
        if s.startswith(prefix):
            out.append(s)
    return out


def v6_entry_names_sha(v6_bytes, prefix, sha):
    """True iff some root entry line with this prefix carries the full 64-hex sha (as a whole token)."""
    pat = re.compile(r'(?<![0-9a-f])%s(?![0-9a-f])' % re.escape(sha))
    return any(pat.search(ln) for ln in v6_entry_lines(v6_bytes, prefix))


def pinned_v6(v6_ref):
    """Note 1: V006 is read only at its constant root path, by the pin root supplies (V006 is an open file)."""
    require(is_pin(v6_ref) and v6_ref['path'] == V6_PATH, 'V6_PATH_NOT_THE_ROOT_FILE',
            None if not isinstance(v6_ref, dict) else v6_ref.get('path'))
    return verify_pin(v6_ref, 'V006')


def registration_in_force(registration_ref, v6_ref):
    """Note 1: the registration is the one this library implements (constant path and sha), and root's V006 entry line
    '**Registration in force:** ... sha256 `<sha>`' names it. A mention anywhere else (a rejection note) does not count."""
    require(is_pin(registration_ref) and registration_ref == const_pin('REGISTRATION'), 'S1_REGISTRATION_NOT_IMPLEMENTED_HERE',
            None if not isinstance(registration_ref, dict) else registration_ref.get('sha256'))
    verify_pin(registration_ref, 'S1_REGISTRATION')
    v6 = pinned_v6(v6_ref)
    require(v6_entry_names_sha(v6, REGISTRATION_ENTRY_PREFIX, REGISTRATION_SHA), 'S1_REGISTRATION_NOT_IN_FORCE')
    return True


def _memory_free_percent():
    """launcher012 memory_free (L29-34): /usr/bin/memory_pressure 'System-wide memory free percentage', else None."""
    import subprocess
    try:
        s = subprocess.check_output(['/usr/bin/memory_pressure'], text=True, stderr=subprocess.STDOUT, timeout=10)
        m = re.findall(r'^System-wide memory free percentage:\s*(\d+)%\s*$', s, re.M)
        return int(m[0]) if len(m) == 1 and 0 <= int(m[0]) <= 100 else None
    except Exception:                                                    # noqa: BLE001 -- unknown reads as None (refuse)
        return None


def snapshot_r5_route_a(M, snap, own_outdir):
    """Note 2: the run trees of the decide snapshot that may be campaign / step-2 calls: driver r5 or an unparsed
    driver (fail closed), not this call's outdir, in route A by the gate's own phase rule (route_a_done_path)."""
    view, _ = M.runs_view(snap, {})
    phase = {r['key']: r['phase'] for r in view}
    return [{'monitor_pid': r.get('monitor_pid'), 'outdir': r.get('outdir'), 'driver_sha256': r.get('driver_sha256'),
             'footprint_gb': r.get('footprint_gb')}
            for r in (snap.get('runs') or [])
            if r.get('outdir') != own_outdir and r.get('driver_sha256') in (R5_SHA, None)
            and phase.get(r.get('monitor_pid')) == 'route_a']


def launch(plan_ref, admission_ref, registration_ref, v6_ref, launch_cfg_ref, *, mode='dry', confirm=None, guard=None,
           gate=None, spawn=None, sleep=None, record_path=None, disk_batch=True, env=None, memory_free=None):
    """Root launch path. Order: S1 checks -> the four 0620 controls (guard012, no process; for an overlap admission
    guard012 also runs its live gate) -> machine gate predicates (read-only probes), the r5 route-A snapshot check,
    A133's root memory rule and memory_pressure -> exclusive pre-launch record -> launcher013 (launch mode only) ->
    exclusive outcome record. Returns the decision record; never raises (a refusal or an internal error is recorded)."""
    out = {'schema': SCHEMA_LAUNCH_RECORD, 'module': MODULE, 'module_sha256': module_sha256(), 'mode': mode,
           'plan': plan_ref, 'admission': admission_ref, 'evaluated': 'AT_HAND_OFF (the launcher worker waits for its own '
           'memory ramp; guard012 re-runs the overlap gate at every pre-start validation)',
           'trace': [], 'controls': {c: 'NOT_EVALUATED' for c in CONTROLS}, 'gate': None, 'decision': None, 'refusal': None}
    stage = 'S1_CHECKS'
    try:
        require(mode in ('dry', 'launch'), 'MODE')
        # ---- S1 checks (no process)
        out['trace'].append('s1_checks')
        if mode == 'launch':                       # launch-mode arguments are checked before anything else runs
            injected = [n for n, v in (('guard', guard), ('gate', gate), ('memory_free', memory_free)) if v is not None]
            require(not injected, 'LAUNCH_MODE_INJECTION_REFUSED', injected)                       # note 7
            require(isinstance(plan_ref, dict) and confirm == plan_ref.get('sha256'), 'LAUNCH_CONFIRMATION_REQUIRED')
            e = dict(env if env is not None else os.environ)
            require(isinstance(admission_ref, dict) and e.get('UNT_STEP4_ADMISSION_PATH') == admission_ref.get('path')
                    and e.get('UNT_STEP4_ADMISSION_SHA256') == admission_ref.get('sha256'), 'PUBLISHED_ADMISSION_ENV_MISMATCH')
            require(isinstance(record_path, str), 'PRELAUNCH_RECORD_PATH_REQUIRED')
        registration_in_force(registration_ref, v6_ref)
        lcfg = pinned_json(launch_cfg_ref, 'LAUNCH_CONFIG')
        require(lcfg.get('schema') == SCHEMA_LAUNCH_CFG, 'LAUNCH_CONFIG_SCHEMA')
        require(lcfg.get('campaign_state') in ('INACTIVE', 'ACTIVE'), 'LAUNCH_CONFIG_CAMPAIGN_STATE')
        require(lcfg.get('step2_route_a_state') == 'INACTIVE', 'STEP2_ROUTE_A_NOT_INACTIVE')
        overlap = lcfg['campaign_state'] == 'ACTIVE'
        if overlap:                                # registration section 11 rule 4 (C14): root's window attestation
            require(lcfg.get('campaign_window') in CAMPAIGN_WINDOWS, 'S1_OVERLAP_CAMPAIGN_WINDOW_REQUIRED')
        else:
            require('campaign_window' not in lcfg, 'S1_CAMPAIGN_WINDOW_ONLY_WITH_OVERLAP')
        plan_raw = verify_pin(plan_ref, 'PLAN')
        plan = strict_json(plan_raw)
        require(isinstance(plan, dict) and plan.get('schema') == SCHEMA_PLAN, 'PLAN_SCHEMA')
        require(plan.get('batch') == 'POST_S1', 'S1_BATCH_NOT_POST_S1')
        require(plan.get('guard') == const_pin('GUARD') and plan.get('launcher') == const_pin('LAUNCHER'),
                'S1_PACKET_NOT_GUARD012_LAUNCHER013')
        calls = plan.get('calls')
        require(isinstance(calls, list) and len(calls) == 1, 'S1_ONE_CALL_PER_BATCH')
        call = calls[0]
        case = call.get('case')
        require(case in S1_CASES, 'S1_CASE_UNKNOWN', case)
        require(call.get('driver') == const_pin('DRIVER'), 'S1_DRIVER_NOT_R5')
        require(call.get('tail_on') is True, 'S1_TAIL_ON_REQUIRED')
        s1 = plan.get('s1') or {}
        fill_rec = pinned_json(s1.get('fill_record'), 'FILL_RECORD')
        require(fill_rec.get('schema') == SCHEMA_FILL and fill_rec.get('dry') is False, 'FILL_RECORD_NOT_WRITTEN_FILL')
        require(call.get('spec') == fill_rec['cases'][case]['spec'], 'S1_SPEC_NOT_FILLED_SPEC')
        spec_raw = verify_pin(call['spec'], 'S1_SPEC')
        replay, st = replay_specs(fill_rec)
        require(replay[case] == spec_raw, 'S1_TEMPLATE_REPLAY_MISMATCH')
        spec = strict_json(spec_raw)
        require(spec['numerics']['composite_grid_spec']['breaks_inverse_kpc'][-1] == CASE_K[case]
                and canonical(spec['numerics']['composite_grid_spec'])
                == canonical(cb_numerics(st, CASE_CB[case])['composite_grid_spec']), 'S1_CASE_K_MISMATCH')
        out.update(case=case, theta_key=fill_rec['theta_key'], branch=fill_rec['branch']['branch'],
                   campaign_state=lcfg['campaign_state'], campaign_window=lcfg.get('campaign_window'))
        # ---- the four 0620 controls (guard012; no process; the fence refuses process creation)
        stage = 'CONTROLS'
        G = guard if guard is not None else load_guard()
        out['trace'].append('control_C2_admission_load')
        if admission_ref is None:
            raise Refusal('PUBLISHED_STEP4_ADMISSION_PENDING')
        try:
            cfg = G.doc(admission_ref)
        except Exception as exc:
            out['controls'][CONTROLS[1]] = 'REFUSED:' + _code(exc)
            raise Refusal(_code(exc))
        want_cp = CORE_PRIORITY_S1_OVERLAP if overlap else CORE_PRIORITY
        if cfg.get('core_priority') != want_cp:
            out['controls'][CONTROLS[1]] = 'REFUSED:S1_ADMISSION_CORE_PRIORITY_NOT_THE_LAUNCH_CONFIG_STATE'
            raise Refusal('S1_ADMISSION_CORE_PRIORITY_NOT_THE_LAUNCH_CONFIG_STATE')
        if overlap and cfg.get('s1_overlap') != {'schema': S1_OVERLAP_SCHEMA, 'replay_module': self_pin(),
                                                 'fill_record': s1.get('fill_record')}:
            out['controls'][CONTROLS[1]] = 'REFUSED:S1_OVERLAP_ADMISSION_NOT_THIS_PATH'
            raise Refusal('S1_OVERLAP_ADMISSION_NOT_THIS_PATH', 'the replay module must be this library, the fill record the plan\'s')
        out['trace'].append('control_C4')
        try:
            G.spec_structure(call, spec)
            require(call['driver']['sha256'] == G.R5_SHA, 'EXACT_R5_OR_DIII_REFERENCE_DRIVER_REQUIRED')
            G.admitted_source(call['driver'], cfg)
        except Exception as exc:
            c = _code(exc)
            out['controls'][_control_for(c, CONTROLS[3])] = 'REFUSED:' + c
            raise Refusal(c)
        out['controls'][CONTROLS[3]] = 'PASS'
        out['trace'].append('control_C1')
        try:
            with G.fence(cfg['sources']):
                C = G.load(cfg['context_module'], cfg, '_step4_context')
                G.adoption(cfg, C)
        except Exception as exc:
            c = _code(exc)
            out['controls'][_control_for(c, CONTROLS[0])] = 'REFUSED:' + c
            raise Refusal(c)
        out['controls'][CONTROLS[0]] = 'PASS'
        out['trace'].append('control_C2_C3_validate')
        G3 = load_gate()
        M = gate if gate is not None else G3.Gate()
        gkw = {'_overlap_gate': M, '_overlap_sleep': sleep} if (mode == 'dry' and gate is not None) else {}
        try:
            G.validate(plan_ref, PINS['LAUNCHER'][0], check_outputs=True, execute_native=True, config_ref=admission_ref,
                       disk_batch=disk_batch, **gkw)
        except Exception as exc:
            c = _code(exc)
            if c.startswith('S1_OVERLAP_GATE') or c.startswith('S1_OVERLAP_R5') or c.startswith('S1_OVERLAP_A133'):
                out['controls'][CONTROLS[1]] = 'PASS'
                out['controls'][CONTROLS[2]] = 'PASS'
                stage = 'GUARD012_OVERLAP_GATE'
                raise Refusal(c)
            ctl = _control_for(c, CONTROLS[1] if isinstance(exc, G.Refusal) else CONTROLS[2])
            out['controls'][ctl] = 'REFUSED:' + c
            if ctl == CONTROLS[2]:
                out['controls'][CONTROLS[1]] = 'NOT_COMPLETED: validate stopped at native preflight (admission checks before it passed)'
            raise Refusal(c)
        out['controls'][CONTROLS[1]] = 'PASS'
        out['controls'][CONTROLS[2]] = 'PASS'
        if overlap:
            out['trace'].append('guard012_overlap_gate')
        # ---- machine gate v003 predicates (read-only probes), the r5 snapshot check, A133's rule, memory_pressure
        stage = 'GATE'
        out['trace'].append('gate_hold_check')
        h = M.hold_check()
        out['gate'] = {'hold_check': {k: h.get(k) for k in ('hold', 'twins', 'probe_ok', 'probe_reasons')}}
        require(h.get('probe_ok') is True, 'GATE_PROBE_FAILED', h.get('probe_reasons'))
        require(h.get('hold') is False, 'GATE_TWIN_HOLD', h.get('twins'))
        out['trace'].append('gate_decide')
        M.sample(force=True)
        (sleep or __import__('time').sleep)(M.P['warmup_s'])
        head = dict(G3.class_from_spec_bytes(spec_raw), name='S1_HEAD_' + case)
        d = M.decide(owned={}, head=head, n_running=0, max_concurrent=1)
        out['gate']['decide'] = {k: d.get(k) for k in ('admit', 'reasons', 'mem_after_admit_gb', 'mem_knee_after_admit_gb',
                                                         'hard_gb', 'knee_gb', 'cores_after_admit', 'pooled_route_a_now',
                                                         'head', 'head_family')}
        require(d.get('admit') is True, 'GATE_REFUSED', d.get('reasons'))
        snap = getattr(M, 'last', None) or {}
        r5 = snapshot_r5_route_a(M, snap, call.get('outdir'))
        out['gate']['r5_route_a_trees'] = r5
        if overlap:                                # guard012's allowance, re-checked here on the lib's own snapshot
            require(len(r5) <= int(M.P['route_a_cap']) - 1, 'S1_OVERLAP_R5_ROUTE_A_BEYOND_GATE_ALLOWANCE', len(r5))
        else:                                      # note 2: the INACTIVE attestation is checked against the machine
            require(not r5, 'S1_CAMPAIGN_ROUTE_A_TREE_WHILE_ATTESTED_INACTIVE', [x['outdir'] for x in r5][:5])
        fp = [r.get('footprint_gb') for r in (snap.get('runs') or [])]
        known = [x for x in fp if type(x) in (int, float) and math.isfinite(x)]
        a133 = {'run_footprint_gb': round(sum(known), 3), 's1_term_gb': A133_S1_TERM_GB,
                'campaign_reserve_gb': A133_CAMPAIGN_RESERVE_GB, 'limit_gb': A133_LIMIT_GB,
                'sum_gb': round(sum(known) + A133_S1_TERM_GB + A133_CAMPAIGN_RESERVE_GB, 3),
                'footprint_unknown_runs': len(fp) - len(known)}
        out['gate']['a133_rule'] = a133
        require(a133['footprint_unknown_runs'] == 0, 'A133_FOOTPRINT_UNKNOWN')
        require(a133['sum_gb'] <= A133_LIMIT_GB, 'A133_MEMORY_RULE', a133['sum_gb'])
        free = (memory_free or _memory_free_percent)()                                             # note 4
        out['gate']['memory_pressure_free_percent'] = free
        require(type(free) is int and MEMORY_FREE_MIN_PERCENT <= free <= 100, 'MEMORY_PRESSURE_FREE_BELOW_25', free)
        # ---- record, then launcher013, then the outcome record
        stage = 'LAUNCH'
        argv = ['/usr/bin/env'] + ['%s=%s' % kv for kv in sorted(BLAS.items())] + \
               ['/usr/bin/nice', '-n', '10', PYTHON, '-I', '-B', PINS['LAUNCHER'][0], plan_ref['path'], '--execute-root-only']
        out['launch_argv'] = argv
        out['decision'] = 'ADMITTED' if mode == 'dry' else 'LAUNCHING'
        if record_path is not None:
            out['trace'].append('record')
            out['record'] = write_exclusive(record_path, record_bytes(out))
        if mode == 'launch':
            launch_after_record(out, argv, {**e, **BLAS}, spawn, record_path)
        return out
    except Refusal as exc:
        out['decision'] = 'REFUSED'
        out['refusal'] = {'stage': stage, 'code': exc.code, 'detail': None if exc.detail is None else str(exc.detail)[:500]}
    except Exception as exc:                                                                       # note 6
        out['decision'] = 'REFUSED'
        out['refusal'] = {'stage': stage, 'code': 'INTERNAL_ERROR', 'detail': ('%s: %s' % (type(exc).__name__, exc))[:500]}
    if record_path is not None and 'record' not in out:
        try:
            out['record'] = write_exclusive(record_path, record_bytes(out))
        except Exception as wexc:                                       # noqa: BLE001 -- reported, never retried
            out['record_error'] = type(wexc).__name__
    return out


def launch_after_record(out, argv, env, spawn, record_path):
    """Note 5: the spawn is wrapped; its outcome (or the exception) is written to <record>.outcome.json by exclusive
    create in every case, after the LAUNCHING record. Never raises."""
    out['trace'].append('spawn')
    try:
        res = (spawn or _spawn)(argv, env)
        out['launcher_result'] = res
        out['decision'] = 'LAUNCHED' if isinstance(res, dict) and res.get('returncode') == 0 else 'LAUNCHER_REFUSED'
    except Exception as exc:                                             # noqa: BLE001 -- recorded, never retried
        out['launcher_result'] = {'exception': ('%s: %s' % (type(exc).__name__, exc))[:1000]}
        out['decision'] = 'SPAWN_FAILED'
    oc = {'schema': SCHEMA_LAUNCH_OUTCOME, 'module': MODULE, 'record': out.get('record'), 'decision': out['decision'],
          'launcher_result': out['launcher_result'], 'plan': out.get('plan'), 'case': out.get('case')}
    try:
        out['outcome_record'] = write_exclusive(record_path + '.outcome.json', record_bytes(oc))
    except Exception as wexc:                                            # noqa: BLE001
        out['outcome_record_error'] = type(wexc).__name__
    return out


def _spawn(argv, env):
    import subprocess
    r = subprocess.run(argv, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
    return {'returncode': r.returncode, 'stdout': r.stdout[-4000:], 'stderr': r.stderr[-4000:]}


# ================================================================================================ part 3: the reader
REUSED_COMPARE_FUNCTIONS = ('read_run', 'pass_rows_ids_code', 'pass_rows_gap', '_pass_rows', 'picard_noise_detail',
                            'route_a_noise', 'pair_noise', 'rpair_branch_row', 'row_stat', 'thresholded',
                            'check_uvt_record', 'rows_codes', 'v2_check', 'classify_failure', 'registered_row_radii',
                            'radii_equal', 'ra4_block_expected', 'check_ro1_record', 'registered_source_rule_is_nodes')
REUSED_V005_FUNCTIONS = ('adapt_result', 'expected_axis', 'driver_mask', 'packet_checks')
STEP5_HELD = 'step-5 values stay unread (validity-only), both phases'
NEXT = {
    'MONITOR_STOP': '(i) the identical spec in a fresh outdir with the cap raised (registration section 10)',
    'BRACKET_HULL_MISS': '(ii) BRACKET_HULL_MISS: its own registration; no D7 or W1 widening (R6 L1084; R11 RA4_NEXT L491)',
    'NAMED_DEFECT': '(iii) fix and rerun that case under V007 with thresholds unchanged (R11 AMB16_NEXT L493)',
    'OTHER_FAILED': '(iv) one identical rerun; a second identical failure is reported as a deterministic defect for review',
    'FLAG_PENDING_RULING': ('no adoption; root rules on the flag (R11 L488; R6 L1796); a root ruling record entered in V6 '
                            '("**S1 flag ruling:**") is a reader input (note 13), then read again'),
    'UNDECIDABLE_FLAGGED': 'rerun that case with seed source_rtol/10 (R6 L1777)',
    'INCOMPLETE_RECORD': ('produce the missing record, then read again (R11 NO_RUN next step L472); E^A comes only from the '
                          'route-A uv_tail record with probe_R_m equal to the registered radii (B3)'),
    'RPAIR': 'R-PAIR once (R6 L1243) through a launch-path successor; still undecidable -> UNDECIDABLE_AT_ITERATION_FLOOR '
             '(reads stay held)',
    'S1_DIAG': 'S1-DIAG: C2T and C6T at the u_A theta bits under a successor registration; V007 T1 and T1_H read literally',
    'NOT_RUN': 'build/name the launch path, then launch when admitted; Phase-1 scoring waits (A133 L188)',
    'SV7_ACCEPTANCE': ('the call\'s A134 Q5 failure reading governs (NON_LAPSE_TAIL_MATERIAL, LO_UNCERTIFIED_TRANSIENT or '
                       'INCOMPLETE; V6 L498, L527); root rules before any S1 rerun'),
}


def compare_closure_digest(raw, names):
    """Informational: sha256 over the AST dumps of every top-level definition reachable by name from the reused functions."""
    tree = ast.parse(raw)
    defs = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defs[node.name] = node
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    defs[t.id] = node
    seen, todo = set(), list(names)
    while todo:
        x = todo.pop()
        if x in seen or x not in defs:
            continue
        seen.add(x)
        todo += [n.id for n in ast.walk(defs[x]) if isinstance(n, ast.Name) and n.id in defs and n.id not in seen]
    h = hashlib.sha256()
    for x in sorted(seen):
        h.update(x.encode() + b'\0' + ast.dump(defs[x], include_attributes=False).encode() + b'\0')
    return {'n_definitions': len(seen), 'sha256': h.hexdigest()}


def reviewed_compare(ref):
    """B1: only a reviewed compare file executes: its sha must be a REVIEWED_COMPARES key at the reviewed path, and the
    AST digest of every reused function must equal the reviewed digest. Returns the verified bytes."""
    require(is_pin(ref), 'COMPARE_PIN_REQUIRED')
    rev = REVIEWED_COMPARES.get(ref['sha256'])
    require(isinstance(rev, dict) and rev.get('path') == ref['path'], 'COMPARE_NOT_REVIEWED', ref['sha256'][:16])
    raw = verify_pin(ref, 'COMPARE')
    require(function_digests(raw, REUSED_COMPARE_FUNCTIONS) == rev['functions'], 'COMPARE_FUNCTION_DIGESTS_NOT_REVIEWED')
    return raw


def load_compare(ref):
    reviewed_compare(ref)
    m = load_source_module(ref, '_s1_compare_of_record', 'COMPARE')
    missing = [f for f in REUSED_COMPARE_FUNCTIONS if not callable(getattr(m, f, None))]
    require(not missing, 'COMPARE_FUNCTIONS_MISSING', missing)
    return m


def reader_context(st, R, V5):
    return {'ids': st['ids'], 'tau': st['tau'], 'sigma': st['sigma'], 'tau_picard': st['tau_picard'], 'C5M': V5,
            'ra4_block': R.ra4_block_expected()}


def _receipt(path):
    guard_path(str(path))
    try:
        raw = read_bytes(path)
    except Refusal as exc:
        if exc.code == 'FILE_MISSING':
            return None, 'MISSING'
        return None, 'RECEIPT_UNREADABLE:%s' % exc.code
    try:
        d = strict_json(raw)
    except Refusal as exc:
        return None, 'RECEIPT_UNREADABLE:%s' % exc.code
    return (d, None) if isinstance(d, dict) else (None, 'RECEIPT_NOT_AN_OBJECT')


def prescan_result_side_paths(result_dir):
    """Note 11: every path read_run (and V005 adapt_result) would open from inside a result record is guarded first:
    route_a_outcome.result_path, stage_records[].stage_dir, passes[].field / .rotation, and each field folder's
    finish.json output pins. A protected path refuses the reading (nothing is written). An unparseable result is left
    to read_run, which then opens no side path."""
    guard_path(str(result_dir))
    rp = Path(result_dir) / 'result.json'
    guard_path(str(rp))
    try:
        r = strict_json(read_bytes(str(rp)))
    except Refusal:
        return []
    if not isinstance(r, dict):
        return []
    rao = r.get('route_a_outcome') if isinstance(r.get('route_a_outcome'), dict) else {}
    side = [rao.get('result_path')]
    side += [x.get('stage_dir') for x in (r.get('stage_records') or []) if isinstance(x, dict)]
    fields = [x.get('field') for x in (r.get('passes') or []) if isinstance(x, dict)]
    side += fields + [x.get('rotation') for x in (r.get('passes') or []) if isinstance(x, dict)]
    side = [p for p in side if isinstance(p, str)]
    for p in side:
        guard_path(p) if os.path.isabs(p) else guard_path(str(Path(result_dir) / p))
    for f in fields:
        if not isinstance(f, str) or not os.path.isabs(f):
            continue
        fj = str(Path(f) / 'finish.json')
        guard_path(fj)
        try:
            fin = strict_json(read_bytes(fj))
        except Refusal:
            continue
        for v in ((fin.get('outputs') or {}).values() if isinstance(fin, dict) and isinstance(fin.get('outputs'), dict) else []):
            if isinstance(v, dict) and isinstance(v.get('path'), str) and os.path.isabs(v['path']):
                guard_path(v['path'])
    return side


def _attestation(ref, case, result_sha, gate, v6):
    """Note 9: the producer's sha must be on a root V6 entry line ('**S1 attestation producer (SV7):**')."""
    d = pinned_json(ref, 'ATTEST_' + gate)
    require(d.get('schema') == SCHEMA_ATTEST and d.get('gate') == gate and d.get('run') == case
            and d.get('result_sha256') == result_sha, 'ATTESTATION_BINDING', '%s %s' % (case, gate))
    for k in ('producer', 'evidence'):
        verify_pin(d.get(k), 'ATTEST_%s_%s' % (gate, k.upper()))
    require(v6_entry_names_sha(v6, ATTESTATION_PRODUCER_ENTRY_PREFIX, d['producer']['sha256']),
            'ATTESTATION_PRODUCER_NOT_ALLOWLISTED', '%s %s' % (case, gate))
    require(d.get('status') in ('PASS', 'FAIL'), 'ATTESTATION_STATUS')
    return d['status']


def ro1_codes(run, reg, R):
    """Note 8: RO1 computed by the reviewed compare (check_ro1_record on route_a_outcome, the CB case's custody list),
    with the compare's worker-kind rule (R11 validity: column_workers 1 -> serial worker, > 1 -> parallel)."""
    rao = run.get('route_a_outcome') if isinstance(run.get('route_a_outcome'), dict) else {}
    if not reg.get('ro1_required'):
        return ['RO1_NOT_REQUIRED_BY_CB_CASE'], {}
    nodes = R.registered_source_rule_is_nodes(reg)
    c, info = R.check_ro1_record(rao, nodes=nodes)
    codes = list(c)
    ns = (run.get('result') or {}).get('normalized_spec') or {}
    cw = ((ns.get('numerics') or {}).get('route_a') or {}).get('column_workers')
    if info.get('worker_kind'):
        if type(cw) is int and cw >= 1:
            if info['worker_kind'] != ('serial' if cw == 1 else 'parallel'):
                codes.append('RO1_WORKER_IS_NOT_THE_%s_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS'
                             % ('serial' if cw == 1 else 'parallel').upper())
        else:
            codes.append('RO1_KIND_CHECK_COLUMN_WORKERS_NOT_A_POSITIVE_INT_A77_2')
    return codes, {'custody_list': 'NODES' if nodes else 'CONTINUUM', 'armed': info.get('armed'),
                   'fired': info.get('fired'), 'worker_kind': info.get('worker_kind')}


def run_gates(case, run, receipt, mrun, fill_rec, st, R, V5, ctx, radii, v6):
    """SV0-SV8 and RO1 for one run. Returns (codes, failure_class, info)."""
    codes, info = [], {'flagged': False, 'uvt_info': None}
    res = run.get('result') or {}
    if run.get('unreadable'):
        return ['RESULT_UNREADABLE:%s' % run['unreadable']], 'NAMED_DEFECT', info
    codes += ['READ:%s' % c for c in run.get('read_codes') or []]
    # SV0
    if res.get('driver_sha256') != R5_SHA:
        codes.append('SV0_DRIVER_NOT_R5')
    want_spec = fill_rec['cases'][case]['spec']['sha256'] if case in S1_CASES else fill_rec['base_spec']['sha256']
    if res.get('call_spec_sha256') != want_spec:
        codes.append('SV0_CALL_SPEC_SHA_NOT_REGISTERED')
    if receipt.get('status') != 'FINISHED':
        codes.append('SV0_RECEIPT_NOT_FINISHED:%s' % receipt.get('status'))
    # failure classification (V005 V1 next steps as amended for the tail era)
    if run.get('failure'):
        f = run['failure']
        cls = f.get('class') or ''
        codes += ['SV1_%s' % c for c in f.get('codes') or [cls]]
        if cls in ('BRACKET_HULL_MISS', 'BRACKET_MISS_OFF_RA4_BLOCK'):
            return codes, 'BRACKET_HULL_MISS', info
        if cls == 'MONITOR_STOP':
            return codes, 'MONITOR_STOP', info
        return codes, 'OTHER_FAILED', info
    # SV1
    codes += ['SV1_%s' % c for c in R.rows_codes(run, st['ids'])]
    if run.get('pass_rows_s9'):
        codes.append('SV1_RECORD_DEFECT_S9:%s' % run['pass_rows_s9'])
    # SV2
    ok2, c2 = R.v2_check(run, ctx)
    if not ok2:
        codes.append('SV2_FINAL_PASS_CHANGE_ABOVE_TAU_PICARD')
    codes += ['SV2_%s' % c for c in c2]
    # SV3: spec content against the registration (CB numerics, u_A physical bits, galaxy, coefficients)
    ns = res.get('normalized_spec') or {}
    num = ns.get('numerics') or {}
    if canonical(strip_certs(num)) != canonical(strip_certs(cb_numerics(st, CASE_CB[case]))):
        codes.append('SV3_NUMERICS_NOT_CB_%s' % CASE_CB[case])
    if (num.get('composite_grid_spec') or {}).get('breaks_inverse_kpc', [None])[-1] != CASE_K[case]:
        codes.append('SV3_K_NOT_%d' % CASE_K[case])
    phys = ns.get('physical') or {}
    for leaf, v in fill_rec['physical_u_A'].items():
        if not (type(phys.get(leaf)) is float and fhex(phys[leaf]) == v['hex']):
            codes.append('SV3_PHYSICAL_NOT_U_A_BITS:%s' % leaf)
    if ns.get('galaxy') != 'DDO154':
        codes.append('SV3_GALAXY')
    if case in S1_CASES:
        spec_doc = strict_json(verify_pin(fill_rec['cases'][case]['spec'], 'S1_SPEC'))
    else:
        spec_doc = strict_json(verify_pin(fill_rec['base_spec'], 'BASE_SPEC'))
    if canonical(ns.get('coefficients')) != canonical(spec_doc.get('coefficients')):
        codes.append('SV3_COEFFICIENTS')
    for slot in CERT_SLOTS:
        if canonical((num.get('uv_tail') or {}).get(slot)) != canonical(spec_doc['numerics']['uv_tail'].get(slot)):
            codes.append('SV3_CERTIFICATE_SLOT:%s' % slot)
    # SV4 / SV5 (V005 packet_checks, pinned)
    try:
        chk, _ = V5.packet_checks(run['adapted'], {'shape': 'cube', 'kmax_inverse_kpc': None},
                                  cb_numerics(st, CASE_CB[case])['composite_grid_spec'], None, False)
        if not chk.get('V4'):
            codes.append('SV4_PACKET_AXIS')
        if not chk.get('V5'):
            codes.append('SV5_PACKET_MASK')
        info['packet'] = {k: chk.get(k) for k in ('V4', 'V5', 'nodes', 'axis_nodes_expected', 'packet_sha256', 'reason')}
    except Exception as exc:                                             # noqa: BLE001 -- a record problem, never a number
        codes.append('SV4_PACKET_UNREADABLE:%s' % type(exc).__name__)
    # SV6: nothing admitted
    if ns.get('admit', {}) != {}:
        codes.append('SV6_ADMITTED_STATE')
    # SV8 and the route-A tail record (E^A, flags); tail content S8 via the config sha
    reg = st['cb']['cases'][CASE_CB[case]]
    if run.get('uvt_record') is None:
        codes.append('SV8_UVT_RECORD:%s' % run.get('uvt_code'))
    else:
        uc, uinfo = R.check_uvt_record(run['uvt_record'], reg, 'uvt:%s' % case, radii)
        codes += ['SV8_%s' % c for c in uc]
        info['uvt_info'] = uinfo
        info['flagged'] = bool(uinfo.get('flagged'))
        info['flags'] = sorted(str(x) for x in (run['uvt_record'].get('flags') or []))
    # RO1 (note 8: computed)
    rc, rinfo = ro1_codes(run, reg, R)
    codes += rc
    info['ro1'] = rinfo
    # attested gate SV7 (tail-era acceptance), producer allowlisted in V6 (note 9)
    for g in ATTESTED_GATES:
        ref = (mrun.get('attestations') or {}).get(g)
        require(ref is not None, 'S1_INPUT_INCOMPLETE', 'attestation %s for %s' % (g, case))
        if _attestation(ref, case, run.get('result_sha256'), g, v6) != 'PASS':
            codes.append('%s_FAIL' % g)
    if any(c.startswith('SV7_') for c in codes):
        return codes, 'SV7_ACCEPTANCE', info
    return codes, ('NAMED_DEFECT' if codes else None), info


def flag_ruling(ref, case, run, flags, v6):
    """Note 13: a root flag ruling for one run: schema, run, result sha and the exact flag list bind; ruling
    FLAG_CLEARED_FOR_S1; the record's sha is on a V6 entry line ('**S1 flag ruling:**'). Returns True when cleared."""
    d = pinned_json(ref, 'FLAG_RULING')
    require(d.get('schema') == SCHEMA_FLAG_RULING and d.get('run') == case and d.get('result_sha256') == run.get('result_sha256')
            and sorted(str(x) for x in (d.get('flags') or [])) == flags and d.get('registration_sha256') == REGISTRATION_SHA,
            'FLAG_RULING_BINDING', case)
    require(v6_entry_names_sha(v6, FLAG_RULING_ENTRY_PREFIX, ref['sha256']), 'FLAG_RULING_NOT_ENTERED_IN_V6', case)
    require(d.get('ruling') in (FLAG_CLEARED, 'FLAG_UPHELD'), 'FLAG_RULING_VALUE', case)
    return d['ruling'] == FLAG_CLEARED


def read_reading(manifest_ref, write_dir=None):
    """The S1 reading of record (registration sections 5-8). Target-free: DDO154 model speeds only."""
    man = pinned_json(manifest_ref, 'MANIFEST')
    require(man.get('schema') == SCHEMA_MANIFEST, 'MANIFEST_SCHEMA')
    require('ea_record' not in man, 'MANIFEST_EA_RECORD_NOT_ACCEPTED')            # B3: no EA fallback
    registration_in_force(man.get('registration'), man.get('v6'))
    v6 = pinned_v6(man['v6'])
    out = {'schema': SCHEMA_READING, 'module': MODULE, 'module_sha256': module_sha256(), 'manifest': manifest_ref,
           'registration': man['registration'],
           'v6': man['v6'], 'target_free': 'DDO154 model speeds only; no NGC3198 file is read'}
    if man.get('u_A_status') is not None:
        require(isinstance(man['u_A_status'], str) and man['u_A_status'].startswith('NO_U_A'), 'U_A_STATUS')
        return _finish(out, 'NOT_RUN', man['u_A_status'], None, write_dir)
    fill_rec = pinned_json(man.get('fill_record'), 'FILL_RECORD')
    require(fill_rec.get('schema') == SCHEMA_FILL and fill_rec.get('dry') is False, 'FILL_RECORD_NOT_WRITTEN_FILL')
    branch = fill_rec['branch']['branch']
    out.update(fill_record=man['fill_record'], theta_key=fill_rec['theta_key'], branch=fill_rec['branch'],
               specs={c: fill_rec['cases'][c]['spec'] for c in S1_CASES}, k4_prime_spec=fill_rec['base_spec'])
    st = load_static()
    cref = man.get('compare') or const_pin('COMPARE_R14')
    R = load_compare(cref)
    V5 = load_source_module(const_pin('COMPARE_V005'), '_s1_compare_v005', 'COMPARE_V005')
    out['compare'] = cref
    craw = verify_pin(cref)
    out['reused_function_digests'] = {'compare': function_digests(craw, REUSED_COMPARE_FUNCTIONS),
                                      'v005': function_digests(verify_pin(const_pin('COMPARE_V005')), REUSED_V005_FUNCTIONS),
                                      'compare_reviewed': True,
                                      'compare_closure_informational': compare_closure_digest(craw, REUSED_COMPARE_FUNCTIONS)}
    ctx = reader_context(st, R, V5)
    radii = R.registered_row_radii(st['ids'])
    runs = man.get('runs') or {}
    require(sorted(runs) == sorted(RUNS), 'MANIFEST_RUNS', sorted(runs))
    dirs = [runs[c].get('result_dir') for c in RUNS]
    require(all(isinstance(d, str) for d in dirs) and len(set(dirs)) == 3, 'SV0_DISTINCT_OUTDIRS')
    fr = man.get('flag_rulings') or {}
    require(isinstance(fr, dict) and set(fr) <= set(RUNS), 'FLAG_RULINGS_SHAPE')
    # presence: NOT_RUN before anything else
    receipts, missing, bad_receipt = {}, [], {}
    for c in RUNS:
        guard_path(runs[c]['result_dir'])
        rc, rcode = _receipt(runs[c]['receipt'])
        receipts[c] = rc
        if rcode == 'MISSING':
            missing.append('NO_RECEIPT:%s' % c)
        elif rcode is not None:
            bad_receipt[c] = rcode
    if missing:
        return _finish(out, 'NOT_RUN', ';'.join(missing), None, write_dir)
    R_, V, codes, classes = {}, {}, {}, {}
    for c in RUNS:
        if c in bad_receipt:
            codes[c], classes[c] = [bad_receipt[c]], 'NAMED_DEFECT'
            continue
        rc = receipts[c]
        rdir = runs[c]['result_dir']
        st_ = rc.get('status')
        if isinstance(st_, str) and st_.startswith('STOPPED_'):
            codes[c], classes[c] = ['MONITOR_STOP:%s' % st_], 'MONITOR_STOP'
            continue
        if st_ == 'REFUSED':
            codes[c], classes[c] = ['MONITOR_REFUSED'], 'OTHER_FAILED'
            continue
        prescan_result_side_paths(rdir)                                                   # note 11
        run = R.read_run(c, rdir, ctx)
        if not run.get('present'):
            codes[c], classes[c] = ['RESULT_ABSENT_AFTER_RECEIPT:%s:%s' % (st_, run.get('absent'))], \
                ('OTHER_FAILED' if st_ == 'CHILD_FAILED' else 'NAMED_DEFECT')
            continue
        R_[c] = run
        cs, cl, info = run_gates(c, run, rc, runs[c], fill_rec, st, R, V5, ctx, radii, v6)
        codes[c], classes[c] = cs, cl
        V[c] = {'_uvt_info': info.get('uvt_info') or {}, 'flagged': info.get('flagged'), 'flags': info.get('flags', []),
                'packet': info.get('packet'), 'ro1': info.get('ro1')}
    # cross-run checks: K4' differs from K4 only at label; K3 from K4 only at the declared paths
    if not any(classes.values()):
        n4, n4p, n3 = (R_[k]['result'].get('normalized_spec') or {} for k in (S1_C4T, K4P, S1_C3T))
        bad = [p for p in diff_paths(n4, n4p) if not allowed_path(p, ('label',))]
        if bad:
            codes[K4P], classes[K4P] = ['SV_K4PRIME_NOT_K4_EXCEPT_LABEL:%s' % bad[:5]], 'NAMED_DEFECT'
        bad3 = [p for p in diff_paths(n4, n3) if not allowed_path(p, ALLOWED_CHANGED[S1_C3T])]
        if bad3:
            codes[S1_C3T], classes[S1_C3T] = ['SV_K3_NOT_K4_EXCEPT_DECLARED:%s' % bad3[:5]], 'NAMED_DEFECT'
        for c in S1_CASES:
            pre = runs[c].get('prelaunch')
            if pre is not None:
                p = pinned_json(pre, 'PRELAUNCH')
                V[c]['prelaunch_normalized_digest_equal'] = (
                    (p.get('checks') or {}).get('normalized_sha256') == digest(R_[c]['result'].get('normalized_spec')))
    out['validity'] = {c: {'codes': codes.get(c, []), 'class': classes.get(c), 'ro1': (V.get(c) or {}).get('ro1')}
                       for c in RUNS}
    out['receipts'] = {c: {k: (receipts[c] or {}).get(k) for k in ('status', 'stop_reason', 'driver_status', 'exit_code')}
                       for c in RUNS}
    bad_runs = [c for c in RUNS if classes.get(c)]
    if bad_runs:
        out['next_step_per_case'] = {c: NEXT[classes[c]] for c in bad_runs}
        sub = ';'.join('%s:%s' % (c, ','.join(codes[c][:6])) for c in bad_runs)
        return _finish(out, 'INVALID', sub, 'PER_CASE', write_dir)
    # ---- the statistic (section 5) and thresholds (section 6). E^A only from the uv_tail record (B3).
    ids, tau = st['ids'], st['tau']
    v = {c: R_[c]['adapted']['rows'] for c in RUNS}
    d = {i: v[S1_C4T][i] - v[S1_C3T][i] for i in ids}
    dp = {i: v[K4P][i] - v[S1_C3T][i] for i in ids}
    d4 = {i: v[S1_C4T][i] - v[K4P][i] for i in ids}
    dhat = max(max(abs(d[i]), abs(dp[i])) / tau[i] for i in ids)
    out['rows'] = {i: {'v_K3': v[S1_C3T][i], 'v_K4': v[S1_C4T][i], 'v_K4prime': v[K4P][i], 'd': d[i], 'd_prime': dp[i],
                       'delta4': d4[i], 'delta4_bitwise_equal': fhex(v[S1_C4T][i]) == fhex(v[K4P][i]),
                       'abs_d_over_tau': abs(d[i]) / tau[i], 'abs_d_prime_over_tau': abs(dp[i]) / tau[i],
                       'd_over_v': d[i] / v[S1_C4T][i] if v[S1_C4T][i] else None, 'tau': tau[i]} for i in ids}
    flagged = {c for c in RUNS if V[c].get('flagged')}
    out['flag_rulings'] = {}
    for c in sorted(fr):                                                                  # note 13
        require(c in flagged, 'FLAG_RULING_FOR_AN_UNFLAGGED_RUN', c)
        cleared = flag_ruling(fr[c], c, R_[c], V[c]['flags'], v6)
        out['flag_rulings'][c] = {'ruling': fr[c], 'cleared': cleared}
        if cleared:
            flagged.discard(c)
    tests = {'TH1': {'Dhat_S1': dhat, 'threshold': TH1_MAX_OVER_TAU, 'members': list(RUNS),
                     'status': 'PASS' if dhat <= TH1_MAX_OVER_TAU else 'FAIL',
                     'decidability': 'not subject (R6 L1237, L1295)'}}
    for pid, (a, b) in (('TH2_K3_K4', (S1_C3T, S1_C4T)), ('TH2_K3_K4PRIME', (S1_C3T, K4P))):
        nz = R.pair_noise(a, b, R_, V, None, ctx)
        t = {'pair': [a, b], 'threshold_over_tau': TH2_MAX_OVER_TAU, 'noise': _jsonable(nz)}
        if nz.get('decidable') is None:
            t['status'] = 'INCOMPLETE'
        elif nz['decidable']:
            stt = R.row_stat(v[a], v[b], ctx)
            t['stat'] = stt
            t['status'] = 'PASS' if R.thresholded(stt, TH2_MAX_OVER_TAU, True) else 'FAIL'
        else:
            t['status'] = 'RPAIR_PENDING'
            t['rpair_branch'], t['rpair_branch_row'] = nz.get('rpair_branch'), nz.get('rpair_branch_row')
        tests[pid] = t
    for t in tests.values():                                   # A48 AMB-04: flags evaluated per test
        mem = t.get('members') or t.get('pair')
        t['flagged_runs'] = sorted(set(mem) & flagged)
        t['raw_status'] = t['status']
        if t['flagged_runs']:
            if t['status'] == 'PASS':
                t['status'] = 'PASS_FLAGGED'
            elif t['status'] == 'FAIL':
                t['status'] = 'UNDECIDABLE_FLAGGED'
    out['tests'] = tests
    out['statistic'] = {'Dhat_S1': dhat, 'definition': 'max_i max(|d_i|, |d_prime_i|)/tau_i (V005 Dhat on the pair (3,4); '
                                                       'worse of the two K=4 records, CHOICE C3)',
                        'operative_pass_bound_note': 'with both pairs decidable, PASS needs Dhat_S1 <= 1/2 (V6 A150 erratum)'}
    if man.get('anchor_reference') is not None:
        out['anchor_comparison'] = _anchor_comparison(man['anchor_reference'], v, d, dp, st)
    sts = [t['status'] for t in tests.values()]
    if tests['TH1']['status'] == 'FAIL':
        return _finish(out, 'FAIL_TH1', None, None, write_dir)
    if any(tests[p]['status'] == 'FAIL' for p in ('TH2_K3_K4', 'TH2_K3_K4PRIME')):
        return _finish(out, 'FAIL_TH2', ','.join(p for p in ('TH2_K3_K4', 'TH2_K3_K4PRIME') if tests[p]['status'] == 'FAIL'),
                       None, write_dir)
    if 'INCOMPLETE' in sts:
        return _finish(out, 'INVALID', 'INCOMPLETE_RECORD:%s' % [k for k, t in tests.items() if t['status'] == 'INCOMPLETE'],
                       'INCOMPLETE_RECORD', write_dir)
    if 'UNDECIDABLE_FLAGGED' in sts:
        return _finish(out, 'INVALID', 'UNDECIDABLE_FLAGGED:%s' % sorted(flagged), 'UNDECIDABLE_FLAGGED', write_dir)
    if 'RPAIR_PENDING' in sts:
        return _finish(out, 'UNDECIDABLE', 'RPAIR_PENDING', None, write_dir)
    if 'PASS_FLAGGED' in sts:
        return _finish(out, 'INVALID', 'FLAG_PENDING_RULING:%s' % sorted(flagged), 'FLAG_PENDING_RULING', write_dir)
    return _finish(out, 'PASS_AT_ADOPTION_POINT' if branch == 'AT_ANCHOR' else 'PASS', None, None, write_dir)


def _anchor_comparison(ref, v, d, dp, st):
    """Reported, never gating: V007's own anchor C3T/C4T rows (from the compare of record, read only after T0)."""
    a = pinned_json(ref, 'ANCHOR_REFERENCE')
    ids, tau = st['ids'], st['tau']
    a3, a4 = a['rows']['C3T'], a['rows']['C4T']
    return {'source': ref, 'rows': {i: {'anchor_d34': a4[i] - a3[i], 'u_i_first_term_anchor': abs(a4[i] - a3[i]),
                                        'abs_d': abs(d[i]), 'abs_d_prime': abs(dp[i]),
                                        'abs_d_over_u_i': abs(d[i]) / abs(a4[i] - a3[i]) if a4[i] != a3[i] else None}
                                    for i in ids},
            'max_over_tau_S1_vs_V007': {'C3T': max(abs(v[S1_C3T][i] - a3[i]) / tau[i] for i in ids),
                                        'C4T': max(abs(v[S1_C4T][i] - a4[i]) / tau[i] for i in ids)},
            'label': 'reported, never gating'}


def _jsonable(o):
    return json.loads(json.dumps(o, default=str, allow_nan=False))


LABELS = {
    'PASS': ('TESTED-POSITIVE for the K3->K4 increment bound (TH-1, and TH-2 decidable) of the C4T numerics at u_A, at the '
             'recorded delta-u. UNTESTED at u_A: contraction (C2T), the K>4 remainder (C6T), K_big and tail implementation '
             '(T2/T3). UNTESTED at every other point, including the Phase-2 reference member unless its theta bits equal '
             'u_A\'s; deciding test: the S1 pair at that point. The Phase-2 publication carries this line.'),
    'PASS_AT_ADOPTION_POINT': ('TESTED-POSITIVE for reproduction of the K3->K4 increment at the adoption point. S1 transfer '
                               'across parameter space is UNTESTED; deciding test: the S1 pair at the first prediction '
                               'point whose theta bits differ from the anchor.'),
    'FAIL_TH1': 'TESTED-NEGATIVE: V005\'s numeric clause Dhat <= 1 fails at u_A. Not a physics outcome.',
    'FAIL_TH2': ('TESTED-NEGATIVE for the tau_i/2 bound only (decidable); transfer is UNTESTED until S1-DIAG. Not a physics '
                 'outcome.'),
    'UNDECIDABLE': 'UNTESTED: TH-1 holds and a TH-2 pair is undecidable (E + E^A > tau_i/8 on some row).',
    'INVALID': 'UNTESTED (a validity gate failed or a record is incomplete).',
    'NOT_RUN': 'UNTESTED (a case has no receipt, or there is no u_A).',
}


def _finish(out, code, sub, cls, write_dir):
    at = (out.get('branch') or {}).get('branch') == 'AT_ANCHOR'
    out['code'], out['sub_code'] = code, sub
    lab = LABELS[code]
    if at and code == 'FAIL_TH2':
        lab += (' AT_ANCHOR: this follows from V007\'s own anchor Dhat_T(3,4) and carries no transfer information.')
    if at and code == 'FAIL_TH1':
        lab += ' AT_ANCHOR: read as a reproduction defect.'
    out['label'] = lab
    if code == 'PASS':
        eff = 'step-5 values may be read in both phases, subject to every other gate (r3a seal, M-12, A133 section 2)'
        nxt = 'prediction proceeds; the reading sha is cited in the freeze'
    elif code == 'PASS_AT_ADOPTION_POINT':
        eff = ('Phase-1 step-5 values may be read, subject to every other gate; Phase-2 step-5 reads stay held until '
               'S1-B reads PASS (V6 A150 R-S1-1)')
        nxt = 'S1-B (V6 A150 R-S1-1): the same pair, statistic, thresholds and reading at the first Phase-2 member whose theta bits differ from the anchor'
    elif code in ('FAIL_TH1', 'FAIL_TH2'):
        eff = ('step-5 use stops in both phases: no step-5 value is read for any score and no new step-5 NGC launch; '
               'in-flight calls finish unread; the campaign is not stopped by S1')
        nxt = NEXT['S1_DIAG']
    elif code == 'UNDECIDABLE':
        eff, nxt = STEP5_HELD, NEXT['RPAIR']
    elif code == 'INVALID':
        eff = STEP5_HELD
        nxt = (' | '.join('%s: %s' % kv for kv in sorted(out['next_step_per_case'].items())) if cls == 'PER_CASE'
               else NEXT.get(cls, NEXT['NAMED_DEFECT']))
    else:
        eff, nxt = STEP5_HELD, NEXT['NOT_RUN']
    out['step5_effect'], out['next_step'] = eff, nxt
    if write_dir is not None:
        name = 'S1_READING_%s.json' % ((out.get('theta_key') or 'NO_U_A')[:16])
        out['written'] = write_exclusive(str(guard_path(write_dir) / name), record_bytes(out))
    return out
