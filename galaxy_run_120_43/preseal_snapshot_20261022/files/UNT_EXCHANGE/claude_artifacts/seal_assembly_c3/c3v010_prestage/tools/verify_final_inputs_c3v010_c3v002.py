# Claude3 (c3v010 FINAL, root 0665 cb0d28ef; c3v002: producers.I4 is a list of {path, sha256}): verify every c3v010 input from bytes through the pinned helper c3v019 (no-follow, read once).
# Structural checks only (the lead cross-checks the disclosures' content against the A-entries). usage: python3 -I -B THIS OUT_JSON
import hashlib, json, subprocess, sys, types
OUT = sys.argv[1]
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'; W2 = C3 + '/c3v010_prestage'; X = '/Users/bgm/Research/UNT_EXCHANGE'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
HP, HS = C3 + '/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
R = {'helper': HS, 'pins': {}, 'checks': {}}
def fb(p, want, label):
    b = H.pin(p, want, label); R['pins'][label] = {'path': p, 'sha256': want, 'bytes': len(b)}; return b
def diff(a, b, path='$'):
    if type(a) is not type(b):
        yield path; return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                yield path + '.' + k
            else:
                yield from diff(a[k], b[k], path + '.' + k)
    elif isinstance(a, list):
        if all(isinstance(x, dict) and 'id' in x for x in a + b):
            ia, ib = [x['id'] for x in a], [x['id'] for x in b]
            if ia != ib:
                yield path + '[ids: %s -> %s]' % (ia, ib)
            ma, mb = {x['id']: x for x in a}, {x['id']: x for x in b}
            for k in ia:
                if k in mb:
                    yield from diff(ma[k], mb[k], path + '[id=%s]' % k)
        elif len(a) != len(b):
            yield path + '[len %d -> %d]' % (len(a), len(b))
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                yield from diff(x, y, path + '[%d]' % i)
    elif a != b:
        yield path
# root messages
for n, f, s in [('0663', '0663_2026-10-19_claude3_c3v003_include_H4.md', '8b05189918e9051f85082378f9444a43583139a9530541144579a82abe99d3ac'),
                ('0664', '0664_2026-10-19_claude3_root_answers_P7_P8_P9.md', 'b6fc8a7d00081006d8113e43b7711c3eb1b19f47d8fc2160d313fd2b36cf88cc'),
                ('0665', '0665_2026-10-19_disclosures_V006_publish_c3v010.md', 'cb0d28efc9bc0410a7a2f03071fad8c5ac21c96b4e8204ac6bee78538ccde8cd')]:
    fb(X + '/FROM_CODEX/' + f, s, 'root_' + n)
