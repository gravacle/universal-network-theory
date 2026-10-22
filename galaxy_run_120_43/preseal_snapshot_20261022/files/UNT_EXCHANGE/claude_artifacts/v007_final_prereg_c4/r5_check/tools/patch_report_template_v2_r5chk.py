# patch_report_template_v2_r5chk.py -- report template v2 = v1 + A103 (21:43Z) and the seal tools v003 context. Anchored edits,
# each anchor exactly once; --dry-run prints the result sha; the real run writes tools/report_template_v2_r5chk.md by exclusive create.
import sys, os, hashlib
D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check'
src = open(os.path.join(D, 'tools', 'report_template_r5chk.md')).read()
E = [
 ("and copy 2 `{S:scratch/V005_ADDENDUM_READ_COPY_2_R5CHK.md}` (21:23:09Z, adds **A102**). Every entry A47-A102 was read in full.",
  "copy 2 `{S:scratch/V005_ADDENDUM_READ_COPY_2_R5CHK.md}` (21:23:09Z, adds **A102**) and copy 3 `{S:scratch/V005_ADDENDUM_READ_COPY_3_R5CHK.md}` (21:50:25Z, adds **A103**). Every entry A47-A103 was read in full. This V002 report supersedes REPORT_R5CHK_C4V001.md (written before A103); every test result is unchanged."),
 ("1 BLOCKING (F-01: A102 at 21:22Z postdates r5 and touches its text)",
  "1 BLOCKING (F-01: A102 at 21:22Z and A103 at 21:43Z postdate r5 and touch its text)"),
 ("On copy 2 (with A102) the 20 rows still re-hash, because A102 was inserted above A101 and changes no other section; **A102 has no row**. `out/ENTRY_SHAS_R5CHK.json` `{P:out/ENTRY_SHAS_R5CHK.json}`, `out/ENTRY_SHAS_ON_COPY2_R5CHK.json` `{P:out/ENTRY_SHAS_ON_COPY2_R5CHK.json}`. TESTED.",
  "On copy 2 (with A102) and copy 3 (with A103) the 20 rows still re-hash, because both entries were inserted above A101 and change no other section; **A102 and A103 have no row**. `out/ENTRY_SHAS_R5CHK.json` `{P:out/ENTRY_SHAS_R5CHK.json}`, `out/ENTRY_SHAS_ON_COPY2_R5CHK.json` `{P:out/ENTRY_SHAS_ON_COPY2_R5CHK.json}`, `out/ENTRY_SHAS_ON_COPY3_R5CHK.json` `{P:out/ENTRY_SHAS_ON_COPY3_R5CHK.json}`. TESTED."),
 ("- **A102 (21:22Z) is not covered**, and it touches r5's text: F-01.",
  "- **A102 (21:22Z) and A103 (21:43Z) are not covered**, and both touch r5's text: F-01."),
 ("| T1b | the same, `--covered-later A102` | REFUSE: FROZEN_PATH_NOT_PATH_TO_BE only |",
  "| T1b | the same, `--covered-later A102` | REFUSE: FROZEN_PATH_NOT_PATH_TO_BE only. A bare name covers the entry: this is Codex3's D-05 counterexample (0637), which seal tools v003 (0633/0634; being built) closes with a root-written dispositions JSON |"),
 ("| GAP-01 | frozen V005 addendum | MISSING. The open file is now 27b62183 (A102); freeze after the last pre-seal entry. M11: a stale pin refuses | Claude2 | YES |",
  "| GAP-01 | frozen V005 addendum | MISSING. The open file moved to 27b62183 (A102) and then 643ef6ef (A103) during this check; freeze after the last pre-seal entry. M11: a stale pin refuses | Claude2 | YES |"),
 ("the r5 table A82-A101 is honest and re-hashes (20/20, on both byte copies). **A102 is uncovered and touches the compare rule (F-01)** | Claude2 (route), then Claude4 (r6) | YES |",
  "the r5 table A82-A101 is honest and re-hashes (20/20, on all three byte copies). **A102 and A103 are uncovered and touch r5's text (F-01)** | Claude2 (route: r6, or v003 dispositions rows marked revised), then Claude4 | YES |"),
 ("Delta reviews by Claude3 and Codex2 pending (0632) | Claude3, Codex2; then Claude2 | YES |",
  "Delta reviews pending: Claude3, and Codex1 substituting for Codex2 (A103, 0635) | Claude3, Codex1; then Claude2 | YES |"),
 ("| GAP-24 (new) | independent review of seal tools v002 | landed 21:21-21:32Z; Codex3's review (0628) was waiting on delivery (0633) | Codex3 | YES (root uses them) |",
  "| GAP-24 (new) | seal tools review | Codex3 reviewed v002 and found the bare `--covered-later` defect (0637, BLOCKING) and B8 (0639). v003 is being built (0633/0634, `seal_tools_v003/`); Codex1 takes the v003 delta (0638); Codex3 is in reserve | Claude4 (v003); Codex1 | YES (root uses them) |"),
 ("**F-01 BLOCKING (TESTED, FORMAL). A102 postdates r5 and touches its text, so r5 cannot be sealed as written.**",
  "**F-01 BLOCKING (TESTED, FORMAL). A102 and A103 postdate r5 and touch its text, so r5 cannot be sealed as written.**"),
 ("- r5's entry table ends at A101. A99.3 requires the prereg to list every entry from A82 to the freeze. Tool 1 v002 refuses UNCOVERED_LATER_ENTRY: A102 (T1a), and my extractor finds A102 without a row.",
  "- A103 (21:43Z) makes Codex1 the r13 cross-lineage delta reviewer of record in place of Codex2 (A81 RI-20 named Codex2), and makes cx3r008 the step-5 NGC driver in place of cx3r007. The open V005 is now 643ef6ef.\n- r5's entry table ends at A101. A99.3 requires the prereg to list every entry from A82 to the freeze. Tool 1 v002 refuses UNCOVERED_LATER_ENTRY: A102 (T1a), and my extractor finds A102 and A103 without rows."),
 ("- r5's compare-slot rule begins \"The final compare round is r12 cx3v002 (4bd7b262 ...)\". That sentence is now false, and r5's RI-28 is no longer open.",
  "- Three r5 sentences are now false: the compare rule's \"The final compare round is r12 cx3v002 (4bd7b262 ...)\"; its \"delta reviews of record, Claude3's and Codex2's\" (A103: Codex1 for r13); and the scope note's \"the step-5 launch registry is SPEC_REGISTRY_CX3R007\" (A103: cx3r008). r5's RI-28 is no longer open."),
 ("- **Fix:** Claude4 writes prereg r6 once r13's delta reviews are in. It needs an A102 row (\"revised here\": the compare slot names r13 and its reviews of record), a generic compare rule (F-02) and RI-28 resolved. Alternatively, Claude2 rules an explicit superseding seal-record note for A102 and the r12 sentence (amending A99.3's literal requirement).",
  "- **Fix, either route:**\n  - (i) Claude4 writes prereg r6 once r13's delta reviews are in. It needs A102 and A103 rows marked \"revised here\" (the compare slot names r13 and its reviews of record, Claude3 and Codex1; the scope note names cx3r008), a generic compare rule (F-02) and RI-28 resolved.\n  - (ii) Root writes the v003 dispositions JSON (0633, 0105) with rows for A102 and A103 marked **revised**, each with a reason that names the r5 sentence it supersedes, and accepts that the sealed text keeps those sentences while the SEAL_RECORD carries the supersession (as RI-35 does for the status line). A `no_change` row for either entry would be untrue."),
 ("- **Owner:** Claude2 (the route), then Claude4.\n\n**F-02",
  "- **Owner:** Claude2 (the route), then Claude4 (r6, or seal tools v003).\n\n**F-02"),
 ("- **Fix (r6):** \"V007 seals on the final round whose delta reviews of record each report 0 blocking (A81 RI-20, as applied by A83, A86, A91, A96, A102); candidates: r12 (superseded, A102), r13\". Any root ruling that clears an item without a fix round is then a later entry, handled by the table.",
  "- **Fix (r6):** \"V007 seals on the final round whose delta reviews of record each report 0 blocking (A81 RI-20, as applied by A83, A86, A91, A96, A102, A103); candidates: r12 (superseded, A102), r13 (reviews of record: Claude3 and Codex1, A103)\". Any root ruling that clears an item without a fix round is then a later entry, handled by the table."),
]
for old, new in E:
    n = src.count(old)
    assert n == 1, ('anchor count', n, old[:80])
    src = src.replace(old, new)
src = src.replace('# REPORT: independent check of prereg r5', '# REPORT V002: independent check of prereg r5', 1)
sha = hashlib.sha256(src.encode()).hexdigest()
if '--dry-run' in sys.argv:
    print('DRY_RUN template v2 sha', sha)
else:
    p = os.path.join(D, 'tools', 'report_template_v2_r5chk.md')
    with open(p, 'x') as f:
        f.write(src)
    print('WROTE', p, hashlib.sha256(open(p, 'rb').read()).hexdigest())
