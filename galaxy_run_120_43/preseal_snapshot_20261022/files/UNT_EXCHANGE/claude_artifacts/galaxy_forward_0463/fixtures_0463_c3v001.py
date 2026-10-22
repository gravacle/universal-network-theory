#!/usr/bin/env python3
"""fixtures_0463_c3v001.py -- independent fixture suite for dispatch 0463 (Modules C and D).

Written from INTERFACE_0463_V001.md (and INTERFACE_0462_V001.md Module 1 for the engine
kwargs) BEFORE any module under test was read.  It never edits a module under test.

Usage:
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  <python3> -I -B fixtures_0463_c3v001.py <artifact_dir_0463> <artifact_dir_0462> <scratch_dir>
      [--results-out <path>] [--only R1,R2,...]

Modules are imported by file path:
  <artifact_dir_0463>/campaign_runner_c3v001.py          (Module C under test)
  <artifact_dir_0463>/batched_engine_adapter_c3v001.py   (Module D under test)
  <artifact_dir_0462>/calibration_region_engine_c3v001.py (0462 engine, not under test)
  <artifact_dir_0463>/mock_worker_0463.py                 (the mock worker, run as subprocess by the runner)

Every campaign directory lives under <scratch_dir>/run_<UTC stamp>/ (created fresh; nothing is
deleted).  The real workers are never run; no NGC3198 velocity is read; no network.

Defined here (fixture-local, per the interface "Fixtures" section):
  * mock_result_reader(outdir)           -> forward-style result for the mock result.json layout
  * make_mock_theta_to_seed(...)         -> theta_to_seed(theta, out_path) writing a seed with the
                                            mock block; speeds derived deterministically from theta
  * a toy forward_many (affine in u with a zero column; 12 rows keyed by the real DDO154 row ids)
    for the batched-adapter equivalence fixtures B1/B2.

Mock conventions used by the fixtures (documented in FIXTURE_NOTES_0463_V001.md):
  theta coordinate 'mock_mode' (float code) selects the mock mode per theta:
      0 ok, 1 exit_nonzero, 2 hang, 3 rss, 4 output, 5 nan, 6 missing_result
  theta coordinate 'mock_sleep_s' overrides the sleep; both are excluded from the speed map.
  speeds[row_k] = 50 + 2k + sum_j 10 (j+1) theta_j (1 + 0.1 k) over the sorted non-mock names.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import os
import shutil
import signal
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone

MODE_CODES = {0: 'ok', 1: 'exit_nonzero', 2: 'hang', 3: 'rss', 4: 'output', 5: 'nan', 6: 'missing_result'}
REGION_PATH_DEFAULT = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                       'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/DDO154_CALIBRATION_OBSERVATION_REGION_V001.json')
REGION_SHA256 = '13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d'
MiB = 1024 * 1024


# ----------------------------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------------------------

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def canonical_or_note(obj):
    """Canonical JSON; if non-finite floats are present fall back to allow_nan and say so."""
    try:
        return canonical(obj), False
    except ValueError:
        return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=True), True


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError('cannot build import spec for %s' % path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def cget(obj, *keys, default=None):
    cur = obj
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, (list, tuple)) and isinstance(k, int) and -len(cur) <= k < len(cur):
            cur = cur[k]
        else:
            return default
    return cur


def is_finite_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))


def count_names(root, filename=None, dirname=None):
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        if filename is not None:
            n += sum(1 for f in filenames if f == filename)
        if dirname is not None:
            n += sum(1 for d in dirnames if d == dirname)
    return n


def listing(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            p = os.path.join(dirpath, f)
            out.append((os.path.relpath(p, root), os.path.getsize(p)))
        for d in dirnames:
            out.append((os.path.relpath(os.path.join(dirpath, d), root) + '/', -1))
    return sorted(out)


def ps_info(pid):
    """Return (alive_or_zombie: bool, stat: str, command: str) for a pid via ps; (False, '', '') if gone."""
    try:
        out = subprocess.run(['ps', '-o', 'pid=,pgid=,stat=,command=', '-p', str(int(pid))],
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception as exc:  # noqa: BLE001
        return False, 'PS_ERROR:%r' % (exc,), ''
    if not out:
        return False, '', ''
    parts = out.split(None, 3)
    stat = parts[2] if len(parts) > 2 else ''
    cmd = parts[3] if len(parts) > 3 else ''
    return True, stat, cmd


def mock_pids_under(campaign_dir):
    """Collect (pid, pgid, path) from every mock start.json under a campaign directory."""
    found = []
    if not os.path.isdir(campaign_dir):
        return found
    for dirpath, dirnames, filenames in os.walk(campaign_dir):
        if 'start.json' in filenames:
            p = os.path.join(dirpath, 'start.json')
            try:
                with open(p, 'r', encoding='utf-8') as fh:
                    d = json.load(fh)
                if isinstance(d, dict) and d.get('schema') == 'MOCK_START_0463_V001':
                    found.append((int(d['pid']), int(d.get('pgid', d['pid'])), p))
            except Exception:  # noqa: BLE001
                continue
    return found


def survey_and_kill_leftover_mocks(campaign_dir):
    """Report mock processes still alive (not reaped) under a campaign, then SIGKILL them.

    Returns {'alive': [...], 'zombie': [...], 'gone': n}.  Killing a mock the fixture itself
    caused to be spawned is cleanup, not deletion.
    """
    rep = {'alive': [], 'zombie': [], 'gone': 0}
    for pid, pgid, path in mock_pids_under(campaign_dir):
        present, stat, cmd = ps_info(pid)
        if not present:
            rep['gone'] += 1
            continue
        if 'mock_worker_0463.py' not in cmd and not stat.startswith('Z'):
            rep['gone'] += 1  # pid reused by an unrelated process; treat the mock as gone
            continue
        if stat.startswith('Z'):
            rep['zombie'].append({'pid': pid, 'stat': stat, 'start_json': path})
            continue
        rep['alive'].append({'pid': pid, 'pgid': pgid, 'stat': stat, 'start_json': path})
        try:
            if pgid == pid:
                os.killpg(pgid, signal.SIGKILL)
            else:
                os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except Exception as exc:  # noqa: BLE001
            rep['alive'][-1]['kill_error'] = repr(exc)
    return rep


class FixtureTimeout(BaseException):
    pass


def _alarm_handler(signum, frame):
    raise FixtureTimeout('fixture wall-time guard fired')


# ----------------------------------------------------------------------------------------------
# fixture-local mock plumbing (per the interface "Fixtures" section)
# ----------------------------------------------------------------------------------------------

def mock_speeds_from_theta(theta, row_ids):
    names = sorted(k for k in theta if not str(k).startswith('mock_'))
    speeds = {}
    for k, rid in enumerate(row_ids):
        val = 50.0 + 2.0 * k
        for j, name in enumerate(names):
            val += 10.0 * (j + 1) * float(theta[name]) * (1.0 + 0.1 * k)
        speeds[rid] = float(val)
    return speeds


def make_mock_theta_to_seed(*, default_mode, default_sleep_s, row_ids, base_seed, call_log):
    """Return theta_to_seed(theta, out_path) -> write_seed-style result (see Module A)."""
    def theta_to_seed(theta, out_path):
        reasons = []
        try:
            out_path = os.fspath(out_path)
        except TypeError:
            return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                    'reasons': ['OUT_PATH_NOT_PATHLIKE']}
        if not isinstance(theta, dict) or not theta:
            return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                    'reasons': ['THETA_NOT_A_NONEMPTY_DICT']}
        for k, v in theta.items():
            if not isinstance(k, str) or not is_finite_number(v):
                reasons.append('THETA_COORD_INVALID:%r' % (k,))
        if reasons:
            return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                    'reasons': reasons}
        if os.path.exists(out_path):
            return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                    'reasons': ['OUT_PATH_EXISTS:%s' % out_path]}
        mode = default_mode
        if 'mock_mode' in theta:
            code = int(round(float(theta['mock_mode'])))
            if code not in MODE_CODES:
                return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                        'reasons': ['MOCK_MODE_CODE_UNKNOWN:%d' % code]}
            mode = MODE_CODES[code]
        sleep_s = float(theta['mock_sleep_s']) if 'mock_sleep_s' in theta else float(default_sleep_s)
        seed = copy.deepcopy(base_seed)
        seed['theta'] = {k: float(theta[k]) for k in sorted(theta)}
        seed['mock'] = {'mode': mode, 'sleep_s': sleep_s, 'speeds': mock_speeds_from_theta(theta, row_ids)}
        data = canonical(seed).encode('utf-8')
        parent = os.path.dirname(out_path)
        try:
            if parent and not os.path.isdir(parent):
                os.makedirs(parent, exist_ok=True)
            with open(out_path, 'xb') as fh:
                fh.write(data)
        except OSError as exc:
            return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                    'reasons': ['SEED_WRITE_FAILED:%r' % (exc,)]}
        digest = sha256_bytes(data)
        call_log.append({'theta_key': canonical(seed['theta']), 'out_path': out_path, 'seed_sha256': digest,
                         'mode': mode, 'sleep_s': sleep_s})
        return {'ok': True, 'seed_sha256': digest, 'path': out_path,
                'changed_fields': [{'pointer': '/theta', 'old': None, 'new': seed['theta']},
                                   {'pointer': '/mock', 'old': None, 'new': seed['mock']}],
                'frozen_field_count': len(base_seed), 'reasons': []}
    return theta_to_seed


def _reject_constant(name):
    raise ValueError('NON_FINITE_CONSTANT:%s' % name)


def mock_result_reader(outdir):
    """forward-style result from <outdir>/result.json in the mock layout."""
    try:
        outdir = os.fspath(outdir)
    except TypeError:
        return {'speeds_km_s': {}, 'valid': False, 'reasons': ['OUTDIR_NOT_PATHLIKE']}
    path = os.path.join(outdir, 'result.json')
    if not os.path.isfile(path):
        return {'speeds_km_s': {}, 'valid': False, 'reasons': ['RESULT_JSON_MISSING:%s' % path]}
    try:
        with open(path, 'rb') as fh:
            raw = fh.read()
        obj = json.loads(raw.decode('utf-8'), parse_constant=_reject_constant)
    except (OSError, ValueError) as exc:
        return {'speeds_km_s': {}, 'valid': False, 'reasons': ['RESULT_JSON_INVALID:%r' % (exc,)]}
    res = obj.get('result') if isinstance(obj, dict) else None
    if not isinstance(res, dict):
        return {'speeds_km_s': {}, 'valid': False, 'reasons': ['RESULT_BLOCK_MISSING']}
    speeds = res.get('speeds_km_s')
    if not isinstance(speeds, dict) or not speeds:
        return {'speeds_km_s': {}, 'valid': False, 'reasons': ['SPEEDS_MISSING']}
    reasons = []
    clean = {}
    for k in sorted(speeds):
        v = speeds[k]
        if not isinstance(k, str) or not is_finite_number(v):
            reasons.append('SPEED_NOT_FINITE:%r' % (k,))
        else:
            clean[k] = float(v)
    if res.get('valid') is not True:
        reasons.append('WORKER_VALID_FLAG_NOT_TRUE')
    if reasons:
        return {'speeds_km_s': {}, 'valid': False, 'reasons': reasons}
    return {'speeds_km_s': clean, 'valid': True, 'reasons': [],
            'provenance': {'result_sha256': sha256_bytes(raw), 'result_path': path,
                           'reader': 'fixtures_0463_c3v001.mock_result_reader'}}


# ----------------------------------------------------------------------------------------------
# toy forward for B1/B2 (affine in u with a zero column)
# ----------------------------------------------------------------------------------------------

TOY_COORDINATES = [
    {'name': 'a_lin', 'transform': 'linear', 'lower': 0.0, 'upper': 2.0, 'role': 'free', 'trial_value': 1.0},
    {'name': 'b_lin', 'transform': 'linear', 'lower': -1.0, 'upper': 1.0, 'role': 'free', 'trial_value': 0.0},
    {'name': 'c_nuis', 'transform': 'linear', 'lower': 0.0, 'upper': 1.0, 'role': 'nuisance', 'trial_value': 0.5},
    {'name': 'd_fixed', 'transform': 'log', 'lower': 0.1, 'upper': 10.0, 'role': 'fixed', 'trial_value': 1.0},
]


def make_toy_forward_many(*, row_ids, observed, rectangles, batch_log):
    a1 = {}
    a2 = {}
    for k, rid in enumerate(row_ids):
        hw = 0.5 * (rectangles[rid][1] - rectangles[rid][0])
        a1[rid] = 4.0 * hw
        a2[rid] = (2.0 * hw) * (1.0 if k % 2 == 0 else -1.0)

    def forward_one(theta):
        if not isinstance(theta, dict):
            return {'speeds_km_s': {}, 'valid': False, 'reasons': ['TOY_THETA_NOT_DICT']}
        try:
            ua = float(theta['a_lin']) / 2.0
            ub = (float(theta['b_lin']) + 1.0) / 2.0
            uc = float(theta['c_nuis'])
        except (KeyError, TypeError, ValueError) as exc:
            return {'speeds_km_s': {}, 'valid': False, 'reasons': ['TOY_COORD_MISSING:%r' % (exc,)]}
        if not all(math.isfinite(x) for x in (ua, ub, uc)):
            return {'speeds_km_s': {}, 'valid': False, 'reasons': ['TOY_COORD_NOT_FINITE']}
        speeds = {}
        for rid in row_ids:
            speeds[rid] = float(observed[rid] + a1[rid] * (ua - 0.5) + a2[rid] * (ub - 0.5) + 0.0 * (uc - 0.5))
        return {'speeds_km_s': speeds, 'valid': True, 'reasons': []}

    def forward_many(thetas=None, **kwargs):
        if kwargs:
            raise TypeError('toy forward_many got unexpected kwargs %r' % sorted(kwargs))
        if thetas is None:
            raise TypeError('toy forward_many needs thetas=')
        thetas = list(thetas)
        batch_log.append(len(thetas))
        return {'ok': True, 'results': [forward_one(t) for t in thetas],
                'campaign': {'status': 'TOY_NO_CAMPAIGN', 'n': len(thetas)}, 'reasons': []}

    return forward_many


# ----------------------------------------------------------------------------------------------
# fixture bookkeeping
# ----------------------------------------------------------------------------------------------

class Fixture:
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.checks = []
        self.numbers = {}
        self.notes = []
        self.status = 'UNTESTED'
        self.error = None
        self.wall_s = None

    def check(self, label, ok, observed=None, expected=None):
        ok = bool(ok)
        rec = {'check': label, 'ok': ok}
        if observed is not None:
            rec['observed'] = observed
        if expected is not None:
            rec['expected'] = expected
        self.checks.append(rec)
        return ok

    def num(self, key, value):
        self.numbers[key] = value
        return value

    def note(self, text):
        self.notes.append(str(text))

    def finalize(self):
        if self.error is not None:
            self.status = 'ERROR'
        elif not self.checks:
            self.status = 'UNTESTED'
        elif all(c['ok'] for c in self.checks):
            self.status = 'PASS'
        else:
            self.status = 'FAIL'

    def as_dict(self):
        return {'name': self.name, 'title': self.title, 'status': self.status, 'wall_s': self.wall_s,
                'n_checks': len(self.checks), 'n_failed_checks': sum(1 for c in self.checks if not c['ok']),
                'checks': self.checks, 'numbers': self.numbers, 'notes': self.notes, 'error': self.error}


class Context:
    def __init__(self):
        self.runner = None
        self.batched = None
        self.engine = None
        self.import_errors = {}
        self.py = sys.executable
        self.worker = None
        self.row_ids = None
        self.observed = None
        self.rectangles = None
        self.run_dir = None
        self.base_seed = None
        self.store = {}  # cross-fixture state (campaign dirs, results)
        self.leftovers = {}
        self.module_pins = {}


def run_fixture(ctx, fx, fn, timeout_s, cleanup_dirs):
    t0 = time.monotonic()
    old = signal.signal(signal.SIGALRM, _alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, float(timeout_s))
    try:
        fn(ctx, fx)
    except FixtureTimeout:
        fx.error = 'FIXTURE_TIMEOUT after %.1f s (the module under test did not return)' % (time.monotonic() - t0)
    except Exception:  # noqa: BLE001
        fx.error = traceback.format_exc()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, old)
    fx.wall_s = round(time.monotonic() - t0, 3)
    for d in cleanup_dirs():
        rep = survey_and_kill_leftover_mocks(d)
        if rep['alive'] or rep['zombie']:
            fx.note('leftover mock processes under %s after the fixture: %s' % (d, canonical(rep)))
            ctx.leftovers[d] = rep
    fx.finalize()
    sys.stdout.write('[%s] %s  %s  (%.1f s)\n' % (fx.status, fx.name, fx.title, fx.wall_s))
    for c in fx.checks:
        if not c['ok']:
            sys.stdout.write('    FAILED CHECK: %s observed=%r expected=%r\n'
                             % (c['check'], c.get('observed'), c.get('expected')))
    if fx.error:
        sys.stdout.write('    ERROR: %s\n' % fx.error.strip().splitlines()[-1])
    sys.stdout.flush()


# ----------------------------------------------------------------------------------------------
# campaign helpers
# ----------------------------------------------------------------------------------------------

def campaign_kwargs(ctx, *, campaign_dir, thetas, theta_to_seed, result_reader, max_workers,
                    per_call_wall_s=60.0, per_call_rss_bytes=2 * 1024 * MiB, per_call_output_bytes=64 * MiB,
                    campaign_wall_s=300.0, resume=False, poll_interval_s=0.25, worker=None):
    return dict(campaign_dir=campaign_dir, python_executable=ctx.py, worker=dict(worker or ctx.worker),
                thetas=thetas, theta_to_seed=theta_to_seed, result_reader=result_reader,
                max_workers=max_workers, per_call_wall_s=per_call_wall_s, per_call_rss_bytes=per_call_rss_bytes,
                per_call_output_bytes=per_call_output_bytes, campaign_wall_s=campaign_wall_s, resume=resume,
                poll_interval_s=poll_interval_s)


def new_tts(ctx, *, mode, sleep_s, log_key):
    log = ctx.store.setdefault('tts_logs', {}).setdefault(log_key, [])
    return make_mock_theta_to_seed(default_mode=mode, default_sleep_s=sleep_s, row_ids=ctx.row_ids,
                                   base_seed=ctx.base_seed, call_log=log)


def call_outdir(call, campaign_dir):
    """Locate the mock's --outdir for a call: from the receipt command if possible, else call_dir/out."""
    rp = call.get('receipt_path') if isinstance(call, dict) else None
    if rp and os.path.isfile(rp):
        try:
            with open(rp, 'r', encoding='utf-8') as fh:
                rec = json.load(fh)
            cmd = rec.get('command') or []
            if '--outdir' in cmd:
                return cmd[cmd.index('--outdir') + 1]
        except Exception:  # noqa: BLE001
            pass
    cd = call.get('call_dir') if isinstance(call, dict) else None
    if cd:
        return os.path.join(cd, 'out')
    return os.path.join(campaign_dir, 'call_%04d' % int(call.get('index', -1)), 'out')


