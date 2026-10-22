"""retention_sweeper_c2v001 -- intermediate-file retention for COMPLETED, VERIFIED calibration forward calls (Claude2).

Authority: principal decision 2026-10-17 ~17:50Z, recorded verbatim in
  /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md
  section heading AUTH_HEADING (below).  Scope: calibration forward calls only (calls under the calibration
  orchestrator work dir), only after the call has completed and been verified; only intermediates (route-A checkpoint
  blobs, node diagnostics, stage arrays) are removed; result.json, receipts, specs, logs are always kept; a full
  sha256+size manifest of every file is written BEFORE anything is removed; earlier runs are never touched.

What one call is (calibration orchestrator c2v001 L640-713 / c2v002 L1347-1434, campaign c2v001 L4, L137-147):
  <work_dir>/waves/wave_NNNN/campaign/call_NNNN/{spec.json, RECEIPT.json(+.launch.json/.stdout.txt/.stderr.txt),
  monitor.stdout.txt, monitor.stderr.txt, out/<driver output>}.  The layout is configurable (--layout JSON).

A call is ELIGIBLE only if ALL hold (fail-closed; any unreadable fact = not eligible):
  E1 the call dir is a layout-conformant path strictly inside realpath(work_dir); no '..', no symlink component;
  E2 neither the work dir nor the call dir is under a PROTECTED root (snapshot denylist of CLAUDE2/runs/* names,
     every sibling of the work dir in each runs dir, both CODEX1 dirs, protected name patterns);
  E3 RECEIPT.json verifies with the pinned monitor's own verify_receipt (self-hash, spec pin == sha(spec.json),
     driver pin == config driver) and has status FINISHED, exit_code 0, stop_reason None, driver_status COMPLETED
     (MODEL_INVALID calls only with --include-model-invalid), result.path == <out>/result.json and
     result.sha256 == sha256(result.json bytes) == finish.json result_sha256;
  E4 the wave was ingested (WAVE_RESULT.json present) and exactly one cache entry (source WAVE) names this call dir and
     binds result_path/result_sha256 to those bytes; the orchestrator's OWN Cache._verify passes on it (called in
     process on the pinned orchestrator module) and the orchestrator's OWN CampaignExecutor.classify re-run on the
     call reproduces the cached classification, failure class, forward record and provenance;
  E5 no live process references the call dir (ps command lines, launch-record child pid; lsof +D unless --no-lsof);
  E6 recompute pins resolve: config driver bytes == pin, spec.json bytes == receipt spec pin, every static pin in
     out/start.json resolves to its sha256, the spec's coefficients pin resolves;
  E7 no symlink and no special file anywhere in the call dir; no whitelisted path is an evidence file of the cache
     entry (c2v002 provenance.evidence_files);
  E8 no other spec.json / WAVE_PLAN.json of the work dir names this call dir (a driver 'admit' block, c2v006 L744-769).
Default categories = the whole authorized scope: node_diagnostics, route_a_attempt_arrays, route_a_checkpoint_blobs,
stage_chain_arrays (--categories selects a subset; see RETENTION_DESIGN.md section 4 for what each tier costs).

Removal (apply): manifest first (tmp + rename + re-read verify), then only whitelisted REGULAR files under out/ are
unlinked through O_NOFOLLOW directory descriptors with inode+size re-checked; directories are never removed; files
with st_nlink > 1 are kept (reported).  Then every kept file is re-hashed against the manifest, the receipt/cache/
classify checks of E3-E4 are re-run, and RETENTION_RECORD.json is written LAST.  State on disk:
  FRESH      no RETENTION/MANIFEST_PRE_RETENTION.json
  PARTIAL    manifest present, no record  (crash between manifest and record; detectable, resumable)
  RETAINED   manifest + record present and both self-hashes verify
Rerun is idempotent: RETAINED calls are skipped (or re-verified with --verify-retained); PARTIAL calls are checked
file-by-file against the manifest (a changed kept file or an unexpected file refuses) and completed.

CLI (python -I -B):
  retention_sweeper_c2v001.py --orch-config CFG --orchestrator PY --orchestrator-sha256 H [--call DIR ...]
        [--runs-dir D ...] [--layout L.json] [--categories a,b] [--include-model-invalid] [--no-lsof]
        [--apply --authorization "<AUTH_HEADING>"] [--instructions PATH] [--verify-retained]
  retention_sweeper_c2v001.py --estimate-from OUTDIR [--free-gb 233] [--wave-sizes 6,12,24]   (read-only stat)
Default mode is PLAN (dry): nothing is written or removed.  Exit: 0 ok, 2 refused (config/authorization),
3 at least one call errored in apply/verify, 4 internal stop.
Importing this module does nothing.  numpy is not used.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import argparse
import datetime
import fcntl
import fnmatch
import hashlib
import importlib.util
import json
import stat
import subprocess
import sys
import time
import types
from pathlib import Path

TOOL_NAME = 'retention_sweeper_c2v001'
SCHEMA_MANIFEST = 'UNT_CALIBRATION_RETENTION_MANIFEST_C2V001'
SCHEMA_RECORD = 'UNT_CALIBRATION_RETENTION_RECORD_C2V001'
SCHEMA_PLAN = 'UNT_CALIBRATION_RETENTION_PLAN_C2V001'
AUTH_HEADING = ('## Principal: intermediate cleanup authorized for calibration calls — 2026-10-17 ~17:50Z')
UNT = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL'
DEFAULT_INSTRUCTIONS = UNT + '/CURRENT_INSTRUCTIONS.md'
REAL_RUNS_DIR = UNT + '/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs'
# Snapshot (2026-10-17) of every directory in CLAUDE2/runs: all of them are earlier runs and never touched.
PROTECTED_RUN_NAMES = (
    'A2_ANCHOR_F10_RUN_V001', 'A2_ANCHOR_F3_RUN_V001', 'A2_SEED_SCAN_G2_RUN_V001', 'A2_SEED_SCAN_REPLAY_C000_V001',
    'A2_SEED_SCAN_REPLAY_C001_V001', 'A2_SEED_SCAN_V004_REPRO_RUN_V001',
    'DDO154_ROUTE_B_C2V004_DECIDING_ADMIT_PREFIX_RUN_V001', 'DDO154_ROUTE_B_C2V005_DECIDING_ADMIT_PREFIX_RUN_V001',
    'DDO154_ROUTE_B_C2V006_DECIDING_ADMIT_PREFIX_RUN_V001', 'KMAX_A2F10_C2R_D7R1_RUN_V001', 'KMAX_A2F10_C3_RUN_V001',
    'KMAX_A2F10_C3_V005_RUN_V001', 'KMAX_A2F10_C4_RUN_V001', 'KMAX_A2F10_C4_V005_RUN_V001', 'KMAX_A2F10_R_RUN_V001',
    'KMAX_A2F10_R_V005_RUN_V001', 'KMAX_A2F10_S2R_D7R1_RUN_V001', 'KMAX_A2F10_S2_RUN_V001',
    'KMAX_A2F10_Y2R_D7R1_RUN_V001', 'KMAX_A2F10_Y2_RUN_V001', 'KMAX_A2F3_C3_RUN_V001', 'KMAX_A2F3_C4_RUN_V001',
    'KMAX_A2F3_R_RUN_V001', 'KMAX_A2F3_S2_RUN_V001', 'KMAX_A2F3_Y2_RUN_V001', 'KMAX_C2_A2_RUN_V001',
    'NGC3198_ROUTE_A_A2F10_RUN_V001', 'REPRO_PINNED_ADMIT_PREFIX_RUN_V001', 'REPRO_PINNED_FULL_RUN_V001')
STATIC_PROTECTED_ROOTS = tuple([UNT + '/CODEX1', UNT + '/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1']
                               + [REAL_RUNS_DIR + '/' + n for n in PROTECTED_RUN_NAMES])
# A work dir whose name matches one of these is an earlier/protected run, never a calibration work dir.
PROTECTED_NAME_PATTERNS = ('A2_ANCHOR*', 'A2_SEED_SCAN*', 'KMAX_*', 'REPRO*', 'NGC*', '*DECIDING*', '*CONVERGENCE*',
                           'CODEX1*', '*D7R1*', 'CAPTURE_*', 'OWNED_*')

# ------------------------------------------------------------------------------------------------ WHITELIST
# Globs are relative to the call OUTDIR (<call>/out), matched segment by segment ('*' never crosses '/').
# Consumer proofs: RETENTION_DESIGN.md section 3.  Nothing outside this table is ever removed.
WHITELIST = (
    {'id': 'W1_ROUTE_A_CHECKPOINT_BLOBS', 'category': 'route_a_checkpoint_blobs', 'authorized_as': 'route-A checkpoint blobs',
     'glob': 'stages/[0-9][0-9]_route_a/checkpoint/blobs/*.npy'},
    {'id': 'W2_ROUTE_A_ATTEMPT_ARRAYS', 'category': 'route_a_attempt_arrays', 'authorized_as': 'stage arrays',
     'glob': 'stages/[0-9][0-9]_route_a/attempt_[0-9][0-9][0-9]/arrays/*.npz'},
    {'id': 'W3_ROUTE_A_NODE_DIAGNOSTICS', 'category': 'node_diagnostics', 'authorized_as': 'node diagnostics',
     'glob': 'stages/[0-9][0-9]_route_a/attempt_[0-9][0-9][0-9]/node_diagnostics/iteration_*_nodes.jsonl'},
    {'id': 'W4_OFFSET_UNIT_NODE_DIAGNOSTICS', 'category': 'node_diagnostics', 'authorized_as': 'node diagnostics',
     'glob': 'stages/[0-9][0-9]_offset/offset/unit_nodes/iteration_*_nodes.jsonl'},
    {'id': 'W5_OFFSET_PREPARED', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays', 'glob': 'stages/[0-9][0-9]_offset/offset/offset_prepared.npz'},
    {'id': 'W5_OFFSET_SOURCE', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays', 'glob': 'stages/[0-9][0-9]_offset/offset/source_offset.npz'},
    {'id': 'W5_OFFSET_UNIT_RESPONSE', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays', 'glob': 'stages/[0-9][0-9]_offset/offset/unit_response.npz'},
    {'id': 'W5_OFFSET_UPDATED_BASE', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays',
     'glob': 'stages/[0-9][0-9]_offset/offset/updated_base_arrays.npz'},
    {'id': 'W6_ROTATION_BASE_ARRAYS', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays',
     'glob': 'stages/[0-9][0-9]_*_rotation/rotation/rotation_base_arrays.npz'},
    {'id': 'W7_FEEDBACK_PREPARED', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays',
     'glob': 'stages/[0-9][0-9]_*_feedback/feedback/feedback_prepared.npz'},
    {'id': 'W7_FEEDBACK_GAS_SOURCE', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays',
     'glob': 'stages/[0-9][0-9]_*_feedback/feedback/gas_source_feedback.npz'},
    {'id': 'W7_FEEDBACK_REFRESHED', 'category': 'stage_chain_arrays', 'authorized_as': 'stage arrays',
     'glob': 'stages/[0-9][0-9]_*_feedback/feedback/refreshed_prepared.npz'},
)
# Tiers (RETENTION_DESIGN.md s4): node_diagnostics are pinned nowhere; route_a_attempt_arrays are pinned only by the
# kept attempt result.json; route_a_checkpoint_blobs and stage_chain_arrays are the in-run chain (read by later stages
# of the SAME call while it runs; needed by a future 'admit' or a pin-walking re-verification of that call).
CATEGORIES = ('node_diagnostics', 'route_a_attempt_arrays', 'route_a_checkpoint_blobs', 'stage_chain_arrays')
# Defence in depth: these are never removable even if a glob above were edited to match them.
NEVER_REMOVE_BASENAMES = frozenset({'result.json', 'finish.json', 'start.json', 'request.json', 'failure.json',
                                    'IDENTITY.json', 'COMPLETED.json', 'START.json', 'operator_identity.json',
                                    'progress.jsonl', 'stdout.txt', 'stderr.txt', 'spec.json', 'RECEIPT.json',
                                    'checkpoint.lock', 'call_spec.json'})
NEVER_REMOVE_PREFIXES = ('FAILURE.', 'RECEIPT', 'monitor.', 'seed_')
NEVER_REMOVE_SUFFIXES = ('.end.json', '.start.json', '.txt', '.log')

LAYOUT_DEFAULT = {'waves_glob': 'waves/wave_[0-9][0-9][0-9][0-9]', 'campaign': 'campaign',
                  'call_glob': 'call_[0-9][0-9][0-9][0-9]', 'outdir': 'out', 'receipt': 'RECEIPT.json',
                  'launch': 'RECEIPT.json.launch.json', 'spec': 'spec.json', 'wave_result': 'WAVE_RESULT.json',
                  'cache_glob': 'cache/*', 'cache_header': 'CACHE_HEADER.json', 'cache_entries': 'entries',
                  'retention_dir': 'RETENTION'}
ADAPTERS = {
    'DDO154_CALIBRATION_ORCHESTRATOR_CONFIG_C2V001': {
        'module_name': 'calibration_orchestrator_c2v001', 'entry_schema': 'DDO154_CALIBRATION_CACHE_ENTRY_C2V001',
        'taxonomy': False},
    'DDO154_CALIBRATION_ORCHESTRATOR_CONFIG_C2V002': {
        'module_name': 'calibration_orchestrator_c2v002', 'entry_schema': 'DDO154_CALIBRATION_CACHE_ENTRY_C2V002',
        'taxonomy': True},
}
VALID_CLASSES = ('VALID',)
MODEL_INVALID_CLASSES = ('INVALID', 'MODEL_INVALID')      # c2v001 / c2v002 names of a final model/solver outcome
EXIT = {'OK': 0, 'REFUSED': 2, 'CALL_ERRORS': 3, 'STOP': 4}


class Refused(Exception):
    """Global refusal (configuration, pins, authorization)."""


class CallRefused(Exception):
    """This call is not eligible / not in a consistent state; nothing (more) is removed from it."""


class _InjectedCrash(BaseException):
    """TESTS ONLY: simulates a process death at a declared point (never raised outside an explicit test hook)."""


# ------------------------------------------------------------------------------------------------ helpers
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    """sha256 of a regular file opened with O_NOFOLLOW (a symlink raises)."""
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError('not a regular file: %s' % path)
        h = hashlib.sha256()
        while True:
            b = os.read(fd, 1 << 22)
            if not b:
                break
            h.update(b)
        return h.hexdigest()
    finally:
        os.close(fd)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def self_sha256():
    return sha256_file(os.path.realpath(__file__))


def safe_parts(rel):
    """Relative path -> segments; refuses absolute paths, empty, '.', '..' segments and NULs."""
    if not isinstance(rel, str) or not rel or rel.startswith('/') or '\x00' in rel:
        raise CallRefused('UNSAFE_PATH %r' % (rel,))
    parts = rel.split('/')
    for p in parts:
        if p in ('', '.', '..'):
            raise CallRefused('UNSAFE_PATH_SEGMENT %r in %r' % (p, rel))
    return parts


def match_rule(rel_out, categories=CATEGORIES):
    """Whitelist rule id for a path relative to the call OUTDIR, or None."""
    parts = safe_parts(rel_out)
    base = parts[-1]
    if base in NEVER_REMOVE_BASENAMES or base.startswith(NEVER_REMOVE_PREFIXES) or base.endswith(NEVER_REMOVE_SUFFIXES):
        return None
    for w in WHITELIST:
        if w['category'] not in categories:
            continue
        gp = w['glob'].split('/')
        if len(gp) == len(parts) and all(fnmatch.fnmatchcase(p, g) for p, g in zip(parts, gp)):
            return w['id']
    return None


def whitelist_sha256():
    return sha256_bytes(canonical(list(WHITELIST)))


def is_under(path, root):
    path, root = os.path.normpath(path), os.path.normpath(root)
    return path == root or path.startswith(root.rstrip('/') + '/')


def load_pinned_module(path, sha, name):
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refused('pin mismatch for %s' % path)
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    if sha256_file(path) != sha:
        raise Refused('%s changed while loading' % path)
    return m


def exec_pinned_bytes(path, sha, name):
    """As campaign_c2v001._load_monitor (L39-47): execute exactly the hashed bytes."""
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refused('pin mismatch for %s' % path)
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def write_json_new(path, obj):
    """Exclusive, crash-safe publish: tmp (exclusive, fsync) -> rename onto an ABSENT final name (caller holds the
    per-call flock) -> fsync dir -> re-read and verify.  Returns the file sha256."""
    path = Path(path)
    raw = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    tmp = path.with_name('.%s.%d.%d.tmp' % (path.name, os.getpid(), time.time_ns()))
    with open(tmp, 'xb') as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())
    if os.path.lexists(path):
        raise CallRefused('REFUSED_OVERWRITE %s exists' % path)
    os.rename(tmp, path)
    dfd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    back = path.read_bytes()
    if back != raw or sha256_bytes(back) != sha256_bytes(raw):
        raise CallRefused('WRITE_VERIFY_FAILED %s' % path)
    return sha256_bytes(raw)


def with_self_hash(body, field):
    body = dict(body)
    body.pop(field, None)
    body[field] = sha256_bytes(canonical(body))
    return body


def check_self_hash(doc, field):
    if not isinstance(doc, dict):
        return False
    body = {k: v for k, v in doc.items() if k != field}
    return doc.get(field) == sha256_bytes(canonical(body))


def append_jsonl(path, obj):
    fd = os.open(str(path), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, canonical(obj) + b'\n')
        os.fsync(fd)
    finally:
        os.close(fd)


# ------------------------------------------------------------------------------------------------ processes
def process_table():
    try:
        p = subprocess.run(['ps', '-axww', '-o', 'pid=,ppid=,command='], capture_output=True, text=True, timeout=60)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    rows = []
    for ln in p.stdout.splitlines():
        parts = ln.strip().split(None, 2)
        if len(parts) < 2:
            continue
        try:
            rows.append((int(parts[0]), int(parts[1]), parts[2] if len(parts) > 2 else ''))
        except ValueError:
            continue
    return rows


def own_ancestry(rows):
    ppid = {p: pp for p, pp, _ in rows}
    out, cur = set(), os.getpid()
    while cur and cur not in out:
        out.add(cur)
        cur = ppid.get(cur)
    return out


def live_refs(call_dir, call_dir_real):
    """Processes (other than this sweeper and its ancestors) whose command line names the call dir.  None = the
    process table could not be read (callers treat it as 'possibly referenced')."""
    rows = process_table()
    if rows is None:
        return None
    mine = own_ancestry(rows)
    out = []
    for pid, _, cmd in rows:
        if pid in mine:
            continue
        for d in {str(call_dir), str(call_dir_real)}:
            if (d + '/') in cmd or (d + ' ') in cmd or cmd.endswith(d):
                out.append({'pid': pid, 'command': cmd[:300]})
                break
    return out


def lsof_refs(path, timeout_s):
    """PIDs holding files open under `path` (lsof +D).  None = lsof failed / timed out (treated as referenced)."""
    try:
        p = subprocess.run(['lsof', '-n', '-P', '-t', '+D', str(path)], capture_output=True, text=True,
                           timeout=timeout_s)
    except Exception:
        return None
    pids = []
    for ln in p.stdout.split():
        try:
            pids.append(int(ln))
        except ValueError:
            return None
    if p.returncode not in (0, 1):      # macOS lsof +D exits 1 also when it printed PIDs (observed); >1 = failure
        return None
    return sorted(set(x for x in pids if x != os.getpid()))


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


# ------------------------------------------------------------------------------------------------ inventory
def inventory(call_dir_real, retention_name):
    """Walk the call dir without following anything.  -> (files {rel: lstat}, symlinks [rel], specials [rel])."""
    files, links, specials = {}, [], []
    stack = ['']
    while stack:
        rel = stack.pop()
        absd = os.path.join(call_dir_real, rel) if rel else call_dir_real
        for name in sorted(os.listdir(absd)):
            r = (rel + '/' + name) if rel else name
            if r == retention_name:
                continue
            st = os.lstat(os.path.join(absd, name))
            if stat.S_ISLNK(st.st_mode):
                links.append(r)
            elif stat.S_ISDIR(st.st_mode):
                stack.append(r)
            elif stat.S_ISREG(st.st_mode):
                files[r] = st
            else:
                specials.append(r)
    return files, links, specials


def open_dir_nofollow(root_real, parts):
    """Directory fd for root_real/parts[0]/.../parts[-1], every component opened O_NOFOLLOW|O_DIRECTORY."""
    fd = os.open(root_real, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for comp in parts:
            nfd = os.open(comp, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nfd
    except BaseException:
        os.close(fd)
        raise
    return fd


def unlink_checked(call_dir_real, rel, ino, size):
    """Unlink one whitelisted regular file.  -> 'REMOVED' | 'ALREADY_ABSENT'.  Raises CallRefused on any mismatch."""
    parts = safe_parts(rel)
    if parts[0] != 'out' or len(parts) < 3:
        raise CallRefused('REMOVAL_OUTSIDE_OUTDIR %s' % rel)
    try:
        fd = open_dir_nofollow(call_dir_real, parts[:-1])
    except FileNotFoundError:
        raise CallRefused('PARENT_DIR_MISSING %s' % rel)
    except OSError as exc:
        raise CallRefused('PARENT_NOT_A_PLAIN_DIR %s: %s' % (rel, exc))
    try:
        try:
            st = os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            return 'ALREADY_ABSENT'
        if not stat.S_ISREG(st.st_mode):
            raise CallRefused('NOT_A_REGULAR_FILE %s' % rel)
        if st.st_ino != ino or st.st_size != size:
            raise CallRefused('FILE_CHANGED_SINCE_MANIFEST %s' % rel)
        if st.st_nlink != 1:
            raise CallRefused('HARDLINKED_AT_REMOVAL %s' % rel)
        os.unlink(parts[-1], dir_fd=fd)
        return 'REMOVED'
    finally:
        os.close(fd)


# ------------------------------------------------------------------------------------------------ environment
class Env:
    """Configuration, pinned modules and global checks (no side effects on disk)."""

    def __init__(self, *, orch_config, orchestrator, orchestrator_sha256, runs_dirs=(), layout=None,
                 categories=CATEGORIES, include_model_invalid=False, use_lsof=True, lsof_timeout_s=300.0):
        self.orch_config_path = os.path.abspath(orch_config)
        raw = Path(self.orch_config_path).read_bytes()
        self.orch_config_sha256 = sha256_bytes(raw)
        cfg = json.loads(raw.decode('utf-8'))
        self.cfg = cfg
        self.adapter = ADAPTERS.get(cfg.get('schema'))
        if self.adapter is None:
            raise Refused('orchestrator config schema %r is not a known calibration orchestrator (%s)'
                          % (cfg.get('schema'), sorted(ADAPTERS)))
        self.layout = dict(LAYOUT_DEFAULT)
        self.layout_sha256 = sha256_bytes(canonical(self.layout))
        if layout:
            lraw = Path(layout).read_bytes()
            extra = json.loads(lraw.decode('utf-8'))
            if set(extra) - set(LAYOUT_DEFAULT):
                raise Refused('unknown layout keys %s' % sorted(set(extra) - set(LAYOUT_DEFAULT)))
            self.layout.update(extra)
            self.layout_sha256 = sha256_bytes(canonical(self.layout))
        wd = cfg.get('work_dir')
        if not isinstance(wd, str) or not os.path.isabs(wd) or '..' in wd.split('/'):
            raise Refused('work_dir must be an absolute path without ..')
        self.work_dir = wd
        if not os.path.isdir(wd) or os.path.islink(wd):
            raise Refused('work_dir %s is not an existing plain directory' % wd)
        self.work_dir_real = os.path.realpath(wd)
        # protection (checked first, before anything inside the work dir is read)
        self.runs_dirs = [REAL_RUNS_DIR] + [os.path.abspath(r) for r in runs_dirs]
        self.protected_roots = self._protected_roots()
        reason = self.protected_reason(self.work_dir_real, check_name=True)
        if reason:
            raise Refused('WORK_DIR_PROTECTED: %s' % reason)
        inside = [r for r in self.protected_roots if is_under(os.path.realpath(r), self.work_dir_real)]
        if inside or any(is_under(os.path.realpath(rd), self.work_dir_real) for rd in self.runs_dirs):
            raise Refused('WORK_DIR_CONTAINS_PROTECTED_RUNS: %s' % (inside[:3] or 'work dir is a runs dir'))
        # only a work dir this config actually drove (orchestrator writes CONFIG_COPY_<sha16>.json, c2v001 L859-861,
        # c2v002 L1580)
        if not os.path.isfile(os.path.join(wd, 'CONFIG_COPY_%s.json' % self.orch_config_sha256[:16])):
            raise Refused('work_dir has no CONFIG_COPY_%s.json: this config did not drive this work dir'
                          % self.orch_config_sha256[:16])
        # pins
        for k in ('driver', 'monitor'):
            pin = cfg.get(k)
            if not isinstance(pin, dict) or not isinstance(pin.get('path'), str) or not isinstance(pin.get('sha256'), str):
                raise Refused('config %s {path, sha256} required' % k)
        self.driver = cfg['driver']
        self.monitor_pin = cfg['monitor']
        self.M = exec_pinned_bytes(self.monitor_pin['path'], self.monitor_pin['sha256'], 'retention_monitor')
        self.orch_pin = {'path': os.path.abspath(orchestrator), 'sha256': orchestrator_sha256}
        self.O = load_pinned_module(self.orch_pin['path'], orchestrator_sha256, 'retention_orch_' + orchestrator_sha256[:8])
        if getattr(self.O, 'MODULE_NAME', None) != self.adapter['module_name']:
            raise Refused('orchestrator module %r does not match config schema %s'
                          % (getattr(self.O, 'MODULE_NAME', None), cfg.get('schema')))
        if getattr(self.O, 'SCHEMA_CACHE_ENTRY', None) != self.adapter['entry_schema']:
            raise Refused('orchestrator cache-entry schema mismatch')
        self.taxonomy = None
        if self.adapter['taxonomy']:
            tp = cfg.get('taxonomy')
            traw = Path(tp['path']).read_bytes()
            if sha256_bytes(traw) != tp['sha256']:
                raise Refused('taxonomy pin mismatch')
            self.taxonomy = self.O.Taxonomy(json.loads(traw.decode('utf-8')), tp['sha256'])
        bad = [c for c in categories if c not in CATEGORIES]
        if bad or not categories:
            raise Refused('categories must be a non-empty subset of %s' % (CATEGORIES,))
        self.categories = tuple(categories)
        self.include_model_invalid = bool(include_model_invalid)
        self.use_lsof = bool(use_lsof)
        self.lsof_timeout_s = float(lsof_timeout_s)
        self.synthetic = cfg.get('synthetic_test') is True
        self._pin_memo = {}
        self._entries = None

    # ---------------------------------------------------------------- protection
    def _protected_roots(self):
        roots = set(STATIC_PROTECTED_ROOTS)
        for rd in self.runs_dirs:
            if not os.path.isdir(rd):
                continue
            for name in os.listdir(rd):
                p = os.path.join(rd, name)
                if os.path.realpath(p) == self.work_dir_real:
                    continue
                roots.add(p)
                roots.add(os.path.realpath(p))
        return sorted(roots)

    def protected_reason(self, path_real, check_name=False):
        for r in self.protected_roots:
            if is_under(path_real, r) or is_under(path_real, os.path.realpath(r)):
                return 'under protected root %s' % r
        if check_name:
            base = os.path.basename(path_real.rstrip('/'))
            for pat in PROTECTED_NAME_PATTERNS:
                if fnmatch.fnmatchcase(base, pat):
                    return 'name %s matches protected pattern %s' % (base, pat)
        return None

    # ---------------------------------------------------------------- enumeration
    def call_dirs(self):
        L = self.layout
        out = []
        for wd in sorted(Path(self.work_dir).glob(L['waves_glob'])):
            cd = wd / L['campaign']
            if not cd.is_dir():
                continue
            for c in sorted(cd.glob(L['call_glob'])):
                if c.is_dir() or c.is_symlink():
                    out.append(str(c))
        return out

    def _structure_ok(self, call_dir):
        """E1: layout-conformant, strictly inside work_dir, no '..', no symlink component."""
        if not isinstance(call_dir, str) or not os.path.isabs(call_dir):
            raise CallRefused('E1 call dir must be absolute: %r' % (call_dir,))
        if '..' in call_dir.split('/') or '/./' in call_dir:
            raise CallRefused('E1 UNSAFE_PATH: %s' % call_dir)
        if not is_under(call_dir, self.work_dir) or os.path.normpath(call_dir) == os.path.normpath(self.work_dir):
            raise CallRefused('E1 call dir is not inside the work dir: %s' % call_dir)
        rel = os.path.relpath(call_dir, self.work_dir)
        parts = safe_parts(rel)
        L = self.layout
        pat = L['waves_glob'].split('/') + [L['campaign'], L['call_glob']]
        if len(parts) != len(pat) or not all(fnmatch.fnmatchcase(p, g) for p, g in zip(parts, pat)):
            raise CallRefused('E1 call dir %s does not match layout %s' % (rel, '/'.join(pat)))
        cur = self.work_dir_real
        for p in parts:
            cur = os.path.join(cur, p)
            st = os.lstat(cur)
            if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode):
                raise CallRefused('E1 SYMLINK_OR_NONDIR_COMPONENT %s' % cur)
        real = os.path.realpath(call_dir)
        if real != cur or not is_under(real, self.work_dir_real):
            raise CallRefused('E1 realpath %s escapes the work dir' % real)
        r = self.protected_reason(real)
        if r:
            raise CallRefused('E2 PROTECTED: %s' % r)
        od = os.path.join(real, L['outdir'])
        st = os.lstat(od) if os.path.lexists(od) else None
        if st is None or stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode):
            raise CallRefused('E1 outdir %s missing or not a plain directory' % od)
        wave_dir = os.path.join(self.work_dir_real, *parts[:len(L['waves_glob'].split('/'))])
        return real, wave_dir

    # ---------------------------------------------------------------- cache
    def entries(self):
        """All cache entries of the work dir: [(path, entry, cache_id, header)]."""
        if self._entries is not None:
            return self._entries
        L = self.layout
        out = []
        for cdir in sorted(Path(self.work_dir).glob(L['cache_glob'])):
            hdrp = cdir / L['cache_header']
            if not hdrp.is_file():
                continue
            hdr = json.loads(hdrp.read_bytes().decode('utf-8'))
            if hdr.get('cache_id') != cdir.name:
                raise Refused('cache header id %r != dir %s' % (hdr.get('cache_id'), cdir.name))
            for p in sorted((cdir / L['cache_entries']).glob('*.json')):
                e = json.loads(p.read_bytes().decode('utf-8'))
                out.append((str(p), e, cdir.name, hdr))
        self._entries = out
        return out

    def spec_texts(self):
        """Every call spec.json and WAVE_PLAN.json of the work dir (read once per Env)."""
        if getattr(self, '_spec_texts', None) is None:
            L = self.layout
            out = []
            for wd in sorted(Path(self.work_dir_real).glob(L['waves_glob'])):
                if wd.is_symlink():
                    continue
                for p in [wd / 'WAVE_PLAN.json'] + sorted((wd / L['campaign']).glob(L['call_glob'] + '/' + L['spec'])):
                    if p.is_file() and not p.is_symlink():
                        out.append((os.path.realpath(str(p)), p.read_bytes().decode('utf-8', 'replace')))
            self._spec_texts = out
        return self._spec_texts

    def stub_ctx(self, cache_id, hdr):
        ctx = types.SimpleNamespace(cache_id=cache_id, row_ids=list(hdr.get('row_ids') or []), synthetic=self.synthetic,
                                    work_dir=Path(self.work_dir), M=self.M, driver=self.driver, taxonomy=self.taxonomy)
        return ctx

    def orch_verify(self, call_dir, entry_path, cache_id, hdr):
        """E3/E4 with the orchestrator's OWN functions: Cache._verify on the (re-read) entry, and
        CampaignExecutor.classify re-run on the call compared with the cached classification/forward/provenance."""
        out = {'cache_verify_ok': False, 'classify_identical': False, 'reasons': []}
        e = json.loads(Path(entry_path).read_bytes().decode('utf-8'))
        ctx = self.stub_ctx(cache_id, hdr)
        cache = self.O.Cache.__new__(self.O.Cache)
        cache.ctx = ctx
        try:
            cache._verify(e, Path(entry_path).stem)
            out['cache_verify_ok'] = True
        except Exception as exc:
            out['reasons'].append('Cache._verify: %s' % exc)
        ex = self.O.CampaignExecutor.__new__(self.O.CampaignExecutor)
        ex.ctx = ctx
        pv = e.get('provenance') or {}
        plan_call = {'spec_sha256': pv.get('spec_sha256')}
        rec = {'status': pv.get('campaign_status'), 'call_dir': pv.get('call_dir')}
        try:
            cls, fc, fwd, prov = ex.classify(plan_call, rec)
            same = (cls == e.get('classification') and fc == e.get('failure_class')
                    and canonical(fwd) == canonical(e.get('forward')))
            diffs = [k for k in prov if canonical(prov[k]) != canonical(pv.get(k))]
            if same and not diffs:
                out['classify_identical'] = True
            else:
                out['reasons'].append('classify differs: class %r/%r fc %r/%r provenance keys %s'
                                      % (cls, e.get('classification'), fc, e.get('failure_class'), diffs[:6]))
        except Exception as exc:
            out['reasons'].append('classify raised %s: %s' % (type(exc).__name__, exc))
        out['entry_file_sha256'] = sha256_file(entry_path)
        out['ok'] = out['cache_verify_ok'] and out['classify_identical']
        return out

    # ---------------------------------------------------------------- recompute pins (E6)
    def _pin_ok(self, path, sha):
        try:
            st = os.stat(path)
        except OSError:
            return False
        k = (path, st.st_size, st.st_mtime_ns, sha)
        if k not in self._pin_memo:
            try:
                self._pin_memo[k] = sha256_bytes(Path(path).read_bytes()) == sha   # pins outside the call: follow
            except OSError:
                self._pin_memo[k] = False
        return self._pin_memo[k]

    def recompute_pins(self, call_real, spec_sha):
        L = self.layout
        out = {'driver': self.driver, 'spec': {'path': os.path.join(call_real, L['spec']), 'sha256': spec_sha},
               'static_pins_checked': 0, 'coefficients': None}
        if not self._pin_ok(self.driver['path'], self.driver['sha256']):
            raise CallRefused('E6 DRIVER_BYTES_DO_NOT_MATCH_PIN %s' % self.driver['path'])
        start = os.path.join(call_real, L['outdir'], 'start.json')
        if not os.path.isfile(start):
            raise CallRefused('E6 out/start.json missing (static pins unknown)')
        sj = json.loads(Path(start).read_bytes().decode('utf-8'))
        if sj.get('driver_sha256') not in (None, self.driver['sha256']) or sj.get('call_spec_sha256') not in (None, spec_sha):
            raise CallRefused('E6 start.json is not bound to this driver/spec')
        sp = sj.get('static_pins')
        if not isinstance(sp, dict) or not sp:
            raise CallRefused('E6 start.json has no static_pins')
        for p, s in sorted(sp.items()):
            if not self._pin_ok(p, s):
                raise CallRefused('E6 STATIC_PIN_BROKEN %s' % p)
        out['static_pins_checked'] = len(sp)
        out['static_pins_sha256'] = sha256_bytes(canonical(sp))
        spec = json.loads(Path(out['spec']['path']).read_bytes().decode('utf-8'))
        co = spec.get('coefficients')
        if isinstance(co, dict) and co.get('path'):
            if not self._pin_ok(co['path'], co.get('sha256')):
                raise CallRefused('E6 COEFFICIENTS_PIN_BROKEN %s' % co['path'])
            out['coefficients'] = {'path': co['path'], 'sha256': co['sha256']}
        return out

    # ---------------------------------------------------------------- eligibility (E1-E7 minus hashing of the tree)
    def eligibility(self, call_dir):
        """-> dict facts; raises CallRefused with the first failing condition."""
        L = self.layout
        call_real, wave_dir = self._structure_ok(call_dir)
        out_real = os.path.join(call_real, L['outdir'])
        facts = {'call_dir': call_dir, 'call_dir_real': call_real, 'outdir': out_real}
        # E3 receipt
        rp = os.path.join(call_real, L['receipt'])
        sp = os.path.join(call_real, L['spec'])
        if not os.path.isfile(rp) or os.path.islink(rp):
            raise CallRefused('E3 NO_RECEIPT')
        if not os.path.isfile(sp) or os.path.islink(sp):
            raise CallRefused('E3 NO_SPEC')
        spec_sha = sha256_file(sp)
        v = self.M.verify_receipt(rp, spec_sha256=spec_sha, driver_sha256=self.driver['sha256'])
        if not v['ok']:
            raise CallRefused('E3 RECEIPT_UNVERIFIED %s' % v['reasons'])
        r = v['receipt']
        if r.get('status') != 'FINISHED' or r.get('exit_code') != 0 or r.get('stop_reason') is not None:
            raise CallRefused('E3 RECEIPT_NOT_FINISHED_EXIT0 status=%r exit=%r stop=%r'
                              % (r.get('status'), r.get('exit_code'), r.get('stop_reason')))
        res_pin = r.get('result') or {}
        res_path = os.path.join(out_real, 'result.json')
        if os.path.realpath(str(res_pin.get('path', ''))) != res_path:
            raise CallRefused('E3 RECEIPT_RESULT_PATH %r is not %s' % (res_pin.get('path'), res_path))
        res_sha = sha256_file(res_path)
        if res_sha != res_pin.get('sha256'):
            raise CallRefused('E3 RESULT_SHA_MISMATCH')
        fin = json.loads(Path(out_real, 'finish.json').read_bytes().decode('utf-8'))
        if fin.get('result_sha256') != res_sha:
            raise CallRefused('E3 FINISH_RESULT_SHA_MISMATCH')
        ds = r.get('driver_status')
        facts.update(receipt={'path': rp, 'file_sha256': sha256_file(rp), 'receipt_sha256_self': r.get('receipt_sha256'),
                              'status': r.get('status'), 'exit_code': r.get('exit_code'), 'driver_status': ds},
                     result={'path': res_path, 'sha256': res_sha}, spec_sha256=spec_sha,
                     monitor_pin_in_receipt=(r.get('pins') or {}).get('monitor'))
        # E4 wave ingested + cache entry
        if not os.path.isfile(os.path.join(wave_dir, L['wave_result'])):
            raise CallRefused('E4 WAVE_NOT_INGESTED (no %s)' % L['wave_result'])
        hits = []
        for p, e, cid, hdr in self.entries():
            pv = e.get('provenance') or {}
            cd = pv.get('call_dir')
            if cd is not None and (cd == call_dir or os.path.realpath(cd) == call_real):
                hits.append((p, e, cid, hdr))
        if len(hits) != 1:
            raise CallRefused('E4 CACHE_ENTRIES_FOR_CALL = %d (need exactly 1)' % len(hits))
        ep, e, cid, hdr = hits[0]
        pv = e.get('provenance') or {}
        if e.get('source') != 'WAVE':
            raise CallRefused('E4 cache entry source %r is not WAVE' % e.get('source'))
        if pv.get('result_sha256') != res_sha or os.path.realpath(str(pv.get('result_path'))) != res_path:
            raise CallRefused('E4 CACHE_ENTRY_NOT_BOUND_TO_RESULT')
        if pv.get('spec_sha256') != spec_sha:
            raise CallRefused('E4 CACHE_ENTRY_SPEC_SHA_MISMATCH')
        if hdr.get('driver_sha256') != self.driver['sha256']:
            raise CallRefused('E4 CACHE_HEADER_DRIVER_MISMATCH')
        cls = e.get('classification')
        if cls in VALID_CLASSES:
            if ds != 'COMPLETED':
                raise CallRefused('E3 VALID entry but driver_status %r' % ds)
        elif cls in MODEL_INVALID_CLASSES:
            if not self.include_model_invalid:
                raise CallRefused('E4 NOT_VALID_CLASS %s (failures preserved; --include-model-invalid to override)' % cls)
        else:
            raise CallRefused('E4 classification %r is not final' % cls)
        ov = self.orch_verify(call_dir, ep, cid, hdr)
        if not ov['ok']:
            raise CallRefused('E4 ORCHESTRATOR_VERIFICATION_FAILED %s' % ov['reasons'])
        facts.update(cache_entry={'path': ep, 'file_sha256': ov['entry_file_sha256'], 'entry_sha256': e.get('entry_sha256'),
                                  'key': e.get('key'), 'cache_id': cid, 'classification': cls,
                                  'failure_class': e.get('failure_class')},
                     evidence_files=sorted((pv.get('evidence_files') or {}).keys()))
        # E8 no spec or wave plan in the work dir names this call (e.g. a driver 'admit' block, c2v006 L744-769)
        for p, text in self.spec_texts():
            if p == os.path.join(call_real, L['spec']):
                continue
            if call_real in text or call_dir in text:
                raise CallRefused('E8 REFERENCED_BY %s' % p)
        # E5 live processes
        refs = live_refs(call_dir, call_real)
        if refs is None:
            raise CallRefused('E5 PROCESS_TABLE_UNREADABLE')
        if refs:
            raise CallRefused('E5 LIVE_PROCESS_REFERENCES %s' % [x['pid'] for x in refs])
        lp = os.path.join(call_real, L['launch'])
        if os.path.isfile(lp):
            try:
                cp = json.loads(Path(lp).read_bytes().decode('utf-8')).get('child_pid')
            except Exception:
                raise CallRefused('E5 LAUNCH_RECORD_UNREADABLE')
            if cp is not None and pid_alive(cp):
                raise CallRefused('E5 LAUNCH_CHILD_PID_ALIVE %s' % cp)
        if self.use_lsof:
            lr = lsof_refs(call_real, self.lsof_timeout_s)
            if lr is None:
                raise CallRefused('E5 LSOF_FAILED')
            if lr:
                raise CallRefused('E5 OPEN_FILES_BY_PIDS %s' % lr)
        # E6
        facts['recompute_pins'] = self.recompute_pins(call_real, spec_sha)
        return facts

    # ---------------------------------------------------------------- tree facts (E7)
    def tree(self, call_real, facts, hash_files):
        L = self.layout
        files, links, specials = inventory(call_real, L['retention_dir'])
        if links:
            raise CallRefused('E7 SYMLINKS_PRESENT %s' % links[:5])
        if specials:
            raise CallRefused('E7 SPECIAL_FILES_PRESENT %s' % specials[:5])
        evidence = set(os.path.realpath(p) for p in facts.get('evidence_files') or [])
        rows = []
        for rel in sorted(files):
            st = files[rel]
            parts = safe_parts(rel)
            rule = None
            if parts[0] == L['outdir'] and len(parts) > 1:
                rule = match_rule('/'.join(parts[1:]), self.categories)
            if rule and os.path.join(call_real, rel) in evidence:
                raise CallRefused('E7 WHITELIST_HITS_EVIDENCE_FILE %s' % rel)
            row = {'relpath': rel, 'size': st.st_size, 'ino': st.st_ino, 'dev': st.st_dev, 'nlink': st.st_nlink,
                   'rule': rule, 'removable': bool(rule) and st.st_nlink == 1,
                   'kept_reason': (None if rule is None or st.st_nlink == 1 else 'HARDLINKED_NLINK_%d' % st.st_nlink)}
            if hash_files:
                row['sha256'] = sha256_file(os.path.join(call_real, rel))
            rows.append(row)
        return rows


# ------------------------------------------------------------------------------------------------ per-call operations
def retention_paths(env, call_real):
    rd = os.path.join(call_real, env.layout['retention_dir'])
    return rd, os.path.join(rd, 'MANIFEST_PRE_RETENTION.json'), os.path.join(rd, 'RETENTION_RECORD.json')


def state_of(env, call_real):
    rd, mp, rp = retention_paths(env, call_real)
    if os.path.lexists(rd) and (os.path.islink(rd) or not os.path.isdir(rd)):
        return 'RETENTION_DIR_NOT_PLAIN'
    if not os.path.lexists(mp):
        return 'RECORD_WITHOUT_MANIFEST' if os.path.lexists(rp) else 'FRESH'
    return 'RETAINED' if os.path.lexists(rp) else 'PARTIAL'


def load_manifest(env, call_real):
    _, mp, _ = retention_paths(env, call_real)
    raw = Path(mp).read_bytes()
    try:
        m = json.loads(raw.decode('utf-8'))
    except Exception:
        raise CallRefused('MANIFEST_UNREADABLE')
    if m.get('schema') != SCHEMA_MANIFEST or not check_self_hash(m, 'manifest_sha256'):
        raise CallRefused('MANIFEST_SELF_HASH_OR_SCHEMA_INVALID')
    if m.get('call_dir_real') != call_real:
        raise CallRefused('MANIFEST_BELONGS_TO_ANOTHER_CALL')
    return m, sha256_bytes(raw)


def plan_call(env, call_dir):
    """Dry evaluation of one call (no writes, no full hashing)."""
    out = {'call_dir': call_dir}
    try:
        call_real = os.path.realpath(call_dir)
        st = state_of(env, call_real) if os.path.isdir(call_real) else 'MISSING'
        out['state'] = st
        if st == 'RETAINED':
            m, _ = load_manifest(env, call_real)
            out.update(eligible=False, reasons=['ALREADY_RETAINED'])
            return out
        if st not in ('FRESH', 'PARTIAL'):
            raise CallRefused('STATE_%s' % st)
        facts = env.eligibility(call_dir)
        rows = env.tree(call_real, facts, hash_files=False)
        if st == 'PARTIAL':
            m, _ = load_manifest(env, call_real)
            present = {r['relpath'] for r in rows}
            rem = [f for f in m['files'] if f['removable']]
            out['partial'] = {'manifest_removable': len(rem), 'already_removed': sum(1 for f in rem if f['relpath'] not in present)}
            rows = [r for r in rows if r['removable']]
        byrule = {}
        for r in rows:
            if r['removable']:
                b = byrule.setdefault(r['rule'], [0, 0])
                b[0] += 1
                b[1] += r['size']
        out.update(eligible=True, reasons=[], classification=facts['cache_entry']['classification'],
                   removable_files=sum(v[0] for v in byrule.values()),
                   removable_bytes=sum(v[1] for v in byrule.values()),
                   by_rule={k: {'files': v[0], 'bytes': v[1]} for k, v in sorted(byrule.items())},
                   hardlinked_kept=[r['relpath'] for r in rows if r.get('kept_reason')],
                   total_files=len(rows), total_bytes=sum(r['size'] for r in rows))
    except CallRefused as exc:
        out.update(eligible=False, reasons=[str(exc)])
    except Exception as exc:
        out.update(eligible=False, reasons=['ERROR %s: %s' % (type(exc).__name__, exc)])
    return out


def _post_verify(env, call_real, manifest, call_dir):
    """Kept files re-hashed against the manifest; removable files absent; no unexpected file; orchestrator checks."""
    L = env.layout
    files, links, specials = inventory(call_real, L['retention_dir'])
    if links or specials:
        raise CallRefused('POST symlink/special file appeared')
    man = {f['relpath']: f for f in manifest['files']}
    extra = sorted(set(files) - set(man))
    if extra:
        raise CallRefused('POST UNEXPECTED_FILES %s' % extra[:5])
    n_kept = 0
    for rel, f in man.items():
        if f['removable']:
            if rel in files:
                raise CallRefused('POST REMOVABLE_STILL_PRESENT %s' % rel)
            continue
        if rel not in files:
            raise CallRefused('POST KEPT_FILE_MISSING %s' % rel)
        if files[rel].st_size != f['size'] or sha256_file(os.path.join(call_real, rel)) != f['sha256']:
            raise CallRefused('POST KEPT_FILE_CHANGED %s' % rel)
        n_kept += 1
    facts = env.eligibility(call_dir)          # E1-E6 again, incl. receipt/cache/classify with the orchestrator's code
    if facts['result']['sha256'] != manifest['pins']['result']['sha256'] or \
            facts['receipt']['file_sha256'] != manifest['pins']['receipt']['file_sha256'] or \
            facts['cache_entry']['file_sha256'] != manifest['pins']['cache_entry']['file_sha256']:
        raise CallRefused('POST receipt/result/cache-entry bytes differ from the manifest pins')
    return {'kept_files_rehashed': n_kept, 'receipt_verify_ok': True, 'orchestrator_cache_verify_ok': True,
            'orchestrator_classify_identical': True, 'recompute_pins': facts['recompute_pins']}


def apply_call(env, call_dir, auth, crash=None):
    """Retain one call.  crash: TESTS ONLY, {'after_removals': n} | {'stage': 'after_manifest'|'before_record'}."""
    call_real = os.path.realpath(call_dir)
    st = state_of(env, call_real)
    if st == 'RETAINED':
        return {'call_dir': call_dir, 'status': 'ALREADY_RETAINED'}
    if st not in ('FRESH', 'PARTIAL'):
        raise CallRefused('STATE_%s' % st)
    facts = env.eligibility(call_dir)
    rd, mp, rp = retention_paths(env, call_real)
    os.makedirs(rd, exist_ok=True)
    if os.path.islink(rd):
        raise CallRefused('RETENTION_DIR_IS_SYMLINK')
    lockfd = os.open(os.path.join(rd, '.lock'), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o644)
    try:
        try:
            fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise CallRefused('CALL_LOCKED_BY_ANOTHER_SWEEPER')
        st = state_of(env, call_real)
        append_jsonl(os.path.join(rd, 'ATTEMPTS.jsonl'), {'utc': utc(), 'pid': os.getpid(), 'state_at_start': st,
                                                          'tool_sha256': self_sha256()})
        t_start = utc()
        if st == 'FRESH':
            rows = env.tree(call_real, facts, hash_files=True)
            man = {'schema': SCHEMA_MANIFEST, 'tool': {'name': TOOL_NAME, 'path': os.path.realpath(__file__),
                                                       'sha256': self_sha256()},
                   'utc': t_start, 'authorization': auth, 'call_dir': call_dir, 'call_dir_real': call_real,
                   'work_dir': env.work_dir, 'outdir': facts['outdir'],
                   'whitelist': {'sha256': whitelist_sha256(), 'rules': list(WHITELIST), 'categories': list(env.categories)},
                   'layout': env.layout,
                   'pins': {'spec': facts['recompute_pins']['spec'], 'driver': env.driver, 'monitor': env.monitor_pin,
                            'monitor_in_receipt': facts['monitor_pin_in_receipt'],
                            'orchestrator': dict(env.orch_pin, module=env.adapter['module_name']),
                            'orchestrator_config': {'path': env.orch_config_path, 'sha256': env.orch_config_sha256},
                            'python': env.cfg.get('python'), 'coefficients': facts['recompute_pins']['coefficients'],
                            'static_pins_sha256': facts['recompute_pins']['static_pins_sha256'],
                            'static_pins_checked': facts['recompute_pins']['static_pins_checked'],
                            'receipt': facts['receipt'], 'result': facts['result'], 'cache_entry': facts['cache_entry']},
                   'files': rows,
                   'totals': {'n_files': len(rows), 'bytes': sum(r['size'] for r in rows),
                              'n_removable': sum(1 for r in rows if r['removable']),
                              'removable_bytes': sum(r['size'] for r in rows if r['removable'])}}
            man = with_self_hash(man, 'manifest_sha256')
            mfile_sha = write_json_new(mp, man)
            m2, mfile_sha2 = load_manifest(env, call_real)       # re-read verification
            if mfile_sha2 != mfile_sha or m2 != man:
                raise CallRefused('MANIFEST_REREAD_MISMATCH')
            if crash and crash.get('stage') == 'after_manifest':
                raise _InjectedCrash('after_manifest')
        else:
            man, mfile_sha = load_manifest(env, call_real)
            if man['whitelist']['sha256'] != whitelist_sha256():
                raise CallRefused('PARTIAL: whitelist changed since the manifest')
            # consistency of the partial state with the manifest
            files, links, specials = inventory(call_real, env.layout['retention_dir'])
            if links or specials:
                raise CallRefused('PARTIAL: symlink/special file present')
            mf = {f['relpath']: f for f in man['files']}
            extra = sorted(set(files) - set(mf))
            if extra:
                raise CallRefused('PARTIAL: UNEXPECTED_FILES %s' % extra[:5])
            for rel, f in mf.items():
                if rel not in files:
                    if not f['removable']:
                        raise CallRefused('PARTIAL: KEPT_FILE_MISSING %s' % rel)
                    continue
                s = files[rel]
                if s.st_size != f['size'] or s.st_ino != f['ino']:
                    raise CallRefused('PARTIAL: FILE_CHANGED %s' % rel)
                if not f['removable'] and sha256_file(os.path.join(call_real, rel)) != f['sha256']:
                    raise CallRefused('PARTIAL: KEPT_FILE_CHANGED %s' % rel)
        # removal
        removed_now, absent_before = [], []
        n = 0
        for f in man['files']:
            if not f['removable']:
                continue
            what = unlink_checked(call_real, f['relpath'], f['ino'], f['size'])
            (removed_now if what == 'REMOVED' else absent_before).append(f['relpath'])
            n += 1
            if crash and crash.get('after_removals') is not None and len(removed_now) >= crash['after_removals']:
                raise _InjectedCrash('after_removals')
        if crash and crash.get('stage') == 'before_record':
            raise _InjectedCrash('before_record')
        post = _post_verify(env, call_real, man, call_dir)
        rem = [f for f in man['files'] if f['removable']]
        byrule = {}
        for f in rem:
            b = byrule.setdefault(f['rule'], {'files': 0, 'bytes': 0})
            b['files'] += 1
            b['bytes'] += f['size']
        now = set(removed_now)
        rec = {'schema': SCHEMA_RECORD, 'tool': man['tool'], 'call_dir': call_dir, 'call_dir_real': call_real,
               'utc_manifest': man['utc'], 'utc_start_this_attempt': t_start, 'utc_end': utc(),
               'authorization': auth, 'authorization_at_manifest': man['authorization'],
               'manifest': {'path': mp, 'file_sha256': mfile_sha, 'manifest_sha256': man['manifest_sha256']},
               'removed': [{'relpath': f['relpath'], 'size': f['size'], 'sha256': f['sha256'], 'rule': f['rule'],
                            'removed_in': 'this_attempt' if f['relpath'] in now else 'earlier_attempt'} for f in rem],
               'kept_hardlinked': [f['relpath'] for f in man['files'] if f.get('kept_reason')],
               'bytes_freed': sum(f['size'] for f in rem), 'by_rule': byrule,
               'n_removed_this_attempt': len(removed_now), 'n_removed_earlier_attempts': len(absent_before),
               'post_verification': post,
               'reproducibility': {'spec': man['pins']['spec'], 'driver': man['pins']['driver'],
                                   'static_pins_sha256': man['pins']['static_pins_sha256'],
                                   'note': 'removed bytes are recomputable only by re-running the pinned driver on '
                                           'spec.json; removed .npy blob names are their sha256 and the kept '
                                           'checkpoint iteration records pin them'}}
        rec = with_self_hash(rec, 'record_sha256')
        rfile_sha = write_json_new(rp, rec)
        back = json.loads(Path(rp).read_bytes().decode('utf-8'))
        if not check_self_hash(back, 'record_sha256') or back != rec:
            raise CallRefused('RECORD_REREAD_MISMATCH')
        return {'call_dir': call_dir, 'status': 'RETAINED', 'bytes_freed': rec['bytes_freed'],
                'n_removed': len(rem), 'record_file_sha256': rfile_sha, 'manifest_file_sha256': mfile_sha,
                'post_verification': {k: v for k, v in post.items() if k != 'recompute_pins'}}
    finally:
        os.close(lockfd)


def verify_retained(env, call_dir):
    call_real = os.path.realpath(call_dir)
    if state_of(env, call_real) != 'RETAINED':
        raise CallRefused('NOT_RETAINED')
    man, msha = load_manifest(env, call_real)
    _, _, rp = retention_paths(env, call_real)
    rec = json.loads(Path(rp).read_bytes().decode('utf-8'))
    if rec.get('schema') != SCHEMA_RECORD or not check_self_hash(rec, 'record_sha256'):
        raise CallRefused('RECORD_SELF_HASH_INVALID')
    if rec['manifest']['file_sha256'] != msha:
        raise CallRefused('RECORD_NOT_BOUND_TO_MANIFEST')
    post = _post_verify(env, call_real, man, call_dir)
    return {'call_dir': call_dir, 'status': 'RETAINED_VERIFIED', 'bytes_freed': rec['bytes_freed'],
            'kept_files_rehashed': post['kept_files_rehashed']}


# ------------------------------------------------------------------------------------------------ authorization
def check_authorization(line, instructions_path):
    if line != AUTH_HEADING:
        raise Refused('AUTHORIZATION_LINE_MISMATCH: --authorization must be exactly %r' % AUTH_HEADING)
    raw = Path(instructions_path).read_bytes()
    lines = raw.decode('utf-8').splitlines()
    if AUTH_HEADING not in lines:
        raise Refused('AUTHORIZATION_NOT_FOUND in %s' % instructions_path)
    return {'heading': AUTH_HEADING, 'instructions_path': os.path.abspath(instructions_path),
            'instructions_sha256': sha256_bytes(raw), 'checked_utc': utc(),
            'scope': 'calibration forward calls under the calibration orchestrator work dir; completed and verified; '
                     'intermediates only (route-A checkpoint blobs, node diagnostics, stage arrays)'}


# ------------------------------------------------------------------------------------------------ estimate (read-only)
def estimate(outdir, free_gb, wave_sizes, categories=CATEGORIES):
    files, links, specials = inventory(os.path.realpath(outdir), '\x00none')
    byrule, total = {}, 0
    for rel, st in files.items():
        total += st.st_size
        r = match_rule(rel, categories)
        if r:
            b = byrule.setdefault(r, {'files': 0, 'bytes': 0})
            b['files'] += 1
            b['bytes'] += st.st_size
    freed = sum(v['bytes'] for v in byrule.values())
    bycat = {}
    for w in WHITELIST:
        if w['id'] in byrule:
            c = bycat.setdefault(w['category'], {'files': 0, 'bytes': 0})
            c['files'] += byrule[w['id']]['files']
            c['bytes'] += byrule[w['id']]['bytes']
    resid = total - freed
    free = int(free_gb * 1e9)
    reserve = 20 * 2 ** 30
    cap = 8 * 2 ** 30
    aff = {'no_retention_calls': free // total if total else None,
           'retention_calls_simple': free // resid if resid else None}
    rows = []
    for w in wave_sizes:
        avail = free - reserve - w * total
        space = (avail // resid + w) if avail > 0 else 0
        gavail = free - reserve - w * cap
        guard = (gavail // resid + w) if gavail >= 0 else 0
        rows.append({'wave_size': w, 'calls_affordable_space_only': space,
                     'calls_before_v001_disk_guard_blocks': guard,
                     'calls_affordable_binding': min(space, guard),
                     'v001_disk_guard_needs_free_bytes': w * cap + reserve,
                     'v001_disk_guard_passes_at_free': free >= w * cap + reserve})
    return {'outdir': os.path.abspath(outdir), 'symlinks': links, 'specials': specials, 'n_files': len(files),
            'total_bytes': total, 'removable_bytes': freed, 'residual_bytes': resid,
            'removable_fraction': (freed / total) if total else None, 'by_rule': dict(sorted(byrule.items())),
            'by_category': bycat, 'free_bytes_assumed': free, 'reserve_bytes_v001_config': reserve,
            'output_cap_bytes_v001_config': cap, 'affordable': aff, 'by_wave_size': rows}


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--orch-config')
    ap.add_argument('--orchestrator')
    ap.add_argument('--orchestrator-sha256')
    ap.add_argument('--call', action='append', default=[])
    ap.add_argument('--runs-dir', action='append', default=[])
    ap.add_argument('--layout')
    ap.add_argument('--categories', default=','.join(CATEGORIES))
    ap.add_argument('--include-model-invalid', action='store_true')
    ap.add_argument('--no-lsof', action='store_true')
    ap.add_argument('--lsof-timeout-s', type=float, default=300.0)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--authorization')
    ap.add_argument('--instructions', default=DEFAULT_INSTRUCTIONS)
    ap.add_argument('--verify-retained', action='store_true')
    ap.add_argument('--estimate-from')
    ap.add_argument('--free-gb', type=float, default=233.0)
    ap.add_argument('--wave-sizes', default='6,12,24')
    a = ap.parse_args(argv)
    try:
        if a.estimate_from:
            out = estimate(a.estimate_from, a.free_gb, [int(x) for x in a.wave_sizes.split(',') if x],
                           tuple(x for x in a.categories.split(',') if x))
            out['status'] = 'OK'
            print(json.dumps(out, indent=1, sort_keys=True))
            return 0
        if not (a.orch_config and a.orchestrator and a.orchestrator_sha256):
            raise Refused('--orch-config, --orchestrator and --orchestrator-sha256 are required')
        auth = None
        if a.apply:
            if a.verify_retained:
                raise Refused('--apply and --verify-retained are exclusive')
            if not a.authorization:
                raise Refused('--apply requires --authorization "%s"' % AUTH_HEADING)
            auth = check_authorization(a.authorization, a.instructions)
        elif a.authorization:
            raise Refused('--authorization without --apply (plan mode never removes anything)')
        env = Env(orch_config=a.orch_config, orchestrator=a.orchestrator, orchestrator_sha256=a.orchestrator_sha256,
                  runs_dirs=a.runs_dir, layout=a.layout, categories=tuple(x for x in a.categories.split(',') if x),
                  include_model_invalid=a.include_model_invalid, use_lsof=not a.no_lsof, lsof_timeout_s=a.lsof_timeout_s)
        calls = a.call or env.call_dirs()
        mode = 'apply' if a.apply else ('verify' if a.verify_retained else 'plan')
        results, errors = [], 0
        for c in calls:
            if mode == 'plan':
                results.append(plan_call(env, c))
                continue
            try:
                if mode == 'verify':
                    results.append(verify_retained(env, c))
                else:
                    p = plan_call(env, c)
                    if not p.get('eligible'):
                        results.append(dict(p, status='SKIPPED_NOT_ELIGIBLE'))
                        continue
                    results.append(apply_call(env, c, auth))
            except CallRefused as exc:
                errors += 1
                results.append({'call_dir': c, 'status': 'CALL_ERROR', 'reasons': [str(exc)]})
        summary = {'schema': SCHEMA_PLAN, 'mode': mode, 'utc': utc(), 'tool_sha256': self_sha256(),
                   'orch_config_sha256': env.orch_config_sha256, 'work_dir': env.work_dir,
                   'whitelist_sha256': whitelist_sha256(), 'categories': list(env.categories),
                   'n_calls': len(calls), 'calls': results,
                   'n_eligible': sum(1 for r in results if r.get('eligible')),
                   'eligible_removable_bytes': sum(r.get('removable_bytes', 0) for r in results if r.get('eligible')),
                   'bytes_freed': sum(r.get('bytes_freed', 0) for r in results if r.get('status') == 'RETAINED'),
                   'authorization': auth, 'status': 'CALL_ERRORS' if errors else 'OK'}
        print(json.dumps(summary, indent=1, sort_keys=True, default=str))
        return EXIT[summary['status']]
    except Refused as exc:
        print(json.dumps({'status': 'REFUSED', 'reasons': [str(exc)]}, indent=1))
        return EXIT['REFUSED']


if __name__ == '__main__':
    sys.exit(main())
