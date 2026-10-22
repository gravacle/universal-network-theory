"""calibration_orchestrator_c2v005 -- DDO154 calibration orchestrator (Claude2 lane); successor of c2v004a (83b67d6d).
The c2v004 / c2v004a text below is kept; the c2v005 changes are listed after it.

calibration_orchestrator_c2v004 -- DDO154 calibration orchestrator (Claude2 lane); successor of c2v003 (cc4fceec).

What it connects (all loaded from pinned bytes):
  * the calibration engine calibration_region_engine_c2v003a (193841fa) and the freeze module prediction_freeze_c2v003a
    (5ee3e5dc), pinned by the coordinate spec DDO154_CALIBRATION_COORDINATE_SPEC_V001.json (unchanged, fdeb5eb9);
  * COORDINATE_SPEC_ADDENDUM_V004.json (pinned): root decision A13 -- the headline calibration FIXES the DDO154 distance at
    its registered 4.04 Mpc; the free coordinates are s, gamma/Eref and ell_F (boxes as in the V001 spec); distance as a
    nuisance is a recorded alternative NOT_EVALUATED_BEFORE_FREEZE;
  * the forward driver named in the config (target: galaxy_m0_forward_c2v008, f8e47701), run through the pinned root
    monitor (ba031c23) and the campaign launcher campaign_c2v003 (be462862, unchanged);
  * FAILURE_TAXONOMY_V003.json (pinned): the rule table for the c2v008 status vocabulary.

Algorithm: unchanged from c2v001-c2v003 (PROBE -> WAVE -> INGEST -> repeat; REPLAY twice with zero uncached calls;
calibration record).  The probe, its STOP sentinel and the sibling budget guard are c2v001 verbatim.

Changes in c2v004 (CHECK_SCIENCE_V001 S1-S4, CHECK_SOFTWARE_V001 F1-F3, root decision A13):
  A13 coordinate mode from the addendum: DDO154_DISTANCE_FIXED_AT_REGISTERED turns the V001 engine coordinate
      distance_Mpc from nuisance into fixed at its trial value 4.04 (box unchanged, so the engine's distance binding to
      region.distance_summary still holds); everything else in the V001 engine coordinates is byte-identical.  A
      non-synthetic config refuses the DDO154_DISTANCE_NUISANCE mode (the recorded alternative).  The mode and the engine
      coordinates enter the cache id.
  S1  taxonomy V003 R30: under a declared Picard bound a nonpositive final pass is MODEL_INVALID only when NO recorded
      pass produced positive rotation; when an earlier pass was positive it is NUMERICS_LIMITED
      FINAL_PICARD_ITERATE_NONPOSITIVE_UNCONVERGED (HALT for root, pass history in the halt item); an unreadable pass
      history is INFRA.  Root confirms an invalid through 'resolve --decision invalid' (ROOT_RESOLUTION; D5 keeps it UNTESTED).
  S2  route_a_contraction_test.threshold must be >= 1 (a ratio below 1 is contraction by definition).
  S3  the anchor alias result is classified by the taxonomy (collect_evidence + classify on its call directory) and must be
      R01 VALID, at install and on every cache open.
  S4  deciding (ii): the comparator file at the report's comparator.path is hashed from bytes (b122b8e6); the report's
      reference must resolve (realpath) to the pinned CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001 and its result.json must hash to
      bcd2f64e from bytes.
  F1  Cache._verify (WAVE) re-verifies the monitor receipt (pinned monitor, file sha, result pin and path) and the
      finish.json -> result binding; classify records the finish pin and refuses an unbound finish (INFRA).
  F2  the lock is created atomically with its content (exclusive temp file + os.link); an empty or unparseable lock is
      treated as live for 60 s by mtime; a stale takeover verifies it moved the lock it judged stale.
  F3  config work_dir_identity pins the resolved work dir, its symlinks (the runs_ext link target) and the volume (mount
      point + VolumeUUID from read-only diskutil); every command (plan, run, resolve, status) compares it; WORK_DIR.json
      (configured, resolved, symlinks, volume, VolumeUUID, work-dir inode) is compared in prepare, plan, status and resolve;
      a populated work dir without WORK_DIR.json is refused.  A re-pointed link or a swapped volume is refused.

c2v004a = c2v004 (753605af) with exactly two changes; cache id, schemas, MODULE_NAME and records otherwise unchanged:
  S9  (CHECK_SCIENCE_V001 of c2v004) NEVER_INVALID_PREFIXES lists every tooling/custody/infra halt code, so
      'resolve --decision invalid' refuses them (retry only).  R14/R41/R42/R02/DEFAULT stay resolvable.
  F4  (CHECK_SOFTWARE_V001 of c2v004) Lock: fcntl.flock(LOCK_EX | LOCK_NB) on ORCHESTRATOR.lock, a file this module never
      renames or unlinks; the kernel drops the flock when the holder dies.  The v004 holder record and its content rules
      are kept and are judged only while the flock is held; a stale record is copied (exclusive create), never moved.

c2v005 = c2v004a (83b67d6d) + Claude4 R-B corrections (REVIEW_ORCHESTRATOR_V004_C4_V001, root A23 of the open V004
addendum).  Cache id: the same Context.cache_id formula and SCHEMA_CACHE_ID as c2v004/c2v004a (none of the fixes below
enters it); the cache id changes only when the numerics block changes (C4-6: a new adopted block = new base spec).
  C4-1  guarded reads: an unreadable or unparseable result.json -> INFRA RESULT_UNPARSEABLE; an unreadable finish.json ->
        INFRA FINISH_JSON_UNREADABLE; any other OSError in a call directory -> INFRA CALL_DIR_UNREADABLE (all never
        resolvable as invalid); a cache entry whose bytes cannot be read or parsed is a refusal (exit 3), never a traceback;
        the taxonomy code template is filled by a function (a driver reason is never a re.sub template); an unreadable lock
        file counts as held (LOCKED).
  C4-2  a work dir holds ONE cache id: plan, run and resolve refuse (exit 3, 'config changed: use a new work dir') when any
        committed WAVE_PLAN has another cache id; an interrupted wave resumes only if every planned spec equals
        mapper.build(theta) (and its bytes), and only through the disk guard; RESOLUTIONS lines carry the cache id and a
        root resolution is materialized / verified only under the cache id of its line and of its HALT's WAVE_PLAN;
        WAVE_PLAN and every ledger line record config_sha256 and gate_digest.
  C4-4  the campaign launcher is campaign_c2v005 (monitors start in their own session, so a signal to the orchestrator's
        process group never reaches a monitor and every driver keeps its caps); a non-synthetic run refuses unless the
        orchestrator is a session leader (launch through launch_setsid_c2v005.py; stop it by PID).
  C4-5  numerics gate: numerics = {block, verdict_artifact, block_source, note}; the verdict artifact is the k_max
        comparison (UNT_KMAX_COMPARISON_C2_V005; non-synthetic: test_mode false and the sealed prereg dbddc02c), its
        decision.outcome must be ADOPT, the adopted case (prereg case of the adopted shape on the adopted grid) must be
        gate-valid and its inputs call_spec_sha256 must equal sha256(block_source bytes); the block must equal
        block_source.numerics outside numerics.route_a, its truncation shape must be the adopted shape and its Picard bound
        a finite positive number.  block_pointer / root_attestation are gone.
  C4-6  gate adoption_regeneration: the pinned adoption_derivation must name this verdict, adopted case and call spec, this
        base spec, this seed spec, this capability evidence, a timing model regenerated for the adopted case, the source
        receipts of the adopted grid's cases (verified by the pinned monitor) and caps equal to the config's and above every
        receipt's measured use.  gate u_i_carrier: the declared carrier of the verdict's u_i (default 'not carried;
        declared'; root sets declared_by; ADMISSION_RECTANGLES is not implemented and refuses).
  B2-2  before every wave (new or resumed) every pinned input is re-hashed from bytes and every gate is re-evaluated; a
        changed byte or gate digest refuses (exit 3).
  SF1   before every wave and before every ingest the work dir is re-resolved and compared with the config pin and
        WORK_DIR.json.
  SF2   run writes a fresh WORK_DIR.json only with --new-campaign (and only on a work dir without one); without it an absent,
        moved or emptied work dir is refused.
  SF4   config python is a {path, sha256} pin; WORK_DIR.json and every WAVE_PLAN record the runtime identity (interpreter
        realpath + sha256 + sys.version, numpy version + build config + core-extension sha256, OS release/build); a changed
        runtime refuses before every wave.
  Addendum V005 (schema ..._C2V005, required): A23 wording of A13 in coordinate_mode.rule / .admissibility; CA-33.

CLI:
  calibration_orchestrator_c2v005.py plan    --config CONFIG.json
  calibration_orchestrator_c2v005.py run     --config CONFIG.json [--max-waves N] [--new-campaign]
  calibration_orchestrator_c2v005.py resolve --config CONFIG.json --wave W (--token T [--token T ...] | --all --halt-sha256 H)
                                             --decision invalid|retry|retry_with_recovery [--recovery PATH] --reason TEXT
  calibration_orchestrator_c2v005.py status  --config CONFIG.json
Exit codes: 0 complete/ok, 3 refused, 4 HALTED_INFRA, 5 HALTED_DISK, 6 MAX_WAVES, 7 HALTED_UNRESOLVED, 8 LOCKED,
9 REPLAY_FAILED, 10 ORPHANS_STILL_RUNNING, 11 HALTED_NUMERICS, 12 RECORD_UNVERIFIED.
Writes only under the configured work_dir.  numpy only (through the engine), single thread.  Never opens an NGC3198 file.
Importing this module does nothing.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import argparse
import ast
import copy
import datetime
import errno
import fcntl                         # v004a F4
import hashlib
import importlib.util
import json
import math
import platform                      # v005 SF4
import plistlib
import re
import shutil
import socket
import subprocess
import sys
import time
import types
from pathlib import Path

MODULE_NAME = 'calibration_orchestrator_c2v005'
LEGACY_MODULE_NAMES = ('calibration_orchestrator_c2v004',)     # v005: a live v004/v004a holder still counts as live (L4)
SCHEMA_CONFIG = 'DDO154_CALIBRATION_ORCHESTRATOR_CONFIG_C2V005'  # v005: python pin, numerics block_source, u_i, adoption
SCHEMA_SPEC = 'DDO154_CALIBRATION_COORDINATE_SPEC_C2V001'
SCHEMA_ADDENDUM = 'DDO154_CALIBRATION_COORDINATE_SPEC_ADDENDUM_C2V005'   # v005: A23 wording + CA-33
SCHEMA_TAXONOMY = 'DDO154_CALIBRATION_FAILURE_TAXONOMY_V003'
SCHEMA_CAPABILITY = 'DDO154_CALIBRATION_DRIVER_CAPABILITY_EVIDENCE_V001'
SCHEMA_THETA_KEY = 'DDO154_CALIBRATION_THETA_KEY_C2V001'          # unchanged: theta keys are comparable with c2v001-3
SCHEMA_CACHE_ID = 'DDO154_CALIBRATION_CACHE_ID_C2V004'           # unchanged in v005: the cache id formula is c2v004's
SCHEMA_CACHE_ENTRY = 'DDO154_CALIBRATION_CACHE_ENTRY_C2V004'     # unchanged in v005
SCHEMA_WAVE_PLAN = 'DDO154_CALIBRATION_WAVE_PLAN_C2V005'         # v005: + config_sha256, gate_digest, runtime
SCHEMA_WAVE_RESULT = 'DDO154_CALIBRATION_WAVE_RESULT_C2V004'
SCHEMA_HALT = 'DDO154_CALIBRATION_HALT_C2V004'
SCHEMA_TOKEN = 'DDO154_CALIBRATION_HALT_TOKEN_C2V004'
SCHEMA_RESOLUTION = 'DDO154_CALIBRATION_RESOLUTION_C2V005'       # v005 C4-2: + cache_id
SCHEMA_WORKDIR = 'DDO154_CALIBRATION_WORK_DIR_C2V005'            # v005 SF4: + runtime (a v004 WORK_DIR.json is refused)
SCHEMA_SUMMARY = 'DDO154_CALIBRATION_ORCHESTRATION_SUMMARY_C2V004'
SCHEMA_ADOPTION = 'DDO154_CALIBRATION_ADOPTION_DERIVATION_C2V005'  # v005 C4-6
# v005 C4-5: the convergence verdict the numerics gate reads (kmax_compare_c2v005.py report) and its sealed prereg
VERDICT_SCHEMAS = ('UNT_KMAX_COMPARISON_C2_V005',)
KMAX_PREREG_SHA256 = ('dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174',)   # KMAX_MATRIX_PREREG_V005
NUMERICS_KEYS = {'block', 'verdict_artifact', 'block_source', 'note'}
# v005 C4-6: where the verdict's carried numerical uncertainty u_i enters (root declares; default NOT_CARRIED_DECLARED)
U_I_CARRIERS = ('NOT_CARRIED_DECLARED', 'FROZEN_BANDS_ONLY', 'ADMISSION_RECTANGLES')
U_I_CARRIERS_IMPLEMENTED = ('NOT_CARRIED_DECLARED', 'FROZEN_BANDS_ONLY')
U_I_KEYS = {'carrier', 'declared_by', 'basis', 'note'}
ADOPTION_CAP_KEYS = ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')
COUNTED_ASSUMPTION_A13 = 'CA-33'                                  # v005: the addendum must count A13
SPEC_MAPPING_ID = 'C2V001_PHYS4_GAMMA_EQ_GE_TIMES_EREF'
MAPPING_ID = 'C2V003_BASE_TEMPLATE_PLUS_NUMERICS_PHYS4'      # mapping unchanged (theta -> call spec)
ANCHOR_ALIAS_RTOL = 1e-14
DECLARED_CHANGED_PATHS = ('label', 'physical.common_scale_s', 'physical.gamma', 'physical.ell_F_m',
                          'physical.distance_Mpc')
# A13: coordinate modes of the addendum.  FIXED = the headline calibration (3 free coordinates, D = 4.04 Mpc);
# NUISANCE = the V001 4-coordinate spec (the recorded alternative; synthetic tests / a later sensitivity only).
MODE_D_FIXED = 'DDO154_DISTANCE_FIXED_AT_REGISTERED'
MODE_D_NUISANCE = 'DDO154_DISTANCE_NUISANCE'
DDO154_DISTANCE_NAME = 'distance_Mpc'
DDO154_REGISTERED_DISTANCE_MPC = 4.04
VARYING_EXPECTED_BY_MODE = {MODE_D_FIXED: ('common_scale_s', 'gamma_over_Eref', 'ell_F_m'),
                            MODE_D_NUISANCE: ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'distance_Mpc')}
LOCK_EMPTY_LIVE_S = 60.0             # F2: an empty / unparseable lock younger than this (mtime) is treated as live
WORK_DIR_MARKERS = ('waves', 'cache', 'records', 'LAUNCH_LEDGER.jsonl', 'RESOLUTIONS.jsonl', 'FINAL_SUMMARY.json')
WORK_DIR_IDENTITY_KEYS = ('resolved', 'volume', 'volume_uuid', 'symlinks')
FIXED_TEMPLATE_CHECKS = (('Eref_J', 'Eref_base_J'), ('entropy_K_factor', 'entropy_K_factor'))
REQUIRED_VERDICT = 'PASS_BITWISE_EQUAL'
PROCESS_BUDGET_MAX = 17              # 6 performance + 12 efficiency cores, one left for the orchestrator/system
CAMPAIGN_MODULE_NAME = 'campaign_c2v005'   # v005 C4-4: monitors in their own session (campaign_c2v003 is refused)
OVERRIDE_KEY_RE = re.compile('0|[1-9][0-9]*')
CLASSES = ('VALID', 'MODEL_INVALID', 'NUMERICS_LIMITED', 'INFRA')
CACHED_CLASSES = ('VALID', 'MODEL_INVALID')
HALT_CLASSES = ('NUMERICS_LIMITED', 'INFRA')
DECISIONS = ('invalid', 'retry', 'retry_with_recovery')
RETRY_DECISIONS = ('retry', 'retry_with_recovery')
# Union with the taxonomy list (C11).  v004a S9 (CHECK_SCIENCE_V001 of c2v004): every tooling / custody / infra halt code
# is refused for 'resolve --decision invalid' (retry is the only resolution).  Kept resolvable on purpose (S9: reasons the
# taxonomy does not recognize, possibly physical): R14 ROUTE_A_NO_FIXED_POINT_UNRECOGNIZED, R41 FAILED_AT_STAGE, R42
# COMPLETED_INVALID, R02 COMPLETED_WITHOUT_VALID_ROWS (S7: an N1 invalid row) and the DEFAULT UNRECOGNIZED.
# Not in the cache id.
NEVER_INVALID_PREFIXES = (
    'MONITOR_STOPPED_', 'DRIVER_CAPABILITY_GAP',                               # v004 (C11): monitor caps, R39
    # orchestrator-level custody checks (CampaignExecutor.classify, finish_binding, InProcessExecutor)
    'CAMPAIGN_', 'NO_RECEIPT', 'RECEIPT_UNVERIFIED', 'SPEC_FILE_MISMATCH', 'NO_RESULT_JSON', 'RESULT_HASH',
    'RESULT_NOT_BOUND_TO_SPEC_OR_DRIVER', 'FINISH_', 'DRIVER_STATUS_MISMATCH', 'IN_PROCESS_NON_DICT',
    'RESULT_UNPARSEABLE', 'CALL_DIR_UNREADABLE',                               # v005 C4-1 (FINISH_JSON_UNREADABLE: FINISH_)
    # taxonomy V003: orchestrator-level checks and the INFRA rules of tooling kind
    'EVIDENCE_UNREADABLE', 'FINAL_PASS_NONPOSITIVE_PASS_HISTORY_UNREADABLE',
    'ROUTE_A_POOL_FAILURE',                                                    # R15
    'FINAL_COLUMN_MEAN_INVALID_FINITE_POSITIVE_ROTATION_INCONSISTENT',         # R31
    'BLOCKED:',                                                                # R40
    'REFUSED:',                                                                # R43
    'FAILED:')                                                                 # R44 (ENOSPC, code bugs); not FAILED_AT_STAGE
PLACEHOLDER_REASON = 'ORCHESTRATOR_PROBE_PLACEHOLDER_NOT_AN_EVALUATION'
SINGLE_FAMILIES = ('seed', 'repair')
CK_FLOAT = 'f'
COLUMN_WORKERS_INVARIANCE = ('UNTESTED for numerics.column_workers (fs/rfs): it changes only how columns are grouped into '
                             'runs (driver c2v008 generated_runs/column_pass); deciding (ii) runs the anchor value 2.  Until a '
                             'call at 2 and at N is compared bitwise, column_workers stays part of the base spec and the '
                             'cache id.  numerics.route_a.column_workers is covered only at the value deciding (ii) verified.')
EXIT = {'COMPLETE': 0, 'OK': 0, 'REFUSED': 3, 'HALTED_INFRA': 4, 'HALTED_DISK': 5, 'MAX_WAVES': 6,
        'HALTED_UNRESOLVED': 7, 'LOCKED': 8, 'REPLAY_FAILED': 9, 'ORPHANS_STILL_RUNNING': 10, 'HALTED_NUMERICS': 11,
        'RECORD_UNVERIFIED': 12}
CONFIG_KEYS = {'schema', 'synthetic_test', 'work_dir', 'work_dir_volume', 'coordinate_spec', 'coordinate_spec_addendum',
               'observation_region', 'numerics', 'max_concurrent', 'process_budget', 'stage_aware_budget', 'n_cores',
               'ngc3198_slots', 'anchor', 'driver', 'deciding_test', 'capability_evidence', 'taxonomy',
               'route_a_contraction_test', 'recovery_rules', 'monitor', 'campaign', 'python', 'per_call',
               'campaign_wall_cap_s', 'disk_guard', 'orphan_wait', 'engine_parameters_override', 'executor', 'notes',
               'work_dir_identity',
               'u_i_carrier', 'adoption_derivation'}                     # v005 C4-6
ANCHOR_KEYS = {'use', 'receipt', 'result', 'spec_sha256', 'driver_sha256'}
# C7: drivers that run the real DDO154 forward (sha256 from bytes); a synthetic_test config may never pin one of them.
KNOWN_REAL_DRIVER_SHA256 = {
    '75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22',   # galaxy_m0_forward_c2v001
    'daa42a9f5407a478bc24e642f17399d120b1a9c813beca02fdd2930747504ab3',   # galaxy_m0_forward_c2v002
    'ed326130e89654a377615e46a077764cf3ad39e0bf07bc9d0606225bc69fbdf2',   # galaxy_m0_forward_c2v003c
    'c53997b4e6fcd6107bb7a564ee251271942fe1dbe9a365f4d9b6ebbb4d0c9e69',   # galaxy_m0_forward_c2v006
    '0338584b4ba8d12609aa3b95f422845a86fb09379de65e2e9980a72bd44e3d4c',   # galaxy_m0_forward_c2v007
    'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28'}   # galaxy_m0_forward_c2v008
SYNTHETIC_DRIVER_MARKER = b'CAL_ORCH_SYNTHETIC_MOCK_DRIVER'
# C5: what the two driver deciding tests must show (driver_v008_c2/deciding/LAUNCH_DECIDING_{I,II}_C2V008.json)
DECIDING_EXPECT = {
    'i_admit_prefix': {
        'spec_sha256': '4ac5527ad1731353d798c2648adc1033335a12102ec071b3ae6a619334313cb7',
        'route_a_converged_iteration': 4,
        'solver_sha256': '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644',
        'attempt_link': {'identity_sha256': '98816902f71d17f9d9be47adf7f11a2652fc5234b7ea81cc09dd2f7be231ad77',
                         'attempt': '01792161909921426000-19994-831a3fbc'},
        'source_profile_sha256': 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'},
    'ii_full_anchor': {
        'spec_sha256': '4978ba17fb05fb3fb096440d9a8a20e1d2d4d657d0b4b8f7007dc457d37c73eb',
        'compare_schema': 'UNT_DRIVER_V008_DECIDING_II_COMPARE_V001',
        'comparator_sha256': 'b122b8e691b46d5fc83149d5b9454f79b560e49dc600f07d8a11b140d174a467',
        'reference_run_name': 'A2_ANCHOR_F10_RUN_V001',
        # S4: the reference is checked from bytes (realpath + result.json sha256), not by its basename alone
        'reference_path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_'
                          '2026-10-13/CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001',
        'reference_result_sha256': 'bcd2f64ec6c858a51718b2badb85b9e35121b6a3575227a4c9e4b8b5c673836e',
        'required_checks': ['RA_BLOBS', 'RA_RECORDS', 'RA_IDENTITY', 'RA_SEED', 'RA_END', 'RA_RESULT', 'RA_ARRAYS',
                            'RA_NODES', 'RA_START', 'RA_FINISH', 'RA_ROWS', 'SPEEDS', 'NEW_CUSTODY']}}
DECIDING_SYNTHETIC_EXPECT_KEYS = set(DECIDING_EXPECT)


class OrchestratorError(Exception):
    """Refusal: configuration, pin, gate or consistency failure (exit 3)."""


class _ProbeStop(BaseException):
    """STOP sentinel (c2v001 verbatim).  A BaseException on purpose: the engine's forward guard (_evaluate_point
    L1048-1053) and its fail-closed wrappers (_fail_closed L185-201) catch Exception only."""

    def __init__(self, reason):
        BaseException.__init__(self, reason)
        self.reason = reason


# --------------------------------------------------------------------------------------------- small helpers
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def utc_compact():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def json_bytes(obj):
    return (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def load_json_file(path, label):
    """L3: an unreadable or torn JSON file is a refusal (exit 3), never a traceback."""
    try:
        return json.loads(Path(path).read_bytes().decode('utf-8'))
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        raise OrchestratorError('%s unreadable (%s): %s: %s' % (label, path, type(exc).__name__, str(exc)[:200]))


def write_json_x(path, obj):
    raw = json_bytes(obj)
    with open(path, 'xb') as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())
    return sha256_bytes(raw)


def write_json_atomic_x(path, obj):
    """F3: exclusive temp file + hard link into place (atomic, never overwrites); the temp name is the orchestrator's
    own file and is unlinked after the link (a leftover temp from a crash is ignored: it never matches *.json)."""
    path = Path(path)
    tmp = path.with_name('.%s.%d.%d.tmp' % (path.name, os.getpid(), time.time_ns()))
    s = write_json_x(tmp, obj)
    os.link(tmp, path)
    os.unlink(tmp)
    return s


def write_json_idempotent(path, obj, core):
    """M1: write once; if the file already exists (a crash after its link and before the step that follows), accept it
    when its semantic core equals the new one, else refuse.  Returns (sha256 of the file in place, written_now)."""
    path = Path(path)
    if path.exists():
        old = load_json_file(path, path.name)
        if canonical(core(old)) != canonical(core(obj)):
            raise OrchestratorError('%s exists with different content (never overwritten): %s' % (path.name, path))
        return sha256_file(path), False
    try:
        return write_json_atomic_x(path, obj), True
    except FileExistsError:                                    # a concurrent identical writer: verify it
        return write_json_idempotent(path, obj, core)


_JSONL_TORN = {}


def append_jsonl(path, obj):
    """One canonical line per os.write (O_APPEND, fsync).  L3: if the file ends in a torn line (crash during a write),
    a newline is written first so the torn fragment stays a separate (skipped) line."""
    line = canonical(obj) + b'\n'
    fd = os.open(path, os.O_RDWR | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        size = os.fstat(fd).st_size
        if size > 0:
            os.lseek(fd, size - 1, os.SEEK_SET)
            if os.read(fd, 1) != b'\n':
                line = b'\n' + line
        os.write(fd, line)
        os.fsync(fd)
    finally:
        os.close(fd)


def read_jsonl(path):
    """L3: an unparseable line can only be a torn write (one canonical line per os.write); it is skipped and counted
    (_JSONL_TORN, reported by status).  Every consumer is safe with a skipped torn line: a ledger line of an uncommitted
    wave never counts, a torn RESOLUTIONS line is a resolve that did not complete, events are informational."""
    if not os.path.isfile(path):
        return []
    out, torn = [], 0
    with open(path, 'rb') as fh:
        for ln in fh.read().split(b'\n'):
            if not ln.strip():
                continue
            try:
                out.append(json.loads(ln.decode('utf-8')))
            except (ValueError, UnicodeDecodeError):
                torn += 1
    _JSONL_TORN[str(path)] = torn
    return out


def pid_alive(pid):
    try:
        os.kill(int(pid), 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except (TypeError, ValueError, OverflowError):
        return False
    return True


def process_command(pid):
    """Command line of a live pid via read-only ps, or None when it cannot be read."""
    try:
        p = subprocess.run(['ps', '-p', str(int(pid)), '-o', 'command='], capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    return p.stdout.strip() or None


def live_processes(substrings):
    """F4: live processes whose command line contains any of `substrings` (read-only `ps`).  Returns a list of
    {pid, command} or None when the process table cannot be read (callers treat None as 'may be alive')."""
    try:
        p = subprocess.run(['ps', '-axww', '-o', 'pid=,command='], capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    me = os.getpid()
    out = []
    for ln in p.stdout.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        parts = ln.split(None, 1)
        if len(parts) != 2:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        if pid == me:
            continue
        if any(s and s in parts[1] for s in substrings):
            out.append({'pid': pid, 'command': parts[1][:300]})
    return out


def read_pinned(pin, label):
    if not isinstance(pin, dict) or not isinstance(pin.get('path'), str) or not isinstance(pin.get('sha256'), str):
        raise OrchestratorError('%s: {path, sha256} required' % label)
    try:
        raw = Path(pin['path']).read_bytes()
    except OSError as exc:
        raise OrchestratorError('%s: unreadable %s: %s' % (label, pin['path'], exc))
    if sha256_bytes(raw) != pin['sha256']:
        raise OrchestratorError('%s: sha256 mismatch for %s' % (label, pin['path']))
    return raw


def load_pinned_module(pin, name, label):
    read_pinned(pin, label)
    sp = importlib.util.spec_from_file_location(name, pin['path'])
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    if sha256_file(pin['path']) != pin['sha256']:
        raise OrchestratorError('%s changed while loading' % label)
    return m


def collect_pins(obj, prefix=''):
    """B2-2 (v005): every {path, sha256} pin with a 64-hex sha256 anywhere inside obj -> [(dotted label, pin)]."""
    out = []
    if isinstance(obj, dict):
        p, s = obj.get('path'), obj.get('sha256')
        if isinstance(p, str) and isinstance(s, str) and re.fullmatch('[0-9a-f]{64}', s):
            out.append((prefix or '$', {'path': p, 'sha256': s}))
        for k, v in obj.items():
            out.extend(collect_pins(v, (prefix + '.' + str(k)) if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(collect_pins(v, '%s[%d]' % (prefix, i)))
    return out


def _file_identity(path):
    """SF4: realpath + sha256 of a file (None fields when unreadable: compared, so an unreadable file is a change)."""
    try:
        rp = os.path.realpath(str(path))
        return {'realpath': rp, 'sha256': sha256_file(rp)}
    except (OSError, TypeError, ValueError):
        return {'realpath': None, 'sha256': None}


def runtime_identity(driver_python_path):
    """SF4 (v005): what a long campaign must not silently change under it.  The orchestrator's own interpreter (it runs
    the engine in process), the driver interpreter of the config (it runs every forward), numpy (version, build
    configuration, core-extension bytes) and the OS (release, kernel build string, macOS version).  No process is
    started.  BLAS is the system Accelerate framework: the OS build string stands for it."""
    out = {'orchestrator_python': dict(_file_identity(sys.executable), executable=sys.executable, version=sys.version),
           'driver_python': dict(_file_identity(driver_python_path), path=driver_python_path)}
    np_mod = sys.modules.get('numpy')
    if np_mod is None:
        out['numpy'] = None
    else:
        core = None
        for name in ('numpy._core._multiarray_umath', 'numpy.core._multiarray_umath'):
            m = sys.modules.get(name)
            if m is not None and getattr(m, '__file__', None):
                core = m.__file__
                break
        try:
            cfgd = np_mod.show_config(mode='dicts')
            cfg_sha = sha256_bytes(json.dumps(cfgd, sort_keys=True, default=str).encode('utf-8'))
        except Exception:                                  # an older numpy without mode='dicts': recorded as unknown
            cfg_sha = None
        out['numpy'] = {'version': getattr(np_mod, '__version__', None), 'file': getattr(np_mod, '__file__', None),
                        'build_config_sha256': cfg_sha, 'core_extension': dict(_file_identity(core), path=core) if core else None}
    u = os.uname()
    out['os'] = {'sysname': u.sysname, 'release': u.release, 'kernel_version': u.version, 'machine': u.machine,
                 'mac_ver': platform.mac_ver()[0]}
    return out


def runtime_differences(old, new, prefix=''):
    """Dotted paths at which two runtime identities differ."""
    return diff_paths(old, new, prefix) if isinstance(old, dict) and isinstance(new, dict) else (
        [] if canonical(old) == canonical(new) else [prefix or '$'])


def session_record():
    """C4-4 (v005): the orchestrator's process group and session.  A session leader (launched through
    launch_setsid_c2v005.py) is the only process of its group, so a group signal cannot reach any monitor."""
    pid = os.getpid()
    sid, pgid = os.getsid(0), os.getpgrp()
    return {'pid': pid, 'pgid': pgid, 'sid': sid, 'session_leader': sid == pid and pgid == pid}


def exec_pinned_bytes(pin, name, label):
    """Execute a pinned file from the exact bytes that were hashed (driver normalizer; the driver's own CLI is
    never run in process: its main() is guarded by __name__ == '__main__')."""
    raw = read_pinned(pin, label)
    m = types.ModuleType(name)
    m.__file__ = str(pin['path'])
    exec(compile(raw, str(pin['path']), 'exec'), m.__dict__)
    return m


def theta_key(theta):
    """Canonical theta hash (c2v001 verbatim)."""
    th = {str(k): float(v) for k, v in theta.items()}
    for k, v in th.items():
        if not math.isfinite(v):
            raise OrchestratorError('non-finite theta[%s]' % k)
    return sha256_bytes(canonical({'schema': SCHEMA_THETA_KEY, 'theta': th}))


def diff_paths(a, b, prefix=''):
    """Dotted paths at which two JSON objects differ (dict keys recursed; anything else compared whole)."""
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


def json_pointer(doc, pointer):
    """RFC 6901 pointer lookup ('' = whole document)."""
    if pointer == '':
        return doc
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise OrchestratorError('JSON pointer must start with /: %r' % (pointer,))
    cur = doc
    for tok in pointer[1:].split('/'):
        tok = tok.replace('~1', '/').replace('~0', '~')
        if isinstance(cur, dict) and tok in cur:
            cur = cur[tok]
        elif isinstance(cur, list) and tok.isdigit() and int(tok) < len(cur):
            cur = cur[int(tok)]
        else:
            raise OrchestratorError('JSON pointer %r does not resolve' % pointer)
    return cur


def decode_ck_float(v):
    """Checkpoint encoding ['f', float.hex] (CK encode) or a plain number -> float; anything else -> None."""
    if isinstance(v, list) and len(v) == 2 and v[0] == CK_FLOAT and isinstance(v[1], str):
        try:
            return float.fromhex(v[1])
        except ValueError:
            return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    return None


def call_weights(numerics, admitted_route_a=False):
    """Busy single-thread processes of one call (driver c2v008): route A runs numerics.route_a.column_workers pool
    workers (1 = reviewed serial worker); fs/rfs column passes run numerics.column_workers stage processes in waves;
    every other stage (reference, body, offset, rotations, feedback, column mean, LE passes under a bound) is one
    process.  peak = the weight from launch until route A has finished; after = the weight bound for the rest."""
    cw = int((numerics or {}).get('column_workers', 1))
    ra = int(((numerics or {}).get('route_a') or {}).get('column_workers', 1))
    after = max(1, cw)
    peak = after if admitted_route_a else max(ra, after)
    return {'route_a_column_workers': ra, 'column_workers': cw, 'peak': peak, 'after_route_a': after}


# --------------------------------------------------------------------------------------------- A7 guards
def lint_override_keys(obj, prefix='', inside=False):
    """A7 (F3) + CHECK_SOFTWARE L6: every key of every *_overrides dict, and every key of every dict nested at ANY depth
    beneath one, must fullmatch 0|[1-9][0-9]*.  Returns the offending dotted paths (empty = clean)."""
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = (prefix + '.' + str(k)) if prefix else str(k)
            if inside:
                if not (isinstance(k, str) and OVERRIDE_KEY_RE.fullmatch(k)):
                    bad.append('%s[%r]' % (prefix, k))
                bad.extend(lint_override_keys(v, p, True))
            elif isinstance(k, str) and k.endswith('_overrides'):
                if not isinstance(v, dict):
                    bad.append(p + ' (not an object)')
                    continue
                bad.extend(lint_override_keys(v, p, True))
            else:
                bad.extend(lint_override_keys(v, p, False))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            bad.extend(lint_override_keys(v, '%s[%d]' % (prefix, i), inside))
    return bad


def relative_paths(obj, prefix=''):
    """A7 (F2): string values under a key named path / *directory* / *_dir must be absolute paths."""
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = (prefix + '.' + str(k)) if prefix else str(k)
            if isinstance(v, str) and isinstance(k, str) and (k == 'path' or 'directory' in k or k.endswith('_dir')):
                if not v or not os.path.isabs(v):
                    bad.append('%s=%r' % (p, v))
            else:
                bad.extend(relative_paths(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            bad.extend(relative_paths(v, '%s[%d]' % (prefix, i)))
    return bad


# --------------------------------------------------------------------------------------------- work dir (External1)
def resolve_work_dir(work_dir, volume):
    """The work dir may sit behind symlinks (CLAUDE2/runs_ext -> /Volumes/External1/...).  Refuses a dangling component
    (volume unmounted) and, with a declared volume, a resolved path outside that mount point.  Returns the record:
    configured path, resolved path, symlinks crossed, volume, nearest existing ancestor (where free space is read)."""
    if not isinstance(work_dir, str) or not os.path.isabs(work_dir):
        raise OrchestratorError('A7_ABSOLUTE_PATH: work_dir must be absolute')
    links = []
    cur = Path('/')
    for part in Path(work_dir).parts[1:]:
        cur = cur / part
        if os.path.islink(cur):
            tgt = os.readlink(cur)
            if not os.path.exists(cur):
                raise OrchestratorError('WORK_DIR_DANGLING_SYMLINK: %s -> %s does not resolve (volume not mounted?)'
                                        % (cur, tgt))
            links.append({'link': str(cur), 'target': tgt, 'resolved': os.path.realpath(cur)})
    real = os.path.realpath(work_dir)
    anc = Path(real)
    while not anc.exists() and anc != anc.parent:
        anc = anc.parent
    rec = {'schema': SCHEMA_WORKDIR, 'configured': work_dir, 'resolved': real, 'symlinks': links,
           'existing_ancestor': str(anc), 'volume': None}
    if volume is not None:
        if not isinstance(volume, str) or not os.path.isabs(volume):
            raise OrchestratorError('work_dir_volume must be an absolute path or null')
        vreal = os.path.realpath(volume)
        if not os.path.ismount(vreal):
            raise OrchestratorError('WORK_DIR_VOLUME_NOT_MOUNTED: %s is not a mount point' % vreal)
        if not (real == vreal or real.startswith(vreal.rstrip('/') + '/')):
            raise OrchestratorError('WORK_DIR_NOT_ON_VOLUME: %s resolves to %s, outside %s' % (work_dir, real, vreal))
        if not (str(anc) == vreal or str(anc).startswith(vreal.rstrip('/') + '/')):
            raise OrchestratorError('WORK_DIR_ANCESTOR_NOT_ON_VOLUME: %s' % anc)
        rec['volume'] = vreal
        rec['volume_st_dev'] = os.stat(vreal).st_dev
        rec['volume_uuid'] = volume_uuid(vreal)
    else:
        rec['volume_uuid'] = None
    rec['existing_ancestor_st_dev'] = os.stat(str(anc)).st_dev
    return rec


def volume_uuid(mount_point):
    """F3: the VolumeUUID of a mount point from read-only `diskutil info -plist` (macOS); None when it cannot be read
    (callers that pinned a UUID treat None as a mismatch: fail closed).  st_dev is NOT an identity: it can change on a
    remount."""
    try:
        p = subprocess.run(['diskutil', 'info', '-plist', str(mount_point)], capture_output=True, timeout=60)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    try:
        d = plistlib.loads(p.stdout)
    except Exception:
        return None
    u = d.get('VolumeUUID')
    if not isinstance(u, str) or not u:
        return None
    if os.path.realpath(str(d.get('MountPoint') or '')) != os.path.realpath(str(mount_point)):
        return None
    return u


def work_dir_identity_core(rec):
    """F3: the identity of a resolved work dir that a config pins (WORK_DIR_IDENTITY_KEYS)."""
    return {'resolved': rec.get('resolved'), 'volume': rec.get('volume'), 'volume_uuid': rec.get('volume_uuid'),
            'symlinks': [{'link': x.get('link'), 'target': x.get('target')} for x in rec.get('symlinks') or []]}


def check_work_dir_identity(pin, rec):
    """F3: compare the config pin with the current resolution; returns a list of mismatch reasons (empty = equal)."""
    if not isinstance(pin, dict) or set(pin) != set(WORK_DIR_IDENTITY_KEYS):
        raise OrchestratorError('work_dir_identity must be {%s}' % ', '.join(WORK_DIR_IDENTITY_KEYS))
    cur = work_dir_identity_core(rec)
    bad = []
    if pin['resolved'] != cur['resolved']:
        bad.append('WORK_DIR_REPOINTED: the work dir resolves to %s, the config pins %s' % (cur['resolved'], pin['resolved']))
    if canonical(pin['symlinks']) != canonical(cur['symlinks']):
        bad.append('WORK_DIR_REPOINTED: symlinks crossed %s differ from the pinned %s' % (cur['symlinks'], pin['symlinks']))
    if pin['volume'] != cur['volume']:
        bad.append('WORK_DIR_VOLUME_MISMATCH: volume %r, pinned %r' % (cur['volume'], pin['volume']))
    if pin['volume_uuid'] is not None and pin['volume_uuid'] != cur['volume_uuid']:
        bad.append('WORK_DIR_VOLUME_IDENTITY_MISMATCH: VolumeUUID %r, pinned %r (another disk at the mount point, or '
                   'unreadable)' % (cur['volume_uuid'], pin['volume_uuid']))
    if pin['volume'] is not None and pin['volume_uuid'] is None:
        bad.append('WORK_DIR_VOLUME_IDENTITY_NOT_PINNED: a declared volume needs its VolumeUUID pinned')
    return bad


# --------------------------------------------------------------------------------------------- gates
def _receipt_ok(mon, rpin, spec_sha, driver_sha, res_pin, label):
    raw = read_pinned(rpin, '%s receipt' % label)
    del raw
    v = mon.verify_receipt(rpin['path'], spec_sha256=spec_sha, driver_sha256=driver_sha)
    if not v['ok']:
        return 'receipt does not verify: %s' % v['reasons']
    r = v['receipt']
    if r.get('status') != 'FINISHED' or r.get('driver_status') != 'COMPLETED':
        return 'receipt status %r / driver_status %r is not FINISHED / COMPLETED' % (r.get('status'), r.get('driver_status'))
    if (r.get('result') or {}).get('sha256') != res_pin['sha256'] or \
            os.path.realpath(str((r.get('result') or {}).get('path'))) != os.path.realpath(res_pin['path']):
        return 'receipt result pin is not the pinned result'
    return None


def _deciding_run(part, label, driver_sha, mon, expect):
    """Common checks of one deciding run: result bytes pin, finish custody, receipt (pinned monitor), driver, spec,
    status COMPLETED.  Returns (reasons, result dict or None)."""
    if not isinstance(part, dict):
        return ['DECIDING_%s_NOT_PINNED' % label.upper()], None
    for k in ('result', 'receipt'):
        p = part.get(k)
        if not isinstance(p, dict) or not isinstance(p.get('path'), str) or not isinstance(p.get('sha256'), str):
            return ['deciding %s: %s {path, sha256} required' % (label, k)], None
    if not isinstance(part.get('finish_path'), str) or not isinstance(part.get('call_spec_sha256'), str):
        return ['deciding %s: finish_path and call_spec_sha256 required' % label], None
    if part['call_spec_sha256'] != expect['spec_sha256']:
        return ['deciding %s: call_spec_sha256 %s is not the deciding spec %s' % (label, part['call_spec_sha256'][:16],
                                                                                 expect['spec_sha256'][:16])], None
    try:
        rraw = read_pinned(part['result'], 'deciding %s result' % label)
        r = json.loads(rraw.decode('utf-8'))
        fin = load_json_file(part['finish_path'], 'deciding %s finish' % label)
    except (OrchestratorError, ValueError) as exc:
        return ['deciding %s: %s' % (label, exc)], None
    reasons = []
    if fin.get('result_sha256') != part['result']['sha256']:
        reasons.append('deciding %s: finish.json result_sha256 != sha256(result.json)' % label)
    try:
        bad = _receipt_ok(mon, part['receipt'], expect['spec_sha256'], driver_sha, part['result'], 'deciding %s' % label)
    except OrchestratorError as exc:
        bad = str(exc)
    if bad:
        reasons.append('deciding %s: %s' % (label, bad))
    if r.get('driver_sha256') != driver_sha:
        reasons.append('deciding %s: driver_sha256 %s is not the config driver %s' % (label, str(r.get('driver_sha256'))[:16],
                                                                                     driver_sha[:16]))
    if r.get('call_spec_sha256') != expect['spec_sha256']:
        reasons.append('deciding %s: result call_spec_sha256 is not the deciding spec' % label)
    if r.get('status') != 'COMPLETED':
        reasons.append('deciding %s: status %r is not COMPLETED' % (label, r.get('status')))
    return reasons, r


def check_deciding(dt, driver_sha256, mon, synthetic=False):
    """C5: BOTH driver deciding tests must pass from bytes.
    (i) ADMIT_PREFIX: deciding_test.verdict PASS_BITWISE_EQUAL; route_a_outcome CONVERGED at 4; custody iteration 4,
        solver 44d9c23c, attempt_link {98816902.., 01792161909921426000-19994-831a3fbc}, source profile f5becd45; no
        geometry key.
    (ii) full anchor: the pinned comparator report (schema, comparator sha, reference run, new run = the pinned result's
        directory, expect_new parallel, column_workers = the result's numerics.route_a.column_workers, the 13 checks all
        pass, verdict PASS_BITWISE_EQUAL, nothing failing); route_a implementation column_workers equal.
    Returns the gate dict; gate['route_a_column_workers_verified'] = N of (ii) when (ii) passes."""
    out = {'ok': False, 'reasons': [], 'required_verdict': REQUIRED_VERDICT, 'parts': {}}
    if not isinstance(dt, dict):
        out['reasons'].append('DECIDING_TEST_NOT_PINNED: config deciding_test is absent')
        return out
    extra = set(dt) - set(DECIDING_EXPECT) - ({'synthetic_expect'} if synthetic else set())
    if extra:
        out['reasons'].append('deciding_test: unknown keys %s' % sorted(extra))
        return out
    expect = copy.deepcopy(DECIDING_EXPECT)
    if 'synthetic_expect' in dt:
        if not synthetic:
            out['reasons'].append('deciding_test.synthetic_expect is allowed only in a synthetic_test config')
            return out
        for k, v in (dt['synthetic_expect'] or {}).items():
            if k in expect:
                expect[k].update(v)
    # (i)
    ri, r = _deciding_run(dt.get('i_admit_prefix'), 'i_admit_prefix', driver_sha256, mon, expect['i_admit_prefix'])
    ei = expect['i_admit_prefix']
    if r is not None:
        verdict = (r.get('deciding_test') or {}).get('verdict')
        oc = r.get('route_a_outcome') or {}
        cust = ((r.get('identity') or {}).get('route_a') or {}).get('custody') or {}
        link = cust.get('attempt_link') or {}
        if verdict != REQUIRED_VERDICT:
            ri.append('deciding i: deciding_test.verdict %r != %s' % (verdict, REQUIRED_VERDICT))
        if oc.get('classification') != 'CONVERGED' or oc.get('converged_iteration') != ei['route_a_converged_iteration']:
            ri.append('deciding i: route_a_outcome %r at %r is not CONVERGED at %d'
                      % (oc.get('classification'), oc.get('converged_iteration'), ei['route_a_converged_iteration']))
        if cust.get('iteration') != ei['route_a_converged_iteration']:
            ri.append('deciding i: custody iteration %r != %d' % (cust.get('iteration'), ei['route_a_converged_iteration']))
        if (cust.get('solver_code') or {}).get('sha256') != ei['solver_sha256']:
            ri.append('deciding i: custody solver_code is not %s' % ei['solver_sha256'][:16])
        if {k: link.get(k) for k in ('identity_sha256', 'attempt')} != ei['attempt_link']:
            ri.append('deciding i: custody attempt_link %r is not %r' % ({k: link.get(k) for k in ('identity_sha256', 'attempt')},
                                                                         ei['attempt_link']))
        if cust.get('source_profile_sha256') != ei['source_profile_sha256']:
            ri.append('deciding i: custody source_profile_sha256 is not %s' % ei['source_profile_sha256'][:16])
        if 'geometry' in r:
            ri.append('deciding i: result carries a geometry key (registered distance required)')
        out['parts']['i_admit_prefix'] = {'ok': not ri, 'reasons': ri, 'verdict': verdict,
                                          'result_sha256': dt['i_admit_prefix']['result']['sha256']}
    else:
        out['parts']['i_admit_prefix'] = {'ok': False, 'reasons': ri}
    # (ii)
    part = dt.get('ii_full_anchor')
    rii, r2 = _deciding_run(part, 'ii_full_anchor', driver_sha256, mon, expect['ii_full_anchor'])
    eii = expect['ii_full_anchor']
    n_verified = None
    if r2 is not None:
        cpin = part.get('comparator')
        if cpin is not None:                      # optional config pin of the comparator (S4): must be the expected bytes
            try:
                ok_c = (isinstance(cpin, dict) and cpin.get('sha256') == eii['comparator_sha256']
                        and sha256_file(cpin.get('path')) == eii['comparator_sha256'])
            except (OSError, TypeError):
                ok_c = False
            if not ok_c:
                rii.append('deciding ii: S4 config comparator pin is not the comparator %s from bytes'
                           % eii['comparator_sha256'][:16])
        cp = part.get('compare_report')
        try:
            rep = json.loads(read_pinned(cp, 'deciding ii compare_report').decode('utf-8'))
        except (OrchestratorError, ValueError) as exc:
            rep = None
            rii.append('deciding ii: %s' % exc)
        n = (((r2.get('normalized_spec') or {}).get('numerics') or {}).get('route_a') or {}).get('column_workers')
        impl = (((r2.get('identity') or {}).get('route_a') or {}).get('implementation') or {})
        if rep is not None:
            checks = rep.get('checks') or {}
            if rep.get('schema') != eii['compare_schema']:
                rii.append('deciding ii: compare report schema %r' % rep.get('schema'))
            if (rep.get('comparator') or {}).get('sha256') != eii['comparator_sha256']:
                rii.append('deciding ii: comparator sha256 is not %s' % eii['comparator_sha256'][:16])
            # S4: the comparator FILE is hashed from bytes (the report's own sha field is a claim about itself)
            cpath = (rep.get('comparator') or {}).get('path')
            try:
                csha = sha256_file(cpath) if isinstance(cpath, str) and os.path.isabs(cpath) else None
            except OSError:
                csha = None
            if csha != eii['comparator_sha256']:
                rii.append('deciding ii: S4 comparator file %r does not hash to %s from bytes (got %s)'
                           % (cpath, eii['comparator_sha256'][:16], str(csha)[:16]))
            if os.path.basename(str(rep.get('reference', '')).rstrip('/')) != eii['reference_run_name']:
                rii.append('deciding ii: reference run %r is not %s' % (rep.get('reference'), eii['reference_run_name']))
            # S4: the reference must BE the pinned anchor run (realpath) and its result.json must hash to the pin
            ref = rep.get('reference')
            if not isinstance(ref, str) or os.path.realpath(ref) != os.path.realpath(eii['reference_path']):
                rii.append('deciding ii: S4 reference %r does not resolve to the pinned %s' % (ref, eii['reference_path']))
            else:
                try:
                    rsha = sha256_file(os.path.join(os.path.realpath(ref), 'result.json'))
                except OSError:
                    rsha = None
                if rsha != eii['reference_result_sha256']:
                    rii.append('deciding ii: S4 reference result.json does not hash to %s from bytes (got %s)'
                               % (eii['reference_result_sha256'][:16], str(rsha)[:16]))
            if os.path.realpath(str(rep.get('new', ''))) != os.path.realpath(os.path.dirname(part['result']['path'])):
                rii.append('deciding ii: compare report new run is not the pinned result directory')
            if rep.get('expect_new') != 'parallel':
                rii.append('deciding ii: compare expect_new %r != parallel' % rep.get('expect_new'))
            if type(n) is not int or n < 2 or rep.get('column_workers') != n or impl.get('column_workers') != n:
                rii.append('deciding ii: route_a column_workers inconsistent (spec %r, report %r, implementation %r)'
                           % (n, rep.get('column_workers'), impl.get('column_workers')))
            missing = [c for c in eii['required_checks'] if (checks.get(c) or {}).get('pass') is not True]
            if missing:
                rii.append('deciding ii: checks not passing: %s' % missing)
            if rep.get('verdict') != REQUIRED_VERDICT or rep.get('failing'):
                rii.append('deciding ii: verdict %r failing %r' % (rep.get('verdict'), rep.get('failing')))
        if r2.get('valid') is not True:
            rii.append('deciding ii: result valid is not true')
        if not rii:
            n_verified = n
        out['parts']['ii_full_anchor'] = {'ok': not rii, 'reasons': rii, 'route_a_column_workers': n,
                                          'result_sha256': part['result']['sha256'],
                                          'compare_report_sha256': (cp or {}).get('sha256'),
                                          'comparator_sha256_from_bytes': eii['comparator_sha256'] if not rii else None,
                                          'reference_result_sha256_from_bytes': eii['reference_result_sha256']
                                          if not rii else None}
    else:
        out['parts']['ii_full_anchor'] = {'ok': False, 'reasons': rii}
    out['route_a_column_workers_verified'] = n_verified
    out['ok'] = all(p['ok'] for p in out['parts'].values()) and len(out['parts']) == 2
    out['reasons'] = (['BOTH deciding tests PASS from bytes ((i) ADMIT_PREFIX, (ii) full anchor with comparator)']
                      if out['ok'] else [x for p in out['parts'].values() for x in p['reasons']])
    return out


def _finite_positive(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x > 0


def check_numerics(ncfg, template_numerics, deciding_route_a_n, synthetic=False):
    """C8 numerics gate, v005 C4-5 (Claude4 R-B): returns (block, gate).  It READS the convergence verdict.
      * numerics = {block, verdict_artifact, block_source, note}; verdict_artifact = the k_max comparison report
        (kmax_compare_c2v005.py: schema UNT_KMAX_COMPARISON_C2_V005), block_source = the adopted case's call spec.
      * the report's prereg is verified from bytes (path + sha256 in the report); a non-synthetic config needs the sealed
        prereg (KMAX_PREREG_SHA256) and test_mode false;
      * decision.outcome must be ADOPT (kmax_compare_c2v005.py:468); the adopted case is the one prereg case with
        shape = decision.adopted_shape on grid = decision.adopted_grid (kmax_inverse_kpc null or the adopted value); it must
        be gate-valid (gates[case].valid_all) and sha256(block_source bytes) must equal inputs[case].call_spec_sha256;
      * the block must equal block_source.numerics outside numerics.route_a (execution only: the route-A pool size, whose
        column_workers must be 1 or the N deciding (ii) verified); its truncation shape (driver c2v008 default cube when
        absent) must be the adopted shape; picard.speed_change_bound_km_s must be a finite positive number (B1-F5)."""
    gate = {'ok': False, 'reasons': [], 'binding': None, 'execution_overrides': {}}
    if ncfg is None:
        gate['reasons'].append('NUMERICS_NOT_PINNED: config numerics is null (the template numerics would be used)')
        return copy.deepcopy(template_numerics), gate
    if not isinstance(ncfg, dict) or set(ncfg) - NUMERICS_KEYS:
        raise OrchestratorError('numerics must be {block, verdict_artifact, block_source, note} (v005 C4-5: block_pointer '
                                'and root_attestation are replaced by block_source, the adopted case call spec)')
    block = ncfg.get('block')
    if not isinstance(block, dict):
        raise OrchestratorError('numerics.block must be the call-spec numerics object')
    block = copy.deepcopy(block)
    gate['block_sha256'] = sha256_bytes(canonical(block))
    R = gate['reasons']
    pc = block.get('picard') or {}
    if not _finite_positive(pc.get('speed_change_bound_km_s')):
        R.append('NUMERICS_PICARD_BOUND_NOT_DECLARED: numerics.block.picard.speed_change_bound_km_s %r must be a finite '
                 'positive number (B1-F5: a null bound makes every COMPLETED call VALID without a convergence check)'
                 % (pc.get('speed_change_bound_km_s'),))
    art, src = ncfg.get('verdict_artifact'), ncfg.get('block_source')
    if not isinstance(art, dict):
        R.append('NUMERICS_VERDICT_NOT_PINNED: numerics.verdict_artifact {path, sha256} (the k_max comparison report) is '
                 'absent')
        return block, gate
    if not isinstance(src, dict):
        R.append('NUMERICS_BLOCK_SOURCE_NOT_PINNED: numerics.block_source {path, sha256} (the adopted case call spec) is '
                 'absent')
        return block, gate
    try:
        rep = json.loads(read_pinned(art, 'numerics.verdict_artifact').decode('utf-8'))
        sraw = read_pinned(src, 'numerics.block_source')
        sdoc = json.loads(sraw.decode('utf-8'))
    except (OrchestratorError, ValueError) as exc:
        R.append(str(exc)[:300])
        return block, gate
    gate['verdict_artifact'] = {'path': art['path'], 'sha256': art['sha256']}
    gate['block_source'] = {'path': src['path'], 'sha256': src['sha256']}
    if not isinstance(rep, dict) or not isinstance(sdoc, dict):
        R.append('numerics verdict artifact / block source is not a JSON object')
        return block, gate
    dec = rep.get('decision') if isinstance(rep.get('decision'), dict) else {}
    gate['outcome'] = dec.get('outcome')
    if rep.get('schema') not in VERDICT_SCHEMAS:
        R.append('NUMERICS_VERDICT_SCHEMA: %r is not one of %s' % (rep.get('schema'), list(VERDICT_SCHEMAS)))
        return block, gate
    if dec.get('outcome') != 'ADOPT':
        R.append('NUMERICS_VERDICT_NOT_ADOPT: decision.outcome %r (only ADOPT admits a calibration numerics block)'
                 % (dec.get('outcome'),))
        return block, gate
    if not synthetic and rep.get('test_mode') is not False:
        R.append('NUMERICS_VERDICT_TEST_MODE: test_mode %r (a non-synthetic config needs a sealed-prereg verdict)'
                 % (rep.get('test_mode'),))
    pp = rep.get('prereg') if isinstance(rep.get('prereg'), dict) else {}
    try:
        pre = json.loads(read_pinned(pp, 'verdict prereg').decode('utf-8'))
    except (OrchestratorError, ValueError) as exc:
        R.append('NUMERICS_VERDICT_PREREG: %s' % str(exc)[:200])
        return block, gate
    if not synthetic and pp.get('sha256') not in KMAX_PREREG_SHA256:
        R.append('NUMERICS_VERDICT_PREREG: %s is not the sealed prereg %s' % (str(pp.get('sha256'))[:16],
                                                                              [s[:16] for s in KMAX_PREREG_SHA256]))
    shape, grid, kmax = dec.get('adopted_shape'), dec.get('adopted_grid'), dec.get('adopted_kmax_inverse_kpc')
    cases = [c for c in (pre.get('cases') or []) if isinstance(c, dict) and c.get('shape') == shape
             and c.get('grid') == grid and c.get('kmax_inverse_kpc') in (None, kmax)]
    if not isinstance(shape, str) or not isinstance(grid, str) or not _finite_positive(kmax) or len(cases) != 1:
        R.append('NUMERICS_ADOPTED_CASE: decision adopted shape %r grid %r k_max %r name %d prereg cases (exactly 1 '
                 'required)' % (shape, grid, kmax, len(cases)))
        return block, gate
    cid = cases[0].get('id')
    inputs = rep.get('inputs') if isinstance(rep.get('inputs'), dict) else {}
    inp = inputs.get(cid) if isinstance(inputs.get(cid), dict) else {}
    if ((rep.get('gates') or {}).get(cid) or {}).get('valid_all') is not True:
        R.append('NUMERICS_ADOPTED_CASE_NOT_GATE_VALID: gates[%s].valid_all is not true' % cid)
    if inp.get('call_spec_sha256') != src['sha256']:
        R.append('NUMERICS_BLOCK_SOURCE_NOT_ADOPTED_CASE: sha256(block_source) %s != inputs[%s].call_spec_sha256 %s'
                 % (src['sha256'][:16], cid, str(inp.get('call_spec_sha256'))[:16]))
    grid_ids = sorted(c.get('id') for c in (pre.get('cases') or []) if isinstance(c, dict) and c.get('grid') == grid)
    gate['adopted'] = {'case_id': cid, 'shape': shape, 'grid': grid, 'kmax_inverse_kpc': kmax,
                       'call_spec_sha256': src['sha256'], 'verdict_sha256': art['sha256'],
                       'prereg_sha256': pp.get('sha256')}
    gate['grid_case_inputs'] = {g: {k: (inputs.get(g) or {}).get(k) for k in
                                    ('call_spec_sha256', 'driver_sha256', 'result_sha256', 'elapsed_seconds')}
                                for g in grid_ids if isinstance(inputs.get(g), dict)}
    u = dec.get('carried_numerical_uncertainty_km_s')
    gate['u_i_km_s'] = copy.deepcopy(u) if isinstance(u, dict) else None
    snum = sdoc.get('numerics')
    if not isinstance(snum, dict):
        R.append('numerics.block_source carries no numerics object')
        return block, gate
    bad = [p for p in diff_paths(snum, block) if not (p == 'route_a' or p.startswith('route_a.'))]
    if bad:
        R.append('NUMERICS_BLOCK_NOT_ADOPTED: numerics.block differs from block_source.numerics outside numerics.route_a: %s'
                 % bad[:8])
    tshape = (block.get('truncation') or {'shape': 'cube'}).get('shape')
    if tshape != shape:
        R.append('NUMERICS_SHAPE_NOT_ADOPTED: block truncation shape %r != decision.adopted_shape %r' % (tshape, shape))
    if canonical(snum.get('route_a')) != canonical(block.get('route_a')):
        gate['execution_overrides']['route_a'] = {'artifact': snum.get('route_a'), 'run': block.get('route_a')}
    ra = block.get('route_a')
    if ra is not None:
        n = ra.get('column_workers') if isinstance(ra, dict) else None
        if type(n) is not int or n < 1:
            R.append('numerics.route_a.column_workers must be a positive int')
        elif n != 1 and n != deciding_route_a_n:
            R.append('ROUTE_A_COLUMN_WORKERS_NOT_COVERED: numerics.route_a.column_workers %d is neither 1 '
                     '(reviewed serial) nor the value deciding (ii) verified (%r)' % (n, deciding_route_a_n))
    if R:
        return block, gate
    gate['binding'] = 'BLOCK_EQUALS_ADOPTED_CASE_NUMERICS %s (verdict ADOPT %s, shape %s, grid %s, k_max %s)%s' % (
        cid, art['sha256'][:16], shape, grid, kmax,
        (' (execution override numerics.route_a %s, covered by deciding (ii))' % canonical(ra).decode())
        if gate['execution_overrides'] else '')
    gate['ok'] = True
    return block, gate


# --------------------------------------------------------------------------------------------- taxonomy
def _tokens_in(msg, tokens):
    found = []
    for t in tokens:
        if re.search(r'(?<![A-Z0-9_])' + re.escape(t) + r'(?![A-Z0-9_])', msg or ''):
            found.append(t)
    return found


def validate_contraction_test(decl, tax_doc):
    """C2: the root-declared contraction discriminator (or None)."""
    if decl is None:
        return None
    sup = ((tax_doc.get('route_a_contraction_test') or {}).get('supported_rules') or {})
    if not isinstance(decl, dict) or decl.get('rule') not in sup:
        raise OrchestratorError('route_a_contraction_test.rule must be one of %s' % sorted(sup))
    if set(decl) != {'rule', 'n_last', 'threshold', 'judgment_call', 'declared_by', 'basis'}:
        raise OrchestratorError('route_a_contraction_test keys must be rule, n_last, threshold, judgment_call, declared_by, basis')
    if type(decl['n_last']) is not int or decl['n_last'] < 1:
        raise OrchestratorError('route_a_contraction_test.n_last must be an int >= 1')
    t = decl['threshold']
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or t < 1.0:
        # S2: a residual ratio below 1 is contraction by definition; a threshold < 1 would label a contracting route A
        # NON_CONTRACTING (MODEL_INVALID)
        raise OrchestratorError('route_a_contraction_test.threshold must be a finite number >= 1 (S2: a ratio < 1 is '
                                'contraction)')
    if type(decl['judgment_call']) is not bool:
        raise OrchestratorError('route_a_contraction_test.judgment_call must be a bool')
    for k in ('declared_by', 'basis'):
        if not isinstance(decl[k], str) or not decl[k].strip():
            raise OrchestratorError('route_a_contraction_test.%s must be non-empty text' % k)
    return copy.deepcopy(decl)


class Taxonomy:
    """Rule table of FAILURE_TAXONOMY_V003.json, evaluated on (result.json, evidence of the call directory)."""

    def __init__(self, doc, sha256, contraction_test=None):
        if not isinstance(doc, dict) or doc.get('schema') != SCHEMA_TAXONOMY:
            raise OrchestratorError('taxonomy schema must be %s' % SCHEMA_TAXONOMY)
        self.doc, self.sha256 = doc, sha256
        ts = doc['token_sets']
        self.col_tokens = dict(ts['COLUMN_NUMERICS_TOKENS']['tokens'])
        self.hi_tokens = dict(ts['HI_NUMERICS_TOKENS']['tokens'])
        self.nonfinite = dict(ts['ROUTE_A_WORKER_NONFINITE_MESSAGES']['messages'])
        self.pool_types = list(ts['ROUTE_A_POOL_FAILURE_TYPES']['types'])
        self.rules = list(doc['rules'])
        self.never_invalid = tuple(sorted(set(NEVER_INVALID_PREFIXES) |
                                          set((doc.get('never_resolve_invalid_code_prefixes') or {}).get('prefixes') or [])))
        self.contraction_test = validate_contraction_test(contraction_test, doc)
        if doc['default']['class'] != 'INFRA':
            raise OrchestratorError('taxonomy default class must be INFRA')
        for r in self.rules:
            if r['class'] not in CLASSES or r['condition'] not in self.CONDITIONS:
                raise OrchestratorError('taxonomy rule %s: unknown class or condition' % r.get('id'))

    def never_invalid_code(self, code):
        return any(str(code or '').startswith(p) for p in self.never_invalid)

    # -- helpers
    def _tok_all(self, msgs, table):
        toks = []
        for m in msgs:
            t = _tokens_in(m, table)
            if not t:
                return None
            toks.append(t[0])
        return toks or None

    def _col_judgment(self, toks):
        return any(not self.col_tokens[t].get('root_specified') for t in toks)

    @staticmethod
    def _ra(ev):
        return ev.get('route_a') or {}

    @staticmethod
    def _oc(ev):
        return ev.get('route_a_outcome') or {}

    @staticmethod
    def _full_chain(ra):
        mx = ra.get('max_iterations')
        return (isinstance(mx, int) and mx > 0 and ra.get('iterations') == list(range(mx))
                and ra.get('completed') == list(range(mx)) and ra.get('converged') == []
                and ra.get('iteration_records_bound') is True)

    def contraction(self, hist):
        """C2: evaluate the declared test on the residual history (None if not declared)."""
        r = [h['residual_J'] for h in hist]
        ratios = [r[i] / r[i - 1] for i in range(1, len(r))]
        out = {'ratios': ratios, 'last_residual_over_bound': hist[-1]['residual_J'] / hist[-1]['bound_J']}
        if ratios and ratios[-1] < 1.0:
            out['iterations_to_bound_at_last_ratio_informational'] = (
                math.log(out['last_residual_over_bound']) / -math.log(ratios[-1]) if out['last_residual_over_bound'] > 1 else 0.0)
        d = self.contraction_test
        if d is None:
            out['verdict'] = 'NO_DISCRIMINATOR_DECLARED'
            return out
        last = ratios[-d['n_last']:] if len(ratios) >= d['n_last'] else None
        out['verdict'] = 'NON_CONTRACTING' if (last is not None and all(q >= d['threshold'] for q in last)) else 'CONTRACTING'
        out['declared_test'] = copy.deepcopy(d)
        return out

    # -- conditions: (matched, fill, override dict or None)
    def c_always(self, res, ev):
        return True, '', None

    def c_valid_true_rows_finite_bound_met(self, res, ev):
        sp = res.get('speeds_km_s')
        if res.get('valid') is not True or not isinstance(sp, dict):
            return False, '', None
        rows = [sp.get(r) for r in ev['row_ids']]
        ok = all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in rows)
        if not self._bound_met(ev, res):
            ok = False                                         # C1 (unknown or unmet bound -> not VALID)
        return ok, '', None

    @staticmethod
    def _bound_met(ev, res):
        """C1: no bound declared -> True.  With a declared bound: the driver's picard_bound_met must be true AND the final
        pass's own max_abs_change_km_s (result bytes) must be a finite number <= the bound (cross-check)."""
        pc = ev.get('picard') or {}
        if pc.get('bound_declared') is False:
            return True
        if pc.get('bound_declared') is not True or res.get('picard_bound_met') is not True:
            return False
        chg, b = pc.get('final_max_abs_change_km_s'), pc.get('bound_km_s')
        return (isinstance(chg, (int, float)) and not isinstance(chg, bool) and math.isfinite(chg)
                and isinstance(b, (int, float)) and not isinstance(b, bool) and chg <= b)

    def c_completed_declared_bound_not_met(self, res, ev):
        pc = ev.get('picard') or {}
        if pc.get('bound_declared') is True and not self._bound_met(ev, res):
            return True, '', {'detail': {'picard': pc, 'passes': ev.get('passes_history')}}
        return False, '', None

    def c_route_a_no_fixed_point_budget_exhausted(self, res, ev):
        ra, oc = self._ra(ev), self._oc(ev)
        hist = ra.get('residual_history') or []
        ok = (oc.get('outcome') == 'ITERATION_BUDGET_EXHAUSTED' and ra.get('end_outcomes') == ['ITERATION_BUDGET_EXHAUSTED']
              and ra.get('end_identities_bound') is True and self._full_chain(ra)
              and [h.get('iteration') for h in hist] == list(range(ra['max_iterations']))
              and all(isinstance(h.get('residual_J'), float) and math.isfinite(h['residual_J']) and h['residual_J'] > 0
                      and isinstance(h.get('bound_J'), float) and math.isfinite(h['bound_J']) and h['bound_J'] > 0
                      for h in hist))
        if not ok:
            return False, '', None
        c = self.contraction(hist)
        detail = {'residual_history': hist, 'contraction': c}
        if c['verdict'] == 'NON_CONTRACTING':
            return True, '', {'class': 'MODEL_INVALID', 'code': 'ROUTE_A_NON_CONTRACTING_WITHIN_MAX_ITERATIONS',
                              'judgment_call': bool(self.contraction_test['judgment_call']), 'detail': detail}
        return True, '', {'class': 'NUMERICS_LIMITED', 'code': 'ROUTE_A_ITERATION_BUDGET_EXHAUSTED_%s' % c['verdict'],
                          'judgment_call': True, 'detail': detail}

    def c_route_a_no_fixed_point_fsp_numerics_tokens(self, res, ev):
        ra, oc = self._ra(ev), self._oc(ev)
        if oc.get('outcome') != 'FAILED_SOURCE_PREPARATION' or ra.get('end_outcomes') != ['FAILED_SOURCE_PREPARATION'] \
                or ra.get('end_identities_bound') is not True:
            return False, '', None
        msgs = [str((oc.get('failure') or {}).get('message', ''))] + list(ra.get('failure_messages') or [])
        toks = self._tok_all(msgs, self.hi_tokens)
        if not toks:
            return False, '', None
        return True, '+'.join(sorted(set(toks))), None

    def c_attempt_link_refused_iteration_cap_without_end_record(self, res, ev):
        ra = self._ra(ev)
        r0 = (ev.get('reasons') or [''])[0]
        ok = (r0.startswith('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT') and ra.get('present') is True
              and ra.get('end_outcomes') == [] and self._full_chain(ra))
        return ok, '', None

    def c_route_a_worker_raised_nonfinite(self, res, ev):
        ra = self._ra(ev)
        msg = (ra.get('attempt_failure') or {}).get('message')
        ok = (ev.get('failed_stages') or []) == ['route_a'] and ra.get('end_outcomes') == [] and msg in self.nonfinite
        return ok, str(msg), None

    def c_route_a_worker_pool_failure(self, res, ev):
        ra = self._ra(ev)
        af = ra.get('attempt_failure') or {}
        ok = (ev.get('failed_stages') or []) == ['route_a'] and af.get('type') in self.pool_types
        return ok, str(af.get('message'))[:100], None

    def c_rotation_missing_columns_numerics_tokens(self, res, ev):
        fs = ev.get('failed_stages') or []
        if len(fs) != 1 or not fs[0].endswith('_rotation'):
            return False, '', None
        tag = fs[0][:-len('_rotation')]
        sf = (ev.get('stage_failures') or {}).get(fs[0]) or {}
        if not str(sf.get('message', '')).startswith('Missing complete'):
            return False, '', None
        msgs = (ev.get('column_failures') or {}).get(tag)
        if not msgs or (ev.get('column_finish_missing') or {}).get(tag):
            return False, '', None
        toks = self._tok_all(msgs, self.col_tokens)
        if not toks:
            return False, '', None
        return True, '%s:%s' % (tag, '+'.join(sorted(set(toks)))), {'judgment_call': self._col_judgment(toks)}

    def c_bracket_source_missing_numerics_tokens(self, res, ev):
        for r in ev.get('reasons') or []:
            m = re.match(r'^(\w+) column\(s\) \[.*\] failed; no bracket source$', r)
            if not m:
                continue
            tag = m.group(1)
            msgs = (ev.get('column_failures') or {}).get(tag)
            if not msgs or (ev.get('column_finish_missing') or {}).get(tag):
                return False, '', None
            toks = self._tok_all(msgs, self.col_tokens)
            if not toks:
                return False, '', None
            return True, '%s:%s' % (tag, '+'.join(sorted(set(toks)))), {'judgment_call': self._col_judgment(toks)}
        return False, '', None

    def c_body_reference_roster_numerics_tokens(self, res, ev):
        fs = ev.get('failed_stages') or []
        if fs != ['body']:
            return False, '', None
        sf = (ev.get('stage_failures') or {}).get('body') or {}
        if not str(sf.get('message', '')).startswith('Full exact saved'):
            return False, '', None
        toks = self._tok_all(ev.get('reference_failures') or [], self.hi_tokens)
        if not toks:
            return False, '', None
        return True, '+'.join(sorted(set(toks))), None

    def c_final_pass_nonpositive_rotation(self, res, ev):
        """R30 (taxonomy V003, CHECK_SCIENCE_V001 S1).  No bound declared: MODEL_INVALID (not a judgment call).  A bound
        declared: a nonpositive pass yields no column-mean rows, so the bound can never stop the loop there.
          * no recorded pass produced positive rotation -> MODEL_INVALID (judgment call, C3);
          * an earlier pass produced positive rotation   -> NUMERICS_LIMITED FINAL_PICARD_ITERATE_NONPOSITIVE_UNCONVERGED
            (the final state may be an unconverged iterate: HALT; root resolves invalid or retry);
          * the pass history is unreadable (a pass without a bool rotation_positive) -> INFRA."""
        fp = ev.get('final_pass') or {}
        if fp.get('rotation_positive') is not False:
            return False, '', None
        hist = ev.get('passes_history') or []
        bd = (ev.get('picard') or {}).get('bound_declared') is not False
        detail = {'picard': ev.get('picard'), 'passes': hist}
        if not bd:
            return True, '', {'judgment_call': False, 'detail': dict(detail, judgment='no bound declared')}
        flags = [h.get('rotation_positive') for h in hist]
        if not hist or any(type(f) is not bool for f in flags):
            return True, '', {'class': 'INFRA', 'code': 'FINAL_PASS_NONPOSITIVE_PASS_HISTORY_UNREADABLE',
                              'judgment_call': False,
                              'detail': dict(detail, judgment='S1: the pass history does not establish whether any '
                                                              'pass produced positive rotation')}
        positive = [h.get('pass') for h in hist if h.get('rotation_positive') is True]
        if positive:
            return True, '', {'class': 'NUMERICS_LIMITED', 'code': 'FINAL_PICARD_ITERATE_NONPOSITIVE_UNCONVERGED',
                              'judgment_call': True,
                              'detail': dict(detail, positive_passes=positive,
                                             judgment='S1: a bound is declared and pass(es) %s produced positive '
                                                      'rotation; the nonpositive final state may be an unconverged '
                                                      'Picard iterate (HALT; root resolves)' % positive)}
        return True, '', {'judgment_call': True,
                          'detail': dict(detail, positive_passes=[],
                                         judgment='S1/C3: a bound is declared and no recorded pass produced positive '
                                                  'rotation (%d passes); MODEL_INVALID, a judgment call' % len(hist))}

    def c_final_column_mean_invalid_rotation(self, res, ev):
        fp = ev.get('final_pass') or {}
        msg = str((fp.get('column_mean_failure') or {}).get('message', ''))
        return msg.startswith('Invalid finite positive rotation'), '', None

    def c_final_pass_column_failures_numerics_tokens(self, res, ev):
        fp = ev.get('final_pass') or {}
        msgs = [str(f.get('message', '')) for f in (fp.get('column_failures') or [])]
        if not msgs:
            return False, '', None
        toks = self._tok_all(msgs, self.col_tokens)
        if not toks:
            return False, '', None
        return True, 'final:%s' % '+'.join(sorted(set(toks))), {'judgment_call': self._col_judgment(toks)}

    def c_blocked_geometry_not_admitted_by_stage_binding(self, res, ev):
        return any('GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING' in r for r in (ev.get('reasons') or [])), '', None

    CONDITIONS = {
        'always': c_always,
        'valid_true_rows_finite_bound_met': c_valid_true_rows_finite_bound_met,
        'completed_declared_bound_not_met': c_completed_declared_bound_not_met,
        'route_a_no_fixed_point_budget_exhausted': c_route_a_no_fixed_point_budget_exhausted,
        'route_a_no_fixed_point_fsp_numerics_tokens': c_route_a_no_fixed_point_fsp_numerics_tokens,
        'attempt_link_refused_iteration_cap_without_end_record': c_attempt_link_refused_iteration_cap_without_end_record,
        'route_a_worker_raised_nonfinite': c_route_a_worker_raised_nonfinite,
        'route_a_worker_pool_failure': c_route_a_worker_pool_failure,
        'rotation_missing_columns_numerics_tokens': c_rotation_missing_columns_numerics_tokens,
        'bracket_source_missing_numerics_tokens': c_bracket_source_missing_numerics_tokens,
        'body_reference_roster_numerics_tokens': c_body_reference_roster_numerics_tokens,
        'final_pass_nonpositive_rotation': c_final_pass_nonpositive_rotation,
        'final_column_mean_invalid_rotation': c_final_column_mean_invalid_rotation,
        'final_pass_column_failures_numerics_tokens': c_final_pass_column_failures_numerics_tokens,
        'blocked_geometry_not_admitted_by_stage_binding': c_blocked_geometry_not_admitted_by_stage_binding,
    }

    def classify(self, res, ev):
        """-> {class, code, rule, judgment_call, detail}.  Never on status alone; unmatched -> INFRA."""
        status = res.get('status')
        reasons = [str(x) for x in (res.get('reasons') or [])]
        ev = dict(ev, reasons=reasons)
        if ev.get('errors'):
            return {'class': 'INFRA', 'code': 'EVIDENCE_UNREADABLE:%s' % ev['errors'][0][:120], 'rule': 'EVIDENCE',
                    'judgment_call': False, 'detail': None}
        first = reasons[0][:120] if reasons else ''
        for r in self.rules:
            if status not in r['statuses']:
                continue
            ok, fill, ov = self.CONDITIONS[r['condition']](self, res, ev)
            if not ok:
                continue
            ov = ov or {}
            code = ov.get('code', r['code'])
            if '<' in code:
                # v005 C4-1 (B1-F3): re.sub with a FUNCTION -- the fill is a driver reason, never a replacement template
                # ('\1', '\q' raised in c2v004a); one pass: the rule's first placeholder gets the fill, any other
                # placeholder of the rule is removed, and the fill text itself is never re-scanned ('<...>' kept)
                _n = [0]

                def _fill(_m, _f=(fill or first)):
                    _n[0] += 1
                    return _f if _n[0] == 1 else ''
                code = re.sub(r'<[^>]*>', _fill, code)
            jc = ov.get('judgment_call', r.get('judgment_call') is True)
            return {'class': ov.get('class', r['class']), 'code': code[:200], 'rule': r['id'], 'judgment_call': bool(jc),
                    'detail': ov.get('detail')}
        return {'class': 'INFRA', 'code': ('UNRECOGNIZED:%s:%s' % (status, first))[:200], 'rule': 'DEFAULT',
                'judgment_call': False, 'detail': None}


