# Claude4 refute helper (dispatch 0650, refute_p6): verify the builder's HASHES table and the shas reported in its build result
# from bytes; list every file of the builder folder and say which are not covered by the table. Read-only; prints JSON only.
# Run under tools/run_fenced_c4st2.py.
import hashlib, json, os, sys

B = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4'
H = B + '/HASHES_SEAL_B7_INPUTS_C4V001.txt'
REPORTED = {  # copied from the build result as given in the dispatch text (these are claims under test, not trusted values)
    'KEY_EQUIVALENCE_MAP_V007.json': '72a21888eda617638df38ddd64a0e7981bfb6842a9f7f17b8c1a7d4b93e50ec4',
    'NEW_ITEM_DISPOSITIONS_V007.json': '9a9ee6cf5af0a85523a4111d62fd0e26ef0bc032398219580eb9527bea9f28bc',
    'NEW_ITEM_DISPOSITIONS_V007_R14_VARIANT.json': '6bd8fa9574e34245266436af88cc40459e0bcd95d606b1630f71e66f6ce9095a',
    'CUSTODY_SPEC_FOR_ROOT_V001.md': '66c1e5e34c507d889585c08a928e98741881857b83fbb1f5e2217f48e6df21cf',
    'tools/make_custody_record_c4v001.py': '1b097cbaf75d4bc1931218d943c6f247f99291a233ca46c2c0a6933d061ca841',
    'VALIDATION_TOOL4_B7_C4V001.json': 'b629efc4fd0b19816c6f9c23acc9a249dfb0f6c55bdba868f54ead9a087e5c9a',
    'TEST_CUSTODY_CONVERTER_SYNTHETIC_C4V002.json': 'd7995aba12415dc1edfaf785291fb5709bc8986238ad08f49ba959b6219e0884',
    'TEST_CUSTODY_CONVERTER_SYNTHETIC_C4V001.json': 'd31ef1792bc7f02dee3772abb446b0375135fea3fd1dec168f22f159bbe47f8b',
    'fixtures/custody_cli_v002/CUSTODY_CLI_PASS.json': 'd9ad6da8920c8991c53e4ab3e7a0020aaea791d18faa858e545176cd6326121d',
    'README_SEAL_B7_INPUTS_C4V001.md': 'a792e1f1dfca111265e79bcdb1ca09b095dc00ad4392861e94c74c82b18ad793',
    'tools/make_key_map_c4v001.py': '146ed46af65d821ed8322294910356f3a1acd214fc9d5f96b85bae0aa2bcd2ab',
    'tools/make_new_items_c4v001.py': 'c2c1f30ab397d1fc1a021278ee9fe66d920d6df3b05409a4d85ce68143c3b546',
    'tools/validate_b7_with_tool4_c4v001.py': 'd745df0f73179ddf879a937242baf45b74d61809a69de8b05102741e376599b1',
    'tools/test_custody_converter_c4v002.py': '7bc27c4a6e0335e48f313c2ac21940c6d9f201f05a7f64cb0ffae8687c56602c',
    'tools/fence_c4v002.py': 'c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5',
    'tools/run_fenced_c4st2.py': 'fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25',
    'PARTIAL.md': '6a6e9cd87ea520bc578ce343884da258e54562a777663c2cad17410e7cfdac3e',
    'HASHES_SEAL_B7_INPUTS_C4V001.txt': '731ff01a8702fc76508b5df1a1ac2467b95184f0b1d86cdadba1fe0e3a34f061',
}


def sha(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


out = {'hashes_file': H, 'hashes_file_sha256': sha(H)}
rows, bad_rows, seen = [], [], set()
for n, line in enumerate(open(H, 'rb').read().decode('utf-8').split('\n'), 1):
    if not line.strip():
        continue
    h, p = line.split('  ', 1)
    rows.append((h, p))
    if p in seen:
        bad_rows.append({'line': n, 'path': p, 'problem': 'DUPLICATE_PATH'})
    seen.add(p)
    if not os.path.isfile(p) or os.path.islink(p):
        bad_rows.append({'line': n, 'path': p, 'problem': 'NOT_A_REGULAR_FILE'})
        continue
    got = sha(p)
    if got != h:
        bad_rows.append({'line': n, 'path': p, 'problem': 'SHA_MISMATCH', 'table': h, 'bytes': got})
out['table_rows'] = len(rows)
out['table_rows_bad'] = bad_rows
walk = []
for root, dirs, files in os.walk(B):
    dirs.sort()
    for f in sorted(files):
        walk.append(os.path.join(root, f))
out['files_in_folder'] = len(walk)
out['files_not_in_table'] = [p for p in walk if p not in seen and p != H]
out['table_paths_not_in_folder'] = [p for p in seen if p not in walk]
out['symlinks_in_folder'] = [p for p in walk if os.path.islink(p)]
rep = []
for rel, h in REPORTED.items():
    p = os.path.join(B, rel)
    got = sha(p)
    rep.append({'file': rel, 'reported': h, 'bytes': got, 'match': got == h,
                'table_row': next((hh for hh, pp in rows if pp == p), None)})
out['reported_vs_bytes'] = rep
out['reported_all_match'] = all(r['match'] for r in rep)
print(json.dumps(out, indent=1, sort_keys=True))
