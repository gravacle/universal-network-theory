# make_root_script_c3v012.py: Claude3 (FROM_CODEX/0644, A107; Codex1 0101). Derives ROOT_SEAL_STEPS_c3v012.sh from c3v011 (af74e9bd).
import hashlib, sys
C3, HELPER_SHA = sys.argv[1], sys.argv[2]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v011.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'af74e9bde45a5ec0d082ed61f61261757986f1796ebf448746355bf1871111dc'
assert hashlib.sha256(open(C3 + '/tools/seal_steps_c3sa_c3v013.py', 'rb').read()).hexdigest() == HELPER_SHA
s = src.decode('utf-8')
R = [
 ('''# ROOT_SEAL_STEPS_c3v011.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640; FROM_CODEX/0642, ruling A105; FROM_CODEX/0643, ruling A106).
''', '''# ROOT_SEAL_STEPS_c3v012.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640; FROM_CODEX/0642, ruling A105; FROM_CODEX/0643, ruling A106; FROM_CODEX/0644, ruling A107).
# c3v012 supersedes ROOT_SEAL_STEPS_c3v011.sh (af74e9bd; FROM_CODEX/0644, A107 in the V006 addendum; Codex1 0101): helper c3v013
#   (C02-SEL-STRICT and C02-SEL-ASSOCIATION for the r6 and v003 SELECTED files; A106-C03-S1; the C-04 gate pass-verdict check) and
#   P12 = A107 option (b): step 3b passes the explicit two-entry exclusion list C04_EXCLUSIONS. Nothing else changes.
'''),
 ('''# |P12| C-04 scope for EPS_NGC and   | V009 registers neither EPS_NGC (1d5eef1b: gate EPS, producer eps_ngc91_        | root ruling            |
# |   | I1T_NGC (0643 finding)       | assemble 04bba30b) nor I1T_NGC (3ae7981a: I1T_NGC is no registry gate). Strict | (PENDING_ROOT_RULING)  |
# |   |                              | C-04 ('every slot must PASS') refuses the current draft at step 3b.            |                        |
''', '''# |P12| C-04 scope for EPS_NGC and   | RULED A107 (V006 addendum), option (b): C-04 excludes exactly EPS_NGC          | done: C04_EXCLUSIONS   |
# |   | I1T_NGC                      | (1d5eef1b) and I1T_NGC (3ae7981a), by name, path and sha; every other slot     |                        |
# |   |                              | must PASS, with its gate's pass verdict. No registry V010.                     |                        |
'''),
 ('# the r13 IMPL) is a ROOT MANUAL CHECK: README_SEAL_ASSEMBLY_C3_c3v004.md gives the exact instructions, and the seal record says so.\n',
  '# the r13 IMPL) is a ROOT MANUAL CHECK: README_SEAL_ASSEMBLY_C3_c3v005.md gives the exact instructions, and the seal record says so.\n'),
 ('COMPARE_R13_SHA="f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157"   # A104: the compare of record; C-04 loads its load_producer_registry\n',
  'COMPARE_R13_SHA="f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157"   # A104: the compare of record; C-04 loads its load_producer_registry\n'
  '# A107 (V006 addendum), P12 option (b): C-04 excludes exactly these two slots, by name, path and sha; every other slot must PASS\n'
  'C04_EXCLUSIONS=("certificates.EPS_NGC=$A/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json=1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d"\n'
  '                "certificates.I1T_NGC=$A/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json=3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6")\n'),
 ('''  STEP=3b; echo "STEP 3b C-04 (A106.2): every slot record through r13's own load_producer_registry against registry V009; every slot must PASS"
  v005_still_frozen 3b
  run_h STEP_03B_C04 slot-registry --compare "$UNT_SEAL_COMPARE_REVIEWED_PATH" --compare-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \\
        --registry "$REGISTRY" --registry-sha "$REGISTRY_SHA" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA" --fence "$FENCE" --fence-sha "$FENCE_SHA"
''', '''  STEP=3b; echo "STEP 3b C-04 (A106.2, A107): every slot record but the two A107 exclusions, through r13's own load_producer_registry against V009, with its gate's pass verdict"
  v005_still_frozen 3b
  local x; C04_ARGS=(); for x in "${C04_EXCLUSIONS[@]}"; do C04_ARGS+=(--exclude "$x"); done
  run_h STEP_03B_C04 slot-registry --compare "$UNT_SEAL_COMPARE_REVIEWED_PATH" --compare-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \\
        --registry "$REGISTRY" --registry-sha "$REGISTRY_SHA" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA" --fence "$FENCE" --fence-sha "$FENCE_SHA" \\
        "${C04_ARGS[@]}"
'''),
 ('every NEW-item id of the NEW-item list is found in r13 as README_SEAL_ASSEMBLY_C3_c3v004.md instructs',
  'every NEW-item id of the NEW-item list is found in r13 as README_SEAL_ASSEMBLY_C3_c3v005.md instructs'),
 ('HELPER="$C3/tools/seal_steps_c3sa_c3v012.py";          HELPER_SHA="b13483966fcb8755608d73e05c0e70dc94e39a2b07635f54efc0c86849748bac"',
  'HELPER="$C3/tools/seal_steps_c3sa_c3v013.py";          HELPER_SHA="%s"' % HELPER_SHA),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
out = s.encode('utf-8')
with open(C3 + '/ROOT_SEAL_STEPS_c3v012.sh', 'xb') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v012.sh', hashlib.sha256(out).hexdigest(), len(out))
