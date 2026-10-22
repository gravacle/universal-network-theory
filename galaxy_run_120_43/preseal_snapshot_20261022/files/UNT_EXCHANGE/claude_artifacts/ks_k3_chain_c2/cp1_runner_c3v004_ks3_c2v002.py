"""KS3' runner (ks_k3_chain_c2 G-wave c2v002; root A175, A176): KS3 runner c2v001 (54595c2d) whose row 32 takes the
G3 GQ producer and the G4 EPS adapter.

It loads the KS3' common. Rows 1-31: unchanged (2832ceb9 GQ, 4de70486 adapt-eps, every check and record c2v001's and so
c3v004's; only the runner/common self-pins name this build). Row 32 (S1_UA_C3T) only: the GQ producer is the G3
successor (kept K 3 node grid; custody KS1), and check_gq wants its pin; POINT_START names it; the EPS review request
and adapt-eps bind the G4 adapter (KS2 producer, 179 shells from 3), whose proof check wants the G4 pin; the plan names
the G-wave producers. Edits: this docstring head, the common pin (2) and S1 approved-producer constant, real_loader_s1,
check_gq's signature and want, three lines of run_point, real_adapter_s1, adapt_point's loader/review/approval/check
lines, and the row-32 plan entry. The text of c2v001 follows.

KS3 runner (ks_k3_chain_c2 c2v001; root A160): cp1_runner_c3v004 (3f5e5c18) plus row 32, S1_UA_C3T.

It loads the KS3 common (rows 1-31 and every c3v004 pin unchanged; row 32 from the root-written row file). For rows
1-31 every stage, check, gate and record is c3v004's; only the runner/common self-pins in the records name this build.
Row 32 (S1_UA_C3T) only: the response producer is KS2 (custody KS1); check_eps wants the 179 unit shells [3,4]..[181,182]
and the KS2 producer pin; check_rho wants coverage [3, 182], the 10-shell partition from [3,4] and the KS2 pin; the F6
source-pin match compares the anchor's pins with row 32's after its custody/producer pins (KS1/KS2, checked) are mapped
to 6810b7c3/a1dcdea8 (C.s1_pins_as_table). GQ is the canonical gq_producer 2832ceb9: its kernel gq_geometry (c6ffb338)
derives custody with 6810b7c3 and takes the K=4 kept region (L39), so row 32 stops at GQ until a K=3 GQ successor exists
(open item for root). adapt-eps is c3v004's (EPS adapter 4de70486, K=4 only: open item for root). The c3v004 text follows.

S4-R-C1 CP-1 runner c3v004, GQ, EPS and RHO (Claude3 lane; root A122, A134, A138; reviewer Codex1 under A115).

Root operates CP-1 in window (b); the builder ran this tool on SYNTHETIC inputs only.

Per point (table order: anchor 8ad6ca4e first, HEADLINE_CORNER_000 second):
  1. load the pinned dry-plan spec, check its sha256 from bytes and its point key with the
     core point_identity recipe (a595c5c0 L233-238) against brief section 3;
  2. compute the point context once (point_response_producer_cx2v002.point_context);
  3. run GQ (gq_producer_cx2v005 2832ceb9, all production nodes), then EPS
     (point_response_producer_cx2v002 a1dcdea8, settings 'registered', full domain,
     shells sequential inside one process: adapter L66-70 / brief R5);
  4. write every record by exclusive create in THIS runner's own output root (never in
     Codex2's certificates_per_point folder), with seconds, CPU seconds and peak RSS per stage.
Producers are imported by their canonical absolute paths, so the proof producer pins equal
what the wrapper compares as whole dicts (brief R4). No smoke or partial setting exists.
Every compute process must run under `taskpolicy -b` and `python3 -I -B` (checked in-process).
Single-thread BLAS is enforced by override at import: the six thread variables are set to 1 before numpy
can load, and their parent values are recorded (F4). Points start only through the memory gate
(`/usr/bin/memory_pressure` free % >= 25 % + margin; never ps sums) AND the stricter-only physical-headroom
floor (`/usr/bin/vm_stat`, F1). A non-anchor point holds after its CONTEXT stage until the anchor's context
record exists (F6). The scheduler never pauses a running worker: SIGSTOP stays root's manual step.
adapt-eps (adapter v003 4de70486) runs only after a distinct-lane EPS review exists.

c3v003 (FROM_CODEX/0696, 0697; A134 Q5 and (a)4) adds ONE stage, RHO, after EPS, and keeps every c3v002 rule:
  5. RHO: point_response_producer_cx2v002 (a1dcdea8) produce_rho with settings 'registered', the full registered search
     and the full point domain: coverage [4, 182] and the 9-shell K_big 128 partition (a1dcdea8 shell_plan L112-121),
     in this worker process with the EPS context (attempt a). At the anchor key 8ad6ca4e the worker then runs attempt b
     in a SEPARATE process (`rho-repeat`, a fresh interpreter and a fresh point context), so that (a)4 has two separate
     rho runs to compare. The bitwise decision is the slot proof's (proof side c3v003 since c3v004: wrapper v002's
     10-key canonical comparison, A138 V03); the runner writes a diagnostic.
     The stage runs only with --allow-rho plus the sha of Codex1's proof-side review record, matched against the
     root-provided pin of that record (bytes read and hashed). Otherwise the stage record reads
     HELD_PENDING_PROOF_SIDE_REVIEW and nothing is computed.
c3v004 (root ruling A138, FROM_CODEX/0703): erratum-class. It loads common c3v004, whose PINS carry V02 (the b1
  enumerator), V09 (the published wrapper path) and the canonical slot producer c3v003. V03: the anchor pair record
  (a diagnostic) names the decisive (a)4 comparison, wrapper v002's 10 keys. No stage, check, gate or format changes.

Commands: plan | run | worker (internal) | rho-repeat (internal; anchor attempt b) | adapt-eps | compare-anchor.
Exit codes: 0 ok, 2 setup refusal, 3 stopped or blocked.
"""
import os
# F4: single-thread BLAS is ENFORCED BY OVERRIDE AT IMPORT, before numpy can load. The parent values are
# kept in PARENT_THREAD_ENV and recorded in POINT_START, every STAGE record and SCHEDULER_START.
PARENT_THREAD_ENV = {_k: os.environ.get(_k) for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                                                       'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')}
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import argparse
import hashlib
import importlib.util
import json
import math
import struct
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = os.path.dirname(os.path.realpath(__file__))
COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v002.py'          # KS3' common
COMMON_SHA = 'fcd63a739c8ec36e3ce3f9ad9de65532acd649da5ecc91e7131b60d020c9d4c8'


