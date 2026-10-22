# Claude3 (c3v010 FINAL, root 0665 cb0d28ef; 0663, 0664 A121): derive ROOT_SEAL_STEPS_c3v026.sh from ROOT_SEAL_STEPS_c3v025.sh (22746e21, never
# published) by an explicit replacement set (each old string exactly once), and write the slot draft c3v007 (= c3v006 with ONLY producer_registry
# -> V012). Every value is read from bytes through the pinned helper c3v019: registry V012 (V011 with only producers.I4 and the note changed),
# its r14 validation record, disclosures V006 (check-disclosures must PASS) and V005 (now superseded). Also: the step-0 superseded-disclosures
# refusal names V006; root's A121 answers (P7, P8, P9) are recorded in the comments; the run summary names V006. No logic changes.
# usage: python3 -I -B make_root_script_c3v026.py OUT_SCRIPT OUT_DRAFT
import hashlib, json, re, subprocess, sys, types
OUT, OUTD = sys.argv[1:3]
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'; W2 = C3 + '/c3v010_prestage'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
SRC, SRC_SHA = C3 + '/ROOT_SEAL_STEPS_c3v025.sh', '22746e2182cbf948cc234c61d12a812473b864607b0a6f45f3e21ab961fd24a0'
HP, HS = C3 + '/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
src = open(SRC, 'rb').read(); assert hashlib.sha256(src).hexdigest() == SRC_SHA; s = src.decode('utf-8')
def fb(p, want, label):
    b = H.pin(p, want, label); return b, hashlib.sha256(b).hexdigest()
V11P = A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V011.json'; v11b, V11S = fb(V11P, '512a7171b952ca97668e8646b106608679ed963faaceba9604dbc3750a7e45f8', 'registry_v011')
V12P = A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json'; v12b, V12S = fb(V12P, '4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa', 'registry_v012')
r11, r12 = H._selected_strict(v11b), H._selected_strict(v12b)
assert {k: v for k, v in r11.items() if k not in ('producers', 'note')} == {k: v for k, v in r12.items() if k not in ('producers', 'note')}
assert {k: v for k, v in r11['producers'].items() if k != 'I4'} == {k: v for k, v in r12['producers'].items() if k != 'I4'}
I4 = r12['producers']['I4']; assert isinstance(I4, list) and len(I4) == 1 and set(I4[0]) == {'path', 'sha256'}
I4P, I4S = I4[0]['path'], I4[0]['sha256']; assert I4P.endswith('/ri33_c3/i4/write_i4_record_c3v003.py'); fb(I4P, I4S, 'i4_producer_c3v003'); assert I4S.startswith('707395ba')
VALP = A + '/producer_registry_c3/out/VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD.json'; vb, VALS = fb(VALP, 'a7c80f8e87456577a1f111b4b82488305bff0af9d5f7868080749d3a8858a155', 'validate_r14_v012')
vo = H._selected_strict(vb); assert vo['registry'] == {'path': V12P, 'sha256': V12S} and vo['all_registered_preseal_pass'] is True and vo['all_registered_shas_match_files'] is True
assert len(vo['preseal_records']) == 15 and vo['guard_refused'] == 0 and vo['empty_slots'] == []
D5P = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V005.json'; d5b, D5S = fb(D5P, 'b1a7b3d5791772ff50c56c9aab277e5112d0ad463ada055067042ac62fbcafd4', 'disclosures_v005')
D6P = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V006.json'; d6b, D6S = fb(D6P, '8dc28480a588f3ef7bd47ebe673767ac79745178a36141cdf50e69e8a040872a', 'disclosures_v006'); assert len(d6b) == 11262
ck = subprocess.run([PY, '-I', '-B', HP, 'check-disclosures', '--disclosures', D6P, '--disclosures-sha', D6S, '--r6-selected', A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json',
                     '--r6-selected-sha', '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0', '--r6-schema', 'UNT_V007_SELECTED_PREREG_C4V001'], capture_output=True, text=True, cwd='/', env={'PATH': '/usr/bin:/bin', 'LANG': 'en_US.UTF-8'})
