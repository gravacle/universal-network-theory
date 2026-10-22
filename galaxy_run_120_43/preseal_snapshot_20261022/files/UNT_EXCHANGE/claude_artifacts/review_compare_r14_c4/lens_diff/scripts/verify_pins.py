# Claude4 lens_diff: verify every {path, sha256[, bytes]} pin in the r14 publication records from bytes; check the pin graph.
# Read-only on author files; one exclusive write into this review folder.
import hashlib, json, os
from pathlib import Path

R14 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14')
OUT = Path(__file__).resolve().parent.parent / 'out' / 'PINS_R14_C4.json'
RECORDS = ['SELECTED_R14_CX1V001.json', 'SELECTED_R14_CX1V002.json', 'HASHES_R14_CX1V001.json', 'HASHES_R14_CX1V002.json',
           'VALIDATION_R14_CX1V001.json', 'SOURCE_DELTA_CX1V001.json', 'BUILD_PROGRESS_CX1V001.json',
           'out/AUTHOR_EXIT_V002.json', 'out/SUITE_EXITS_V001.json']
GIVEN = {  # the dispatch's stated pins (full where given, prefix where the dispatch gave a prefix)
    'SELECTED_R14_CX1V001.json': 'dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533',
    'kmax_tail_compare_c2v007_r14_cx1v001.py': 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7',
    'FIELDS_R14_CX1V002.md': '2ce9f1c7', 'FIELDS_R14_CX1V001.md': 'a33b153b', 'COMPARE_V007_IMPL_R14.md': '854cad0d',
    'VALIDATION_R14_CX1V001.json': '930ca7bc', 'tests_kmax_tail_compare_c2v007_r14_cx1v001.py': '998e0c2e',
    'SOURCE_DELTA_CX1V001.json': '56a95b7e', 'HASHES_R14_CX1V001.json': '8b92153a',
}
R13_SRC = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'

def sha_of(p):
    b = Path(p).read_bytes()
    return hashlib.sha256(b).hexdigest(), len(b)

def pins(obj, where):
    out = []
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj:
            out.append({'record': where, 'path': obj['path'], 'sha256': obj['sha256'], 'bytes': obj.get('bytes')})
        for k, v in obj.items():
            out += pins(v, where + '.' + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += pins(v, where + '[%d]' % i)
    return out

res = {'records': {}, 'pins': [], 'failures': [], 'given_vs_bytes': {}}
all_pins = []
for r in RECORDS:
    p = R14 / r
    s, n = sha_of(p)
    res['records'][r] = {'sha256': s, 'bytes': n}
    all_pins += pins(json.loads(p.read_bytes()), r)
for pn in all_pins:
    try:
        s, n = sha_of(pn['path'])
        ok_sha = s == pn['sha256']
        ok_bytes = pn['bytes'] is None or pn['bytes'] == n
        pn.update({'actual_sha256': s, 'actual_bytes': n, 'ok': ok_sha and ok_bytes})
    except Exception as e:  # missing file, or the fence refused it
        pn.update({'ok': False, 'error': repr(e)[:200]})
    res['pins'].append(pn)
    if not pn['ok']:
        res['failures'].append(pn)
for name, want in GIVEN.items():
    s, _ = sha_of(R14 / name)
    res['given_vs_bytes'][name] = {'given': want, 'actual': s, 'ok': s.startswith(want)}
s13, n13 = sha_of(R13_SRC)
res['given_vs_bytes']['r13 source'] = {'given': 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157', 'actual': s13,
                                       'ok': s13 == 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'}

# pin graph over files in the r14 publication: who pins whose sha; check acyclicity
edges = {}
for pn in all_pins:
    src = str(R14 / pn['record'].split('.')[0].split('[')[0]) if not pn['record'].startswith('out/') else str(R14 / pn['record'].split('.json')[0]) + '.json'
    edges.setdefault(src, set()).add(pn['path'])
# also: IMPL V002 names the source sha in its text
impl2 = (R14 / 'COMPARE_V007_IMPL_R14_CX1V002.md').read_text()
if 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7' in impl2:
    edges.setdefault(str(R14 / 'COMPARE_V007_IMPL_R14_CX1V002.md'), set()).add(str(R14 / 'kmax_tail_compare_c2v007_r14_cx1v001.py'))
def cyc(edges):
    color = {}; found = []
    def dfs(u, stack):
        color[u] = 1; stack.append(u)
        for v in edges.get(u, ()):  # noqa
            if color.get(v) == 1:
                found.append(stack[stack.index(v):] + [v])
            elif color.get(v) is None:
                dfs(v, stack)
        stack.pop(); color[u] = 2
    for u in list(edges):
        if color.get(u) is None:
            dfs(u, [])
    return found
res['pin_graph_edges'] = {k: sorted(v) for k, v in edges.items()}
res['pin_graph_self_pins'] = [k for k, v in edges.items() if k in v]
res['pin_graph_cycles'] = cyc(edges)

# which r14 publication files (top level + tools + record_mutation_independent/tools) are pinned anywhere
pinned_paths = {pn['path'] for pn in all_pins}
listing = []
for rel in sorted(os.listdir(R14)):
    if (R14 / rel).is_file():
        listing.append(rel)
for sub in ('tools', 'record_mutation_independent/tools'):
    for rel in sorted(os.listdir(R14 / sub)):
        if (R14 / sub / rel).is_file():
            listing.append(sub + '/' + rel)
res['publication_files'] = [{'file': f, 'sha256': sha_of(R14 / f)[0], 'pinned_by_any_record': str(R14 / f) in pinned_paths}
                            for f in listing]
res['n_pins'] = len(res['pins']); res['n_failures'] = len(res['failures'])
with open(OUT, 'x') as f:
    json.dump(res, f, indent=1, default=str)
print(json.dumps({'records': res['records'], 'n_pins': res['n_pins'], 'n_failures': res['n_failures'],
                  'failures': res['failures'], 'given_vs_bytes': res['given_vs_bytes'],
                  'pin_graph_self_pins': res['pin_graph_self_pins'], 'pin_graph_cycles': res['pin_graph_cycles'],
                  'unpinned_publication_files': [x['file'] for x in res['publication_files'] if not x['pinned_by_any_record']]},
                 indent=1))
by_rec = {}
for pn in res['pins']:
    by_rec.setdefault(pn['record'].split('.')[0].split('[')[0], []).append(pn['ok'])
print('per-record pin results:', json.dumps({k: [sum(v), len(v)] for k, v in by_rec.items()}))
