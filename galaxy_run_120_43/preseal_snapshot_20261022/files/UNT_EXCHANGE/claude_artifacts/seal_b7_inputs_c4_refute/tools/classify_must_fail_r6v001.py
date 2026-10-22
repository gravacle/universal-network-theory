# Claude4 refute helper (dispatch 0650, refute_p6): for every must_fail_tests name in the builder's two NEW-item files, list the
# run-of-record tests it resolves to (the generator's own name_matches) and each test's 'expected' field, to see which resolved
# tests are controls (expected ADOPT-like) rather than must-fail. Read-only; prints JSON. Run under tools/run_fenced_c4st2.py.
import hashlib, importlib.util, json, sys
from pathlib import Path
B = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4')
spec = importlib.util.spec_from_file_location('gen', str(B / 'tools' / 'make_new_items_c4v001.py'))
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
out = {}
for v, fn in (('r13', 'NEW_ITEM_DISPOSITIONS_V007.json'), ('r14', 'NEW_ITEM_DISPOSITIONS_V007_R14_VARIANT.json')):
    run_path, run_sha = G.VARIANTS[v]['run']
    raw = Path(run_path).read_bytes(); assert hashlib.sha256(raw).hexdigest() == run_sha
    tests = json.loads(raw)['tests']
    obj = json.loads((B / fn).read_bytes())
    rows = []
    for it in obj['items']:
        for n in it['must_fail_tests']:
            hit = [t for t in tests if G.name_matches(n, t['test'])]
            exp = {}
            for t in hit:
                exp.setdefault(str(t.get('expected'))[:60], []).append(t['test'])
            rows.append({'id': it['id'], 'name': n, 'n_resolved': len(hit), 'all_pass': all(t.get('pass') is True for t in hit),
                         'expected_values': {k: len(x) for k, x in exp.items()},
                         'control_like': [t['test'] for t in hit if 'ADOPT' in str(t.get('expected')) and 'NO_ADOPT' not in str(t.get('expected'))]})
    out[v] = rows
print(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False))