def _load_common():
    with open(COMMON_PATH, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != COMMON_SHA:
        raise SystemExit('REFUSED: s4rc1_common pin mismatch')
    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004_ks3_c2v002', COMMON_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    exec(compile(raw, COMMON_PATH, 'exec'), mod.__dict__)
    return mod


C = _load_common()
Refusal = C.Refusal
RUNNER_PATH = os.path.realpath(__file__)
STAGE_SCHEMA = 'S4RC1_CP1_STAGE_C3V002'
REVIEW_SCHEMA_EPS = 'UNT_POINT_EPS_REVIEW_CX2V001'
EPS_SHELLS = C.SHELL_END - 4                      # 178 unit shells [4,5] .. [181,182]
EPS_AUDITS = 14                                   # producer AUDIT_LO below 182
ADAPT_EPS_APPROVED_PRODUCERS = (C.PINS['response_producer'][1], C.PINS['eps_adapter'][1])
DEFAULT_TOL = 1e-3                                # anchor cross-check, proposal for root
ANCHOR_TOL_MAX = 1e-2                             # F2: the tolerance must be finite with 0 < tol <= 1e-2
DEFAULT_R2_SPIKE_ALLOWANCE_GIB = 26.0             # F1 floor defaults: root choices (run sheet section 3)
DEFAULT_PER_WORKER_PEAK_GIB = 2.0
DEFAULT_FLOOR_MARGIN_GIB = 4.0
ANCHOR_CONTEXT_HOLD_POLL_SECONDS = 30.0           # F6: a held point re-reads the anchor folder this often
# c3v003 RHO stage (0696; A134 Q5, (a)4). No threshold is declared: these are the registered record's own fields.
RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'    # response producer a1dcdea8 L30
RHO_VERDICT = 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED'  # a1dcdea8 L360
RHO_COVERAGE = [4.0, float(C.SHELL_END)]          # [4, ceil(sqrt(2) * 128)] = [4, 182] (a1dcdea8 L361)
RHO_PARTITION = [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
                 [64.0, 128.0], [128.0, 182.0]]   # a1dcdea8 shell_plan(unit=False) L112-121 at K_big 128
RHO_HELD = 'HELD_PENDING_PROOF_SIDE_REVIEW'
RHO_GATE_SCHEMA = 'S4RC1_CP1_RHO_GATE_C3V003'
RHO_PAIR_SCHEMA = 'S4RC1_CP1_ANCHOR_RHO_PAIR_C3V003'
RHO_REVIEW_ROOTS = ('/Users/bgm/Research',)       # Codex1's review record: anywhere in Research, lexical policy applies
RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')   # wrapper v002 L177-178
# KS3 (A160): row 32 (S1_UA_C3T, kept K 3) only.
EPS_LO_S1 = 3                                     # 179 unit shells [3,4] .. [181,182]
RHO_COVERAGE_S1 = [3.0, float(C.SHELL_END)]
RHO_PARTITION_S1 = [[3.0, 4.0]] + RHO_PARTITION   # the 10-shell partition of KS2 shell_plan(unit=False) at K 3
ADAPT_EPS_APPROVED_PRODUCERS_S1 = (C.PINS['response_producer_ks2'][1], C.PINS['eps_adapter_g4'][1])   # KS3' (G4)


def runner_pin():
    return {'path': RUNNER_PATH, 'sha256': C.sha256_file(RUNNER_PATH)}


def common_pin():
    return {'path': COMMON_PATH, 'sha256': COMMON_SHA}


def thread_env_record():
    """F4: the in-process values (all '1': enforced by override at import) and the parent values, as found."""
    return {'thread_env': C.single_thread_env(), 'thread_env_parent': dict(PARENT_THREAD_ENV),
            'thread_env_rule': 'ENFORCED_BY_OVERRIDE_AT_IMPORT (parent values are recorded, never refused)'}


def require_anchor_tol(tol):
    """F2: nan, inf or 1e3 (a typo for 1e-3) would turn the anchor stop rule into AGREE on any record."""
    if type(tol) not in (int, float) or not math.isfinite(tol) or not 0 < tol <= ANCHOR_TOL_MAX:
        raise Refusal('ANCHOR_TOL_MUST_BE_FINITE_WITH_0_LT_TOL_LE_1e-2: %r' % (tol,))
    return tol


def require_nonnegative(name, x):
    """F1/F2: a setting that must be finite and >= 0 (the swap hold in MiB, the floor settings in GiB)."""
    if type(x) not in (int, float) or not math.isfinite(x) or x < 0:
        raise Refusal('%s_MUST_BE_FINITE_AND_NONNEGATIVE: %r' % (name, x))
    return x


def validate_out_root(out_root, *, parent=C.LANE_ROOT, prefix='cp1_'):
    p = str(out_root)
    C.require_policy(p, (C.ART,), 'out-root')            # lexical: uvt_, ngc3198, C5H, run trees, '..'
    if os.path.dirname(p) != parent or not os.path.basename(p).startswith(prefix):
        raise Refusal('OUT_ROOT_MUST_BE %s/%s<name> (runner own folder; never Codex2 certificates_per_point)' % (parent, prefix))
    return p


def point_dir_name(row, attempt):
    return 'P%02d_%s_%s_a%d' % (row['row'], row['key'][:16], row['label'], attempt)


def anchor_attempt_dirs(out_root):
    row = C.point_rows()[0]
    stem = 'P%02d_%s_%s_a' % (row['row'], row['key'][:16], row['label'])
    if not os.path.isdir(out_root):
        return []
    return [os.path.join(out_root, d) for d in sorted(os.listdir(out_root)) if d.startswith(stem)]


def anchor_context_record(out_root):
    """F6: (record, None) for the single anchor attempt's STAGE_CONTEXT; (None, 'HOLD') while that attempt has
    neither a readable context record nor a POINT_STOP/POINT_DONE; otherwise (None, stop code).

    certs_common PINS 'lwr_common' and 'seed_scan_result' carry sha None (not verified at load),
    so every point's recorded source pins must equal the anchor's: a drift stops the point.
    More than one anchor attempt is refused: no attempt is picked by sort order.
    """
    k16 = C.ANCHOR_KEY[:16]
    dirs = anchor_attempt_dirs(out_root)
    if len(dirs) > 1:
        return None, 'ANCHOR_ATTEMPTS_AMBIGUOUS (%d anchor attempt folders; none is picked by sort order)' % len(dirs)
    if not dirs:
        return None, 'ANCHOR_NOT_STARTED_IN_THIS_OUT_ROOT'
    try:
        with open(os.path.join(dirs[0], 'STAGE_CONTEXT_%s.json' % k16), 'rb') as f:
            return json.loads(f.read()), None
    except (OSError, ValueError):
        pass                                          # absent or still being written: hold unless the anchor ended
    for end in ('POINT_STOP', 'POINT_DONE'):
        if os.path.exists(os.path.join(dirs[0], '%s_%s.json' % (end, k16))):
            return None, 'ANCHOR_ENDED_WITHOUT_A_READABLE_CONTEXT_RECORD (%s)' % end
    return None, 'HOLD'


def hold_for_anchor_context(out_root, *, poll=ANCHOR_CONTEXT_HOLD_POLL_SECONDS, sleep=time.sleep):
    """F6: a non-anchor point that has run its CONTEXT stage holds here until the anchor's context record
    exists. It stops if the anchor stops first, if no anchor attempt exists, or if more than one does."""
    t0, polls = time.monotonic(), 0
    while True:
        rec, why = anchor_context_record(out_root)
        if why != 'HOLD':
            return rec, why, {'polls': polls, 'held_seconds': time.monotonic() - t0}
        if polls == 0:
            sys.stderr.write(json.dumps({'event': 'ANCHOR_CONTEXT_HOLD', 'utc': C.utc(), 'out_root': out_root}) + '\n')
            sys.stderr.flush()
        polls += 1
        sleep(poll)


def measured_stage_peak_rss(out_root):
    """F1: the largest STAGE peak RSS (bytes) recorded in this out-root, 0 if none yet.

    None if any STAGE record is unreadable or malformed (for example still being written): the floor then
    fails closed for that poll.
    """
    peak = 0
    if not os.path.isdir(out_root):
        return peak
    for d in sorted(os.listdir(out_root)):
        pdir = os.path.join(out_root, d)
        if not (d.startswith('P') and os.path.isdir(pdir)):
            continue
        for name in sorted(os.listdir(pdir)):
            if not (name.startswith('STAGE_') and name.endswith('.json')):
                continue
            try:
                with open(os.path.join(pdir, name), 'rb') as f:
                    v = json.loads(f.read()).get('peak_rss_bytes_process_high_water')
            except (OSError, ValueError, AttributeError):
                return None
            if not C.finite_number(v, 0):
                return None
            peak = max(peak, v)
    return peak


def require_registered(settings, shell_ranges, node_limit):
    """No smoke and no partial work can enter CP-1 (brief section 4 item 3)."""
    if settings != 'registered':
        raise Refusal('SMOKE_OR_UNREGISTERED_SETTINGS_REFUSED: %r' % (settings,))
    if shell_ranges is not None:
        raise Refusal('PARTIAL_SHELL_SELECTION_REFUSED (full point domain only)')
    if node_limit is not None:
        raise Refusal('PARTIAL_GQ_NODE_LIMIT_REFUSED (all production nodes only)')


def require_compute_environment():
    if not C.background_qos():
        raise Refusal('BACKGROUND_QOS_REQUIRED: run under `taskpolicy -b` (getpriority(PRIO_DARWIN_PROCESS) != 1)')
    if not C.isolated_interpreter():
        raise Refusal('ISOLATED_INTERPRETER_REQUIRED: python3 -I -B')
    env = C.single_thread_env()
    if any(v != '1' for v in env.values()):           # F4: an invariant of the override at import; it can
        raise Refusal('SINGLE_THREAD_BLAS_ENV_REQUIRED: %r' % (env,))   # fire only if os.environ changes later


def load_spec(row):
    """Spec pin check from bytes, then the point key (core recipe) against brief section 3."""
    path = C.require_policy(row['spec_path'], (C.ART,), 'spec')
    with open(path, 'rb') as f:
        raw = f.read()
    if C.sha256_bytes(raw) != row['spec_sha256']:
        raise Refusal('SPEC_PIN_MISMATCH: ' + path)
    spec = json.loads(raw)
    key = C.point_key(spec)
    if key != row['key']:
        raise Refusal('POINT_KEY_MISMATCH: %s != %s' % (key, row['key']))
    if spec.get('galaxy') != 'DDO154':
        raise Refusal('DDO154_SPEC_REQUIRED')
    uv = spec['numerics']['uv_tail']
    if uv.get('outer') != {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0} or uv.get('gas', {}).get('M_s') != 128:
        raise Refusal('PRODUCTION_K128_MS128_REQUIRED')
    return spec, {'path': path, 'sha256': row['spec_sha256']}


def real_loader():
    """Canonical-path imports of the two pinned producers (R4)."""
    gq = C.load_pinned('gq_producer', 's4rc1_cp1_gq_producer_cx2v005')
    pr = C.load_pinned('response_producer', 's4rc1_cp1_point_response_cx2v002')
    return gq, pr


def real_loader_s1():
    """KS3', row 32 (S1_UA_C3T): the G3 GQ producer successor and the KS2 response producer (both on KS1)."""
    gq = C.load_pinned('gq_producer_g3', 's4rc1_cp1_gq_producer_g3_c2v001')
    pr = C.load_pinned('response_producer_ks2', 's4rc1_cp1_point_response_ks2_c2v001')
    return gq, pr


def check_gq(gq, key, custody_sha256, s1=False):
    want = C.canonical_pin('gq_producer_g3' if s1 else 'gq_producer')   # KS3': row 32's GQ producer is the G3 successor
    checks = {
        'schema_gate': gq.get('schema') == C.PROOF_SCHEMA and gq.get('gate') == 'GQ',
        'status_TESTED_verdict_PASS': gq.get('status') == 'TESTED' and gq.get('verdict') == 'PASS',
        'point_sha256_is_key': gq.get('point_sha256') == key,
        'custody_sha256_matches_context': gq.get('custody_sha256') == custody_sha256,
        'producer_pin_canonical_R4': gq.get('producer') == want,
        'all_production_nodes': gq.get('all_production_kperp_nodes') is True and
                                gq.get('nodes_tested') == gq.get('production_nodes'),
        'method_and_orders': gq.get('method') == 'GEOMETRY_UNIFORM_COLUMN_BOUND' and gq.get('M_s') == 128 and
                             gq.get('M_s_doubled') == 256 and gq.get('K_big_inverse_kpc') == 128.0,
    }
    b, z = gq.get('max_column_difference_over_analytic_Pi0'), gq.get('max_zero_mode_relative_error')
    checks['bound_le_1e-12'] = (C.finite_number(b, 0) and C.finite_number(z, 0) and z < 1 and b / (1 - z) <= 1e-12)
    return checks


def gq_c000_crosscheck(gq):
    """HEADLINE_CORNER_000 only: compare with Codex2's existing record a785ccca (no stop)."""
    old = C.read_json_pinned(C.canonical_pin('gq_record_c000'), (C.ART,), 'GQ record a785ccca')
    keys = ('point_sha256', 'custody_sha256', 'max_column_difference_over_analytic_Pi0',
            'max_zero_mode_relative_error', 'nodes_tested', 'production_nodes', 'columns', 'worst',
            'geometry_sha256', 'verdict', 'producer')
    diff = sorted(k for k in keys if gq.get(k) != old.get(k))
    return {'reference': C.canonical_pin('gq_record_c000'), 'compared_fields': list(keys),
            'differing_fields': diff, 'verdict': 'AGREE' if not diff else 'DIFFER'}


def check_eps(eps, key, custody, s1=False):
    shells = eps.get('shells') or []
    want = [[float(n), float(n + 1)] for n in range(EPS_LO_S1 if s1 else 4, C.SHELL_END)]   # KS3: row 32 from 3
    return {
        'schema_gate': eps.get('schema') == 'UNT_POINT_EPS_NUMERICAL_CX2V001' and eps.get('gate') == 'EPS',
        'registered_full_search': eps.get('settings') == 'registered' and eps.get('full_registered_search_executed') is True
                                  and eps.get('coverage_complete') is True,
        'registered_discrete_CERTIFIED': eps.get('registered_discrete_verdict') == 'CERTIFIED',
        'verdict_review_required': eps.get('verdict') == 'NUMERICAL_RULE_PASSED_REVIEW_REQUIRED',
        'point_sha256_is_key': eps.get('point_sha256') == key,
        'custody_matches_context': eps.get('custody') == custody,
        'producer_pin_canonical_R4': eps.get('producer') == C.canonical_pin('response_producer_ks2' if s1 else 'response_producer'),
        ('shells_3_to_182_unit' if s1 else 'shells_4_to_182_unit'): [s.get('range_inverse_kpc') for s in shells] == want,
        'dense_audits_14': len(eps.get('envelope_audit') or []) == EPS_AUDITS,
    }


# ---------------------------------------------------------------- c3v003: the RHO stage (0696)
def rho_gate(allow_rho=False, review_pin=None, review_sha256=None, *, out_root=None):
    """0696: the RHO stage runs only with --allow-rho plus the sha of Codex1's proof-side review record, matched against
    the root-provided pin of that record, whose bytes are read and hashed here. Anything else reads
    HELD_PENDING_PROOF_SIDE_REVIEW. Never raises: a malformed gate is a held gate."""
    rec = {'schema': RHO_GATE_SCHEMA, 'utc': C.utc(), 'allow_rho': allow_rho is True, 'review_pin': review_pin,
           'review_sha256': review_sha256, 'open': False, 'status': RHO_HELD, 'reason': None}
    try:
        if allow_rho is not True:
            raise Refusal('ALLOW_RHO_NOT_GIVEN')
        if not C.is_pin(review_pin):
            raise Refusal('ROOT_PROVIDED_REVIEW_PIN_MISSING_OR_NOT_AN_EXACT_PIN')
        if not C.is_sha(review_sha256) or review_sha256 != review_pin['sha256']:
            raise Refusal('PROOF_SIDE_REVIEW_SHA_DOES_NOT_MATCH_THE_ROOT_PIN')
        p = C.require_policy(review_pin['path'], RHO_REVIEW_ROOTS, 'proof-side review')
        if out_root and p.startswith(str(out_root).rstrip('/') + '/'):
            raise Refusal('REVIEW_INSIDE_RUNNER_OUTPUT_ROOT (the runner never holds or writes approvals)')
        C.read_bytes_pinned(review_pin, RHO_REVIEW_ROOTS, 'proof-side review', max_bytes=None)
        rec.update(open=True, status='OPEN', reason='REVIEW_RECORD_BYTES_MATCH_THE_ROOT_PIN')
    except (Refusal, OSError, ValueError, TypeError, KeyError) as exc:
        rec['reason'] = type(exc).__name__ + ': ' + str(exc)
    return rec


def gate_argv(gate_args):
    """The worker/rho-repeat arguments that carry the operator's gate inputs unchanged (each process re-checks)."""
    g = gate_args or {}
    out = ['--allow-rho'] if g.get('allow_rho') is True else []
    if g.get('review_pin') is not None:
        out += ['--proof-side-review-pin', json.dumps(g['review_pin'], sort_keys=True)]
    if g.get('review_sha256') is not None:
        out += ['--proof-side-review-sha256', str(g['review_sha256'])]
    return out


def gate_args_from_cli(ns):
    pin = None
    if getattr(ns, 'proof_side_review_pin', None):
        try:
            pin = json.loads(ns.proof_side_review_pin)
        except ValueError:
            pin = 'UNPARSEABLE_JSON'                  # read as a held gate, never a crash
    return {'allow_rho': bool(getattr(ns, 'allow_rho', False)), 'review_pin': pin,
            'review_sha256': getattr(ns, 'proof_side_review_sha256', None)}


def check_rho(rho, key, custody, s1=False):
    shells = rho.get('shells') if isinstance(rho.get('shells'), list) else []
    vals = [s.get('rho_used') if isinstance(s, dict) else None for s in shells]
    return {
        'schema_gate': rho.get('schema') == RHO_SCHEMA and rho.get('gate') == 'RHO_G',
        'status_TESTED_verdict_review_required': rho.get('status') == 'TESTED' and rho.get('verdict') == RHO_VERDICT,
        'registered_full_search': rho.get('settings') == 'registered' and rho.get('full_registered_search_executed') is True
                                  and rho.get('coverage_complete') is True,
        ('coverage_3_to_182' if s1 else 'coverage_4_to_182'):
            rho.get('required_coverage_inverse_kpc') == (RHO_COVERAGE_S1 if s1 else RHO_COVERAGE),
        ('partition_10_shells_K_big_128' if s1 else 'partition_9_shells_K_big_128'):
            [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells] == (RHO_PARTITION_S1 if s1 else RHO_PARTITION),
        'rho_used_finite_nonnegative': bool(vals) and all(C.finite_number(v, 0) for v in vals),
        'point_sha256_is_key': rho.get('point_sha256') == key,
        'custody_matches_context': rho.get('custody') == custody,
        'producer_pin_canonical_R4': rho.get('producer') == C.canonical_pin('response_producer_ks2' if s1 else 'response_producer'),
    }


def rho_projection(rho):
    """INTERFACE_C3V001 section 0 (the slot proof's definition): partition plus IEEE-754 bits of every rho_used."""
    return [[list(s['range_inverse_kpc']), struct.pack('<d', float(s['rho_used'])).hex()] for s in rho['shells']]


def rho_stage(pr, spec, ctx, key, details, out_root, out, k16, letter, gate, s1=False):
    """One registered rho run (attempt a or b) in THIS process; record, stage record, checks. Returns (ok, stage)."""
    plog = C.LineLog(out('RHO_PROGRESS_%s_%s.jsonl' % (k16, letter)), out_root)
    u0 = C.usage()
    rho = pr.produce_rho(spec, settings='registered', shell_ranges=None, context=ctx,
                         progress=lambda x: plog.write(dict(x, utc=C.utc())))
    u1 = C.usage()
    plog.close()
    pin = C.write_new(out('RHO_NUMERIC_%s_%s.json' % (k16, letter)), rho, out_root)
    checks = check_rho(rho, key, details['custody'], s1=s1)
    rec = dict({'schema': STAGE_SCHEMA, 'stage': 'RHO', 'rho_attempt': letter, 'utc': C.utc(), 'key': key, 'record': pin,
                'pid': os.getpid(), 'gate': gate}, **C.stage_metrics(u0, u1), **thread_env_record(),
               producer_seconds=rho.get('seconds'), producer_peak_rss_bytes=rho.get('peak_rss_bytes'),
               verdict=rho.get('verdict'), n_shells=len(rho.get('shells') or []),
               record_bytes=os.path.getsize(pin['path']), checks=checks, ok=all(checks.values()))
    C.write_new(out('STAGE_RHO_%s_%s.json' % (letter, k16)), rec, out_root)
    return rec['ok'], rec


def anchor_rho_pair_record(rec_a, rec_b, out_root):
    """Diagnostic only: (a)4 is decided by the slot proof (lo_slot_proof_c3v003, V03) on root-registered records."""
    a = C.read_json_pinned(rec_a['record'], (out_root,), 'anchor rho a', max_bytes=None)
    b = C.read_json_pinned(rec_b['record'], (out_root,), 'anchor rho b', max_bytes=None)
    pa, pb = rho_projection(a), rho_projection(b)
    ca, cb = (C.canonical({k: x.get(k) for k in RHO_COMPARE_KEYS}) for x in (a, b))
    return {'schema': RHO_PAIR_SCHEMA, 'utc': C.utc(), 'key': C.ANCHOR_KEY, 'records': [rec_a['record'], rec_b['record']],
            'pids': [rec_a.get('pid'), rec_b.get('pid')], 'separate_processes': rec_a.get('pid') != rec_b.get('pid'),
            'distinct_records': rec_a['record']['sha256'] != rec_b['record']['sha256'] and rec_a['record']['path'] != rec_b['record']['path'],
            'projection_bitwise_equal_diagnostic': pa == pb, 'projection_sha256': [C.digest(pa), C.digest(pb)],
            'wrapper_v002_10_key_canonical_equal_diagnostic': ca == cb,
            'rule': ('A134 (a)4 is decided by lo_slot_proof_c3v003 on two root-registered rho records at this key, by '
                     'wrapper v002\'s 10-key canonical comparison (L177-179, L189-191; A138 V03); the projection is a '
                     'diagnostic only. This record is the runner diagnostic only. Registration is root\'s: slot rho = '
                     'attempt a, (a)4 pair = (a, b).')}


def spawn_rho_repeat(row, out_root, *, attempt, run_id, gate_args):
    """(a)4 attempt b: a SEPARATE process (taskpolicy -b python3 -I -B, single-thread BLAS) with a fresh context."""
    cmd = [C.TASKPOLICY, '-b', sys.executable, '-I', '-B', RUNNER_PATH, 'rho-repeat', '--out-root', out_root,
           '--point', row['key'], '--attempt', str(attempt), '--run-id', run_id] + gate_argv(gate_args)
    env = dict(os.environ)
    env.update({k: '1' for k in C.THREAD_ENV})
    logdir = os.path.join(out_root, 'worker_logs')
    os.makedirs(logdir, exist_ok=True)
    base = os.path.join(logdir, point_dir_name(row, attempt) + '_rho_b_' + (run_id or 'run'))
    with open(base + '.stdout.txt', 'x') as so, open(base + '.stderr.txt', 'x') as se:
        rc = subprocess.call(cmd, stdin=subprocess.DEVNULL, stdout=so, stderr=se, env=env, close_fds=True)
    return rc, {'exit': rc, 'stdout': base + '.stdout.txt', 'stderr': base + '.stderr.txt'}


def rho_repeat_point(row, out_root, *, attempt=1, run_id='', gate_args=None, loader=real_loader):
    """The anchor's attempt b, run by `rho-repeat` in its own process: fresh point context, the same registered call."""
    require_compute_environment()
    if row['key'] != C.ANCHOR_KEY:
        raise Refusal('RHO_REPEAT_IS_FOR_THE_ANCHOR_KEY_ONLY ((a)4)')
    gate = rho_gate(**(gate_args or {}), out_root=out_root)
    if not gate['open']:
        raise Refusal(RHO_HELD + ': ' + str(gate['reason']))
    spec, _ = load_spec(row)
    key, k16 = row['key'], row['key'][:16]
    pdir = find_point_dir(out_root, row, attempt)
    out = lambda name: os.path.join(pdir, name)
    st_a = read_stage(pdir, out_root, 'STAGE_RHO_a_%s.json' % k16)
    ctx_a = read_stage(pdir, out_root, 'STAGE_CONTEXT_%s.json' % k16)
    if st_a.get('ok') is not True:
        raise Refusal('RHO_ATTEMPT_A_NOT_OK')
    for name in ('RHO_NUMERIC_%s_b.json' % k16, 'STAGE_RHO_b_%s.json' % k16):
        if os.path.exists(out(name)):
            raise Refusal('RHO_ATTEMPT_B_EXISTS (one attempt b per point attempt; never overwritten)')
    _, pr = loader()
    ctx = pr.point_context(spec)
    details = ctx['details']
    if details['point_sha256'] != key or C.digest(details['custody']) != details['custody_sha256'] \
            or details['custody'] != ctx_a.get('custody'):
        raise Refusal('RHO_REPEAT_CONTEXT_POINT_OR_CUSTODY_MISMATCH')
    ok, rec = rho_stage(pr, spec, ctx, key, details, out_root, out, k16, 'b', gate)
    return (0 if ok else 3), rec


def run_point(row, out_root, *, operator_lane, attempt=1, run_id='', loader=None,
              settings='registered', shell_ranges=None, node_limit=None,
              hold_poll_seconds=ANCHOR_CONTEXT_HOLD_POLL_SECONDS, hold_sleep=time.sleep,
              rho_gate_args=None, rho_spawn=None):
    """One point, GQ then EPS then RHO (c3v003), in this process (anchor attempt b in a separate one). (exit, summary)."""
    s1 = C.is_s1_row(row)                             # KS3: row 32 (S1_UA_C3T) takes KS1/KS2 and the kept-K-3 checks
    loader = loader or (real_loader_s1 if s1 else real_loader)
    require_registered(settings, shell_ranges, node_limit)
    require_compute_environment()
    if not isinstance(operator_lane, str) or not operator_lane.strip():
        raise Refusal('OPERATOR_LANE_REQUIRED')
    spec, spec_pin = load_spec(row)
    key = row['key']
    k16 = key[:16]
    pdir = os.path.join(out_root, point_dir_name(row, attempt))
    C.require_policy(pdir, (out_root,), 'point dir')
    if os.path.realpath(os.path.dirname(pdir)) != out_root:      # F5: checked BEFORE os.mkdir, never after
        raise Refusal('OUTPUT_PARENT_NOT_CANONICAL (realpath differs; no point folder created): ' + out_root)
    try:
        os.mkdir(pdir)                               # exclusive: an existing attempt is never reused
    except FileExistsError:
        raise Refusal('POINT_DIR_EXISTS_NOT_RERUN (use a new --attempt): ' + pdir)
    out = lambda name: os.path.join(pdir, name)
    start = {'schema': 'S4RC1_CP1_POINT_START_C3V002', 'utc': C.utc(), 'run_id': run_id, 'attempt': attempt,
             'point': {k: row[k] for k in ('row', 'key', 'label', 'names', 'distance_Mpc', 'q_inf')},
             'spec': spec_pin, 'operator_lane': operator_lane, 'runner': runner_pin(), 'common': common_pin(),
             'producers': {'gq': C.canonical_pin('gq_producer_g3' if s1 else 'gq_producer'), 'eps': C.canonical_pin('response_producer_ks2' if s1 else 'response_producer')},
             'settings': settings, 'shell_ranges': shell_ranges, 'gq_node_limit': node_limit,
             'qos': {'darwin_bg': C.background_qos(), 'taskpolicy': '-b'}, 'thread_env': C.single_thread_env(),
             'python': {'executable': sys.executable, 'version': sys.version, 'isolated': sys.flags.isolated,
                        'dont_write_bytecode': sys.flags.dont_write_bytecode}, 'pid': os.getpid()}
    start.update(thread_env_record())                 # F4
    if s1:                                            # KS3: the row file it came from (row 32 only)
        start['s1_c3t_row'] = {'row_file': row['row_file'], 'kept_K': row['kept_K']}
    C.write_new(out('POINT_START_%s.json' % k16), start, out_root)
    summary = {'point_dir': pdir, 'key': key, 'stages': {}}

    def stop(stage, reason, extra=None):
        rec = {'schema': 'S4RC1_CP1_POINT_STOP_C3V002', 'utc': C.utc(), 'key': key, 'stage': stage,
               'reason': reason, 'detail': extra, 'stages': summary['stages']}
        C.write_new(out('POINT_STOP_%s.json' % k16), rec, out_root)
        return 3, dict(summary, stopped=stage, reason=reason)

    try:
        gq_mod, pr = loader()
        import numpy
        start_np = {'numpy_version': numpy.__version__, 'numpy_file': numpy.__file__}
        # Context once (shared by EPS now and by LO later).
        u0 = C.usage()
        ctx = pr.point_context(spec)
        u1 = C.usage()
        details = ctx['details']
        ctx_rec = dict({'schema': STAGE_SCHEMA, 'stage': 'CONTEXT', 'utc': C.utc(), 'key': key},
                       **C.stage_metrics(u0, u1), **thread_env_record(), runtime=start_np,
                       point_sha256=details['point_sha256'], custody=details['custody'],
                       custody_sha256=details['custody_sha256'], source_pins=ctx.get('source_pins'),
                       point_symbol_checks=ctx.get('checks'),
                       checks={'point_sha256_is_key': details['point_sha256'] == key,
                               'custody_sha256_is_digest': C.digest(details['custody']) == details['custody_sha256']})
        mine = ctx_rec['source_pins']
        if s1:                                        # KS3: KS1/KS2 replace exactly the custody and producer pins (F6)
            try:
                mine = C.s1_pins_as_table(mine)
                ctx_rec['checks']['s1_source_pins_are_ks1_and_ks2'] = True
            except Refusal:
                mine, ctx_rec['checks']['s1_source_pins_are_ks1_and_ks2'] = None, False
        anchor_ctx, anchor_why, hold = None, None, None
        if key != C.ANCHOR_KEY:                       # F6: never proceed while the anchor's context record is absent
            anchor_ctx, anchor_why, hold = hold_for_anchor_context(out_root, poll=hold_poll_seconds, sleep=hold_sleep)
            ctx_rec['checks']['anchor_context_record_present'] = anchor_ctx is not None
        ctx_rec['checks_info'] = {'source_pins_match_anchor': None if anchor_ctx is None else
                                  anchor_ctx.get('source_pins') == mine,
                                  'anchor_context': 'THIS_POINT_IS_THE_ANCHOR' if key == C.ANCHOR_KEY else
                                  (anchor_why or 'PRESENT'), 'anchor_context_hold': hold}
        if anchor_ctx is not None:
            ctx_rec['checks']['source_pins_match_anchor'] = anchor_ctx.get('source_pins') == mine
        C.write_new(out('STAGE_CONTEXT_%s.json' % k16), ctx_rec, out_root)
        summary['stages']['CONTEXT'] = ctx_rec['seconds']
        if not all(ctx_rec['checks'].values()):
            return stop('CONTEXT', ('ANCHOR_CONTEXT_RECORD_UNAVAILABLE: ' + anchor_why) if anchor_why else
                        'CONTEXT_POINT_CUSTODY_OR_SOURCE_PIN_MISMATCH', ctx_rec['checks'])
        # GQ (its producer derives custody itself; it takes no context argument).
        u2 = C.usage()
        gq = gq_mod.produce(spec, node_limit=None, progress=None)
        u3 = C.usage()
        gq_pin = C.write_new(out('GQ_PROOF_%s.json' % k16), gq, out_root)
        gq_checks = check_gq(gq, key, details['custody_sha256'], s1=s1)
        gq_rec = dict({'schema': STAGE_SCHEMA, 'stage': 'GQ', 'utc': C.utc(), 'key': key, 'record': gq_pin},
                      **C.stage_metrics(u2, u3), **thread_env_record(), producer_seconds=gq.get('seconds'), status=gq.get('status'),
                      verdict=gq.get('verdict'), conservative_bound=gq.get('conservative_bound'),
                      record_bytes=os.path.getsize(gq_pin['path']), checks=gq_checks, ok=all(gq_checks.values()))
        if key == C.CORNER000_KEY:
            gq_rec['c000_existing_record_crosscheck'] = gq_c000_crosscheck(gq)
        C.write_new(out('STAGE_GQ_%s.json' % k16), gq_rec, out_root)
        summary['stages']['GQ'] = gq_rec['seconds']
        if not gq_rec['ok']:
            return stop('GQ', 'GQ_NOT_A_CLEAN_PASS (recorded as measured; EPS skipped for this point)', gq_checks)
        # EPS: full registered domain, shells sequential in this process.
        plog = C.LineLog(out('EPS_PROGRESS_%s.jsonl' % k16), out_root)
        u4 = C.usage()
        eps = pr.produce_eps(spec, settings='registered', shell_ranges=None, context=ctx,
                             progress=lambda x: plog.write(dict(x, utc=C.utc())))
        u5 = C.usage()
        plog.close()
        eps_pin = C.write_new(out('EPS_NUMERIC_%s.json' % k16), eps, out_root)
        eps_checks = check_eps(eps, key, details['custody'], s1=s1)
        size = os.path.getsize(eps_pin['path'])            # slot record: no 8 MiB rule (guard reads proofs, not slots)
        eps_rec = dict({'schema': STAGE_SCHEMA, 'stage': 'EPS', 'utc': C.utc(), 'key': key, 'record': eps_pin},
                       **C.stage_metrics(u4, u5), **thread_env_record(), producer_seconds=eps.get('seconds'),
                       producer_peak_rss_bytes=eps.get('peak_rss_bytes'), verdict=eps.get('verdict'),
                       eps_max=eps.get('eps_max'), eps_max_shell=eps.get('eps_max_shell'),
                       n_shells=len(eps.get('shells') or []), n_audits=len(eps.get('envelope_audit') or []),
                       record_bytes=size, checks=eps_checks, ok=all(eps_checks.values()))
        C.write_new(out('STAGE_EPS_%s.json' % k16), eps_rec, out_root)
        summary['stages']['EPS'] = eps_rec['seconds']
        if not eps_rec['ok']:
            return stop('EPS', 'EPS_RECORD_NOT_ADMISSIBLE_AS_RECORDED', eps_checks)
        # c3v003 RHO (0696): one stage after EPS; held unless the proof-side review gate is open.
        gate = rho_gate(**(rho_gate_args or {}), out_root=out_root)
        rho_done = {'status': RHO_HELD, 'gate': gate}
        if not gate['open']:
            u6 = C.usage()
            held = dict({'schema': STAGE_SCHEMA, 'stage': 'RHO', 'utc': C.utc(), 'key': key, 'status': RHO_HELD,
                         'record': None, 'gate': gate}, **C.stage_metrics(u6, u6), **thread_env_record())
            C.write_new(out('STAGE_RHO_HELD_%s.json' % k16), held, out_root)
            summary['stages']['RHO'] = RHO_HELD
        else:
            ok_a, rec_a = rho_stage(pr, spec, ctx, key, details, out_root, out, k16, 'a', gate, s1=s1)
            summary['stages']['RHO_a'] = rec_a['seconds']
            if not ok_a:
                return stop('RHO', 'RHO_RECORD_NOT_ADMISSIBLE_AS_RECORDED (attempt a)', rec_a['checks'])
            rho_done = {'status': 'COMPUTED', 'gate': gate, 'rho_numeric': rec_a['record']}
            if key == C.ANCHOR_KEY:                   # (a)4: attempt b in a separate process, after attempt a
                rc_b, info_b = (rho_spawn or spawn_rho_repeat)(row, out_root, attempt=attempt, run_id=run_id,
                                                               gate_args=rho_gate_args or {})
                try:
                    st_b = read_stage(pdir, out_root, 'STAGE_RHO_b_%s.json' % k16)
                except (OSError, ValueError, Refusal):
                    st_b = None
                if rc_b != 0 or not isinstance(st_b, dict) or st_b.get('ok') is not True:
                    return stop('RHO_ANCHOR_REPEAT', 'ANCHOR_RHO_ATTEMPT_B_NOT_A_CLEAN_RECORD (exit %s)' % (rc_b,),
                                {'spawn': info_b, 'stage_b_ok': None if not isinstance(st_b, dict) else st_b.get('ok')})
                pair = C.write_new(out('ANCHOR_RHO_PAIR_%s.json' % k16), anchor_rho_pair_record(rec_a, st_b, out_root), out_root)
                summary['stages']['RHO_b'] = st_b.get('seconds')
                rho_done.update(rho_numeric_b=st_b['record'], anchor_rho_pair=pair)
        request = {'schema': 'S4RC1_EPS_REVIEW_REQUEST_C3V002', 'verdict': 'TEMPLATE_NOT_A_REVIEW',
                   'note': 'Copy these exact bindings into a distinct-lane review written OUTSIDE the runner output '
                           'root (template REVIEW_TEMPLATE_EPS_C3V001.json). The runner never writes a review.',
                   'bindings': {'schema': REVIEW_SCHEMA_EPS, 'numeric_ref': eps_pin,
                                'point_sha256': key, 'custody_sha256': details['custody_sha256'],
                                'adapter_sha256': C.PINS['eps_adapter_g4' if s1 else 'eps_adapter'][1],   # KS3': G4 for row 32
                                'accepts_registered_numerical_estimate_not_rigorous_sup': '<FILL: true only after review>'},
                   'excluded_reviewer_lanes': sorted({operator_lane, C.CODEX2_PRODUCER_LANE})}
        C.write_new(out('EPS_REVIEW_REQUEST_%s.json' % k16), request, out_root)
        done = {'schema': 'S4RC1_CP1_POINT_DONE_C3V002', 'utc': C.utc(), 'key': key, 'spec': spec_pin,
                'gq_proof': gq_pin, 'eps_numeric': eps_pin, 'custody_sha256': details['custody_sha256'],
                'stages_seconds': summary['stages'], 'rho': rho_done,
                'next': ('distinct-lane EPS review, then `adapt-eps`; root registers the rho record(s), then the LO slot '
                         'proof (proof side c3v003); LO is per-state post-run acceptance (A134 Q2-Q5)')}
        C.write_new(out('POINT_DONE_%s.json' % k16), done, out_root)
        return 0, dict(summary, done=True)
    except Refusal as exc:
        return stop('REFUSAL', str(exc))
    except Exception as exc:                          # recorded, never retried automatically (A50)
        return stop('EXCEPTION', type(exc).__name__ + ': ' + str(exc)[:2000],
                    traceback.format_exc(limit=8)[-4000:])


# ---------------------------------------------------------------- anchor cross-check (stop rule)
def _rel(a, b):
    if not (C.finite_number(a) and C.finite_number(b)):
        return math.inf
    return abs(a - b) / max(abs(b), 1e-300)


def compare_anchor_records(eps, v006, tol=DEFAULT_TOL):
    """Anchor EPS (cx2v002) against EPS_CERT_V006 on overlapping shells.

    V006 [2,5) shells carry eps = converged actual-set value with eps_envelope above it, so
    raw `eps` is NOT comparable on [4,5]. Compared per shell:
      envelope:   eps_envelope(cx2) vs eps_envelope(V006)                (verdict)
      dominating: eps(cx2) vs max(eps, eps_envelope)(V006)               (verdict)
      discrete:   eps_base, eps_refined, refinements                      (diagnostic)
      actual-set: actual.estimate(cx2) vs eps_actual_set(V006)            (diagnostic)
    AGREE iff all 178 shells overlap and both verdict ratios are <= tol (F2: finite, 0 < tol <= 1e-2).
    """
    require_anchor_tol(tol)
    old = {tuple(s['range_inverse_kpc']): s for s in v006.get('shells', [])}
    rows, worst_env, worst_dom, bad = [], 0.0, 0.0, []
    for s in eps.get('shells', []):
        r = tuple(s['range_inverse_kpc'])
        o = old.get(r)
        if o is None:
            bad.append('NO_V006_SHELL_%s' % (list(r),))
            continue
        env = _rel(s.get('eps_envelope'), o.get('eps_envelope'))
        dom = _rel(s.get('eps'), max(o.get('eps'), o.get('eps_envelope')))
        row = {'range_inverse_kpc': list(r), 'rel_envelope': env, 'rel_dominating': dom,
               'rel_eps_base': _rel(s.get('eps_base'), o.get('eps_base')),
               'rel_eps_refined': _rel(s.get('eps_refined'), o.get('eps_refined')),
               'refinements_equal': s.get('refinements') == o.get('refinements'),
               'rel_actual_set': _rel((s.get('actual') or {}).get('estimate'), o.get('eps_actual_set'))}
        rows.append(row)
        worst_env, worst_dom = max(worst_env, env), max(worst_dom, dom)
        if env > tol or dom > tol:
            bad.append('SHELL_%s_DISAGREES' % (list(r),))
    if len(rows) != EPS_SHELLS:
        bad.append('OVERLAP_COUNT_%d_NOT_%d' % (len(rows), EPS_SHELLS))
    return {'verdict': 'AGREE' if not bad else 'DISAGREE', 'tolerance_relative': tol,
            'overlap_shells': len(rows), 'max_rel_envelope': worst_env, 'max_rel_dominating': worst_dom,
            'max_rel_discrete': max([max(x['rel_eps_base'], x['rel_eps_refined']) for x in rows] or [0.0]),
            'refinement_mismatches': sum(not x['refinements_equal'] for x in rows),
            'problems': bad[:50], 'shells': rows,
            'rule': 'brief section 5 / dispatch: stop CP-1 if the anchor EPS disagrees with EPS_CERT_V006 on '
                    'overlapping shells. Tolerance is the builder proposal; root may set another.'}


def find_point_dir(out_root, row, attempt):
    pdir = os.path.join(out_root, point_dir_name(row, attempt))
    C.require_policy(pdir, (out_root,), 'point dir')
    if not os.path.isdir(pdir):
        raise Refusal('POINT_DIR_MISSING: ' + pdir)
    return pdir


def read_stage(pdir, out_root, name):
    p = os.path.join(pdir, name)
    C.require_policy(p, (out_root,), 'stage')
    with open(p, 'rb') as f:
        return json.loads(f.read())


def run_compare_anchor(out_root, *, attempt=1, tol=DEFAULT_TOL, v006_pin=None):
    row = C.point_rows()[0]
    pdir = find_point_dir(out_root, row, attempt)
    st = read_stage(pdir, out_root, 'STAGE_EPS_%s.json' % row['key'][:16])
    if st.get('ok') is not True:
        raise Refusal('ANCHOR_EPS_STAGE_NOT_OK')
    eps = C.read_json_pinned(st['record'], (out_root,), 'anchor EPS record', max_bytes=None)
    ref = v006_pin or C.canonical_pin('eps_cert_v006')
    v6 = C.read_json_pinned(ref, (C.ART, out_root), 'EPS_CERT_V006')
    res = compare_anchor_records(eps, v6, tol)
    res.update(schema='S4RC1_ANCHOR_EPS_CROSSCHECK_C3V002', utc=C.utc(), anchor_eps=st['record'], eps_cert_v006=ref)
    tag = ('%g' % tol).replace('.', 'p').replace('-', 'm').replace('+', '')
    pin = C.write_new(os.path.join(pdir, 'ANCHOR_EPS_CROSSCHECK_%s_tol%s.json' % (row['key'][:16], tag)), res, out_root)
    return res['verdict'], pin, res


def anchor_agreed(out_root):
    """True iff at least one anchor cross-check exists (any attempt) and every one reads AGREE."""
    row = C.point_rows()[0]
    stem = 'P%02d_%s_%s_a' % (row['row'], row['key'][:16], row['label'])
    verdicts = []
    if not os.path.isdir(out_root):
        return False
    for d in sorted(os.listdir(out_root)):
        if not d.startswith(stem):
            continue
        pdir = os.path.join(out_root, d)
        for name in sorted(os.listdir(pdir)):
            if name.startswith('ANCHOR_EPS_CROSSCHECK_'):
                try:
                    with open(os.path.join(pdir, name), 'rb') as f:
                        verdicts.append(json.loads(f.read()).get('verdict'))
                except (OSError, ValueError):
                    verdicts.append('UNREADABLE')
    return bool(verdicts) and all(v == 'AGREE' for v in verdicts)


# ---------------------------------------------------------------- scheduler (across points only)
class Scheduler:
    """Starts one worker process per point; parallel across points only (R5).

    A point starts only when: a slot is free (max_concurrent), the hold file is absent, swap
    has not grown past the hold threshold (stricter-only guard, A130/0166), the memory gate
    passes (memory_pressure free % >= 25 + margin), the physical-headroom floor passes (F1:
    vm_stat (free + speculative) x page size >= r2_spike_allowance + (running + 1) x per_worker_peak
    + floor_margin; stricter-only beside the 0674 gate, and a start needs both), and, for every point
    except the anchor and HEADLINE_CORNER_000, the anchor EPS cross-check reads AGREE. At most one start
    per poll. The scheduler never pauses a running worker: SIGSTOP stays root's manual run-sheet step (S6).
    """

    def __init__(self, rows, out_root, *, operator_lane, max_concurrent, margin_pct, attempt=1,
                 hold_file=None, swap_hold_mib=512.0, poll_seconds=60.0, spawn=None, memory=None,
                 swap=None, sleep=time.sleep, compare=None, log=None, tol=DEFAULT_TOL, run_id='',
                 r2_spike_allowance_gib=DEFAULT_R2_SPIKE_ALLOWANCE_GIB, per_worker_peak_gib=DEFAULT_PER_WORKER_PEAK_GIB,
                 floor_margin_gib=DEFAULT_FLOOR_MARGIN_GIB, vmstat=None, rho_gate_args=None):
        if type(max_concurrent) is not int or not 1 <= max_concurrent <= 8:
            raise Refusal('MAX_CONCURRENT_1_TO_8')
        if type(margin_pct) not in (int, float) or not 1 <= margin_pct <= 50:
            raise Refusal('MARGIN_PCT_1_TO_50 (gate is 25 %% + margin)')
        if not isinstance(operator_lane, str) or not operator_lane.strip():
            raise Refusal('OPERATOR_LANE_REQUIRED')
        require_anchor_tol(tol)                                                     # F2
        require_nonnegative('SWAP_HOLD_MIB', swap_hold_mib)                         # F2
        for name, v in (('R2_SPIKE_ALLOWANCE_GIB', r2_spike_allowance_gib), ('PER_WORKER_PEAK_GIB', per_worker_peak_gib),
                        ('FLOOR_MARGIN_GIB', floor_margin_gib)):
            require_nonnegative(name, v)                                            # F1
        self.floor_gib = {'r2_spike_allowance_gib': r2_spike_allowance_gib, 'per_worker_peak_gib': per_worker_peak_gib,
                          'floor_margin_gib': floor_margin_gib}                     # F1: root choices, recorded
        self.vmstat = vmstat or C.vm_stat_reading
        self.rows, self.out_root, self.lane = list(rows), out_root, operator_lane
        self.max_concurrent, self.margin, self.attempt = max_concurrent, margin_pct, attempt
        self.hold_file, self.swap_hold, self.poll, self.run_id = hold_file, swap_hold_mib, poll_seconds, run_id
        self.spawn, self.memory = spawn or self._spawn, memory or C.memory_free_percent
        self.swap, self.sleep, self.log, self.tol = swap or C.swap_used_mib, sleep, log, tol
        self.compare = compare or (lambda: run_compare_anchor(out_root, attempt=attempt, tol=tol))
        self.running, self.results, self.stopped = {}, {}, None
        self.swap_base = None
        self.rho_gate_args = dict(rho_gate_args or {})   # c3v003: passed unchanged to every worker (each re-checks)

    def note(self, **ev):
        ev['utc'] = C.utc()
        if self.log:
            self.log.write(ev)

    def _spawn(self, row):
        cmd = [C.TASKPOLICY, '-b', sys.executable, '-I', '-B', RUNNER_PATH, 'worker',
               '--out-root', self.out_root, '--point', row['key'], '--operator-lane', self.lane,
               '--attempt', str(self.attempt), '--run-id', self.run_id] + gate_argv(self.rho_gate_args)
        env = dict(os.environ)
        env.update({k: '1' for k in C.THREAD_ENV})
        logdir = os.path.join(self.out_root, 'worker_logs')
        os.makedirs(logdir, exist_ok=True)
        base = os.path.join(logdir, point_dir_name(row, self.attempt) + '_' + (self.run_id or 'run'))
        so = open(base + '.stdout.txt', 'x')
        se = open(base + '.stderr.txt', 'x')
        return subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=so, stderr=se, env=env, close_fds=True)

    def _reap(self):
        for key, (row, proc) in list(self.running.items()):
            rc = proc.poll()
            if rc is None:
                continue
            del self.running[key]
            self.results[key] = rc
            self.note(event='POINT_EXIT', key=key, row=row['row'], label=row['label'], exit_code=rc)
            if key == C.ANCHOR_KEY:
                if rc != 0:
                    self.stopped = 'ANCHOR_WORKER_DID_NOT_FINISH_CLEANLY (exit %s)' % rc
                    continue
                try:
                    verdict, pin, res = self.compare()
                except Exception as exc:
                    verdict, pin, res = 'ERROR', None, {'error': type(exc).__name__ + ': ' + str(exc)}
                self.note(event='ANCHOR_EPS_CROSSCHECK', verdict=verdict, record=pin,
                          max_rel_envelope=res.get('max_rel_envelope'), max_rel_dominating=res.get('max_rel_dominating'),
                          error=res.get('error'))
                if verdict != 'AGREE':
                    self.stopped = 'ANCHOR_EPS_DISAGREES_WITH_EPS_CERT_V006 or check failed (stop rule; root ruling required)'

    def _floor(self):
        """F1: the physical-headroom floor for one start decision (recorded with that decision)."""
        g = self.floor_gib
        configured = g['per_worker_peak_gib'] * C.GIB
        measured = measured_stage_peak_rss(self.out_root)
        if measured is None:
            return {'ok': False, 'reason': 'STAGE_PEAK_RSS_UNREADABLE (a STAGE record in this out-root is unreadable '
                    'or malformed; no start this poll)', 'settings_gib': dict(g)}
        ok, why, detail = C.physical_floor(self.vmstat(), running=len(self.running),
                                           r2_spike_allowance_bytes=g['r2_spike_allowance_gib'] * C.GIB,
                                           per_worker_peak_bytes=max(configured, measured),
                                           floor_margin_bytes=g['floor_margin_gib'] * C.GIB)
        return dict(detail, ok=ok, reason=why, settings_gib=dict(g), per_worker_peak_configured_bytes=configured,
                    per_worker_peak_measured_stage_bytes=measured)

    def _gate(self, row):
        """Returns (reason or None, memory free percent, physical-floor record) for this decision."""
        if self.stopped:
            return 'STOPPED: ' + self.stopped, None, None
        if len(self.running) >= self.max_concurrent:
            return 'SLOTS_FULL', None, None
        if row['key'] not in (C.ANCHOR_KEY, C.CORNER000_KEY) and not anchor_agreed(self.out_root):
            if C.ANCHOR_KEY not in [r['key'] for r in self.rows]:
                self.stopped = 'ANCHOR_CROSSCHECK_AGREE_REQUIRED_BEFORE_OTHER_POINTS (run the anchor first)'
                return 'STOPPED: ' + self.stopped, None, None
            return 'WAITING_FOR_ANCHOR_EPS_CROSSCHECK', None, None
        if self.hold_file and os.path.exists(self.hold_file):
            return 'HOLD_FILE_PRESENT (root pause, e.g. a T-case waiting for admission)', None, None
        sw = self.swap()
        if sw is None or self.swap_base is None or sw > self.swap_base + self.swap_hold:
            return 'SWAP_GROWTH_HOLD (used %s MiB; base %s MiB; hold +%.0f MiB)' % (sw, self.swap_base, self.swap_hold), None, None
        free = self.memory()
        ok, why = C.memory_gate(free, self.margin)
        floor = self._floor()                         # F1: stricter-only; a start needs the 0674 gate AND the floor
        if not ok:
            return why, free, floor
        return (None if floor['ok'] else floor['reason']), free, floor

    def run(self):
        pending = list(self.rows)
        self.swap_base = self.swap()
        self.note(event='SCHEDULER_START', swap_used_mib_base=self.swap_base, points=[r['key'] for r in pending], max_concurrent=self.max_concurrent,
                  margin_pct=self.margin, poll_seconds=self.poll, operator_lane=self.lane, run_id=self.run_id,
                  physical_floor_settings_gib=dict(self.floor_gib), thread_env_parent=dict(PARENT_THREAD_ENV),
                  rho_gate=rho_gate(**self.rho_gate_args, out_root=self.out_root))
        last_wait = None
        while pending or self.running:
            self._reap()
            if pending:
                row = pending[0]
                pdir = os.path.join(self.out_root, point_dir_name(row, self.attempt))
                if os.path.exists(pdir):
                    self.results[row['key']] = 'POINT_DIR_EXISTS_NOT_RERUN'
                    self.note(event='SKIP', key=row['key'], reason='POINT_DIR_EXISTS_NOT_RERUN (use a new --attempt)')
                    pending.pop(0)
                    continue
                why, free, floor = self._gate(row)
                if why is None:
                    try:
                        proc = self.spawn(row)
                    except OSError as exc:
                        self.results[row['key']] = 'SPAWN_FAILED'
                        self.note(event='SPAWN_FAILED', key=row['key'], error=str(exc))
                        pending.pop(0)
                        continue
                    self.running[row['key']] = (row, proc)
                    pending.pop(0)
                    last_wait = None
                    self.note(event='POINT_START', key=row['key'], row=row['row'], label=row['label'],
                              memory_free_percent=free, physical_floor=floor, running=len(self.running))
                elif why.startswith('STOPPED'):
                    for r in pending:
                        self.results.setdefault(r['key'], 'NOT_STARTED')
                    self.note(event='SCHEDULER_STOP', reason=why, not_started=[r['key'] for r in pending])
                    pending = []
                elif why != last_wait:
                    self.note(event='WAIT', key=row['key'], reason=why, memory_free_percent=free, physical_floor=floor)
                    last_wait = why
            if pending or self.running:
                self.sleep(self.poll)
        self.note(event='SCHEDULER_END', results=self.results, stopped=self.stopped)
        return 0 if not self.stopped and all(v == 0 for v in self.results.values()) else 3