# registry V012 against V011
V11P = A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V011.json'; V12P = A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json'
r11 = H._selected_strict(fb(V11P, '512a7171b952ca97668e8646b106608679ed963faaceba9604dbc3750a7e45f8', 'registry_v011'))
r12 = H._selected_strict(fb(V12P, '4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa', 'registry_v012'))
dr = list(diff(r11, r12)); R['checks']['registry_v011_to_v012_diff_paths'] = dr
assert all(p.startswith('$.producers.I4') or p == '$.note' for p in dr) and dr, dr
assert set(r11) == set(r12) and set(r11['producers']) == set(r12['producers'])
R['checks']['registry_v011_I4'] = r11['producers']['I4']; R['checks']['registry_v012_I4'] = r12['producers']['I4']
R['checks']['registry_v012_note'] = r12['note']
i4 = r12['producers']['I4']   # a list of {path, sha256} entries (one: the producer script)
assert isinstance(i4, list) and len(i4) == 1 and isinstance(i4[0], dict) and set(i4[0]) == {'path', 'sha256'}, i4
i4p, i4s = i4[0]['path'], i4[0]['sha256']
assert isinstance(i4p, str) and isinstance(i4s, str) and i4s.startswith('707395ba') and i4p.endswith('write_i4_record_c3v003.py'), i4
fb(i4p, i4s, 'i4_producer_c3v003')
# validation record (the lead gives the prefix a7c80f8e)
VALP = A + '/producer_registry_c3/out/VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD.json'
vb = H.read_nofollow(VALP, 'validate_r14_v012'); vs = hashlib.sha256(vb).hexdigest(); assert vs.startswith('a7c80f8e'), vs
R['pins']['validate_r14_v012'] = {'path': VALP, 'sha256': vs, 'bytes': len(vb)}
vo = H._selected_strict(vb); vt = vb.decode()
R['checks']['validate_r14_v012_top_keys'] = sorted(vo)
R['checks']['validate_r14_v012_names_v012_sha'] = '4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa' in vt
R['checks']['validate_r14_v012_summary'] = {k: vo[k] for k in vo if k in ('verdict', 'overall', 'summary', 'n_pass', 'n_fail', 'n_checks', 'passed', 'failed', 'counts', 'result', 'status')}
# disclosures V006 against V005
D5P = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V005.json'; D6P = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V006.json'
d5 = H._selected_strict(fb(D5P, 'b1a7b3d5791772ff50c56c9aab277e5112d0ad463ada055067042ac62fbcafd4', 'disclosures_v005'))
d6b = fb(D6P, '8dc28480a588f3ef7bd47ebe673767ac79745178a36141cdf50e69e8a040872a', 'disclosures_v006'); assert len(d6b) == 11262, len(d6b)
d6 = H._selected_strict(d6b)
dd = list(diff(d5, d6)); R['checks']['disclosures_v005_to_v006_diff_paths'] = dd
assert dd and all(p.startswith('$.root_disclosures[id=A114_A117') for p in dd), dd
assert set(d5) == set(d6) and d5['schema'] == d6['schema'] and d5['e_r6_1_text'] == d6['e_r6_1_text'] and d5['c08_table'] == d6['c08_table'] and d5['c08_confirmation'] == d6['c08_confirmation']
R['checks']['disclosures_v006_row_ids'] = [x['id'] for x in d6['root_disclosures']]
ck = subprocess.run([PY, '-I', '-B', HP, 'check-disclosures', '--disclosures', D6P, '--disclosures-sha', '8dc28480a588f3ef7bd47ebe673767ac79745178a36141cdf50e69e8a040872a',
                     '--r6-selected', A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json', '--r6-selected-sha', '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0',
                     '--r6-schema', 'UNT_V007_SELECTED_PREREG_C4V001'], capture_output=True, text=True, cwd='/', env={'PATH': '/usr/bin:/bin', 'LANG': 'en_US.UTF-8'})
R['checks']['check_disclosures_v006'] = {'rc': ck.returncode, 'stdout_tail': ck.stdout[-400:], 'stderr_tail': ck.stderr[-300:]}; assert ck.returncode == 0
# unchanged inputs
cu = H._selected_strict(fb(CTRL + '/V007_SEAL_ASSEMBLY_INPUTS/custody_run_v002/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json', '9ca16b4fd07fd470359cb604526e38807ecf50093cf59ad7895441601535f67d', 'b7_successor_custody'))
assert cu.get('verdict') == 'PASS' and cu.get('stages_total') == 24
fb(A + '/seal_b7_inputs_c4/KEY_EQUIVALENCE_MAP_V007.json', '72a21888eda617638df38ddd64a0e7981bfb6842a9f7f17b8c1a7d4b93e50ec4', 'key_equivalence_map')
fb(A + '/seal_b7_inputs_c4/NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json', '68164144b2f9bf56626be65663566e8c51afba65382e3b6789f53eb144252cd2', 'b7_new_item_complete')
fb(A + '/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py', 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7', 'compare_r14')
fb(A + '/v007_compare_c2/r14/SELECTED_R14_CX1V002.json', '6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a', 'compare_r14_selection')
dp = H._selected_strict(fb(CTRL + '/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json', '6a3fa5353e575fbfe617aa497abd4752e8a2c8676d19f6c4c16a69dfeac0c9fe', 'p5_dispositions'))
assert dp.get('entries') == [] and dp.get('frozen_addendum_sha256') == 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1'
fb(A + '/cascade_map_r5_addendum_cx3/CASCADE_MAP_R5_ADDENDUM_CX3V001.json', '86c897304ec5a0971c3ad1552a60cfad90fc3ac809d68fdacee2be1b942caf9e', 'cascade_addendum_cx3v001')
# derivation sources
fb(W2 + '/SLOT_VALUES_DRAFT_c3v006.json', 'f542e394467873cbb3901f0a08fe880489250db4c15fb5ea8b696557f59d8fec', 'slot_draft_c3v006')
fb(C3 + '/ROOT_SEAL_STEPS_c3v025.sh', '22746e2182cbf948cc234c61d12a812473b864607b0a6f45f3e21ab961fd24a0', 'script_c3v025')
R['verdict'] = 'ALL_VERIFIED'
t = json.dumps(R, indent=1, sort_keys=True) + '\n'
with open(OUT, 'x') as f:
    f.write(t)
print(t)
