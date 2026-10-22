# c3v002: asserts from r14's bytes that root's P8 spelling is one of its C5H_REGISTERED_RUN_DIRS (recorded); the watchdog line gives its absolute path.
# Claude3 (c3v010 FINAL, root 0665 cb0d28ef): render README_SEAL_ASSEMBLY_C3_c3v010.md and SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json into OUTDIR
# (exclusive create). Every sha is read from bytes at render time (helper c3v019 read_nofollow). Publication is a byte copy of these renders into
# seal_assembly_c3 by exclusive create. usage: python3 -I -B THIS OUTDIR
import hashlib, json, os, sys, time, types
OUT = sys.argv[1]
X = '/Users/bgm/Research/UNT_EXCHANGE'; A = X + '/claude_artifacts'; C3 = A + '/seal_assembly_c3'; W2 = C3 + '/c3v010_prestage'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
HP, HS = C3 + '/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
def P(path, want=None):
    b = H.read_nofollow(path, 'render'); s = hashlib.sha256(b).hexdigest()
    if want:
        assert s.startswith(want), (path, s, want)
    return {'path': path, 'sha256': s, 'bytes': len(b)}
def s8(e):
    return e['sha256'][:8]
UTC = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
DRY = C3 + '/dry_run_20261019T060546Z'; DRY1 = C3 + '/dry_run_20261019T060249Z'; TAG = '20261019T060933Z'; TAG2 = '20261019T061125Z'
T = {'script': P(C3 + '/ROOT_SEAL_STEPS_c3v026.sh', 'b43cc38be5f19c473167d8d57211c54d336d09d58fcfd66f5ca8187ad033c464'), 'helper': P(HP, HS),
     'runner': P(C3 + '/tools/run_pinned_c3sa_c3v003.py', '2b040e94'), 'fence': P(C3 + '/tools/fence_c3sa_c3v003.py', '9c62ad49'),
     'slot_json': P(W2 + '/SLOT_VALUES_DRAFT_c3v007.json', '184ff5cbc01eb2683ace5cee8fbee1e82b38d7d6ac152726713501c1ddc83729'),
     'gates_manifest_draft': P(C3 + '/MANIFEST_GATES_ONLY_DRAFT_C3SA.json', 'e5967bb9')}
