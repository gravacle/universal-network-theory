"""campaign_runner_c3v001.py -- INTERFACE_0463_V001 Module C: parallel campaign runner.

Root launches `run_campaign` once per campaign; it runs up to `max_workers`
(1..12) worker subprocesses concurrently, each a separate single-thread process
started with `start_new_session=True`, and records one durable receipt per call.

Properties (see RUNNER_NOTES_0463_V001.md):
  * inert at import; standard library only (no numpy, no threads, no network);
  * every public function is keyword-only with no defaults, returns
    {ok, reasons, ...} and fails closed; a refusal starts nothing;
  * the runner never deletes, overwrites or edits anything: a call starts only
    in an absent call directory; the receipt is written exactly once;
  * no automatic retry: a failure is recorded once with its reason;
  * all four pins (worker, solver, checkpoint module, seed) are SHA256 over
    bytes, verified before the child starts and recorded in the receipt;
  * caps: per-call wall, per-call RSS (`ps -o rss=` polled), per-call output
    bytes (total size under the call directory), campaign wall (no new starts);
  * resume: a verified receipt (self-hash, same theta_key, same worker pins,
    result.json and seed re-hashed from bytes) is reused as RESUMED_OK /
    RESUMED_FAILED without rerun; anything else existing is
    DIR_EXISTS_UNVERIFIED and is never run or touched.
"""
import datetime
import hashlib
import json
import math
import os
import re
import signal
import stat
import subprocess
import time

MODULE_NAME = 'campaign_runner_c3v001'
MAX_WORKERS_LIMIT = 12
RECEIPT_NAME = 'RECEIPT.json'
CALL_STATUSES = ('OK', 'FAILED', 'RESUMED_OK', 'RESUMED_FAILED',
                 'DIR_EXISTS_UNVERIFIED', 'NOT_STARTED')
RECEIPT_STATUSES = ('OK', 'FAILED')
CAMPAIGN_STATUSES = ('COMPLETE', 'CAMPAIGN_CAP', 'REFUSED')
KILL_WAIT_S = 30.0

_HEX64 = re.compile(r'^[0-9a-f]{64}$')
_THREAD_ENV = {'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1',
               'MKL_NUM_THREADS': '1'}
_WORKER_KEYS = ('worker_path', 'worker_sha256', 'solver_path', 'solver_sha256',
                'checkpoint_module_path', 'checkpoint_module_sha256',
                'start_iteration', 'command_template')
# Placeholders a caller may use in worker['command_template'] (a list of argv
# tokens; each token is rendered with str.format_map over these names). The
# runner never hard-codes any worker's command line: the caller supplies the
# template for the driver it launches. {seed} and {outdir} are mandatory so
# that every call reads its own seed and writes into its own fresh directory.
COMMAND_PLACEHOLDERS = ('python', 'worker', 'seed', 'seed_sha256', 'solver',
                        'solver_sha256', 'checkpoint_module',
                        'checkpoint_module_sha256', 'outdir', 'checkpoint_dir',
                        'start_iteration')
_MANDATORY_PLACEHOLDERS = ('seed', 'outdir')


class _StrictMap(dict):
    def __missing__(self, key):
        raise KeyError(key)


def _template_placeholders(token):
    """Return the placeholder names used by one template token."""
    import string as _string
    names = []
    for _lit, field, _spec, _conv in _string.Formatter().parse(token):
        if field is not None:
            names.append(field)
    return names


def _check_command_template(template):
    reasons = []
    if not isinstance(template, (list, tuple)) or not template:
        return ['COMMAND_TEMPLATE_NOT_NONEMPTY_LIST']
    used = set()
    for i, tok in enumerate(template):
        if not isinstance(tok, str) or not tok:
            reasons.append('COMMAND_TEMPLATE_TOKEN_NOT_STR:%d' % i)
            continue
        try:
            names = _template_placeholders(tok)
        except ValueError as exc:
            reasons.append('COMMAND_TEMPLATE_TOKEN_UNPARSEABLE:%d:%s' % (i, exc))
            continue
        for name in names:
            if name not in COMMAND_PLACEHOLDERS:
                reasons.append('COMMAND_TEMPLATE_UNKNOWN_PLACEHOLDER:%d:%s' % (i, name))
            used.add(name)
    for name in _MANDATORY_PLACEHOLDERS:
        if name not in used:
            reasons.append('COMMAND_TEMPLATE_MISSING_PLACEHOLDER:' + name)
    return reasons


def render_command(*, template, mapping):
    """Render a validated command template; returns {ok, command, reasons}."""
    reasons = _check_command_template(template)
    if not isinstance(mapping, dict):
        reasons.append('MAPPING_NOT_DICT')
    if reasons:
        return {'ok': False, 'command': None, 'reasons': reasons}
    out = []
    for tok in template:
        try:
            out.append(tok.format_map(_StrictMap({k: str(v) for k, v in mapping.items()})))
        except (KeyError, ValueError, IndexError) as exc:
            return {'ok': False, 'command': None,
                    'reasons': ['COMMAND_TEMPLATE_RENDER_FAILED:%s' % exc]}
    return {'ok': True, 'command': out, 'reasons': []}
