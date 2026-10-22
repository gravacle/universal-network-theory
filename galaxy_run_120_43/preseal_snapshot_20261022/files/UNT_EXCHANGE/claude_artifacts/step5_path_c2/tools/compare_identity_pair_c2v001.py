"""compare_identity_pair_c2v001.py -- the NGC serial = parallel identity test (A132; A133 1.4).  Booleans only.

THE PAIR.  Two run trees of driver cx3r008 (577f8c94) at one theta: the serial call of record (spec leaf
numerics.route_a.column_workers 1) and its identity twin (column_workers 8).  Both specs are the fill_step5_c2v001
output for one handoff; the tool checks from bytes that they differ only in that leaf, and that each run's
inputs/call_spec.json is its pinned spec.

WHAT IS COMPARED (the I4 producer's idea, write_i4_record_c3v003 707395ba, cut to what one NGC route-A stage writes
by iteration k; the checkpoint module c2v003 069b3935 is loaded inert from verified bytes for its own record reader,
canonical form and decoder):
  C1 custody   stages/NN_route_a/request.json: the driver-planned worker and solver per side (serial ee27227c / 8ef3079b;
               twin 293a417f / 7667025b); '--column-workers', '8' exactly once, right after '--start-iteration', '0', on
               the twin only; otherwise the argv lists are equal after the run-root, worker and solver tokens.
  C2 identity  checkpoint/IDENTITY.json per side: record integrity (the module's _read) and identity_sha256 =
               sha256(canonical(identity)); then across sides: format, fixed_source, environment, inputs_sha256,
               shapes, controls, code.checkpoint and code.modules equal; code.solver = the side's planned solver; the
               decoded caller identity equal after the run-root, worker and solver tokens (its sha256 verified per side).
  C3 payloads  for every compared iteration k: iteration_k/START.json, COMPLETED.json and column_00000 ... column_{n-1}
               (n = column_count) present on both sides, each read with the module's integrity check; equal after
               removing only the identity-chain fields (identity_sha256, iteration_start_sha256, attempt,
               payload_sha256); per side, every iteration_start_sha256 equals that side's START payload_sha256; no
               FAILURE record in a compared iteration.
  C4 digests   every blob a compared START / COMPLETED names exists on its side and hashes to its name (content
               addressing, so equal references mean byte-equal arrays).
  C5 sidecar   uv_tail_sidecar/SIDECAR_IDENTITY.json per side: identity_sha256 = sha256(canon(identity)) and
               identity.checkpoint_identity_sha256 = that side's checkpoint identity; across sides the identity is equal
               without checkpoint_identity_sha256 (run-root tokens).  iteration_k.json: 'payload' equal (the
               'diagnostics' block holds wall-clock seconds and per-process cache counters, controller L494-506);
               elements_k.npz arrays digest per side to the payload's positions_digest and J_digest.
Nothing else is read.  No value is printed or recorded: the record holds booleans, counts and relative paths only.
Iteration 0 is required; --iterations N compares 0..N-1 (root rules N; 2 covers the first warm-state transfer).

VERDICT.  SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON only when every check holds; DIFFERENT when a compared file
differs; NOT_READY when an iteration to compare is not complete on both sides (re-run later; nothing is decided).
Exit 0 equal, 1 different, 3 refused (no record), 4 not ready (record written).

  PY -I -B compare_identity_pair_c2v001.py --serial RUN_S --twin RUN_T --serial-spec S --serial-spec-sha256 H
       --twin-spec T --twin-spec-sha256 H [--iterations N] --out RECORD.json
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

SCHEMA = 'UNT_STEP5_NGC_IDENTITY_PAIR_RECORD_C2V001'
EQUAL = 'SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
DRIVER = (ART + '/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
          '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377')
CHECKPOINT = (ART + '/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py',
              '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114')
W = ART + '/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/'
V = ART + '/tail_scheme_impl_c2/route_a/'
ROLE = {
    'serial': {'column_workers': 1,
               'worker': (W + 'ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py',
                          'ee27227c2cee3093589ae6b6546a0d88a1bbe20c47ba4dacff497ad7cc80189f'),
               'solver': (V + 'coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py',
                          '8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469')},
    'twin': {'column_workers': 8,
             'worker': (W + 'ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py',
                        '293a417f493fee2b59176bc60873fa3cdea5e586f375efbe51cbd10651e045b1'),
             'solver': (V + 'coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py',
                        '7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db')}}
LEAF = ('numerics', 'route_a', 'column_workers')
CHAIN = ('identity_sha256', 'iteration_start_sha256', 'attempt', 'payload_sha256')
IDENTITY_EQUAL = ('format', 'fixed_source', 'environment', 'inputs_sha256', 'shapes', 'controls')
STAGE_RE = re.compile(r'[0-9]{2}_route_a')
NGC_WORDS = ('target', 'velocit', 'vobs', 'v_obs', 'rotcur', 'rotmod', 'observed')


class Refused(Exception):
    pass


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def pinned(path, digest, what):
    try:
        b = Path(path).read_bytes()
    except OSError as exc:
        raise Refused('%s unreadable (%s)' % (what, type(exc).__name__))
    if sha_b(b) != digest:
        raise Refused('%s is not %s' % (what, digest[:12]))
    return b


def strict(b, what):
    def pairs(ps):
        d = {}
        for k, v in ps:
            if k in d:
                raise Refused('DUPLICATE_JSON_KEY ' + what)
            d[k] = v
        return d
    try:
        return json.loads(b.decode('utf-8'), object_pairs_hook=pairs)
    except (UnicodeDecodeError, ValueError):
        raise Refused('UNPARSEABLE_JSON ' + what)


def protected(p):
    s = os.path.normpath(str(p)).casefold()
    parts = s.split('/')
    if any(x.startswith('uvt_') for x in parts) or 'kmax_a2f10_c5h' in s or s == '/.vol' or s.startswith('/.vol/'):
        return True
    return 'ngc3198' in s and any(w in s.replace('target_free', '').replace('target-free', '') for w in NGC_WORDS)


def load_checkpoint_module():
    pinned(CHECKPOINT[0], CHECKPOINT[1], 'checkpoint module')
    spec = importlib.util.spec_from_file_location('c2_identity_pair_checkpoint', CHECKPOINT[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    pinned(CHECKPOINT[0], CHECKPOINT[1], 'checkpoint module (after load)')
    return m


def strip_leaf(spec):
    s = copy.deepcopy(spec)
    node = s
    for k in LEAF[:-1]:
        node = node[k]
    return s, node.pop(LEAF[-1])


class Side:
    def __init__(self, role, run, cm):
        self.role, self.cm, self.want = role, cm, ROLE[role]
        run = Path(run)
        if not run.is_absolute() or protected(run) or protected(os.path.realpath(run)):
            raise Refused('run path refused: ' + role)
        if not run.is_dir():
            raise Refused('run directory missing: ' + role)
        self.run, self.real = str(run), os.path.realpath(run)
        st = [d for d in sorted(os.listdir(run / 'stages')) if STAGE_RE.fullmatch(d)] if (run / 'stages').is_dir() else []
        if len(st) != 1:
            raise Refused('%s: exactly one stages/NN_route_a directory required' % role)
        self.stage_name = st[0]
        self.stage = run / 'stages' / st[0]
        for q in (self.stage, self.stage / 'checkpoint', self.stage / 'uv_tail_sidecar'):
            if os.path.islink(q):
                raise Refused('symlink inside the run tree: ' + role)

    def tok(self, obj):
        """Run-root, worker and solver spellings -> role-free tokens (keys and values)."""
        reps = [(self.real, '<RUN>'), (self.run, '<RUN>'), (self.want['worker'][0], '<ROUTE_A_WORKER>'),
                (self.want['worker'][1], '<ROUTE_A_WORKER_SHA256>'), (self.want['solver'][0], '<ROUTE_A_SOLVER>'),
                (self.want['solver'][1], '<ROUTE_A_SOLVER_SHA256>')]

        def s(x):
            for a, b in reps:
                x = x.replace(a, b)
            return x
        if isinstance(obj, dict):
            return {s(k): self.tok(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.tok(v) for v in obj]
        return s(obj) if isinstance(obj, str) else obj

    def json(self, rel):
        p = self.stage / rel
        return strict(p.read_bytes(), self.role + ':' + rel)

    def record(self, rel, kind):
        p = self.stage / 'checkpoint' / rel
        if not p.is_file():
            return None
        try:
            return self.cm._read(str(p), kind)
        except self.cm.CheckpointError as exc:
            raise Refused('%s: checkpoint record %s fails its own integrity check (%s)' % (self.role, rel, str(exc).split(' ')[0]))


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False)


def compare(a):
    cm = load_checkpoint_module()
    pinned(DRIVER[0], DRIVER[1], 'driver')
    sb = pinned(a.serial_spec, a.serial_spec_sha256, 'serial spec')
    tb = pinned(a.twin_spec, a.twin_spec_sha256, 'twin spec')
    s_spec, s_leaf = strip_leaf(strict(sb, 'serial spec'))
    t_spec, t_leaf = strip_leaf(strict(tb, 'twin spec'))
    if (s_leaf, t_leaf) != (1, 8) or canon(s_spec) != canon(t_spec):
        raise Refused('the two specs must differ only in numerics.route_a.column_workers (1 vs 8)')
    if a.iterations < 1 or a.iterations > 32:
        raise Refused('--iterations must be 1..32')
    S, T = Side('serial', a.serial, cm), Side('twin', a.twin, cm)
    if S.real == T.real:
        raise Refused('the two runs are one directory')
    checks, diffs, counts, missing = {}, [], {'files_compared': 0, 'columns_compared': 0, 'blobs_verified': 0}, []
    for side, raw in ((S, sb), (T, tb)):
        p = Path(side.run) / 'inputs' / 'call_spec.json'
        checks['spec_pin_' + side.role] = p.is_file() and p.read_bytes() == raw
    checks['same_stage_directory'] = S.stage_name == T.stage_name
    # C1 custody
    reqs = {}
    for side in (S, T):
        r = side.json('request.json')
        w = side.want
        argv = [str(x) for x in r.get('argv', [])]
        ok = r.get('script') == w['worker'][0] and r.get('script_sha256') == w['worker'][1]
        ok = ok and argv.count('--solver') == 1 and argv[argv.index('--solver') + 1] == w['solver'][0]
        ok = ok and argv.count('--solver-sha256') == 1 and argv[argv.index('--solver-sha256') + 1] == w['solver'][1]
        n = argv.count('--column-workers')
        if side.role == 'twin':
            i = argv.index('--column-workers') if n == 1 else -1
            ok = ok and n == 1 and argv[i + 1] == '8' and argv[i - 2:i] == ['--start-iteration', '0']
            argv = argv[:i] + argv[i + 2:] if n == 1 else argv
        else:
            ok = ok and n == 0
        checks['custody_' + side.role] = bool(ok)
        reqs[side.role] = side.tok(argv)
    checks['request_argv_equal_after_tokens'] = reqs['serial'] == reqs['twin']
    if not checks['request_argv_equal_after_tokens']:
        diffs.append(S.stage_name + '/request.json')
    # C2 identity
    ids = {}
    for side in (S, T):
        rec = side.record('IDENTITY.json', 'identity')
        if rec is None:
            raise Refused(side.role + ': checkpoint/IDENTITY.json missing (the run has not started route A)')
        ident = rec['identity']
        checks['identity_digest_' + side.role] = sha_b(cm._canonical(ident)) == rec['identity_sha256']
        caller = cm.decode(ident['caller']['record'])
        checks['caller_digest_' + side.role] = cm.digest(caller) == ident['caller']['sha256']
        checks['solver_pin_' + side.role] = ident['code']['solver'] == {'path': side.want['solver'][0], 'sha256': side.want['solver'][1]}
        side.identity_sha256 = rec['identity_sha256']
        ids[side.role] = (ident, side.tok(ident['caller']['record']))   # the exact encoded form (floats as hex)
    for k in IDENTITY_EQUAL:
        checks['identity_' + k] = canon(ids['serial'][0].get(k)) == canon(ids['twin'][0].get(k))
    checks['identity_code_checkpoint_modules'] = canon({k: ids['serial'][0]['code'][k] for k in ('checkpoint', 'modules')}) == \
        canon({k: ids['twin'][0]['code'][k] for k in ('checkpoint', 'modules')})
    checks['identity_caller_after_tokens'] = canon(ids['serial'][1]) == canon(ids['twin'][1])
    if not all(checks[k] for k in checks if k.startswith('identity_')):
        diffs.append(S.stage_name + '/checkpoint/IDENTITY.json')
    counts['files_compared'] += 1
    # C3/C4 iterations
    for k in range(a.iterations):
        it = 'iteration_%04d' % k
        recs = {}
        for side in (S, T):
            start = side.record(it + '/START.json', 'iteration_start')
            done = side.record(it + '/COMPLETED.json', 'iteration_completed')
            if start is None or done is None:
                missing.append('%s:%s' % (side.role, it))
                continue
            n = start['column_count']
            cols = [side.record(it + '/column_%05d.json' % j, 'column') for j in range(n)]
            if any(c is None for c in cols):
                missing.append('%s:%s/columns' % (side.role, it))
                continue
            fail = [x for x in os.listdir(side.stage / 'checkpoint' / it) if x.startswith('FAILURE.')]
            checks['%s_no_failure_%s' % (it, side.role)] = not fail
            chain = all(c['iteration_start_sha256'] == start['payload_sha256'] for c in cols) and \
                done['iteration_start_sha256'] == start['payload_sha256'] and \
                all(r['identity_sha256'] == side.identity_sha256 for r in [start, done] + cols)
            checks['%s_chain_%s' % (it, side.role)] = chain
            blobs_ok = True
            for r in (start, done):
                for v in r.values():
                    if isinstance(v, dict) and 'blob' in v and 'file_sha256' in v:
                        p = side.stage / 'checkpoint' / v['blob']
                        blobs_ok = blobs_ok and p.is_file() and sha_b(p.read_bytes()) == v['file_sha256'] and \
                            v['blob'] == 'blobs/' + v['file_sha256'] + '.npy'
                        counts['blobs_verified'] += 1
            checks['%s_blob_digests_%s' % (it, side.role)] = blobs_ok
            recs[side.role] = (start, done, cols)
        if len(recs) < 2:
            continue

        def body(r):
            return canon({x: y for x, y in r.items() if x not in CHAIN})
        (s0, s1, sc), (t0, t1, tc) = recs['serial'], recs['twin']
        for name, x, y in (('START.json', s0, t0), ('COMPLETED.json', s1, t1)):
            eq = body(x) == body(y)
            checks['%s_%s_equal' % (it, name.split('.')[0])] = eq
            counts['files_compared'] += 1
            if not eq:
                diffs.append('%s/checkpoint/%s/%s' % (S.stage_name, it, name))
        eqc = len(sc) == len(tc)
        for j, (x, y) in enumerate(zip(sc, tc)):
            counts['columns_compared'] += 1
            if body(x) != body(y):
                eqc = False
                diffs.append('%s/checkpoint/%s/column_%05d.json' % (S.stage_name, it, j))
        checks['%s_columns_equal' % it] = eqc
        # C5 sidecar iteration record
        pay = {}
        for side in (S, T):
            p = side.stage / 'uv_tail_sidecar' / ('%s.json' % it)
            if not p.is_file():
                missing.append('%s:sidecar %s' % (side.role, it))
                continue
            rec = strict(p.read_bytes(), side.role + ':sidecar ' + it)
            pl = rec.get('payload')
            el = pl.get('elements') if isinstance(pl, dict) else None
            ok = isinstance(el, dict) and el.get('file') == 'elements_%04d.npz' % k
            if ok:
                import numpy as np
                with np.load(side.stage / 'uv_tail_sidecar' / el['file'], allow_pickle=False) as f:
                    ok = _adigest(f['positions_m']) == el['positions_digest'] and _adigest(f['integrated_J']) == el['J_digest']
            checks['%s_sidecar_elements_%s' % (it, side.role)] = bool(ok)
            pay[side.role] = canon(pl)
        if len(pay) == 2:
            checks['%s_sidecar_payload_equal' % it] = pay['serial'] == pay['twin']
            counts['files_compared'] += 1
            if pay['serial'] != pay['twin']:
                diffs.append('%s/uv_tail_sidecar/%s.json' % (S.stage_name, it))
    # C5 sidecar identity
    sid = {}
    for side in (S, T):
        p = side.stage / 'uv_tail_sidecar' / 'SIDECAR_IDENTITY.json'
        if not p.is_file():
            missing.append(side.role + ':SIDECAR_IDENTITY.json')
            continue
        rec = strict(p.read_bytes(), side.role + ':SIDECAR_IDENTITY')
        ident = rec.get('identity')
        checks['sidecar_identity_digest_' + side.role] = isinstance(ident, dict) and \
            sha_b(json.dumps(ident, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()) == rec.get('identity_sha256')
        checks['sidecar_checkpoint_binding_' + side.role] = isinstance(ident, dict) and \
            ident.get('checkpoint_identity_sha256') == side.identity_sha256
        sid[side.role] = canon(side.tok({x: y for x, y in (ident or {}).items() if x != 'checkpoint_identity_sha256'}))
    if len(sid) == 2:
        checks['sidecar_identity_equal'] = sid['serial'] == sid['twin']
        counts['files_compared'] += 1
        if not checks['sidecar_identity_equal']:
            diffs.append(S.stage_name + '/uv_tail_sidecar/SIDECAR_IDENTITY.json')
    if missing:
        verdict = 'NOT_READY'
    elif all(checks.values()) and not diffs:
        verdict = EQUAL
    else:
        verdict = 'DIFFERENT'
    return {'schema': SCHEMA, 'verdict': verdict, 'bitwise_equal': verdict == EQUAL, 'iterations_compared': list(range(a.iterations)),
            'checks': checks, 'differing_files': sorted(set(diffs)), 'not_ready': sorted(missing), 'counts': counts,
            'pins': {'driver': {'path': DRIVER[0], 'sha256': DRIVER[1]}, 'checkpoint_module': {'path': CHECKPOINT[0], 'sha256': CHECKPOINT[1]},
                     'serial_spec': {'path': a.serial_spec, 'sha256': a.serial_spec_sha256},
                     'twin_spec': {'path': a.twin_spec, 'sha256': a.twin_spec_sha256},
                     'tool': {'path': os.path.realpath(__file__), 'sha256': sha_b(Path(__file__).read_bytes())}},
            'runs': {'serial': S.run, 'twin': T.run, 'stage': S.stage_name},
            'values_printed': False,
            'reading': 'A133 1.4: EQUAL makes the serial = parallel identity TESTED at this theta (later calls may run at 8 '
                       'workers; the re-binding key then excludes column_workers). DIFFERENT keeps every call serial; the twin is '
                       'recorded and not used. NOT_READY decides nothing.'}


def _adigest(a):
    import numpy as np
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ('serial', 'twin', 'serial-spec', 'serial-spec-sha256', 'twin-spec', 'twin-spec-sha256', 'out'):
        ap.add_argument('--' + k, required=True)
    ap.add_argument('--iterations', type=int, default=1)
    a = ap.parse_args(argv)
    try:
        out = Path(a.out)
        if not out.is_absolute() or os.path.lexists(out) or not out.parent.is_dir() or protected(out):
            raise Refused('--out must be absolute, absent, with an existing parent')
        rec = compare(a)
    except Refused as exc:
        print('REFUSED: %s' % exc, file=sys.stderr)
        return 3
    except (OSError, KeyError, TypeError, ValueError, IndexError, AttributeError) as exc:
        print('REFUSED: %s' % type(exc).__name__, file=sys.stderr)
        return 3
    b = (json.dumps(rec, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    with open(out, 'xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    print(json.dumps({'verdict': rec['verdict'], 'record': str(out), 'sha256': sha_b(b)}))
    return {EQUAL: 0, 'DIFFERENT': 1, 'NOT_READY': 4}[rec['verdict']]


if __name__ == '__main__':
    sys.exit(main())