assert ck.returncode == 0, ck.stderr[-300:]
row6 = [x for x in H._selected_strict(d6b)['root_disclosures'] if x['id'] == 'A114_A117_I4_AFTER_SEAL'][0]['text']
assert 'write_i4_record_c3v003.py' in row6 and I4S in row6 and 'PRODUCER_REGISTRY_C3V012.json' in row6 and V12S in row6   # the comment below says so
DR6, DR6S = W2 + '/SLOT_VALUES_DRAFT_c3v006.json', 'f542e394467873cbb3901f0a08fe880489250db4c15fb5ea8b696557f59d8fec'
t = open(DR6, 'rb').read(); assert hashlib.sha256(t).hexdigest() == DR6S; t = t.decode(); d = json.loads(t)
blk = '"producer_registry": {\n  "path": %s,\n  "sha256": %s\n }' % (json.dumps(d['producer_registry']['path']), json.dumps(d['producer_registry']['sha256']))
assert t.count(blk) == 1 and d['producer_registry'] == {'path': V11P, 'sha256': V11S}
t2 = t.replace(blk, '"producer_registry": {\n  "path": %s,\n  "sha256": %s\n }' % (json.dumps(V12P), json.dumps(V12S)))
d2 = json.loads(t2); assert {k: v for k, v in d2.items() if k != 'producer_registry'} == {k: v for k, v in d.items() if k != 'producer_registry'} and d2['producer_registry'] == {'path': V12P, 'sha256': V12S}
with open(OUTD, 'x') as f:
    f.write(t2)
DR7S = hashlib.sha256(t2.encode()).hexdigest()
SUP = ' '.join(['b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6', 'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3',
                '990be628e810bc38afd6657ac151cfb908c761ce266c232de71baf8bd6d300eb', 'adac5030770ec78114145fe80ae1b21e454d43b788037a632c01af076b25abfe'])
def cell(old, txt):
    new = ('| ' + txt).ljust(len(old) - 1) + '|'; assert len(new) == len(old), (old, new); return new
