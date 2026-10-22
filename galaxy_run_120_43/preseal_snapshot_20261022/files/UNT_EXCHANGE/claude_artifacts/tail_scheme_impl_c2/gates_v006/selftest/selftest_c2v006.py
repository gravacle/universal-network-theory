"""c2v006 selftest driver (Claude2 gates_v006).  Synthetic trees only; no real run is read.
Runs, under each driver selection r4 and r5, as separate processes (python3 -I -B, single-thread BLAS):
  A  Codex2 reproducible counterexamples (ported, ported_cx2/): source_audit whole-gate (9 cases: B1 key collision, structured
     npz/npy, storage order, duplicate JSON key, ordinary controls) + duplicate NPZ members (2 cases); every non-baseline must
     FAIL and name the c2v006 check that owns the finding (REQUIRED below).
  B  Codex2 c2v005 canary suites (ported): structural 23 cases (gate Z2_OFF), invocation/value 24 cases (P17 re-declared FAIL
     under ARRAY_POLICY).  These are the c2v005-era canary sets (gates_v005/selftest/ holds no builder canary set on bytes).
  C+D canaries_c2v006.py: the c2v004 CHECK canary set ported onto c2v005/6-valid trees, and own c2v006 canaries.
  S  source / unit checks: load_cm, load_driver and driver_tables execute or parse the bytes they hashed (AST: no
     spec_from_file_location, no read of a path after hashing); Store re-hash detects a changed file (unit).
Writes SELFTEST_C2V006.json (exclusive) into --out.
  python3 -I -B selftest_c2v006.py --comparator C --out DIR
"""
import argparse
import ast
import datetime
import hashlib
import json
import os
import subprocess
import sys
import types
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
HERE = Path(__file__).resolve().parent
P = HERE / 'ported_cx2'
REQUIRED_A = {'key_collision': ['NORM_INJECTIVE'], 'duplicate_json_key': ['STRICT_PARSE'], 'duplicate_npz_member': ['STRICT_PARSE'],
              'structured_npz': ['STAGES'], 'structured_npy': ['STAGES'], 'npz_storage_order': ['STAGES'], 'npy_storage_order': ['STAGES'],
              'ordinary_result_change': ['RESULT'], 'ordinary_result_extra': ['RESULT']}
# c2v006 policy re-declaration: the Codex2 source-audit fixture's positive control carries the literal normalizer text '<RUN>/x'
# as a result.json key on both sides.  c2v006 refuses raw normalizer text (normalization would not be injective), so the
# baseline is expected to FAIL on NORM_INJECTIVE (RAW_TEXT_CONTAINS_NORMALIZER_TOKEN) and on nothing else.  The plain-key
# form of the same positive control is canaries_c2v006 D_O30 (MUST_PASS).
OVERRIDE_A = {'baseline': {'should_pass': False, 'required': ['NORM_INJECTIVE'], 'only': ['NORM_INJECTIVE'],
                           'why': 'fixture key <RUN>/x is raw normalizer text (c2v006 NORM_INJECTIVE policy)'}}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(cmd, env_extra=None, log=None):
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
    env.update(env_extra or {})
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if log:
        with open(log, 'x') as f:
            f.write('$ %s\n--- stdout\n%s\n--- stderr\n%s\n--- rc %d\n' % (' '.join(cmd), p.stdout, p.stderr, p.returncode))
    return p


