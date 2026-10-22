"""Mutation check for phase1_c2v003 (SYNTHETIC ONLY; dev evidence for the A144 build, not a record of any value).

Each mutant is phase1_c2v003.py with exactly one A144 / A135-item-10 site changed (exact substring, present once).  The
mutant and an unchanged copy of test_phase1_c2v003.py are written to
<this dir>/test_runs_v003/MUTATION_<UTC>_<pid>/<mutant>/ (exclusive create), and the suite runs there (python3 -I -B);
a mutant is KILLED when its run has at least one FAIL.  The tool and the tests next to this file are only read.

usage: <codex python3> -I -B mutation_phase1_c2v003.py
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(os.path.dirname(os.path.realpath(__file__)))
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
OUT = HERE / 'test_runs_v003' / ('MUTATION_%s_%d' % (STAMP, os.getpid()))
MUTANTS = {
    'M01_region_test_without_the_lp_max_clip': ("v = A @ c - np.maximum(b, 0.0)", "v = A @ c - b"),
    'M02_region_test_exact_comparison': ("bool(np.any(v[fam[f]] > E._LP_EPS))", "bool(np.any(v[fam[f]] > 0.0))"),
    'M03_e_q_back_to_the_A137_formula': (
        "coef = abs(1.0 - float(np.sum(d / du))) + float(np.sum(np.abs(d) / h))",
        "coef = 2.0 * float(np.sum(np.abs(d) / h))"),
    'M04_BOX_before_TRUST_RADIUS': ("REGION_FAMILIES = ('TRUST_RADIUS', 'BOX', 'LINEAR_DDO')",
                                    "REGION_FAMILIES = ('BOX', 'TRUST_RADIUS', 'LINEAR_DDO')"),
    'M05_no_L1_module_custody': ("    if l1.get('module') != MODULE:   # A144 custody", "    if False:   # A144 custody"),
    'M06_no_certificate_map_scope_check': ("            if other:\n                bad.append",
                                           "            if False:\n                bad.append"),
    'M07_no_members_eps_contract': ("    check_member_eps(mv, len(mvals['query_ids']))", "    pass"),
    'M08_negative_member_eps_accepted': ("    if e < 0:\n        return None, 'MEMBER_EPS_NEGATIVE'",
                                         "    if False:\n        return None, 'MEMBER_EPS_NEGATIVE'"),
    'M09_single_point_ignores_LP_status': (
        "        if any(s != 'OPTIMAL' for x in res for s in x['lp_status']):\n            return 'NOT_AVAILABLE'",
        "        if False:\n            return 'NOT_AVAILABLE'"),
    'M10_e_q_without_eps_m': ("                    e = eq = eps_m + bounded", "                    e = eq = bounded"),
    'M11_unbounded_member_pair_gets_e_q_0': (
        "                    e = eq = bounded\n                    flag = 'MEMBER_POINT",
        "                    e = eq = 0.0\n                    flag = 'MEMBER_POINT"),
    'M12_e_q_with_unsigned_du': ("coef = abs(1.0 - float(np.sum(d / du)))", "coef = abs(1.0 - float(np.sum(d / h)))"),
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(name):
    d = OUT / name
    p = subprocess.run([PY, '-I', '-B', str(d / 'test_phase1_c2v003.py')], capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if not k.startswith('PYTHON')})
    res = sorted((d / 'test_runs_v003').glob('RUN_*/RESULTS.json'))
    if not res:
        return name, {'killed': True, 'note': 'no RESULTS.json (crash)', 'rc': p.returncode, 'stderr': p.stderr[-400:]}
    doc = json.loads(res[-1].read_text())
    fails = [r['id'] for r in doc['results'] if not r['pass']]
    return name, {'killed': bool(fails), 'n_fail': len(fails), 'n': doc['summary']['n'], 'failing_checks': fails,
                  'rc': p.returncode}


def main():
    src = (HERE / 'phase1_c2v003.py').read_text()
    test = (HERE / 'test_phase1_c2v003.py').read_bytes()
    OUT.mkdir(parents=True)
    for name, (a, b) in MUTANTS.items():
        if src.count(a) != 1:
            raise SystemExit('mutation site %s found %d times' % (name, src.count(a)))
        (OUT / name).mkdir()
        with open(OUT / name / 'phase1_c2v003.py', 'x') as fh:
            fh.write(src.replace(a, b))
        with open(OUT / name / 'test_phase1_c2v003.py', 'xb') as fh:
            fh.write(test)
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = dict(ex.map(run, sorted(MUTANTS)))
    summary = {'tool_sha256': sha(HERE / 'phase1_c2v003.py'), 'test_sha256': sha(HERE / 'test_phase1_c2v003.py'),
               'mutants': len(MUTANTS), 'killed': sum(1 for r in results.values() if r['killed']),
               'survivors': sorted(n for n, r in results.items() if not r['killed'])}
    with open(OUT / 'MUTATION_RESULTS.json', 'x') as fh:
        json.dump({'summary': summary, 'results': results,
                   'mutations': {n: {'from': a, 'to': b} for n, (a, b) in MUTANTS.items()}}, fh, indent=1)
    print(json.dumps(dict(summary, out=str(OUT)), indent=1))
    return 0 if not summary['survivors'] else 1


if __name__ == '__main__':
    sys.exit(main())