def collect_evidence(outdir, res, row_ids, taxonomy):
    """Read-only evidence from one call directory (driver c2v008 layout: <outdir>/stages/NN_<name>/...).  Every file read
    is recorded with its sha256 (bound into the cache entry and re-derived on every open, C9).  The 44 MB route-A attempt
    result.json is not read: result.route_a_outcome carries its classification record (driver L2253-2257)."""
    outdir = Path(outdir)
    ev = {'files': {}, 'errors': [], 'row_ids': list(row_ids)}

    def rd(p):
        raw = Path(p).read_bytes()
        ev['files'][str(p)] = sha256_bytes(raw)
        return raw

    def rj(p):
        return json.loads(rd(p).decode('utf-8'))

    try:
        # the call spec the driver ran (bound to the result) -> the declared Picard bound (C1, C3)
        csp = outdir / 'inputs' / 'call_spec.json'
        craw = rd(csp)
        if sha256_bytes(craw) != res.get('call_spec_sha256'):
            ev['errors'].append('CALL_SPEC_NOT_BOUND: %s does not hash to result.call_spec_sha256' % csp)
            return ev
        cspec = json.loads(craw.decode('utf-8'))
        pc = ((cspec.get('numerics') or {}).get('picard') or {})
        bound = pc.get('speed_change_bound_km_s')
        fps = res.get('passes') or []
        ev['picard'] = {'bound_declared': bound is not None, 'bound_km_s': bound, 'passes_cap': pc.get('passes', 3),
                        'picard_bound_met': res.get('picard_bound_met'), 'passes_realized': len(fps),
                        'final_max_abs_change_km_s': (fps[-1].get('max_abs_change_km_s') if fps else None)}
        stages = outdir / 'stages'
        sdirs = sorted(d for d in stages.iterdir() if d.is_dir()) if stages.is_dir() else []

        def stage_named(name):
            return [d for d in sdirs if '_' in d.name and d.name.split('_', 1)[1] == name]
        # route A (computed by this call)
        ra = {'present': False}
        rad = stage_named('route_a')
        if rad:
            sd = rad[0]
            cp, att = sd / 'checkpoint', sd / 'attempt_000'
            ra['present'] = cp.is_dir()
            ident = rj(cp / 'IDENTITY.json').get('identity_sha256') if (cp / 'IDENTITY.json').is_file() else None
            ra['identity_sha256'] = ident
            ends = sorted((cp / 'attempts').glob('*.end.json')) if (cp / 'attempts').is_dir() else []
            erecs = [rj(p) for p in ends]
            ra['end_outcomes'] = [str(e.get('outcome')) for e in erecs]
            ra['end_identities_bound'] = bool(ident) and all(e.get('identity_sha256') == ident for e in erecs)
            its = []
            if cp.is_dir():
                for x in sorted(cp.iterdir()):
                    if x.is_dir() and x.name.startswith('iteration_') and re.fullmatch(r'\d{4}', x.name[10:]):
                        its.append(int(x.name[10:]))
            ra['iterations'] = its
            comp, conv, fmsgs, hist, bound_ok = [], [], [], [], True
            for i in its:
                d = cp / ('iteration_%04d' % i)
                if (d / 'COMPLETED.json').is_file():
                    c = rj(d / 'COMPLETED.json')
                    comp.append(i)
                    if c.get('converged') is True:
                        conv.append(i)
                    if c.get('identity_sha256') != ident or c.get('iteration') != i:
                        bound_ok = False
                    hist.append({'iteration': i, 'residual_J': decode_ck_float(c.get('gas_fourier_residual_J')),
                                 'bound_J': decode_ck_float(c.get('bound_J'))})
                for fp in sorted(d.glob('FAILURE.*.json')):
                    txt = rd(fp).decode('utf-8', 'replace')
                    toks = _tokens_in(txt, taxonomy.hi_tokens) if taxonomy else []
                    fmsgs.append(' '.join(toks) if toks else txt[:300])
            ra['completed'], ra['converged'], ra['failure_messages'] = comp, conv, fmsgs
            ra['residual_history'] = hist
            ra['iteration_records_bound'] = bool(ident) and bound_ok
            if (att / 'failure.json').is_file():
                f = rj(att / 'failure.json')
                ra['attempt_failure'] = {'type': f.get('type'), 'message': f.get('message')}
            if (att / 'finish.json').is_file():
                ra['attempt_finish_status'] = rj(att / 'finish.json').get('status')
            mx = None
            if (sd / 'request.json').is_file():
                req = rj(sd / 'request.json')
                argv = [str(a) for a in req.get('argv') or []]
                if '--seed' in argv and argv.index('--seed') + 1 < len(argv):
                    sp = Path(argv[argv.index('--seed') + 1])
                    if sp.is_file():
                        v = rj(sp).get('numerical_inputs', {}).get('max_iterations')
                        mx = v if type(v) is int else None
            ra['max_iterations'] = mx
        ev['route_a'] = ra
        oc = res.get('route_a_outcome')
        ev['route_a_outcome'] = ({k: oc.get(k) for k in ('outcome', 'classification', 'converged_iteration',
                                                          'iterations_completed', 'failure')}
                                 if isinstance(oc, dict) else None)
        # failed stages and their failure records
        failed = []
        for r in res.get('reasons') or []:
            m = re.match(r'^stage\(s\) exited nonzero: (\[.*\])$', str(r))
            if m:
                try:
                    failed = [str(x) for x in ast.literal_eval(m.group(1))]
                except (ValueError, SyntaxError):
                    failed = ['UNPARSEABLE']
        ev['failed_stages'] = failed
        sf = {}
        for name in failed:
            for d in stage_named(name):
                cands = sorted(d.glob('*/failure.json'))
                if cands:
                    f = rj(cands[0])
                    sf[name] = {'type': f.get('type'), 'message': f.get('message')}
        ev['stage_failures'] = sf
        cf, cmiss = {}, {}
        for d in sdirs:
            m = re.fullmatch(r'\d+_(\w+?)_columns_\d+', d.name)
            if not m:
                continue
            tag = m.group(1)
            fin = d / 'columns' / 'finish.json'
            if fin.is_file():
                cf.setdefault(tag, []).extend(str(x.get('message', '')) for x in rj(fin).get('failures') or [])
            else:
                cmiss[tag] = True
        ev['column_failures'], ev['column_finish_missing'] = cf, cmiss
        rf = []
        for d in stage_named('reference'):
            fin = d / 'reference' / 'finish.json'
            if fin.is_file():
                rf.extend(str(x.get('message', '')) for x in rj(fin).get('failures') or [])
        ev['reference_failures'] = rf
        # Picard pass history (C3) and the final pass, from result.json itself
        passes = res.get('passes') or []
        ev['passes_history'] = [{'pass': p.get('pass'), 'rotation_positive': p.get('rotation_positive'),
                                 'max_abs_change_km_s': p.get('max_abs_change_km_s'),
                                 'n_column_failures': len(p.get('column_failures') or []),
                                 'column_mean_status': (p.get('column_mean') or {}).get('status')
                                 if isinstance(p.get('column_mean'), dict) else p.get('column_mean')}
                                for p in passes]
        if passes:
            fp = passes[-1]
            ev['final_pass'] = {'pass': fp.get('pass'), 'rotation_positive': fp.get('rotation_positive'),
                                'column_failures': fp.get('column_failures') or [],
                                'column_mean_failure': fp.get('column_mean_failure')}
    except Exception as exc:   # unreadable evidence -> INFRA (never a guess)
        ev['errors'].append('%s: %s' % (type(exc).__name__, exc))
    return ev


