"""calibration_orchestrator_c2v002 -- DDO154 calibration orchestrator (Claude2 lane); successor of c2v001 (51895c04).

What it connects (all loaded from pinned bytes):
  * the calibration engine calibration_region_engine_c2v003a (193841fa) and the freeze module prediction_freeze_c2v003a
    (5ee3e5dc), pinned by the coordinate spec DDO154_CALIBRATION_COORDINATE_SPEC_V001.json (unchanged, fdeb5eb9);
  * the forward driver named in the config (target: the generalized driver galaxy_m0_forward_c2v006, c53997b4, which
    has no route-A iteration-4 lock), run through the pinned root monitor (ba031c23) and campaign launcher (71274ceb);
  * FAILURE_TAXONOMY_V001.json (pinned): the rule table that classifies every terminal call outcome.

Algorithm: unchanged from c2v001 (PROBE -> WAVE -> INGEST -> repeat; REPLAY twice with zero uncached calls; calibration
record).  The probe, its STOP sentinel and the sibling budget guard are c2v001 verbatim (see c2v001 docstring and
CHECK_V001 sections 2-3).

Changes in c2v002 (dispatch items 1-9; CHECK_V001 F1-F6; ROOT_DECISIONS A7):
  1. BASE SPEC = the anchor template spec with the numerics block from the config (pinned to the convergence verdict
     artifact); theta changes ONLY label + physical.{common_scale_s, gamma, ell_F_m, distance_Mpc} relative to the base.
     Every generated spec passes the pinned driver's own normalize_spec before launch, and its normalized form may differ
     from the normalized base only in those fields.  DRIVER CAPABILITY GATE: the trial point and all 16 box corners
     must be accepted; otherwise 'run' refuses (c2v006 refuses DDO154 distance != 4.04, see LAUNCH_V002.md).
  2. DECIDING GATE: 'run' refuses unless the config pins a deciding result of THIS driver whose bytes pass:
     result sha256 == pin; finish.result_sha256 == sha256(result bytes); result.driver_sha256 == config driver sha;
     result.call_spec_sha256 == pinned deciding spec sha; result.status == COMPLETED;
     result.deciding_test.verdict == PASS_BITWISE_EQUAL.
     NUMERICS GATE: the numerics block must be pinned to a verdict artifact (path+sha256 from bytes) and either equal
     the JSON at a declared pointer inside it, or carry a root attestation string.
  3. A7 GUARDS (fail-closed, every spec before launch): every key of every *_overrides dict (and of the nested pass
     tables of le_factor_overrides) fullmatches 0|[1-9][0-9]*; every path in the spec, the work dir, the campaign dir
     and therefore every call outdir is absolute.
  4. FAILURE TAXONOMY (fixes F1): VALID | MODEL_INVALID (cached, final) | NUMERICS_LIMITED (not cached, HALT) |
     INFRA (not cached, HALT), from (status, reasons, route-A attempt end-record outcome, stage records); default INFRA.
     resolve --decision invalid | retry | retry_with_recovery (the last records a pre-declared, config-allowlisted
     bracket recovery rule {path, sha256}; the relaunch of that theta uses its brackets block; nothing is automatic).
  5. F2: cache entries of launched calls are re-derived from result.json bytes (and evidence-file hashes) on every open.
     F3: ledger lines count only for waves whose plan was committed (atomic link); planless wave dirs are skipped;
     the calibration record name is deterministic (run sha) and an existing record is verified and reused.
     F4: orphan detection also scans live processes for the call directory (monitors that died before launch.json);
     resolve retry refuses while any live process references the call directory.
     F5/F6: coordinate-spec addendum (pinned) carried into plan/summary (D5 deciding test, D14/D19/D10 items, D3 open,
     side_bound_calls 11, NGC placeholder wording).
  6. column_workers, max_concurrent, n_cores are config fields; max_concurrent x column_workers <= min(n_cores, 12)
     (12 = the pinned campaign launcher's limit, campaign_c2v001 L84, L110-111).  column_workers enters the cache id
     (column-worker invariance of result rows is UNTESTED, see TIMING_MODEL_V001.json).
  7. Disk forecast in 'plan' and 'status'; HALTED_DISK unchanged; the orchestrator never deletes anything.

CLI:
  calibration_orchestrator_c2v002.py plan    --config CONFIG.json
  calibration_orchestrator_c2v002.py run     --config CONFIG.json [--max-waves N]
  calibration_orchestrator_c2v002.py resolve --config CONFIG.json --wave W (--key PREFIX | --all)
                                             --decision invalid|retry|retry_with_recovery [--recovery PATH] --reason TEXT
  calibration_orchestrator_c2v002.py status  --config CONFIG.json
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
import hashlib
import importlib.util
import json
import math
import re
import shutil
import socket
import subprocess
import sys
import time
import types
from pathlib import Path

MODULE_NAME = 'calibration_orchestrator_c2v002'
SCHEMA_CONFIG = 'DDO154_CALIBRATION_ORCHESTRATOR_CONFIG_C2V002'
SCHEMA_SPEC = 'DDO154_CALIBRATION_COORDINATE_SPEC_C2V001'
SCHEMA_ADDENDUM = 'DDO154_CALIBRATION_COORDINATE_SPEC_ADDENDUM_C2V002'
SCHEMA_TAXONOMY = 'DDO154_CALIBRATION_FAILURE_TAXONOMY_V001'
SCHEMA_THETA_KEY = 'DDO154_CALIBRATION_THETA_KEY_C2V001'          # unchanged: theta keys are comparable with c2v001
SCHEMA_CACHE_ID = 'DDO154_CALIBRATION_CACHE_ID_C2V002'
SCHEMA_CACHE_ENTRY = 'DDO154_CALIBRATION_CACHE_ENTRY_C2V002'
SCHEMA_WAVE_PLAN = 'DDO154_CALIBRATION_WAVE_PLAN_C2V002'
SCHEMA_WAVE_RESULT = 'DDO154_CALIBRATION_WAVE_RESULT_C2V002'
SCHEMA_SUMMARY = 'DDO154_CALIBRATION_ORCHESTRATION_SUMMARY_C2V002'
SPEC_MAPPING_ID = 'C2V001_PHYS4_GAMMA_EQ_GE_TIMES_EREF'           # the coordinate spec's mapping (theta -> physical)
MAPPING_ID = 'C2V002_BASE_TEMPLATE_PLUS_NUMERICS_PHYS4'           # c2v002: base spec = template + config numerics
ANCHOR_ALIAS_RTOL = 1e-14
DECLARED_CHANGED_PATHS = ('label', 'physical.common_scale_s', 'physical.gamma', 'physical.ell_F_m',
                          'physical.distance_Mpc')
VARYING_EXPECTED = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'distance_Mpc')
FIXED_TEMPLATE_CHECKS = (('Eref_J', 'Eref_base_J'), ('entropy_K_factor', 'entropy_K_factor'))
REQUIRED_VERDICT = 'PASS_BITWISE_EQUAL'
CAMPAIGN_PROCESS_LIMIT = 12          # campaign_c2v001 L84 (max_concurrent 1..12) and L110-111 (mc x workers <= 12)
OVERRIDE_KEY_RE = re.compile('0|[1-9][0-9]*')
CLASSES = ('VALID', 'MODEL_INVALID', 'NUMERICS_LIMITED', 'INFRA')
CACHED_CLASSES = ('VALID', 'MODEL_INVALID')
HALT_CLASSES = ('NUMERICS_LIMITED', 'INFRA')
DECISIONS = ('invalid', 'retry', 'retry_with_recovery')
PLACEHOLDER_REASON = 'ORCHESTRATOR_PROBE_PLACEHOLDER_NOT_AN_EVALUATION'
SINGLE_FAMILIES = ('seed', 'repair')
COLUMN_WORKERS_INVARIANCE = ('UNTESTED: column_workers changes only how fs/rfs columns are grouped into runs '
                             '(driver c2v006 L1782-1828); every column is solved independently and the rotation stage '
                             'assembles columns by radial index (rotation v001 L210-218).  Deciding test: one real DDO154 '
                             'call at 2 and at N column workers, result rows compared bitwise.  Until then '
                             'column_workers is part of the cache id.')
EXIT = {'COMPLETE': 0, 'OK': 0, 'REFUSED': 3, 'HALTED_INFRA': 4, 'HALTED_DISK': 5, 'MAX_WAVES': 6,
        'HALTED_UNRESOLVED': 7, 'LOCKED': 8, 'REPLAY_FAILED': 9, 'ORPHANS_STILL_RUNNING': 10, 'HALTED_NUMERICS': 11,
        'RECORD_UNVERIFIED': 12}
CONFIG_KEYS = {'schema', 'synthetic_test', 'work_dir', 'coordinate_spec', 'coordinate_spec_addendum',
               'observation_region', 'numerics', 'column_workers', 'max_concurrent', 'n_cores', 'ngc3198_slots',
               'anchor', 'driver', 'deciding_test', 'taxonomy', 'recovery_rules', 'monitor', 'campaign', 'python',
               'per_call', 'campaign_wall_cap_s', 'disk_guard', 'orphan_wait', 'engine_parameters_override',
               'executor', 'notes'}


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


def write_json_x(path, obj):
    raw = json_bytes(obj)
    with open(path, 'xb') as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())
    return sha256_bytes(raw)


def write_json_atomic_x(path, obj):
    """F3: exclusive temp file + hard link into place (atomic, never overwrites); the temp name is the orchestrator's
    own file and is unlinked after the link."""
    path = Path(path)
    tmp = path.with_name('.%s.%d.%d.tmp' % (path.name, os.getpid(), time.time_ns()))
    s = write_json_x(tmp, obj)
    os.link(tmp, path)
    os.unlink(tmp)
    return s


def append_jsonl(path, obj):
    line = canonical(obj) + b'\n'
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, line)
        os.fsync(fd)
    finally:
        os.close(fd)


def read_jsonl(path):
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, 'rb') as fh:
        for ln in fh.read().split(b'\n'):
            if ln.strip():
                out.append(json.loads(ln.decode('utf-8')))
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


# --------------------------------------------------------------------------------------------- A7 guards (item 3)
def lint_override_keys(obj, prefix=''):
    """A7 (F3): every key of every *_overrides dict, and every key of a dict nested in one (le_factor_overrides pass
    tables), must fullmatch 0|[1-9][0-9]*.  Returns the offending dotted paths (empty = clean)."""
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = (prefix + '.' + str(k)) if prefix else str(k)
            if isinstance(k, str) and k.endswith('_overrides'):
                if not isinstance(v, dict):
                    bad.append(p + ' (not an object)')
                    continue
                for k2, v2 in v.items():
                    if not (isinstance(k2, str) and OVERRIDE_KEY_RE.fullmatch(k2)):
                        bad.append('%s[%r]' % (p, k2))
                    if isinstance(v2, dict):
                        for k3 in v2:
                            if not (isinstance(k3, str) and OVERRIDE_KEY_RE.fullmatch(k3)):
                                bad.append('%s[%r][%r]' % (p, k2, k3))
            else:
                bad.extend(lint_override_keys(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            bad.extend(lint_override_keys(v, '%s[%d]' % (prefix, i)))
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


# --------------------------------------------------------------------------------------------- gates (item 2)
def check_deciding(dt, driver_sha256):
    """Deciding gate: the same admissibility checks as kmax_compare_c2v005.v005_admissibility (L184-220), applied to
    the driver of this config, plus a pin of the result bytes and status COMPLETED."""
    out = {'ok': False, 'reasons': [], 'required_verdict': REQUIRED_VERDICT}
    if not isinstance(dt, dict):
        out['reasons'].append('DECIDING_TEST_NOT_PINNED: config deciding_test is absent')
        return out
    res_pin = dt.get('result')
    if not isinstance(res_pin, dict) or not isinstance(res_pin.get('path'), str) or not isinstance(res_pin.get('sha256'), str):
        out['reasons'].append('deciding_test.result {path, sha256} required')
        return out
    fin_path = dt.get('finish_path')
    spec_sha = dt.get('call_spec_sha256')
    if not isinstance(fin_path, str) or not isinstance(spec_sha, str):
        out['reasons'].append('deciding_test.finish_path and deciding_test.call_spec_sha256 required')
        return out
    if dt.get('required_verdict', REQUIRED_VERDICT) != REQUIRED_VERDICT:
        out['reasons'].append('deciding_test.required_verdict must be %s' % REQUIRED_VERDICT)
        return out
    out.update(result_path=res_pin['path'], finish_path=fin_path)
    try:
        rraw = Path(res_pin['path']).read_bytes()
    except OSError as exc:
        out['reasons'].append('deciding result unreadable: %s' % exc)
        return out
    out['result_sha256'] = sha256_bytes(rraw)
    if out['result_sha256'] != res_pin['sha256']:
        out['reasons'].append('deciding result bytes %s differ from the pinned %s' % (out['result_sha256'], res_pin['sha256']))
        return out
    try:
        fin = json.loads(Path(fin_path).read_bytes().decode('utf-8'))
        r = json.loads(rraw.decode('utf-8'))
    except Exception as exc:
        out['reasons'].append('deciding files unreadable: %s: %s' % (type(exc).__name__, exc))
        return out
    out['status'] = r.get('status')
    out['verdict'] = (r.get('deciding_test') or {}).get('verdict')
    if fin.get('result_sha256') != out['result_sha256']:
        out['reasons'].append('finish.json result_sha256 %s != sha256(result.json) %s' % (fin.get('result_sha256'), out['result_sha256']))
    elif r.get('driver_sha256') != driver_sha256:
        out['reasons'].append('deciding driver_sha256 %s is not the config driver %s' % (r.get('driver_sha256'), driver_sha256))
    elif r.get('call_spec_sha256') != spec_sha:
        out['reasons'].append('deciding call_spec_sha256 %s is not the pinned %s' % (r.get('call_spec_sha256'), spec_sha))
    elif r.get('status') != 'COMPLETED':
        out['reasons'].append('deciding result status %r is not COMPLETED' % r.get('status'))
    elif out['verdict'] != REQUIRED_VERDICT:
        out['reasons'].append('deciding_test.verdict %r != %s' % (out['verdict'], REQUIRED_VERDICT))
    else:
        out['ok'] = True
        out['reasons'].append('PASS_BITWISE_EQUAL with the config driver and the pinned spec; finish custody verified')
    return out


def check_numerics(ncfg, template_numerics):
    """Numerics gate: returns (block, gate).  The block is the config block (template numerics only if the config
    names none, which fails the gate)."""
    gate = {'ok': False, 'reasons': []}
    if ncfg is None:
        gate['reasons'].append('NUMERICS_NOT_PINNED: config numerics is null (the template numerics would be used)')
        return copy.deepcopy(template_numerics), gate
    if not isinstance(ncfg, dict) or set(ncfg) - {'block', 'verdict_artifact', 'block_pointer', 'root_attestation', 'note'}:
        raise OrchestratorError('numerics must be {block, verdict_artifact, block_pointer, root_attestation, note}')
    block = ncfg.get('block')
    if not isinstance(block, dict):
        raise OrchestratorError('numerics.block must be the call-spec numerics object')
    block = copy.deepcopy(block)
    gate['block_sha256'] = sha256_bytes(canonical(block))
    art = ncfg.get('verdict_artifact')
    if not isinstance(art, dict):
        gate['reasons'].append('NUMERICS_VERDICT_NOT_PINNED: numerics.verdict_artifact {path, sha256} is absent')
        return block, gate
    try:
        raw = read_pinned(art, 'numerics.verdict_artifact')
    except OrchestratorError as exc:
        gate['reasons'].append(str(exc))
        return block, gate
    gate['verdict_artifact'] = {'path': art['path'], 'sha256': art['sha256']}
    ptr = ncfg.get('block_pointer')
    if ptr is not None:
        try:
            doc = json.loads(raw.decode('utf-8'))
            got = json_pointer(doc, ptr)
        except Exception as exc:
            gate['reasons'].append('numerics.block_pointer: %s' % exc)
            return block, gate
        if canonical(got) != canonical(block):
            gate['reasons'].append('numerics.block differs from the verdict artifact at %s' % ptr)
            return block, gate
        gate['binding'] = 'BLOCK_EQUALS_ARTIFACT_AT_POINTER %s' % ptr
    else:
        att = ncfg.get('root_attestation')
        if not isinstance(att, str) or not att.strip():
            gate['reasons'].append('numerics: neither block_pointer nor root_attestation binds the block to the verdict')
            return block, gate
        gate['binding'] = 'ROOT_ATTESTATION: %s' % att
    gate['ok'] = True
    return block, gate


# --------------------------------------------------------------------------------------------- taxonomy (item 4)
def _tokens_in(msg, tokens):
    found = []
    for t in tokens:
        if re.search(r'(?<![A-Z0-9_])' + re.escape(t) + r'(?![A-Z0-9_])', msg or ''):
            found.append(t)
    return found


class Taxonomy:
    """Rule table of FAILURE_TAXONOMY_V001.json, evaluated on (result.json, evidence of the call directory)."""

    def __init__(self, doc, sha256):
        if not isinstance(doc, dict) or doc.get('schema') != SCHEMA_TAXONOMY:
            raise OrchestratorError('taxonomy schema must be %s' % SCHEMA_TAXONOMY)
        self.doc, self.sha256 = doc, sha256
        ts = doc['token_sets']
        self.col_tokens = dict(ts['COLUMN_NUMERICS_TOKENS']['tokens'])
        self.hi_tokens = dict(ts['HI_NUMERICS_TOKENS']['tokens'])
        self.nonfinite = dict(ts['ROUTE_A_WORKER_NONFINITE_MESSAGES']['messages'])
        self.rules = list(doc['rules'])
        if doc['default']['class'] != 'INFRA':
            raise OrchestratorError('taxonomy default class must be INFRA')
        for r in self.rules:
            if r['class'] not in CLASSES or r['condition'] not in self.CONDITIONS:
                raise OrchestratorError('taxonomy rule %s: unknown class or condition' % r.get('id'))

    # -- condition helpers: each returns (matched, fill, judgment_override)
    def _col_tokens_ok(self, msgs):
        toks = []
        for m in msgs:
            t = _tokens_in(m, self.col_tokens)
            if not t:
                return None
            toks.append(t[0])
        return toks or None

    def _hi_tokens_ok(self, msgs):
        toks = []
        for m in msgs:
            t = _tokens_in(m, self.hi_tokens)
            if not t:
                return None
            toks.append(t[0])
        return toks or None

    def _col_judgment(self, toks):
        return any(not self.col_tokens[t].get('root_specified') for t in toks)

    def c_always(self, res, ev):
        return True, '', None

    def c_valid_true_rows_finite(self, res, ev):
        sp = res.get('speeds_km_s')
        if res.get('valid') is not True or not isinstance(sp, dict):
            return False, '', None
        rows = [sp.get(r) for r in ev['row_ids']]
        ok = all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in rows)
        return ok, '', None

    def _ra(self, ev):
        return ev.get('route_a') or {}

    def c_route_a_end_iteration_budget_exhausted(self, res, ev):
        ra = self._ra(ev)
        mx = ra.get('max_iterations')
        ok = (ra.get('end_outcomes') == ['ITERATION_BUDGET_EXHAUSTED'] and isinstance(mx, int) and mx > 0
              and ra.get('completed') == list(range(mx)) and ra.get('converged') == [])
        return ok, '', None

    def c_route_a_end_failed_source_preparation_numerics_tokens(self, res, ev):
        ra = self._ra(ev)
        if ra.get('end_outcomes') != ['FAILED_SOURCE_PREPARATION']:
            return False, '', None
        msgs = ra.get('failure_messages') or []
        toks = self._hi_tokens_ok(msgs)
        if not toks:
            return False, '', None
        return True, '+'.join(sorted(set(toks))), None

    def c_route_a_iteration_cap_without_outcome_record(self, res, ev):
        ra = self._ra(ev)
        mx = ra.get('max_iterations')
        ok = (ra.get('present') is True and ra.get('end_outcomes') == [] and isinstance(mx, int) and mx > 0
              and ra.get('completed') == list(range(mx)) and ra.get('converged') == []
              and ra.get('iterations') == list(range(mx)))
        return ok, '', None

    def c_route_a_worker_raised_nonfinite(self, res, ev):
        ra = self._ra(ev)
        fs = ev.get('failed_stages') or []
        af = ra.get('attempt_failure') or {}
        msg = af.get('message')
        ok = fs == ['route_a'] and ra.get('end_outcomes') == [] and msg in self.nonfinite
        return ok, str(msg), None

    def c_route_a_end_not_converged_other(self, res, ev):
        ra = self._ra(ev)
        outs = ra.get('end_outcomes') or []
        ok = bool(outs) and any(o != 'CONVERGED_FINITE_FIXED_POINT' for o in outs)
        return ok, ','.join(outs), None

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
        toks = self._col_tokens_ok(msgs)
        if not toks:
            return False, '', None
        return True, '%s:%s' % (tag, '+'.join(sorted(set(toks)))), self._col_judgment(toks)

    def c_bracket_source_missing_numerics_tokens(self, res, ev):
        for r in ev.get('reasons') or []:
            m = re.match(r'^(\w+) column\(s\) \[.*\] failed; no bracket source$', r)
            if not m:
                continue
            tag = m.group(1)
            msgs = (ev.get('column_failures') or {}).get(tag)
            if not msgs or (ev.get('column_finish_missing') or {}).get(tag):
                return False, '', None
            toks = self._col_tokens_ok(msgs)
            if not toks:
                return False, '', None
            return True, '%s:%s' % (tag, '+'.join(sorted(set(toks)))), self._col_judgment(toks)
        return False, '', None

    def c_body_reference_roster_numerics_tokens(self, res, ev):
        fs = ev.get('failed_stages') or []
        if fs != ['body']:
            return False, '', None
        sf = (ev.get('stage_failures') or {}).get('body') or {}
        if not str(sf.get('message', '')).startswith('Full exact saved'):
            return False, '', None
        toks = self._hi_tokens_ok(ev.get('reference_failures') or [])
        if not toks:
            return False, '', None
        return True, '+'.join(sorted(set(toks))), None

    def c_final_pass_nonpositive_rotation(self, res, ev):
        fp = ev.get('final_pass') or {}
        return fp.get('rotation_positive') is False, '', None

    def c_final_column_mean_invalid_rotation(self, res, ev):
        fp = ev.get('final_pass') or {}
        msg = str((fp.get('column_mean_failure') or {}).get('message', ''))
        return msg.startswith('Invalid finite positive rotation'), '', None

    def c_final_pass_column_failures_numerics_tokens(self, res, ev):
        fp = ev.get('final_pass') or {}
        msgs = [str(f.get('message', '')) for f in (fp.get('column_failures') or [])]
        if not msgs:
            return False, '', None
        toks = self._col_tokens_ok(msgs)
        if not toks:
            return False, '', None
        return True, 'final:%s' % '+'.join(sorted(set(toks))), self._col_judgment(toks)

    CONDITIONS = {
        'always': c_always,
        'valid_true_rows_finite': c_valid_true_rows_finite,
        'route_a_end_iteration_budget_exhausted': c_route_a_end_iteration_budget_exhausted,
        'route_a_end_failed_source_preparation_numerics_tokens': c_route_a_end_failed_source_preparation_numerics_tokens,
        'route_a_iteration_cap_without_outcome_record': c_route_a_iteration_cap_without_outcome_record,
        'route_a_worker_raised_nonfinite': c_route_a_worker_raised_nonfinite,
        'route_a_end_not_converged_other': c_route_a_end_not_converged_other,
        'rotation_missing_columns_numerics_tokens': c_rotation_missing_columns_numerics_tokens,
        'bracket_source_missing_numerics_tokens': c_bracket_source_missing_numerics_tokens,
        'body_reference_roster_numerics_tokens': c_body_reference_roster_numerics_tokens,
        'final_pass_nonpositive_rotation': c_final_pass_nonpositive_rotation,
        'final_column_mean_invalid_rotation': c_final_column_mean_invalid_rotation,
        'final_pass_column_failures_numerics_tokens': c_final_pass_column_failures_numerics_tokens,
    }

    def classify(self, res, ev):
        """-> {class, code, rule, judgment_call}.  Never on status alone: route-A rules read the attempt end records,
        stage rules read the stage records; unmatched -> INFRA."""
        status = res.get('status')
        reasons = [str(x) for x in (res.get('reasons') or [])]
        ev = dict(ev, reasons=reasons)
        if ev.get('errors'):
            return {'class': 'INFRA', 'code': 'EVIDENCE_UNREADABLE:%s' % ev['errors'][0][:120], 'rule': 'EVIDENCE',
                    'judgment_call': False}
        first = reasons[0][:120] if reasons else ''
        for r in self.rules:
            if status not in r['statuses']:
                continue
            ok, fill, jo = self.CONDITIONS[r['condition']](self, res, ev)
            if not ok:
                continue
            code = r['code']
            if '<' in code:
                code = re.sub(r'<[^>]*>', fill or first, code, count=1)
                code = re.sub(r'<[^>]*>', '', code)
            jc = r.get('judgment_call')
            judgment = jo if jo is not None else (jc is True)
            return {'class': r['class'], 'code': code[:200], 'rule': r['id'], 'judgment_call': bool(judgment)}
        return {'class': 'INFRA', 'code': ('UNRECOGNIZED:%s:%s' % (status, first))[:200], 'rule': 'DEFAULT',
                'judgment_call': False}


def collect_evidence(outdir, res, row_ids, taxonomy):
    """Read-only evidence from one call directory (driver c2v006 layout: <outdir>/stages/NN_<name>/...).  Every file
    read is recorded with its sha256 (bound into the cache entry for F2 re-verification)."""
    outdir = Path(outdir)
    ev = {'files': {}, 'errors': [], 'row_ids': list(row_ids)}

    def rd(p):
        raw = Path(p).read_bytes()
        ev['files'][str(p)] = sha256_bytes(raw)
        return raw

    def rj(p):
        return json.loads(rd(p).decode('utf-8'))

    try:
        stages = outdir / 'stages'
        sdirs = sorted(d for d in stages.iterdir() if d.is_dir()) if stages.is_dir() else []

        def stage_named(name):
            return [d for d in sdirs if '_' in d.name and d.name.split('_', 1)[1] == name]
        # route A
        ra = {'present': False}
        rad = stage_named('route_a')
        if rad:
            sd = rad[0]
            cp, att = sd / 'checkpoint', sd / 'attempt_000'
            ra['present'] = cp.is_dir()
            ends = sorted((cp / 'attempts').glob('*.end.json')) if (cp / 'attempts').is_dir() else []
            ra['end_outcomes'] = [str(rj(p).get('outcome')) for p in ends]
            its = []
            if cp.is_dir():
                for x in sorted(cp.iterdir()):
                    if x.is_dir() and x.name.startswith('iteration_') and re.fullmatch(r'\d{4}', x.name[10:]):
                        its.append(int(x.name[10:]))
            ra['iterations'] = its
            comp, conv, fmsgs = [], [], []
            for i in its:
                d = cp / ('iteration_%04d' % i)
                if (d / 'COMPLETED.json').is_file():
                    comp.append(i)
                    if rj(d / 'COMPLETED.json').get('converged') is True:
                        conv.append(i)
                for fp in sorted(d.glob('FAILURE.*.json')):
                    txt = rd(fp).decode('utf-8', 'replace')
                    toks = _tokens_in(txt, taxonomy.hi_tokens) if taxonomy else []
                    fmsgs.append(' '.join(toks) if toks else txt[:300])
            ra['completed'], ra['converged'], ra['failure_messages'] = comp, conv, fmsgs
            if (att / 'failure.json').is_file():
                f = rj(att / 'failure.json')
                ra['attempt_failure'] = {'type': f.get('type'), 'message': f.get('message')}
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
        # column failures by pass tag (fs, rfs, le1, ...)
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
        # reference per-radius failures
        rf = []
        for d in stage_named('reference'):
            fin = d / 'reference' / 'finish.json'
            if fin.is_file():
                rf.extend(str(x.get('message', '')) for x in rj(fin).get('failures') or [])
        ev['reference_failures'] = rf
        # final pass (from result.json itself)
        passes = res.get('passes') or []
        if passes:
            fp = passes[-1]
            ev['final_pass'] = {'pass': fp.get('pass'), 'rotation_positive': fp.get('rotation_positive'),
                                'column_failures': fp.get('column_failures') or [],
                                'column_mean_failure': fp.get('column_mean_failure')}
    except Exception as exc:   # unreadable evidence -> INFRA (never a guess)
        ev['errors'].append('%s: %s' % (type(exc).__name__, exc))
    return ev


def forward_from_result(res, classification, failure_class, rule, row_ids):
    """The engine-facing forward record, a pure function of result.json bytes + the stored class (F2 re-derivation)."""
    if classification == 'VALID':
        sp = res['speeds_km_s']
        return {'valid': True, 'speeds_km_s': {rid: sp[rid] for rid in row_ids}, 'reasons': []}
    if classification == 'MODEL_INVALID':
        return {'valid': False, 'speeds_km_s': {},
                'reasons': ['MODEL_INVALID %s (taxonomy %s)' % (failure_class, rule), 'DRIVER_STATUS %s' % res.get('status')]
                + [str(x)[:300] for x in (res.get('reasons') or [])[:4]]}
    raise OrchestratorError('no forward record for class %s' % classification)


# --------------------------------------------------------------------------------------------- context
class Context:
    """Everything derived from the configuration and the pinned inputs (no side effects on disk)."""

    def __init__(self, config):
        if isinstance(config, (str, Path)):
            self.config_path = str(config)
            raw = Path(config).read_bytes()
            self.config_sha256 = sha256_bytes(raw)
            config = json.loads(raw.decode('utf-8'))
        else:
            self.config_path = None
            self.config_sha256 = sha256_bytes(canonical(config))
        self.cfg = cfg = config
        extra = set(cfg) - CONFIG_KEYS
        if cfg.get('schema') != SCHEMA_CONFIG or extra:
            raise OrchestratorError('config schema must be %s with keys %s (extra: %s)'
                                    % (SCHEMA_CONFIG, sorted(CONFIG_KEYS), sorted(extra)))
        self.synthetic = cfg.get('synthetic_test') is True
        if not isinstance(cfg.get('work_dir'), str) or not os.path.isabs(cfg['work_dir']):
            raise OrchestratorError('A7_ABSOLUTE_PATH: work_dir must be absolute')
        self.work_dir = Path(cfg['work_dir'])
        self.gates = {}
        # coordinate spec (V001, unchanged) and the c2v002 addendum
        spec_raw = read_pinned(cfg['coordinate_spec'], 'coordinate_spec')
        self.spec = spec = json.loads(spec_raw.decode('utf-8'))
        if spec.get('schema') != SCHEMA_SPEC:
            raise OrchestratorError('coordinate spec schema must be %s' % SCHEMA_SPEC)
        if spec['call_spec_mapping']['mapping_id'] != SPEC_MAPPING_ID:
            raise OrchestratorError('coordinate spec mapping_id %r is not %r' % (spec['call_spec_mapping']['mapping_id'],
                                                                               SPEC_MAPPING_ID))
        self.addendum = None
        if cfg.get('coordinate_spec_addendum') is not None:
            self.addendum = json.loads(read_pinned(cfg['coordinate_spec_addendum'], 'coordinate_spec_addendum'))
            if self.addendum.get('schema') != SCHEMA_ADDENDUM or \
                    self.addendum.get('applies_to_coordinate_spec_sha256') != cfg['coordinate_spec']['sha256']:
                raise OrchestratorError('coordinate spec addendum schema / target sha mismatch')
        # engine and freeze modules from pinned bytes (spec pins them)
        self.E = load_pinned_module(spec['engine'], 'orch2_engine_c2v003a', 'engine')
        self.F = load_pinned_module(spec['freeze'], 'orch2_freeze_c2v003a', 'freeze')
        # observation region
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
        # engine coordinates through the freeze module (D4); NGC slots never reach the engine
        ngc = cfg.get('ngc3198_slots') or spec['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation']
        self.ngc_slots_placeholder = cfg.get('ngc3198_slots') is None
        fs = self.F.make_freeze_coordinate_spec(coordinates=list(spec['coordinates']) + list(ngc))
        if not fs['ok']:
            raise OrchestratorError('make_freeze_coordinate_spec: %s' % fs['reasons'])
        self.freeze_spec = fs
        self.engine_coordinates = fs['engine_coordinates']
        if canonical(self.engine_coordinates) != canonical(spec['engine_coordinates']):
            raise OrchestratorError('engine coordinates differ from the coordinate spec record')
        self.es = self.E.make_coordinate_spec(coordinates=self.engine_coordinates)
        if not self.es['ok']:
            raise OrchestratorError('engine make_coordinate_spec: %s' % self.es['reasons'])
        if tuple(self.es['varying_names']) != VARYING_EXPECTED:
            raise OrchestratorError('varying coordinates %r are not the mapping\'s %r' % (self.es['varying_names'],
                                                                                          VARYING_EXPECTED))
        self.n_varying = self.es['n_varying']
        params = copy.deepcopy(spec['engine_parameters'])
        if cfg.get('engine_parameters_override'):
            if not self.synthetic:
                raise OrchestratorError('engine_parameters_override is allowed only in a synthetic_test config')
            params.update(copy.deepcopy(cfg['engine_parameters_override']))
        self.params = params
        # template, numerics block (gate), concurrency
        mp = spec['call_spec_mapping']
        self.template_raw = read_pinned(mp['template'], 'call-spec template')
        self.template = json.loads(self.template_raw.decode('utf-8'))
        self.template_sha256 = mp['template']['sha256']
        self.inclination_deg = float(spec['ddo154_forward_constants']['inclination_deg']['value'])
        if float(self.template['physical']['inclination_deg']) != self.inclination_deg:
            raise OrchestratorError('template inclination differs from the declared DDO154 constant')
        block, self.gates['numerics_verdict'] = check_numerics(cfg.get('numerics'), self.template['numerics'])
        cw = cfg.get('column_workers', block.get('column_workers', 1))
        if type(cw) is not int or not 1 <= cw <= CAMPAIGN_PROCESS_LIMIT:
            raise OrchestratorError('column_workers must be an int 1..12')
        self.column_workers = cw
        self.numerics = copy.deepcopy(block)
        self.numerics['column_workers'] = cw
        self.numerics_is_template = canonical(self.numerics) == canonical(self.template['numerics'])
        # driver, its normalizer, taxonomy, deciding gate
        self.driver = cfg['driver']
        read_pinned(self.driver, 'driver')
        self.D = exec_pinned_bytes(self.driver, 'orch2_driver_normalizer', 'driver')
        if not callable(getattr(self.D, 'normalize_spec', None)):
            raise OrchestratorError('driver exposes no normalize_spec')
        tax_raw = read_pinned(cfg['taxonomy'], 'taxonomy')
        self.taxonomy = Taxonomy(json.loads(tax_raw.decode('utf-8')), cfg['taxonomy']['sha256'])
        if self.taxonomy.doc['driver']['sha256'] != self.driver['sha256'] and not self.synthetic:
            raise OrchestratorError('taxonomy is written for driver %s, config driver is %s'
                                    % (self.taxonomy.doc['driver']['sha256'][:16], self.driver['sha256'][:16]))
        self.gates['deciding_test'] = check_deciding(cfg.get('deciding_test'), self.driver['sha256'])
        self.recovery_rules = cfg.get('recovery_rules') or []
        self.python = cfg['python']
        self.executor_kind = cfg.get('executor', 'campaign')
        if self.executor_kind not in ('campaign', 'in_process_test'):
            raise OrchestratorError('executor must be campaign or in_process_test')
        if self.executor_kind == 'in_process_test' and not self.synthetic:
            raise OrchestratorError('in_process_test executor requires synthetic_test')
        mc = cfg.get('max_concurrent', 1)
        nc = cfg.get('n_cores', CAMPAIGN_PROCESS_LIMIT)
        if type(mc) is not int or mc < 1 or type(nc) is not int or nc < 1:
            raise OrchestratorError('max_concurrent and n_cores must be positive ints')
        if mc * cw > min(nc, CAMPAIGN_PROCESS_LIMIT):
            raise OrchestratorError('max_concurrent (%d) x column_workers (%d) = %d exceeds min(n_cores %d, campaign '
                                    'limit %d)' % (mc, cw, mc * cw, nc, CAMPAIGN_PROCESS_LIMIT))
        self.max_concurrent, self.n_cores = mc, nc
        self.M = self.C = None
        if self.executor_kind == 'campaign':
            self.M = load_pinned_module(cfg['monitor'], 'orch2_monitor_c2v001', 'monitor')
            self.C = load_pinned_module(cfg['campaign'], 'orch2_campaign_c2v001', 'campaign')
        # base spec (item 1) and A7 guards on it
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
            'taxonomy_sha256': self.taxonomy.sha256, 'row_ids': self.row_ids,
            'engine_names': list(self.es['names']), 'ddo154_inclination_deg': self.inclination_deg}))
        P = self.params
        # one march side: <= floor(log2(sqrt(n)/march_step)) + 1 doublings + 1 edge + bisection_steps; +1 margin
        self.side_bound = int(math.floor(math.log2(math.sqrt(self.n_varying) / float(P['march_step'])))) + 3 + \
            int(P['bisection_steps'])
        self.trial_u = self._engine_trial_u()
        self.gates['driver_capability'] = self.capability_probe()

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

    def capability_probe(self):
        """Item 1 gate: the trial point and all 2^n box corners (fixed coordinates at trial) must pass prelaunch_check."""
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
        refused, accepted = [], 0
        for label, th in pts:
            try:
                b = self.mapper.build(th)
                self.prelaunch_check(b['spec'])
                accepted += 1
            except OrchestratorError as exc:
                refused.append({'point': label, 'distance_Mpc': th['distance_Mpc'], 'reason': str(exc)[:300]})
        return {'ok': not refused, 'n_points': len(pts), 'n_accepted': accepted, 'refused': refused,
                'reasons': ([] if not refused else ['DRIVER_CAPABILITY_GAP: the pinned driver refuses %d of %d probe '
                                                    'points (first: %s)' % (len(refused), len(pts), refused[0]['reason'][:200])])}

    def gates_ok(self):
        return all(g.get('ok') for g in self.gates.values())

    def gate_report(self):
        return {k: {kk: vv for kk, vv in v.items() if kk != 'refused' or len(vv) <= 20} for k, v in self.gates.items()}

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
                doc = json.loads(read_pinned(r, 'recovery rule'))
                bk = doc.get('brackets')
                if not isinstance(bk, dict):
                    raise OrchestratorError('recovery rule %s has no brackets block' % path)
                a7 = lint_override_keys(bk)
                if a7:
                    raise OrchestratorError('A7_GUARD recovery rule: %s' % a7)
                return {'path': r['path'], 'sha256': r['sha256'], 'rule_id': r.get('rule_id'), 'brackets': bk}
        raise OrchestratorError('recovery rule %s is not in the config allowlist recovery_rules' % path)

    def disk_forecast(self, n_next=None):
        dg = self.cfg.get('disk_guard') or {}
        per = int(dg.get('per_call_bytes', (self.cfg.get('per_call') or {}).get('output_cap_bytes', 0)))
        reserve = int(dg.get('reserve_bytes', 0))
        meas = dg.get('measured_per_call_bytes')
        p = self.work_dir
        while not p.exists() and p != p.parent:
            p = p.parent
        free = shutil.disk_usage(str(p)).free
        out = {'free_bytes': free, 'reserve_bytes': reserve, 'per_call_bytes_guard': per,
               'calls_affordable_now_guard': (max(0, (free - reserve) // per) if per > 0 else None),
               'measured_per_call_bytes': meas,
               'calls_affordable_now_measured': (max(0, (free - reserve) // int(meas)) if meas else None),
               'rule': 'HALTED_DISK before a wave unless free >= n_calls x per_call_bytes_guard + reserve; nothing is deleted'}
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
        spec['label'] = 'DDO154 calibration orchestrator c2v002 theta %s; base %s' % (key[:16], ctx.base_sha256[:8])
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


# --------------------------------------------------------------------------------------------- cache
class Cache:
    """theta-keyed cache: one immutable JSON file per canonical theta hash; never overwritten.
    Only VALID and MODEL_INVALID are cached (NUMERICS_LIMITED and INFRA halt)."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.dir = ctx.work_dir / 'cache' / ctx.cache_id
        self.entries_dir = self.dir / 'entries'
        self.entries = {}

    def open(self, create):
        if create:
            self.entries_dir.mkdir(parents=True, exist_ok=True)
            hdr = self.dir / 'CACHE_HEADER.json'
            body = {'schema': SCHEMA_CACHE_ID, 'cache_id': self.ctx.cache_id, 'mapping_id': MAPPING_ID,
                    'template_sha256': self.ctx.template_sha256, 'base_spec_sha256': self.ctx.base_sha256,
                    'driver_sha256': self.ctx.driver['sha256'], 'taxonomy_sha256': self.ctx.taxonomy.sha256,
                    'numerics': self.ctx.numerics, 'row_ids': self.ctx.row_ids,
                    'engine_names': list(self.ctx.es['names'])}
            if hdr.exists():
                if json.loads(hdr.read_text())['cache_id'] != self.ctx.cache_id:
                    raise OrchestratorError('cache header id mismatch')
            else:
                write_json_atomic_x(hdr, body)
        self.entries = {}
        if not self.entries_dir.is_dir():
            return self
        for p in sorted(self.entries_dir.glob('*.json')):
            e = json.loads(p.read_bytes().decode('utf-8'))
            self._verify(e, p.stem)
            self.entries[e['key']] = e
        return self

    def _verify(self, e, stem):
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
        if src == 'WAVE':
            # F2: the cached forward must be re-derivable from the result.json bytes the receipt pinned
            rp, rs = pv.get('result_path'), pv.get('result_sha256')
            if not rp or not rs or not os.path.isfile(rp):
                raise OrchestratorError('cache entry %s: result.json missing' % stem)
            raw = Path(rp).read_bytes()
            if sha256_bytes(raw) != rs:
                raise OrchestratorError('cache entry %s: result.json bytes no longer verify' % stem)
            res = json.loads(raw.decode('utf-8'))
            fwd2 = forward_from_result(res, e['classification'], e.get('failure_class'),
                                       (pv.get('taxonomy') or {}).get('rule'), self.ctx.row_ids)
            if canonical(fwd2) != canonical(f):
                raise OrchestratorError('cache entry %s: forward record differs from the one derived from result.json '
                                        '(F2 custody)' % stem)
            for p, s in (pv.get('evidence_files') or {}).items():
                if not os.path.isfile(p) or sha256_file(p) != s:
                    raise OrchestratorError('cache entry %s: evidence file changed: %s' % (stem, p))
        elif src == 'ANCHOR_ALIAS':
            rp, rs = pv.get('result_path'), pv.get('result_sha256')
            raw = Path(rp).read_bytes() if rp and os.path.isfile(rp) else b''
            if sha256_bytes(raw) != rs:
                raise OrchestratorError('cache entry %s: anchor result bytes no longer verify' % stem)
            res = json.loads(raw.decode('utf-8'))
            fwd2 = {'valid': True, 'speeds_km_s': {rid: float(res['speeds_km_s'][rid]) for rid in self.ctx.row_ids},
                    'reasons': []}
            if canonical(fwd2) != canonical(f):
                raise OrchestratorError('cache entry %s: alias speeds differ from the anchor result (F2)' % stem)
        elif src == 'ROOT_RESOLUTION':
            if e['classification'] != 'MODEL_INVALID' or f['speeds_km_s']:
                raise OrchestratorError('cache entry %s: a root resolution can only declare MODEL_INVALID' % stem)
        elif src == 'IN_PROCESS_TEST':
            if not self.ctx.synthetic:
                raise OrchestratorError('cache entry %s: IN_PROCESS_TEST entry in a non-synthetic cache' % stem)
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
            old = json.loads(path.read_bytes().decode('utf-8'))
            strip = lambda d: {k: v for k, v in d.items() if k not in ('ingested_utc', 'entry_sha256')}  # noqa: E731
            if canonical(strip(old)) != canonical(strip(e)):
                raise OrchestratorError('cache entry %s exists with different content (never overwritten)' % key)
            self.entries[key] = old
            return old, False
        self._verify(e, key)
        write_json_atomic_x(path, e)
        self.entries[key] = e
        return e, True


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
    """One wave = one campaign of the pinned campaign launcher in <wave_dir>/campaign."""

    def __init__(self, ctx):
        self.ctx = ctx

    def campaign_dict(self, plan):
        cfg = self.ctx.cfg
        return {'calls': [{'spec': c['spec']} for c in plan['calls']], 'max_concurrent': self.ctx.max_concurrent,
                'per_call': cfg['per_call'], 'campaign_wall_cap_s': cfg['campaign_wall_cap_s'],
                'driver': cfg['driver'], 'monitor': cfg['monitor']}

    @staticmethod
    def call_markers(d):
        d = str(d)
        return [d + '/spec.json', d + '/out']

    def orphans(self, campaign_dir):
        """Call dirs of an interrupted campaign without a receipt.  alive: True (driver child alive, or F4: any live
        process referencing the call dir), False (dead), None (unknown: no launch record and no live process)."""
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
                alive = True                     # process table unreadable: treat as possibly alive (fail closed)
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
        meta = {k: out.get(k) for k in ('status', 'launched', 'max_concurrent_observed', 'n_ok', 'n_failed',
                                        'n_resumed', 'n_not_started', 'n_unverified', 'campaign_wall_used_s',
                                        'summary_path')}
        meta['orphans'] = orph
        return out['calls'], meta

    def classify(self, plan_call, rec):
        """-> (class, code, forward or None, provenance)."""
        ctx = self.ctx
        prov = {'call_dir': rec.get('call_dir'), 'campaign_status': rec.get('status'), 'spec_sha256': plan_call['spec_sha256']}
        st = rec.get('status')
        if st not in ('OK', 'FAILED', 'RESUMED_OK', 'RESUMED_FAILED'):
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
        raw = Path(pin['path']).read_bytes()
        if sha256_bytes(raw) != pin['sha256']:
            return 'INFRA', 'RESULT_HASH', None, prov
        prov.update({'result_path': pin['path'], 'result_sha256': pin['sha256']})
        res = json.loads(raw.decode('utf-8'))
        if res.get('call_spec_sha256') != plan_call['spec_sha256'] or res.get('driver_sha256') != ctx.driver['sha256']:
            return 'INFRA', 'RESULT_NOT_BOUND_TO_SPEC_OR_DRIVER', None, prov
        ds = r.get('driver_status')
        if ds != res.get('status'):
            return 'INFRA', 'DRIVER_STATUS_MISMATCH %r/%r' % (ds, res.get('status')), None, prov
        ev = collect_evidence(Path(pin['path']).parent, res, ctx.row_ids, ctx.taxonomy)
        out = ctx.taxonomy.classify(res, ev)
        prov['taxonomy'] = {'rule': out['rule'], 'code': out['code'], 'class': out['class'],
                            'judgment_call': out['judgment_call'], 'taxonomy_sha256': ctx.taxonomy.sha256}
        prov['evidence_files'] = ev['files']
        prov['route_a'] = {k: (ev.get('route_a') or {}).get(k) for k in ('end_outcomes', 'iterations', 'converged',
                                                                       'max_iterations')}
        if out['class'] in CACHED_CLASSES:
            return out['class'], out['code'], forward_from_result(res, out['class'], out['code'], out['rule'],
                                                                  ctx.row_ids), prov
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
        f = {k: v for k, v in f.items() if not k.startswith('_')}
        if f.get('valid') is True:
            return 'VALID', None, copy.deepcopy(f), prov
        return 'MODEL_INVALID', 'IN_PROCESS_INVALID', copy.deepcopy(f), prov


