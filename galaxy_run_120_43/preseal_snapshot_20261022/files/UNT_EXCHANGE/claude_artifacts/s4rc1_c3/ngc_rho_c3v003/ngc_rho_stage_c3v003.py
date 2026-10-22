"""NGC rho stage c3v003, CP-1 style (Claude3 lane; root A136 G1-G4; 0717 R4; structure of cp1_runner_c3v004 3f5e5c18 rho
stage).  The successor of ngc_rho_stage_c3v002 (bb9e0a76): CHANGES_C3V003 E3 (W6), E4 (W7), E5 (schemas) and E9 (A166);
c3v002's D1 and D6 are unchanged.

Root operates it; the builder ran it on SYNTHETIC inputs only (test_ngc_rho_c3v003.py).
Per point (theta key from the S0 record 1be5ed70; the filled NGC call spec by exact pin):
  - D1 (0717 R4): the cw8 twin gets no rho record.  `run` and `attempt` read the spec by exact pin and refuse any spec
    whose numerics.route_a.column_workers is not exactly int 1 (NGC_RHO_TWIN_GETS_NO_RECORD), before any computation or
    output other than the usual refusal record (exit 2; no point folder).  Custody keeps column_workers (A136 G3);
  - HELD unless --allow-rho AND a root review pin {path, sha256} whose bytes are read and hashed here AND
    --root-review-sha256 equal to that pin.  Otherwise the stage writes STAGE_RHO_HELD and computes nothing (exit 5);
  - attempt a runs in a SEPARATE process: python3 -I -B ngc_rho_stage_c3v003.py attempt ... with single-thread BLAS
    (E9, A166: no taskpolicy -b; the attempt inherits the caller's scheduling); at the S0 seed key the stage then runs
    attempt b in another separate process (a fresh interpreter and a fresh point context), so G4 has two records from
    two processes.  The decision on the pair is the slot proof's (10-key canonical); the stage writes a diagnostic only;
  - each attempt process re-checks the interpreter flags, BLAS 1 and the gate, then calls the producer
    (ngc_rho_producer_c3v003, exact bytes) with the registered settings and the registered inputs only.  E4 (W7): the
    producer's own Refusal (D9 BEFORE and AFTER included) becomes this stage's clean refusal (exit 2 and one REFUSED
    JSON line, no traceback), with no rho record and no stage record; run_point converts one from an in-process spawn;
  - E3 (W6): the spec read refuses a path any of whose components contains 'ngc3198' before realpath (which lstats);
  - every output is created exclusively (O_EXCL | O_NOFOLLOW) inside the named out-root: an existing canonical
    directory whose name starts with 'ngc_rho_out_'.  A point attempt folder is never reused.  worker_logs is created
    with os.makedirs(exist_ok=True), so stage processes launched together in one out-root all proceed (D6).
Refusals (exit 2): not python3 -I -B; -O; BLAS env not 1; a producer refusal (E4).  E9 (A166, FROM_CODEX/0740): the
c3v002 taskpolicy -b (QoS) refusal is dropped.  The -I -B (no -O) and single-thread BLAS rules stay, BLAS forced to 1:
the two-process bitwise G4 pair needs one deterministic reduction order (correctness, not resources).
Commands: plan | run | attempt (internal).  Exit codes: 0 ok, 2 setup refusal, 3 stopped, 5 HELD.
"""
import os

THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')
PARENT_THREAD_ENV = {_k: os.environ.get(_k) for _k in THREAD_ENV}
for _k in THREAD_ENV:                       # single-thread BLAS by override at import, before numpy can load
    os.environ[_k] = '1'

import datetime  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import resource  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

