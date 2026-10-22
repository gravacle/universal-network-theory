# Claude4 seal tools v002: fill a Markdown template's placeholders from bytes and write the result with exclusive create.
# {UTC} = argv UTC; {SHA:rel} = sha256 of <folder>/rel; {R2_PASSED} {R2_TOTAL} {R2_TAGS} {R2_RUN} from the r2 test results;
# {FILES_TABLE} = a sha table of the delivered files. Refuses (exit 1, nothing written) if a placeholder is left or a file is missing.
# usage: python3 -I -B fill_template_c4st2.py FOLDER TEMPLATE OUT UTC R2_RUN
import hashlib, json, re, sys
from pathlib import Path

folder, template, out, utc, r2run = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
t = template.read_text()
res = json.loads((folder / 'r2/tests' / r2run / 'TEST_RESULTS_C4V002.json').read_bytes())
t = t.replace('{UTC}', utc).replace('{R2_RUN}', r2run).replace('{R2_PASSED}', str(res['passed'])).replace('{R2_TOTAL}', str(res['total']))
t = t.replace('{R2_TAGS}', ', '.join('%s %s' % (k, v) for k, v in sorted(res['by_tag'].items())))
FILES = ['r2/seal_common_c4v002.py', 'r2/check_frozen_addendum_c4v002.py', 'r2/check_sealed_compare_c4v002.py', 'r2/check_slot_fill_c4v002.py',
         'r2/build_seal_record_c4v002.py', 'r2/print_driver_build_record_c4v002.py', 'r2/tests/test_seal_tools_c4v002.py',
         'r2/tests/%s/TEST_RESULTS_C4V002.json' % r2run,
         'seal_common_c4v002.py', 'check_frozen_addendum_c4v002.py', 'check_sealed_compare_c4v002.py', 'check_slot_fill_c4v002.py',
         'build_seal_record_c4v002.py', 'print_driver_build_record_c4v002.py', 'tests/test_seal_tools_c4v002.py',
         'tools/fence_c4v001.py', 'tools/fence_c4v002.py', 'tools/make_fence_c4v002.py', 'tools/run_fenced_c4st2.py', 'tools/xwrite_c4st2.py',
         'out/FENCE_C4V001_TO_C4V002.diff']
rows = ['| file | role | sha256 |', '|---|---|---|']
for f in FILES:
    role = ('r2 (of record)' if f.startswith('r2/') else 'r1 (superseded by r2)' if f.endswith('_c4v002.py') and not f.startswith('tools/') else 'fence / tools' if f.startswith('tools/') else 'evidence')
    rows.append('| `%s` | %s | `%s` |' % (f, role, sha(folder / f)))
t = t.replace('{FILES_TABLE}', '\n'.join(rows))
t = re.sub(r'\{SHA:([^}]+)\}', lambda m: sha(folder / m.group(1)), t)
left = re.findall(r'\{[A-Z_0-9]+(?::[^}]*)?\}', t)
if left:
    print('REFUSED: placeholders left: %r' % left)
    raise SystemExit(1)
with open(out, 'x') as fh:
    fh.write(t)
print('WROTE', sha(out), out)