def mock_intervals(calls, campaign_dir):
    """(start_unix, finish_unix) per call from the mock's own start.json/finish.json."""
    ivs = []
    for c in calls:
        od = call_outdir(c, campaign_dir)
        sp = os.path.join(od, 'start.json')
        fp = os.path.join(od, 'finish.json')
        if os.path.isfile(sp) and os.path.isfile(fp):
            with open(sp, 'r', encoding='utf-8') as fh:
                s = json.load(fh)
            with open(fp, 'r', encoding='utf-8') as fh:
                f = json.load(fh)
            ivs.append((float(s['started_unix']), float(f['finished_unix']), int(c.get('index', -1))))
    return ivs


def max_overlap(intervals):
    events = []
    for s, f, _ in intervals:
        events.append((s, 1))
        events.append((f, -1))
    events.sort(key=lambda e: (e[0], e[1]))  # at equal times, finish (-1) before start (+1)
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best


def receipt_hashes(campaign_dir):
    out = {}
    if not os.path.isdir(campaign_dir):
        return out
    for name in sorted(os.listdir(campaign_dir)):
        rp = os.path.join(campaign_dir, name, 'RECEIPT.json')
        if name.startswith('call_') and os.path.isfile(rp):
            out[name] = sha256_file(rp)
    return out