# ---------------------------------------------------------------- adapt-eps (after the review)
def real_adapter():
    return C.load_pinned('eps_adapter', 's4rc1_cp1_eps_adapter_cx2v003')


def real_adapter_s1():
    """KS3', row 32 (S1_UA_C3T): the G4 EPS adapter successor (KS2, KS1)."""
    return C.load_pinned('eps_adapter_g4', 's4rc1_cp1_eps_adapter_g4_c2v001')


def adapt_point(row, out_root, *, review_path, approved_review_sha256, approved_signer_lanes,
                attempt=1, adapter_loader=None, require_env=True, review_roots=(C.EXCHANGE,)):
    """Distinct-lane review first, then adapter v003 adapt_eps, then the proof (exclusive create)."""
    s1 = C.is_s1_row(row)                             # KS3': row 32 (S1_UA_C3T) takes the G4 adapter
    adapter_loader = adapter_loader or (real_adapter_s1 if s1 else real_adapter)
    if require_env:
        require_compute_environment()
    spec, spec_pin = load_spec(row)
    key, k16 = row['key'], row['key'][:16]
    pdir = find_point_dir(out_root, row, attempt)
    start = read_stage(pdir, out_root, 'POINT_START_%s.json' % k16)
    st = read_stage(pdir, out_root, 'STAGE_EPS_%s.json' % k16)
    ctx = read_stage(pdir, out_root, 'STAGE_CONTEXT_%s.json' % k16)
    if st.get('ok') is not True:
        raise Refusal('EPS_STAGE_NOT_OK')
    numeric_ref = st['record']
    C.read_bytes_pinned(numeric_ref, (out_root,), 'EPS numeric record', max_bytes=None)
    if os.path.exists(os.path.join(pdir, 'EPS_PROOF_%s.json' % k16)):
        raise Refusal('EPS_PROOF_EXISTS for this attempt (one proof per point attempt; never overwritten)')
    if not review_path:
        raise Refusal('EPS_REVIEW_MISSING (distinct-lane review required before adapt_eps)')
    rp = C.require_policy(review_path, review_roots, 'review')
    if not os.path.isfile(rp):
        raise Refusal('EPS_REVIEW_MISSING: ' + rp)
    C.require_canonical(rp)
    if rp.startswith(out_root.rstrip('/') + '/'):
        raise Refusal('REVIEW_INSIDE_RUNNER_OUTPUT_ROOT (the tool never holds or writes approvals)')
    with open(rp, 'rb') as f:
        raw = f.read()
    sha = C.sha256_bytes(raw)
    if not C.is_sha(approved_review_sha256) or sha != approved_review_sha256:
        raise Refusal('EPS_REVIEW_SHA_NOT_ROOT_APPROVED')
    review = json.loads(raw)
    problems = C.distinct_review_problems(review, approved_signer_lanes=approved_signer_lanes,
                                          excluded_lanes={start.get('operator_lane'), C.CODEX2_PRODUCER_LANE})
    want = {'schema': REVIEW_SCHEMA_EPS, 'verdict': 'APPROVED', 'numeric_ref': numeric_ref, 'point_sha256': key,
            'custody_sha256': ctx.get('custody_sha256'), 'adapter_sha256': C.PINS['eps_adapter_g4' if s1 else 'eps_adapter'][1],
            'accepts_registered_numerical_estimate_not_rigorous_sup': True}
    problems += ['EPS_REVIEW_FIELD_MISMATCH: ' + k for k, v in want.items() if review.get(k) != v]
    if problems:
        raise Refusal('EPS_REVIEW_REFUSED: ' + '; '.join(problems))
    review_ref = {'path': rp, 'sha256': sha}
    ad = adapter_loader()
    res = ad.adapt_eps(spec, numeric_ref, review_ref=review_ref,
                       approved_producer_sha256=ADAPT_EPS_APPROVED_PRODUCERS_S1 if s1 else ADAPT_EPS_APPROVED_PRODUCERS,
                       approved_review_sha256=(sha,))
    res_pin = C.write_new(os.path.join(pdir, 'EPS_ADAPTER_RESULT_%s_r%s.json' % (k16, sha[:12])), res, out_root)
    if res.get('verdict') != 'READY_FOR_MANIFEST' or not isinstance(res.get('proof'), dict):
        return 3, {'adapter_result': res_pin, 'blockers': res.get('blockers')}
    proof = res['proof']
    checks = {'producer_pin_canonical_R4': proof.get('producer') == C.canonical_pin('eps_adapter_g4' if s1 else 'eps_adapter'),
              'driver_certificate_is_numeric_ref': proof.get('driver_certificate') == numeric_ref,
              'point_sha256': proof.get('point_sha256') == key,
              'custody_sha256': proof.get('custody_sha256') == ctx.get('custody_sha256'),
              'tested_pass': proof.get('status') == 'TESTED' and proof.get('verdict') == 'PASS'}
    if not all(checks.values()):
        return 3, {'adapter_result': res_pin, 'checks': checks}
    proof_pin = C.write_new(os.path.join(pdir, 'EPS_PROOF_%s.json' % k16), proof, out_root)
    return 0, {'adapter_result': res_pin, 'eps_proof': proof_pin, 'checks': checks}


