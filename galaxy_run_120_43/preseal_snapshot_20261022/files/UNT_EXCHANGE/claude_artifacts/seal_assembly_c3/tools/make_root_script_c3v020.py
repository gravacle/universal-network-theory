# Claude3 (c3v009; FROM_CODEX/0648 ruling A112; SELECTED_SEAL_TOOLS_V004_C4V001 593c59fa): derive ROOT_SEAL_STEPS_c3v020.sh from
# ROOT_SEAL_STEPS_c3v019.sh (f4843a47, SELECTED c3v008) by an explicit replacement set (each old string exactly once). Every value it
# writes is read from bytes here, through the pinned helper c3v019 (pin(): no-follow walk, one read, sha; _selected_strict(): the
# strict SELECTED parser): the v004 SELECTED file's files.* roles (role-qualified; all five tools from seal_tools_v004), the V002
# disclosures file's sha (A112), and the SEAL_RECORD format from tool 4 v004's own source (its SCHEMA constant and its manual_disclosures
# field {pin, content, raw_text}). It supersedes the c3v009 pre-stage generator (c3v009_prestage/tools/make_root_script_c3v020.py
# 62318ef6), which required a plain 'readme' role the v004 file does not have and pinned V001. It writes the script exclusively,
# compiles every embedded python program, runs bash -n, and prints a JSON summary.
# usage: python3 -I -B make_root_script_c3v020.py OUT_SCRIPT
import ast, hashlib, json, os, re, subprocess, sys, types
OUT = sys.argv[1]
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'
SRC, SRC_SHA = C3 + '/ROOT_SEAL_STEPS_c3v019.sh', 'f4843a47dadf4fc98aca287d0f9b982e10a5f90e6f73de1f158123440b686e67'
HP, HS = C3 + '/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
V4, V4S, V4C = A + '/v007_final_prereg_c4/seal_tools_v004/SELECTED_SEAL_TOOLS_V004_C4V001.json', '593c59faf39074b14579f927ae17c5aeda1f7450ee4a9f264f96a1f2c7b195e0', 'UNT_V007_SELECTED_SEAL_TOOLS_C4V001'
V3, V3S = A + '/v007_final_prereg_c4/seal_tools_v003/SELECTED_SEAL_TOOLS_V003_C4V001.json', 'cf7e5b2f1b3daf55c485ada1c869bc7249040a8db8202eb1b1a90bebe1431305'
R6, R6S = A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json', '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'
D2, D2_ROOT_SHA = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json', 'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3'   # A112 / 0648
D1S = 'b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6'                                                                 # V001, superseded
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS, 'HELPER_BYTES'
H = types.ModuleType('c3sa_helper_pinned'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
src = open(SRC, 'rb').read(); assert hashlib.sha256(src).hexdigest() == SRC_SHA, 'C3V019_BYTES'; s = src.decode('utf-8')
sel = H._selected_strict(H.pin(V4, V4S, 'v004_selected'))
assert sel.get('schema') == V4C, sel.get('schema')
F = sel['files']
def role(r):
    e = F[r]
    assert isinstance(e, dict) and set(e) == {'path', 'sha256'} and e['path'].startswith('/') and H.HEX64.fullmatch(e['sha256']), r
    H.pin(e['path'], e['sha256'], r)                      # every role file verifies from bytes now
    return e['path'], e['sha256']
TOOLS = {'T_COMMON': 'seal_common', 'T1': 'tool_1_check_frozen_addendum', 'T2': 'tool_2_check_sealed_compare', 'T3': 'tool_3_check_slot_fill',
         'T4': 'tool_4_build_seal_record', 'T5': 'tool_5_print_driver_build_record'}
tp = {v: role(r) for v, r in TOOLS.items()}
tdirs = {os.path.dirname(p) for p, _ in tp.values()}
assert tdirs == {A + '/v007_final_prereg_c4/seal_tools_v004'}, tdirs     # basis.selection: all five tools from seal_tools_v004
TD = tdirs.pop()
RMD3, RMD4 = role('readme_v003_run_order'), role('readme_v004_delta')
assert role('selected_r6') == (R6, R6S) and role('selected_v003_superseded_for_the_seal') == (V3, V3S)
v4_disc = role('root_manual_disclosures_file')           # names V001 (b9db6fd1): superseded by root A112, so not a pin source here
assert v4_disc[1] == D1S, v4_disc
d2b = H.pin(D2, D2_ROOT_SHA, 'manual_disclosures_v002'); D2S = hashlib.sha256(d2b).hexdigest(); assert D2S == D2_ROOT_SHA and len(d2b) == 6286
# the record format, read from tool 4 v004's own bytes
t4src = H.pin(*tp['T4'], 'tool_4').decode('utf-8')
assert "SCHEMA = 'UNT_V007_SEAL_RECORD_C4V004'" in t4src
assert t4src.count("'manual_disclosures': mdr,") == 1
assert "return {'pin': {'path': p, 'sha256': h}, 'content': obj, 'raw_text': text}" in t4src
assert "p.add_argument('--manual-disclosures')" in t4src and "p.add_argument('--manual-disclosures-sha256')" in t4src
REC_KEY, REC_FORM, REC_SCHEMA = 'manual_disclosures', 'pin_content_raw_text', 'UNT_V007_SEAL_RECORD_C4V004'
def tline(var):
    m = re.search(r'^%s="\$TD/([^"]+)";(\s+)%s_SHA="([0-9a-f]{64})"$' % (var, var), s, re.M)
    return m
R = []
for var in ('T_COMMON', 'T1', 'T2', 'T3', 'T5'):            # same basenames and bytes as v003: the lines stay, $TD moves to the v004 folder
    m = tline(var); p, h = tp[var]
    assert m and m.group(1) == os.path.basename(p) and m.group(3) == h, (var, m and m.groups(), p, h)
t4p, t4h = tp['T4']
R += [
 ('header', '# ROOT_SEAL_STEPS_c3v019.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY.',
  '# ROOT_SEAL_STEPS_c3v020.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY.'),
 ('header rulings', '# FROM_CODEX/0646 + 0647, rulings A110 and A111).\n', '# FROM_CODEX/0646 + 0647, rulings A110 and A111; FROM_CODEX/0648, ruling A112).\n'),
 ('history', '# c3v019 supersedes ROOT_SEAL_STEPS_c3v018.sh (32a023f0;',
  '''# c3v020 supersedes ROOT_SEAL_STEPS_c3v019.sh (f4843a47, SELECTED c3v008): FROM_CODEX/0648 (A112) and Claude4's
#   SELECTED_SEAL_TOOLS_V004_C4V001.json (593c59fa, 02:40:54Z), wired from its bytes, role-qualified:
#   P13 DONE: the v004 SELECTED file is the pin source of every seal tool; all five run from seal_tools_v004 (tool 4
#     build_seal_record_c4v004.py %s; seal_common and tools 1, 2, 3 and 5 are byte-identical to v003, at their v004-folder paths).
#     Step 0 checks every tool, both readmes (readme_v003_run_order, readme_v004_delta), selected_r6 and
#     selected_v003_superseded_for_the_seal against that one file.
#   A112: the disclosures file of record is SEAL_MANUAL_DISCLOSURES_V002.json (%s; V001 b9db6fd1 is superseded and refused in step 0).
#     Tool 4 gets it at step 10 with --manual-disclosures / --manual-disclosures-sha256 (basis.tool_4_cli_for_r6).
#   R-02 (basis.for_the_seal_script): step 11 checks the WRITTEN SEAL_RECORD before step 12 (helper c3v019 check-seal-record-disclosures,
#     form pin_content_raw_text at key manual_disclosures, record schema UNT_V007_SEAL_RECORD_C4V004, all read from tool 4 v004 bytes):
#     raw_text as UTF-8 = the V002 bytes; pin = the V002 path and sha; content.e_r6_1_text = SELECTED_R6 basis.erratum_E_R6_1; content =
#     the file object. Generated by tools/make_root_script_c3v020.py. Nothing else changes.
# c3v019 superseded ROOT_SEAL_STEPS_c3v018.sh (32a023f0;''' % (t4h[:8], D2S[:8])),
 ('P13 rows', '''# |P13| tool 4 v004 (A110, 0646;     | PENDING (NOT PUBLISHED): build_seal_record + --manual-disclosures <path>        | Claude4's seal-tools   |
# |   | Claude4)                     | --manual-disclosures-sha256 <hex>, root's disclosures file verbatim in the     | SELECTED file (v004 or |
# |   |                              | SEAL_RECORD. Step 0 REFUSES until V004_SELECTED and T4 are wired from it.      | v003 r2)               |''',
  '''# |P13| tool 4 v004 (A110, 0646;     | DONE (c3v020): wired from SELECTED_SEAL_TOOLS_V004_C4V001.json (593c59fa), the  | done (c3v020)          |
# |   | Claude4)                     | pin source of every tool; step 11 checks the written SEAL_RECORD (R-02) against | A112: V002 disclosures |
# |   |                              | root's V002 disclosures file (a0284ece; A112).                                  |                        |'''),
 ('helper pin', 'HELPER="$C3/tools/seal_steps_c3sa_c3v017.py";          HELPER_SHA="3c642d1a8be8bdac12d3472add602065c6d86cc47c7f3d96c297f534056a047b"',
  'HELPER="$C3/tools/seal_steps_c3sa_c3v019.py";          HELPER_SHA="%s"' % HS),
 ('disclosures', '''# A110 (0646, 0647): root's manual disclosures (E_R6_1's text, the C-08 table and confirmation, root's disclosures), carried verbatim
# INSIDE the SEAL_RECORD by tool 4 v004 (step 10); step 0 pins and pre-checks them (helper check-disclosures)
DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json"; DISCLOSURES_SHA="b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6"
''', '''# A110 (0646, 0647) + A112 (0648): root's manual disclosures (E_R6_1's text, the C-08 table and confirmation, root's disclosures with the
# A106_2_SRR13_CHECK_SPLIT row for r6 seal_record_requirements[13], R-05), carried verbatim INSIDE the SEAL_RECORD by tool 4 v004 (step 10);
# step 0 pins and pre-checks the file (helper check-disclosures) and refuses a superseded version; step 11 checks the written record (R-02)
DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json"; DISCLOSURES_SHA="%s"
DISCLOSURES_SUPERSEDED_SHAS="%s"   # A112: V001, superseded (left in place, never used)
# R-02: where and how tool 4 v004 writes it (read from build_seal_record_c4v004.py %s: its SCHEMA and its manual_disclosures field)
DISCLOSURES_RECORD_KEY="%s"; DISCLOSURES_RECORD_FORM="%s"; SEAL_RECORD_SCHEMA="%s"
''' % (D2S, D1S, t4h[:8], REC_KEY, REC_FORM, REC_SCHEMA)),
 ('tools status', '''# seal tools v003 (P1 DONE): Claude4's SELECTED_SEAL_TOOLS_V003_C4V001.json (00:51:45Z), checked role-qualified in step 0
SEAL_TOOLS_STATUS="V003_SELECTED_C4V001"
''', '''# seal tools v004 (P1 and P13 DONE, c3v020): Claude4's SELECTED_SEAL_TOOLS_V004_C4V001.json (02:40:54Z) is the pin source of every tool
# (V004_SELECTED below); the v003 SELECTED file stays pinned only as the role selected_v003_superseded_for_the_seal of that file (step 0)
SEAL_TOOLS_STATUS="V004_SELECTED_C4V001"
'''),
 ('TD', 'TD="$A/v007_final_prereg_c4/seal_tools_v003"', 'TD="$A/v007_final_prereg_c4/seal_tools_v004"   # c3v020: every tool runs from here (v004 basis.selection; A112)'),
 ('P13 block', '''# P13 (A110): tool 4 is v004 (build_seal_record + --manual-disclosures), as Claude4's seal-tools SELECTED file (v004 or v003 r2) names
# it: PENDING, NOT PUBLISHED, so step 0 refuses. v003's tool 4 (de0ceb15) is no longer the seal's tool 4.
V004_SELECTED="PENDING_SEAL_TOOLS_V004_SELECTED_FILE (Claude4, A110)"; V004_SELECTED_SHA="PENDING"; V004_SELECTED_SCHEMA="PENDING"
T4="PENDING_TOOL4_V004 (Claude4, A110)";        T4_SHA="PENDING"''',
  '''# P13 (A110) DONE in c3v020: tool 4 is v004, exactly as Claude4's SELECTED_SEAL_TOOLS_V004_C4V001.json names it (role tool_4_build_seal_record),
# checked from bytes in step 0 with every other tool. v003's tool 4 (de0ceb15) is not the seal's tool 4.
V004_SELECTED="$A/v007_final_prereg_c4/seal_tools_v004/SELECTED_SEAL_TOOLS_V004_C4V001.json"; V004_SELECTED_SHA="%s"; V004_SELECTED_SCHEMA="%s"
T4="$TD/%s";          T4_SHA="%s"''' % (V4S, V4C, os.path.basename(t4p), t4h)),
 ('readmes', 'V003_README="$TD/README_SEAL_TOOLS_V003.md";    V003_README_SHA="8601211723b352a9498fa4cb8d3dc4b64d30b7451c400c89230e5d13cd909ea0"',
  'V003_README="%s";    V003_README_SHA="%s"   # role readme_v003_run_order\nV004_README="$TD/%s";    V004_README_SHA="%s"   # role readme_v004_delta'
  % (RMD3[0].replace(A, '$A', 1), RMD3[1], os.path.basename(RMD4[0]), RMD4[1])),
 ('B2 comment', '# the B2 record of record (A100; r6 asks the seal record to repeat its disclosure block, so v003 tool 4 needs --b2-record): V009 gate_records.B2',
  '# the B2 record of record (A100; r6 asks the seal record to repeat its disclosure block, so tool 4 needs --b2-record): V009 gate_records.B2'),
 ('PENDING case', '''  case "$SEAL_TOOLS_STATUS $V003_SELECTED $V003_SELECTED_SHA $V004_SELECTED $V004_SELECTED_SHA $V004_SELECTED_SCHEMA $T4 $T4_SHA $DISCLOSURES $DISCLOSURES_SHA $PREREG_TOR''',
  '''  case "$SEAL_TOOLS_STATUS $V003_SELECTED $V003_SELECTED_SHA $V004_SELECTED $V004_SELECTED_SHA $V004_SELECTED_SCHEMA $T4 $T4_SHA $DISCLOSURES $DISCLOSURES_SHA $DISCLOSURES_RECORD_KEY $DISCLOSURES_RECORD_FORM $SEAL_RECORD_SCHEMA $PREREG_TOR'''),
 ('PENDING message', '''*PENDING*) echo "REFUSE: a PINS value is still PENDING (P13: tool 4 v004 and Claude4's seal-tools SELECTED file naming it, A110)" >&2; false;; esac''',
  '''*PENDING*) echo "REFUSE: a PINS value is still PENDING" >&2; false;; esac'''),
 ('superseded disclosures', '''  case " $COMPARE_SUPERSEDED_SHAS " in *" $UNT_SEAL_COMPARE_REVIEWED_SHA256 "*) echo "REFUSE: the compare source is a superseded round (A102)" >&2; false;; esac\n''',
  '''  case " $COMPARE_SUPERSEDED_SHAS " in *" $UNT_SEAL_COMPARE_REVIEWED_SHA256 "*) echo "REFUSE: the compare source is a superseded round (A102)" >&2; false;; esac
  case " $DISCLOSURES_SUPERSEDED_SHAS " in *" $DISCLOSURES_SHA "*) echo "REFUSE: the disclosures file is a superseded version (A112: V002 is the file of record)" >&2; false;; esac
'''),
 ('role checks', '''  # 0643 C: the seal tools are exactly what Claude4's v003 SELECTED file names (paths and shas, from bytes)
  H selected-roles --selected "$V003_SELECTED" --selected-sha "$V003_SELECTED_SHA" --schema "$V003_SELECTED_SCHEMA" \\
        --role-pin "seal_common=$T_COMMON=$T_COMMON_SHA" --role-pin "tool_1_check_frozen_addendum=$T1=$T1_SHA" \\
        --role-pin "tool_2_check_sealed_compare=$T2=$T2_SHA" --role-pin "tool_3_check_slot_fill=$T3=$T3_SHA" \\
        --role-pin "tool_5_print_driver_build_record=$T5=$T5_SHA" \\
        --role-pin "readme=$V003_README=$V003_README_SHA" --role-pin "selected_r6=$R6_SELECTED=$R6_SELECTED_SHA"
  # P13 (A110): tool 4 v004 exactly as Claude4's seal-tools SELECTED file names it (role tool_4_build_seal_record)
  H selected-roles --selected "$V004_SELECTED" --selected-sha "$V004_SELECTED_SHA" --schema "$V004_SELECTED_SCHEMA" \\
        --role-pin "tool_4_build_seal_record=$T4=$T4_SHA"
''', '''  # 0643 C / P13 (c3v020): the seal tools are exactly what Claude4's v004 SELECTED file names (paths and shas, from bytes, role-qualified);
  # it also names both readmes, the r6 SELECTED file and the v003 SELECTED file it supersedes for the seal. (Its role
  # root_manual_disclosures_file names V001, superseded by root A112; the disclosures pin is root's V002 above.)
  H selected-roles --selected "$V004_SELECTED" --selected-sha "$V004_SELECTED_SHA" --schema "$V004_SELECTED_SCHEMA" \\
        --role-pin "seal_common=$T_COMMON=$T_COMMON_SHA" --role-pin "tool_1_check_frozen_addendum=$T1=$T1_SHA" \\
        --role-pin "tool_2_check_sealed_compare=$T2=$T2_SHA" --role-pin "tool_3_check_slot_fill=$T3=$T3_SHA" \\
        --role-pin "tool_4_build_seal_record=$T4=$T4_SHA" --role-pin "tool_5_print_driver_build_record=$T5=$T5_SHA" \\
        --role-pin "readme_v003_run_order=$V003_README=$V003_README_SHA" --role-pin "readme_v004_delta=$V004_README=$V004_README_SHA" \\
        --role-pin "selected_r6=$R6_SELECTED=$R6_SELECTED_SHA" --role-pin "selected_v003_superseded_for_the_seal=$V003_SELECTED=$V003_SELECTED_SHA"
'''),
 ('step 11 R-02', '''  [ "$SR_SHA" = "$(jf "$T4_STDERR" seal_record_sha256)" ] || { echo "REFUSE: SEAL_RECORD sha differs from tool 4 stderr" >&2; false; }\n''',
  '''  [ "$SR_SHA" = "$(jf "$T4_STDERR" seal_record_sha256)" ] || { echo "REFUSE: SEAL_RECORD sha differs from tool 4 stderr" >&2; false; }
  # R-02 (SELECTED v004 basis.for_the_seal_script; A112): the WRITTEN SEAL_RECORD carries the V002 disclosures file verbatim, before step 12:
  # raw_text as UTF-8 = the file bytes; pin = its path and sha; content.e_r6_1_text = SELECTED_R6 basis.erratum_E_R6_1; content = the file
  run_h STEP_11_DISCLOSURES_VERBATIM check-seal-record-disclosures --seal "$SEAL_RECORD" --seal-sha "$SR_SHA" --disclosures "$DISCLOSURES" \\
        --disclosures-sha "$DISCLOSURES_SHA" --key-path "$DISCLOSURES_RECORD_KEY" --form "$DISCLOSURES_RECORD_FORM" --record-schema "$SEAL_RECORD_SCHEMA" \\
        --r6-selected "$R6_SELECTED" --r6-selected-sha "$R6_SELECTED_SHA" --r6-schema "$R6_SELECTED_SCHEMA"
'''),
 ('B8 comment', '  # B8 (README_SEAL_TOOLS_V003): v003 tool 4 --check-admission-config on the written config and the SEAL_RECORD, before the receipt',
  '  # B8 (README_SEAL_TOOLS_V003 order; README_SEAL_TOOLS_V004_DELTA): tool 4 v004 --check-admission-config on the written config and the SEAL_RECORD, before the receipt'),
 ('root_next C-08', '''is recorded in c08_table and c08_confirmation of the disclosures file SEAL_MANUAL_DISCLOSURES_V001.json b9db6fd1, which tool 4 v004 carried verbatim INSIDE the SEAL_RECORD: nothing to publish separately",''',
  '''is recorded in c08_table and c08_confirmation of the disclosures file SEAL_MANUAL_DISCLOSURES_V002.json %s (A112; its row A106_2_SRR13_CHECK_SPLIT states the C-02 to C-08 split, R-05), which tool 4 v004 carried verbatim INSIDE the SEAL_RECORD (checked at step 11, R-02): nothing to publish separately",''' % D2S[:8]),
 ('summary pins', '''    manual_disclosures "$DISCLOSURES $DISCLOSURES_SHA (verbatim inside the SEAL_RECORD through tool 4 v004; A110)"''',
  '''    manual_disclosures "$DISCLOSURES $DISCLOSURES_SHA (V002 per A112; verbatim inside the SEAL_RECORD through tool 4 v004; A110)" \\
    manual_disclosures_in_record "$DISCLOSURES_RECORD_KEY ($DISCLOSURES_RECORD_FORM; record schema $SEAL_RECORD_SCHEMA), checked at step 11 (R-02)"'''),
]
out = s
for rid, o, n in R:
    assert out.count(o) == 1, (rid, out.count(o))
    out = out.replace(o, n)
assert 'PENDING_SEAL_TOOLS_V004_SELECTED_FILE' not in out and 'T4_SHA="PENDING"' not in out and 'SEAL_MANUAL_DISCLOSURES_V001.json"' not in out
assert out.count('--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"') == 1
assert '"$V003_SELECTED"' not in out.replace('selected_v003_superseded_for_the_seal=$V003_SELECTED=$V003_SELECTED_SHA', '')
progs = re.findall(r'"\$\{PYX\[@\]\}" -c \'(.*?)\'', out, re.S)
for pr in progs:
    compile(pr, 'embedded', 'exec', dont_inherit=True)
summ = out[out.index('summary() {'):out.index('step0_preflight\nstep1_freeze')]
assert "'" not in summ.split("-c '", 1)[1].split("' \"$SUMMARY\"", 1)[0]
with open(OUT, 'x') as f:
    f.write(out)
bn = subprocess.run(['/bin/bash', '-n', OUT], capture_output=True, text=True)
print(json.dumps({'generated': {'path': OUT, 'sha256': hashlib.sha256(out.encode()).hexdigest(), 'bytes': len(out.encode())}, 'from': SRC_SHA,
                  'v004_selected': {'path': V4, 'sha256': V4S}, 'td': TD, 'tool_4': {'path': t4p, 'sha256': t4h},
                  'tools': {v: {'path': p, 'sha256': h} for v, (p, h) in tp.items()}, 'readmes': {'v003_run_order': RMD3, 'v004_delta': RMD4},
                  'disclosures_v002': {'path': D2, 'sha256': D2S, 'bytes': len(d2b)}, 'v004_file_names_disclosures': {'path': v4_disc[0], 'sha256': v4_disc[1], 'note': 'V001, superseded by A112'},
                  'record_format': {'key': REC_KEY, 'form': REC_FORM, 'schema': REC_SCHEMA}, 'replacements': len(R), 'embedded_python_programs_compiled': len(progs),
                  'bash_n_ok': bn.returncode == 0}, indent=1))
sys.exit(0 if bn.returncode == 0 else 2)
