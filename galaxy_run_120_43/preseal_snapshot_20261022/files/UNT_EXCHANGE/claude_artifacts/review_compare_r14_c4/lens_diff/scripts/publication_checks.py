# Claude4 lens_diff: SELECTED V001 vs V002, IMPL V001 vs V002, and the author / real / mutation rosters of r14 vs r13 (read-only).
import hashlib, json
from pathlib import Path
C = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2')
R14 = C / 'r14'; R13 = C / 'r13'
OUT = Path(__file__).resolve().parent.parent / 'out' / 'PUBLICATION_CHECKS_C4.json'
H = lambda b: hashlib.sha256(b).hexdigest()
res = {}
s1 = json.loads((R14 / 'SELECTED_R14_CX1V001.json').read_bytes()); s2 = json.loads((R14 / 'SELECTED_R14_CX1V002.json').read_bytes())
res['selected_keys_v1'] = sorted(s1); res['selected_keys_v2'] = sorted(s2)
res['selected_fields_differing'] = sorted(k for k in set(s1) | set(s2) if s1.get(k) != s2.get(k))
res['selected_v2_supersedes_v1_sha'] = s2.get('supersedes_selection', {}).get('sha256') == H((R14 / 'SELECTED_R14_CX1V001.json').read_bytes())
i1 = (R14 / 'COMPARE_V007_IMPL_R14.md').read_bytes(); i2 = (R14 / 'COMPARE_V007_IMPL_R14_CX1V002.md').read_bytes()
res['impl_v2_starts_with_v1_bytes'] = i2.startswith(i1)
res['impl_v2_appended'] = i2[len(i1):].decode() if i2.startswith(i1) else None
res['impl_v2_names_r14_sha_full'] = b'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7' in i2
res['impl_v1_names_r14_sha_full'] = b'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7' in i1

def roster(p):
    d = json.loads(Path(p).read_bytes())
    return d, [(t['test'], t['pass'], t.get('outcome'), t.get('expected'), t.get('subtype')) for t in d['tests']]
d13, r13 = roster(R13 / 'out/author_cx3v001/TEST_SUMMARY.json')
d14, r14 = roster(R14 / 'out/author_v002/TEST_SUMMARY.json')
d14a, r14a = roster(R14 / 'out/author_v001/TEST_SUMMARY.json')
res['author_r13'] = {'n': d13['n'], 'n_pass': d13['n_pass'], 'script_sha256': d13.get('script_sha256'), 'tests_sha256': d13.get('tests_sha256')}
res['author_r14_v002'] = {'n': d14['n'], 'n_pass': d14['n_pass'], 'script_sha256': d14.get('script_sha256'), 'tests_sha256': d14.get('tests_sha256')}
res['author_r14_v001'] = {'n': d14a['n'], 'n_pass': d14a['n_pass'], 'script_sha256': d14a.get('script_sha256'), 'tests_sha256': d14a.get('tests_sha256'),
                          'failed': [t[0] for t in r14a if not t[1]]}
ids13 = [t[0] for t in r13]; ids14 = [t[0] for t in r14]
new_ids = [x for x in ids14 if x not in set(ids13)]
res['author_new_ids'] = new_ids
res['author_ids_r13_order_preserved'] = [x for x in ids14 if x in set(ids13)] == ids13
res['author_dup_ids_r14'] = sorted({x for x in ids14 if ids14.count(x) > 1})
res['author_dup_ids_r13'] = sorted({x for x in ids13 if ids13.count(x) > 1})
# inherited tests: same (pass, outcome, expected, subtype)?  compare by position among inherited
inh14 = [t for t in r14 if t[0] in set(ids13)]
res['author_inherited_rows_identical'] = inh14 == r13
res['author_inherited_rows_differing'] = [[a, b] for a, b in zip(r13, inh14) if a != b][:20]
pos = ids14.index(new_ids[0]) if new_ids else None
res['author_new_ids_position'] = [pos, ids14[pos - 1] if pos else None]
# real and mutation rosters
def load(p):
    return json.loads(Path(p).read_bytes())
real14 = load(R14 / 'out/real_v001.json')
res['real_r14_keys'] = sorted(real14)[:30]
mut14 = load(R14 / 'out/mutation_v001/MUTATION_R13.json')
res['mutation_r14_keys'] = sorted(mut14)[:30]
with open(OUT, 'x') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1)[:6000])
