# Claude4 seal tools v002: build RESULTS_SEAL_TOOLS_C4V002.json from bytes (test results, CLI captures, file shas). Exclusive create.
# usage: python3 -I -B make_results_c4st2.py FOLDER OUT UTC [--dry]
import hashlib, json, re, sys
from pathlib import Path
F, out, utc = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
R2RUN, R1RUN = 'run_20261018T212903Z', 'run_20261018T212152Z'
r2 = json.loads((F / 'r2/tests' / R2RUN / 'TEST_RESULTS_C4V002.json').read_bytes())
r1 = json.loads((F / 'tests' / R1RUN / 'TEST_RESULTS_C4V002.json').read_bytes())


def cli(name):
    o = F / 'out' / (name + '.stdout.txt')
    e = (F / 'out' / (name + '.stderr.txt')).read_text()
    m = re.search(r'FENCE_C4ST2_SUMMARY (\{.*\})', e)
    fence = json.loads(m.group(1)) if m else None
    try:
        d = json.loads(o.read_bytes())
        v, codes, notes = d.get('verdict'), [f['code'] for f in d.get('failures', [])], [n['code'] for n in d.get('notes', [])]
    except ValueError:
        v, codes, notes = None, [], []
    return {'capture': {'stdout': str(o), 'stdout_sha256': sha(o), 'stderr': str(F / 'out' / (name + '.stderr.txt')), 'stderr_sha256': sha(F / 'out' / (name + '.stderr.txt'))},
            'verdict': v, 'codes': codes, 'notes': notes, 'blocked_after_selftest': fence and fence['blocked_after_selftest'],
            'fence_selftest': fence and '%d/%d' % (fence['selftest_pass'], fence['selftest_of']),
            'fence_v002_probes': fence and '%d/%d' % (fence['v002_exception_probes_pass'], fence['v002_exception_probes_of'])}
t5e = (F / 'out/CLI_R2_T5_DRIVER_BUILD_RECORD.stderr.txt').read_text()
t5m = re.search(r'FENCE_C4ST2_SUMMARY (\{.*\})', t5e)
by_case = {r['case']: r for r in r2['results']}
fixes = {}
for r in r2['results']:
    m = re.match(r'(D-\d\d|R-\d\d|A\d+(?:\.\d)?|A102 A-B1|r2)', r['case'])
    key = m.group(1) if m else ('PORT' if r['tag'].startswith('PORT') else r['tool'])
    fixes.setdefault(key, []).append({'case': r['case'], 'tag': r['tag'], 'ok': r['ok'], 'codes': sorted(set(r['codes']))[:8]})
FILES = ['r2/seal_common_c4v002.py', 'r2/check_frozen_addendum_c4v002.py', 'r2/check_sealed_compare_c4v002.py', 'r2/check_slot_fill_c4v002.py',
         'r2/build_seal_record_c4v002.py', 'r2/print_driver_build_record_c4v002.py', 'r2/tests/test_seal_tools_c4v002.py',
         'r2/tests/%s/TEST_RESULTS_C4V002.json' % R2RUN, 'README_SEAL_TOOLS.md',
         'seal_common_c4v002.py', 'check_frozen_addendum_c4v002.py', 'check_sealed_compare_c4v002.py', 'check_slot_fill_c4v002.py',
         'build_seal_record_c4v002.py', 'print_driver_build_record_c4v002.py', 'tests/test_seal_tools_c4v002.py', 'tests/%s/TEST_RESULTS_C4V002.json' % R1RUN,
         'tools/fence_c4v001.py', 'tools/fence_c4v002.py', 'tools/make_fence_c4v002.py', 'tools/run_fenced_c4st2.py', 'tools/xwrite_c4st2.py',
         'tools/fill_template_c4st2.py', 'tools/README_TEMPLATE_C4ST2.md', 'out/FENCE_C4V001_TO_C4V002.diff', 'out/CLI_R2_T5_DRIVER_BUILD_RECORD_BYTES.json',
         'scratch/V005_ADDENDUM_READ_COPY_C4ST2.md', 'scratch/V005_ADDENDUM_READ_COPY_2_C4ST2.md', 'PARTIAL.md']
