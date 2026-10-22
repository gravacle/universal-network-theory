# dev helper (work copy, continuation run 3): fill the {{...}} placeholders of dev/README_SEAL_TOOLS_V003.md from the final published run and
# the mutation result, writing dev/README_SEAL_TOOLS_V003.filled.md (exclusive create); each placeholder must occur exactly once.
# usage: python3 -I -B fill_readme_c4v003.py RUN_DIR MUTATION_JSON UTC
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
run, mut, utc = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_bytes()), sys.argv[3]
res = json.loads((run / 'TEST_RESULTS_C4V003.json').read_bytes())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


files = [('seal_common_c4v003.py', 'shared helpers'), ('check_frozen_addendum_c4v003.py', 'tool 1'), ('check_sealed_compare_c4v003.py', 'tool 2'),
         ('check_slot_fill_c4v003.py', 'tool 3'), ('build_seal_record_c4v003.py', 'tool 4 (builder, admission check)'),
         ('print_driver_build_record_c4v003.py', 'tool 5'), ('tests/test_seal_tools_c4v003.py', 'tests'),
         ('tests/%s/TEST_RESULTS_C4V003.json' % run.name, 'final run record'), ('DELTA_V002R2_TO_V003.md', 'every changed source line, with its reason'),
         ('MUTATION_C4V003.json', 'mutation check'), ('tools/fence_c4v002.py', 'fence (v002 copy)'), ('tools/run_fenced_c4st2.py', 'fenced runner (v002 copy)'),
         ('tools/make_mutants_final_c4v003.py', 'mutant generator'), ('tools/run_one_mutant_c4v003.sh', 'one-mutant runner'),
         ('tools/analyze_mutants_final_c4v003.py', 'mutation analysis'), ('tools/make_delta_c4v003.py', 'DELTA generator'),
         ('tools/delta_reasons_c4v003.py', 'DELTA reasons'), ('tools/publish_c4v003.py', 'exclusive-create publisher')]
for f, _ in files:
    assert f.startswith('tests/') or (HERE / f).is_file() or f in ('DELTA_V002R2_TO_V003.md', 'MUTATION_C4V003.json'), f
table = '| file | role | sha256 |\n|---|---|---|\n'
for f, role in files:
    p = HERE / f
    if not p.is_file():                        # DELTA and MUTATION are published with this README: their dev copies have the same bytes
        p = HERE / 'dev' / {'DELTA_V002R2_TO_V003.md': 'delta/DELTA_V002R2_TO_V003.md', 'MUTATION_C4V003.json': 'MUTATION_C4V003_ROUND2.json'}[f]
    table += '| `%s` | %s | `%s` |\n' % (f, role, sha(p))
by_tag = ', '.join('%s %s' % (k, v) for k, v in sorted(res['by_tag'].items()))
vals = {'{{UTC}}': utc, '{{FINAL_PASSED}}': str(res['passed']), '{{FINAL_TOTAL}}': str(res['total']), '{{FINAL_BY_TAG}}': by_tag,
        '{{FINAL_RUN}}': run.name, '{{FINAL_RESULTS_SHA}}': sha(run / 'TEST_RESULTS_C4V003.json'),
        '{{MUT_KILLED}}': str(mut['counts'].get('KILLED', 0)), '{{MUT_TOTAL}}': str(mut['total']), '{{FILES_TABLE}}': table.rstrip('\n')}
s = (HERE / 'dev' / 'README_SEAL_TOOLS_V003.md').read_text()
for k, v in vals.items():
    assert s.count(k) == 1, (k, s.count(k))
    s = s.replace(k, v)
assert '{{' not in s
with open(HERE / 'dev' / 'README_SEAL_TOOLS_V003.filled.md', 'x') as f:
    f.write(s)
print(hashlib.sha256(s.encode('utf-8')).hexdigest())
