# Claude4 helper: the builder's NEW-item rule (compare_impl must name the reviewed source sha in full) against the real IMPL lineage.
# Uses the CLI base (r13 reviewed source). Writes only new files into that base folder.
import glob, hashlib, json, re, sys
from pathlib import Path
CA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
sys.path.insert(0, str(CA / 'v007_final_prereg_c4/seal_tools_v002/r2'))
import seal_common_c4v002 as C
import build_seal_record_c4v002 as T4
base = Path(sorted(glob.glob(str(Path(__file__).resolve().parent / 'cli_base_*')))[-1])
man = json.loads((base / 'CLI_BASE_MANIFEST.json').read_bytes())
IMPLS = {'r11': CA / 'v007_compare_c2/r11/COMPARE_V007_IMPL_R11.md', 'r12': CA / 'v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md', 'r13': CA / 'v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md'}


class A:
    pass


out = {}
for tag, impl in IMPLS.items():
    txt = impl.read_bytes().decode('utf-8', 'replace')
    ids = sorted(set(re.findall(r'\bNEW-\d{1,3}\b', txt)), key=lambda x: int(x[4:]))
    items = [{'id': i, 'disposition': 'ADOPTED', 'reason': 'synthetic test row', 'must_fail_tests': ['T_X']} for i in (ids or ['NEW-73'])]
    p = base / ('NEW_ITEMS_FROM_%s_IMPL_C4CHK.json' % tag)
    with open(p, 'x', encoding='utf-8') as f:
        f.write(json.dumps({'schema': T4.NEW_ITEMS_SCHEMA, 'compare_impl': {'path': str(impl), 'sha256': C.sha(impl)}, 'items': items}, indent=1) + '\n')
    a = A()
    a.slots, a.prereg, a.text_of_record, a.text_of_record_sha = man['slots'], man['sealed_prereg'], man['tor'], man['tor_sha256']
    a.frozen, a.covered_later = man['frozen'], man['covered_later'].split(',')
    a.reviewed, a.sealed_compare = man['reviewed'], man['sealed_compare']
    a.gates_only_output, a.validity_only_output = man['gates_only'], man['validity_only']
    a.key_equivalence_map, a.new_item_list, a.successor_custody, a.b2_record = man['key_map'], str(p), man['custody'], man['b2']
    r, t = T4.safe_build(a)
    out[tag] = {'impl_sha256': C.sha(impl), 'names_reviewed_r13_sha': man['reviewed_sha256'] in txt, 'declared_new_ids': len(ids), 'first_last': [ids[:1], ids[-1:]],
                'builder_verdict': r['verdict'], 'codes': sorted(set(f['code'] for f in r['failures']))}
print(json.dumps(out, indent=1))
