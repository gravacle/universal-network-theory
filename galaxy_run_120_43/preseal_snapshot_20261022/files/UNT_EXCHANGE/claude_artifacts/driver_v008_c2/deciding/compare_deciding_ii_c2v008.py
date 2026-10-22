"""Deciding test (ii) comparator for driver c2v008 (Claude2 lane driver_v008_c2).  INERT on import; reads two run
directories, writes ONE report file (exclusive create).  numpy only.
C2V008: successor of driver_v007_c2/deciding/compare_deciding_ii_c2v007.py (aee8b7a6) with ONLY the CHECK_V001 C1 fix:
RA_IDENTITY verifies, per side, identity.caller.sha256 == digest(decode(identity.caller.record)) with the checkpoint
module's own digest/decode, and only then replaces caller.sha256 by the token <CALLER_SHA> (the caller digest covers the
run-dir seed path, the seed sha, the worker and the solver code_pin, so it differs on every correct new run).  The
decoded caller itself stays compared (its expected differences are tokenized like every other field).  Code
factored into identity_check() so the fixtures can call it on a real-caller IDENTITY.  Nothing else changed.

  python3 -I -B compare_deciding_ii_c2v008.py --reference REF_RUN --new NEW_RUN --column-workers N --out REPORT.json
         [--expect-new parallel|serial]   (default parallel; 'serial' only for the comparator's self-test REF vs REF)

REF_RUN = CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001 (driver c2v001, reviewed serial worker c4cb6826 + solver 44d9c23c).
NEW_RUN = the c2v008 call at the same spec with numerics.route_a.column_workers = N (parallel worker 9dbdaf11 + solver aed4dd59).

PASS (verdict PASS_BITWISE_EQUAL) requires every check below.  ROUTE-A OUTPUTS (stage *_route_a of both runs):
  RA_BLOBS        checkpoint/blobs: same file-name set; every file byte-identical (sha256 from bytes).
  RA_RECORDS      checkpoint/iteration_*/ records: same relative-path set; every record passes the checkpoint module's own
                  integrity read (payload self-hash, canonical bytes); content equal after dropping the identity-bound fields
                  attempt, payload_sha256, identity_sha256, iteration_start_sha256.
  RA_IDENTITY     IDENTITY.json: self-hash verifies on both sides; the identity is equal after replacing, per side, ONLY the
                  expected-to-differ values by tokens: run directory prefix, solver path+sha (ref serial 44d9c23c / new parallel
                  aed4dd59), route-A worker path+sha (ref c4cb6826 / new 9dbdaf11), seed sha (each run's own
                  inputs/seed_c2v001.json bytes).  Plus: ref code.solver == serial, new code.solver == parallel; decoded caller
                  worker == the side's worker.  C2V008 (C1): per side caller.sha256 == digest(decode(caller.record)) is
                  REQUIRED, then caller.sha256 is replaced by <CALLER_SHA> before the comparison.
  RA_SEED         the two seeds are equal except the c2_changed_fields annotation (numerical_inputs bitwise equal).
  RA_END          checkpoint/attempts: one start + one end record per side; end outcome and records_written equal.
  RA_RESULT       attempt_000/result.json equal after the same substitutions (+ attempt token, identity sha), top-level
                  elapsed_seconds dropped, and every array reference's file digest (NPZ zip bytes carry write timestamps)
                  replaced by the digest of the referenced array CONTENT (dtype, shape, bytes).
  RA_ARRAYS       attempt_000/arrays/*.npz: same names; every member array equal in dtype, shape and bytes.
  RA_NODES        attempt_000/node_diagnostics/*: same names; bytes equal after the same substitutions.
  RA_START        attempt_000/start.json equal after the substitutions, except the key column_workers (new only, == N) and the
                  seed copy's c2_changed_fields annotation (RA_SEED).
  RA_FINISH       attempt_000/finish.json status RETURNED_ACTUAL_RESULT on both.
  RA_ROWS         result.json identity.route_a.route_a_rows equal (the route-A worker's own 12 rows).
TWELVE SPEEDS (top-level result.json):
  SPEEDS          both status COMPLETED and valid True; speeds_km_s (12 ids) equal as JSON floats; rows equal; final_pass equal;
                  every pass's rows and max_abs_change_km_s equal.
NEW-RUN CUSTODY (c2v007/c2v008 records): identity.route_a.implementation == {column_workers N, PARALLEL_C2V001, worker 9dbdaf11,
  solver aed4dd59}; identity.route_a.custody.solver_code == the parallel solver; route_a_outcome CONVERGED at the reader's
  iteration (== the reference's converged iteration).
DIAGNOSTIC ONLY (never decides): attempt_000/progress.jsonl equal after the same normalization (event content and order;
  the parallel interface says only timing differs, and events carry no timing field)."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

CKPT = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py',
        '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114')
SERIAL = {'solver': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py',
                     '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644'),
          'worker': ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/ddo_composite_stable_cached_root_worker_v002.py',
                     'c4cb682669993afbad3c623a010244cc8a31b9fcbacfe44e6bc692bf2d5895a4')}
PARALLEL = {'solver': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_c2v001.py',
                       'aed4dd59b38bfe1043e0c38ad4592e4b6bb74c8c4bbee969a707a310926e6f58'),
            'worker': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/ddo_composite_stable_cached_root_worker_v002_parallel_c2v001.py',
                       '9dbdaf11eb80fd4fa8d47e8c0827eae51d06e87f05efdd6e5c11d422ecbd197a')}
RECORD_DROP = ('attempt', 'payload_sha256', 'identity_sha256', 'iteration_start_sha256')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load_ckpt_module():
    raw = Path(CKPT[0]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CKPT[1]:
        raise SystemExit('checkpoint module pin mismatch')
    import types
    m = types.ModuleType('ck_cmp_c2v008')
    m.__file__ = CKPT[0]
    exec(compile(raw, CKPT[0], 'exec'), m.__dict__)
    return m


def array_content_digest(npz, member):
    import numpy as np
    with np.load(npz, allow_pickle=False) as f:
        a = np.ascontiguousarray(f[member])
    h = hashlib.sha256((a.dtype.str + str(a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def first_diffs(a, b, path='', out=None, limit=20):
    out = [] if out is None else out
    if len(out) >= limit:
        return out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append(path + '.' + str(k) + (' (new only)' if k not in a else ' (ref only)'))
            else:
                first_diffs(a[k], b[k], path + '.' + str(k), out, limit)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append('%s (length %d vs %d)' % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            first_diffs(x, y, '%s[%d]' % (path, i), out, limit)
    elif a != b or type(a) is not type(b):
        out.append('%s: %s | %s' % (path, repr(a)[:120], repr(b)[:120]))
    return out


class Side:
    def __init__(self, run, code, label):
        self.run = Path(run).resolve()
        self.label = label
        st = sorted(self.run.glob('stages/*_route_a'))
        if len(st) != 1:
            raise SystemExit('%s: expected one *_route_a stage, found %s' % (label, st))
        self.ra = st[0]
        self.cp = self.ra / 'checkpoint'
        self.att = self.ra / 'attempt_000'
        self.code = code
        self.seed_path = self.run / 'inputs' / 'seed_c2v001.json'
        self.seed_sha = sha_file(self.seed_path)
        ident = json.loads((self.cp / 'IDENTITY.json').read_text())
        self.identity_sha = ident['identity_sha256']
        starts = sorted(x.name for x in (self.cp / 'attempts').glob('*.start.json'))
        self.attempt_tokens = [x[:-len('.start.json')] for x in starts]
        self.subs = [(str(self.run), '<RUN>'), (code['solver'][0], '<SOLVER_PATH>'), (code['solver'][1], '<SOLVER_SHA>'),
                     (code['worker'][0], '<WORKER_PATH>'), (code['worker'][1], '<WORKER_SHA>'), (self.seed_sha, '<SEED_SHA>'),
                     (self.identity_sha, '<IDENTITY_SHA>')] + [(t, '<ATTEMPT>') for t in self.attempt_tokens]
        self.fired = {}

    def norm_text(self, s):
        for old, tok in self.subs:
            n = s.count(old)
            if n:
                self.fired[tok] = self.fired.get(tok, 0) + n
                s = s.replace(old, tok)
        return s

    def norm_bytes(self, b):
        for old, tok in self.subs:
            ob = old.encode()
            n = b.count(ob)
            if n:
                self.fired[tok] = self.fired.get(tok, 0) + n
                b = b.replace(ob, tok.encode())
        return b

    def norm_obj(self, obj):
        return json.loads(self.norm_text(json.dumps(obj, sort_keys=True)))


def identity_check(cm, ref, new):
    """RA_IDENTITY for two Sides.  C2V008 (CHECK_V001 C1): per side, identity.caller.sha256 must equal
    cm.digest(cm.decode(identity.caller.record)) (how the checkpoint module's _identity builds it); only then is it replaced
    by <CALLER_SHA>, and the identities are compared after the Side substitutions.  Returns (ok, detail)."""
    def ident(s):
        d = json.loads((s.cp / 'IDENTITY.json').read_text())
        ok = d['identity_sha256'] == cm._sha(cm._canonical(d['identity']))
        caller = cm.decode(d['identity']['caller']['record'])
        recorded = d['identity']['caller'].get('sha256')
        caller_ok = isinstance(recorded, str) and recorded == cm.digest(caller)
        tok = json.loads(json.dumps(d['identity']))
        if caller_ok:
            tok['caller']['sha256'] = '<CALLER_SHA>'  # verified; its expected per-run difference is not compared again
        return d['identity'], ok, caller, caller_ok, recorded, tok
    ir, okr, cr, cokr, csr, tr = ident(ref)
    inew, okn, cn, cokn, csn, tn = ident(new)
    nr, nn = ref.norm_obj(tr), new.norm_obj(tn)
    solver_ok = (ir['code'].get('solver') == {'path': ref.code['solver'][0], 'sha256': ref.code['solver'][1]}
                 and inew['code'].get('solver') == {'path': new.code['solver'][0], 'sha256': new.code['solver'][1]})
    worker_ok = (cr.get('worker') == {'path': ref.code['worker'][0], 'sha256': ref.code['worker'][1]}
                 and cn.get('worker') == {'path': new.code['worker'][0], 'sha256': new.code['worker'][1]})
    raw_diff = first_diffs(ir, inew, 'identity', limit=40)
    ok = okr and okn and cokr and cokn and nr == nn and solver_ok and worker_ok
    return ok, {'self_hash_reference': okr, 'self_hash_new': okn,
                'caller_sha256_is_digest_of_decoded_caller': {'reference': cokr, 'new': cokn},
                'caller_sha256': {'reference': csr, 'new': csn},
                'equal_after_expected_substitutions': nr == nn,
                'remaining_differences': first_diffs(nr, nn, 'identity'), 'solver_fields_as_expected': solver_ok,
                'caller_worker_as_expected': worker_ok, 'raw_differences_first40': raw_diff,
                'identity_sha256': {'reference': ref.identity_sha, 'new': new.identity_sha}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--reference', required=True)
    ap.add_argument('--new', required=True)
    ap.add_argument('--column-workers', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--expect-new', choices=('parallel', 'serial'), default='parallel')
    a = ap.parse_args(argv)
    out = Path(a.out)
    if out.exists():
        raise SystemExit('report exists: %s' % out)
    cm = load_ckpt_module()
    ref = Side(a.reference, SERIAL, 'reference')
    new = Side(a.new, PARALLEL if a.expect_new == 'parallel' else SERIAL, 'new')
    checks = {}

    def put(name, ok, detail):
        checks[name] = {'pass': bool(ok), 'detail': detail}
        print(('PASS ' if ok else 'FAIL ') + name, flush=True)

    # RA_BLOBS
    bl = {s.label: {p.name: sha_file(p) for p in sorted((s.cp / 'blobs').iterdir()) if p.is_file()} for s in (ref, new)}
    bad = sorted(n for n in set(bl['reference']) | set(bl['new']) if bl['reference'].get(n) != bl['new'].get(n))
    named_ok = all(n.split('.')[0] == h for d in bl.values() for n, h in d.items() if n.endswith('.npy'))
    put('RA_BLOBS', not bad and bl['reference'] and named_ok,
        {'n_reference': len(bl['reference']), 'n_new': len(bl['new']), 'differing_or_missing': bad[:20],
         'names_are_content_sha256': named_ok})

    # RA_RECORDS
    def records(s):
        res, errors = {}, []
        for p in sorted(s.cp.glob('iteration_*/*.json')):
            rel = s.norm_text(str(p.relative_to(s.cp)))  # a FAILURE.<attempt token>.json name is token-normalized
            name = p.name
            kind = ('iteration_start' if name == 'START.json' else 'iteration_completed' if name == 'COMPLETED.json'
                    else 'column' if name.startswith('column_') else 'failure' if name.startswith('FAILURE') else None)
            try:
                body = cm._read(str(p), kind) if kind else json.loads(p.read_text())
            except Exception as exc:
                errors.append('%s: %s' % (rel, exc))
                continue
            res[rel] = {k: v for k, v in body.items() if k not in RECORD_DROP}
        return res, errors
    rr, er = records(ref)
    rn, en = records(new)
    diff = sorted(k for k in set(rr) | set(rn) if rr.get(k) != rn.get(k))
    put('RA_RECORDS', not diff and not er and not en and rr,
        {'n_reference': len(rr), 'n_new': len(rn), 'differing_or_missing': diff[:20],
         'first_field_diffs': first_diffs(rr.get(diff[0]), rn.get(diff[0])) if diff and diff[0] in rr and diff[0] in rn else None,
         'integrity_errors_reference': er[:5], 'integrity_errors_new': en[:5]})

    # RA_IDENTITY (C2V008: identity_check, with the C1 caller-digest fix)
    ok, detail = identity_check(cm, ref, new)
    put('RA_IDENTITY', ok, detail)

    # RA_SEED
    sr, sn = json.loads(ref.seed_path.read_text()), json.loads(new.seed_path.read_text())
    strip = lambda s: {k: v for k, v in s.items() if k != 'c2_changed_fields'}
    put('RA_SEED', strip(sr) == strip(sn) and sr['numerical_inputs'] == sn['numerical_inputs'],
        {'seed_sha256': {'reference': ref.seed_sha, 'new': new.seed_sha},
         'annotation': {'reference': sr.get('c2_changed_fields', {}).get('driver'), 'new': sn.get('c2_changed_fields', {}).get('driver')},
         'differences_outside_annotation': first_diffs(strip(sr), strip(sn))})

    # RA_END
    def ends(s):
        e = [cm._read(str(p), 'attempt_end') for p in sorted((s.cp / 'attempts').glob('*.end.json'))]
        return e, len(s.attempt_tokens)
    er_, nsr = ends(ref)
    en_, nsn = ends(new)
    ok = (len(er_) == len(en_) == 1 and nsr == nsn == 1 and er_[0]['outcome'] == en_[0]['outcome']
          and er_[0]['records_written'] == en_[0]['records_written'])
    put('RA_END', ok, {'reference': [{k: x.get(k) for k in ('outcome', 'records_written')} for x in er_],
                       'new': [{k: x.get(k) for k in ('outcome', 'records_written')} for x in en_],
                       'attempt_starts': {'reference': nsr, 'new': nsn}})

    # RA_RESULT
    content = {}

    def content_refs(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get('array_file'), str) and 'sha256' in obj and 'member' in obj:
                key = (obj['array_file'], obj['member'])
                if key not in content:
                    content[key] = array_content_digest(obj['array_file'], obj['member'])
                obj = dict(obj, sha256='CONTENT:' + content[key])
            return {k: content_refs(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [content_refs(v) for v in obj]
        return obj

    def result(s):
        r = json.loads((s.att / 'result.json').read_text())
        r.pop('elapsed_seconds', None)
        return s.norm_obj(content_refs(r))
    rres, nres = result(ref), result(new)
    put('RA_RESULT', rres == nres, {'remaining_differences': first_diffs(rres, nres, 'result'),
                                    'array_refs_content_digested': len(content)})

    # RA_ARRAYS
    import numpy as np
    an = {s.label: sorted(p.name for p in (s.att / 'arrays').glob('*.npz')) for s in (ref, new)}
    bad = []
    if an['reference'] != an['new']:
        bad.append('name sets differ')
    else:
        for n in an['reference']:
            with np.load(ref.att / 'arrays' / n, allow_pickle=False) as fa, np.load(new.att / 'arrays' / n, allow_pickle=False) as fb:
                if sorted(fa.files) != sorted(fb.files):
                    bad.append(n + ' members')
                    continue
                for k in fa.files:
                    x, y = fa[k], fb[k]
                    if x.dtype != y.dtype or x.shape != y.shape or x.tobytes() != y.tobytes():
                        bad.append('%s[%s]' % (n, k))
    put('RA_ARRAYS', not bad and an['reference'], {'n': len(an['reference']), 'differing': bad[:20]})

    # RA_NODES
    nd = {s.label: sorted(p.name for p in (s.att / 'node_diagnostics').iterdir() if p.is_file()) for s in (ref, new)}
    bad = []
    if nd['reference'] != nd['new']:
        bad.append('name sets differ')
    else:
        for n in nd['reference']:
            with open(ref.att / 'node_diagnostics' / n, 'rb') as fa, open(new.att / 'node_diagnostics' / n, 'rb') as fb:
                i = 0
                while True:
                    la, lb = fa.readline(), fb.readline()
                    if not la and not lb:
                        break
                    i += 1
                    if ref.norm_bytes(la) != new.norm_bytes(lb):
                        bad.append('%s line %d' % (n, i))
                        break
    put('RA_NODES', not bad and nd['reference'], {'files': nd['reference'], 'differing': bad[:20]})

    # RA_START / RA_FINISH
    sr_ = json.loads((ref.att / 'start.json').read_text())
    sn_ = json.loads((new.att / 'start.json').read_text())
    cw = sn_.pop('column_workers', None)
    for x in (sr_, sn_):  # the seed copy in start.json: its annotation is checked by RA_SEED
        if isinstance(x.get('seed'), dict):
            x['seed'].pop('c2_changed_fields', None)
    cw_ok = (cw == a.column_workers) if a.expect_new == 'parallel' else (cw is None)
    nsr_, nsn_ = ref.norm_obj(sr_), new.norm_obj(sn_)
    put('RA_START', nsr_ == nsn_ and cw_ok, {'column_workers_new': cw, 'remaining_differences': first_diffs(nsr_, nsn_, 'start')})
    fr, fn = json.loads((ref.att / 'finish.json').read_text()), json.loads((new.att / 'finish.json').read_text())
    put('RA_FINISH', fr.get('status') == fn.get('status') == 'RETURNED_ACTUAL_RESULT', {'reference': fr.get('status'), 'new': fn.get('status')})

    # top-level results
    Rr = json.loads((ref.run / 'result.json').read_text())
    Rn = json.loads((new.run / 'result.json').read_text())
    put('RA_ROWS', Rr['identity']['route_a'].get('route_a_rows') == Rn['identity']['route_a'].get('route_a_rows')
        and Rr['identity']['route_a'].get('route_a_rows') is not None,
        {'n': len(Rr['identity']['route_a'].get('route_a_rows') or [])})
    pr, pn = Rr.get('passes') or [], Rn.get('passes') or []
    pass_rows = [{'pass': x.get('pass'), 'rows_equal': x.get('rows') == y.get('rows'),
                  'max_abs_change_equal': x.get('max_abs_change_km_s') == y.get('max_abs_change_km_s')} for x, y in zip(pr, pn)]
    ok = (Rr.get('status') == Rn.get('status') == 'COMPLETED' and Rr.get('valid') is True and Rn.get('valid') is True
          and isinstance(Rr.get('speeds_km_s'), dict) and len(Rr['speeds_km_s']) == 12 and Rr['speeds_km_s'] == Rn.get('speeds_km_s')
          and Rr.get('rows') == Rn.get('rows') and Rr.get('final_pass') == Rn.get('final_pass') and len(pr) == len(pn)
          and all(x['rows_equal'] and x['max_abs_change_equal'] for x in pass_rows))
    put('SPEEDS', ok, {'status': [Rr.get('status'), Rn.get('status')], 'valid': [Rr.get('valid'), Rn.get('valid')],
                       'n_speeds': [len(Rr.get('speeds_km_s') or {}), len(Rn.get('speeds_km_s') or {})],
                       'speeds_equal': Rr.get('speeds_km_s') == Rn.get('speeds_km_s'), 'rows_equal': Rr.get('rows') == Rn.get('rows'),
                       'final_pass': [Rr.get('final_pass'), Rn.get('final_pass')], 'passes': pass_rows,
                       'speed_differences': {k: [Rr['speeds_km_s'].get(k), (Rn.get('speeds_km_s') or {}).get(k)]
                                             for k in (Rr.get('speeds_km_s') or {}) if Rr['speeds_km_s'].get(k) != (Rn.get('speeds_km_s') or {}).get(k)}})
    if a.expect_new == 'parallel':
        ra = Rn['identity']['route_a']
        exp_impl = {'column_workers': a.column_workers, 'kind': 'PARALLEL_C2V001',
                    'worker': {'path': PARALLEL['worker'][0], 'sha256': PARALLEL['worker'][1]},
                    'solver': {'path': PARALLEL['solver'][0], 'sha256': PARALLEL['solver'][1]}}
        oc = Rn.get('route_a_outcome') or {}
        ok = (ra.get('implementation') == exp_impl
              and (ra.get('custody') or {}).get('solver_code') == {'path': PARALLEL['solver'][0], 'sha256': PARALLEL['solver'][1]}
              and oc.get('classification') == 'CONVERGED' and oc.get('converged_iteration') == (ra.get('custody') or {}).get('iteration')
              and (ra.get('custody') or {}).get('iteration') == (Rr['identity']['route_a'].get('custody') or {}).get('iteration', 4))
        put('NEW_CUSTODY', ok, {'implementation': ra.get('implementation'), 'solver_code': (ra.get('custody') or {}).get('solver_code'),
                                'route_a_outcome': {k: oc.get(k) for k in ('classification', 'converged_iteration', 'outcome')},
                                'custody_iteration': (ra.get('custody') or {}).get('iteration')})

    # diagnostic: progress.jsonl
    def prog(s):
        lines = (s.att / 'progress.jsonl').read_text().splitlines()
        return [s.norm_obj(content_refs(json.loads(x))) for x in lines if x.strip()]
    try:
        ppr, ppn = prog(ref), prog(new)
        diag = {'events': [len(ppr), len(ppn)], 'equal': ppr == ppn,
                'first_difference': next((i for i, (x, y) in enumerate(zip(ppr, ppn)) if x != y), None)}
    except Exception as exc:
        diag = {'error': '%s: %s' % (type(exc).__name__, exc)}
    report = {'schema': 'UNT_DRIVER_V008_DECIDING_II_COMPARE_V001', 'comparator': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
              'reference': str(ref.run), 'new': str(new.run), 'column_workers': a.column_workers, 'expect_new': a.expect_new,
              'checks': checks, 'diagnostic_progress_jsonl': diag,
              'expected_substitutions_fired': {'reference': ref.fired, 'new': new.fired},
              'verdict': 'PASS_BITWISE_EQUAL' if all(c['pass'] for c in checks.values()) else 'FAIL',
              'failing': [k for k, c in checks.items() if not c['pass']]}
    with open(out, 'x') as f:
        json.dump(report, f, indent=1, default=str)
        f.write('\n')
    print(json.dumps({'verdict': report['verdict'], 'failing': report['failing']}))
    return 0 if report['verdict'] == 'PASS_BITWISE_EQUAL' else 1


if __name__ == '__main__':
    sys.exit(main())