def forward_from_result(res, classification, failure_class, rule, row_ids):
    """The engine-facing forward record, a pure function of result.json bytes + the class (F2 re-derivation)."""
    if classification == 'VALID':
        sp = res['speeds_km_s']
        return {'valid': True, 'speeds_km_s': {rid: sp[rid] for rid in row_ids}, 'reasons': []}
    if classification == 'MODEL_INVALID':
        return {'valid': False, 'speeds_km_s': {},
                'reasons': ['MODEL_INVALID %s (taxonomy %s)' % (failure_class, rule), 'DRIVER_STATUS %s' % res.get('status')]
                + [str(x)[:300] for x in (res.get('reasons') or [])[:4]]}
    raise OrchestratorError('no forward record for class %s' % classification)


def tax_record(out, taxonomy):
    return {'rule': out['rule'], 'code': out['code'], 'class': out['class'], 'judgment_call': out['judgment_call'],
            'detail': out.get('detail'), 'taxonomy_sha256': taxonomy.sha256}


def halt_token(cache_id, wave, key, call_index, cls, reason, launch_ordinal):
    """M2: a wave-and-key-specific authorization token (deterministic, so an idempotent HALT rewrite reproduces it)."""
    return sha256_bytes(canonical({'schema': SCHEMA_TOKEN, 'cache_id': cache_id, 'wave': int(wave), 'key': key,
                                   'call_index': int(call_index), 'class': cls, 'reason': str(reason),
                                   'launch_ordinal': int(launch_ordinal)}))