IN = {'producer_registry_V012': P(A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json', '4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa'),
      'registry_validation_r14_V012': P(A + '/producer_registry_c3/out/VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD.json', 'a7c80f8e'),
      'i4_producer_c3v003_named_by_V012': P(A + '/ri33_c3/i4/write_i4_record_c3v003.py', '707395ba'),
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
MSG = {'0659': P(FC + '0659_2026-10-19_custody_record_written_c3v010_finalize.md', '365b1926'), '0661': P(FC + '0661_2026-10-19_disclosures_V004_pin_in_c3v010.md', '24b4ada5'),
       '0662': P(FC + '0662_2026-10-19_A120_NEW44_erratum_V005_release_c3v010.md', '17e6e258'), '0663': P(FC + '0663_2026-10-19_claude3_c3v003_include_H4.md', '8b051899'),
       '0664': P(FC + '0664_2026-10-19_claude3_root_answers_P7_P8_P9.md', 'b6fc8a7d'), '0665': P(FC + '0665_2026-10-19_disclosures_V006_publish_c3v010.md', 'cb0d28ef')}
EV = [('r14 + B7 + supersession (r13 and CX1V001 refused; PENDING placeholders; draft compare slot; IMPL r14; B7 pins; stale B7 env; V002-V005 and the V010/V011 drafts and REGISTRY refused)', 'c3v010_prestage/tools/mustfail_r14_c3v026_c3sa_c3v004.py', 'mustfail_r14_%s/MUSTFAIL_R14_C3V024_RESULTS_C3SA.json' % TAG, '21/21'),
      ('per-site && suite (one MUST_FAIL per site on a copy of the PRODUCTION c3v026; the same fixtures on c3v016)', 'c3v010_prestage/tools/e1_sites_mustfail_c3v006.py', 'e1_sites_c3v026_%s/E1_SITES_RESULTS_C3SA.json' % TAG, '12/12 refuse; defect reproduced on c3v016 9/9; S02 control: no defect'),
      ('disclosures + step 0 + SA-C3-E1 (target pins V006)', 'c3v010_prestage/tools/mustfail_disclosures_c3sa_c3v007.py', 'mustfail_disclosures_%s/MUSTFAIL_DISCLOSURES_RESULTS_C3SA.json' % TAG, '60/60'),
      ('R-02 + A112 (written SEAL_RECORD; V001-V005 records, pins and tool-4 inputs refused at step 0 or step 11)', 'c3v010_prestage/tools/mustfail_r02_a112_c3sa_c3v005.py', 'mustfail_r02a112_%s/MUSTFAIL_R02_A112_RESULTS_C3SA.json' % TAG, '35/35'),
      ('A + C-02 to C-06 + SELECTED roles + C03-S1 + C-04 (registry V012, r14 loader)', 'c3v010_prestage/tools/mustfail_c0x_c3sa_c3v008.py', 'mustfail_c0x_%s/MUSTFAIL_C0X_RESULTS_C3SA.json' % TAG, '85/85'),
      ('v004 tools', 'c3v010_prestage/tools/mustfail_v004_c3sa_c3v002.py', 'mustfail_v004_%s/MUSTFAIL_V004_RESULTS_C3SA.json' % TAG, '17/17'),
      ('tool-4 imports / RUN FORM / CLI on the real v004 bytes (check c3v003)', 'c3v009_prestage/tools/check_tool4_imports_c3v003.py', 'CHECK_TOOL4_IMPORTS_c3v026.json', 'PASS'),
      ('W7-S1 + RP-S1', 'tools/mustfail_w7_rps1_c3sa_c3v001.py', 'mustfail_w7rps1_%s/MUSTFAIL_W7_RPS1_RESULTS_C3SA.json' % TAG, '41/41'),
      ('B1 + B3', 'tools/mustfail_controls_c3sa_c3v002.py', 'mustfail_regress_%s/MUSTFAIL_RESULTS_C3SA.json' % TAG, 'ALL_OK (8 B1 rows, 17 B3 rows)'),
      ('B2 + N1', 'tools/mustfail_b2_n1_c3sa_c3v003.sh', 'mustfail_b2n1_%s/B2_N1_RESULTS_C3SA.txt' % TAG2, 'ALL_OK'),
      ('tor_table_bytes (script c3v026)', 'tools/test_tor_table_bytes_c3sa_c3v001.sh', 'tor_table_bytes_test_%s/TOR_TABLE_BYTES_RESULTS_C3SA.txt' % TAG2, 'ALL_OK'),
      ('watchdog step2_disk_watch.sh (bd0d9bab)', 'tools/test_step2_disk_watch_c3sa_c3v001.sh', 'watchdog_test_%s/WATCHDOG_TEST_RESULTS_C3SA.txt' % TAG2, 'ALL PASS')]
EVP = [(n, P(C3 + '/' + t), P(C3 + '/' + r), c) for n, t, r, c in EV]
DRYF = {}
for p_ in 'AB':
    for f in ('RUN_%s.sh', 'RUN_%s.stdout.txt', 'RUN_%s.stderr.txt', 'ROOT_SEAL_STEPS_DRYRUN_%s.sh', 'SUBSTITUTIONS_%s.json'):
        DRYF['pass%s/%s' % (p_, f % p_)] = P(DRY + '/pass%s/%s' % (p_, f % p_))
    for f in ('SEAL_RECORD_V007.json', 'logs/STEP_11_DISCLOSURES_VERBATIM.json', 'logs/STEP_03B_C04.json'):
        DRYF['pass%s/scratch_ctrl/V007_SEAL_ASSEMBLY/%s' % (p_, f)] = P(DRY + '/pass%s/scratch_ctrl/V007_SEAL_ASSEMBLY/%s' % (p_, f))
TOOLS = {'dry_run_shim': P(C3 + '/tools/dryrun_tool_shim_c3sa_c3v007.py', 'df19ac11'), 'dry_run_generator': P(W2 + '/tools/make_dry_run_c3sa_c3v013.py', '379afda7'),
         'dry_run_setup_of_record': P(W2 + '/tools/setup_dry_run_c3sa_c3v019.sh', '893de27a'), 'dry_run_setup_first_c3v026_run': P(W2 + '/tools/setup_dry_run_c3sa_c3v018.sh', '8aa0ed10'),
         'root_script_generator': P(W2 + '/tools/make_root_script_c3v026.py', 'ec3b9b2a'), 'input_verifier': P(W2 + '/tools/verify_final_inputs_c3v010_c3v002.py', '64c27dab'),
         'input_verification_record': P(W2 + '/VERIFY_FINAL_INPUTS_C3V010_c3v002.json', '211f6369'), 'watchdog_unchanged': P(C3 + '/step2_disk_watch.sh', 'bd0d9bab'),
         'renderer_of_this_file': P(W2 + '/tools/render_publication_c3v010_c3v002.py')}
KEPT = {'ROOT_SEAL_STEPS_c3v021.sh (pre-stage)': P(W2 + '/ROOT_SEAL_STEPS_c3v021.sh'), 'ROOT_SEAL_STEPS_c3v022.sh (near-final)': P(W2 + '/ROOT_SEAL_STEPS_c3v022.sh', 'b4f71a84'),
        'ROOT_SEAL_STEPS_c3v023.sh (V010/V003; Claude4 0142 stop)': P(C3 + '/ROOT_SEAL_STEPS_c3v023.sh', '50a87b6b'), 'ROOT_SEAL_STEPS_c3v024.sh (V011/V004; B7 hold)': P(C3 + '/ROOT_SEAL_STEPS_c3v024.sh', 'c26d847b'),
        'ROOT_SEAL_STEPS_c3v025.sh (V011/V005; I4 c3v002 hold)': P(C3 + '/ROOT_SEAL_STEPS_c3v025.sh', '22746e21'), 'SLOT_VALUES_DRAFT_c3v004.json': P(W2 + '/SLOT_VALUES_DRAFT_c3v004.json', '723a36d1'),
        'SLOT_VALUES_DRAFT_c3v005.json': P(W2 + '/SLOT_VALUES_DRAFT_c3v005.json', 'd6924860'), 'SLOT_VALUES_DRAFT_c3v006.json': P(W2 + '/SLOT_VALUES_DRAFT_c3v006.json', 'f542e394')}
C5H = '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001'
ACK = 'RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12'
st = open(T['script']['path']).read()
assert ('REQUIRED_ACK="%s"' % ACK) in st and 'case "$UNT_SEAL_C5H_RUN_DIR" in *KMAX_A2F10_C5H_RUN_V001)' in st
REG14 = H._module_strings(H.pin(IN['compare_r14']['path'], IN['compare_r14']['sha256'], 'compare_r14').decode('utf-8'))['C5H_REGISTERED_RUN_DIRS']
assert isinstance(REG14, tuple) and C5H in REG14, REG14
E = ENVF
BLOCK = '\n'.join([
 'export UNT_SEAL_COMPARE_REVIEWED_PATH="%s"' % IN['compare_r14']['path'], 'export UNT_SEAL_COMPARE_REVIEWED_SHA256="%s"' % IN['compare_r14']['sha256'],
 'export UNT_SEAL_COMPARE_SELECTION_PATH="%s"' % IN['compare_r14_selection']['path'], 'export UNT_SEAL_COMPARE_SELECTION_SHA256="%s"' % IN['compare_r14_selection']['sha256'],
 'export UNT_SEAL_DISPOSITIONS_PATH="%s"' % E['dispositions_P5']['path'], 'export UNT_SEAL_DISPOSITIONS_SHA256="%s"' % E['dispositions_P5']['sha256'],
 'export UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH="%s"' % E['key_equivalence_map']['path'], 'export UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256="%s"' % E['key_equivalence_map']['sha256'],
 'export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH="%s"' % E['cascade_addendum_P7']['path'], 'export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256="%s"' % E['cascade_addendum_P7']['sha256'],
 'export UNT_SEAL_C5H_RUN_DIR="%s"' % C5H, 'export UNT_SEAL_MIN_FREE_GIB=300', 'export UNT_SEAL_ROOT_ACK="%s"' % ACK,
 '# optional: export UNT_SEAL_ATTEMPT=1    (1-9; default 1; n > 1: a fresh seal folder and bound names)'])
UNSET = ('unset UNT_SEAL_NEW_ITEM_LIST_PATH UNT_SEAL_NEW_ITEM_LIST_SHA256 UNT_SEAL_SUCCESSOR_CUSTODY_PATH UNT_SEAL_SUCCESSOR_CUSTODY_SHA256 \\\n'
         '      UNT_SEAL_DRIVER_CHECK_RECORD_PATH UNT_SEAL_DRIVER_CHECK_RECORD_SHA256 UNT_SEAL_RULING_EPS_NGC UNT_SEAL_RULING_I1T_NGC')
RUN = 'shasum -a 256 %s    # must print %s\n/bin/bash %s' % (T['script']['path'], T['script']['sha256'], T['script']['path'])
for k in ('compare_r14', 'compare_r14_selection'):
    assert IN[k]['sha256'] in st
C0 = [('C-02', 'checked by c3v026', 'step 0 : L437 (`check-tor`, verdict on stderr); step 4a : L661 (`STEP_04A_C02.json`); step 10 : L727 (`STEP_10_C02.json`)', 'PASS / PASS'),
      ('C-03', 'checked by c3v026', '**step 8 : L693** (`gates-provenance` → `STEP_08_C03.json`)', 'PASS / PASS'),
      ('C-04', 'checked by c3v026', 'step 3b : L630 (`slot-registry` → `STEP_03B_C04.json`: r14 loader, registry V012, A107 excludes EPS_NGC and I1T_NGC)', 'PASS / PASS'),
      ('C-05', 'checked by c3v026', 'step 3 : L606 (`bound-check`, c05 part → `STEP_03_C05_C06.json`)', 'PASS / PASS'),
      ('C-06', 'checked by c3v026', 'step 3 : L606 (`bound-check`, c06 part → `STEP_03_C05_C06.json`)', 'PASS / PASS'),
      ('C-07', 'not checked by script', 'D-05, enforced by seal tools v004 (step 2 : L541 checks the dispositions object, which is related but is not C-07)', 'n/a (step 2 PASS / PASS)'),
      ('C-08', 'not checked by script', "root's manual check in V006's `c08_table` (19 rows) and `c08_confirmation`; step 0 : L449 (`check-disclosures`, form only) and step 11 : L748 (R-02, verbatim) do not check its content", 'n/a (steps 0 and 11 PASS / PASS)')]
lines = st.splitlines()
for ln, frag in ((437, 'H check-tor'), (449, 'H check-disclosures'), (541, 'STEP_02_DISPOSITIONS dispositions'), (606, 'STEP_03_C05_C06 bound-check'), (630, 'STEP_03B_C04 slot-registry'),
                 (661, 'STEP_04A_C02 check-tor'), (693, 'STEP_08_C03 gates-provenance'), (727, 'STEP_10_C02 check-tor'), (748, 'STEP_11_DISCLOSURES_VERBATIM check-seal-record-disclosures')):
    assert frag in lines[ln - 1], (ln, frag)
def row(*c):
    return '| ' + ' | '.join(c) + ' |'
R = []
R.append('# README c3v010: the seal assembly tuple for root\'s seal run (registry V012, disclosures V006, root\'s A121 answers), Claude3\n')
R.append('Written %s (`date -u`), for root 0665 (`%s`), which releases c3v010. Root\'s answers on P7, P8 and P9 are 0664 (A121, `%s`).' % (UTC, s8(MSG['0665']), s8(MSG['0664'])))
R.append('- **Supersedes** `README_SEAL_ASSEMBLY_C3_c3v009.md` (`ac575ce8`) and the selection `SELECTED_SEAL_PRESTAGE_C3SA_c3v009.json` (`9e10eae1`).')
R.append('- **The selection of record** is `SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json`; the full listing is `HASHES_C3SA_c3v009.txt`.')
R.append('- **No pin is PENDING.** Every pinned value was read from bytes. Step 0 checks each of them again, then checks the run inputs root supplies (the block below).')
R.append('- Nothing here launched anything, opened the C5H run, or created the real step-2 output root. Step 9 was stubbed in every dry run and never executed.\n')
R.append('## The tuple')
R.append(row('role', 'file', 'sha256'))
R.append(row('---', '---', '---'))
R.append(row('script', '`ROOT_SEAL_STEPS_c3v026.sh` (%d bytes)' % T['script']['bytes'], T['script']['sha256']))
R.append(row('helper (unchanged since c3v009)', '`tools/seal_steps_c3sa_c3v019.py`', T['helper']['sha256']))
R.append(row('runner / fence (unchanged)', '`tools/run_pinned_c3sa_c3v003.py` / `tools/fence_c3sa_c3v003.py`', '%s… / %s…' % (s8(T['runner']), s8(T['fence']))))
R.append(row('slot draft', '`c3v010_prestage/SLOT_VALUES_DRAFT_c3v007.json` (= c3v006 with only `producer_registry` moved to V012)', T['slot_json']['sha256']))
R.append(row('step-8 manifest draft (unchanged)', '`MANIFEST_GATES_ONLY_DRAFT_C3SA.json`', s8(T['gates_manifest_draft']) + '…'))
R.append('\nThe watchdog `step2_disk_watch.sh` (`%s…`) is unchanged and stays outside the hash chain.\n' % s8(TOOLS['watchdog_unchanged']))
R.append('## Pinned inputs (constants in the script; verified from bytes by `c3v010_prestage/tools/verify_final_inputs_c3v010_c3v002.py`, record `VERIFY_FINAL_INPUTS_C3V010_c3v002.json` `%s`)' % s8(TOOLS['input_verification_record']))
R.append(row('input', 'file', 'sha256', 'what was checked'))
R.append(row('---', '---', '---', '---'))
R.append(row('producer registry **V012**', '`producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json`', IN['producer_registry_V012']['sha256'], 'V011 `512a7171` with only `producers.I4` (now `ri33_c3/i4/write_i4_record_c3v003.py` `%s`) and `note` changed. Validated on r14: `VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD.json` `%s` (15 pre-seal records, all PASS; every registered sha matches its file; guard refusals 0)' % (s8(IN['i4_producer_c3v003_named_by_V012']), s8(IN['registry_validation_r14_V012']))))
R.append(row("root's disclosures **V006**", '`root_inputs/SEAL_MANUAL_DISCLOSURES_V006.json` (%d bytes)' % IN['manual_disclosures_V006_root']['bytes'], IN['manual_disclosures_V006_root']['sha256'], 'V005 with only the row `A114_A117_I4_AFTER_SEAL` changed (its `source` and `text`); keys, schema, `e_r6_1_text` and the C-08 fields unchanged; helper `check-disclosures` PASS. Its content is not cross-checked against the A-entries here'))
R.append(row('B7 NEW-item list', '`seal_b7_inputs_c4/NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json`', IN['b7_new_item_list_COMPLETE']['sha256'], 'unchanged (V006 row `E_A118_1` governs the A118 sentence it quotes)'))
R.append(row("B7 successor custody (root)", '`$CTRL/V007_SEAL_ASSEMBLY_INPUTS/custody_run_v002/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json`', IN['b7_successor_custody_root']['sha256'], 'verdict PASS, 24 stages'))
R.append(row('compare r14 / its selection / IMPL r14', '`v007_compare_c2/r14/…`', '%s… / %s… / %s…' % (s8(IN['compare_r14']), s8(IN['compare_r14_selection']), s8(IN['impl_r14'])), 'step 0 requires exactly these (A114/A116)'))
R.append(row('text of record r6 / SELECTED_R6 / seal tools v004 SELECTED', '`v007_final_prereg_c4/…`', '%s… / %s… / %s…' % (s8(IN['text_of_record_r6']), s8(IN['selected_r6']), s8(IN['seal_tools_v004_selected'])), 'unchanged since c3v009'))
R.append('\n**Superseded and refused**')
R.append('- **Disclosures** %s.' % '; '.join('%s `%s` (%s)' % (v, s8(e), why) for v, why, e in SUP_D))
R.append('  - All five are in `DISCLOSURES_SUPERSEDED_SHAS`, and step 0 refuses each one.')
R.append('  - The refusal now reads `REFUSE: the disclosures file is a superseded version (root 0665: V006 is the file of record)`.')
R.append('  - MUST_FAIL coverage: r14 suite N-10 to N-10d; R-02/A112 suite A112-1 to A112-1e (step 0), A112-2 to A112-2d (step 11) and R02-6 to R02-6e and R02-15 to R02-15c (helper).')
R.append('- **Registries** %s.' % '; '.join('%s `%s`' % (v, s8(e)) for v, e in SUP_R))
R.append('  - Neither is pinned; `REGISTRY_SHA` is V012, verified from bytes.')
R.append("  - Step 0 refuses a slot draft whose `producer_registry` is not `REGISTRY`.")
R.append('  - MUST_FAIL coverage: N-3c (V011 as REGISTRY, with draft c3v007), N-11b (draft c3v005, on V010) and N-11c (draft c3v006, on V011).')
R.append('- **Compares:** r13 `f5adfd11` and older rounds, and `SELECTED_R14_CX1V001` `dc74949d`, are refused in step 0 (N-1, N-1b, N-2).\n')
R.append("## Root's invocation: the filled env block")
R.append('Values come from bytes and from root:')
R.append('- **P2:** compare r14 and its selection (A114/A116).')
R.append("- **P5:** root's dispositions file (0659; 0665's table).")
R.append("- **P6:** the key map (RI-30; 0665's table).")
R.append('- **P7:** CX3V001, from 0664 (A121).')
R.append('- **P8:** the External1 spelling, from 0664 (A121).')
R.append('- **P9:** the ack string, confirmed exactly in 0664 (A121).')
R.append('- **P10:** 300 GiB, from 0659.\n')
R.append('```bash\n' + BLOCK + '\n```\n')
R.append('**Do NOT set any of these.** Step 0 refuses each one if it is set at all, even to an empty value:')
R.append('- `UNT_SEAL_NEW_ITEM_LIST_PATH` / `_SHA256` and `UNT_SEAL_SUCCESSOR_CUSTODY_PATH` / `_SHA256`: the B7 NEW-item list and the custody record are pinned constants.')
R.append('- `UNT_SEAL_DRIVER_CHECK_RECORD_PATH` / `_SHA256`, `UNT_SEAL_RULING_EPS_NGC` and `UNT_SEAL_RULING_I1T_NGC`: A111 ruled P3 and P4, and the slot draft fixes them.')
R.append('- There is no disclosures or registry input either: both are pinned constants.\n')
R.append('A safe way to clear them, then check the script and run it:\n')
R.append('```bash\n' + UNSET + '\n' + RUN + '\n```\n')
R.append('**What step 0 checks on these inputs:**')
R.append('- `UNT_SEAL_ROOT_ACK` must equal `REQUIRED_ACK` exactly.')
R.append('- `UNT_SEAL_MIN_FREE_GIB` must be digits only.')
R.append('- The compare and selection shas must be r14 `f3f9ba7e` and `6b650ece`.')
R.append('- The dispositions JSON must lie in `$CTRL/V007_SEAL_ASSEMBLY_INPUTS/`.')
R.append('- `UNT_SEAL_C5H_RUN_DIR` must end in `KMAX_A2F10_C5H_RUN_V001`.')
R.append("  - Step 9 uses it only as a string: `make-c5h-manifest` and `check-manifest` compare it with the sealed compare's `C5H_REGISTERED_RUN_DIRS`, which contains root's External1 spelling exactly (one of its %d entries, checked from r14's bytes at render time)." % len(REG14))
R.append('  - Neither the script nor the helper passes it through `path_policy`.')
R.append('\nStart the watchdog at the launch: `nohup /bin/bash %s --log /ABS/PATH/STEP2_DISK_WATCH_V007.log > /dev/null 2>&1 &` (A105.3; a convenience, not part of the seal; root chooses the log path).\n' % TOOLS['watchdog_unchanged']['path'])
R.append('## C-02 to C-08 (R-05; r6 `seal_record_requirements[13]`), read from the c3v026 bytes and from dry run `060546Z`')
R.append(row('item', 'c3v026', 'step : line (helper subcommand → log)', 'dry run A / B'))
R.append(row('---', '---', '---', '---'))
for c in C0:
    R.append(row(*c))
R.append("\nThis agrees, item by item, with V006's row `A106_2_SRR13_CHECK_SPLIT`:")
R.append('> C-02, C-03, C-04, C-05 and C-06 were checked by the seal script; C-07 is D-05, enforced by seal tools v004; C-08 was checked by hand by root.\n')
R.append('Each step function starts at: step 0 L404, step 2 L537, step 3 L577, step 3b L626, step 4a L655, step 8 L679, step 10 L716, step 11 L740.\n')
R.append('## Dry run of record: `dry_run_20261019T060546Z` (setup `c3v010_prestage/tools/setup_dry_run_c3sa_c3v019.sh` `%s`, generator c3v013 `%s`)' % (s8(TOOLS['dry_run_setup_of_record']), s8(TOOLS['dry_run_generator'])))
R.append('- **Both passes: ALL STEPS PASS**, 32 PASS lines each.')
R.append('  - Step 11 R-02 passes on V006 in both passes.')
R.append('  - `fence_refused` is 0 at steps 2a, 3b and 8.')
R.append('  - The pycache prefix stayed empty, and the scratch output root is a real, empty directory.')
R.append('- **No stand-in.**')
R.append("  - The RUN files carry root's answered inputs, labelled as such: P5 `6a3fa535` (copied byte-identically into scratch, since S09 moves that folder), r14 and its selection, the key map, P7, the P8 External1 string, the P9 ack and the P10 floor 300.")
R.append('  - The dry-run scripts pin V012, V006, draft c3v007, COMPLETE and the custody record.')
R.append('- **Only the published scratch substitutions** were applied: S01 to S06, S09 to S14, S17, S18, the step-9 stub S15 and the D-10 allowance S16/S16b; pass B adds S23 (no dispositions to the tools).')
R.append("- The first c3v026 dry run, `dry_run_20261019T060249Z` (setup c3v018), also passed both passes. It still carried the old /Users C5H string and STAND-IN labels; it is kept and superseded.\n")
R.append('## Controls (helper c3v019 / script c3v026 / dry run 060546Z; run tag %s)' % TAG)
R.append(row('suite', 'tool (sha)', 'result file (sha)', 'result'))
R.append(row('---', '---', '---', '---'))
for n, t, r, c in EVP:
    R.append(row(n, '`%s` (`%s`)' % (t['path'].replace(C3 + '/', ''), s8(t)), '`%s` (`%s`)' % (r['path'].replace(C3 + '/', ''), s8(r)), '**%s**' % c))
R.append('\nThe r14 suite\'s result file kept its c3v003 name; its `schema` field reads `C3SA_MUSTFAIL_R14_C3V026_V004`.\n')
R.append('## What changed since SELECTED c3v009 (script c3v020)')
R.append('**The scripts in between were never published.**')
R.append('- **c3v021, pre-stage (A114/A116):**')
R.append('  - The reviewed compare is r14, as `SELECTED_R14_CX1V002` stores it.')
R.append('  - IMPL r14 is pinned, and r13 is refused as superseded.')
R.append("  - C-04 loads r14's `load_producer_registry`.")
R.append('  - The draft compare slot is checked against the reviewed compare.')
R.append('- **c3v022, near-final (0658):**')
R.append('  - Disclosures V003 and registry V010.')
R.append('  - The B7 NEW-item list and the custody record became pinned constants, and their env inputs are refused.')
R.append('- **c3v023 (V010/V003):** stopped by Claude4 0142, an A115 (a) defect in the I4 producer c3v001.')
R.append('- **c3v024 (0659, 0661 A119):** V011, V004 and the custody record `9ca16b4f`; held over the B7 NEW-44 class (b) issue.')
R.append('- **c3v025 (0662 A120):** V005; held over the I4 producer c3v002 class (a) defect.')
R.append('- **c3v026 (0665):**')
R.append('  - V012, V006 and draft c3v007.')
R.append('  - The step-0 refusal text names V006.')
R.append("  - Root's A121 answers are recorded in the comments, and the run summary names V006.")
R.append('  - Exactly 7 non-comment lines differ from c3v025: the 4 pins, the refusal text and 2 summary strings.')
R.append('- **Unchanged since c3v009:** helper c3v019, runner, fence, gates manifest, shim and watchdog.\n')
R.append('## NOTEs (A115: none is blocking)')
R.append('- **Registry supersession is enforced by pin, not by a list.**')
R.append('  - Unlike the disclosures, there is no `REGISTRY_SUPERSEDED_SHAS` list.')
R.append('  - V010 and V011 cannot enter: `REGISTRY_SHA` is checked from bytes, and the draft is cross-checked against it (N-3c, N-11b, N-11c).')
R.append("  - A copy of the script pinning V011 together with a V011 draft would pass step 0, but it would not be the selected script's bytes.")
R.append('- **P8 is a /Volumes spelling.**')
R.append('  - The tooling uses it as a string only.')
R.append('  - Step 9 is root\'s real run, and it hands that string to the sealed compare r14 through the manifest. No dry run executed step 9, so how the compare itself handles the spelling was not exercised here.')
R.append('- **First input verifier.** `verify_final_inputs_c3v010_c3v001.py` stopped before writing anything because it misread the shape of `producers.I4` (a list). c3v002 is the record.\n')
R.append('## Kept, not selected (nothing deleted)')
for k, e in KEPT.items():
    R.append('- `%s` `%s`' % (k, s8(e)))
R.append('- Dry runs: `c3v010_prestage/dry_run_20261019T035955Z`, `…040145Z` and `…042057Z`; `dry_run_20261019T044217Z` (c3v024); `dry_run_20261019T060249Z` (c3v026, setup c3v018).')
R.append('- The smoke folder `c3v010_prestage/smoke_gen_20261019T043857Z` (SMOKE ONLY).\n')
R.append('## PENDING')
R.append('- **Nothing in the script.** Root exports the block above at the run.')
R.append("- 0665 asks Claude4 for the c3v003 delta, then the c3v010 delta (A115 scope). \"On two zeros, root runs the seal.\"")
README = '\n'.join(R) + '\n'
assert "'" not in BLOCK
os.mkdir(OUT)
with open(OUT + '/README_SEAL_ASSEMBLY_C3_c3v010.md', 'x') as f:
    f.write(README)
RD = {'path': C3 + '/README_SEAL_ASSEMBLY_C3_c3v010.md', 'sha256': hashlib.sha256(README.encode()).hexdigest(), 'bytes': len(README.encode())}
SEL = {'schema': 'C3SA_SELECTED_SEAL_PRESTAGE_V010', 'utc': UTC,
       'author': 'Claude3 seal-assembly builder (c3v010 on root 0665 cb0d28ef; root answers 0664 A121)',
       'supersedes': [{'path': C3 + '/SELECTED_SEAL_PRESTAGE_C3SA_c3v009.json', 'sha256': P(C3 + '/SELECTED_SEAL_PRESTAGE_C3SA_c3v009.json', '9e10eae1')['sha256'],
                       'why': 'c3v009 pinned compare r13 (now superseded by r14, A114/A116), disclosures V002 (superseded) and no B7 pins; root inputs P2 and P5-P10 were open'}],
       'status': 'c3v010 FINAL: script c3v026 with every pin filled from bytes (registry V012, disclosures V006, slot draft c3v007, B7 NEW-item COMPLETE, custody record); root supplies only the env block (filled with the A121 answers). Both dry runs ALL STEPS PASS with no stand-in; every suite passes. No launch; no C5H access; the real step-2 output root was never created; step 9 was never executed.',
       'selected_tuple': T, 'pinned_inputs': IN,
       'superseded_and_refused': {'disclosures': [dict(e, version=v, superseded_at=w) for v, w, e in SUP_D], 'registries': [dict(e, version=v) for v, e in SUP_R],
                                  'how': 'disclosures: DISCLOSURES_SUPERSEDED_SHAS, refused in step 0 (the refusal names V006); registries: not pinned, REGISTRY_SHA = V012 from bytes, and step 0 refuses a draft whose producer_registry is not REGISTRY; compares r13 and older and SELECTED_R14_CX1V001 refused in step 0'},
       'root_env_inputs': {'files': E, 'block': BLOCK, 'do_not_set': ['UNT_SEAL_NEW_ITEM_LIST_PATH', 'UNT_SEAL_NEW_ITEM_LIST_SHA256', 'UNT_SEAL_SUCCESSOR_CUSTODY_PATH', 'UNT_SEAL_SUCCESSOR_CUSTODY_SHA256',
                                                                     'UNT_SEAL_DRIVER_CHECK_RECORD_PATH', 'UNT_SEAL_DRIVER_CHECK_RECORD_SHA256', 'UNT_SEAL_RULING_EPS_NGC', 'UNT_SEAL_RULING_I1T_NGC'],
                           'run': RUN, 'p8_in_r14_C5H_REGISTERED_RUN_DIRS': {'exact_string_member': True, 'entries': len(REG14), 'checked_from': IN['compare_r14']}, 'sources': {'P2': 'compare r14 + SELECTED_R14_CX1V002 (A114/A116)', 'P5': 'root dispositions 6a3fa535 (0659; 0665 table)', 'P6': 'key map 72a21888 (RI-30; 0665 table)',
                                                   'P7': 'CASCADE_MAP_R5_ADDENDUM_CX3V001 86c89730 (0664 A121)', 'P8': 'the /Volumes/External1 spelling (0664 A121)', 'P9': 'the ack string (0664 A121, confirmed exactly)', 'P10': '300 GiB (0659)'}},
       'root_messages_read': MSG,
       'c02_c08_split': {'in': 'README_SEAL_ASSEMBLY_C3_c3v010.md, section C-02 to C-08', 'lines_c3v026': {c[0]: c[2] for c in C0}, 'dry_run': {c[0]: c[3] for c in C0},
                         'agrees_with_V006_row_A106_2_SRR13_CHECK_SPLIT': True},
       'dry_run_of_record': {'dir': DRY, 'files': DRYF, 'result': 'passes A and B ALL STEPS PASS (32 PASS lines each); STEP_11 R-02 PASS on V006; fence_refused 0; no stand-in',
                             'superseded_first_run': {'dir': DRY1, 'note': 'setup c3v018: passed both passes, but carried the old /Users C5H string and STAND-IN labels'}},
       'evidence': {'readme': RD, 'suites': [{'suite': n, 'tool': t, 'result_file': r, 'result': c} for n, t, r, c in EVP]},
       'dry_run_only_and_build_tools_not_seal_tools': TOOLS,
       'findings_A115': {'registry_supersession_by_pin': 'NOTE: no REGISTRY_SUPERSEDED_SHAS list; V010/V011 refused through the pin and the draft cross-check (N-3c, N-11b, N-11c)',
                         'p8_volumes_spelling': 'NOTE: a string only in the script and the helper; the sealed compare reads it at step 9, which no dry run executes',
                         'r14_result_file_name': 'NOTE: the r14 suite result file kept its c3v003 name; its schema field is C3SA_MUSTFAIL_R14_C3V026_V004',
                         'verifier_c3v001': 'NOTE: stopped before writing (producers.I4 is a list); c3v002 is the record'},
       'left_behind_kept': KEPT,
       'pending': {'script': 'none', 'root': 'export the env block at the run', 'reviews': '0665: Claude4 c3v003 delta, then the c3v010 delta (A115 scope); on two zeros root runs the seal'},
       'hashes_file': C3 + '/HASHES_C3SA_c3v009.txt (written after this file; it lists this file sha)'}
SJ = json.dumps(SEL, indent=1) + '\n'
with open(OUT + '/SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json', 'x') as f:
    f.write(SJ)
print(json.dumps({'readme': RD, 'selected_sha256': hashlib.sha256(SJ.encode()).hexdigest(), 'selected_bytes': len(SJ.encode()), 'utc': UTC}, indent=1))