# --------------------------------------------------------------------------------------------- orchestrator
class Lock:
    def __init__(self, work_dir):
        self.path = Path(work_dir) / 'ORCHESTRATOR.lock'
        self.held = False
        self.stale = None

    def acquire(self):
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                try:
                    old = json.loads(self.path.read_text())
                except Exception:
                    old = {}
                if pid_alive(old.get('pid')) and old.get('host') == socket.gethostname():
                    return False
                self.stale = str(self.path) + '.stale_%s_%s' % (utc_compact(), old.get('pid'))
                os.rename(self.path, self.stale)
                continue
            os.write(fd, canonical({'pid': os.getpid(), 'utc': utc(), 'host': socket.gethostname(),
                                    'module': MODULE_NAME}))
            os.close(fd)
            self.held = True
            return True
        return False

    def release(self):
        if self.held:
            try:
                if json.loads(self.path.read_text()).get('pid') == os.getpid():
                    os.unlink(self.path)   # the orchestrator's own lock file
            except OSError:
                pass
            self.held = False


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
        self.retry_path = ctx.work_dir / 'RETRY_AUTHORISED.jsonl'
        self.resolution_path = ctx.work_dir / 'RESOLUTIONS.jsonl'
        self.events_path = ctx.work_dir / 'EVENTS.jsonl'
        self._log = log or (lambda m: print('[%s] %s' % (utc(), m), file=sys.stderr, flush=True))
        self.alias = None

    def log(self, msg, **kw):
        self._log(msg)
        if self.ctx.work_dir.is_dir():
            append_jsonl(self.events_path, dict({'utc': utc(), 'pid': os.getpid(), 'msg': msg}, **kw))

    # ---------------------------------------------------------------- setup
    def prepare(self, create):
        if create:
            self.ctx.work_dir.mkdir(parents=True, exist_ok=True)
            cfg_copy = self.ctx.work_dir / ('CONFIG_COPY_%s.json' % self.ctx.config_sha256[:16])
            if not cfg_copy.exists():
                write_json_atomic_x(cfg_copy, self.ctx.cfg)
        self.cache.open(create=create)
        self.alias = self.install_anchor_alias(write=create)
        return self.alias

    def install_anchor_alias(self, write):
        ctx = self.ctx
        an = ctx.cfg.get('anchor')
        if not an or not an.get('use'):
            return {'used': False, 'reason': 'ANCHOR_DISABLED_IN_CONFIG'}
        if not ctx.numerics_is_template:
            return {'used': False, 'reason': 'NUMERICS_DIFFER_FROM_ANCHOR (seed will be computed)'}
        if an['spec_sha256'] != ctx.template_sha256:
            raise OrchestratorError('anchor spec sha is not the template sha')
        if an['driver_sha256'] != ctx.driver['sha256'] and an.get('accept_driver_equivalence') is not True:
            return {'used': False, 'reason': 'ANCHOR_DRIVER_DIFFERS_AND_EQUIVALENCE_NOT_ACCEPTED'}
        read_pinned(an['receipt'], 'anchor receipt')
        mon = ctx.M if ctx.M is not None else load_pinned_module(ctx.cfg['monitor'], 'orch2_monitor_alias', 'monitor')
        v = mon.verify_receipt(an['receipt']['path'], spec_sha256=an['spec_sha256'], driver_sha256=an['driver_sha256'])
        if not v['ok']:
            raise OrchestratorError('anchor receipt does not verify: %s' % v['reasons'])
        rec = v['receipt']
        if rec.get('status') != 'FINISHED' or rec.get('driver_status') != 'COMPLETED' or \
                (rec.get('result') or {}).get('sha256') != an['result']['sha256']:
            raise OrchestratorError('anchor receipt is not a FINISHED/COMPLETED receipt of the pinned result')
        res = json.loads(read_pinned(an['result'], 'anchor result').decode('utf-8'))
        if res.get('call_spec_sha256') != ctx.template_sha256 or res.get('driver_sha256') != an['driver_sha256'] or \
                res.get('valid') is not True or res.get('status') != 'COMPLETED':
            raise OrchestratorError('anchor result does not bind to the template spec / anchor driver or is not valid')
        sp = res.get('speeds_km_s') or {}
        if any(rid not in sp or not math.isfinite(sp[rid]) for rid in ctx.row_ids):
            raise OrchestratorError('anchor result lacks finite speeds for the region rows')
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
                'anchor_driver_sha256': an['driver_sha256'], 'calibration_driver_sha256': ctx.driver['sha256'],
                'driver_equivalence_accepted': an['driver_sha256'] != ctx.driver['sha256'],
                'alias_spec_sha256_not_launched': built['sha256'], 'relative_deviation': dev,
                'alias_rtol': ANCHOR_ALIAS_RTOL, 'elapsed_seconds': rec.get('elapsed_seconds')}
        fwd = {'valid': True, 'speeds_km_s': {rid: float(sp[rid]) for rid in ctx.row_ids}, 'reasons': []}
        if write:
            self.cache.put(key=built['key'], theta=theta, classification='VALID', failure_class=None,
                           source='ANCHOR_ALIAS', provenance=prov, forward=fwd)
        elif built['key'] not in self.cache.entries:
            self.cache.entries[built['key']] = {'key': built['key'], 'forward': fwd, 'classification': 'VALID',
                                                'source': 'ANCHOR_ALIAS(unwritten)'}
        return {'used': True, 'key': built['key'], 'max_relative_deviation': max(dev.values()),
                'driver_equivalence_accepted': prov['driver_equivalence_accepted']}

    # ---------------------------------------------------------------- waves, ledger (F3)
    def wave_dirs(self):
        if not self.waves_dir.is_dir():
            return []
        return sorted(p for p in self.waves_dir.glob('wave_*') if p.is_dir())

    def committed_waves(self):
        """Waves whose plan was committed (atomic link).  Planless dirs (crash before commit) are not waves."""
        out = {}
        for wd in self.wave_dirs():
            p = wd / 'WAVE_PLAN.json'
            if p.is_file():
                try:
                    out[json.loads(p.read_text())['wave']] = wd
                except (ValueError, KeyError):
                    raise OrchestratorError('unreadable wave plan %s' % p)
        return out

    def launches(self):
        """F3: a ledger line counts as a launch only if its wave's plan was committed (the campaign starts only after
        the commit)."""
        committed = self.committed_waves()
        n = {}
        for ln in read_jsonl(self.ledger_path):
            if ln.get('wave') in committed:
                n[ln['key']] = n.get(ln['key'], 0) + 1
        return n

    def authorised(self):
        n = {}
        for ln in read_jsonl(self.retry_path):
            n[ln['key']] = n.get(ln['key'], 0) + 1
        return n

    def recovery_for(self, key):
        last = None
        for ln in read_jsonl(self.retry_path):
            if ln['key'] == key:
                last = ln
        if last is None or not last.get('recovery'):
            return None
        rr = self.ctx.recovery_rule(last['recovery']['path'])
        if rr['sha256'] != last['recovery']['sha256']:
            raise OrchestratorError('recovery rule bytes changed since the resolve: %s' % rr['path'])
        return rr

    def make_plan(self, wave_no, misses):
        calls, seen = [], set()
        for m in misses:
            if m['key'] in seen:
                continue
            seen.add(m['key'])
            rec = self.recovery_for(m['key'])
            b = self.ctx.mapper.build(m['theta'], recovery=rec)
            if b['key'] != m['key']:
                raise OrchestratorError('mapper key differs from probe key')
            self.ctx.prelaunch_check(b['spec'], recovery=rec is not None)
            calls.append({'call_index': len(calls), 'key': m['key'], 'theta': m['theta'], 'family': m['family'],
                          'branch': m['branch'], 'purpose': m['purpose'], 'u': m['u'], 'sibling': m['sibling'],
                          'spec': b['spec'], 'spec_sha256': b['sha256'], 'changed_paths': b['changed_paths'],
                          'recovery': ({k: rec[k] for k in ('path', 'sha256', 'rule_id')} if rec else None)})
        return {'schema': SCHEMA_WAVE_PLAN, 'wave': wave_no, 'created_utc': utc(), 'cache_id': self.ctx.cache_id,
                'module': MODULE_NAME, 'calls': calls, 'n_calls': len(calls),
                'families': sorted(set(tuple(c['family']) for c in calls)),
                'max_concurrent': self.ctx.max_concurrent, 'column_workers': self.ctx.column_workers,
                'batches': int(math.ceil(len(calls) / float(max(1, self.ctx.max_concurrent))))}

    def disk_ok(self, n_calls):
        f = self.ctx.disk_forecast(n_calls)
        return f['next_wave_fits'], f

    def ingest(self, wave_dir, plan, records, meta):
        n = {'VALID': 0, 'MODEL_INVALID': 0, 'NUMERICS_LIMITED': 0, 'INFRA': 0, 'already_cached': 0}
        halt = []
        out_calls = []
        for c, rec in zip(plan['calls'], records):
            cls, fc, fwd, prov = self.executor.classify(c, rec)
            prov = dict(prov, wave=plan['wave'], call_index=c['call_index'], recovery=c.get('recovery'))
            if cls in HALT_CLASSES:
                n[cls] += 1
                halt.append({'key': c['key'], 'call_index': c['call_index'], 'class': cls, 'reason': fc,
                             'provenance': prov})
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
        result = {'schema': SCHEMA_WAVE_RESULT, 'wave': plan['wave'], 'utc': utc(), 'counts': n, 'calls': out_calls,
                  'campaign': meta, 'halt': halt}
        if halt:
            write_json_atomic_x(wave_dir / 'HALT.json', {
                'wave': plan['wave'], 'utc': utc(), 'items': halt,
                'rule': 'never retried automatically; root resolves each key with: resolve --decision '
                        'invalid | retry | retry_with_recovery --recovery <allowlisted rule path>'})
        write_json_atomic_x(wave_dir / 'WAVE_RESULT.json', result)
        return result

    def run_wave(self, wave_dir, plan, resume):
        t0 = time.monotonic()
        records, meta = self.executor.execute(wave_dir, plan, resume, self.log)
        if records is None:
            return None, meta
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
                                            'spec_sha256': c['spec_sha256'], 'utc': utc()})
        write_json_atomic_x(wd / 'WAVE_PLAN.json', plan)

    # ---------------------------------------------------------------- main loop
    def run(self, max_waves=None):
        ctx = self.ctx
        if not ctx.gates_ok():
            return {'status': 'REFUSED', 'reasons': ['GATES_NOT_PASSED'], 'gates': ctx.gate_report()}
        ctx.work_dir.mkdir(parents=True, exist_ok=True)
        lock = Lock(ctx.work_dir)
        if not lock.acquire():
            return {'status': 'LOCKED'}
        try:
            self.prepare(create=True)
            self.log('orchestrator start', cache_id=ctx.cache_id, alias=self.alias, stale_lock=lock.stale)
            final = ctx.work_dir / 'FINAL_SUMMARY.json'
            if final.exists():
                return dict(json.loads(final.read_text()), status='COMPLETE', note='already complete')
            for wd in self.wave_dirs():
                if (wd / 'WAVE_PLAN.json').is_file() and not (wd / 'WAVE_RESULT.json').exists():
                    plan = json.loads((wd / 'WAVE_PLAN.json').read_text())
                    pr = self.probe.run(self.cache, 'probe', exclude=[c['key'] for c in plan['calls']])
                    if [m['key'] for m in self._dedup(pr['misses'])] != [c['key'] for c in plan['calls']]:
                        raise OrchestratorError('interrupted wave %s: the probe no longer predicts its calls '
                                                '(determinism failure)' % wd.name)
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
                launched, auth = self.launches(), self.authorised()
                again = [m['key'] for m in misses if launched.get(m['key'], 0) >= 1 + auth.get(m['key'], 0)]
                if again:
                    self.log('halt: %d requested theta were launched before and are unresolved' % len(again))
                    return {'status': 'HALTED_UNRESOLVED', 'keys': again,
                            'rule': 'an earlier launch of these theta halted (NUMERICS_LIMITED or INFRA); resolve them'}
                if max_waves is not None and waves_run >= max_waves:
                    return {'status': 'MAX_WAVES', 'next_wave_calls': len(misses)}
                ok, disk = self.disk_ok(len(misses))
                if not ok:
                    self.log('halt: disk guard', disk=disk)
                    return {'status': 'HALTED_DISK', 'disk': disk}
                wave_no = len(self.wave_dirs()) + 1
                wd = self.waves_dir / ('wave_%04d' % wave_no)
                plan = self.make_plan(wave_no, misses)          # every spec passes prelaunch_check before any write
                plan['probe'] = {k: pr[k] for k in ('stop_reason', 'calls', 'hits', 'placeholders', 'families')}
                plan['disk'] = disk
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
        doc = json.loads(Path(rec_path).read_bytes().decode('utf-8'))
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
        # F3: deterministic record name -> a rerun after a crash reuses (and re-verifies) the record, never duplicates it
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
            if not pp.is_file():                       # F3: planless wave dir (crash before commit) -> skipped
                waves.append({'wave_dir': wd.name, 'planless': True})
                continue
            p = json.loads(pp.read_text())
            r = json.loads((wd / 'WAVE_RESULT.json').read_text()) if (wd / 'WAVE_RESULT.json').exists() else {}
            waves.append({'wave': p['wave'], 'n_calls': p['n_calls'], 'batches': p['batches'], 'families': p['families'],
                          'counts': r.get('counts'), 'wall_s': r.get('wall_s')})
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
        inv, judg, recov = {}, [], []
        for k in used_set:
            e = self.cache.entries.get(k)
            if not e:
                continue
            tx = (e.get('provenance') or {}).get('taxonomy') or {}
            if e['classification'] == 'MODEL_INVALID':
                inv[e.get('failure_class')] = inv.get(e.get('failure_class'), 0) + 1
            if tx.get('judgment_call'):
                judg.append({'key': k, 'rule': tx.get('rule'), 'code': tx.get('code'), 'class': tx.get('class')})
            if (e.get('provenance') or {}).get('recovery'):
                recov.append({'key': k, 'recovery': e['provenance']['recovery']})
        jac = run.get('jacobian') or {}
        return {
            'schema': SCHEMA_SUMMARY, 'module': MODULE_NAME, 'utc': utc(), 'synthetic_test': ctx.synthetic,
            'config_sha256': ctx.config_sha256, 'cache_id': ctx.cache_id, 'base_spec_sha256': ctx.base_sha256,
            'pins': {'coordinate_spec': ctx.cfg['coordinate_spec'], 'coordinate_spec_addendum': ctx.cfg.get('coordinate_spec_addendum'),
                     'observation_region': ctx.region_pin, 'engine': ctx.spec['engine'], 'freeze': ctx.spec['freeze'],
                     'driver': ctx.driver, 'taxonomy': ctx.cfg['taxonomy'], 'monitor': ctx.cfg.get('monitor'),
                     'campaign': ctx.cfg.get('campaign'), 'template': ctx.spec['call_spec_mapping']['template'],
                     'orchestrator': {'path': os.path.realpath(__file__), 'sha256': sha256_file(os.path.realpath(__file__))}},
            'gates': ctx.gate_report(), 'numerics': ctx.numerics, 'numerics_is_template': ctx.numerics_is_template,
            'column_workers': ctx.column_workers, 'max_concurrent': ctx.max_concurrent,
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
            'freeze_gate': ('ROOT_CALL_ORDER step 2 may start (record pinned at step 5)' if run['status'] == 'COMPLETE'
                            else 'NO FREEZE: engine status %s is a result to register, not to retry silently' % run['status']),
        }

    # ---------------------------------------------------------------- resolve / plan / status
    def resolve(self, wave, key_prefix, decision, reason, recovery_path=None):
        ctx = self.ctx
        if decision not in DECISIONS:
            raise OrchestratorError('decision must be one of %s' % (DECISIONS,))
        if decision == 'retry_with_recovery':
            if not recovery_path:
                raise OrchestratorError('retry_with_recovery needs --recovery PATH (an allowlisted rule)')
            rr = ctx.recovery_rule(recovery_path)
        elif recovery_path:
            raise OrchestratorError('--recovery is only valid with retry_with_recovery')
        wd = self.waves_dir / ('wave_%04d' % int(wave))
        halt = json.loads((wd / 'HALT.json').read_text())
        plan = json.loads((wd / 'WAVE_PLAN.json').read_text())
        by_key = {c['key']: c for c in plan['calls']}
        self.cache.open(create=True)
        items = [it for it in halt['items'] if key_prefix == '*' or it['key'].startswith(key_prefix)]
        if decision != 'invalid':
            # F4: never authorise a relaunch while any process still references the call directory
            for it in items:
                cd = (it.get('provenance') or {}).get('call_dir')
                if cd:
                    procs = live_processes(CampaignExecutor.call_markers(cd))
                    if procs is None or procs:
                        raise OrchestratorError('F4: live process(es) still reference %s: %s; wait or stop them first'
                                                % (cd, procs))
        done = []
        for it in items:
            c = by_key[it['key']]
            if it['key'] in self.cache.entries:
                done.append({'key': it['key'], 'note': 'already resolved/cached'})
                continue
            line = {'utc': utc(), 'wave': int(wave), 'key': it['key'], 'decision': decision, 'reason': reason,
                    'halt_class': it['class'], 'halt_reason': it['reason']}
            if decision == 'invalid':
                self.cache.put(key=it['key'], theta=c['theta'], classification='MODEL_INVALID',
                               failure_class='ROOT_DECLARED_INVALID_AFTER_%s:%s' % (it['class'], str(it['reason']).split(':')[0]),
                               source='ROOT_RESOLUTION', provenance=dict(it['provenance'], root_reason=reason),
                               forward={'valid': False, 'speeds_km_s': {},
                                        'reasons': ['ROOT_DECLARED_INVALID after %s %s: %s'
                                                    % (it['class'], it['reason'], reason)]})
            else:
                auth = {'key': it['key'], 'utc': utc(), 'wave': int(wave), 'reason': reason, 'decision': decision}
                if decision == 'retry_with_recovery':
                    auth['recovery'] = {'path': rr['path'], 'sha256': rr['sha256'], 'rule_id': rr['rule_id']}
                    line['recovery'] = auth['recovery']
                append_jsonl(self.retry_path, auth)
            append_jsonl(self.resolution_path, line)
            done.append(line)
        return {'status': 'OK', 'resolved': done}

    def plan_only(self):
        self.prepare(create=False)
        pr = self.probe.run(self.cache, 'probe')
        base = {'gates': self.ctx.gate_report(), 'gates_ok': self.ctx.gates_ok(), 'alias': self.alias,
                'cache_id': self.ctx.cache_id, 'base_spec_sha256': self.ctx.base_sha256,
                'n_cached': len(self.cache.entries), 'column_workers': self.ctx.column_workers,
                'max_concurrent': self.ctx.max_concurrent,
                'open_items_from_addendum': sorted(((self.ctx.addendum or {}).get('items') or {}).keys())}
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
                                          'physical': {k: c['spec']['physical'][k] for k in
                                                       ('common_scale_s', 'gamma', 'ell_F_m', 'distance_Mpc')}}
                                         for c in plan['calls']]},
                    disk=self.ctx.disk_forecast(plan['n_calls']))

    def status(self):
        ctx = self.ctx
        self.cache.open(create=False)
        halts = []
        for wd in self.wave_dirs():
            h = wd / 'HALT.json'
            if h.is_file():
                d = json.loads(h.read_text())
                halts.append({'wave': wd.name, 'classes': sorted(set(i['class'] for i in d['items'])),
                              'n_items': len(d['items'])})
        return {'status': 'OK', 'cache_id': ctx.cache_id, 'n_cached': len(self.cache.entries),
                'waves': [p.name for p in self.wave_dirs()], 'final': (ctx.work_dir / 'FINAL_SUMMARY.json').exists(),
                'halts': halts, 'gates_ok': ctx.gates_ok(), 'gates': ctx.gate_report(),
                'disk': ctx.disk_forecast(None)}


