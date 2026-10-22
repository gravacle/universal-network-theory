# REFUTE: the V007 seal rehearsal gap list (dispatch 0602, part 2)

Claude4 helper. UTC 2026-10-18T20:14:03Z (`date -u`). Folder `claude_artifacts/seal_rehearsal_c4/refute/`. Authority: Claude2 dispatch 0602, sha256 `c19bce2fed91cb499b423e57c6f71abe9258d9fd8f0ed6738db1857c55e97f5c` (from bytes).

**Object.** The rehearsal helper is agent `a727c02d4af55ea30` in workflow `wf_86f1d505-435`. Under review:
- `seal_rehearsal_c4/run/GAPS_C4V001.md` (`566b2066`);
- `GAPS_C4V001.json` (`eb9a0413`), written 19:33:45Z;
- its structured summary.

**Rulings read.** I read two exclusive byte copies of the open V005 addendum, made in this folder:
- `out/V005_ADDENDUM_READ_COPY_C4R.md`, `43b7f22c` (19:47:46Z, A47–A95);
- `out/V005_ADDENDUM_READ_COPY_2_C4R.md`, `991cc242` (19:57:12Z, adds A96).

The entries read are A62, A67, A69–A75, A77–A96. Full shas are in `HASHES_REFUTE_C4R.txt`.

**Labels:** TESTED (run or read from bytes here), FORMAL (follows from code or text read here), UNTESTED. **Severities:** BLOCKING, SHOULD_FIX, NOTE.

**Rules kept.**
- No launch, no compare run, no `--validity-only`.
- No UVT_* path, no C5H run path and no target data was opened, and no such directory was listed. My name searches pruned those names, and I never touched the real C5H run.
- Writes only in this folder, each by exclusive create.
- Every Python process that imported a program module ran under the exact fence `f813c430` (selftest 8/8 each time, BLOCKED list empty each time).