HERE = os.path.dirname(os.path.realpath(__file__))
STAGE_PATH = os.path.realpath(__file__)
PRODUCER = (os.path.join(HERE, 'ngc_rho_producer_c3v003.py'), 'd3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4')
SLOT_PROOF = (os.path.join(HERE, 'ngc_lo_slot_proof_c3v003.py'), 'ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a')
PRODUCER_MODULE = 'ngc_rho_producer_c3v003'     # load_producer() executes the producer under this name (E4: its Refusal)
SEED_KEY = '968c915bece706ea1d6c0fa15357984884a87443e7c19eebd104230c9c961981'
OUT_PREFIX = 'ngc_rho_out_'
REVIEW_ROOTS = ('/Users/bgm/Research/',)
HELD = 'HELD_PENDING_ROOT_REVIEW'
GATE_SCHEMA = 'NGC_RHO_STAGE_GATE_C3V003'
STAGE_SCHEMA = 'NGC_RHO_STAGE_C3V003'
PAIR_SCHEMA = 'NGC_RHO_SEED_PAIR_DIAGNOSTIC_C3V003'
TWIN_CODE = 'NGC_RHO_TWIN_GETS_NO_RECORD'
EXIT_OK, EXIT_SETUP, EXIT_STOP, EXIT_HELD = 0, 2, 3, 5


class Refusal(Exception):
    """Fail-closed refusal with a stable code."""


CAUGHT = (Refusal, ValueError, KeyError, TypeError, OSError, AttributeError)


def need(ok, code):
    if not ok:
        raise Refusal(code)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def _is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and _is_sha(x['sha256'])


def isolated_interpreter():
    return sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0


def single_thread_env():
    return {k: os.environ.get(k) for k in THREAD_ENV}


def require_compute_environment():
    """E9 (A166, 0740): no QoS requirement.  Kept for correctness: python3 -I -B without -O, and single-thread BLAS (forced
    to 1 at import), so the two G4 processes reduce in one deterministic order."""
    need(isolated_interpreter(), 'ISOLATED_INTERPRETER_REQUIRED: python3 -I -B (no -O)')
    env = single_thread_env()
    need(all(v == '1' for v in env.values()), 'SINGLE_THREAD_BLAS_ENV_REQUIRED: %r' % (env,))


def validate_out_root(out_root):
    need(isinstance(out_root, str) and os.path.isabs(out_root), 'OUT_ROOT_NOT_ABSOLUTE')
    need(os.path.realpath(out_root) == out_root, 'OUT_ROOT_NONCANONICAL (symlink or relative component)')
    need(os.path.isdir(out_root), 'OUT_ROOT_NOT_AN_EXISTING_DIRECTORY')
    need(os.path.basename(out_root).startswith(OUT_PREFIX), 'OUT_ROOT_NOT_NAMED (%s*)' % OUT_PREFIX)
    need(not (STAGE_PATH.startswith(out_root.rstrip('/') + '/')), 'OUT_ROOT_CONTAINS_THE_STAGE')
    return out_root


def inside(path, root):
    rp = os.path.realpath(os.path.dirname(path))
    return rp == root or rp.startswith(root.rstrip('/') + '/')


def write_new(path, obj, out_root, raw=None):
    """Exclusive create inside out_root only."""
    validate_out_root(out_root)
    need(isinstance(path, str) and os.path.isabs(path) and inside(path, out_root), 'WRITE_OUTSIDE_OUT_ROOT: ' + str(path))
    raw = raw if raw is not None else (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}


def read_pinned(ref, roots, label):
    need(_is_pin(ref), label + ': NOT_AN_EXACT_PIN')
    p = ref['path']
    need(os.path.isabs(p) and os.path.realpath(p) == p, label + ': NONCANONICAL_PATH')
    need(any(p.startswith(r) for r in roots), label + ': OUTSIDE_ALLOWED_ROOTS')
    need('ngc3198' not in os.path.basename(p).lower(), label + ': NGC3198_NAMED_FILE_REFUSED (0708)')
    fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], label + ': BYTE_PIN_MISMATCH')
    return raw


def _ngc3198_named(p):
    """E3 (W6): True when any component string of the path contains 'ngc3198' (case-insensitive); no filesystem call."""
    return any('ngc3198' in part.lower() for part in p.split('/'))