# --------------------------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('command', choices=('plan', 'run', 'resolve', 'status'))
    ap.add_argument('--config', required=True)
    ap.add_argument('--max-waves', type=int, default=None)
    ap.add_argument('--wave', type=int)
    ap.add_argument('--key')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--decision', choices=DECISIONS)
    ap.add_argument('--recovery')
    ap.add_argument('--reason')
    a = ap.parse_args(argv)
    try:
        ctx = Context(a.config)
        orch = Orchestrator(ctx)
        if a.command == 'plan':
            out = orch.plan_only()
        elif a.command == 'run':
            out = orch.run(max_waves=a.max_waves)
        elif a.command == 'resolve':
            if a.wave is None or a.decision is None or not a.reason or not (a.key or a.all):
                raise OrchestratorError('resolve needs --wave, --decision, --reason and --key PREFIX or --all')
            out = orch.resolve(a.wave, '*' if a.all else a.key, a.decision, a.reason, a.recovery)
        else:
            out = orch.status()
    except OrchestratorError as exc:
        out = {'status': 'REFUSED', 'reasons': [str(exc)]}
    print(json.dumps({k: v for k, v in out.items() if k not in ('waves',)} if a.command == 'run' else out,
                     indent=1, sort_keys=True, default=str))
    return EXIT.get(out.get('status'), 3)


if __name__ == '__main__':
    sys.exit(main())