_PIN_NAMES = ('worker', 'solver', 'checkpoint_module')
_RUN_KWARGS = frozenset(('campaign_dir', 'python_executable', 'worker',
                         'theta_to_seed', 'result_reader', 'max_workers',
                         'per_call_wall_s', 'per_call_rss_bytes',
                         'per_call_output_bytes', 'campaign_wall_s', 'resume',
                         'poll_interval_s'))
_RECEIPT_KEYS = ('runner', 'index', 'theta', 'theta_key', 'call_dir', 'seed',
                 'worker_pins', 'python_executable', 'start_iteration',
                 'command', 'started_utc', 'finished_utc', 'wall_s',
                 'exit_code', 'reason', 'detail', 'max_rss_bytes_observed',
                 'output_bytes', 'result_json', 'result', 'status', 'caps',
                 'receipt_sha256')


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'),
                      allow_nan=False)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec='microseconds')


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _is_finite_number(x):
    if isinstance(x, bool):
        return False
    if isinstance(x, int):
        return True
    if isinstance(x, float):
        return math.isfinite(x)
    return False


def _is_positive_number(x):
    return _is_finite_number(x) and x > 0


def _is_hex64(s):
    return isinstance(s, str) and _HEX64.match(s) is not None


def _tree_bytes(root):
    """Sum of regular-file sizes under root (symlinks not followed)."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in filenames:
            try:
                st = os.lstat(os.path.join(dirpath, name))
            except OSError:
                continue
            if stat.S_ISREG(st.st_mode):
                total += st.st_size
    return total


def _ps_rss_bytes(pid):
    """RSS of one pid via `ps -o rss= -p pid` (KiB on macOS) in bytes, or None."""
    try:
        cp = subprocess.run(['ps', '-o', 'rss=', '-p', str(pid)],
                            stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, timeout=10.0)
    except (OSError, subprocess.SubprocessError):
        return None
    if cp.returncode != 0:
        return None
    text = cp.stdout.strip()
    if not text:
        return None
    try:
        return int(text.split()[0]) * 1024
    except ValueError:
        return None


def _killpg(pid):
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        pass


def _write_once(path, text):
    """Create `path` exclusively and write text; never overwrites."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        data = text.encode('utf-8')
        view = memoryview(data)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)


def _clean_theta(theta):
    """Return (clean_theta, theta_key) or (None, reason)."""
    if not isinstance(theta, dict):
        return None, 'THETA_NOT_DICT'
    for k, v in theta.items():
        if not isinstance(k, str) or not k:
            return None, 'THETA_COORDINATE_NAME_NOT_STR'
        if not _is_finite_number(v):
            return None, 'THETA_VALUE_NOT_FINITE_NUMBER:' + str(k)
    try:
        key = canonical_json(theta)
        clean = json.loads(key)
    except (TypeError, ValueError) as exc:
        return None, 'THETA_NOT_CANONICALIZABLE:' + type(exc).__name__
    return clean, key


def _check_forward_result(raw):
    """Validate a forward-style result; return (clean_dict, None) or (None, why)."""
    if not isinstance(raw, dict):
        return None, 'RESULT_NOT_DICT'
    for k in ('speeds_km_s', 'valid', 'reasons'):
        if k not in raw:
            return None, 'RESULT_KEY_MISSING:' + k
    if not isinstance(raw['valid'], bool):
        return None, 'RESULT_VALID_NOT_BOOL'
    if not isinstance(raw['speeds_km_s'], dict):
        return None, 'RESULT_SPEEDS_NOT_DICT'
    for k, v in raw['speeds_km_s'].items():
        if not isinstance(k, str):
            return None, 'RESULT_SPEED_ID_NOT_STR'
        if not _is_finite_number(v):
            return None, 'RESULT_SPEED_NOT_FINITE_NUMBER:' + str(k)
    if not isinstance(raw['reasons'], list) or any(
            not isinstance(r, str) for r in raw['reasons']):
        return None, 'RESULT_REASONS_NOT_STR_LIST'
    if 'provenance' in raw and raw['provenance'] is not None and not isinstance(
            raw['provenance'], dict):
        return None, 'RESULT_PROVENANCE_NOT_DICT'
    try:
        clean = json.loads(canonical_json(raw))
    except (TypeError, ValueError) as exc:
        return None, 'RESULT_NOT_CANONICALIZABLE:' + type(exc).__name__
    return clean, None