def read_spec(spec_pin):
    """The filled call spec by exact pin, with the producer's read rules (absolute canonical path, no symlink, no
    NGC3198-named file, sha256 of the bytes read; strict JSON).  E3 (W6): the NGC3198 test runs first, on every path
    component, before realpath (which lstats every component)."""
    need(_is_pin(spec_pin), 'SPEC_PIN_NOT_EXACT')
    p = spec_pin['path']
    need(not _ngc3198_named(p), 'SPEC: NGC3198_NAMED_FILE_REFUSED (0708; any path component, before realpath)')
    need(os.path.isabs(p) and os.path.realpath(p) == p, 'SPEC_PATH_NONCANONICAL')
    fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == spec_pin['sha256'], 'SPEC: BYTE_PIN_MISMATCH')

    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'SPEC: DUPLICATE_JSON_KEY')
            out[k] = v
        return out

    def bad(s):
        raise Refusal('SPEC: NONFINITE_JSON')
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    except ValueError as exc:
        raise Refusal('SPEC: JSON_INVALID: ' + str(exc))


def require_member_spec(spec_pin):
    """D1 (0717 R4): the cw8 twin gets no rho record.  Refuses any spec whose numerics.route_a.column_workers is not exactly
    int 1; an honest member spec (column_workers 1) passes.  Custody keeps column_workers (A136 G3)."""
    spec = read_spec(spec_pin)
    num = spec.get('numerics') if isinstance(spec, dict) else None
    ra = num.get('route_a') if isinstance(num, dict) else None
    cw = ra.get('column_workers') if isinstance(ra, dict) else None
    need(type(cw) is int and cw == 1, TWIN_CODE + ' (0717 R4): numerics.route_a.column_workers is %r, not int 1; the cw8 '
         'twin is never a member and gets no rho record' % (cw,))
    return cw


def rho_gate(allow_rho=False, review_pin=None, review_sha256=None, *, out_root=None):
    """HELD unless --allow-rho, an exact root review pin whose bytes match, and the matching sha.  Never raises."""
    rec = {'schema': GATE_SCHEMA, 'utc': utc(), 'allow_rho': allow_rho is True, 'review_pin': review_pin,
           'review_sha256': review_sha256, 'open': False, 'status': HELD, 'reason': None}
    try:
        need(allow_rho is True, 'ALLOW_RHO_NOT_GIVEN')
        need(_is_pin(review_pin), 'ROOT_REVIEW_PIN_MISSING_OR_NOT_AN_EXACT_PIN')
        need(_is_sha(review_sha256) and review_sha256 == review_pin['sha256'], 'ROOT_REVIEW_SHA_DOES_NOT_MATCH_THE_PIN')
        if out_root:
            need(not review_pin['path'].startswith(str(out_root).rstrip('/') + '/'),
                 'REVIEW_INSIDE_THE_OUT_ROOT (the stage never holds or writes approvals)')
        read_pinned(review_pin, REVIEW_ROOTS, 'root review')
        rec.update(open=True, status='OPEN', reason='ROOT_REVIEW_BYTES_MATCH_THE_PIN')
    except CAUGHT as exc:
        rec['reason'] = type(exc).__name__ + ': ' + str(exc)
    return rec


def gate_argv(g):
    g = g or {}
    out = ['--allow-rho'] if g.get('allow_rho') is True else []
    if g.get('review_pin') is not None:
        out += ['--root-review-pin', json.dumps(g['review_pin'], sort_keys=True)]
    if g.get('review_sha256') is not None:
        out += ['--root-review-sha256', str(g['review_sha256'])]
    return out


def gate_args_from_cli(ns):
    pin = None
    if getattr(ns, 'root_review_pin', None):
        try:
            pin = json.loads(ns.root_review_pin)
        except ValueError:
            pin = 'UNPARSEABLE_JSON'                    # a held gate, never a crash
    return {'allow_rho': bool(getattr(ns, 'allow_rho', False)), 'review_pin': pin,
            'review_sha256': getattr(ns, 'root_review_sha256', None)}


def point_dir(out_root, key, attempt):
    return os.path.join(out_root, 'NGC_RHO_P_%s_a%d' % (key[:16], attempt))


