# Claude3 (c3v011, root 0667 A123; Claude4 0154): render README_SEAL_ASSEMBLY_C3_c3v011.md and SELECTED_SEAL_PRESTAGE_C3SA_c3v011.json into OUTDIR
# (exclusive create). Every sha, line number and dry-run verdict is read from bytes at render time (helper c3v019 read_nofollow). Publication is a
# byte copy of these renders into seal_assembly_c3 by exclusive create. usage: python3 -I -B THIS OUTDIR
import hashlib, json, os, re, sys, time, types
OUT = sys.argv[1]
X = '/Users/bgm/Research/UNT_EXCHANGE'; A = X + '/claude_artifacts'; C3 = A + '/seal_assembly_c3'; W2 = C3 + '/c3v010_prestage'; W3 = C3 + '/c3v011_prestage'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
HP, HS = C3 + '/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
def P(path, want=None):
    b = H.read_nofollow(path, 'render'); s = hashlib.sha256(b).hexdigest()
    if want:
        assert s.startswith(want), (path, s, want)
    return {'path': path, 'sha256': s, 'bytes': len(b)}
def J(path):
    return H._selected_strict(H.read_nofollow(path, 'render'))
def s8(e):
    return e['sha256'][:8]
def rel(p):
    return p.replace(C3 + '/', '')
UTC = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
DRY = C3 + '/dry_run_20261019T064733Z'; DRY0 = C3 + '/dry_run_20261019T060546Z'; TAG = '20261019T065046Z'
T = {'script': P(C3 + '/ROOT_SEAL_STEPS_c3v027.sh', '239a51c34439b9510155762db8ba02709f1a478b3601de371799ec78591df02f'), 'helper': P(HP, HS),
     'runner': P(C3 + '/tools/run_pinned_c3sa_c3v003.py', '2b040e94'), 'fence': P(C3 + '/tools/fence_c3sa_c3v003.py', '9c62ad49'),
     'slot_json': P(W2 + '/SLOT_VALUES_DRAFT_c3v007.json', '184ff5cbc01eb2683ace5cee8fbee1e82b38d7d6ac152726713501c1ddc83729'),
     'gates_manifest': P(C3 + '/MANIFEST_GATES_ONLY_C3SA_c3v002.json', '46dc53104d518edc9b00e77c0b4995df3e4871999c7264926dad186726ed62ca')}