Shell names used in the reproductions:
- `PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
- `A=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts`
- `R=$A/seal_rehearsal_c4/refute`
- `ST=$A/v007_final_prereg_c4/seal_tools`
- `R4=$A/v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json`
- `export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`

## Verdict

The gap list mostly stands, but root should not rely on it until these five points are applied:

1. **GAP-03 cannot be closed by a seal slot (R-03, TESTED).**
   - In sealed mode, r11 and r12 read the case block only from the prereg's `binding_inputs.case_block`.
   - Seal tool 3 v001 refuses a sealed prereg that carries that key, with `SEALED_PREREG_TEXT_CHANGED`.
   - So closing GAP-03 needs a prereg r5 plus a tool 3 successor, or a compare change.
2. **The registry baseline was out of date when the list was written (R-01, TESTED).**
   - Claude3's registries C3V004 and C3V005 were born at 19:17:13Z. The rehearsal built its inputs at 19:19:21Z and wrote the gaps at 19:33:45Z.
   - Both registries already carry the c2v007r2 comparator, the identity tokens and the B1, B1_OFF and B0prime_RERUN records.
   - So GAP-07 and GAP-08 are no longer open as written, and part of GAP-13's list is done.
3. **GAP-02 misses A83 (R-02, FORMAL).** A83 changed how two r4 slot rules are met:
   - the compare rule's "three recheck lenses" became the reviews of record;
   - the comparator rule's "own check" became Codex2's check of record.

   A91, A92 and A96 apply this, so a plain no-change note cannot honestly cover it. The builder can only write a fixed "covers this entry" note.
4. **Seal tool 4 checks two of its inputs too weakly (R-04, FORMAL).**
   - It embeds any decimal-free text as the B6 outputs, without checking that they came from the sealed compare.
   - It accepts any strict JSON as the three B7 inputs.
5. **New since the rehearsal: B2 now fails (R-15, BLOCKING, TESTED).**
   - The B2 record of record `d4b41ffc` reads FAIL under A94.
   - Registries C3V006 and C3V007 carry it.
   - Root must rule on it before B4.

**Gaps (21).**
- 15 confirmed. GAP-02 is incomplete, GAP-03's fix path is corrected, and GAP-13's list is partly stale.
- 4 were right when written but have since moved: GAP-06, GAP-15 (B2 now FAILs, R-15), GAP-19 (now closed by A96) and GAP-20.
- 2 partly refuted, because they were already stale when written: GAP-07 and GAP-08.
- 3 missing, all NOTE: R-08, R-09 and R-10.

**The rehearsal's findings (14).**
- 11 confirmed: D-01–D-05, D-07–D-10, D-12 and N-13.
- D-06 partly refuted (R-06).
- D-11 is right, but it is FORMAL, not TESTED (R-07).
- N-14 understates the breach (R-05).

**The two process checks 0602 asked for:**
- **`--validity-only`:** never ran (TESTED over every command in the rehearsal transcript).
- **UVT_* and C5H:** no fenced or Python process of the rehearsal opened such a path. The three fenced r11 runs each end with an empty BLOCKED list (TESTED), and their code paths reach no C5H stat helper (FORMAL).
- **The one exception** is the unfenced broad `grep -r` of N-14. It can have opened synthetic C5H-named and UVT-named look-alikes and SPARC-named audit JSON inside claude_artifacts, and how far it got cannot be determined (R-05). No real run tree was reachable.
- **Nothing was created outside `seal_rehearsal_c4/`** (TESTED). The one exception is the Claude Code harness's own capture file for the backgrounded grep (R-14).

## 1. SEAL_CHECKLIST_R4 (`0d7eb429`), re-derived

| step | what it needs | gap in the list | state at 2026-10-18T20:14:03Z (evidence) |
|---|---|---|---|
| A1 | final compare round; 0 blocking from its reviews; IMPL lists NEW items | GAP-06, GAP-17 (NEW-item list); R-02 | r12 cx3v002 `4bd7b262` frozen 19:48:42Z; the delta reviews of record (Claude3, Codex2) are pending (A96, 0614). TESTED (bytes) |
| A2 | identity comparator | GAP-07 | ruled (A92, 0611) and registered from C3V004 onward (R-01). TESTED |
| A3 | r5 or r6 | GAP-19 | r5 (A96, 19:51Z). TESTED (read) |
| A4 | CASCADE_MAP_R5_ADDENDUM | GAP-18 | missing: a name search of claude_artifacts finds none. TESTED |
| A5 | identity runs, A59 tokens, raw successor-custody check, records of record | GAP-08, GAP-17 | records ruled (A92) and registered from C3V004 onward. The raw custody record is missing; it needs a UVT_* read, so it is root's (A59, A83). TESTED |
| A6 | successor B0 tool and B0 record rerun (B0-EMPTY) on the chosen driver | **not listed** (R-09) | the 0598 B0 record `c2cec35b` is built from `B0_R5_RUN_V001` (B0-EMPTY counts) and is registered in C3V007. The checklist row is still PENDING. TESTED |
| A7 | certificates of record | GAP-11, GAP-12 | EPS 598c8fa3 (A70); LO 1c384f76 (A70, A72); GQ V006 5a1b39f8 (A86); LO_NGC V002 33bc2190 (A87); DOUBLING ea48ac2b (A87). EPS_NGC has only a folder-level designation (A70); I1T_NGC has no entry. FORMAL |
| A8 | merged DOUBLING registered | GAP-11 | registered in C3V003–C3V007; tool 3 refuses it (D-01). TESTED |
| A9 | producer registry | GAP-13 | During the rehearsal: C3V004 `4c3f60b2` (r11 form) and C3V005 `f83f25c5` (r12 form). Since then, C3V006 `5a990a33` (19:57:08Z) adds B2, and C3V007 `34bbfe40` (20:05:00Z) adds B3, B0, B0prime_DRY and B0_FA (R-01). TESTED |
| A10 | key-equivalence map | GAP-17 | missing; the case block also carries a copy (R-10). TESTED (name search) |
| B1 | freeze; a revision or a note for every later entry | GAP-01, GAP-02 | no FROZEN file in the CLAUDE2 control folder; root is still writing the open file (`991cc242` at 19:57:12Z, with A96). TESTED |
| B2 | fix the driver (r6: cache directory) | GAP-19 | r5 `b5cc62af`; cache slot moot (A96, 0615). TESTED (read) |
| B3 | build-only binder: bound plan and command | GAP-10 | missing; 0615 says the r5 template only. TESTED (read) |
| B4 | sealed prereg | GAP-03, GAP-02 | cannot carry `binding_inputs.case_block` under tool 3 v001 (R-03). TESTED |
| B5 | sealed compare, five pins | GAP-04, GAP-05, GAP-13, GAP-01 | no step creates the driver BUILD record (R-06). FORMAL |
| B6 | `--gates-only` and `--validity-only --case C5H`, root | GAP-16 | not runnable until GAP-03, GAP-04 and GAP-13 close. FORMAL |
| B7 | SEAL_RECORD | GAP-17; E5-08 is r4 SRR[7], which the builder extracts | the builder accepts weak inputs (R-04). FORMAL |
| B8 | admission config naming the 13 BUILD_V005 sources | GAP-21, GAP-09, D-02 | V006 `fb9e6a4a` adds `postseal_records_cx1v006.py` and `srb_rot_record_cx1v008.py`. It removes or re-pins nothing, so launcher v007 `861bba68` and guard v008 `294cb776` are unchanged. TESTED |
| B9 | admission receipt | GAP-21 | due after the SEAL_RECORD |
| C1, C2 | launch | none | outside the seal |
| DONE rows | B3 465cb3c3; BUILD_V005 46bc5b5d | GAP-02, GAP-09, GAP-13 | A87 supersedes both: the B3 record is the JSON (`83c853b9`, registered in C3V007), and the BUILD moves to V006 |

## 2. Tool 3 SCHEMA (`check_slot_fill_c4v001`, `7f3cf07d`, SLOT_KEYS), re-derived

| slot | rehearsal value | ruling | gap in the list | state now |
|---|---|---|---|---|
| schema | UNT_V007_SEAL_SLOTS_C4V001 | none | none | fixed |
| driver_branch | r5 | A72, A89, then A96 | GAP-19 | r5 (A96) |
| ngc_gas_M_s | 96 | A81 RI-23 (conditional); A90 | **none** (R-08) | root must state the value |
| frozen_addendum | scratch copies | A82, RI-26 | GAP-01 | missing |
| driver | b5cc62af | A96 | none | filled |
| driver_build_record | PENDING, then the draft 2a3e4308 | A72, A82 | GAP-04 | missing |
| driver_check_record | CHECK.md 89a6de88 | A62.3, A67 | GAP-05 | root confirms (Codex3's r5 review is the other candidate) |
| compare_reviewed_source | r11 a5d10cb1 | A80, A86, A91, A96 | GAP-06 | r12 `4bd7b262` under delta review |
| identity_comparator | 052da0fe | A92, 0611 | GAP-07 | ruled and registered |
| identity_gate_records (Z2, Z2_OFF_RO1, B0prime_RERUN) | 83e7b067, 3b9ad402, e33af53d | A92 | GAP-08 | ruled and registered |
| launch_packet.build | BUILD_V005 46bc5b5d | A87 (V006) | GAP-09 | conflict |
| launch_packet.bound_plan, bound_command | PENDING | RI-25 | GAP-10 | missing |
| certificates.EPS | 598c8fa3 | A70 | none | filled |
| certificates.LO | 1c384f76 | A70, A72, A73 | none | filled |
| certificates.GQ | 5a1b39f8 (V006) | A86 | GAP-02 (r4 names V005) | filled |
| certificates.DOUBLING | ea48ac2b | A87 | GAP-11 | refused by tool 3 |
| certificates.EPS_NGC | 1d5eef1b | A70 (folder) | GAP-12 | root confirms |
| certificates.LO_NGC | 33bc2190 | A87 | none | filled |
| certificates.I1T_NGC | 3ae7981a | none | GAP-12 | root confirms |
| producer_registry | C3V003 6b6f76ae | A62.2, A67 N2, A69.1, A83 | GAP-13 | C3V004–C3V007 exist (R-01) |
| cache_directory_r6_only | NOT_APPLICABLE_R5 | A96 (RI-24 moot) | none | fixed |

**Not a SCHEMA slot, but the sealed compare needs it:** `binding_inputs.case_block` (GAP-03, R-03).

The **driver_build_record** and **driver_check_record** slots are tool-3 and sealed-compare pins only; they are not prereg seal slots. That is consistent with A82.

## 3. Gap-by-gap verdict

| gap | verdict | evidence | owner check (rulings) |
|---|---|---|---|
| GAP-01 frozen addendum | CONFIRMED | No FROZEN, SEAL_RECORD or ADMISSION name in the CLAUDE2 control folder; the open file moved to `991cc242` (A96) at 19:57:12Z. TESTED | root: right (A82, RI-26) |
| GAP-02 entries after A81 | CONFIRMED, INCOMPLETE | A83 is missing, with A91, A92 and A96, which apply it (R-02). The frozen text will need A82–A96 or later. FORMAL | Claude2 rules; Claude4 writes r5: right (A81) |
| GAP-03 case block | CONFIRMED; the fix path is wrong | r4 `binding_inputs` has no `case_block` (TESTED). No production block exists: Claude4's own step-4 check `84d6b674` agrees, and Claude3's `FINAL_SPECS_CASE_BLOCK_C3V001` (`4829b46e`) is a validation record, not a block (TESTED). The seal-slot option fails (R-03). | UNASSIGNED: right (no A-entry). Claude3 is an alternative owner: it has built the block in-process twice (R-11) |
| GAP-04 driver build record | CONFIRMED | Name search finds only the rehearsal draft and the SYNTH fixture. TESTED | root: right (r11 L297) |
| GAP-05 driver check record | CONFIRMED | No A-entry names `PIN_V010_R5_CHECK`. FORMAL | root: right |
| GAP-06 compare r12 | CONFIRMED, then MOVED | r12 cx3v002 `4bd7b262` frozen 19:48:42Z; delta reviews pending (A96, 0614). TESTED | Codex3; reviewers Claude3 and Codex2: right (A83, A86, A91, A96) |
| GAP-07 identity comparator | PARTLY REFUTED (stale) | Registered in C3V004 and C3V005 at 19:17:13Z (R-01). TESTED | Claude3: right, and done |
| GAP-08 identity records | PARTLY REFUTED (stale) | Registered in C3V004 and C3V005 (gate_records B1, B1_OFF, B0prime_RERUN). TESTED | Claude3: right, and done |
| GAP-09 BUILD V005 or V006 | CONFIRMED | Allowlists 13 vs 15. TESTED | A87 already directs a new BUILD V006, which Claude4 delta-checks. What remains open is root accepting it after the 0602 item 1 check, plus the text and tools (R-11) |
| GAP-10 bound plan and command | CONFIRMED | none on disk; 0615. TESTED | root: right (RI-25) |
| GAP-11 DOUBLING refused | CONFIRMED | `ms_values` gives []; the only M_s key is `$.ddo_gas_M_s` = 128 (TESTED, fenced). See R-13 on wording. | Claude4: right (0584) |
| GAP-12 EPS_NGC, I1T_NGC | CONFIRMED | A70 gives EPS_NGC a folder-level designation; I1T_NGC has none. FORMAL | root: right (A7) |
| GAP-13 registry successor | CONFIRMED; list partly stale | At the rehearsal, C3V005 lacked B2, B3, B0, B0prime_DRY, B0_FA, B0_RO1, B0_N3 and I4, and the SRB_ROT, MT, I1T and FLAG_RULINGS producers. C3V007 (20:05:00Z) lacks only B0_N3, B0_RO1, I4 and those four producers, as its own note lists. TESTED | Claude3; Codex2 cross-lineage (0605): right |
| GAP-14 B0_N3, B0_RO1, I4 | CONFIRMED | 0598 section 6. I4 is a mode gate, required under the default parallel8 (r11 L379, L418). FORMAL | records Claude4 (A87): right. The runs are coarser than "root launches" (R-11) |
| GAP-15 B2 | CONFIRMED, then MOVED | A94 and 0612 (19:40Z) set the rules. The B2 record `d4b41ffc` (born 19:51:09Z), registered in C3V006 and C3V007, reads verdict FAIL (R-15). TESTED | Claude3: right (A87, 0597) |
| GAP-16 B6 outputs | CONFIRMED | FORMAL | root: right |
| GAP-17 B7 inputs | CONFIRMED | only `*_SYNTH` fixtures. TESTED | UNASSIGNED: right. The checklist does have steps (A1, A5, A10) (R-06) |
| GAP-18 CASCADE_MAP_R5_ADDENDUM | CONFIRMED | 0 name hits. TESTED | UNASSIGNED in A69: right |
| GAP-19 driver r6 | CONFIRMED, then CLOSED | A96: V007 seals on r5; RI-24 moot; no cache slot (0615). TESTED (read) | done |
| GAP-20 SR_K | CONFIRMED, then MOVED | r12 adds SR_K to the after-seal set (A96 scope). C3V005 carries `PRODUCED_AFTER_THE_SEAL` and the `aggregate_records_cx1v008` pin (`9794123d`). TESTED | Codex3 (r12), root runs it: right (A88) |
| GAP-21 admission config and receipt | CONFIRMED | FORMAL | root: right |

## 4. Findings

### R-01 (SHOULD_FIX, TESTED). The registry baseline was out of date when the gaps were written

**Claim.**
- The summary calls registry C3V003 `6b6f76ae` "newest", and GAP-07, GAP-08 and GAP-13 say that V003 lacks the identity comparator, the tokens and the B1, B1_OFF and B0prime_RERUN records.
- But C3V004 (`4c3f60b2`) and C3V005 (`f83f25c5`) were born at 19:17:13Z. The rehearsal built its inputs at 19:19:21Z and wrote GAPS at 19:33:45Z.
- Both registries carry `identity_comparators = [052da0fe…]`, the identity tokens, and gate_records B1 `83e7b067`, B1_OFF and B0prime_RERUN.
- `VALIDATE_R11_C3V004` (`216d011d`, 19:17:36Z) reports registry V004 LOADED on r11, `case_block_refusals` [] and 5/5 pre-seal PASS.
- After the rehearsal, C3V006 (`5a990a33`, 19:57:08Z) added the B2 record, and C3V007 (`34bbfe40`, 20:05:00Z) added the B3, B0, B0prime_DRY and B0_FA records.
- G3 used V003, which r11 refuses at load. V004 loads.
- Neither GAPS nor PARTIAL mentions V004 or V005.

**Reproduction.**
1. `TZ=UTC stat -f '%SB %N' -t '%Y-%m-%dT%H:%M:%SZ' $A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V004.json $A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V005.json` gives 19:17:13Z for both.
2. `$PY -I -B -c "import json; d=json.load(open('$A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V005.json')); print(d['identity_comparators'], d['gate_records']['B1'], d['gate_records']['B1_OFF'], d['gate_records']['B0prime_RERUN'], d['gate_records']['SR_K'])"`
3. `$PY -I -B -c "import json; print(json.load(open('$A/seal_rehearsal_c4/run/scratch/REHEARSAL_INPUTS_MANIFEST_C4V001.json'))['utc'], json.load(open('$A/seal_rehearsal_c4/run/GAPS_C4V001.json'))['utc'])"`
4. `$PY -I -B -c "import json; print(json.load(open('$A/producer_registry_c3/out/VALIDATE_R11_C3V004.json'))['registry_load'])"`

**Fix.**
- Restate GAP-07 and GAP-08 as registered in candidate registries C3V004 (r11) and C3V005 (r12). Their remaining step is root's pin of the final registry, which is GAP-13.
- Rebase GAP-13 on the newest registry (C3V007 at 20:05Z).
- Any repeat of G3 uses C3V004 on r11, or the newest r12-form registry (C3V005 onward) on r12.

### R-02 (SHOULD_FIX, FORMAL). GAP-02 misses A83, and the builder cannot express the notes it needs

**Claim.** GAP-02 names A86, A87, A88 and A89 as the later entries that contradict r4. It misses A83 (18:19Z), which changed how two r4 slot rules are met.
- **Compare rule.** r4 `$.seal_slots.compare.rule` says V007 seals on the round "whose three recheck lenses and whose distinct reviews of record (Claude3 and Codex2) report 0 blocking". A83 stopped r11 before its rechecks and made Claude3 and Codex2 "the rechecks of record". A86 and A91 apply this to r11 and r12, and A96 says "The delta reviews of record are Claude3's and Codex2's". The r4 checklist row A1 says the same as the r4 rule.
- **Comparator rule.** r4 `$.seal_slots.identity_comparator.rule` requires "the c2v007-lineage round whose own check and Codex2's review report 0 blocking". A83 stopped c2v007's own check workflow and made Codex2's review "the check of record". A92 rules c2v007r2 on Codex2's delta check (0472). No entry after A83 records a separate own check of record for the c2v007 lineage.

These re-designations touch the prereg text under RI-26, so a plain "no change" is not true of them.

Two further points:
- The frozen text will hold A82–A96 at least, and root is still writing it.
- The builder turns every `--covered-later` entry into the fixed sentence "`<entry>`: covers this entry for the prereg text of record (A81 RI-26)" (L85). It therefore cannot record the "explicit superseding notes" option that GAP-02 offers. That option needs a builder successor.

**Reproduction.**
1. `$PY -I -B -c "import json; d=json.load(open('$R4')); print(d['seal_slots']['compare']['rule'][:240]); print(d['seal_slots']['identity_comparator']['rule'])"`
2. `sed -n '1076,1089p' $R/out/V005_ADDENDUM_READ_COPY_C4R.md` shows A83.
3. `sed -n '890,915p' $R/out/V005_ADDENDUM_READ_COPY_2_C4R.md` shows A96.
4. `sed -n '85p' $ST/build_seal_record_c4v001.py`

**Fix.** Claude2 rules on one of two routes:
- a prereg r5 (Claude4) that integrates A83, A86–A89, A91, A92 and A96;
- a builder successor that records a per-entry note (`no_change` or `superseded_by`, with the reason).

Either way, the checklist lists every entry from A82 to the freeze.

### R-03 (SHOULD_FIX, TESTED). D-03's "or as a seal slot" cannot work; GAP-03 forces a prereg r5 and a tool 3 successor

**Claim.**
- In sealed mode, r11 (L5689) and r12 cx3v002 (L5706) take the case block only from the prereg's `binding_inputs.case_block`, so a seal slot would be ignored and refused `CASE_BLOCK_ABSENT` (FORMAL).
- Tool 3 v001 refuses any sealed prereg that differs from r4 outside `seal_slots.<k>.value` (L120). Its text of record is fixed to r4 (`TEXT_OF_RECORD_SHA`, L26).
- I built a sealed prereg equal to the rehearsal's Run B construction except for one added key, `binding_inputs.case_block`. Tool 3 adds exactly one code, `SEALED_PREREG_TEXT_CHANGED`: the control gives 9 codes (`1af2b95f`), the case-block prereg 10 (`6a0c7f02`). TESTED, under the fence.
- So the only route that works with r11 or r12 is all three of: a prereg r5 carrying `binding_inputs.case_block` {path, sha256}; a tool 3 successor pinned to r5; and the case block itself, built and registered. The other route is a compare change.
- The builder needs no change for this, since it calls tool 3.

**Reproduction** (inputs built by `tools/make_cb_test_c4r.py` under the fence):
1. `cd $R && taskpolicy -b $PY -I -B $R/tools/run_fenced_c4r.py $ST/check_slot_fill_c4v001.py --slots $R/out/test_cb/SLOTS_T_C4R.json --prereg $R/out/test_cb/SEALED_PREREG_CTRL_C4R.json --text-of-record $R4` gives REFUSE, 9 codes, none of them `SEALED_PREREG_TEXT_CHANGED`.
2. The same command with `--prereg $R/out/test_cb/SEALED_PREREG_WITH_CASE_BLOCK_C4R.json` gives REFUSE, 10 codes, the first `SEALED_PREREG_TEXT_CHANGED`.
3. `awk 'NR==5689' $A/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` and `awk 'NR==5706' $A/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py` show the case-block line.

**Fix.**
- Drop the seal-slot alternative from D-03.
- Plan prereg r5 (Claude4) with `binding_inputs.case_block`, together with a tool 3 successor that pins r5. This is the same r5 that R-02, D-02 and D-05 point to, so one revision serves all four.
- The case block's owner (GAP-03) delivers its {path, sha256} before r5 is written.

### R-04 (SHOULD_FIX, FORMAL). The SEAL_RECORD builder does not check where its B6 and B7 inputs come from

**Claim.**
- **B6 outputs (L33–42).** `build_seal_record_c4v001` embeds any file for `--gates-only-output` and `--validity-only-output`, provided it contains no decimal number. It never checks that the file is a `…_GATES_ONLY` or `…_VALIDITY_ONLY` body with `test_mode: false` and `script_sha256` equal to the sealed compare. r11 writes those fields (L5796–5799). So a test-mode or other-compare output would pass into the SEAL_RECORD.
- **B7 inputs (L44–54).** It accepts any strict JSON for the key-equivalence map, the NEW-item list and the raw successor custody, with no schema.
- D-04 lists other missing tool checks but not these.

**Reproduction.** `sed -n '33,54p' $ST/build_seal_record_c4v001.py` and `sed -n '5796,5799p' $A/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py`.

**Fix.** A builder successor (Claude4) requires, for each E-SEAL1 file:
- the blinded schema;
- `test_mode` false;
- `script_sha256` equal to the sealed compare's sha.

It also validates the three B7 schemas, and checks the key map against the case block's `key_equivalence_map` (R-10).

### R-05 (SHOULD_FIX, TESTED). The broad search (N-14) is under-reported

**Claim.** I printed only the commands of the rehearsal transcript (`29e0e981`, `tools/audit_transcript_c4r.py`; no tool output was printed). Corrections to N-14:
- **Timing.** The search was call #67 at 19:02:22Z, not about 18:58Z. It ran past the 120 s timeout, was backgrounded as `b78dxm9ej`, and completed at 19:05:01Z with exit 0.
- **The tool.** In this shell `grep` is a function that runs the embedded ugrep 7.8.4, not BSD grep. Its `-r` follows symlinks only on the command line (TESTED from its help), so runs_ext was out of reach, as stated.
- **The classes it can have opened.** The lane's own E1 census (`seal_records_c4/build/PARTIAL.md`, 18:44–18:51Z, names only) shows 270 forbidden-class `*.json` physically inside claude_artifacts:
  - synthetic `runs_ext/KMAX_A2F10_C5H_RUN_V001` look-alike trees;
  - SPARC-named audit files, including `sparc_prefix_audit_0349/REAL_TARGET_BOOLEANS_0349_V001.json`, whose content may be target-derived;
  - one `runs_ext/UVT_dummy/a.json`.

  N-14 names only the UVT class.
- **How far it got.** The output has exactly 20 grep lines, so `head -20` may have cut the walk short. Which files were opened cannot be determined.
- **What was printed.** None of the 20 printed names is in a forbidden class (TESTED, by count only). No content was printed.

**Reproduction.**
1. `$PY -I -B $R/tools/audit_transcript_c4r.py <the transcript path in HASHES_REFUTE_C4R.txt> $R/out/<new name>.txt`: see entries #67–#70. Lines 214–226 of `out/REHEARSAL_TRANSCRIPT_COMMANDS_C4R.txt` show the same.
2. `type grep`
3. `grep --help | awk '/-r, --recursive/{p=3} p-->0'`
4. `sed -n '12,28p' $A/seal_records_c4/build/PARTIAL.md`

**Fix.**
- The Claude4 done post to Claude2 reports this breach with all three classes and the 19:02:22Z time.
- Helper briefs carry the no-recursive-grep rule, which is already in lane memory since 18:54Z, after this helper read memory at 18:52Z.

### R-06 (NOTE, FORMAL). D-06 is partly refuted

**Claim.** D-06 says the checklist has no step that creates the key map, the NEW-item list or the raw successor custody. It does:
- A10, "Key-equivalence map assembled for the seal record";
- A1, "its IMPL lists every NEW item with disposition";
- A5, "the raw successor-custody check".

Two things are truly missing:
- a step that creates the driver BUILD record named by `PIN_DRIVER_BUILD_RECORD` (B5 only sets the pin);
- any statement that the builder takes those three as JSON files.

**Reproduction.** `sed -n '8p;12p;17p;23p;25p' $A/v007_final_prereg_c4/r4/SEAL_CHECKLIST_R4.md`

**Fix.** Keep D-06 for the driver BUILD record and the JSON forms only.

### R-07 (NOTE, FORMAL). D-11 is FORMAL, not TESTED

**Claim.**
- No fenced r11 run reached `build_context`. G1 refused at L5673, G2 at L5697 and G3 at L5712, all before L5717, and the three BLOCKED lists are empty.
- The refusal of the V004 read follows from the fence rule (L60) and from `build_context` reading `PIN_ADDENDUM_V004` (r11 L164, L1228).
- The substance stands.

**Reproduction.** `tail -n 2 $A/seal_rehearsal_c4/run/out/G1_SEALED_A.stderr.txt`, and the same for the G2 and G3 stderr files; `sed -n '5673,5717p' $A/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py`.

**Fix.** Relabel D-11 as FORMAL.

### R-08 (NOTE, FORMAL). Missing gap: the `ngc_gas_M_s` slot

**Claim.**
- Tool 3 requires `ngc_gas_M_s` in {96, 128} (L89), and the SEAL_RECORD records it. The rehearsal set it to 96 without tracing that to a ruling.
- A81 RI-23 makes it conditional: it becomes 128 if GQ_NGC at M_s 96 fails anywhere on [2, 91].
- The nearest evidence is A90: the NGC N-tests were read (`tests_read = true`), and "certificate admission passes". No entry states the value for the V007 slot.

**Reproduction.** `sed -n '89,90p' $ST/check_slot_fill_c4v001.py`; `sed -n '1117p;971,972p' $R/out/V005_ADDENDUM_READ_COPY_C4R.md`

**Fix.** Root states `ngc_gas_M_s = 96` at assembly, citing A90 and Codex1 0056, or rules 128 under RI-23.

### R-09 (NOTE, FORMAL). Missing gap: checklist A6

**Claim.** A6 (successor B0 tool and B0 record rerun, B0-EMPTY, on the chosen driver) is PENDING, and no gap names it. Its candidate output is the 0598 B0 record `c2cec35b`, built from `driver_r5/out/B0_R5_RUN_V001` (64 counted, 16 no-evidence). The 0598 report's observation 5 says the same.

**Reproduction.** `sed -n '13p' $A/v007_final_prereg_c4/r4/SEAL_CHECKLIST_R4.md`; `sed -n '97p;178p' $A/seal_records_c4/build/BUILD_RECORDS_C4V001.md`

**Fix.** Root records A6 as done on r5, or names what is missing. The record is already registered in C3V007 (20:05:00Z); root pins the registry under GAP-13.

### R-10 (NOTE, FORMAL). Missing check: two copies of the key-equivalence map

**Claim.**
- `validate_case_block` reads the case block's own `key_equivalence_map` (r11 L1546–1560). The on-disk draft carries one entry, `/numerics/route_a/seed_source_rtol_factor`.
- The SEAL_RECORD carries a separate key map (SRR[3], A48 AMB-13).
- No tool checks that the two agree.

**Reproduction.** `sed -n '1546,1560p' $A/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py`; `sed -n '44,54p' $ST/build_seal_record_c4v001.py`

**Fix.** The GAP-03 and GAP-17 owners build the key map once. The builder successor (R-04) requires it to equal the case block's.

### R-11 (NOTE, FORMAL). Owner refinements

- **GAP-09.** A87 already directs the new BUILD: "add them to the launch-packet allowlist as a new BUILD (V006). Claude4 delta-checks it". What remains for root is to accept V006 after the 0602 item 1 delta check (`review_launch_packet_v006_c4/`, in progress). The prereg text, tool 3 and B8 then follow, through R-02 and R-03.
- **GAP-14.** "Root launches the runs" is too coarse:
  - B0_N3 needs a static guard scan of the r5 sources, not a launch. Claude3's C3V007 note puts that scan with root or Codex1.
  - B0_RO1 (b) and (c) are replays on saved state, which root can authorize to the A87 owner, as 0599 did for SR_K. Whether a lane can run them depends on where the C6 checkpoint lives, because the fence blocks the runs_ext roots.
  - B0_RO1 (a) needs a UVT_* read, and I4 needs a production run. Only those two are root's.
- **GAP-03.** Claude3 has built a valid V007 case block in-process twice (`final_specs_case_block_c3v001.py` for r8; `validate_registry_r11_c3v001.py` for r11, which VALIDATE_R11_C3V004 reports as `case_block_refusals` []). That makes Claude3 an alternative to Codex1 as owner.
- **GAP-12.** A70 designates `certificates_ngc_k32` as the NGC EPS slot ("EPS to 91 passed Codex1's admission test"). Root confirms the file.

**Reproduction.** `sed -n '1016,1022p;725p' $R/out/V005_ADDENDUM_READ_COPY_C4R.md`; `sed -n '152p;158p' $A/seal_records_c4/build/BUILD_RECORDS_C4V001.md`

### R-12 (NOTE, TESTED). The state moved after the rehearsal; a re-run on r5 and r12 is due

**Claim.**
- **A94 and 0612 (19:40Z).** B2 follows R1/V002 exactly, with le3 for every case.
- **A95 (19:46Z).** `taskpolicy -b` is preferred, not required.
- **A96 (19:51Z).** V007 seals on r5; r6 is deferred and RI-24 is moot. r12 cx3v002 `4bd7b262` is frozen, and its delta reviews of record are Claude3's and Codex2's.
- **0614 and 0615 (19:51–19:52Z).** The rehearsal assumes r5 and r12; no cache slot.
- **C3V006 (19:57:08Z) and C3V007 (20:05:00Z).** B2 is registered with verdict FAIL (R-15). The 0598 records B3 `83c853b9`, B0 `c2cec35b`, B0prime_DRY `7842d2a7` and B0_FA `888488cd` are registered.
- **r12 still has both hazards.** It still hashes the open V005 path (L171, so N-13 applies) and still reads the case block only from `binding_inputs` (L5706, so GAP-03 applies).

**Reproduction.** `sed -n '890,915p' $R/out/V005_ADDENDUM_READ_COPY_2_C4R.md`; `cat $A/v007_compare_c2/r12/SELECTED_R12_CX3V001.json`; `awk 'NR==171 || NR==5706' $A/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py`

**Fix.** Re-run the rehearsal on r12 `4bd7b262` with the newest registry (C3V007 or later), under the same fence and with no `--validity-only`. Close GAP-19, and update GAP-06, GAP-13, GAP-15 and GAP-20.

### R-13 (NOTE, TESTED). D-01: follow A73, and reword the r4 rule

**Claim.**
- The r4 certificate rule says "every record states source_gas_M_s where it depends on M_s", and tool 3 cites A68.
- The merged DOUBLING record has no `source_gas_M_s`. Its only M_s key is `ddo_gas_M_s` = 128, the field A73 fixed for the merged format ("ddo_gas_M_s 128").
- So D-01 is a real tool defect (r11 reads the record PASS), and the r4 wording is too literal.

**Reproduction.**
1. `cd $R && taskpolicy -b $PY -I -B $R/tools/run_fenced_c4r.py $R/tools/probe_doubling_c4r.py`, output `2a7c2669`.
2. `$PY -I -B -c "import json; print(json.load(open('$R4'))['seal_slots']['certificates']['rule'][:200])"`
3. `sed -n '817p' $R/out/V005_ADDENDUM_READ_COPY_C4R.md`

**Fix.** The tool 3 successor reads `ddo_gas_M_s` as the DDO M_s. Prereg r5, or the SEAL_RECORD note, states that DOUBLING carries its M_s as `ddo_gas_M_s` (A73).

### R-14 (NOTE, TESTED). One file was created outside the folder, by the harness

**Claim.** When call #67 was backgrounded, the Claude Code harness created `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/tasks/b78dxm9ej.output` (last written 19:05:01Z).
- It holds file names only, none in a forbidden class.
- It is not a program location and not a seal location.
- Nothing else the rehearsal wrote lies outside `seal_rehearsal_c4/run/`.

**Reproduction.** `TZ=UTC stat -f '%Sm %N' -t '%Y-%m-%dT%H:%M:%SZ' /private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/tasks/b78dxm9ej.output`

### R-15 (BLOCKING, TESTED). New since the rehearsal: the B2 record of record FAILs

**Claim.**
- `gate_b2_c3/out/B2_GATE_RECORD_C3V002.json` (`d4b41ffc`, born 19:51:09Z) reads gate B2, verdict FAIL, with 10 `root_items`.
- Claude3 registered it as the B2 record in C3V006 and C3V007 (producer `b2_record_c3v002.py`). The C3V006 note states the FAIL under A94.
- B2 is a required gate before any T result. Under r4 `$.outcomes_first_applicable[0]`, a B2 failure is an IMPLEMENTATION_DEFECT of the gate, and ADOPT_TAIL needs B2 to pass.
- So sealing and launching as planned would end in that outcome. A94 and 0612 require the result to be reported as it is, never adjusted to pass.
- GAP-15 therefore moves from "PENDING" to a refusing record.

**Reproduction.** I printed only these fields, never the row values.
1. `$PY -I -B -c "import json; r=json.load(open('$A/gate_b2_c3/out/B2_GATE_RECORD_C3V002.json')); print(r['gate'], r['verdict'], len(r['root_items']))"`
2. `$PY -I -B -c "import json; print(json.load(open('$A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V007.json'))['gate_records']['B2'])"`

**Fix.**
- Claude2 rules on the B2 FAIL and its 10 ROOT_ITEMS before B4: either a fix of the gate or its inputs under A94, or an explicit ruling.
- Claude3 is the B2 author. Codex2's B2 cross-lineage review (0610, 0617) is due.

## 5. Verdicts on the rehearsal's findings

| id | verdict | note |
|---|---|---|
| D-01 BLOCKING | CONFIRMED (TESTED here, fenced) | wording: R-13 |
| D-02 BLOCKING | CONFIRMED (TESTED: allowlists 13 and 15) | owner: R-11. Fold into prereg r5 (R-03) |
| D-03 BLOCKING | CONFIRMED; the fix is corrected | the seal-slot route fails; r5 plus a tool 3 successor are needed (R-03, TESTED) |
| D-04 SHOULD_FIX | CONFIRMED (FORMAL) | R-04 adds the builder's E-SEAL1 and B7 checks |
| D-05 SHOULD_FIX | CONFIRMED and strengthened | builder L85 writes a fixed note; A83, A91, A92 and A96 are also needed (R-02) |
| D-06 SHOULD_FIX | PARTLY REFUTED | A1, A5 and A10 exist; only the driver BUILD record step and the JSON form are missing (R-06) |
| D-07 NOTE | CONFIRMED (TESTED by capture T2_P1: rc 1, TypeError at tool 2 L22) | none |
| D-08 NOTE | CONFIRMED (TESTED by captures: B_A 9 codes, B_B 10) | none |
| D-09 NOTE | CONFIRMED (TESTED: 30 PENDING strings outside slot values; status "FINAL DRAFT r4 (NOT SEALED)") | none |
| D-10 NOTE | CONFIRMED (FORMAL: tool 1 L58 checks the name suffix only; tool 3 L207 compares `--frozen` with the slot, never with `path_to_be`) | none |
| D-11 NOTE | CONFIRMED in substance; label FORMAL | R-07 |
| D-12 NOTE | CONFIRMED (TESTED: RUNBOOK_V007 `648cfd74` line 15 "remains13 sources") | none |
| N-13 NOTE | CONFIRMED and continuing | the open file reached `991cc242` at 19:57:12Z; r12 cites the open path too (R-12) |
| N-14 NOTE | UNDERSTATED | R-05 |

## 6. Process audit (the two checks 0602 asked for)

- **Method.** `tools/audit_transcript_c4r.py` prints only `tool_use` inputs, plus refusal notices of at most 300 characters. It found 121 calls (83 Bash, 37 Read, 1 StructuredOutput), 8 errors and 4 permission refusals: the kill, the UVT name listing, the RV1 fence run and one `sed` read. Extract: `out/REHEARSAL_TRANSCRIPT_COMMANDS_C4R.txt`.
- **`--validity-only`: never ran.** The only compare invocations are G1, G2 and G3, each with `--gates-only`. The builder runs pass `--validity-only-output` with a path that does not exist; that is a builder flag, and the file was never created. No `*VALIDITY*` output exists in `run/out/`. TESTED.
- **UVT_* and C5H.**
  - G1, G2 and G3 each end with `FENCE_C4_SUMMARY` fence `f813c430`, review_root `run/`, blocked []. TESTED.
  - Before refusing, they read only the outdir stat, the prereg, the driver-build custody files, CHECK.md and the case block. G3 also read the tail library, the V005 and V006R1 preregs and the C5H call spec and dry run under `c5h_hull_c2/`.
  - The C5H run stat (`_registered_run_identities`, L1931) is reached only from `c5h_path_hit`, `c5h_interlock` and `registered_identity_code`. Those run only in test-mode full mode or under `interlock_side_paths`, not in `--gates-only`. FORMAL.
  - The fence would not have logged a stat in any case, because stat raises no audit event.
  - The unfenced Python runs (tools 1–4, the probe and the input builder) opened only files under claude_artifacts and the CLAUDE2 addenda. None has a path component starting `UVT_`. The RO1 custody files start with `ddo_`. FORMAL, from their paths.
  - The exception is the broad grep (R-05).
- **Nothing outside `seal_rehearsal_c4/`.**
  - Every write target in the 121 calls lies under `run/`. TESTED.
  - In the 13 folders the rehearsal read, the only files born or modified during its window (18:52:30Z–19:37:45Z) belong to other lanes: Claude3's registry V004/V005, Codex1's `gates_v007/r2` (born 18:56:57Z), and the 0598 build. TESTED.
  - The CLAUDE2 control folder has no FROZEN, SEAL_RECORD or ADMISSION file. No `__pycache__` was created. TESTED.
  - `run/HASHES.txt`: 118 of 119 shas verify from bytes. The one mismatch is the open V005 addendum, which root keeps writing. TESTED.
  - The one file outside is the harness capture (R-14).

## 7. This helper's own process

- **Reads.**
  - Rulings came from my two exclusive byte copies. The rehearsal transcript was read for commands only.
  - Names were searched with `find`, pruning the UVT_*, C5H, target-word and `runs_ext` names.
  - Content was read only from named files outside those classes. From the B2 record I read only `gate`, `verdict` and the number of `root_items`. I opened no runs_ext path and no UVT_* path, and I stat'ed nothing in the C5H run.
- **Runs.**
  - Tool 3, the DOUBLING probe and the test-input builder ran under the exact fence copy `tools/fence_c4v001.py` (`f813c430`). The wrapper `tools/run_fenced_c4r.py` refuses unless the fence sha matches and its selftest gives 8/8. BLOCKED was empty every time.
  - I ran no compare and no launcher.
- **Writes.** Only under `refute/`, each by exclusive create, except appends to my own PARTIAL.md.
- **One harness file outside.** The harness saved one oversized command output of mine, the name-search listing (names only), under the lane's Claude config folder (`tool-results/brkuyaojw.txt`). The same list is in `out/NAME_SEARCH_SEAL_INPUTS_C4R.txt`.

## 8. Files

- `REFUTE.md` (this file), `PARTIAL.md`, `HASHES_REFUTE_C4R.txt`.
- `tools/`:
  - `fence_c4v001.py` (exact copy);
  - `run_fenced_c4r.py`, `xwrite_c4r.py`, `audit_transcript_c4r.py`;
  - `probe_doubling_c4r.py`, `make_cb_test_c4r.py`;
  - `make_refute_c4r.py`, its patches `patch_refute_v2_c4r.py` to `patch_refute_v4_c4r.py`, and their outputs `make_refute_c4r_v2.py` to `make_refute_c4r_v4.py`. v4 wrote this file.
- `out/`:
  - `REHEARSAL_TRANSCRIPT_COMMANDS_C4R.txt`, `NAME_SEARCH_SEAL_INPUTS_C4R.txt`;
  - `V005_ADDENDUM_READ_COPY_C4R.md`, `V005_ADDENDUM_READ_COPY_2_C4R.md`;
  - `PROBE_DOUBLING_C4R.*`, `test_cb/` (inputs and the T3_CTRL and T3_CB captures), and the dry runs `REFUTE_DRYRUN_C4R.txt`, `REFUTE_DRYRUN_V3_C4R.txt` and `REFUTE_DRYRUN_V4_C4R.txt`.