R = [
 ('header', '# ROOT_SEAL_STEPS_c3v025.sh:', '# ROOT_SEAL_STEPS_c3v026.sh:'),
 ('history', '# c3v025 supersedes ROOT_SEAL_STEPS_c3v024.sh (c26d847b, never published) for the c3v010 selection: root 0662 (A120, 17e6e258). DISCLOSURES is',
  '''# c3v026 supersedes ROOT_SEAL_STEPS_c3v025.sh (22746e21, never published) for the c3v010 selection: root 0665 (cb0d28ef), after the I4 producer
#   c3v002 (2a315da2) was found to give honest pairs a false FAIL (A115 (a): RO1 firing identically on both sides; a substring run-root match;
#   Claude3 0142/0143, root 0663). From bytes (make_root_script_c3v026.py):
#   - REGISTRY = V012 (%s; V011 with only producers.I4 moved to write_i4_record_c3v003.py %s, and its note; validated on r14,
#     VALIDATE_R14_C3V012 %s: 15 pre-seal records, all PASS); the slot draft c3v007 moves only its producer_registry slot to V012.
#     V011 and V010 are not pinned; a slot draft still on either refuses in step 0.
#   - DISCLOSURES = root V006 (%s; V005 with only the A114_A117 row changed, naming c3v003 and V012); V005 (%s) joins V004, V003,
#     V002 and V001 as superseded and refused in step 0, whose refusal text now names V006 as the file of record.
#   - root's answers on P7, P8 and P9 (0664, A121) are recorded in the P table and the input list; they stay root's env inputs (the
#     filled block is in README_SEAL_ASSEMBLY_C3_c3v010.md). The run summary names V006. Nothing else changes.
# c3v025 superseded ROOT_SEAL_STEPS_c3v024.sh (c26d847b, never published) for the c3v010 selection: root 0662 (A120, 17e6e258). DISCLOSURES is''' % (V12S[:8], I4S[:8], VALS[:8], D6S[:8], D5S[:8])),
 ('P7 cell', '| env (owner TBD)        |', cell('| env (owner TBD)        |', 'env (A121: CX3V001)')),
 ('P8 cell', '| env (root)             |', cell('| env (root)             |', 'env (A121: External1)')),
 ('P14 rows', '''# |P14| producer registry (A114/A119)| DONE (c3v024): V011 512a7171 (V010 with only producers.I4 -> c3v002 2a315da2), validated   | done (c3v024)          |
# |   |                              | on r14 (VALIDATE_R14_C3V011 54eaf584); slot draft c3v006 pins the same file             |                        |''',
  '''# |P14| producer registry (A114/A119)| DONE (c3v026): V012 %s (0665; V011 with only producers.I4 -> c3v003 %s), validated | done (c3v026)          |
# |   |                              | on r14 (VALIDATE_R14_C3V012 %s); slot draft c3v007 pins the same file             |                        |''' % (V12S[:8], I4S[:8], VALS[:8])),
 ('P15 row', '''# |P15| root disclosures (A116-A120) | DONE (c3v025): V005 b1a7b3d5 (0662); V001, V002, V003 and V004 superseded and refused  | done (c3v025)          |''',
  '''# |P15| root disclosures (A116-A121) | DONE (c3v026): V006 %s (0665); V001 to V005 superseded and refused               | done (c3v026)          |''' % D6S[:8]),
 ('input cascade', '#   UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH / _SHA256\n',
  '#   UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH / _SHA256   P7, root 0664 (A121): CASCADE_MAP_R5_ADDENDUM_CX3V001.json 86c89730 (Codex3 0646)\n'),
 ('input c5h', '#   UNT_SEAL_C5H_RUN_DIR                  the C5H run directory spelling for step 9 (string only until step 9)\n',
  '#   UNT_SEAL_C5H_RUN_DIR                  the C5H run directory spelling for step 9 (string only until step 9); P8, root 0664 (A121):\n'
  '#                                         the /Volumes/External1 spelling (no symlinked ancestor; $CTRL/runs_ext is itself a link)\n'),
 ('input floor', '#   UNT_SEAL_MIN_FREE_GIB                 integer\n', '#   UNT_SEAL_MIN_FREE_GIB                 integer (P10, root 0659: 300)\n'),
 ('input ack', '#   UNT_SEAL_ROOT_ACK                     exactly: RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12\n',
  '#   UNT_SEAL_ROOT_ACK                     exactly: RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12 (P9, root 0664, A121)\n'),
 ('draft', 'DRAFT="$C3/c3v010_prestage/SLOT_VALUES_DRAFT_c3v006.json";              DRAFT_SHA="%s"   # schema UNT_V007_SEAL_SLOTS_C4V002 (v003); P3, P4 ruled (A111); compare slot r14 (A116); registry V011 (A119)' % DR6S,
  'DRAFT="%s";              DRAFT_SHA="%s"   # schema UNT_V007_SEAL_SLOTS_C4V002 (v003); P3, P4 ruled (A111); compare slot r14 (A116); registry V012 (0665)' % (OUTD.replace(C3, '$C3', 1), DR7S)),
 ('disclosures', '''# A116 (0654) + root 0658 + 0661 (A119) + 0662 (A120): the disclosures file of record is root's V005 (V002 plus the rows E_R6_2,
# A113_ROOT_ITEMS_R6 (its NEW-44 phrase corrected, A120), A114_A117_I4_AFTER_SEAL (naming I4 producer c3v002 2a315da2 and registry V011),
# A118_CUSTODY_FORM and E_A118_1; the C-08 table re-read on r14; the same five keys; e_r6_1_text byte-identical). V001-V004 are superseded.
DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V005.json"; DISCLOSURES_SHA="%s"
DISCLOSURES_SUPERSEDED_SHAS="%s"   # V001 (A112), V002 (0658), V003 (0661), V004 (0662); left in place, never used''' % (D5S, SUP),
  '''# A116 (0654) + root 0658 + 0661 (A119) + 0662 (A120) + 0665: the disclosures file of record is root's V006 (V002 plus the rows E_R6_2,
# A113_ROOT_ITEMS_R6 (its NEW-44 phrase corrected, A120), A114_A117_I4_AFTER_SEAL (naming I4 producer c3v003 %s and registry V012),
# A118_CUSTODY_FORM and E_A118_1; the C-08 table re-read on r14; the same five keys; e_r6_1_text byte-identical). V001-V005 are superseded.
DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V006.json"; DISCLOSURES_SHA="%s"
DISCLOSURES_SUPERSEDED_SHAS="%s %s"   # V001 (A112), V002 (0658), V003 (0661), V004 (0662), V005 (0665); left in place, never used''' % (I4S[:8], D6S, SUP, D5S)),
 ('registry', '''# A114 (0651) + A119 (0661): the producer registry of record is V011 (V010 with only producers.I4 moved to write_i4_record_c3v002.py 2a315da2;
# Claude4 0142; validated on r14 with producers.I4: VALIDATE_R14_C3V011_CASEBLOCK_OF_RECORD 54eaf584); slot draft c3v006 pins it. V010 is superseded.
REGISTRY="$A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V011.json"; REGISTRY_SHA="%s"''' % V11S,
  '''# A114 (0651) + A119 (0661) + 0665: the producer registry of record is V012 (V011 with only producers.I4 moved to write_i4_record_c3v003.py
# %s, and its note; root 0663; validated on r14 with producers.I4: VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD %s); slot draft c3v007
# pins it. V011 and V010 are superseded (not pinned; a slot draft still on either refuses in step 0).
REGISTRY="$A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json"; REGISTRY_SHA="%s"''' % (I4S[:8], VALS[:8], V12S)),
 ('step-0 refusal text', 'echo "REFUSE: the disclosures file is a superseded version (A112: V002 is the file of record)" >&2',
  'echo "REFUSE: the disclosures file is a superseded version (root 0665: V006 is the file of record)" >&2'),
 ('summary C-08', 'disclosures file of record (root V003, A116; pins.manual_disclosures;', 'disclosures file of record (root V006, 0665; pins.manual_disclosures;'),
 ('summary pin label', '(the disclosures file of record, V003 per A116; verbatim', '(the disclosures file of record, V006 per root 0665; verbatim'),
]
out = s
for rid, o, n in R:
    assert out.count(o) == 1, (rid, out.count(o))
    out = out.replace(o, n)