def load_producer():
    path, sha = PRODUCER
    need(os.path.realpath(path) == path, 'NONCANONICAL_PRODUCER_PATH')
    with open(path, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == sha, 'PRODUCER_PIN_MISMATCH')
    spec = importlib.util.spec_from_file_location(PRODUCER_MODULE, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[PRODUCER_MODULE] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def is_producer_refusal(exc):
    """E4 (W7): the producer raises its OWN Refusal class, not this module's (so it is outside CAUGHT); it is recognised by
    its class name and its defining module, the name load_producer() executes the producer under."""
    t = type(exc)
    return t.__name__ == 'Refusal' and getattr(t, '__module__', None) == PRODUCER_MODULE


def _usage():
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return {'wall': time.monotonic(), 'cpu': ru.ru_utime + ru.ru_stime, 'maxrss': ru.ru_maxrss}


def attempt(spec_pin, key, out_root, *, attempt_no, letter, gate_args, run_id='', produce=None):
    """One rho attempt in THIS process (the separate attempt process).  Returns (exit, stage record)."""
    require_compute_environment()
    validate_out_root(out_root)
    require_member_spec(spec_pin)                        # D1 (0717 R4): before any computation or output
    need(letter in ('a', 'b'), 'ATTEMPT_LETTER')
    need(letter == 'a' or key == SEED_KEY, 'ATTEMPT_B_IS_FOR_THE_SEED_KEY_ONLY (G4)')
    gate = rho_gate(**(gate_args or {}), out_root=out_root)
    need(gate['open'], HELD + ': ' + str(gate['reason']))
    pdir = point_dir(out_root, key, attempt_no)
    need(os.path.isdir(pdir) and os.path.realpath(pdir) == pdir, 'POINT_DIR_MISSING (the run command creates it)')
    k16 = key[:16]
    rec_path = os.path.join(pdir, 'RHO_NUMERIC_%s_%s.json' % (k16, letter))
    st_path = os.path.join(pdir, 'STAGE_RHO_%s_%s.json' % (letter, k16))
    need(not os.path.exists(rec_path) and not os.path.exists(st_path), 'RHO_ATTEMPT_EXISTS (never overwritten)')
    if produce is None:
        P = load_producer()
        produce = lambda: P.produce(spec_pin, key)                # registered registry and symbol only
    u0 = _usage()
    try:
        rec = produce()
    except Exception as exc:                             # E4 (W7): the producer's own Refusal, D9 BEFORE/AFTER included
        if not is_producer_refusal(exc):
            raise
        raise Refusal('PRODUCER_REFUSED: ' + str(exc)) from None      # no rho record and no stage record are written
    u1 = _usage()
    raw = (json.dumps(rec, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    pin = write_new(rec_path, None, out_root, raw=raw)
    checks = {'theta_key': (rec.get('identity') or {}).get('theta_key') == key,
              'settings_registered': rec.get('settings') == 'registered' and rec.get('full_registered_search_executed') is True,
              'coverage_complete': rec.get('coverage_complete') is True, 'pid_is_this_process': rec.get('pid') == os.getpid()}
    st = {'schema': STAGE_SCHEMA, 'stage': 'RHO', 'attempt': attempt_no, 'letter': letter, 'utc': utc(), 'key': key,
          'record': pin, 'pid': os.getpid(), 'run_id': run_id, 'gate': gate, 'checks': checks, 'ok': all(checks.values()),
          'seconds': round(u1['wall'] - u0['wall'], 3), 'cpu_seconds': round(u1['cpu'] - u0['cpu'], 3),
          'peak_rss_bytes': u1['maxrss'], 'thread_env': single_thread_env(), 'thread_env_parent': dict(PARENT_THREAD_ENV),
          'python': {'executable': sys.executable, 'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode}}
    write_new(st_path, st, out_root)
    return (EXIT_OK if st['ok'] else EXIT_STOP), st


def spawn_attempt(spec_pin, key, out_root, *, attempt_no, letter, gate_args, run_id):
    """A SEPARATE process: python3 -I -B this file attempt ..., single-thread BLAS (forced to 1 in its env).  E9 (A166): no
    taskpolicy -b; the attempt inherits the caller's scheduling."""
    cmd = [sys.executable, '-I', '-B', STAGE_PATH, 'attempt', '--spec-pin', json.dumps(spec_pin, sort_keys=True),
           '--point', key, '--out-root', out_root, '--attempt', str(attempt_no), '--letter', letter,
           '--run-id', run_id] + gate_argv(gate_args)
    env = dict(os.environ)
    env.update({k: '1' for k in THREAD_ENV})
    logdir = os.path.join(out_root, 'worker_logs')
    os.makedirs(logdir, exist_ok=True)                   # D6 (V6): stage processes launched together all proceed
    base = os.path.join(logdir, 'NGC_RHO_%s_a%d_%s_%s' % (key[:16], attempt_no, letter, run_id or 'run'))
    with open(base + '.stdout.txt', 'x') as so, open(base + '.stderr.txt', 'x') as se:
        rc = subprocess.call(cmd, stdin=subprocess.DEVNULL, stdout=so, stderr=se, env=env, close_fds=True)
    return rc, {'exit': rc, 'stdout': base + '.stdout.txt', 'stderr': base + '.stderr.txt'}


def _read_stage(pdir, out_root, name):
    p = os.path.join(pdir, name)
    need(inside(p, out_root) and os.path.isfile(p), 'STAGE_RECORD_MISSING ' + name)
    with open(p, 'rb') as f:
        return json.loads(f.read())


def seed_pair_diagnostic(pdir, out_root, key, P=None):
    """Diagnostic only: the decision is the slot proof's on root-registered records (10-key canonical)."""
    k16 = key[:16]
    st = [_read_stage(pdir, out_root, 'STAGE_RHO_%s_%s.json' % (x, k16)) for x in ('a', 'b')]
    recs = []
    for s in st:
        with open(s['record']['path'], 'rb') as f:
            raw = f.read()
        need(hashlib.sha256(raw).hexdigest() == s['record']['sha256'], 'PAIR_RECORD_CHANGED')
        recs.append(json.loads(raw))
    keys = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
            'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')
    can = lambda r: json.dumps({k: r.get(k) for k in keys}, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return {'schema': PAIR_SCHEMA, 'utc': utc(), 'key': key, 'records': [s['record'] for s in st],
            'pids': [s['pid'] for s in st], 'separate_processes': st[0]['pid'] != st[1]['pid'],
            'distinct_records': st[0]['record']['sha256'] != st[1]['record']['sha256'],
            'wrapper_v002_10_key_canonical_equal_diagnostic': can(recs[0]) == can(recs[1]),
            'rule': 'G4 is decided by ngc_lo_slot_proof_c3v003 on two ROOT-REGISTERED seed records; this is a diagnostic.'}


def run_point(spec_pin, key, out_root, *, attempt_no=1, gate_args=None, run_id='', spawn=spawn_attempt):
    """One point: gate, point folder, attempt a in a separate process; at the seed, attempt b in another one."""
    require_compute_environment()
    validate_out_root(out_root)
    need(_is_pin(spec_pin), 'SPEC_PIN_NOT_EXACT')
    need(_is_sha(key), 'POINT_KEY_NOT_64_HEX')
    need(type(attempt_no) is int and attempt_no >= 1, 'ATTEMPT_NUMBER')
    require_member_spec(spec_pin)                        # D1 (0717 R4): before the point folder or any record
    pdir = point_dir(out_root, key, attempt_no)
    try:
        os.mkdir(pdir)                                   # exclusive: an attempt folder is never reused
    except FileExistsError:
        raise Refusal('POINT_DIR_EXISTS_NOT_RERUN (use a new --attempt): ' + pdir)
    k16 = key[:16]
    gate = rho_gate(**(gate_args or {}), out_root=out_root)
    write_new(os.path.join(pdir, 'POINT_START_%s.json' % k16),
              {'schema': 'NGC_RHO_POINT_START_C3V003', 'utc': utc(), 'key': key, 'spec': spec_pin, 'attempt': attempt_no,
               'run_id': run_id, 'gate': gate, 'stage': {'path': STAGE_PATH}, 'producer_pin': {'path': PRODUCER[0], 'sha256': PRODUCER[1]},
               'thread_env': single_thread_env(), 'thread_env_parent': dict(PARENT_THREAD_ENV), 'pid': os.getpid()}, out_root)
    summary = {'key': key, 'attempt': attempt_no, 'point_dir': pdir, 'gate': gate['status'], 'attempts': {}}
    if not gate['open']:
        write_new(os.path.join(pdir, 'STAGE_RHO_HELD_%s.json' % k16),
                  {'schema': STAGE_SCHEMA, 'stage': 'RHO', 'utc': utc(), 'key': key, 'status': HELD, 'gate': gate,
                   'computed': False}, out_root)
        summary['status'] = HELD
        return EXIT_HELD, summary
    letters = ('a', 'b') if key == SEED_KEY else ('a',)
    for letter in letters:
        try:
            rc, info = spawn(spec_pin, key, out_root, attempt_no=attempt_no, letter=letter, gate_args=gate_args, run_id=run_id)
        except Exception as exc:                         # E4 (W7): a producer Refusal raised by an in-process spawn
            if not is_producer_refusal(exc):
                raise
            raise Refusal('PRODUCER_REFUSED_AT_ATTEMPT_%s: %s' % (letter, exc)) from None
        summary['attempts'][letter] = info
        if rc != 0:
            summary['status'] = 'STOPPED_AT_ATTEMPT_' + letter
            return EXIT_STOP, summary
    if key == SEED_KEY:
        diag = seed_pair_diagnostic(pdir, out_root, key)
        summary['seed_pair_diagnostic'] = write_new(os.path.join(pdir, 'SEED_PAIR_DIAGNOSTIC_%s.json' % k16), diag, out_root)
    summary['status'] = 'DONE'
    return EXIT_OK, summary


def plan():
    return {'schema': 'NGC_RHO_STAGE_PLAN_C3V003', 'stage': STAGE_PATH, 'producer': list(PRODUCER), 'slot_proof': list(SLOT_PROOF),
            'seed_key': SEED_KEY, 'attempts': 'a (all points); b at the seed only, each in a separate process',
            'gate': '--allow-rho + --root-review-pin {path,sha256} + --root-review-sha256; else ' + HELD,
            'members': 'numerics.route_a.column_workers == int 1 only (0717 R4: the cw8 twin gets no rho record; %s)' % TWIN_CODE,
            'environment': {'qos': ('not required (E9; A166, FROM_CODEX/0740): the attempt processes inherit the caller\'s '
                                    'scheduling'), 'interpreter': 'python3 -I -B', 'blas': single_thread_env()},
            'out_root': 'an existing canonical directory named %s*' % OUT_PREFIX}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description='NGC rho stage c3v003')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('plan')
    r = sub.add_parser('run')
    w = sub.add_parser('attempt')
    for p in (r, w):
        p.add_argument('--spec-pin', required=True)
        p.add_argument('--point', required=True)
        p.add_argument('--out-root', required=True)
        p.add_argument('--attempt', type=int, default=1)
        p.add_argument('--run-id', default='')
        p.add_argument('--allow-rho', action='store_true')
        p.add_argument('--root-review-pin')
        p.add_argument('--root-review-sha256')
    w.add_argument('--letter', required=True, choices=('a', 'b'))
    ns = ap.parse_args(argv)
    if not isolated_interpreter():                       # E9 (A166): no QoS check; the interpreter and BLAS checks stay
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B, no -O)', flush=True)
        return EXIT_SETUP
    if any(v != '1' for v in single_thread_env().values()):
        print('REFUSED: SINGLE_THREAD_BLAS_ENV_REQUIRED', flush=True)
        return EXIT_SETUP
    if ns.cmd == 'plan':
        print(json.dumps(plan(), sort_keys=True), flush=True)
        return EXIT_OK
    try:
        spec_pin = json.loads(ns.spec_pin)
        g = gate_args_from_cli(ns)
        if ns.cmd == 'run':
            rc, summary = run_point(spec_pin, ns.point, ns.out_root, attempt_no=ns.attempt, gate_args=g, run_id=ns.run_id)
        else:
            rc, summary = attempt(spec_pin, ns.point, ns.out_root, attempt_no=ns.attempt, letter=ns.letter, gate_args=g,
                                  run_id=ns.run_id)
    except CAUGHT as exc:
        print(json.dumps({'verdict': 'REFUSED', 'blocker': type(exc).__name__ + ': ' + str(exc)}), flush=True)
        return EXIT_SETUP
    print(json.dumps({'exit': rc, 'summary': summary}, sort_keys=True, default=str), flush=True)
    return rc


if __name__ == '__main__':
    sys.exit(main())