def _verify_worker(worker):
    """Verify the three static worker pins from bytes; return (pins, reasons)."""
    reasons = []
    if not isinstance(worker, dict):
        return None, ['WORKER_NOT_DICT']
    for k in _WORKER_KEYS:
        if k not in worker:
            reasons.append('WORKER_KEY_MISSING:' + k)
    if reasons:
        return None, reasons
    pins = {}
    for name in _PIN_NAMES:
        path = worker[name + '_path']
        expected = worker[name + '_sha256']
        if not isinstance(path, str) or not os.path.isabs(path):
            reasons.append('WORKER_PATH_NOT_ABSOLUTE:' + name)
            continue
        if not _is_hex64(expected):
            reasons.append('WORKER_SHA256_NOT_HEX64:' + name)
            continue
        if not os.path.isfile(path):
            reasons.append('WORKER_FILE_MISSING:%s:%s' % (name, path))
            continue
        try:
            actual = sha256_file(path)
        except OSError as exc:
            reasons.append('WORKER_FILE_UNREADABLE:%s:%s' % (name, exc))
            continue
        if actual != expected:
            reasons.append('WORKER_PIN_MISMATCH:%s:%s:expected=%s:actual=%s'
                           % (name, path, expected, actual))
            continue
        pins[name] = {'path': path, 'sha256': actual}
    if not _is_int(worker['start_iteration']) or worker['start_iteration'] < 0:
        reasons.append('WORKER_START_ITERATION_NOT_NONNEGATIVE_INT')
    reasons.extend(_check_command_template(worker['command_template']))
    if reasons:
        return None, reasons
    return pins, []


def _refused(reasons):
    return {'ok': False, 'status': 'REFUSED', 'calls': [], 'n_ok': 0,
            'n_failed': 0, 'n_resumed': 0, 'n_not_started': 0,
            'n_unverified': 0, 'evaluations_run': 0,
            'campaign_wall_used_s': 0.0, 'max_concurrent_observed': 0,
            'reasons': list(reasons)}


def _record(index, theta, key, call_dir, status, reason, detail, receipt_path,
            result, wall_s, exit_code, max_rss, output_bytes):
    return {'index': index, 'theta': theta, 'theta_key': key,
            'call_dir': call_dir, 'status': status, 'reason': reason,
            'detail': detail, 'receipt_path': receipt_path, 'result': result,
            'wall_s': wall_s, 'exit_code': exit_code,
            'max_rss_bytes_observed': max_rss, 'output_bytes': output_bytes}


# ----------------------------------------------------------------------------
# receipts
# ----------------------------------------------------------------------------