def source_checks(cmp_path):
    src = Path(cmp_path).read_text()
    tree = ast.parse(src)
    fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    out = {}
    for name in ('load_cm', 'load_driver', 'driver_raw'):
        seg = ast.get_source_segment(src, fn[name])
        out[name] = {'no_spec_from_file_location': 'spec_from_file_location' not in seg and 'importlib' not in seg,
                     'exec_compile_of_hashed_bytes': (name == 'driver_raw') or ('exec(compile(raw' in seg)}
    seg = ast.get_source_segment(src, fn['auto_custody'])
    out['auto_custody_reference_driver_tables_from_hashed_bytes'] = 'driver_tables(raw, rdrv)' in seg and 'sha_b(raw) == rsha' in seg
    seg = ast.get_source_segment(src, fn['_compare'])
    out['compare_uses_store_for_run_files'] = 'read_json(' not in src and 'read_text()' not in seg
    # unit: Store detects a change after its read
    m = types.ModuleType('_c6_unit')
    m.__file__ = str(cmp_path)
    exec(compile(Path(cmp_path).read_bytes(), str(cmp_path), 'exec'), m.__dict__)
    return out, m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--comparator', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    C = str(Path(a.comparator).resolve())
    S = sha(C)
    res = {'A': {}, 'B': {}, 'CD': {}, 'S': {}}
    for drv in ('r4', 'r5'):
        # A: Codex2 source-audit counterexamples
        for tag, script in (('whole_gate', 'test_whole_gate_edge_cases_cx2v001_port_c2v006.py'), ('duplicate_npz', 'test_duplicate_npz_members_cx2v001_port_c2v006.py')):
            d = out / ('A_%s_%s' % (tag, drv))
            p = run([PY, '-I', '-B', str(P / script), C, S, str(d), drv], log=str(out / ('A_%s_%s.log' % (tag, drv))))
            rj = d / 'RESULTS.json'
            rows = json.loads(rj.read_bytes())['rows'] if rj.is_file() else []
            chk = []
            for r in rows:
                ov = OVERRIDE_A.get(r['name'])
                need = ov['required'] if ov else REQUIRED_A.get(r['name'], [])
                want = ov['should_pass'] if ov else r['should_pass']
                ok = (r['actual_pass'] == want) and all(x in (r['failing'] or []) for x in need)
                if ov and ov.get('only') is not None:
                    ok = ok and sorted(r['failing'] or []) == sorted(ov['only'])
                extra = {}
                if r['name'] == 'key_collision':  # the B1 exploit must be reported as a KEY_COLLISION naming both raw keys
                    rep_ = json.loads(Path(r['report']['path']).read_bytes())
                    kc = [c for c in rep_['checks']['NORM_INJECTIVE']['detail']['new'] if c.get('kind') == 'KEY_COLLISION']
                    extra = {'key_collision_entries': kc}
                    ok = ok and any(len(c.get('raw_keys', [])) == 2 and '<RUN>/x' in c['raw_keys'] and c['raw_keys'][0].endswith('/new/x') for c in kc)
                chk.append(dict({'name': r['name'], 'should_pass_cx2': r['should_pass'], 'should_pass_c2v006': want, 'actual_pass': r['actual_pass'],
                                 'failing': r['failing'], 'required_failing': need, 'override': ov, 'ok': ok}, **extra))
            res['A']['%s_%s' % (tag, drv)] = {'rc': p.returncode, 'results': str(rj), 'results_sha256': sha(rj) if rj.is_file() else None,
                                              'n': len(chk), 'ok': sum(c['ok'] for c in chk), 'rows': chk}
        # B: structural + invocation
        d = out / ('B_structural_%s' % drv)
        d.mkdir()
        p = run([PY, '-I', '-B', str(P / 'run_structural_canaries_cx2v002_port_c2v006.py'), '--comparator', C, '--sha256', S, '--driver', drv],
                env_extra={'C2V006_PORT_OUT': str(d)}, log=str(out / ('B_structural_%s.log' % drv)))
        runs = sorted(d.glob('run_*/STRUCTURAL_RESULTS.json'))
        sj = json.loads(runs[-1].read_bytes()) if runs else {}
        res['B']['structural_%s' % drv] = {'rc': p.returncode, 'results': str(runs[-1]) if runs else None, 'results_sha256': sha(runs[-1]) if runs else None,
                                           'passed': sj.get('passed'), 'total': sj.get('total'),
                                           'failed': [c['case'] for c in sj.get('cases', []) if not c['pass']]}
        d = out / ('B_invocation_%s' % drv)
        p = run([PY, '-I', '-B', str(P / 'invocation_canaries_cx2v003_port_c2v006.py'), '--comparator', C, '--sha256', S, '--out', str(d), '--driver', drv],
                log=str(out / ('B_invocation_%s.log' % drv)))
        ij = json.loads((d / 'RESULT.json').read_bytes()) if (d / 'RESULT.json').is_file() else {}
        res['B']['invocation_%s' % drv] = {'rc': p.returncode, 'results': str(d / 'RESULT.json'),
                                           'results_sha256': sha(d / 'RESULT.json') if (d / 'RESULT.json').is_file() else None,
                                           'passed': ij.get('passed'), 'total': ij.get('total'), 'unexpected': ij.get('unexpected')}
        # C + D
        d = out / ('CD_canaries_%s' % drv)
        p = run([PY, '-I', '-B', str(HERE / 'canaries_c2v006.py'), '--comparator', C, '--sha256', S, '--driver', drv, '--out', str(d)],
                log=str(out / ('CD_canaries_%s.log' % drv)))
        cj = json.loads((d / 'CANARIES_C2V006.json').read_bytes()) if (d / 'CANARIES_C2V006.json').is_file() else {}
        res['CD']['canaries_%s' % drv] = {'rc': p.returncode, 'results': str(d / 'CANARIES_C2V006.json'),
                                          'results_sha256': sha(d / 'CANARIES_C2V006.json') if (d / 'CANARIES_C2V006.json').is_file() else None,
                                          'summary': cj.get('summary'), 'n': len(cj.get('rows', []))}
    sc, m = source_checks(C)
    ud = out / 'S_unit_store'
    ud.mkdir()
    f = ud / 'x.json'
    with open(f, 'x') as fh:
        fh.write('{"a": 1}')
    st = m.Store(ud, 'unit')
    v1 = st.json(f)
    with open(f, 'r+') as fh:
        fh.write('{"a": 2}')
    changed = st.verify()
    sc['store_verify_detects_change_after_single_read'] = bool(changed) and v1 == {'a': 1}
    dk = None
    try:
        m.jloads(b'{"k": 1, "k": 1}')
    except m.DuplicateKey as e:
        dk = str(e)
    sc['jloads_refuses_equal_duplicate'] = dk is not None
    res['S'] = sc
    tot_ok = (all(v['ok'] == v['n'] and v['n'] > 0 for v in res['A'].values())
              and all(v['passed'] == v['total'] and v['total'] for v in res['B'].values())
              and all(v['summary'] and not v['summary']['breaches'] for v in res['CD'].values())
              and all((x if isinstance(x, bool) else all(x.values())) for x in sc.values()))
    rep = {'schema': 'SELFTEST_C2V006_V001', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'comparator': {'path': C, 'sha256': S, 'sha256_at_end': sha(C)}, 'harness': {'path': str(Path(__file__).resolve()), 'sha256': sha(__file__)},
           'ported_sources': {p_.name: sha(p_) for p_ in sorted(P.glob('*.py'))},
           'results': res, 'verdict': 'PASS' if tot_ok and sha(C) == S else 'FAIL'}
    with open(out / 'SELFTEST_C2V006.json', 'x') as fh:
        json.dump(rep, fh, indent=1)
    print(json.dumps({'verdict': rep['verdict'],
                      'A': {k: [v['ok'], v['n']] for k, v in res['A'].items()},
                      'B': {k: [v['passed'], v['total'], v.get('failed') or v.get('unexpected')] for k, v in res['B'].items()},
                      'CD': {k: v['summary'] for k, v in res['CD'].items()}, 'S': sc}, indent=1))


if __name__ == '__main__':
    main()