# ---------------------------------------------------------------- CLI
def plan(rows):
    out = []
    for row in rows:
        try:
            _, pin = load_spec(row)
            status = 'SPEC_AND_KEY_VERIFIED'
        except Refusal as exc:
            pin, status = None, 'REFUSED: ' + str(exc)
        out.append({'row': row['row'], 'label': row['label'], 'names': row['names'], 'key': row['key'],
                    'spec': pin, 'status': status, 'q_inf': row['q_inf'], 'distance_Mpc': row['distance_Mpc']})
        if C.is_s1_row(row):                          # KS3: row 32 only
            out[-1].update(kept_K=row['kept_K'], row_file=row['row_file'], eps_shells='179 unit shells [3,4]..[181,182]',
                           rho='coverage [3,182], 10 shells from [3,4]', producers={'eps_rho': C.canonical_pin('response_producer_ks2'),
                                                                                     'gq': C.canonical_pin('gq_producer_g3'),
                                                                                     'eps_adapter': C.canonical_pin('eps_adapter_g4')},
                           gwave='KS3\' (A175/A176): GQ is the G3 successor (kept K 3 node grid, custody KS1) and adapt-eps the '
                                 'G4 successor (KS2, 179 shells from 3); the S1 C1 approves G4, G3 and the G1 slot proof')
    return {'schema': 'S4RC1_CP1_PLAN_C3V002', 'utc': C.utc(), 'runner': runner_pin(), 'common': common_pin(),
            'points': out, 'gates': {'memory': 'memory_pressure free % >= 25 % + margin (default 5)',
                                     'physical_floor': 'vm_stat (free + speculative) x page size >= r2_spike_allowance + '
                                                       '(running + 1) x per_worker_peak + floor_margin (defaults 26, 2, 4 GiB)',
                                     'qos': 'taskpolicy -b and python3 -I -B required',
                                     'blas': 'single-thread BLAS enforced by override at import; parent values recorded',
                                     'anchor': 'other points wait for anchor AGREE; C000 holds after CONTEXT for the anchor context',
                                     'rho': ('c3v003: after EPS, produce_rho a1dcdea8 registered, [4,182], the 9-shell K_big 128 '
                                             'partition; the anchor runs attempt b in a separate process ((a)4); only with '
                                             '--allow-rho and the root-pinned proof-side review sha, else ' + RHO_HELD)},
            'estimates_UNTESTED': 'per point ~25-30 min normal QoS, ~40-90 min background QoS (brief section 5)'}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('plan')
    p.add_argument('--points')
    r = sub.add_parser('run')
    r.add_argument('--out-root', required=True)
    r.add_argument('--operator-lane', required=True)
    r.add_argument('--points')
    r.add_argument('--max-concurrent', type=int, default=4)
    r.add_argument('--margin-pct', type=float, default=5.0)
    r.add_argument('--attempt', type=int, default=1)
    r.add_argument('--hold-file')
    r.add_argument('--swap-hold-mib', type=float, default=512.0)
    r.add_argument('--poll-seconds', type=float, default=60.0)
    r.add_argument('--anchor-tol', type=float, default=DEFAULT_TOL)
    r.add_argument('--r2-spike-allowance-gib', type=float, default=DEFAULT_R2_SPIKE_ALLOWANCE_GIB)
    r.add_argument('--per-worker-peak-gib', type=float, default=DEFAULT_PER_WORKER_PEAK_GIB)
    r.add_argument('--floor-margin-gib', type=float, default=DEFAULT_FLOOR_MARGIN_GIB)
    w = sub.add_parser('worker')
    w.add_argument('--out-root', required=True)
    w.add_argument('--point', required=True)
    w.add_argument('--operator-lane', required=True)
    w.add_argument('--attempt', type=int, default=1)
    w.add_argument('--run-id', default='')
    rr = sub.add_parser('rho-repeat')                 # c3v003 internal: the anchor's attempt b, in its own process
    rr.add_argument('--out-root', required=True)
    rr.add_argument('--point', required=True)
    rr.add_argument('--attempt', type=int, default=1)
    rr.add_argument('--run-id', default='')
    for sp_ in (r, w, rr):                            # c3v003: the RHO gate inputs (0696)
        sp_.add_argument('--allow-rho', action='store_true')
        sp_.add_argument('--proof-side-review-pin', help='root-provided JSON pin {path, sha256} of Codex1\'s review record')
        sp_.add_argument('--proof-side-review-sha256')
    a = sub.add_parser('adapt-eps')
    a.add_argument('--out-root', required=True)
    a.add_argument('--point', required=True)
    a.add_argument('--attempt', type=int, default=1)
    a.add_argument('--review')
    a.add_argument('--approved-review-sha256')
    a.add_argument('--approved-signer-lane', action='append', default=[])
    c = sub.add_parser('compare-anchor')
    c.add_argument('--out-root', required=True)
    c.add_argument('--attempt', type=int, default=1)
    c.add_argument('--tol', type=float, default=DEFAULT_TOL)
    ns = ap.parse_args(argv)
    try:
        if ns.cmd == 'plan':
            print(json.dumps(plan(C.select_points(ns.points)), indent=1, sort_keys=True))
            return 0
        if ns.cmd in ('run', 'worker', 'adapt-eps', 'rho-repeat'):
            require_compute_environment()             # before any path is created or any input read
        if getattr(ns, 'attempt', 1) < 1:
            raise Refusal('ATTEMPT_MUST_BE_POSITIVE')
        if ns.cmd == 'run':                           # F1/F2: every setting is validated before any path is used
            require_anchor_tol(ns.anchor_tol)
            require_nonnegative('SWAP_HOLD_MIB', ns.swap_hold_mib)
            for name in ('r2_spike_allowance_gib', 'per_worker_peak_gib', 'floor_margin_gib'):
                require_nonnegative(name.upper(), getattr(ns, name))
        if ns.cmd == 'compare-anchor':
            require_anchor_tol(ns.tol)                # F2
        out_root = validate_out_root(ns.out_root)
        if ns.cmd == 'run':
            if ns.poll_seconds < 10:
                raise Refusal('POLL_SECONDS_MIN_10')
            rows = C.select_points(ns.points)
            os.makedirs(out_root, exist_ok=True)
            if os.path.realpath(out_root) != out_root:
                raise Refusal('OUT_ROOT_NOT_CANONICAL')
            run_id = C.utc_compact() + '_%d' % os.getpid()
            log = C.LineLog(os.path.join(out_root, 'SCHEDULER_%s.jsonl' % run_id), out_root)
            s = Scheduler(rows, out_root, operator_lane=ns.operator_lane, max_concurrent=ns.max_concurrent,
                          margin_pct=ns.margin_pct, attempt=ns.attempt, hold_file=ns.hold_file,
                          swap_hold_mib=ns.swap_hold_mib, poll_seconds=ns.poll_seconds, log=log, tol=ns.anchor_tol,
                          run_id=run_id, r2_spike_allowance_gib=ns.r2_spike_allowance_gib,
                          per_worker_peak_gib=ns.per_worker_peak_gib, floor_margin_gib=ns.floor_margin_gib,
                          rho_gate_args=gate_args_from_cli(ns))
            rc = s.run()
            log.close()
            print(json.dumps({'status': 'DONE' if rc == 0 else 'STOPPED', 'results': s.results, 'stopped': s.stopped,
                              'log': log.path}))
            return rc
        if ns.cmd == 'worker':
            rows = C.rows_for_key(ns.point)           # KS3: row 32 only for a key none of the 31 has
            if len(rows) != 1:
                raise Refusal('WORKER_POINT_KEY_NOT_IN_TABLE')
            if not os.path.isdir(out_root):
                raise Refusal('OUT_ROOT_MISSING')
            rc, summary = run_point(rows[0], out_root, operator_lane=ns.operator_lane, attempt=ns.attempt,
                                    run_id=ns.run_id, rho_gate_args=gate_args_from_cli(ns))
            print(json.dumps(summary, default=str))
            return rc
        if ns.cmd == 'rho-repeat':
            rows = C.rows_for_key(ns.point)
            if len(rows) != 1:
                raise Refusal('RHO_REPEAT_POINT_KEY_NOT_IN_TABLE')
            rc, rec = rho_repeat_point(rows[0], out_root, attempt=ns.attempt, run_id=ns.run_id,
                                       gate_args=gate_args_from_cli(ns))
            print(json.dumps({'ok': rec.get('ok'), 'record': rec.get('record'), 'pid': rec.get('pid')}, default=str))
            return rc
        if ns.cmd == 'adapt-eps':
            sel = C.select_points(ns.point)
            if len(sel) != 1:
                raise Refusal('ONE_POINT_REQUIRED')
            rc, res = adapt_point(sel[0], out_root, review_path=ns.review, approved_review_sha256=ns.approved_review_sha256,
                                  approved_signer_lanes=ns.approved_signer_lane, attempt=ns.attempt)
            print(json.dumps(res, default=str))
            return rc
        if ns.cmd == 'compare-anchor':
            verdict, pin, res = run_compare_anchor(out_root, attempt=ns.attempt, tol=ns.tol)
            print(json.dumps({'verdict': verdict, 'record': pin, 'max_rel_envelope': res['max_rel_envelope'],
                              'max_rel_dominating': res['max_rel_dominating']}))
            return 0 if verdict == 'AGREE' else 3
    except Refusal as exc:
        print(json.dumps({'status': 'REFUSED', 'reason': str(exc)}))
        return 2
    return 2


if __name__ == '__main__':
    sys.exit(main())