def call_dirs(campaign_dir):
    if not os.path.isdir(campaign_dir):
        return []
    return sorted(n for n in os.listdir(campaign_dir) if n.startswith('call_') and os.path.isdir(os.path.join(campaign_dir, n)))


def status_list(res):
    return [cget(c, 'status') for c in (res.get('calls') or [])] if isinstance(res, dict) else None


def reason_list(res):
    return [cget(c, 'reason') for c in (res.get('calls') or [])] if isinstance(res, dict) else None


def require_runner(ctx, fx):
    if ctx.runner is None:
        fx.check('runner module imported', False, observed=ctx.import_errors.get('campaign_runner_c3v001'))
        return False
    return True


# ----------------------------------------------------------------------------------------------
# fixtures R1..R12
# ----------------------------------------------------------------------------------------------

def fx_R1(ctx, fx):
    if not require_runner(ctx, fx):
        return
    cdir = os.path.join(ctx.run_dir, 'R1_concurrency')
    thetas = [{'alpha': 0.1 * i, 'beta': 1.0 + 0.25 * i} for i in range(8)]
    tts = new_tts(ctx, mode='ok', sleep_s=2.0, log_key='R1')
    kw = campaign_kwargs(ctx, campaign_dir=cdir, thetas=thetas, theta_to_seed=tts, result_reader=mock_result_reader,
                         max_workers=3, per_call_wall_s=30.0, campaign_wall_s=120.0)
    t0 = time.monotonic()
    res = ctx.runner.run_campaign(**kw)
    wall = time.monotonic() - t0
    ctx.store['R1'] = {'campaign_dir': cdir, 'thetas': thetas, 'result': res, 'kwargs': kw}
    fx.num('fixture_wall_s', round(wall, 3))
    fx.num('status', res.get('status'))
    fx.num('n_ok', res.get('n_ok'))
    fx.num('n_failed', res.get('n_failed'))
    fx.num('evaluations_run', res.get('evaluations_run'))
    fx.num('campaign_wall_used_s', res.get('campaign_wall_used_s'))
    fx.num('max_concurrent_observed_by_runner', res.get('max_concurrent_observed'))
    fx.check('ok is True', res.get('ok') is True, observed=res.get('ok'))
    fx.check('status COMPLETE', res.get('status') == 'COMPLETE', observed=res.get('status'))
    calls = res.get('calls') or []
    fx.check('8 call records', len(calls) == 8, observed=len(calls), expected=8)
    fx.check('n_ok == 8', res.get('n_ok') == 8, observed=res.get('n_ok'))
    fx.check('evaluations_run == 8', res.get('evaluations_run') == 8, observed=res.get('evaluations_run'))
    order_ok = all(cget(c, 'index') == i and cget(c, 'theta') == thetas[i] and cget(c, 'theta_key') == canonical(thetas[i])
                   for i, c in enumerate(calls)) and len(calls) == 8
    fx.check('results in theta order (index, theta, theta_key)', order_ok,
             observed=[(cget(c, 'index'), cget(c, 'theta')) for c in calls])
    fx.check('all statuses OK', all(cget(c, 'status') == 'OK' for c in calls) and len(calls) == 8,
             observed=status_list(res))
    dirs_ok = all(os.path.abspath(str(cget(c, 'call_dir'))) == os.path.join(cdir, 'call_%04d' % i) for i, c in enumerate(calls))
    fx.check('call_dir == campaign_dir/call_{index:04d}', dirs_ok, observed=[cget(c, 'call_dir') for c in calls][:2])
    speeds_ok = True
    for i, c in enumerate(calls):
        exp = mock_speeds_from_theta(thetas[i], ctx.row_ids)
        got = cget(c, 'result', 'speeds_km_s')
        if cget(c, 'result', 'valid') is not True or got != exp:
            speeds_ok = False
    fx.check('every result valid and speeds == deterministic expectation from theta', speeds_ok)
    ver = []
    for c in calls:
        rp = cget(c, 'receipt_path')
        v = ctx.runner.verify_receipt(receipt_path=rp) if rp else {'ok': False, 'reasons': ['NO_RECEIPT_PATH']}
        ver.append(bool(v.get('ok')))
    fx.num('receipts_verified', sum(ver))
    fx.check('all 8 receipts verify via verify_receipt', all(ver) and len(ver) == 8, observed=ver)
    ivs = mock_intervals(calls, cdir)
    fx.num('mock_intervals_found', len(ivs))
    mo = max_overlap(ivs)
    fx.num('max_simultaneous_from_mock_timestamps', mo)
    fx.num('mock_run_durations_s', [round(f - s, 3) for s, f, _ in ivs])
    if ivs:
        span = max(f for _, f, _ in ivs) - min(s for s, _, _ in ivs)
        fx.num('mock_span_first_start_to_last_finish_s', round(span, 3))
    fx.check('8 start/finish timestamp pairs found', len(ivs) == 8, observed=len(ivs))
    fx.check('max simultaneous <= max_workers (3)', mo <= 3, observed=mo)
    fx.check('max simultaneous == 3 at some instant', mo == 3, observed=mo)
    fx.check('runner max_concurrent_observed <= 3', isinstance(res.get('max_concurrent_observed'), int) and res.get('max_concurrent_observed') <= 3,
             observed=res.get('max_concurrent_observed'))
    fx.num('wall_s_per_call', [cget(c, 'wall_s') for c in calls])
    fx.num('exit_codes', [cget(c, 'exit_code') for c in calls])
    fx.num('receipt_sha256', receipt_hashes(cdir))


def _single_cap_fixture(ctx, fx, *, label, mode, sleep_s, cap_kwargs, expected_reason, extra):
    if not require_runner(ctx, fx):
        return
    cdir = os.path.join(ctx.run_dir, label)
    thetas = [{'alpha': 0.3, 'beta': 2.0}]
    tts = new_tts(ctx, mode=mode, sleep_s=sleep_s, log_key=label)
    kw = campaign_kwargs(ctx, campaign_dir=cdir, thetas=thetas, theta_to_seed=tts, result_reader=mock_result_reader,
                         max_workers=1, campaign_wall_s=120.0, **cap_kwargs)
    t0 = time.monotonic()
    res = ctx.runner.run_campaign(**kw)
    wall = time.monotonic() - t0
    ctx.store[label] = {'campaign_dir': cdir, 'thetas': thetas, 'result': res, 'kwargs': kw}
    fx.num('fixture_wall_s', round(wall, 3))
    fx.num('status', res.get('status'))
    calls = res.get('calls') or []
    c0 = calls[0] if calls else {}
    fx.num('call_status', cget(c0, 'status'))
    fx.num('call_reason', cget(c0, 'reason'))
    fx.num('call_wall_s', cget(c0, 'wall_s'))
    fx.num('exit_code', cget(c0, 'exit_code'))
    fx.num('max_rss_bytes_observed', cget(c0, 'max_rss_bytes_observed'))
    fx.num('output_bytes', cget(c0, 'output_bytes'))
    fx.check('status COMPLETE (campaign continues after a failed call)', res.get('status') == 'COMPLETE', observed=res.get('status'))
    fx.check('one call record', len(calls) == 1, observed=len(calls))
    fx.check('call status FAILED', cget(c0, 'status') == 'FAILED', observed=cget(c0, 'status'))
    fx.check('reason == %s' % expected_reason, cget(c0, 'reason') == expected_reason, observed=cget(c0, 'reason'))
    fx.check('n_failed == 1', res.get('n_failed') == 1, observed=res.get('n_failed'))
    rp = cget(c0, 'receipt_path')
    fx.check('receipt present', bool(rp) and os.path.isfile(str(rp)), observed=rp)
    if rp and os.path.isfile(str(rp)):
        v = ctx.runner.verify_receipt(receipt_path=rp)
        fx.check('receipt verifies', v.get('ok') is True, observed=v.get('reasons'))
        fx.num('receipt_status', cget(v, 'receipt', 'status'))
        fx.num('receipt_reason', cget(v, 'receipt', 'reason'))
    fx.num('n_out_dirs_in_call_dir', count_names(os.path.join(cdir, 'call_0000'), dirname='out'))
    fx.num('n_receipts_in_call_dir', count_names(os.path.join(cdir, 'call_0000'), filename='RECEIPT.json'))
    fx.num('n_start_json_in_call_dir', count_names(os.path.join(cdir, 'call_0000'), filename='start.json'))
    fx.check('no second attempt: exactly one out/ and one RECEIPT.json and one start.json',
             fx.numbers['n_out_dirs_in_call_dir'] == 1 and fx.numbers['n_receipts_in_call_dir'] == 1
             and fx.numbers['n_start_json_in_call_dir'] == 1)
    extra(res, c0, cdir)