def halt_core(d):
    return {'wave': d.get('wave'), 'items': [{k: it.get(k) for k in ('key', 'call_index', 'class', 'reason', 'token')}
                                            for it in d.get('items') or []]}


def wave_result_core(d):
    return {'wave': d.get('wave'), 'counts': d.get('counts'),
            'calls': [{k: c.get(k) for k in ('key', 'classification', 'failure_class', 'reason')} for c in d.get('calls') or []]}


def entry_core(e):
    """M1: the semantic core of a cache entry (what an idempotent re-ingest must reproduce)."""
    pv = dict(e.get('provenance') or {})
    pv.pop('campaign_status', None)
    return {k: (pv if k == 'provenance' else e.get(k)) for k in
            ('schema', 'cache_id', 'key', 'theta', 'classification', 'failure_class', 'source', 'provenance', 'forward')}


def normalize_campaign_status(st):
    return {'RESUMED_OK': 'OK', 'RESUMED_FAILED': 'FAILED'}.get(st, st)


# --------------------------------------------------------------------------------------------- context
class Context:
    """Everything derived from the configuration and the pinned inputs (no side effects on disk)."""

    def __init__(self, config):
        if isinstance(config, (str, Path)):
            self.config_path = str(config)
            raw = Path(config).read_bytes()
            self.config_sha256 = sha256_bytes(raw)
            try:
                config = json.loads(raw.decode('utf-8'))
            except ValueError as exc:
                raise OrchestratorError('config unreadable: %s' % exc)
        else:
            self.config_path = None
            self.config_sha256 = sha256_bytes(canonical(config))
        self.cfg = cfg = config
        extra = set(cfg) - CONFIG_KEYS
        if cfg.get('schema') != SCHEMA_CONFIG or extra:
            raise OrchestratorError('config schema must be %s with keys %s (extra: %s)'
                                    % (SCHEMA_CONFIG, sorted(CONFIG_KEYS), sorted(extra)))
        self.synthetic = cfg.get('synthetic_test') is True
        self.work_dir_record = resolve_work_dir(cfg.get('work_dir'), cfg.get('work_dir_volume'))
        self.work_dir = Path(cfg['work_dir'])
        # F3: the config pins the work dir identity (resolved path, symlinks crossed, volume, VolumeUUID); every command
        # builds a Context, so plan / run / resolve / status all compare it.  A re-pointed runs_ext link or another disk
        # at the mount point is refused before anything is read or written.
        wpin = cfg.get('work_dir_identity')
        if wpin is None:
            if not self.synthetic:
                raise OrchestratorError('F3: work_dir_identity {%s} is required in a non-synthetic config'
                                        % ', '.join(WORK_DIR_IDENTITY_KEYS))
            self.work_dir_identity = {'pinned': False, 'note': 'NOT_PINNED (synthetic_test)'}
        else:
            bad = check_work_dir_identity(wpin, self.work_dir_record)
            if bad:
                raise OrchestratorError('F3: %s' % '; '.join(bad))
            self.work_dir_identity = {'pinned': True, 'pin': copy.deepcopy(wpin)}
        self.gates = {}
        # driver first (C7 needs it before anything synthetic is relaxed)
        self.driver = cfg['driver']
        draw = read_pinned(self.driver, 'driver')
        if self.synthetic:
            if self.driver['sha256'] in KNOWN_REAL_DRIVER_SHA256 or SYNTHETIC_DRIVER_MARKER not in draw:
                raise OrchestratorError('C7_SYNTHETIC_WITH_REAL_DRIVER: synthetic_test=true requires a mock driver '
                                        '(marker %s, not a known real driver sha)' % SYNTHETIC_DRIVER_MARKER.decode())
        tax_raw = read_pinned(cfg['taxonomy'], 'taxonomy')
        tax_doc = json.loads(tax_raw.decode('utf-8'))
        if self.synthetic and self.driver['sha256'] == tax_doc.get('driver', {}).get('sha256'):
            raise OrchestratorError('C7_SYNTHETIC_WITH_REAL_DRIVER: the config driver is the taxonomy driver')
        # coordinate spec (V001, unchanged) and the c2v004 addendum (coordinate mode, A13)
        spec_raw = read_pinned(cfg['coordinate_spec'], 'coordinate_spec')
        self.spec = spec = json.loads(spec_raw.decode('utf-8'))
        if spec.get('schema') != SCHEMA_SPEC:
            raise OrchestratorError('coordinate spec schema must be %s' % SCHEMA_SPEC)
        if spec['call_spec_mapping']['mapping_id'] != SPEC_MAPPING_ID:
            raise OrchestratorError('coordinate spec mapping_id %r is not %r' % (spec['call_spec_mapping']['mapping_id'],
                                                                               SPEC_MAPPING_ID))
        # A13: the addendum is required; it carries the coordinate mode
        if cfg.get('coordinate_spec_addendum') is None:
            raise OrchestratorError('coordinate_spec_addendum is required (it declares the coordinate mode, A13)')
        self.addendum = json.loads(read_pinned(cfg['coordinate_spec_addendum'], 'coordinate_spec_addendum'))
        if self.addendum.get('schema') != SCHEMA_ADDENDUM or \
                self.addendum.get('applies_to_coordinate_spec_sha256') != cfg['coordinate_spec']['sha256']:
            raise OrchestratorError('coordinate spec addendum schema / target sha mismatch')
        # v005 (A23 / B3-S2): A13 is a counted assumption of the headline calibration; the addendum must count it
        if not isinstance((self.addendum.get('counted_assumptions') or {}).get(COUNTED_ASSUMPTION_A13), dict):
            raise OrchestratorError('coordinate spec addendum does not count %s (A13, DDO154 distance fixed at 4.04 Mpc)'
                                    % COUNTED_ASSUMPTION_A13)
        self.coordinate_mode = cm = copy.deepcopy(self.addendum.get('coordinate_mode'))
        if not isinstance(cm, dict) or cm.get('mode') not in VARYING_EXPECTED_BY_MODE:
            raise OrchestratorError('addendum coordinate_mode.mode must be one of %s' % sorted(VARYING_EXPECTED_BY_MODE))
        if cm['mode'] == MODE_D_NUISANCE and not self.synthetic:
            raise OrchestratorError('A13: the headline calibration fixes the DDO154 distance; coordinate mode %s (the '
                                    'recorded alternative, NOT_EVALUATED_BEFORE_FREEZE) is refused in a non-synthetic '
                                    'config' % MODE_D_NUISANCE)
        self.E = load_pinned_module(spec['engine'], 'orch4_engine_c2v003a', 'engine')
        self.F = load_pinned_module(spec['freeze'], 'orch4_freeze_c2v003a', 'freeze')
        reg_pin = cfg['observation_region']
        read_pinned(reg_pin, 'observation_region')
        if reg_pin['sha256'] != spec['observation_region']['sha256'] and not self.synthetic:
            raise OrchestratorError('observation region differs from the coordinate spec pin (only a synthetic_test '
                                    'config may use another region)')
        self.region_pin = reg_pin
        self.region = self.E.load_observation_region(path=reg_pin['path'], expected_sha256=reg_pin['sha256'])
        if not self.region['ok']:
            raise OrchestratorError('observation region: %s' % self.region['reasons'])
        self.row_ids = list(self.region['row_ids'])
        ngc = cfg.get('ngc3198_slots') or spec['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation']
        self.ngc_slots_placeholder = cfg.get('ngc3198_slots') is None
        fs = self.F.make_freeze_coordinate_spec(coordinates=list(spec['coordinates']) + list(ngc))
        if not fs['ok']:
            raise OrchestratorError('make_freeze_coordinate_spec: %s' % fs['reasons'])
        self.freeze_spec = fs
        self.engine_coordinates_v001 = fs['engine_coordinates']
        if canonical(self.engine_coordinates_v001) != canonical(spec['engine_coordinates']):
            raise OrchestratorError('engine coordinates differ from the coordinate spec record')
        self.engine_coordinates = self._apply_coordinate_mode(self.engine_coordinates_v001, cm)
        self.es = self.E.make_coordinate_spec(coordinates=self.engine_coordinates)
        if not self.es['ok']:
            raise OrchestratorError('engine make_coordinate_spec: %s' % self.es['reasons'])
        want = VARYING_EXPECTED_BY_MODE[cm['mode']]
        if tuple(self.es['varying_names']) != want or tuple(cm.get('free_coordinates') or ()) != want:
            raise OrchestratorError('varying coordinates %r are not the mode\'s %r (addendum free_coordinates %r)'
                                    % (self.es['varying_names'], want, cm.get('free_coordinates')))
        self.engine_coordinates_sha256 = sha256_bytes(canonical(self.engine_coordinates))
        self.n_varying = self.es['n_varying']
        params = copy.deepcopy(spec['engine_parameters'])
        if cfg.get('engine_parameters_override'):
            if not self.synthetic:
                raise OrchestratorError('engine_parameters_override is allowed only in a synthetic_test config')
            params.update(copy.deepcopy(cfg['engine_parameters_override']))
        self.params = params
        mp = spec['call_spec_mapping']
        self.template_raw = read_pinned(mp['template'], 'call-spec template')
        self.template = json.loads(self.template_raw.decode('utf-8'))
        self.template_sha256 = mp['template']['sha256']
        self.inclination_deg = float(spec['ddo154_forward_constants']['inclination_deg']['value'])
        if float(self.template['physical']['inclination_deg']) != self.inclination_deg:
            raise OrchestratorError('template inclination differs from the declared DDO154 constant')
        # monitor (receipts of the deciding runs and of every call), deciding gate, numerics gate
        self.M = load_pinned_module(cfg['monitor'], 'orch4_monitor_c2v001', 'monitor')
        self.gates['deciding_test'] = check_deciding(cfg.get('deciding_test'), self.driver['sha256'], self.M,
                                                     synthetic=self.synthetic)
        block, self.gates['numerics_verdict'] = check_numerics(
            cfg.get('numerics'), self.template['numerics'], self.gates['deciding_test'].get('route_a_column_workers_verified'),
            synthetic=self.synthetic)                                       # v005 C4-5
        self.numerics = copy.deepcopy(block)
        cw = self.numerics.get('column_workers', 1)
        if type(cw) is not int or not 1 <= cw <= 12:
            raise OrchestratorError('numerics.column_workers must be an int 1..12')
        self.column_workers = cw
        self.weights = call_weights(self.numerics)
        self.numerics_is_template = canonical(self.numerics) == canonical(self.template['numerics'])
        self.D = exec_pinned_bytes(self.driver, 'orch4_driver_normalizer', 'driver')
        if not callable(getattr(self.D, 'normalize_spec', None)):
            raise OrchestratorError('driver exposes no normalize_spec')
        self.taxonomy = Taxonomy(tax_doc, cfg['taxonomy']['sha256'], cfg.get('route_a_contraction_test'))
        if self.taxonomy.doc['driver']['sha256'] != self.driver['sha256'] and not self.synthetic:
            raise OrchestratorError('taxonomy is written for driver %s, config driver is %s'
                                    % (self.taxonomy.doc['driver']['sha256'][:16], self.driver['sha256'][:16]))
        self.recovery_rules = cfg.get('recovery_rules') or []
        # v005 SF4: the driver interpreter is a {path, sha256} pin (bytes of the file the path resolves to)
        self.python_pin = cfg.get('python')
        if not isinstance(self.python_pin, dict) or set(self.python_pin) != {'path', 'sha256'} or \
                not isinstance(self.python_pin.get('path'), str) or not os.path.isabs(self.python_pin['path']):
            raise OrchestratorError('SF4: python must be {path, sha256} (an absolute interpreter path and the sha256 of the '
                                    'file it resolves to)')
        read_pinned(self.python_pin, 'python (SF4)')
        self.python = self.python_pin['path']
        self.executor_kind = cfg.get('executor', 'campaign')
        if self.executor_kind not in ('campaign', 'in_process_test'):
            raise OrchestratorError('executor must be campaign or in_process_test')
        if self.executor_kind == 'in_process_test' and not self.synthetic:
            raise OrchestratorError('in_process_test executor requires synthetic_test')
        # concurrency: process budget (<= 17), calls, per-call weights
        mc, pb, nc = cfg.get('max_concurrent', 1), cfg.get('process_budget'), cfg.get('n_cores', 18)
        if type(mc) is not int or mc < 1 or type(nc) is not int or nc < 1:
            raise OrchestratorError('max_concurrent and n_cores must be positive ints')
        if type(pb) is not int or not 1 <= pb <= min(PROCESS_BUDGET_MAX, nc):
            raise OrchestratorError('process_budget must be an int 1..min(%d, n_cores %d)' % (PROCESS_BUDGET_MAX, nc))
        if self.weights['peak'] > pb:
            raise OrchestratorError('one call needs %d processes (route-A pool %d, column workers %d) > process_budget %d'
                                    % (self.weights['peak'], self.weights['route_a_column_workers'], cw, pb))
        if mc > pb:
            raise OrchestratorError('max_concurrent %d exceeds process_budget %d' % (mc, pb))
        sa = cfg.get('stage_aware_budget', False)
        if type(sa) is not bool:
            raise OrchestratorError('stage_aware_budget must be a bool')
        self.max_concurrent, self.process_budget, self.n_cores, self.stage_aware = mc, pb, nc, sa
        # per-call caps and disk guard (L2)
        pc = cfg.get('per_call') or {}
        for k in ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes'):
            v = pc.get(k)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0:
                raise OrchestratorError('per_call.%s must be a positive number' % k)
        dg = cfg.get('disk_guard')
        if not isinstance(dg, dict):
            raise OrchestratorError('disk_guard {per_call_bytes, reserve_bytes, measured_per_call_bytes} required')
        per, res_b = dg.get('per_call_bytes'), dg.get('reserve_bytes', 0)
        if type(per) is not int or per <= 0 or per < int(pc['output_cap_bytes']):
            raise OrchestratorError('disk_guard.per_call_bytes must be an int > 0 and >= per_call.output_cap_bytes')
        if type(res_b) is not int or res_b < 0:
            raise OrchestratorError('disk_guard.reserve_bytes must be an int >= 0')
        self.C = None
        if self.executor_kind == 'campaign':
            self.C = load_pinned_module(cfg['campaign'], 'orch5_campaign_c2v005', 'campaign')
            if getattr(self.C, 'MODULE_NAME', None) != CAMPAIGN_MODULE_NAME or \
                    getattr(self.C, 'PROCESS_BUDGET_MAX', None) != PROCESS_BUDGET_MAX:
                raise OrchestratorError('campaign must be %s (process budget %d)' % (CAMPAIGN_MODULE_NAME, PROCESS_BUDGET_MAX))
        # base spec and A7 guards on it
        base = copy.deepcopy(self.template)
        base['numerics'] = copy.deepcopy(self.numerics)
        bad = [p for p in diff_paths(self.template, base) if not (p == 'numerics' or p.startswith('numerics.'))]
        if bad:
            raise OrchestratorError('base spec differs from the template outside numerics: %s' % bad)
        self.base = base
        self.base_sha256 = sha256_bytes(canonical(base))
        a7 = lint_override_keys(base) + relative_paths(base)
        if a7:
            raise OrchestratorError('A7_GUARD base spec: %s' % a7)
        try:
            self.norm_base = self.D.normalize_spec(copy.deepcopy(base))
        except Exception as exc:
            raise OrchestratorError('driver refuses the base spec: %s: %s' % (type(exc).__name__, exc))
        self.mapper = Mapper(self)
        self.cache_id = sha256_bytes(canonical({
            'schema': SCHEMA_CACHE_ID, 'mapping_id': MAPPING_ID, 'template_sha256': self.template_sha256,
            'base_spec_sha256': self.base_sha256, 'driver_sha256': self.driver['sha256'],
            'taxonomy_sha256': self.taxonomy.sha256, 'route_a_contraction_test': self.taxonomy.contraction_test,
            'row_ids': self.row_ids, 'engine_names': list(self.es['names']),
            'ddo154_inclination_deg': self.inclination_deg, 'coordinate_mode': cm['mode'],
            'varying_names': list(self.es['varying_names']), 'engine_coordinates_sha256': self.engine_coordinates_sha256}))
        P = self.params
        self.side_bound = int(math.floor(math.log2(math.sqrt(self.n_varying) / float(P['march_step'])))) + 3 + \
            int(P['bisection_steps'])
        self.trial_u = self._engine_trial_u()
        # v005 C4-6: the seed spec = the call spec of the engine's seed point (to_natural at the trial u)
        nat = self.E.to_natural(spec=self.es, u=self.trial_u)
        self.seed_theta = nat['theta_natural'] if nat.get('ok') else None
        self.seed_spec_sha256 = self.mapper.build(self.seed_theta)['sha256'] if self.seed_theta is not None else None
        self.gates['driver_capability'] = self.capability_probe()
        self.gates['adoption_regeneration'] = self.check_adoption()          # v005 C4-6
        self.gates['u_i_carrier'] = self.check_u_i_carrier()                 # v005 C4-6
        self.gate_digest = self.gate_digest_of(self.gates)                   # v005 B2-2 / C4-2
        self.pins = self.all_pins()                                          # v005 B2-2
        self.runtime = runtime_identity(self.python)                         # v005 SF4

    # ------------------------------------------------------------------ v005: C4-6 gates, B2-2 recheck
    def check_u_i_carrier(self):
        """C4-6 (c): where the verdict's carried numerical uncertainty u_i enters.  The default declaration is
        NOT_CARRIED_DECLARED (u_i is recorded with the calibration and enters neither the engine nor the admission
        rectangles); root sets declared_by and basis.  FROZEN_BANDS_ONLY is recorded for the freeze successor.
        ADMISSION_RECTANGLES needs a widened observation region (a new region pin, hence a new cache id) that this
        orchestrator cannot build: refused (U_I_CARRIER_NOT_IMPLEMENTED)."""
        g = {'ok': False, 'reasons': [], 'u_i_km_s_from_verdict': (self.gates.get('numerics_verdict') or {}).get('u_i_km_s')}
        d = self.cfg.get('u_i_carrier')
        if d is None:
            if self.synthetic:
                g.update(ok=True, declaration='NOT_DECLARED (synthetic_test)')
            else:
                g['reasons'].append('U_I_CARRIER_NOT_DECLARED: config u_i_carrier {carrier, declared_by, basis, note} is '
                                    'required (C4-6: an ADOPT verdict prescribes "carry u_i")')
            return g
        if not isinstance(d, dict) or set(d) != U_I_KEYS:
            g['reasons'].append('u_i_carrier must be {%s}' % ', '.join(sorted(U_I_KEYS)))
            return g
        g['declaration'] = copy.deepcopy(d)
        if d['carrier'] not in U_I_CARRIERS:
            g['reasons'].append('u_i_carrier.carrier %r is not one of %s' % (d['carrier'], list(U_I_CARRIERS)))
        elif d['carrier'] not in U_I_CARRIERS_IMPLEMENTED:
            g['reasons'].append('U_I_CARRIER_NOT_IMPLEMENTED: %s needs u_i-widened admission rectangles (a new observation '
                                'region pin and cache id); c2v005 carries u_i only as a record' % d['carrier'])
        if not (isinstance(d['declared_by'], str) and d['declared_by'].strip() and isinstance(d['basis'], str)
                and d['basis'].strip()):
            g['reasons'].append('U_I_CARRIER_ROOT_TO_SET: u_i_carrier.declared_by and .basis must be set by root (default '
                                '"not carried; declared" is a proposal until root signs it)')
        g['ok'] = not g['reasons']
        return g

    def check_adoption(self):
        """C4-6 (a)(b): the launch numerics are the ADOPTed case's block, so everything derived on another block is
        regenerated.  The pinned adoption_derivation (schema DDO154_CALIBRATION_ADOPTION_DERIVATION_C2V005) must name:
        this verdict (sha256), adopted case id and call spec; this config's base spec and seed spec; this config's
        capability evidence; a timing model {path, sha256} whose JSON names the adopted call spec and this base spec;
        source_receipts [{case_id, path, sha256}] = receipts of cases on the adopted grid (the adopted case included),
        each verified by the pinned monitor against the verdict's inputs (spec, driver, result sha256); per_call caps equal
        to the config's and above every receipt's elapsed / peak RSS / output; disk_guard per_call_bytes and
        measured_per_call_bytes equal to the config's, per_call_bytes >= every receipt's output."""
        g = {'ok': False, 'reasons': []}
        R = g['reasons']
        pin = self.cfg.get('adoption_derivation')
        ng = self.gates.get('numerics_verdict') or {}
        if pin is None:
            if self.synthetic:
                g.update(ok=True, status='NOT_CHECKED (synthetic_test, no adoption derivation pinned)')
            else:
                R.append('ADOPTION_DERIVATION_NOT_PINNED: C4-6 the config, seed spec, capability evidence, timing and caps '
                         'must be regenerated from the adopted case (adoption_derivation {path, sha256})')
            return g
        try:
            doc = json.loads(read_pinned(pin, 'adoption_derivation').decode('utf-8'))
            if not isinstance(doc, dict):
                raise ValueError('not an object')
        except (OrchestratorError, ValueError) as exc:
            R.append(str(exc)[:300])
            return g
        g['adoption_derivation'] = {'path': pin['path'], 'sha256': pin['sha256']}
        ad = ng.get('adopted') or {}
        if not ng.get('ok') or not ad:
            R.append('ADOPTION_WITHOUT_ADOPT_VERDICT: the numerics gate has not verified an ADOPT verdict')
        want = {'schema': SCHEMA_ADOPTION, 'verdict_artifact_sha256': ad.get('verdict_sha256'),
                'adopted_case_id': ad.get('case_id'), 'adopted_call_spec_sha256': ad.get('call_spec_sha256'),
                'base_spec_sha256': self.base_sha256, 'seed_spec_sha256': self.seed_spec_sha256,
                'capability_evidence_sha256': (self.cfg.get('capability_evidence') or {}).get('sha256')}
        for k, v in want.items():
            if doc.get(k) != v or v is None:
                R.append('C4-6 REGENERATE: adoption_derivation.%s %r != %r' % (k, str(doc.get(k))[:20], str(v)[:20]))
        tm = doc.get('timing_model')
        try:
            tdoc = json.loads(read_pinned(tm, 'adoption_derivation.timing_model').decode('utf-8'))
            if not isinstance(tdoc, dict) or tdoc.get('adopted_call_spec_sha256') != ad.get('call_spec_sha256') or \
                    tdoc.get('base_spec_sha256') != self.base_sha256:
                R.append('C4-6 REGENERATE: the timing model does not name the adopted call spec and this base spec')
        except (OrchestratorError, ValueError) as exc:
            R.append('C4-6 timing model: %s' % str(exc)[:200])
        inputs = ng.get('grid_case_inputs') or {}
        rs = doc.get('source_receipts')
        used = {'elapsed_seconds': 0.0, 'peak_rss_bytes': 0, 'output_bytes': 0}
        if not isinstance(rs, list) or not rs:
            R.append('C4-6 source_receipts: a non-empty list of {case_id, path, sha256} is required')
            rs = []
        cases_seen = set()
        for r in rs:
            cid = r.get('case_id') if isinstance(r, dict) else None
            inp = inputs.get(cid)
            if inp is None:
                R.append('C4-6 source receipt case %r is not a case of the adopted grid %r' % (cid, ad.get('grid')))
                continue
            try:
                read_pinned({'path': r.get('path'), 'sha256': r.get('sha256')}, 'source receipt %s' % cid)
                v = self.M.verify_receipt(r['path'], spec_sha256=inp.get('call_spec_sha256'),
                                          driver_sha256=inp.get('driver_sha256'))
            except (OrchestratorError, OSError, ValueError) as exc:
                R.append('C4-6 source receipt %s: %s' % (cid, str(exc)[:200]))
                continue
            rc = v.get('receipt') or {}
            if not v.get('ok') or rc.get('status') != 'FINISHED' or rc.get('driver_status') != 'COMPLETED' or \
                    (rc.get('result') or {}).get('sha256') != inp.get('result_sha256'):
                R.append('C4-6 source receipt %s does not verify as the FINISHED/COMPLETED receipt of the verdict input '
                         '(%s)' % (cid, v.get('reasons')))
                continue
            cases_seen.add(cid)
            for k, rk in (('elapsed_seconds', 'elapsed_seconds'), ('peak_rss_bytes', 'peak_rss_bytes')):
                x = rc.get(rk)
                if _finite_positive(x):
                    used[k] = max(used[k], x)
            for rk in ('final_output_bytes', 'peak_output_bytes'):
                x = rc.get(rk)
                if _finite_positive(x):
                    used['output_bytes'] = max(used['output_bytes'], x)
        if ad.get('case_id') and ad.get('case_id') not in cases_seen:
            R.append('C4-6 source_receipts must include the verified receipt of the adopted case %s' % ad.get('case_id'))
        g['measured_max'] = used
        pc, dpc = self.cfg.get('per_call') or {}, doc.get('per_call') or {}
        for k, uk in zip(ADOPTION_CAP_KEYS, ('elapsed_seconds', 'peak_rss_bytes', 'output_bytes')):
            if dpc.get(k) != pc.get(k):
                R.append('C4-6 caps: adoption_derivation.per_call.%s %r != config per_call.%s %r' % (k, dpc.get(k), k, pc.get(k)))
            elif not (isinstance(pc.get(k), (int, float)) and pc.get(k) > used[uk]):
                R.append('C4-6 caps: per_call.%s %r is not above the measured %r of the adopted grid receipts'
                         % (k, pc.get(k), used[uk]))
        dg, ddg = self.cfg.get('disk_guard') or {}, doc.get('disk_guard') or {}
        for k in ('per_call_bytes', 'measured_per_call_bytes'):
            if ddg.get(k) != dg.get(k):
                R.append('C4-6 disk: adoption_derivation.disk_guard.%s %r != config %r' % (k, ddg.get(k), dg.get(k)))
        if isinstance(dg.get('per_call_bytes'), int) and dg['per_call_bytes'] < used['output_bytes']:
            R.append('C4-6 disk: per_call_bytes %d is below the measured output %r' % (dg['per_call_bytes'], used['output_bytes']))
        g['ok'] = not R
        return g

    @staticmethod
    def gate_digest_of(gates):
        return sha256_bytes(canonical({k: gates[k] for k in sorted(gates)}))

    def all_pins(self):
        """B2-2: every pinned input file: the config's pins, the coordinate spec's (engine, freeze, template, region)."""
        out = collect_pins(self.cfg, 'config')
        for k in ('engine', 'freeze', 'observation_region'):
            if isinstance(self.spec.get(k), dict):
                out.extend(collect_pins(self.spec[k], 'coordinate_spec.%s' % k))
        out.extend(collect_pins(self.spec['call_spec_mapping']['template'], 'coordinate_spec.template'))
        return out

    def fresh_gates(self):
        """B2-2: every gate re-evaluated from the bytes on disk now (same functions, same order as __init__)."""
        g = {'deciding_test': check_deciding(self.cfg.get('deciding_test'), self.driver['sha256'], self.M,
                                             synthetic=self.synthetic)}
        blk, g['numerics_verdict'] = check_numerics(self.cfg.get('numerics'), self.template['numerics'],
                                                    g['deciding_test'].get('route_a_column_workers_verified'),
                                                    synthetic=self.synthetic)
        if canonical(blk) != canonical(self.numerics):
            g['numerics_verdict'] = dict(g['numerics_verdict'], ok=False,
                                         reasons=['the numerics block differs from the one this process started with'])
        saved, self.gates = self.gates, dict(self.gates, **g)
        try:
            g['driver_capability'] = self.capability_probe()
            self.gates['driver_capability'] = g['driver_capability']
            g['adoption_regeneration'] = self.check_adoption()
            self.gates['adoption_regeneration'] = g['adoption_regeneration']
            g['u_i_carrier'] = self.check_u_i_carrier()
        finally:
            self.gates = saved
        return g

    def recheck(self, label):
        """B2-2 (v005): before every wave.  Re-hash every pinned input from bytes, re-evaluate every gate, compare the gate
        digest with the one this process started with.  Returns the list of reasons (empty = unchanged and passing)."""
        bad = []
        for lab, p in self.all_pins():
            try:
                s = sha256_file(p['path'])
            except OSError as exc:
                s = 'UNREADABLE %s' % type(exc).__name__
            if s != p['sha256']:
                bad.append('PIN_CHANGED %s: %s no longer hashes to %s (%s)' % (lab, p['path'], p['sha256'][:16], s[:24]))
        fresh = self.fresh_gates()
        dig = self.gate_digest_of(fresh)
        if dig != self.gate_digest:
            bad.append('GATES_CHANGED: gate digest %s != %s at process start (%s)'
                       % (dig[:16], self.gate_digest[:16],
                          [k for k in sorted(fresh) if canonical(fresh[k]) != canonical(self.gates.get(k))]))
        notok = [k for k, v in fresh.items() if not v.get('ok')]
        if notok:
            bad.append('GATES_NOT_PASSED before %s: %s' % (label, notok))
        return bad

    @staticmethod
    def _apply_coordinate_mode(coords, cm):
        """A13: DDO154_DISTANCE_FIXED_AT_REGISTERED changes ONLY the role of the V001 engine coordinate distance_Mpc
        (nuisance -> fixed); its trial value must be the registered 4.04 Mpc and its box stays the V001 box (the engine
        still binds that box to region.distance_summary).  DDO154_DISTANCE_NUISANCE returns the V001 list unchanged."""
        out = copy.deepcopy(coords)
        if cm['mode'] == MODE_D_NUISANCE:
            if cm.get('fixed_engine_coordinates'):
                raise OrchestratorError('coordinate mode %s fixes nothing' % MODE_D_NUISANCE)
            return out
        fx = cm.get('fixed_engine_coordinates')
        if fx != {DDO154_DISTANCE_NAME: DDO154_REGISTERED_DISTANCE_MPC}:
            raise OrchestratorError('coordinate mode %s must fix exactly {%r: %r}, got %r'
                                    % (MODE_D_FIXED, DDO154_DISTANCE_NAME, DDO154_REGISTERED_DISTANCE_MPC, fx))
        hit = [c for c in out if c.get('name') == DDO154_DISTANCE_NAME]
        if len(hit) != 1:
            raise OrchestratorError('the V001 engine coordinates carry no single %s' % DDO154_DISTANCE_NAME)
        c = hit[0]
        if c.get('role') != 'nuisance' or c.get('scope') != 'DDO154' or c.get('units') != 'Mpc' or \
                float(c.get('trial_value')) != DDO154_REGISTERED_DISTANCE_MPC:
            raise OrchestratorError('V001 %s is not the DDO154 nuisance at trial 4.04 Mpc: %r' % (DDO154_DISTANCE_NAME, c))
        c['role'] = 'fixed'
        changed = [(a['name'], k) for a, b in zip(coords, out) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
        if changed != [(DDO154_DISTANCE_NAME, 'role')]:
            raise OrchestratorError('coordinate mode changed more than the distance role: %r' % changed)
        return out

    def _engine_trial_u(self):
        E, es = self.E, self.es
        tu = []
        for nm in es['varying_names']:
            tr = es['transforms'][nm]
            x_lo, x_hi = E._x_of(tr, es['lower'][nm]), E._x_of(tr, es['upper'][nm])
            tu.append((E._x_of(tr, es['trial_values'][nm]) - x_lo) / (x_hi - x_lo))
        return tu

    def prelaunch_check(self, spec, recovery=False):
        """Before launch: A7 lint, absolute paths, the pinned driver's own normalize_spec, and the normalized spec may
        differ from the normalized base only in label + the four physical fields (+ numerics.brackets under recovery)."""
        a7 = lint_override_keys(spec) + relative_paths(spec)
        if a7:
            raise OrchestratorError('A7_GUARD: %s' % a7[:5])
        try:
            n = self.D.normalize_spec(copy.deepcopy(spec))
        except Exception as exc:
            raise OrchestratorError('DRIVER_REFUSES_SPEC: %s: %s' % (type(exc).__name__, str(exc)[:300]))
        bad = []
        for p in diff_paths(self.norm_base, n):
            if p in DECLARED_CHANGED_PATHS:
                continue
            if recovery and (p == 'numerics.brackets' or p.startswith('numerics.brackets.')):
                continue
            bad.append(p)
        if bad:
            raise OrchestratorError('normalized spec differs from the normalized base at undeclared paths %s' % bad)
        return n

    def probe_points(self):
        es = self.es
        names = list(es['varying_names'])
        pts = [('trial', {nm: es['trial_values'][nm] for nm in es['names']})]
        for mask in range(1 << len(names)):
            th = {nm: es['trial_values'][nm] for nm in es['names']}
            lab = []
            for j, nm in enumerate(names):
                hi = (mask >> j) & 1
                th[nm] = es['upper'][nm] if hi else es['lower'][nm]
                lab.append('%s=%s' % (nm, 'hi' if hi else 'lo'))
            pts.append(('corner ' + ','.join(lab), th))
        return pts

    def capability_probe(self):
        """Layer 1: the trial point and all 2^n box corners pass prelaunch_check (normalize_spec, declared fields only).
        Layer 2: the pinned run-mode admission evidence (the driver's own dry-run of exactly these specs) reports no
        stage-binding refusal (driver c2v008 BLOCKS any DDO154 distance != 4.04 in run mode, L2184-2190)."""
        pts = self.probe_points()
        refused, accepted, shas = [], 0, {}
        for label, th in pts:
            try:
                b = self.mapper.build(th)
                self.prelaunch_check(b['spec'])
                accepted += 1
                shas[label] = b['sha256']
            except OrchestratorError as exc:
                refused.append({'point': label, 'distance_Mpc': th['distance_Mpc'], 'reason': str(exc)[:300]})
        out = {'ok': False, 'n_points': len(pts), 'n_accepted': accepted, 'refused': refused, 'reasons': [],
               'layer1_normalize_ok': not refused}
        if refused:
            out['reasons'].append('DRIVER_CAPABILITY_GAP: the pinned driver refuses %d of %d probe points (first: %s)'
                                  % (len(refused), len(pts), refused[0]['reason'][:200]))
        ev = self.cfg.get('capability_evidence')
        if ev is None:
            if self.synthetic:
                out['layer2_run_mode'] = 'NOT_CHECKED (synthetic_test, no evidence pinned)'
                out['ok'] = not refused
            else:
                out['layer2_run_mode'] = 'UNVERIFIED'
                out['reasons'].append('RUN_MODE_ADMISSION_UNVERIFIED: capability_evidence (driver dry-run of the probe '
                                      'points) is not pinned')
            return out
        try:
            doc = json.loads(read_pinned(ev, 'capability_evidence').decode('utf-8'))
        except (OrchestratorError, ValueError) as exc:
            out['reasons'].append(str(exc))
            out['layer2_run_mode'] = 'UNREADABLE'
            return out
        l2 = []
        if doc.get('schema') != SCHEMA_CAPABILITY or (doc.get('driver') or {}).get('sha256') != self.driver['sha256'] \
                or doc.get('base_spec_sha256') != self.base_sha256:
            l2.append('capability_evidence is not for this driver / base spec (schema %r, driver %s, base %s)'
                      % (doc.get('schema'), str((doc.get('driver') or {}).get('sha256'))[:16], str(doc.get('base_spec_sha256'))[:16]))
        else:
            rows = {r.get('spec_sha256'): r for r in doc.get('rows') or []}
            gap = []
            for label, s in shas.items():
                r = rows.get(s)
                if r is None:
                    gap.append({'point': label, 'reason': 'not in the evidence'})
                elif r.get('run_mode_admitted') is not True:
                    gap.append({'point': label, 'distance_Mpc': (r.get('physical') or {}).get('distance_Mpc'),
                                'reason': r.get('run_mode_refusal') or 'run mode not admitted'})
            out['run_mode_refused'] = gap
            if gap:
                l2.append('DRIVER_CAPABILITY_GAP_RUN_MODE: the driver\'s own dry-run reports %d of %d probe points not '
                          'admitted in run mode (first: %s: %s)' % (len(gap), len(shas), gap[0]['point'], str(gap[0]['reason'])[:200]))
        out['layer2_run_mode'] = 'ADMITTED' if not l2 else 'REFUSED'
        out['capability_evidence'] = {'path': ev['path'], 'sha256': ev['sha256']}
        out['reasons'].extend(l2)
        out['ok'] = not refused and not l2
        return out

    def gates_ok(self):
        return all(g.get('ok') for g in self.gates.values())

    def gate_report(self):
        rep = {}
        for k, v in self.gates.items():
            rep[k] = {kk: (vv if not (kk in ('refused', 'run_mode_refused') and isinstance(vv, list) and len(vv) > 20)
                           else vv[:20] + ['... %d more' % (len(vv) - 20)]) for kk, vv in v.items()}
        return rep

    def run_kwargs(self):
        P = self.params
        return dict(coordinates=self.engine_coordinates, observation_region_path=self.region_pin['path'],
                    observation_region_sha256=self.region_pin['sha256'], u_seed=P['u_seed'], budget=P['budget'],
                    rel_step=P['rel_step'], min_step=P['min_step'], max_halvings=P['max_halvings'],
                    null_tolerance=P['null_tolerance'], repair_iterations=P['repair_iterations'],
                    max_repair_step=P['max_repair_step'], march_step=P['march_step'],
                    bisection_steps=P['bisection_steps'], design_count=P['design_count'],
                    global_design_count=P['global_design_count'], max_march_rounds=P['max_march_rounds'],
                    hull_growth_tol=P['hull_growth_tol'], ddo154_distance=P['ddo154_distance'],
                    rng_seed=P['rng_seed'])

    def branch_bound(self, family):
        P = self.params
        name = family[0]
        if name == 'jacobian':
            return 2 * (int(P['max_halvings']) + 1)
        if name in ('march0', 'lp', 'axis'):
            return self.side_bound
        return 1

    def recovery_rule(self, path):
        """A config-allowlisted, pre-declared bracket recovery rule (e.g. KMAX_D7_RECOVERY_R1.json); verified from bytes."""
        for r in self.recovery_rules:
            if isinstance(r, dict) and r.get('path') == path:
                try:
                    doc = json.loads(read_pinned(r, 'recovery rule'))
                except ValueError as exc:
                    raise OrchestratorError('recovery rule %s unreadable: %s' % (path, exc))
                bk = doc.get('brackets')
                if not isinstance(bk, dict):
                    raise OrchestratorError('recovery rule %s has no brackets block' % path)
                a7 = lint_override_keys(bk)
                if a7:
                    raise OrchestratorError('A7_GUARD recovery rule: %s' % a7)
                return {'path': r['path'], 'sha256': r['sha256'], 'rule_id': r.get('rule_id'), 'brackets': bk}
        raise OrchestratorError('recovery rule %s is not in the config allowlist recovery_rules' % path)

    def disk_forecast(self, n_next=None):
        dg = self.cfg['disk_guard']
        per = int(dg['per_call_bytes'])
        reserve = int(dg.get('reserve_bytes', 0))
        meas = dg.get('measured_per_call_bytes')
        anc = Path(self.work_dir_record['resolved'])
        while not anc.exists() and anc != anc.parent:
            anc = anc.parent
        free = shutil.disk_usage(str(anc)).free
        out = {'free_bytes': free, 'free_bytes_read_at': str(anc), 'volume': self.work_dir_record.get('volume'),
               'work_dir_resolved': self.work_dir_record['resolved'], 'reserve_bytes': reserve,
               'per_call_bytes_guard': per, 'calls_affordable_now_guard': max(0, (free - reserve) // per),
               'measured_per_call_bytes': meas,
               'calls_affordable_now_measured': (max(0, (free - reserve) // int(meas)) if meas else None),
               'rule': 'HALTED_DISK before a wave unless free >= n_calls x per_call_bytes_guard + reserve; nothing is '
                       'ever deleted (principal: keep everything)'}
        if n_next is not None:
            out['next_wave_calls'] = n_next
            out['next_wave_fits'] = free >= n_next * per + reserve
        return out


# --------------------------------------------------------------------------------------------- theta -> call spec
class Mapper:
    """theta (every engine coordinate) -> forward call spec = base spec with only the declared fields changed."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.names = list(ctx.es['names'])
        self.fixed = {nm: ctx.es['trial_values'][nm] for nm in ctx.es['fixed_names']}
        self.lower, self.upper = dict(ctx.es['lower']), dict(ctx.es['upper'])

    def build(self, theta, recovery=None):
        ctx = self.ctx
        if not isinstance(theta, dict) or sorted(theta) != sorted(self.names):
            raise OrchestratorError('theta must carry exactly the engine coordinates %s' % self.names)
        th = {k: float(v) for k, v in theta.items()}
        for nm, v in th.items():
            if not math.isfinite(v):
                raise OrchestratorError('theta[%s] not finite' % nm)
            if not (self.lower[nm] <= v <= self.upper[nm]):
                raise OrchestratorError('theta[%s] = %r outside the computational box' % (nm, v))
        for nm, tv in self.fixed.items():
            if th[nm] != tv:
                raise OrchestratorError('fixed coordinate %s = %r differs from its trial value %r' % (nm, th[nm], tv))
        spec = copy.deepcopy(ctx.base)
        ph = spec['physical']
        for field, nm in FIXED_TEMPLATE_CHECKS:
            if float(ph[field]) != th[nm]:
                raise OrchestratorError('base physical.%s %r != theta %s %r' % (field, ph[field], nm, th[nm]))
        if float(ph['inclination_deg']) != ctx.inclination_deg:
            raise OrchestratorError('base inclination is not the declared DDO154 constant')
        key = theta_key(th)
        ph['common_scale_s'] = th['common_scale_s']
        ph['gamma'] = th['gamma_over_Eref'] * th['Eref_base_J']
        ph['ell_F_m'] = th['ell_F_m']
        ph['distance_Mpc'] = th['distance_Mpc']
        spec['label'] = 'DDO154 calibration orchestrator c2v004 theta %s; base %s' % (key[:16], ctx.base_sha256[:8])
        if recovery is not None:
            spec['numerics']['brackets'] = copy.deepcopy(recovery['brackets'])
            spec['label'] += '; recovery %s' % (recovery.get('rule_id') or recovery['sha256'][:8])
        changed = diff_paths(ctx.base, spec)
        for p in changed:
            if p in DECLARED_CHANGED_PATHS:
                continue
            if recovery is not None and (p == 'numerics.brackets' or p.startswith('numerics.brackets.')):
                continue
            raise OrchestratorError('undeclared call-spec change at %s' % p)
        raw = json_bytes(spec)
        return {'key': key, 'spec': spec, 'raw': raw, 'sha256': sha256_bytes(raw), 'changed_paths': changed}


# --------------------------------------------------------------------------------------------- custody helpers
def finish_binding(result_path, result_sha256):
    """F1: the driver's <outdir>/finish.json (written after result.json, DRV L2897) must name this result by path and
    sha256.  Returns (finish pin or None, reason or None)."""
    fp = Path(result_path).parent / 'finish.json'
    if not fp.is_file():
        return None, 'FINISH_JSON_MISSING'
    try:
        raw = fp.read_bytes()                             # v005 C4-1: an unreadable finish.json is INFRA, not a crash
        fin = json.loads(raw.decode('utf-8'))
    except (OSError, ValueError, UnicodeDecodeError):
        return None, 'FINISH_JSON_UNREADABLE'
    if not isinstance(fin, dict) or fin.get('result_sha256') != result_sha256:
        return None, 'FINISH_NOT_BOUND_TO_RESULT'
    if os.path.realpath(str(fin.get('result_path'))) != os.path.realpath(str(result_path)):
        return None, 'FINISH_NOT_BOUND_TO_RESULT_PATH'
    return {'path': str(fp), 'sha256': sha256_bytes(raw)}, None


def receipt_and_finish_custody(ctx, pv):
    """F1 (CHECK_SOFTWARE_V001): re-verify, from bytes, the monitor receipt an entry records (pinned monitor, receipt file
    sha256, its result pin and path) and the finish.json -> result binding.  Returns a reason or None."""
    rp = pv.get('receipt_path')
    if not isinstance(rp, str) or not os.path.isfile(rp):
        return 'receipt missing'
    try:
        if sha256_file(rp) != pv.get('receipt_file_sha256'):
            return 'receipt file bytes changed'
    except OSError as exc:                                # v005 C4-1
        return 'receipt unreadable: %s' % type(exc).__name__
    v = ctx.M.verify_receipt(rp, spec_sha256=pv.get('spec_sha256'), driver_sha256=ctx.driver['sha256'])
    if not v['ok']:
        return 'receipt does not verify: %s' % v['reasons']
    r = v['receipt']
    pin = r.get('result') or {}
    if pin.get('sha256') != pv.get('result_sha256'):
        return 'receipt result sha256 is not the entry result sha256'
    if os.path.realpath(str(pin.get('path'))) != os.path.realpath(str(pv.get('result_path'))):
        return 'receipt result path is not the entry result path'
    if r.get('receipt_sha256') != pv.get('receipt_sha256_self'):
        return 'receipt self-hash differs from the entry'
    fin, why = finish_binding(pv['result_path'], pv['result_sha256'])
    if why:
        return why
    if canonical(fin) != canonical(pv.get('finish')):
        return 'finish.json pin differs from the entry'
    return None


def classify_alias_result(ctx, result_path, res):
    """S3: the anchor alias result through the taxonomy (collect_evidence on its call directory + classify)."""
    ev = collect_evidence(Path(result_path).parent, res, ctx.row_ids, ctx.taxonomy)
    return ctx.taxonomy.classify(res, ev), ev


# --------------------------------------------------------------------------------------------- cache
class Cache:
    """theta-keyed cache: one immutable JSON file per canonical theta hash; never overwritten.
    Only VALID and MODEL_INVALID are cached (NUMERICS_LIMITED and INFRA halt)."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.dir = ctx.work_dir / 'cache' / ctx.cache_id
        self.entries_dir = self.dir / 'entries'
        self.entries = {}
        self._resolutions = None

    def open(self, create):
        if create:
            self.entries_dir.mkdir(parents=True, exist_ok=True)
            hdr = self.dir / 'CACHE_HEADER.json'
            body = {'schema': SCHEMA_CACHE_ID, 'cache_id': self.ctx.cache_id, 'mapping_id': MAPPING_ID,
                    'template_sha256': self.ctx.template_sha256, 'base_spec_sha256': self.ctx.base_sha256,
                    'driver_sha256': self.ctx.driver['sha256'], 'taxonomy_sha256': self.ctx.taxonomy.sha256,
                    'route_a_contraction_test': self.ctx.taxonomy.contraction_test,
                    'numerics': self.ctx.numerics, 'row_ids': self.ctx.row_ids,
                    'engine_names': list(self.ctx.es['names']), 'coordinate_mode': self.ctx.coordinate_mode['mode'],
                    'varying_names': list(self.ctx.es['varying_names']),
                    'engine_coordinates_sha256': self.ctx.engine_coordinates_sha256}
            write_json_idempotent(hdr, body, lambda d: {'cache_id': d.get('cache_id')})
        self.entries = {}
        self._resolutions = None
        if not self.entries_dir.is_dir():
            return self
        for p in sorted(self.entries_dir.glob('*.json')):
            e = load_json_file(p, 'cache entry %s (torn or corrupt)' % p.stem)
            self._verify(e, p.stem)
            self.entries[e['key']] = e
        return self

    def resolutions(self):
        if self._resolutions is None:
            self._resolutions = read_jsonl(self.ctx.work_dir / 'RESOLUTIONS.jsonl')
        return self._resolutions

    def _verify(self, e, stem):
        """v005 C4-1: a cache entry whose pinned bytes (result.json, receipt, finish.json, evidence) cannot be read or
        parsed, or whose record is malformed, is a refusal (exit 3) naming the entry, never a traceback."""
        try:
            return self._verify_impl(e, stem)
        except OrchestratorError:
            raise
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            raise OrchestratorError('cache entry %s unverifiable (C4-1): %s: %s' % (stem, type(exc).__name__,
                                                                                     str(exc)[:200]))

    def _verify_impl(self, e, stem):
        if not isinstance(e, dict):
            raise OrchestratorError('cache entry %s is not an object' % stem)
        body = {k: v for k, v in e.items() if k != 'entry_sha256'}
        if sha256_bytes(canonical(body)) != e.get('entry_sha256'):
            raise OrchestratorError('cache entry %s self-hash mismatch' % stem)
        if e.get('schema') != SCHEMA_CACHE_ENTRY or e.get('cache_id') != self.ctx.cache_id or e.get('key') != stem:
            raise OrchestratorError('cache entry %s does not belong to this cache' % stem)
        if theta_key(e['theta']) != e['key']:
            raise OrchestratorError('cache entry %s key does not hash its theta' % stem)
        f = e.get('forward')
        if not isinstance(f, dict) or not isinstance(f.get('valid'), bool) or not isinstance(f.get('speeds_km_s'), dict):
            raise OrchestratorError('cache entry %s: malformed forward record' % stem)
        if e.get('classification') not in CACHED_CLASSES:
            raise OrchestratorError('cache entry %s: classification %r is not cacheable' % (stem, e.get('classification')))
        if (e['classification'] == 'VALID') != (f['valid'] is True):
            raise OrchestratorError('cache entry %s: classification inconsistent with forward.valid' % stem)
        pv = e.get('provenance') or {}
        src = e.get('source')
        ctx = self.ctx
        if src == 'WAVE':
            # F2 + C9 + M3: everything is re-derived from the pinned bytes
            rp, rs = pv.get('result_path'), pv.get('result_sha256')
            if not rp or not rs or not os.path.isfile(rp):
                raise OrchestratorError('cache entry %s: result.json missing' % stem)
            raw = Path(rp).read_bytes()
            if sha256_bytes(raw) != rs:
                raise OrchestratorError('cache entry %s: result.json bytes no longer verify' % stem)
            res = json.loads(raw.decode('utf-8'))
            rec = pv.get('recovery')
            rr = None
            if rec:
                rr = ctx.recovery_rule(rec.get('path'))
                if rr['sha256'] != rec.get('sha256'):
                    raise OrchestratorError('cache entry %s: recovery rule bytes changed' % stem)
            b = ctx.mapper.build(e['theta'], recovery=rr)
            if not (b['sha256'] == res.get('call_spec_sha256') == pv.get('spec_sha256')):
                raise OrchestratorError('cache entry %s: theta does not map to the result call spec (M3)' % stem)
            if res.get('driver_sha256') != ctx.driver['sha256']:
                raise OrchestratorError('cache entry %s: result driver is not the config driver' % stem)
            bad = receipt_and_finish_custody(ctx, pv)
            if bad:
                raise OrchestratorError('cache entry %s: F1 custody: %s' % (stem, bad))
            ev = collect_evidence(Path(rp).parent, res, ctx.row_ids, ctx.taxonomy)
            if canonical(ev['files']) != canonical(pv.get('evidence_files') or {}):
                raise OrchestratorError('cache entry %s: evidence files changed or differ from the recorded set' % stem)
            out = ctx.taxonomy.classify(res, ev)
            tx = pv.get('taxonomy') or {}
            code = out['code'] if out['class'] != 'VALID' else None
            if canonical(tax_record(out, ctx.taxonomy)) != canonical(tx) or out['class'] != e['classification'] or \
                    code != e.get('failure_class'):
                raise OrchestratorError('cache entry %s: the taxonomy re-run on the pinned evidence gives %s/%s/%s, the '
                                        'entry says %s/%s/%s (C9 custody)' % (stem, out['class'], out['rule'], out['code'],
                                                                             e['classification'], tx.get('rule'),
                                                                             e.get('failure_class')))
            fwd2 = forward_from_result(res, out['class'], code, out['rule'], ctx.row_ids)
            if canonical(fwd2) != canonical(f):
                raise OrchestratorError('cache entry %s: forward record differs from the one derived from result.json '
                                        '(F2 custody)' % stem)
        elif src == 'ANCHOR_ALIAS':
            rp, rs = pv.get('result_path'), pv.get('result_sha256')
            raw = Path(rp).read_bytes() if rp and os.path.isfile(rp) else b''
            if sha256_bytes(raw) != rs:
                raise OrchestratorError('cache entry %s: anchor result bytes no longer verify' % stem)
            res = json.loads(raw.decode('utf-8'))
            if res.get('driver_sha256') != ctx.driver['sha256'] or res.get('call_spec_sha256') != ctx.template_sha256:
                raise OrchestratorError('cache entry %s: anchor alias of another driver or spec (C5: no equivalence)' % stem)
            nat = ctx.E.to_natural(spec=ctx.es, u=ctx.trial_u)
            if theta_key(nat['theta_natural']) != e['key']:
                raise OrchestratorError('cache entry %s: alias theta is not the trial point' % stem)
            out, ev = classify_alias_result(ctx, rp, res)          # S3: the taxonomy on the alias result, every open
            if out['rule'] != 'R01' or out['class'] != 'VALID':
                raise OrchestratorError('cache entry %s: S3 the anchor alias result classifies %s/%s, not R01 VALID'
                                        % (stem, out['class'], out['rule']))
            if canonical(ev['files']) != canonical(pv.get('evidence_files') or {}) or \
                    canonical(tax_record(out, ctx.taxonomy)) != canonical(pv.get('taxonomy') or {}):
                raise OrchestratorError('cache entry %s: S3 alias evidence or taxonomy record differs from the entry' % stem)
            fwd2 = {'valid': True, 'speeds_km_s': {rid: float(res['speeds_km_s'][rid]) for rid in ctx.row_ids},
                    'reasons': []}
            if canonical(fwd2) != canonical(f):
                raise OrchestratorError('cache entry %s: alias speeds differ from the anchor result (F2)' % stem)
        elif src == 'ROOT_RESOLUTION':
            if e['classification'] != 'MODEL_INVALID' or f['speeds_km_s']:
                raise OrchestratorError('cache entry %s: a root resolution can only declare MODEL_INVALID' % stem)
            # L1: the RESOLUTIONS line and the HALT item must exist and agree
            tok, wave = pv.get('halt_token'), pv.get('wave')
            lines = [ln for ln in self.resolutions() if ln.get('token') == tok and ln.get('key') == e['key']
                     and ln.get('decision') == 'invalid' and ln.get('wave') == wave]
            if len(lines) != 1 or sha256_bytes(canonical(lines[0])) != pv.get('resolution_line_sha256'):
                raise OrchestratorError('cache entry %s: no matching RESOLUTIONS line (L1)' % stem)
            # v005 C4-2: a root decision is bound to the cache id of its RESOLUTIONS line and of its HALT's WAVE_PLAN
            if lines[0].get('cache_id') != ctx.cache_id:
                raise OrchestratorError('cache entry %s: C4-2 the RESOLUTIONS line was written under cache id %s, not %s'
                                        % (stem, str(lines[0].get('cache_id'))[:16], ctx.cache_id[:16]))
            wpp = ctx.work_dir / 'waves' / ('wave_%04d' % int(wave)) / 'WAVE_PLAN.json'
            wplan = load_json_file(wpp, 'WAVE_PLAN.json') if wpp.is_file() else {}
            if wplan.get('cache_id') != ctx.cache_id:
                raise OrchestratorError('cache entry %s: C4-2 the HALT\'s WAVE_PLAN was planned under cache id %s, not %s'
                                        % (stem, str(wplan.get('cache_id'))[:16], ctx.cache_id[:16]))
            hp = ctx.work_dir / 'waves' / ('wave_%04d' % int(wave)) / 'HALT.json'
            halt = load_json_file(hp, 'HALT.json') if hp.is_file() else {}
            items = [it for it in halt.get('items') or [] if it.get('key') == e['key'] and it.get('token') == tok]
            if len(items) != 1:
                raise OrchestratorError('cache entry %s: no matching HALT item (L1)' % stem)
            want = resolution_entry(items[0], lines[0], e['theta'])
            if canonical(entry_core(dict(want, schema=SCHEMA_CACHE_ENTRY, cache_id=ctx.cache_id, key=e['key']))) != \
                    canonical(entry_core(e)):
                raise OrchestratorError('cache entry %s: content differs from its resolution (L1)' % stem)
        elif src == 'IN_PROCESS_TEST':
            if not ctx.synthetic:
                raise OrchestratorError('cache entry %s: IN_PROCESS_TEST entry in a non-synthetic cache' % stem)
            b = ctx.mapper.build(e['theta'])
            if b['sha256'] != pv.get('spec_sha256') and not pv.get('recovery'):
                raise OrchestratorError('cache entry %s: theta does not map to the recorded spec (M3)' % stem)
        else:
            raise OrchestratorError('cache entry %s: unknown source %r' % (stem, src))

    def forward(self, key):
        e = self.entries.get(key)
        return copy.deepcopy(e['forward']) if e is not None else None

    def put(self, *, key, theta, classification, failure_class, source, provenance, forward):
        if classification not in CACHED_CLASSES:
            raise OrchestratorError('only VALID and MODEL_INVALID are cached, not %r' % classification)
        e = {'schema': SCHEMA_CACHE_ENTRY, 'cache_id': self.ctx.cache_id, 'key': key,
             'theta': {k: float(v) for k, v in theta.items()}, 'classification': classification,
             'failure_class': failure_class, 'source': source, 'provenance': provenance, 'forward': forward,
             'ingested_utc': utc()}
        if theta_key(e['theta']) != key:
            raise OrchestratorError('cache put: key does not hash theta')
        e['entry_sha256'] = sha256_bytes(canonical(e))
        path = self.entries_dir / (key + '.json')
        if path.exists():
            old = load_json_file(path, 'cache entry %s' % key)
            if canonical(entry_core(old)) != canonical(entry_core(e)):          # M1: semantic core only
                raise OrchestratorError('cache entry %s exists with different content (never overwritten)' % key)
            self.entries[key] = old
            return old, False
        self._resolutions = None
        self._verify(e, key)
        try:
            write_json_atomic_x(path, e)
        except FileExistsError:
            return self.put(key=key, theta=theta, classification=classification, failure_class=failure_class,
                            source=source, provenance=provenance, forward=forward)
        self.entries[key] = e
        return e, True


def resolution_entry(item, line, theta):
    """The cache entry content of a root 'invalid' resolution: a pure function of (HALT item, RESOLUTIONS line)."""
    return {'theta': {k: float(v) for k, v in theta.items()}, 'classification': 'MODEL_INVALID',
            'failure_class': 'ROOT_DECLARED_INVALID_AFTER_%s:%s' % (item['class'], str(item['reason']).split(':')[0]),
            'source': 'ROOT_RESOLUTION',
            'provenance': {'wave': line['wave'], 'call_index': item['call_index'], 'halt_token': item['token'],
                           'halt_class': item['class'], 'halt_reason': item['reason'],
                           'resolution_line_sha256': sha256_bytes(canonical(line)), 'root_reason': line['reason'],
                           'call_dir': (item.get('provenance') or {}).get('call_dir')},
            'forward': {'valid': False, 'speeds_km_s': {},
                        'reasons': ['ROOT_DECLARED_INVALID after %s %s: %s' % (item['class'], item['reason'], line['reason'])]}}


# --------------------------------------------------------------------------------------------- engine probe (c2v001)
class Probe:
    """Runs the unmodified engine against the cache; c2v001 verbatim (see its docstring for the probe rules)."""

    def __init__(self, ctx):
        E = ctx.E
        self.ctx = ctx
        self.code_eval = E._evaluate_point.__code__
        self.code_jac = E.finite_difference_jacobian.__wrapped__.__code__
        self.code_explore = E._explore_impl.__code__
        nested = {c.co_name: c for c in self.code_explore.co_consts if isinstance(c, types.CodeType)}
        self.code_march = nested['march_side']
        self.code_gd = nested['global_design']
        self.code_evaluate = nested['evaluate']

    def context(self, f):
        if f is None or f.f_code is not self.code_eval:
            return {'family': ('unknown',), 'branch': ('unknown',), 'purpose': None, 'u': None, 'counter': None,
                    'm_id': 0}
        L = f.f_locals
        out = {'purpose': L.get('purpose'), 'u': list(L.get('u_list') or []), 'counter': L.get('counter'), 'm_id': 0}
        g = f.f_back
        if g is not None and g.f_code is self.code_jac:
            if out['purpose'] == 'seed':
                out.update(family=('seed',), branch=('seed',))
            else:
                out.update(family=('jacobian',), branch=('jac', int(g.f_locals['j'])))
            return out
        if g is None or g.f_code is not self.code_evaluate:
            out.update(family=('unknown',), branch=('unknown',))
            return out
        h = g.f_back
        x = h
        while x is not None and x.f_code is not self.code_explore:
            x = x.f_back
        if x is None:
            out.update(family=('unknown',), branch=('unknown',))
            return out
        XL = x.f_locals
        out['m_id'] = len(XL.get('ident') or [])
        purpose = out['purpose']
        if h.f_code is self.code_march:
            HL = h.f_locals
            rec = HL['rec']
            if HL.get('round0_k') is not None:
                out.update(family=('march0',), branch=('m0', int(HL['round0_k']), HL['round0_side']))
            else:
                rnd = int(XL['rnd'])
                if rec.get('kind') == 'lp_ray':
                    out.update(family=('lp', rnd), branch=('lp', rnd, int(rec['direction']), rec['side']))
                else:
                    out.update(family=('axis', rnd), branch=('ax', rnd, int(rec['anchor_log_index']),
                                                              int(rec['direction']), rec['side']))
        elif h.f_code is self.code_gd:
            HL = h.f_locals
            fam = ('gd_pre',) if HL['run_before_march'] else ('design',)
            out.update(family=fam, branch=('gd', int(HL['jj'])))
        elif h.f_code is self.code_explore and purpose == 'design':
            out.update(family=('design',), branch=('d', int(XL['jj'])))
        elif h.f_code is self.code_explore and purpose == 'repair':
            out.update(family=('repair',), branch=('repair', int(XL['it'])))
        else:
            out.update(family=('explore_%s' % purpose,), branch=(str(purpose),))
        return out

    def run(self, cache, mode, exclude=None):
        ctx = self.ctx
        exclude = set(exclude or ())
        st = {'misses': [], 'fake_family': None, 'faked': set(), 'entry': {}, 'branch_calls': {}, 'calls': 0, 'hits': 0,
              'placeholders': 0, 'families': [], 'keys_requested': [], 'stop': None}

        def fwd(theta):
            st['calls'] += 1
            c = self.context(sys._getframe(1))
            fam = c['family']
            if fam not in st['entry']:
                cnt = c['counter']
                st['entry'][fam] = (cnt['used'] - 1, cnt['budget']) if isinstance(cnt, dict) else (None, None)
                st['families'].append(fam)
            if st['fake_family'] is not None and fam != st['fake_family']:
                raise _ProbeStop('FAMILY_BOUNDARY_AFTER_PLACEHOLDERS')
            key = theta_key(theta)
            st['keys_requested'].append(key)
            if st['fake_family'] is not None:
                b0 = tuple(c['branch'])
                st['branch_calls'][b0] = st['branch_calls'].get(b0, 0) + 1
            got = None if key in exclude else cache.forward(key)
            if got is not None:
                st['hits'] += 1
                return got
            miss = {'key': key, 'theta': {k: float(v) for k, v in theta.items()}, 'family': list(fam),
                    'branch': list(c['branch']), 'purpose': c['purpose'], 'u': c['u'],
                    'sibling': st['fake_family'] is not None}
            br = tuple(c['branch'])
            if mode == 'replay':
                st['misses'].append(miss)
                raise _ProbeStop('REPLAY_MISS')
            if st['fake_family'] is None:
                st['misses'].append(miss)
                if fam[0] in SINGLE_FAMILIES or fam[0] == 'unknown' or fam[0].startswith('explore_'):
                    raise _ProbeStop('SINGLE_REQUEST_FAMILY')
                st['fake_family'] = fam
                st['branch_calls'] = {}
            elif br not in st['faked']:
                cnt = c['counter']
                extra = sum(max(0, ctx.branch_bound(fam) - st['branch_calls'].get(b, 0)) for b in st['faked'])
                if not isinstance(cnt, dict) or (cnt['used'] - 1) + extra >= cnt['budget']:
                    raise _ProbeStop('SIBLING_BUDGET_GUARD')
                st['misses'].append(miss)
            st['faked'].add(br)
            st['placeholders'] += 1
            return {'valid': False, 'speeds_km_s': {}, 'reasons': [PLACEHOLDER_REASON]}

        run = None
        try:
            run = ctx.E.run_calibration_region(forward=fwd, **ctx.run_kwargs())
        except _ProbeStop as stop:
            st['stop'] = stop.reason
        res = {'mode': mode, 'stop_reason': st['stop'], 'misses': st['misses'], 'calls': st['calls'],
               'hits': st['hits'], 'placeholders': st['placeholders'],
               'families': [list(f) for f in st['families']], 'keys_requested': st['keys_requested']}
        res['complete'] = st['stop'] is None and not st['misses'] and st['placeholders'] == 0
        res['run'] = run if res['complete'] else None
        return res


# --------------------------------------------------------------------------------------------- executors
class CampaignExecutor:
    """One wave = one campaign of the pinned campaign launcher (c2v003) in <wave_dir>/campaign."""

    def __init__(self, ctx):
        self.ctx = ctx

    def campaign_dict(self, plan):
        cfg = self.ctx.cfg
        return {'calls': [{'spec': c['spec']} for c in plan['calls']], 'max_concurrent': self.ctx.max_concurrent,
                'process_budget': self.ctx.process_budget, 'stage_aware': self.ctx.stage_aware,
                'per_call': cfg['per_call'], 'campaign_wall_cap_s': cfg['campaign_wall_cap_s'],
                'driver': cfg['driver'], 'monitor': cfg['monitor']}

    @staticmethod
    def call_markers(d):
        d = str(d)
        return [d + '/spec.json', d + '/out']

    def orphans(self, campaign_dir):
        out = []
        if not campaign_dir.is_dir():
            return out
        for d in sorted(campaign_dir.glob('call_*')):
            if (d / 'RECEIPT.json').exists():
                continue
            lp = d / 'RECEIPT.json.launch.json'
            pid = None
            if lp.is_file():
                try:
                    pid = json.loads(lp.read_text())['child_pid']
                except Exception:
                    pid = None
            procs = live_processes(self.call_markers(d))
            alive = pid_alive(pid) if pid else None
            if procs is None:
                alive = True
            elif procs:
                alive = True
            out.append({'call_dir': str(d), 'child_pid': pid, 'alive': alive,
                        'live_processes': procs if procs else [], 'launch_record': lp.is_file()})
        return out

    def wait_orphans(self, campaign_dir, log):
        ow = self.ctx.cfg.get('orphan_wait') or {}
        poll, cap, grace = float(ow.get('poll_s', 30.0)), float(ow.get('cap_s', 21600.0)), float(ow.get('receipt_grace_s', 120.0))
        t0 = time.monotonic()
        dead_since = {}
        seen = self.orphans(campaign_dir)
        while True:
            pend = self.orphans(campaign_dir)
            if not pend:
                return {'orphans_seen': len(seen), 'waited_s': time.monotonic() - t0, 'still_running': []}
            now = time.monotonic()
            waiting = []
            for o in pend:
                if o['alive'] is True:
                    waiting.append(o)
                else:
                    dead_since.setdefault(o['call_dir'], now)
                    if now - dead_since[o['call_dir']] < grace:
                        waiting.append(o)
            if not waiting:
                return {'orphans_seen': len(seen), 'waited_s': now - t0, 'still_running': [],
                        'dead_without_receipt': [o['call_dir'] for o in pend]}
            if now - t0 > cap:
                return {'orphans_seen': len(seen), 'waited_s': now - t0, 'still_running': waiting}
            log('waiting for %d orphaned call(s) of an interrupted wave' % len(waiting))
            time.sleep(poll)

    def execute(self, wave_dir, plan, resume, log):
        cdir = wave_dir / 'campaign'
        if not cdir.is_absolute():
            raise OrchestratorError('A7_ABSOLUTE_PATH: campaign dir %s is not absolute' % cdir)
        orph = {'orphans_seen': 0, 'waited_s': 0.0, 'still_running': []}
        if resume and cdir.exists():
            orph = self.wait_orphans(cdir, log)
            if orph['still_running']:
                return None, {'status': 'ORPHANS_STILL_RUNNING', 'orphans': orph}
        out = self.ctx.C.run_campaign(campaign=self.campaign_dict(plan), campaign_dir=str(cdir),
                                      resume=bool(resume and cdir.exists()), python=self.ctx.python)
        if not out.get('ok'):
            raise OrchestratorError('campaign refused: %s' % out.get('reasons'))
        meta = {k: out.get(k) for k in ('status', 'launched', 'max_concurrent_observed', 'max_accounted_processes',
                                        'process_budget', 'stage_aware', 'n_ok', 'n_failed', 'n_resumed',
                                        'n_not_started', 'n_unverified', 'campaign_wall_used_s', 'summary_path')}
        meta['orphans'] = orph
        return out['calls'], meta

    def classify(self, plan_call, rec):
        """-> (class, code, forward or None, provenance).  v005 C4-1: every read of the call directory is guarded; an
        OSError outside the result / finish reads is INFRA CALL_DIR_UNREADABLE (never resolvable as invalid)."""
        prov = {'call_dir': rec.get('call_dir'), 'campaign_status': normalize_campaign_status(rec.get('status')),
                'spec_sha256': plan_call['spec_sha256']}
        try:
            return self._classify(plan_call, rec, prov)
        except OSError as exc:
            return 'INFRA', 'CALL_DIR_UNREADABLE:%s: %s' % (type(exc).__name__, str(exc)[:120]), None, prov

    def _classify(self, plan_call, rec, prov):
        ctx = self.ctx
        st = prov['campaign_status']                                        # M1
        if st not in ('OK', 'FAILED'):
            return 'INFRA', 'CAMPAIGN_%s' % st, None, prov
        d = Path(rec['call_dir'])
        rp = d / 'RECEIPT.json'
        if not rp.is_file():
            return 'INFRA', 'NO_RECEIPT', None, prov
        v = ctx.M.verify_receipt(rp, spec_sha256=plan_call['spec_sha256'], driver_sha256=ctx.driver['sha256'])
        if not v['ok']:
            return 'INFRA', 'RECEIPT_UNVERIFIED: %s' % v['reasons'], None, prov
        r = v['receipt']
        prov.update({'receipt_path': str(rp), 'receipt_file_sha256': sha256_file(rp),
                     'receipt_sha256_self': r.get('receipt_sha256'), 'monitor_status': r.get('status'),
                     'driver_status': r.get('driver_status'), 'exit_code': r.get('exit_code'),
                     'stop_reason': r.get('stop_reason'), 'elapsed_seconds': r.get('elapsed_seconds'),
                     'peak_rss_bytes': r.get('peak_rss_bytes'), 'final_output_bytes': r.get('final_output_bytes'),
                     'driver_sha256': ctx.driver['sha256']})
        if not (d / 'spec.json').is_file() or sha256_file(d / 'spec.json') != plan_call['spec_sha256']:
            return 'INFRA', 'SPEC_FILE_MISMATCH', None, prov
        if str(r.get('status', '')).startswith('STOPPED_'):
            return 'INFRA', 'MONITOR_%s' % r['status'], None, prov
        pin = r.get('result')
        if not pin:
            return 'INFRA', 'NO_RESULT_JSON', None, prov
        try:                                                                # v005 C4-1 (B1-F1, B5-2)
            raw = Path(pin['path']).read_bytes()
        except (OSError, TypeError, KeyError) as exc:
            return 'INFRA', 'RESULT_UNPARSEABLE:%s' % type(exc).__name__, None, prov
        if sha256_bytes(raw) != pin['sha256']:
            return 'INFRA', 'RESULT_HASH', None, prov
        prov.update({'result_path': pin['path'], 'result_sha256': pin['sha256']})
        try:
            res = json.loads(raw.decode('utf-8'))
        except (ValueError, UnicodeDecodeError) as exc:                    # truncated / torn / non-UTF-8 bytes
            return 'INFRA', 'RESULT_UNPARSEABLE:%s' % type(exc).__name__, None, prov
        if not isinstance(res, dict):
            return 'INFRA', 'RESULT_UNPARSEABLE:not an object', None, prov
        if res.get('call_spec_sha256') != plan_call['spec_sha256'] or res.get('driver_sha256') != ctx.driver['sha256']:
            return 'INFRA', 'RESULT_NOT_BOUND_TO_SPEC_OR_DRIVER', None, prov
        fin, why = finish_binding(pin['path'], pin['sha256'])          # F1: finish.json -> result binding
        if why:
            return 'INFRA', why, None, prov
        prov['finish'] = fin
        ds = r.get('driver_status')
        if ds != res.get('status'):
            return 'INFRA', 'DRIVER_STATUS_MISMATCH %r/%r' % (ds, res.get('status')), None, prov
        ev = collect_evidence(Path(pin['path']).parent, res, ctx.row_ids, ctx.taxonomy)
        out = ctx.taxonomy.classify(res, ev)
        prov['taxonomy'] = tax_record(out, ctx.taxonomy)
        prov['evidence_files'] = ev['files']
        prov['route_a'] = {k: (ev.get('route_a') or {}).get(k) for k in ('end_outcomes', 'iterations', 'converged',
                                                                       'max_iterations')}
        prov['passes_history'] = ev.get('passes_history')
        if out['class'] in CACHED_CLASSES:
            code = out['code'] if out['class'] != 'VALID' else None
            return out['class'], code, forward_from_result(res, out['class'], code, out['rule'], ctx.row_ids), prov
        return out['class'], out['code'], None, prov


class InProcessExecutor:
    """SYNTHETIC TESTS ONLY: evaluates a Python forward(call_spec) in process (no monitor, no receipts)."""

    def __init__(self, ctx, spec_forward):
        if not ctx.synthetic:
            raise OrchestratorError('InProcessExecutor requires synthetic_test')
        self.ctx = ctx
        self.spec_forward = spec_forward

    def execute(self, wave_dir, plan, resume, log):
        recs = []
        for c in plan['calls']:
            recs.append({'status': 'IN_PROCESS', 'forward': self.spec_forward(c['spec'])})
        return recs, {'status': 'IN_PROCESS', 'launched': len(recs), 'orphans': None}

    def classify(self, plan_call, rec):
        f = rec['forward']
        prov = {'executor': 'IN_PROCESS_TEST_ONLY', 'spec_sha256': plan_call['spec_sha256']}
        if not isinstance(f, dict):
            return 'INFRA', 'IN_PROCESS_NON_DICT', None, prov
        cls = f.get('_class')
        if cls in HALT_CLASSES:
            return cls, f.get('_code', 'IN_PROCESS_%s' % cls), None, prov
        jc = bool(f.get('_judgment'))
        f = {k: v for k, v in f.items() if not k.startswith('_')}
        if f.get('valid') is True:
            prov['taxonomy'] = {'rule': 'IN_PROCESS', 'code': 'VALID', 'class': 'VALID', 'judgment_call': False,
                                'detail': None, 'taxonomy_sha256': None}
            return 'VALID', None, copy.deepcopy(f), prov
        prov['taxonomy'] = {'rule': 'IN_PROCESS', 'code': 'IN_PROCESS_INVALID', 'class': 'MODEL_INVALID',
                            'judgment_call': jc, 'detail': None, 'taxonomy_sha256': None}
        return 'MODEL_INVALID', 'IN_PROCESS_INVALID', copy.deepcopy(f), prov


# --------------------------------------------------------------------------------------------- orchestrator
class Lock:
    """L4: a lock whose holder pid is alive and whose command is this orchestrator is LOCKED, whatever the host name
    (macOS host names change with the network).  An unreadable process table counts as alive (fail closed).
    F2 (CHECK_SOFTWARE_V001): the lock file appears atomically WITH its content (exclusive temp file, fsync, os.link into
    place), so no contender can read a created-but-empty lock of this version; an empty or unparseable lock (another
    writer, a torn legacy lock) is treated as live until its mtime is LOCK_EMPTY_LIVE_S old; a stale takeover renames the
    lock it judged stale and verifies the renamed bytes are the bytes it judged (otherwise it restores the link and
    reports LOCKED).
    F4 (CHECK_SOFTWARE_V001 of c2v004; v004a): the mutual exclusion is fcntl.flock(LOCK_EX | LOCK_NB) on ORCHESTRATOR.lock,
    a file this orchestrator never renames or unlinks (it is created once with O_EXCL); the kernel releases the flock when
    the holding process dies, so no stale judgement or rename decides who holds.  After the flock, the path must still
    name the inode that was flocked (otherwise retry).  The v004 holder record (pid, utc, host, module, cmd_marker) is
    written in place only while the flock is held, and is marked released_utc on release.  The v004 content rules are
    kept, judged under the flock, as a fail-closed guard against a holder that does not flock (a v004 process, a foreign
    writer): a record of a live orchestrator -> LOCKED; an empty or unparseable file younger than LOCK_EMPTY_LIVE_S ->
    LOCKED, except the empty file this call created; any other record is stale: its bytes are kept in a new
    ORCHESTRATOR.lock.stale_<utc>_<pid>_<mypid> copy (exclusive create) and are overwritten only if they are still the
    bytes judged (otherwise LOCKED).  The process that created the file retries the non-blocking flock for up to
    CREATOR_FLOCK_WAIT_S: a contender that flocks the creator's still-empty file only judges it (empty and fresh ->
    LOCKED) and lets go, so without the retry every contender of a fresh work dir could report LOCKED."""
    CREATOR_FLOCK_WAIT_S = 5.0

    def __init__(self, work_dir):
        self.path = Path(work_dir) / 'ORCHESTRATOR.lock'
        self.held = False
        self.stale = None
        self._fd = None
        self._created = False

    @staticmethod
    def holder_alive(old):
        pid = old.get('pid')
        if not pid_alive(pid):
            return False
        cmd = process_command(pid)
        if cmd is None:
            return True
        marker = old.get('cmd_marker')
        return (MODULE_NAME in cmd or any(m in cmd for m in LEGACY_MODULE_NAMES)
                or (isinstance(marker, str) and bool(marker) and marker in cmd))

    def _judge(self):
        """Called only while the flock is held.  -> ('gone', bytes) free: the empty file this call created, or a record
        marked released | ('live', None) | ('stale', bytes judged) | ('gone', None) the path vanished (foreign unlink)."""
        try:
            raw = self.path.read_bytes()
            mtime = os.stat(self.path).st_mtime
        except FileNotFoundError:
            return 'gone', None
        except OSError:
            return 'live', None                           # v005 C4-1: an unreadable lock file counts as held (fail closed)
        if self._created and raw == b'':
            return 'gone', raw                            # F4: the file this call created (O_EXCL), not yet written
        try:
            old = json.loads(raw.decode('utf-8'))
            if not isinstance(old, dict) or not old:
                old = None
        except (ValueError, UnicodeDecodeError):
            old = None
        if old is None:
            if time.time() - mtime < LOCK_EMPTY_LIVE_S:
                return 'live', None                       # F2: an empty / unparseable lock may be a lock being written
            return 'stale', raw
        if old.get('released_utc'):
            return 'gone', raw                            # F4: released by its holder (the flock is ours now)
        if self.holder_alive(old):
            return 'live', None
        return 'stale', raw

    def _write_fd(self, data):
        os.pwrite(self._fd, data, 0)                      # in place: the lock file is never renamed or unlinked
        os.ftruncate(self._fd, len(data))
        os.fsync(self._fd)

    def _drop(self):
        fd, self._fd = self._fd, None
        if fd is not None:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            finally:
                os.close(fd)

    def acquire(self):
        body = canonical({'pid': os.getpid(), 'utc': utc(), 'host': socket.gethostname(), 'module': MODULE_NAME,
                          'cmd_marker': os.path.basename(sys.argv[0] or '')})
        if self.held or self._fd is not None:
            raise OrchestratorError('Lock.acquire called twice on one Lock')
        for _ in range(4):
            created = False
            try:
                try:
                    fd = os.open(self.path, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
                    created = True
                except FileExistsError:
                    fd = os.open(self.path, os.O_RDWR | os.O_NOFOLLOW)
            except FileNotFoundError:
                continue
            except OSError as exc:
                if exc.errno == errno.ELOOP:
                    return False                          # a symlink at the lock path: fail closed (LOCKED)
                if exc.errno in (errno.EACCES, errno.EPERM):
                    return False                          # v005 C4-1: an unreadable lock file counts as held (LOCKED)
                raise
            self._fd, self._created = fd, created
            try:
                deadline = time.monotonic() + self.CREATOR_FLOCK_WAIT_S if created else None
                while True:
                    try:
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        break
                    except OSError as exc:
                        if exc.errno not in (errno.EWOULDBLOCK, errno.EAGAIN):
                            raise
                        if deadline is None or time.monotonic() >= deadline:
                            self._drop()
                            return False                  # F4: another process holds the flock
                        time.sleep(0.01)                  # the creator outwaits contenders that only judge its file
                try:
                    sp, sf = os.stat(self.path, follow_symlinks=False), os.fstat(fd)
                except FileNotFoundError:
                    self._drop()
                    continue
                if (sp.st_dev, sp.st_ino) != (sf.st_dev, sf.st_ino):
                    self._drop()                          # F4: the path names another inode now (foreign rename)
                    continue
                state, raw = self._judge()
                if state == 'live':
                    self._drop()
                    return False
                if raw is None:
                    self._drop()
                    continue
                if state == 'stale':
                    pid = None
                    try:
                        pid = json.loads(raw.decode('utf-8')).get('pid')
                    except Exception:
                        pass
                    stale = str(self.path) + '.stale_%s_%s_%d' % (utc_compact(), pid, os.getpid())
                    try:
                        with open(stale, 'xb') as fh:     # the stale record is kept as a copy; the lock is never moved
                            fh.write(raw)
                            fh.flush()
                            os.fsync(fh.fileno())
                    except FileExistsError:
                        self._drop()
                        return False
                    self.stale = stale
                try:
                    now = self.path.read_bytes()
                except FileNotFoundError:
                    now = None
                if now != raw:                            # a writer that does not flock changed it: LOCKED
                    self._drop()
                    return False
                self._write_fd(body)
                self.held = True
                return True
            except BaseException:
                self._drop()
                raise
        return False

    def release(self):
        if self.held:
            try:
                old = json.loads(self.path.read_text())
                if isinstance(old, dict) and old.get('pid') == os.getpid() and not old.get('released_utc'):
                    self._write_fd(canonical(dict(old, released_utc=utc())))   # in place; the file is kept
            except (OSError, ValueError):
                pass
            self.held = False
        self._drop()


class Orchestrator:
    def __init__(self, ctx, executor=None, log=None):
        self.ctx = ctx
        self.executor = executor if executor is not None else (
            CampaignExecutor(ctx) if ctx.executor_kind == 'campaign' else None)
        if self.executor is None:
            raise OrchestratorError('in_process_test configs need an explicit InProcessExecutor')
        self.cache = Cache(ctx)
        self.probe = Probe(ctx)
        self.waves_dir = ctx.work_dir / 'waves'
        self.ledger_path = ctx.work_dir / 'LAUNCH_LEDGER.jsonl'
        self.resolution_path = ctx.work_dir / 'RESOLUTIONS.jsonl'
        self.events_path = ctx.work_dir / 'EVENTS.jsonl'
        self._log = log or (lambda m: print('[%s] %s' % (utc(), m), file=sys.stderr, flush=True))
        self.alias = None
        self.work_dir_json = None

    def log(self, msg, **kw):
        self._log(msg)
        if self.ctx.work_dir.is_dir():
            append_jsonl(self.events_path, dict({'utc': utc(), 'pid': os.getpid(), 'msg': msg}, **kw))

    # ---------------------------------------------------------------- setup
    @staticmethod
    def _work_dir_json_core(d):
        return {'configured': d.get('configured'), 'resolved': d.get('resolved'), 'volume': d.get('volume'),
                'volume_uuid': d.get('volume_uuid'), 'work_dir_st_ino': d.get('work_dir_st_ino'),
                'symlinks': [{'link': x.get('link'), 'target': x.get('target')} for x in d.get('symlinks') or []]}

    def check_work_dir_json(self, create):
        """F3: WORK_DIR.json is the work dir's own identity record (configured and resolved path, symlinks crossed,
        volume, VolumeUUID, inode of the resolved work dir).  Compared in prepare (run), plan, status and resolve; a
        populated work dir without it is refused; with create=True a missing record is written (fresh work dir only).
        Returns 'NOT_CREATED' | 'MATCHES' | 'WRITTEN'."""
        ctx = self.ctx
        wd = ctx.work_dir
        if not wd.is_dir():
            if create:
                raise OrchestratorError('F3: work dir %s does not exist at prepare' % wd)
            return 'NOT_CREATED'
        if os.path.realpath(str(wd)) != ctx.work_dir_record['resolved']:
            raise OrchestratorError('F3: WORK_DIR_REPOINTED: %s now resolves to %s, not %s'
                                    % (wd, os.path.realpath(str(wd)), ctx.work_dir_record['resolved']))
        cur = dict(ctx.work_dir_record, work_dir_st_ino=os.stat(ctx.work_dir_record['resolved']).st_ino,
                   existing_ancestor=ctx.work_dir_record['resolved'],
                   runtime=ctx.runtime, module=MODULE_NAME)                 # v005 SF4: recorded, compared per wave
        p = wd / 'WORK_DIR.json'
        if p.exists():
            old = load_json_file(p, 'WORK_DIR.json')
            if old.get('schema') != SCHEMA_WORKDIR or \
                    canonical(self._work_dir_json_core(old)) != canonical(self._work_dir_json_core(cur)):
                raise OrchestratorError('F3: WORK_DIR.json identity differs from the current work dir (re-pointed link, '
                                        'copied or replaced tree, or another volume): recorded %s, now %s'
                                        % (self._work_dir_json_core(old), self._work_dir_json_core(cur)))
            return 'MATCHES'
        populated = [m for m in WORK_DIR_MARKERS if (wd / m).exists()]
        if populated:
            raise OrchestratorError('F3: work dir %s holds %s but no WORK_DIR.json (refused: identity unknown)'
                                    % (wd, populated))
        if not create:
            return 'NOT_CREATED'
        write_json_idempotent(p, cur, self._work_dir_json_core)
        return 'WRITTEN'

    def prepare(self, create, init_work_dir=None):
        """create: open the cache for writing.  init_work_dir (v005 SF2): whether a fresh WORK_DIR.json may be written;
        run passes it explicitly (True only with --new-campaign); None (direct in-process callers) means create.  With
        create and without init, a work dir that has no WORK_DIR.json is refused."""
        init = bool(create if init_work_dir is None else init_work_dir)
        if init:
            self.ctx.work_dir.mkdir(parents=True, exist_ok=True)
        self.work_dir_json = self.check_work_dir_json(init)
        if create and self.work_dir_json == 'NOT_CREATED':
            raise OrchestratorError('SF2 WORK_DIR_NOT_INITIALIZED: %s has no WORK_DIR.json (absent, moved or emptied work '
                                    'dir); a fresh campaign needs run --new-campaign' % self.ctx.work_dir)
        self.check_plan_cache_ids()                                          # v005 C4-2, before the cache opens
        if create:
            cfg_copy = self.ctx.work_dir / ('CONFIG_COPY_%s.json' % self.ctx.config_sha256[:16])
            if not cfg_copy.exists():
                write_json_atomic_x(cfg_copy, self.ctx.cfg)
        self.cache.open(create=create)
        if create:
            self.materialize_invalid_resolutions()
        self.alias = self.install_anchor_alias(write=create)
        return self.alias

    def plan_cache_id_mismatches(self):
        """C4-2: committed WAVE_PLANs planned under another cache id (a config change that changed the cache id)."""
        bad = []
        for w, wd in sorted(self.committed_waves().items()):
            p = load_json_file(wd / 'WAVE_PLAN.json', 'wave plan')
            if p.get('cache_id') != self.ctx.cache_id:
                bad.append({'wave': w, 'cache_id': p.get('cache_id'), 'config_sha256': p.get('config_sha256')})
        return bad

    def check_plan_cache_ids(self):
        bad = self.plan_cache_id_mismatches()
        if bad:
            raise OrchestratorError('C4-2 config changed: use a new work dir (committed wave(s) %s were planned under cache '
                                    'id(s) %s; this config gives %s; a work dir holds one cache id)'
                                    % ([b['wave'] for b in bad], sorted(set(str(b['cache_id'])[:16] for b in bad)),
                                       self.ctx.cache_id[:16]))

    def check_runtime(self):
        """SF4: the runtime identity now must equal the one WORK_DIR.json recorded when the campaign started."""
        p = self.ctx.work_dir / 'WORK_DIR.json'
        old = load_json_file(p, 'WORK_DIR.json').get('runtime') if p.is_file() else None
        now = runtime_identity(self.ctx.python)
        if not isinstance(old, dict):
            return ['SF4 RUNTIME_NOT_RECORDED: WORK_DIR.json carries no runtime identity']
        d = runtime_differences(old, now)
        return ['SF4 RUNTIME_CHANGED at %s (recorded when the campaign started; a mixed-runtime cache is refused)' % d] \
            if d else []

    def check_identity_now(self):
        """SF1: re-resolve the work dir now and compare it with the config pin, the Context record and WORK_DIR.json."""
        ctx = self.ctx
        bad = []
        try:
            rec = resolve_work_dir(ctx.cfg.get('work_dir'), ctx.cfg.get('work_dir_volume'))
        except OrchestratorError as exc:
            return ['SF1 %s' % exc]
        if rec['resolved'] != ctx.work_dir_record['resolved']:
            bad.append('SF1 WORK_DIR_REPOINTED: %s now resolves to %s, not %s' % (ctx.work_dir, rec['resolved'],
                                                                                  ctx.work_dir_record['resolved']))
        if ctx.work_dir_identity.get('pinned'):
            bad.extend('SF1 %s' % b for b in check_work_dir_identity(ctx.work_dir_identity['pin'], rec))
        if not bad:
            try:
                if self.check_work_dir_json(False) != 'MATCHES':
                    bad.append('SF1 WORK_DIR_JSON_MISSING: %s/WORK_DIR.json is gone' % ctx.work_dir)
            except OrchestratorError as exc:
                bad.append('SF1 %s' % exc)
        return bad

    def pre_wave_checks(self, label):
        """v005: SF1 + SF4 + B2-2 + C4-2 before every wave (new or resumed); any failure refuses (exit 3)."""
        bad = self.check_identity_now()
        if bad:                                   # SF1: nothing is written into a tree whose identity is broken
            self._log('refused before %s: %s' % (label, bad))
            raise OrchestratorError('refused before %s: %s' % (label, '; '.join(bad)[:1500]))
        bad.extend(self.check_runtime())
        bad.extend(self.ctx.recheck(label))
        m = self.plan_cache_id_mismatches()
        if m:
            bad.append('C4-2 config changed: use a new work dir (%s)' % m)
        if bad:
            self.log('refused before %s' % label, reasons=bad)
            raise OrchestratorError('refused before %s: %s' % (label, '; '.join(bad)[:1500]))

    def materialize_invalid_resolutions(self):
        """M2/L1 crash window: a RESOLUTIONS 'invalid' line whose cache entry is missing (crash between the line and the
        put) gets its entry, a pure function of (HALT item, line).  v005 C4-2: only a line of this cache id whose HALT's
        WAVE_PLAN is of this cache id (anything else refuses)."""
        made = []
        for ln in self.cache.resolutions():
            if ln.get('decision') != 'invalid' or ln.get('key') in self.cache.entries:
                continue
            if ln.get('cache_id') != self.ctx.cache_id:
                raise OrchestratorError('C4-2: RESOLUTIONS invalid line for %s was written under cache id %s, not %s: '
                                        'config changed, use a new work dir' % (str(ln.get('key'))[:16],
                                                                               str(ln.get('cache_id'))[:16],
                                                                               self.ctx.cache_id[:16]))
            item, plan_call = self._halt_item(ln['wave'], ln['token'])
            ent = resolution_entry(item, ln, plan_call['theta'])
            self.cache.put(key=ln['key'], **ent)
            made.append(ln['key'])
        if made:
            self.log('materialized %d root invalid resolution(s) after an interrupted resolve' % len(made))
        return made

    def _halt_item(self, wave, token):
        wd = self.waves_dir / ('wave_%04d' % int(wave))
        halt = load_json_file(wd / 'HALT.json', 'HALT.json of wave %s' % wave)
        plan = load_json_file(wd / 'WAVE_PLAN.json', 'WAVE_PLAN.json of wave %s' % wave)
        if plan.get('cache_id') != self.ctx.cache_id:                       # v005 C4-2
            raise OrchestratorError('C4-2: wave %s was planned under cache id %s, not %s: config changed, use a new work '
                                    'dir' % (wave, str(plan.get('cache_id'))[:16], self.ctx.cache_id[:16]))
        items = [it for it in halt.get('items') or [] if it.get('token') == token]
        if len(items) != 1:
            raise OrchestratorError('token %s is not an item of the HALT of wave %s' % (str(token)[:16], wave))
        by_key = {c['key']: c for c in plan['calls']}
        return items[0], by_key[items[0]['key']]

    def install_anchor_alias(self, write):
        ctx = self.ctx
        an = ctx.cfg.get('anchor')
        if not an or not an.get('use'):
            return {'used': False, 'reason': 'ANCHOR_DISABLED_IN_CONFIG'}
        if set(an) - ANCHOR_KEYS:
            raise OrchestratorError('anchor keys must be %s (accept_driver_equivalence is gone, C5): extra %s'
                                    % (sorted(ANCHOR_KEYS), sorted(set(an) - ANCHOR_KEYS)))
        if not ctx.numerics_is_template:
            return {'used': False, 'reason': 'NUMERICS_DIFFER_FROM_ANCHOR (seed will be computed)'}
        if an['spec_sha256'] != ctx.template_sha256:
            raise OrchestratorError('anchor spec sha is not the template sha')
        if an['driver_sha256'] != ctx.driver['sha256']:
            return {'used': False, 'reason': 'ANCHOR_DRIVER_DIFFERS (C5: no driver-equivalence shortcut)'}
        read_pinned(an['receipt'], 'anchor receipt')
        v = ctx.M.verify_receipt(an['receipt']['path'], spec_sha256=an['spec_sha256'], driver_sha256=an['driver_sha256'])
        if not v['ok']:
            raise OrchestratorError('anchor receipt does not verify: %s' % v['reasons'])
        rec = v['receipt']
        if rec.get('status') != 'FINISHED' or rec.get('driver_status') != 'COMPLETED' or \
                (rec.get('result') or {}).get('sha256') != an['result']['sha256']:
            raise OrchestratorError('anchor receipt is not a FINISHED/COMPLETED receipt of the pinned result')
        res = json.loads(read_pinned(an['result'], 'anchor result').decode('utf-8'))
        if res.get('call_spec_sha256') != ctx.template_sha256 or res.get('driver_sha256') != an['driver_sha256'] or \
                res.get('valid') is not True or res.get('status') != 'COMPLETED':
            raise OrchestratorError('anchor result does not bind to the template spec / driver or is not valid')
        sp = res.get('speeds_km_s') or {}
        if any(rid not in sp or not math.isfinite(sp[rid]) for rid in ctx.row_ids):
            raise OrchestratorError('anchor result lacks finite speeds for the region rows')
        out, ev = classify_alias_result(ctx, an['result']['path'], res)        # S3: never past the taxonomy
        if out['rule'] != 'R01' or out['class'] != 'VALID':
            raise OrchestratorError('S3: the anchor alias result classifies %s/%s (%s) under the taxonomy, not R01 VALID; '
                                    'set anchor.use false or pin a converged anchor' % (out['class'], out['rule'],
                                                                                      out['code']))
        nat = ctx.E.to_natural(spec=ctx.es, u=ctx.trial_u)
        if not nat['ok']:
            raise OrchestratorError('to_natural at trial_u: %s' % nat['reasons'])
        theta = nat['theta_natural']
        built = ctx.mapper.build(theta)
        tp, bp = ctx.template['physical'], built['spec']['physical']
        dev = {}
        for k in tp:
            dev[k] = 0.0 if tp[k] == bp[k] else abs(bp[k] - tp[k]) / abs(tp[k])
        if max(dev.values()) > ANCHOR_ALIAS_RTOL:
            raise OrchestratorError('anchor alias: mapped seed physical deviates beyond %g: %r' % (ANCHOR_ALIAS_RTOL, dev))
        other = [p for p in diff_paths({k: v for k, v in ctx.template.items() if k != 'physical'},
                                       {k: v for k, v in built['spec'].items() if k != 'physical'}) if p != 'label']
        if other:
            raise OrchestratorError('anchor alias: non-physical fields differ: %s' % other)
        prov = {'anchor_receipt_path': an['receipt']['path'], 'anchor_receipt_file_sha256': an['receipt']['sha256'],
                'anchor_receipt_sha256_self': rec.get('receipt_sha256'), 'result_path': an['result']['path'],
                'result_sha256': an['result']['sha256'], 'anchor_spec_sha256': an['spec_sha256'],
                'anchor_driver_sha256': an['driver_sha256'], 'alias_spec_sha256_not_launched': built['sha256'],
                'relative_deviation': dev, 'alias_rtol': ANCHOR_ALIAS_RTOL, 'elapsed_seconds': rec.get('elapsed_seconds'),
                'taxonomy': tax_record(out, ctx.taxonomy), 'evidence_files': ev['files']}
        fwd = {'valid': True, 'speeds_km_s': {rid: float(sp[rid]) for rid in ctx.row_ids}, 'reasons': []}
        if write:
            self.cache.put(key=built['key'], theta=theta, classification='VALID', failure_class=None,
                           source='ANCHOR_ALIAS', provenance=prov, forward=fwd)
        elif built['key'] not in self.cache.entries:
            self.cache.entries[built['key']] = {'key': built['key'], 'forward': fwd, 'classification': 'VALID',
                                                'source': 'ANCHOR_ALIAS(unwritten)'}
        return {'used': True, 'key': built['key'], 'max_relative_deviation': max(dev.values()), 'taxonomy_rule': out['rule']}

    # ---------------------------------------------------------------- waves, ledger (F3), tokens (M2)
    def wave_dirs(self):
        if not self.waves_dir.is_dir():
            return []
        return sorted(p for p in self.waves_dir.glob('wave_*') if p.is_dir())

    def committed_waves(self):
        out = {}
        for wd in self.wave_dirs():
            p = wd / 'WAVE_PLAN.json'
            if p.is_file():
                d = load_json_file(p, 'wave plan')
                if 'wave' not in d:
                    raise OrchestratorError('unreadable wave plan %s' % p)
                out[d['wave']] = wd
        return out

    def ledger(self):
        committed = self.committed_waves()
        return [ln for ln in read_jsonl(self.ledger_path) if ln.get('wave') in committed]

    def launches(self):
        n = {}
        for ln in self.ledger():
            n[ln['key']] = n.get(ln['key'], 0) + 1
        return n

    def last_launch_wave(self):
        w = {}
        for ln in self.ledger():
            w[ln['key']] = max(w.get(ln['key'], 0), int(ln['wave']))
        return w

    def consumed_tokens(self):
        return set(ln['authorized_by'] for ln in self.ledger() if ln.get('authorized_by'))

    def pending_authorizations(self):
        """M2: key -> the unused retry resolution of the key's latest committed launch (at most one per key)."""
        last, used = self.last_launch_wave(), self.consumed_tokens()
        out = {}
        for ln in self.cache.resolutions():
            if ln.get('decision') in RETRY_DECISIONS and ln.get('wave') == last.get(ln.get('key')) \
                    and ln.get('token') not in used and ln.get('cache_id') == self.ctx.cache_id:   # v005 C4-2
                out[ln['key']] = ln
        return out

    def make_plan(self, wave_no, misses):
        calls, seen = [], set()
        auths = self.pending_authorizations()
        for m in misses:
            if m['key'] in seen:
                continue
            seen.add(m['key'])
            auth = auths.get(m['key'])
            rec = None
            if auth and auth.get('recovery'):
                rec = self.ctx.recovery_rule(auth['recovery']['path'])
                if rec['sha256'] != auth['recovery']['sha256']:
                    raise OrchestratorError('recovery rule bytes changed since the resolve: %s' % rec['path'])
            b = self.ctx.mapper.build(m['theta'], recovery=rec)
            if b['key'] != m['key']:
                raise OrchestratorError('mapper key differs from probe key')
            self.ctx.prelaunch_check(b['spec'], recovery=rec is not None)
            calls.append({'call_index': len(calls), 'key': m['key'], 'theta': m['theta'], 'family': m['family'],
                          'branch': m['branch'], 'purpose': m['purpose'], 'u': m['u'], 'sibling': m['sibling'],
                          'spec': b['spec'], 'spec_sha256': b['sha256'], 'changed_paths': b['changed_paths'],
                          'authorized_by': auth['token'] if auth else None,
                          'recovery': ({k: rec[k] for k in ('path', 'sha256', 'rule_id')} if rec else None)})
        w = self.ctx.weights
        per_batch = max(1, min(self.ctx.max_concurrent, self.ctx.process_budget // max(1, w['peak'])))
        return {'schema': SCHEMA_WAVE_PLAN, 'wave': wave_no, 'created_utc': utc(), 'cache_id': self.ctx.cache_id,
                'module': MODULE_NAME, 'calls': calls, 'n_calls': len(calls),
                # v005 C4-2 / B2-2 / SF4: what the wave was planned under
                'config_sha256': self.ctx.config_sha256, 'gate_digest': self.ctx.gate_digest,
                'base_spec_sha256': self.ctx.base_sha256, 'runtime': self.ctx.runtime,
                'orchestrator_sha256': sha256_file(os.path.realpath(__file__)), 'session': session_record(),
                'families': sorted(set(tuple(c['family']) for c in calls)),
                'max_concurrent': self.ctx.max_concurrent, 'process_budget': self.ctx.process_budget,
                'stage_aware_budget': self.ctx.stage_aware, 'call_weights': w,
                'column_workers': self.ctx.column_workers,
                'batches': int(math.ceil(len(calls) / float(per_batch))),
                'batches_rule': 'conservative estimate: calls launched together at peak weight %d within budget %d'
                                % (w['peak'], self.ctx.process_budget)}

    def disk_ok(self, n_calls):
        f = self.ctx.disk_forecast(n_calls)
        return f['next_wave_fits'], f

    def ingest(self, wave_dir, plan, records, meta):
        n = {'VALID': 0, 'MODEL_INVALID': 0, 'NUMERICS_LIMITED': 0, 'INFRA': 0, 'already_cached': 0}
        halt = []
        out_calls = []
        launched = self.launches()
        for c, rec in zip(plan['calls'], records):
            cls, fc, fwd, prov = self.executor.classify(c, rec)
            prov = dict(prov, wave=plan['wave'], call_index=c['call_index'], recovery=c.get('recovery'),
                        authorized_by=c.get('authorized_by'))
            if cls in HALT_CLASSES:
                n[cls] += 1
                tok = halt_token(self.ctx.cache_id, plan['wave'], c['key'], c['call_index'], cls, fc,
                                 launched.get(c['key'], 1))
                halt.append({'key': c['key'], 'call_index': c['call_index'], 'class': cls, 'reason': fc, 'token': tok,
                             'never_resolve_invalid': self.ctx.taxonomy.never_invalid_code(fc), 'provenance': prov})
                out_calls.append({'key': c['key'], 'classification': cls, 'reason': fc})
                continue
            src = 'WAVE' if isinstance(self.executor, CampaignExecutor) else 'IN_PROCESS_TEST'
            _, new = self.cache.put(key=c['key'], theta=c['theta'], classification=cls, failure_class=fc, source=src,
                                    provenance=prov, forward=fwd)
            n[cls] += 1
            if not new:
                n['already_cached'] += 1
            out_calls.append({'key': c['key'], 'classification': cls, 'failure_class': fc,
                              'taxonomy': prov.get('taxonomy'), 'elapsed_seconds': prov.get('elapsed_seconds'),
                              'peak_rss_bytes': prov.get('peak_rss_bytes'),
                              'final_output_bytes': prov.get('final_output_bytes')})
        n_core = {k: v for k, v in n.items() if k != 'already_cached'}
        result = {'schema': SCHEMA_WAVE_RESULT, 'wave': plan['wave'], 'utc': utc(), 'counts': n_core, 'calls': out_calls,
                  'campaign': meta, 'halt': halt, 'already_cached_at_ingest': n['already_cached']}
        if halt:
            write_json_idempotent(wave_dir / 'HALT.json', {
                'schema': SCHEMA_HALT, 'wave': plan['wave'], 'utc': utc(), 'items': halt,
                'rule': 'never retried automatically; root resolves with: resolve --wave W (--token T ... | --all '
                        '--halt-sha256 <sha256 of this file>) --decision invalid | retry | retry_with_recovery '
                        '--recovery <allowlisted rule path> --reason TEXT; each token is single-use and only valid while '
                        'this wave is the key\'s latest launch; invalid is refused for never_resolve_invalid items'},
                halt_core)
        write_json_idempotent(wave_dir / 'WAVE_RESULT.json', result, wave_result_core)
        return result

    def run_wave(self, wave_dir, plan, resume):
        t0 = time.monotonic()
        records, meta = self.executor.execute(wave_dir, plan, resume, self.log)
        if records is None:
            return None, meta
        bad = self.check_identity_now()                                     # v005 SF1: before every ingest
        if bad:
            self._log('refused before ingest of %s: %s' % (wave_dir.name, bad))
            raise OrchestratorError('refused before ingest of %s: %s' % (wave_dir.name, '; '.join(bad)[:1500]))
        res = self.ingest(wave_dir, plan, records, meta)
        res['wall_s'] = time.monotonic() - t0
        return res, meta

    @staticmethod
    def halt_status(res, wd):
        classes = set(h['class'] for h in res['halt'])
        status = 'HALTED_INFRA' if 'INFRA' in classes else 'HALTED_NUMERICS'
        return {'status': status, 'wave': wd.name, 'halt': res['halt']}

    def _commit_plan(self, wd, plan):
        """F3 order: ledger intent lines first (they count only once the plan is committed), then the atomic commit."""
        for c in plan['calls']:
            append_jsonl(self.ledger_path, {'wave': plan['wave'], 'call_index': c['call_index'], 'key': c['key'],
                                            'spec_sha256': c['spec_sha256'], 'authorized_by': c.get('authorized_by'),
                                            'cache_id': plan['cache_id'], 'config_sha256': plan['config_sha256'],
                                            'gate_digest': plan['gate_digest'],                  # v005 C4-2 / B2-2
                                            'utc': utc()})
        write_json_atomic_x(wd / 'WAVE_PLAN.json', plan)

    def check_resume_plan(self, wd, plan):
        """C4-2 (v005): an interrupted wave runs only the specs this config builds: every planned spec must equal
        mapper.build(theta[, its recovery rule]) by sha256 AND its own bytes, keep its key, and pass prelaunch_check; the
        plan's cache id must be this cache id.  Returns the number of calls still without a receipt (disk guard)."""
        ctx = self.ctx
        if plan.get('cache_id') != ctx.cache_id:
            raise OrchestratorError('C4-2 config changed: use a new work dir (interrupted wave %s was planned under cache id '
                                    '%s, this config gives %s)' % (wd.name, str(plan.get('cache_id'))[:16], ctx.cache_id[:16]))
        bad = []
        for c in plan.get('calls') or []:
            rec = c.get('recovery')
            rr = None
            if rec:
                rr = ctx.recovery_rule(rec.get('path'))
                if rr['sha256'] != rec.get('sha256'):
                    bad.append('%s: recovery rule bytes changed' % str(c.get('key'))[:16])
                    continue
            b = ctx.mapper.build(c['theta'], recovery=rr)
            if b['key'] != c.get('key') or b['sha256'] != c.get('spec_sha256') or \
                    sha256_bytes(json_bytes(c.get('spec'))) != c.get('spec_sha256'):
                bad.append('%s: planned spec %s is not the spec this config builds (%s)'
                           % (str(c.get('key'))[:16], str(c.get('spec_sha256'))[:16], b['sha256'][:16]))
                continue
            ctx.prelaunch_check(c['spec'], recovery=rr is not None)
        if bad:
            raise OrchestratorError('C4-2 config changed: use a new work dir (interrupted wave %s: %s)' % (wd.name, bad[:4]))
        cdir = wd / 'campaign'
        return sum(1 for i in range(len(plan.get('calls') or []))
                   if not (cdir / ('call_%04d' % i) / 'RECEIPT.json').exists())

    # ---------------------------------------------------------------- main loop
    def run(self, max_waves=None, new_campaign=False):
        ctx = self.ctx
        if not ctx.gates_ok():
            return {'status': 'REFUSED', 'reasons': ['GATES_NOT_PASSED'], 'gates': ctx.gate_report()}
        sess = session_record()                                             # v005 C4-4
        if not ctx.synthetic and not sess['session_leader']:
            return {'status': 'REFUSED', 'session': sess,
                    'reasons': ['C4-4 NOT_A_SESSION_LEADER: launch the orchestrator through launch_setsid_c2v005.py (its '
                                'own session and process group) and stop it by PID only']}
        initialized = (ctx.work_dir / 'WORK_DIR.json').is_file()           # v005 SF2
        if new_campaign and initialized:
            return {'status': 'REFUSED', 'reasons': ['SF2 NEW_CAMPAIGN_ON_INITIALIZED_WORK_DIR: %s already holds a '
                                                     'campaign (WORK_DIR.json); resume without --new-campaign'
                                                     % ctx.work_dir]}
        if not new_campaign and not initialized:
            return {'status': 'REFUSED', 'reasons': ['SF2 WORK_DIR_NOT_INITIALIZED: %s has no WORK_DIR.json (an absent, '
                                                     'moved or emptied work dir is never restarted silently); start a '
                                                     'fresh campaign with --new-campaign' % ctx.work_dir]}
        if new_campaign:
            ctx.work_dir.mkdir(parents=True, exist_ok=True)
        lock = Lock(ctx.work_dir)
        if not lock.acquire():
            return {'status': 'LOCKED'}
        try:
            self.prepare(create=True, init_work_dir=new_campaign)
            self.log('orchestrator start', cache_id=ctx.cache_id, alias=self.alias, stale_lock=lock.stale,
                     work_dir=ctx.work_dir_record, session=sess, config_sha256=ctx.config_sha256,
                     gate_digest=ctx.gate_digest, new_campaign=bool(new_campaign))
            final = ctx.work_dir / 'FINAL_SUMMARY.json'
            if final.exists():
                return dict(load_json_file(final, 'FINAL_SUMMARY.json'), status='COMPLETE', note='already complete')
            for wd in self.wave_dirs():
                if (wd / 'WAVE_PLAN.json').is_file() and not (wd / 'WAVE_RESULT.json').exists():
                    plan = load_json_file(wd / 'WAVE_PLAN.json', 'wave plan')
                    pr = self.probe.run(self.cache, 'probe', exclude=[c['key'] for c in plan['calls']])
                    if [m['key'] for m in self._dedup(pr['misses'])] != [c['key'] for c in plan['calls']]:
                        raise OrchestratorError('interrupted wave %s: the probe no longer predicts its calls '
                                                '(determinism failure)' % wd.name)
                    remaining = self.check_resume_plan(wd, plan)            # v005 C4-2: specs of THIS config only
                    self.pre_wave_checks('resume of %s' % wd.name)          # v005 SF1 / SF4 / B2-2 / C4-2
                    ok, disk = self.disk_ok(remaining)                      # v005 C4-2 (N6): the disk guard on resume
                    if not ok:
                        self.log('halt: disk guard (resume)', disk=disk)
                        return {'status': 'HALTED_DISK', 'disk': disk, 'wave': wd.name}
                    self.log('resuming interrupted wave %s (%d calls)' % (wd.name, plan['n_calls']))
                    res, meta = self.run_wave(wd, plan, resume=True)
                    if res is None:
                        return {'status': 'ORPHANS_STILL_RUNNING', 'wave': wd.name, 'meta': meta}
                    if res['halt']:
                        return self.halt_status(res, wd)
            waves_run = 0
            while True:
                pr = self.probe.run(self.cache, 'probe')
                if pr['complete']:
                    break
                misses = self._dedup(pr['misses'])
                if not misses:
                    raise OrchestratorError('probe stopped (%s) without a miss' % pr['stop_reason'])
                launched, auth = self.launches(), self.pending_authorizations()
                again = [m['key'] for m in misses if launched.get(m['key'], 0) >= 1 and m['key'] not in auth]
                if again:
                    self.log('halt: %d requested theta were launched before and have no unused retry token' % len(again))
                    return {'status': 'HALTED_UNRESOLVED', 'keys': again,
                            'rule': 'an earlier launch of these theta halted; each relaunch needs one unused retry token of '
                                    'its latest halt (resolve --token)'}
                if max_waves is not None and waves_run >= max_waves:
                    return {'status': 'MAX_WAVES', 'next_wave_calls': len(misses)}
                ok, disk = self.disk_ok(len(misses))
                if not ok:
                    self.log('halt: disk guard', disk=disk)
                    return {'status': 'HALTED_DISK', 'disk': disk}
                wave_no = len(self.wave_dirs()) + 1
                wd = self.waves_dir / ('wave_%04d' % wave_no)
                plan = self.make_plan(wave_no, misses)
                plan['probe'] = {k: pr[k] for k in ('stop_reason', 'calls', 'hits', 'placeholders', 'families')}
                plan['disk'] = disk
                self.pre_wave_checks('wave %d' % wave_no)                    # v005 SF1 / SF4 / B2-2 / C4-2
                wd.mkdir(parents=True, exist_ok=False)
                self._commit_plan(wd, plan)
                self.log('wave %d: %d calls, families %s, batches %d' % (wave_no, plan['n_calls'], plan['families'],
                                                                         plan['batches']))
                res, meta = self.run_wave(wd, plan, resume=False)
                waves_run += 1
                if res is None:
                    return {'status': 'ORPHANS_STILL_RUNNING', 'wave': wd.name, 'meta': meta}
                self.log('wave %d ingested: %s' % (wave_no, res['counts']))
                if res['halt']:
                    return self.halt_status(res, wd)
            return self.finalise()
        finally:
            lock.release()

    @staticmethod
    def _dedup(misses):
        out, seen = [], set()
        for m in misses:
            if m['key'] not in seen:
                seen.add(m['key'])
                out.append(m)
        return out

    # ---------------------------------------------------------------- replay, record (F3), summary
    def _existing_record(self, rec_path, reg_path):
        vr = self.ctx.E.verify_calibration_record(record_path=str(rec_path), registry_path=str(reg_path))
        if not vr['ok']:
            return None, vr
        doc = load_json_file(rec_path, 'calibration record')
        fsha = sha256_file(rec_path)
        line = None
        for ln in read_jsonl(reg_path):
            if ln.get('record_file_sha256') == fsha:
                line = ln
        w = {'ok': True, 'record_path': str(rec_path), 'record_file_sha256': fsha, 'record_sha256': doc.get('record_sha256'),
             'registry_path': str(reg_path), 'registry_line_sha256': (line or {}).get('line_sha256'),
             'exploration_fingerprint': doc.get('exploration_fingerprint'), 'reused_existing_record': True}
        return w, vr

    def finalise(self):
        ctx = self.ctx
        r1 = self.probe.run(self.cache, 'replay')
        r2 = self.probe.run(self.cache, 'replay')
        replay = {'calls': r1['calls'], 'hits': r1['hits'], 'uncached_calls': len(r1['misses']),
                  'complete': r1['complete'] and r2['complete'], 'stop_reason': r1['stop_reason']}
        if not (r1['complete'] and r2['complete']) or r1['misses'] or r2['misses'] or r1['calls'] != r1['hits']:
            self.log('REPLAY FAILED', replay=replay)
            return {'status': 'REPLAY_FAILED', 'replay': replay}
        b1, b2 = ctx.E._canonical_bytes(r1['run']), ctx.E._canonical_bytes(r2['run'])
        replay['deterministic'] = b1 == b2
        replay['run_canonical_sha256'] = sha256_bytes(b1)
        if not replay['deterministic']:
            return {'status': 'REPLAY_FAILED', 'replay': replay}
        run = r1['run']
        rec_dir = ctx.work_dir / 'records'
        rec_dir.mkdir(exist_ok=True)
        rec_path = rec_dir / ('CALIBRATION_RECORD_%s_%s.json' % (run['status'], replay['run_canonical_sha256'][:16]))
        reg_path = rec_dir / 'CALIBRATION_REGISTRY.jsonl'
        if rec_path.exists():
            w, vr = self._existing_record(rec_path, reg_path)
            if w is None:
                self.log('existing calibration record does not verify', reasons=vr.get('reasons'))
                return {'status': 'RECORD_UNVERIFIED', 'record_path': str(rec_path), 'verify': vr}
        else:
            w = ctx.E.write_calibration_record(run=run, record_path=str(rec_path), registry_path=str(reg_path))
            if not w['ok']:
                raise OrchestratorError('write_calibration_record: %s' % w['reasons'])
            vr = ctx.E.verify_calibration_record(record_path=str(rec_path), registry_path=str(reg_path))
        summary = self.summary(run, replay, w, vr)
        self._write_final(summary)
        self.log('orchestration complete: engine status %s, record %s' % (run['status'], w['record_file_sha256']))
        return dict(summary, status='COMPLETE')

    def _write_final(self, summary):
        summary['summary_file_sha256'] = write_json_atomic_x(self.ctx.work_dir / 'FINAL_SUMMARY.json', summary)

    @staticmethod
    def d5_assessment(run_status, used_entries):
        """C4: an engine NO_ADMITTED_POINT_FOUND run is eligible to count toward D5 TESTED-NEGATIVE only with zero
        judgment-call MODEL_INVALID entries and zero root-declared invalid entries among its evaluations."""
        if run_status != 'NO_ADMITTED_POINT_FOUND':
            return None
        jc = sorted(e['key'] for e in used_entries if e.get('classification') == 'MODEL_INVALID'
                    and ((e.get('provenance') or {}).get('taxonomy') or {}).get('judgment_call') is True)
        root = sorted(e['key'] for e in used_entries if e.get('source') == 'ROOT_RESOLUTION')
        cond = not jc and not root
        return {'this_run_meets_tested_negative_condition': cond,
                'n_judgment_call_model_invalid': len(jc), 'judgment_call_model_invalid_keys': [k[:16] for k in jc],
                'n_root_declared_invalid': len(root), 'root_declared_invalid_keys': [k[:16] for k in root],
                'status': ('UNTESTED: this run meets the D5 condition; TESTED-NEGATIVE needs the second declared D5 run to '
                           'meet it as well, and root confirms') if cond else
                          ('UNTESTED: this run does NOT meet the D5 condition (%d judgment-call MODEL_INVALID, %d root-'
                           'declared invalid); a numerics budget is not a claim that the region is empty' % (len(jc), len(root)))}

    def summary(self, run, replay, w, vr):
        ctx = self.ctx
        used = []
        for e in run.get('evaluation_log') or []:
            if isinstance(e.get('theta_natural'), dict):
                used.append(theta_key(e['theta_natural']))
        used_set = set(used)
        launched = self.launches()
        waste = sorted(k for k in launched if k not in used_set and k in self.cache.entries)
        waves = []
        for wd in self.wave_dirs():
            pp = wd / 'WAVE_PLAN.json'
            if not pp.is_file():
                waves.append({'wave_dir': wd.name, 'planless': True})
                continue
            p = load_json_file(pp, 'wave plan')
            r = load_json_file(wd / 'WAVE_RESULT.json', 'wave result') if (wd / 'WAVE_RESULT.json').exists() else {}
            waves.append({'wave': p['wave'], 'n_calls': p['n_calls'], 'batches': p['batches'], 'families': p['families'],
                          'counts': r.get('counts'), 'wall_s': r.get('wall_s'),
                          'max_accounted_processes': (r.get('campaign') or {}).get('max_accounted_processes')})
        real_waves = [x for x in waves if not x.get('planless')]
        ex = run.get('exploration') or {}
        side_recs = []
        for k, sides in (ex.get('boundary_detail') or {}).items():
            for sd, rec in (sides or {}).items():
                if rec:
                    side_recs.append(('round0', rec))
        for rr in ex.get('march_rounds') or []:
            for ray in rr.get('lp_rays') or []:
                if ray.get('side_record'):
                    side_recs.append(('round%d_lp' % rr['round'], ray['side_record']))
            for an in rr.get('anchors') or []:
                for rec in an.get('sides') or []:
                    side_recs.append(('round%d_axis' % rr['round'], rec))
        validity_limited = [{'where': wh, 'anchor_log_index': r.get('anchor_log_index'), 'direction': r.get('direction'),
                             'side': r.get('side'), 'kind': r.get('kind'), 'boundary_cause': r.get('boundary_cause')}
                            for wh, r in side_recs if str(r.get('boundary_cause', '')).startswith('INVALID_EVALUATION')]
        edge_limited = []
        names = list(ctx.es['varying_names'])
        for pt in ex.get('admitted_points') or []:
            for j, x in enumerate(pt['u']):
                if x <= 1e-9:
                    edge_limited.append((names[j], 'lower'))
                elif x >= 1.0 - 1e-9:
                    edge_limited.append((names[j], 'upper'))
        edge_limited = sorted(set(edge_limited))
        inv, judg, recov, used_entries = {}, [], [], []
        for k in used_set:
            e = self.cache.entries.get(k)
            if not e:
                continue
            used_entries.append(e)
            tx = (e.get('provenance') or {}).get('taxonomy') or {}
            if e['classification'] == 'MODEL_INVALID':
                inv[e.get('failure_class')] = inv.get(e.get('failure_class'), 0) + 1
            if tx.get('judgment_call'):
                judg.append({'key': k, 'rule': tx.get('rule'), 'code': tx.get('code'), 'class': tx.get('class')})
            if (e.get('provenance') or {}).get('recovery'):
                recov.append({'key': k, 'recovery': e['provenance']['recovery']})
        jac = run.get('jacobian') or {}
        ng = ctx.gates.get('numerics_verdict') or {}
        return {
            'schema': SCHEMA_SUMMARY, 'module': MODULE_NAME, 'utc': utc(), 'synthetic_test': ctx.synthetic,
            'config_sha256': ctx.config_sha256, 'cache_id': ctx.cache_id, 'base_spec_sha256': ctx.base_sha256,
            'work_dir': ctx.work_dir_record,
            'pins': {'coordinate_spec': ctx.cfg['coordinate_spec'], 'coordinate_spec_addendum': ctx.cfg.get('coordinate_spec_addendum'),
                     'observation_region': ctx.region_pin, 'engine': ctx.spec['engine'], 'freeze': ctx.spec['freeze'],
                     'driver': ctx.driver, 'taxonomy': ctx.cfg['taxonomy'], 'monitor': ctx.cfg.get('monitor'),
                     'campaign': ctx.cfg.get('campaign'), 'template': ctx.spec['call_spec_mapping']['template'],
                     'capability_evidence': ctx.cfg.get('capability_evidence'),
                     'orchestrator': {'path': os.path.realpath(__file__), 'sha256': sha256_file(os.path.realpath(__file__))}},
            'coordinate_mode': ctx.coordinate_mode, 'varying_names': list(ctx.es['varying_names']),
            'engine_coordinates_sha256': ctx.engine_coordinates_sha256, 'work_dir_identity': ctx.work_dir_identity,
            'gates': ctx.gate_report(), 'numerics': ctx.numerics, 'numerics_is_template': ctx.numerics_is_template,
            'numerics_binding': ng.get('binding'), 'numerics_root_attestation': ng.get('root_attestation'),
            'numerics_execution_overrides': ng.get('execution_overrides'),
            'numerics_adopted_case': ng.get('adopted'), 'u_i_km_s_from_verdict': ng.get('u_i_km_s'),       # v005 C4-5/6
            'u_i_carrier': (ctx.gates.get('u_i_carrier') or {}).get('declaration'),
            'seed_spec_sha256': ctx.seed_spec_sha256, 'gate_digest': ctx.gate_digest, 'runtime': ctx.runtime,
            'route_a_contraction_test': ctx.taxonomy.contraction_test,
            'column_workers': ctx.column_workers, 'call_weights': ctx.weights, 'max_concurrent': ctx.max_concurrent,
            'process_budget': ctx.process_budget, 'stage_aware_budget': ctx.stage_aware,
            'column_workers_invariance': COLUMN_WORKERS_INVARIANCE, 'anchor_alias': self.alias,
            'engine_parameters': ctx.params, 'ngc_slots_placeholder': ctx.ngc_slots_placeholder,
            'engine_status': run['status'], 'engine_ok': run['ok'], 'stage_reached': run.get('stage_reached'),
            'n_admitted': (ex.get('n_admitted') if ex else None), 'region_possibly_truncated': run.get('region_possibly_truncated'),
            'truncation_causes': run.get('truncation_causes'), 'exploration_fingerprint': run.get('exploration_fingerprint'),
            'refinement_status': ex.get('refinement_status') if ex else None,
            'jacobian_steps_detail': jac.get('steps_detail'),
            'evaluations_in_run': len(used), 'distinct_theta_in_run': len(used_set),
            'model_invalid_evaluations_in_run_by_code': inv,
            'judgment_call_classifications_in_run': judg,
            'evaluations_under_recovery_rules': recov,
            'D5_assessment': self.d5_assessment(run['status'], used_entries),
            'replay': replay,
            'record': {'record_path': w['record_path'], 'record_file_sha256': w['record_file_sha256'],
                       'record_sha256': w['record_sha256'], 'registry_path': w['registry_path'],
                       'registry_line_sha256': w['registry_line_sha256'], 'exploration_fingerprint': w['exploration_fingerprint'],
                       'reused_existing_record': bool(w.get('reused_existing_record')),
                       'verify_ok': vr['ok'], 'registry_chain_ok': vr['registry_chain_ok'], 'verify_reasons': vr['reasons']},
            'waves': waves, 'n_waves': len(real_waves), 'n_batches': sum(x['batches'] for x in real_waves),
            'n_planless_wave_dirs': len(waves) - len(real_waves),
            'n_launched': sum(launched.values()), 'n_launched_distinct': len(launched),
            'unused_launched_theta': waste, 'n_unused_launched_theta': len(waste),
            'validity_limited_sides_D6': validity_limited, 'edge_limited_D7': [list(x) for x in edge_limited],
            'open_items_from_addendum': (ctx.addendum or {}).get('items'),
            'no_admitted_point_rule_D5': ((ctx.addendum or {}).get('items') or {}).get('D5')
            if run['status'] == 'NO_ADMITTED_POINT_FOUND' else None,
            'freeze_gate': (('ROOT_CALL_ORDER step 2 may start (record pinned at step 5)' if ctx.coordinate_mode['mode'] ==
                             MODE_D_NUISANCE else 'ROOT_CALL_ORDER step 2 needs a freeze coordinate list that represents '
                             'the A13 fixed DDO154 distance (addendum item FREEZE_COORDINATE_COMPATIBILITY: '
                             'prediction_freeze_c2v003a requires role nuisance for a ddo154_nuisance distance); record '
                             'pinned at step 5') if run['status'] == 'COMPLETE'
                            else 'NO FREEZE: engine status %s is a result to register, not to retry silently' % run['status']),
        }

    # ---------------------------------------------------------------- resolve / plan / status
    def resolve(self, wave, decision, reason, tokens=None, all_items=False, halt_sha256=None, recovery_path=None):
        """M2/L5/C11: validated completely before anything is written; one atomic RESOLUTIONS line per item."""
        ctx = self.ctx
        if decision not in DECISIONS:
            raise OrchestratorError('decision must be one of %s' % (DECISIONS,))
        if not isinstance(reason, str) or not reason.strip():
            raise OrchestratorError('resolve needs a non-empty --reason')
        rr = None
        if decision == 'retry_with_recovery':
            if not recovery_path:
                raise OrchestratorError('retry_with_recovery needs --recovery PATH (an allowlisted rule)')
            rr = ctx.recovery_rule(recovery_path)
        elif recovery_path:
            raise OrchestratorError('--recovery is only valid with retry_with_recovery')
        if not ctx.work_dir.is_dir():
            raise OrchestratorError('work dir %s does not exist' % ctx.work_dir)
        lock = Lock(ctx.work_dir)
        if not lock.acquire():
            return {'status': 'LOCKED', 'reason': 'an orchestrator run holds the lock (L5)'}
        try:
            self.work_dir_json = self.check_work_dir_json(False)                  # F3
            self.check_plan_cache_ids()                                          # v005 C4-2
            wd = self.waves_dir / ('wave_%04d' % int(wave))
            hp = wd / 'HALT.json'
            if not hp.is_file():
                raise OrchestratorError('wave %s has no HALT.json' % wave)
            halt = load_json_file(hp, 'HALT.json')
            plan = load_json_file(wd / 'WAVE_PLAN.json', 'WAVE_PLAN.json')
            if plan.get('cache_id') != ctx.cache_id:                             # v005 C4-2
                raise OrchestratorError('C4-2 config changed: use a new work dir (wave %s was planned under cache id %s, '
                                        'this config gives %s)' % (wave, str(plan.get('cache_id'))[:16], ctx.cache_id[:16]))
            by_key = {c['key']: c for c in plan['calls']}
            if all_items:
                if tokens:
                    raise OrchestratorError('use either --token or --all --halt-sha256')
                if halt_sha256 != sha256_file(hp):
                    raise OrchestratorError('--all needs --halt-sha256 equal to the sha256 of %s' % hp)
                items = list(halt['items'])
            else:
                if not tokens:
                    raise OrchestratorError('resolve needs --token T (repeatable) or --all --halt-sha256 H')
                by_tok = {it['token']: it for it in halt['items']}
                miss = [t for t in tokens if t not in by_tok]
                if miss:
                    raise OrchestratorError('token(s) not in the HALT of wave %s: %s' % (wave, [t[:16] for t in miss]))
                if len(set(tokens)) != len(tokens):
                    raise OrchestratorError('duplicate --token')
                items = [by_tok[t] for t in tokens]
            self.cache.open(create=True)
            self.materialize_invalid_resolutions()
            used = set(ln.get('token') for ln in self.cache.resolutions())
            last = self.last_launch_wave()
            problems = []
            for it in items:
                if it['token'] in used:
                    problems.append('%s: TOKEN_ALREADY_USED' % it['key'][:16])
                if last.get(it['key']) != int(wave):
                    problems.append('%s: STALE_TOKEN (the key\'s latest launch is wave %s)' % (it['key'][:16], last.get(it['key'])))
                if it['key'] in self.cache.entries:
                    problems.append('%s: ALREADY_CACHED' % it['key'][:16])
                if decision == 'invalid' and ctx.taxonomy.never_invalid_code(it.get('reason')):
                    problems.append('%s: INVALID_REFUSED_FOR_%s (C11)' % (it['key'][:16], str(it.get('reason')).split(':')[0]))
            if problems:
                raise OrchestratorError('resolve refused, nothing written: %s' % problems)
            if decision != 'invalid':
                for it in items:
                    cd = (it.get('provenance') or {}).get('call_dir')
                    if cd:
                        procs = live_processes(CampaignExecutor.call_markers(cd))
                        if procs is None or procs:
                            raise OrchestratorError('F4: live process(es) still reference %s: %s; wait or stop them first'
                                                    % (cd, procs))
            done = []
            for it in items:
                line = {'schema': SCHEMA_RESOLUTION, 'utc': utc(), 'wave': int(wave), 'key': it['key'],
                        'token': it['token'], 'decision': decision, 'reason': reason, 'halt_class': it['class'],
                        'halt_reason': it['reason'], 'cache_id': ctx.cache_id,           # v005 C4-2
                        'config_sha256': ctx.config_sha256}
                if rr is not None:
                    line['recovery'] = {'path': rr['path'], 'sha256': rr['sha256'], 'rule_id': rr['rule_id']}
                append_jsonl(self.resolution_path, line)
                self.cache._resolutions = None
                if decision == 'invalid':
                    ent = resolution_entry(it, line, by_key[it['key']]['theta'])
                    self.cache.put(key=it['key'], **ent)
                done.append(line)
            return {'status': 'OK', 'resolved': done}
        finally:
            lock.release()

    def plan_only(self):
        self.prepare(create=False)
        pr = self.probe.run(self.cache, 'probe')
        base = {'gates': self.ctx.gate_report(), 'gates_ok': self.ctx.gates_ok(), 'alias': self.alias,
                'cache_id': self.ctx.cache_id, 'base_spec_sha256': self.ctx.base_sha256,
                'n_cached': len(self.cache.entries), 'column_workers': self.ctx.column_workers,
                'call_weights': self.ctx.weights, 'max_concurrent': self.ctx.max_concurrent,
                'process_budget': self.ctx.process_budget, 'stage_aware_budget': self.ctx.stage_aware,
                'work_dir': self.ctx.work_dir_record, 'work_dir_json': self.work_dir_json,
                'work_dir_identity': self.ctx.work_dir_identity, 'coordinate_mode': self.ctx.coordinate_mode,
                'varying_names': list(self.ctx.es['varying_names']),
                'open_items_from_addendum': sorted(((self.ctx.addendum or {}).get('items') or {}).keys()),
                # v005: what an adoption derivation (C4-6) must name, and what every wave plan records
                'seed_spec_sha256': self.ctx.seed_spec_sha256, 'config_sha256': self.ctx.config_sha256,
                'gate_digest': self.ctx.gate_digest, 'runtime': self.ctx.runtime, 'session': session_record(),
                'counted_assumptions_from_addendum': sorted(((self.ctx.addendum or {}).get('counted_assumptions')
                                                             or {}).keys())}
        if pr['complete']:
            return dict(base, status='OK', next_wave=None, note='probe complete: the next run step is the replay',
                        disk=self.ctx.disk_forecast(0))
        misses = self._dedup(pr['misses'])
        plan = self.make_plan(len(self.wave_dirs()) + 1, misses)
        return dict(base, status='OK',
                    probe={k: pr[k] for k in ('stop_reason', 'calls', 'hits', 'placeholders', 'families')},
                    next_wave={'n_calls': plan['n_calls'], 'batches': plan['batches'], 'families': plan['families'],
                               'calls': [{'key': c['key'][:16], 'family': c['family'], 'branch': c['branch'],
                                          'purpose': c['purpose'], 'u': c['u'], 'sibling': c['sibling'],
                                          'spec_sha256': c['spec_sha256'], 'recovery': c['recovery'],
                                          'authorized_by': c['authorized_by'],
                                          'physical': {k: c['spec']['physical'][k] for k in
                                                       ('common_scale_s', 'gamma', 'ell_F_m', 'distance_Mpc')}}
                                         for c in plan['calls']]},
                    disk=self.ctx.disk_forecast(plan['n_calls']))

    def status(self):
        ctx = self.ctx
        self.work_dir_json = self.check_work_dir_json(False)                      # F3
        self.cache.open(create=False)
        used = set(ln.get('token') for ln in self.cache.resolutions())
        halts = []
        for wd in self.wave_dirs():
            h = wd / 'HALT.json'
            if h.is_file():
                d = load_json_file(h, 'HALT.json')
                halts.append({'wave': wd.name, 'halt_file_sha256': sha256_file(h),
                              'classes': sorted(set(i['class'] for i in d['items'])), 'n_items': len(d['items']),
                              'items': [{'key': i['key'][:16], 'class': i['class'], 'reason': i['reason'],
                                         'token': i['token'], 'token_used': i['token'] in used,
                                         'never_resolve_invalid': i.get('never_resolve_invalid')} for i in d['items']]})
        self.ledger()
        wdj = ctx.work_dir / 'WORK_DIR.json'
        return {'status': 'OK', 'cache_id': ctx.cache_id, 'n_cached': len(self.cache.entries),
                'plan_cache_id_mismatches_C4_2': self.plan_cache_id_mismatches(),          # v005: reported, not refused
                'runtime_check_SF4': self.check_runtime() if wdj.is_file() else 'NO_WORK_DIR_JSON',
                'config_sha256': ctx.config_sha256, 'gate_digest': ctx.gate_digest,
                'waves': [p.name for p in self.wave_dirs()], 'final': (ctx.work_dir / 'FINAL_SUMMARY.json').exists(),
                'halts': halts, 'gates_ok': ctx.gates_ok(), 'gates': ctx.gate_report(),
                'torn_jsonl_lines_skipped': {k: v for k, v in _JSONL_TORN.items() if v},
                'work_dir': ctx.work_dir_record, 'work_dir_json': self.work_dir_json,
                'work_dir_identity': ctx.work_dir_identity, 'coordinate_mode': ctx.coordinate_mode,
                'disk': ctx.disk_forecast(None)}


# --------------------------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('command', choices=('plan', 'run', 'resolve', 'status'))
    ap.add_argument('--config', required=True)
    ap.add_argument('--max-waves', type=int, default=None)
    ap.add_argument('--wave', type=int)
    ap.add_argument('--token', action='append', default=[])
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--halt-sha256')
    ap.add_argument('--decision', choices=DECISIONS)
    ap.add_argument('--recovery')
    ap.add_argument('--reason')
    ap.add_argument('--new-campaign', action='store_true',
                    help='run only: start a fresh campaign in a work dir without WORK_DIR.json (v005 SF2)')
    a = ap.parse_args(argv)
    try:
        if a.new_campaign and a.command != 'run':
            raise OrchestratorError('--new-campaign is valid only with run')
        ctx = Context(a.config)
        orch = Orchestrator(ctx)
        if a.command == 'plan':
            out = orch.plan_only()
        elif a.command == 'run':
            out = orch.run(max_waves=a.max_waves, new_campaign=a.new_campaign)
        elif a.command == 'resolve':
            if a.wave is None or a.decision is None or not a.reason:
                raise OrchestratorError('resolve needs --wave, --decision, --reason and --token ... or --all --halt-sha256')
            out = orch.resolve(a.wave, a.decision, a.reason, tokens=a.token, all_items=a.all, halt_sha256=a.halt_sha256,
                               recovery_path=a.recovery)
        else:
            out = orch.status()
    except OrchestratorError as exc:
        out = {'status': 'REFUSED', 'reasons': [str(exc)]}
    print(json.dumps({k: v for k, v in out.items() if k not in ('waves',)} if a.command == 'run' else out,
                     indent=1, sort_keys=True, default=str))
    return EXIT.get(out.get('status'), 3)


if __name__ == '__main__':
    sys.exit(main())