def verify_receipt(*, receipt_path):
    """Verify a RECEIPT.json: canonical bytes, self-hash, structure, theta_key,
    and (when present) the result.json hash recomputed from bytes."""
    reasons = []
    if not isinstance(receipt_path, str) or not os.path.isabs(receipt_path):
        return {'ok': False, 'receipt': None,
                'reasons': ['RECEIPT_PATH_NOT_ABSOLUTE']}
    if not os.path.isfile(receipt_path):
        return {'ok': False, 'receipt': None, 'reasons': ['RECEIPT_MISSING']}
    try:
        with open(receipt_path, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        return {'ok': False, 'receipt': None,
                'reasons': ['RECEIPT_UNREADABLE:' + str(exc)]}
    try:
        obj = json.loads(raw.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return {'ok': False, 'receipt': None, 'reasons': ['RECEIPT_NOT_JSON']}
    if not isinstance(obj, dict):
        return {'ok': False, 'receipt': None, 'reasons': ['RECEIPT_NOT_OBJECT']}
    for k in _RECEIPT_KEYS:
        if k not in obj:
            reasons.append('RECEIPT_KEY_MISSING:' + k)
    if reasons:
        return {'ok': False, 'receipt': None, 'reasons': reasons}
    recorded = obj['receipt_sha256']
    if not _is_hex64(recorded):
        reasons.append('RECEIPT_SELF_HASH_NOT_HEX64')
    else:
        body = {k: v for k, v in obj.items() if k != 'receipt_sha256'}
        try:
            if sha256_text(canonical_json(body)) != recorded:
                reasons.append('RECEIPT_SELF_HASH_MISMATCH')
        except (TypeError, ValueError):
            reasons.append('RECEIPT_NOT_CANONICALIZABLE')
    try:
        if raw != canonical_json(obj).encode('utf-8'):
            reasons.append('RECEIPT_BYTES_NOT_CANONICAL')
    except (TypeError, ValueError):
        reasons.append('RECEIPT_NOT_CANONICALIZABLE')
    if obj['status'] not in RECEIPT_STATUSES:
        reasons.append('RECEIPT_STATUS_INVALID')
    if not _is_int(obj['index']) or obj['index'] < 0:
        reasons.append('RECEIPT_INDEX_INVALID')
    clean, key = _clean_theta(obj['theta'])
    if clean is None or key != obj['theta_key']:
        reasons.append('RECEIPT_THETA_KEY_MISMATCH')
    pins = obj['worker_pins']
    if not isinstance(pins, dict):
        reasons.append('RECEIPT_WORKER_PINS_NOT_DICT')
    else:
        for name in _PIN_NAMES + ('seed',):
            p = pins.get(name)
            if not isinstance(p, dict) or 'path' not in p or 'sha256' not in p:
                reasons.append('RECEIPT_PIN_MALFORMED:' + name)
            elif name != 'seed' and not _is_hex64(p['sha256']):
                reasons.append('RECEIPT_PIN_NOT_HEX64:' + name)
    rj = obj['result_json']
    if rj is not None:
        if (not isinstance(rj, dict) or not isinstance(rj.get('path'), str)
                or not _is_hex64(rj.get('sha256'))):
            reasons.append('RESULT_JSON_MALFORMED')
        elif not os.path.isfile(rj['path']):
            reasons.append('RESULT_JSON_MISSING:' + rj['path'])
        else:
            try:
                actual = sha256_file(rj['path'])
            except OSError:
                actual = None
            if actual != rj['sha256']:
                reasons.append('RESULT_SHA256_MISMATCH:' + rj['path'])
    res = obj['result']
    if res is not None:
        clean_res, why = _check_forward_result(res)
        if clean_res is None:
            reasons.append('RECEIPT_RESULT_MALFORMED:' + str(why))
    if obj['status'] == 'OK':
        if rj is None or not isinstance(res, dict) or res.get('valid') is not True:
            reasons.append('RECEIPT_OK_WITHOUT_VALID_RESULT')
    if reasons:
        return {'ok': False, 'receipt': None, 'reasons': reasons}
    return {'ok': True, 'receipt': obj, 'reasons': []}


def _existing_dir_record(index, theta, key, call_dir, pins, resume):
    """Classify an existing call_dir; never runs, never touches it."""
    receipt_path = os.path.join(call_dir, RECEIPT_NAME)
    rp = receipt_path if os.path.isfile(receipt_path) else None
    base = _record(index, theta, key, call_dir, 'DIR_EXISTS_UNVERIFIED', '',
                   '', rp, None, 0.0, None, 0, 0)
    if resume is not True:
        base['reason'] = 'DIR_EXISTS_RESUME_FALSE'
        return base
    if rp is None:
        base['reason'] = 'RECEIPT_MISSING'
        return base
    v = verify_receipt(receipt_path=receipt_path)
    if not v['ok']:
        base['reason'] = 'RECEIPT_UNVERIFIED'
        base['detail'] = '; '.join(v['reasons'])
        return base
    r = v['receipt']
    if r['index'] != index:
        base['reason'] = 'INDEX_MISMATCH'
        base['detail'] = 'receipt index %r' % (r['index'],)
        return base
    if r['theta_key'] != key:
        base['reason'] = 'THETA_KEY_MISMATCH'
        base['detail'] = 'receipt theta_key ' + str(r['theta_key'])
        return base
    for name in _PIN_NAMES:
        if r['worker_pins'][name]['sha256'] != pins[name]['sha256']:
            base['reason'] = 'WORKER_PIN_MISMATCH'
            base['detail'] = '%s: receipt %s current %s' % (
                name, r['worker_pins'][name]['sha256'], pins[name]['sha256'])
            return base
    seed_pin = r['worker_pins']['seed']
    if seed_pin['sha256'] is not None:
        if not _is_hex64(seed_pin['sha256']) or not isinstance(
                seed_pin['path'], str):
            base['reason'] = 'SEED_PIN_MALFORMED'
            return base
        if not os.path.isfile(seed_pin['path']):
            base['reason'] = 'SEED_MISSING'
            base['detail'] = seed_pin['path']
            return base
        try:
            actual = sha256_file(seed_pin['path'])
        except OSError:
            actual = None
        if actual != seed_pin['sha256']:
            base['reason'] = 'SEED_HASH_MISMATCH'
            base['detail'] = seed_pin['path']
            return base
    if r['status'] == 'OK':
        base['status'] = 'RESUMED_OK'
    elif r['status'] == 'FAILED':
        base['status'] = 'RESUMED_FAILED'
    else:
        base['reason'] = 'RECEIPT_STATUS_UNKNOWN'
        return base
    base['reason'] = r['reason']
    base['detail'] = r['detail']
    base['result'] = r['result']
    base['wall_s'] = r['wall_s']
    base['exit_code'] = r['exit_code']
    base['max_rss_bytes_observed'] = r['max_rss_bytes_observed']
    base['output_bytes'] = r['output_bytes']
    return base


# ----------------------------------------------------------------------------
# one call: start, finalize
# ----------------------------------------------------------------------------

def _start_call(ctx, index, theta, key):
    """Create the fresh call_dir, write the seed, verify its pin, spawn the
    worker. Returns ('running', state) or ('record', record)."""
    call_dir = os.path.join(ctx['campaign_dir'], 'call_%04d' % index)
    seed_path = os.path.join(call_dir, 'seed.json')
    out_dir = os.path.join(call_dir, 'out')
    ckpt_dir = os.path.join(call_dir, 'ckpt')
    state = {'index': index, 'theta': theta, 'key': key, 'call_dir': call_dir,
             'seed_path': seed_path, 'seed_sha256': None, 'out_dir': out_dir,
             'command': [], 'proc': None, 'fh_out': None, 'fh_err': None,
             't_start': time.monotonic(), 'started_utc': _utc_now(),
             'max_rss': 0, 'output_bytes': 0, 'cap': None, 'detail': ''}
    try:
        os.mkdir(call_dir)
    except FileExistsError:
        return 'record', _record(index, theta, key, call_dir,
                                 'DIR_EXISTS_UNVERIFIED', 'DIR_EXISTS_RACE',
                                 '', None, None, 0.0, None, 0, 0)
    except OSError as exc:
        return 'record', _record(index, theta, key, call_dir, 'FAILED',
                                 'CALL_DIR_CREATE_FAILED', str(exc), None,
                                 None, 0.0, None, 0, 0)
    # seed via the adapter's theta_to_seed(theta, out_path)
    try:
        sres = ctx['theta_to_seed'](theta, seed_path)
    except Exception as exc:  # the adapter failed; recorded, never retried
        state['detail'] = '%s: %s' % (type(exc).__name__, exc)
        return 'record', _finalize(ctx, state, 'SEED_WRITE_EXCEPTION')
    if not isinstance(sres, dict) or sres.get('ok') is not True:
        why = ''
        if isinstance(sres, dict):
            why = '; '.join(str(r) for r in sres.get('reasons', []))
        state['detail'] = why
        return 'record', _finalize(ctx, state, 'SEED_WRITE_FAILED')
    if not os.path.isfile(seed_path):
        return 'record', _finalize(ctx, state, 'SEED_MISSING')
    try:
        seed_sha = sha256_file(seed_path)
    except OSError as exc:
        state['detail'] = str(exc)
        return 'record', _finalize(ctx, state, 'SEED_UNREADABLE')
    declared = sres.get('seed_sha256')
    if declared is not None and declared != seed_sha:
        state['detail'] = 'declared=%s bytes=%s' % (declared, seed_sha)
        return 'record', _finalize(ctx, state, 'SEED_HASH_MISMATCH')
    state['seed_sha256'] = seed_sha
    pins = ctx['pins']
    rendered = render_command(template=ctx['command_template'], mapping={
        'python': ctx['python_executable'], 'worker': pins['worker']['path'],
        'seed': seed_path, 'seed_sha256': seed_sha,
        'solver': pins['solver']['path'],
        'solver_sha256': pins['solver']['sha256'],
        'checkpoint_module': pins['checkpoint_module']['path'],
        'checkpoint_module_sha256': pins['checkpoint_module']['sha256'],
        'outdir': out_dir, 'checkpoint_dir': ckpt_dir,
        'start_iteration': ctx['start_iteration']})
    if not rendered['ok']:
        state['detail'] = ';'.join(rendered['reasons'])
        return 'record', _finalize(ctx, state, 'COMMAND_RENDER_FAILED')
    command = rendered['command']
    state['command'] = command
    env = dict(os.environ)
    env.update(_THREAD_ENV)
    try:
        fh_out = open(os.path.join(call_dir, 'stdout.txt'), 'xb')
        fh_err = open(os.path.join(call_dir, 'stderr.txt'), 'xb')
    except OSError as exc:
        state['detail'] = str(exc)
        return 'record', _finalize(ctx, state, 'STDIO_OPEN_FAILED')
    state['fh_out'] = fh_out
    state['fh_err'] = fh_err
    try:
        proc = subprocess.Popen(command, stdin=subprocess.DEVNULL,
                                stdout=fh_out, stderr=fh_err, env=env,
                                cwd=call_dir, start_new_session=True,
                                close_fds=True)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        state['detail'] = '%s: %s' % (type(exc).__name__, exc)
        return 'record', _finalize(ctx, state, 'SPAWN_FAILED')
    state['t_start'] = time.monotonic()
    state['started_utc'] = _utc_now()
    state['proc'] = proc
    return 'running', state


def _finalize(ctx, state, failure_reason):
    """Close handles, read the result through result_reader (when the child
    exited 0), write the receipt once, return the per-call record.
    failure_reason is None for a normally exited child, else the failure code."""
    for k in ('fh_out', 'fh_err'):
        fh = state.get(k)
        if fh is not None:
            try:
                fh.close()
            except OSError:
                pass
            state[k] = None
    proc = state['proc']
    exit_code = proc.returncode if proc is not None else None
    wall_s = time.monotonic() - state['t_start']
    finished_utc = _utc_now()
    call_dir = state['call_dir']
    output_bytes = _tree_bytes(call_dir)
    state['output_bytes'] = output_bytes
    detail = state.get('detail', '')
    result_json = None
    result = None
    status = 'FAILED'
    reason = failure_reason
    if reason is None:
        if exit_code != 0:
            reason = 'EXIT_NONZERO'
            detail = 'exit_code=%r' % (exit_code,)
        elif output_bytes > ctx['per_call_output_bytes']:
            reason = 'OUTPUT_CAP'
            detail = 'output_bytes=%d cap=%d (measured at exit)' % (
                output_bytes, ctx['per_call_output_bytes'])
        else:
            rpath = os.path.join(state['out_dir'], 'result.json')
            if not os.path.isfile(rpath):
                reason = 'RESULT_MISSING'
                detail = rpath
            else:
                try:
                    rsha = sha256_file(rpath)
                except OSError as exc:
                    rsha = None
                    reason = 'RESULT_UNREADABLE'
                    detail = str(exc)
                if rsha is not None:
                    result_json = {'path': rpath, 'sha256': rsha}
                    try:
                        raw = ctx['result_reader'](state['out_dir'])
                    except Exception as exc:
                        reason = 'READER_EXCEPTION'
                        detail = '%s: %s' % (type(exc).__name__, exc)
                    else:
                        clean, why = _check_forward_result(raw)
                        if clean is None:
                            reason = 'READER_MALFORMED'
                            detail = str(why)
                        elif clean['valid'] is True:
                            status = 'OK'
                            reason = 'OK'
                            result = clean
                        else:
                            reason = 'READER_INVALID'
                            result = clean
                            detail = '; '.join(clean['reasons'])
    pins = ctx['pins']
    receipt = {
        'runner': MODULE_NAME,
        'index': state['index'],
        'theta': state['theta'],
        'theta_key': state['key'],
        'call_dir': call_dir,
        'seed': {'path': state['seed_path'], 'sha256': state['seed_sha256']},
        'worker_pins': {
            'worker': dict(pins['worker']),
            'solver': dict(pins['solver']),
            'checkpoint_module': dict(pins['checkpoint_module']),
            'seed': {'path': state['seed_path'], 'sha256': state['seed_sha256']}},
        'python_executable': {'path': ctx['python_executable'],
                              'sha256': ctx['python_sha256']},
        'start_iteration': ctx['start_iteration'],
        'command': list(state['command']),
        'started_utc': state['started_utc'],
        'finished_utc': finished_utc,
        'wall_s': wall_s,
        'exit_code': exit_code,
        'reason': reason,
        'detail': detail,
        'max_rss_bytes_observed': state['max_rss'],
        'output_bytes': output_bytes,
        'result_json': result_json,
        'result': result,
        'status': status,
        'caps': {'per_call_wall_s': ctx['per_call_wall_s'],
                 'per_call_rss_bytes': ctx['per_call_rss_bytes'],
                 'per_call_output_bytes': ctx['per_call_output_bytes']},
    }
    receipt['receipt_sha256'] = sha256_text(canonical_json(receipt))
    receipt_path = os.path.join(call_dir, RECEIPT_NAME)
    try:
        _write_once(receipt_path, canonical_json(receipt))
    except OSError as exc:
        receipt_path = None
        detail = (detail + ' | ' if detail else '') + 'RECEIPT_WRITE_FAILED: ' + str(exc)
    return _record(state['index'], state['theta'], state['key'], call_dir,
                   status, reason, detail, receipt_path, result, wall_s,
                   exit_code, state['max_rss'], output_bytes)


def _kill_and_wait(state):
    proc = state['proc']
    _killpg(proc.pid)
    try:
        proc.wait(timeout=KILL_WAIT_S)
    except subprocess.TimeoutExpired:
        state['detail'] = (state['detail'] + ' | ' if state['detail'] else '') + \
            'KILL_WAIT_TIMEOUT'


# ----------------------------------------------------------------------------
# public API
# ----------------------------------------------------------------------------

def run_campaign(*, campaign_dir, python_executable, worker, thetas,
                 theta_to_seed, result_reader, max_workers, per_call_wall_s,
                 per_call_rss_bytes, per_call_output_bytes, campaign_wall_s,
                 resume, poll_interval_s):
    t_begin = time.monotonic()
    reasons = []
    # --- argument validation: any problem refuses with nothing started ------
    if not isinstance(campaign_dir, str) or not os.path.isabs(campaign_dir):
        reasons.append('CAMPAIGN_DIR_NOT_ABSOLUTE')
    elif os.path.lexists(campaign_dir) and not os.path.isdir(campaign_dir):
        reasons.append('CAMPAIGN_DIR_NOT_A_DIRECTORY')
    if (not isinstance(python_executable, str)
            or not os.path.isabs(python_executable)
            or not os.path.isfile(python_executable)
            or not os.access(python_executable, os.X_OK)):
        reasons.append('PYTHON_EXECUTABLE_NOT_ABSOLUTE_EXECUTABLE_FILE')
    if not callable(theta_to_seed):
        reasons.append('THETA_TO_SEED_NOT_CALLABLE')
    if not callable(result_reader):
        reasons.append('RESULT_READER_NOT_CALLABLE')
    if not _is_int(max_workers) or not 1 <= max_workers <= MAX_WORKERS_LIMIT:
        reasons.append('MAX_WORKERS_NOT_IN_1_TO_%d' % MAX_WORKERS_LIMIT)
    for name, value in (('per_call_wall_s', per_call_wall_s),
                        ('per_call_rss_bytes', per_call_rss_bytes),
                        ('per_call_output_bytes', per_call_output_bytes),
                        ('campaign_wall_s', campaign_wall_s),
                        ('poll_interval_s', poll_interval_s)):
        if not _is_positive_number(value):
            reasons.append(name.upper() + '_NOT_POSITIVE')
    if not isinstance(resume, bool):
        reasons.append('RESUME_NOT_BOOL')
    cleaned = []
    if not isinstance(thetas, list):
        reasons.append('THETAS_NOT_LIST')
    else:
        for i, theta in enumerate(thetas):
            clean, key = _clean_theta(theta)
            if clean is None:
                reasons.append('THETA_%d_%s' % (i, key))
            else:
                cleaned.append((clean, key))
    pins, preasons = _verify_worker(worker)
    reasons.extend(preasons)
    if reasons:
        return _refused(reasons)
    try:
        python_sha256 = sha256_file(python_executable)
    except OSError as exc:
        return _refused(['PYTHON_EXECUTABLE_UNREADABLE:' + str(exc)])
    try:
        os.makedirs(campaign_dir, exist_ok=True)
    except OSError as exc:
        return _refused(['CAMPAIGN_DIR_CREATE_FAILED:' + str(exc)])
    ctx = {'campaign_dir': campaign_dir, 'python_executable': python_executable,
           'python_sha256': python_sha256, 'pins': pins,
           'start_iteration': worker['start_iteration'],
           'command_template': list(worker['command_template']),
           'theta_to_seed': theta_to_seed, 'result_reader': result_reader,
           'per_call_wall_s': per_call_wall_s,
           'per_call_rss_bytes': per_call_rss_bytes,
           'per_call_output_bytes': per_call_output_bytes}
    n = len(cleaned)
    records = [None] * n
    pending = []
    # --- pre-scan: existing call directories are classified, never touched --
    for i, (theta, key) in enumerate(cleaned):
        call_dir = os.path.join(campaign_dir, 'call_%04d' % i)
        if os.path.lexists(call_dir):
            records[i] = _existing_dir_record(i, theta, key, call_dir, pins,
                                              resume)
        else:
            pending.append(i)
    running = {}
    max_concurrent = 0
    evaluations_run = 0
    campaign_capped = False
    try:
        while True:
            # 1. poll running children: reap finished, enforce per-call caps
            for i in list(running):
                st = running[i]
                proc = st['proc']
                if proc.poll() is None:
                    elapsed = time.monotonic() - st['t_start']
                    rss = _ps_rss_bytes(proc.pid)
                    if rss is not None and rss > st['max_rss']:
                        st['max_rss'] = rss
                    out_b = _tree_bytes(st['call_dir'])
                    st['output_bytes'] = out_b
                    cap = None
                    if elapsed > per_call_wall_s:
                        cap = 'WALL_CAP'
                        st['detail'] = 'elapsed_s=%.3f cap_s=%r' % (
                            elapsed, per_call_wall_s)
                    elif rss is not None and rss > per_call_rss_bytes:
                        cap = 'RSS_CAP'
                        st['detail'] = 'rss_bytes=%d cap=%d' % (
                            rss, per_call_rss_bytes)
                    elif out_b > per_call_output_bytes:
                        cap = 'OUTPUT_CAP'
                        st['detail'] = 'output_bytes=%d cap=%d' % (
                            out_b, per_call_output_bytes)
                    if cap is None:
                        continue
                    st['cap'] = cap
                    _kill_and_wait(st)
                    # recorded once with the cap reason; never retried
                    records[i] = _finalize(ctx, st, cap)
                    del running[i]
                    continue
                records[i] = _finalize(ctx, st, None)
                del running[i]
            # 2. start new calls while slots remain and the campaign wall holds
            while pending and len(running) < max_workers:
                if time.monotonic() - t_begin > campaign_wall_s:
                    campaign_capped = True
                    break
                i = pending.pop(0)
                theta, key = cleaned[i]
                kind, payload = _start_call(ctx, i, theta, key)
                if kind == 'running':
                    running[i] = payload
                    evaluations_run += 1
                else:
                    records[i] = payload
            if len(running) > max_concurrent:
                max_concurrent = len(running)
            if campaign_capped:
                while pending:
                    i = pending.pop(0)
                    theta, key = cleaned[i]
                    records[i] = _record(
                        i, theta, key,
                        os.path.join(campaign_dir, 'call_%04d' % i),
                        'NOT_STARTED', 'CAMPAIGN_CAP',
                        'campaign_wall_s=%r elapsed_s=%.3f' % (
                            campaign_wall_s, time.monotonic() - t_begin),
                        None, None, 0.0, None, 0, 0)
            if not running and not pending:
                break
            if running:
                time.sleep(poll_interval_s)
    finally:
        # Only reached with children alive when an exception escapes the loop
        # (e.g. KeyboardInterrupt): kill their process groups and record once.
        for i in list(running):
            st = running[i]
            st['detail'] = 'runner aborted by exception'
            _kill_and_wait(st)
            try:
                records[i] = _finalize(ctx, st, 'RUNNER_ABORTED')
            except Exception:
                pass
            del running[i]
    # --- summary in theta order ---------------------------------------------
    counts = {s: 0 for s in CALL_STATUSES}
    for rec in records:
        counts[rec['status']] += 1
    n_not_started = counts['NOT_STARTED']
    n_unverified = counts['DIR_EXISTS_UNVERIFIED']
    status = 'CAMPAIGN_CAP' if n_not_started else 'COMPLETE'
    for rec in records:
        if rec['status'] not in ('OK', 'RESUMED_OK'):
            reasons.append('call_%04d:%s:%s' % (rec['index'], rec['status'],
                                                rec['reason']))
    if status == 'CAMPAIGN_CAP':
        reasons.insert(0, 'CAMPAIGN_CAP')
    return {'ok': status == 'COMPLETE' and n_unverified == 0,
            'status': status,
            'calls': records,
            'n_ok': counts['OK'],
            'n_failed': counts['FAILED'],
            'n_resumed': counts['RESUMED_OK'] + counts['RESUMED_FAILED'],
            'n_not_started': n_not_started,
            'n_unverified': n_unverified,
            'evaluations_run': evaluations_run,
            'campaign_wall_used_s': time.monotonic() - t_begin,
            'max_concurrent_observed': max_concurrent,
            'reasons': reasons}


def _forward_from_record(rec):
    prov_call = {'index': rec['index'], 'call_dir': rec['call_dir'],
                 'receipt_path': rec['receipt_path'], 'status': rec['status'],
                 'reason': rec['reason'], 'detail': rec['detail']}
    res = rec['result']
    good = rec['status'] in ('OK', 'RESUMED_OK')
    if isinstance(res, dict) and 'speeds_km_s' in res and 'valid' in res \
            and 'reasons' in res:
        out = dict(res)
        out['speeds_km_s'] = dict(res['speeds_km_s'])
        out['reasons'] = list(res['reasons'])
        if not good or res['valid'] is not True:
            out['valid'] = False
            out['reasons'] = out['reasons'] + [
                'CAMPAIGN_CALL_' + rec['status'], str(rec['reason'])]
        prov = dict(res['provenance']) if isinstance(
            res.get('provenance'), dict) else {}
        prov['campaign_call'] = prov_call
        out['provenance'] = prov
        return out
    reasons = ['CAMPAIGN_CALL_' + rec['status'], str(rec['reason'])]
    if rec['detail']:
        reasons.append(str(rec['detail']))
    return {'speeds_km_s': {}, 'valid': False, 'reasons': reasons,
            'provenance': {'campaign_call': prov_call}}


def forward_many(*, thetas, **kwargs):
    """Batched forward: one campaign for `thetas`; results in theta order."""
    missing = sorted(_RUN_KWARGS - set(kwargs))
    extra = sorted(set(kwargs) - _RUN_KWARGS)
    if missing or extra:
        reasons = ['FORWARD_MANY_KWARG_MISSING:' + k for k in missing] + \
                  ['FORWARD_MANY_KWARG_UNKNOWN:' + k for k in extra]
        campaign = _refused(reasons)
        return {'ok': False, 'results': [], 'campaign': campaign,
                'reasons': list(reasons)}
    campaign = run_campaign(thetas=thetas, **kwargs)
    if campaign['status'] == 'REFUSED':
        return {'ok': False, 'results': [], 'campaign': campaign,
                'reasons': list(campaign['reasons'])}
    results = [_forward_from_record(rec) for rec in campaign['calls']]
    return {'ok': campaign['ok'], 'results': results, 'campaign': campaign,
            'reasons': list(campaign['reasons'])}