def fx_R2(ctx, fx):
    def extra(res, c0, cdir):
        pids = mock_pids_under(cdir)
        fx.num('mock_pids', [p for p, _, _ in pids])
        gone = True
        details = []
        for pid, pgid, _ in pids:
            present, stat, cmd = ps_info(pid)
            details.append({'pid': pid, 'present': present, 'stat': stat})
            if present and ('mock_worker_0463.py' in cmd or stat.startswith('Z')):
                gone = False
        fx.num('process_survey_after_return', details)
        fx.check('one mock pid recorded', len(pids) == 1, observed=len(pids))
        fx.check('process gone after run_campaign returned (not alive, not zombie)', gone, observed=details)
        w = cget(c0, 'wall_s')
        fx.check('wall_s within [3, 6) s', is_finite_number(w) and 3.0 <= float(w) < 6.0, observed=w)
        fx.check('no result.json written by the hung mock', not os.path.isfile(os.path.join(call_outdir(c0, cdir), 'result.json')))
        fx.check('no finish.json written by the hung mock', not os.path.isfile(os.path.join(call_outdir(c0, cdir), 'finish.json')))
        fx.check('call result is None or invalid', cget(c0, 'result') is None or cget(c0, 'result', 'valid') is not True,
                 observed=cget(c0, 'result'))
    _single_cap_fixture(ctx, fx, label='R2_wall_cap', mode='hang', sleep_s=0.0,
                        cap_kwargs=dict(per_call_wall_s=3.0, poll_interval_s=0.25), expected_reason='WALL_CAP', extra=extra)


def fx_R3(ctx, fx):
    def extra(res, c0, cdir):
        rss = cget(c0, 'max_rss_bytes_observed')
        fx.check('max_rss_bytes_observed > 100 MiB cap', is_finite_number(rss) and rss > 100 * MiB, observed=rss, expected='> %d' % (100 * MiB))
        w = cget(c0, 'wall_s')
        fx.check('killed by the RSS poll before the 8 s hold ended (wall_s < 7)', is_finite_number(w) and float(w) < 7.0, observed=w)
        fx.check('no result.json (mock killed before writing it)', not os.path.isfile(os.path.join(call_outdir(c0, cdir), 'result.json')))
    _single_cap_fixture(ctx, fx, label='R3_rss_cap', mode='rss', sleep_s=8.0,
                        cap_kwargs=dict(per_call_wall_s=20.0, per_call_rss_bytes=100 * MiB, poll_interval_s=0.25),
                        expected_reason='RSS_CAP', extra=extra)


def fx_R4(ctx, fx):
    def extra(res, c0, cdir):
        ob = cget(c0, 'output_bytes')
        fx.check('output_bytes > 10 MiB cap', is_finite_number(ob) and ob > 10 * MiB, observed=ob, expected='> %d' % (10 * MiB))
        w = cget(c0, 'wall_s')
        fx.check('killed by the output poll before the 8 s hold ended (wall_s < 7)', is_finite_number(w) and float(w) < 7.0, observed=w)
        bulk = os.path.join(call_outdir(c0, cdir), 'bulk_output.bin')
        fx.num('bulk_output_bytes_on_disk', os.path.getsize(bulk) if os.path.isfile(bulk) else None)
    _single_cap_fixture(ctx, fx, label='R4_output_cap', mode='output', sleep_s=8.0,
                        cap_kwargs=dict(per_call_wall_s=20.0, per_call_output_bytes=10 * MiB, poll_interval_s=0.25),
                        expected_reason='OUTPUT_CAP', extra=extra)


def fx_R5(ctx, fx):
    if not require_runner(ctx, fx):
        return
    cdir = os.path.join(ctx.run_dir, 'R5_failures')
    thetas = [{'alpha': 0.5, 'beta': 1.5, 'mock_mode': 1.0},   # exit_nonzero
              {'alpha': 0.6, 'beta': 1.5, 'mock_mode': 5.0},   # nan
              {'alpha': 0.7, 'beta': 1.5, 'mock_mode': 6.0}]   # missing_result
    tts = new_tts(ctx, mode='ok', sleep_s=0.2, log_key='R5')
    kw = campaign_kwargs(ctx, campaign_dir=cdir, thetas=thetas, theta_to_seed=tts, result_reader=mock_result_reader,
                         max_workers=3, per_call_wall_s=30.0, campaign_wall_s=60.0)
    res = ctx.runner.run_campaign(**kw)
    ctx.store['R5'] = {'campaign_dir': cdir, 'thetas': thetas, 'result': res, 'kwargs': kw}
    calls = res.get('calls') or []
    fx.num('status', res.get('status'))
    fx.num('statuses', status_list(res))
    fx.num('reasons', reason_list(res))
    fx.num('exit_codes', [cget(c, 'exit_code') for c in calls])
    fx.num('n_failed', res.get('n_failed'))
    fx.check('status COMPLETE', res.get('status') == 'COMPLETE', observed=res.get('status'))
    fx.check('3 call records', len(calls) == 3, observed=len(calls))
    fx.check('all three FAILED', len(calls) == 3 and all(cget(c, 'status') == 'FAILED' for c in calls), observed=status_list(res))
    fx.check('n_failed == 3', res.get('n_failed') == 3, observed=res.get('n_failed'))
    fx.check('exit_nonzero call has exit_code 3', cget(calls, 0, 'exit_code') == 3, observed=cget(calls, 0, 'exit_code'))
    fx.check('nan call: result None or valid False', cget(calls, 1, 'result') is None or cget(calls, 1, 'result', 'valid') is not True,
             observed=cget(calls, 1, 'result'))
    fx.check('nan call: exit_code 0 (failure is the reader, not the process)', cget(calls, 1, 'exit_code') == 0, observed=cget(calls, 1, 'exit_code'))
    fx.check('missing_result call: result None or valid False', cget(calls, 2, 'result') is None or cget(calls, 2, 'result', 'valid') is not True,
             observed=cget(calls, 2, 'result'))
    fx.check('every call has a reason string', all(isinstance(cget(c, 'reason'), str) and cget(c, 'reason') for c in calls) and len(calls) == 3,
             observed=reason_list(res))
    ver = [bool(ctx.runner.verify_receipt(receipt_path=cget(c, 'receipt_path')).get('ok')) if cget(c, 'receipt_path') else False for c in calls]
    fx.check('all three receipts verify', all(ver) and len(ver) == 3, observed=ver)
    fx.num('receipt_sha256', receipt_hashes(cdir))


def fx_R6(ctx, fx):
    if not require_runner(ctx, fx):
        return
    if 'R5' not in ctx.store:
        fx.note('R5 did not run; R6 untested')
        return
    st = ctx.store['R5']
    cdir = st['campaign_dir']
    counts = {}
    for name in call_dirs(cdir):
        d = os.path.join(cdir, name)
        counts[name] = {'out_dirs': count_names(d, dirname='out'), 'receipts': count_names(d, filename='RECEIPT.json'),
                        'start_json': count_names(d, filename='start.json')}
    fx.num('per_call_counts_R5', counts)
    fx.check('R5: each FAILED call_dir has exactly one out/ and one RECEIPT.json and one start.json',
             len(counts) == 3 and all(v == {'out_dirs': 1, 'receipts': 1, 'start_json': 1} for v in counts.values()), observed=counts)
    if 'R2_wall_cap' in ctx.store:
        d2 = os.path.join(ctx.store['R2_wall_cap']['campaign_dir'], 'call_0000')
        c2 = {'out_dirs': count_names(d2, dirname='out'), 'receipts': count_names(d2, filename='RECEIPT.json'),
              'start_json': count_names(d2, filename='start.json')}
        fx.num('per_call_counts_R2', c2)
        fx.check('R2: the WALL_CAP call_dir has exactly one out/ and one RECEIPT.json', c2['out_dirs'] == 1 and c2['receipts'] == 1, observed=c2)
    before = receipt_hashes(cdir)
    listing_before = listing(cdir)
    kw = dict(st['kwargs'])
    kw['resume'] = True
    kw['theta_to_seed'] = new_tts(ctx, mode='ok', sleep_s=0.2, log_key='R6_resume')
    res = ctx.runner.run_campaign(**kw)
    after = receipt_hashes(cdir)
    fx.num('status', res.get('status'))
    fx.num('statuses', status_list(res))
    fx.num('evaluations_run', res.get('evaluations_run'))
    fx.num('n_resumed', res.get('n_resumed'))
    fx.check('resume=True on R5: all RESUMED_FAILED', status_list(res) == ['RESUMED_FAILED'] * 3, observed=status_list(res))
    fx.check('evaluations_run == 0', res.get('evaluations_run') == 0, observed=res.get('evaluations_run'))
    fx.check('theta_to_seed never called on resume', len(ctx.store['tts_logs']['R6_resume']) == 0, observed=len(ctx.store['tts_logs']['R6_resume']))
    fx.check('receipt bytes unchanged by the resume', before == after and len(before) == 3)
    fx.check('no new files under the campaign call dirs', [e for e in listing(cdir) if e[0].startswith('call_')] == [e for e in listing_before if e[0].startswith('call_')])
    fx.check('n_resumed == 3', res.get('n_resumed') == 3, observed=res.get('n_resumed'))
    fx.check('n_failed == 3 on resume', res.get('n_failed') == 3, observed=res.get('n_failed'))


def fx_R7(ctx, fx):
    if not require_runner(ctx, fx):
        return
    if 'R1' not in ctx.store:
        fx.note('R1 did not run; R7 untested')
        return
    st = ctx.store['R1']
    cdir = st['campaign_dir']
    before = receipt_hashes(cdir)
    kw = dict(st['kwargs'])
    kw['resume'] = True
    kw['theta_to_seed'] = new_tts(ctx, mode='ok', sleep_s=2.0, log_key='R7_resume')
    t0 = time.monotonic()
    res = ctx.runner.run_campaign(**kw)
    wall = time.monotonic() - t0
    after = receipt_hashes(cdir)
    ctx.store['R7'] = {'result': res}
    fx.num('fixture_wall_s', round(wall, 3))
    fx.num('status', res.get('status'))
    fx.num('statuses', status_list(res))
    fx.num('evaluations_run', res.get('evaluations_run'))
    fx.num('n_resumed', res.get('n_resumed'))
    fx.check('status COMPLETE', res.get('status') == 'COMPLETE', observed=res.get('status'))
    fx.check('all 8 RESUMED_OK', status_list(res) == ['RESUMED_OK'] * 8, observed=status_list(res))
    fx.check('evaluations_run == 0', res.get('evaluations_run') == 0, observed=res.get('evaluations_run'))
    fx.check('n_resumed == 8', res.get('n_resumed') == 8, observed=res.get('n_resumed'))
    fx.check('theta_to_seed never called on resume', len(ctx.store['tts_logs']['R7_resume']) == 0)
    fx.check('resume took < 5 s (no reruns)', wall < 5.0, observed=round(wall, 3))
    first = [cget(c, 'result') for c in (st['result'].get('calls') or [])]
    second = [cget(c, 'result') for c in (res.get('calls') or [])]
    s1, _ = canonical_or_note(first)
    s2, _ = canonical_or_note(second)
    fx.check('results identical to the first run (canonical JSON of the 8 forward-style results)', s1 == s2 and len(first) == 8)
    fx.num('results_canonical_sha256_first_run', sha256_bytes(s1.encode()))
    fx.num('results_canonical_sha256_resume', sha256_bytes(s2.encode()))
    fx.check('receipt bytes unchanged by the resume', before == after and len(before) == 8)
    fx.check('theta order preserved on resume', all(cget(c, 'index') == i and cget(c, 'theta') == st['thetas'][i]
                                                    for i, c in enumerate(res.get('calls') or [])) and len(res.get('calls') or []) == 8)