OLDMAN = P(C3 + '/MANIFEST_GATES_ONLY_DRAFT_C3SA.json', 'e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da')
IN = {'producer_registry_V012': P(A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json', '4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa'),
      'registry_validation_r14_V012': P(A + '/producer_registry_c3/out/VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD.json', 'a7c80f8e'),
      'i4_producer_c3v003_named_by_V012': P(A + '/ri33_c3/i4/write_i4_record_c3v003.py', '707395ba'),
      'gate_record_B0_RO1': P(A + '/ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json', '332452b7a9e63b1bc2cb24a2875f0f281e89c4332571d24825a87dcf52a466ae'),
      'gate_record_B0_N3': P(A + '/ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json', 'dd1dd912580ac478e36246c226aecd5e809b2459effe35a84eac66681a42012b'),
      'manual_disclosures_V006_root': P(C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V006.json', '8dc28480a588f3ef7bd47ebe673767ac79745178a36141cdf50e69e8a040872a'),
      'b7_new_item_list_COMPLETE': P(A + '/seal_b7_inputs_c4/NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json', '68164144'),
      'b7_successor_custody_root': P(CTRL + '/V007_SEAL_ASSEMBLY_INPUTS/custody_run_v002/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json', '9ca16b4f'),
      'compare_r14': P(A + '/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py', 'f3f9ba7e'),
      'compare_r14_selection': P(A + '/v007_compare_c2/r14/SELECTED_R14_CX1V002.json', '6b650ece'),
      'impl_r14': P(A + '/v007_compare_c2/r14/COMPARE_V007_IMPL_R14_CX1V002.md', '2ba6d12e'),
      'text_of_record_r6': P(A + '/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json', 'd28c95f5'),
      'selected_r6': P(A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json', '7200acd9'),
      'seal_tools_v004_selected': P(A + '/v007_final_prereg_c4/seal_tools_v004/SELECTED_SEAL_TOOLS_V004_C4V001.json', '593c59fa')}
ENVF = {'dispositions_P5': P(CTRL + '/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json', '6a3fa535'),
        'key_equivalence_map': P(A + '/seal_b7_inputs_c4/KEY_EQUIVALENCE_MAP_V007.json', '72a21888'),
        'cascade_addendum_P7': P(A + '/cascade_map_r5_addendum_cx3/CASCADE_MAP_R5_ADDENDUM_CX3V001.json', '86c89730')}
SUP_D = [('V001', 'A112', P(C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json', 'b9db6fd1')), ('V002', '0658', P(C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json', 'a0284ece')),
         ('V003', '0661', P(C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V003.json', '990be628')), ('V004', '0662', P(C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V004.json', 'adac5030')),
         ('V005', '0665', P(C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V005.json', 'b1a7b3d5'))]
SUP_R = [('V010', P(A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V010.json', 'b8435877')), ('V011', P(A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V011.json', '512a7171'))]
FC = X + '/FROM_CODEX/'
MSG = {'0659': P(FC + '0659_2026-10-19_custody_record_written_c3v010_finalize.md', '365b1926'), '0664': P(FC + '0664_2026-10-19_claude3_root_answers_P7_P8_P9.md', 'b6fc8a7d'),
       '0665': P(FC + '0665_2026-10-19_disclosures_V006_publish_c3v010.md', 'cb0d28ef'), '0666': P(FC + '0666_2026-10-19_A122_step4_start_blockers_builders.md', 'bd3a1d80'),
       '0667': P(FC + '0667_2026-10-19_A123_c3v011_B0_gates_in_E_SEAL1.md', '92a1aa78'),
       'Claude4_0154': P(X + '/FROM_CLAUDE4/0154_2026-10-19_c3v010-BLOCKING-candidate-B0_RO1-B0_N3-MISSING-in-E-SEAL1-small-fix-and-ACK-0666.md', '3b7cc56f')}
PREV = {'selected_c3v010': P(C3 + '/SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json', '1f62deb4abe3375a02a63a1b803e2aa4c49a4b2ad997d399a618869ef240e161'),
        'readme_c3v010': P(C3 + '/README_SEAL_ASSEMBLY_C3_c3v010.md', 'a43c36a7'), 'hashes_c3v009': P(C3 + '/HASHES_C3SA_c3v009.txt', '479b57b3')}
# pre-publication checks (A123): the manifest checker, its MUST_FAIL suite, and the GATES_ONLY table
CHK = {'checker': P(W2 + '/tools/check_manifest_gates_vs_registry_c3v001.py', 'f92a4e03'), 'checker_result_on_c3v002': P(W3 + '/CHECK_MANIFEST_GATES_VS_V012_c3v002.json'),
       'checker_mustfail_suite': P(W2 + '/tools/mustfail_manifest_gates_check_c3v001.py', '006f3ea9'),
       'checker_mustfail_results': P(W3 + '/mustfail_manifest_gates_20261019T064537Z/MUSTFAIL_MANIFEST_GATES_CHECK_RESULTS_C3SA.json'),
       'gates_only_table_tool': P(W2 + '/tools/gates_only_table_c3v001.py', '72248a64'), 'gates_only_table_json': P(W3 + '/GATES_ONLY_TABLE_c3v027_064733Z.json', '920926b7'),
       'gates_only_table_md': P(W3 + '/GATES_ONLY_TABLE_c3v027_064733Z.md', '4e12b1dc')}
cr = J(CHK['checker_result_on_c3v002']['path']); assert cr['verdict'] == 'PASS' and cr['n_pre_seal'] == 15 and cr['n_produced_after_the_seal'] == 10 and cr['manifest']['sha256'] == T['gates_manifest']['sha256']
cm = J(CHK['checker_mustfail_results']['path']); assert cm['all_ok'] and cm['n'] == cm['n_ok'] == 16
gt = J(CHK['gates_only_table_json']['path']); assert gt['all_ok'] and gt['dry_run'] == DRY and gt['n_pass_A'] == gt['n_pass_B'] == 15 and gt['n_missing_A'] == gt['n_missing_B'] == 10 and gt['gates_changed_vs_base'] == ['B0_N3', 'B0_RO1']
for p_ in 'AB':
    assert P(gt['gates_only'][p_]['path'])['sha256'] == gt['gates_only'][p_]['sha256']
GTMD = H.read_nofollow(CHK['gates_only_table_md']['path'], 'render').decode('utf-8').rstrip('\n')
reg = J(IN['producer_registry_V012']['path']); POST = sorted(g for g, v in reg['gate_records'].items() if v == 'PRODUCED_AFTER_THE_SEAL'); PRE = sorted(g for g, v in reg['gate_records'].items() if isinstance(v, list) and v)
assert len(POST) == 10 and 'I4' in POST and len(PRE) == 15 and {'B0_RO1', 'B0_N3'} <= set(PRE)
for r in gt['rows']:
    assert (r['status_A'], r['status_B']) == (('PASS', 'PASS') if r['gate'] in PRE else ('MISSING', 'MISSING')), r
b0 = J(DRY0 + '/passA/scratch_ctrl/V007_SEAL_ASSEMBLY/E_SEAL1_GATES_ONLY_OUT/GATES_ONLY.json')['gates']   # c3v010's dry run of record: the defect, from bytes
assert b0['B0_RO1']['status'] == b0['B0_N3']['status'] == 'MISSING'
EV = [('r14 + B7 + supersession', 'c3v010_prestage/tools/mustfail_r14_c3v026_c3sa_c3v004.py', 'mustfail_r14_%s/MUSTFAIL_R14_C3V024_RESULTS_C3SA.json' % TAG, '21/21'),
      ('per-site && suite (one MUST_FAIL per site on a copy of the PRODUCTION c3v027; the same fixtures on c3v016)', 'c3v010_prestage/tools/e1_sites_mustfail_c3v007.py', 'e1_sites_c3v027_%s/E1_SITES_RESULTS_C3SA.json' % TAG, '12/12 refuse; defect reproduced on c3v016 9/9; S02 control: no defect'),
      ('disclosures + step 0 + SA-C3-E1', 'c3v010_prestage/tools/mustfail_disclosures_c3sa_c3v007.py', 'mustfail_disclosures_%s/MUSTFAIL_DISCLOSURES_RESULTS_C3SA.json' % TAG, '60/60'),
      ('R-02 + A112 (V001-V005 refused at step 0 or step 11)', 'c3v010_prestage/tools/mustfail_r02_a112_c3sa_c3v006.py', 'mustfail_r02a112_%s/MUSTFAIL_R02_A112_RESULTS_C3SA.json' % TAG, '35/35'),
      ('A + C-02 to C-06 + SELECTED roles + C03-S1 + C-04 (registry V012, r14 loader)', 'c3v010_prestage/tools/mustfail_c0x_c3sa_c3v008.py', 'mustfail_c0x_%s/MUSTFAIL_C0X_RESULTS_C3SA.json' % TAG, '85/85'),
      ('v004 tools', 'c3v010_prestage/tools/mustfail_v004_c3sa_c3v002.py', 'mustfail_v004_%s/MUSTFAIL_V004_RESULTS_C3SA.json' % TAG, '17/17'),
      ('tool-4 imports / RUN FORM / CLI on the real v004 bytes (check c3v003)', 'c3v009_prestage/tools/check_tool4_imports_c3v003.py', 'CHECK_TOOL4_IMPORTS_c3v027.json', 'PASS'),
      ('W7-S1 + RP-S1', 'tools/mustfail_w7_rps1_c3sa_c3v001.py', 'mustfail_w7rps1_%s/MUSTFAIL_W7_RPS1_RESULTS_C3SA.json' % TAG, '41/41'),
      ('B1 + B3', 'tools/mustfail_controls_c3sa_c3v002.py', 'mustfail_regress_%s/MUSTFAIL_RESULTS_C3SA.json' % TAG, 'ALL_OK (8 B1 rows, 17 B3 rows)'),
      ('B2 + N1', 'tools/mustfail_b2_n1_c3sa_c3v003.sh', 'mustfail_b2n1_20261019T065307Z/B2_N1_RESULTS_C3SA.txt', 'ALL_OK'),
      ('tor_table_bytes (script c3v027)', 'tools/test_tor_table_bytes_c3sa_c3v001.sh', 'tor_table_bytes_test_20261019T065308Z/TOR_TABLE_BYTES_RESULTS_C3SA.txt', 'ALL_OK'),
      ('watchdog step2_disk_watch.sh (bd0d9bab)', 'tools/test_step2_disk_watch_c3sa_c3v001.sh', 'watchdog_test_20261019T065308Z/WATCHDOG_TEST_RESULTS_C3SA.txt', 'ALL PASS'),
      ('NEW (A123): the manifest-vs-registry checker on synthetic copies', 'c3v010_prestage/tools/mustfail_manifest_gates_check_c3v001.py', 'c3v011_prestage/mustfail_manifest_gates_20261019T064537Z/MUSTFAIL_MANIFEST_GATES_CHECK_RESULTS_C3SA.json', '16/16')]
EVP = [(n, P(C3 + '/' + t), P(C3 + '/' + r), c) for n, t, r, c in EV]
for n, t, r, c in EVP:
    if r['path'].endswith('.json') and 'CHECK_TOOL4' not in r['path']:
        j = J(r['path'])
        ok = j.get('all_ok', j.get('ALL_OK'))
        if ok is None and 'cases' in j:
            ok = j.get('n_ok') == j.get('n')
        assert ok in (True, None) or ok is True, (r['path'], ok)
DRYF = {}
for p_ in 'AB':
    for f in ('RUN_%s.sh', 'RUN_%s.stdout.txt', 'RUN_%s.stderr.txt', 'ROOT_SEAL_STEPS_DRYRUN_%s.sh', 'SUBSTITUTIONS_%s.json'):
        DRYF['pass%s/%s' % (p_, f % p_)] = P(DRY + '/pass%s/%s' % (p_, f % p_))
    for f in ('SEAL_RECORD_V007.json', 'E_SEAL1_GATES_ONLY_OUT/GATES_ONLY.json', 'logs/STEP_11_DISCLOSURES_VERBATIM.json', 'logs/STEP_08_C03.json', 'logs/STEP_03B_C04.json'):
        DRYF['pass%s/scratch_ctrl/V007_SEAL_ASSEMBLY/%s' % (p_, f)] = P(DRY + '/pass%s/scratch_ctrl/V007_SEAL_ASSEMBLY/%s' % (p_, f))
    so = H.read_nofollow(DRY + '/pass%s/RUN_%s.stdout.txt' % (p_, p_), 'render').decode()
    assert so.count('  PASS  ') == 32 and 'ROOT_SEAL_STEPS: ALL STEPS PASS' in so, p_
DRYF['fixtures/MANIFEST_GATES_ONLY_STANDIN.json'] = P(DRY + '/fixtures/MANIFEST_GATES_ONLY_STANDIN.json')
stn = J(DRYF['fixtures/MANIFEST_GATES_ONLY_STANDIN.json']['path']); mn = J(T['gates_manifest']['path'])
assert list(stn['gates'].items()) == list(mn['gates'].items()) and stn['identity_runs'] == {}
TOOLS = {'dry_run_shim': P(C3 + '/tools/dryrun_tool_shim_c3sa_c3v007.py', 'df19ac11'), 'dry_run_generator': P(W2 + '/tools/make_dry_run_c3sa_c3v014.py', 'b49181e2'),
         'dry_run_setup': P(W2 + '/tools/setup_dry_run_c3sa_c3v020.sh', 'cd406258'), 'root_script_generator': P(W2 + '/tools/make_root_script_c3v027.py', '3388d1c3'),
         'manifest_builder': P(W2 + '/tools/make_manifest_gates_c3v002.py', '78c747ca'), 'slot_xref_successor_documentation_only': P(C3 + '/SLOT_XREF_C3SA_c3v002.json', 'ef77df63'),
         'slot_xref_superseded': P(C3 + '/SLOT_XREF_C3SA.json', '4bd214a8'), 'input_verifier': P(W2 + '/tools/verify_final_inputs_c3v010_c3v002.py', '64c27dab'),
         'input_verification_record': P(W2 + '/VERIFY_FINAL_INPUTS_C3V010_c3v002.json', '211f6369'), 'watchdog_unchanged': P(C3 + '/step2_disk_watch.sh', 'bd0d9bab'),
         'renderer_of_this_file': P(W2 + '/tools/render_publication_c3v011_c3v001.py')}
C5H = '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001'
ACK = 'RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12'
st = H.read_nofollow(T['script']['path'], 'render').decode('utf-8'); lines = st.splitlines()
assert ('REQUIRED_ACK="%s"' % ACK) in st and 'case "$UNT_SEAL_C5H_RUN_DIR" in *KMAX_A2F10_C5H_RUN_V001)' in st
REG14 = H._module_strings(H.pin(IN['compare_r14']['path'], IN['compare_r14']['sha256'], 'compare_r14').decode('utf-8'))['C5H_REGISTERED_RUN_DIRS']; assert C5H in REG14
def L(frag):
    hits = [i + 1 for i, ln in enumerate(lines) if frag in ln and not ln.lstrip().startswith('#')]
    assert len(hits) == 1, (frag, hits); return hits[0]
LN = {k: L(f) for k, f in {'s0_tor': '  H check-tor --text-of-record', 's0_disc': '  H check-disclosures --disclosures', 's2': 'run_h STEP_02_DISPOSITIONS dispositions',
                            's3': 'run_h STEP_03_C05_C06 bound-check', 's3b': 'run_h STEP_03B_C04 slot-registry', 's4a': 'run_h STEP_04A_C02 check-tor', 's8': 'run_h STEP_08_C03 gates-provenance',
                            's8g': 'run_h STEP_08_MANIFEST_CHECK check-manifest', 's10': 'run_h STEP_10_C02 check-tor', 's11': 'run_h STEP_11_DISCLOSURES_VERBATIM check-seal-record-disclosures',
                            'pin': 'MANIFEST_GATES="$C3/MANIFEST_GATES_ONLY_C3SA_c3v002.json"', 'f0': 'step0_preflight() {', 'f2': 'step2_tool1() {', 'f3': 'step3_bind() {',
                            'f3b': 'step3b_c04() {', 'f4a': 'step4a_tool3() {', 'f8': 'step8_gates_only() {', 'f10': 'step10_tool4() {', 'f11': 'step11_seal_record() {'}.items()}
def lv(p_, name):
    return J(DRY + '/pass%s/scratch_ctrl/V007_SEAL_ASSEMBLY/logs/%s.json' % (p_, name)).get('verdict')
def sv(p_, step):
    t = H.read_nofollow(DRY + '/pass%s/RUN_%s.stderr.txt' % (p_, p_), 'render').decode()
    m = re.findall(r'"step": "%s", "utc": "[^"]*", "verdict": "([A-Z]+)"' % step, t); assert len(m) == 1, (p_, step, m); return m[0]
V = {}
for p_ in 'AB':
    V[p_] = {'s0_tor': sv(p_, 'check-tor'), 's0_disc': sv(p_, 'check-disclosures'), 's2': lv(p_, 'STEP_02_DISPOSITIONS'), 's3': lv(p_, 'STEP_03_C05_C06'), 's3b': lv(p_, 'STEP_03B_C04'),
             's4a': lv(p_, 'STEP_04A_C02'), 's8': lv(p_, 'STEP_08_C03'), 's10': lv(p_, 'STEP_10_C02'), 's11': lv(p_, 'STEP_11_DISCLOSURES_VERBATIM')}
    assert set(V[p_].values()) == {'PASS'}, V[p_]
E = ENVF
BLOCK = '\n'.join([
 'export UNT_SEAL_COMPARE_REVIEWED_PATH="%s"' % IN['compare_r14']['path'], 'export UNT_SEAL_COMPARE_REVIEWED_SHA256="%s"' % IN['compare_r14']['sha256'],
 'export UNT_SEAL_COMPARE_SELECTION_PATH="%s"' % IN['compare_r14_selection']['path'], 'export UNT_SEAL_COMPARE_SELECTION_SHA256="%s"' % IN['compare_r14_selection']['sha256'],
 'export UNT_SEAL_DISPOSITIONS_PATH="%s"' % E['dispositions_P5']['path'], 'export UNT_SEAL_DISPOSITIONS_SHA256="%s"' % E['dispositions_P5']['sha256'],
 'export UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH="%s"' % E['key_equivalence_map']['path'], 'export UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256="%s"' % E['key_equivalence_map']['sha256'],
 'export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH="%s"' % E['cascade_addendum_P7']['path'], 'export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256="%s"' % E['cascade_addendum_P7']['sha256'],
 'export UNT_SEAL_C5H_RUN_DIR="%s"' % C5H, 'export UNT_SEAL_MIN_FREE_GIB=300', 'export UNT_SEAL_ROOT_ACK="%s"' % ACK,
 '# optional: export UNT_SEAL_ATTEMPT=1    (1-9; default 1; n > 1: a fresh seal folder and bound names)'])
prev_block = J(PREV['selected_c3v010']['path'])['root_env_inputs']['block']; assert BLOCK == prev_block, 'the exports differ from c3v010'
UNSET = ('unset UNT_SEAL_NEW_ITEM_LIST_PATH UNT_SEAL_NEW_ITEM_LIST_SHA256 UNT_SEAL_SUCCESSOR_CUSTODY_PATH UNT_SEAL_SUCCESSOR_CUSTODY_SHA256 \\\n'
         '      UNT_SEAL_DRIVER_CHECK_RECORD_PATH UNT_SEAL_DRIVER_CHECK_RECORD_SHA256 UNT_SEAL_RULING_EPS_NGC UNT_SEAL_RULING_I1T_NGC')
RUN = 'shasum -a 256 %s    # must print %s\n/bin/bash %s' % (T['script']['path'], T['script']['sha256'], T['script']['path'])
def row(*c):
    return '| ' + ' | '.join(c) + ' |'
def pa(k):
    return '%s / %s' % (V['A'][k], V['B'][k])
R = []
R.append('# README c3v011: the seal assembly tuple with B0_RO1 and B0_N3 in the gates-only manifest (root A123), Claude3\n')
R.append('Written %s (`date -u`), for root 0667 (A123, `%s`), which upholds Claude4 0154 (`%s`).' % (UTC, s8(MSG['0667']), s8(MSG['Claude4_0154'])))
R.append('- **Supersedes** `README_SEAL_ASSEMBLY_C3_c3v010.md` (`%s`) and the selection `SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json` (`%s`).' % (s8(PREV['readme_c3v010']), s8(PREV['selected_c3v010'])))
R.append('- **The selection of record** is `SELECTED_SEAL_PRESTAGE_C3SA_c3v011.json`; the full listing is `HASHES_C3SA_c3v010.txt`.')
R.append("- **The env exports are unchanged** from c3v010. Only the script name and its sha in the run lines change.")
R.append('- Nothing here launched anything, opened the C5H run, or created the real step-2 output root. Step 9 was stubbed in every dry run and never executed.\n')
R.append('## What c3v011 fixes (class (b), and (a); Claude4 0154, root A123)')
R.append('**The defect.**')
R.append('- Step 8 ran the sealed compare `--gates-only` on `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` (`%s`), a registry-V009-era draft with `gates.B0_RO1` and `gates.B0_N3` null.' % s8(OLDMAN))
R.append("- E-SEAL1 therefore recorded both as `MISSING` (`GATE_RECORD_MISSING`), although V012 registers their pre-seal records and prereg r6 `seal_record_requirements[0]` puts the RO1 replay's gate output into E-SEAL1.")
R.append('- c3v010\'s dry run of record shows it in both passes (`dry_run_20261019T060546Z/pass*/…/GATES_ONLY.json`).')
R.append("- **I missed it.** I did not compare GATES_ONLY.json against V012's pre-seal set. C-03 (step 8) checks only the slotted gate records, and B0_RO1 and B0_N3 are not slotted, so nothing caught it.\n")
R.append('**The fix** (to the letter of A123):')
R.append('- `MANIFEST_GATES_ONLY_C3SA_c3v002.json` (`%s`) is e5967bb9 with only two values changed:' % s8(T['gates_manifest']))
R.append('  - `gates.B0_RO1` = `%s` (`%s`);' % (IN['gate_record_B0_RO1']['path'], s8(IN['gate_record_B0_RO1'])))
R.append('  - `gates.B0_N3` = `%s` (`%s`).' % (IN['gate_record_B0_N3']['path'], s8(IN['gate_record_B0_N3'])))
R.append('  - Both use the absolute form the draft uses for every other gate, and both match V012\'s `gate_records` from bytes. The diff is those two lines; the note is unchanged.')
R.append('- `ROOT_SEAL_STEPS_c3v027.sh` changes only the `MANIFEST_GATES` / `MANIFEST_GATES_SHA` pin (L%d), plus the header and history comments. No check was added.' % LN['pin'])
R.append('- **Things keyed to e5967bb9 were moved with it:**')
R.append("  - the dry-run generator: c3v014's S10 now matches the target's own manifest line;")
R.append("  - the dry-run setup: c3v020 derives the gates-only stand-in from the target's manifest pin, and the generator checks it gate for gate (only `identity_runs` is emptied);")
R.append('  - a documentation-only successor, `SLOT_XREF_C3SA_c3v002.json` (`%s`). The script and helper never read SLOT_XREF.\n' % s8(TOOLS['slot_xref_successor_documentation_only']))
R.append('## E-SEAL1 gates-only, gate by gate, from the bytes of dry run `064733Z`')
R.append('The two GATES_ONLY.json files: pass A `%s`, pass B `%s`.\n' % (gt['gates_only']['A']['sha256'][:8], gt['gates_only']['B']['sha256'][:8]))
R.append(GTMD)
R.append('\n**Result.**')
R.append('- **15 PASS:** every pre-seal gate V012 registers, each with its registered record sha.')
R.append('- **10 MISSING:** exactly the PRODUCED_AFTER_THE_SEAL gates (%s), each with only `GATE_RECORD_MISSING:<gate>`.' % ', '.join(POST))
R.append('- **Against c3v010\'s dry run, only B0_N3 and B0_RO1 changed**, MISSING to PASS, in both passes.')
R.append('- The table tool `c3v010_prestage/tools/gates_only_table_c3v001.py` (`%s`) writes `c3v011_prestage/GATES_ONLY_TABLE_c3v027_064733Z.json` (`%s`) and `.md` (`%s`).\n' % (s8(CHK['gates_only_table_tool']), s8(CHK['gates_only_table_json']), s8(CHK['gates_only_table_md'])))
R.append('## Pre-publication check (A123: a stand-alone check, not a script step)')
R.append('`c3v010_prestage/tools/check_manifest_gates_vs_registry_c3v001.py` (`%s`) reads, from bytes:' % s8(CHK['checker']))
R.append("- every gate V012 registers with record shas must be named in the manifest by a path whose bytes hash to one of those shas;")
R.append('- every PRODUCED_AFTER_THE_SEAL gate must be null;')
R.append('- the gate key sets must be equal.\n')
R.append('**Results:**')
R.append('- **On manifest c3v002: PASS**, with 15 pre-seal gates and 10 PRODUCED_AFTER_THE_SEAL gates (`c3v011_prestage/CHECK_MANIFEST_GATES_VS_V012_c3v002.json` `%s`).' % s8(CHK['checker_result_on_c3v002']))
R.append('- **Its MUST_FAILs, on synthetic copies: 16/16** (`%s`). Among them:' % s8(CHK['checker_mustfail_results']))
R.append('  - the superseded draft e5967bb9, refused for both B0_RO1 and B0_N3;')
R.append('  - B0_RO1 alone null, and B0_N3 alone null;')
R.append('  - another pre-seal gate null, and I4 named by a path;')
R.append('  - a wrong record, a missing or extra key, an empty registry slot, a non-path, a wrong sha, a symlink and an unknown form.\n')
R.append('## The tuple')
R.append(row('role', 'file', 'sha256'))
R.append(row('---', '---', '---'))
R.append(row('script', '`ROOT_SEAL_STEPS_c3v027.sh` (%d bytes)' % T['script']['bytes'], T['script']['sha256']))
R.append(row('**step-8 gates-only manifest (new)**', '`MANIFEST_GATES_ONLY_C3SA_c3v002.json`', T['gates_manifest']['sha256']))
R.append(row('helper (unchanged)', '`tools/seal_steps_c3sa_c3v019.py`', T['helper']['sha256']))
R.append(row('runner / fence (unchanged)', '`tools/run_pinned_c3sa_c3v003.py` / `tools/fence_c3sa_c3v003.py`', '%s… / %s…' % (s8(T['runner']), s8(T['fence']))))
R.append(row('slot draft (unchanged)', '`c3v010_prestage/SLOT_VALUES_DRAFT_c3v007.json`', T['slot_json']['sha256']))
R.append('\nThe watchdog `step2_disk_watch.sh` (`%s…`) is unchanged and stays outside the hash chain.\n' % s8(TOOLS['watchdog_unchanged']))
R.append('## Pinned inputs (unchanged from c3v010)')
R.append(row('input', 'sha256'))
R.append(row('---', '---'))
for k in ('producer_registry_V012', 'manual_disclosures_V006_root', 'b7_new_item_list_COMPLETE', 'b7_successor_custody_root', 'compare_r14', 'compare_r14_selection', 'impl_r14', 'text_of_record_r6', 'selected_r6', 'seal_tools_v004_selected'):
    R.append(row('`%s`' % IN[k]['path'].replace(A + '/', '').replace(CTRL, '$CTRL'), IN[k]['sha256']))
R.append('\nV012 is validated on r14 (`%s`). V006 passes `check-disclosures`; its content is not cross-checked against the A-entries here.\n' % s8(IN['registry_validation_r14_V012']))
R.append('**Superseded and refused**')
R.append('- **Disclosures** %s.' % '; '.join('%s `%s`' % (v, s8(e)) for v, w, e in SUP_D))
R.append("  - Step 0 refuses each one, naming V006 as the file of record.")
R.append('- **Registries** %s.' % '; '.join('%s `%s`' % (v, s8(e)) for v, e in SUP_R))
R.append('  - Neither is pinned, and step 0 refuses a draft that is not on V012.')
R.append('- **Gates-only manifest** e5967bb9: no longer pinned. The pre-publication checker refuses it (MG-1, MG-1b).')
R.append('- **Compares:** r13 and older rounds, and `SELECTED_R14_CX1V001`, are refused in step 0.\n')
R.append("## Root's invocation: the env block (unchanged from c3v010; 0664 A121, 0659, 0665)")
R.append('```bash\n' + BLOCK + '\n```\n')
R.append('**Do NOT set any of these.** Step 0 refuses each one if it is set at all, even to an empty value: `UNT_SEAL_NEW_ITEM_LIST_PATH` / `_SHA256`, `UNT_SEAL_SUCCESSOR_CUSTODY_PATH` / `_SHA256`, `UNT_SEAL_DRIVER_CHECK_RECORD_PATH` / `_SHA256`, `UNT_SEAL_RULING_EPS_NGC` and `UNT_SEAL_RULING_I1T_NGC`. There is no disclosures, registry or manifest input; all three are pinned constants.\n')
R.append('Clear them, check the script and run it (the script name and sha are the only change):\n')
R.append('```bash\n' + UNSET + '\n' + RUN + '\n```\n')
R.append("**P8.** `UNT_SEAL_C5H_RUN_DIR` is root's External1 spelling. It is exactly one of the %d entries in r14's `C5H_REGISTERED_RUN_DIRS`, checked from bytes at render time. Step 0 checks only its suffix, and step 9 compares it as a string.\n" % len(REG14))
R.append('Start the watchdog at the launch: `nohup /bin/bash %s --log /ABS/PATH/STEP2_DISK_WATCH_V007.log > /dev/null 2>&1 &` (A105.3; a convenience, not part of the seal; root chooses the log path).\n' % TOOLS['watchdog_unchanged']['path'])
R.append('## C-02 to C-08 (R-05), read from the c3v027 bytes and from dry run `064733Z`')
R.append(row('item', 'c3v027', 'step : line', 'dry run A / B'))
R.append(row('---', '---', '---', '---'))
R.append(row('C-02', 'checked', 'step 0 : L%d (`check-tor`); step 4a : L%d; step 10 : L%d' % (LN['s0_tor'], LN['s4a'], LN['s10']), '%s; %s; %s' % (pa('s0_tor'), pa('s4a'), pa('s10'))))
R.append(row('C-03', 'checked', '**step 8 : L%d** (`gates-provenance`; slotted gate records only)' % LN['s8'], pa('s8')))
R.append(row('C-04', 'checked', 'step 3b : L%d (`slot-registry`: r14 loader, registry V012)' % LN['s3b'], pa('s3b')))
R.append(row('C-05 / C-06', 'checked', 'step 3 : L%d (`bound-check`)' % LN['s3'], pa('s3')))
R.append(row('C-07', 'not by script', 'D-05, enforced by seal tools v004 (step 2 : L%d checks the dispositions object)' % LN['s2'], pa('s2')))
R.append(row('C-08', 'not by script', "root's manual check in V006's `c08_table`; step 0 : L%d and step 11 : L%d check only the file's form and that the record carries it verbatim" % (LN['s0_disc'], LN['s11']), '%s; %s' % (pa('s0_disc'), pa('s11'))))
R.append("\nThis agrees with V006's row `A106_2_SRR13_CHECK_SPLIT`.")
R.append('- The step functions start at: step 0 L%d, step 2 L%d, step 3 L%d, step 3b L%d, step 4a L%d, step 8 L%d, step 10 L%d, step 11 L%d.' % (LN['f0'], LN['f2'], LN['f3'], LN['f3b'], LN['f4a'], LN['f8'], LN['f10'], LN['f11']))
R.append('- Step 8\'s manifest check is at L%d.\n' % LN['s8g'])
R.append('## Dry run of record: `dry_run_20261019T064733Z` (setup c3v020 `%s`, generator c3v014 `%s`)' % (s8(TOOLS['dry_run_setup']), s8(TOOLS['dry_run_generator'])))
R.append('- **Both passes: ALL STEPS PASS**, 32 PASS lines each.')
R.append('  - Step 11 R-02 passes on V006 in both passes.')
R.append('  - `fence_refused` is 0, and the scratch output root is empty.')
R.append("- **The RUN files carry root's answered inputs** (P5, P7, P8 as a string, P9, P10).")
R.append('- **The gates-only stand-in** (S10, `%s`) is manifest c3v002 with only `identity_runs` emptied, so the dry run evaluates exactly the seal\'s gate records.' % s8(DRYF['fixtures/MANIFEST_GATES_ONLY_STANDIN.json']))
R.append('- Only the published scratch substitutions were applied: S01 to S06, S09 to S18, S15, S16/S16b, and S23 in pass B.\n')
R.append('## Controls (helper c3v019 / script c3v027 / dry run 064733Z; run tag %s)' % TAG)
R.append(row('suite', 'tool (sha)', 'result file (sha)', 'result'))
R.append(row('---', '---', '---', '---'))
for n, t, r, c in EVP:
    R.append(row(n, '`%s` (`%s`)' % (rel(t['path']), s8(t)), '`%s` (`%s`)' % (rel(r['path']), s8(r)), '**%s**' % c))
R.append('\n## NOTEs (A115: none is blocking)')
R.append("- **The manifest's note is stale.** It still reads \"registry V009 … null = not built (B0_N3, B0_RO1, I4: fail closed)\", because A123 allows only the two gate values to change. Its gates are what step 8 uses, and they are correct.")
R.append('- **C-03 checks only slotted gate records**, so the script would still not catch a pre-seal gate left null in a future manifest. Per A123 that guard is the pre-publication checker above, not a script step.')
R.append('- **Carried from c3v010:**')
R.append('  - registry supersession is by pin, not by a list;')
R.append('  - P8 is a /Volumes spelling, used as a string only;')
R.append("  - the r14 suite's result file kept its c3v003 name.\n")
R.append('## Kept, not selected (nothing deleted)')
R.append('- `ROOT_SEAL_STEPS_c3v026.sh` `b43cc38b` (SELECTED c3v010, superseded); c3v021 to c3v025 as listed in README c3v010.')
R.append('- `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` `%s`; `SLOT_XREF_C3SA.json` `%s`.' % (s8(OLDMAN), s8(TOOLS['slot_xref_superseded'])))
R.append("- c3v010's dry run `dry_run_20261019T060546Z` (it shows the defect) and the earlier ones.\n")
R.append('## PENDING')
R.append('- **Nothing in the script.** Root exports the block above at the run.')
R.append('- Per 0667, Claude4 does the c3v011 delta (A115 scope). "On two zeros, root runs the seal."')
README = '\n'.join(R) + '\n'
os.mkdir(OUT)
with open(OUT + '/README_SEAL_ASSEMBLY_C3_c3v011.md', 'x') as f:
    f.write(README)
RD = {'path': C3 + '/README_SEAL_ASSEMBLY_C3_c3v011.md', 'sha256': hashlib.sha256(README.encode()).hexdigest(), 'bytes': len(README.encode())}
SEL = {'schema': 'C3SA_SELECTED_SEAL_PRESTAGE_V011', 'utc': UTC,
       'author': 'Claude3 seal-assembly builder (c3v011 on root 0667 A123 92a1aa78, after Claude4 0154 3b7cc56f)',
       'supersedes': [{'path': PREV['selected_c3v010']['path'], 'sha256': PREV['selected_c3v010']['sha256'],
                       'why': 'its gates-only manifest e5967bb9 had gates.B0_RO1 and gates.B0_N3 null, so E-SEAL1 recorded both MISSING although V012 registers their pre-seal records (class (b) and (a); Claude4 0154; root A123)'}],
       'status': 'c3v011: script c3v027 = c3v026 with only the MANIFEST_GATES pin moved to MANIFEST_GATES_ONLY_C3SA_c3v002 (46dc5310: the draft with only gates.B0_RO1 and gates.B0_N3 set). Dry run 064733Z: both passes ALL STEPS PASS; E-SEAL1 gates-only 15 PASS (every V012 pre-seal gate) and 10 MISSING (exactly the PRODUCED_AFTER_THE_SEAL gates, I4 among them). Every suite passes. The env exports are unchanged. No launch; no C5H access; the real step-2 output root was never created; step 9 was never executed.',
       'selected_tuple': T, 'pinned_inputs': IN,
       'superseded_and_refused': {'disclosures': [dict(e, version=v, superseded_at=w) for v, w, e in SUP_D], 'registries': [dict(e, version=v) for v, e in SUP_R],
                                  'gates_manifest': dict(OLDMAN, why='gates.B0_RO1 and gates.B0_N3 null (Claude4 0154; A123); not pinned; the pre-publication checker refuses it (MG-1, MG-1b)'),
                                  'how': 'disclosures: DISCLOSURES_SUPERSEDED_SHAS, refused in step 0 (the refusal names V006); registries: not pinned, REGISTRY_SHA = V012 from bytes, and step 0 refuses a draft whose producer_registry is not REGISTRY; the old gates-only manifest: not pinned (MANIFEST_GATES_SHA = c3v002); compares r13 and older and SELECTED_R14_CX1V001 refused in step 0'},
       'root_env_inputs': {'files': E, 'block': BLOCK, 'block_unchanged_from_c3v010': True,
                           'do_not_set': ['UNT_SEAL_NEW_ITEM_LIST_PATH', 'UNT_SEAL_NEW_ITEM_LIST_SHA256', 'UNT_SEAL_SUCCESSOR_CUSTODY_PATH', 'UNT_SEAL_SUCCESSOR_CUSTODY_SHA256',
                                          'UNT_SEAL_DRIVER_CHECK_RECORD_PATH', 'UNT_SEAL_DRIVER_CHECK_RECORD_SHA256', 'UNT_SEAL_RULING_EPS_NGC', 'UNT_SEAL_RULING_I1T_NGC'],
                           'unset_line': UNSET, 'run': RUN, 'p8_in_r14_C5H_REGISTERED_RUN_DIRS': {'exact_string_member': True, 'entries': len(REG14)},
                           'sources': {'P2': 'compare r14 + SELECTED_R14_CX1V002 (A114/A116)', 'P5': 'root dispositions 6a3fa535 (0659; 0665 table)', 'P6': 'key map 72a21888 (RI-30; 0665 table)',
                                       'P7': 'CASCADE_MAP_R5_ADDENDUM_CX3V001 86c89730 (0664 A121)', 'P8': 'the /Volumes/External1 spelling (0664 A121)', 'P9': 'the ack string (0664 A121)', 'P10': '300 GiB (0659)'}},
       'e_seal1_gates_only_dry_run': {'table_rows': gt['rows'], 'gates_only_files': gt['gates_only'], 'pass_A': {'PASS': gt['n_pass_A'], 'MISSING': gt['n_missing_A']}, 'pass_B': {'PASS': gt['n_pass_B'], 'MISSING': gt['n_missing_B']},
                                      'pre_seal_gates_V012': PRE, 'produced_after_the_seal_V012': POST, 'changed_vs_c3v010_dry_run': gt['gates_changed_vs_base'], 'table_json': CHK['gates_only_table_json'], 'table_md': CHK['gates_only_table_md'], 'tool': CHK['gates_only_table_tool']},
       'pre_publication_checks_A123': {'checker': CHK['checker'], 'result_on_manifest_c3v002': dict(CHK['checker_result_on_c3v002'], verdict='PASS', n_pre_seal=15, n_produced_after_the_seal=10),
                                       'mustfail_suite': CHK['checker_mustfail_suite'], 'mustfail_results': dict(CHK['checker_mustfail_results'], result='16/16')},
       'root_messages_read': MSG,
       'c02_c08_lines_c3v027': {k: LN[k] for k in LN}, 'c02_c08_dry_run_verdicts': V,
       'dry_run_of_record': {'dir': DRY, 'files': DRYF, 'result': 'passes A and B ALL STEPS PASS (32 PASS lines each); STEP_11 R-02 PASS on V006; fence_refused 0; the S10 stand-in = manifest c3v002 with identity_runs emptied'},
       'evidence': {'readme': RD, 'suites': [{'suite': n, 'tool': t, 'result_file': r, 'result': c} for n, t, r, c in EVP]},
       'dry_run_only_and_build_tools_not_seal_tools': TOOLS,
       'findings_A115': {'manifest_note_stale': 'NOTE: the c3v002 note still says registry V009 and null = not built (B0_N3, B0_RO1, I4); A123 allows only the two gate values to change',
                         'c03_slotted_only': 'NOTE: C-03 checks only slotted gate records; the guard against a null pre-seal gate is the pre-publication checker (A123), not a script step',
                         'c3v010_lapse': 'the defect was visible in the c3v010 dry run of record (060546Z GATES_ONLY.json); Claude3 had not compared it with the V012 pre-seal set',
                         'carried': ['registry supersession by pin', 'P8 a string only', 'r14 result file name']},
       'previous_publication': PREV,
       'pending': {'script': 'none', 'root': 'export the env block at the run', 'reviews': '0667: Claude4 c3v011 delta (A115 scope); on two zeros root runs the seal'},
       'hashes_file': C3 + '/HASHES_C3SA_c3v010.txt (written after this file; it lists this file sha)'}
SJ = json.dumps(SEL, indent=1) + '\n'
with open(OUT + '/SELECTED_SEAL_PRESTAGE_C3SA_c3v011.json', 'x') as f:
    f.write(SJ)
print(json.dumps({'readme': RD, 'selected_sha256': hashlib.sha256(SJ.encode()).hexdigest(), 'selected_bytes': len(SJ.encode()), 'utc': UTC, 'lines': LN}, indent=1))
