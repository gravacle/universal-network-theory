# Claude4 lens_diff: line diffs of the r14 harness files against their r13 parents (read-only; exclusive writes here).
import difflib, hashlib, json
from pathlib import Path

C = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2')
OUT = Path(__file__).resolve().parent.parent / 'out'
PAIRS = [
    ('author_r13_vs_r14', 'r13/tests_kmax_tail_compare_c2v007_r13_cx3v001.py', 'r14/tests_kmax_tail_compare_c2v007_r14_cx1v001.py'),
    ('author_r13_vs_r14copy_v001', 'r13/tests_kmax_tail_compare_c2v007_r13_cx3v001.py', 'r14/tests_kmax_tail_compare_c2v007_r13_cx3v001.py'),
    ('author_v001_vs_v002', 'r14/tests_kmax_tail_compare_c2v007_r13_cx3v001.py', 'r14/tests_kmax_tail_compare_c2v007_r14_cx1v001.py'),
    ('entry', 'r13/tools/author_entry_cx3v001.py', 'r14/tools/author_entry_cx3v001.py'),
    ('guard', 'r13/tools/guard_r13_cx3v001.py', 'r14/tools/guard_r13_cx3v001.py'),
    ('rmi_fixture_library', 'r13/record_mutation_independent/tools/fixture_library_cx3v001.py', 'r14/record_mutation_independent/tools/fixture_library_cx3v001.py'),
    ('rmi_guard', 'r13/record_mutation_independent/tools/guard_r13_cx3v001.py', 'r14/record_mutation_independent/tools/guard_r13_cx3v001.py'),
    ('rmi_mutation', 'r13/record_mutation_independent/tools/mutation_check_r13_cx3v001.py', 'r14/record_mutation_independent/tools/mutation_check_r13_cx3v001.py'),
    ('rmi_real', 'r13/record_mutation_independent/tools/real_record_check_r13_cx3v001.py', 'r14/record_mutation_independent/tools/real_record_check_r13_cx3v001.py'),
    ('rmi_run_checks', 'r13/record_mutation_independent/tools/run_checks_cx3v001.py', 'r14/record_mutation_independent/tools/run_checks_cx3v001.py'),
]
summary = {}
for tag, a, b in PAIRS:
    ba = (C / a).read_bytes(); bb = (C / b).read_bytes()
    la = ba.decode().splitlines(keepends=True); lb = bb.decode().splitlines(keepends=True)
    d = ''.join(difflib.unified_diff(la, lb, a, b, n=1))
    sm = difflib.SequenceMatcher(a=la, b=lb, autojunk=False)
    ops = [(t, i1 + 1, i2, j1 + 1, j2) for (t, i1, i2, j1, j2) in sm.get_opcodes() if t != 'equal']
    summary[tag] = {'a': a, 'a_sha256': hashlib.sha256(ba).hexdigest(), 'a_lines': len(la),
                    'b': b, 'b_sha256': hashlib.sha256(bb).hexdigest(), 'b_lines': len(lb),
                    'identical': ba == bb, 'n_hunks': len(ops), 'ops': ops,
                    'lines_removed': sum(i2 - i1 + 1 for (t, i1, i2, j1, j2) in ops if t in ('replace', 'delete')),
                    'lines_added': sum(j2 - j1 + 1 for (t, i1, i2, j1, j2) in ops if t in ('replace', 'insert'))}
    with open(OUT / ('HDIFF_%s.diff' % tag), 'x') as f:
        f.write(d)
with open(OUT / 'HDIFF_SUMMARY.json', 'x') as f:
    json.dump(summary, f, indent=1)
for k, v in summary.items():
    print(k, 'identical' if v['identical'] else 'hunks=%d -%d +%d' % (v['n_hunks'], v['lines_removed'], v['lines_added']),
          v['a_sha256'][:8], '->', v['b_sha256'][:8], 'lines', v['a_lines'], '->', v['b_lines'])