pins = out[out.index('# ============================================================================================================ PINS'):out.index('# ---------------------------------------------------------------------------------------------------- OUTPUTS')]
assert not re.search(r'^[A-Z0-9_]+="PENDING', pins, re.M) and '_SHA="PENDING"' not in pins, 'a PINS value is still PENDING'
assert 'PRODUCER_REGISTRY_C3V011.json"' not in pins and 'SEAL_MANUAL_DISCLOSURES_V005.json"' not in pins and 'SLOT_VALUES_DRAFT_c3v006.json"' not in pins
assert ('DISCLOSURES_SHA="%s"' % D6S) in pins and ('REGISTRY_SHA="%s"' % V12S) in pins and D5S in pins.split('DISCLOSURES_SUPERSEDED_SHAS="', 1)[1].split('"', 1)[0]
progs = re.findall(r'"\$\{PYX\[@\]\}" -c \'(.*?)\'', out, re.S)
for pr in progs:
    compile(pr, 'embedded', 'exec', dont_inherit=True)
summ = out[out.index('summary() {'):out.index('step0_preflight\nstep1_freeze')]
assert "'" not in summ.split("-c '", 1)[1].split("' \"$SUMMARY\"", 1)[0]
# the logic is c3v025's: every non-comment line outside the PINS block is unchanged
def code(x):
    return [ln for ln in x.splitlines() if not ln.lstrip().startswith('#')]
cs, co = code(s), code(out)
changed = [(a, b) for a, b in zip(cs, co) if a != b]
assert len(cs) == len(co) and len(changed) == 7, (len(cs), len(co), len(changed))
with open(OUT, 'x') as f:
    f.write(out)
bn = subprocess.run(['/bin/bash', '-n', OUT], capture_output=True, text=True)
print(json.dumps({'script': {'path': OUT, 'sha256': hashlib.sha256(out.encode()).hexdigest(), 'bytes': len(out.encode())}, 'draft': {'path': OUTD, 'sha256': DR7S},
                  'from': SRC_SHA, 'registry_v012': V12S, 'i4_producer': [I4P, I4S], 'validate_r14_v012': VALS, 'disclosures_v006': D6S, 'disclosures_v005_superseded': D5S,
                  'replacements': len(R), 'non_comment_lines_changed': [b[:160] for a, b in changed], 'embedded_python_programs_compiled': len(progs),
                  'no_pending_pins': True, 'bash_n_ok': bn.returncode == 0}, indent=1))
sys.exit(0 if bn.returncode == 0 else 2)