def _flip_receipt_byte(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    marker = b'"receipt_sha256":"'
    i = raw.find(marker)
    if i >= 0:
        pos = i + len(marker)
    else:
        pos = len(raw) // 2
    old = raw[pos:pos + 1]
    new = b'1' if old != b'1' else b'2'
    raw2 = raw[:pos] + new + raw[pos + 1:]
    with open(path, 'wb') as fh:
        fh.write(raw2)
    return {'position': pos, 'old_byte': old.decode('latin-1'), 'new_byte': new.decode('latin-1'),
            'sha256_before': sha256_bytes(raw), 'sha256_after': sha256_bytes(raw2), 'bytes': len(raw)}


def fx_R8(ctx, fx):
    if not require_runner(ctx, fx):
        return
    if 'R1' not in ctx.store:
        fx.note('R1 did not run; R8 untested')
        return
    st = ctx.store['R1']
    src = st['campaign_dir']
    # (a) tampered receipt on a copy of the R1 campaign
    cdir_a = os.path.join(ctx.run_dir, 'R8a_tampered_copy_of_R1')
    shutil.copytree(src, cdir_a)
    tampered = os.path.join(cdir_a, 'call_0002', 'RECEIPT.json')
    flip = _flip_receipt_byte(tampered)
    fx.num('tamper', flip)
    v = ctx.runner.verify_receipt(receipt_path=tampered)
    fx.check('(a) verify_receipt on the tampered receipt is ok=False', v.get('ok') is False, observed=v.get('reasons'))
    before = receipt_hashes(cdir_a)
    list_before = listing(os.path.join(cdir_a, 'call_0002'))
    kw = dict(st['kwargs'])
    kw['campaign_dir'] = cdir_a
    kw['resume'] = True
    kw['theta_to_seed'] = new_tts(ctx, mode='ok', sleep_s=2.0, log_key='R8a')
    res = ctx.runner.run_campaign(**kw)
    after = receipt_hashes(cdir_a)
    fx.num('(a) status', res.get('status'))
    fx.num('(a) statuses', status_list(res))
    fx.num('(a) evaluations_run', res.get('evaluations_run'))
    fx.check('(a) tampered call_0002 is DIR_EXISTS_UNVERIFIED on resume', cget(res.get('calls') or [], 2, 'status') == 'DIR_EXISTS_UNVERIFIED',
             observed=cget(res.get('calls') or [], 2, 'status'))
    fx.check('(a) the other 7 calls are RESUMED_OK', [s for i, s in enumerate(status_list(res) or []) if i != 2] == ['RESUMED_OK'] * 7,
             observed=status_list(res))
    fx.check('(a) evaluations_run == 0', res.get('evaluations_run') == 0, observed=res.get('evaluations_run'))
    fx.check('(a) theta_to_seed never called', len(ctx.store['tts_logs']['R8a']) == 0)
    fx.check('(a) every receipt byte-identical after the run (tampered one untouched)', before == after and after.get('call_0002') == flip['sha256_after'])
    fx.check('(a) tampered call_dir listing unchanged', listing(os.path.join(cdir_a, 'call_0002')) == list_before)
    fx.check('(a) tampered call has result None', cget(res.get('calls') or [], 2, 'result') is None, observed=cget(res.get('calls') or [], 2, 'result'))

    # (b) a call_dir without receipt (empty directory) on a fresh campaign
    cdir_b = os.path.join(ctx.run_dir, 'R8b_empty_call_dir')
    os.makedirs(os.path.join(cdir_b, 'call_0001'))
    thetas_b = [{'alpha': 0.11, 'beta': 1.1}, {'alpha': 0.22, 'beta': 1.2}]
    kw_b = campaign_kwargs(ctx, campaign_dir=cdir_b, thetas=thetas_b, theta_to_seed=new_tts(ctx, mode='ok', sleep_s=0.5, log_key='R8b'),
                           result_reader=mock_result_reader, max_workers=2, per_call_wall_s=30.0, campaign_wall_s=60.0, resume=True)
    res_b = ctx.runner.run_campaign(**kw_b)
    fx.num('(b) status', res_b.get('status'))
    fx.num('(b) statuses', status_list(res_b))
    fx.num('(b) evaluations_run', res_b.get('evaluations_run'))
    fx.check('(b) empty call_0001 is DIR_EXISTS_UNVERIFIED', cget(res_b.get('calls') or [], 1, 'status') == 'DIR_EXISTS_UNVERIFIED',
             observed=status_list(res_b))
    fx.check('(b) fresh call_0000 ran OK', cget(res_b.get('calls') or [], 0, 'status') == 'OK', observed=status_list(res_b))
    fx.check('(b) call_0001 still empty (never touched)', os.listdir(os.path.join(cdir_b, 'call_0001')) == [],
             observed=os.listdir(os.path.join(cdir_b, 'call_0001')))
    fx.check('(b) evaluations_run == 1', res_b.get('evaluations_run') == 1, observed=res_b.get('evaluations_run'))

    # (c) resume=False with existing call_dirs: refused per call, never overwritten
    before_c = receipt_hashes(cdir_a)
    list_c = [listing(os.path.join(cdir_a, n)) for n in call_dirs(cdir_a)]
    kw_c = dict(st['kwargs'])
    kw_c['campaign_dir'] = cdir_a
    kw_c['resume'] = False
    kw_c['theta_to_seed'] = new_tts(ctx, mode='ok', sleep_s=2.0, log_key='R8c')
    t0 = time.monotonic()
    res_c = ctx.runner.run_campaign(**kw_c)
    wall_c = time.monotonic() - t0
    after_c = receipt_hashes(cdir_a)
    fx.num('(c) status', res_c.get('status'))
    fx.num('(c) ok', res_c.get('ok'))
    fx.num('(c) statuses', status_list(res_c))
    fx.num('(c) evaluations_run', res_c.get('evaluations_run'))
    fx.num('(c) wall_s', round(wall_c, 3))
    fx.check('(c) resume=False: every existing call is DIR_EXISTS_UNVERIFIED', status_list(res_c) == ['DIR_EXISTS_UNVERIFIED'] * 8,
             observed=status_list(res_c))
    fx.check('(c) evaluations_run == 0', res_c.get('evaluations_run') == 0, observed=res_c.get('evaluations_run'))
    fx.check('(c) theta_to_seed never called', len(ctx.store['tts_logs']['R8c']) == 0)
    fx.check('(c) receipts byte-identical (never overwritten)', before_c == after_c)
    fx.check('(c) call_dir listings unchanged', [listing(os.path.join(cdir_a, n)) for n in call_dirs(cdir_a)] == list_c)
    fx.check('(c) took < 5 s (nothing ran)', wall_c < 5.0, observed=round(wall_c, 3))


def fx_R9(ctx, fx):
    if not require_runner(ctx, fx):
        return
    cdir = os.path.join(ctx.run_dir, 'R9_campaign_cap')
    thetas = [{'alpha': 0.05 * i, 'beta': 3.0} for i in range(6)]
    tts = new_tts(ctx, mode='ok', sleep_s=2.0, log_key='R9')
    kw = campaign_kwargs(ctx, campaign_dir=cdir, thetas=thetas, theta_to_seed=tts, result_reader=mock_result_reader,
                         max_workers=2, per_call_wall_s=30.0, campaign_wall_s=3.0, poll_interval_s=0.25)
    t0 = time.monotonic()
    res = ctx.runner.run_campaign(**kw)
    wall = time.monotonic() - t0
    ctx.store['R9'] = {'campaign_dir': cdir, 'result': res}
    calls = res.get('calls') or []
    fx.num('fixture_wall_s', round(wall, 3))
    fx.num('status', res.get('status'))
    fx.num('statuses', status_list(res))
    fx.num('n_ok', res.get('n_ok'))
    fx.num('n_not_started', res.get('n_not_started'))
    fx.num('campaign_wall_used_s', res.get('campaign_wall_used_s'))
    fx.num('evaluations_run', res.get('evaluations_run'))
    fx.check('status CAMPAIGN_CAP', res.get('status') == 'CAMPAIGN_CAP', observed=res.get('status'))
    fx.check('some NOT_STARTED (n_not_started >= 1)', isinstance(res.get('n_not_started'), int) and res.get('n_not_started') >= 1,
             observed=res.get('n_not_started'))
    fx.check('6 call records in theta order', len(calls) == 6 and all(cget(c, 'theta') == thetas[i] for i, c in enumerate(calls)),
             observed=len(calls))
    fx.check('started calls finished OK under their own caps (no kills)',
             all(cget(c, 'status') in ('OK', 'NOT_STARTED') for c in calls) and len(calls) == 6, observed=status_list(res))
    fx.check('n_ok + n_not_started == 6', (res.get('n_ok') or 0) + (res.get('n_not_started') or 0) == 6,
             observed=[res.get('n_ok'), res.get('n_not_started')])
    ns_dirs = [os.path.isdir(os.path.join(cdir, 'call_%04d' % i)) for i, c in enumerate(calls) if cget(c, 'status') == 'NOT_STARTED']
    fx.check('NOT_STARTED calls have no call_dir on disk', not any(ns_dirs), observed=ns_dirs)
    fx.check('NOT_STARTED calls have receipt_path None and result None',
             all(cget(c, 'receipt_path') is None and cget(c, 'result') is None for c in calls if cget(c, 'status') == 'NOT_STARTED'))
    fx.check('NOT_STARTED calls are the trailing ones (no new start after the cap)',
             status_list(res) == sorted(status_list(res) or [], key=lambda s: 0 if s == 'OK' else 1), observed=status_list(res))
    ivs = mock_intervals(calls, cdir)
    fx.num('max_simultaneous_from_mock_timestamps', max_overlap(ivs))
    fx.check('max simultaneous <= 2', max_overlap(ivs) <= 2, observed=max_overlap(ivs))
    fx.check('campaign_wall_used_s >= 3', is_finite_number(res.get('campaign_wall_used_s')) and res.get('campaign_wall_used_s') >= 3.0,
             observed=res.get('campaign_wall_used_s'))


def fx_R10(ctx, fx):
    if not require_runner(ctx, fx):
        return
    thetas = [{'alpha': 0.1, 'beta': 1.0}]
    # (a) max_workers 13
    cdir_a = os.path.join(ctx.run_dir, 'R10a_max_workers_13')
    kw = campaign_kwargs(ctx, campaign_dir=cdir_a, thetas=thetas, theta_to_seed=new_tts(ctx, mode='ok', sleep_s=0.2, log_key='R10a'),
                         result_reader=mock_result_reader, max_workers=13)
    res = ctx.runner.run_campaign(**kw)
    fx.num('(a) status', res.get('status'))
    fx.num('(a) reasons', res.get('reasons'))
    fx.check('(a) max_workers 13 -> status REFUSED', res.get('status') == 'REFUSED', observed=res.get('status'))
    fx.check('(a) ok is False', res.get('ok') is False, observed=res.get('ok'))
    fx.check('(a) nothing started (no call_* dirs, theta_to_seed not called)',
             call_dirs(cdir_a) == [] and len(ctx.store['tts_logs']['R10a']) == 0, observed=call_dirs(cdir_a))
    # (a2) informational: max_workers 0
    cdir_a2 = os.path.join(ctx.run_dir, 'R10a2_max_workers_0')
    kw = campaign_kwargs(ctx, campaign_dir=cdir_a2, thetas=thetas, theta_to_seed=new_tts(ctx, mode='ok', sleep_s=0.2, log_key='R10a2'),
                         result_reader=mock_result_reader, max_workers=0)
    res = ctx.runner.run_campaign(**kw)
    fx.num('(a2) max_workers 0 status', res.get('status'))
    fx.check('(a2) max_workers 0 -> REFUSED, nothing started', res.get('status') == 'REFUSED' and call_dirs(cdir_a2) == [],
             observed=res.get('status'))
    # (b) wrong worker sha
    cdir_b = os.path.join(ctx.run_dir, 'R10b_wrong_worker_sha')
    bad_worker = dict(ctx.worker)
    h = bad_worker['worker_sha256']
    bad_worker['worker_sha256'] = h[:-1] + ('0' if h[-1] != '0' else '1')
    kw = campaign_kwargs(ctx, campaign_dir=cdir_b, thetas=thetas, theta_to_seed=new_tts(ctx, mode='ok', sleep_s=0.2, log_key='R10b'),
                         result_reader=mock_result_reader, max_workers=1, worker=bad_worker)
    res = ctx.runner.run_campaign(**kw)
    fx.num('(b) status', res.get('status'))
    fx.num('(b) reasons', res.get('reasons'))
    fx.check('(b) wrong worker sha -> REFUSED', res.get('status') == 'REFUSED', observed=res.get('status'))
    fx.check('(b) nothing started', call_dirs(cdir_b) == [] and len(ctx.store['tts_logs']['R10b']) == 0, observed=call_dirs(cdir_b))
    # (c) relative campaign_dir
    rel = 'fixtures0463_relative_campaign_dir_R10c'
    kw = campaign_kwargs(ctx, campaign_dir=rel, thetas=thetas, theta_to_seed=new_tts(ctx, mode='ok', sleep_s=0.2, log_key='R10c'),
                         result_reader=mock_result_reader, max_workers=1)
    res = ctx.runner.run_campaign(**kw)
    fx.num('(c) status', res.get('status'))
    fx.num('(c) reasons', res.get('reasons'))
    fx.check('(c) relative campaign_dir -> REFUSED', res.get('status') == 'REFUSED', observed=res.get('status'))
    fx.check('(c) no directory created in cwd or scratch',
             not os.path.exists(os.path.join(os.getcwd(), rel)) and not os.path.exists(os.path.join(ctx.run_dir, rel))
             and len(ctx.store['tts_logs']['R10c']) == 0)
    fx.check('(c) refused campaign reports calls empty or all NOT_STARTED',
             (res.get('calls') in (None, [])) or all(cget(c, 'status') == 'NOT_STARTED' for c in res.get('calls')), observed=status_list(res))


def fx_R11(ctx, fx):
    if not require_runner(ctx, fx):
        return
    cdir = os.path.join(ctx.run_dir, 'R11_forward_many')
    thetas = [{'alpha': 0.1, 'beta': 1.0, 'mock_mode': 0.0, 'mock_sleep_s': 1.2},
              {'alpha': 0.2, 'beta': 1.0, 'mock_mode': 0.0, 'mock_sleep_s': 0.3},
              {'alpha': 0.3, 'beta': 1.0, 'mock_mode': 1.0, 'mock_sleep_s': 0.1},
              {'alpha': 0.4, 'beta': 1.0, 'mock_mode': 0.0, 'mock_sleep_s': 0.6}]
    kw = campaign_kwargs(ctx, campaign_dir=cdir, thetas=thetas, theta_to_seed=new_tts(ctx, mode='ok', sleep_s=0.5, log_key='R11'),
                         result_reader=mock_result_reader, max_workers=4, per_call_wall_s=30.0, campaign_wall_s=60.0)
    res = ctx.runner.forward_many(**kw)
    results = res.get('results')
    fx.num('ok', res.get('ok'))
    fx.num('reasons', res.get('reasons'))
    fx.num('campaign_status', cget(res, 'campaign', 'status'))
    fx.num('campaign_statuses', status_list(res.get('campaign') or {}))
    fx.check('results is a list of 4', isinstance(results, list) and len(results) == 4, observed=type(results).__name__ if results is not None else None)
    results = results if isinstance(results, list) else []
    shape_ok = all(isinstance(r, dict) and isinstance(r.get('speeds_km_s'), dict) and isinstance(r.get('valid'), bool)
                   and isinstance(r.get('reasons'), list) for r in results) and len(results) == 4
    fx.check('every result is forward-style {speeds_km_s: dict, valid: bool, reasons: list}', shape_ok)
    fx.check('campaign output present with 4 call records', len(cget(res, 'campaign', 'calls', default=[]) or []) == 4)
    ok_idx = [0, 1, 3]
    speeds_ok = all(cget(results, i, 'valid') is True and cget(results, i, 'speeds_km_s') == mock_speeds_from_theta(thetas[i], ctx.row_ids)
                    for i in ok_idx) and len(results) == 4
    fx.check('results[0,1,3] valid with speeds == expectation from their own theta (theta order despite completion order 2,1,3,0)', speeds_ok)
    fx.check('results[i] carry exactly the 12 row ids', all(sorted(cget(results, i, 'speeds_km_s', default={})) == sorted(ctx.row_ids) for i in ok_idx) and len(results) == 4)
    fx.check('results[2] (exit_nonzero) valid False', cget(results, 2, 'valid') is False, observed=cget(results, 2))
    fx.check('results[2] reasons non-empty', bool(cget(results, 2, 'reasons')), observed=cget(results, 2, 'reasons'))
    fx.num('completion_order_by_mock_finish', [i for _, _, i in sorted(mock_intervals(cget(res, 'campaign', 'calls', default=[]) or [], cdir), key=lambda t: t[1])])
    fx.num('n_ok', cget(res, 'campaign', 'n_ok'))
    fx.num('n_failed', cget(res, 'campaign', 'n_failed'))


def _pins_in(obj, acc):
    """Collect every {path, sha256} pair found anywhere in a receipt."""
    if isinstance(obj, dict):
        if isinstance(obj.get('path'), str) and isinstance(obj.get('sha256'), str):
            acc.append((obj['path'], obj['sha256']))
        for v in obj.values():
            _pins_in(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            _pins_in(v, acc)
    return acc


def fx_R12(ctx, fx):
    if not require_runner(ctx, fx):
        return
    if 'R1' not in ctx.store:
        fx.note('R1 did not run; R12 untested')
        return
    st = ctx.store['R1']
    call = (st['result'].get('calls') or [{}])[0]
    rp = cget(call, 'receipt_path')
    fx.check('receipt_path exists', bool(rp) and os.path.isfile(str(rp)), observed=rp)
    if not (rp and os.path.isfile(str(rp))):
        return
    with open(rp, 'rb') as fh:
        raw = fh.read()
    rec = json.loads(raw.decode('utf-8'))
    v = ctx.runner.verify_receipt(receipt_path=rp)
    fx.check('verify_receipt ok', v.get('ok') is True, observed=v.get('reasons'))
    pins = _pins_in(rec, [])
    pin_map = {}
    for p, s in pins:
        pin_map.setdefault(os.path.abspath(p), set()).add(s)
    fx.num('pins_found', [{'path': p, 'sha256': s} for p, s in pins])
    w = ctx.worker
    for label, pkey, skey in (('worker', 'worker_path', 'worker_sha256'), ('solver', 'solver_path', 'solver_sha256'),
                              ('checkpoint_module', 'checkpoint_module_path', 'checkpoint_module_sha256')):
        got = pin_map.get(os.path.abspath(w[pkey]), set())
        fx.check('%s pin recorded with the sha256 of its bytes' % label, w[skey] in got and sha256_file(w[pkey]) == w[skey], observed=sorted(got), expected=w[skey])
    py_abs = os.path.abspath(ctx.py)
    py_pin = pin_map.get(py_abs, set())
    fx.num('python_executable_pin_sha256', sorted(py_pin))
    fx.check('fourth pin: python_executable path with a sha256 recorded (and it matches the binary bytes)',
             bool(py_pin) and sha256_file(py_abs) in py_pin, observed=sorted(py_pin))
    seed_path = cget(rec, 'seed', 'path')
    seed_sha = cget(rec, 'seed', 'sha256')
    fx.check('seed sha recorded and equals sha256 of seed.json bytes', isinstance(seed_path, str) and os.path.isfile(seed_path)
             and sha256_file(seed_path) == seed_sha, observed=seed_sha)
    rj_path = cget(rec, 'result_json', 'path')
    rj_sha = cget(rec, 'result_json', 'sha256')
    fx.check('result_json sha re-verifies from bytes', isinstance(rj_path, str) and os.path.isfile(rj_path) and sha256_file(rj_path) == rj_sha,
             observed=rj_sha)
    recorded = rec.get('receipt_sha256')
    body = {k: val for k, val in rec.items() if k != 'receipt_sha256'}
    cj, nan_note = canonical_or_note(body)
    recomputed = sha256_bytes(cj.encode('utf-8'))
    fx.num('receipt_sha256_recorded', recorded)
    fx.num('receipt_sha256_recomputed', recomputed)
    fx.check('receipt self-hash == sha256(canonical JSON with receipt_sha256 absent)', recorded == recomputed and not nan_note)
    fx.check('receipt file bytes are canonical JSON', raw == canonical(rec).encode('utf-8'))
    fx.check('theta_key == canonical(theta)', rec.get('theta_key') == canonical(rec.get('theta')), observed=rec.get('theta_key'))
    fx.check('command is a list containing the exact real argument names',
             isinstance(rec.get('command'), list) and all(a in rec['command'] for a in
                                                          ('--seed', '--seed-sha256', '--solver', '--solver-sha256', '--checkpoint-module',
                                                           '--checkpoint-module-sha256', '--outdir', '--checkpoint-directory', '--start-iteration')),
             observed=rec.get('command'))
    fx.check('command starts with python_executable -I -B worker', isinstance(rec.get('command'), list) and len(rec['command']) >= 4
             and rec['command'][1:3] == ['-I', '-B'] and os.path.abspath(rec['command'][3]) == os.path.abspath(w['worker_path']), observed=(rec.get('command') or [])[:4])
    fx.check('receipt seed sha == --seed-sha256 on the command', isinstance(rec.get('command'), list) and '--seed-sha256' in rec['command']
             and rec['command'][rec['command'].index('--seed-sha256') + 1] == seed_sha)
    for key in ('index', 'theta', 'theta_key', 'seed', 'command', 'started_utc', 'finished_utc', 'wall_s', 'exit_code', 'reason',
                'max_rss_bytes_observed', 'output_bytes', 'result_json', 'result', 'status', 'receipt_sha256'):
        fx.check('receipt has key %s' % key, key in rec)
    fx.num('receipt_status', rec.get('status'))
    fx.num('receipt_exit_code', rec.get('exit_code'))
    fx.num('receipt_max_rss_bytes_observed', rec.get('max_rss_bytes_observed'))
    fx.num('receipt_output_bytes', rec.get('output_bytes'))


# ----------------------------------------------------------------------------------------------
# B1/B2 batched-adapter equivalence
# ----------------------------------------------------------------------------------------------

def _engine_kwargs(u_seed):
    return dict(coordinates=copy.deepcopy(TOY_COORDINATES), observation_region_path=REGION_PATH_DEFAULT,
                observation_region_sha256=REGION_SHA256, u_seed=list(u_seed), budget=400, rel_step=0.05, min_step=1e-4,
                max_halvings=4, null_tolerance=1e-3, repair_iterations=6, max_repair_step=0.5, march_step=0.05,
                bisection_steps=6, design_count=24, rng_seed=7)


def _batched_equivalence(ctx, fx, *, u_seed, label):
    if ctx.engine is None:
        fx.check('engine module imported', False, observed=ctx.import_errors.get('calibration_region_engine_c3v001'))
        return
    if ctx.batched is None:
        fx.check('batched adapter module imported', False, observed=ctx.import_errors.get('batched_engine_adapter_c3v001'))
        return
    seq_batches = []
    fm_seq = make_toy_forward_many(row_ids=ctx.row_ids, observed=ctx.observed, rectangles=ctx.rectangles, batch_log=seq_batches)

    def forward_seq(theta):
        return fm_seq(thetas=[theta])['results'][0]

    kw = _engine_kwargs(u_seed)
    t0 = time.monotonic()
    seq = ctx.engine.run_calibration_region(forward=forward_seq, **kw)
    t_seq = time.monotonic() - t0
    fx.num('sequential_ok', seq.get('ok'))
    fx.num('sequential_status', seq.get('status'))
    fx.num('sequential_evaluations_used', seq.get('evaluations_used'))
    fx.num('sequential_forward_many_calls', len(seq_batches))
    fx.num('sequential_wall_s', round(t_seq, 3))
    fx.num('sequential_reasons', seq.get('reasons'))
    fx.num('seed_admitted', cget(seq, 'jacobian', 'seed_admitted'))
    fx.num('identified_directions', cget(seq, 'identifiability', 'identified'))
    fx.num('near_null_directions', cget(seq, 'identifiability', 'near_null'))
    fx.num('exploration_status', cget(seq, 'exploration', 'status'))
    fx.num('admitted_points', len(cget(seq, 'exploration', 'admitted_points', default=[]) or []))
    fx.num('rejected_points', len(cget(seq, 'exploration', 'rejected_points', default=[]) or []))
    fx.check('sequential engine run ok and COMPLETE', seq.get('ok') is True and seq.get('status') == 'COMPLETE',
             observed=[seq.get('ok'), seq.get('status'), seq.get('reasons')])
    fx.check('toy has exactly one near-null direction (zero column)', cget(seq, 'identifiability', 'near_null') is not None
             and len(cget(seq, 'identifiability', 'near_null')) == 1, observed=cget(seq, 'identifiability', 'near_null'))
    seq_json, seq_nan = canonical_or_note(seq)
    fx.num('sequential_result_sha256', sha256_bytes(seq_json.encode('utf-8')))

    bat_batches = []
    fm_bat = make_toy_forward_many(row_ids=ctx.row_ids, observed=ctx.observed, rectangles=ctx.rectangles, batch_log=bat_batches)
    mc = ctx.batched.make_cache()
    fx.check('make_cache ok', mc.get('ok') is True, observed=mc.get('reasons'))
    cache = mc.get('cache')
    stats = {}
    t0 = time.monotonic()
    bat = ctx.batched.run_calibration_region_batched(engine=ctx.engine, forward_many=fm_bat, cache=cache, stats=stats,
                                                     engine_sha256=ctx.module_pins['calibration_region_engine_c3v001']['sha256'],
                                                     **_engine_kwargs(u_seed))
    t_bat = time.monotonic() - t0
    fx.num('batched_ok', bat.get('ok'))
    fx.num('batched_reasons', bat.get('reasons'))
    fx.num('batched_wall_s', round(t_bat, 3))
    fx.num('batching', bat.get('batching'))
    fx.num('toy_forward_many_batch_sizes_batched', list(bat_batches))
    fx.num('toy_forward_many_batches_batched', len(bat_batches))
    fx.num('toy_thetas_evaluated_batched', sum(bat_batches))
    fx.num('stats', {k: (v if isinstance(v, (int, float, str, bool, type(None))) else str(v)) for k, v in stats.items()})
    fx.check('batched ok', bat.get('ok') is True, observed=bat.get('reasons'))
    er = bat.get('engine_result')
    fx.check('engine_result present', isinstance(er, dict))
    bat_json, bat_nan = canonical_or_note(er if isinstance(er, dict) else {})
    fx.num('batched_engine_result_sha256', sha256_bytes(bat_json.encode('utf-8')))
    fx.check('canonical JSON of engine results identical (sequential vs batched)', seq_json == bat_json and not seq_nan and not bat_nan)
    if seq_json != bat_json and isinstance(er, dict):
        diffs = [k for k in sorted(set(seq) | set(er)) if canonical_or_note(seq.get(k))[0] != canonical_or_note(er.get(k))[0]]
        fx.num('differing_top_level_keys', diffs)
        if 'evaluation_log' in diffs:
            la = seq.get('evaluation_log') or []
            lb = er.get('evaluation_log') or []
            fx.num('evaluation_log_lengths', [len(la), len(lb)])
            first = next((i for i in range(min(len(la), len(lb))) if canonical_or_note(la[i])[0] != canonical_or_note(lb[i])[0]), None)
            fx.num('first_differing_log_index', first)
            if first is not None:
                fx.num('first_diff_sequential', la[first])
                fx.num('first_diff_batched', lb[first])
    rnc = cget(bat, 'batching', 'replay_new_calls')
    fx.check('replay_new_calls == 0', rnc == 0, observed=rnc)
    batches = cget(bat, 'batching', 'batches')
    fx.check('batching.batches is a non-empty list of {purpose, n_requested, n_fetched}',
             isinstance(batches, list) and len(batches) >= 1 and all(isinstance(b, dict) and {'purpose', 'n_requested', 'n_fetched'} <= set(b) for b in batches),
             observed=batches)
    fx.check('toy forward_many saw fewer calls than the sequential run (batching happened)', len(bat_batches) < len(seq_batches),
             observed=[len(bat_batches), len(seq_batches)])
    fx.check('at least one toy batch had size > 1', any(n > 1 for n in bat_batches), observed=bat_batches)
    fx.check('evaluations_used equal', seq.get('evaluations_used') == cget(er, 'evaluations_used'),
             observed=[seq.get('evaluations_used'), cget(er, 'evaluations_used')])
    fx.num('cache_hits', cget(bat, 'batching', 'cache_hits'))
    fx.num('cache_misses', cget(bat, 'batching', 'cache_misses'))
    fx.num('sequential_fallbacks', cget(bat, 'batching', 'sequential_fallbacks'))


def fx_B1(ctx, fx):
    _batched_equivalence(ctx, fx, u_seed=[0.5, 0.5, 0.5], label='B1')


def fx_B2(ctx, fx):
    _batched_equivalence(ctx, fx, u_seed=[0.95, 0.5, 0.5], label='B2')
    fx.check('B2 seed point not admitted (repair path exercised)', fx.numbers.get('seed_admitted') is False, observed=fx.numbers.get('seed_admitted'))


# ----------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------

FIXTURES = [
    ('R1', 'concurrency limit, theta order, receipts verify', fx_R1, 90.0),
    ('R2', 'per-call wall cap (hang)', fx_R2, 45.0),
    ('R3', 'per-call RSS cap', fx_R3, 45.0),
    ('R4', 'per-call output cap', fx_R4, 60.0),
    ('R5', 'exit_nonzero / nan / missing_result -> FAILED', fx_R5, 45.0),
    ('R6', 'no retry; resume gives RESUMED_FAILED', fx_R6, 45.0),
    ('R7', 'resumption by verified receipt (RESUMED_OK, identical results)', fx_R7, 45.0),
    ('R8', 'tampered receipt / empty call_dir / resume=False refusal', fx_R8, 90.0),
    ('R9', 'campaign wall cap -> CAMPAIGN_CAP with NOT_STARTED', fx_R9, 60.0),
    ('R10', 'refusals: max_workers 13, wrong worker sha, relative campaign_dir', fx_R10, 30.0),
    ('R11', 'forward_many shapes and order', fx_R11, 45.0),
    ('R12', 'pins in receipts', fx_R12, 20.0),
    ('B1', 'batched adapter == sequential engine (admitted seed)', fx_B1, 120.0),
    ('B2', 'batched adapter == sequential engine (non-admitted seed, repair path)', fx_B2, 120.0),
]


def main(argv):
    ap = argparse.ArgumentParser(prog='fixtures_0463_c3v001.py')
    ap.add_argument('artifact_dir_0463')
    ap.add_argument('artifact_dir_0462')
    ap.add_argument('scratch_dir')
    ap.add_argument('--results-out', default=None)
    ap.add_argument('--only', default=None, help='comma-separated fixture names to run')
    args = ap.parse_args(argv)

    a63 = os.path.abspath(args.artifact_dir_0463)
    a62 = os.path.abspath(args.artifact_dir_0462)
    scratch = os.path.abspath(args.scratch_dir)
    os.makedirs(scratch, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = os.path.join(scratch, 'run_%s_%d' % (stamp, os.getpid()))
    os.makedirs(run_dir)

    ctx = Context()
    ctx.run_dir = run_dir
    sys.stdout.write('fixtures_0463_c3v001: run_dir=%s python=%s\n' % (run_dir, ctx.py))

    # placeholders for the solver / checkpoint-module pins of the mock
    ph = os.path.join(run_dir, 'placeholders')
    os.makedirs(ph)
    solver_path = os.path.join(ph, 'mock_solver_placeholder.py')
    ckpt_path = os.path.join(ph, 'mock_checkpoint_placeholder.py')
    with open(solver_path, 'w', encoding='utf-8') as fh:
        fh.write('# placeholder solver module for mock_worker_0463 fixtures (never imported)\nSOLVER_PLACEHOLDER = True\n')
    with open(ckpt_path, 'w', encoding='utf-8') as fh:
        fh.write('# placeholder checkpoint module for mock_worker_0463 fixtures (never imported)\nCHECKPOINT_PLACEHOLDER = True\n')
    mock_path = os.path.join(a63, 'mock_worker_0463.py')
    # Route-A style command template (the real DDO/NGC workers' argparse); the
    # runner itself hard-codes no command line (0465): the caller supplies it.
    ROUTE_A_COMMAND_TEMPLATE = ['{python}', '-I', '-B', '{worker}',
                               '--seed', '{seed}', '--seed-sha256', '{seed_sha256}',
                               '--solver', '{solver}', '--solver-sha256', '{solver_sha256}',
                               '--checkpoint-module', '{checkpoint_module}',
                               '--checkpoint-module-sha256', '{checkpoint_module_sha256}',
                               '--outdir', '{outdir}', '--checkpoint-directory', '{checkpoint_dir}',
                               '--start-iteration', '{start_iteration}']
    ctx.worker = {'worker_path': mock_path, 'worker_sha256': sha256_file(mock_path),
                  'solver_path': solver_path, 'solver_sha256': sha256_file(solver_path),
                  'checkpoint_module_path': ckpt_path, 'checkpoint_module_sha256': sha256_file(ckpt_path),
                  'start_iteration': 0, 'command_template': ROUTE_A_COMMAND_TEMPLATE}
    ctx.base_seed = {'schema': 'MOCK_SEED_0463_V001', 'frozen_a': 1.0, 'frozen_b': [1, 2, 3], 'frozen_c': {'x': 'y'},
                     'frozen_note': 'every field except theta and mock is frozen'}

    # modules by file path
    for name, d in (('campaign_runner_c3v001', a63), ('batched_engine_adapter_c3v001', a63), ('calibration_region_engine_c3v001', a62)):
        path = os.path.join(d, name + '.py')
        pin = {'path': path, 'exists': os.path.isfile(path), 'sha256': sha256_file(path) if os.path.isfile(path) else None,
               'import_ok': False, 'error': None}
        if pin['exists']:
            try:
                mod = load_module(name, path)
                pin['import_ok'] = True
                setattr(ctx, {'campaign_runner_c3v001': 'runner', 'batched_engine_adapter_c3v001': 'batched',
                              'calibration_region_engine_c3v001': 'engine'}[name], mod)
            except Exception:  # noqa: BLE001
                pin['error'] = traceback.format_exc()
                ctx.import_errors[name] = pin['error'].strip().splitlines()[-1]
        else:
            ctx.import_errors[name] = 'MODULE_FILE_MISSING:%s' % path
        ctx.module_pins[name] = pin
        sys.stdout.write('module %s: exists=%s import_ok=%s sha256=%s\n' % (name, pin['exists'], pin['import_ok'], pin['sha256']))

    # region rows (DDO154 calibration region; no NGC3198 data is touched)
    region_sha = sha256_file(REGION_PATH_DEFAULT)
    if region_sha != REGION_SHA256:
        sys.stdout.write('REGION PIN MISMATCH %s != %s; aborting\n' % (region_sha, REGION_SHA256))
        return 2
    with open(REGION_PATH_DEFAULT, 'r', encoding='utf-8') as fh:
        region = json.load(fh)
    ctx.row_ids = [r['id'] for r in region['rows']]
    ctx.observed = {r['id']: float(r['observed_speed_km_s']) for r in region['rows']}
    ctx.rectangles = {r['id']: [float(r['conditional_random_acceptance_low_km_s']), float(r['conditional_random_acceptance_high_km_s'])]
                      for r in region['rows']}
    assert len(ctx.row_ids) == 12, ctx.row_ids

    only = set(s.strip() for s in args.only.split(',')) if args.only else None
    fixtures = []
    t_all = time.monotonic()
    for name, title, fn, timeout_s in FIXTURES:
        fx = Fixture(name, title)
        if only is not None and name not in only:
            fx.note('skipped by --only')
            fx.finalize()
            fixtures.append(fx)
            continue
        run_fixture(ctx, fx, fn, timeout_s, lambda: [os.path.join(ctx.run_dir, d) for d in os.listdir(ctx.run_dir) if d != 'placeholders'])
        fixtures.append(fx)
    total_wall = time.monotonic() - t_all

    summary = {s: sum(1 for f in fixtures if f.status == s) for s in ('PASS', 'FAIL', 'ERROR', 'UNTESTED')}
    out = {
        'schema': 'FIXTURE_RESULTS_0463_V001',
        'created_utc': now_iso(),
        'fixture_script': {'path': os.path.abspath(__file__), 'sha256': sha256_file(os.path.abspath(__file__))},
        'mock_worker': {'path': mock_path, 'sha256': ctx.worker['worker_sha256']},
        'python_executable': ctx.py,
        'python_version': sys.version,
        'artifact_dir_0463': a63, 'artifact_dir_0462': a62, 'scratch_run_dir': run_dir,
        'module_pins': ctx.module_pins,
        'placeholders': {'solver': {'path': solver_path, 'sha256': ctx.worker['solver_sha256']},
                         'checkpoint_module': {'path': ckpt_path, 'sha256': ctx.worker['checkpoint_module_sha256']}},
        'region': {'path': REGION_PATH_DEFAULT, 'sha256': region_sha, 'row_ids': ctx.row_ids},
        'toy_coordinates': TOY_COORDINATES,
        'total_wall_s': round(total_wall, 3),
        'summary': summary,
        'all_pass': summary['FAIL'] == 0 and summary['ERROR'] == 0 and summary['PASS'] == len(FIXTURES),
        'leftover_mock_processes_after_fixtures': ctx.leftovers,
        'fixtures': [f.as_dict() for f in fixtures],
        'prohibitions_respected': {'real_workers_run': False, 'ngc3198_velocity_read': False, 'network': False, 'deletion': False,
                                   'modules_under_test_edited': False},
    }
    results_out = args.results_out or os.path.join(a63, 'FIXTURE_RESULTS_0463_V001.json')
    text, nan_note = canonical_or_note(out)
    with open(results_out, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(out, sort_keys=True, indent=1, allow_nan=True))
    sys.stdout.write('\nSUMMARY %s total_wall_s=%.1f results=%s%s\n' % (canonical(summary), total_wall, results_out,
                                                                    ' (non-finite floats present in results)' if nan_note else ''))
    for f in fixtures:
        sys.stdout.write('  %-4s %-8s %s\n' % (f.name, f.status, f.title))
    return 0 if out['all_pass'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