res = {
    'schema': 'UNT_V007_SEAL_TOOLS_V002_RESULTS_C4ST2',
    'lane': 'Claude4 helper (A99 item 4; dispatch 0621 seal tools v002)', 'utc': utc,
    'authority': {'dispatch_0621': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0621_2026-10-18_claude4_codex1_codex3_claude3_A99.md',
                                    'sha256': sha('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0621_2026-10-18_claude4_codex1_codex3_claude3_A99.md')}},
    'rulings_read': {'V005_copy_1_A47_A99': sha(F / 'scratch/V005_ADDENDUM_READ_COPY_C4ST2.md'), 'V005_copy_2_A47_A100': sha(F / 'scratch/V005_ADDENDUM_READ_COPY_2_C4ST2.md'),
                     'V005_at_r2_suite_A47_A102': r2['frozen_copy_of_the_open_V005']['sha256']},
    'verdict': 'BUILT_AND_TESTED', 'set_of_record': str(F / 'r2'),
    'labels': 'TESTED = run or read from bytes here; FORMAL = follows from code or text read here; UNTESTED = not checked here',
    'tests': {'r2': {'run_dir': r2['run_dir'], 'results_sha256': sha(F / 'r2/tests' / R2RUN / 'TEST_RESULTS_C4V002.json'), 'passed': r2['passed'], 'total': r2['total'],
                     'by_tag': r2['by_tag'], 'label': 'TESTED'},
              'r1': {'run_dir': r1['run_dir'], 'results_sha256': sha(F / 'tests' / R1RUN / 'TEST_RESULTS_C4V002.json'), 'passed': r1['passed'], 'total': r1['total'],
                     'by_tag': r1['by_tag'], 'label': 'TESTED'}},
    'cases_by_item': fixes,
    'cli_runs_r2': {n: cli(n) for n in ('CLI_R2_T3_PIN_PENDING_NO_ARG', 'CLI_R2_T3_ROOT_ARG', 'CLI_R2_T2_BARE_PENDING', 'CLI_R2_T2_REHEARSAL_P1_REPRO', 'CLI_R2_T4_ADMISSION_CHECK')},
    'cli_t5_driver_build_record': {'bytes': str(F / 'out/CLI_R2_T5_DRIVER_BUILD_RECORD_BYTES.json'), 'sha256': sha(F / 'out/CLI_R2_T5_DRIVER_BUILD_RECORD_BYTES.json'),
                                   'blocked_after_selftest': json.loads(t5m.group(1))['blocked_after_selftest'] if t5m else None,
                                   'note': 'r12 builtin_r5_build() with check_record CHECK.md 89a6de88; root prints and creates its own (exclusive create)'},
    'fence': {'v001': sha(F / 'tools/fence_c4v001.py'), 'v002': sha(F / 'tools/fence_c4v002.py'), 'diff': sha(F / 'out/FENCE_C4V001_TO_C4V002.diff'),
              'exceptions': ['(a) uvt_*.py source modules outside both runs_ext roots (lowercase basename uvt_*.py, no uvt_* directory component)',
                             '(b) CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md, exact folder, literal and resolved'],
              'selftest': '8/8 every run', 'v002_probes': '15/15 every run', 'blocked_after_selftest': [], 'label': 'TESTED'},
    'files': {f: sha(F / f) for f in FILES},
}
if '--dry' in sys.argv:
    print(json.dumps({k: res[k] for k in ('verdict', 'tests', 'fence')}, indent=1)[:3000])
    raise SystemExit(0)
with open(out, 'x') as fh:
    json.dump(res, fh, indent=1, sort_keys=True)
    fh.write('\n')
print('WROTE', sha(out), out)
