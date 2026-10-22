# Claude3 seal-assembly builder (FROM_CODEX/0646 + 0647): derive ROOT_SEAL_STEPS_c3v019.sh from ROOT_SEAL_STEPS_c3v018.sh (32a023f0,
# used only by dry run 20261019T013817Z, which stopped at the summary): the two new root_next strings contained apostrophes, which
# closed the summary's single-quoted python program. They are reworded without one; the step-12 echo no longer says "v003". This
# generator also compiles every single-quoted python program the script passes to "${PYX[@]}" -c. Writes the script exclusively.
# usage: python3 -I -B make_root_script_c3v019.py SEAL_ASSEMBLY_C3_DIR
import hashlib, re, sys
C3 = sys.argv[1]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v018.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == '32a023f0bc2ea7587cf05bc963d6ad96a30bd6a9b84164083afe1f46fa91ab1b'
s = src.decode('utf-8')
R = []
R.append(('header', '# ROOT_SEAL_STEPS_c3v018.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY.',
          '# ROOT_SEAL_STEPS_c3v019.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY.'))
R.append(('history', '# c3v018 supersedes ROOT_SEAL_STEPS_c3v017.sh (b6037eee; never run, never published).',
          '''# c3v019 supersedes ROOT_SEAL_STEPS_c3v018.sh (32a023f0; used only by dry run 20261019T013817Z, which passed steps 0-13 and stopped at
#   the summary): its two new root_next strings held apostrophes, which closed the summary's single-quoted python program. Reworded;
#   the step-12 echo says "tool 4", not "v003 tool 4". Nothing else changes.
# c3v018 superseded ROOT_SEAL_STEPS_c3v017.sh (b6037eee; never run, never published).'''))
R.append(('root_next C-08', '''"C-08 (A106.2, A110): root's manual check against the IMPL of record r13 COMPARE_V007_IMPL_R13.md 274f7049 is recorded in the disclosures file's c08_table and c08_confirmation (SEAL_MANUAL_DISCLOSURES_V001.json b9db6fd1), which tool 4 v004 carried verbatim INSIDE the SEAL_RECORD: nothing to publish separately",''',
          '''"C-08 (A106.2, A110): the root manual check against the IMPL of record r13 COMPARE_V007_IMPL_R13.md 274f7049 is recorded in c08_table and c08_confirmation of the disclosures file SEAL_MANUAL_DISCLOSURES_V001.json b9db6fd1, which tool 4 v004 carried verbatim INSIDE the SEAL_RECORD: nothing to publish separately",'''))
R.append(('root_next E_R6_1', '''"erratum E_R6_1 (A110): INSIDE the SEAL_RECORD (the disclosures file's e_r6_1_text, byte-equal to the r6 SELECTED file's basis.erratum_E_R6_1, checked in step 0): no separate statement",''',
          '''"erratum E_R6_1 (A110): INSIDE the SEAL_RECORD (e_r6_1_text of the disclosures file, byte-equal to basis.erratum_E_R6_1 of the r6 SELECTED file, checked in step 0): no separate statement",'''))
R.append(('step 12 echo', 'echo "  PASS  STEP_12_TOOL4_ADMISSION.json (v003 tool 4, B8)"', 'echo "  PASS  STEP_12_TOOL4_ADMISSION.json (tool 4, B8)"'))
out = s
for rid, o, n in R:
    assert out.count(o) == 1, (rid, out.count(o))
    out = out.replace(o, n)
# every "${PYX[@]}" -c '...' program (single-quoted in bash) must compile as python: no apostrophe can end it early
progs = re.findall(r'"\$\{PYX\[@\]\}" -c \'(.*?)\'', out, re.S)
assert len(progs) >= 4, len(progs)
for p in progs:
    compile(p, 'embedded', 'exec', dont_inherit=True)
summ = out[out.index('summary() {'):out.index('step0_preflight\nstep1_freeze')]
assert "root's" not in summ and "file's" not in summ
dst = C3 + '/ROOT_SEAL_STEPS_c3v019.sh'
with open(dst, 'x') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v019.sh', hashlib.sha256(out.encode()).hexdigest(), 'replacements', len(R), 'embedded python programs compiled', len(progs))
