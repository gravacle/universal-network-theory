# ROOT DECISIONS: NGC3198 construction, V006 addendum (opened 2026-10-18 23:56Z)

V005 closed with A106. Its final bytes are sha256 c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1, 143,081 bytes. This addendum holds every later root ruling (A82, A106.3). Entries continue the A-numbering.

## A107: seal-script rulings (Claude3 0095 P12; Codex1 0101/0102) (2026-10-18 23:56Z, before any T result)

1. **P12: option (b).** **EPS_NGC** (EPS_CERT_NGC91_V001, 1d5eef1b) and **I1T_NGC** (I1T_NGC_T120L_V001, 3ae7981a) are **excluded by name from C-04**, the check that every slot loads through r13's registry.
   - They are step-5 NGC certificates that the seal carries; the V007 compare never evaluates them.
   - Their custody is the slot sha pin plus tool 2's NGC M_s check.
   - C-04 applies to every other slot.
   - **There is no registry V010.** Putting 1d5eef1b under gate EPS would widen the DDO EPS gate's admissible set, which is the reason Claude3 gives against it.
2. **C02 corrections (Codex1 0101), required before C-02 closes.** Claude3 fixes these in **c3v005**:
   - **C02-SEL-ASSOCIATION:** require the SELECTED schema's complete, exact association of stored path and hash. Unrelated strings and suffixed paths refuse.
   - Codex1's second C02 item, and the local C03 should-fix, exactly as Codex1 0101 states them.

   Codex1 delta-checks c3v005.
3. **Prereg r6 (Codex1 0105): provisional cross-check PASS,** 33/33, with 0 content blockers. Claude4 publishes the r6 SELECTED file after its refuter's verdict, and Codex1 confirms the selected bytes.
4. **C-08** stays a root manual check, following Claude3's README. The seal record states the id/file/line table and the manual confirmation.

## A108: proceed from seal to the step-2 launch without waiting on the principal (2026-10-19 00:00Z)

**Principal, in Claude2's chat:** "Can you proceed to Step 2 once Step 1 is complete without requiring anything from me?"

**Root proceeds on its own** under the standing directive, in this order:
1. When Codex1's final deltas on r6, v003 and c3v005 each report 0 blocking, root runs the selected ROOT_SEAL_STEPS script. This covers the freeze, binder, sealed prereg and compare, tools 1 to 4, gates-only, validity-only C5H (booleans only), and the SEAL_RECORD, config and receipt.
2. Root performs the C-08 manual check.
3. Root launches step 2 under the RUNBOOK_V008 / BUILD_V007 bound command: core priority, internal-SSD outputs, caffeinate tied to the launcher, and the disk watchdog. It then runs SR_K as the first post-seal step (A88).

**Any refusal stops the script.** Root rules and commissions the fix with no principal input. The principal is alerted only for a lane stall, which needs a nudge, or once step 2 has launched.

There are no automatic retries of scientific runs.

## A109: a stalled lane's work is reassigned automatically (principal, 2026-10-19 ~00:10Z)

**Principal:** "if a lane does stall remove the work from that lane and reassign it … I may not be there to poke them so you will have to assume that they have stalled and remove their work."

**Stall test.** A lane is stalled if either holds:
- a dispatch addressed to it has gone **10 minutes** without an acknowledgement; or
- an object it must build or review has existed for **15 minutes** with no write from that lane.

**What happens.** Root moves the work at once, with a reassignment dispatch, and does not wait for a nudge:

| Stalled lane | Its builds go to | Its reviews go to |
|---|---|---|
| Claude3 | Claude4 | Claude4, or Codex1 if Claude4 built the object |
| Claude4 | Claude3 | Claude3, or Codex1 if Claude3 built the object |
| Codex1 | — | the Claude lane that did **not** build the object; Codex3 (reserve) for small reviews |
| Two lanes stall | root runs the work itself as a workflow | root runs the work itself as a workflow |

A lane that recovers resumes only the work it still holds. Reassigned work is not handed back.

## A110: manual disclosures are bound into the SEAL_RECORD (Codex1 0114) (2026-10-19 01:22Z)

**The finding.** Script016 (c3v007) moved the E_R6_1 erratum and the C-08 table out to a separate publication packet. Prereg r6 and A107.4 require both **in the SEAL_RECORD**, and tool 4 has no input for manual disclosures, so the gap is real.

**Ruling: route 2, a reviewed and exclusive finalization.** The companion-only route is rejected, because a separate file is not bound by the seal chain.
1. **Claude4 builds seal tool 4 v004.**
   - It adds one input, `--manual-disclosures <path> --manual-disclosures-sha256 <hex>`. That is a byte-pinned JSON with a strict schema, and a duplicate key refuses (A71).
   - Tool 4 embeds the JSON **verbatim** in the SEAL_RECORD's disclosure block, alongside the derived prereg disclosures.
   - Nothing else changes.
2. **Claude3 wires it in as c3v008.** The disclosures file is pinned in step 0 and passed to tool 4. The config and receipt bind the SEAL_RECORD that contains it.
3. **Root authors `SEAL_MANUAL_DISCLOSURES_V001.json`.** It holds:
   - the exact E_R6_1 text from r6;
   - the C-08 id/file/line table and root's manual confirmation;
   - the A100 B2 disclosure (raw misses, gas-rule attribution, both readings, ADV C3 on le4);
   - the A101 B2 documentation erratum;
   - A105's E-OPS5 (the C5H `du` metadata access);
   - any other prereg disclosure that r6 lists as manual.
4. **Codex1** delta-checks tool 4 v004 and c3v008. **Claude3** cross-checks root's disclosures JSON against r6.

## A111: P3 and P4; C-08 done (2026-10-19 01:30Z)

**P3 (RI-36), the driver check record.** The record of record is **`driver_r5/check/CHECK.md` (89a6de88)**. The compare accepts it as a BUILD check record, which Claude3 TESTED on r11. Codex3's cross-lineage R5_REVIEW_FINAL (6758bd24) is cited as supporting evidence.

**P4 (GAP-12), the NGC certificate slots.** EPS_NGC is **1d5eef1b** and I1T_NGC is **3ae7981a**. Both are excluded from C-04 (A107).

**C-08 was checked by hand by root.**
- The r13 compare source (f5adfd11) carries 19 earlier-round tags: NEW-4, 7, 13, 16, 17, 19, 21, 30, 31, 34, 39, 44, 52, 53, 54, 60, 64, 71 and 73.
- The r13 IMPL of record (274f7049) declares **0** NEW items.
- The table, with file and first line for each tag, is in `seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json`, together with E_R6_1 and the A100, A101, A105, A107 and A111 disclosures.

## A112: seal tool 4 v004 SELECTED; the disclosures file V002 (2026-10-19 02:45Z)

**Tool 4 v004 is SELECTED:** SELECTED_SEAL_TOOLS_V004_C4V001, **593c59fa**, with tool 4 at 9787cf58. Claude4's refuter passed with 0 blocking and 0 should-fix, and the suite gives 467/467. Tools 1, 2, 3 and 5 carry their v003 bytes unchanged.

**R-05 / requirement 13 is ruled option (b).** Root published **SEAL_MANUAL_DISCLOSURES_V002.json**, sha256 **a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3**, 6,286 bytes.
- It is V001 plus one row, `A106_2_SRR13_CHECK_SPLIT`:
  - C-02 to C-06 are checked by the seal script;
  - C-07 (D-05) is enforced by seal tools v004;
  - C-08 is checked by hand by root.
- The script is named by its role, not by sha, which avoids a pin cycle.
- V001 (b9db6fd1) is superseded and kept.

**R-02.** Claude3's c3v009 runs the verbatim disclosure check on the written SEAL_RECORD before step 12:
- `raw_text` equals the V002 file's bytes;
- the pin equals the V002 path and sha;
- `e_r6_1_text` equals r6's `basis.erratum_E_R6_1`.

## A113: the open ROOT_ITEMS_R6 rulings, and the missing gate records (2026-10-19 03:25Z, before any T result)

The seal script's root inputs (P5 to P10) exposed root items in ROOT_ITEMS_R6 that were never ruled. They are ruled here.

| Item | Ruling |
|---|---|
| **RI-30** | **Adopted.** There is one key-equivalence map of record: the SEAL_RECORD's map equals the case block's, `[]`. Root supplies `[]` as the B7 key map. |
| **RI-31** | **Run the production M_s 128 r5 = r4 dry-identity first** (A55 ruling 2: every spec). It is dry planning, so it is cheap. A6 is done when it reads PASS_PLAN_IDENTICAL on the c7023846 set, under the B0-EMPTY rule. **Owner: Claude4**, with Codex1's delta. |
| **RI-32** | **CASCADE_MAP_R5_ADDENDUM owner: Codex3** (reserve; it found the gap in 0602), with Codex1's delta. It is the immutable inventory addendum naming the unreachable pin-only successor (A69). |
| **RI-33** | **B0_N3 and B0_RO1 are built before the seal.** Neither depends on any T result. **Owner: Claude3**, with Codex1's delta. The registry successor V010 adds their records. B0_N3 is a static guard scan of driver r5. B0_RO1 (a) reads the identity-gate runs; (b) replays the C6 iteration-8 checkpoint; (c) tests exceptions. **I4: Claude3 reports first** what r13's I4 gate requires and whether its inputs are pre-seal. If I4 needs a V007 run output, it joins the after-seal set like SR_K (A88); that means a compare r14 (one line) plus delta reviews. |
| **RI-35** | **Accepted.** The SEAL_RECORD, not the prereg's status line, is the authority on sealed status. The manual disclosures state this. |
| **RI-36** | Ruled in A111 (CHECK.md 89a6de88). |
| **RI-37** | **Claude3's reading is confirmed.** The aggregator `aggregate_records` v008 (9794123d) is the only SR_K gate-record producer. `sr_k_static` v009 is under producer-side custody in the RUNBOOK. |

**P6 (the B7 inputs). Owner: Claude4,** assembling with root.
- The key map is `[]` (RI-30).
- The NEW-item disposition list (A81 RI-20) is compiled from each round's IMPL; the C-08 table is its id index.
- The raw successor-custody record (A59, A67 N1) is produced by c2v007r2's own tool from the R5_V001 identity runs. Root runs it, since it reads `UVT_*`.

**P5:** dispositions with `entries: []`, because r6's table runs through A106 and V005 is final. **P8:** the C5H directory spelling, read from r13's C5H_REGISTERED_RUN_DIRS. **P9:** the root acknowledgement, which is this entry. **P10:** a floor of 300 GiB (A105.3: about 250 GB expected).

## A114: I4 joins the after-seal set (Claude3 0118) (2026-10-19 03:35Z, before any T result)

**The finding** (r13 g_I4, L3741–3759, read from bytes).
- I4 is required, because the case block sets `route_a_mode: parallel8`.
- It needs a serial (N1) and a parallel (N8) C2T run, both under b5cc62af with the tail ON, compared bitwise outside the custody fields.
- No such pair exists under r5. The C2V008-era pair (e1d3c072) ran under a different driver.
- Prereg r6 (RI-33) already expects I4 "once the runs exist". **r13 contradicts this by refusing the after-seal token for I4.**

**Ruling (as A88 for SR_K).**
1. **Compare r14 = r13 plus `'I4'` added to GATE_RECORD_AFTER_SEAL_ALLOWED,** with tests for the token on I4: accepted for I4, still refused for B0–B3, EPS, GQ, LO, LO_NGC, DOUBLING and the identity gates. Nothing else changes.
   - **Builder: Codex1.**
   - **Reviews of record: Claude3 and Claude4,** each needing 0 blocking (A81 RI-20, as A103 applies it). Both are of a different lineage from the builder.
   - r14 replaces r13 in the compare slot. Prereg r6's slot rule ("the round whose reviews of record report 0 blocking") covers it, and the seal record names r14 with this entry.
2. **The I4 producer is registered in V010** (Claude3, option (b)), with PRODUCED_AFTER_THE_SEAL. It compares the C2T N1 and N8 run trees under b5cc62af's custody list and writes the FIELDS record that g_I4 reads.
3. **The I4 run pair.**
   - **N8** is the V007 C2T T-run itself.
   - **N1** is a companion that **root launches after the seal**, as the identity runs were launched: through root_monitor with the driver, under b5cc62af, tail ON. Its spec is C2T's spec with `route_a.column_workers 1` and is identical in every other field. Claude3 drafts that spec, and root pins it.
   - The N1 spec sha is pinned in V010's I4 entry before the seal.
   - It runs in parallel with step 2. Being serial, it may take longer than the C2T N8 run.
4. **Disclosure:** this entry and r14 are named in the seal record's manual disclosures, V003.

## A115: the threat model is honest producers, and the physics comes first (principal, 2026-10-19 ~03:30Z)

**Principal:** "Are we sure that the reviewer isn't getting bogged down in process machinery instead of the physics? I've seen that before." This repeats the 2026-10-15 directive "stop building custody machinery".

**Root's assessment.** Yes. Most of the 10-18/19 review findings concerned forged or malformed inputs: duplicate JSON keys, NPZ aliases, 4,300-digit integers, firmlink symlinks, stale `.pyc` files, argparse echo. The program's own pinned producers cannot emit any of these. Fixing them did not change, and could not have changed, any V007 physics reading.

**Ruling. This is the blocking criterion from now on, for every review lane.**
- **A finding is BLOCKING only if** (a) it is reachable from the program's honest, pinned producers acting on the real records, **or** (b) it could change a physics reading: a T-test value, a decision branch, a gate verdict on genuine records, a numerical certificate, or the blinding of C5H.
- **Everything else is a NOTE** for a later version: forged or malformed inputs, adversarial path spellings, parser corner cases that no pinned producer emits, and robustness of the seal tooling against tampering. Notes never block a seal or a launch.
- **The remaining seal reviews** (r14, V010 and the B0_N3/B0_RO1/I4 records, the B7 inputs, the cascade addendum) are scoped this way.
- **During step 2, lane effort goes to the physics:**
  - the meaning of each possible V007 outcome;
  - the step-4/5 calibration and prediction science;
  - the NGC readings;
  - the miss-reading semantics.

## A116: r14 enters the compare slot; the r6 wording is carried as an erratum, with no prereg r7 (2026-10-19 03:58Z)

**Reviews of r14:**
- Claude3 0124: PASS_WITH_FINDINGS, 0 blocking under A115 ((a) 0, (b) 0, 7 notes).
- Claude4's review is pending. **Both must read 0 blocking** (A114).

**Ruling:**
1. **The compare slot value is r14:** `kmax_tail_compare_c2v007_r14_cx1v001.py` **f3f9ba7e**, SELECTED_R14_CX1V002 **6b650ece**, IMPL_R14_CX1V002 **2ba6d12e**. r13 (f5adfd11) is superseded.
2. **No prereg r7.** r6's `seal_slots.compare.rule` names r13 as the final round, and its `producer_registry.rule` says "the … I4 records once built". Both are now outdated. **This is a documentation erratum that changes no physics reading** (A115; precedents E_R6_1 and A101). It is carried in the seal record as **erratum E_R6_2** in disclosures V003:
   - under A114 and A116 the compare of record is r14 (r13 plus `'I4'` in the after-seal set);
   - I4 is an after-seal gate, with its producer registered in V010;
   - r6's own slot rule ("the round whose reviews of record report 0 blocking") selects r14.
3. **C-08 carries over to IMPL r14.** Root re-read the NEW tags from r14's source bytes: the same 19 ids, and IMPL r14 declares none. This is already in the draft V003's c08_confirmation.
4. **Claude3 builds c3v010** against r14, V010 and disclosures V003. **Claude4 confirms** that seal tools v004 need no change for r14. Its 0129 found no hardcoded r13 sha; it should also confirm that tool 3 does not check the compare slot value against the rule text.
5. **N2 (Claude3).** V010 is validated on r14, and `producers.I4` carries the I4 producer pin.

## A117: r14 is the compare of record; the N1 spec pin moves (2026-10-19 04:05Z)

**Both r14 reviews of record read 0 blocking under A115:** Claude3 0124 and Claude4 0134. **Compare r14 is the compare of record:** f3f9ba7e, SELECTED_R14_CX1V002 6b650ece. Seal tools v004 accept it with only the slot value changed (Claude4 0133).

**The N1 spec pin (Claude4 S2, class (a) for V010).** Registry schema C2V003 has no field for the C2T N1 spec sha. **It is therefore pinned in disclosures V003**, in the A114 row, which puts it in the SEAL_RECORD. V010 carries only the I4 producer pin, with PRODUCED_AFTER_THE_SEAL. This corrects A114.3. At launch, root verifies the N1 spec from bytes against the V003 pin.

## A118: NEW-30 and NEW-44 ruled; the B7 custody source (Claude4 0135) (2026-10-19 04:10Z, before any T result)

- **NEW-30: ADOPTED.** It is reporting only: a NO_RUN reading still reports the failing EPS and T2I gates with their next steps. It cannot change a reading (A115).
- **NEW-44: ADOPTED as implemented. RB_FP is not an envelope consumer; it reads `eps_max`.** This is a physics ruling (A115 (b)):
  - The EPS V006 envelope ε is about 1.277× `eps_max` (8.20e-4 against 6.42e-4 at (2,3]).
  - RB_FP uses ε as an allowance, so the smaller `eps_max` can only turn passes into fails, never the reverse. That is the conservative direction for an adoption test.
  - r14 stays as reviewed.
- **The NEW-item list.** Claude4 completes `NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json` with the generator, using `--require-complete` and citing A118 for NEW-30 and NEW-44. It covers all 19 ids, and compare_impl is IMPL_R14_CX1V002 (2ba6d12e). Claude3 checks it.
- **Successor custody: Option A.** Root converts c2v007r2's Z2 report of record, `out/IDENTITY_C2V007_R5_V001/Z2.json` (ac793faf), using Claude4's converter (1b097cba). No run is touched, and C5H is not accessed (A105). Option B would make the guard stat the C5H directory, so it is rejected.

## A119: the I4 producer is c3v002; registry V011; disclosures V004 (2026-10-19 04:42Z)

**Claude4 0142, BLOCKING class (a), accepted.** I4 producer c3v001 (4d6263f6) refused any run path that contained a symlink, so it would have refused the honest I4 runs.

- **c3v002 (2a315da2)** walks the path component by component. It allows symlinked ancestors and still refuses symlinks inside the run trees.
- **Registry V011:** **512a7171**. It is V010 with only `producers.I4` changed, which root verified from bytes.
- **Disclosures V004:** **adac5030**. It is V003 with only the A114 row's producer and registry names changed.
- c3v010 pins V011 and V004. Claude4's delta covers c3v002 and V011.

**The custody record of record is RAW_SUCCESSOR_CUSTODY_Z2_R5_V001, 9ca16b4f.** Root produced it with converter v002 (f7d78bce), Option A.

## A120: erratum to A118's NEW-44 rationale. The direction was stated backwards; the ruling is unchanged (Claude3 0140, class (b)) (2026-10-19 04:50Z, before any T result)

**The error (root's).** A118 said RB_FP uses ε as an allowance, so the smaller `eps_max` is the conservative direction. **That is backwards.**
- In r14 (L4113, L4174–4177), RB-FP_i = 2·ε·|dv_i/dλ|·κ_i ≤ τ_i/10. ε scales the bias bound, so a **larger ε is stricter**.
- EPS V006: the global `eps_max` is 6.4230e-4 and the global envelope is 8.2025e-4, so globally `eps_max` is the looser value.

**The ruling stands on the correct basis: NEW-44 is ADOPTED as implemented, RB_FP reads `eps_max`, and r14 is unchanged.**
- RB_FP reads `eps_max` as preregistered (A52.5: converged; the dense audit gives 6.41976e-4).
- Both global maxima lie in shell (2,3], which is below K = 4 and outside RB_FP's shell domain [4, √2·128]. The pinned `shell_split_static` drops shells with hi ≤ K.
- **Over RB_FP's own 178 shells the envelope sup is 2.05e-4, at (4,5], so `eps_max` is 3.13× more conservative than the envelope where RB_FP reads.**
- The only rows a global-envelope reading could change are those with 3.05 τ < (|dv|+E)·κ ≤ 3.89 τ. No T-test value, nor the EPS or SRB_ROT gate, nor the C5H blinding, reads ε.

**The record (route A, the fastest).** Disclosures **V005** = V004 with:
- the A113_ROOT_ITEMS_R6 row's NEW-44 phrase corrected;
- an erratum row **E_A118_1**, carrying this text.

The COMPLETE NEW-item file (68164144) keeps its quoted A118 sentence, and E_A118_1 in the SEAL_RECORD governs it (precedent A101).

**Also noted (Claude3 0140; no change required):**
- A118's Option-B wording should read "the guard lists runs_ext, reaching C5H metadata", not "stats C5H";
- A59's "all 21 stages" should be 16 successor-kind stages.

## A121: the I4 producer c3v003 rulings; the root seal inputs P7, P8 and P9 (2026-10-19 05:00Z)

**I4 producer c3v003** (Claude3 0142, Claude4 0147). These fix false FAILs reachable on an honest pair; c3v002 is superseded.
- **D1, class (b):** RO1 firing identically on both sides must not FAIL I4. RO1 firing in a T-run is recorded, not an invalidity. The check C6 is made per side (RO1 rule, armed, key set, worker and binding shas). `fired` and `events` are left to the bitwise result comparison, so a **one-sided** firing still FAILs.
- **D2, class (a):** the other run's root matches only on a path boundary.
- **D3 (H4), class (a):** stdout and stderr compare as **sets of distinct lines**. Counts may differ, but a line on one side only FAILs.
- H1 closes the open sidecar risk: honest tail-ON sidecars PASS under declared classes.
- The chain is: c3v003 and its verifier, then registry V012 (only the I4 producer pin changes), then root's disclosures V006, then c3v010.

**Root inputs:**
- **P9:** the ack string is `RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12`. Every item is ruled.
- **P8:** the C5H directory is the External1 spelling, which has no symlinked ancestor.
- **P7:** the cascade addendum is 86c89730.
- **Run placement:** the I4 runs go under `/Users/bgm/Research/UNT_INTERNAL_RUNS/…`, with no `UVT_*` names and no symlinked ancestor.

## A122: step-4 start blockers get builders during step 2; the I4 N1 companion caps (2026-10-19 06:36Z, before the seal)

**Step-4 start blockers** (Claude4 ROOT_ITEMS_STEP45_V002 `417de6fe`; Claude3 0147). Root adopts the file's recommendations on builders:
- **S4-R-C1, the per-point certificate registry.** Claude3 builds the LO producer successor and the registry tooling, for **31 points**. Codex1 reviews (cross-lineage). CP-1 runs in **window (b)**: during step 2, background QoS, with root's memory attestation (free ≥ 25 %), never holding back a T-case. The first bundle is timed end to end.
- **S4-R-B4a, the one-call PRELAUNCH tool: option (a).** Codex1 builds it; it calls guard007's `native_preflight` unchanged. Codex1 also builds the G7-SCOPE-1 inventory (S4-R-B6), covering the tool and the disk guard (S4-R-D17). Claude3 reviews.
- **B1/R-A2:** a policy successor that reads the bare-sha `PIN_ADDENDUM_V005`. Claude4 builds it after its c3v010 delta; Codex1 reviews. It touches no sealed object.
- **Priority:** a blocking c3v010 finding preempts all of these. Lane work runs at background QoS from the step-2 launch (A85.2, with the A95 waiver).
- The root rulings D1, D2, D5, D8, D9, D11 and D17 come in a later entry, before T0.

**I4 N1 caps.**
- RSS and output caps are C2T's plan caps: 22,548,578,304 B and 103,079,215,104 B. The wall cap is **345,600 s (96 h)**.
- `column_workers` does not touch the serial tail builds (TIMING_V003). N1 is therefore slower than C2T only on the non-tail column work: UNTESTED, plausibly 1.5–4× C2T. The cap is a safety bound, not a forecast.
- N1 runs at normal QoS. It starts right after the step-2 launch, since it is likely the longest single run.
- If N1 hits a cap, I4 reads MISSING and root rules (A50).

## A123: E-SEAL1 must carry the pre-seal B0_RO1 and B0_N3 records; c3v011 (Claude4 0154) (2026-10-19 06:42Z, before the seal)

**The finding (Claude4 0154; root confirmed from bytes).** BLOCKING, class (b), and class (a).
- The gates-only manifest pinned by c3v026 is `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` (`e5967bb9`). It dates from the registry-V009 era and still has `gates.B0_RO1 = null` and `gates.B0_N3 = null`.
- The dry run of record's E-SEAL1 accordingly reads **MISSING** for both gates.
- Their registered pre-seal records exist and pass: B0_RO1 `332452b7`, B0_N3 `dd1dd912` (V012; A113).
- Prereg r6 `seal_record_requirements[0]` puts the identity-gate records and the RO1 replay into E-SEAL1. Sealing c3v026 would irreversibly record a genuine PASS gate as MISSING.

**Ruling.** Adopt Claude4's fix:
1. a manifest successor that sets exactly those two gates to their record paths;
2. script c3v027, changing only that pin and any check keyed to the old manifest sha;
3. both dry runs re-run;
4. SELECTED c3v011.

**Done when:**
- in the dry-run E-SEAL1 gates-only output, every pre-seal gate registered in V012 reads PASS, and only the PRODUCED_AFTER_THE_SEAL gates (I4 among them) read MISSING;
- Claude3 and Claude4 report 0 blocking on c3v011.

**Root rehearsal of real-mode step 8 (06:41Z).**
- Run: helper c3v019 `gates-only --mode root`, using the dry run's sealed compare (`83fa73d7`) and sealed prereg (`5c00bb71`), on manifest `e5967bb9` with the real identity-run trees.
- Output: `V007_STEP2_LAUNCH_ROOT/STEP8_ROOT_REHEARSAL_V001/`, GATES_ONLY `4f374bdb`.
- Result: compare rc 0 and fence refused 0. 10,127 identity-tree entries were scanned, with no symlink. **Z2, Z2-OFF and B0prime_RERUN are all valid**, with no codes.
- Gate verdicts match the dry run: every pre-seal gate PASSes except B0_RO1 and B0_N3, which are MISSING (this finding). Only PRODUCED_AFTER_THE_SEAL gates are otherwise MISSING.
- No C5H access.
- The real step 8 has therefore been exercised on the real identity inputs. c3v011 needs only the manifest change.

**Register (lesson, a repeat of A113).** Walking the whole seal checklist was not enough. The dry run's E-SEAL1 *verdicts* had to be read against the registry. A PASS of the step does not show that each gate it records holds the right verdict.

## A124: S4-R-D17, the step-4 disk plan and the disk guard (Codex1 0129) (2026-10-19 06:43Z)

**Ruling: option (a).**
- **Placement.** The step-4 direct calls (HEADLINE11, DIII4, SENS_LO9, SENS_HI9) and S4-POST-S1 go to External1. They go under one fresh step-4 run root, `/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001`, with a distinct output directory per call.
  - The root is not under `runs_ext`. It has no `UVT_*` name and no symlinked ancestor.
  - Root creates it at T0, not before.
- **Step 2 stays on the internal SSD** (A85.3, A105.3).
- **Disk guard, failing closed** (Codex1 implements it in the 0616 packet's successors; Claude3 reviews it with G7-SCOPE-1):
  - at batch admission, the free space on the output volume must be at least the batch's call count × the output cap, plus 20 GiB;
  - before each start, it must be at least one output cap plus 20 GiB, checked in the launcher beside the memory gate.
- **Interim, until the guard lands:** root records a `df` reading of the output volume in each batch's admission record and does not admit a batch that fails the admission bound. An alert-only watchdog runs on the output volume at one output cap plus 20 GiB.
- **Retention (D3) is ruled before the campaign.** The typical model (3.25 TiB) exceeds External1's free space: 3,273 GiB measured at 06:42Z. The headline outputs are measured and the space re-projected first.

## A125: V007 is sealed, and step 2 is launched (2026-10-19 07:02Z)

**The seal.**
- **What ran:** SELECTED c3v011 (`d28d02b6`), script c3v027 (`239a51c3`), wrapper `V007_STEP2_LAUNCH_ROOT/run_seal_root_c2v002.sh`. It ran after the two zeros, Claude4 0156 and Claude3 0158.
- **Result:** ALL STEPS PASS, exit 0, at 07:00:44Z.
- **Shas:**

  | Object | sha |
  |---|---|
  | SEAL_RECORD | `a9646fe3aa5fbeb554090dcdd4f8ffbfd75ddac80e35e38d1bca4899551f98df` |
  | config | `e7110cde86a12efc31734f94e2a46a5f4b6dc7941fc1a6e4016d6859863f2c0b` |
  | receipt | `c9d0090f982cf18909f5b3f682f3f7d2837c459077438bfd5371dda6fd4d58f8` |
  | frozen V005 | `c01b3c51` |

- **Published:** root publication 0669 (`9a704b22`). Claude3 0159 verified it independently.
- **E-SEAL1:**
  - 15 of 15 pre-seal gates PASS;
  - the 10 after-seal gates read MISSING;
  - the identity runs are valid;
  - C5H `valid_all` true, read as booleans only.

**The step-2 launch**, by `launch_step2_root_c2v001.sh`; launch record `STEP2_LAUNCH_RECORD_V001.json` (`165a2af7`):
- **Before launch:** UNT_ROOT_ADMISSION_SHA256 was taken from 0669's published line. The config, seal and receipt matched the published values from bytes. The bound plan `2d0cf8f5` and command `fcc39bae` were re-verified immediately before running.
- **Output root:** `/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007` (dev 16777232, ino 15006242), still empty, on the Data volume, with 397 GiB free.
- **Processes:** the launcher worker started as pid 4255 at 07:01:24Z, with `caffeinate -i -w 4255` as pid 4258 and the disk watchdog as pid 3385.
- **First case:** C4T-KHI was admitted at 07:01:39Z with 86 % memory free.

**I4 N1** started at 07:01:45Z. Root monitor pid 5268, caffeinate pid 5380, record `f84c81d7`.

**SR_K (A88)** started at 07:02Z, at background QoS. Its record follows.

**SR_K done (07:41Z).**
- **Run:** `run_sr_k_root_c2v001.sh`, under `taskpolicy -b` and `nice` 10, with single-thread BLAS. It read no T output.
- **Records** are in `V007_POSTSEAL_RECORDS/SR_K/`:
  - component records: C2R3 `d3c598b8`, C3R3 `415f765e`, C4R3 `9c98cf38`;
  - **gate record `SR_K_GATE_RECORD_V001.json` `a1e2b76d6d61ae5026fe6dfe5f0e3d8bd0b17dd69dca487e041cf7aadf71b6d6`**: verdict REPLAYED, states C2R3/C3R3/C4R3, sealed compare `a99105a1`.
- **The A88 check passes:** the three Delta vectors (K = 2, 3, 4) are pairwise distinct, so there is no RECORD_DEFECT.
- The gate itself is read by the sealed compare at step 3.

## A126: B1/R-A2 placement and finalization (Claude4 0158; Codex1 0133) (2026-10-19 07:06Z)

- **Placement:** the sibling folder `calib_tail_readiness_cx2/v006r10_c4/`, which keeps the wrapper's relative loads unchanged. Nothing else is written in the cx2 tree.
- **Finalization happens once, after the V007 verdict.** The same generator reruns with the verdict tuple. Reviewers check the four small diffs: the policy constant, the core pin, the wrapper pin, and Codex1's guard/PRELAUNCH owner contract.
- Until then, `APPROVED_V007_SEALS` stays empty, so no step-4 call can adopt before the verdict.

## A127: C4T-KHI stopped on the RSS cap, a measurement artifact. Step 2 is relaunched as R2 with RSS caps at 128 GiB (2026-10-19 07:29Z)

**Facts (TESTED, from the receipt, the launcher log and vm readings).**
- **The stop.** C4T-KHI ended at 07:23:47Z (1,327 s) with `STOPPED_RSS_CAP`, exit -15. Its peak RSS was 47.29 GB against a cap of 47.24 GB. It had completed 311 of 576 columns of iteration 0, with no completed route-A iteration.
- **Launcher response.** As designed (RUNBOOK L12), the launcher classed this as systemic and finished, admitting nothing more. No T output was read.
- **The metric.** The monitor's RSS is the sum of `ps` RSS over the 11-process tree: the main process plus 8 column workers, among others.
  - It stayed at 2.4–3.9 GB for 21 min.
  - It then jumped from 3.6 to 44.3 GB in 6 s (1,290–1,296 s), which is about +4 GB in each of ~10 processes at once.
  - At the launcher's 1,322 s reading the tree sum was 46.8 GB, yet system memory was still **85 % free** (`memory_pressure`, the launcher's own admission metric). It read 86 % after KHI ended.
  - The jump is therefore shared or file-backed pages counted once per process, not physical memory. The cap fired on an artifact of the metric, not on memory pressure.
- **Not physics.** The specs, driver and numerics are unchanged, and nothing was read from any T output. KHI's partial outputs are preserved as they are.

**Ruling (A50: no automatic retry; root decides relaunch).** Relaunch all 10 cases as **R2** under the same seal, using bound plan `P128/LAUNCH_PLAN_V011_CX3V001_R2_BOUND_R5_V007_SEAL.json` (`44b55a7e`) and command `P128/LAUNCH_COMMAND_V011_CX3V001_R2_BOUND_R5_V007_SEAL.txt` (`6d10b23f`).
- **Generation.** `make_relaunch_r2_template_c2v001.py` builds the R2 template from the V011 template bytes (`1b406591`); the template is `6a0994c5`. The unchanged binder then binds it with the same driver (b5cc62af) and frozen V005 (c01b3c51).
- **Root leaf diff against the sealed V011 bound plan.** Only these change:
  - all 10 `rss_cap_bytes_proposed` → **137,438,953,472 (128 GiB, the machine's RAM)**, and the matching argv value;
  - outdir, receipt and monitor_log gain `_R2`;
  - the launcher log gains `_R2`;
  - template_pin.

  Order, specs, wall caps, output caps, admission rule, monitor, launcher and guard are all unchanged. The sealed compare reads no cap and no run-directory name; run names are registered nowhere.
- **Why 128 GiB.** A ps-sum cap cannot bound physical memory for forked multi-worker trees. Set at RAM, it still stops a runaway tree. Physical protection rests on the launcher's ≥ 25 % free admission gate, plus a root **memory watchdog** that alerts with sound below 20 % free (alert only; root decides).
- **I4 N1 restarts as `I4_COMPANION_C2T_N1_SERIAL_V002`,** with the same 128 GiB cap, because the same metric risk applies. The V001 run (started 07:01:45Z) is stopped by root and preserved. N1 is not a T-run, so nothing is read from it.
- **Review.** Distinct review is a delta of this relaunch packet by Claude4, with Codex1 as alternate, under A115 scope. Root launches on the first zero.
- **Register.** The caps (A61/0538) were set from modelled physical peaks, while the monitor measures a ps-sum. That metric mismatch was not caught before launch.

**Launched (07:31Z).**
- **Review:** Claude3 0162 (distinct; leaf diff from bytes; 0 blocking under A115). Root's own checks found that launcher v007 binds only the driver and frozen addendum to the seal, and that the sealed compare reads no cap and no run name. Claude4's delta (0160) is still running; a blocking result stops the R2 runs, and nothing is read from them before then.
- **I4 N1 V001 stopped:** root sent TERM to its process group at 07:30:57Z. Receipt: CHILD_FAILED, -15, peak 3.08 GB, preserved.
- **R2 launch:** `launch_step2_r2_root_c2v002.sh` at **07:31:06Z**. Launcher worker pid 24287, caffeinate pid 24290, record `ea957f22`. All 41 R2 paths were absent beforehand, with 393 GiB free. KHI R2 was admitted first.
- **I4 N1 V002:** started at 07:31:21Z. Monitor pid 24392, record `fd7df4f7`.
- **Memory watchdog:** pid 21121, alert-only. Claude3 0162's recommendation, to pause admissions below 15–20 % and stop the newest case below 10 %, is noted. Root watches live instead; any stop is a root act.
- **Delta verdicts:** Claude4 0161 and Codex1 0136 both report **0 blocking**.

## A128 (contingent): R3 with RSS caps of 1 TiB, if KHI R2's ps-sum artifact keeps growing (2026-10-19 07:36Z)

**Why.** Claude4 0161/0162: in V001, after the worker jump, the ps-sum rose at about 0.115 GB/s and was still rising at the stop. If that is linear, KHI R2 reaches 128 GiB at about 08:06Z.

**Root's diagnostic (read-only).** Every 15 s, root logs the run's process group:
- the ps-sum;
- the sum of top's MEM, the physical footprint;
- the system free %.

Log: `V007_STEP2_LAUNCH_ROOT/KHI_R2_FOOTPRINT_V001.csv` (sampler pid 35836).

**Ruling, contingent.** If after the worker jump the ps-sum climbs toward 128 GiB while the footprint and free % stay flat, root stops R2 (preserved, nothing read) and launches R3.
- **R3 packet:** plan `52d5872c`, command `3424ce8b`, generator `9e4819b9`, template `3950c4ea`.
- **What R3 changes:** RSS caps of 1 TiB and `_R3` names. Root's leaf diff: 73 leaves, all declared.
- **Pre-review:** 0673. One zero is enough.
- **With R3, the per-run RSS stop is effectively off.** The physical guards are:
  - the launcher's 25 % admission gate;
  - the alert-only watchdog plus root's hand stop of the newest case if free memory keeps falling;
  - the OS.
- **Otherwise R3 is not used.**

**Claude3 0166, a challenge to A127's diagnosis (07:46Z).**
- From code: the route-A workers are `spawn` processes that receive pickled private copies of TailState (about 0.81 GB). No mmap or shared memory is used.
- `memory_pressure` free % counts private anonymous pages as free.
- So KHI's ps-sum is probably **real** private memory, leveling off near 55–60 GB.
- The deciding test is root's footprint sampler at the worker jump (about 07:52Z): top's MEM is the physical footprint. If the challenge holds, A127's "artifact" reading is wrong and is corrected in A130.

**Register.** A metric that counts shared pages once per process cannot serve as a physical cap. A footprint-based monitor successor is the durable fix. It is not needed for V007 if R3 holds.

## A130: correction to A127. KHI's memory is real private memory. R3 is not used; root watches real memory (2026-10-19 07:56Z)

**TESTED: root's footprint sampler, `KHI_R2_FOOTPRINT_V001.csv`.**
- At KHI R2's worker start (07:53:01Z), the physical footprint (top MEM) was **40.70 GB** and the ps-sum 40.88 GB. They are equal, so **this is not shared-page over-counting.**
- The footprint then fell to 37.5, 22.1 and 14.9 GB, and sat at about **14–16 GB** by 07:54Z.
- So this is a **transient spike at the start of each iteration**, real private memory: the TailState (about 0.81 GB) and `prepared` are pickled to 8 spawned workers (solver 7667025b L884–1008). Claude3 0166 and Claude4 0165 found this from bytes.

**Corrections.**
- A127's "artifact" reading was wrong. Root inferred it from `memory_pressure`'s free %, which counts private anonymous memory as free (Claude3 0166 point 2, TESTED at 07:45Z).
- V001's stop at 47.29 GB was a **real** peak, caught by a cap derived from a tail-memory model about 7× too small.
- **The A127 R2 relaunch stands on its own merit:** a 128 GiB cap is above KHI's real spike, changes no computed value, and two reviewers found 0 blocking.

**R3 (A128) is not used.** Its packet stays on disk, unlaunched.

**Operational risk under the sealed launcher (Claude3 0166; Claude4 0161 NOTE 3 and 0165).** Up to 6 route-A cases can run concurrently, and coinciding per-iteration spikes could overcommit RAM. That would cost time through swap, or a jetsam kill that fails closed. It cannot produce a wrong value.

**What root watches.**
- `memory_watch_root_c2v002.sh` (alert only), log `STEP2_MEMORY_WATCH_V002.csv`. It records the per-run physical footprint, its total, swap and the compressor. It alerts when the total run footprint exceeds 95 GB or swap exceeds 8 GB.
- `memory_pressure` free % is no longer used as root's metric. The launcher's own gate keeps using it, because it is sealed.

**Lever.** If swap keeps climbing, root pauses (SIGSTOP) the newest case's process group, preserving it. Pausing changes no value, and a paused case before its first iteration also holds the ramp. Root resumes it (SIGCONT) when memory allows. Wall caps keep counting while paused, so root watches them.

## A129: R-A2 finalization is policy-only, through generator v002 (Claude4 0164) (2026-10-19 07:48Z)

This amends A126.
- Step-4 finalization happens once, after the verdict. Generator v002 `--policy-only` writes `v006r11_c4/adoption_policy_cx2v006r11_c4.py`, and root's admission names it as `adoption_policy`.
- The wrapper stays ef3d3d69, so guard009's owner contract is unchanged.
- Review is the two-line diff. Codex1 reviews generator v002.
- Step 5 comes later, through the same generator.

## A131: R1 fix accepted; R1G-A1 (the direct adapter refuses the registered spec's 3-key template pin) is fixed by a root-built adapter successor (2026-10-19 09:22Z)

- **The R1 fix is accepted:** guard010 `151e9484` and PRELAUNCH004 `427f5554`. Claude3's verdict of record (0169) is PASS, 0 blocking.
- **R1G-A1 (Claude3 0169).**
  - This is a pre-existing (a) BLOCKING item for H1. It is a refusal only, with no physics effect.
  - The production direct adapter `step4_direct_preflight_cx1v001.py` (`eee61ac6`) L20 passes the registered coordinate spec's template pin `{path, schema, sha256}` (spec `50e7288e`, template `a93c95b9`) to `G.doc`, which accepts only `{path, sha256}`. The result is PIN_REQUIRED for all 29 tail-ON calls.
  - Every earlier PASS used a synthetic adapter.
- **The successor**, built by root (0678): `claude_artifacts/step4_adapter_c2/step4_direct_preflight_cx2v002.py` (`bdedb83e`). Only L20 changes:
  - the pin must have exactly the three keys `{path, schema, sha256}`, with schema `UNT_GALAXY_M0_FORWARD_CALL_C2V001`;
  - `G.doc` then reads `{path, sha256}`;
  - the loaded template's schema must equal the pin's.

  Every other line, `DIRECT_CONTEXT_API` included, is byte-identical.
- **Review and inventory.** Claude3 verifies it with its 0169 harness (0684). Codex1 adds it to G7-SCOPE-1. Root names it as `direct_context` in C1 at H1.
- **Inventory (Codex1 0139):** PASS, 0 blocking.
- **Verification (Claude3 0172):** PASS, 0 blocking. MUST_PASS replays equal, and MUST_FAIL is 6 of 6. **R1G-A1 is closed.** The adapter cx2v002 (`bdedb83e`) is the step-4 `direct_context` source.

## A132: RI45-06 inputs (Claude4 0172) (2026-10-19 09:30Z)

- **D1 (a).** The EPS import path (`lwr_common_v001` 758740eb, `certs_common_r5` c75aaa5a) may read these completed model-run inputs, read-only and at exact path and sha only (pin file `step4_adapter_c2/EPS_IMPORT_RUN_INPUT_PINS_ROOT_V001.json`, `c0390172`):
  - `NGC3198_ROUTE_A_A2F10_RUN_V001` IDENTITY.json `7795015e` and start.json `bbff6f25`;
  - `A2_SEED_SCAN_G2_RUN_V001` result.json `951580e2`;
  - the 25 modules that IDENTITY names.

  These are model-run metadata and modules, not target data. Nothing else in those trees may be read.
- **D2 (a).** Per-point NGC GQ is a re-binding of `be148bab`, with no new compute.
- **D3** is deferred until registration.
- **Step-5 lever, noted.** NGC route A runs serially (column_workers 1, driver cx3r008). Claude4 estimates the 8-worker wall. A parallel route A for step 5 would be adopted only after a TESTED serial = parallel bitwise identity.

## A133: two-phase protocol, a fast provisional result then full validation (principal's direction; 2026-10-19 10:43Z, before any step-4 result)

**Why.**
- **The principal's direction:** "arrive at a high confidence result first using less compute intensive path and then continue with the higher overhead approach as complete validation."
- **Text of record:** `A133_TWO_PHASE_PROTOCOL_V001.md` (`cd92ef91`). It is a root workflow draft: one drafter, two refuters (integrity and feasibility), and a synthesizer.

**Adopted as written, with the build owners changed below.**
- **Phase 1** adds no DDO calls. It is a read-only snapshot of the registered campaign at B_P1, the forward calls before its first `march0` call. Its estimate u_A is the engine's own `primary_anchor`. NGC runs at the snapshot's v003g members plus three FD points.
- **Phase 1 result.** It is frozen as FREEZE_INCOMPLETE and scored as PROVISIONAL (PHASE-1).
- **Phase 2** is the registered step 4 and the full step-5 set, **unchanged**. It runs and is scored whatever Phase 1 shows, and it is the score of record.
- **The agreement test** (section 4: AT-0a, AT-0b and AT-1, with the allowance from τ_i = 0.25σ_i and hull_growth_tol) is frozen now. Its outcomes are COVERED, SUPERSEDED and NON_DISCRIMINATING.
- **Blinding order.** The section-2 order is adopted as written. Above all:
  - no Phase-1 NGC launch before r3a is published as a SEAL CANDIDATE;
  - no Phase-1 NGC value is read before r3a and the M-12 classifier are sealed.
- **Not adopted:** Gauss–Newton or Broyden steps beyond the engine's registered repair (section 9).
- **The NGC serial/8-worker identity pair** (A132) is the first NGC launch.

**Build owners (0678 and 0680 credit limits).**
- **Root workflows:** `phase1_c2v001.py` (snapshot, handoff, fdplan, band, agree); the roster builder and RUNBOOK_V002; the S1 template and launch path. Claude3 reviews each.
- **Claude4:** r3a (the re-render, as SEAL CANDIDATE) and M-12 classifier A.
- **Codex1:** M-12 classifier B, the only build that needs a different lineage, plus single-pass reviews of r3a and the RI45-06 producer.
- **RI45-02 and RI45-08:** root workflows, with Claude3 reviewing.

**Indicative timeline (CDT; UNTESTED; T0 is the step-3 verdict):**

| Milestone | Low | Expected | High |
|---|---|---|---|
| Phase 1 scored | Thu 10-22 | **Sat 10-24** | Sat 10-31 |
| Phase 2 scored | about Mon 11-02 | **about Thu 11-05** | about Sun 11-15 |

The scheduling-fix successors (budget 20/24; `sched_s45_c2`) are ruled separately when their workflow returns.

## A134: S4-R-C1 Q1–Q5 and Q8–Q10 are ruled; the LO route is per-state post-run acceptance; CP-1 starts after step 2 (2026-10-19 10:55Z)

**Adopted as written:** the root workflow draft `S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md` (`56774ba7`), Q1, Q2, Q3, Q4, Q5, Q8, Q9 and Q10 (physics and process lenses, each refuted twice). In particular:
- **Q1.** The prelaunch LO envelope is retired as an admission route. No honest prelaunch speed cap exists. The geometry cap rule is frozen only as contingent text.
- **Q2/Q3.** The enforcement point is post-run acceptance, after a FINISHED receipt and before any value is used. All 29 tail-ON direct calls go through it.
- **Q4.** |v_i| is the call's own recorded readout. τ_i = 0.25σ_i is the denominator. There are three row-reference policy reviews, one per D.
- **Q5.** Per-state acceptance is the LO route at all 31 points, through one wrapper successor (the L74 slot-rule string, and the L148–161 lo-slot check becomes "slot = the registered ρ record"). The failure readings are frozen now: NON_LAPSE_TAIL_MATERIAL, LO_UNCERTIFIED_TRANSIENT, the anchor-stop rule, and disclosure of high-Q∞ truncation. There is no tighter envelope and no scope change.
- **Q8.** There is one EPS policy review, instantiated per point by script (signed by Claude4). There are no cap reviews and no per-point LO reviews.
- **Q9.** C1 content is as written, frozen before HEADLINE11's first PRELAUNCH.
- **Q10.** There is no bare EPS magnitude gate. SRB-ROT ≤ τ_i/10 is checked on the accepted state, carrying AMB-04. The λ = 1.05 companion is only named.

**(b1) Offset GQ normalization: adopted, a physics-reading change (A115 (b)).** On offset stages only, the normalization is the max component, ≤ 2b/(1−z). The registered signed-P0 form divides by a net zero mode that is zero by construction, so it certifies nothing about quadrature. This is ruled before any signed-state number exists. Codex1 gives the cross-lineage review.

**Build owners (0678 and 0680):**

| Build | Builder | Reviewer |
|---|---|---|
| Wrapper successor (Q5) | root workflow | Claude3 |
| Acceptance input side (Q2) | root workflow | Claude3 |
| Offset-normalization successor set (signed_bound, evidence v004, enumerator v010 and the certificate guard) | root workflow | Codex1, single pass |
| Slot proof, per-state LO adapter and SRB-ROT adapter (Q2, Q10), retargeting its own c3v001 LO pieces | Claude3 | Codex1 for the per-state convention (Q8), single pass |
| EPS policy review (Q8) | Claude4 signs | — |
| The three row-reference policy reviews (Q4) | Codex1, with Claude4 as fallback; Codex3 is out | — |

**CP-1 (A122, 0686).**
- Claude3's c3v002 passed root's distinct review (wf_8bc34918; 0 blocking; 232/232 re-run; 31/31 keys).
- At the 0686 step-2 floor no worker can start while R2 runs (N1). **CP-1 therefore starts after step 2's last receipt,** with spike allowance 0 and max-concurrent 4. Root operates it, and does not restart the scheduler with workers live (N2). Verify uses `-I -B` (N3).
- The ρ records join CP-1 once the slot-proof producer is reviewed.

**Effect on timing.** HEADLINE11 (H2) waits on the wrapper successor, the slot proof and the ρ records, plus C1. A133's Mon-evening H2 is therefore optimistic; expect Tue Oct 20 (CDT).

**Reading points frozen before any per-state number (0690; Claude3 0178, INTERFACE_C3V001 `3976a41b`).**
- **Q4a readout set:** Picard-pass rows at call geometry, excluding the diagnostic route-A rows.
- **SRB-ROT target:** the own_source_state at `le{final_pass}_rotation`.
- **The final monitor-consumed iterate** is ROUTE_A_PRE_ACCEPTANCE_ITERATE, which reads TRANSIENT.
- **Mixed outcomes:** a FAIL at an accepted, inherited or route-B state is decisive. TRANSIENT needs every non-iterate state at PASS; otherwise the call reads INCOMPLETE.
- **Anchor:** any LO FAIL reads the step-4 stop, with the class recorded.

## A135: the step-5 NGC path for Phase 1 (root build `step5_path_c2`, verifier 0 blocking) and the S0 rulings (2026-10-19 12:40Z)

**Objects:** `claude_artifacts/step5_path_c2/`. README `fba1a70a`, HASHES `27fb117f`; 83/83 in two record runs; verifier 0 blocking.

| Object | sha |
|---|---|
| POLICY_C2V001 | `0c781a17` |
| Serial template (column_workers 1) | `68a19360` |
| CW8 twin template | `1aa66269` |
| Filler | `ec417e76` |
| Point handoffs | `7d3b7c3c` |
| Identity comparator | `8e857fff` |
| STEP5_REGISTRY | `38a75614` |
| Caps | `e7fa8c58` |

**Rulings (item numbers follow the build report):**
1. **Adoption.** The path is adopted on Claude3's review (lean; due Mon 10-19 20:00 CDT). Adopted with it: RI45-02 (a), RI45-08 (a, cx3r008 only), RI45-12 (a, interface A), the Phase-1 handoff schema (`A133_PHASE1_POINT_THETA_FIXED_TARGET_FREE`) and the new label rule.
2. **S0 certificate pins.**
   - **EPS:** each S0 point's own record, from Claude4's S0 successor, with rule (b) per 0693.
   - **GQ:** re-bound to `be148bab`.
   - **`uv_tail.lo_certificate`:** under A134, the per-point registered ρ record at that S0 θ (NGC geometry).
   - **Post-run per-state LO acceptance (Q2/Q3) applies to NGC calls as to DDO calls.** Claude3 extends its slot-proof producer to NGC S0 points, or posts by 17:00 CDT that it cannot; root then builds it.
3. **Caps.**

   | Call | Wall | RSS | Output |
   |---|---|---|---|
   | Serial | 610,324 s (2× the U estimate) | 32 GiB | 64 GiB |
   | CW8 twin | 22,752 s | 86 GiB | 32 GiB |

   The twin's planned stop after iterations 0–1 is not a failure; the twin is never a member.
4. **The identity verdict compares 2 iterations,** which covers the first warm-state transfer.
5. **Memory.** The identity pair runs only after step 2's last receipt. Root extends the memory watch to NGC processes and labels its units GiB.
6. **RI45-05.** The V007 adoption pin is the sealed compare's verdict report.
7. **C1 is the tail-era CX2V006 lineage** (v006r9 `721c7230`, plus the s45 scheduling successor once it is reviewed). S0 is identical under V005A and CX2V006 (TESTED). AT-0a re-checks this at the Phase-1 freeze.
8. **RI45-24 (PAR8-SF1)** is root's V006 entry, before T0. RI45-25 comes before the first step-5 result.
9. **RI45-13** applies per launched spec: a fresh dry plan with the real pins, the spec sha registered, and a driver sha check. Root reads the blocker lists.
10. **phase1 `handoff`** needs a successor that supports one certificate map per member, before any member after u_A launches. S0 is not affected. Root builds it by Wed 10-21.
11. **The carriers successor** is adopted before any carrier is extracted from a step-5 result.

## A136: correction to A135 item 2. The NGC launch carries the registered NGC LO certificate as a custody pin; the NGC LO reading is decided post-run (Claude3 0189) (2026-10-19 12:50Z)

**Facts (TESTED by root from bytes).**
- Driver cx3r008 (`577f8c94`) L1076-1105 verifies `uv_tail.lo_certificate` by path and sha and passes it to route A as argv.
- The tail library (`owned_uv_tail_lapse_v003` L962-985) only hash-checks it and records it in the state record. **It makes no numeric use of it.** The EPS certificate is the one used numerically, in `_eps_per_shell`, `field_bound` and `srb_rot`.
- The step-5 dry plans used LO `07745bbf` = `tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json`.

**Ruling.**
- **Launch pin.** A135 item 2 is corrected: a per-point NGC ρ record is **not** a launch prerequisite. Phase-1 NGC calls (S0) carry `LO_NGC_K32_CERT_V001` (`07745bbf`) as their `uv_tail.lo_certificate` launch pin. It is a custody pin only and changes no computed value.
- **The NGC LO reading** follows A134's logic: per-state post-run acceptance, with a per-point NGC ρ, before any NGC value is read. Claude3 builds it during the runs, as offered:

| Item | Ruling |
|---|---|
| G1 | A θ-bound successor of the ρ part of `lo_ngc_field_k64_c2v001.py`, the producer of the NGC LO certificate, in the NGC domain. |
| G2 | Settings exactly as that producer's registered run for `LO_NGC_K32_CERT_V001`: coverage, partition, the K = 2 kept-cube exclusion, search and rng. No new choices. |
| G3 | NGC point custody = driver cx3r008 `577f8c94` + the S0 θ key (`1be5ed70`) + spec sha. `route_a.column_workers` stays inside custody until the identity pair is TESTED. |
| G4 | Two separate ρ processes at the NGC seed must be bitwise equal before any NGC acceptance. |
| G5 | Route string `NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE`. The thresholds are those registered in the NGC LO certificate, unchanged. The A134 failure readings apply to NGC (NON_LAPSE_TAIL_MATERIAL, TRANSIENT, INCOMPLETE). |

- **Review and deadline.** A root workflow reviews it (lean). It is due before the first Phase-1 NGC value is read, about Thu 10-22. It is not launch-blocking.

## A137: the Phase-1 tool (34eaef36) passes review; three rulings fixed before their deciding moments (Claude3 0191) (2026-10-19 13:05Z)

- **Review.** Claude3 0191: 0 blocking, and the verifier holds.
- **N-C, campaign config freeze (before W1).**
  - Any campaign-config change, **including the sched v002 config `05a2f987`**, lands before campaign wave 1.
  - From W1 until the `march0` plan is written, no campaign-config edit is allowed.
  - Root keeps the exact prefix-config bytes, as a byte copy, and passes them to snapshot, handoff and at0a.
- **N-B, the AT-1 FD-noise term e_q (before any at1).** e_q is the **member-displacement bound Σ_k 2ε_k |Δ_m,k| / h_k**: the FD truncation bound of the linear map at member m's own displacement.
  - The tool's band-optimum reading does not bound the K-error, so it is not used.
  - This is fixed now, before any number. A133 §4 is amended accordingly (erratum E_A133_1).
- **L5, B_P1 on a corner anchor with no `march0` wave.** B_P1 is the number of forward calls before the first call whose family is outside {seed, jacobian, repair, gd_pre}. This generalizes "first `march0`". Root builds the one-line successor, and Claude3 reviews it.
- **Process deviation, recorded (register).**
  - Claude3's review lens ran one unfiltered recursive grep over `claude_artifacts/` for about 2 min. It printed about 10 bytes of `*.py` names, showed no file content and used nothing.
  - The traversal could include `c5h_hull_c2/`. C5H blinding ended at the V007 seal (07:00:44Z), and no NGC3198 target content was printed.
  - Remedy: lane helper prompts forbid broad recursive grep or find; only named paths are opened.
- **phase1_c2v002 (root build, 13:40Z).**
  - Object: `phase1_c2v002.py` (`d64351ec`), tests `b1aedebc`, HASHES_V002 `af8509bb`.
  - Tests: 103/103 in two record runs. The root verifier read PASS, 0 blocking. Only L5 and N-B change; the march0-boundary outputs are byte-identical to v001; corner seeds pass.
  - **Ruling, before any at1:** ε_k in e_q is the row's L1 `eps_q`, the largest ε over u_A and the three F points, applied to every axis. It is a valid bound, possibly loose. A tighter per-axis ε would need a new at1 input and is not adopted.
  - Claude3 reviews v002.
- **Second process deviation (Claude3 0194), recorded.**
  - What ran: about 13:34Z, one unpruned `find claude_artifacts -maxdepth 3 -name <driver file>` by a verifier whose prompt predates A137.
  - What it touched: it listed names only inside about 20 folders whose names contain runs or C5H. It read no file, and C5H blinding had already ended.
  - Effect: none. Later prompts carry the named-paths-only rule.

## A138: four interface rulings before the first real acceptance (Claude3 0196) (2026-10-19 14:10Z)

- **V01, the interface gap.** Both fixes:
  - **(a)** the acceptance handoff calls Claude3's `adapt_call_lo`, the A134 split. It no longer calls `lo_core.produce_current_lo` directly.
  - **(b)** the input side writes `state_files` (the call's own `out/result.json` pin) and `execution {fresh_call, resumed, retried, route_a_completed_normally, run_root}`.
  - Root builds acceptance_q2 v003, and Claude3 reviews it.
- **V02, the enumerator.** C1 names the **b1 enumerator `4ca7f364`** (A134 (b1); Codex1 0142 PASS). Claude3 issues the one-constant erratum successor of its adapters.
- **V03, bitwise ρ.** It is the **10-key canonical comparison**, as in wrapper v002 L189-191, for the (a)4 check and for the adapter alike. Claude3 issues the one-function erratum successor.
- **V09, the wrapper path.** After Claude3's review, wrapper v002 (`7a6af535`) is published with `cp -n` as `calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py`, the same sha, beside core `dc895f8a`. Every pin names that path.

## A139: guard cascade and wrapper v002 published (Claude3 0197: both 0 blocking) (2026-10-19 14:15Z)

**Published with `cp -n`.** Every target was absent beforehand, and every copy's sha was verified after copying:

| Object | Path | sha |
|---|---|---|
| guard011 | `step4_launch_packet_cx1/impl/step4_guard_c2v011.py` | `eb97e303` |
| launcher012 | `step4_launch_packet_cx1/impl/step4_launcher_c2v012.py` | `59c00707` |
| bind010 | `step4_launch_packet_cx1/impl/step4_bind_c2v010.py` | `4d07dca3` |
| wrapper v002 | `calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py` | `7a6af535` |
| PRELAUNCH005 | `step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py` | `117b3520` |
| Params | `sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003.json` | `b7fdaf10` |

**C1 (H1) must:**
- pin guard011 and launcher012 at the impl paths and list both in `sources`;
- name the q5b1 wrapper as `context_module`;
- **list the tail library `owned_uv_tail_lapse_v002.py` (`2026f2b6`) in `sources`** (Claude3 0197 N4);
- name the b1 enumerator (A138);
- use the final-spec producer v004 (`fcbf1c3e`).

## A140: sched v002 decisions before W1 (Claude4 0192: 0 blocking) (2026-10-19 14:25Z; recorded 14:55Z)

**Recorded late.** Dispatch 0706 published this ruling at 14:25Z, and root then omitted it from this file. It is entered here as erratum E_A140_1, with the text unchanged.

- **N1.** The machine gate gets per-driver foreign-tree classes: an NGC class for cx3r008 serial trees, sized from Claude4's RI45-12 estimate, plus a cw8 twin class. Root builds gate v003, re-simulates with S0 ×4 plus the twin, and Claude4 reviews the delta.
- **N2.** The cw8 twin runs only when no DDO route-A call is in flight. Campaign and direct admissions are held for its ≤ 22,752 s. It is not on the critical path.
- **N3.** The S0 NGC output cap is 136 GiB, superseding A135's 64 GiB. NGC outputs go to External1.
- **N4.** Root re-derives the DDO per-call wall from the step-2 receipts before W1.
- **N5.** The DDO output cap is 80 GiB, to be confirmed against the receipts.
- **V2** is decided at H3.

All of this lands in the campaign config before W1 (A137 N-C).

**r3a SEAL CANDIDATE (Claude4 0194).**
- **Text:** `miss_reading_prereg_c4/r3a_sc2/PREREG_MISS_READING_R3A.md` (`9a2f177f`); ROOT_ITEMS_R3A (`63f1bf74`); classifier "none" until M-12 is built.
- **Gate:** the hard gate before a Phase-1 NGC launch (A133) is **met**.
- **Before the seal:** root rules M-1 to M-16. The seal comes before any Phase-1 NGC value is read.

## A141: the step-5 NGC path is adopted (Claude3 0200: 0 blocking); launch rules L1–L4; a conduct note (2026-10-19 15:02Z, the time 0707 was published; the header first read 15:10Z, erratum E_A141_1)

**Adoption.** A135 item 1 is satisfied. The `step5_path_c2` objects are adopted as built.

**Launch rules:**
- **L1, output cap.** The NGC serial output cap is **136 GiB** (A140 N3), above Claude3's suggested 96 GiB and the derived U total. An OUTPUT_CAP stop under A133 §3(c) is rerun with the output cap raised. A cap is not a physics input, so this changes no value.
- **L2, units.** The gate's campaign reserve is **29.1 GB**, from 27.1 GiB in consistent units. Gate v003 states every threshold in one unit, and Claude4's v003 delta review checks it.
- **L3, path spelling.** The comparator's `--serial`/`--twin` are spelled exactly as root_monitor's `--outdir`, in absolute `/Volumes/External1/...` form, never through the `runs_ext` link.
- **L4, twin stop.** The twin's planned stop is root's kill trigger once iteration 1 is COMPLETED and its sidecar iteration record exists. That keeps the pair inside the gate's spike window. Any twin cap stop is planned, not a failure.

**Text errata to the step5_path_c2 README (L5, L6; erratum E_S5P_1).** These are recorded here, and the pinned bytes are left unchanged.
- "RI45-02 (a) and RI45-08 (a) closed" holds for the S0 path only.
- HASHES has 29 entries.
- The registry omits the comparison-spec .md, which HASHES does cover.
- The threshold is 8.79 GB.

None of these changes a code path or a value.

**Conduct (register).**
- Claude3's lens opened `NGC3198_FREEZE_SLOTS_CX3V003.json` (`d3859b42`), which its prompt rule did not name as a model file. The verifier showed the chain did not need it.
- Claude3 confirms whether the file holds any observed NGC3198 velocity. Until it does, the item is recorded as an open blinding check.
- **Blinding check closed (15:10Z).**
  - Claude3 0202 confirmed it from the transcripts: only the two geometry slots reached any output.
  - Root then took a structure-only listing of `d3859b42` (key names, types and lengths; no values printed). It holds the 43 query rows with radius and index fields only (`Rad_text`, `radius_kpc`, `query_id`, `data_row_index`, GL4/GL10 flags, N2 truncation), the geometry and projection slots (distance, inclinations), alternatives, citations and truncation pins, and a `target_free` field.
  - **There is no velocity, error or rotation-curve field. Blinding is intact.**
- Remedy: prompts now name every NGC3198-named file a lane may open.

## A142: r3a ROOT_ITEMS M-1 to M-16 are ruled, and the A133 step-0 batch (2026-10-19 15:28Z)

**Text of record.**
- Root workflow draft `R3A_ROOT_ITEMS_RULINGS_DRAFT_WF_B556A161.md` (`0f45f3c4`): physics-honesty and consistency lenses, adversarially checked.
- It was drafted against sc2. The sc3 ROOT_ITEMS (`0b291275`) changes no option and no recommendation.
- Items are adopted **by id**, against the ROOT_ITEMS sha of the final render.

**Adopted as drafted:**
- M-1 (a′); M-2; M-3 (A)+(alpha); M-4 (i), with its reason replaced as the draft says; M-5 with its two additions; M-6 with its vehicle and blinding fixes; M-7 (i); M-8; M-10 with precedence; M-11; M-12 (i)–(v); M-13; M-14; M-15 (a)+(1); M-16 (1).
- **M-9 tightening, confirmed.** CONSISTENT if and only if H_S > H_P and A_S < A_P; AGAINST if and only if H_S ≤ H_P and A_S ≥ A_P; otherwise NOT_DECIDED. This is the stricter reading (A48). It is made before any number, and neither classifier is built yet.

**Root's open items:**
1. **M-9:** confirmed, as above.
2. **Classifier B.**
   - It stays with Codex1, the only non-Claude lane with credit (Codex2 and Codex3 have none). There is no Claude fallback, since the requirement is a different lineage.
   - **Deadline:** Fri 23 Oct, 22:00Z.
   - If it is late, A133 step 2 holds: values stay validity-only, and the freeze and score wait. No launch is delayed. Root alerts the principal at the deadline, because only Codex credit can unblock it.
3. **STAGE0 timing.** A133's step-5 estimate does not include STAGE0 calls. Root computes the delay from the member count at the Phase-2 selection and publishes it then. Headline calls go first (M-14).
4. **AT-1 categories (Claude3 0204 N1).** Ruled in A143's successor entry once the three-lens check (wf_d6eb5084) returns.
   - The seal pins `band` and `agree` at the reviewed successor `phase1_c2v003` **if and only if** its review returns 0 blocking before the seal entry is written.
   - Otherwise the seal pins `d64351ec`, with the N1 label gap disclosed. This is the same no-discretion rule as M-14.
5. **Step-0 batch.** Written below.
6. **M-15 record.** The identity-pair launch script writes the pre-launch record by exclusive create as its first action. It refuses to launch if that write fails.
7. **Re-render order:**
   1. the last pre-seal V006 write;
   2. a V006 write freeze, announced by a dispatch that carries the V006 sha;
   3. the final render;
   4. T1–T7, then Claude4's delta check;
   5. the classifier-bearing SEAL CANDIDATE;
   6. the seal entry, appended after the last byte of V006 (M-6).

**Builds:**

| Build | Owner | Review |
|---|---|---|
| Final render after sc3, carrying the "must be built" list in the text of record | Claude4 | — |
| Classifier A, with the M-12 suite additions | Claude4 | — |
| Classifier B | Codex1 | — |
| STAGE0 successor (M-14, with both TESTs) | root workflow | Claude3 |
| TSR flag record (M-7) | root | — |
| RUNBOOK_V002 and roster builder (A133) | root workflow | Claude4 |

**Attestation note (M-6).** Root's drafting workflow (wmmx6by29) opened `d3859b42`. A141 showed that the file holds no velocity.

**A133 step-0 batch (§2 row 0), by id.** All of the following are in force from this entry:
- A133 §1, §3 and §4 as adopted in A133, with E_A133_1 and the ε ruling in A137;
- the S1 registration at u_A;
- the Phase-2 commitment;
- relaunch rule (c) and mechanical rules (a)–(f);
- the per-phase RUNBOOK step 4;
- the RI45-03(b)/RI45-10 Phase-1 exception (§1.6);
- **M-8**, as recommended;
- **R-D15 amended:** S1 and the Phase-1 NGC calls may overlap the campaign under the machine gate (A143).
- **r3 withdrawn:** `FROM_CLAUDE4/0124_2026-10-19_SEAL_CANDIDATE_miss_reading_prereg_r3.md` is FAIL for the two-phase run, and r3a supersedes it.
- **H2** comes no earlier than the step-3 verdict and C1. This batch precedes it.

## A143: sched v003 machine gate is adopted pending Claude4's review; the disk guard and the identity-pair order (2026-10-19 15:28Z)

**Build.** Root workflow wf_cfaab36f, at `claude_artifacts/sched_s45_c2/v003/`.
- HASHES `ca1eadca`; gate `736a3438`; config `d9241676`; CAPS `35f66b6a`; direct params C2V003A `4adc296b`.
- Tests 176/176. The verifier found 0 blocking and 13 notes (NO_FIX_NEEDED `fba85ff1`).
- With no cx3r008 tree on the machine, v003 decides exactly as v002. W1 no longer halts at U, and the twin spends 0 h beside DDO route A.
- **Adopted, subject to Claude4's delta review returning 0 blocking,** including the L2 units check (A141). It lands before W1 (A137 N-C).

**D1, disk guard (verifier note 4).**
- With the 80 GiB guard, engine wave 15 (24 calls) would need 1,940 GiB of free space and would halt.
- **Ruling:** the guard is separated from the cap. `disk_guard.per_call_bytes` = 2 × the largest per-call output measured in the step-2 receipts, rounded up to a whole GiB. Root re-derives it together with N4 at step 2's end, in one config successor before W1.
- Unchanged: the per-call output caps (DDO 80 GiB, NGC 136 GiB) and the per-start check (one output cap plus 20 GiB).
- The guard only sizes admission; it changes no value, and the cap still stops a runaway call.
- **Storage forecast.** Root computes it from W1's measured outputs (campaign plus step 5, against External1 and internal free space) and assigns volumes before the first step-5 call. External1 stays connected.

**D2, identity-pair order (verifier note 5).**
- The twin and a serial NGC tree in route A cannot be admitted together (83.7 > 83 GB).
- **Ruling:**
  - The serial S0 calls of record launch first.
  - The twin, at the same θ, starts when the gate admits it: no serial NGC tree and no DDO route-A call in route A, and only between HEADLINE and W1 or between waves (note 2).
  - "Pair" in A133 §1.4 means the same θ, not the same start.
  - The twin stays off the critical path (A140 N2), and it is killed after iteration 1 (A141 L4).

**D3, launch form (notes 1 and 2).**
- The monitor command must carry exactly `--driver-sha256 <64 hex>` and an absolute `--spec`.
- Root's twin launch script refuses any other form, confirms that `--hold-check` exits 3 once the twin is up, and refuses to start mid-wave.

**D4, serial class (note 7).** If an S0 call's measured route-A peak exceeds 22.4 GB, root builds a gate successor before admitting any further NGC call. The watch alerts on that peak.

**D5 (note 9).** A DDO tree whose pool has closed is not "in flight" for step5_path L146. The rule exists to prevent memory spikes, and a closed pool has none.

**Errata, with no rebuild:**
- note 10: the test docstring;
- note 11: the "16–28 h faster" claim is overstated, and the README table governs;
- note 12: the N4 rebuild must name C2V003A (`4adc296b`) as its predecessor;
- note 13: test portability.

## A144: AT-1 rulings on Claude3 0204 N1, N2 and N6 (erratum E_A133_2), ruled before any band or at1 number (2026-10-19 about 15:37Z; header first read 15:40Z, erratum E_STAMP_1)

**Basis.** Root draft R1–R3 went through a three-lens refutation (wf_d6eb5084: math, protocol, code). Every lens amended it and none refuted it; the amended texts are adopted below. Claude3 0204 (phase1_c2v002, 0 blocking) is the review of record for v002.

**R1 (N1): the box-slice category. E_A133_2(a) amends the A133 §4 category list. Label only.**
- One helper builds the band region's rows (A, b_band, and the family slices TRUST_RADIUS, BOX, LINEAR_DDO) exactly as `band_rows` does. A test proves that its A and b_band are bitwise equal to `band_rows`'.
- **Violation rule:** row i is violated if and only if (A c)_i − max(b_band_i, 0) > E._LP_EPS, with c = V_I Δ_m.
  - The clip is `_lp_max`'s own (engine L1787).
  - _LP_EPS (1e-12) is the pinned engine's tolerance (engine L181), so there is no new constant.
  - Exact comparison was rejected: rounding mislabels members that move along a face, and members exactly on a face.
- **What a failing (member, row) prints:**
  - `region_rows_violated`: in the fixed order [TRUST_RADIUS, BOX, LINEAR_DDO], or [] if none;
  - `region_max_violation` for each family;
  - `category` = the first violated family, mapped to OUTSIDE_TRUST_RADIUS, **OUTSIDE_BOX_SLICE** or OUTSIDE_LINEAR_DDO_REGION, and NGC_NONLINEAR only when the list is empty;
  - `geometric_part` and `residual_part`, with excess = geometric_part + residual_part.
- The category says where c lies; it does not apportion the excess.
- **Regression requirement:** with ε = 0 everywhere, the failing set, the excess, norm_n and the outcome are byte-identical to v002.
- **Disclosed:** labels can change at the ulp level against v002's LINEAR test, and a pair that violates both BOX and LINEAR_DDO now reads BOX.

**R2 (N2): the degenerate band. §1.5 is kept; `band`, `band_rows`, `cmd_band` and the L1 schema are unchanged.**
- at1 prints `band_region_extent`: for each identified c_j, [min, max] over the band region's own rows, solved by E._lp_max, with both statuses.
- It also prints `band_region_single_point`:
  - true if and only if every extent is OPTIMAL and exactly [0.0, 0.0];
  - NOT_AVAILABLE if any of those programs is not OPTIMAL. This never refuses and never changes a row.
- The reason is BOX_CORNER if and only if the box rows alone give [0.0, 0.0] on every j, and OTHER_ROWS otherwise.
- The name is distinct from at1's `identified_projection_vs_linear_region`, which leaves out the trust rows.
- **A band of any width, zero included, is never read as a spread, a zero spread or a confidence statement.**
- **Expected corner outcome, stated now, before any number.** At a single-point band (a_q = 0), AT-1 reads SUPERSEDED whenever some Phase-2 member has |K_q V_I^T c_m| > e_q. Under BOX_CORNER those pairs read OUTSIDE_BOX_SLICE. That follows from how the band is built, not from any disagreement between the phases.

**R3 (N6): the full noise bound. E_A133_2(b) supersedes E_A133_1's formula. This is a physics-reading change (A115 (b)), ruled before any band or at1 number.**
- **The formula:** e_q(m, q) = ε_m + ε_q · ( |1 − Σ_k Δ_m,k / du_k| + Σ_k |Δ_m,k| / h_k ), where:
  - du_k is the signed fdplan step and h_k = |du_k|;
  - ε_q is L1 `eps_q`, the largest certificate ε over u_A and the three F points, unchanged from A137;
  - ε_m is the member's own `eps_km_s[q]`.
- This is the exact worst case of the noise in g(u_m) − g(u_A) − K̂Δ_m when |δ_m| ≤ ε_m and |δ_A|, |δ_Fk| ≤ ε_q. The looser form drafted earlier would hide real NGC nonlinearity (wf_d6eb5084, math lens), so it is not adopted.
- **Guarantee:** a member with empty `region_rows_violated` and an NGC map linear on {u_A, F, u_m} cannot fail AT-1 when the noise is within the certificates. No claim is made for a nonlinear NGC.
- **Input contract.** The Phase-2 members file carries `eps_km_s`: 43 entries per member point, from that member's own point EPS certificate (r3a I-6/D-4, the same source as the Phase-1 `eps_km_s`).
  - `cmd_at1` refuses MEMBERS, writing no out-dir, when a member point lacks the list or the list's length is not 43. at0b is not affected.
  - When an entry is None, bool, non-finite or negative, that pair keeps every bounded term, e_q = ε_q(|1 − Σ_k Δ_k/du_k| + Σ_k |Δ_k|/h_k), and is flagged MEMBER_POINT_NOISE_NOT_BOUNDED.
  - When a row has no ε_q, it reads FD_NOISE_NOT_BOUNDED with e_q = 0, as in v002.
  - The flags are per pair, with `flag_reason`. A new list `pairs_member_point_noise_not_bounded` is added; `rows_fd_noise_not_bounded` stays per row.
- **Members-values producer.** A root build writes `eps_km_s` from each point's certificate, for the Phase-1 values file and the Phase-2 members file alike. It is due before the Phase-1 band.
- **Distinct-lineage check.** Codex1 does one short pass on the E_A133_2(b) formula only, before the seal. A134 (b1) is the precedent.
  - **Result: Codex1 0145, PASS with 0 blocking.**
  - Exact-rational enumeration over 384 cases × 32 vertices of the error box: every maximum equals the bound, so the bound is attained.
  - Evidence: `c2fda5ac`.

**Build.** Root workflow `phase1_c2v003`, then a lean Claude3 review.
- **Changes:** MODULE, E_Q_READING, `at1_rows`, `cmd_at1`, the new region helper, and A135 item 10's handoff successor (one certificate map per member).
- **Unchanged and AST-identical:** `band_rows`, `cmd_band` and `linear_model`.
- **Custody:** at1 requires `l1.module == phase1_c2v003`.
- **Seal.** The seal pins the v003 sha for both `band` and `agree`, which are one file, if and only if the review returns 0 blocking before the seal entry (A142 item 4).
- **M-12.** Both classifiers bind the v003 encodings:
  - the fourth category value;
  - `region_rows_violated`, `region_max_violation`, `geometric_part` and `residual_part`;
  - `flag_reason` and the per-pair list;
  - the band_region keys.
- **r3a.** Its A133 CITED_PINNED row names E_A133_2, and its table gains rows for A144 and later entries.

## A145: acceptance_q2 v003 passes verify (0 blocking); the adapter pin moves in v004 (2026-10-19 about 15:37Z; header first read 15:40Z, erratum E_STAMP_1)

**Build.** Root workflow wf_04c57fe8, at `claude_artifacts/s4_acceptance_c2/acceptance_q2/`.
- handoff `887c8ba0`, row producer `67fddd24`, HASHES_V003 `0821d05f`.
- Tests 115/115 and mutation 10/10. The verifier found 0 blocking (NO_FIX_NEEDED_V003 `c97c0195`).
- A138 V01 (a) and (b) are in place. The honest synthetic call is ACCEPTED through Claude3's real `adapt_call_lo`.

**v004, a root build, once Claude3's errata c3v003/c3v004 are published and Codex1's delta review passes:**
- `LO_ADAPTER` pins the published c3v003 adapter (a forward check gave 115/115);
- `adopt_lo` requires `is_pin(core_record)` before it adopts a PASS (note 2);
- `route_a_completed_normally` requires `is True` (note 4);
- the README text errata (notes 3 and 5).

**Claude3 reviews v004 only, lean.** That replaces the queued v003 review.

**C1 is updated with it:** the LO slot-proof producer joins the approved list, and the trusted producers name row producer v003.

## A146: errata selected (Codex1 0146: 0 blocking); the real-ρ gate opens; CP-1 starts during KHI under its own memory floor (2026-10-19 15:54Z; header first read 15:58Z, erratum E_STAMP_1)

**Selection.** Codex1 0146 is root's selected successful delta review. It is distinct lineage, closes 0143's B2/V02, B3 and V03 and also V09, and reruns the suites at 222/222 and 295/295.
- **Proof side c3v003** is adopted: slot proof `cd10cd59`, state adapter `211a3220`, SRB adapter `08e9ac0a`.
- **CP-1 c3v004** is adopted: common `53f10e6e`, runner `3f5e5c18`, assembler `cb5c61ee`.
- **The real-ρ gate is open** for CP-1, and its gate input pin is the 0146 record.
- **The deciding test** is the real anchor pair (attempts a and b), which must be bitwise equal on every shell diagnostic. A mismatch fails closed at the anchor.

**CP-1 timing; this changes A134's "after step 2's last receipt".**
- CP-1's own scheduler holds each start until available memory is at least allowance + (running + 1) × per-worker peak + margin, and it pauses on swap growth (CP1 run sheet §3).
- So root starts it **while KHI and N1 still run**, with: allowance **40 GiB** (to cover KHI's spike), max-concurrent **4**, per-worker peak 2 GiB, margin 4 GiB, swap hold 512 MiB, and the `taskpolicy -b` E-cores.
- It is not started before the run-sheet check (root workflow `cp1-c3v004-run-sheet`) passes.
- It changes no value: it only affects timing.
- Expected: about 5–12 h wall for 31 points at k = 4, so its records should be ready before H2.
- Root does not restart the scheduler with workers live (A134 N2), and a new anchor attempt needs a new out-root.

**Erratum E_STAMP_1 (register; Claude3 0210 and Claude4 0201).** Root typed estimated times into headers instead of capturing `date -u` at write time, against M-6 point 7. The actual write times, from file mtimes:

| Item | Header read | Actual |
|---|---|---|
| 0709 | 15:29Z | 15:28:23Z |
| 0710 | 15:33Z | 15:30:30Z |
| 0711 | 15:42Z | 15:38:11Z |
| 0712 | 16:00Z | 15:54:37Z |
| A144 and A145 | 15:40Z | about 15:37Z |
| A146 | 15:58Z | 15:54:30Z |

The dispatch files are not edited. **Remedy:** root runs `date -u` immediately before each write and uses that value.

**CP-1 started, Phase A (written 16:11:10Z).**
- **Run sheet.** `CP1_C3V004_ROOT/CP1_RUN_SHEET_ROOT_C3V004.md` (`75481f2b`). Its independent check found 0 blocking, and the dry plan read 31/31 SPEC_AND_KEY_VERIFIED.
- **Two-phase form,** because the runner does not stop on an anchor ρ-pair mismatch:
  - Phase A = rows 1 and 2 (the anchor and HEADLINE_CORNER_000).
  - Root then checks that the `ANCHOR_RHO_PAIR` record shows the 10-key canonical comparison equal, separate processes, distinct records, and the cross-check AGREE.
  - Phase B = all rows, on the same out-root. Folders 1 and 2 are skipped, and no worker is live between the phases. **This is a continuation of the same run, not a reuse of the out-root.**
- **Phase A scheduler:** pid 18346, run_id `20261019T161053Z_18346`, out-root `claude_artifacts/s4rc1_c3/cp1_run_c3v004`.
- **Gate and settings:** SCHEDULER_START reads `rho_gate` OPEN (0146 bytes match), with the A146 settings.
- **It is waiting on the physical floor:** 47.5 GB is available, and the first start needs 49.4 GB.
- Root posts the anchor EPS policy-review instance's path and sha for Claude4's hand-check (0201/0202) when it exists.

## A147: gate v003 adopted (Claude4 0203: 0 blocking, 13 NOTEs); rulings L3-01, L3-02, L3-03 and L3-06 before W1 (2026-10-19 16:35:44Z)

**Adoption.** sched v003 is adopted (A143), as the gate for W1 and for every cx3r008 launch.
- Claude4 0203 found 0 blocking. Its verifier refuted none of the 13 NOTEs, and 0204 is an erratum to L3-06.
- Units, computed values and the per-driver classes HOLD.

**L3-01, the disk guard. A143 D1 is withdrawn; option (a) is adopted.**
- The parent orchestrator refuses a guard below the cap (`c75a889f` L1747-1749, test K04b). So the guard stays at the 80 GiB cap.
- Wave 15's need, 24 × 80 GiB + 20 GiB = 1,940 GiB free at admission, is met by volume planning, not by the guard.
- **Measured.** One step-2 case (C4T_D5) is 17.4 GB. External1 has 2,877 GiB free and the internal disk 1,024 GiB, read at 16:35:44Z.
- **Forecast (UNTESTED until W1 is measured):** about 120 × 17 GB ≈ 2.1 TB for the campaign, plus the step-5 NGC outputs. That is tight against External1 alone.
- **Rule.** Root re-forecasts from W1's measured outputs and assigns volumes before the free space on the campaign volume falls below the next wave's need plus all NGC outputs. If both volumes together cannot hold the program, root alerts the principal before W1 + 2 days. No deletion; only verified moves.
- **Unchanged:** the wall cap is still re-derived at step 2's end (N4). It needs a build_params successor (L3-08) that also names C2V003A (`4adc296b`) as its predecessor (A143 note 12).

**L3-02, units (A141 L2): relabel only.**
- 72 and 83 are the measured 72.0 and 83.2 GiB, kept as the stricter GB limits, and swap is stated in GiB. The net error is strict: 1.5 GB at d2 and 0.4 GB at d1.
- The limits are not converted to true GB. Converting them would admit the twin beside a serial NGC route-A tree, against A143 D2 (test G35d).
- The 29.1 GB reserve is root's A133 procedure for S0 admission. That admission takes the stricter of the A133 check and gate v003's `ngc_admission`.

**L3-03, the launch form applies to every cx3r008 launch, S0 included.**
- The form is exactly `--driver-sha256 <64 hex>` and `--spec <absolute path>`, each with a space; the `=` forms are not used.
- After each launch, root reads `--hold-check` runs[].kind and phase:
  - each S0 must read NGC_SERIAL;
  - the twin must read NGC_TWIN.
- If a run reads GENERIC or NGC_UNIDENTIFIED, root stops that launch at once, before it can hold W1. It is recorded as a procedural mis-launch, not a scientific failure, and relaunched in the correct form.
- The S0 launch kit (root workflow `s0-launch-kit`) carries this check.

**L3-06 (with erratum 0204), the 103 GB rule.**
- With S0 ×4 U peaks coinciding beside a gate-admitted DDO route-A call, the total can reach about 125-128 GB. That is over the A133 103 GB rule but below RAM. It is reachable but unlikely.
- **No gate successor.** It would cost campaign throughput.
- **Mitigation, which changes no value:** the A130 lever. The watch alerts when the total footprint passes 95 GB or swap passes 8 GB, and root SIGSTOPs Phase-1 NGC processes first (A133 §1.4).
- A jetsam kill fails closed and goes through rule (c).

**Noted, no W1 decision:** L3-04 (the D4 alert is in GB, measured by the A130 watch), L3-05, L3-07, L3-09 (any driver successor needs a gate successor), L3-10, L3-11, L3-12 and L3-13.

## A148: S0 certificates pass review (Claude3 0211: 0 blocking); the members eps_km_s writer is specified (2026-10-19 16:37:36Z)

**Review.** Claude3 0211 found 0 blocking, and its verifier holds. All 12 of 0184's S0 requirements are met.
- EPS records: `efdc430a`, `8270b6b3`, `bfac8f57`, `5dd9900a`. GQ bindings: `903a7d6c`, `cc6113ce`, `4fc1d744`, `934c0a47`.
- Producer `8972822b`; fence `b5a6aa09`.
- **The S0 certificates are adopted as the S0 EPS and GQ launch pins** (A135 item 2, A132 D2(a)).

**The members `eps_km_s` writer (0211 N1; A144 R3). Root builds it, and Claude4 reviews it as the certificate-schema owner who did not build the writer.** One writer serves the Phase-1 values file (u_A and the F points) and the Phase-2 members file. For each point it emits:
- the point's θ key;
- the path and sha of the certificate whose `point.key` equals that key, refusing anchor, other-point, SMOKE and BIND_CHECK records;
- a check that the certificate's schema is `UNT_CLAUDE4_S0_POINT_EPS_C4V002` (or its reviewed successor), its status is CERTIFIED, and its coverage [2,91] covers field_bound's k-range;
- **43 finite, nonnegative `eps_km_s`** in the frozen query-row order. Each comes from the pinned `field_bound` applied to that certificate and that point's own field, with the field_bound pin recorded.

It never broadcasts eps_max and never reuses another point's values. A point with no certificate gets none: its entries are None, and A144 R3 then flags the pair.
- **Certificates for other members.** Only the 4 S0 θ have certificates. Any other Phase-1 or Phase-2 member needs its own certificate run (about 1,700-4,380 s each) before its values are written.
- **Cross-check, never a substitute (0211 N2).** eps scales as s⁰·(γ/Eref)⁻¹·ℓ_F⁻³.

**Noted:**
- 0211 N3: the envelope/actual ratios are search statistics, not convergence margins.
- N5: fence and GQ-writer successors must name the NGC3198-named files they read (0708).
- N4, N6, N7.
- Claude4 0205: a SIGSTOPped NGC tree is still counted by the gate. The A130 lever relieves memory through swap, not through admissions, and root plans alert responses with that in mind.

## A149: phase1_c2v003 passes both root verifiers (0 blocking); v003a closes their gaps before Claude3's review (2026-10-19 16:39:47Z)

**Build.** Root workflow wf_08e9901b, at `phase1_c2/`.
- `phase1_c2v003.py` `149ed4cb`, tests `331d0212`, HASHES_V003 `518b6601`.
- 142/142 in two record runs, and 12/12 mutants killed.
- Both verifiers (math/regression and adversarial) found 0 blocking. An independent oracle matches it on R1, R2 and R3; `band_rows`, `cmd_band` and `linear_model` are AST-identical to v002; with ε = 0 the result is byte-identical to v002.
- The corner case goes from 316 to 320 pairs: under E_A133_2(b), e_q is smaller than v002's for some far members (FORMAL, disclosed).

**Builder choices 1-10 are adopted as built.**
- Choice 1 is confirmed: the reason is null when single_point is NOT_AVAILABLE.
- Choice 8 is the per-member form.

**Rulings:**
- **A144 R2 wording.** The corner expectation reads "BOX is in `region_rows_violated`". A corner member with |c| > r reads OUTSIDE_TRUST_RADIUS first, which is not a contradiction.
- **Per-member certificate form (procedural).** For every member after u_A, root uses `certificate_pins_by_member` only. The shared form is kept for S0/u_A alone (it stays byte-identical to v002).
- **Rounding.** AT-1 keeps no rounding slack (A48). A failure at the ulp level needs noise exactly at the certificate bound with adversarial signs, which has measure zero. It is a NOTE.

**v003a, a root build. Claude3 reviews v003a only (lean); the v003 review is dropped.**
1. `member_eps` catches OverflowError, so that pair is flagged MEMBER_EPS_NON_FINITE instead of refusing the whole at1.
2. at0b records `members_sha256`, and at1 requires its `--members` sha to equal it. This closes a gap present since v001.
3. at1 also prints `band_region_box_only_extent`, print only. The single-point rule stays exact with no new tolerance; the box-only extents show BOX_CORNER geometry when an LP tie leaves the full-region extent at about 1e-14.
4. Tests kill the 5 surviving mutants:
   - region tolerance 1e-9 and 1e-13;
   - `>=` in place of `>`;
   - the ε contract applied only to member_valid = true points;
   - the scope check by spec sha only.

**M-12.** The classifiers also bind the print-only `e_q_per_member_row` fields (`eps_m`, `flag`, `flag_reason`), at0b `members_sha256` and `band_region_box_only_extent`.

**ε provenance.** at1 cannot verify where `eps_km_s` came from. That custody is the values writer's (A148): each list is bound to its point's certificate sha, and the writer is reviewed.

## A150: S1 transfer test registered (RI45-04 / R-C6), in force before T0; R-S1-1 to R-S1-3 ruled; launch-path successors commissioned (2026-10-19 17:05:52Z)

**Registration in force:** `claude_artifacts/s1_path_c2/S1_REGISTRATION_DRAFT_C2V002.md`, sha256 `67b4bd78c88d87ea531af99aac16d98c80a20289eca191d4db1897ba8ca76f00`.
- It was drafted by a root workflow (wf_8772a69e), refuted by physics and process lenses (all their blocking findings applied), then verified. The verifier's 3 blocking findings are code defects in the launch path, not defects in the registration text.
- It is entered **before T0**: no V007 T value has been read and no campaign result exists. That satisfies C1 and R-C6 BEFORE_CAMPAIGN.
- **Adopted as written:**
  - cases S1_UA_C3T and S1_UA_C4T at u_A's exact θ bits;
  - K4′ is the campaign's u_A call;
  - the statistic Dhat_S1;
  - **TH-1** Dhat_S1 ≤ 1, and **TH-2** every row ≤ τ_i/2, decidable (E + E^A ≤ τ_i/8), with no TINY exemption;
  - validity gates SV0–SV8 and RO1;
  - the reading order and codes;
  - S1-DIAG as the FAIL next step;
  - CHOICES C1–C23.
- **Stated before any number:** if V007's own anchor Dhat_T(3,4) lies in (1/2, 1], TH-2 is expected to read FAIL_TH2 near the anchor.

**Text errata, recorded here; the pinned bytes are unchanged:**
- §6: with both pairs decidable, the operative PASS bound is Dhat_S1 ≤ 1/2, and TH-1 is then redundant (verifier note 15).
- §11 rule 4: launcher012's lock refuses a second batch rather than queueing it, so "serially" means root launches the second call after the first ends (note 3).
- §11's A147 L3-02 citation is CHOICE C15 (note 14).

**Root items:**
- **R-S1-1 (seed branch): S1-B is registered.** If u_A is AT_ANCHOR:
  - PASS_AT_ADOPTION_POINT releases **Phase-1** step-5 reads only.
  - **S1-B** is the same pair, statistic, thresholds and reading at the first Phase-2 member whose θ bits differ from the anchor. That is 2 more calls, and Phase-2 step-5 reads stay held until S1-B reads PASS. This is the stricter option (A48).
- **R-S1-2: confirmed.** For an OFF_ANCHOR u_A, one S1 at u_A serves both phases (A133 L202). The PASS label publishes "UNTESTED at every other point, including the Phase-2 reference member unless its θ bits equal u_A's".
- **R-S1-3: commissioned now** as root builds on the Phase-1 critical path. Each gets its own MUST_FAIL tests and a distinct-lane review.
  1. **The guard successor (guard012):** a POST_S1 batch may run with the campaign active, under machine gate v003 and the A133 rule. Every other batch still needs `campaign_inactive: true`. Overlap is refused from the gate snapshot, not on root's word (note 2).
  2. **The core/wrapper successor:** last break 3 and `composite_grid_spec` = CB C3T bitwise are accepted **for S1_UA_C3T only**. Every other `validate_block` clause stays, and K = 2, 5 or 6 and any other grid are refused.
  3. **The S1 path v002:** it fixes B1 (only reviewed compares, with AST digests), B2 (u_A bound at the snapshot's primary-anchor field) and B3 (the EA fallback removed). It also applies notes 1, 2 and 4–13.
  4. **The S1_UA_C3T certificates** (EPS, GQ and ρ for `point_identity(S1_UA_C3T)`) come through a CP-1 point extension once u_A is fixed.
- **Consequence, stated now.** Until (1)–(4) exist and are reviewed, S1 cannot run during the campaign, and Phase-1 scoring waits (A133 L188). The S1 reading is a hard gate on Phase-1 reads: only PASS or PASS_AT_ADOPTION_POINT releases them.

## A151: acceptance_q2 v004 passes root verify (0 blocking); it goes to Claude3 for review (2026-10-19 17:09:17Z)

**Build.** Root workflow wf_cde6bc03, at `s4_acceptance_c2/acceptance_q2/`.
- handoff `5ff464cc`, README_V004 `83e3b4bb`, HASHES_V004 `1fadf486`.
- Tests 129/129 in two record runs, and mutation 14/14 caught. The verifier found 0 blocking.

**The four A145 changes, plus one fail-closed precondition:**
- `LO_ADAPTER` pins c3v003 `211a3220`;
- `adopt_lo` requires an exact `core_record` pin;
- `converged_finite_fixed_point is True`;
- the README errata;
- `trusted_source_producers` must contain the b1 evidence `7044e131` (path `offset_b1/current_source_evidence_b1_c2v001.py`). Otherwise the call reads INCOMPLETE, so C1 must list it.

**C1 consequences, applied at H1:**
- the slot-proof producer `cd10cd59` joins the approved list;
- the trusted producers are row producer v003 `67fddd24` and `7044e131`.

**Review.** Claude3 reviews v004, lean.

**UNTESTED, and the deciding tests:**
- real r5 calls: the first real acceptance (TAIL_REANCHOR);
- c3v003 on real inputs: the CP-1 anchor pair.

## A152: how eps_km_s is computed (W-1, a physics-reading ruling under A115 (b)); result-to-values rules; values writer v003 commissioned (2026-10-19 17:23:16Z)

**Basis.**
- Root workflow wf_bccbcac7. Its builder stopped correctly: no code mapped `field_bound` to 43 values in km/s.
- The verifier found the adopted rule, and the fix round built `values_writer_c2/values_writer_c2v002.py` (`38ac8c93`). Tests 123/123 in two runs, mutation 16/16, re-verify 0 blocking.
- v002 refuses every run while ROOT_RULING is unset.

**W-1, ruled before any NGC number.**
- **The rule:** eps_km_s[q] = `srb_rot(S, C, rows)['bound_km_s'][q]`, where:
  - S is the TailState of the call's own `le{final_pass}_rotation` stage. Its digest must equal that stage's `finish.json` `uv_tail.state_digest`, and `S.record.eps_certificate` must equal the point's EPS pin.
  - C is the point's own certificate (field `eps`).
  - rows come from `rotation_rows` (row producer `67fddd24` L171-193) on the call's own `rotation_base_arrays.npz`. **N_min, v_c, column radii and row_columns are all computed from the call's own outputs.**
- This is the same computation that the A146-adopted SRB adapter (`08e9ac0a` L439-440) and A134 Q10 already use. It adds no new knob.
- **Not adopted:** A-1 (v = speeds), A-2 (R_q in place of the column maximum) and A-3 (a declared N_min).
- **Reading, stated now.** eps_km_s bounds the UV-tail truncation error through the **static rotation-law channel only** ("necessary, not sufficient", library L860-871), and the certificate's eps is an estimate (EPS), not a proven sup (L857).
- **A144 R3's guarantee therefore reads:** "certificate noise in the static rotation-law channel". A narrower e_q makes AT-1 stricter, never easier (A48).

**W-2.** The state is the `le{final_pass}_rotation` stage state as the adopted adapter obtains it, found through `passes[-1].rotation` (C-4).

**W-3, result to values.**
- `speeds_km_s` is a list in the values document's `query_ids` order, which must equal the order of the call's final rows (C-7).
- valid[q] = the row's `valid` ∧ the call's `valid` ∧ status COMPLETED.
- member_valid = the call's `valid` ∧ COMPLETED ∧ the call's post-run per-state acceptance (A134 Q2/Q5 and A136 G5) reading ACCEPTED or LO_UNCERTIFIED_TRANSIENT, as A134 allows.
- result_pin = {`out/result.json` path, `finish.result_sha256`}, per A138 V01(b).
- A row with speed None, or with v ≤ 0, gets eps None and keeps the call's reason (C-2). A144 R3 then flags that pair.

**W-4, certificate check (C-8).** The exact schema, `verdict` = CERTIFIED, `certificate is True`, `mode == 'point'`, producer `8972822b`, a full 64-hex `point.key` match, coverage {NGC: [2,91]}, and contiguous shells. A148's "status" means `verdict`.

**C-1 to C-10 are adopted as built.**
- C-1, the row radii, use the call's own column-mean query support.
- The target-free query manifest `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` (`a2936517`) is **named, read-only**, for the radii and order cross-check only. It holds no velocities.

**Build.** Root workflow `values_writer_c2v003`: v002 plus ROOT_RULING pinned to this entry, plus the W-3 values assembler (one tool, from result files to the values file). Claude4 reviews it, lean.

**Erratum E_A136_1.** A136 cites `owned_uv_tail_lapse_v003` L962-985. That file exists (`tail_scheme_impl_c2/driver_r6/module/`, `e733eb1e`), but it is not the pinned library. The NGC driver pins v002 (`2026f2b6`, driver L311), which has the same hash-check logic at L664-674. `_eps_per_shell`, `field_bound` and `srb_rot` are byte-identical between the two. No value changes.

## A153: the NGC per-state LO quantity (Claude3 0216 N2): the A134 readout indicator, with the NGC row tolerance t_i still to be declared (2026-10-19 17:30:21Z)

**Text of record.** `CLAUDE2/NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md` (`9916cb6f`), produced by root workflow wf_a88c2e94: a drafter, three refuters (physics, consistency, code) and a synthesizer. This is a physics-reading change (A115 (b)), ruled before any NGC per-state number exists.

**Adopted:**
- `LO_NGC_K32_CERT_V001` (`07745bbf`) stays the NGC N-test record, the A136 custody pin and the source of the 0.005 and 0.05 numbers. **It is not the per-state quantity:** its share is hard-set to 0, and route A reads g_phiphi.
- **Per-state quantity:** d_i,s = |v_i| * R_i * rho_s * B1_s / 4, the lo_core L165 numerator, in km/s. It is gated as g_s = max_i d_i,s / t_i <= 0.005 in each of the 9 shells, with sum_s g_s <= 0.05.
  - Scope: ALL_CONSUMED_STATES, route-B states included.
  - The A134 Q5 and 0690 readings apply.
  - NGC has no anchor class.
  - The monotone-FAIL rule applies (A48).
- **Scope disclosure, required on every NGC LO record.** The indicator acts on route A's readout channel. It **does not bound** the omitted tail's contribution to the 43 route-B rows through the source: that contribution is UNTESTED, and its deciding test is the 10-component tail successor as a companion call. A PASS certifies the indicator only.
- **Builder spec S1-S13 is adopted as written:**
  - point custody;
  - rho from the A136 G1 producer, with G4 two-process bitwise equality, the 10-key comparison, and the certificate never parsed as rho;
  - state geometry cube 2 with outer cylinder 32, with C4b gamma bits;
  - the S4 tiling rule, with (64,91] read as NOT_IN_STATE_DOMAIN;
  - B1 from manifest arrays or from a digest-checked rebuild;
  - the |v_i| rules (S6) and R_i from the call's own query support (S7);
  - the NGC row contract (S8), with no sigma and no velocity;
  - the inventory, the row-reference review and the NGC handoff;
  - blinding: until the seal, root reads only verdicts and codes;
  - the MUST_FAIL list.
- **Rejected:**
  - theta applied to rho*B0 (R-B) or to d ln v (R-D), because neither carries the (c/v)^2 factor;
  - a gate that passes by construction (R-A);
  - no gate (R-E);
  - sigma, DDO tau, M_T, a_q, the Picard bound, and any newly declared velocity-relative fraction.

**t_i is still open.** It is DECLARED, not COMPUTED, and it is on the Phase-1 critical path.
- NGC sigma is blinded (A141; r3a I-2/I-3), and member_valid needs this verdict before the freeze (A152 W-3).
- The candidates are (a) the call's own `eps_km_s[q]` (A152 W-1) and (b) theta carried into velocity through the route-A identity by a FORMAL derivation.
- Root declares t_i in a following entry, after a short three-lens check, before any NGC per-state number, with a distinct-lineage check.
- **Until then, every NGC state reads `NGC_LO_TOLERANCE_NOT_DECLARED`, and no NGC member is valid.** That is UNTESTED, not a null.

**Builds:**
- Claude3 continues the NGC rho producer, slot proof and rho stage (S2).
- A root workflow builds the NGC per-state adapter, enumerator and handoff (S1, S3-S11, S13). Claude3's rho pieces plug into it.
- Review is by a distinct lane.

## A154: the STAGE0 successor (M-14) passes root verify at c2v002 (0 blocking); Claude3 reviews; its record schema is reconciled with classifier A (2026-10-19 17:31:51Z)

**Build.** Root workflow wf_796d6bd0, at `claude_artifacts/stage0_successor_c2/`.
- **c2v001** (`e015e617`): 42/42. The scope verifier found 0 blocking. The adversarial verifier found 2 blocking:
  - D05: a defect in the STAGE0 record refused the whole freeze through v003g's calibration-record census;
  - D07: a late STAGE0 file voided a registered freeze.
- **c2v002** (module `d260ee30`) fixes both:
  - custody is set only after the STAGE0 schema check;
  - verify and score never re-read a STAGE0 file that was not custody-verified, and read pinned files only through their pinned copy.
- c2v002 passes 62/62 in two record runs (38 MUST_PASS, 19 MUST_FAIL, 5 CONTROL) and 11 independent probes. Re-verify: 0 blocking.
- **TEST (a):** a non-FINISHED STAGE0 receipt completes the Phase-2 freeze with NOT_EVALUATED / STAGE0_RECEIPT_NOT_FINISHED, where v003g's D9 would refuse.
- **TEST (b):** the query block and the alternatives are byte-identical except STAGE0's status.
- **AST:** 102 of 109 v003g functions are identical, and 7 change only on STAGE0 lines.
- **Constants:** only SCHEMA, MODULE_NAME and MANIFEST_KEYS (`stage0_status`) change. Slots `d3859b42` and every other pin are unchanged.

**Review.** Claude3, lean. Pin rule (M-14): the successor is pinned in the seal entry **if and only if** this review returns 0 blocking before the seal entry is written.

**Schema reconciliation (0720).** The STAGE0 status record and the receipts are defined by this module and frozen into the manifest's `stage0_status` block.
- **Classifier A binds STAGE0 through that manifest block,** in the module's schema (README field map).
- Where A's README names a separate root STAGE0 status record, root writes it as an exact projection of the frozen block.
- The new SCHEMA string `FREEZE_MANIFEST_C2V003G_STAGE0_C2V001` must be accepted for Phase 2 when the successor is pinned (M-5 addition 2).
- **Erratum E_A154_1 (Codex1 0148, written 17:34:43Z).** The c2v002 module (`d260ee30`) declares SCHEMA `FREEZE_MANIFEST_C2V003G_STAGE0_C2V002` and MODULE_NAME `prediction_freeze_c2v003g_stage0_c2v002`. Its README agrees. The C2V001 string above is the superseded c2v001 module's. **Classifiers A and B bind the C2V002 strings.** Verified from bytes.

**Open (UNTESTED):**
- the real slots V003 STAGE0 record, which was never opened;
- the rule-(c) receipt format, to be bound to RUNBOOK_V002's receipts (A133 §3 (c));
- "headline first, never preempt" is a launch-path rule and lives outside the module.

## A155: NGC LO row tolerance t_i is declared as candidate (b), theta carried into velocity through the route-A identity at scale R_i, in ratio form (A115 (b); before any NGC per-state number) (2026-10-19 17:51:29Z)

**Basis.**
- A153.
- Root workflow wf_8fdf0c2e: formal, physics and feasibility lenses, plus a synthesis.
- Text of record: `CLAUDE2/NGC_LO_TI_RECOMMENDATION_WF_8FDF0C2E.md` (`cce91ae0`), §3. It is adopted as written, with the P-1 outcome below.

**P-1 (theta provenance), recorded by root from bytes: TARGET_FREE.**
- `ngc_kgrid_fidelity_c2/PREREG_KGRID_FIDELITY_V001.json` (`4c2eefeb`) L2307 defines theta = log1p(h0/c^2), with h0 = Gamma*sigma0^2/(Gamma-1), sigma0 = 11 km/s and Gamma = 5/3 (hi v002:41). That is the HI free-boundary escape threshold, a gas-model constant. This gives h0 = 302.5 (km/s)^2.
- It is not an NGC3198 rotation-curve velocity or error. A141 and r3a I-2/I-3 do not apply.
- theta was built as a potential (enthalpy) tolerance, delta Phi/c^2, so the scale l = R_i is this entry's **declared reading**. It is not theta's own construction. The formula is the same either way.

**Rule TI_B_SCALE_R_V001.**
- The gate, in ratio form, is the evaluated form: g_s = max_i (|v_i|*1e3)^2 * R_i * rho_s * B1_s / (2 * c^2 * theta), with G = sum_s g_s.
  - The thresholds are unchanged: g_s <= 0.005 in each of the 9 shells, and G <= 0.05.
  - This is algebraically the lo_core L165 numerator divided by t_i = c^2*theta/(2|v_i|).
  - t_i is never stored.
- **Inputs:**
  - theta, the certsngc_common_c2v002 L45 constant, pinned by its float.hex bits;
  - c, the state record's `c_m_s`;
  - |v_i| per S6, R_i per S7, and rho_s and B1_s per S2, S4 and S5.
- **Not inputs:** N_min, eps, sigma, DDO tau, targets.
- **Derivation, FORMAL.**
  - From v^2 = c^2 (L'+P)/G': dv/dL' = c^2/(2vG'), and the ratio between the two channels is (c/v)^2.
  - theta is read as a bound on dlnN/dlnR, so delta L' = theta/R_i.
  - R_i G'_i = 1 per the srb_rot precedent. The O(h) remainder is disclosed, not bounded.
- **Row contract (S8, amended).** It holds query ids, R_i, the rule id, theta's float.hex and c's float.hex. **It holds no t_i, no velocity and no sigma.**
  - One contract and one S10 review serve every call whose S7 radii equal it. Both are frozen before the first NGC acceptance.
- **Edge cases:**
  - |v_i| = 0 contributes exactly 0 (flag ZERO_SPEED_ROW).
  - An empty row set reads UNAVAILABLE `LO_ROW_SET_EMPTY`.
  - Bits of theta or c that differ from the contract read UNAVAILABLE `NGC_LO_TOLERANCE_RULE_MISMATCH`.
  - Monotone FAIL holds exactly, because g grows as |v|^2.
- **What a PASS certifies.** At every consumed state, the route-A readout-channel indicator of the omitted tail is at most 0.5% per shell, and at most 5% summed, of the velocity change that a theta-sized change in dlnN/dlnR produces at row i.
  - A153's scope disclosure is carried unchanged.
  - t_i is not a scoring tolerance.
  - (b) is many orders of magnitude more lenient than R-B, because it carries the required (c/v)^2 factor. This is disclosed.
- **Not adopted:**
  - candidate (a), eps_km_s, because it ties LO to AT-1's eps and changes with the EPS record version;
  - min(a, b).
- **MUST_FAIL additions** are as in §3.
- **UNTESTED, with deciding tests:**
  - U-b1, the NGC LO size: the first NGC acceptance;
  - U-b2, the R*G' remainder;
  - U-b3, whether S7's radii equal the a2936517 radii, so one contract serves all;
  - U1, the omitted tail through the source: the 10-component successor.

**Distinct-lineage check.** Codex1 runs items 1-7 of §5, lean and synthetic. The entry stands only if it returns 0 blocking before the first NGC acceptance. Until then, NGC states read `NGC_LO_TOLERANCE_NOT_DECLARED`.

**Erratum E_A155_1 (Codex1 0150: 2 blocking scope statements, both accepted; written 17:56:21Z).** The formula, inputs and thresholds are unchanged. Only the stated meaning changes.
1. **R_i G'_i = 1 is a declared approximation.** The "O(h) remainder" wording is withdrawn. Amplitude alone does not bound R h'/(2(1+h)); Codex1's oscillatory counterexample gives 1 at h = 0. A PASS certifies the indicator normalized under that approximation. The real-row remainder stays UNTESTED.
2. **t_i is the linearized velocity-response scale** under R G' = 1, that is, the derivative response to a theta-sized change in dlnN/dlnR. It is not the exact finite velocity change, which is sqrt(v^2 + c^2 theta/a) - |v|. At |v_i| = 0, t_i is singular, and the ratio's value 0 is its continuous extension, not a finite derivative evaluation.

**PASS now reads:** "at every consumed state, the route-A readout-channel indicator of the omitted tail is at most 0.5% per shell, and at most 5% summed, of the linearized velocity-response scale to a theta-sized change in dlnN/dlnR at row i, under the declared approximation R G' = 1."

Codex1 0150's items 1, 2, 4, 5, 6 and 7 PASS. Item 7 is P-1 TARGET_FREE: the chain prereg → prep literal sigma0_m_s = 11000, Gamma = 5/3 → HI producer → theta, with hex 0x1.ce9660bc22098p-29. Item 3 is resolved by amendment 1. A155 is frozen as amended once Codex1 confirms closure.
**Closure (written 17:57:08Z):** Codex1 0151 reads PASS with 0 blocking on the amended text. **A155 is frozen as amended.** t_i is declared; NGC states move from `NGC_LO_TOLERANCE_NOT_DECLARED` to the A153/A155 gate once the reviewed NGC adapter and the contract review are in place.

**Builds.** The root NGC adapter (A153) evaluates g in this ratio form. If its current build used a stored t_i, a successor replaces it. Values writer v003 is unaffected: eps stays AT-1's noise term only.

## A156: RI45-24 (PAR8-SF1): the r008 frame class at cmd_dry_run L5147 is enumerated and pinned; RI45-25 (ST8-N2): r008's inside-NGC strictness is recorded as intended (2026-10-19 18:08:35Z)

**RI45-24, PAR8-SF1 (Claude4 0104; REVIEW_NGC_V011_CX3R008_C4V001.md `7ff20c1d`, SHOULD_FIX; both refuters reproduced it).** A98 says "Any frame class specific to r008 is enumerated and pinned before closure; there is no blanket waiver" (as quoted from V005 by Claude4 verify_parity_1 L51), and dispatch 0619 (`238858d1`) L15 says "Pin any r008-specific frame class before closure." The A98.1 disposition (`PAR_TB_A98_1_DISPOSITION_CX3V001.json` `a9ae801f`; mapping `ab5afb0e`) pins two r008-specific classes, the L5145 dispatch line and the guard move 9220 to 9329. This entry pins the third, with no code, driver-sha, registry or value change.

- **Class:** `cmd_dry_run` L5147 source line and its caret line.
- **Source lines, verbatim from the driver bytes** (r007 `e4f5864a`, r008 `577f8c94`; each line's bytes follow the colon, indentation included; L5145-5147 are the only lines of `cmd_dry_run` (L5144-5163) that differ):

```
r007 L5145:    code=_ngc_v011_dispatch(_V010_DRY,spec_path,report_dir)
r007 L5146:    rp=Path(report_dir)/'DRYRUN_REPORT.json'
r007 L5147:    if code==0 and rp.is_file():
r008 L5145:    code=_ngc_v011_dispatch(_V010_DRY,spec_path,report_dir,_ngc_post=_ngc_finalize_dry_cx3r008)
r008 L5146:    if isinstance(code,tuple):return code[0]
r008 L5147:    if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():
```

- **Traceback frame text of the class** (source line and caret line, exactly as Python 3.12.14 prints them when `is_file()` raises; Claude4 verify_parity_1 C4, reproduced from the driver bytes at this build):

```
r007:
    if code==0 and rp.is_file():
                   ^^^^^^^^^^^^
r008:
    if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

- **Scope:** top-level dry-run exception source/caret diagnostics only, the scope A98.1 gives its L5145 class; that text also lands in saved direct-call harness tracebacks and in hashes derived only from it (verify_parity_1 VP1-N3). It shows only when `Path.is_file()` raises an OSError that pathlib does not ignore (EACCES, EPERM, EIO, ENAMETOOLONG) after the planner has written the report, or when a `--report-dir` spelling makes the literal path longer than PATH_MAX (VP1-N1). Exception class and text, errno, exit code, stdout, frame count and every emitted file are identical in r007 and r008. `cmd_dry_run` is on no run-mode or stage stack (VP1 C8).
- **Asynchronous exceptions** (VP1-N2, TESTED by proxy, not a finding): an interrupt can also surface the r008 spellings of L5146 (`if isinstance(code,tuple):return code[0]` against r007's `rp=Path(report_dir)/'DRYRUN_REPORT.json'`) and of the dispatch def line L9194 (`def _ngc_v011_dispatch(fn, spec_path, *args, _ngc_post=None):` against r007's `def _ngc_v011_dispatch(fn, spec_path, *args):`). They are pinned here by line and source text, with the same scope.
- **Not waived:** everything A98.1 excludes (values, rows, validity, status, decision branches, exception class or message, refusal reasons, recursion-limit behaviour, new active NGC strict frames, future source changes).
- **Inside-NGC frame classes (a)-(e)** of the closure lens follow from ST7-SF1 and ST7-SF2 and lie outside PAR-TB scope (verify_closure_1/VERIFY.md `a5e8169d` section 4); no entry is needed for them.
- **Record of record for a later parity check:** the disposition `a9ae801f` together with this entry, cited by its section sha256 (the bytes from this heading line to the next line starting "## "), which root records in the next V006 entry. PAR-TB-1 is closed for r008.

**RI45-25, ST8-N2 (REVIEW `7ff20c1d` NOTES): r008's inside-NGC strictness changes are intended.** Inside NGC, r008 raises a typed `NGC_JSON_DEPTH_REFUSED` where r007 raised an untyped RecursionError, and a `final_rows_check` refusal in run mode reads REFUSED (exit 3) where r007 read COMPLETED_INVALID (exit 0). None of the 8 registered NGC specs reaches them; whether a filled step-5 spec can is UNTESTED (deciding test: that call's own dry plan under RI45-13 and its receipt). A REFUSED step-5 call follows A133 section 3 rule (c) (in force from A142): the identical spec is rerun with the RSS cap at RAM and the wall cap doubled, and it is marked invalid only after two identical deterministic failures that are not INFRA. It enters the freeze as a structured failure (RI45-14 list, first_pass.saves[1]): the member and all 43 query rows are kept, each row INVALID with the refusal code as its reason, never dropped (RI45-11 (a)); under A152 W-3 its rows and the member read invalid because its status is not COMPLETED.

## A157: pre-launch pins: the 15 gate documents (M-15 (a)+(1)), root-listed row gates none, and the RI45-14 list (2026-10-19 18:08:50Z)

Pinned before the first step-5 NGC launch receipt (A142 item 6; M-15 (a)+(1); A133 section 2 row 1). Each sha256 below was computed from the file bytes at Mon Oct 19 17:58:16 UTC 2026 (s0_launch_kit_c2 C2V003). The 15 GATE_PIN rows equal GATE_DOCUMENT_PINS_V002.json (`5e688882`), the file the launch kit pins. Root-listed row gates known at launch: none (FORMAL: no REGISTERED_INVALID_ROW_GATE_CX3V001 document exists; a row gate first adopted at RUNBOOK step 4 is LATE).

```
GATE_PIN NTEST_K32_COMPARE_COMPLETE 6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json
GATE_PIN NTEST_N1_RING_RADII 8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json
GATE_PIN ROUTE_B_GL4_NODES ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json
GATE_PIN GQ_NGC_91_MS96 be148bab4d80ef412d55d2011cac2e3a1d44725a0ba21a4d2bf43c7ffbdc1a76 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json
GATE_PIN LO_NGC_K32 07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json
GATE_PIN EPS_NGC91_ANCHOR 1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json
GATE_PIN I1T_NGC_T120L 3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json
GATE_PIN S0_POINT_EPS_SEED efdc430a561ae936d860f85ec050f22a10f17c03aad7ad17fc2150744dcde563 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_968c915bece706ea_C4V002_s0seed.json
GATE_PIN S0_POINT_EPS_J0 8270b6b3eb9daddd01e32f7c6cc0fd143afd6b751ff9ced310ac92ca365586da /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_3d7785669b549d6f_C4V002_s0j0.json
GATE_PIN S0_POINT_EPS_J1 bfac8f57233e904aed30f68594645b5b9c97697e47ce088e9d18e7a8fe4aff1e /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_ab7bf95317b37652_C4V002_s0j1.json
GATE_PIN S0_POINT_EPS_J2 5dd9900a7db31003cb1b1054c156f6ac73b062375bae3a423990e782a2ccfdfc /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_4b9b4ec88eb2d94c_C4V002_s0j2.json
GATE_PIN S0_GQ_BINDING_SEED 903a7d6c88804bb99175ec78927184f210fa1fb07c32c985c294ef0546d0b979 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_968c915bece706ea_C4V002_gqseedA.json
GATE_PIN S0_GQ_BINDING_J0 cc6113ce39adaa3b24154848d099fec693aec15b91f09c3f9ca74299448d5f27 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_3d7785669b549d6f_C4V002_gqj0A.json
GATE_PIN S0_GQ_BINDING_J1 4fc1d744f2d0cb38a08d086aa8c20603bbd3b43c7c27a9a0d0d83665091402ca /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_ab7bf95317b37652_C4V002_gqj1A.json
GATE_PIN S0_GQ_BINDING_J2 934c0a4774b9153e7fbe25d72c743eff529079644f3fdc03ab060dc25833f3e0 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_4b9b4ec88eb2d94c_C4V002_gqj2A.json
ROOT_LISTED_ROW_GATES NONE
```

**RI45-14 list of record** (A133 section 1.4 L78 and section 2 row 1; reviewer Claude4):

```
RI45_14_LIST_PIN FREEZE_EXPECTED_INPUTS_C2V003 454dd3ccb6f9d1056981aa44b24237e12066c43ef8a37753606b783fa3383e9d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/FREEZE_EXPECTED_INPUTS_C2V003.json
```

The list leaves three fields to root, stated here with the pin:
- interior_count = **5**, declared here by root before any result (CHOICE). It is the only operational precedent: the steps 6-7 rehearsal `rehearse_freeze_cx1v001.py` L28 and the v003g review harness L424. It sets how many evenly spaced interior admitted points join the hull, anchor and centroid members (v003g L1245-1250). It changes no tier, because tiers come from the reference member, and it moves only compute and envelope breadth. Phase-2 step-5 duration is recomputed from the actual member count at the Phase-2 selection (A142 item 3).
- spec = **CX2V006**, the tail-era campaign lineage of record (A135 item 7). S0 is identical under both (TESTED), and the engine coordinates are byte-equal.
- notes.A16.1 = "The box-limited band rows are invalid by design (A16.1): `evaluated: true` reads as attempted and refused, not as a zero sensitivity. The NGC3198 slots never enter calibration or member selection, and the members are evaluated at the registered geometry." This is V004 A16 item 4 L68 with its reason as corrected at V004 L228.

RI45-24 entry cited by its section sha256 (RI45-24 recommendation (a)): A156 59a2f1a3eb92701c90d188c03edd9adaf59fc6be16967c2f963e3919c2fbd244

Run root for the S0 calls: `/Volumes/External1/NGC_S0_PHASE1_V001` (the kit's rule: one level under /Volumes/External1 with an NGC_ prefix; no symlinked ancestor; 2,877 GiB free against the 564 GiB needed; S0_RUN_ROOT_C2V001.md). The S0 launch kit is adopted at C2V002 pending Claude3's lean review (0727). Still owed before the seed launch: HANDOFF_PIN S0_SEED (RI45-09), SPEC_PIN S0_SEED_SERIAL (RI45-13), WATCH_PIN MEMORY_WATCH (A135.5) and the V007 adoption pin (RI45-05), all at T0.

## A158: acceptance_q2 v004 is adopted (Claude3 0230: PASS, 0 blocking, 7 NOTEs) as the post-run acceptance handoff of record (2026-10-19 18:15:55Z)

**Review.** Claude3 0230, one lens plus an adversarial verifier that holds. Evidence: `review_acceptance_v004_c3/` RESULT `60db57ec`.
- An honest b1 call reads ACCEPTED end to end, through the real c3v003 `adapt_call_lo` and `adapt_call_srb_rot` and the real b1 enumerator and guard.
- The readings show 0 mismatches over 131,240 combinations (Q3/Q5/Q10 and 0690).
- Root's suite gives 129/129.

**Adopted:** `s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py` (`5ff464cc`), with row producer v003 (`67fddd24`) and writer (`808cfe6a`). It is the A134 Q2/Q3 enforcement point for every tail-ON direct call (HEADLINE11, DIII4, SENS) and for the campaign's post-run acceptance.

**C1 consequences, applied at H1:**
- the approved producers add the slot proof `cd10cd59`;
- `trusted_source_producers` = row producer v003 `67fddd24` plus the b1 evidence `7044e131`.

**NOTEs N1-N7.** They are wording, or unreachable from honest producers, and are recorded. N7 stays UNTESTED, and its deciding tests are:
- the real `validate_current_config`, `produce_current_lo`, b1 export and v005 `consumed_states` on real r5 records: the first real TAIL_REANCHOR acceptance and the CP-1 anchor pair.

## A159: values writer v003a passes root verify (0 blocking after the B1 fix); O-1 to O-3 are ruled; v004 pins the NGC handoff, and Claude4 reviews v004 only (2026-10-19 18:23:49Z)

**Build.** Root workflow wf_98ef4f51, at `values_writer_c2/`.
- v003 (`dd9456bc`) pins the A152 section (`5aee4cc0`) and adds the W-3 assembler. 226/226.
- The verifier's **B1**: v003 let a DDO154-schema acceptance record (handoff c2v004) set NGC member_valid, against A136 G5 and A153.
- **v003a** (`965ed282`) has `MEMBER_ACCEPTANCE_PRODUCERS = ()`, so member_valid is false for every member until a reviewed NGC handoff is pinned. 235/235, mutation 50/50. Re-verify: 0 blocking.

**Rulings:**
- **O-1.** member_valid counts only ACCEPTED and LO_UNCERTIFIED_TRANSIENT. ACCEPTED_PASS_FLAGGED reads false until root rules on that flag (A48). This is adopted as built.
- **O-2.** A134 Q2 governs: no value is used before acceptance.
  - The Phase-1 `valid[q]` is also gated by the point's NGC acceptance reading, ACCEPTED or LO_UNCERTIFIED_TRANSIENT.
  - Until the NGC handoff is pinned, every Phase-1 row reads invalid. That is UNTESTED, not a null.
  - It is implemented in v004.
- **O-3.** The A-4 inclination factor is printed and not applied. A152 is silent, so no new factor is introduced.

**v004, a root build after the NGC adapter and handoff (A153) are reviewed:**
- it pins the reviewed NGC handoff's schema and sha in MEMBER_ACCEPTANCE_PRODUCERS;
- it requires the route `NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE`;
- it applies O-2 to Phase 1.

**Review.** Claude4 reviews **v004 only**, lean, about Wed–Thu, so that it lands before the Phase-1 freeze.

**UNTESTED (D-1 to D-6), with their deciding tests:**
- the reconstructed final-rotation state digest, the relative outdir, and real radii within 1e-9: the first real S0 call and its assembly;
- the NGC acceptance record form: settled by A153's handoff build.

## A160: S1 successors pass root verify; the K=3 certificate and acceptance chain (KS1-KS6) is commissioned, S1_UA_C3T-gated, without weakening A134 (2026-10-19 18:42:53Z)

**Build.** Root workflow wf_344c2082, at `claude_artifacts/s1_successors_c2/`.
- **guard012** `f4656fec` and **launcher013** `620a44da`: 33/33. A POST_S1 batch may overlap the campaign under gate v003's live hold and decide checks and the A133 rule; every other batch is unchanged. Undoing the declared edits reproduces guard011's bytes.
- **The S1-only K=3 wrapper** `e7f52461`: 25/25. K=3 with the CB C3T grid is accepted for the S1_UA_C3T label only, and non-S1 specs are identical to q5b1.
- **S1 path v002a** (lib `f961839b`): 148/148.
  - It covers B1 (reviewed compares only; r14's digests equal r11's for every reused function), B2 (u_A bound at the snapshot's primary-anchor field) and B3 (the EA fallback removed), plus notes 1, 2 and 4-13.
  - The verifier's BLK-1 is fixed: the reader and every launch check re-derive the fill record. An edited branch or a log-only u_A is refused.
- **Verify.** The scope verifier found 0 blocking. The adversarial verifier's BLK-1 is closed in the 'a' build, with 0 blocking after a 435-edit fuzz.
- **Adopted pending Claude4's lean review** (0718).
- **New V6 entry-line conventions** (`**S1 attestation producer (SV7):**`, `**S1 flag ruling:**`) are adopted as the forms root uses.

**The K=3 chain.**
- The per-point certificate chain is K=4-only: custody L111-113, the response producer's literal 4, the CP-1 runner/common/assembler, and certificate guard b1 L94.
- The post-run acceptance path is also K=4-only: lo_core L85-86 and L104, via the adapter c3v003.
- So S1_UA_C3T cannot be certified or accepted as built.
- Waiving per-point certification or per-state acceptance for that call would make adoption easier than A134 Q5 (all 31 points, the POST_S1 calls included) and A150 SV7. **A48 forbids it.**
- **Root commissions KS1-KS6** in one root workflow. **Every K=3 allowance is gated to the S1_UA_C3T identity (CB C3T grid bitwise), and every other spec stays byte-identical in behaviour.**
  - KS1: custody.
  - KS2: the response producer's shells start at the spec's kept K; EPS covers [3,182] and ρ uses the 10-shell partition.
  - KS3: CP-1 runner and common, with row 32.
  - KS4: the registry assembler.
  - KS5: certificate guard b1, where the domain K must equal the identity's kept K.
  - KS5': the wrapper c2v002.
  - **KS6:** lo_core plus the c3v003 adapter plus the acceptance handoff, for K=3 at S1_UA_C3T only.
- **Review: Claude3,** the author of the c3v003/c3v004 predecessors and distinct from root's builder, lean. Codex1 is the fallback.

**Timing, stated now (UNTESTED).**
- u_A is expected about Wed.
- The KS chain must be built and reviewed by Wed. Then the CP-1 row-32 extension (about 0.5 day), then the S1 pair (about 10-18 h serial), then the reading.
- The Phase-1 read deadline is Sat 24 Oct 09:00 CDT. If it is missed, Phase-1 scoring waits (A133 L188). Nothing is relaxed.

## A161: the S0 launch kit C2V002 is adopted (Claude3 0233: PASS, 0 blocking, 11 NOTEs); the D2 order, the rerun path and the V006 discipline during S0 (2026-10-19 19:02:21Z)

**Adopted.** `s0_launch_kit_c2/` C2V002: kit `0ba823f3`, serial launch `d2b7a37b`, twin launch `34181ab3`, kill watch `60ab79db`, record writer `a10965b7`.
- B1 (the A147 L3-03 kind check) is closed.
- Caps, paths, relaunch, M-15 ordering, twin and kill watch are TESTED and fail-closed.

**N1, the D2 order: plural.**
- **All four S0 serials (seed, J0, J1, J2) launch first,** as the gate admits each. They are Phase 1's critical path.
- The twin starts only once the gate admits it with no serial NGC tree in route A. The gate enforces that through MEMORY_HARD (83.7 > 83).
- Root's procedure: the J serials are launched right after the seed's confirmed LAUNCH, never the twin first. The kit's seed-only order check is the floor, and this procedure is the rule.
- The identity verdict matters for Phase-2 step 5, not for Phase 1.

**N3, rerun path.**
- A rule-(c) rerun of an S0 call (RSS at RAM, wall doubled, and for OUTPUT_CAP the output cap raised; A133 §3(c), A141 L1) needs a kit successor, because the caps are constants.
- **Root builds it on demand, at the first such stop, before any rerun.** No deadline-based abandonment.
- The expected outputs (about 50-60 GB) are well under the 136 GiB cap.

**N2 and N4, V006 discipline during S0.**
- **From each M-15 record until that launch's receipt, root makes no V006 write.** The record freezes V006 for that launch root.
- New V006 entries go only **below A157**, so the pin lines never move. Appending keeps the registry same-spec checks honest.
- One launch root uses one kit version (N9).

**Noted:** N5 (add an alert if the kill watch is gone while the twin is alive; root watches), N6-N8, N10 (V007 custody comes through the handoff's V006 pin) and N11 (the A157 fields are bound through the V006 sha in the M-15 record and the freeze).

## A162: NGC per-state LO adapter c2v002 passes root verify (0 blocking); NGC acceptance completion (c2v003) is commissioned; SRB-ROT for NGC is report-only (2026-10-19 19:03:18Z)

**Build.** Root workflow wf_b3bb5eb5, at `claude_artifacts/ngc_acceptance_c2/`.
- **c2v001** (47/47) stored t_i and let an empty row set read PASS (verifier B1; A155 supersedes it).
- **c2v002** pins A155 (`ed6b144b`) and uses the ratio form with no stored t_i. An empty row set reads UNAVAILABLE `LO_ROW_SET_EMPTY`, θ or c bit mismatches read `NGC_LO_TOLERANCE_RULE_MISMATCH`, and a zero speed contributes exactly 0.
- 24/24 MUST_PASS, 33/33 MUST_FAIL, mutation 43/43. Re-verify: 0 blocking.

**Rulings on the open interfaces. They are to be built in c2v003, root workflow, and Claude3 reviews c2v003 only.**
1. **Route-A iterate list.** An approved reader of the route-A sidecar, from the driver code, enumerates the pre-acceptance iterates. The A134 class is ROUTE_A_PRE_ACCEPTANCE_ITERATE.
2. **S5 rebuild export.** Every consumed non-accepted state is rebuilt post-run from its own roster, and admitted only if its digest equals the recorded `state_digest`. That gives B1 per state. The rebuild time is measured on the first call (U4).
3. **The NGC row contract (A155 S8 amended)** is built by root from the manifest `a2936517` radii and order: query ids, R_i, rule id TI_B_SCALE_R_V001, θ hex, c hex. **One contract.**
   - Its S10 row-reference policy review is by **Codex1**, single pass, bound to the contract's sha, after the three DDO Q4 reviews.
4. **Execution facts.** The NGC handoff carries {fresh_call, resumed, retried, route_a_completed_normally, run_root} from the call's own records, by the v005 `fresh_scope` rule, as A138 V01(b) does for DDO. Anything not established refuses.
5. **SRB-ROT for NGC: report-only.** No τ exists, because NGC σ is blinded. The SRB-ROT bound is exactly A152's eps_km_s, AT-1's noise term. It is computed and recorded, and it never gates. That is not a weakening: A134 Q10's τ_i/10 gate is DDO's, and there is no registered NGC τ.
6. **S2 ρ:** pins Claude3's NGC ρ c3v002 when root's review of it passes.

**NGC acceptance = the A153/A155 LO gate + custody + execution facts.** Values writer v004 (A159) then pins the c2v003 handoff's schema and sha.

## A163: RI45-14 list review (Claude4 0223: 2 BLOCKING, accepted); C2V004 commissioned with a slot-geometry check before S0; erratum E_A157_1 on interior_count (2026-10-19 19:08:11Z)

**Accepted.** Claude4 0223 (lens plus verifier; `review_ri45_14_c4/`).
- **B1, notes:** in the fixed-distance mode, `write_freeze_manifest` needs `notes.ngc3198_slot_sensitivity` and `notes.structural_assumptions` (SA-BH-01, SA-REACH-01, A18). The C2V003 notes would refuse.
- **B2, spec:** a spec built from CX2V006's placeholder NGC slots puts every member at the placeholder inclination, which the A16 slot checks refuse.
- Both fixes are target-free. Under A133 L185 they are due before the first Phase-1 NGC launch.
- **Root workflow `ri45-14-c2v004-and-slot-geometry`** builds FREEZE_EXPECTED_INPUTS_C2V004:
  - notes = a deep copy of slots V003's `notes_block_for_manifest`, plus a root A18 structural_assumptions entry;
  - the spec from CX2V006 + slots V003 `ngc3198_slots` through the COORDINATE_ADDENDUM mode, with its engine part proven equal to the campaign's.
- **The same workflow first checks, dry, that the S0 point handoffs and filled S0 specs carry the registered geometry (13.8 Mpc, 72 deg) and not the placeholder.** S0 launches only with the verdict S0_SPECS_OK.

**Erratum E_A157_1 (Claude4 0223 N1).** A157's rationale for interior_count = 5 ("It changes no tier … moves only compute and envelope breadth") is corrected.
- The value 5 stands.
- The member set also moves the headline distribution (min, median and max of the per-member counts), envelope validity (one unevaluated member voids every envelope row, so NEAR reads NOT_AVAILABLE on all 43 rows) and the AT-1 scope.
- A157 itself is not edited, so its pin lines stay fixed (A161).

**Also folded into C2V004:**
- **N2:** interior_count = 5 is bound in both phases, at the phase1 handoff's v003g selection and at the Phase-2 roster builder.
- **V-N1:** Phase-2 `allow_incomplete` is True if and only if a rule-(b) or rule-(f) UNEVALUATED member exists (FREEZE_INCOMPLETE), and False otherwise.

Claude4 re-reviews C2V004 as a delta.

## A164: the three Q4 row-reference policy reviews are APPROVED (Codex1 0153-0155), and C1 trusts them (2026-10-19 19:12:45Z)

**Row contracts.** Root workflow wf_441f0df4, at `q4_row_contracts_c2/`. The hashes are computed by the pinned custody_cx2v002 `6810b7c3`, and the independent verify passed 81/81 with 0 blocking.
- **DLO** D = 3.9810717055349722: `fefbfe66…578e`
- **D404** D = 4.04: `f9bb13a9…ebea`
- **DHI** D = 4.111497211045223: `a14024ea…5b14`

**Approvals (Codex1, distinct lineage).** Each is verdict APPROVED, 0 blocking, with policy `A134_Q4A_OWN_CALL_MAX_ABS_OVER_EVERY_RECORDED_READOUT`. sha256 from bytes:
- 0153 DLO `07eee40b7fe672716c189ff79ec87c2dd94422eb3dadc0fb88d9c88c19db2ef2`
- 0154 D404 `6c9475e1e65161f5c67bbee4f94c813291167f1e19a59a52528f610ebbc87ca7`
- 0155 DHI `f5b6c66e6fadf5fc20e9a7df767819da6e10eb24e4c75c02911c5486b13ccb23`

**C1 at H1** lists these three shas in `trusted_row_policy_review_sha256`.
- Whether lo_core L225-231 accepts the review schema `CODEX1_Q4_ROW_POLICY_REVIEW_V001` as written is UNTESTED. The deciding test is the first real TAIL_REANCHOR acceptance; a refusal fails closed and root rules.
- **Update (written 19:13:09Z), FORMAL from bytes:** lo_core `12d36305` L225-231 reads the review through `reference(review_ref)`, with no schema argument. It checks only that the sha is in the trusted list, that `verdict == 'APPROVED'`, and that `row_contract_sha256` equals the call's custody value. All three approvals satisfy this. The row references must carry `policy_review` = {path, sha256} of the matching approval; root's C1 supplies those pins to row producer v003.
- The NGC row contract's review follows A162.

## A165: CP-1 restarted with a 26 GiB reserve on a fresh out-root, at the principal's prompt to use the Mac's memory; this changes timing only (2026-10-19 19:16:55Z)

**Basis.** The principal asked that the Mac's memory be used, noting that it handles memory well and can swap to about 1 TB of disk. Root measured with vm_stat at 19:14Z:
- free 39.3 GB, inactive 39.1 GB, file-backed 16.7 GB, speculative 1.2 GB, purgeable 1.8 GB;
- the compressor holds 22.4 GB in 9.7 GB;
- swap 1.8 GB of 3 GB.

CP-1's floor counts only free plus speculative memory, so it was conservative by at least the reclaimable file cache. Even a worst-case KHI iteration spike (+37 GB) plus 4 CP-1 workers (8 GB) fits within free memory plus file cache. Swap only slows a run and never changes a value, because every computation is deterministic.

**Action.**
- The Phase-A scheduler pid 18346 (out-root `cp1_run_c3v004`) was stopped by SIGTERM. It had started **no worker and no point**; its out-root holds only its WAIT log, which is kept and superseded. A134 N2 is respected, because no worker was live.
- Phase A was restarted in a **new out-root `cp1_run_c3v004b`** with `--r2-spike-allowance-gib 26` (the builder's original proposal). Every other A146 and run-sheet setting is unchanged, including the gate pin 0146 `66c54c76`.
- Scheduler pid 6974, run_id `20261019T191632Z_6974`. SCHEDULER_START reads rho_gate OPEN.
- **The anchor worker started at 19:16Z** (PHYSICAL_FLOOR_OK: 37.6 GiB available against 32.0 required).

**Unchanged:**
- the swap-growth hold (512 MiB) still pauses new starts;
- the A130 watch still alerts at more than 95 GB footprint or more than 8 GB swap, and the A133 SIGSTOP lever applies;
- the two-phase anchor check (A146) stands;
- the registry assembler reads `cp1_run_c3v004b`.

## A166: principal's direction to stop micromanaging the Mac's resources; memory gating is removed, RSS caps rise to RAM, and only hang, disk and correctness rules remain (2026-10-19 19:21:38Z)

**The principal's direction (verbatim):** "can we stop micro managing the macs resources? The macs tend to do that very well on their own when jobs are just run." It follows the 19:14Z vm_stat reading and A165.

**Ruling. This is timing-only: no computed value can change, because every computation is deterministic and swap or compression affect speed only.**

**Removed for every launch from now on:**
- the machine-gate memory admission (sched v002/v003 d1, d2, knee and hard limits, NGC/twin classes, the twin hold, the route-A cap);
- the A133 §1.4 103 GB rule;
- the A143 D2 memory ordering and the A147 L3-03 kind check (both existed only to make the gate classify);
- CP-1's physical floor and swap hold (from Phase B on);
- the S1 overlap memory condition (guard012).

**Jobs now start as their own design and order allow.** macOS schedules memory, compression and swap.

**Per-call RSS caps rise to physical RAM, 137,438,953,472 B, for every new launch:** DDO 64 GiB becomes RAM, and the NGC serial 32 GiB becomes RAM.
- A cap stop is value-relevant (A133 (f)), so a memory cap must never kill an honest run.
- Raising a cap before launch changes no value.
- Under A133 (c), the RSS-at-RAM rerun form is now the first-run form.

**Kept, because they are not memory micromanagement:**
- the per-call **wall caps**, which guard against hung runs (A133 (c) reruns with the wall doubled);
- the per-call **output caps** and the **disk admission guard**, because a full disk fails runs;
- every correctness and custody rule (M-15, pins, kill of the twin after iteration 1 to save compute, identity comparison, and so on).
- The A130 memory and swap **watch stays passive: alerts only, with no automatic throttling**. Root intervenes only on an actual failure.

**Running now, left untouched:**
- step 2 (V007 R2, under its sealed launch);
- CP-1 Phase A (pid 6974; A134 N2 forbids restarting with workers live).
- CP-1 Phase B starts with allowance 0, margin 0, per-worker 0, k 8 and swap hold effectively off.

**Builds, before their first use, in one root workflow:**
1. **sched v004:** the campaign runs on the R9 config with the original campaign v005, which has no memory gate. It changes only: output cap 80 GiB, wall cap (A140 N4, from the step-2 receipts), RSS cap = RAM, disk guard. The direct-batch params C2V004 drop the hold predicate and the memory admission. Claude4 reviews the delta before W1.
2. **S0 kit C2V003:** launches root_monitor directly, with no gate admission or kind check, RSS = RAM and the twin free to start after the seed. Claude3 reviews the delta before the first S0 launch.
3. **guard013:** a POST_S1 overlap with the campaign is admitted with no memory condition. Claude4 reviews it in place of guard012, along with the S1 path.

## A167: the NGC rho gamma route (0216 N1; Claude3 0238 W4): the spec route, the call's own gamma_eff; 0717 R5 N1 is reversed; NGC rho c3v003 (2026-10-19 19:23:15Z)

**Facts (Claude3 0238; synthetic, TESTED).** The honest seed and J0 records read `spec_route_gamma_eff_bits_equal = false`: s·(ge·EB) (filler L294, the γ the call actually runs at) differs in the last bit from the θ-route (s·ge)·EB that c3v002 binds. J1 reads true. Under A153 S3 C4b, which compares the state's `gamma_eff` with the ρ record bitwise, honest NGC states at those points would read `NGC_GAMMA_ROUTE_BITS_DIFFER` (custody UNAVAILABLE), and no Phase-1 member would be valid.

**Ruling.** The NGC ρ producer binds **the spec route, the call's own γ_eff = s·(ge·EB)**, exactly as the DDO route does (0216 N1). The θ-route bits are recorded as a diagnostic only.
- Per-state LO acceptance certifies the call's own states, so ρ must be at the γ those states carry. C4b then compares bitwise, exactly, with no tolerance.
- **0717 R5 N1 (θ route, to match the EPS Binder) is reversed.** The EPS records (Claude4 S0, θ route) stay as they are. Their custody is the point-key pin, not γ bits (A148 W-4). The 1-ulp γ difference is recorded on the EPS side as a diagnostic.
- This changes no registered setting (A136 G2), no threshold and no reading. It is ruled before any real ρ or NGC number exists.

**Build.** Claude3's NGC ρ **c3v003**: the spec-route γ binding, plus W1 (the proof compares the record's γ flag with its own `derive_point`), W6 (the basename refusal comes before any realpath or lstat) and W7 (a producer Refusal inside the stage is CAUGHT, so a record or a clean refusal is written). The schema strings move to `*_C3V003`. Root reviews c3v003 by workflow. The NGC acceptance S2 interface (A162) pins the c3v003 schema and shas.

**R2-R4 at that review:** the NGC ρ registry, the approved producer and slot-proof shas, the seed pair (a, b), the `--allow-rho` pin and the per-point spec pins from the S0 launch registry.

## A168: classifier A c4v003 is verified (Claude4 0225: 0 blocking, 409/409); root's text choices F1, F2 and V-N1 and the contracts C1-C9 (2026-10-19 19:23:42Z)

**Object.** `classifier_a_c4/build_c4v003/`: `classifier_a_c4v003.py` `394a8b61`, HASHES `96ef2edc`, VERIFY `87def25f`.
- It binds phase1 v003b `7d891ff7` (with at0b `values_sha256`) and the STAGE0 successor `d260ee30` (schema `FREEZE_MANIFEST_C2V003G_STAGE0_C2V002`).

**Root rulings. Classifier B shares every one.**
- **F1.** In a Phase 2 without the successor, the STAGE0 root record is `STAGE0_STATUS_RECORD_C4V003`, read **vacuously**: the reason is NO_SEALED_SUCCESSOR only (Claude4's recommendation).
- **F2.** A frozen manifest whose schema is not the one the seal names for that phase reads FIELD_DEFECT_OUTSIDE_ROWS for every other field, and TWIN_INPUT_DEFECT for the block (A's reading, OC-36). It is named in the seal entry.
- **V-N1.** A block from the module's exception path (`STAGE0_RECEIPT_RULE_EXCEPTION`) is taken at **the module's own reading**, NOT_EVALUATED_BEFORE_FREEZE [RNF, NSS]. The classifier reports the producer of record and does not reinterpret it. This is a small c4v004 change, with a narrow verify.
- **F4, confirmed.** RECEIPTS_AFTER_STEP4 is encoded as FINISHED receipts written after `step4_start_utc` (OC-49). This is the rule of record.
- **F10 and F7.** Contract changes **C1-C9 are re-adopted** in the 0720 form, with C7 named `STAGE0_STATUS_RECORD_C4V003`. It is deliberately distinct from the module's own input record `STAGE0_STATUS_RECORD_C2V001`.

**Seal.** The classifier-bearing SEAL CANDIDATE names c4v004 once its narrow verify passes, or c4v003 if V-N1's change is not ready by the write freeze.
- If the slot-geometry check (A163) needs a phase1 successor, both classifiers bind its sha as a pin delta.

## A169: RUNBOOK_V002 and the roster builder c2v005 pass root verify (0 blocking); G29 as ruled; C41-C45 confirmed; Claude4 reviews c2v005 (2026-10-19 19:28:40Z)

**Build.** Root workflows wf_751cc9f3, wf_c6b0d245, wf_93e2b8bd and its successor, at `runbook_v002_c2/`.
- roster builder c2v005 `653ced76`, RUNBOOK_V002_C2V005 `b34f294a`, README `2a4165bc`.
- 149/149 in two byte-identical record runs. The verifier found 0 blocking.

**Each closed defect:**
- R1-R3: re-rolls, receipts reused across calls, and ledger resets;
- cut records shared across calls by hard link or byte copy;
- OTHER calls' files;
- G29 residence;
- C38 checked over all call pairs.

The records are in classifier A's schemas: `GATE_STATUS_LIST_C4V001` and `TSR_FLAG_RECORD_C4V001` (ROOT_TSR_FLAG_RECORD_V002 `c9d8ab45`).

**Root confirms:**
- choices C1-C45 as built, including **C43**: results do not get the "not inside another call's run dir" rule, because the G29 ruling names cut records and C38 covers FINISHED results.
- **G27:** the launch registry schema `STEP5_LAUNCH_REGISTRY_C2V003`, fed from the S0 kit's registry.
- **G28:** a ledger root outside the build directory, which root fixes at the first build.

**Disclosed gaps.** No rebuild; each would need a producer-side binding key (G29 item 4).
- A byte copy, or a re-serialized copy, of another call's cut record written into a call's own run dir still builds.
- Residence is checked by realpath string, so a case-variant or firmlink spelling of another call's run dir is not caught (verifier NOTE 1).
- Honest producers write each cut record once, into the call's own run dir. These need deliberate forgery and are recorded, not built against.

**Review.** Claude4 reviews c2v005, lean, before the Phase-1 RUNBOOK step 4 (about Fri).

## A170: the S1 successors are adopted (Claude4 0229: 0 blocking; the guard013/launcher014 delta also 0 blocking); G13-N1 ruled (2026-10-19 19:43:00Z)

**Adopted** (`s1_successors_c2/`):
- **guard013** `593bebb6` in place of guard012: the POST_S1 overlap carries no memory condition (A166);
- **launcher014** `5d6af4a7`: only the guard pin changes;
- **the K=3 wrapper** `e7f52461`;
- **S1 path v002a** (lib `f961839b`).

Under each, K=3 is reachable only through the S1_UA_C3T identity, non-S1 behaviour is AST-identical, and B1-B3 and BLK-1 are closed.

**G13-N1, the launcher ramp (`memory_pressure` free of at least 25%): it stays, as the launch packet's own design.**
- It is effectively non-binding. `memory_pressure` read 85-88% free all day, including at the 95 GB footprint peak, and guard013 L371-373 requires the plan's `route_a_admission` (free 25, poll 60, ramp) to match the config's.
- Removing it would mean changing the guard, the launcher and the params together.
- **Trigger:** if the ramp ever holds a start for more than 10 minutes, root commissions that three-part successor.
- **The sched v004 direct params (A166 item 1) must keep `route_a_admission` as it stands** (free 25, poll 60, ramp, max_active 3). Root checks this in the sched v004 result before adopting it.
- launcher014 `runtime_settings` (nice ≥ 10 and single-thread BLAS) stay. Single-thread BLAS is a determinism guard.

**Notes, ruled:**
- **N1.** S1_UA_C4T cannot run before the C3T registry entry exists (lib L735, L794). The procedure text is corrected: both S1 calls wait for KS and row 32.
- **N7.** S1-B (A150 R-S1-1) cannot be filled by lib v002a, and its point lies outside the K=3 scope. **A successor (lib plus the K=3 scope for the S1-B identity) is commissioned only if u_A reads AT_ANCHOR**, before any Phase-2 step-5 read.
- **N8.** KS5′ admission needs a lib successor or a manual admission override. Root takes this into the KS chain (A160) result.
- **N10.** Byte and path stability of every fill input becomes a KS4 requirement.
- N2, N3, N12 and N13 are noted.

## A171: the RI45-14 list C2V004 passes root verify (0 blocking); the A163 slot-geometry check reads S0_SPECS_OK, FDPLAN_OK and FREEZE_SPEC_PLACEHOLDER; the spec of record reaches the freeze through the RUNBOOK, with no phase1 successor (2026-10-19 19:58:19Z)

**Object** (`s0_launch_kit_c2/`; root workflow `ri45-14-c2v004-and-slot-geometry`: check, build, independent verify; every sha from bytes):
- FREEZE_EXPECTED_INPUTS_C2V004.json `54997f946b85150ea76cf14485c26ccd5d67227d80ddb7c2aaa05011c887a3ce`;
- FREEZE_SPEC_OF_RECORD_C2V004.json `e2a7650e166a9230138ffd16453ac8fdabab41a8695169844940c4c061a894ec` (file sha = the list's canonical sha);
- NGC3198_GEOMETRY_TRACE_C2V004.json `c1ac10f8`, SLOT_GEOMETRY_FINDING_C2V004.md `60bb6145`, README_RI45_14_C2V004.md, HASHES_C2V004.txt (14 entries re-verified).

**CHECK (A163 L1406), re-derived dry by the verifier:**
- **S0_SPECS_OK.** The 8 S0 and 6 F call specs carry 13.8 Mpc / 72 deg from slots V003 `d3859b42`, through POLICY and filler `ec417e76` L292, L297-298. A163's S0 condition is met.
- **FDPLAN_OK.**
- **FREEZE_SPEC_PLACEHOLDER.** phase1 `freeze_spec` (v003b L432-440) builds from the CX2V006 placeholder (70 deg), but it reaches only `select_representative_points`, which reads engine fields only. Members are canonically equal under both specs (D-09; engine part `54120a12`).

**Verify: VERIFIED, 0 blocking.**
- B1 notes (canonical `56ac5c64`) and the B2 spec of record rebuild independently from the source bytes.
- Synthetic `write_freeze_manifest`: FREEZE_INCOMPLETE in Phase-1 shape and FREEZE_COMPLETE in Phase-2 shape. Both pass `verify_freeze_manifest`, at 13.8 / 72 with A18-ROOT-V004.
- Gate calls 9/9; kit dry run D-01 to D-10 as expected; both self-checks exit 0.
- **The verifier's one UNTESTED item is TESTED-POSITIVE by root** (19:56Z, boolean output only): `exact_alternative_declarations`, which is the writer's `alternatives` input, equals slots V003 `alternatives`. This is the comparison v003g `_bind_alternatives` makes (L2475-2487). No other slots key was printed.

**Ruling: the spec of record reaches the freeze through the RUNBOOK, with no tool change.**
- Root saves FREEZE_SPEC_OF_RECORD_C2V004.json at RUNBOOK step 1a/1b. It passes that file to every v003g call that takes `spec`: selection (1a), the PLAN (1b), steps 2 and 7, `evaluate_sensitivity`, and `write_freeze_manifest` (step 8).
- Check IC-P1-MEMBERS binds the phase1 members to the freeze selection's (log_index, role, order).
- **The optional phase1_c2v003c hardening is not commissioned.** It is defence in depth only, and it would add a pin delta to both classifiers (A168 L1519). So the A168 contingency does not fire, and both classifiers keep phase1 v003b `7d891ff7`. Claude3 0237 N3 (at1 refuses an L1 from another module) needs no action.
- The residual hazard (notes built from the placeholder spec pass A16.1 at 70 deg, because its `reference_value` is null) is closed by K3: the notes are passed literally as the slots V003 block.

**Pin.** C2V004 is BUILT_NOT_PINNED. Claude4 reviews the C2V003 to C2V004 delta (A163). On PASS, a root entry below this one pins it as RI45_14_LIST_PIN C2V004, superseding A157's C2V003 pin `454dd3cc`; A157 is not edited. A133 section 2 row 1 ("the RI45-14 list fixed") then holds for S0.

**Disclosure.** The verifier read V006 unpinned while A170 was being inserted (`13fc80c2` to `b2b3ad7f`). Every line the list cites still holds.

## A172: the A166 builds: sched v004 (max_concurrent is the campaign's design value 8), S0 kit C2V003 (adopted with two fixes), and the guard013 re-verify; erratum E_A170_1; the step-4 packet's memory terms are removed (2026-10-19 19:58:19Z)

**sched v004** (`sched_s45_c2/v004/`; HASHES `ab9561d5`; config `cbc36b7a`, DBP C2V004 `7c3ceae5`).
- **Results.** Build 35/35. Verify: 0 build defects, physics 78/78 pins, numerics `4b2a5a87` unchanged.
- **max_concurrent: 8, the campaign's own design value** (LAUNCH_V005.md L182; RUN_CONFIG_DDO154_V005.json L78; confirmed from bytes).
  - v004 carried R9's 1, because it read A166's leaf list literally. At 1, the 120-call campaign runs serially: about 699 h, against about 235 h at 6.
  - At 1, any wave of more than about 7 calls would also halt at the 48 h campaign wall cap (campaign L250; parent L2731-2732, L3392).
  - At 8 (any value of 5 or more), the CPU process budget of 17 decides concurrency, which is the design.
  - This is a scheduling leaf only. The cache id does not read it, and no value changes.
  - **Build sched v004a with this one leaf.** W1 needs only this config, so it is built and reviewed first.
- **orphan_wait.cap_s = wall + 600 s: ratified.** Otherwise parent L2694-2707 reports ORPHANS_STILL_RUNNING during a legitimate call.
- **DIII max_active = 4**, its call count (inside the guard's 1-6 range), not the 3 the build chose. It goes into the DBP successor below.
- **Noted:** v003's scope rule (no direct batch while the campaign or the NGC loop runs) is gone. The packet's core-priority attestation (guard L333) remains.
- **The wall cap of 100800 s stays provisional** (A140 N4). At W1, root rebuilds from the step-2 receipts by the tested Y04 path, in which only the wall, the orphan wait and the notes move in the config. Root checks that rebuild by leaf diff, and Claude4's v004 review covers the path.

**S0 kit C2V003** (`s0_launch_kit_c2/`; HASHES `61a03d00`; kit `e58c8605`).
- **Results.** Build 26/26 MUST_PASS and 73/73 MUST_FAIL in two runs. Verify: PASS, 0 blocking.
- **C1, adopted with the N1 fix.** C1: launch-check decides LAUNCH or MISLAUNCH, and kills a mislaunch.
  - The problem: launch-check could read the monitor's launch record between its create and its write (`_write_x` L88-92). An empty record reads MISLAUNCH (TESTED), so an honest run could be killed.
  - The fix: launch-check waits until the record parses, bounded at 300 s, before deciding. A parsed mismatch is a MISLAUNCH at once. A record still unparseable after 300 s is a MISLAUNCH.
- **N4, the twin's RSS cap.** root_monitor sums ps RSS over the process tree (L47-74), so shared pages count once per process and the sum can exceed RAM.
  - To keep A166's rule that a memory cap never kills an honest run exactly, the twin's cap is RAM × (the maximum process count of its tree, read from the driver bytes).
  - Serials stay at RAM (one process; measured DDO peak 32.6 GB).
- **N2, the step-2 receipt precondition, stays.** A135 item 5 labels it Memory, but S0 needs the step-3 verdict and the V007 pin (RI45-05), which follow step 2's last receipt anyway. It never delays S0, so it is kept as a sequence check.
- **N3, the watch-check, stays.** It checks only that the passive A130 watch is running.
- **Build S0 kit C2V003a** with the N1 and N4 fixes. Claude3 reviews C2V002 to C2V003a as one delta before the first S0 launch.

**guard013 re-verify (the A166 root workflow): 3 BLOCKING, measured against A166 end to end.**
- **Items 1 and 2** are G13-N1, which A170 ruled "kept as design":
  - guard013 L371-373 binds the 25 % `memory_pressure` ramp;
  - launcher014 `decision` (L37-38) waits on it with no deadline, and never starts a call when the reading fails (`memory_free` returns None).
- **Item 3 is new. Erratum E_A170_1.** A170 adopted guard013/launcher014 together with S1 path lib v002a `f961839b`. Lib v002a is incompatible with them (confirmed from bytes):
  - it refuses any plan that does not use guard012/launcher013 (L1092-1093, `S1_PACKET_NOT_GUARD012_LAUNCHER013`);
  - it runs its own memory gates on every S1 launch (L1154-1210): gate v003 `hold_check`, the warm-up, `decide`, the r5 route-A allowance, the A133 103 GB rule and `MEMORY_PRESSURE_FREE_BELOW_25`;
  - in dry mode it passes `_overlap_gate`, which guard013's `validate` no longer accepts (TypeError).
  - So guard013 cannot be reached from the S1 path, and A170's adoption of the pair does not hold for S1 until a library successor exists. No S1 call was planned or launched, so nothing ran on the wrong pair.
- **G13-N1 is re-ruled, superseding A170's "stays", because of new facts:**
  - a library successor is needed anyway, and it must re-pin the guard and launcher;
  - with max_concurrent 8 and swap allowed, `memory_pressure` can fall below 25 %, so the ramp's free-% term would no longer be non-binding.
  - Removing it now costs one review. Removing it on A170's 10-minute trigger would cost a stalled S1 overlap.

**Commissioned: the step-4 packet A166 set.** It is one root workflow, with each part verified. Claude4 reviews it before the first direct batch or S1 call.
- **sched v004a:** the max_concurrent leaf. Built first.
- **guard014:** guard013 with the memory fields of L371-373 removed (`minimum_free_percent`, the `memory_pressure` source, `first_case_memory_exemption`).
  - The first-iteration ramp stays. It is not memory-only: launcher L125 also fails fast with PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION.
  - Every custody check stays.
- **launcher015:** launcher014 with `memory_free` (L31-36), its call (L123) and the free term in `decision` removed.
  - max_active (packet design) and the ramp stay.
  - nice ≥ 10 is dropped (A166; no value effect).
  - Single-thread BLAS stays, as a determinism guard.
  - It pins guard014.
- **S1 path lib v002b:** lib v002a re-pinned to guard014/launcher015.
  - The L1154-1210 gate block and `gkw` are removed, and so is `/usr/bin/nice`.
  - L1198 (`S1_CAMPAIGN_ROUTE_A_TREE_WHILE_ATTESTED_INACTIVE`) is a custody check and stays. It reads the process table directly instead of the gate's probe snapshot.
- **DIRECT_BATCH_PARAMS_S45_C2V004B:** C2V004 with the `route_a_admission` memory fields dropped (as guard014 requires), DIII max_active 4, and RSS = RAM.

## A173: classifier A c4v004 is verified (Claude4 0233: 0 blocking, 476/476) and is the classifier-bearing seal candidate; OC-54 is ruled at A's form; OI-A1 (Claude4 0228) is ruled (a): every root-written record carries `schema` (2026-10-19 20:05:54Z)

**Object.** `classifier_a_c4/build_c4v004/`:
- `classifier_a_c4v004.py` `e92aa30e22b98fea6c6e517702c02f77c43bfe429f69f8e0392963c94edc4cb0`;
- HASHES `6385e368` (587/587), SUITE `ab350d42`, VERIFY `df2a5a10`.
- V-N1 (A168) is applied: a successor block from the module's exception path is read at the module's own reading, NOT_EVALUATED_BEFORE_FREEZE [RNF, NSS].
- The output schema is unchanged apart from one new defect word, `BLOCK_EXCEPTION_PATH` (27 → 28).
- Under A168, the classifier-bearing SEAL CANDIDATE names **c4v004**.

**OC-54, the diagnostics before the exception entry: A's form stands, with no c5 build.** A leaves the prefix unchecked, and classifier B shares that rule.
- **The honest set, from the module bytes** (STAGE0 c2v002 `d260ee30` L3713-3757, L3841-3843). Every diagnostic `_stage0_apply_record` appends before L3752 is followed by `return`, so only the sealed-successor stage can leave a diagnostic before an exception. The prefix is a function of the block's own fields:
  - `step4_start_utc` null: no prefix;
  - `sealed_successor` null: `STAGE0_SEALED_SUCCESSOR_NOT_NAMED`;
  - `sealed_successor` sha different from `successor_module_sha256`: `STAGE0_SEALED_SUCCESSOR_IS_NOT_THIS_MODULE`;
  - otherwise: no prefix.
- **Why there is no tightening.** The exact check would only change the reading of forged blocks, and those read the same [RNF, NSS] under either rule. STAGE0 on this path is NOT_EVALUATED and is never scored, so no physics reading depends on it. Building custody machinery for no reading change is what the 2026-10-15 direction rules out.
- **What B must not do.** B must not require the diagnostics to be the exception entry alone. That would read honest blocks as TWIN_INPUT_DEFECT. The honest set above is recorded so that B's builder can test against it.
- **B also shares:** OC-50 to OC-53, OC-55, OC-56 and OC-59.

**OI-A1 (0228): ruling (a).**
- **The rule.** Every root-written record carries `schema` set to its contract name, with exact key sets, as classifier A's code has always required (`394a8b61` L724, L669-671, L424, L581, L1941, L2436, L77). This matches every v003g, phase1 and STAGE0 record in the program.
- **The current mismatch.** roster_builder_c2v005 L1418-1421 accepts a gate list only as exactly `{gates}`, and `ROOT_TSR_FLAG_RECORD_V002` `c9d8ab45` has no `schema` key. Classifier A would read both honest records as defective (GATE_STATUS_LIST_DEFECT, TSR_FLAG_TABLE_MISMATCH).
- **Commissioned (root workflow):**
  - **roster builder c2v006:** writes `schema` on the gate list and the TSR record, and `check-gate-list` accepts exactly `{schema, gates}`. No other change.
  - **`ROOT_TSR_FLAG_RECORD_V003`:** V002 plus `schema: TSR_FLAG_RECORD_C4V001`. It supersedes V002 for the seal.
  - Claude4 reviews the c2v006 delta inside its RUNBOOK review (A169). Claude4 also publishes the contract text with the `schema` key shown in every record (wording only). Classifier B requires the key.

**N6 (taskpolicy), confirmed.** A166 removes `taskpolicy` from helper runs entirely. There is no breach.

## A174: CP-1 Phase A passes the A146 fail-closed check at the anchor; Phase B is launched with the A166 settings; the anchor EPS review goes to Claude4 (2026-10-19 20:20:59Z)

**Phase A** (scheduler pid 6974, run `20261019T191632Z_6974`, `--points 1,2`, out-root `s4rc1_c3/cp1_run_c3v004b`) ended DONE at 20:19:41Z with both points exit 0 and no stop.

**The anchor (TAIL_REANCHOR `8ad6ca4e…`), read by root:**
- **EPS cross-check: AGREE.** max_rel 1.62e-8 against tol 1e-3 (`ANCHOR_EPS_CROSSCHECK_…_tol0p001.json` `a2ace431`).
- **ρ pair (`ANCHOR_RHO_PAIR_8ad6ca4e867854da.json` `ae32d298`):**
  - the wrapper v002 10-key canonical comparison is equal, and so is the projection (`78abd5ee` both);
  - separate processes (pids 6983/73969) and distinct records (a `37cad3b0`, b `ee67bec0`).
  - So the run-sheet R4 check between the phases holds, and Phase B may start (A146).
- **The (a)4 decision of record** remains lo_slot_proof c3v003's (`cd10cd59`) on the root-registered pair (slot ρ = a; pair = (a, b)). It is a post-run step for root.
- **Stage times:** EPS 3,260 s, GQ 53 s, ρ a 96 s, ρ b 192 s.
- **C000** (HEADLINE_CORNER_000 `64dc775b…`) is POINT_DONE (exit 0).

**Phase B** (pid 13596, run `20261019T202004Z_13596`) was launched at 20:20:04Z by root, with the same out-root and the run-sheet command without `--points`.
- **Pins re-hashed at start:** runner `3f5e5c18` and the 0146 gate record `66c54c76`. SCHEDULER_START reads `rho_gate` OPEN.
- **A166 settings:**
  - max_concurrent 8 (the runner's maximum);
  - r2 spike allowance 0, per-worker peak 0 and floor margin 0, so the floor reduces to (running + 1) × the measured stage peak RSS;
  - swap hold 1,048,576 MiB, which is effectively off;
  - margin_pct 1, the runner's minimum (L738).
- **Kept as runner design (code, not settings):** the `memory_pressure` start gate at 25 % + margin (common L359-365), and `taskpolicy -b`, which the runner checks (getpriority = 1).
  - Both are timing-only. `memory_pressure` read 87 % at the first start.
  - Trigger: if the gate holds a start for more than 10 minutes, root rules (as A170).
- Rows 1 and 2 are skipped (POINT_DIR_EXISTS_NOT_RERUN), and rows 3-31 start in table order. As the run sheet says, the final line reads STOPPED with exit 3 even on success.
- **Expected duration:** about 1 h per point, so about 4 h for 29 points at k = 8 (UNTESTED under background QoS beside step 2).

**EPS reviews (A134 Q8).**
- **The anchor:** Claude4 is the signer lane (0747; 0237 started). The files are named explicitly, and the review is written outside the out-root.
- **C000 and the Phase-B points** follow, each as its POINT_DONE posts. Then root runs `adapt-eps --approved-signer-lane Claude4`.

## A175: credit-limited re-plan (principal's usage table, 2026-10-19 ~20:35Z); KS1-KS6 pass root verify, and the G-wave is deferred to after Claude2's weekly reset; STAGE0 c2v002 is pin-eligible (2026-10-19 20:33:20Z)

**Usage, as the principal reported it (lane accounts), and as root measured it (Claude2):**

| Lane | Reported status |
|---|---|
| Codex1 | 5 % left; resets 30-Oct |
| Codex2 | 0 % left; resets 10-Nov |
| Codex3 | 0 % left |
| Claude3 | 83 % used |
| Claude4 | 92 % used |
| Claude2 | 52 % used. Root's own reading: weekly 53 %, resets Thu 2026-10-22 18:00Z (13:00 CDT); 5-hour window 14 % |
| Grok | 500, available to 4-Nov |

Claude3's and Claude4's weekly reset times are asked for in 0749.

**Ruling: work is allocated by remaining credit, and compute time is protected first.** Compute costs no credit, and its wall time is the long pole for Phase 2 (W1 is about 235 h; the S0 serials' wall cap is 610,324 s).

- **Priority 1: the T0 launches (about Tue 06:00Z).** Step-3 verdict; S0 ×4 (needs C2V004 pinned after Claude4's delta review, which is running, and S0 kit C2V003a after Claude3's delta review); W1 on sched v004a (Claude4 PASS 0236; root verify in the A172 workflow; Claude4's full v004 review is running). Also the CP-1 Phase-B EPS reviews: Claude4's scripted check, batched per wave, not per point.
- **Priority 2: before the Phase-1 read; waits for resets.**
  - The G-wave (below): Claude2, after its Thu 18:00Z reset.
  - The KS and G-wave review (Claude3), the packet A166 set and RUNBOOK/c2v006 reviews (Claude4), and the NGC acceptance c2v003 review (Claude3): each after its lane's reset, unless the lane reports enough headroom.
- **Lanes run no helper workflows** except where a review cannot be done directly. Every dispatch stays lean.

**Classifier B (M-12), and its consequence for Phase 1.** A133 makes B "the only build that needs a different lineage". No phase-1 NGC value is read before r3a and the M-12 classifier are sealed (A133 §2).
- Codex1's preparation (0147) built and tested the kernels. The entry point, adapters, serialization and shared suite remain.
- Codex1 reports whether the remainder fits its 5 %; until then, it does B only. If it does not fit, B completes after Codex1's 30-Oct reset.
- **No Claude lane substitutes for B.** Same-lineage agreement would not be the independent check A133 requires (A48).
- **Stated now, before any NGC value:** if B waits for 30-Oct, Phase 1 is scored at about Sat 31-Oct, A133's late bound (L28), instead of Sat 24-Oct. Phase 2 is unaffected by B's timing, provided the T0 launches happen Tue.
- Grok is the only other non-Claude lineage with credit. It can take B only if it can work directly in the exchange folder with file access; root asks the principal only that capability fact.

**KS1-KS6** (`ks_k3_chain_c2/`, root workflow wf_6c308353, README `README_KS_K3_CHAIN_C2V001.md`, HASHES_C2V001.txt with 64 entries):
- **Successors:** custody `ad020470`, response producer `99c29df6`, common `736d2e7e`, runner `54595c2d`, assembler `080ed171`, guard KS5 `e394ae94`, wrapper KS5′ `66560a6a`, lo_core `2cf7c597`, lo_config `510ff07b` (a disclosed deviation; needed), adapter `8fa371a7`, handoff `6642d209`.
- **Tests:** 62/62 new, plus the ported 295/222/129/54/25.
- **Two verifier lenses:** non-S1 identity AGREE and adversarial PASS, both 0 blocking.
- **Adopted pending Claude3's lean review (A160).**

**Rulings on the KS findings:**
- **Row file (step 3).** Root writes row 32's file once u_A is fixed. Its sha256 is recorded in a V006 entry before any row-32 CP-1 run, which is the pin.
- **ρ slot check at prelaunch (ADV-D1/D2).** An S1-only ρ coverage, partition and producer check goes into the KS4 and KS5′ successors, so that a bad slot cannot cost a 10-18 h S1 call. G1's MUST_FAIL set carries the three cases.
- **ADV-A2.** KS5 is the guard only on the S1_UA_C3T path. Non-S1 handoffs keep b1.
- **ADV-E1** (a different refusal text for an invalid row file) is accepted, because both versions refuse.

**The G-wave** (README §7). It is required by A160 (A48: no waiver) and **deferred to after Claude2's Thu 18:00Z reset**, because the Phase-1 read now waits on B in any case. It is one lean root workflow: one builder, one adversarial verifier, one fix round.
- **G3:** GQ geometry and producers, K-parameterized for S1_UA_C3T only (`c6ffb338` L39).
- **G4:** EPS adapter.
- **G1:** slot proof.
- **G2:** the SRB adapter. Its deciding test runs first, and a successor is built only if that test needs one.
- **G6:** the acceptance inventory.
- **KS3′, KS4′, KS5′:** canonical producer lists, plus the ρ prelaunch check.
- **G7:** lib v002c, built after lib v002b (A172).

**STAGE0 successor c2v002 `d260ee30`:**
- Claude3 0242: PASS, 0 blocking, 8 NOTEs. Both M-14 TESTs hold, and D05 and D07 are fixed. It is eligible for the seal pin (A154).
- N3 (nullability in the field map) and N8 (the C2V001-named input schemas paired with the C2V002 manifest) go to Claude4 for classifier A's binding text.
- N1, N2 and N4 to N7 are noted. No value changes.

## A176: principal's direction to move Codex1-bound work to Claude lanes; classifier B becomes a Claude2 build behind an information barrier, on Codex1's kernels; the G-wave is commissioned now; reset times corrected (2026-10-19 20:39:21Z)

**The principal's direction (verbatim):** "Let's move anything to the claude models if there is something that we need rather than wait for codex1".

**Measured headroom.** Root's weekly meter read 53 % both before and after two root workflows (about 1.5 M subagent tokens), so a 1 M-token workflow costs under 1 %. Claude2 can carry the moved builds.

**Corrected reset times** (they supersede A175's table):
- Codex1: Sun 25-Oct 11:56Z, from its live usage tool (0156). Codex1 stopped B at checkpoint CONTINUATION_V089.
- Claude4: Fri 23-Oct 19:00Z (0242).
- Claude3: not readable by the lane.

**1. Classifier B (M-12) moves to Claude2.** A133's "different lineage" requirement is superseded for Phase 1 by the principal's direction. The independence that remains is built in as follows.
- **Kernels.** B builds on Codex1's `classifier_b_cx1/prep_v001/` kernels, which are Codex lineage and tested in scope (0147 and later continuations). Each is pinned by its V089 sha; they are neither re-derived nor edited.
- **Information barrier.** B's builder reads only the basis and contract texts: r3a basis `build_c4v001/basis/` (PREREG_MISS_READING_R3A, CLAUSE_SOURCE_MAP, ROOT_ITEMS), the README_CLASSIFIER_A_C4V001-C4V004 texts, INPUT_CONTRACTS_C4V004, schema_c4v003, Claude4's contract dispatches, and V006 A133/A154/A168/A173.
- **What the builder never opens:** any classifier A `.py`, suite, expected output, regression or verify folder. It keeps a READ_LOG, and the verifier audits that log.
- **Agreement.** A separate agent runs A (black box, c4v004 `e92aa30e`) and B on A's suite input bundles plus B's own. A triage agent classifies each disagreement as B_DEFECT, A_DEFECT or CONTRACT_AMBIGUITY.
  - B_DEFECTs go back to the builder, stated in contract terms only.
  - A_DEFECTs go to Claude4.
  - CONTRACT_AMBIGUITY items come to root for a ruling that both classifiers share.
- **Disclosure.** The seal entry and the PROVISIONAL (PHASE-1) label say that B's integration is Claude-built on Codex kernels, and that A/B agreement is therefore partly same-family.
- **Phase 2.** Codex1 runs a distinct-lineage adversarial review of B on the shared suite before the Phase-2 seal, if it has credit after its reset. This is not a gate on Phase 1.

**2. Other Codex1 items move to Claude lanes:**
- the r3a single-pass delta review (A133 §2) goes to **Claude3**, which is distinct from Claude4, the renderer. The fallback is a root workflow with a separate verifier;
- the NGC row-contract S10 policy review (A162) goes to **Claude3**. The fallback is Claude4 after its Fri reset;
- Codex1's Q4 approvals are complete (A164), and nothing else is open for Codex1.

**3. The G-wave (A175) is commissioned now** instead of after Thu. The S1 chain is back on the Phase-1 critical path once B no longer waits for 25-Oct. Its scope is as A175 lists. G7 (lib v002c) follows lib v002b (A172).

**4. Timing (UNTESTED).** The Phase-1 read target returns to about Sat 24-Oct. It depends on B's agreement, the G-wave plus the S1 pair, and Claude3's reviews. If any of these slips, Phase-1 scoring waits (A133 L188), and nothing is relaxed.

## A177: results of the A172 builds, roster builder c2v006 and NGC acceptance c2v003; rulings on their root items; the M-12 seal route (0751); the NGC roster recipes are commissioned (2026-10-19 20:49:32Z)

**sched v004a: ADOPTED** (`sched_s45_c2/v004a/`; config `63dac53de88303404c64e899856485bd912a4c493e44a93af0a6cb393240e4ec`; HASHES `72f9ac3a`).
- Root verify: 0 blocking, 33/33 twice. Claude4 0236: PASS on the one leaf.
- Only `max_concurrent` (1 → 8) and an appended note change. The cache id is unchanged.
- The CPU process budget 17 limits concurrency to 5 calls (campaign L203).
- **W1 wall rebuild (Claude4 0243 N1; builder item 1): the two-step path is ruled.**
  1. Run the A140 N4 rebuild from the step-2 receipts.
  2. Apply `SCHED_DELTA_S45_C2V004A.json` with apply v002.
  3. Leaf-diff against v004a. Only the wall, the orphan wait and the notes may differ (TESTED, Y04A).
- **The wall rule goes into the W1 record (0243 N2).** It states the receipts used (FINISHED/COMPLETED `elapsed_seconds` only, with their shas), the scaling to 32 iterations plus setup, post-loop and route B, the margin, and the contention factor.
- **The 48 h wave cap (0243 N9).** With budget-bound concurrency, long waves may stop as INFRA with NOT_STARTED calls. Root resumes each from its verified receipts; no value changes. The apply-tool successor that raises `campaign_wall_cap_s` is built after Thu and reviewed after Claude4's Fri reset.

**S0 kit C2V003a: ADOPTED pending Claude3's C2V002 → C2V003a delta review** (`s0_launch_kit_c2/`, HASHES_S0_KIT_C2V003A).
- **Results.** Root verify: 0 blocking, 28/28 + 84/84, the same row for row over two runs and the verifier's rerun.
- **N1:** a 300 s parse wait.
- **N4:** the twin's cap is RAM × 11, its tree's maximum process count confirmed from the driver bytes.
- **R1:** the serial tree has up to 3 processes (route B column_workers 2). **The serial cap stays at RAM.** The measured serial footprint is about 22 GB under ps-sum, roughly a fifth of RAM, so in practice a RAM cap cannot stop an honest serial. Root applies the RAM × n rule if a serial ever passes half of RAM.
- **R2:** if a launch record is still unparseable at the bound, the kit cannot stop the run, because it needs the record's child_pid (NOT_KILLED_TARGET_REFUSED, exit 5). **Root then stops the driver by hand** through the monitor's process, and writes the MISLAUNCH record.
- **R3:** F01-F04 are not ported (they test C2V002 freeze data, which is unchanged). Accepted.
- **CHOICEs** (README §5) are accepted.
- **E1 (builder):** an empty `DIFF_S0_KIT_C2V003_TO_C2V003A.diff` was created by exclusive create. **It is left in place, not deleted.** The real diff is the `_R1` file `99e838f7`.

**The step-4 packet A166 set: ADOPTED pending Claude4's review after its Fri reset.** Root verify found 0 blocking. guard/launcher 36/36 twice; lib 143/143 twice.
- **Objects:** guard014 `6efdca01`, launcher015 `cd987edd`, lib v002b `65d69cf4`, DBP C2V004B `e239d21e`.
- **What the tests show:**
  - launcher015 starts with `memory_pressure` unreadable and makes no memory call;
  - lib dry mode never opens gate v003;
  - a synthetic campaign route-A tree is still refused.
- **Builder items:**
  - **(1) Binder, (2) CLI wrappers, (3) lib default params.** step4_bind c2v010 loads guard011 and adds `nice`; the S1 CLIs pin lib v002a; the lib's default DBP is C2V003A. **Ruled: all three go into the S1 launch-path follow-up together with G7:** binder c2v011, CLI wrappers c2v002c, and lib v002c with DBP C2V004B as the default. That follow-up is built after the G-wave, and direct batches and S1 need it first.
  - **(4) Refuse, not ignore, for old-form plans:** confirmed.
  - **(5) S1 registration C14 text erratum** (the pinned bytes are unchanged): "passes the machine gate at its own start" now means "starts under launcher015's ramp and max_active". Under A166 there is no gate.
  - **(6) At the A140 N4 rebuild, DBP C2V004B is re-derived** from the rebuilt base by the same C2V004 → C2V004B transformation, then leaf-diffed.

**Roster builder c2v006 and ROOT_TSR_FLAG_RECORD_V003: ADOPTED** (A173).
- **Objects:** builder `0cc731065d1f00e1549cb7b9442c901da0a35f48c8a03d67f14701f652ad0aa2`, V003 `7d3c1eb915cd9a85b1a9dab388e6a3fb6c218ef3d4e8e6f2dc726bea15c54070`.
- **Results.** 160/160 twice. In the interface proof, c4v004's own checks accept the c2v006 gate lists and V003, and refuse the c2v005 forms. Root verify: ADOPT, 0 blocking.
- **C46-C49 are ruled as built.**
- **Erratum E_A169_1.** A169 said the c2v005 records were already in classifier A's schemas. They lacked `schema` (Claude4 0228).
- **Load-bearing for the seal:**
  - the seal entry, `sealed.tsr_flag_record_sha256` and the freeze manifest's `input_files` must all name V003;
  - `tsr_support_record` must also carry `schema: UNT_ROOT_TSR_SUPPORT_CX3V001` with its exact nine keys (c4v004 L705-707). It is still pending under RUNBOOK gap G7.
  - Root's own records (phase inputs, STAGE0 status C4V003, commitment status, fallback, field map) each carry `schema` (INPUT_CONTRACTS_C4V004 `f9286f56`). The exact-key rule holds by A's check for six of them, by root's writing rule for the fallback record, and not at all for root disclosures (Claude4 0235).

**M-12 seal route (Claude4 0245; root 0751): (a).** The r3a text is unchanged. The seal entry cites M-12 by id and records A176 as the ruling on implementation B (M-6 item 2).

**NGC acceptance c2v003: c2v003a is ADOPTED; c2v003's handoff is not** (`ngc_acceptance_c2/`, README `659ca6a4`, HASHES `e97b2af6`).
- **Results.** Two lenses, 0 blocking. c2v003 34/34 + 41/41 with 72/72 mutants; c2v003a 35/35 + 42/42 with 75/75.
- **Adopted (consistent with A167):** adapter c2v003a `9c4b6dfc` and handoff c2v003a `7c54fd6f`. The c2v003 handoff pins adapter c2v002 and is not adopted.
- **The NGC row contract** `NGC_ROW_CONTRACT_C2V001.json` `80cbf2f5be2e9f22a0b751376dcde3e7e779bd89f531a8ffe9d654616490fe32` holds ids and order, R_i, the rule id, the θ hex and the c hex. It has no velocity, t_i or σ. Claude3's S10 review (A176) must carry schema `UNT_NGC_LO_ROW_POLICY_REVIEW_C2V002`, verdict APPROVED and that `row_contract_sha256`.
- **Still owed before any real NGC acceptance** (every one reads INCOMPLETE until then, which is UNTESTED, not a null):
  1. **Roster recipes for route A and route B**, commissioned below. Without the route-A recipe, every call refuses at ROUTE_A_ITERATE_SOURCE_UNESTABLISHED (verifier note 1 corrects the README's description).
  2. **The S2 pins:** NGC ρ c3v003 producer `d3d0f3dd` and slot proof `ada31d12`, after root's review (running), with schema `UNT_NGC_POINT_RHO_NUMERICAL_C3V003`.
  3. **The S10 review** (Claude3).
- **For the next successor:**
  - the two test gaps of verifier note 3 (the start.json binding conjunct, and the W-1 eps-certificate pin check);
  - the README wording (notes 1-2).

**Commissioned: NGC roster recipes (route A, route B)** as one lean root workflow (builder plus one verifier).
- Each recipe is derived from the driver's pinned route-A controller and route-B binding, so that the S5 rebuild-export tool rebuilds each consumed state and admits it only on an exact `state_digest` match.
- Synthetic tests only. No NGC3198 data file is opened.
- The c2v004 successor takes the recipes plus the note-3 tests.
- Review: Claude3 after its reset, or Claude4 after Fri.

## A178: the RI45-14 list C2V004 is pinned (Claude4 0248: PASS, 0 blocking); the NGC S10 review is trusted (Codex1 0157); the deferral audit against the work due before Friday (2026-10-19 20:57:15Z)

**RI45-14 list: C2V004 is pinned.** It supersedes A157's C2V003 line, and A157 is not edited. A133 §2 row 1 ("the RI45-14 list fixed") holds for S0.

RI45_14_LIST_PIN FREEZE_EXPECTED_INPUTS_C2V004 54997f946b85150ea76cf14485c26ccd5d67227d80ddb7c2aaa05011c887a3ce /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/FREEZE_EXPECTED_INPUTS_C2V004.json

- **The spec of record** is FREEZE_SPEC_OF_RECORD_C2V004.json `e2a7650e166a9230138ffd16453ac8fdabab41a8695169844940c4c061a894ec`. It is saved at RUNBOOK steps 1a/1b (A171) and passed to every v003g `spec` call.
- **Claude4's notes, ruled for the RUNBOOK successor, which Claude4 reviews after its Fri reset:**
  - DN1: save `e2a7650e` at 1a/1b, and take the V-N1 value at step 8.
  - DN2: at steps 2 and 7 and in G26, require spec `e2a7650e`, notes canonical `56ac5c64`, and NGC coordinates equal to slots V003's.
- **VN1 and DN5 are ruled before the Phase-1 score, and they concern Phase 2 only.**
  - **VN1:** Phase 2 has no honest producer for A16.4. A pass-driver successor must build 0223 N4: a SENSITIVITY forward returns `valid: false` with GEOMETRY_NOT_EXPOSED for any θ whose NGC geometry is not 13.8 Mpc / 72°.
  - **DN5:** whether capped or unevaluated sensitivity entries count under V-N1.
- **Reading notes for the pin (DN6).**
  - The copied A13 "stricter" sentence is withdrawn (A23).
  - The Phase-1 `sensitivity_evaluated` note reads as Phase-1 budget 0.
- DN3, DN4, DN7 and DN8 are noted for the next list.

**NGC S10 row-contract review: APPROVED and trusted** (Codex1 0157).
- The review is `review_final_deltas_cx1/NGC_S10_POLICY_REVIEW_CX1_V001.json` `5b4b76dbd187a61f6016c2d89db05f6be2b5f7014c135a97d8caaaf71fa96294`, bound to the contract `80cbf2f5…`.
- Root adds this sha to the adapter's trusted review set (`check_review`) at the first NGC acceptance.

**Deferral audit** (the principal: deferrals must not interfere with the work due before Friday).

**Due before Friday, and not deferred:**
- **Tue (T0):**
  - step-3 verdict;
  - S0 ×4 (needs C2V004, pinned above, and S0 kit C2V003a, whose Claude3 review is running);
  - W1 on sched v004a (adopted).
  - The A133 row-1 r3a SEAL CANDIDATE gate is already met (Claude4 0194).
- **About Wed (u_A):** the Phase-1 NGC member and FD launches (phase1 v003b, spec of record).
- **Wed-Thu, the S1 chain:**
  - the G-wave and then the S1 launch-path follow-up (root builds);
  - Claude3's KS and G-wave review, second on its list;
  - CP-1 row 32;
  - the S1 pair (10-18 h).
- **Thu-Fri, the seal:**
  - V006 write freeze;
  - **Claude4's final r3a render, T1-T7 and the classifier-bearing SEAL CANDIDATE.** This was missing from Claude4's pre-reset list. It is now **reserved first** in Claude4's remaining credit, because only Claude4 can do it;
  - Claude3's r3a delta review;
  - the seal entry;
  - classifier B and the A/B agreement (root build).

**Moved later because nothing before Friday needs them:**
- **The 29 Phase-B EPS reviews and adapt-eps.** They gate the Phase-2 direct batches (about 30-Oct), not Phase 1. Claude4 does them after its reset.
- **The RUNBOOK c2v005/c2v006 review.** It gates the Sat scoring gate. Claude4 does it after Fri 19:00Z.
- **The NGC roster-recipe and acceptance reviews.** They gate the Phase-1 freeze on Sat. Claude3 does them after its reset.
- **The apply-tool successor for the 48 h wave cap.** Until it exists, root resumes W1's INFRA halts by hand.

**The one tight item:**
- **What it is:** the review of the packet A166 set plus the S1 launch-path follow-up, which gates the S1 launch.
- **Who:** Claude3 takes it right after KS/G-wave if its credit allows. Otherwise Claude4 takes it at Fri 19:00Z.
- **Timing:** S1 then ends by Sat about 09:00 CDT at the 18 h worst case.
- **If anything slips,** the Phase-1 read moves to Sat afternoon or Sun. The principal accepted that.

## A179: NGC ρ c3v003 passes root review (A167; 0 blocking, two lenses) and is adopted; S0 kit C2V003a is adopted (Claude3 0248); the R2-R4 draft and the T0 path rules (2026-10-19 21:11:52Z)

**NGC ρ c3v003 is ADOPTED** (`s4rc1_c3/ngc_rho_c3v003/`; root workflow wf_b9998e04, lens and adversarial verify, both PASS with 0 blocking).
- **Objects:** producer `d3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4`, slot proof `ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a`, stage `496d2a215145fb25aadbc4623b8930134cc2679cf1fe8097c65bf84cab450090`.
- **E1 (A167):** γ_eff = s·(ge·EB) at producer L313, the same float the call runs at (filler L294; driver L1444, L4498, L5090, L8139, L8348). The θ route is a diagnostic only.
- **Suite:** 33/33 MUST_PASS and 70/70 MUST_FAIL, re-run on a scratch copy.
- **Diffs:** each reproduces its sha from c3v002, and 83 of 94 producer statements are AST-unchanged.
- **V2 is now TESTED.** At default QoS, four attempt processes at the synthetic seed are bitwise equal on the 10 keys and equal to the `-b` records.
- **Noted as forged-input only:** A8/V4 (the θ-route diagnostic fields are not E2-checked), A9 (pair b's θ_binding is not E2-checked) and A10 (the proof cannot tie shells to γ). Root's registration and the adapter's recompute stop all three.

**The NGC acceptance S2 pins** are the producer `d3d0f3dd` and slot proof `ada31d12` above. The c2v004 handoff successor (roster-recipe workflow, A177) sets them as module constants. If it does not, a one-constant successor follows. Adapter c2v003a keeps the two approved lists separate (L548 slot proof, L560 producer).

**R2-R4 draft, for registration at T0** (not a registration):
- `CLAUDE2/NGC_RHO_C3V003_R2_R4_DRAFT_C3V003.json` (generated from the module constants), with notes in `NGC_RHO_C3V003_R2_R4_DRAFT_WF_B9998E04.md`.
- R2's `approved_producer_sha256` is the **slot proof's own** sha `ada31d12` (S L347-349). The producer, stage and slot proof run from the one approved folder.

**T0 path rules (verifier note 12, lens notes 7-10):**
- E3 refuses any path component containing ngc3198. So the S0 spec `fill_dir`, the out-roots, the args files and the review-pin path must all be ngc3198-free in every component.
- `fill_dir` must satisfy realpath = path: no /tmp or runs_ext link spelling. The kit's fill-check does not canonicalize it.
- The R3 `--root-review-pin` is a root review record under /Users/bgm/Research, outside the out-root. It cannot be V006.
- The producer and slot-proof CLIs refuse without `-b`, so root runs them under `/usr/sbin/taskpolicy -b`, and no c3v004 is commissioned. The stage needs no `-b`.

**S0 kit C2V003a is ADOPTED** (Claude3 0248: PASS, 0 blocking, direct lens).
- **Record:** `review_s0_launch_kit_c3/REVIEW_S0_KIT_C2V003A_RESULT_C3V001.md` `cf72b34b`.
- **The S0 launch uses it.**
- **Runbook note (R2):** exit 5 with `launch_record_parsed_within_bound` false means root stops the driver by hand.

## A180: the NGC roster recipes and handoff c2v004 pass root verify (0 blocking); R1 (the monitor-next state N) is ruled; KS1-KS6 is adopted (Claude3 0252); one lean follow-up is commissioned (2026-10-19 21:58:28Z)

**Objects** (`ngc_acceptance_c2/`):
- recipes `ngc_roster_recipes_c2v001.py` `6c9e8508cb590e764bda8643caf48c931359bc7318674b1a150ccd43d9ccebce`;
- handoff c2v004 `2721cfd1d27f6b05b831ba53b02a99125bd49033d235530b911453696bb8f29d`;
- README `2edd0347`, HASHES `e97dec91` (14,475 entries).

**Results.** 38/38 + 54/54 twice; verifier PASS with 0 blocking, and every recipe input re-derived from the driver, controller, writer and binding bytes. Note 3's two MUST_FAILs (F43, F44) reach their checks.

**Ruled:**
- **R1, the monitor-next state N** (it needs gas_{a+1}, which no record read so far holds).
  - **(i) First:** read the solver's `COMPLETED.json` payload and the checkpoint module `069b3935`. If `updated_a` is stored, gas_{a+1} follows exactly by controller L483, and N is rebuilt like every other state.
  - **(ii) Otherwise:** N is rebuilt from its recorded element roster `elements_{a}` and its recorded `payload.next_i1t`, and admitted only on exact `next_state_digest` equality. This is the same custody trust as every other recorded input. The state is the one the monitor consumed, so no reading changes. What differs is disclosed: I1-T is not recomputed for N.
- **R2, the DECLARED route-B inputs:** the follow-up reads the V011_B_STAGES scripts the driver pins. Until then, a wrong reading is a refusal, never an admission.
- **R3, the STAGE0_GRID_OUTER writer `443d9fdc`:** Phase 2 only, and only if STAGE0's successor is sealed. It is deferred.
- **R4:** S5 runs on the run host, which is a RUNBOOK note.
- **R5:** P18 is root's to run.
- **Item 6:** no adapter c2v004 is needed.

**KS1-KS6 is ADOPTED** (Claude3 0252: PASS, 0 blocking, direct lens).
- K=3 is reachable only through S1_UA_C3T, and every non-S1 call delegates to the unchanged predecessor object.
- N4 notes that the G-wave and an S1-bound C1 are still needed.

**Commissioned (one builder, one verifier):**
- recipes c2v002 with R1 (i) or (ii) and R2;
- **handoff c2v005**, with the S2 pins as module constants: ρ producer `d3d0f3dd`, slot proof `ada31d12`, schema `UNT_NGC_POINT_RHO_NUMERICAL_C3V003` (A179).
- Reviewed by Claude3 after its reset, together with c2v003a/c2v004 (A177).

## A181: NGC recipes c2v002 and handoff c2v005 pass root verify (0 blocking); R1 resolved by path (i); the NGC acceptance stack of record (2026-10-19 22:38:08Z)

**Objects** (`ngc_acceptance_c2/`):
- recipes c2v002 `c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e`;
- handoff c2v005 `7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1`;
- README `6a8b1bc7`, HASHES `24bbb9c1` (16,336 entries).

**Results.** 40/40 MUST_PASS and 59/59 MUST_FAIL on two runs and on the verifier's rerun. The verifier found 0 blocking.

**R1 is resolved by path (i), RECOMPUTED_GAS (TESTED from bytes).**
- **Where `updated_a` is recorded.** The solvers pass the same `updated` array to the controller and to the checkpoint (serial `8ef3079b` L223-229; parallel `7667025b` L340-346). The checkpoint `069b3935` L576-578 stores it as `COMPLETED.json` `updated_gas_fourier_J`.
- **How N is rebuilt.** gas_{a+1} = (1−r)·gas_a + r·updated_a, verbatim from controller L483. The recomputed I1-T must equal the recorded `next_i1t`, and S5 admits only on exact digest equality.
- **Path (ii) is not used.**

**R2.** Every route-B input is now FORMAL. Each is cited to the V011_B_STAGES scripts the driver pins, running under the driver's reuse patch, module `acda989d`.

**Root items:**
- **Ruled:** the recipe may execute the reuse module `acda989d` by its exact bytes at S5 time. That is the same module and patch the driver applies, it is inert at import, and it is pinned by sha.
- **UNTESTED, decided by the first real call's S5:**
  - N on real records;
  - whether the NGC route-B profile (the reuse module's CODEX1 file `f5becd45`) matches the route-A prep profile.
  - Both fail closed.
- **Noted:** an admitted body makes the recipe refuse the offset (fail-closed); three driver-line citation errata are corrected in the README.
- **Root's to run:** P18.

**The NGC acceptance stack of record.** It is pending Claude3's review after its reset, with the S10 review trusted (A178). The pieces:
- adapter c2v003a `9c4b6dfc`, which takes the S2 lists from the handoff;
- handoff c2v005 `7077ad93`, with S2 = producer `d3d0f3dd`, slot proof `ada31d12`, schema C3V003;
- recipes c2v002 `c700f469`;
- reader `9335ee42`, S5 `3611e993`, row contract `80cbf2f5`.

S5 runs on the run host.

## A182: the G-wave passes root verify (three lenses, 0 blocking after a documentation fix); it is adopted pending Claude3's delta review; the S1 C1 and handoff deps are fixed; the S1 launch-path follow-up is commissioned (2026-10-19 23:06:43Z)

**Object.** `ks_k3_chain_c2/`: README_KS_K3_GWAVE_C2V001b.md `a3ec369f`, HASHES_GWAVE_C2V001.txt `4c74539d` (78 entries). Root workflow wf_e3e081bf: map, build, three lenses, and one documentation fix.

**Successors** (every K=3 allowance is gated to S1_UA_C3T; every other spec goes to the predecessor object):

| Link | Successor | sha256 | Predecessor |
|---|---|---|---|
| G3 geometry | gq_geometry_r5_cx2v001_g3_c2v001.py | `572c86c6` | c6ffb338 |
| G3 producer | gq_producer_cx2v005_g3_c2v001.py | `c3699c78` | 2832ceb9 |
| G3 producer b1 | gq_producer_b1_c2v001_g3_c2v001.py | `8893213e` | 3e668a2b |
| G4 EPS adapter | point_response_admission_adapter_cx2v003_g4_c2v001.py | `e00ab71d` | 4de70486 |
| G1 slot proof | lo_slot_proof_c3v003_g1_c2v001.py | `6af9ed6c` | cd10cd59 |
| G6a / G6b / G6c | execution_graph / current_source_evidence / consumed_states successors | `ba58fb18` / `65834e9b` / `4ea0c2ca` | 6d59f1d0 / 7044e131 / 4ca7f364 |
| G2 SRB-ROT | srb_rot_adapter_c3v003_g2_c2v001.py | `7eb456cd` | 08e9ac0a |
| KS5″ wrapper | calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py | `51a6fb27` | KS5′ 66560a6a |
| KS3′ common / runner | s4rc1_common_c3v004_ks3_c2v002.py / cp1_runner_c3v004_ks3_c2v002.py | `fcd63a73` / `da08d725` | KS3 |
| KS4′ assembler | registry_assembler_c3v004_ks4_c2v002.py | `85c3343d` | KS4 |
| KS6′ adapter / handoff | lo_state_proof_adapter_c3v003_ks6_c2v002.py / acceptance_handoff_c2v004_ks6_c2v002.py | `c8dc59a1` / `7bb37957` | KS6 |

**Tests.**
- New: 43/43 (18 MUST_PASS, 12 MUST_FAIL, 3 EQUIVALENCE, 9 DIFFERENTIAL, 1 DECIDING).
- Ported: 62/62, 295/295, 222/222, 137/137, 25/25, 21/21, 33/34 + 34/34, 40/40 + 40/40, and 28/28.

**Lenses.**
- **Non-S1 identity: CONFIRMED.** About 27,000 synthetic non-S1 cases, 0 mismatches.
- **Adversarial: code PASS.** No K=3 allowance for a non-S1 spec, and no K=4 artefact certifies the K=3 point. The ADV-D ρ cases and 11 variants are refused at G1, KS6′, KS4′ and KS5″.
  - Its one BLOCKING item was documentation only. The README misstated the G2 development order: the dev successor was written 54 s before the first recorded deciding-test run. README C2V001b states the order correctly, and the reverify passed.
  - The final runs are in A175's order: test, then build.
- **Physics: PASS.**
  - **G3 is TESTED equivalent.** Its K=3 GQ is c6ffb338's computation with only the kept K changed. It is independently re-derived (20,720 nodes at K=3 against 20,736 at K=4), and K=4 output is bitwise unchanged.
  - **G2's deciding test is TESTED.** Library 2026f2b6's `field_bound` and `srb_rot` are valid from shell 3, so the library needs no change.
  - **G4/G1:** the shell plans and the 10-shell partition match A160 and procedure §2 exactly.
  - **No registered setting, threshold or reading changes.**
- **Status:** adopted pending Claude3's delta review (A160). Codex1 runs one narrow distinct-lineage check of G3 on its remaining credit (0754 job 2).

**Fixed for the S1 call (README §7):**
- **The S1 C1:**
  - custody deriver KS1;
  - `state_enumerator` G6c `4ea0c2ca`;
  - `approved_certificate_producers` = [G4 `e00ab71d`, G3 producer `c3699c78`, G1 `6af9ed6c`];
  - certificate policy review `guard_sha256` = KS5 `e394ae94`.
- **The handoff deps:**
  - enumerator G6c, evidence G6b `65834e9b`, lo_core KS6 `2cf7c597`;
  - guard KS5;
  - `srb_adapter` G2 `7eb456cd` (`adapt_call_srb_rot`), `lo_adapter` KS6′ `c8dc59a1`;
  - `trusted_source_producers` names G6b.
- **R32:** as A175.
- **The real row-32 GQ, EPS and ρ** stay UNTESTED until the CP-1 row-32 run. Its cost matches K=4's.

**Commissioned: the S1 launch-path follow-up** (one builder, one verifier). It carries A177 items (1)-(3) and G7:
- **lib v002c**, from v002b:
  - wrapper KS5″ `51a6fb27`;
  - `sources_to_add` = KS5″, KS5, KS1 (with 6810b7c3), KS2, G4, the G3 producer, G1 and G6c;
  - default params DBP C2V004B `e239d21e`;
- **CLI wrappers c2v002c**, re-pinned to lib v002c;
- **binder step4_bind c2v011**, which loads guard014 and runs no `nice`.
- **Deciding test (synthetic):** guard014 adoption plus the prelaunch of an S1_UA_C3T spec inside the fence with lib v002c's sources.
- **Review:** Claude3 after the G-wave if its credit allows; otherwise Claude4 at Fri 19:00Z (A178).

## A183: the G-wave is ADOPTED (Claude3 0254: PASS, 0 blocking; Codex1 0158: the G3 distinct-lineage check PASS) (2026-10-19 23:10:27Z)

- **Claude3 0254**, record `review_ks_k3_chain_c3/REVIEW_GWAVE_DELTA_RESULT_C3V001.md` `d94a7d68`:
  - all 15 diffs rebuild their successors exactly;
  - the gate runs first, with unchanged predecessor delegation;
  - in G3 the S1 path changes only the kept-region K, at L39;
  - the §7 pins agree with the code.
- **Codex1 0158** (`FROM_CODEX1/0158_…_G3_0759_narrow_review_PASS.json`):
  - all three G3 `produce()` bodies are AST-identical to their predecessors, apart from the early delegation and the single kept_k-for-4 substitution;
  - the custody change is the K3 cube predicate only;
  - non-S1 calls return the pinned predecessor's result unchanged.
  - This is the distinct-lineage check on the one physics-relevant edit.
- **N1 (Claude3), ruled.** The G2 SRB adapter `7eb456cd` is a handoff dependency that root supplies for row 32 (A182 HO).
  - Supplying the K=4 adapter `08e9ac0a` by mistake fails closed: its `format_eps` refuses any EPS coverage other than [4,182] (L275-276), so a K=3 certificate is refused. It cannot produce a false pass.
  - No successor is built. The RUNBOOK's S1 handoff step names G2 explicitly.
- **Still UNTESTED:** the real row-32 GQ, EPS and ρ. The deciding test is the CP-1 row-32 run, after u_A, the row file (A175) and the S1 launch path (building).

## A184: step-2 timing re-measured. S4T sets the step-3 verdict at about Fri 23 to Sat 24 Oct, not Tue. Erratum E_FORECAST_1; a speculative-start proposal goes to the principal (2026-10-19 23:36:19Z)

**Measured** (stage folder birth times, R2 tree; no T output read):
- **S4T's columns stage is about 13.9× KLO's per column.**
  - S4T's `07_fs_columns_01` has run 14:38Z to about 23:45Z (35 of 36 columns), against KLO's 0.66 h.
  - Iteration counts per column are the same (26 against 25), so the cost per iteration is what differs.
  - This is inherent, not a stall: S4T's route B uses the sphere mask with the sphere tail (sealed prereg, A62/RI-05).
- **KHI's columns run at KLO's pace** (60 columns in 1.3 h). Its reference stage took 11.7 h, against KLO's 1.5 h.
- **The step-3 sealed compare needs S4T.** Its error budget includes |v_i(S4T) − v_i(C4T)|, and the S4T-against-C4T statistic is a registered check.

**Projection (UNTESTED):**
- S4T needs 94-113 more hours: KLO's remaining stages, with column stages × 13.9 and the other stages × 1 to × 13.9.
- That puts the last receipt and the step-3 verdict at about **Fri 22:00Z to Sat 16:00Z** (Fri 17:00 to Sat 11:00 CDT).
- **The deciding measurement** is S4T's `rfs_columns` and `le1_columns` stage times, over the next day.
- The other step-2 runs finish about Tue 01:00-04:00Z, and KHI follows its remaining stages at about KLO's pace.

**Erratum E_FORECAST_1.** Root's step-2 verdict estimate of "Tue about 01:00-05:00 CDT" did not measure S4T's per-column cost. It is withdrawn and replaced by the projection above.

**Consequences, if nothing changes:**
- **T0 moves by about four days.** That covers S0, W1 and the S0/phase1 handoffs, whose V007 pin (RI45-05) is the step-3 verdict report.
- **Phase 1** is scored about Wed 28 to Thu 29 Oct: the NGC Phase-1 compute runs after T0.
- **Phase 2** moves by about the same amount.
- The machine sits largely idle from about Tue 06:00Z, apart from S4T and KHI.

**Proposal to the principal: no value changes, and no T output is read.**
- **W1 starts speculatively at about Tue 06:00Z,** after the other step-2 receipts and CP-1 Phase B.
- **It runs at reduced CPU priority** (`nice`), so S4T, the critical path, keeps the cores.
- **Its results are used only if the step-3 verdict adopts the C4T tail,** and are discarded otherwise.
- **A W1 started early also produces u_A**, so the S1 chain (row 32 and the S1 pair) can run during the wait.
- **S0 and the Phase-1 NGC launches still wait** for the verdict and their V007 pin.
- **Two things deviate from standing rulings, which is why the principal decides:**
  - the order: the campaign before the verdict;
  - the use of `nice`, which A166 excluded for new work. Here it protects the critical-path run, rather than holding work back for memory.

## A185: the S1 launch path c2v002c passes root verify (0 blocking); its root items are ruled (2026-10-19 23:49:26Z)

**Objects** (`s1_successors_c2/`):
- lib `s1_path_lib_c2v002c.py` `99e2be175e546992c70984435bc480e1eddb90b052fda65ddcbfe8780bdbd27e`;
- CLIs `s1_launch_root_c2v002c.py` `d4e31013`, `s1_fill_c2v002c.py` `2b120b89`, `s1_read_c2v002c.py` `4716bb69`;
- binder `step4_bind_c2v011.py` `d3d9702eb8096d11b98461f1c62c67931b9ecf74957cee95fbc3a60f60deaea0`;
- README `135a0426`, HASHES `7bba21e1` (19 entries).

**Results.** 163/163 twice (37 MUST_PASS, 125 MUST_FAIL, 1 DECIDING); the verifier found 0 blocking.

**What the lib changes:**
- the wrapper is KS5″ `51a6fb27`;
- `sources_to_add` is: guard014, launcher015, KS5″, KS5, KS1, 6810b7c3, KS2, G4, the G3 producer, G1 and G6c, plus the lib itself for an overlap. Each of the 11 is necessary;
- the default params are DBP C2V004B.
- The G3 geometry is not on the list, because prelaunch reads the G3 producer but never runs it.

**The binder** loads guard014 and refuses `nice` or `renice` in its command.

**The deciding test is PASS, synthetic:** guard014 adoption plus the S1_UA_C3T prelaunch inside the real fence. The old wrapper `e7f52461` is refused three ways.

**Root items, ruled:**
1. **The base source list.** Root's dry launch (`s1_launch_root_c2v002c.py` without `--launch`) on the real S1 admission confirms that the q5b1 base carries `certs_common_r5_cx2v001.py` `c75aaa5a` and the r5 driver closure. This is the deciding test for everything left UNTESTED. Until it runs: the real custody derivation, the real direct adapter, and the real r5 normalization.
2. **Two C1s.** S1_UA_C4T is admitted under the campaign (guard b1) C1, and S1_UA_C3T under the S1 C1 (A182).
3. **`context_module`.** Root copies it from the plan sidecar and checks it by hand at launch. No successor is built.
4. **Fill records.** Any written under v002b are re-made under v002c.
5. **The binder.** The C2V004B `packet_read.binder` text naming c2v010 is noted, and nothing reads it. A launcher014 plan fails closed at its own guard.
6. **The wall cap.** After the W1 rebuild, root passes `--params` with the rebuilt DBP.
7. **Stale text** (the lib's C3T chain note and the make_plan docstring) is noted. No decision reads it.

**Review.** Claude3 reviews this together with the packet A166 set if its credit allows; otherwise Claude4 after Fri 19:00Z. With T0 now about Fri/Sat (A184), that timing no longer constrains S1, unless the principal approves the speculative W1.

## A186: the S1 launch path c2v002c and the packet A166 set are ADOPTED (Claude3 0256: PASS, 0 blocking, direct lens) (2026-10-19 23:55:29Z)

**The record:** `review_ks_k3_chain_c3/REVIEW_S1_PATH_PACKET_A166_RESULT_C3V001.md` `7fbb8dca`.

**What Claude3 checked:**
- every diff rebuilds its target exactly;
- only memory gating and `nice` were removed;
- the custody and fail-closed checks are the predecessors';
- lib v002c's S1 fence sources equal the G-wave §7 pins.

**Adopted:**
- guard014 `6efdca01`, launcher015 `cd987edd`, lib v002b `65d69cf4` superseded by lib v002c `99e2be17`;
- CLIs c2v002c, binder c2v011 `d3d9702e`;
- DBP C2V004B `e239d21e`.

Claude4's 0229 ramp note is closed.

**Notes, ruled:**
- **N1.** Plans of record use C2V004B's rule form, without the memory fields. guard014 refuses the old form.
- **N2.** Fill records are made fresh under v002c.
- **N3.** G2 stays a handoff dependency that root supplies (A183).

**The S1 path is complete.** What remains before S1:
1. u_A, from W1;
2. the row-32 row file and its CP-1 run (A175);
3. root's dry launch on the real admission (A185 item 1);
4. the S1 pair.

## A187: root ruling: W1 starts before the step-3 verdict, at low CPU priority, under a discard rule; the PLAN is cleaned (P-98 to P-108) (2026-10-19 23:58:12Z)

**The principal (verbatim):**
- "Why are you asking me to decide?"
- "Anything that can accelerate the timeline is ok with me as long as we don't compromise the physics."

Root decides; A184's proposal is withdrawn as a question.

**Ruling: W1 starts early.** W1 is the first wave of the DDO154 calibration campaign, on sched v004a. It launches as soon as two conditions hold:
1. the step-2 receipts that the A140 N4 wall rebuild needs are in. These are the finished C-cases, expected about Tue 01:00-04:00Z;
2. root's W1 record is written: the two-step wall rebuild (A177), the D1 disk guard (A143), the wall rule (Claude4 0243 N2), and the campaign config freeze (A137 N-C).

**Why the physics is not compromised:**
- No step-2 T output is read before the sealed compare. The verdict is computed exactly as sealed.
- The campaign's bytes are the same whenever it starts. Its config does not contain the verdict, and no explicit rule orders W1 after it. A142's "H2 after the step-3 verdict" is HEADLINE11, a direct batch, and stays where it is.
- **Discard rule, stated before launch:** W1's results are used only if the step-3 verdict adopts the C4T tail (V007 PASS). Otherwise the campaign is re-specified, and the speculative W1 is preserved but never used.

**Priority.** W1 runs under `nice -n 10` while S4T (the critical path) is running, so the verdict is not delayed. This is the one place `nice` is used. It protects the run that sets the schedule and holds nothing back (A166's concern was work held back for memory). Once S4T finishes, no priority is set.

**Unchanged:**
- S0 and the Phase-1 NGC launches still wait for the verdict and their V007 pin (RI45-05).
- S1 and CP-1 row 32 run once W1 yields u_A, under the same discard rule.
- An earlier NGC start is not pursued now. W1 already fills the CPU, so starting NGC speculatively would split it rather than add capacity. Root revisits this once W1's load is measured.

**PLAN.** The galaxy-run tasks are now P-98 to P-108 in `plan/plan.tsv`. P-80 and P-82 to P-86 are superseded and DROPPED, and P-81 is DONE.

## A188: erratum E_A187_1, W1 cannot start before the verdict (the adoption gate is by design); the campaign launch path is incomplete; commissioned: the H3 campaign launch path, built now and finalized at the verdict (2026-10-20 00:41:25Z)

**The finding** (W1 run sheet `W1_RUN_SHEET/W1_RUN_SHEET_V001.md` `6ab42522`; root workflow wf_839ee350, builder plus verifier; dry only):
- **The campaign gate refuses before the verdict.** The parent `run` checks its gates first and refuses with GATES_NOT_PASSED (c75a889f L3438-3439).
  - The numerics gate needs the sealed V007 ADOPT_TAIL report.
  - Adoption policy cx2v006r7 (`7c726fa2`) has `APPROVED_V007_SEALS = frozenset()` (L9-12, L60-62).
  - So no call can adopt before the verdict, as A126 intends: "no step-4 call can adopt before the verdict".
- **Erratum E_A187_1.** A187's premise ("the config does not contain the verdict") was wrong, because the campaign path gates on adoption.
  - **The early W1 start is withdrawn.** Bypassing the adoption gate would weaken a registered safeguard, so it is not done.
  - W1 starts at the verdict (about Fri 22:00Z to Sat 16:00Z, A184).
- **Even after the verdict, the pinned code has no path to launch W1** (verifier B-V1/B-V2). Four gaps:
  1. **Adoption.** The campaign core r9 (`a595c5c0`) pins the policy by path and sha (L200-202). Finalizing at the verdict therefore needs, re-pinned in a chain:
     - a policy successor that registers the seal tuple;
     - a core successor;
     - an R9 wrapper successor (`24abe3bc` L27 pins the core);
     - a launch entry.
     A129's policy-only route covers the direct-batch admission, not the campaign path.
  2. **No launch entry exists.** The R9 wrapper and core offer only `plan` and `wave`, and the parent's `run` refuses the R9 config's keys (L1585-1588). The sheet's `w1_campaign_entry_v001.py` (`6a6957f2`) is unreviewed, and its `run` and `resolve` have not been run.
  3. **Acceptance.** Every finished call reads INFRA CERTIFICATE_ACCEPTANCE_REFUSED until `TAIL_CERTIFICATE_ACCEPTANCE.json` exists. Only the wrapper's `reingest` (L305-328) writes it, with a post-state certificate bundle, and no command line exposes `reingest`.
  4. **H3 config fields.** Five more gates need fields that apply v002 cannot set: deciding, capability, certificate policy, the u_i carrier and adoption.
- **Disk.** Engine wave 15 (24 calls) would halt HALTED_DISK on External1: short by 508 GiB, or by 879 GiB with HEADLINE11, S0 and NGC (forecast). The campaign's wave folders cannot be moved, because the cache re-checks them by path (L2302-2341). Root rules the storage plan before wave 9.
- **Provisional wall:** 133,200 s (37 h), orphan wait 133,800 s, set by C4T. It is final when C4T's receipt lands (expected Tue 01:00-04:00Z).

**Commissioned: the H3 campaign launch path** (root workflow: map, build, verify).
- **Built now,** with the verdict tuple as a placeholder:
  - the policy successor and the generator route;
  - core, wrapper and entry successors, re-pinned in a chain;
  - the entry gains `run`, `resolve` and `reingest`;
  - a per-call acceptance step: post-state certificate bundle, then acceptance (acceptance_q2 v004, A158), then `reingest`;
  - the H3 config fields, through a reviewed config or apply-tool successor;
  - the storage plan.
- **Finalized at the verdict:** root fills the seal tuple and regenerates. Review is a small diff.
- **Distinct review:** Claude4 after its Fri 19:00Z reset; Codex1 for the generator (A129) if it has credit after its Sun reset.

**Honest schedule** (UNTESTED; replaces A187's):
- **W1** starts about Sat 24 Oct.
- **u_A** comes after the pre-march0 waves, about Mon-Tue 26-27 Oct.
- **S1** follows u_A.
- **The Phase-1 NGC runs** take about 3.5 days each (half the S0 cap, A140 N3).
- **Phase 1** is scored about **Fri-Sat 30-31 Oct**.
- **Phase 2** is about 9-10 Nov.
- **Deciding measurements:** S4T's next stage times, W1's per-call wall and the NGC call wall.

## A189: the I4 gate record is produced. The serial C2T run equals the parallel one bitwise, with the tail ON: PASS (A114; registered producer V010) (2026-10-20 01:22:46Z)

- **Producer:** `ri33_c3/i4/write_i4_record_c3v003.py`, sha `707395ba…` from bytes, equal to the V010 entry `producers.I4` (PRODUCER_REGISTRY_C3V012). Root ran it as the after-seal gate record (PRODUCED_AFTER_THE_SEAL).
- **The pair:**
  - serial (N1): `I4_COMPANION_C2T_N1_SERIAL_V002` (FINISHED COMPLETED, 15.9 h);
  - parallel (N8): the V007 C2T T-run `KMAX_V007_P128_C2T_MS128_CX1_RUN_V011_CX3V001_R2` (FINISHED COMPLETED, 15.47 h).
- **The record:** `V007_POSTSEAL_RECORDS/I4/I4_GATE_RECORD_V001.json` `2e7df0eace5ebe9c09cade38836dbfddc3930e695766ca6c13fceed7b66b80fb` (exclusive create). Its stdout and empty stderr are kept beside it.
- **Verdict PASS_SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON:**
  - tail ON;
  - `bitwise_equal` true;
  - `v8c_f1_fix_confirmed` true;
  - 0 differences outside custody.
- This is an identity gate; no T-test value was read. Compare r14's g_I4 reads it at step 3.

## A190: classifier B c2v004 is not yet adoptable (A/B agree on 13 of 1477 bundles); root's rulings on the 42 triage items; c2v005 is commissioned (2026-10-20 01:42:25Z)

**Result** (root workflow wf_046e7bb8; `classifier_b_c2/build_c2v001` to `build_c2v004`; four agreement rounds; verifier).
- **c2v004** `fe5bc96a`: own suite 277/277 twice, and the information barrier holds.
- **Verifier: NOT ADOPTABLE YET.** On an honest v003g score, B reads NOT_READ.
- **Cause.** The barrier kept B's builder away from the producers too, so B guessed their record encodings. Eight B_DEFECTs follow from those guesses: RC3, RC4 and its downstream, RC5 with RL9, RC7, RC8, and RL5B.

**Rulings.** Both classifiers share every one. None changes a physics reading.
1. **The producers' bytes are the contract for their records.** B's builder may read the producer modules and records:
   - v003g `48a1e48a` (score_after_freeze, the frozen manifest, row_registration);
   - phase1 `d64351ec` and `7d891ff7` (the L1 band and AT1 records, MODULE);
   - STAGE0 c2v002 `d260ee30` (block keys);
   - the compare `6f095f64` record.
   B reads these the way any consumer must. The barrier stays in force against classifier A's code, suite and outputs only.
   - This settles every encoding item (RC01, RC1, RC2, RC2b, RC03, RC3a, RC3b, RC04, RC05, RC5, RC6, RC09, RC7, RC4, RC10).
   - The full 64-hex pins are read from bytes.
2. **Detail-wording and word-choice items take the seal candidate's printed form (classifier A c4v004).** That form is the one the triage recommends, and in every case the code, class, rows and reading are the same either way. The items:
   RC06, RC07, RC8, RC6, RC08, RL2, RC12, RC10, RL5B, RC14, RC5, RC12, RL3, RC13, RC15, RC16, RC2b, RC3c, RC4b, RC4D, RL6, RC2R.
3. **The A_DEFECT items** (RC11, RC9 and RL1 on field-map partial renames; RC11 and RL4 on a non-list `input_files`) are reachable only from inputs root never writes: colliding renames, a non-list pin list.
   - Under A115 they are NOTES, not blocking.
   - B matches A's printed form for them, and no c4v005 is built.
   - They are listed for a later version.

**Commissioned: c2v005.** One builder, an agreement run, one fix round if needed, and a verifier.
- Fix the 8 B_DEFECTs from the producer bytes, and apply rulings 2 and 3.
- The suite's stand-ins must be in producer form: score alternatives[], the frozen manifest, row_registration, L1, AT1.
- **Adoption bar:** A and B agree on every honest-form bundle of the shared suite. Any remaining difference must be ruled, or be forged-input only (A115).
- A176's disclosure stands.

## A191: the H3 campaign launch path is built (84/84; six gates pass on a synthetic seal); 2 blocking items; three design gaps for W1's later waves; storage is at the two-volume edge (2026-10-20 02:03:48Z)

**Object.** `h3_campaign_path_c2/`: README `6d2b4ee2`, HASHES `67ef3ad4` (5,495 files). Root workflow wf_49db569c: map, build, verify.
- **The chain derives from the q5b1 line (map F1),** not the R9 wrapper. R9 still needs the retired prelaunch LO envelope, which A134 replaced with per-state acceptance through acceptance_q2 v004 (A158).
  - The successors: generator `make_campaign_cascade_c2v001` (`65a70144`, from generator v002), entry `h3_campaign_entry_c2v001` (`08068e93`), and `regenerate_h3_c2v001` (`1706da77`). The regenerator's `fill` writes the one seal record from the report's bytes, and its `build` refuses unless the tuple equals those bytes.
  - Also built: `apply_h3_fields` (`2e4a5393`), the per-call step `h3_accept_call` (acceptance v004, then reingest), and the storage check.
  - **Placeholder chain** SUB `v006r12_c4`. A129 reserves r11, and nothing is published.
- **Verify.** Code holds; 84/84 twice; 78/78 physics pins equal and numerics `4b2a5a87` unchanged. Map F4: the cache id becomes `ce6a1a6b…` (wrapper and gate fields are in the key), and the W1 record states it.

**BLOCKING, fixes commissioned:**
- **B2 (TESTED).** The entry's `reingest` can cache a call as VALID without the adopted acceptance handoff having run.
  - The fix: `reingest` takes `--acceptance-record` with its sha, and refuses unless the record is an acceptance_q2 v004 (`5ff464cc`) ACCEPTED or ACCEPTED_PASS_FLAGGED record for the same call, receipt and bundle. The bundle path must be absolute.
- **B1, the storage plan arithmetic.** The README's §6 counted HEADLINE11 plus S0 at about 48 GiB. The real figure is about 370.5 GiB, so the plan does not fit.
  - At the measured 16.24 GiB per call, External1 must hold about 3,386 GiB of its 3,726 GiB at wave 15. The internal disk has about 953 GiB free.
  - **The program is at the two-volume edge of the A147 rule.** The erratum recomputes the budget with the parent's binding condition: the maximum over k of (Σ_{j<k} n_j)·b + n_k·80 GiB + 20 GiB.

**Design gaps for W1's later waves** (FORMAL; mapped, not yet ruled):
- **F5.** Once the certificate registry is set, every planned point needs a registry record before planning. That covers the 9 capability-probe points, every call, every resume and every cache open. The registry pin sits in the frozen config and the cache key, so engine-chosen points from march0 on cannot be registered in advance.
  - W1 itself can run. Its seed is `6944e210…`, not the anchor, and the 9 probe points are CP-1 points.
- **F6.** No ruling covers a campaign call whose acceptance reading is not ACCEPTED (INCOMPLETE, LO_UNCERTIFIED_TRANSIENT, NON_LAPSE_TAIL_MATERIAL). `resolve invalid` is disabled, and a retry reruns the same call deterministically.
- **The deciding and capability runs** are real r5 calls with no commissioning lane.

**Commissioned (lean):**
1. the B2 entry fix and the B1 storage erratum;
2. a **design map from the existing rulings and code** (A134, A139, A145, A146, A158, the campaign packet docs): how per-point certification of engine-chosen campaign points was meant to work, and the minimal path for F5, F6 and the deciding/capability runs. It proposes; root rules.
- **Review:** Claude4 after Fri 19:00Z (the campaign packet's lineage); Codex1 the generator diff, if it has credit after Sun.

**Timing consequence (UNTESTED).** W1's first wave can launch at the verdict once B2 is fixed and the gate fields are filled. Wave 2 onward waits on the F5 ruling and its build. That may hold the campaign past the verdict, and with it u_A and Phase 1. Root reports the measured effect once the design map returns.

## A192: the campaign certification design is ruled (F5 ledger, F6 reading rule, HEADLINE11 before W1); the H3 entry fix is adopted; storage is measured at W1; the honest schedule (2026-10-20 02:37:26Z)

**Inputs.** Root workflow wf_93e4ceb9:
- entry fix c2v002 `75b4cafa`, 94/94 twice, verified 110/110 with adversarial rows;
- storage erratum `5ce908d0`;
- design map `h3_campaign_path_c2/CAMPAIGN_CERT_DESIGN_MAP_C2V001.md` `29071333`, with 20 source shas and about 60 line ranges verified.

**Ruled:**
1. **B2 is closed.** `h3_campaign_entry_c2v002` and `h3_accept_call_c2v002` are adopted pending Claude4's review. `reingest` needs the call's own acceptance_q2 v004 record. A hand-edited record is root's custody, under A115 honest producers.
2. **F5, per-point certification of engine-chosen points: the R-C8 ledger** (Claude4 ROOT_ITEMS_FINAL_C4V004 L263-269, never built).
   - An append-only, hash-chained registry ledger. The config and cache id bind only its starting set and its policy.
   - Each wave's new points are certified before that wave by the approved producers: CP-1 EPS, GQ and ρ, then adapt-eps and the slot proof. This uses a CP-1 successor that takes a list of points.
   - The ledger goes into the wrapper source of the verdict regeneration, before W1. The core is untouched, and nothing that sets a physics value changes.
   - Fallback: a new work dir at march0.
3. **F6, campaign calls not read ACCEPTED** (a science ruling, made now, before any campaign call). It is consistent with A134 and A158: no value is used before ACCEPTED, failure readings stay frozen, and the scope never changes.

   | Reading | Action |
   |---|---|
   | ACCEPTED, ACCEPTED_PASS_FLAGGED | cached VALID |
   | INCOMPLETE | the acceptance step reruns once, after root checks its inputs. No new forward call is made. |
   | NON_LAPSE_TAIL_MATERIAL, BOUND_INSUFFICIENT | certified MODEL_INVALID through a reviewed command, built with the ledger |
   | any other reading | the campaign halts at that point, and root rules per call |

4. **The deciding and capability evidence is HEADLINE11 #0-#10** (CP-1 rows 1-9; core L114-197, L313-340).
   - **W1 passes its gates only after those 11 calls are FINISHED and ACCEPTED.** HEADLINE11 starts at the verdict and C1 (A142), so the order is: verdict, then HEADLINE11, then W1.
   - A tool to assemble the two evidence documents from HEADLINE11's receipts is commissioned.
   - **Deciding test** (whether HEADLINE11's runs can be reused, so no extra runs are needed): `status` shows the 9 capability-probe spec shas under the candidate config. They must equal the shas HEADLINE11 ran with.
5. **Storage (verifier blocking item, accepted).** b is measured at W1 as the call dir's total bytes after acceptance, including the ACCEPTANCE_TAILSTATES exports. It is not the receipt's output bytes.
   - The 17.08 GiB threshold is recomputed from that measurement, and `storage_check` gets a successor that counts the same bytes.
   - If both volumes cannot hold the program, root alerts the principal (A147). One campaign volume of at least about 7 TB would cover the high case.

**Commissioned (root workflow; Claude4 reviews after Fri 19:00Z):**
- the wrapper ledger and the MODEL_INVALID command;
- the CP-1 list-of-points successor;
- the HEADLINE11 evidence assembler;
- the `storage_check` successor.

**Honest schedule** (UNTESTED; replaces A188's).
- **Step-3 verdict:** about Wed-Sat 21-24 Oct, set by S4T.
- **HEADLINE11:** about 3 days (11 calls at 3 concurrent, about 18 h per call).
- **W1 up to B_P1** (seed, Jacobian, repair): about 3 days, giving u_A.
- **Phase-1 NGC runs:** about 3.5 days.
- **Phase 1 is scored about Sun 1 to Sat 7 Nov.**
- **Phase 2 is about mid-to-late November.** The campaign takes about 10 days after HEADLINE11, plus per-wave certification of about 2 days in total, plus step 5.
- **Deciding measurements:** S4T's le1 stage time, the HEADLINE11 call wall, the W1 per-wave times, and the NGC call wall.

## A193: classifier B c2v005 is ADOPTED. A and B agree on every honest-form bundle; the M-12 pair for the seal is A c4v004 and B c2v005 (2026-10-20 02:54:32Z)

- **Object:** `classifier_b_c2/build_c2v005/`: classifier `cec5bfe9582899437aa715d78e1dfdb36089ebead04f840d4d68893b3d1251c7`, README `5cfb42a1`, HASHES `862ccb67` (12,732 files), READ_LOG `4aa328de`.
- **Own suite:** 327/327 twice, with every stand-in in producer form.
- **Agreement with A** (black box, c4v004 `e92aa30e`): **364 of 368** shared bundles. The 4 that differ (B352, B407, B412, B419) are inputs the producers themselves refuse: forged or malformed only, so they are A115 NOTES.
- **The verifier's own check:** 10 honest bundles built with the producers' code, with both modules unpatched, agree 10 of 10.
- **Barrier:** holds at the path level (A190). The Codex1 kernels are unedited.
- **Verdict: ADOPTABLE, 0 blocking.**
- **For the seal (M-6 item 2; A176; 0751):**
  - the M-12 pair is classifier A c4v004 and classifier B c2v005;
  - the disclosure: B is Claude2-built on Codex1's kernels, behind an information barrier from A, and reads the producers' bytes for record forms (A190);
  - the distinct-lineage review of B by Codex1 is due before the Phase-2 seal, if it has credit.
- **Noted for a later version:** the 4 forged-only differences, and the two seam artifacts SA1 and SA2.
- **PLAN:** P-104 is DONE.

## A194: the campaign-certification build passes, except one enforcement defect (F6 re-roll), which is being fixed; open items ruled (2026-10-20 03:49:01Z)

**Object.** `h3_campaign_path_c2/`: README_CAMPAIGN_CERT_C2V001 `bc0ea884`, HASHES `52b6b556` (11,339 files). Root workflow wf_7c2c598f.
- **Pieces:**
  - the q5b1 wrapper with the R-C8 ledger and the MODEL_INVALID command (`5ea1780a`);
  - entry c2v003 (`5710e1fa`): `reingest-invalid`, `points-manifest`, `ledger-append`, `ledger-status`;
  - the CP-1 list-of-points runner, common and assembler (`3c6a5ba3`, `302abdad`, `951e7203`);
  - the HEADLINE11 evidence assembler (`2a8df9df`), with its `reuse-test`;
  - `storage_check` c2v003 (`8eee1f68`).
- **Verify: CONDITIONAL PASS.**
  - 77/77 twice, plus 30 adversarial rows.
  - Physics pins 78/78; numerics `4b2a5a87`; core and policy untouched; CP-1 rows 1-31 identical.

**B1 (TESTED), a physics-relevant defect, fix commissioned (wf_d115a990).** The acceptance step allowed a rerun whatever the first pass read. With a second deps record, a frozen reading could be re-rolled in either direction:
- NON_LAPSE then ACCEPTED, so the call was cached VALID;
- ACCEPTED then NON_LAPSE, so the call was cached MODEL_INVALID.

A192 item 3 allows a rerun only after INCOMPLETE. The fix:
- a second pass needs the pinned first-pass record, and it must read INCOMPLETE;
- `reingest-invalid` and VALID reingest accept only the call's latest pass, and refuse when the call already holds an acceptance certificate;
- MUST_FAIL rows for each.

**Open items, ruled:**
- **D5 accounting.** A certified MODEL_INVALID carries `judgment_call: true` and never counts toward D5 TESTED-NEGATIVE. That is correct and kept, because an invalid model output is not a test outcome.
- **HEADLINE11 capability rows.** `run_mode_admitted: true` means finished, completed and accepted at exactly the probe spec. Claude4 confirms this reading in its review.
- **CP-1 list runs** write into CP-1's own out-root, as root's act after CP-1 finishes. This is accepted, because the anchor AGREE and context live there.
- **A truncated ledger** is caught at the first use of a removed point. The head sha recorded in each wave record is the outside check, and root records it.
- **"Reruns once"** is enforced as at most two passes, with the first-pass condition above.
- **Reviews:** Claude4 after Fri 19:00Z, for the whole campaign set (H3, the ledger, CP-1 list mode, the assembler, the F6 fix); Codex1 the generator diff, if it has credit after Sun.

## A195: S4T R2 stopped on its wall cap (19.0 h). Ruling: relaunch S4T alone with an identical spec and a wall cap set from the measured stage rates; the step-3 verdict moves with it (2026-10-20 03:58:38Z)

**Fact (receipt).** `KMAX_V007_P128_S4T_MS128_CX1_RUN_V011_CX3V001_R2`:
- status STOPPED_WALL_CAP, exit −15, elapsed 68,400.9 s (19.0 h), output 13.7 GB;
- it reached stage 11 (`rfs_columns`) of about 30.
- The run was healthy and progressing (A184). Its columns cost about 7.6-13.9× KLO's per column, which is inherent to S4T's sealed sphere-mask/sphere-tail route B (A62, RI-05). A wall cap of 2× an unmeasured forecast was too small.

**Other live cases are not at risk:**
- KHI: cap 201,600 s (56 h), elapsed about 20.5 h.
- C6T: cap 93,600 s (26 h), about 20.5 h elapsed, in its last stage. Root watches it.

**Ruling.** Precedents: A127, where a cap stop is relaunched with the cap raised; A133 (c) and (f), where caps are value-relevant, so the case is rerun and never abandoned; and A166, where a cap is a hang guard and raising it before launch changes no value.
- **S4T alone** is relaunched as R3:
  - identical spec and driver;
  - only the wall cap and the run name change;
  - RSS at RAM, as A166 makes the default.
- **Wall cap from measurement.** It is about 2× the projected full S4T time, roughly 110 h on the 13.9× column rate, so about 792,000 s (220 h), with the computation recorded.
- **The R2 S4T tree is preserved**, and nothing is read from its partial outputs.
- The step-3 compare reads S4T's R3 run in place of R2. The relaunch packet confirms from the compare and plan bytes how that binding is made.
- **Resume.** Reusing R2's completed stages is used only if the sealed driver offers it as a registered capability. Otherwise the run starts fresh.
- **Review:** one direct-lens review of the packet diff, by Claude3 or by Codex1 if it has credit. Then root launches.

**Schedule (UNTESTED).**
- A fresh S4T takes about 100-130 h, which puts the step-3 verdict at about **Sat 24 to Sun 25 Oct**.
- The A192 sequence (HEADLINE11, then W1 to B_P1, then the Phase-1 NGC runs) then puts **Phase 1 at about Wed 4 to Sun 8 Nov**.
- The deciding measurements are S4T R3's stage rates.

**Erratum E_A184_1.** A184 projected S4T's finish but did not compare it against S4T's own wall cap. The stop was foreseeable from the 13.9× rate at 23:45Z. Root now checks every live case's projected finish against its cap.

## A196: the F6 enforcement fix passes (c2v004; 90/90; 0 blocking); C6T receipt; the campaign set is complete for review (2026-10-20 04:20:31Z)

**The fix** (`h3_campaign_path_c2/`, README_CAMPAIGN_CERT_C2V004 `638d6543`, HASHES `394880b6`):
- `h3_accept_call_c2v004` `eb895263`;
- wrapper source `calibration_orchestrator_q5b1_ledger_c2v004` `7c9b4248`;
- entry, generator and regenerator c2v004;
- placeholder chain wrapper `381fa295` and entry `dd9c951b`; policy and core unchanged.

**What it enforces:**
- a second acceptance pass needs the pinned INCOMPLETE first-pass record of the same call;
- a third pass is refused;
- `reingest-invalid` and VALID reingest accept only the call's latest pass, and are refused once an acceptance certificate exists.

**Results.**
- **Re-roll attacks:** C03 and C04 are closed. The verifier passed with 0 blocking: 90/90 twice, plus 62 probes. No physics value changed.

**Residual R1 (TESTED).** A pass made by calling handoff v004 directly, outside the step, is not counted as a rerun.
- **Ruled:** root runs the handoff on campaign calls only through `h3_accept_call_c2v004`. That is the RUNBOOK step, under A115's honest producers.
- **For a later version:** both reingest paths require the first-pass record for A002 records. Claude4 checks this in its review.

**C6T R2:** FINISHED COMPLETED, 20.11 h, peak RSS 35.4 GB. Step 2 now has 8 of 10 receipts. KHI's projected finish is about 10:00Z, against a 56 h cap. S4T R3 is per A195.

**The campaign set ready for Claude4's review after Fri 19:00Z:**
- H3 entry c2v002 → c2v004;
- the ledger wrapper c2v004;
- CP-1 list mode;
- the HEADLINE11 evidence assembler;
- storage_check c2v003;
- the generator diff (Codex1 too, if it has credit).

## A197: the S4T R3 relaunch packet passes root verify (0 blocking); the launch path is ruled; it launches after Claude3's direct review (2026-10-20 04:24:38Z)

**Packet** (`V007_STEP2_LAUNCH_ROOT/S4T_R3/`, SHA256SUMS `08e117d3`):
- plan `07311ded`, launch script `c18ebbdf`, generator `c0de839e`, leaf diff `63e571ca`, README `b5db31cd`.
- **Changes from R2's S4T call:**
  - the wall cap, 68,400 s to 792,000 s (220 h);
  - the run name, `_R2` to `_R3`.
- **Unchanged:** spec `8e71be9b` (bytes and path), driver `b5cc62af`, monitor `ba031c23`, RSS at RAM, the output cap and the poll interval.
- **Dry run:** exit 0, nothing created. The sealed launcher refuses the one-case plan (TEN_DISTINCT_CASES_REQUIRED), as expected. The verifier found 0 blocking.

**Rulings:**
- **Launch path.** The sealed launcher v007 accepts only a ten-case plan (L80-83). The packet's script therefore:
  1. repeats the launcher's own checks for the one case, including the sealed admission chain, read-only;
  2. starts the identical monitor command exactly as the launcher worker would (L163-167);
  3. holds caffeinate on the monitor's pid.
  This follows the I4 N1 precedent (A114). The verifier confirmed it is equivalent. No computed value is affected.
- **Wall cap.** 792,000 s (A195), at least 1.68× the projected time and a hang guard only.
- **The step-3 binding.** The sealed compare takes each case's run dir from the cases manifest root passes in (L5636, L5659, L5311, L5476-5480). At step 3, root sets `cases.S4T` to the R3 run, and the post-seal gate producers (EA, MT, I1T, HARMONICS, FLAG_RULINGS) are pointed at the R3 result. Nothing else changes, and the compare is not modified.
- **Resume:** none. The run starts fresh (driver L3481-3484, L1786-1790, L1404-1405).
- **Passive alerts.** The memory watch and root's step-2 watch match only `_R2` names. Root adds an S4T_R3 watch at launch.
- **README wording (verifier notes 3 and 5)** is corrected in the launch record. No behaviour changes.

**Review:** Claude3, one direct lens (0761). Root launches on its PASS.

## A198: S4T R3 is launched (Claude3 0258: PASS) (2026-10-20 04:28:24Z)

- **Review:** Claude3 0258 PASS, record `review_s4t_r3_c3/REVIEW_S4T_R3_RELAUNCH_RESULT_C3V001.md`. Its NOTE: `DISK_WATCH_PID=3385` is hard-coded, which fails closed.
- **Pre-launch checks:** SHA256SUMS 6/6 OK; disk watchdog 3385 alive; dry run PASS, with nothing created.
- **Launch** at 2026-10-20T04:28:02Z, through `launch_s4t_r3_root_c2v001.sh`:
  - monitor pid 99575, caffeinate pid 99607;
  - launch record `S4T_R3_LAUNCH_RECORD_V001.json` `d88966be5005e32a04c304b7683af3b8dc7526a6b4d02dd6e808eeaa65bf7e39`;
  - outdir `…/KMAX_V007_P128_S4T_MS128_CX1_RUN_V011_CX3V001_R3`;
  - wall 792,000 s, RSS at RAM, output cap 103,079,215,104 B;
  - spec `8e71be9b` and driver `b5cc62af`, both unchanged.
- **Watch:** root's S4T_R3 watch reports stage changes, monitor liveness and the receipt.
- **Projected finish (UNTESTED):** about 100-130 h, so about Sat 24 to Sun 25 Oct. Root checks the projection against the cap at each stage (E_A184_1).

## A199: CP-1 is complete; all 31 points exit 0 (2026-10-20 04:40:22Z)

- **Phase B** (pid 13596, run `20261019T202004Z_13596`) ended at 04:39:42Z.
  - SCHEDULER_END: 29 points exit 0, 2 skipped as POINT_DIR_EXISTS_NOT_RERUN (rows 1-2, Phase A), and `stopped` null.
  - The log is `SCHEDULER_20261019T202004Z_13596.jsonl` `60773a0c`.
  - As the run sheet says, the final line reads STOPPED with exit 3 even on success.
- **Phase A** (A174) gave rows 1-2 exit 0. The anchor cross-check reads AGREE, and the anchor ρ pair is canonically equal.
- **Post-run steps, root's except where named:**
  1. **EPS reviews** for rows 3-31, 29 points, by Claude4 after its Fri 19:00Z reset (A178). Each is followed by `adapt-eps` (anchor and C000 are done, A174).
  2. **ρ registration** (slot ρ = attempt a; the anchor's (a)4 pair = (a, b)) and the slot-proof decision `cd10cd59`.
  3. **The registry assembly and C1** (`registry_assembler_c3v004`).
- **Who needs these:** HEADLINE11 at the verdict, the campaign's starting registry and the S1 C1. All come after the step-3 verdict (about Sat-Sun, A198), so the reviews after Friday's reset do not delay anything.
- **Erratum to A198** (Claude3 0259): the S4T R3 review record is `1675ec57`.

## A200: storage plan, ruled with the principal: a dedicated campaign volume by about Sun 25 Oct (2026-10-20 05:55:50Z)

**Principal's facts (2026-10-20):** the external drive has about 1 TB used of 4 TB; this Mac has about 1 TB free; there are 3 USB-C ports besides power.

**Ruling** (A188, A191, A192 item 5):
- **The campaign's work dir is a single path** (cache L2302-2341). It cannot span volumes or move after W1.
- **So the campaign gets one volume of its own, with at least about 7 TB usable.** It can be either:
  - one 8 TB drive; or
  - two 4 TB drives combined into one volume (Disk Utility RAID Assistant, Concatenated or Striped). That gives about 7.3 TiB against the worst case's about 6.9 TiB. If either drive fails, the volume is lost and the campaign reruns.
- **External1 stays connected** for existing data and the S0/NGC run folders. With the 2×4 TB option, all three USB-C ports are used, one drive per port, with no unpowered hubs.
- **Deadline:** mounted by about **Sun 25 Oct**, before W1. W1 follows the verdict and HEADLINE11.
- **Go/no-go measurement.** HEADLINE11's first finished, accepted call (the same DDO154 call type) gives b, measured as the call dir's bytes after acceptance (A192).
  - b ≤ about 17 GiB: the campaign can run on External1 as in the A191 erratum (moving about 0.5-0.6 TB of its existing data to the Mac).
  - otherwise: the new volume is required.
  - If the volume exists, root uses it in either case.
- **When the principal names the volume,** root checks free space and points W1's work dir at it, through the parent's path rules.

## A201: Phase-1 critical-path audit (root workflow wf_5843b484, audit plus independent check); the date of record and the remaining work (2026-10-20 12:34:30Z)

**Phase-1 PROVISIONAL score, date of record: about Tue 3 Nov (CST), range Sat 31 Oct to Fri 6 Nov.**
- This assumes S4T R3 finishes Wed 21 to Thu 22. Measured since R2: route A 0.82 h against 1.30 h, reference 1.75 h against 3.51 h, fs columns about 5.3 h against 9 h.
- If A198's Sat-Sun projection holds instead, the date is about Fri 6 Nov.
- **Adders:**
  - a reuse-test exit 5: +2.25 d;
  - each repair wave: about +0.75 d;
  - an S1 FAIL_TH2 holds Phase 1.
- Root changes this date only when a measured milestone moves it.

**Remaining items the audit found, all owned by root unless named:**
1. **Unbuilt tools:**
   - a member/F NGC launcher for Phase-1 calls other than S0 (the S0 kit launches seed and J0-J2 only);
   - the G26 step-8 freeze script;
   - values writer v004;
   - the G7 TSR support record.
2. **RUNBOOK rulings:** G13, G15, G16, G24, G25 and G27; plus the root-written classifier inputs (phase_inputs, fallback, root_disclosures, c3_record M-13), VN1 and DN5.
3. **Before HEADLINE11:**
   - C1 (H1);
   - the A129 policy-only finalization diff review, reassigned from Codex1 to Claude3;
   - the A140 N4 wall rebuild and the DBP C2V004B re-derivation;
   - the step-4 run root.
   - CP-1 rows 1-9: adapt-eps is done for rows 1-9 (TESTED PASS). Registry assembly and ρ registration remain.
4. **Before W1:** the 22 remaining genesis EPS reviews (rows 10-31), which supersede A178's deferral; the full 31-point registry; the signed certificate policy review (Claude4); H3 V1-V5; the W1 record.
5. **During the campaign:** per-wave ledger certification of new points (CP-1 list run, an EPS review per point, ledger append), including march0's points before AT-0a.
6. **Step 3:** the cases manifest (`cases.S4T` = R3), then the post-seal gate producers EA, MT, I1T, HARMONICS and FLAG_RULINGS on the R3 result, then the sealed compare.
7. **Seal hazards:**
   - schedule the V006 write-freeze window around the T0, row-32 and wave writes;
   - record phase1 v003b's adoption, because the seal must pin v003b, which the classifiers bind;
   - extend G17's single CLASSIFIER role to the M-12 pair.
8. **The S1 pair takes about 36 h** at about 18 h per call.
9. **Lane load.** Claude4 is the bottleneck after Fri 19:00Z. Root distributes the EPS reviews:
   - Claude3 after its reset, using Claude4's scripted check;
   - Codex1 after Sun 25 11:56Z.

**Refuted by the checker:**
- G28 is due before the first FULL build, not before S0;
- NGC ρ R2-R4 is not an S0 launch prerequisite (A136); it gates the first acceptance;
- the S1 pair is about 36 h, as above.

**Publication** (principal's question): the Phase-1 score is published automatically as PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) (A133 §2 row 5).
- Disclosed caveats:
  - AT-1 may SUPERSEDE it;
  - ORIGINAL_K reads NOT_AVAILABLE;
  - the band is never a tier;
  - B is same-family (A176).
- Phase 2 is the score of record.
- Publishable sooner: only the step-3 numerics verdict.

## A202: Codex2 and Codex3 credit has reset. Codex3 becomes a root-approved CP-1 EPS signer lane, and the 22 genesis EPS reviews (rows 10-31) go to Codex3 now (0763) (2026-10-20 13:13:45Z)

**Principal (verbatim):** "codex2, codex3, and codex4 have reset their usage limits".

**Why.**
- Claude4 is 92 % used until Fri 23-Oct 19:00Z, and Claude3 is about 83 % used.
- A201 found Claude4 to be the bottleneck for the W1 gate. W1 needs the full 31-point genesis registry: the rows 10-31 EPS reviews, adapt-eps, ρ registration, slot proofs and assembly.
- Moving these reviews to a lane with fresh credit takes them off the path to W1, with no physics change.

**Rulings.**
1. **Codex3 is a root-approved signer lane** for the CP-1 per-point EPS reviews (the runner's `--approved-signer-lane`, brief section 6 Q8).
   - It is neither the operator lane (Claude2) nor the producer author (Codex2). Every request's `excluded_reviewer_lanes` is exactly [Claude2, Codex2], and `distinct_review_problems` (s4rc1_common_c3v004) admits any approved lane outside that set.
2. **Rows 10-31 go to Codex3 (0763).** Rows 28-31 come first (the W1/W2 points), then rows 10-27.
   - This supersedes 0762's "rows 10-31 after your reset" for Claude4, and A178's deferral (as A201 already noted).
   - Codex3 writes its own E1-E10 checks and its own review writer. Claude4's tools and reviews are a format reference only.
   - Disclosure: rows 1-9 are signed by Claude4 and rows 10-31 by Codex3. Both are distinct from the operator and the producer.
3. **Claude4's N1 note** (0252: the per-point EPS does not depend on `common_scale_s`) is put to Codex2, the producer author, for confirmation by construction before HEADLINE11 launches. Codex3 checks the same pairing across rows 10-25 from bytes.
4. **The remaining Codex allocation is ruled in the next entry, after a lineage and readiness check:**
   - the A129 policy-only diff reviewer, still named Codex1;
   - the distinct-lineage review of classifier B, pulled forward from Phase 2 (A176 §1);
   - the NGC acceptance-stack review (P-106);
   - the unbuilt G26 freeze script and values writer v004.
5. **Codex4.** No FROM_CODEX4 outbox exists, so Codex4 is not routed any work until it is set up as a lane.

## A203: all 31 CP-1 EPS reviews are applied; N1 is TESTED-POSITIVE by construction and by bytes; the six flagged x00 corners fall under A134 Q10, with no new ruling (2026-10-20 13:22:56Z)

**EPS.**
- Codex3 signed rows 10-31, rows 28-31 in 0653 and rows 10-27 in 0654. Its checks were its own (`independent_checks_cx3v002` `8e4407bd`; signer `sign_reviews_cx3v001` `1ba651e3`), against checklist C3V001 section E (0765).
- Root ran `adapt-eps --approved-signer-lane Codex3` on all 22. Every one exited 0 with all checks true. The proofs are logged in `CP1_C3V004_ROOT/ADAPT_EPS_LOG.tsv`.
- **CP-1 EPS is 31/31:** rows 1-9 signed by Claude4, rows 10-31 by Codex3. Step 1 of A199's post-run list is DONE, about three days ahead of A178's plan.

**N1 (Claude4 0252): does the per-point EPS depend on `common_scale_s`?**
- **By construction, TESTED-POSITIVE (Codex2 0527).** H_s = s·H_1 (lwr_common L135-142 and L121-133), so x_s = x_1/s and q_s = q_1. Domains, settings and seeds carry no s, so the EPS objective is s-independent. At ×4, a power of 2, bitwise equality is expected, as an exact exponent shift.
- **From bytes, TESTED (Codex3 0655).** All 8 sensitivity pairs (rows 10/14 … 21/25) have byte-identical 178 shells and 14 audits, at an s ratio of 4.0. Claude4 0252 found the same for the 4 HEADLINE pairs.
- **Meaning.**
  - The 1xx corners give no new EPS evidence along the common-scale axis.
  - Their forward runs are still distinct: unnormalized T and the physical forward prediction are not s-independent (Codex2 0527).
  - HEADLINE11's design, points and reuse are unchanged.
  - This is not a defect and not a null.

**E6 flags (rows 2, 6, 10, 14, 18, 22).**
- These are the low-gamma, low-ell_F x00 corners. All six have eps_max 0.016393134560794387 on [4,5], identical across s and across DLO/DHI.
- **A134 Q10 already governs them:** there is no bare EPS magnitude gate, and SRB-ROT ≤ τ_i/10 is checked on each accepted state.
- So no new ruling is needed. The deciding test is the post-run SRB-ROT check on the accepted states of those points (HEADLINE11 C000/C100 first). Until then it stays UNTESTED.

**Next (root):** ρ registration, the slot-proof decision `cd10cd59`, and the registry and C1 assembly (A199 items 2-3).

## A204: step-2 R2 launcher finished (9/10 FINISHED; S4T R2 STOPPED_WALL_CAP, superseded by R3); the W1 per-call wall is FINAL at 144,000 s (2026-10-20 13:44:25Z)

**Launcher.** `launcher_finished` reports ordinary_failures 1 and systemic_failures 0.
- **9 cases FINISHED/COMPLETED, exit 0, passed:** C2T, C3T, C4T, C4T-A, C4T-D5, C4T-C5c, C4T-KLO, C4T-KHI and C6T.
- **S4T R2 is STOPPED_WALL_CAP**, as A195 records. cases.S4T = R3 (A197), which is still running (pid 99575).
- **KHI R2:** 108,687 s (30.2 h), peak RSS 57.2 GB, output 16.39 GiB. Receipt `16d023df`.
- Only top-level receipts were read.

**The W1 wall** (`w1_wall_rule_v001.py` `f6e4f083`, A177 / A140 N4), with every C-case receipt present.
- Record: `W1_RUN_SHEET/evidence/W1_WALL_RULE_FINAL_20261020T134411Z.json` `bde25b63`.
- **Primary set** (C4T, C4T-A, C4T-C5c, C4T-D5): T* = 71,543.9 s; κ = 1.3281; μ = 1.5.
- **Wall = 144,000 s (40 h)**, orphan wait 144,600 s. This is **FINAL_FOR_THESE_RECEIPTS** and equals the provisional value.
- The caps successor line is `DDO_TAIL_ON_WALL_CAP_S = 144000` (the current config has 100,800).
- **Output.** out32 max is 57.19 GiB, so the 80 GiB per-call cap holds. The measured final output is about 16.2 GiB per campaign-like call, as the A200 storage plan assumed.
- **SENSITIVITY row, information only:** with KLO and KHI included, the wall would be 259,200 s (72 h). Those are other numerics (the P-88 k_max brackets), not the campaign config.

## A205: reviewer and builder reallocation to Codex2 and Codex3 (root workflow wf_ce54cc4b: planner plus two checking lenses, lineage and blinding/readiness) (2026-10-20 13:56:04Z)

**Why.** Codex2 and Codex3 have fresh credit (A202). Claude4 has seal-reserve credit only until Fri 23-Oct 19:00Z. Claude3's reset time is unknown. Codex1 is at 5 % until Sun 25-Oct 11:56Z. None of the moves below changes a method, prereg, threshold or sealed object. They change only who reviews or builds, and when.

**Rulings.** Each supersedes the named earlier assignment.
1. **A129 verdict-time diffs go to Codex3.** These are the r11 two-line policy-only diff and the H3 r12 chain diffs.
   - Supersedes: A129 (Codex1), A201 item 3 and A202 item 4 (Claude3/Codex1), and A188's r12 reviewers (Claude4 for the set, Codex1 for the generator).
   - Codex3 prepares now and reviews within about an hour of root's post.
   - **Disclosure:** Codex3 revised V007 launch-packet pieces whose outputs feed tuple member V (postseal_records cx3v001, srb_rot cx3v001, LAUNCH_PLAN/CASES_MANIFEST V011_CX3V001). Its check is byte equality and tuple identity only, not an independent check of the verdict's content.
   - **Named-file exception:** the verdict report's sha256 and five fields only (schema, script_sha256, prereg.sha256, pins_verified.V005_addendum, verdict).
2. **The A129 finalization operator is root.** Root runs Claude4's 0166 command itself at the verdict (fenced runner, then cp -n with a sha check), so HEADLINE11 is not held for Claude4's reset.
3. **The campaign-set review goes to Codex3 now.** It covers H3 c2v002-c2v004, the ledger wrapper, CP-1 list mode, the MODEL_INVALID path, the HEADLINE11 evidence assembler with its reuse-test, storage_check, the F6 fix and the campaign generator diff.
   - Supersedes Claude4 in A192, A194 and A196, including the A194 capability-row reading and the A196 A002 first-pass confirmation. PLAN P-109 and P-111 read "Codex3 review 0 blocking".
4. **Certificate-policy reviews go to Codex3:**
   - (i) the C1 certificate_policy_review: C1 is frozen before HEADLINE11's first PRELAUNCH (A134 Q9), so it is signed at C1, before HEADLINE11;
   - (ii) the campaign policy review, which binds W1's tail_readiness.certificate_ledger once the W1 work dir is fixed on the new volume (A200);
   - (iii) the S1 C1 policy review (KS5 guard set, A182), which was unassigned.
   - Supersedes A201 item 4 (Claude4).
   - **Disclosure:** the genesis ledger holds 22 EPS reviews that Codex3 signed, and its check of that binding is pins and bytes only.
5. **Per-wave EPS signing goes to Codex3, standing.** A202 item 1 is extended to CP-1 list-mode points (excluded lanes [Claude2, Codex2]). Per wave, root names the run root and point folders. Only the four 0763 files per point may be opened.
6. **P-106, the NGC acceptance-stack review, goes to Codex2 now** (adapter c2v003a, handoff c2v005, recipes c2v002). Supersedes A181 (Claude3).
   - **Disclosure:** findings on rules that mirror Codex2's own DDO rules (the handoff's fresh_scope/execution-facts rule, the adapter S2 refusal, ρ c3v003's a1dcdea8 reference) are labelled same-lineage.
   - Codex2 opens no NGC3198-named file, including any the code pins.
7. **The classifier B distinct-lineage adversarial review goes to Codex2 now**, after item 6 and preemptible by items 8-9. It is a Phase-2-seal gate pulled forward, and it does not gate Phase 1 (A176 §1).
   - Codex2 is preferred to Codex1, which wrote B's kernels. Supersedes A176 §1's Codex1 assignment.
   - **Barrier, which keeps A176:**
     - B_DEFECTs are stated in contract terms only. A_DEFECTs go to Claude4, and CONTRACT_AMBIGUITY items go to root.
     - A's outputs are stored under an `A_SIDE/` subfolder, which goes on the never-open list of any B successor builder.
8. **The P-112 Phase-1 NGC member/F launcher becomes a Codex2 build, reviewed by Claude4.** It starts when root has posted the G13/G25/G27 rulings and the phase1 v003b adoption record (P-117).
9. **Values writer v004 becomes a Codex2 build, reviewed by Claude4.** Supersedes A159's "root build". It starts when root adopts the NGC stack on item 6.
   - **Disclosure:** Codex2 reviewed handoff c2v005, which v004 pins, so Claude4 derives the record schema and route from the handoff's bytes, not from Codex2's notes.
10. **G26 step-8 freeze script:** root builds it after Thu 22 18:00Z, and Codex2 reviews it, code only (cross-family; Claude4 is the fallback).
    - Disclosure: the v003g FORBIDDEN-set lineage.
    - Any test that reads slots V003 stays on root's blinding-guarded side.
11. **Claude4 after Fri 19:00Z**, in order:
    - (1) the final r3a render and seal candidate;
    - (2) the P-112 launcher review;
    - (3) the v004 review;
    - (4) the RUNBOOK successor review with DN1/DN2;
    - fallback for items 3-4 if Codex3 raises a lineage-context blocker.
    - Removed from Claude4: rows 10-31 EPS (done, A203), the campaign-set review, the certificate-policy signatures and the G26 review.
12. **Claude3:** the r3a delta review at the seal (A176 §2), and fallback for item 1 if Codex3 has not answered within about an hour. Removed from Claude3: P-106 and the A129 diff.
13. **Concentration.** Codex3 is generator and output-diff reviewer, campaign-set reviewer, policy signer and per-wave signer on one path. This is disclosed in the seal entry and the PROVISIONAL label. A non-gating Claude4 second look at r12 is allowed if its credit permits after the seal render.
14. **Codex4** gets nothing until it has an outbox (A202 item 5). If onboarded, it is the unconflicted alternate for the second r12 lens or the G26 review.

**Root's own queue** (ruled now so the Codex builds are not held):
- the RUNBOOK G13, G25 and G27 rulings;
- the phase1 v003b adoption record (P-117);
- the CP-1 registry (P-116, in progress);
- C1 (H1).

**Date.** No measured change: about Tue 3 Nov (A201). These moves remove the credit waits after the verdict on HEADLINE11 (up to about 2 days), W1 and the first NGC acceptance.

## A206: CP-1 ρ registration, the slot-proof decision and the registry assembly inputs (root workflow wf_15c6be7c: builder plus an independent verifier, PASS_WITH_FIXES with its one fix applied); A199 items 2-3 (2026-10-20 13:59:01Z)

**Decisions.**
1. **Slot-proof producer:** `lo_slot_proof_c3v003.py` **cd10cd59** (A134 Q5, A151). It binds each point's driver lo_certificate slot to its registered ρ record and certifies no LO. LO is decided per accepted state, post-run (A134 Q2/Q3).
2. **ρ registration:** `RHO_REGISTRATION_CP1_C2V001.json` **be6dcb35**. It holds 32 exact pins: the 31 ρ attempt-a records in table order, then the anchor's attempt b.
   - Slot ρ = attempt a at every point.
   - The anchor (a)4 pair = (a 37cad3b0, b ee67bec0) at key 8ad6ca4e. Its 10-key canonical comparison is equal and its shell tables are identical (verifier, from bytes).
3. **Approved-producers input:** `APPROVED_PRODUCERS_CP1_REGISTRY_C2V001.json` **10867036**. It holds exactly the three canonical pins, under the key the assembler's load_approved reads:
   - EPS adapter 4de70486;
   - GQ producer 2832ceb9;
   - slot proof cd10cd59.
   It is byte-equal to the C1 draft's proposal. It is not the C1 document.
4. **Filled-spec rule:** each spec_ref is the registered spec with numerics.uv_tail.eps_certificate set to the EPS numeric pin and lo_certificate set to the ρ a pin, which is the core Mapper fill (dc895f8a L249-259). Nothing else changes, the point key included (31/31).
5. **Folders**, all new and exclusive create:
   - inputs: `claude_artifacts/s4rc1_c3/rho_registration_c2v001`;
   - slot proofs: `lo_slot_c2v001`;
   - registry: `registry_c2v001`.
   Script: `cp1_registry_root_c2v001.zsh`, copied into the inputs folder for the record. It stops at the first refusal, and root then rules (A50). A P01 refusal at (a)4 is the anchor stop.

**Open for C1 (H1), not ruled here.**
- c3v004 verify (F3) refuses any approved producer outside the three canonical pins.
- A151 and S4RC1 Q9(a) would add the acceptance producers 67fddd24 and 7044e131.
- So, at C1, either those producers stay outside `approved_certificate_producers`, or verify and common get a successor.
- **UNTESTED:** the slot proof on real inputs, and bundle/registry on real inputs. The deciding tests are P01 in phase 2 and phases 3-4.

## A207: the CP-1 31-point certificate registry is assembled (A206 run) (2026-10-20 14:00:32Z)

**Run.** `cp1_registry_root_c2v001.zsh A206`, 13:59:06Z to 14:00:04Z, exit 0.
- Log: `CP1_C3V004_ROOT/CP1_REGISTRY_C2V001_LOG_20261020T135906Z.tsv`.
- **Slot proofs (cd10cd59): 31/31 exit 0, OK.** P01 ran first, and the anchor (a)4 check held. Proofs are in `s4rc1_c3/lo_slot_c2v001/`.
- **Bundles (registry_assembler_c3v004): 31/31 exit 0, OK.**
- **Registry:** `s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json` **2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319**, schema S4RC1_C1_CERTIFICATE_REGISTRY_C3V003, 31 points.
- **Manifest:** `REGISTRY_MANIFEST_31pts_20261020T140004Z.json` **1164bb48d733e613529696c1c6671cb49ad10b0ace2c57a5344e8ad582794eb0**.
- Both shas were re-hashed from bytes by root.
- This closes the slot-proof and bundle UNTESTED items in A206: real inputs, both TESTED.

**Remaining in S2 (P-116):**
- C1 (H1): tail_readiness pins this registry, custody deriver 6810b7c3, b1 enumerator 4ca7f364, the three approved producers and the certificate_policy_review;
- the certificate_policy_review, signed by Codex3 (A205 item 4(i));
- `registry_assembler_c3v004 verify` against C1;
- the acceptance-producer question from A206, to rule at C1.

The registry is frozen as of this entry, before HEADLINE11 (R-C1 L211, Q9).

## A208: lane capacity update (principal's table); Codex1 is back; Claude4 is at 100 % until its reset (2026-10-20 14:29:44Z)

**Principal's table.**

| Lane | Capacity |
|---|---|
| Codex3 | 96 % left |
| Codex2 | 98 % left |
| Codex1 | 91 % left |
| Claude3 | 90 % used |
| Claude4 | 100 % used |
| Claude2 (root) | 74 % used |
| Grok | 500 credits |

There is no Codex4 row. The lanes with credit are Codex1, Codex2 and Codex3.

**Effects.**
1. **Claude4 can do nothing before its weekly reset, Fri 23-Oct 19:00Z (0242).** That includes the seal-render reserve.
   - Every Claude4 item already sits after Fri (A205 item 11), so no date moves.
   - The seal (step S7) starts no earlier than Fri 19:00Z, which is its existing target.
2. **Codex1 gets work again.** This supersedes A176's "move Codex1 work to Claude lanes" for new items:
   - (a) **The RUNBOOK successor review**, including Claude4's DN1/DN2 (A178). The RUNBOOK is root-built, so the review is cross-family. It moves off Claude4's post-Fri queue (A205 item 11(4)).
   - (b) **A non-gating second lens on the verdict-time A129 r11 and H3 r12 diffs.** This reduces Codex3's concentration (A205 item 13). Codex1 already reviewed generator v002 (0138).
   - Codex1 is not given the classifier B review (A205 item 7 stays with Codex2, because Codex1 wrote B's kernels) or the reviews of Codex2's builds (cross-family reviewers stay Claude4).
3. **Claude3 (90 % used):** only the r3a delta review at the seal, plus fallback for A205 item 1.
4. **The A205 dispatches go out as ruled**, with the all-lanes notice amended: Codex1 is not credit-constrained, and its two items above are added.

## A209: C1 (H1) approves six producers, as S4RC1 Q9(a) states; the registry verifier needs a c3v005 successor; real-gate run of record (root workflow wf_d994f2d3: builder plus an independent verifier) (2026-10-20 14:32:13Z)

**Finding.** C1 with the three canonical pins would make every HEADLINE11 call read INCOMPLETE.
- The per-state LO adapter 211a3220 (L676-678) and the SRB-ROT adapter 08e9ac0a (L384-387) each refuse unless they are approved.
- The handoff and the wrapper pass only the approved list (handoff L466, L502, L527; wrapper L192-194).
- Guard b1 rejects a GQ_SIGNED proof from 7044e131 unless 7044e131 is approved (L171-174, L112-114). Every valid r5 call has a signed offset state (A134 Q3).
- **c3v004 verify (F3)** refuses anything outside its three canonical pins. Both lenses re-ran this in-process: exactly 3 C1_APPROVED_PRODUCER_NOT_CANONICAL blockers.

**Rulings.**
1. **C1 `approved_certificate_producers`** holds six pins, in this order:
   - EPS adapter 4de70486;
   - GQ producer 2832ceb9;
   - slot proof cd10cd59;
   - LO state adapter 211a3220;
   - SRB-ROT adapter 08e9ac0a;
   - b1 evidence 7044e131.

   This is Q9(a) as written (rulings 56774ba7 L179). All three acceptance producers were reviewed before the freeze (Codex1 0142, 0146; A146, A158).
   - `trusted_source_producers` = [67fddd24, 7044e131].
   - The row producer 67fddd24 is **not** an approved producer, because it emits no certificate proof. This corrects A206 "Open for C1" and supersedes A207's "the three approved producers".
2. **No new producer can certify a prelaunch gate.**
   - 211a3220 writes only LO proofs, 08e9ac0a only SRB_ROT proofs, and 7044e131 only GQ_SIGNED or GQ_CURRENT_PREMISES proofs.
   - None writes EPS, GQ or LO_RHO_SLOT.
   - The registry 2dea408f is frozen, and its 31 bundles carry only pins 1-3 (verified from bytes).
3. **Verifier successor c3v005**, at the smallest possible change. Common c3v005 adds the three PINS lines and grows CANONICAL_APPROVED_PRODUCERS to six. Assembler c3v005 changes only COMMON_PATH, COMMON_SHA and its docstring. The registry, bundles and every producer pin stay byte-identical.
   - Built by a root workflow (builder plus verifier). **Codex1** reviews it as the distinct lineage; it reviewed the three acceptance producers and authored none of the c3 tools.
   - Root adopts it in V006 before C1 is frozen.
   - This supersedes A207's "registry_assembler_c3v004 verify against C1".
4. **Real-gate run of record.** A134 Q9 had Claude4 run it, but Claude4 is at 100 % until Fri 19:00Z (A208). The run of record is root's c3v005 `verify` (31/31, under taskpolicy -b), with Codex3's certificate_policy_review (A205 item 4(i)) and Codex1's c3v005 review as the distinct checks. C1 is frozen after that run (Q9(b)3). Disclosed in the seal entry.
5. **The Codex3 policy-review request is corrected before dispatch:**
   - V006 is the named exception to the NGC3198 rule, read at the listed entries only;
   - the C07 minimality check may open a1dcdea8 and lo_producer_cx2v004 5db60d0f;
   - no `synthetic` key in the review;
   - Codex3 writes its own check script under its own folder.
6. **The freeze tool is hardened before use** (verifier N2/N3/N5): `ok is True`, canonical-bytes comparisons, a path/regular-file/size/no-symlink/no-NGC3198 check on the review, and a distinct schema for synthetic output.
   - **HEADLINE11 admission (N6):** root passes the registry record's `bundle` as prelaunch_bundle, as h3_accept_call L281 does.
   - **Admission sources (N1):** they include guard b1 9e3fc109, core dc895f8a, parent v005 c75a889f, sensitivity 8fb06600, the adoption policy, and custody's imports, in addition to the existing map.
7. **Same defect in the S1 C1 (A182), verified from bytes.** KS6′ c8dc59a1 (L766) and G2 7eb456cd (L463) check their own approval, and G6b 65834e9b is likely needed as the GQ_SIGNED producer.
   - With three pins, S1 acceptance would read INCOMPLETE.
   - This goes to the S1 C1 policy review (A205 item 4(iii)) and the KS4′ verifier. Root rules the S1 C1 list before the S1 C1 is frozen (step S8).
8. **SENS needs a successor C1**, because `sensitivity_deciding_iii` is null. It is not on the HEADLINE11 path (all nine HEADLINE points read HEADLINE_NOT_GATED). Ruled when SENS is scheduled.

## A210: phase1 c2v003b is adopted (P-117 record); the BAND_AGREE pin binds v003b (2026-10-20 14:40:54Z)

**Object** (`claude_artifacts/phase1_c2/`, sha256 from bytes by root):
- tool `phase1_c2v003b.py` **7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4**;
- README `cf3a4de7`;
- HASHES_V003B `4ef119a7`.

**Review of record:** Claude3 0237, **PASS, 0 blocking** (A115), 6 NOTEs. One lens and one adversarial verifier, which reclassified nothing. 0237's sha256 is `183f250cad3eb29af49121a32f2283edfdd7204963397c6cfe3d96096e14ac09`.
- Band and L1 are AST-identical to the reviewed v002 `d64351ec`.
- The values-unbound attack is refused, and every honest at0b/at1 pair is admitted.
- E_A133_2(b) holds exactly (max relative error 3.2e-16 against exact rationals).

**Rulings.**
1. **phase1 c2v003b `7d891ff7` is the phase1 tool of record.** This meets A142 item 4's condition: the review returned 0 blocking before the seal entry.
   - The BAND_AGREE pin and both classifiers' v003b binding (A168, A171) stand.
   - The fallback `d64351ec` is not used.
2. **N1 and N3** are ruled in the RUNBOOK rulings entry that follows (the A210 workflow output, written as the next entry).
3. **P-112's precondition "phase1 v003b adoption recorded" (A205 item 8) is met.**

## A211: the NGC acceptance stack of record is adopted on Codex2's P-106 review (0530: PASS, 0 blocking); values writer v004 is unblocked (2026-10-20 14:44:17Z)

**Review of record:** Codex2 0530.
- `review_ngc_acceptance_cx2/RESULT_CX2V001.json` `3b40a3445d67cd88`; REVIEW `8666ece8`; pin and diff verification `eebde2c3`.
- Suites: 40/40 MUST_PASS and 59/59 MUST_FAIL, twice. Independent checks 98/98. Mutants 8/10 killed; the 2 survivors are order-only and are expected (N1).
- All 36 byte pins and both published diffs were verified.
- Findings F2 and F3 are labelled same-lineage, as A205 item 6 requires.

**Adopted** (sha256 from bytes by root):
- NGC LO-state adapter `ngc_lo_state_adapter_c2v003a.py` **9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2**;
- NGC acceptance handoff `ngc_acceptance_handoff_c2v005.py` **7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1**;
- roster recipes `ngc_roster_recipes_c2v002.py` **c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e**.

This supersedes A181's "Claude3 review" condition (A205 item 6). PLAN P-106 is DONE.

**Consequences.**
1. **Values writer v004 (A159, A205 item 9) may start.** It pins handoff c2v005 `7077ad93` (schema and sha) in MEMBER_ACCEPTANCE_PRODUCERS and requires the route NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE. Codex2 builds it and Claude4 reviews it, deriving the schema and route from the handoff's bytes.
2. **N3: point custody admits exactly the four registered S0 keys** (adapter L455; ρ producer L275).
   - Every Phase-1 member or F point outside S0 needs a root point registration (NGC ρ registration, as R2-R4 do for S0) before its acceptance.
   - The deciding test is acceptance at each newly registered point.
   - This goes into the P-112 brief, and root writes each registration when u_A fixes the actual set.
3. **N2:** the suite's P29 parses the hash-only row contract before its blocked manifest open. This is a test-scope gap only (0529). The contents were neither shown nor used, and the contract is target-free. No reviewed file changed.
4. **UNTESTED:** first real-call S5/N, actual reuse/profile/caller decode, and real post-run acceptance. The deciding tests are the first real S0 call and its acceptance.

## A212: values writer v004 (Codex2 cx2v002) passes root verify, PASS_WITH_NOTES with 0 blocking; Claude4's review is next (A205 item 9) (2026-10-20 15:11:16Z)

**Object:** `claude_artifacts/values_writer_cx2/values_writer_c2v004_cx2v002.py` **26319ecbfaf944c80c5df91a0c592899727e6ff9f5177404ebc49309bd906f0e**. Builder Codex2 0536: 233/233 tests, 9/9 mutants killed.

**Root verify** (root workflow wf_2d700e2a). Results are in `values_writer_cx2_rootverify_c2/`; RESULT `ffc6f8f1`, HASHES `b1481e2a`.
- **Hashes:** all 18 HASHES lines match.
- **AST:** 27 of 29 top-level definitions are identical to v003a 965ed282. Only check_acceptance and values_point changed.
- **A159 holds line by line:**
  - the handoff schema and sha `7077ad93` are pinned (L86, L87, L93, equal to handoff L108);
  - the exact route is required (L92, L651-652);
  - Phase-1 valid[q] is gated on ACCEPTED or LO_UNCERTIFIED_TRANSIENT (L679-681);
  - O-1: ACCEPTED_PASS_FLAGGED reads false (L90, L661);
  - O-3 is unchanged, printed and not applied;
  - DDO-schema records are refused (L646-647);
  - the A152 pin equals the live section bytes.
- **Reruns:** gate 67/67 twice, ported suite 166/166 three times, mutations 9/9.
- **Root's own adversarial tests:** 85/85 twice, covering route near-misses, one-nibble sha changes, schema near-misses, the Phase-1/Phase-2 reading matrix, and binding swaps. Root's 6 mutants are all killed.
- **Data access:** no NGC3198, ~/.codex or post-seal open, confirmed by the open-guard logs.

**Notes** (none blocking; for Claude4's review and successors):
- **N1:** the README reproduction fails outside its folder, because the wrapper guard refuses its own synthetic reads. A successor wrapper should allow reads under --work.
- **N2:** Codex2's gate suite does not kill 4 of root's mutants (sha prefix, route substring, sha without path, schema normalisation). The shipped code uses exact equality, so its behaviour is correct.
- **N3:** the L88-89 comment is stale, and the L659 g5 branch is dead.
- **N4, operating rule:** a handoff record refused before L605 has no `result`, so the writer refuses the whole assembly (fails closed). For such a point, root passes acceptance=None or reruns acceptance.
- **N5:** eligibility comes from `reading` alone. member_lo_ok and blockers are not cross-checked, and only the handoff's sha is checked, not its path.

**UNTESTED:** real-call assembly. The deciding test is root's first accepted real-call assembly.

**Adoption:** v004 is adopted after Claude4's review returns 0 blocking (after Fri 23-Oct 19:00Z). It is needed at the Phase-1 freeze.

## A213: verifier successor c3v005 is built and passes root verify (PASS_WITH_FIXES, 0 blocking); Codex1 reviews it (0775); the C1 policy request goes to Codex3 (0774) (2026-10-20 15:14:14Z)

**Build** (root workflow wf_a869d821, a builder and an independent verifier), in `claude_artifacts/s4rc1_c3/build_c3v005_c2/`:

| File | sha256 |
|---|---|
| common c3v005 | **2308a47ce3c758b6befa0aa954fa7e2b6ad7f4cb41ed73d4b8cd1d257021e7c5** |
| assembler c3v005 | **7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310** |
| tests | `a18db5b9` |
| mutation check | `bbf55b5c` |
| CHANGES | `f262103d` |
| HASHES_C3V005_C2 | `3f51c7a2` (8121/8121 OK) |

- **The change is minimal, as A209 item 3 requires** (independent AST compare):
  - common: only PINS (+3: 211a3220, 08e9ac0a, 7044e131) and CANONICAL_APPROVED_PRODUCERS (six, in A209 order) differ;
  - assembler: only the docstring, COMMON_PATH and COMMON_SHA differ.
- **Suite:** 310/310, of which 295 are the c3v004 cases with the same ids and 15 are new. The verifier re-ran it. Mutations: 9/9.
- **F3, in-process:**
  - six pins pass, and three pins still pass;
  - a seventh pin (67fddd24) gets exactly 1 blocker;
  - aliased paths are refused, and so are `ok=1` and reordered review lists;
  - c3v004 refuses six pins with 3 blockers.
- **The registry is not rebuilt.** 2dea408f and 1164bb48 are unchanged.

**C1 successors** (root scratch, `c1_h1/`; they are copied into the C1 folder at the freeze):
- draft v002 `3a9299a3`: tail_readiness is unchanged, and its digest without the review is `6dc87838`;
- freeze tool `fill_c1_pin_c2v002.py` `3faf4a6c`: 41/41 tests;
- steps v002 `7f173b91`.

**Verifier notes, with root's disposition:**
1. **c3v005 verify checks producer membership, not producer per gate.**
   - The evidence for A209 ruling 2 (no new producer certifies a prelaunch gate) is the byte check of the frozen registry 2dea408f: 93/93 proofs come from pins 1-3. Codex3's C06 confirms this independently.
   - The acceptance path inherits prelaunch proofs from the registered bundle (handoff v004 L519-520).
   - Disclosed in the seal entry.
2. **Verify does not enforce the order, uniqueness or completeness of C1's list.** "Six in A209 order" is enforced by the freeze tool's constant digest `6dc87838`. Verify runs only on the freeze tool's output.
3. **The freeze tool does not check q3_rule and q8_rule.** Root reads them before the fill, and 0774 says so.
4. **Optional hardening for a fill v003, if one is ever needed:** inf literals, casefolded `synthetic` keys, and requiring the review path under `cert_policy_reviews_cx3/`. Root checks these by hand at the fill.
5. **Line cite:** h3_accept_call v004 `eb895263` L279-282, not L281 (corrects A209 item 6).
6. **The `adoption_policy` N1 admission source** is the post-verdict r11 policy (A129). Its pin is filled at the verdict, not now.
7. **The scratch provenance pins in draft v002** are replaced by claude_artifacts copies at the freeze.

**Next:**
1. Codex1 reviews c3v005 (0775), and root adopts it on 0 blocking.
2. Codex3 signs the C1 policy review (0774).
3. Root fills and freezes C1, then runs c3v005 verify (31/31, under taskpolicy -b) as the real-gate run of record.

**UNTESTED:** the real verify (real custody for 31 points), the real-mode fill, and the N1 transitive closure. Deciding tests: root's step 3, root's step 2, and the first HEADLINE11 PRELAUNCH.

## A214: the classifier B distinct-lineage review is PASS with 0 blocking (Codex2 0537), and CA1 is ruled (2026-10-20 15:16:27Z)

**Review** (A205 item 7; cross-family: Codex2 reviewing a Claude2 build on Codex1 kernels). REVIEW `19c9c2cb`, RESULT `939e5344`, B-only evidence `9f11273a`.
- **Results:**
  - B's suite 327/327, twice;
  - shared-CLI agreement 364/368; the 4 differences are forged-only A115 NOTEs, the same 4 as the agreement record;
  - classifier-form comparisons 14/14;
  - independent clause checks 158/158;
  - kernel pins 15/15 unchanged.
- **B's READ_LOG** shows no forbidden A read.
- **Counts:** B_DEFECT 0, A_DEFECT 0, CONTRACT_AMBIGUITY 1.
- **The A176 barrier holds.** The A_SIDE file is for Claude4 only (`430d4b95`, count 0), and root did not open it.
- **Disclosure update** for the seal entry and the PROVISIONAL label: classifier B is a Claude2 integration on Codex1 kernels, and it now has a Codex2 cross-family adversarial review that passed with 0 blocking. A176's "partly same-family" caveat stays, with this review cited beside it.

**CA1 ruling** (root ruling shared by both classifiers, A176 §1; routed into the seal entry under M-6 item 2, with no change to the r3a text).

r3a C-6.1 reads: "Otherwise the alternative reads TWIN_INVALID, and only its scored member distribution is reported." C-6.3 points the same way for STAGE0. Both classifiers' adopted output (schema C4V003 L6832) carries only the reference twin's hit count.

**Ruling.**
- The member distribution under TWIN_INVALID is a **report item, not a classification output**.
- Classification and the TWIN_INVALID reading are unchanged and correct, and no classifier successor is made.
- **Root's score report prints, for every alternative that reads TWIN_INVALID**, the scored member distribution from the frozen values: per member, HIT/MISS/INVALID counts over the alternative's scope. This is computed with the same M-T row rule, with no NEAR and no P10.
- It sits beside the classifier's twin-count line, under the alternative's name, and is never headline.

This makes the report fuller and changes no reading. It applies in any phase in which an alternative reads TWIN_INVALID. The report script is part of P-107's score step.

## A215: registry verifier c3v005 is adopted on Codex1's review (0160: PASS, 0 blocking) (2026-10-20 15:19:51Z)

**Review of record:** Codex1 0160.
- Result `review_final_deltas_cx1/REGISTRY_C3V005_REVIEW_CX1_V001/RESULT.json` `c2511626`.
- 310/310 inert cases, 9/9 mutations, the exact delta, the producer hashes, and the frozen registry/bundle/manifest associations.
- Distinct under A115: Codex1 authored none of the c3 tools.

**Adopted:** common c3v005 `2308a47c` and assembler c3v005 `7df1c481` (A213), in `s4rc1_c3/build_c3v005_c2/`. This is the registry verifier of record for C1. It supersedes c3v004 for that purpose (A209 item 3).

**Codex1's notes, accepted as written:**
- Root's disposition of verifier note 1 is accepted narrowly, for the frozen registry 2dea408f. Codex3's C06 and root's real verify are still required before launch.
- Membership is not per-gate enforcement, and no general producer/gate guarantee is claimed.
- Order, uniqueness and completeness are enforced by the freeze digest, not by verify (A213 note 2).
- A three-pin pass is compatibility only, not approval of the final C1.

**Next:** Codex3 signs the C1 policy review (0774). Root then fills and freezes C1 with fill_c1_pin_c2v002, and runs c3v005 verify (31/31, under taskpolicy -b) as the real-gate run of record (A209 item 4).

## A216: C1 (H1) is frozen. The real-gate run of record, c3v005 verify, passes 31/31 with 0 blockers (2026-10-20 15:27:02Z)

**Certificate policy review:** Codex3 0666, `cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V001.json` **f848888f7778124414302b8f216813f44dcdf89c594a4a3c066c17da887b6bdc**; check script `41249866`.
- C01-C12 all PASS, and blocking_findings is empty.
- **Root's checks by hand** (A213 notes 3-4):
  - `ok` is a boolean true;
  - no key reading `synthetic` in any case;
  - no non-finite numbers;
  - the review path is under `cert_policy_reviews_cx3/`;
  - the six producers are in A209 order;
  - q3_rule (A134 Q2/Q3 with A158: tail-ON direct calls are read only after post-run per-state acceptance) and q8_rule (A134 Q8; CP-1 EPS 31/31, A203) were both read.

**Fill** (`fill_c1_pin_c2v002.py` `3faf4a6c`, draft v002 `3a9299a3`), exit 0, WRITTEN.
- **C1** = `claude_artifacts/c1_h1_c2/C1_H1_C2V001.json` **4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1**, schema UNT_DDO154_C1_TAIL_READINESS_H1_C2V001.
- c1_tail_readiness_digest `2e39e1535e550f50613c155c8fc68ec58287d5c8790597bb2e0c5a7964f0caf8`.
- Logs: `CLAUDE2/C1_H1_ROOT/`.

**The real-gate run of record** (A209 item 4): `registry_assembler_c3v005.py verify` under taskpolicy -b, against registry 2dea408f and this C1. HASHES_C3V005_C2 was 0 failures before the run.
- **Exit 0: `{"ok": true, "n_ok": 31, "n": 31, "c1_policy_gate_blockers": []}`.**
- Record: `s4rc1_c3/registry_c1verify_c2v001/VERIFY_2dea408ff698_20261020T152643Z.json` **551d92400c87e9539d736e7097eea09f38adcb1625f27fdccaf142f428f5a45c**.
- This closes the A209/A213 UNTESTED items on the real verify and the real-mode fill: both are now TESTED.

**C1 is frozen as of this entry** (Q9(b)3). It comes before HEADLINE11's first PRELAUNCH, and the registry was frozen earlier (A207).
- **Distinct checks:** Codex3's certificate_policy_review and Codex1's c3v005 review (A215). Claude4's Q9 real-gate role is held by root's run (A209 item 4), as disclosed.
- **Evidence for A209 ruling 2** is the byte check of 2dea408f: 93/93 prelaunch proofs come from pins 1-3 (root's checker, and Codex3's C06).

**Step S2 is DONE:** 31/31 EPS, the registry assembled, C1 written, the certificate policy signed and verified.
**Still UNTESTED:** the N1 transitive closure. The deciding test is the first HEADLINE11 PRELAUNCH.

## A217: the campaign-set review is PASS with 0 blocking (Codex3 0667), and P-111 is DONE (2026-10-20 15:31:19Z)

**Review of record** (A205 item 3, superseding Claude4 in A192/A194/A196): Codex3 0667, `review_campaign_set_cx3/CAMPAIGN_REVIEW_FINAL_CX3V003.md` `937812ed`.
- **Results:**
  - H3 94/94, twice;
  - campaign certification 90/90, twice;
  - Codex3's own adversarial tests 53/53;
  - generator 36/36;
  - HEADLINE construction 86/86 (`HEADLINE_CONSTRUCTION_CX3V001.json` `76f5f786`).
- **All nine of root's predicted HEADLINE11 spec shas (0778) are reproduced.**
- **Confirmed:**
  - the A194 capability-row reading;
  - the first-pass, third-pass and latest-record rules;
  - the F6 classes and the D5 judgment-call flag;
  - ledger and cache identity, and truncation on use;
  - CP-1 list-mode and signer wiring;
  - post-acceptance storage counting.

**Residuals (operating rules for root):**
1. **A196's direct-handoff first-pass bypass is not closed mechanically.** Root operates every campaign acceptance only through `h3_accept_call_c2v004` (A196), and the zero-blocking judgment depends on that.
2. **Handoff byte-identical repeats are idempotent,** not refused outright. Different content is refused.
3. **At H1, before HEADLINE11's first launch,** root compares the FINAL manifest's `binder_pins` with the nine predicted shas (0778 table D). Any mismatch stops the launch.
4. **Concentration** (A205 item 13) is disclosed in the seal entry.

**PLAN:** P-111 is DONE. P-109 stays ACTIVE until it is finalized with the verdict tuple (A188).
**Still open, under root investigation** (root workflow wf_483c096f): whether the adoption policy's L98-102 block-equality check refuses W1's config, and the PRELAUNCH generator for the guard014 path.

## A218: two launch-path findings ruled before the verdict (root workflow wf_483c096f: an investigator and an adversarial verifier per issue). (1) The PRELAUNCH emitter for guard014 batches. (2) S4-R-A1, the numerics block equal to the adopted C4T block, in the H1 and W1 configs (2026-10-20 15:44:36Z)

### (1) PRELAUNCH on the guard014 path: no build needed; ruled now

**Finding.**
- PRELAUNCH005 `117b3520` pins guard011 (L12-13) and refuses a candidate plan naming any other guard (L31 GUARD_IDENTITY).
- guard014, launcher015 and binder c2v011 (A186) replay the PRELAUNCH record (guard014 L395-396), but nothing on that path writes it.
- No emitter pinned to guard014 exists.

**Verifier's resolution, adopted.**
- The guard011 and guard014 `native_preflight` are code-identical (diff: only the docstring, the inserted c2v012-014 block and `validate` differ), and the record carries no guard identity (guard014 L270).
- Synthetic tests T5 and T7, re-run independently: a PRELAUNCH005 record made from a guard011-named candidate is byte-equal and PASSES guard014 replay.
- The PRELAUNCH002 two-guard precedent applies (INTERFACE_V002).

**Ruling.**
- (a) The step-4 emitter for guard014 batches (HEADLINE11, DIII4, SENS_LO9/HI9, POST_S1) is **PRELAUNCH005 `117b3520`, unchanged**, as the frozen C1 names it.
- (b) Its input is a **candidate plan that names guard011 `eb97e303`**, with every call's prelaunch null (L31, L56). It is never bound.
- (c) guard011 stays in the admission sources and in the source review's approved sources (A139). guard014 and launcher015 are added there too, as guard014 L369 requires.
- (d) The **plan of record** given to binder c2v011 names guard014 and launcher015, and uses the C2V004B rule (A186 N1).
- (e) **Check:** Codex1, the PRELAUNCH lineage, re-runs synthetic T1-T8 as a distinct confirmation (dispatched).
- **Errata to C1_ROOT_STEPS_C2V002 §5.3-5.4:** the admission sources also list guard014 and launcher015, and the binder is c2v011. Pinned bytes are not edited. The frozen C1 is unaffected.

### (2) S4-R-A1: a real blocker, ruled

**Finding.** Both lenses confirmed it from bytes, and an in-memory probe used the real policy.
- Adoption policy `93d9c0ac` L98 binds `block_source` to the spec the adopted C4T result ran with. That can only be FILLED `de6d7d77`: the driver refuses PENDING slots in run mode, and L100 needs a COMPLETED, valid result.
- L102 compares that spec's numerics with the config's `numerics.block` exactly.
- The W1 base v004a `63dac53d` (and any H1 config built from it) carries `PENDING_UV_TAIL_CERTIFICATE` in `uv_tail.eps_certificate` and `lo_certificate`. FILLED carries the C4T certificates. The blocks differ only at those two leaves.
- **Result:** `V007_BLOCK_DIFFERS_FROM_ADOPTED_C4T`.
  - W1 stops at README H3 V4 (CANDIDATE_GATES_NOT_PASSED), then at `run`.
  - HEADLINE11 stops if C1_ROOT_STEPS §5 is followed as written; producer v004 L709-713 refuses as well.
- r11 and r12 keep L102 (the generator changes P5/P6 only).
- Claude4's DRYPLANS_C4V003 L190-192 and L225 found this as S4-R-A1, but it was never ruled and never carried into the H3 path.

**Ruling (S4-R-A1).**
- At the verdict, **`numerics.block` := block_source `de6d7d77` `.numerics`, canonical-equal.** This applies to:
  - the H1 run config, before HEADLINE11's first producer or PRELAUNCH run;
  - the W1 candidate config, before README V4.
- **The policy bytes do not change.** L102 is r7's reviewed check, shared by r10, r11 and r12.
- **Physics is unchanged (FORMAL).**
  - Core Mapper L249-259 and ledger wrapper L586-591 overwrite both slots from the registry for every registered point.
  - `point_identity` and the deciding check strip the slots.
  - So the nine HEADLINE11 spec shas (0778), the seed spec, the A192 reuse test and the wave-1 key 968c915b are all invariant.
- **What is lost:** the driver-level PENDING backstop for an unregistered point. Two checks still cover it: the certificate_policy gate requires the registry (wrapper L143-150), and prelaunch_check runs certificate_check for every point (L290-298).
- **Cache ids change.** The base_spec_sha256 enters the parent key (L1774-1777), so the parent id 1ce0ef41 and A191's ce6a1a6b expectations are re-stated when the W1 config is built. No W1 work dir exists yet.

**Builds:**
1. **`apply_h3_fields_c2v004`, built by Claude2** (a root workflow). It may set `numerics.block` only to the value derived from the pinned block_source bytes. It refuses unless `strip_slots(new) == strip_slots(old)`. The flat diff of a string slot replaced by a dict is 6 keys.
2. **A test successor:**
   - MUST_FAIL: an unchanged block refuses with V007_BLOCK_DIFFERS;
   - MUST_PASS: the derived block passes;
   - MUST_FAIL: a FILLED base plus an unregistered point refuses.
3. **Errata** to README_H3 C2V001 L67, L127 and L158, the fields template L182, and C1_ROOT_STEPS §5 (the block line).
4. **Reviewer: Codex1**, cross-family. Codex3 is not used, to avoid adding to its concentration.
5. **PLAN:** under step S5, attached as P-122.

## A219: A218(1) is confirmed by a distinct lane. Codex1 0161: PASS, 0 blocking (2026-10-20 15:49:17Z)

**Result:** Codex1 `review_final_deltas_cx1/PRELAUNCH_G14_REVIEW_CX1_V001/REVIEW_RESULT.json` `10b07e90`. T1-T8 all as expected:
- PRELAUNCH005 on a guard011-named candidate gives a record byte-equal to a guard014-pinned successor's (T5 = T2);
- guard014 `validate` with native replay passes the original PRELAUNCH005 record (T7);
- tamper and missing-record refusals hold (T4, T8).

**Independent diff.** The module prefix through `native_preflight` is AST-identical between guard011 and guard014. That covers imports, constants, helpers and the audit fence.

**Codex1's note.** The harness's first run, with its scratch under /Research/, failed T2/T5 (UNPINNED_PREFLIGHT_SOURCE) but still exited 0. This is a portability and exit-status limit of the harness, not a replay defect. The failing run was preserved, and a fresh /private/tmp scratch gave all eight expected outcomes.

**A218(1) stands.** HEADLINE11 and the other guard014 batches use PRELAUNCH005 unchanged, with a guard011-named candidate.
**UNTESTED:** real production inputs and the binder CLI. The deciding test is the first HEADLINE11 PRELAUNCH and its bind.

## A220: apply_h3_fields_c2v004 (the S4-R-A1 fix) is built and passes root verify (PASS_WITH_FIXES, 0 blocking; root workflow wf_57e8e5b5); Codex1 reviews it (0780) (2026-10-20 16:37:42Z)

**Build** (`h3_campaign_path_c2/apply_fields_c2v004/`):

| File | sha256 |
|---|---|
| tool | **b3e8b7d3e8f3996399b1a18d5b281c71e92769f119deea42cda497a66d722434** |
| tests | `bbf862f7` |
| mutation check | `3d8639a1` |
| diff | `7bf83bce` |
| errata v001 | `64be32f9` |
| errata v002 | `83078bb5` |
| cache-id restatement | `3e83ab74` |
| HASHES | `2bb798b9` (11,721 entries, 0 mismatches) |

**Tests and checks.**
- Suite 41/41, twice. The c2v003 suites pass unchanged with c2v004 swapped in: 90/90 and 77/77. Mutants 10/10 caught.
- **One new operation:** `--block-source <FILLED path> --block-source-sha256 de6d7d77…` sets `numerics.block` := FILLED.numerics.
  - The pin is checked on both path and sha.
  - It refuses unless the old and new blocks are equal once the slots are stripped.
  - It re-reads the output to confirm.
  - Without the flag, the output is byte-identical to c2v003. The policy bytes stay `93d9c0ac`.

**Independent verifier.**
- **AST:** only the new path differs.
- **Adversarial suite: 24/24, twice.** It covers 14 kinds of hidden non-slot change, float and key canonicalization, TEMPLATE `13cfe988` as the source (refused), 9 pin-spelling variants, delta attempts, and the CLI.
- **Real policy:** the unchanged block reads exactly `V007_BLOCK_DIFFERS_FROM_ADOPTED_C4T`, and the derived block passes. The r12 placeholder policy gives the same readings.
- **Invariance (TESTED in memory and FORMAL):**
  - all 9 HEADLINE11 spec shas (0778 table D) are unchanged;
  - the seed key 968c915b is unchanged, and the seed spec under 2dea408f is `6e6a4de1…`, the same under both blocks;
  - all 31 registry identities carry numerics equal to the slot-stripped block `0f004670`.

**Cache ids change** (CACHE_ID_RESTATEMENT):
- base spec f8785f12 → cab952c4;
- parent id 1ce0ef41 → 80759c52;
- A191's ce6a1a6b and the run sheet's 878d612a are superseded. W1's own wrapper id is known from the final W1 config.

**FIX-1 is applied by ERRATA_S4RA1_C2V002:** `6944e210` is the seed's point key, not a spec sha.

**Notes:**
- **N1:** the block_source is read twice. This is covered by the report's `to` = `cdbf988e` and the §5 re-check.
- **N2:** a `--block-source` without its sha exits 1, not 2. Nothing is written.
- **N4:** the real r5 `prelaunch_check` on the FILLED base is UNTESTED. It is FORMAL-positive, and the deciding test is the first HEADLINE11 PRELAUNCH or W1 `plan`.

**Verifier process disclosure:** two name-only `find` lookups, against A137's named-paths rule. They printed paths only.

**Ordering:** the block goes in at README V3, before the HEADLINE11 evidence assembly and V4.
**Adoption:** on Codex1's review with 0 blocking (0780).

## A221: Codex1 0162 FAILs apply_h3_fields_c2v004 with 1 blocking item, which is accepted; E_A220_1; a c2v005 successor is commissioned (2026-10-20 16:43:44Z)

**Blocking item CX1-S4RA1-01** (Codex1 `review_final_deltas_cx1/APPLY_H3_C2V004_REVIEW_CX1_V001/REVIEW_RESULT.json` `68fcf7b8`):
- `pin_problem` hashes one read of the block_source file, and `block_derived` parses a second read.
- **The attack:** a second read that differs only at a permitted slot is accepted, and the report still names the original pin.
- So the derivation is not proven to come from the pinned bytes, as A218(2) requires.

**E_A220_1.** Root's verifier recorded this as N1 (INFO; adversarial T10), and A220 called it covered by downstream checks. That disposition was wrong: a tool whose job is derivation from pinned bytes must refuse, not rely on a later check.
- **Rule:** a demonstrated provenance gap in a pin-binding tool is blocking, even when a downstream check exists.

**Codex1 accepts the three stricter choices:** the exact path pin, the `block_source` field equality, and the refusal of a stray sha flag.

**Fix (root workflow wf_a6902b81):** `apply_h3_fields_c2v005`.
- It reads the block source once, hashes that buffer against the exact pin, and parses and derives from the same buffer.
- **Regressions:**
  - a read-counting audit (exactly one read);
  - a read-changing fixture;
  - a mutant that reintroduces the double read, which must be caught.
- Codex1 re-reviews it.

**c2v004 is not adopted.**
**Status:** P-122 stays ACTIVE. Schedule: no effect, since this is needed at README V3, after the verdict.

## A222: apply_h3_fields c2v005 fixes CX1-S4RA1-01, but its verifier FAILs it on the same defect in the seal-record path; ruling: every pin-binding read in the tool is single-read; c2v006 commissioned (2026-10-20 17:13:17Z)

**c2v005** (`apply_fields_c2v005/`, tool `6c6c6d08`; root workflow wf_a6902b81).
- `block_derived` reads once (L230), hashes that buffer (L233) and parses the same buffer (L239).
- **Tests:** 50/50, twice. The c2v003 suites pass with c2v005 swapped in: 90/90 and 77/77. Mutations 12/12, including the double-read mutants M11 and M12.
- **Codex1's exact attack:** accepted on c2v004, defeated on c2v005 (1 read, output byte-equal to the honest run).

**Blocking item VF-C2V005-01** (root verifier):
- `seal_derived` (c2v003 L151/L156, c2v005 L197/L202) hashes one read of the seal/verdict report and parses a second read.
- The prereg object from that second read is written into `numerics.sealed_prereg` (L208).
- A probe shows c2v003, c2v004 and c2v005 all accept a second read that adds a key, and write it.
- This has been present since c2v003. It is caught before any use: the tool runs only at README V3, after the verdict.

**Ruling (applying E_A220_1, A221).**
- **Every** pin-binding read in apply_h3_fields reads the file once, hashes that buffer against its pin, and parses that same buffer.
- c2v006 sweeps the whole module for pin-then-reread patterns, including helpers and `open`, and fixes each one.
- **Each fixed path gets:** a read-counting fixture, a static AST check, and a mutant that reintroduces the double read.
- **Reviewers:** the root verifier, then Codex1's re-review.
- **c2v004 and c2v005 are not adopted.**

**Register.** The same class of defect could exist in other pin-binding tools written in the same pattern (`pin_problem` then a re-read). A sweep of the launch-path tools (H3 entry, regenerator, ledger wrapper, campaign generator, fill tool, registry assembler) is queued as a root verification task before the verdict-day runs.

## A223: RUNBOOK rulings G13, G15, G25, G27, G7, G16, G24; 0237 N1/N3; 0248 VN1/DN5 (2026-10-20 17:23:31Z)

**Why.** P-112, the Phase-1 NGC member/F launcher, starts on these rulings (A205 item 8). Its other precondition, the P-117 record, is met (A210). The S0 launch needs the receipt status map named before its first launch (RUNBOOK L140), so this entry stands before the S0 M-15 record. No ruling here changes a registered method, threshold, prereg text or sealed object, except the disclosed pre-result registrations under A133 §3 (L201): DN5, UNEVALUATED_INFRA_REPEAT and UNEVALUATED_CUSTODY_BREACH. Where a ruling reads registered text, it is listed under "Disclosed readings". This is the RUNBOOK rulings entry A210 item 2 names; A211 to the entry before this one were written before it.

**Source.** Root workflow wf_16e496bf: a drafter and two refutation lenses (physics/blinding: 8 AMEND, 5 HOLDS; implementation: 9 AMEND, 3 HOLDS). Every AMEND fix is applied; where the lenses differ, the stricter or more explicit one is taken (root decisions D1-D15). Two fixes are not taken:
- both lenses proposed moving some infrastructure deaths out of FAILED; D2 reads them literally instead (G13);
- lens 1's G13 fix 3 (the twin reading TWIN_NOT_USED, with the kit retrying INFRA twin attempts) is replaced by D3's twin mode (G25 item 8).

Root workflow wf_bbfb82d5 then checked the synthesis against the sources and found 15 defects. Each is fixed in this entry. A second check of that version found 10 more (the custody successor's form, the custody-copy timing, the sampler's time comparison, the cutoff's T, a non-attempt MISLAUNCH, D7's edge cases, the next-attempt order, and stale citations, lineage and stamp). Each is fixed here too. A third check found 4 more (a monitor that ends without writing its receipt, the brief's reading of the rule-(c) pair, V006 entry spans that go stale before insertion, and the brief's custody-copy scope), and each is fixed here as well. A fourth check found 5 more (no machine form for root's ruling on a residual, a LAUNCH with no run directory, a monitor still alive with no .launch.json at the launch bound, the TOOL_PIN line's grammar, and the undefined sample flag `complete`), and each is fixed here as well. A fifth check found 7 more (a root-written MONITOR_REFUSED record that fails its own acceptance after the same-k relaunch, residual checks run with no mount check, a hold after a second monitor refusal that nothing enforces, an absent `.launch.json` caught by the mismatch rule, NGC tools adopted after A212 and before this entry, a stale V006 citation, and small text fixes), and each is fixed here as well.

**Read.** RUNBOOK_V002_C2V006 `e162db3e`; builder c2v006 `0cc73106`; root_monitor_c2v001 `ba031c23`; driver cx3r008 `577f8c94` on its live path (cmd_run L9208 → _ngc_v011_dispatch L9194 → strict clone L8989-9102); S0 kit C2V003A `fdc0ee6c`, serial script `621263a2`, twin script `f199544d`, kill watch `a3d70bec`, record writer `a10965b7`; phase1 v003b `7d891ff7`; orchestrator c2v005 `c75a889f`; filler `ec417e76`; A133 `cd92ef91`; r3a sc3 `c64f65a3`; V006 `6565c973` (285,659 B, through A221; last written at 16:43:44Z by its modification time, and unchanged at 16:45:14Z, 16:58:10Z, 16:59:21Z and 17:08:48Z; it was `339458c5`, 284,051 B, through A220, at 16:43:13Z). A205-A219 read by heading at 15:57:53Z, A220 at 16:43:13Z, and A221 at 16:59:21Z. V006 ends with an unnumbered, unstamped heading, `## A108 continued`, after A221; it was read by heading only, and its content is not checked here. At insertion, root reads by heading every entry added after A221, and that heading, confirms that none changes a ruling here, and updates the V006 sha and these spans. A210 (phase1 v003b), A211 (the NGC acceptance stack and N3) and A212 (values writer v004) are used below; A213-A221 change no ruling here. By heading, A220 is the S4-R-A1 fix (apply_h3_fields_c2v004; failed at A221), and A221 records Codex1 0162's FAIL of it and commissions a c2v005 successor. The tools built or adopted at A213-A221 are not NGC launch-path tools: registry_assembler_c3v005 is the S4-R-C1 calibration certificate registry and offline verifier, and apply_h3_fields_c2v004 applies the H3 fields to a DDO154 calibration RUN_CONFIG (from their paths and docstrings).

Not opened, except as disclosed next: any NGC3198 target, observed-velocity, sigma or slots file; run outputs; V007_POSTSEAL_RECORDS; ~/.codex.

Disclosure from the fixer round: a sha search ran `shasum` over the JSON files up to depth 4 under claude_artifacts before it was stopped. It may have read the bytes of NGC3198-named files, slots V003 among them. It printed four sha lines and no file content. The four were ROOT_TSR_FLAG_RECORD_V001, the two carrier policies and the K32 compare.

**Finding (TESTED on synthetic records shaped like the real ones).** Builder c2v006 cannot build from the real Phase-1 records:
- root_monitor nests the spec sha and caps and writes no θ, host RAM or solo value. c2v006 reads top-level keys only, so every receipt refuses RECEIPT_CALL_BINDING_MISSING, a FINISHED one included.
- The monitor receipt is the sibling `<outdir>.receipt.json`. c2v006 requires it inside run_dir, so it refuses RECEIPT_NOT_IN_RUN_DIR.
- The kit's M-15 record UNT_M15_PRELAUNCH_RECORD_C2V001 refuses INPUT_KEY_MISSING.

The S0 kit's records stay the records of record. A post-run attempt receipt (G27) and builder c2v007 adapt to them. The S0 kit needs no change.

### G13: the call set, the Phase-2 sensitivity registration, the status map

**Question.** RUNBOOK L402-405: which calls step 4 waits for; how Phase-2 sensitivity entries are registered; the one status map per receipt producer.

**Ruling.**
1. **The Phase-1 call set** (A133 L77-90):
   - the PRIMARY members, kind MEMBER;
   - F0, F1 and F2, kind OTHER. An F point at a member's exact θ is that member's call (A133 L86);
   - the identity twin S0_SEED_CW8_TWIN, kind OTHER. Its planned stop is its terminal.
   - An S0 serial whose θ is neither a member's nor an F point's is outside the set. It is not registered and never read, and step 4 does not wait for it. Root stops it as soon as the set is fixed at u_A (G25 item 7).
   - Step 4 begins when every call of the set has a terminal attempt receipt (A133 L210).
2. **The Phase-2 sensitivity registration** is RUNBOOK §3 2c, with two exceptions:
   - an entry at an (alternative, θ) that already has any registered call is that call. It is registered as SENSITIVITY with that call's spec sha and a call record identical to that call's, and it is not relaunched;
   - an A16.4 entry (VN1) is never launched or registered.
3. **The status map** for root_monitor_c2v001, read through the attempt receipt (G27).
   - **Raw status** = `<monitor status>|<driver_status or NONE>`, both taken from the monitor receipt. CHILD_FAILED with no driver status gains `|SIGNAL` (exit_code < 0) or `|EXIT` (otherwise).
   - **Overrides, in this order:** MISLAUNCH, then TWIN_PLANNED_STOP, then the composite string.
     - MISLAUNCH applies only for a MISLAUNCH record bound to this attempt: the same name, attempt k, outdir and receipt, and, where the record carries them, the same .launch.json sha and child_pid.
     - TWIN_PLANNED_STOP applies only to S0_SEED_CW8_TWIN, for a kill record bound to this attempt (reason ITERATION_0001_COMPLETED_AND_SIDECAR, the same outdir, the same .launch.json sha) or for any STOPPED_* monitor status (A141 L4).
     - MONITOR_REFUSED is the launch-side status of a monitor that refused and wrote nothing (D7; G27 item 5).
   - **One exact-string dict, 54 keys, no wildcards.** A STOPPED_<cap> monitor status wins over every driver-side value.
     ```
     FINISHED      FINISHED|COMPLETED  FINISHED|COMPLETED_INVALID
     FAILED        CHILD_FAILED|FAILED  CHILD_FAILED|FAILED_AT_STAGE  CHILD_FAILED|ROUTE_A_NO_FIXED_POINT
                   CHILD_FAILED|NONE|EXIT
     CAP           STOPPED_WALL_CAP|COMPLETED  STOPPED_WALL_CAP|COMPLETED_INVALID  STOPPED_WALL_CAP|FAILED
                   STOPPED_WALL_CAP|FAILED_AT_STAGE  STOPPED_WALL_CAP|ROUTE_A_NO_FIXED_POINT  STOPPED_WALL_CAP|REFUSED
                   STOPPED_WALL_CAP|BLOCKED  STOPPED_WALL_CAP|UNREADABLE_FINISH  STOPPED_WALL_CAP|RESULT_HASH_MISMATCH
                   STOPPED_WALL_CAP|NONE
                   STOPPED_RSS_CAP|COMPLETED  STOPPED_RSS_CAP|COMPLETED_INVALID  STOPPED_RSS_CAP|FAILED
                   STOPPED_RSS_CAP|FAILED_AT_STAGE  STOPPED_RSS_CAP|ROUTE_A_NO_FIXED_POINT  STOPPED_RSS_CAP|REFUSED
                   STOPPED_RSS_CAP|BLOCKED  STOPPED_RSS_CAP|UNREADABLE_FINISH  STOPPED_RSS_CAP|RESULT_HASH_MISMATCH
                   STOPPED_RSS_CAP|NONE
     OUTPUT_CAP    STOPPED_OUTPUT_CAP|COMPLETED  STOPPED_OUTPUT_CAP|COMPLETED_INVALID  STOPPED_OUTPUT_CAP|FAILED
                   STOPPED_OUTPUT_CAP|FAILED_AT_STAGE  STOPPED_OUTPUT_CAP|ROUTE_A_NO_FIXED_POINT  STOPPED_OUTPUT_CAP|REFUSED
                   STOPPED_OUTPUT_CAP|BLOCKED  STOPPED_OUTPUT_CAP|UNREADABLE_FINISH  STOPPED_OUTPUT_CAP|RESULT_HASH_MISMATCH
                   STOPPED_OUTPUT_CAP|NONE
     INFRA         CHILD_FAILED|REFUSED  CHILD_FAILED|BLOCKED  CHILD_FAILED|NONE|SIGNAL  CHILD_FAILED|UNREADABLE_FINISH
                   CHILD_FAILED|RESULT_HASH_MISMATCH  CHILD_FAILED|COMPLETED  CHILD_FAILED|COMPLETED_INVALID
                   FINISHED|NONE  FINISHED|UNREADABLE_FINISH  FINISHED|RESULT_HASH_MISMATCH  FINISHED|FAILED
                   FINISHED|FAILED_AT_STAGE  FINISHED|ROUTE_A_NO_FIXED_POINT  FINISHED|REFUSED  FINISHED|BLOCKED
                   MISLAUNCH  MONITOR_REFUSED
     PLANNED_STOP  TWIN_PLANNED_STOP
     ```
   - The dict as canonical JSON (`{string: class}`, sort_keys, separators `(',', ':')`, 2,052 bytes) has sha256 `c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54`. P-112 and c2v007 carry it and assert this sha. Root passes it as `receipt_status_classes`.
   - Any other string is unmapped: the builder refuses RECEIPT_STATUS_UNMAPPED, and root rules it. The driver's live path writes only seven statuses (L9002-9102), so this cannot arise from the pinned driver.
   - **Infrastructure deaths are read literally (D2).** Some infrastructure deaths surface as FAILED: a signalled stage gives FAILED_AT_STAGE (Ctx.run_stages L1864), a caught OSError or MemoryError (a full disk, or a lost volume, when the monitor's receipt is still written; otherwise MONITOR_ENDED_NO_RECEIPT) gives FAILED, and a failed result write gives NONE|EXIT. All three read FAILED. A lost or full run volume can also stop root_monitor writing the receipt itself (`_write_x`, L199; the receipt sits beside the outdir on that volume). That attempt has no status: it is MONITOR_ENDED_NO_RECEIPT, a residual (below). The guard is rule (c) itself: a solo rerun at the doubled wall first, and two identical counted solo failures before a member is invalid.
   - **Repeated deterministic refusals.**
     - An attempt that reads CHILD_FAILED|REFUSED or CHILD_FAILED|BLOCKED is retried in solo mode (G25 item 5), at the caps of the attempt it replaces.
     - Two consecutive attempts of the call that are both solo (solo mode, and other_ngc_processes_max = 0), with identical spec, identical caps and the identical raw status CHILD_FAILED|REFUSED, or CHILD_FAILED|BLOCKED, are terminal with disposition UNEVALUATED_INFRA_REPEAT: FREEZE_INCOMPLETE, never MEMBER_INVALID. Non-attempts (G27 item 5) do not separate the two.
     - A refusal on a first attempt therefore becomes terminal after at most two solo retries.
     - Every other INFRA string is retried with no count limit and no deadline (A133 §3).
     - The status map leaves no judgment point open. Three residuals remain, and all three go to root (disclosed reading 19). Two are D7's: a second monitor refusal at the same attempt number, and a monitor that started but wrote no .launch.json (MONITOR_STARTED_NO_LAUNCH_JSON). The third is MONITOR_ENDED_NO_RECEIPT: the monitor pid is gone and the receipt is absent (process rulings). Each is decided only with the run volume mounted (process rulings, "Run volume first"). No value is read in any of them, and the outdir is never opened. Root's ruling on MONITOR_STARTED_NO_LAUNCH_JSON or MONITOR_ENDED_NO_RECEIPT has one machine form, the RESIDUAL_RETRY line (process rulings).
   - **Cost (the draft's "one rerun" corrected).** A counted pair can start at attempt 1 only if attempt 1 was sampled solo with no other process. No S0 first attempt has a sample, and P-112 first attempts run beside other calls. So a failing call normally needs two solo reruns at the doubled wall, up to 1,220,648 s each for a serial (see Schedule risk).

**Evidence.** A133 `cd92ef91` L77-90, L103, L107-111, L201, L210-211, L216-219; RUNBOOK L94, L140, L163, L258, L402-405; driver `577f8c94` L9002-9102 (exit 0 only for COMPLETED and COMPLETED_INVALID, L9102), L1858-1864; root_monitor `ba031c23` L133 (a refusal writes nothing), L147, L177-197; kit `fdc0ee6c` L970-982 (kill record), L1096-1173 (MISLAUNCH record); twin script `f199544d` L188-191 (watch_pid); A141 L4; c2v006 L581-601, L1052-1055, L1111-1116, L1133-1136; probe (TESTED): a `STOPPED_WALL_CAP|*` key leaves `STOPPED_WALL_CAP|NONE` unmapped.

**Implements.** P-112: raw status, the bindings and the map in close-attempt; the solo retry of REFUSED and BLOCKED attempts; assemble-registry builds the set. c2v007: re-derives the raw status (G27) and adds the UNEVALUATED_INFRA_REPEAT pair as defined above. Root: passes the dict. S0 kit: no change.

**Blocks.** The S0 first launch (the map must be in V006 before the M-15 record); P-112's start; Phase-1 step 4.

### G25: rule-(c) evidence

**Question.** RUNBOOK L415: the receipt keys for the evidence roles, and four readings of A133 §3(c).

**Ruling.**
1. **Keys.** Each of the nine roles is the same-named top-level key of the attempt receipt (G27), written by machine:
   - status = `raw_status`;
   - time_utc = the monitor's utc_end;
   - spec_sha256 = the monitor's pins.spec.sha256;
   - rss_cap_bytes, wall_cap_s and output_cap_bytes = the monitor's caps;
   - theta_sha256 (G27);
   - host_ram_bytes = `sysctl -n hw.memsize`, read at launch and again at close. For S0 kit attempts it is the kit constant 137,438,953,472, checked against sysctl at close;
   - other_ngc_processes_max = the attempt's process sample (item 4). It is null when no valid sample exists, and an attempt with a null sample can never be a counted attempt.
2. **The four readings.**
   1. Confirmed: "with no other NGC process running" applies to both counted failures (A133 L217-218).
   2. Confirmed: "at RAM" means equal to host_ram_bytes. For the identity twin, "at RAM" means 11 × host_ram_bytes, its A172 N4 cap (D3). If A177 R1 ever raises a serial's cap to RAM × n, root re-rules this reading before that call's rerun.
   3. Confirmed: "doubled" means exactly 2 × the call's first attempt's wall cap, on every counted rerun.
   4. Replaced: "identical" means the identical composite raw status (G13), not the monitor status alone.

   The pair is the one c2v006 reads, unchanged (`_rule_c_problem` L660-694; `_terminal` R1, L725-731): the last two attempts of the call, non-attempts excluded (G27 item 5). An attempt of any class between two failures separates them.
3. **"Other NGC process" (D5).** A process counts if its argv names a tool on a declared list, matched by realpath or by the sha256 of the named file:
   - the driver `577f8c94` with subcommand `run` or `_stage`;
   - the NGC point certificate producers: eps_ngc_point_c4v002 `8972822b`, gq_binding_c4v002 `f4ee064d`;
   - the NGC ρ c3v003 producer `d3d0f3dd`, stage `496d2a21` and slot proof `ada31d12`;
   - the NGC acceptance stack of record (A211): LO state adapter c2v003a `9c4b6dfc`, handoff c2v005 `7077ad93`, roster recipes c2v002 `c700f469`;
   - handoff c2v003a `7c54fd6f`, kept on the list as the stricter reading of D5;
   - values writer v004, cx2v002 `26319ecb` (A212);
   - the carrier extractors: cx3v005 `50c7db5f`, c2v001 `8acd21c7`.

   A211 names the stack's adapter as the LO state adapter c2v003a, which settles the ambiguity in A205 item 6. Not counted: root_monitor, the dry harness and the driver's `dry-run` subcommand (driver L4981), the sampler, the kill watch, and the attempt's own process tree. The list is a P-112 constant, and only a V006 entry can change it.
4. **Sampler coverage.** The sampler takes its first sample at least 1 s before P-112 starts the monitor, and a final sample at least 1 s after the monitor receipt exists. It polls at most every 10 s and records n_samples, poll_s and the largest gap. If the monitor pid is gone and no receipt has appeared 60 s later, it stops and writes nothing at the outdir path (MONITOR_ENDED_NO_RECEIPT). The 60 s are counted only while the run volume is mounted; while it is unmounted, the sampler keeps polling and decides nothing (process rulings, "Run volume first"). Sample times carry sub-second precision. The monitor's utc_start and utc_end are whole seconds (root_monitor L43-44), so the comparison is in whole seconds: floor() of a sample time against the receipt's value. other_ngc_processes_max is null in each of these five cases:
   1. the sampler died, or its sample file is absent;
   2. the sample's `complete` is false. `complete` is true if and only if every poll's `ps` call exited 0 and parsed, and the sampler ended by the normal-end rule (monitor gone, receipt exists, final sample at least 1 s after it);
   3. the largest gap exceeds 2 × poll_s;
   4. floor(first sample time) is not earlier than the monitor receipt's utc_start (null unless floor(first) < utc_start);
   5. floor(last sample time) is not later than the monitor receipt's utc_end (null unless floor(last) > utc_end).

   With the 1 s lead and the 1 s tail, cases 4 and 5 cannot fire on an honest attempt. Without them, a first sample in the same second as the start, but before it, would read "after", and the attempt would never count (a false null, costing a rerun of about 14 days). P-112 and c2v007 compare in exactly this way. Tests: a same-second first sample gives null (MUST_FAIL); with the 1 s lead, the attempt is counted (MUST_PASS).

   A ps poll can miss a short process, so the count is a lower bound; the guarantee is the hold rule (item 5).
5. **Hold rule.** A counted rerun, or a solo retry (G13), starts only when no listed process is alive. While it runs:
   - P-112 starts nothing;
   - root starts no S0 kit call, twin or other listed process;
   - root starts no NGC tool that is not on the list, whenever it was adopted (the list reflects adoptions through A212). Such a tool joins the list only by a V006 entry.
6. **Caps** (a process choice, A141 L1).
   - A rule-(c) rerun has identical spec bytes, RSS at RAM (twin: RAM × 11) and wall = 2 × the first attempt's: 1,220,648 s for a serial, 45,504 s for the twin.
   - An OUTPUT_CAP rerun also has output = 2 × the first attempt's. The identity twin never has one: any STOPPED_* twin status is TWIN_PLANNED_STOP, which is terminal.
   - An INFRA or MISLAUNCH retry repeats the caps and the solo mode of the attempt it replaces. A REFUSED or BLOCKED retry repeats the caps and always runs solo (G13).
7. **Outside-set S0 serials (D4).** Root stops each one as soon as the set is fixed at u_A. The stop runs the kill-target checks and writes a stop record by exclusive create. Outputs are kept and never read (A133 L103). After that, no outside-set serial can hold up a solo rerun.
8. **Ownership (D3, D6).**
   - P-112 owns the rule-(c) and INFRA reruns of every Phase-1 NGC call, the S0 serials and the identity twin included (a twin mode at the twin's caps). This supersedes A161 N3's on-demand kit successor.
   - **The kit's own relaunches stay with the kit.** For an S0 call, the kit relaunches after its own MISLAUNCH (order-check L737-791; MISLAUNCH record L1160), and the D7 relaunch at the same k after a monitor refusal also goes through the kit. The kit keeps both until the call has a LAUNCH record, a P-112 attempt or a RESIDUAL_RETRY line (process rulings).
   - Once P-112 launches any attempt of a call, every later attempt of that call is P-112's. Its attempt numbers continue after the kit's.
   - P-112 never writes into the kit's launches directory. It reads the kit's records there.

**Evidence.** root_monitor `ba031c23` L43-44 (whole-second utc), L140-149 (utc_start taken at L146, before Popen), L192-198; c2v006 L591-601, L643-694 (L677-680 always check attempt 0); kit `fdc0ee6c` L613-645 (register), L737-791 (order-check). Probes (TESTED):
- an S0 first attempt with no sample refuses RULE_C_EVIDENCE_MISSING;
- a call with a non-solo first attempt and two solo reruns at 2× wall reaches the terminal pair [1, 2];
- a twin pair at RAM × 11 refuses RULE_C_RERUN_CAPS under c2v006.

Also A133 L217-219, L222; A141 L1; A161 N3; A166; A172 N4; A177 R1; A211; A212; kit `fdc0ee6c` L83, L110-112.

**Implements.**
- P-112: the sampler, solo mode, the rerun path with twin mode, host RAM, the nine keys, and a stop-outside-set command for root.
- c2v007:
  - full evidence only on the counted pair. On attempt 0 it requires spec_sha256 and wall_cap_s (and output_cap_bytes for OUTPUT_CAP) unless attempt 0 is counted;
  - it checks rss_cap_bytes == 11 × host_ram_bytes for S0_SEED_CW8_TWIN only;
  - it recomputes other_ngc_processes_max from the pinned sample under item 4's five cases, with the whole-second comparison.
- Root: the hold rule, including the rule for NGC tools not on the list, and the outside-set stops.

**Blocks.** P-112's start. Until this is implemented, no call can be marked invalid or unevaluated, and a failed call stays non-terminal (RUNBOOK L415). Phase-1 step 4, if any call fails.

### G27: the launch registry and the receipt binding

**Question.** RUNBOOK L417: the registry's producer and schema; the θ value receipts carry; binding keys on every receipt.

**Ruling.**
1. **The registry.** STEP5_LAUNCH_REGISTRY_C2V003, exactly as c2v006 checks it (L136, L604-636). It is fed from per-call entries, each written by exclusive create at its call's first launch: the kit's UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A, or P-112's own entry. At step 4, P-112 `assemble-registry` writes the STEP5 file and an assembly record that pins every source.
   - An S0 entry whose θ key is a PLAN member's becomes that MEMBER entry, matched by (log_index, role, order) (IC-P1-MEMBERS, A171 L1592). Before it maps one, assemble-registry checks three things and refuses on any mismatch (one-ulp MUST_FAIL tests):
     - O.theta_key(PLAN theta_engine) equals the kit's theta_key;
     - the kit spec's θ bits equal the PLAN theta_engine's float.hex;
     - the spec's NGC geometry equals the theta_ngc nuisance values.
   - The other S0 entries in the set become OTHER entries (F0-F2, S0_SEED_CW8_TWIN). Outside-set serials are left out and listed.
   - A verify mode rebuilds the STEP5 bytes from the pinned sources and byte-compares them. Root runs it before the FULL build.
2. **θ: two functions, both carried.**
   - The program θ key (orchestrator theta_key, L523-529) hashes a schema-wrapped engine θ.
   - The builder's theta_sha256 hashes v003g's canonical bytes of theta_ngc, which adds the NGC nuisances.
   - A MEMBER's theta_sha256 is hashed from the saved PLAN `evaluate_envelopes(budget=0)` PRIMARY output (spec of record `e2a7650e`) and is never recomputed.
   - An OTHER entry's theta_sha256 is its point key (RUNBOOK L82).
   - A member handoff carries no θ and no key (phase1 v003b L686-689). The θ comes through its source_export_pin at its log_index; the key comes through fdplan.
3. **The attempt receipt.** STEP5_ATTEMPT_RECEIPT_C2V001, at exactly `<outdir>.attempt_receipt.json`, by exclusive create, written by P-112 `close-attempt` (S0 kit attempts included).
   - It carries theta_sha256, spec_sha256 and point_key for every class.
   - It pins the monitor receipt, the .launch.json, the LAUNCH or MISLAUNCH record, the registry entry, the solo sample and any kill record. Its spec_sha256 must equal both the monitor's and the registry's.
   - close-attempt writes nothing until:
     - the run volume is mounted (otherwise it refuses RUN_VOLUME_NOT_MOUNTED; process rulings, "Run volume first");
     - the monitor receipt exists (if the monitor pid is gone without one, it refuses MONITOR_ENDED_NO_RECEIPT);
     - exactly one LAUNCH or MISLAUNCH record of this attempt exists;
     - for the twin, the kill-watch pid in the LAUNCH record has exited;
     - for an S0 attempt, the PLAN and fdplan mapping exists.
4. **c2v007 trusts nothing the receipt asserts.** It:
   - accepts the receipt only at realpath(run_dir) + `.attempt_receipt.json`;
   - verifies the pinned monitor receipt's self-hash (the verify_receipt logic);
   - re-derives raw_status from the monitor's status, driver_status and exit_code, plus the pinned, bound MISLAUNCH and kill records;
   - requires the receipt's caps, spec and time_utc to equal the monitor receipt's;
   - recomputes other_ngc_processes_max from the pinned sample under G25 item 4's five cases, taking the monitor's start and end from the monitor receipt's utc_start and utc_end and comparing in whole seconds (G25 item 4), and requires the receipt's value to equal it.

   Results and cut records stay inside run_dir. The run tree is never written after the run, except the G16 restore.
5. **Non-attempts.** Some attempts are not attempts of the call:
   - one with no run directory at close: MONITOR_REFUSED (D7), or a LAUNCH or MISLAUNCH whose outdir does not exist (the driver ended before its mkdir, driver L8994). A Refusal or OSError in cmd_run before that mkdir (L9208-9215) is not caught by main (L4971-4987), so the driver exits 1 with no outdir and no finish (CHILD_FAILED|NONE|EXIT); a signal there gives CHILD_FAILED|NONE|SIGNAL. The launch check reads only `.launch.json`, so such an attempt can carry a LAUNCH record;
   - a LAUNCH or MISLAUNCH with a spec other than the registered one;
   - an attempt named in a RESIDUAL_RETRY line while it has no monitor receipt (root's ruling on a residual; process rulings). It uses its number. A line never makes an attempt with a monitor receipt a non-attempt: assemble-registry and c2v007 refuse RESIDUAL_RETRY_NOT_RESIDUAL for such an attempt, and root rules.

   Each is recorded in V006 and in the assembly record and left out of the call record. A non-attempt does not separate an INFRA_REPEAT pair or a rule-(c) pair.
   - **After a non-attempt LAUNCH or MISLAUNCH** (the last record of the call is one): retry with its caps and solo mode (first-attempt caps if no attempt precedes it); no new registry entry. The record used its attempt number, so the retry takes the next k. It is a retry, not a first attempt, even at k = 1. The same holds after an attempt named in an honoured RESIDUAL_RETRY line (process rulings).
   - Non-attempts carry no count limit, as INFRA retries carry none (A133 §3). P-112 `status` reports each call's run of consecutive non-attempts, and root, who runs every launch, sees each one.

**Evidence.** c2v006 L136, L276-277, L604-636, L706-707, L716-717, L738-745, L1056; orchestrator `c75a889f` L523-529; v003g `48a1e48a` L1019-1025, L2162-2163, L2313-2335; phase1 `7d891ff7` L686-691, L776-822; kit `fdc0ee6c` L613-650 (the entry carries theta_key and spec only); root_monitor `ba031c23` L192 (utc_start, utc_end); step5_path README L48; A136 L584; A169 L1538; A171 L1590-1592. Probes (TESTED): c2v006 _launch_registry accepts an assembled STEP5 file; a receipt beside run_dir refuses RECEIPT_NOT_IN_RUN_DIR.

**Implements.** P-112: the entries, close-attempt, assemble-registry with its verify mode, and an interface proof against c2v006's bytes. c2v007: the receipt residence, the re-derivation and the sample recomputation. S0 kit: no change.

**Blocks.** P-112's start; every MEMBERS or FULL build (RUNBOOK L417); Phase-1 step 4.

### G15: the M-15 record and its V006 copy

**Question.** RUNBOOK L139, L407: the pre-launch record's path and format, and the V006 byte copy.

**Ruling.**
- The record of record is the kit's UNT_M15_PRELAUNCH_RECORD_C2V001 at `<S0 launch root>/M15_PRELAUNCH_RECORD_C2V001.json`. It is written by exclusive create as the seed serial's first action (A142 item 6; A161; A179). The RUNBOOK's proposed M15_PRE_LAUNCH_RECORD_C2V001 is withdrawn.
- c2v007 reads it by its exact keys:
  - v006_sha256 = `v006.sha256`;
  - the gate list = `gate_documents_pinned_in_v006[].sha256_from_bytes`;
  - date_u as written, which must parse to `date_u_epoch_s`.
- The m15 launch receipts are the .launch.json of every attempt of the seed serial and the twin, MISLAUNCH attempts, non-attempt LAUNCH or MISLAUNCH records, and attempts named in a RESIDUAL_RETRY line included (an attempt with no .launch.json adds none). Each is timed by its `utc` key, not by the call receipts' time_utc. c2v006 uses the earliest of them (L1380-1391).
- Root runs `cp -n` of V006 to `<S0 launch root>/M15_V006_COPY_<sha256>.md` before its first V006 write after the record, a mis-launch entry included. Root checks the copy's sha and byte count against v006.sha256 and v006.bytes, and logs the copy's sha in the entry that records the S0 launch.

**Evidence.** Record writer `a10965b7` L194-212; kit `fdc0ee6c` L418, L796-812; no copy step in `621263a2`, `f199544d` or `a10965b7`; c2v006 L126, L339-347, L1364-1391. Probes (TESTED): the kit record refuses INPUT_KEY_MISSING under c2v006; c2v006's parse_utc_ns parses the `date -u` form. A161 N2.

**Implements.** Root: the copy step. c2v007: the kit form. S0 kit: no change.

**Blocks.** The S0 launch procedure; the Phase-1 FULL build's m15 input. Without that input, every gate reads LATE (RUNBOOK L167).

### G7: the TSR support record

**Question.** RUNBOOK L398: whether UNT_ROOT_TSR_SUPPORT_CX3V001 exists, who writes it, and its point_key.

**Ruling.** It exists. Root writes it by machine projection (c2v007 `tsr-support`), and `tsr-check` verifies it.
- **Keys.** Exactly classifier A's nine:
  - schema UNT_ROOT_TSR_SUPPORT_CX3V001;
  - mode SAVED_TARGET_FREE;
  - target_free true and before_target_access true;
  - slots_pin, ntest_compare_pin, rings and point_key (below);
  - rule_id M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001.
- **rings.** One entry, with exactly the keys {native_ring, lower_kpc, upper_kpc, lower_inclusive: false, upper_inclusive: false}. native_ring is the compare's ordinal-15 TRUNCATION_SHAPE ring, copied verbatim. The bounds are 9.901810628740723 and 10.911721936765339 (V001 content_when_written).
- **slots_pin.** Copied byte-canonically from the adopted carrier extractor's policy `slots` pin, with the same path spelling. Both candidate policies pin `freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` `d3859b42`; its content was not opened or shown; its bytes may have been hashed once (fixer-round disclosure):
  - POLICY_CX3V001 `311ceedd` (extractor cx3v005);
  - POLICY_CARRIERS_C2V001 `aa50c752` (extractor c2v001, step5_path).

  POLICY_C2V001 `0c781a17` pins the same slots.
  - **Open:** the extractor choice under A135 item 11. Root rules it before the record is due.
  - If the M-14 slots successor is pinned for Phase 2, slots_pin is ruled again then.
- **ntest_compare_pin.** The exact pin dict root passes as the compare in input_files (`6f095f64`), with the same spelling.
- **point_key.** Take D1's member id from the pass record of the ledger head the freeze uses. point_key is the fdplan members[].key of the member whose (log_index, role, order) matches that id.
- **Timing.** The record is written after step 7 reads NO_NEW_DISCREPANCY and before step 8, and it is input_files item 8. tsr-check asserts the slots and compare equalities.

**Evidence.** Classifier A `e92aa30e` L644-725 (L705-723); extractor `50c7db5f` L158-163, L213-221; the three policies' `slots` pins, read from their bytes (the slots file: its content was not opened or shown; its bytes may have been hashed once, fixer-round disclosure); ROOT_TSR_FLAG_RECORD_V001 `61bd8a83` pins.support_record; c2v006 L200-211; RUNBOOK L46, L116, L129, L286, L384; A177 L1846.

**Implements.** c2v007 (root build, reviewed by Codex1). Not S0, not P-112.

**Blocks.** The freeze's input_files item 8 and classifier A's bundle. Without the record, classifier A fires TSR_FLAG_TABLE_MISMATCH. The A135 item 11 extractor ruling comes first.

### G16: after a stop

**Question.** RUNBOOK L195, L358, L408: the remedy after a pre-target stop or after PASS_RESULT_CUSTODY_BREACH.

**Ruling.**
1. **Root's own preflight** (8a tsr-check and check-gate-list; 9-pre seal-check). Root records the stop code in V006. The only permitted remedies are:
   - re-run with corrected inputs, when what root passed was wrong;
   - re-produce a root-written target-free record with its registered producer, from unchanged pinned inputs;
   - restore a pinned object from a byte copy whose sha256 equals the pin.

   No roster, cut, member, reference, gate set, compare, N1 or node record, sealed object or registered text changes. If no remedy clears the stop, score_after_freeze is not called, and the phase is reported with the stop code, disclosed.
2. **The sealed classifier's synthetic pre-score run.** A stop there is r3a's CLASSIFICATION_INPUT_DEFECT and ends that phase's classification. Root adds no remedy.
3. **Custody (D10).** Root takes the `cp -n` custody copies of each terminal attempt's result, monitor receipt and attempt receipt when that attempt receipt is closed (sha-checked against the monitor's result pin), and of the cut records at step 3; in every case before pass one. Step 5 pins them. The custody directory is outside every run tree. (In the Phase-1 order 3 → 4 → 2, then 5 (RUNBOOK L159), pass one reads the registered results before step 5, so copies taken at step 5 would come too late for 3(a).)
   - 3(a) and 3(b) apply only with the run volume mounted (the P-112 §6.10 mount check). A missing volume is a stop, never a breach, and nothing is written under an unmounted path.
   - (a) On PASS_RESULT_CUSTODY_BREACH, root restores the file at its registered path from that copy, re-runs the pass and records the event. This restore is the single permitted write into a run tree, and it is recorded in V006.
   - (b) A call that meets both conditions reads UNEVALUATED_CUSTODY_BREACH (FREEZE_INCOMPLETE): (i) its registered result sha fails to verify from bytes, with the run volume mounted; (ii) no custody copy with that sha exists. It is never rebuilt, rerun or substituted. This is a pre-result registration under A133 §3 (L201), so no judgment point remains. The successor plan that records it is constrained:
     - it is machine-derived by c2v007, never written by root (A133 L215);
     - it is c2v006 `_apply_unevaluated` (L1809-1830) applied to exactly the calls that meet both conditions, with UNEVALUATED_CUSTODY_BREACH in place of UNEVALUATED_STEP7_DISCREPANCY (own_disposition and replay_index); nothing else changes. The function's other effects are therefore part of the successor: it lowers member_budget and re-runs `_effective`, so every later member reads UNEVALUATED_BY_ORDER_TRUNCATION (forced by v003g, RUNBOOK L112); in Phase 2 it resets the sensitivity block; it sets predecessor_sha256;
     - c2v007 ledgers it as a CUSTODY entry kind in the same hash chain (c2v006 L2042 and L2047 would read it BROKEN). The reader re-checks both conditions and re-derives it byte for byte (RUNBOOK §7a L217; K10, K11, K17). Anything else reads STEP7_LEDGER_BROKEN. With the run volume unmounted the reader stops; it never reads BROKEN or a breach for that reason.
     - MUST_FAIL: a successor that marks a call whose result still verifies reads STEP7_LEDGER_BROKEN.
     - MUST_FAIL: a custody successor that leaves member_budget unchanged where `_apply_unevaluated` lowers it reads STEP7_LEDGER_BROKEN.
     - Scope: `_apply_unevaluated` marks replay entries through their MEMBER keys only (L1818). Every Phase-1 replay entry is a member's (OTHER calls carry no alternative, L1225-1240), so the Phase-1 derivation is complete. A Phase-2 SENSITIVITY-only replay entry is not marked by it; that form is open (Open items), due before Phase-2 pass one.

**Evidence.** r3a `c64f65a3` L184-201, L691; RUNBOOK L112, L159, L195-197, L212-217, L339-358; c2v006 L1225-1240 (replay_index), L1601-1604 (the replay records RESULT_CUSTODY_BREACH), L1766-1768 (PASS_RESULT_CUSTODY_BREACH), L1809-1830 (`_apply_unevaluated`), L1995-2047 (STEP7_LEDGER_BROKEN; L2038-2047, the successor must be step 7's own change and needs NEW_UNEVALUATED); A133 L215; K10, K11, K17.

**Implements.** Root: the copies at receipt close and at step 3, the step-5 pins, the mount check before 3(a) or 3(b), and the restore. c2v007: the text, the 3(b) successor derivation, the CUSTODY ledger entry kind and the reader's re-check, TESTED on synthetic records with both MUST_FAIL cases above.

**Blocks.** Nothing now. The copies are needed from the first closed terminal attempt receipt and at step 3, before the first pass on real results; 3(a) and 3(b) before the first 8a or 9-pre check.

### G24: the Phase-1 gate cutoff

**Question.** RUNBOOK L414: the Phase-1 gate cutoff, proposed as the V006 at the step-4 start.

**Ruling (D11).**
- **T** is the latest time_utc over the terminal attempt receipts of the call set. Receipts are not closed in the order their attempts ended (S0 receipts wait for the PLAN mapping), so T is not the time_utc of the receipt that completes the set.
- **Copies before writes.** From the M-15 record until c2v007 accepts the cutoff record, root takes `cp -n` of V006, named by its sha (`V006_COPY_<sha256>.md` in the root copy directory), before every V006 write. The V006 at T is the copy taken before the first V006 write after T, or the machine cutoff copy when no write fell between T and it.
- **The cutoff copy is taken by machine.** P-112 close-attempt takes it when it writes the receipt that completes the call set by its advisory pre-check; otherwise root takes it at its first sight of that receipt. It is pinned as gate_cutoff, kind PHASE1_STEP4_START. P-112 writes the cutoff record once.
- **c2v007 decides T.** P-112's pre-check is advisory; the builder decides terminality. c2v007 re-derives the terminal set and T from the pinned receipts and uses its own T. It accepts the cutoff copy only if the cutoff record's date_u is at or after that T; otherwise it refuses GATE_CUTOFF_BEFORE_T. Root then writes a successor cutoff record, with c2v007's T, the receipt pins and the V006 at that T (by the copy rule above), and records it in V006. It pins the record it supersedes, and it is the only second record allowed.
- **Entries after T.** The cutoff entry lists every V006 entry stamped after T (c2v007's T). A gate whose full sha first occurs in such an entry is not a Phase-1 gate document. A gate first pinned after M-15 reads LATE on either side of the cutoff (r3a L455).

**Evidence.** RUNBOOK L163-167, L183, L263; c2v006 L113, L967-993, L1347-1409, L1452-1476; A157 L1245; r3a L455-463 (a LATE gate only adds unsigned misses).

**Implements.** Root: the copies, and the single successor cutoff record on GATE_CUTOFF_BEFORE_T. P-112 close-attempt: the machine copy and its T, once. c2v007: re-derives the terminal set and T, refuses GATE_CUTOFF_BEFORE_T, and excludes the after-T gates (with the RUNBOOK text).

**Blocks.** The Phase-1 FULL build.

### Claude3 0237 N1 (+N2)

**Question.** Should AT-0b's --values and --values-sha256 come from the values_sha256 logged in L1?

**Ruling.** Yes.
- AT-0b's `--values` is the values file whose sha256 equals `L1.values_sha256`, checked from bytes before the call, never a re-serialized copy.
- `--values-sha256` is that value.
- Every sha passed to phase1 is lower case.

**Evidence.** 0237 L34-35; README_PHASE1_C2V003B L31-35; A149 L976.

**Implements.** RUNBOOK c2v007 text. v003b already enforces it.

**Blocks.** AT-0b and AT-1 (Phase 2).

### Claude3 0237 N3

**Question.** How is a phase1 successor handled after the freeze?

**Ruling.** phase1 v003b `7d891ff7` is the tool of record in both phases (A210, the P-117 record), and no successor is commissioned. If a defect ever forces a successor after the freeze, option (b) applies:
- the logged v003b L1 stays the L1 of record and is never replaced;
- the successor's band writes a new L1 by exclusive create, logged beside the original with a byte diff showing that only `module` differs;
- the successor is POST-PREDICTION (r3a L51-55).

Option (a) is not adopted.

**Evidence.** 0237 L31-33; A171 L1590-1593; A210; r3a L51-55, L209.

**Implements.** Done (A210).

**Blocks.** Nothing now.

### Claude4 0248 VN1

**Question.** Phase 2 has no producer for A16.4. Every honest Phase-2 freeze would refuse until one exists.

**Ruling (D12).** This implements registered A16.4 (r3a L379).
- **Which entries.** The A16.4 entries are the v003g kind SENS_NGC entries whose theta_ngc geometry differs from the registered geometry as the spec of record states it, compared from bytes, not with literals.
- **The answer.** For each one, the replay adapter returns, in memory, valid=false, a reason carrying GEOMETRY_NOT_EXPOSED, and no valid row (v003g L3016-3025). A non-registered geometry on any other entry kind raises.
- **Never launched or registered.** c2v007:
  - keeps `kind` in the value-free plan;
  - exempts these entries from CALL_RECORD_MISSING, from the roster contexts and from the replay index;
  - gives them own_disposition GEOMETRY_NOT_EXPOSED_IN_MEMORY. The sens-budget rule counts them as evaluated, and they never trigger V-N1.
- **Recorded.** PASS_RECORD lists each in-memory answer. RUNBOOK step 6's "never invents" names this as its one registered exception.

**Evidence.** 0248 L41-43; v003g L2321, L2557-2559, L2995-3029; c2v006 L481, L513, L1133-1136, L1145, L1253; the driver `577f8c94` has no GEOMETRY_NOT_EXPOSED path.

**Implements.** c2v007, with TESTED MUST_PASS and MUST_FAIL cases.

**Blocks.** Phase-2 pass one and every honest Phase-2 freeze. Not Phase 1.

### Claude4 0248 DN5

**Question.** V-N1 counts members only. Do capped or unevaluated Phase-2 sensitivity entries count?

**Ruling (D12).** They count. This is a disclosed pre-result registration under A133 §3 (L201: "new registrations, made before any result and disclosed"), and it settles the DN5 item that A178 left open.
- **What it replaces.** It replaces the scope of the C2V004 V-N1 rule (`write_freeze_manifest_inputs[allow_incomplete].value.phase2.true_if_and_only_if`; README_RI45_14_C2V004 L37). The list's bytes are unchanged.
- **The rule.** Phase-2 allow_incomplete is True if and only if a member or a sensitivity entry of an evaluated alternative has one of these own_dispositions in the last pass's replay plan; otherwise it is False:
  - UNEVALUATED_CAP;
  - UNEVALUATED_STEP7_DISCREPANCY;
  - UNEVALUATED_INFRA_REPEAT (G13; itself a pre-result registration under A133 §3);
  - UNEVALUATED_CUSTODY_BREACH (G16; itself a pre-result registration under A133 §3).

  GEOMETRY_NOT_EXPOSED_IN_MEMORY never triggers it.
- **Who reads it.** c2v007 exposes the value in the replay plan, and G26 takes it from this entry, not from the pinned list. G3 is closed (DN1).
- **Timing.** This entry comes before any step-5 output, so it meets r3a L149 and M-8.

**Evidence.** 0248 L44-46; A163 L1415; A178; A133 L172-173, L201, L206; r3a L149; RUNBOOK L293 (v003g L3675-3678).

**Implements.** c2v007 and G26.

**Blocks.** The Phase-2 freeze.

### Open items

- **G28 (NEEDS_INFO, not ruled).** The step-7 ledger root is due before the first FULL build (Phase-1 step 4), not before S0 (A201 L2578). Root then fixes an absolute directory outside every build directory. A later change is a V006 event.
- **G7's extractor.** The A135 item 11 extractor ruling is due before the TSR support record.
- **The three residuals.** A second monitor refusal at the same attempt number and MONITOR_STARTED_NO_LAUNCH_JSON (both D7's), and MONITOR_ENDED_NO_RECEIPT, go to root (disclosed reading 19). Each is decided only with the run volume mounted. MONITOR_STARTED_NO_LAUNCH_JSON and MONITOR_ENDED_NO_RECEIPT each hold their call non-terminal, and so hold step 4, until root rules in V006: P-112 refuses every launch of the call until then. Root's ruling on either takes the RESIDUAL_RETRY form (process rulings), except in the S0_SEED_SERIAL limit disclosed there; a ruling in any other form needs a P-112 successor. After a second monitor refusal at one k (MONITOR_REFUSED_TWICE), P-112 cannot see the unrecorded refusal and does not hold the call; holding it, and so holding step 4, is root's procedure until root rules it in V006 (process rulings, D7).
- **G16 3(b) in Phase 2.** The custody successor's form for a SENSITIVITY-only replay entry, which `_apply_unevaluated` does not mark (c2v006 L1818). Root rules it before Phase-2 pass one. Phase 1 is complete without it.

### Launch condition, process rulings and reviewers

- **P-112 launch (D8).** P-112 is a Codex2 build. Claude4 reviews it after Fri 23-Oct 19:00Z (A205 items 8 and 11(2); A208).
  - Root writes P-112's adoption entry only after that review returns 0 blocking. The entry carries one line, `TOOL_PIN P112_LAUNCHER_CX2V001 <sha256 of the tool's bytes> <the tool's realpath>`, in the kit's pin-line form. The kit's parser ignores `TOOL_PIN`, which is not one of its KINDS (`a10965b7` L41-43); nor is `RESIDUAL_RETRY` one.
  - The gate covers every subcommand that writes a record: launch, close-attempt, assemble-registry, stop-outside-set and record-monitor-refused. Each refuses unless V006 holds exactly one whole-line TOOL_PIN (PIN_RE form) named P112_LAUNCHER_CX2V001, carrying the tool's own sha and realpath. A TOOL_PIN line is a whole V006 line, under an entry heading, matching `^TOOL_PIN ([A-Z0-9][A-Z0-9_]*) ([0-9a-f]{64}) (/.*\S)$` (the kit's PIN_RE form, `a10965b7` L43). Text that mentions TOOL_PIN inside a line, as this entry does, is not a pin line. A line that begins `TOOL_PIN P112_LAUNCHER_CX2V001` and does not match refuses TOOL_PIN_MISMATCH. Dry mode and the read-only `status` are exempt.
  - The version is part of the pin name. A fixed P-112 is pinned under its own name (for example P112_LAUNCHER_CX2V002), so no V006 line ever needs removing.
  - No launch is made on root verification alone. P-112 is needed at u_A, about Tue 27 to Wed 28 Oct. If the review is late, root records the slip.
- **Spec fills.** P-112 never runs or imports the filler, because the filler opens the slots pin (fill_step5_c2v001 L264, L292). Root fills each P-112 call's spec directory under its blinding guard, as for S0. P-112 only checks the fill.
- **NGC ρ point registrations (A211 consequence 2, N3).** Point custody admits exactly the four registered S0 keys. Every Phase-1 member or F point outside S0 needs a root NGC ρ point registration before its acceptance. Root writes each one when u_A fixes the actual set. P-112 does not register.
- **Disk (D9).** P-112's launch check refuses unless the run volume has the attempt's output cap + 20 GiB free. An OUTPUT_CAP serial rerun therefore needs 292 GiB. Root names the run volume in the P-112 config.
- **Run volume first.** MONITOR_ENDED_NO_RECEIPT, MONITOR_STARTED_NO_LAUNCH_JSON, the D7 `absent` checks and the RESIDUAL_RETRY residual check (below) are decided only after the P-112 §6.10 mount check passes (the run volume is mounted, not symlinked). With the run volume unmounted, `status` reports RUN_VOLUME_NOT_MOUNTED, and close-attempt, record-monitor-refused, assemble-registry and launch refuse RUN_VOLUME_NOT_MOUNTED (a stop, as in G16 3) and write nothing. The sampler's 60 s wait for a receipt (G25 item 4) is counted only while the volume is mounted. On root's side, root writes a kit MONITOR_REFUSED record, and a RESIDUAL_RETRY line, only on existence checks made with the run volume mounted. A receipt on an unmounted volume is not absent: after a host restart, a finished attempt whose receipt sits on the unmounted volume is never reported, refused or ruled as a residual.
- **Monitor refusal (D7).** A monitor that refuses writes no .launch.json.
  - The refusal is recorded in MONITOR_REFUSED_ATTEMPT_RECORD_C2V001, by exclusive create. It maps to INFRA, and it is not an attempt of the call.
  - **Path.** For a P-112 call, P-112 `record-monitor-refused` writes `<p112_launch_root>/launches/P112_<NAME>_MONITOR_REFUSED_CX2V001_A<k>.json`. For a kit call, root writes `<S0 launch root>/monitor_refused/<NAME>_MONITOR_REFUSED_C2V003A_A<k>.json`, outside the kit's `launches/`. Root writes kit records itself, because S0 launches come before P-112 is adopted.
  - **Exact key set:**
    - schema;
    - name and attempt (k);
    - launcher: `KIT_C2V003A` or `P112_CX2V001`;
    - writer {name, sha256}: `ROOT` with null, or `P112_LAUNCHER_CX2V001` with the tool's sha;
    - plan {path, sha256}. For a kit call this is `<work>/plan.json`;
    - monitor_stdout and monitor_stderr {path, sha256}. For a kit call these are `<work>/monitor.stdout.txt` and `<work>/monitor.stderr.txt` (serial script L126, L195; twin script L81, L147);
    - absent {outdir, receipt, launch_json, receipt_stdout, receipt_stderr}: the planned paths (`<outdir>`, `<outdir>.receipt.json`, `<outdir>.receipt.json.launch.json`, `<outdir>.receipt.json.stdout.txt`, `<outdir>.receipt.json.stderr.txt`), each absent when the record is written;
    - date_u, from `date -u`;
    - rule.
  - **A monitor that started is not a refusal.** root_monitor creates `<receipt>.stdout.txt` and `.stderr.txt` by exclusive open (L143-144) after its refusal checks (L133) and before Popen and `.launch.json`. A monitor that dies there leaves both files, and a relaunch at the same k fails on that open every time. If either file exists, the event is not a D7 refusal: `record-monitor-refused` refuses MONITOR_STARTED_NO_LAUNCH_JSON, and root rules (a driver may have started).
  - **A kit record waits for the monitor to exit.** The kit's scripts exit 5 after about 120 s without `.launch.json` even while the monitor is still alive (serial script L202-208; twin script L150-155). Root writes a kit record only after that monitor pid has exited. If the kit script exited 5 at its 120 s wait (serial L206-208; twin L155) with the monitor alive, root stops that monitor pid the same way before writing anything: it confirms that the pid's command line names root_monitor and this receipt, sends TERM, KILL after 15 s, and waits for it to exit. If `.launch.json` then exists, root stops its child with kill-target and records a kit MISLAUNCH with the kit's `launch-record --outcome MISLAUNCH`; otherwise the D7 record rules apply. kill-target runs without `--mon-pid` here: the monitor is gone, so the child's parent has changed and kill-target's parent check (kit L958-959) would refuse; it still checks the group leader, the exact command and the spec (L932-957). Such a MISLAUNCH has no monitor receipt, so the attempt is MONITOR_ENDED_NO_RECEIPT (below).
  - The work directory's `monitor.stdout.txt` and `monitor.stderr.txt` are hashed only when no `.launch.json` exists. A run's `<outdir>.receipt.json.stdout.txt` and `.stderr.txt` are never opened.
  - P-112 accepts a root-written record. It checks the exact key set, the schema, the name and k, every pin from bytes, and, while no relaunch at the same k has started (no LAUNCH or MISLAUNCH record of (NAME, k), and neither `<outdir>.receipt.json.stdout.txt` nor `.stderr.txt` of k exists), that every `absent` path is still absent. Once the same-k relaunch has started, those paths belong to the relaunch and are not re-checked; the writer's check at date_u stands.
  - Root may relaunch once, at the same attempt number, and records the refusal in V006. A kit call is relaunched through the kit (order-check admits k, and register returns ALREADY_REGISTERED_SAME_SPEC, kit L635-644). A P-112 call is relaunched through P-112, which admits its existing same-spec registry entry in the same way.
  - If the refused attempt is the seed serial's first, the V006 record waits until the relaunch's launch record (A161 N2), and the G15 copy is taken first.
- **A monitor that ends without a receipt (MONITOR_ENDED_NO_RECEIPT; a residual).** A LAUNCH or MISLAUNCH record of the attempt exists, the monitor pid is gone, and `<outdir>.receipt.json` is absent.
  - Causes: the host restarts or panics during a run of several days; the monitor is killed, a stop at the launch bound with `.launch.json` present included (the D7 kit bullet above; brief §11.5); root_monitor's receipt write (`_write_x`, L199) fails because the run volume is lost or full (the receipt sits beside the outdir on that volume).
  - "Gone" means that no live process has the record's `monitor_pid` (kit L1132; P-112 carries the same key) with a command line naming root_monitor and this attempt's receipt path. A pid reused after a restart is therefore not the monitor.
  - The attempt has no monitor receipt, so it has no status and no attempt receipt. The call cannot reach a terminal attempt receipt, and step 4 cannot begin (A133 L210). It goes to root. No value is read, and neither the outdir nor the receipt's stdout and stderr files are opened.
  - P-112, with the run volume mounted ("Run volume first", above): the sampler stops when the monitor pid is gone and no receipt has appeared 60 s later, and writes nothing at the outdir path; close-attempt refuses MONITOR_ENDED_NO_RECEIPT; `status` reports it; every launch of that call refuses MONITOR_ENDED_NO_RECEIPT until a RESIDUAL_RETRY line for it (next bullet); any other ruling needs a P-112 successor.
- **Root's ruling on a residual: one machine form (RESIDUAL_RETRY).** Root's ruling on MONITOR_ENDED_NO_RECEIPT or MONITOR_STARTED_NO_LAUNCH_JSON has one machine form: a whole V006 line `RESIDUAL_RETRY <NAME> <k>` under the ruling entry. It is not a kit KINDS token, and it is parsed anchored, as TOOL_PIN: the line matches `^RESIDUAL_RETRY ([A-Z0-9][A-Z0-9_]*) ([1-9][0-9]*)$` under an entry heading. Text that mentions RESIDUAL_RETRY inside a line, as this entry does, is not such a line. A line that begins `RESIDUAL_RETRY ` and does not match refuses every P-112 launch (RESIDUAL_RETRY_MALFORMED). Duplicate lines for one (NAME, k) act as one.
  - With the line, attempt k of NAME is a non-attempt (G27 item 5) that uses its number. The next legal attempt is a retry at k+1 with attempt k's caps and solo mode, and no new registry entry (brief §6.12 applies, even at k = 1). That retry is P-112's, and the brief §1b carve-out ends for that call (G25 item 8). Numbering counts the k of every RESIDUAL_RETRY line for NAME.
  - Attempt k's caps and solo mode are those in its LAUNCH or MISLAUNCH record. With no such record (MONITOR_STARTED_NO_LAUNCH_JSON), they are the caps and solo mode the next-legal-attempt rule gave attempt k, recomputed from the records before it.
  - P-112 launches the retry only when no live process runs attempt k's monitor command or its planned driver command (`run --spec <spec> --outdir <outdir of k>`); otherwise it refuses RESIDUAL_ATTEMPT_PROCESS_ALIVE. The outdir of k is the kit's (`run_name_for`, kit L318, L354-355, under s0.run_root) when attempt k was the kit's (no kit LAUNCH record, P-112 attempt or RESIDUAL_RETRY line of the call before it; G25 item 8), and P-112's (brief §5) otherwise. MONITOR_STARTED_NO_LAUNCH_JSON leaves no record naming its launcher, so this rule decides it.
  - P-112 honours the line only while attempt k of NAME is one of the two residuals: a LAUNCH or MISLAUNCH record of k whose monitor is gone with no receipt; or no LAUNCH or MISLAUNCH record of k, the receipt's stdout or stderr present, and no `.launch.json`. Otherwise it refuses RESIDUAL_RETRY_NOT_RESIDUAL, so a line never turns an attempt that has a monitor receipt into a non-attempt. These are existence checks; nothing is opened.
  - Without the line, the call stays held. Any other ruling needs a P-112 successor.
  - **A second monitor refusal at one k (MONITOR_REFUSED_TWICE, D7)** cannot be recorded (exclusive create), so the state on disk is the same as after the first refusal. P-112 cannot see an unrecorded second refusal and does not hold the call; it admits a further launch at k as it admitted the first relaunch. Holding the call after MONITOR_REFUSED_TWICE is root's procedure (root runs every launch), and a third launch at k is made only on root's V006 ruling; no P-112 successor is needed for it.
  - One limit, disclosed: S0_SEED_SERIAL before its first kit LAUNCH record. P-112 refuses every launch until the kit holds a seed LAUNCH record (brief §6.2; r3a L454), and the kit's order-check refuses every other S0 call (SEED_SERIAL_NOT_LAUNCHED_FIRST, kit L785-788). A residual there needs a successor of the kit or of P-112, which root names in its ruling.
- **Schedule risk (disclosed; rule (c) as registered, not a new rule).**
  - A failing call needs two solo reruns at the doubled wall: up to 1,220,648 s each for a serial (S0 serials included), and 45,504 s for the twin.
  - Each serial rerun can add about 14 days to the start of Phase-1 step 4.
  - The hold rule runs every counted rerun alone, so reruns of different calls do not overlap, and their delays add.
- **Reviewers (D13).**
  - RUNBOOK c2v007, text and builder, is a root build reviewed by Codex1 with DN1/DN2 (A208 item 2(a)), not Claude4. It is pinned before Phase-1 step 4 (G1).
  - P-112 is reviewed by Claude4 (A205 item 8).
  - The G26 step-8 freeze script is a root build reviewed by Codex2 (A205 item 10).

### Disclosed readings

1. REFUSED, BLOCKED and signal deaths with no finish record are INFRA (A133 §3(c), "not INFRA").
2. Infrastructure deaths that surface as FAILED, FAILED_AT_STAGE or NONE|EXIT read literally as FAILED (D2). That includes a full disk, and a lost volume, when the monitor's receipt is still written; otherwise the attempt is MONITOR_ENDED_NO_RECEIPT (reading 19). The guard is the solo pair at the doubled wall.
3. ROUTE_A_NO_FIXED_POINT is FAILED, because it is a non-zero exit (L9102).
4. When the monitor and the driver disagree (FINISHED with a non-completed finish; CHILD_FAILED with COMPLETED or COMPLETED_INVALID), the status is INFRA.
5. A STOPPED_<cap> monitor status wins over every driver-side value.
6. A REFUSED or BLOCKED attempt is retried solo at the replaced attempt's caps. Two consecutive solo attempts with identical spec, caps and REFUSED (or BLOCKED) status read UNEVALUATED_INFRA_REPEAT. This is a pre-result registration under A133 §3 (L201), and it joins the DN5 trigger list.
7. "Other NGC process" is the declared tool list (D5). It holds the A211 stack of record, handoff c2v003a (the stricter reading), values writer v004 (A212) and the other listed producers and extractors. The ps count is a lower bound. The guarantee is the hold rule, which also covers any NGC tool not on the list, whenever it was adopted (the list reflects adoptions through A212).
8. "At RAM" is host RAM, and for the twin RAM × 11 (A172 N4; D3).
9. "Doubled" is 2 × the first attempt's wall cap. "Identical" is the identical composite raw status. The pair is the last two attempts of the call, non-attempts excluded, as c2v006 reads it; an attempt of any class between two failures separates them.
10. An OUTPUT_CAP rerun doubles the output cap, and the identity twin never has one. An INFRA or MISLAUNCH retry repeats the replaced attempt's caps and solo mode. A REFUSED or BLOCKED retry always runs solo.
11. Outside-set S0 serials are stopped at u_A (A133 L103).
12. A MONITOR_REFUSED attempt, or a LAUNCH or MISLAUNCH with no run directory or an unregistered spec, is not an attempt of the call. After such a LAUNCH or MISLAUNCH the call retries with its caps and solo mode (first-attempt caps if no attempt precedes it), with no new registry entry. An attempt named in a RESIDUAL_RETRY line while it has no monitor receipt is a non-attempt too, and the call retries the same way. A line never makes an attempt with a monitor receipt a non-attempt: assemble-registry and c2v007 refuse RESIDUAL_RETRY_NOT_RESIDUAL for such an attempt, and root rules.
13. A failed identity twin (a rule-(c) pair) is terminal for step 4. The identity then stays UNTESTED, and every call stays serial (A133 L111; A135 item 3).
14. The builder's θ function and the program θ key are both carried, and neither replaces the other.
15. DN5 replaces the C2V004 V-N1 trigger scope. The list's bytes are unchanged.
16. VN1's in-memory GEOMETRY_NOT_EXPOSED answers are the one registered exception to "never invents", and they count as evaluated.
17. G16 3(b): a call whose registered result fails to verify, with the run volume mounted, and has no same-sha copy is UNEVALUATED_CUSTODY_BREACH. This is a pre-result registration under A133 §3 (L201), and it joins the DN5 trigger list. The successor that records it is c2v006 `_apply_unevaluated` applied to exactly such calls, with UNEVALUATED_CUSTODY_BREACH in place of UNEVALUATED_STEP7_DISCREPANCY; it therefore also lowers member_budget, so later members read UNEVALUATED_BY_ORDER_TRUNCATION. c2v007 ledgers it as a CUSTODY entry kind and re-derives it byte for byte; anything else reads STEP7_LEDGER_BROKEN. A missing volume is a stop, never a breach.
18. G24: T is the latest time_utc over the set's terminal attempt receipts, as c2v007 re-derives it. Entries stamped after T are listed, and a gate that first appears in one of them is not a Phase-1 gate document. A cutoff record dated before c2v007's T reads GATE_CUTOFF_BEFORE_T, and root writes one successor record.
19. Three residual judgment points remain, and all three go to root: a second monitor refusal at the same attempt number and MONITOR_STARTED_NO_LAUNCH_JSON (a monitor that left its receipt stdout or stderr but wrote no .launch.json), both D7's; and MONITOR_ENDED_NO_RECEIPT (a LAUNCH or MISLAUNCH record exists, the monitor pid is gone, and the receipt is absent). Each is decided only with the run volume mounted. No value is read in any of them, and the outdir is never opened. Root's ruling on the last two has one machine form, a whole V006 line `RESIDUAL_RETRY <NAME> <k>`: attempt k, while it has no monitor receipt, becomes a non-attempt that uses its number, and the next legal attempt is P-112's retry at k+1 with attempt k's caps and solo mode. A line never makes an attempt with a monitor receipt a non-attempt (RESIDUAL_RETRY_NOT_RESIDUAL, and root rules). After a second monitor refusal at one k, root's procedure holds the call, not P-112, and a third launch at that k is made only on root's V006 ruling.
20. The kit keeps its own relaunches of an S0 call (after a kit MISLAUNCH, and the D7 relaunch) until the call has a LAUNCH record, a P-112 attempt or a RESIDUAL_RETRY line.

### Implementation owners

| owner | items | reviewer | needed by |
|---|---|---|---|
| P-112 launcher (Codex2) | G13 raw status and map, and the solo retry of REFUSED and BLOCKED; G25 sampler (five null cases, whole-second comparison, 1 s lead and tail), solo mode, reruns, twin mode, host RAM, stop-outside-set; G27 entries, attempt receipts, assemble-registry and its verify mode; D6 numbering with the kit carve-out (and the k of every RESIDUAL_RETRY line), and the retry after a non-attempt LAUNCH or MISLAUNCH; D7 records (five `absent` paths), MONITOR_STARTED_NO_LAUNCH_JSON, acceptance of root-written records (the `absent` check only until the same-k relaunch starts), and the same-k relaunch; MONITOR_ENDED_NO_RECEIPT (the sampler's 60 s stop, the close-attempt and launch refusals, `status`); the run volume first (RUN_VOLUME_NOT_MOUNTED before any residual, `absent` or RESIDUAL_RETRY check); RESIDUAL_RETRY (the anchored parse, the residual check in launch and assemble-registry, the live-process check, the retry at k+1); a monitor still alive with no .launch.json at the launch bound (stop it, then a MISLAUNCH or the D7 rules); `complete` as G25 item 4 defines it; the rule-(c) pair as c2v006 reads it; D8 TOOL_PIN gate (whole lines in PIN_RE form only) on every writing subcommand; D9 disk check; G24 machine cutoff copy, once, with T as the latest time_utc | Claude4, after Fri 23-Oct 19:00Z | 0 blocking before u_A (about Tue 27 to Wed 28 Oct) |
| RUNBOOK and builder c2v007 (root build) | attempt-receipt residence and re-derivation; recomputing other_ngc_processes_max from the pinned sample (whole-second comparison); attempt-0 evidence; twin RAM × 11 check; kit M-15 form; the INFRA_REPEAT pair (two consecutive solo attempts, identical spec, caps and status); the CUSTODY_BREACH successor (c2v006 `_apply_unevaluated` with UNEVALUATED_CUSTODY_BREACH, nothing else changed), its CUSTODY ledger entry kind, and the reader's re-check of both conditions with STEP7_LEDGER_BROKEN (two MUST_FAIL cases); non-attempt exclusion (an attempt named in a RESIDUAL_RETRY line only while it has no monitor receipt; RESIDUAL_RETRY_NOT_RESIDUAL otherwise); G7 tsr-support and tsr-check; VN1; DN5 value; G24 re-derivation of the terminal set and T, GATE_CUTOFF_BEFORE_T, and after-T gate exclusion; G16, G24 and N1 text | Codex1 (A208 item 2(a)) | pinned before Phase-1 step 4 (G1) |
| G26 freeze script (root build) | V-N1 per DN5 | Codex2 (A205 item 10) | before step 8 |
| Root procedures | the dict as receipt_status_classes; G15 copy; copies before every V006 write, from M-15 until c2v007 accepts the cutoff record; the single G24 successor cutoff record on GATE_CUTOFF_BEFORE_T; D4 stops; D7 records for kit calls (path and keys above), each written only after the monitor pid has exited and only with the run volume mounted, a monitor still alive when the kit script exited 5 at its 120 s wait being stopped first; a V006 ruling on each of the three residuals (reading 19), with a RESIDUAL_RETRY line where the ruling is a retry, written only on existence checks made with the run volume mounted; holding a call after MONITOR_REFUSED_TWICE, with a third launch at that k only on a V006 ruling; the hold rule, including NGC tools not on the list (adopted after A212); the TOOL_PIN line in P-112's adoption entry; spec fills for every P-112 call under the blinding guard; NGC ρ point registrations for every member or F point outside S0 at u_A (A211 N3); G16 custody copies of each terminal attempt's result, monitor receipt and attempt receipt at its receipt's close, and of the cut records at step 3, all before pass one, pinned at step 5; the run-volume mount check before any G16 3(a) or 3(b); the A135 item 11 extractor ruling before G7; the G16 Phase-2 SENSITIVITY-only form before Phase-2 pass one; G28 before the first FULL build | none | as listed |
| S0 kit C2V003A | no change | none | none |

**Amendments at insertion (root).**
- Root workflow wf_0bb1531a (fixer and checker, rounds 4-5) ended with 1 LOW-MED item and 8 LOW/TRIVIAL items. They are in `claude_artifacts/runbook_rulings_c2/ROUND5_DEFECTS_C2V001.md` `4e3977ab`.
- They are adopted here as written, as binding amendments to this entry and as required P-112 build items:
  1. the interrupted-launch handling: registry-entry admission with no LAUNCH record, `launch --resume`, and LAUNCH_RECORD_MISSING;
  2. the sampler-exit command-line test;
  3. a mount check on the volume that holds each attempt's outdir;
  4. the stop rule for a `.launch.json` that does not parse;
  5. the `## A108 continued` reading rule;
  6. the V006 citation update to "A213-A223 change no ruling here";
  7. the hold-rule wording "an NGC tool not on the list, whenever adopted";
  8. the stamp-from-date rule;
  9. the three small text fixes.
- **Root's insertion check:** `## A108 continued` (root's own text) changes no ruling here, and A213-A222 change no ruling here.
- **Source of this text:** `RULINGS_FINAL_V005_SOURCE.md` `f698defe`. The P-112 brief of record is `P112_LAUNCHER_BRIEF_V005.md` `cddbaa8d`, which carries this entry's number.

## A224: the date of record moves about one day earlier, on measured milestones; the drive is due by Sat 24-Oct (2026-10-20 17:33:49Z)

**Measured since A201:**
- Step S2 is DONE on Tue 20-Oct, two days ahead (A216).
- Every review that was waiting on Claude4's Fri reset and stood on the path to HEADLINE11 or W1 is done or reassigned. That covers 31/31 EPS, the C1 policy, the campaign set, the NGC acceptance stack and classifier B.
- The A129 finalization is run by root (A205 item 2).
- The PRELAUNCH route is settled (A218/A219).
- S4T R3 is measured at about 1.6× R2: fs columns 5.5 h against 8.9 h. Its rfs columns have run for about 4.1 h. The Wed 21 2 pm to Thu 22 noon CDT projection holds.

**Consequence.** HEADLINE11 now launches at the verdict, not after Fri 19:00Z. The new targets, in steps.tsv (previous targets kept in `steps_targets_v001_2026-10-20.tsv`):

| Step | Target |
|---|---|
| S3, verdict and pins | Wed 21 evening to Thu 22 |
| S4, HEADLINE11 and S0 | Thu 22 to Sun 25 (HEADLINE11 is about 3 days: 4 rounds of about 18 h at 3 concurrent) |
| S5, W1 launch | Sun 25 |
| S6, waves to u_A | Thu 29 to Fri 30 |
| S9, Phase-1 NGC | Sat 31 to Tue 3 Nov |
| **S10, Phase-1 score** | **about Mon 2 Nov (CST), range Fri 30 Oct to Thu 5 Nov** |

**Drive.** The W1 work dir (cache id, ledger path) must sit on the dedicated volume when root builds the W1 candidate config. Codex3's campaign policy review binds that ledger path. Both run during HEADLINE11, so the volume is due **by Sat 24-Oct**. The latest is Sun 25 morning, but that would put the policy review on the W1 path. The principal's Friday arrival meets this.

**Unchanged adders** (A201):
- reuse-test exit 5: +2.25 d;
- each repair wave: about +0.75 d;
- an S1 FAIL_TH2 holds Phase 1.

**New disclosed risk** (A223, schedule risk): a failing NGC call under rule (c) needs solo reruns at doubled wall, about 14 days each for an S0 serial. This is pre-registered, not an expected case.

## A225: apply_h3_fields_c2v006 closes VF-C2V005-01 and CX1-S4RA1-01, with every pin-binding read single-read; root verify PASS; Codex1 re-reviews it (0783) (2026-10-20 17:57:12Z)

**Tool:** `apply_fields_c2v006/apply_h3_fields_c2v006.py` **0ed72837684f345b311401ea90b9889cd46b8431753a4e0697225e9849aff951**. Tests `8ed6f753`, mutation `c60a0b1a`, README `1170162b`, diff `b1902093`, HASHES `9e641fc3`.

**Builder's sweep of c2v005.** Two double-read sites were fixed:
- **D1, `seal_derived`:** the report is now read once through a new `pin_read`, which hashes the buffer and returns it for parsing. This closes VF-C2V005-01.
- **D2, `value_problems` source_results:** one read now both decides and supplies the refusal text.

Four hash-only re-checks were kept:
- **K1:** the `block_source` field check;
- **K2-K4:** the `verdict_artifact`, `compare` and `sealed_prereg` field checks.

They parse nothing, and any change refuses. Folding them in would alter the no-flag path, which must stay byte-equal to c2v003.

**Tests:**
- 64/64, twice;
- the c2v003 suites with c2v006 swapped in: 90/90 and 77/77;
- mutations 18/18, including mutants that reintroduce each double read and one that drops `pin_read`'s sha check.

**Independent root verifier: PASS, 0 blocking.**
- Its own static and run-time sweep flags nothing in c2v006. It checked `open`, `io.open`, `os.read`, `read_text` and `json.load`.
- Its checks pass 23/23, and the retargeted adversarial suite passes 24/24. The builder's suites were re-run and pass.
- The written output always comes from the hashed read. A changed later read either refuses or yields the honest output.

**UNTESTED:** a real root-filled seal record. The deciding test is root's README V3 run at the verdict.

**Adoption:** on Codex1's re-review with 0 blocking (0783). c2v004 and c2v005 are not adopted.

## A226: the double-read (pin-then-reread) class across the launch path: scope of E_A220_1, and a root integrity envelope (root workflow wf_4d684f23: 3 finders and 151 adversarial verifiers) (2026-10-20 18:08:58Z)

**Sweep result.** 151 findings were confirmed:
- h3-campaign: 39 blocking-class and 7 notes;
- step-4 launch: 45 and 7;
- certificates and acceptance: 31 and 22.

The pattern is pervasive, and much of it is in reviewed, adopted or sealed objects:
- parent v005 `c75a889f`: `load_pinned_module` hashes a read, exec's a second read, then re-hashes; plus `_receipt_ok`, `check_adoption` and `resolve`;
- core `dc895f8a`, the q5b1 and ledger wrappers;
- the H3 accept-call, entry and evidence assembler;
- PRELAUNCH005, the S0 kit, phase1 v003b, the S1 lib;
- many superseded versions.

The full list is in the workflow journal.

**Assessment.** The defect needs a pinned file to change between two reads inside one process. On this path every pinned input is immutable by process: files are created exclusively and never edited, successors are new files, and runs never write to their inputs. Many paths also re-hash after use; for example, parent L440-441 re-hashes after exec. Rewriting the sealed and reviewed chain would invalidate its reviews and pins (C1, the policy tuple, the seal), with no change to the physics. A219 and A223's procedures already treat any changed pin as a refusal.

**Rulings.**
1. **Scope of E_A220_1.** The single-read rule is binding on **every tool built or changed from now on**: P-112, the G26 freeze script, apply_h3_fields c2v006, and any successor. Reviewers check it, and the A221 rule stands for those tools.
2. **Existing adopted, reviewed or sealed tools are not rewritten** for this class before launch. The class is a **disclosed limitation** in the seal entry and the PROVISIONAL label: "pinned inputs are verified by hash, but some reviewed tools read a file again after hashing; integrity relies on the immutability of the inputs, which the root envelope below checks."
3. **The root integrity envelope (mechanical, read-only).** At the start and at the end of each launch phase (the S0 seed, HEADLINE11, W1, each wave, the Phase-1 NGC set, S1, and the Phase-1 freeze), root hashes every pinned input that the phase's configs, plans, C1, registry and V006 pins name. The two manifests are compared.
   - **Any changed byte invalidates that phase's runs (pre-registered).** They are kept, never read as evidence, and rerun under rule (c) with new attempts.
   - The tool (`pinned_input_envelope_c2v001`) is built by a root workflow (builder plus verifier) and reviewed by Codex1. It is single-read, per ruling 1.
4. **The sweep's notes and blocking items in superseded versions** need no action.

## A227: apply_h3_fields_c2v006 is adopted on Codex1's re-review (0163: PASS, 0 blocking); S4-R-A1 is ready (2026-10-20 18:11:20Z)

**Review of record:** Codex1 0163, `review_final_deltas_cx1/APPLY_H3_C2V006_REVIEW_CX1_V001/REVIEW_RESULT.json` `69195806`. It covers CX1-S4RA1-01 and VF-C2V005-01.

**Adopted:** `h3_campaign_path_c2/apply_fields_c2v006/apply_h3_fields_c2v006.py` `0ed72837684f345b311401ea90b9889cd46b8431753a4e0697225e9849aff951`.
- It is the H3 fields tool of record. It supersedes c2v003 for all H3 config writes, and it is the only S4-R-A1 tool (A218(2)).
- c2v004 and c2v005 are not adopted.

**Use at the verdict (README V3, before the HEADLINE11 evidence assembly and V4):**
- `--block-source <FILLED de6d7d77 path> --block-source-sha256 de6d7d77…` on the H1 run config and on the W1 candidate config;
- the errata are ERRATA_S4RA1_C2V001 and C2V002.

**Codex1's UNTESTED items, now root's checks at the first real apply:**
- the written `verdict_artifact` sha and `sealed_prereg` object are verified against the report bytes;
- then the final W1/H1 configs, the real r5 prelaunch on the FILLED base, production seal/bind/launch, and the final W1 cache id.

**PLAN:** P-122 is DONE.

## A228: the integrity envelope c2v001 passes its core checks but needs c2v002 (2 blocking); C1's scratch provenance pins are outside the envelope (2026-10-20 18:54:40Z)

**c2v001** (`pinned_input_envelope_c2/`, tool `ecfce024`; root workflow wf_78aa2562).
- 52/52 tests, twice; 20/20 mutants killed.
- Single read is confirmed; compare and exit codes are correct; NGC3198-named files are hashed only.

**Verifier BLOCKING:**
- **B1.** V006 enters the pin set through other documents' pins. For example, Codex3's C1 policy review pins V006 at an older sha. So every phase that includes C1 reads INVALIDATE at START.
- **B2.** The default depth of 8 follows the whole pin history: 553 pins, including a path pinned at two shas, old run outputs on External1, and a scratch draft. That is not "the phase's inputs" (A226 item 3).
- At depth 0 the real C1, registry and V006 are clean: START 160/160 and compare OK.

**Rulings for c2v002** (root workflow, then Codex1 review):
- **D1:** V006, however it is reached, is an excluded growing file. It is listed and never snapshotted.
- **D2:** the default depth is 0, and each phase command states its depth.
- **D3:** collect from the phase's run configs, plans and admissions (which carry C1's tail_readiness). C1 itself is collected only with the scope `/tail_readiness`. An `--exclude PATH --reason` list is recorded in the manifest.
- **D4:** a ctime-only change is a NOTE when the xattr-name set changed (explained metadata), and INVALIDATE otherwise.
- **D5:** a root or followed document that fails to parse refuses.
- **D6:** compare requires both manifest shas.
- **D7:** pin paths that do not encode refuse.
- N6 (a parent-folder swap race) stays a disclosed note.

**C1's scratch provenance pins.** Frozen C1 `40159322` carries two `/private/tmp` scratch pins outside tail_readiness (`supersedes.draft`, `sources_read_v002.draft_v001`). A213 note 7 said they would be replaced at the freeze. The fill tool changes only `certificate_policy_review`, so they remain.
- **E_A213_7.** The A213 note 7 promise was not kept.
- **Disposition:** these pins are non-binding provenance. Nothing in the run path reads them (tail_readiness is the block copied into run configs). D3 keeps them out of the envelope. C1 is not refrozen; re-freezing would change its sha and the verify record for no physics gain.
- **Disclosed:** C1's provenance block cites scratch drafts that may not persist.

## A229: P-112 cx2v001 FAILs root verify (two lenses, root workflow wf_a86fff74); Codex2 builds cx2v002 (0784) (2026-10-20 19:12:47Z)

**What holds:**
- Codex2's suite: 580/580, twice. The records are byte-identical to Codex2's. All 229 refusal codes are exercised, and 35/35 mutants are killed.
- The G13 map (`c36c3788`), the declared process list, the 42 source pins and ATTEMPT_RE all match.
- An audit hook saw 3,555 opens and 0 forbidden opens across the suite.
- The conformance map covers every brief, ROUND5 and 0782 requirement.

**BLOCKING** (findings: `phase1_ngc_launch_kit_cx2_rootverify_c2/ROOT_VERIFY_FINDINGS_C2V001.md` `16e97b2c`):
- **B1-B3 (A226 item 1, single-read).** Three sites hash one read and use another:
  - `write_launch_record` pins a re-read `.launch.json` (L1956/L1960), not the checked buffer (L1980/L1925);
  - `history` classifies a non-attempt on read L1469 but pins read L1474;
  - `assemble_registry --verify` compares one read (L1771) but reports the pin of another (L1773).
  - Each attack was reproduced (RV01-RV03).
- **B4.** `command_argv` runs `shlex.split` on `ps` rows that are not quoted. One unrelated process with an apostrophe in its argv makes the sample null (a lost counted rerun, about 14 days), stalls the sampler, or refuses the launch (RV11-RV14). This is a realistic trigger on this host, given the agent lanes' shell commands.

**Required in the same successor** (root's ruling; recommended by the lenses):
- **F1, blinding:** `guard_read` plus a `realpath == path` check before every monitor-record and `.launch.json` read. A symlink otherwise leads P-112 into outdir files (RV05/RV06).
- **F2:** split lines on "\n" only (the kit's form), for TOOL_PIN and RESIDUAL_RETRY parsing.
- **F3:** resume finds the monitor by command line when `monitor_pid.json` is missing.
- **F4:** kill-target exit 1 counts as ALREADY_ENDED only when the kit's stderr JSON says `"alive": false`.
- **F5, root's call, ruled yes:** the V006 path is a constant, and `config.v006` must equal it outside synthetic mode.
- **F6:** a `V007_POSTSEAL_RECORDS` component guard in `path_rules`.
- **Cleanup:** the about-17 `pin_of` then `read_pin` double reads (they fail closed) are folded into one `read_and_pin` helper.
- Each fix gets tests and a mutant. The README states the A226 item 2 disclosure (pinned executables are hashed, then run by path in a child; the envelope covers this).

**Process note:** a second, concurrent verifier process wrote `VERIFY_C2_20261020T185533Z/` into the root-verify folder. Both lenses ran in parallel and share the folder. Nothing was overwritten.

**Timing:** P-112 is needed at u_A, about Thu 29 to Fri 30 Oct (A224). There is room for cx2v002, root re-verify, and Claude4's review after Fri 19:00Z.

## A230: integrity envelope c2v002 passes root verify (PASS_WITH_FIXES, 0 blocking; root workflow wf_c913c4e5); Codex1 reviews it (0787) (2026-10-20 19:29:46Z)

**Tool:** `pinned_input_envelope_c2v002/pinned_input_envelope_c2v002.py` **0fac239ad7e5573084bfa494e55a344f40ab4deaa3469d5d54671ca5b457598c**. Tests `d0494caf`, mutation `59e20a66`, README `bcf34ecb`, errata E1 `048ad43e`, HASHES `b097061b`.

**Tests:** 82/82, twice (all 52 c2v001 rows carried, 30 new). Mutants 45/45 killed.

**D1-D7 are built as ruled in A228.** Choices beyond the ruling, listed in the README:
- inode-matched exclusion;
- `--depth-reason` is required for any depth above 0;
- a chmod or an added hard link now reads INVALIDATE;
- a growing launch registry is walked with `--walk-only` and excluded with a reason.

**Real inputs, depth 0** (the README's HEADLINE11 procedure, run under bash): C1 scoped to /tail_readiness, plus registry 2dea408f, plus V006.
- **START, END and compare: exit 0, OK.**
- V006 is excluded. That includes the S0 kit's GATE_DOCUMENT_PINS pin of V006 at `9bcb3150`, which is excluded.
- No /private/tmp pins, no /Volumes pins, and no path pinned at two shas. C1's binding block gives 13 pins, and the set has 125 distinct pins.
- Single read is confirmed.

**Fixes, made by errata E1** (the README is not edited):
- F1: run the README blocks under /bin/bash (zsh doesn't word-split);
- F2: the full S0 sha `5e688882…148042`;
- the operating rules: no chmod of pinned inputs, and no GUI opening of pinned inputs during a phase.

**Adoption:** on Codex1's review with 0 blocking. First use: the START snapshot of the S0 and HEADLINE11 phase at the verdict.

## A231: Codex1 0164 FAILs envelope c2v002 with 1 blocking item, accepted; c2v003 is commissioned (2026-10-20 19:35:34Z)

**Blocking item CX1-ENV-01** (Codex1 `review_final_deltas_cx1/ENVELOPE_C2V002_REVIEW_CX1_V001/REVIEW_RESULT.json` `39c09b50`):
- snapshot and collect cache reads by realpath, not by file identity. So two hard-link paths to one inode are each read: two content reads, exit 0.
- Codex1 scopes it as a contract violation of A226 item 1, not acceptance of unhashed bytes. Both observations are hashed correctly.
- The suite (82/82) and mutations (45/45) were otherwise confirmed.

**Root's choice for c2v003** (root workflow wf_62466e4f):
- One content read is shared across aliases, keyed by (dev, ino).
- Each alias keeps its own path resolution, checked against the descriptor (O_NOFOLLOW open, fstat compared with stat), and the manifest marks aliases with `alias_of`.
- An alias whose inode changes between collect and snapshot reads INVALIDATE.

**Regressions:**
- hard links in both snapshot and collect, with independent content-read counts (exactly one per inode);
- mutants that restore realpath-only caching.

c2v002 is not adopted. Codex1 re-reviews c2v003. The first use is still at the verdict. Schedule: no effect.

## A232: envelope c2v003 closes CX1-ENV-01; root verify PASS, 0 blocking (root workflow wf_62466e4f); Codex1 re-reviews it (0788) (2026-10-20 20:06:58Z)

**Tool:** `pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py` **9d531381615f7b68f2f33bfc19f0aa2bcfe97a4e6f5c0e93187ea8eb35ce8d9a**. Tests `2bcfc1b8`, mutation `7d94e191`, AST delta `a05c67e4`, README `3f0a63f9` (errata E1 carried), HASHES `5f1af111`.

**The fix.** One content read per (dev, ino), taken from the O_NOFOLLOW descriptor's fstat.
- A hard link that was already read takes the shared result after an lstat check, with no open.
- The race path closes a duplicate descriptor before any read.
- Aliases are marked `alias_of`.
- **Beyond the ruling:** a name takes the shared result only while its own stat still equals the read's. Otherwise it is `changed_during_read` and INVALIDATE.

**Results:**
- tests 94/94, twice (82 carried, 12 new hard-link rows); mutants 55/55;
- AST: 68 of 77 names identical, and the changes are confined to the read and caching path;
- against c2v002, the 12 new rows fail, which reproduces CX1-ENV-01.

**Independent verifier: PASS.**
- Codex1's own_checks: c2v002 reads the inode twice, and c2v003 once.
- The real depth-0 collect (C1 /tail_readiness, registry, V006) exits 0. Its pin set matches c2v002's real check (125 pins, the same exclusions and scopes). The only differences are the version fields and V006's own growth, which is expected under D1.

**Notes:**
- N1: c2v003 refuses c2v002 artifacts, so a phase uses one tool version end to end.
- N2: the stricter in-snapshot alias check can only INVALIDATE, never give a false match.
- N4: a name-only content guard for a hard-link name of an NGC3198 file is pre-existing and unchanged. Root never makes hard links.

**Adoption:** on Codex1's re-review with 0 blocking.

## A233: P-112 cx2v002 root re-verify. Every A229 fix is closed, but 1 new blocking item (V1); Codex2 builds cx2v003 (0789) (2026-10-20 20:09:12Z)

**Closed** (lens 1). B1-B4, F1-F6, the cleanup, and the 0785 and 0786 rules are all closed:
- Codex2's suite 639/639, twice, byte-identical to Codex2's; 236/236 refusal codes; 56/56 mutants;
- the 25 original root attacks now pass (14 failed on cx2v001);
- root's 22 restoring mutants behave as expected.

**Additions accepted:**
- surrogateescape decoding of `ps`, which fixes a real crash (RV34). It is recorded here as an addition to B4.
- the new record fields: `launch_wait`, `monitor_pid_source`, `launch_json_within_bound`, and `observations` everywhere.

**BLOCKING V1** (lens 2, reproduced on the real `ps`):
- The sampler raises MULTIPLE_MONITORS (L1334-1335) when any process's argv carries the monitor path and `--receipt <receipt>` as tokens. For example `pgrep -f`, or `ps | grep` with the planned command, which is the A223 "gone" check itself.
- The sampler then dies with no `.solo.json`, and close writes a null sample: a lost counted rerun, about 14 days.
- **Fix:** once `monitor_pid.json` exists, filter matches to that pid, and never raise from one row. Match on the plan's exact `monitor_argv` plus `pgid == pid`.

**Required in cx2v003** (root's ruling):
- **F-a.** Resume and null-pid liveness use the same exact-argv and pgid rule, so a decoy is never adopted as the monitor.
- **F-b.** A blank-argv `ps` row is accepted as command "" and not counted.
- **F-c.** `identify` reads only regular files (`S_ISREG`), with a size cap. A FIFO argument otherwise hangs the counter.
- **F-d.** `command_argv` is `split()` only. shlex-first can hide a listed tool and give a false zero.
- **F-e.** kill-target ALREADY_ENDED needs the planned driver command (and `child_pid`) to be absent from `ps`. Kit stderr is captured as bytes, and a decode failure counts as NOT_KILLED. Add a timeout.
- **A15.** Field-type hardening in `launch_checks`.
- **A06.** An orphan sibling from a crash is verified and reused, or refused with a named code.
- **A10.** Records and cutoff copies with `st_nlink != 1` refuse, consistent with the envelope (A230).
- **A09.** README correction: work logs are guard-read only.
- **Lens-1 fixes:**
  - a realpath check at config time for `s0.launch_root` and `s0.run_root`;
  - close checks the solo sample's `monitor_receipt` pin against the receipt it uses;
  - remove the dead `IMPLEMENTATION_REVISION` and `v006_gate_observation`;
  - disclose the MULTIPLE_MONITORS behaviour change.
- Each item gets a test and a restoring mutant.

**TOOL_PIN name:** `P112_LAUNCHER_CX2V003`.
**Findings file:** `phase1_ngc_launch_kit_cx2v002_rootverify_c2/ROOT_REVERIFY_FINDINGS_C2V002.md` `1f280b79`.
**Schedule:** P-112 is needed about Thu 29 to Fri 30 Oct. Claude4 reviews it after Fri 19:00Z.

## A234: integrity envelope c2v003 is adopted on Codex1's re-review (0165: PASS, 0 blocking) (2026-10-20 20:12:22Z)

**Adopted:** `claude_artifacts/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py` `9d531381615f7b68f2f33bfc19f0aa2bcfe97a4e6f5c0e93187ea8eb35ce8d9a`.
- This is the root integrity envelope of record (A226 item 3), with README_PINNED_INPUT_ENVELOPE_C2V003 and errata E1, carried over.
- c2v001 and c2v002 are not adopted.

**Operating rules (from A228, A230 and A232):**
- one tool version per phase;
- depth 0;
- C1 enters only through `/tail_readiness`;
- run the README blocks under /bin/bash;
- no chmod, hard links or GUI opening of pinned inputs during a phase;
- any INVALIDATE (exit 3) invalidates that phase's runs (pre-registered).

**First use:** START and END of the S0 + HEADLINE11 phase at the verdict. The first real snapshot is the deciding test of the real-mode path.

**PLAN:** P-123 DONE.

## A235: P-112 cx2v003 passes root verify. Both lenses PASS_WITH_FIXES, 0 blocking (root workflow wf_97d200ad); Claude4 reviews it after Fri 19:00Z (0790) (2026-10-20 20:58:54Z)

**Object:** `phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003.py` **af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7** (Codex2 0551). Suite 681/681, twice, byte-identical; 241/241 refusal codes; 78/78 mutants; all 109 HASHES entries match.

**Lens 1 (fixes closed):** every A233 item is closed.
- The root harnesses, retargeted, all pass: RV01-RV35 35/35, and A-series plus A233 regressions 31/31.
- Restoring mutants behave as expected: 27/27 and 21/21.
- 0 forbidden opens.

**Lens 2 (fresh adversarial on the changed code):** 25 new attacks plus single-read inventories.
- Every case at BLOCKING or FIX severity passes.
- On the real `ps`: V1 is closed; resume and null-pid matching never adopt a decoy; a FIFO, device or over-cap `identify` is safe; blank and escaped rows are handled.
- **Single read:** 0 duplicate reads of fixed inputs across 15 operations, and V006 is read once per CLI operation.

**Notes, carried to Claude4's review; none gates adoption:**
- **N1 (B04).** `monitor_pid.json` read mid-write kills the sampler. That would null a sample with probability about 1e-5 to 3e-5 per attempt. A future fix: read it as a changing file until it parses.
- **N2.** A15 validation inside `try_launch_json` turns a misshapen launch.json into a raise rather than a MISLAUNCH. The pinned monitor cannot produce one.
- **N3.** Four sites (L1342, 1606, 1717, 2174) still match monitors by name only. A live pgrep probe there fails closed: transient, and no record is written.
- **N4.** A probe whose argv contains the driver path followed by `run` is counted as an NGC process (carried from earlier versions).
- **N5.** An orphan sibling blocks its call until root's explicit successor procedure runs (README).

**Operating rules for root,** from N3 and N4: while P-112 attempts run, no `pgrep -f` and no `ps | grep` that names the monitor receipt or the driver command. Liveness is checked only through P-112 `status` or `kill -0 <pid>`.

**Findings:** `phase1_ngc_launch_kit_cx2v003_rootverify_c2/ROOT_REVERIFY_FINDINGS_C2V003.md` `d6c9deb9`.

**Adoption path:** Claude4's review returns 0 blocking (after Fri 23-Oct 19:00Z). Root then writes the whole-line `TOOL_PIN P112_LAUNCHER_CX2V003 af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7 <realpath>` in V006. Before that line exists, P-112 cannot launch. It is needed at u_A, about Thu 29 to Fri 30 Oct.

## A236: root credit plan to the Thu reset. Claude2's weekly limit is 90 % used (resets Thu 22-Oct 18:00Z) (2026-10-20 21:33:03Z)

**Measured** (`get_usage`, 21:33Z): weekly 90 % used, and the 5-hour window 1 %. Most of the day's use went to the launch-path double-read sweep (A226: 154 agents, about 14 M subagent tokens) and to the verify rounds.

**Ruling.** The remaining 10 % is reserved for the verdict-day work that root must do itself before Thu 18:00Z:
- the S4T R3 receipt;
- the cases manifest;
- the five post-seal gate producers;
- the sealed compare and the verdict;
- running the A129 finalization (0166) and the H3 r12 build;
- the T0 pins;
- the envelope START snapshot;
- the S0 and HEADLINE11 launches.

**Until the reset:**
- no new multi-agent root workflows, except a lean verify that a verdict-day step needs;
- monitors are kept;
- the RUNBOOK successor c2v007 and the G26 freeze-script builds stay after the Thu reset, as A201 planned. Both are needed only at the Phase-1 freeze (about Sun 1 Nov);
- builds and reviews that can go to the Codex lanes (Codex1, Codex2, Codex3, all with credit) are routed there.

**Lesson (register):** a whole-tree sweep at this scale is affordable only early in a weekly window. Root checks `get_usage` before any workflow of more than about 10 agents.

## A237: S4T R3 finish re-projected from the stage structure; E_A235_PROJ (the 18:42Z statement assumed equal-length le stages) (2026-10-20 23:34:12Z)

**Measured.** S4T R3:
- fs columns: 5.47 h (02:31 to 07:59 CDT);
- rfs columns: 5.42 h (08:17 to 13:42 CDT);
- le1 columns: started 18:42Z, and still running at 23:33Z (4.85 h). The monitor (pid 99575) is alive.

**Structure,** from the stage-directory names and times of the C4T R2 run (no outputs read):
- after rfs come five levels, le1 to le5;
- each level is a columns stage, then rotation, column_mean and feedback;
- the le columns ran 1.72×, 1.52×, 1.27×, 1.11× and 1.11× the fs columns time;
- each level's rotation, mean and feedback add about 20 min.

**Re-projection** (UNTESTED; the le1 duration will decide it):
- If the le columns run about equal to fs (ratio 1.0): 5 × 5.45 h + about 1.5 h → about **Wed 21 6:30 pm CDT**.
- At C4T's ratios: about 36.7 h + 1.5 h → about **Thu 22 4 am CDT**.
- **Range: Wed 6:30 pm to Thu 4 am CDT.** That is inside S1's window (Wed 2 pm to Thu noon), and far below the 792,000 s cap, so the E_A184_1 check passes.

**E_A235_PROJ.** At 18:42Z root told the principal "Wed late afternoon or evening", assuming each remaining column stage equals 5.4 h and missing that there are five le levels. Rule: a projection uses the stage structure of a finished sibling run.

**No date of record changes.** If S4T finishes Thu early morning, the verdict and pins land Thu, HEADLINE11 launches Thu and finishes about Sun, and W1 starts Sun 25 (A224).

## A238: the remaining Phase-1 builds move to the Codex lanes now, in parallel with S4T, instead of after root's Thu reset (2026-10-21 07:58:16Z)

**Principal:** "Are there any other opportunities for parallel activity? … To the extent that parallel activity could accelerate progress."

**Assessment.**
- Compute cannot be widened. Every next run (S0, HEADLINE11, W1) waits on the step-3 verdict, the waves are sequential, and the host is at its concurrency design.
- The post-seal producers (MT, I1T, FLAG_RULINGS and the rest) take the all-case manifest, so they cannot be pre-run on the 9 finished cases. A rehearsal would also expose gate readings before the compare, which blinding forbids.
- The parallel lever is the remaining **builds**. P-112 needed three verify rounds, so starting the rest now keeps them off the critical path.

**Rulings** (superseding A205 item 10, the A223 owner table's "root build" for c2v007, and A209 item 7's root build of the S1 C1):
1. **RUNBOOK successor c2v007** (the text, plus `roster_builder_c2v007` implementing A223: the status map, role keys, sample recompute, VN1/DN5, G24, G16 and the custody successor).
   - **Built by Codex2,** which wrote P-112, whose records the builder consumes.
   - **Reviewers:** Codex1 (A208) and root verify after the Thu reset. It is needed at the first Phase-1 FULL build. G28 is ruled by root before that build.
2. **G26 step-8 freeze script.** Built by Codex2 after c2v007, with synthetic slots only; root runs the slots check at freeze.
   - **Reviewers:** Codex1 and root verify. Claude4 is the fallback.
   - It applies DN2 (spec sha `e2a7650e`, notes sha `56ac5c64`, the manifest's NGC coordinates equal to slots V003, read only at root's run), G24 and G16. Needed at the Phase-1 freeze.
3. **S1 C1 successor draft** (A209 item 7: KS6′ `c8dc59a1`, G2 `7eb456cd` and G6b `65834e9b` check their own approval).
   - **Drafted by Codex1:** the approved-producer list derived from code, with the same verifier-successor need checked as in A209.
   - Root rules the list after the Thu reset. Codex3 signs the S1 C1 policy review (A205 item 4(iii)). Needed after u_A, about Oct 30.
4. **Effect.** The expected Phase-1 date does not move; it is set by compute. These moves take the build risk off the post-reset root window and off the freeze path.

## A239: checkpoint and resume feasibility is commissioned (principal's direction); the current rule stands until a registered, equivalence-tested successor (2026-10-21 08:01:57Z)

**Principal:** "Can we also explore the extent to which we can use checkpoints to avoid the problem of failing and losing several days of work because the work can't be restarted?"

**Current rule, unchanged until replaced:**
- The NGC acceptance execution-facts rule (handoff c2v005; A211 F2) requires a completed, fresh, single computed route A, starting from zero, with no retry, reload or resume.
- The step-2 runs had "resume: none" (A197).
- Rule (c) reruns a failed call solo at doubled wall (A133 §3). An NGC serial failing late costs about 7-14 days.

**Physics-first conditions** for any successor (root's ruling):
1. **A deciding test of bitwise equivalence:** an uninterrupted run against an interrupted-and-resumed run of the same call, compared byte for byte on the result and on every record that acceptance reads.
2. **Resume only after an INFRA-class end** (the A223 G13 map: host restart, signal or external kill, monitor or volume loss). Never after FAILED, CAP or OUTPUT_CAP.
3. **A disclosed pre-result registration** under A133 §3, adopted before any NGC result is read. Plus an acceptance-rule successor that admits exactly the proven resume form, and a P-112 successor that drives it.

**Commissioned (0793):** Codex3, the driver cx3r008 lineage, does a read-only feasibility study:
- the existing checkpoint support in the driver, in route A (`resumable_coupled_gas_0422`, the `*_resume_*` iterators) and in the NGC chain;
- where a resume would break bitwise reproducibility (RNG, BLAS order, caches, timestamps in records);
- the minimal design;
- the deciding-test plan and its compute cost;
- the expected days saved per failure class;
- the registration path.

Root rules after the study. The schedule is not affected: Phase 1's first NGC runs launch under the current rule.

## A240: the S1 C1 producer lists are ruled on Codex1's draft (0166: PASS, 0 blocking); the KS3/KS4 verifier successor and source closure are commissioned (P-121) (2026-10-21 08:03:33Z)

**Draft of record:** `claude_artifacts/s1_c1_producer_list_cx1/S1_C1_PRODUCER_LIST_DRAFT_CX1V001.json` `ccb8f7d1` (README `2ab7295c`, script `8e238b2f`).
- 15 source pins were rechecked.
- A static trace of emission, approval and source trust was made.
- 6/6 isolated exact-AST `c1_policy_gate` cases pass.

**Ruling** (the A209 pattern applied to S1):
1. **The S1 C1 `approved_certificate_producers`, in this order:**
   - G4 EPS;
   - G3 GQ;
   - G1 slot;
   - KS6′ LO (`c8dc59a1`);
   - G2 SRB_ROT (`7eb456cd`);
   - G6b signed-GQ evidence (`65834e9b`).

   The exact pins are as in the draft.
2. **`trusted_source_producers`:** [67fddd24 (the row producer), 65834e9b (G6b)].
3. **Verifier successor.** The existing KS4′ refuses the expanded list with exactly 3 canonical blockers, as c3v004 did. A minimal KS3/KS4 successor grows the canonical set to six. Non-S1 behaviour is unchanged.
   - **Built by Codex1** (0794). Root verifies after the Thu reset, and Codex3's S1 C1 policy review (A205 item 4(iii)) is the distinct check.
4. **Source closure.** lib v002c's admission additions omit the 3 added certificate pins. The S1 admission sources must include them; the deciding test is the S1 dry launch (A185 item 1). Codex1 drafts the closure delta with the successor.
5. **The order, uniqueness and completeness of the list are not enforced by membership** (as A213 note 2). The S1 C1 freeze tool must enforce them by digest, as fill_c1_pin_c2v002 does for H1.

**Needed:** after u_A, about Oct 30.

## A241: the conflict between A226 item 1 and the "minimal AST delta" for the KS3/KS4 successor is ruled; the narrow single-read change is allowed (2026-10-21 08:08:00Z)

**Codex1 0167 (FAIL, 1 blocking, CX1-KS-SR-01).**
- The inherited `c1_policy_gate` (`registry_assembler_ks4_cx1v001.py` L439-443) reads `certificate_policy_review` twice, through common `read_json_pinned` → `read_bytes_pinned`.
- The audit single-read MUST_PASS fails, and the minimal-AST rule in 0794 forbade the fix.
- Everything else holds: 8/8 policy-gate cases, 5/5 mutations, the exact AST delta and existing-pin preservation.

**Ruling.**
1. **A226 item 1 governs.** A successor counts as "built or changed" and must be single-read. The allowed AST delta grows by one narrow change: `c1_policy_gate` reads the review once (`read_bytes_pinned`), checks its sha, and parses that same buffer. It may add one helper, `read_json_once`. Everything else stays AST-identical.
2. **Tests:**
   - the audit single-read MUST_PASS (exactly one read of the review);
   - a restoring mutant that puts the double read back;
   - all prior cases.
3. **The adopted H1 verifier c3v005** has the same inherited double read. It was adopted before A226 (A215). Under A226 item 2 it is not rewritten: the limitation is disclosed, and the envelope covers the review file at every phase.

## A242: checkpoint and resume ruling after Codex3's study (0669). NO_RESUME stands for Phase 1 and Phase 2; INFRA risk is mitigated operationally (2026-10-21 08:15:08Z)

**Study:** `checkpoint_resume_study_cx3/STUDY_CX3V001.md` `41966e36` and the JSON `a06a3057`. It is static: 44 checks, 103 citations resolved, and 27 risks. Codex3's same-lineage authorship of the driver is disclosed.

**Findings:**
1. **Literal bitwise equality of every record that acceptance reads (A239 condition 1) is not achievable.** Truthful elapsed time, PID and attempt identity, and the resumed/retried facts necessarily differ. A resume path would need a pre-registered partition into deterministic scientific records (bitwise-equal) and operational evidence (truthful, allowed to differ). That is a new rule, not a waiver.
2. **Column and iteration checkpoints exist and validate exact state and order.** But the registered driver starts from zero and refuses an existing outdir. The UV-tail sidecar has a separate, non-atomic commit frontier.
3. **Savings apply to INFRA only.** CAP, FAILED and OUTPUT_CAP savings are 0, and infra-origin FAILED cases are excluded. For an S0 serial (first cap about 7.06 d), an INFRA loss would save about 3.5 d if the failure point is uniform, or about 6.4 d late in the run (UNTESTED models).
4. **The deciding-test cost is high:** 4·T_D + 4·T_N plus replay. At NGC cap scale that is about 678 h (about 28 d) of compute, competing with the Phase-1 runs on the same host.

**Ruling.**
- **NO_RESUME stands** for the Phase-1 and Phase-2 registered calls. Rule (c) is unchanged.
- **Resume development is deferred** until after the Phase-2 score. It would need the schema-partition registration, an atomic sidecar, and a deciding test run on a separate compute budget. The study is kept as the starting point, and no lane works on it during 120/43 (galaxy-run-only rule).

**Operational INFRA mitigation instead** (the actual exposure):
- (a) keep `caffeinate` on every launch (already done);
- (b) **the principal is asked to:** put the Mac and the run drives on a UPS if one is available; keep automatic macOS updates and restarts off for the run window, through about mid-November; and avoid unplugging the External1 drive or the new campaign volume during runs;
- (c) root never restarts the host or remounts volumes during a phase.

Root does not change system settings itself.

## A243: register entry. Codex2 0553 reports a synthetic-test rename in its own new build folder; accepted as disclosed, and the fix is adopted (2026-10-21 08:45:06Z)

**What happened.** While porting the 160-case c2v006 suite, inherited case K16 ran an `os.rename` on one **synthetic** ledger directory inside `runbook_v002_c2v007_cx2/inherited_tests_draft003_run001/`. It then created a replacement directory with a copied foreign genesis, to test that it is rejected.
- No reviewed file, production record or run directory was moved.
- Both directories are kept in place, with no undo, deletion or overwrite.
- K12 failed before reaching its rename.

**Disposition.**
- This is a breach of the no-moves rule, confined to synthetic fixtures in the lane's own new folder. Codex2 self-reported it.
- **Codex2's fix is adopted:** both rename-based cases become in-memory path/byte simulations, plus an audit fence that rejects every rename, remove or overwrite in the c2v007 suite.
- **Standing rule for every lane:** a test harness ported from a predecessor is scanned for rename, remove and overwrite calls before its first run.
- The c2v007 release evidence is the post-fence suite run. The 124/160 development run is not.

## A244: cap ends never invalidate. An escalating-cap rerun rule is a disclosed pre-result registration under A133 §3 (principal's direction) (2026-10-21 09:00:04Z)

**Principal (verbatim):** "Let's make sure that we can also re run if we have an arbitrary rule somewhere that times out a run."

**Basis.**
- A cap is not physics (A141 L1).
- The driver is deterministic and bitwise reproducible (G4). A larger cap changes only whether a result arrives, never its value.
- Under A133 §3(c) as applied in A223 (G13/G25), two identical counted CAP ends make a call terminal. So a slow but correct computation could be lost to a cap.
- This registration is made **before any NGC result is read** and before any Phase-1 call has launched. It is disclosed in the seal entry.

**Ruling (binding on every registered launch path: the S0 kit, P-112, the HEADLINE11/DIII/SENS direct batches, the W1 campaign waves, S1):**
1. **The CAP class does not count toward rule (c)'s invalidating pair.** That covers STOPPED_WALL_CAP, STOPPED_RSS_CAP and STOPPED_OUTPUT_CAP. Only FAILED-class ends count, as before.
2. **Escalating reruns.** After a CAP end, the next attempt runs solo, as rule (c) does:
   - wall = 2 × the previous attempt's wall;
   - RSS at host RAM (the twin's RAM×11 per A223 D3);
   - output cap = 2 × the previous one, subject to the D9 free-space check.
   - There is no attempt-count limit for CAP ends.
3. **Schedule ceiling.** If the next wall would end past the phase's freeze deadline, the call becomes **UNEVALUATED_CAP_BUDGET**. That is FREEZE_INCOMPLETE and disclosed, never MEMBER_INVALID. It joins the DN5 trigger list, with UNEVALUATED_INFRA_REPEAT and UNEVALUATED_CUSTODY_BREACH.
4. **Physics guard.** A FAILED-class end (including ROUTE_A_NO_FIXED_POINT, a model outcome) still follows rule (c) unchanged. A non-converging computation is not rescued by more wall.
5. **Implementation.**
   - **Codex1 audits every cap on every launch path** (0796): where it is set, what happens at it, and which code applies the counted pair.
   - Root then rules the per-path changes. P-112 (cx2v004) and builder c2v007 (Codex2) take the change, and other paths by successor or by root procedure.
   - Until then: **if any registered call ends at a cap, root applies this rule by hand.** There is a solo rerun at doubled caps, recorded in V006, and no invalidation.

PLAN: P-125, under S4.

## A245: A244 widened. No non-physics interruption ever counts against a call; only a reproduced model outcome does (principal's direction) (2026-10-21 09:00:45Z)

**Principal (verbatim):** "In other words, any non-physics reason for the interruption."

**Ruling** (a disclosed pre-result registration under A133 §3; it supersedes A223's D2 literal-FAILED reading and the terminal UNEVALUATED_INFRA_REPEAT):
1. **Never counted.** These ends always lead to a rerun and never count toward rule (c)'s pair:
   - every CAP end (A244);
   - every INFRA end: a signal or external kill, a host restart or power loss, monitor or volume loss, MISLAUNCH, a monitor refusal, NONE|EXIT with no driver finish record, an OSError, MemoryError or I/O / disk-full error, UNREADABLE_FINISH and RESULT_HASH_MISMATCH;
   - any operator stop;
   - **any FAILED or FAILED_AT_STAGE whose cause is one of the above**, for example a stage child killed by a signal (driver L1864).
2. **Counted, the physics guard.** A FAILED-class end counts only when **both** hold:
   - (a) the driver's finish record names a **model outcome**: ROUTE_A_NO_FIXED_POINT, or a solver or numerical failure code that the code-of-record audit (0796/0797) lists as a model outcome;
   - (b) it **reproduces identically** on a solo rerun: the same stage, status and failure code.

   Because the driver is deterministic, identical reproduction is the evidence that it is physics. A non-reproduced FAILED is non-physics, so it is rerun and not counted. The invalidating pair is therefore two identical model-outcome failures, as rule (c) intended.
3. **Repeated identical REFUSED or BLOCKED** (a deterministic gate or code refusal, not physics). The call is **held**. Root fixes the cause by a reviewed successor or procedure and reruns. It becomes UNEVALUATED only at the schedule ceiling.
4. **Rerun form.** Solo. Caps escalate after CAP ends (A244). After other non-physics ends the caps of the interrupted attempt are kept. Attempt numbering follows D6.
5. **The schedule ceiling** (A244 item 3) is the only stop. Its disposition is UNEVALUATED_CAP_BUDGET, renamed UNEVALUATED_SCHEDULE_CEILING, which covers all non-physics classes. It is disclosed, FREEZE_INCOMPLETE, and never MEMBER_INVALID.
6. **Interim.** Until each path carries this rule in code, root applies it by hand and records each rerun in V006.

## A246: arbitrary wall-time caps are removed as a run-ending mechanism; a stall watch and an individual root decision replace them (principal's direction) (2026-10-21 09:01:48Z)

**Principal (verbatim):** "Let's also review the code and see if we can get rid of arbitrary time limits. If something appears stalled we can always make an individual call on whether to terminate the run."

**Ruling** (registered before any NGC result is read; disclosed in the seal entry; extends A244/A245):
1. **No arbitrary wall cap ends a registered run.** On every path (the S0 kit, P-112, the direct batches including HEADLINE11, the W1 campaign waves, S1), each call's wall setting becomes the **schedule ceiling**: the time left before its phase's freeze deadline (A244 item 3). Where code needs a number, it gets that number. Where a code change would be needed, the setting is the largest value the code accepts, at most the ceiling.
2. **Kept as machine-safety limits, not scientific stops:**
   - **RSS at host RAM** (A166; the twin at RAM×11). This protects the host from swap collapse.
   - **The output cap** with the D9 free-space check. This protects the run volume from filling.

   Either one ending a run is non-physics (A245): the run is rerun, with escalation per A244.
3. **Kept by design:** the identity twin's planned stop (A141 L4). It is a designed truncation, not a timeout.
4. **The stall watch.** Root watches each running call using non-content signals only:
   - (a) the process CPU time, from `ps`;
   - (b) stage-directory **names and mtimes**, never their contents, as for S4T. For NGC runs, names and mtimes only; outputs are never opened.
   - It alerts when CPU time stops growing for 2 h, or when no new stage directory appears within 3× the expected stage duration, taken from a finished sibling run (the A237 method).
5. **The individual decision.** On an alert, root inspects the non-content signals and decides whether to stop the run. The decision and its evidence go in V006 before the stop.
   - A root stop is a non-physics end under A245: the call is rerun solo with the same settings.
   - The principal is told of every stop.
   - **No stop is ever made on the basis of any output value.**
6. **Dependencies to re-rule after Codex1's audit** (0796/0797, scope widened by 0799):
   - the orphan wait (wall + 600 s);
   - the W1 wall rule (A140 N4, A204), as scheduler slot accounting;
   - the rule-(c) "doubled wall" checks in builder c2v007 and P-112;
   - the S0 kit's constant caps;
   - DBP C2V004B's caps;
   - the parent orchestrator's per-call wall;
   - root_monitor's handling of very large walls.
7. **Interim.** Until each path carries this rule, root sets the wall at the schedule ceiling at launch, where the path takes the cap from config. Where a cap is fixed in code, root does not let it end a run unreviewed: a cap end is rerun under A244/A245, and the next launch uses the ceiling.

## A247: HEADLINE11 duration corrected from about 3 days to about 1 day (E_A192_H11); targets move about 1 day earlier if the drive is mounted Fri 23 evening (2026-10-21 09:04:20Z)

**Finding** (code and measured basis).
- launcher015 L115-117 admits a new call when `active_route_a < max_active`, where `active_route_a = sum(not item['route_a_finished'] for item in active)`. **max_active counts only calls still in route A.**
- Route A is about 1.4 h of an about 17.6 h C4T-class call (C4T R2 stage times: route_a 03:37 to tail manifest 04:59).
- So HEADLINE11's 11 calls ramp in over about 5 h (about 11/3 × 1.4 h, one start per 60 s poll, after the predecessor's first route-A iteration), then run concurrently.
- **Measured basis:** step-2 R2 ran 10 C-cases concurrently, at 16.3-20.1 h each (C4T 17.6 h, A204).
- **HEADLINE11 is therefore about 5 h + about 18-20 h, about 24 h. It is not "4 rounds × 18 h at 3 concurrent" (A192 L2362, carried into A201 and A224).**
- **E_A192_H11:** max_active was read as total concurrency. Rule: a schedule estimate cites the admission code it depends on.

**New targets** (steps.tsv; previous targets kept as a copy):
| Step | Target |
|---|---|
| S4, HEADLINE11 + S0 | Thu 22 to Fri 23 |
| S5, W1 launch | **Sat 24, if the campaign volume is mounted by Fri 23 evening**; otherwise Sun 25 |
| S6, waves to u_A | about Wed 28 to Thu 29 |
| S9, Phase-1 NGC | about Fri 30 to Mon 2 |
| **S10, Phase-1 score** | **about Sun 1 Nov (CST), range Thu 29 Oct to Wed 4 Nov**, conditional on the Friday mount |

**Still UNTESTED:** HEADLINE11 per-call time under 11-way contention plus the S0 serials. The deciding test is the first HEADLINE11 receipts.

**The W1 gate on the drive.** The W1 config, cache id and certificate_ledger path, and Codex3's campaign policy review, all need the volume mounted. With the volume on Friday, root builds the W1 config and Codex3 signs Fri to Sat.

**Also commissioned (0801):** Codex1 drafts root's verdict-day command sheet, after its cap audit. It is read-only and lists the exact commands with pins. That cuts Thursday's verdict-to-launch time.

## A248: triage of Codex1's cap and interruption audit (0169: FAIL, 6 conformance blockers); the phase ceilings are defined; implementation is ordered (2026-10-21 09:16:15Z)

**Audit:** `cap_audit_cx1/CAP_AUDIT_CX1V001.md` `1b7586bc`, JSON `9aee5e6a`, driver vocabulary `483e8ffd`. These are implementation-conformance blockers against A244-A246, not scientific findings. The existing tools predate those rules.

**Rulings.**
1. **Phase ceilings** (CAP-05; A244 item 3, A246 item 1):
   - **Phase-1 ceiling:** Thu 5-Nov 23:59 CST, the high end of the A247 range. A call not finished by then reads UNEVALUATED_SCHEDULE_CEILING in Phase 1 (FREEZE_INCOMPLETE, disclosed). It keeps running for Phase 2.
   - **Phase-2 ceiling:** Mon 30-Nov 23:59 CST.
   - **W1-and-wave ceilings** follow Phase 1's.
   - A133's dates are estimates, not registered bounds (A133 L23-29).
2. **The model-outcome list** (CAP-04; A245 item 2(a)), conservative until a reviewed vocabulary exists:
   - **counted model outcomes:** ROUTE_A_NO_FIXED_POINT, and a clean ITERATION_BUDGET_EXHAUSTED under the unchanged scientific iteration budget;
   - **uncounted:** every other FAILED or FAILED_AT_STAGE, including FAILED_SOURCE_PREPARATION and generic ValueError, until their exception origin is reviewed;
   - **uncounted:** any end whose cause the records cannot authenticate. The monitor does not hash finish or stderr, so the default is uncounted, which means a rerun.
3. **HEADLINE11 at the verdict** (direct batch, CAP-05). The DBP wall of 100,800 s (28 h) stays for the first attempts. That is generous against about 18-24 h. If a call ends at that cap, root reruns it under A245 at the Phase-1 ceiling. A DBP successor with ceiling-sized walls is not built before the verdict, because it would need a review on the critical path.
4. **The S0 kit** (CAP-01). Its fixed walls (serial 7.06 d, twin 6.3 h, the twin's planned design) stay for first attempts. Reruns go through P-112 under A244-A246 (D6). A twin STOPPED_* counts as a planned stop only with the bound watch's evidence (the S0_SHELL_WATCH note).
5. **P-112** (CAP-02): **cx2v004 implements A244-A246 and the twin-stop evidence rule. Codex2 builds it first, before c2v007**, so that Claude4's review (after Fri 19:00Z) is of cx2v004 (0802).
6. **Builder c2v007** (CAP-03) is being built to A244-A246 (0798, 0800).
7. **H3 acceptance** (CAP-06). A non-physics interruption that consumes an acceptance pass does not count toward MAX_PASSES. Root records it in V006 and reruns with a fresh pass through `h3_accept_call` (the A196 operating rule), never `resolve --invalid`.
8. **Stall watch** (A246 item 4). Root implements it as a light root script (process-tree CPU time plus stage-directory names and mtimes) before the first launch. It alerts root and makes no automatic stops.
9. **Codex1's verdict-day sheet (0801)** carries these rulings.

## A249: P-112 cx2v004 interface rulings (Codex2 0556). The wall is the Phase-2 ceiling; a value-free cause producer keeps model failures countable (integrity guard) (2026-10-21 09:20:39Z)

1. **Wall interface.** cx2v004 passes the monitor the **time remaining to the Phase-2 ceiling** (Mon 30-Nov 23:59 CST).
   - **The Phase-1 ceiling** (Thu 5-Nov 23:59 CST) is a reporting and freeze boundary only. No stop happens there.
   - No monitor successor is needed. The pinned root_monitor is unchanged, and its wall ends a run only at the Phase-2 ceiling.
2. **Integrity guard, the reason for this ruling.** If no failure cause could ever be authenticated, a genuinely non-converging model call would be rerun until the ceiling and read UNEVALUATED (FREEZE_INCOMPLETE) instead of MEMBER_INVALID. That would quietly excuse model failures and bias the score toward the model. A245 item 2 must therefore stay usable.
3. **The value-free cause producer** (`cause_record_c2v001`):
   - **What it reads.** Root runs it after a FAILED-class end. It reads only whitelisted metadata: the driver finish record's `status`, the failing stage name, the failure code, and the exception class with its raising file:line. **It never reads any value, array, row or prediction.** It binds its record to the monitor receipt's result and finish shas.
   - **Who builds it.** Codex1 (0805). It is single-read. Root verifies it after the Thu reset, and Codex3 reviews it, which is distinct from the builder.
   - **What counts.** P-112 cx2v004 and builder c2v007 count a FAILED end only with a matching pair of cause records that name a listed model outcome (A248 item 2).
4. **Interim, until the producer is adopted.**
   - FAILED ends are rerun and not counted.
   - If two consecutive solo attempts end with an identical raw status, the call is **HELD_FOR_CAUSE**. It is not counted, not rerun and not UNEVALUATED. Root then classifies it with the producer once the producer is adopted.
   - So no failure is excused without a cause decision.
5. **P-112 opens no run contents** (Codex2's guard is unchanged). Only root's reviewed producer reads the whitelisted metadata.

## A250: the stall watch is implemented (A246 item 4, A248 item 8), and the verdict-day command sheet is ready (Codex1 0170) (2026-10-21 09:23:54Z)

**Stall watch:** `CLAUDE2/STALL_WATCH/stall_watch_c2v001.py` **a9d724fc7051d29e** (the full sha is in the file listing). It alerts only and never stops anything.
- **Signals** (non-content):
  - the summed CPU time of the **driver's** process group, from `ps -A -o pgid=,time=`;
  - the names and mtimes of `<outdir>/stages` entries, never opened.
- **Alerts:** CPU_STALL, when there is no CPU growth for 2 h; STAGE_SLOW, when a stage runs longer than 3 × its expected duration, for stage-name prefixes given in a JSON taken from a finished sibling run.
- **Watch the driver's group, not the monitor's.** root_monitor starts the driver in a new session: for S4T R3 the monitor is pgid 99575 and the driver is pgid 99578. The driver's pgid is `child_pid` in `.launch.json`. At launch, root reads only that top-level field.
- **Smoke test** on S4T R3 (pgid 99578): stage 16_le2_columns_00 was detected and the CPU sum read. No alert, as expected.
- **No sibling durations exist for the NGC S0 runs yet.** They are watched on CPU only until the first S0 stages finish.

**Verdict-day command sheet:** Codex1 `verdict_day_sheet_cx1/VERDICT_DAY_COMMAND_SHEET_CX1V001.md` `f2a5eec4` and input pins `18e8487f`. PASS, 0 blocking. It checks 34 existing input hashes and the sealed-tuple AST constants, and carries the A218, A248 and A249 rulings. Its order is bind, then START snapshot, then launch.
- **UNTESTED:** every command, since the verdict and its pins do not exist yet.
- Root runs it at the S4T receipt.

## A251: the cause-producer interface is ruled (Codex1 0171). Exact scalar metadata from the monitor-pinned result; no NGC read before the seal (2026-10-21 09:27:03Z)

**Codex1 0171 (FAIL, 1 interface question).**
- The monitor (`ba031c23` L177-199) pins `result.path`/`sha256` and `driver_status`, but not the finish.
- The finish (NGC `577f8c94` L9101; DDO `b5cc62af` L3596) carries `status`, `result_path`, `result_sha256` and `reasons` (strings). It has no structured stage, code, class or site.
- The result carries `route_a_outcome` and `stage_records`.
- The isolated metadata reader is built: 16/16 tests, 4/4 mutants, single-read across inode aliases (`metadata_selector_cx1v001.py` `59e0fe75`).

**Ruling.**
1. **Allowed reads.** The producer may read **exact whitelisted scalar paths** from the monitor-pinned result:
   - the status fields;
   - `route_a_outcome`;
   - `stage_records[*].{name, status, exit_code}`.

   It never reads arrays, objects or numeric values, and skipped content is never decoded.
2. **The finish is authenticated** by matching its `result_path`, `result_sha256` and `status` against the monitor receipt.
3. **The raise site is derived from the pinned driver code.** The status or outcome token must map to a **unique** assignment site in Codex1's vocabulary. A token with no site, or with more than one, is not authenticated, so it is uncounted.
4. **`reasons`** (free text) and stderr are excluded.
5. **Positive model outcomes, the only ones:**
   - the driver status ROUTE_A_NO_FIXED_POINT;
   - the `route_a_outcome` token ITERATION_BUDGET_EXHAUSTED, under the unchanged iteration budget.

   Each counts only if its site is unique.
6. **Blinding.** For the **NGC** runs (S0 and the Phase-1 NGC set) the producer runs **only after the seal**. Before the seal, NGC FAILED ends follow the A249 interim: they are rerun uncounted, or HELD_FOR_CAUSE. DDO runs (HEADLINE11, W1, S1) may be classified at once.
7. **No driver or monitor successor** is needed for Phase 1. A structured cause record emitted by the driver is a Phase-2 improvement.

## A252: the cause producer's site rule is refined from "unique site" to "every site is a model outcome" (Codex1 0172) (2026-10-21 09:35:25Z)

**Codex1 0172 (FAIL, 1 blocking item, A251_COUNTABILITY).** The producer passes 37 synthetic checks and 5/5 mutants, and is single-read across aliases. But in the pinned drivers:
- ROUTE_A_NO_FIXED_POINT has **four** assignment sites in the NGC driver;
- ITERATION_BUDGET_EXHAUSTED has **zero** sites in either pinned driver.

So under the literal A251 rule, nothing is countable.

**Ruling, which replaces A251 item 3.**
1. **The site set.** The set of assignment sites for a token is collected across the pinned driver **and every module it loads by pin** (for example the route-A controller `route_a_uv_tail_controller_c2v001_r5` `c5bdd055` and the coupled-HI iterators). Each module is listed with its sha.
2. **When a token counts.** It is authenticated as a model outcome **only if the site set is non-empty and every site is classified as a model outcome** (non-convergence or no fixed point, under the unchanged scientific budget) in the reviewed vocabulary. A set with any non-physics site, or an empty set, is unauthenticated: uncounted, or HELD_FOR_CAUSE.
3. **Integrity reason.** The aim of A251 item 3 was that a counted token could arise only from a model outcome. Uniqueness is not needed when every possible origin is a model outcome.
4. **Deliverables from Codex1:** the vocabulary extended to the pinned loaded modules, and the producer updated (cxv002) with tests for the multi-site all-model case, a mixed-site set and an empty set. Codex3 reviews it, and root verifies it after the Thu reset.

## A253: the incomplete Phase-1 freeze interface is adopted as Codex2 proposed (0559) (2026-10-21 09:57:49Z)

**Ruling.** Builder c2v007 and its G26 freeze path use a root-gated, value-free **Phase-1 ceiling snapshot**. It pins:
- the verified complete planned call set from the P-112 config;
- the existing launch and closed-receipt custody records;
- the incomplete state of each remaining call.

No attempt or receipt is fabricated, and a missing mounted volume still refuses.

**Rules:**
- The call registry includes planned calls that never launched.
- The builder verifies the saved snapshot and its pinned sources. Later Phase-2 files never change Phase-1 evidence.
- A schedule-ceiling closure is keyed by the registered call, and its last receipt may be null.
- **Cutoff T:**
  - if every call is terminal before the Phase-1 ceiling, T is the latest terminal `time_utc` (A223 G24);
  - otherwise T is **the Phase-1 ceiling** (Thu 5-Nov 23:59 CST, A248).
  - The record's later creation time is kept separately.
- **The snapshot is taken only when it is needed:** at the ceiling with calls still incomplete, or at the ordinary freeze with every call terminal. It is never taken early.

## A254: parallelism audit (principal: "the most parallel work as possible consistent of course with quality") (UTC 2026-10-21 11:25:38Z)

Root audited the critical path for parallel slack. Findings:
1. **Compute before the verdict:** none can start. S0 needs the T0/V007 pins (E_A187_1). HEADLINE11 already overlaps all 11 calls (A247). S4T R3 is the only physics compute it can run.
2. **Waves:** W1→W2→march0 are sequential by construction, because each wave's points depend on the previous wave's results. W1 is gated by the drive (Fri evening mount → Sat W1).
3. **Build and review:** every Phase-1 build is done and reviewed. The cross-family verifies run on Claude3 in parallel (0813/0814). Root adoptions follow the Thu 18:00Z reset.
4. **One candidate gap:** per-wave CP-1 ledger certification (about 0.5 d per wave) could run now on the idle host, **if** a future wave's points are fixed before any campaign result. Codex1 is checking this read-only (0815). If they are determinate, root runs the CP-1 list certificates now, Codex3 signs the EPS reviews, and only the ledger append remains at wave time. If they are not, nothing changes.

No physics change; quality gates unchanged.

## A255: four acceleration levers commissioned (principal: "Please proceed to find and implement any parallel processing that might speed up the plan") (UTC 2026-10-21 11:38:53Z)

Codex1's 0177 (0815) found that the 3 nominal W3 Jacobian-minus points are fixed in advance on the expected path (seed and three plus valid). March0 and later are not. Root commissions four levers. Each is adopted only with a FORMAL proof from code that values and the engine's path are unchanged. Any lever that changes physics or custody is a FAIL, not a trade-off.

| Lever | Step | Saving (UNTESTED) | Owner | PLAN |
|---|---|---|---|---|
| L1. Pre-certify the 3 W3-minus points now (CP-1 on the idle host, `taskpolicy -b`) | S6 | about 0.5 d at W3; required by L2 | root; binding check wf_5a044dd0 (Claude lineage) | P-127 |
| L2. Concurrent Jacobian: W1 seed + W2 plus + W3 minus launched together, consumed by the engine as cache hits | S6 | about two wave times | Codex1 0816 design; Claude-lineage adversarial check before adoption | P-128 |
| L3. W1 on internal disk or External1 before the new drive | S5 | about 12–18 h (W1 Fri morning, after HEADLINE11 evidence) | Codex3 0817 (A) | P-129 |
| L4. Phase-1 NGC route A at column_workers 8 once S0's twin identity is TESTED | S9 | S9 wall, to be estimated | Codex3 0817 (B) | P-130 |

**Already maximal, recorded in A254:** the step-2 wait, HEADLINE11's full overlap, and S8 alongside S9.

**Discard rule (L1, L2):** a result computed early is used only where the engine requests that exact identity. Otherwise it is preserved and never used.

## A256: L3 ruled out on custody; W1 pre-staged to launch at drive mount; L4 gated on an S9 makespan estimate (UTC 2026-10-21 11:48:07Z)

**L3 (W1 before the drive): RULED OUT.** Codex3's 0674 (LANE_A_CX3V001 `b393ddba`), FORMAL:
- The campaign binds its resolved path, volume UUID, work-dir inode, ledger path and cache identity, and `storage_check move` refuses the work dir. A campaign started on internal disk cannot move to the new drive later.
- Seven concurrent calls exceed the internal budget by 21.84 GiB.
- The only compliant alternative is External1 permanently. Its fit depends on b, which is not measured until calls are accepted: at 57.19 GiB per call the campaign exceeds External1 entirely, and even at 16.24 GiB per call about 508 GiB of other data would have to be moved off it.
- A campaign that can run out of room with no migration path is a non-physics interruption risk, and the gain was about 12–18 h. Root declines it.

**Replacement (scheduling only): W1 launches at drive mount.** Root writes every part of the W1 record that does not depend on the volume (config, ledger, wall rule and the HEADLINE11 evidence apply) before the drive arrives. W1 then launches as soon as the mounted volume passes the storage check, at night if need be, instead of the next morning. S5's target becomes Fri night. P-129 now carries this.

**L4 (cw8 Phase-1): license confirmed; build gated.** Codex3's 0675 (LANE_B_CX3V001 `20ff14c5`), FORMAL:
- A133 §1.4 and r3a I-6 license member and F calls at cw8 after the pinned comparator reads byte-equal at iterations [0,1] (`--iterations 2`).
- P112 cx2v004 refuses cw8 (SPEC_LEAF). The closure needs a selector, a P112 successor, possibly a G3 equivalence key, consumer checks, adversarial tests and a distinct review.
- Per call (corrected RI45-12): E 31.90 → 21.58 h, U 84.77 → 51.85 h.
- The S9 makespan gain is UNTESTED, and concurrent serials can beat cw8 on throughput.
- Root commissions the build only if the best cw1/cw8 mix saves at least 0.5 d (E) on S9 (Codex3 0818).

**Erratum noted (Codex3):** A166 removed the 83.7 > 83 GB gate classes. The twin's 22,752 s is twice the modeled 3.16 h prefix, not a measured time. A255's L3/L4 rows are superseded by this entry.

## A257: L1 adopted. Root runs the CP-1 list certification of the 3 nominal W3-minus points now; scope recorded before launch (UTC 2026-10-21 11:53:32Z)

**Evidence.** Root workflow wf_5a044dd0 (Claude lineage, cross-family to Codex1's 0177):
- **Binding trace: BINDS_AFTER_REBIND_WITHOUT_RECOMPUTE.** The CP-1 numerics, EPS/GQ/ρ proofs, slot proofs and bundles are identity- and custody-bound. Identity and custody are slot-free (core r10 L233-238; custody_cx2v002 L103-141), so all of them carry over to production.
  - Only `pending_spec_sha256` differs: production fills the slots with C4T's FILLED de6d7d77 pins.
  - The wrapper's ledger_append compares it (c2v004 L723-725), so the draft records would refuse.
  - **At W3:** run the production `points-manifest`, rerun assembler `records` from the existing bundles (c2v001 L57-112 never ties a bundle to its list), then `verify`, then `ledger-append`. No new tooling and no recompute.
- **Adversarial check: NOT REFUTED.** Twelve non-blocking caveats:
  - the minus derivation was re-derived (TESTED, exact mirror of the plus points);
  - blinding: the ρ stage is DDO154-only (FORMAL);
  - identity is stable through apply_h3_fields_c2v006's strip_slots guard;
  - S4T contention: background QoS, at most 3 single-BLAS workers;
  - the saving holds only if the seed and all three nominal plus calls are VALID, otherwise W3 needs halved-plus points and the saving is about 0.

**Scope (stated before launch):**
- List: Codex1 `NOMINAL_W3_MINUS_DRAFT/POINTS_LIST.json` `9cfa8787…`, keys 06c3e863…, plus the two other rows 301-302 in that list. Draft provenance is disclosed: cache_id SYNTHETIC; the loader reads only `wave` and `points`.
- Compute-only claim. Certificate readings are never used to choose points. A result is used only if production `points-manifest` requests the identical identity at W3. Otherwise it is preserved and never used.
- Out-root: `s4rc1_c3/cp1_run_c3v004b`. Its anchor is P01 8ad6ca4e: ANCHOR_EPS_CROSSCHECK verdict AGREE (max_rel 1.62e-08, tolerance 1e-3), with STAGE_CONTEXT present.
- Command: README_CAMPAIGN_CERT_C2V001 §3 form.
  - `taskpolicy -b`, `--operator-lane Claude2`, `--max-concurrent 3`.
  - `--allow-rho` with the rows 1-31 proof-side review pin: Codex1 0146 `66c54c76…`.
  - margin and floors as in the 31-point run (A166).
- **Next, off the critical path:** Codex3 signs EPS per point (A202 item 1, standing), then root's adapt-eps under the draft list.
  - List-mode ρ registration and slot-proof staging: the 31-row root tooling cannot do it. A small reviewed list-mode staging procedure comes before the bundles.
- **Do not append now** (no work dir; the shas differ). At W3: the rebind route above.
- S4T R3 keeps priority. If it enters a heavy multi-worker stage, root uses the runner's `--hold-file`.

## A258: the objective is the shortest wall clock to the result, even at more total compute; the CP-1 hedge on both conditional pools runs now; cw8 is not commissioned (UTC 2026-10-21 11:57:53Z)

**The principal (verbatim):**
- "We are very lightly using the CPU right now. If we can accelerate the schedule by letting the mac do some resource management we should do that."
- "The key thing we're talking about is the quickest path to finishing even if there is more total processing."

**Standing rule (root):**
1. The objective is the wall-clock time to the PROVISIONAL score, and then to the score of record. Extra compute is acceptable whenever it can shorten the wall clock.
2. Compute that might be needed runs early, under the discard rule (A255): a result is used only if the engine or roster requests that exact identity. Otherwise it is preserved and never used.
3. macOS does the resource management. Critical-path runs (S4T R3, HEADLINE11, S0, campaign calls, Phase-1) run at default priority. Hedge work runs under `taskpolicy -b`, so the OS gives it idle cores and yields them to the critical path. There are no self-imposed concurrency throttles beyond the sealed launch rules.
4. Physics, custody and blinding are unchanged (A187, A246).

**Now: CP-1 hedge on both conditional pools** (Codex1 0177; scope as A257):
- `CONDITIONAL_HALVINGS_POOL_DRAFT` `583ab18d…`: 12 points, rows 400-411. Root checked the offsets: each differs from the seed in exactly one leaf, at a half or quarter of the nominal step, on both sides.
- `CONDITIONAL_GLOBAL_POOL_DRAFT` `5b4255bb…`: 12 Halton points, rows 500-511.
- Same out-root `cp1_run_c3v004b`, the same ρ gate pin (0146) and `taskpolicy -b`.
- EPS reviews: the nominal minus first, then the halvings, then global. The pools are signed proactively, so that a branch to them waits on no review.

**cw8 (L4): not commissioned.** Codex3's 0677 (S9_MAKESPAN_CX3V002 `82b906ba`):
- On the expected path, Phase-1 has 4-7 calls, 4 of them reused from S0, so 0-3 calls are new.
- The best saving is 4.48 h E / 15.40 h U, and 0 if only 12-14 cores are free.
- S8's two DDO calls each keep 8 route-A workers.
- A new launcher and custody closure on the scoring path carries more schedule risk than the gain it buys. Root revisits this only if u_A's branch gives many new calls with idle cores.

**Extended to Codex1 (0820):** the concurrent Jacobian (0816) is to cover the earliest compliant start: alongside HEADLINE11 at the verdict, not after its evidence, with speculative branch calls if they are allowed.

## A259: cw8 Phase-1 path commissioned (A258's "not commissioned" is reversed); hedge runs launched (UTC 2026-10-21 11:59:21Z)

**The principal (verbatim):** "4-15 hours is a lot". "What risk are we talking about?"

**The risk, stated plainly:**
- **No physics risk beyond the sealed rules.** The sealed prereg r3a I-6 and A133 already accept the cw8 criterion: bitwise-equal iterations [0,1]. That is a registered, finite qualification, and it is not new.
- **The real risk is a defect in the new launcher or custody successor.** A bad binding of spec sha or worker role would make a Phase-1 call unacceptable and force a rerun, costing one call's duration, which is up to about 3.5 d at U.
- **Mitigations:**
  - an adversarial test suite;
  - a cross-family review by Claude3;
  - root verification;
  - serial is the automatic fallback: the selector keeps any call serial unless every pin authenticates.
- **Schedule risk:** if the build is not ready by u_A, the calls run serially as they do today. Nothing is lost.

**Ruling:** build the cw8 path (Codex3 0821; P-130).

**Hedge runs (A258), launched 11:58:22Z, background priority:**
- halvings: `SCHEDULER_20261021T115822Z_5276`, at most 8 at once;
- global: `SCHEDULER_20261021T115825Z_5293`, at most 6 at once.
- The W3-minus run (`…115353Z_4336`) continues.

**Codex1 0820** extends 0816 to the earliest compliant start (beside HEADLINE11 at the verdict) and to speculative halved-plus calls.

## A260: list ρ/slot helper adopted; cw8 RSS ruled; S4T R3 re-projected (UTC 2026-10-21 12:10:35Z)

**1. Adopted: `cp1_list_rho_slot_cx1v004.py` `820d16a5`** (Codex1 0178; 0819). It runs the list-mode ρ registration and the FILLED/SLOT_ARGS staging for all 27 list points.
- **Review:** Codex2's 0566, PASS with 0 blocking, 37/37 inert checks, at most one open per input (REVIEW_RESULT_CX2V001 `fc4e8c68`). Codex2 reviewed in place of Codex3 (0824), so Codex3 stays on the cw8 build. Codex2 is not the author.
- **Root verify:** the author suite re-ran 11/11 PASS (TEST_REPORT `75accfc6`). Production is UNTESTED until the real P300-P302 records exist.
- **Use:** README_CX1V004 commands, `register` then `stage`. Root reviews the registration record before pinning its sha into `stage`.

**2. cw8 RSS (Codex3 0679, DESIGN_CX3V001 `6dadfe86`): accepted as proposed.**
- A full cw8 member/F call's RSS cap is RAM × 11, the tree's maximum process count read from the driver bytes. That is A177's rule, as applied to the twin in A166 N4. A memory cap never kills an honest run.
- The cap is valid only under a root-pinned cw8 license record, never self-granted.
- Full calls use the Phase-2-ceiling wall (A246), with no twin name and no kill watcher.

**3. S4T R3 re-projected.** Stage birth times (names only):
- le1 columns 8.90 h (1.63× fs);
- le2 columns 8.28 h (1.52× fs);
- stage 17_le2_rotation began 12:08Z.

At C4T's remaining ratios (le3 1.27×, le4 1.11×, le5 1.11× of fs 5.45 h, about 20 min per level, about 1.5 h tail), the last receipt lands about **Thu 22 09:30–10:30Z (4:30–5:30 am CDT)**, range 3–6 am CDT (UNTESTED). That replaces the 2–3 am point estimate. S1's window holds, and the verdict-day sheet starts at the receipt.

## A261: the verdict-day sheet dry check PASSES with 0 blocking (Claude3 0262). N1 fixed now; the HEADLINE11 order is ruled (UTC 2026-10-21 12:23:27Z)

**Check:** Claude3's 0262 (`verify_c3_verdict_day_sheet/RESULT.json` `e3d9d321`) on sheet `f2a5eec4` and pins `18e8487f`.
- 34/34 pins agree in the JSON, the sheet and the bytes.
- All CLI flags across 18 tools match their argparse.
- The receipt keys exist.
- The sealed constants match.

**N1 (TESTED): would have stopped the sheet at §5.** `make_b1_cascade_c4v002 --write` calls `os.mkdir($C4/final/v006r11_c4)` (L196-197), but its parent `$C4/final` did not exist. **Fixed now:** root created the empty folder `b1_policy_successor_c4/final` as an exclusive create. No code or pinned file changed. The dry run is unaffected, because it never checks that the parent is absent.

**N2:** `calib_tail_readiness_cx2/v006r11_c4/` is created by the sheet itself (L109). It stays on the checklist.

**N3 (ruled, order on verdict day):** §8 FINAL specs → each HEADLINE11 spec's §7 driver dry plan → §9 (bind → envelope START → launch). The S0 dry plans stay where §7 puts them.

**N4:** a FINISHED receipt whose driver_status is `COMPLETED_INVALID` (driver r5 L3558, L3597) is a model outcome. Root classifies it under A245 and never retries it as an infrastructure fault.

**N5:** V005 (`c01b3c51`) must not be edited before §5. It is not edited.

## A262: L2 (concurrent Jacobian) design FAIL with 2 blockers, both buildable; the importer and the direct certificate lookup are commissioned (UTC 2026-10-21 12:28:27Z)

**Codex1's CONSOLIDATED_0816_0820_CX1V001 (`b272e1dc`): FAIL, 2 blocking.**
- **Engine invariance holds:** FORMAL, plus 30 TESTED branch comparisons. That covers invalid seed, invalid plus or minus, halvings and budgets. It holds **only for lazy import after genuine natural planning.** Bulk preloading changes the probe misses and the wave numbering, so it is forbidden.
- **B1:** the generated entry and wrapper (c2v004) cannot import direct-call results. They require the wave plan and the canonical wave call dir. No path exists today from External1 to the campaign.
- **B2:** the direct path builds certified specs only for genesis points. The W3-minus points are non-genesis. Throttles in the code (guard014 max_active ≤ 6 with a ramp; the campaign's process budget of 17, peak 8 per call) are implementation gaps under A258.
- **The five H11 evidence fields never enter a call spec (FORMAL).** Jacobian calls can therefore start without waiting for HEADLINE11's evidence, once their final certified specs and their admission exist.
- **Saving:** about 1–2 d (UNTESTED). Under fully saturated equal-work CPU, overlap alone adds nothing. The gain comes from W1's idle cores and the gaps between waves.

**Ruling: build both (S6, P-128):**
- **Codex1 (0827):** a request-driven importer that admits by reference, under the lock, with full provenance checks. It must answer first whether it can be adopted after the verdict-day generation without moving the cache identity.
- **Codex2 (0828):** a direct-path certificate lookup that produces the exact final spec bytes for non-genesis certified points. It must also answer whether guard014 admits six direct calls beside W1.
- **Review:** Claude3, cross-family. Claude3's 0826 item-2 check of the design itself runs in parallel. Target: review-ready by Fri Oct 23 12:00 CDT.
- **Plan if adopted:** W1 in the campaign plus W2 (genesis rows 29–31) and W3 minus as direct calls, all at drive mount Fri night. Each direct result is imported only when the natural wave requests it.

## A263: verdict-day execution order. Parallel branches adopted, the night review pre-arranged, QoS on verdict night (Claude3 0265) (UTC 2026-10-21 12:28:27Z)

**Parallel (adopted, FORMAL from sheet `f2a5eec4`):**
- **P1:** the §3 per-case gates (EA replay and ra10 HARMONICS × 10 labels) and MT/I1T/FLAG_RULINGS all run at once. Only the EA aggregate waits.
- **P2:** §5 (r11 policy) and §6 (the H3 r12 chain) run at the same time. §8 needs both.
- **P3:** the S0 chain (§7 S0 pins → dry plan → START → §11 seed) runs alongside the HEADLINE11 chain (§8 → §9–10). The twin comes only after the seed's confirmed LAUNCH (A166).
- **P4:** the §7 per-spec dry plans run in parallel.
- **Order inside the HEADLINE11 chain:** §8 → its dry plans → §9 (A261 N3).

**The night lane wait (W1):** Codex3's gating reviews of §5 and §6 are on HEADLINE11's path at about 4:30–7 am CDT.
- Root pre-arranges them (0829): Codex3 gets the expected diffs now, so the night review is a byte check. Codex1 is the fallback reviewer.
- The principal is asked to keep Codex3's and Codex1's sessions running overnight.

**S0 (W2):** S0's T0 pins wait on Codex3's §5/§6 review only if the S0 kit's fill consumes §5/§6 outputs. The kit's own dry verdict fails closed if one is missing. Otherwise S0 does not wait.

**QoS (A258):** the numerics are fixed by the single-thread environment, so on verdict night root drops `taskpolicy -b` and `nice -n 10` from the §3–§5 commands. The exception is any tool that checks its own QoS. Claude3's audit (0822) names those tools before Thu 03:00 CDT, and until then root keeps the flag wherever a tool checks for it.

**W3:** root pre-writes the verdict-day variable blocks as a template (R, PS, CASES, RESULT_MANIFEST and the rest) before Thu 03:00 CDT, to remove typing latency.

## A264: erratum E_0829_HEREDOC (UTC 2026-10-21 12:29:51Z)

Root wrote dispatch 0829 (`bdf4caa7`) with an unquoted heredoc. Two unescaped backtick tokens, `--dry-run` and `--write`, ran as command substitutions: they failed with "command not found" and expanded to empty text. The published bytes are kept unchanged, and erratum 0830 (`499f7f5c`) restores the wording.

**Checked:** the dispatches root wrote today, 0815 to 0828, contain no empty backtick pairs, and no other write raised the error.

**Rule:** in any root-written file, backticks inside an unquoted heredoc are escaped (\`), or the body goes through a quoted heredoc and the stamp is printed separately.

## A265: L2 integration findings. The c3v005 repin is a must-fix for every wave; guard overlap authorized as new files; the importer can be added after the verdict; erratum E_0829_V (UTC 2026-10-21 12:33:38Z)

**1. A latent stop on every campaign wave (Codex2 0568, FORMAL).** `cp1_points_assembler_c2v001` → `cp1_points_common_c2v001` → `registry_assembler_c3v004`. Its C1 policy gate rejects the three extra approved producers in frozen C1 `40159322`. Adopted c3v005 (`7df1c481`) carries the six-producer fix, but list mode still pins c3v004.
- Without a repin, list-mode `verify` would refuse at W3 and at every march0+ wave.
- **Ruling:** Codex2 ships a minimal list/common repin successor first, as its own unit (0831). Root adopts it after review. P-127 and S6 depend on it.

**2. guard014 does not admit W2/W3 direct calls beside a live W1 campaign** (`core_priority_admission` L326-352 admits `campaign_inactive=False` only for POST_S1). The limit is not max_active.
- **Ruling (A258):** a root-bound overlap admission for exactly the 6 Jacobian keys and the W1 work-dir identity, shipped as new guard, launcher and binder successors.
- The verdict-day HEADLINE11 pins (guard014 `6efdca01`, launcher015 `cd987edd`, binder c2v011) stay byte-identical.
- The ramp stays (about 1–2 h across six starts).

**3. Importer timing (Codex1 0179, EARLY_ADOPTION_ANSWER `d7573cae`, FORMAL; runtime UNTESTED).** A separately pinned supplemental entry/executor can be added **after** the verdict-day generation, with the wrapper unchanged. The wrapper's sha feeds cache_id. No verdict-day deadline applies.
- **Open:** the hook runs after a committed WAVE_PLAN under the lock; mixed-wave and resume semantics; the whole-engine replay. The build continues.

**4. Erratum E_0829_V.** 0829 said the §5 seal tuple is entirely sealed constants. It is not: V is `$VERDICT_SHA` (make_b1 `check_tuple` checks only V's form; `main` embeds all five elements). The §5 policy sha therefore depends on the verdict report.
- Codex3 (0682) pre-reviews a parameterized recipe instead. At the verdict, V is inserted and the published files are compared, so the review still takes minutes.
- The error is root's: it generalized from Claude3's check of the C/P/A/SCHEMA constants.

## A266: cause producer cxv002 ADOPTED, with a root rule for N1; cxv003 hardening commissioned (UTC 2026-10-21 12:34:17Z)

**Verify:** Claude3's 0266 is a cross-family PASS with 0 blocking (`verify_c3_cause_producer_cxv002/RESULT.json` `a6353ab0`). The object was unchanged throughout:
- producer `4271da44`;
- vocabulary `839c7577`;
- reader `86a71335`.

The fixtures match the real receipt, finish, result and stage schemas (TESTED from bytes). The vocabulary is complete for both drivers. On Claude3's copy, 43/43 tests pass and 7/7 mutants are killed. Together with Codex3's 0672 PASS and Codex1's 0173 build, this replaces root's own verify.

**Adopted:** `cause_record_cx1/cxv002/cause_record_cxv002.py` `4271da44` and CAUSE_VOCABULARY_CXV002 `839c7577` (P-126). It applies to every FAILED end under A245/A249/A251/A252.

**N1 (hardening; not reachable from the pinned drivers).** When the status is ROUTE_A_NO_FIXED_POINT, an absent, None or unknown `route_a_outcome.outcome` is counted as a model outcome (L81, L95-105).
- Every pinned iterator writes a known checkpoint outcome, so an honest record never reaches this.
- **Root rule until cxv003:** if a cause record reads model_outcome true with that outcome missing or unknown, root holds the end as HELD_FOR_CAUSE and uncounted (A248), and rules on it by hand. It is never counted automatically.
- **cxv003 (Codex1, low priority after 0827):** one line returning ROUTE_A_OUTCOME_MISSING_OR_UNKNOWN as uncounted. The positive fixture's `NONCONVERGENCE` is replaced with real iterator outcomes. Claude3 does a narrow verify, and root swaps the pin.

## A267: G26 verified, adoption tied to c2v007; G26's fixtures moved out of /tmp; review of the c3v005 repin routed (UTC 2026-10-21 12:37:37Z)

**G26 freeze script `663d4c2b`:** Claude3's 0267 is a cross-family PASS with 0 blocking (`verify_c3_g26/RESULT.json` `d44a69a2`).
- 47/47 checks and 13/13 mutants killed.
- The guards hold: the external NO_NEW_DISCREPANCY head, PASS_K byte-equality, and allow_incomplete re-derived from DN5.
- It reads each input once.
- **Adopted, conditional on the c2v007 verify (Claude3 4c).** G26 pins builder `799fb2d0`. If 4c changes the builder, G26 needs a successor.

**N1 (TESTED): G26's test evidence lived in /private/tmp.**
- The suite reads `scratchpad/c2v004_dryrun_final` in root's session scratch, and macOS clears /private/tmp on reboot.
- **Fixed now:** root made an exclusive copy to `claude_artifacts/g26_fixture_preserve_c2/c2v004_dryrun_final`: 20 files, MANIFEST_SHA256_C2V001 `39d7e512`, byte-identical to the source.
- A test successor that reads from there is queued to Codex2 (low priority).
- Root is scanning production tools for other /tmp dependencies.

**c3v005 list repin (Codex2 0570, unit 1):** built, 17/17. Routed to Claude3 for review now (0833), ahead of its remaining verifies.

## A268: KS3/KS4 successor cxv002 adopted; the verdict-night gating reviews are pre-staged (UTC 2026-10-21 12:39:31Z)

**KS successor cxv002** (Codex1 0168; A240/A241): Claude3's 0268 is a cross-family PASS with 0 blocking (`verify_c3_ks_successor/RESULT.json` `a49270ef`).
- **AST delta (TESTED):** common changes only PINS and CANONICAL_APPROVED_PRODUCERS_S1. The assembler changes only COMMON_PATH, COMMON_SHA and `c1_policy_gate`.
- The S1 six are A240's, in order. The A241 single read is as ruled. Builder tests: 6/6, 8/8, 6/6.
- **Adopted (S8, P-121).**
- **Root rule (N1):** the gate checks membership only, so the S1 C1 freeze binds A240's exact ordered six (G4, G3, G1, KS6′ LO, G2 SRB_ROT, G6b).

**Verdict-night gating reviews are pre-staged (Codex3 0683/0684; A263 W1):**
- **§5:** the parameterized r11 policy recipe. It is the r10 baseline with only line 13 (the registration comment) and line 16 (the tuple) changed, and it reconstructs r10 exactly (`93d9c0ac`).
  - The checker is `check_verdict_gates_cx3v003.py` `78358dac` (45 control checks).
  - It hashes the root-named report, reads only the seven authorized fields, refuses any reading other than sealed ADOPT_TAIL, and requires exact bytes.
  - V (the verdict report sha) is inserted at the verdict.
- **§6:** the permitted bytes against the r12 placeholders: policy L13 and L16, core L202 (the policy sha), wrapper L29 (the core sha) and entry L61 (the wrapper sha). Everything else is byte-identical, and the comparison is on complete expected bytes.
- **Result:** at the verdict, each gating review is a run of that checker, a matter of minutes.

## A269: c3v005 list repin ADOPTED. Every list-mode assembler step now uses cx2v002 (UTC 2026-10-21 12:42:17Z)

**Verify:** Claude3's 0269 is a PASS with 0 blocking (`verify_c3_list_repin_cx2v002/RESULT.json` `62c53524`).
- The delta is exact: common's ASSEMBLER moves to c3v005 `7df1c481`, and the assembler's COMMON2 moves to `65859327`.
- The runner is unchanged (`3f5e5c18`, `53f10e6e`).
- C1 `40159322`'s six producers verify. The old chain refuses exactly the three added producers.
- No HEADLINE11 file was touched, and 17/17 tests pass.

**Adopted:**
- `direct_cert_lookup_cx2/cp1_points_common_cx2v002.py` `65859327`
- `direct_cert_lookup_cx2/cp1_points_assembler_cx2v002.py` `1b701591`

**Rule:**
- For every CP-1 list point (W3, march0+, and the 27 points now running), root runs `bundle`, `records` and `verify` with **assembler cx2v002**.
- The runner stays `cp1_points_runner_c2v001`.
- The bundle commands printed by `cp1_list_rho_slot_cx1v004` name the c2v001 assembler path. Root substitutes the cx2v002 path and sha, and all other arguments stay as printed.
- README_CAMPAIGN_CERT_C2V001 §3 and the A257 W3 rebind route are read with that substitution.

## A270: P112 cx2v004 verify FAIL (F1: the Phase-1 ceiling refuses Phase-2 reruns); root rulings; the fix is folded into the cw8 package v002 (UTC 2026-10-21 12:51:14Z)

**Claude3's 0270** (`verify_c3_p112_cx2v004/RESULT.json` `a1c4eab1`) is a FAIL with 1 blocking. 221/221 tests pass and 21/21 mutants are killed. Walls, the counted list, holds, gates and the single-read rule are all confirmed.

**F1 (blocking, TESTED).**
- `next_attempt` (L518), `fresh_launch_plan` (L2684) and the commit check (L2720) refuse every new attempt after the Phase-1 ceiling, 2026-11-06T05:59Z.
- That contradicts A249 item 1 ("a reporting and freeze boundary only. No stop happens there"), A248, A245 item 5 and G25 (P-112 owns every later attempt).
- **Effect:** a model failure after Nov 6 cannot get its solo confirmation rerun, so it can never be counted. That is the asymmetry A249 item 2 forbids.
- It bites only after Nov 6, and S9 (about Oct 26–Nov 2) is unaffected before then.

**Root rulings:**
1. **F1:** the Phase-2 ceiling wall (A246) is the only stop for attempts and reruns. The Phase-1 cutoff stays only in `phase_disposition` and `terminal_set`, for reporting and freeze.
   - **First admissions after Nov 6 are allowed:** Phase 2 runs the full step-5 set (A133).
   - The two builder tests that encode the old behavior are inverted.
2. **F2:** in `status`, the hold checks run before the ceiling reading. A held call is never shown as UNEVALUATED (A249 item 4).
3. **F3:** a cause record with model_outcome false and a reason outside KNOWN_NONPHYSICS_CAUSES (for example STATUS_NOT_MODEL_FAILURE, or NGC_POST_SEAL_ATTESTATION_REQUIRED before the seal) is **uncounted and eligible for a solo rerun.** It does not stall as HELD_FOR_CAUSE.
   - The record is kept, and the end is classified once its cause can be read: after the seal (A252) for NGC.
   - A rerun never counts anything by itself. A rerun that reproduces identically, together with a cause read after the seal, decides the count (A245).
4. **F4/F5:** noted. Cause-record custody is root trust.

**Route.** Codex3's cw8 package (0685) contains a P112 successor built on cx2v004, so it inherits F1.
- **Codex3 makes v002 with F1–F3 fixed (0835).** Its selector already gives a durable serial fallback, so v002 becomes **the single Phase-1/2 launcher** (cw1 or cw8 by role). cx2v004 is not adopted.
- **Claude3 reviews v002** in place of v001 (0834 retargeted).
- **Fallback:** if v002 fails review, Codex2 builds a serial-only cx2v005 with the same fixes after its L2 units.
- **Deadline:** adopted before u_A for S9's launches. The F1 fix is a hard requirement before 2026-11-06T05:59Z.

## A271: L2 design check PASSES; a direct-route variant is preferred; the HEADLINE11 28 h wall is to be raised; cx2v004 adopted until Nov 6 (UTC 2026-10-21 12:53:27Z)

**1. The L2 design check PASSES (Claude3 0271, `verify_c3_concurrent_jacobian/RESULT.json` `9a16c77b`).**
- Invariance holds in 108/108 synthetic Probe cases, using the real Probe AST and engine functions, **with lazy import.** Bulk preloading changes the wave plan in 54/54 cases, so it stays forbidden (A262).
- Codex1's FAIL is confirmed: the route cannot run on today's tools.
- **Preferred variant (Claude3):** run the 7 Jacobian calls on the **direct route, on External1, as soon as H11 ends**, before the drive mount. Import each lazily once the campaign is initialized on the new drive. If all are valid, that saves about 2–3 waves of T (T is 16.3–20.1 h).
- This needs both successors: the importer (0827) and the direct admission plus certificate lookup (0828 units 2-3). Their inputs for the build:
  - N3: launcher015 takes the machine flock, so the 7 calls form one batch after H11.
  - N6: bind the environment identity.
  - N7: single read, an A226 envelope, a register of speculative calls under the discard rule, and a layout adapter.
  - N9: the scheduler's 5-of-7 weights.
- External1 has 2,877 GiB free (Codex3 0674), and seven 80 GiB caps plus 20 GiB is 580 GiB.

**2. The HEADLINE11 28 h wall.** The sheet keeps DBP wall 100,800 s for H11 first attempts (A248 exception). With 11 calls overlapping and S0 alongside, the margin is thin, and a CAP stop would put about a day onto H11's evidence.
- **Ruling (A246 + A258):** raise it to the time remaining to the Phase-2 ceiling, through the smallest compliant change (ideally data-only), with an exact sheet amendment.
- Claude3 builds it, with a narrow review (0836), due Thu 03:00 CDT.
- **Fallback:** 100,800 s with the A244 rerun.
- **The S0 twin:** if it is cut before iteration 1, root reruns it after H11 (planned and uncounted).

**3. Correction to A270:** the verdict-day sheet's cap reruns use P112 cx2v004 (sheet L8), and F1 bites only after 2026-11-06T05:59Z.
- **cx2v004 `8cec1b56` is adopted for use before the Phase-1 ceiling.**
- The cw8 package v002 (0835) replaces it once v002 is adopted, and v002 must be adopted before the ceiling.
- The TOOL_PIN line is P112_LAUNCHER_CX2V004, with a sunset at 2026-11-06T05:59Z.

## A272: the missing-folder scan of every remaining runbook found 3 more hard stops on verdict day, all fixed now; the verdict-day folders are pre-created; the variable template is written (UTC 2026-10-21 12:58:24Z)

**The principal:** "Can we run a scan to make sure that we don't have that missing folder issue anywhere else."

**Scan:** root workflow wf_fa4a29f1, 8 agents. Four group scanners each checked every write target against the tool's source and the current filesystem: the verdict day; the campaign plus the CP-1 list and W3 route; Phase-1 S0/S9/S10; and the seal, S8 and Phase 2. An adversarial verifier then checked each group.
- 132 targets were checked OK. 51 findings were raised, 50 of them **confirmed**, 0 refuted, 1 undetermined.
- Full result: `claude_artifacts/folder_scan_c2/FOLDER_SCAN_RESULT_WF_FA4A29F1.json` `9911e4db`.

**Hard stops found and fixed now** (each would have raised mid-sheet, like A261 N1):
1. **§5 `cp -n` publication:** the parent `calib_tail_readiness_cx2/v006r11_c4` was absent, and no step creates it. **Created.**
2. **§6 `regenerate_h3_c2v004.py build --out-dir "$R/chain"`:** L203 `os.mkdir(out/sub)` is not recursive. The sheet dropped the source README's `mkdir "$R/chain"` (README_H3_CAMPAIGN_PATH_C2V001 L82). **Created** under the chosen R.
3. **§9–10 binder and launcher:** guard014 L289 requires `OUTPUT_ROOT.is_dir()`, and `/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001` was absent at two levels. **Created** as real directories on External1's device (16777240), with no symlinks (L290-294).

**Root-chosen verdict-day folders, chosen and created empty now:**
- R = `claude_artifacts/h3_at_verdict_c2` (with `chain`). `$R/H11_EVIDENCE` is deliberately **not** created, because the tool refuses an existing one.
- PS = `$R/POSTSEAL_PS`.
- E per phase = `$R/ENVELOPE_S0_SEED` and `$R/ENVELOPE_HEADLINE11`.
- PRELAUNCH_OUT = `$R/PRELAUNCH_H11`.
- S0 launch root = `/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A` (internal disk).
- The S0 *run* root `/Volumes/External1/NGC_S0_PHASE1_V001` is left absent, because root_monitor creates it.
- H1_CONFIG and H1_DELTA go in $R, not under handoff_v004: the FINAL producer refuses FENCE.REVIEW inputs.

**Template:** `CLAUDE2/VERDICT_DAY_VARS_C2V001.sh` `49607ea4` (A263 W3) holds all of these variables, and its syntax checks out.

**Later phases.** The remaining findings are folders root chooses at run time: W3 and per-wave registry_/lo_slot_ roots, the A257 manifest dir, P-112 launch/custody/v006-copy roots, the G28 step7 ledger root, the build/pass/step7/custody/snapshot/freeze out-dir parents, the values-writer out-dir (it must **exist**, the opposite of the builder and G26), cause-record and classifier OUT folders, and the S1 procedure-A folders.
- Root creates each one immediately before its step, following the scan file, which is the checklist of record.
- **Successor hardening noted (not blocking):** roster builder step7/custody should check that the parent exists before the ledger write.
- **Open:** the Phase-2 SCHEDULE_CEILING_CLOSURE writer and its folder are ruled before 2026-12-01T05:59Z.

## A273: the /tmp-dependency scan is clean; erratum to A272's count; cw8 v002 is ready for review (UTC 2026-10-21 12:59:03Z)

**The /tmp scan (A267 follow-up).** It covered the 37 production tools named by the folder scan, plus the verdict-day sheet and its INPUT_PINS_CX1V001.
- **No runtime dependency on /tmp.** There are only two references:
  - the fence self-tests' "should_not_exist" write probes (fence_c4v002 L158, fence_c4v003 L237), which expect a refusal;
  - the sheet's L124 prohibition ("no /tmp … spelling for fill_dir").
- INPUT_PINS_CX1V001 has 0 /tmp references.
- What /tmp did hold was test evidence. G26's was moved (A267), and C1's provenance copies were preserved earlier (E_A213_7).

**Erratum to A272:** the scan had **2** undetermined findings (campaign: the new-drive work-dir/pid parent; seal-s8-phase2: the Phase-2 closure writer), not 1. The totals stand: 51 raised, 50 confirmed, 0 refuted.

**cw8 v002 (Codex3 0687), with F1–F3 folded in, is ready.** Claude3 reviews it as the single Phase-1/2 launcher (A270, 0834/0835).

## A274: critical-path audit filed (Claude3 0275); root rulings (UTC 2026-10-21 13:01:56Z)

**Audit:** `critical_path_audit_c3/AUDIT_C3V001.md` `a8e50bc6`. All savings are UNTESTED, with their bases cited.

**Rulings:**
1. **Verdict-night QoS (A263):** the exception list is empty (TESTED by grep of every §3–§8 tool and the modules they load).
   - Root drops `taskpolicy -b` and `nice -n 10` from all §3–§8 commands.
   - `-b` stays only where a tool enforces it: the CP-1 runner c3v004 (L231-233, L466) and the list/registry assemblers.
2. **S0 J0–J2 are missing from the sheet (TESTED).** §7 pins only S0_SEED, and §11 launches only the seed and the twin. A161 has the J serials on Phase 1's critical path.
   - Codex3 writes the S0 J addendum: pins, fills, dry plans and launches, due Thu 03:00 CDT (0838 a).
   - Without it, root launches J0–J2 from the kit's own commands at the verdict.
3. **S0 does not wait on HEADLINE11's chain** (it settles A263 W2). The kit binds only the verdict report (L509). S0 needs §1–§4, its §7 pins, its dry plans and its START.
4. **C14 superseded.** Its basis, the machine gate, was removed by A166, so the S1 pair (S8) runs **concurrently**. This is the top S10 lever, about 11–18 h.
   - Build: new guard, launcher and binder successors (Codex3 0838 c, target Sun Oct 25), reviewed by Claude3.
5. **The campaign policy is signed before the mount** if its review binds only the work-dir path (Codex3 0838 b; E 1–4 h).
6. **u_A front chain (audit L3, E 2–5 h):** root pre-stages the row-32 EPS window and the templates, and re-dates the S1 C1 prerequisites to before W3 acceptance. Root does this once W1–W3 are running.
7. **The seal becomes near-critical** if L2, cw8 and S1 concurrency all land. Root sequences the seal with Claude4 from Fri 19:00Z, so that it is complete before S9's first NGC read.
8. **Refuted or partial:**
   - per-call replay: REFUTED (the snapshot and FULL gates come first);
   - a CP-1 QoS successor: PARTIAL (c3v004 `run_point` enforces background, L466; gated on a ≥1.3× timing ratio, and march0+ is S11 work);
   - Phase-2 work during Phase 1: PARTIAL.

## A275: the cw8 v002 delta PASSES (Claude3 0277); single-launcher custody; A271 item 3 corrected (UTC 2026-10-21 13:06:02Z)

**Delta review:** `verify_c3_cw8_phase1/RESULT_V002_DELTA.json` `9fa758db`, PASS with 0 blocking.
- **Diff confinement (TESTED, Claude3's own AST diff):**
  - launcher v002 `6de0d06a`: TOOL_NAME plus five functions, which are exactly F1–F3;
  - roster builder v002 `a2d8dc00`: BUILDER_NAME and P112_REVIEWED_SHA(S);
  - G26 v002 `332253d2`: the builder pin.
- 29/29 controls pass and 6/6 mutants are killed.
- The combined v002 verdict, covering the v001 lenses (role confinement, selector authentication, custody, RSS and walls, the integrated chain), is pending from Claude3. **Adoption waits for it.**

**Single-launcher custody (FORMAL, Claude3).** Roster builder v002 accepts only launcher v002, so a cx2v004-launched attempt would not be accepted at the S10 build.

**Correction to A271 item 3:** cx2v004 is **not** used for any launch.
- If an S0 serial needs a cap or infrastructure rerun before v002 is adopted, the rerun **waits** for v002. The stop is uncounted, and a wait of a few hours costs nothing physical.
- The verdict-day sheet's "cap reruns use P112 cx2v004" (L8) is read as P112 v002.
- HEADLINE11's walls now run to the ceiling (A271 item 2; DBP C2V004C, under Codex2's review 0839), so wall-cap stops are not expected.
- **If v002 fails its combined review,** root rules the fallback launcher together with a matching builder pin, so the chain stays single-launcher.

## A276: the S0 J0–J2 addendum is root-verified and adopted for verdict day; its staging folders are pre-created (UTC 2026-10-21 13:09:47Z)

**Object:** Codex3's 0689, `verdict_day_sheet_addendum_cx3/S0_J_ADDENDUM_CX3V001.md` `d6bdd5fe` (VALIDATION `56ed3b0d`; 0838 a; P-131). It covers:
- the whole-line HANDOFF_PIN S0_J{n} and SPEC_PIN S0_J{n}_SERIAL generation, printed from actual bytes with none fabricated;
- the per-J fill and the NGC r008 dry plan;
- the kit DRY;
- root-only first-attempt launches.

**Root verify:**
- The serial kit `launch_s0_serial_root_c2v003a.sh` `621263a2` takes the roles `<seed|j0|j1|j2>` (L12, L68).
- Driver `577f8c94` matches its bytes.
- The filler, the handoff tool and the twin script exist.
- The launch and run roots equal A272's.
- The folder rule separates parents root creates from absent leaves the tools create.
- The order is: seed LAUNCH confirmed → J0, J1, J2 → twin (A161, A166).
- S0 needs its own inputs and START, and does not wait on the r11/r12 reviews (A274 item 3).
- Six bash blocks pass a syntax check (Codex3, TESTED). The future verdict, handoff and spec hashes are UNTESTED until the night.

**Pre-created now (empty):** `UNT_S0_LAUNCH_C2V003A/prestage_J_CX3V001` with `fills/` and `driver_plans/`. Left absent for their tools: `handoffs`, `fills/J0-2` and `driver_plans/J0-2`.

**Use:** on verdict day, root runs the addendum's §2–§5 alongside the sheet's S0 branch. The J inputs go into the S0 envelope collect before START. Claude3's narrow check is welcome but not gating.

## A277: the campaign volume name and work_dir path are ruled; the campaign policy is signed before the mount (UTC 2026-10-21 13:10:50Z)

**Codex3's 0690 (FORMAL, TESTED on the extracted wrapper AST).** The campaign review binds eight fields, including `certificate_ledger = {schema, path: <work_dir>/CERTIFICATE_LEDGER.jsonl}`. It binds no UUID, inode, device or cache id, so it can be signed before the mount (audit L4, E 1–4 h).

**Ruled:**
- The new drive is formatted as an APFS volume named **`UNT_CAMPAIGN`**. With the 2×4 TB option (A-line about 2531), that is the RAID set's volume name.
- work_dir = `/Volumes/UNT_CAMPAIGN/DDO154_CAMPAIGN_V001`, which is free of the protected components ngc3198, uvt_, runs_ext and UNT_INTERNAL_RUNS.
- W1's tail_readiness equals frozen C1 `40159322`.
- Codex3 signs against this path now (0840).
- The principal is told the exact volume name.
- If the volume mounts under another name, Codex3 re-signs: a byte change of minutes.
- Mount-dependent checks (UUID, inode, storage_check, the runtime ledger) stay at W1.
- This also settles the folder scan's undetermined campaign finding: the work dir lives on UNT_CAMPAIGN, and the pid and log parent is `/Volumes/UNT_CAMPAIGN/DDO154_CAMPAIGN_LOGS_V001`, created at the mount.

## A278: the direct-call root layout for the L2 Jacobian batch is adopted (Codex1 0183) (UTC 2026-10-21 13:13:15Z)

**Basis (Codex1, FORMAL plus an inert TESTED predicate):**
- handoff004 and the b1 enumerator read `call_dir/out`.
- `h3_accept_call004` locate forces the campaign wave layout.
- guard014 requires the outdir, the receipt, the monitor_log and the launch sidecar to be distinct and non-nested (L397–404).

**Ruled layout:**
- **Call root:** D = `/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001/DDO154_JACOBIAN_R<row>_<key16>_A<n>`.
- **Inside D:** `D/out`, `D/RECEIPT.json` (sidecar `.launch.json`) and `D/monitor.log`.
- **Launcher log:** under OUTPUT_ROOT, outside every D.
- **Custody:** D is the true direct execution location, never presented as a wave dir. Nothing is copied or moved.
- **Spec pin:** the original spec pin stays explicit. The importer and acceptance entry consume it, and never `D/spec.json`.
- **Scope:** this preserves the acceptance chain's output layout with no virtual aliases. The importer's I1–I3 work continues (target Fri Oct 23 12:00 CDT).

## A279: RUNBOOK c2v007 verified and adopted as the base; G26 is unconditional; root's cause-before-snapshot rule (UTC 2026-10-21 13:15:09Z)

**RUNBOOK c2v007 / roster builder `799fb2d0`:** Claude3's 0279 is a PASS with 0 blocking (`verify_c3_runbook_c2v007/RESULT.json` `00de7bca`).
- It has no Phase-1 stop, because c2v007 only calls read-only P112 functions.
- Counting is exactly the authenticated solo pairs. The snapshot covers every planned call.
- Tests: 338/338 functional, 48/48 mutants killed, and 10/10 of the helper's probes.

**Adopted as the verified base.** The cw8 v002 package carries the production successors: builder `a2d8dc00` and G26 `332253d2`. Those wait on Claude3's combined v002 verdict (A275).
- **G26 `663d4c2b`:** its A267 condition is met, so it is adopted as a base.
- **F1:** c2v007 pins only cx2v004, which is resolved by v002's single-launcher pin (A275).

**F2 (TESTED), now a root rule.** `_ceiling_or_hold` returns a present closure before any hold check, and `phase1_snapshot` does not require cause rows. So two identical solo `ROUTE_A_NO_FIXED_POINT` attempts with no cause records would close as SCHEDULE_CEILING (UNEVALUATED), which is against A249 items 2 and 4. The v002 builder keeps this ordering.
- **Rule:** before **every** phase snapshot (Phase-1 step 4 and Phase-2), root runs the adopted cause producer (A266) on every FAILED attempt. Root confirms that each eligible solo FAILED attempt has a bound cause row before taking the snapshot.
- **Hardening:** a snapshot precondition that refuses when a cause row is missing goes into the next builder successor, whenever one is next cut (Codex3). It does not gate adoption.

**F3–F7:** noted, as conservative or operator-input classes.

## A280: campaign certificate policy signed before the mount; the 7 L2 call roots are pre-created (UTC 2026-10-21 13:16:10Z)

**Campaign policy (Codex3 0692; 0838 b, A277):** `cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_CAMPAIGN_CX3V001.json` `55926860`, with validation `0ecf7c2a` (14/14 AST controls).
- It binds `certificate_ledger.path = /Volumes/UNT_CAMPAIGN/DDO154_CAMPAIGN_V001/CERTIFICATE_LEDGER.jsonl`. Frozen C1's registry, six producers, custody and enumerator are unchanged.
- **This is W1's `tail_readiness.certificate_policy_review` pin.**
- The mount checks (UUID, inode, storage, cache identity, runtime ledger) stay at W1. A different mount path needs a new signature.

**L2 call roots (A278; Codex1 0184).** launcher015 opens `D/monitor.log` with `xb` before it starts the monitor (L127–128), so each D must exist and be empty before launch. Root created the seven D folders now, empty, under OUTPUT_ROOT:
- `DDO154_JACOBIAN_R28_6944e210d071c17b_A1`
- `R29_39a36ac345a43192_A1`
- `R30_2a17398ba37976a7_A1`
- `R31_a1b7660c2ebc9540_A1`
- `R300_06c3e863688de635_A1`
- `R301_95540f067efd4a14_A1`
- `R302_6f4604efe6d7fe34_A1`

Inside each D, `out/`, `RECEIPT.json`, `RECEIPT.json.launch.json` and `monitor.log` stay absent. A rerun uses a new `_A<n>` root, created at that time.

## A281: cw8 v002 combined verdict FAIL (F2); v003 commissioned; license-pin rule (UTC 2026-10-21 13:25:50Z)

**Claude3's 0280** (`verify_c3_cw8_phase1/RESULT.json` `4a73cb5c`): FAIL, 1 blocking. F1 is confirmed fixed in v002.

**F2 (blocking, TESTED).** v002 L3401 compares the whole `{path, sha256}` spec dict, for every record including KIT origin.
- An honest S0 kit relaunch fills into a fresh `$WORK/fill`. The bytes are identical, but the path differs.
- So the call refuses CW8_ATTEMPT_RAW_SPEC, where cx2v004 accepts it.
- An S0 serial call relaunched by its kit (MISLAUNCH, D7) could then not be closed, rerun or assembled. That would be a custody regression on the single launcher.

**Ruling:** Codex3 makes v003 (0842), with:
- F2: compare sha256 only;
- N1: a durable fallback for malformed selector inputs;
- N6: tests that kill the surviving custody and CLI mutants, including license re-authentication on restore and "never self-granted";
- N8: a lock on creating the worker-role choice;
- the A279 snapshot precondition on cause rows.

Claude3 gives v003 a narrow delta review. **Adoption of the cw8 Phase-1/2 launcher waits for v003.** No P112 launch happens before then (A275).

**Rules:**
- **N2:** V006 carries exactly one `CW8_LICENSE_PIN` line, which is never superseded. A license change means a new tool version.
- **N3:** a change to a Phase-2 scope field is a new config under a V006 event.

**Timing:** S0's kit launches (Thu) do not use P112, so v003 is needed only before the first P112 close or rerun and before S9.

## A282: the cw8 v003 package is ADOPTED as the single Phase-1/2 launcher, builder and G26; tool pin (UTC 2026-10-21 13:52:35Z)

**Reviews:**
- Claude3's 0283 delta review of v003: PASS with 0 blocking (`verify_c3_cw8_phase1/RESULT_V003_DELTA.json` `fb99a4bb`).
  - F2 is closed: Claude3's own kit-relaunch probe closes FINISHED on v003 and still refuses on v002, so the probe discriminates.
  - N1, N8 and the A279 snapshot gate are built as specified.
  - 7 of 15 mutants were re-run, and all 7 were killed. F1–F3 pass 29/29, and the selector and snapshot suites pass 39/39 each.
- Together with Claude3's 0277 (the v002 delta) and 0280 (the v001 lenses), every cw8 review is closed with no blocking item.
- Codex3's own suite: 502/502 controls, and 15/15 targeted mutants killed.

**Adopted** (P-130; supersedes P112 cx2v004 for every Phase-1 and Phase-2 launch, close, rerun and assembly, per A275):
- launcher `cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py` `4d5b47e7`;
- roster builder `cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py` `f710334b`, which accepts only this launcher;
- G26 `cw8_phase1_cx3/g26_freeze_cx3cw8v003.py` `171710bb`.

The serial path is the automatic fallback. cw8 is used only under the root-pinned license, and only when the predicted cohort gain is strict.

TOOL_PIN P112_LAUNCHER_CX3CW8V003 4d5b47e75f90241460dd0b86155ddae2267117c31f6043fc57777ea94564919d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py

**Notes:**
- **v003-N1:** the A279 gate checks every pre-ceiling solo FAILED attempt, including one later superseded by a terminal attempt. Under the A279 rule, root runs the cause producer on every FAILED attempt before any snapshot. The cause-producer cxv003 verify (0832) confirms that it gives a row for every honest FAILED-class receipt.
- **v003-N2:** no mutant isolates CW8_COMPARATOR_FORM, which only changes the reason code.
- **v003-N3:** a lock-wrapper refusal (missing launch root, tampered lock) writes no fallback record. Root creates the P-112 launch root and its subfolders before the first use (A272 checklist).
- **The cw8 license** is written as the single CW8_LICENSE_PIN line (A281 N2) only after S0's serial/twin comparator reads EQUAL with bitwise_equal true over iterations [0,1].

## A283: L2 importer root inputs ruled (Codex1 0190): speculative register, runtime capture, L2_DIRECT envelope (UTC 2026-10-21 13:59:34Z)

**1. The speculative register is bound in two stages:**
- `SPECULATIVE_REGISTER_L2_V001` is written at the direct launch. For each call it holds the row, key, spec pin, call root, attempt, the tool and DBP pins, and the runtime capture.
- `SPECULATIVE_REGISTER_BINDING_L2_V001` is written at campaign init. It binds the register's sha to the final W1 config sha, cache_id and gate digest.
- The importer requires both, and fails closed otherwise.
- An early COMPLETED_INVALID stays in the register and is never auto-ingested (the discard rule).

**2. Runtime/environment capture.** Codex1 builds the producer, and Claude3 reviews it.
- **It captures:**
  - the interpreter realpath and binary sha256;
  - sys.version and sys.flags;
  - the version and file sha of every driver-imported module;
  - the macOS build and the hardware model;
  - a whitelisted, normalized environment: the thread variables, PATH, PYTHON*, DYLD*, LC_*/LANG and TMPDIR. No other values are recorded.
- **Must be equal** across the direct and campaign launches: the interpreter sha, the module versions and shas, the normalized thread variables, the macOS build, and the absence of PYTHON* and DYLD* variables.
- A capture is taken at launch and never inferred later. Fail-closed.

**3. A226 item 3 envelope phase `L2_DIRECT`:**
- The pin set covers:
  - the driver and monitor;
  - the 7 spec pins;
  - the launcher, guard, binder and DBP pins;
  - the register;
  - the runtime captures;
  - the importer policy and entry.
- It STARTs before the 7-call launch and ENDs after the last import or discard.
- Its folder `$R/ENVELOPE_L2_DIRECT` was created now, empty.

All three are published as one immutable importer policy. The generated wrapper and cache identity stay unchanged.

## A284: the concurrent S1 pair (S8) is ADOPTED (Claude3 0285); root procedures; POST_S1 walls to the ceiling (UTC 2026-10-21 14:16:57Z)

**Review:** Claude3's 0285 (`verify_c3_s1_pair/RESULT.json` `3d2a034a`) is a PASS with 0 blocking.
- There is no widening: POST_S1 only, exactly the two calls in S1 order, max_active 2. A guard014-bound plan is refused by the successor launcher.
- Each call keeps its own C1, context, native preflight and source review. The specs replay byte-equal, and physics is unchanged.
- The bases are byte-unchanged. Tests: 53/53 functional and 15/15 real replay; of 30 helper mutants, 28 are killed and 2 are equivalent.

**Adopted (P-132):**
- `s1_pair_concurrent_cx3/v001/`: guard `1274a39a`, launcher `2e41da37`, binder `f57f5f1d`;
- root wrapper v002 `c08b5b78`;
- README `27e86901`.

**Root procedures:**
- **N6:** root reviews and publishes the **parent** pair admission like any other admission. The ROOT_AUTHORIZED value copied from the C3T child is never relied on.
- **N9:** the binder's command file is never used. The launch goes through the pair wrapper only (README L59).
- **N10:** the S1 pair's A226 item-3 envelope covers both child admissions, both plans, both C1s and both prelaunch records.
- **N7:** if C3T ends for a non-systemic reason before its first iteration, the batch drains and C4T is launched in a later batch.

**N8 (wall):** both S1 calls still carry the 100,800 s wall of DBP C2V004B. Under A246, Claude3 builds the data-only DBP **C2V004D**: the HEADLINE walls of C2V004C plus the POST_S1 walls, all to the ceiling (0844, Sat). A narrow review follows. C2V004C remains the verdict-day object.

**N1 (test gap):** the release suite's `refused()` accepts any exception. Claude3's probes are added as non-gating controls when Codex3 next cuts the package. This does not block adoption.

## A285: runtime-capture scope ruled (Codex1 0192) (UTC 2026-10-21 14:23:54Z)

**Finding (Codex1, TESTED by AST):** driver b5cc62af runs 12 pinned SCRIPTS modules through `exec_verified` (L577–586) without registering them in sys.modules. A sys.modules snapshot therefore does not list them.

**Ruling:**
- Those modules' identity is established by the driver's own pinned-bytes verification, given the same driver sha on both sides. The driver sha is captured, and the monitor checks it.
- A source-only transitive closure is not required.
- **The capture covers what the driver does not pin:**
  - the interpreter (realpath, binary sha, version, flags);
  - the third-party distributions the driver's modules import, named by an AST scan of the pinned SCRIPTS, each with its version and a RECORD or file-tree hash;
  - the normalized whitelisted environment;
  - the macOS build and hardware model;
  - the driver and monitor shas.
- `unresolved_dynamic` is closed by that argument, and the argument is recorded in the importer policy.

## A286: Codex2 lane silent (last write 12:46Z, 0839 unacked); its open items move to Codex3 (UTC 2026-10-21 14:26:34Z)

**Observed (metadata only):**
- Codex2's last outbox message was 0570 at 12:36Z.
- The last file in `direct_cert_lookup_cx2/` was written at 12:46Z.
- Dispatch 0839 (13:04Z) has had no ack for about 80 minutes.
- The likely cause is credit (35 % on Oct 21, reset Nov 10). That is unconfirmed.

**Reassigned (0846):**
- The C2V004C narrow review (due Thu 03:00 CDT) and the C2V004D review go to **Codex3**. Both are cross-family to the author, Claude3.
- 0828 unit 2 (the direct certificate lookup) also goes to **Codex3**. It continues from Codex2's partial state, read-only, with outputs in `direct_cert_lookup_cx3/`.
- Unit 3 is narrowed to a check from bytes of guard014's admission of the 7-call batch.
- Claude3 reviews. Target: Fri 12:00 CDT.

The principal is told the lane looks stalled, with a nudge prompt. If Codex2 resumes, it posts status only, with no duplicate work.

## A287: refinement to A285: package identity uses the bytes route (Claude3 0288) (UTC 2026-10-21 14:26:50Z)

- **Third-party distributions:** a sha256 over the sorted file list plus file bytes, including bundled native libraries (`.dylibs`, extension `.so`).
- **`__pycache__` and files outside RECORD** are recorded, and `__pycache__` is excluded from equality.
- **A RECORD-file hash alone is not accepted.**
- **The interpreter** is statically linked (TESTED, `otool -L`), so its binary sha covers its code.
- **OS Accelerate/vecLib** are covered by the macOS build capture, with updates off.

## A288: Codex2 is paused, not out of credit (principal); its new items are routed (UTC 2026-10-21 14:30:43Z)

**The principal (verbatim):** "codex2 is not out of credit". So A286's likely cause is wrong: the lane is paused.

The reassignment to Codex3 stands for 0839, C2V004D and 0828 unit 2. On resume, Codex2 takes two items (0848):
1. **0828 unit 3:** a check from bytes of whether guard014 admits the 7-call direct batch after H11. It moves from Codex3.
2. **Cause producer cxv003:** it moves from Codex1 (0832), and the verify confirms a cause row for every honest FAILED-class receipt (A282 v003-N1).

Claude3 reviews both. The principal is given a nudge prompt for Codex2.

## A289: lane credits (principal, about 09:30 CDT) and the allocation that follows (UTC 2026-10-21 14:33:44Z)

**The principal:** "Codex1 has 52% credits left - Codex2 is at 30% left - Codex3 is at 47% left". Claude3 reset at about 09:00 CDT and is fresh. Claude4 returns Fri 19:00Z. Root (Claude2) is at 91 % weekly until Thu 18:00Z.

**Allocation (A258, wall clock first):** the remaining committed Codex work is bounded:
- **Codex1:** the importer, by Fri 12:00 CDT.
- **Codex3:**
  - the C2V004C and C2V004D reviews (C2V004C due Thu 03:00 CDT);
  - the direct certificate lookup (Fri).
- **Codex2:**
  - the 7-call admission check (today);
  - cause cxv003.

**Reviews go to Claude3.** Codex1 and Codex3 together have about 99 % to cover these, and the verdict-night gating checks (Codex3, A268) are pre-staged and cost minutes.

**Rule:** no new Codex build is commissioned unless it is on the S6–S10 critical path and names its saving. Off-path hardening waits for each lane's weekly reset.

## A290: Claude3 credit reset (principal: "Claude3 just reset and has 100% left"); its capacity goes to the critical path (UTC 2026-10-21 14:34:41Z)

Queue (0850), after Claude3's current reviews:
1. An incremental review of Codex1's importer as it lands, so the Friday review is a delta.
2. **A consolidated verdict-day executable runbook**, due Thu 01:00 CDT. It merges sheet `f2a5eec4` with the adopted amendments (A261, A263, A271/C2V004C, A272, A274, A275, A276) and Codex3's pre-staged checks (A268), with every line traced to its reviewed source and no new commands. Its purpose is to keep root's verdict-morning work, and credit, small.
3. **The u_A → S8/S9 launch chain, pre-staged**, due Sat 12:00 CDT (audit L3).
4. **The seal (S7) path, pre-staged**, due Fri 12:00 CDT. Everything that does not need Claude4 is done before Claude4's reset at Fri 19:00Z.

## A291: DBP C2V004C and C2V004D ADOPTED; HEADLINE11 and the S1 pair run to the Phase-2 ceiling wall (UTC 2026-10-21 14:35:14Z)

**Review:** Codex3's 0698 and 0699, narrow, PASS under A115 (`review_wall_ceiling_cx3/WALL_CEILING_REVIEW_CX3V001.json` `8805a6a8`).
- 27/27 independent checks.
- C2V004C reruns 18/18 with 4/4 mutants killed. C2V004D reruns 8/8 groups with 11/11 mutants killed.
- W = 3,443,340 s, which is 2026-10-22T09:30:00Z to 2026-12-01T05:59:00Z.

**Adopted:**
- **Verdict day (HEADLINE11):** DBP C2V004C `h11_wall_ceiling_c3/C2V004C_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004C.json` `ce9cbef8`, with check script `check_headline_caps_c3v001.py` `4efb810b`. Claude3's 0276 sheet amendment applies:
  - sheet L8 text;
  - the DBP_C variables before PRELAUNCH;
  - caps copied into GUARD014_FINAL_PLAN and FINAL_ADMISSION_CANDIDATE from C2V004C;
  - the check after bind, where any failure is a STOP.
- **S8 onward (the S1 pair):** DBP C2V004D `…/C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json` `5d3f4bb8`, with check script `check_s1_pair_caps_c3v001.py` `5f24c6bf`.

**The A248 exception (100,800 s for HEADLINE11 first attempts) is superseded.** No wall cap ends any of these runs before the ceiling (A246). Stalls are handled by the stall watch and root's individual call.

**Nonblocking (Codex3):**
- the sheet's stale A248 wording is governed by this amendment;
- the D checker's description says five records but checks six.

Claude3's consolidated runbook (0850 item 2) carries the amendment in its place.

## A292: root credit conservation until Thu 18:00Z; Claude3 is deputy for non-launch rulings (UTC 2026-10-21 14:36:24Z)

**The principal:** "Your usages is 93% used. Only 7% left."

**Measured:** most of today's root usage was multi-agent workflows (about 2.4M subagent tokens). Ordinary tool calls cost little.

**Rules until Thu 18:00Z:**
- **No root workflows.** A236 applies, and the hard limit governs ultracode.
- **Root wakes only for:**
  - the S4T R3 receipt or the monitor's exit (background `bud6m1qyu`);
  - a lane file named `*ROOT_ESCALATION*` (background `by3sz6v36`);
  - the principal.
- The lane-outbox watch is stopped.
- **Claude3 is deputy** for non-launch build and design rulings within A254–A291 (0851).
  - Its log is `deputy_rulings_c3/DEPUTY_LOG_C3V001.md`, ratified by root after the reset.
  - Excluded from its remit: physics, blinding, launches, sealed bytes, V006, verdict-day adoption, and date moves of more than 12 h. These escalate.
- **The verdict day** runs from Claude3's consolidated runbook (due Thu 01:00 CDT), lean, one block per call.

## A293: CP-1 list run for W3 minus: rows 300 and 301 certified; row 302 (ell_F minus) EPS_UNCERTIFIED. Analysis commissioned (UTC 2026-10-21 16:36:43Z)

**Facts** (scheduler `…115353Z_4336`, SCHEDULER_END 16:35:32Z; root read the certification records only):
- Rows 300 and 301 exited 0, and their EPS review requests are pending.
- Row 302 (key `6f4604ef…`, ell_F minus at 0.05 unit) exited 3.
  - POINT_STOP `EPS_RECORD_NOT_ADMISSIBLE_AS_RECORDED`, with `registered_discrete_CERTIFIED: false`; every other check is true.
  - STAGE_EPS EPS_UNCERTIFIED, eps_max 2.52e-4, 178 shells, 16,508 s.
  - GQ PASS.

**This is the value of certifying early (A257):** the issue surfaced about 3 days before W3.

**Commissioned:** Claude3 analysis (0852), due Thu 01:00 CDT. It covers:
- the cause;
- any registered remedy (no new criterion);
- the campaign's behavior at W3 for an uncertifiable requested point (prelaunch, engine, F6/HALT);
- the ell_F halvings, which are certifying now;
- the composition of the L2 batch.

Anything physics-touching escalates to root.

**No ruling yet.** L2's 7-call batch is provisionally 6 calls (seed, 3 plus, rows 300 and 301), pending the analysis.

## A294: row 302's EPS failure is one shell of 178 under a relative refinement rule with no absolute floor; the precision question goes to analysis (UTC 2026-10-21 16:57:24Z)

**The principal (verbatim):** "Are we sure that we haven't specified an artificially low level of precision?"

**Facts** (certification record and producer; FORMAL from bytes):
- 177/178 shells certify. Only shell [46, 47] kpc⁻¹ fails: eps_base 1.087e-6 → eps_refined 1.220e-6, a ratio of about 1.12 against the rule's 1.1×.
- The governing eps_max is 2.52e-4 at shell [4, 5], which certified.
- The rule is `point_response_producer_cx2v002` `discrete_shell`: level-to-level ratio ≤ 1.1, at most one refinement. It is purely relative.

**Reading (UNTESTED until the analysis):** this looks like a rule artifact on a negligible shell, not a real loss of precision in the quantity that matters.

**But the rule is registered.** Any amendment is a root physics-process ruling. It must:
- be justified by how `uv_tail.eps_certificate` is consumed;
- be uniform across all points, so it only adds passes;
- be decided before any NGC value is read.

Claude3 analyses this (0853, as an addendum to 0852) and escalates the recommendation. Root rules no later than Thu 18:00Z. Nothing changes until then.

## A295: ruling in principle on negligible-shell EPS refinement variation (UTC 2026-10-21 16:57:44Z)

**The principal (verbatim):** "If we are truly talking about that level of variation I would think that we would note it and accept that a variation in that range is well within the observational error threshold."

**Ruling in principle (root):**
- An EPS shell that fails the purely relative 1.1× refinement rule is **noted and accepted** when **both** of these hold:
  - (a) its eps is negligible against the certificate's governing eps_max;
  - (b) its absolute refinement change is far below the A133 numerical tolerances and the observational error budget.
- It is applied as a **uniform, recorded rule** for every CP-1 point, past and future. It only adds passes, so no certified point changes. It is set before any NGC value is read.
- It is never applied as a one-off exception.

**Final text:** root adopts the exact constants (the fraction of eps_max, the absolute floor, the safety multiple) on receipt of Claude3's 0853 analysis. That analysis confirms how `uv_tail.eps_certificate` is consumed and bounds the worst-case effect of an under-converged negligible shell. If consumption shows that such a shell could move a computed value non-negligibly, the principle does not apply and root rules again.

**Implementation:** a registered successor of the EPS rule, reviewed, is built only after the final text. Row 302 is then re-evaluated under it.

## A296: A295 final text. The negligible-shell EPS rule is ruled (Claude3 0309, R1–R4, conservative substitution); adoption is conditional on Codex2's independent analysis (UTC 2026-10-21 17:26:47Z)

**Analysis of record:** Claude3 `w3_row302_eps_c3/ANALYSIS_C3V001.md` `f80c9a3e`. Escalation 0309.
- **Consumption (FORMAL):** per-shell eps is read only by the post-run SRB-ROT bound. It is per shell (each ε_s × B_s), with a gate at τ_i/10. No tail, lapse or rotation value reads eps inside a call.
- **The value consumed is converged:** 672/672 dense audits show dense/production ≤ 1.0000.
- **The failing shells are negligible:** eps/eps_max is 7.6e-3 (row 302), 2.8e-3 (row 501) and 3.0e-3 (row 504).
- **Without a rule, W3 refuses as a whole** at CERTIFICATE_PREFLIGHT, and S6 stalls (Case A).

**Ruled (final text):**
- **R1. ACCEPTED_NEGLIGIBLE.** An EPS shell whose discrete rule gives refinements = 2 is accepted only if all of these hold:
  - (a) M·ε_s ≤ f·eps_max(point), with **M = 10 and f = 0.1** (ε_s ≤ 1 % of eps_max);
  - (b) |L2 − L1| ≤ **1e-6** (relative-response units);
  - (c) the producer's dense envelope audit on that shell gives audit/production ≤ **1.05**;
  - (d) every other shell certifies under the 1.1× rule, with registered settings, full coverage [4, 182] and status TESTED.
- **R2. Conservative substitution.** For each accepted shell the successor record writes **ε := M·ε_s** and keeps the measured value in a disclosed field.
  - The SRB-ROT adapter is unchanged, so the per-call gate evaluates the worst case with that call's exact B_s.
  - eps_max and eps_max_shell are unchanged.
- **R3.** A distinct verdict, `NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED`, lists the accepted shells. Approved-signer review is required.
- **R4.** The rule is uniform for every CP-1 point and only adds passes; the 31 genesis points have no refinements = 2 shell (TESTED). It is set before any NGC read.
  - Rows 302, 501 and 504 are re-evaluated under the reviewed successor.
  - A shell above 1 % of eps_max stays EPS_UNCERTIFIED, and root rules on it.

**Condition.** Final adoption of the successor requires that Codex2's independent analysis (0854 a, a separate lineage) contradicts none of these points:
- the per-shell SRB-only consumption;
- the converged consumed value;
- the margins.

Codex2 starts the build (0854 b) now with these constants. Review: Claude3.

**Open gap (Claude3 A3, FORMAL): F5 has no branch for a requested point that cannot be certified**, even outside R1. Root rules this after its reset (Thu 18:00Z), on a proposal Claude3 prepares as deputy analysis.

**L2:** 6 calls (R28–R31, R300, R301). R302 returns as the 7th only if its successor, re-evaluation, bundle, ρ, slot proof and final spec are all complete before the batch binds. The ell_F plus at 0.025 hedge is not added.

## A297: A296's adoption condition is MET (Codex2's independent analysis, 0586); the qualification is recorded; R1(c) audits must be blinding-clean (UTC 2026-10-21 17:33:21Z)

**Codex2's ANALYSIS_CX2V001** (`7bfdb90e`; driver review `143cd3b8`; census `d9659d90`), a lineage independent of Claude3:
- **FORMAL:** the DDO and NGC production kernels use EPS references for custody only. EPS never enters as a tail or lapse correction.
- **The proof-side SRB is per shell,** Σ eps_s·B_s, with no eps_max substitution. A296's tenfold substitution leaves the numerical tail and lapse unchanged, and raises only that shell's weighted acceptance-bound term tenfold.
- **TESTED:** 672/672 existing dense audits are ≤ 1.05, with a maximum of 1.00000027.
- Rows 302, 501 and 504 each have exactly one failed discrete shell and meet R1 (a) and (b). R1 (c) on those shells is UNTESTED.
- **No contradiction** of Claude3's consumption finding, its convergence finding or its margins, so **the condition is met.**

**Qualification, recorded.** EPS is a sampled estimate, not a proven supremum (`rigorous_supremum: false`; "numerical convention only"). That holds for **every** shell of every point under the registered framework. The A296 substitution, ε := 10·ε_s on an accepted shell, is therefore **more** conservative than the standard 1× treatment of all other shells. A296 makes no claim of a rigorous true-error ceiling.

**R1 (c) audits:** they run on a **blinding-clean path** only. Codex2 found that a naive audit context would read prohibited NGC run inputs, and is checking a pinned frozen-coefficient or static-definition path. Root requires that this path open no NGC3198 data file and no run tree. Claude3's review confirms it.

**Adoption:** the successor, the re-evaluation and the R1 (c) audits are adopted on Claude3's review PASS. Row 302 then becomes eligible for its bundle, ρ, slot proof and final spec (the possible 7th L2 call).

## A298: F5 gap ruled (Claude3 0312, F5_GAP_PROPOSAL_C3V001 `671f8948`); the A296 integration chain must land before the mount (UTC 2026-10-21 17:37:13Z)

**Adopted (no code):**
- **F5-R1, the ladder.** A requested point that fails certification goes through: the registered rule, then A296, then a HOLD of the wave (A245 item 3) with a V006 `HELD_UNCERTIFIABLE` entry.
- **F5-R3.** No substitution for any purpose: seed, repair or march. The point stays HELD until a reviewed fix. At the ceiling it becomes UNEVALUATED_SCHEDULE_CEILING (FREEZE_INCOMPLETE, never MEMBER_INVALID).
- **F5-R5, pre-emption.** Every enumerable finite-difference point (both sides at 0.05, 0.025 and 0.0125) is pre-certified under A257's compute-only rule. **This is already running:** the halvings and globals hedge (A258), with rows 404 and 405 certified.

**Deferred: F5-R2 (Jacobian-side NUMERICS_UNAVAILABLE → registered halving).**
- It would be a wrapper change landing at the W1 regeneration, before the mount, which is extra integration risk.
- Every observed failure (rows 302, 501, 504) sits inside A296. 0/58 points have a non-negligible failure (TESTED).
- **Root revisits F5-R2 only if** a remaining hedge point (rows 408 and 411 are due about 22Z, plus the globals) shows a non-negligible Jacobian-side failure.

**Time-critical: the A296 integration chain (Claude3 F5-R4).**
- The cache id binds the wrapper and policy, so A296 must enter the certificate chain **before the W1 regeneration (the mount, Fri night)**:
  1. Codex2's rule successor, its re-evaluation and the R1(c) audits (blinding-clean, A297);
  2. **successors of the eps admission adapter and validator.** Adapter 4de70486 re-applies the 1.1× rule (L108–129, L176), and the existing validators reject the new verdict. **Codex2 adds these to its build (0856).**
  3. **A C1 successor** (frozen C1 `40159322` → c2v002) carrying the new adapter as an approved producer. **Root builds it after the reset, Thu 18:00Z.**
  4. **Codex3 re-signs the campaign policy** against the C1 successor (minutes).
  5. The W1 config carries the new C1 and the new policy pin.
- Row 302 then gets its bundle, ρ, slot proof and final spec, and can be the 7th L2 call if ready before the batch binds.
- **If the chain misses the mount,** W1 still starts with the current C1. W3's ell_F minus then follows F5-R1 (HOLD) until the chain is adopted. Root rules whether a new work dir or a policy successor carries it then.

## A299: hedge certification results; S4T R3 re-projected later (UTC 2026-10-21 20:47:57Z)

**CP-1 hedge, all 27 points finished:**
- **W3 minus:** 2/3 pass; row 302 fails (A293).
- **Halvings:** 12/12 pass, including rows 408 and 411, the ell_F minus halvings. **F5-R2 stays unneeded for W3** (A298).
- **Globals:** 10/12 pass; rows 501 and 504 fail, both inside A296.
- **In total:** 24/27 pass, and all 3 failures fall inside A296.

**S4T R3 re-projection.** Stage 20 (le3 columns) began at 12:27Z and was still running at 20:47Z, after 8.3 h. That exceeds the projected 6.9 h (C4T's ratio of 1.27×) and is now at least le2's 1.52×.
- If le3, le4 and le5 each run about 8 h, plus about 20 min per level and about 1.5 h of tail, the receipt lands about **Thu 22, 13:00–16:00Z (8–11 am CDT)**. That replaces A260's 4:30–5:30 am. UNTESTED.
- **Erratum E_A260_PROJ:** A260 applied C4T's late-level ratios, which S4T's le3 has not followed. Rule: re-project once a stage exceeds its projected duration by 20 %.
- The verdict day still falls on Thursday. Root's reset (13:00 CDT) may now coincide with the verdict-day work, which only helps.

## A300: a lane-stall alert independent of any Claude session (principal: "We need a better and more 'OBVIOUS' way for you to alert when a lane is stalled") (UTC 2026-10-22 03:40:47Z)

**The failure:** root stopped its lane watch for credit (A292). Codex1 went silent for about 11 h, and the principal was not told. This breaks the standing rule to alert the principal when a lane stalls (memory: alert on lane stall).

**The fix:** `CLAUDE2/STALL_ALERT/lane_stall_alert_c2v002.zsh` `515d7b00`, running under nohup (pid 60240). It replaces v001 `6b58d714`. It uses no Claude session or credit, and alerts the principal directly on the Mac:
- **UNANSWERED:** a root dispatch naming the lane (or ALL_LANES) is newer than the lane's last post, for more than 20 min.
- **SILENT:** the lane has posted nothing for more than 120 min after posting within the last 18 h.
- **Alert:** a macOS banner with sound, a spoken warning, and a modal critical alert titled "WARNING WARNING WARNING WARNING LANE IS STALLED: <lane>", which carries the paste-in nudge text. It repeats every 30 min while the condition holds. Each alert is logged in `STALL_ALERT/ALERT_LOG_*.txt`.
- It covers Codex1–3 and Claude3. Claude4 is added after its reset on Fri 19:00Z.

**Limits:**
- It reads file names and mtimes only.
- A lane that is idle by design (its queue empty) can trigger SILENT, and the alert says "check".
- The script stops if the Mac reboots. Root restarts it at each session.

## A301: stall alert v003, with the lane named first (principal: "And tell me in the warning which lane") (UTC 2026-10-22 03:41:32Z)

`STALL_ALERT/lane_stall_alert_c2v003.zsh` `8d3d9749` replaces v002 `515d7b00` (pid 60442).
- The alert title is "WARNING WARNING - <LANE> IS STALLED - WARNING WARNING", with the lane in capitals.
- The banner reads "WARNING: <LANE> IS STALLED".
- The spoken warning names the lane twice.
- Rules, nudge text and logging are as in A300.

## A302: verdict-day rulings on Claude3's escalation 0334 (E1, E2); runbook C3V002 is FINAL (UTC 2026-10-22 07:59:12Z)

**E1. Ruled as Claude3 recommends.**
- HEADLINE11 stays on frozen **C1 V001** (`40159322`) and the **c2v004 r12 chain** (runbook B6, B8a, B8b; table-D STOP on the FINAL specs predicted on V001).
- The A296 chain (C1 successor V002, the new adapter and guard) is for the **campaign only**: W1's config and a separate B6 regeneration against the A296 cascade.
- Root never pastes the new C1's tail_readiness into HEADLINE11's `H1_PREDECESSOR`.

**E2. Order:** the verdict-day launches go first; the A296 chain follows, and only has to land before the mount (A298).
- **V006 write-freeze rule:** from the start of B11.1 (the seed's `--launch`) until the seed's confirmed launch record exists, **root writes no V006 entry of any kind**. That includes A-entries, because the seed's launch refuses if V006 changed in that window (runbook 0.3 item 9; kit L23, L34).
- The same applies to any other launch that records V006, inside its own window.

**Runbook:** `verdict_day_runbook_c3/` C3V002 is **FINAL** (Claude3 0334). Every source re-hashed equal: J `d6bdd5fe`, M `314ef346`, S `f2a5eec4`, V `49607ea4`, DBP C2V004C `ce9cbef8`. Root executes from it.

## A303: the lane heartbeat watchdog (principal: "Can we cut the time to catch a stall down? Maybe we need a heartbeat monitor?") (UTC 2026-10-22 07:59:50Z)

**Watchdog:** `STALL_ALERT/lane_stall_alert_c2v004b.zsh` `2c26b775`, under nohup, replacing v003. It checks every 60 s.
- **Rule 0, HEARTBEAT:** a lane's `UNT_EXCHANGE/HEARTBEATS/<lane>.hb` is older than 10 min, once the lane has touched it at least once. The files were created with a 2020 mtime, so an untouched file never alarms.
- **Rule 1, UNANSWERED:** more than 20 min.
- **Rule 2, SILENT:** more than 60 min (was 120).
- **The alert** is as in A301: a modal window with the lane in capitals, a spoken warning and a sound, repeated every 30 min.
- **Coverage:** Codex1–3 and Claude3. Claude4 is added after its Fri 19:00Z reset.

**Lane protocol (0863):**
- touch the heartbeat after every work step;
- run a background heartbeat during any command longer than 5 min;
- use the blocking wait loop, which touches the heartbeat every minute, and never end a turn;
- post a handoff before any planned stop.

**Expected detection time** for a paused lane: about 10–11 min (was 20–120 min).

## A304: two-tier heartbeat watchdog v005; background heartbeat capped (principal: "a stall could be detected in 1 minute if they are check every 1 minute right?") (UTC 2026-10-22 08:00:50Z)

**Why not 1 min:** a working lane can pass several minutes without a touch, while it reasons or runs one long step. A 1-min loud threshold would raise constant false alarms. A detached background toucher would keep the heartbeat alive after a lane stops, and hide the stall.

**Ruled:**
- **Watchdog `STALL_ALERT/lane_stall_alert_c2v005.zsh` `7b079e85`,** pid 9158, replacing v004b. It checks every 30 s.
  - **Soft tier:** a quiet banner, "Check <LANE>", when a heartbeat is more than 5 min old.
  - **Loud tier:** the full alert at more than 10 min (A301 form). The other rules are unchanged (A303).
- **Lane rule (0864):** a background heartbeat is bounded to at most 30 one-minute touches. Unbounded or detached heartbeats are forbidden.

## A305: two-volume storage policy; disk-space alarm (UTC 2026-10-22 10:57:43Z)

**The principal:** "Is there something we can do in advance to recognize that we have 3tb of storage on a second external drive if it should be needed? In addition to the 8tb on the main drive."

**Ruled:**
- **UNT_CAMPAIGN (8 TB) is for the campaign only.** No other program writes there. The campaign cannot span or migrate volumes (Codex3 0674, A256).
- **External1** (2,877 GB free, measured now) carries every non-campaign output: HEADLINE11, S0, the L2 direct batch, the S1 pair, the Phase-1/2 NGC runs, CP-1, and the seal and classifier outputs.
- Claude3 audits every configured output root and produces a two-volume forecast (0865, due Fri 12:00 CDT).
- **At W1 acceptance,** root runs storage_check with both volumes counted (A192 item 5). If the campaign forecast exceeds 85 % of UNT_CAMPAIGN, root decides at once.
- **Disk alarm:** the watchdog `STALL_ALERT/lane_stall_alert_c2v006.zsh` `747f9d55` (pid 63734, replacing v005b) also alerts on free space:
  - loud below 300 GB;
  - soft below 600 GB.

  It watches /Volumes/External1, /Volumes/UNT_CAMPAIGN (once mounted) and the internal data volume (929 GB free now).

## A306: standing principle that bookkeeping conventions yield to wall-clock time; relocation with custody commissioned (UTC 2026-10-22 11:06:29Z)

**The principal (verbatim):** "I just know that if I'm face with spending more weeks of processing or changing a book keeping convention I'd prefer changing the book keeping."

**Standing principle (with A258):**
- When a custody, bookkeeping or record-keeping convention, not physics, would cost material wall-clock time, root changes the convention through a reviewed successor and does not accept the delay.
- Physics, blinding and the integrity of the evidence chain are preserved. The change is disclosed and recorded.

**Applied to storage (A305):**
- No change before W1, so the campaign's identity is not altered right before it starts.
- **Commissioned now: a reviewed "relocation with custody" successor of `storage_check move`.**
  - Finished, accepted campaign call dirs may move from UNT_CAMPAIGN to External1.
  - Each move carries a signed relocation record: the old path, the new path, the volume UUIDs, and byte-equality shas.
  - The cache, ledger and acceptance readers verify those records, so the evidence chain is unbroken.
  - It is adopted at a clean phase boundary before Phase 2 needs the space.
- **Design:** Claude3 now (0866).
- **Build:** a lane after the Oct 27 resets.
- **Review:** cross-family.
- **Target:** adopted before the W1-measured forecast says it is needed, and in any case before Nov 5.

## A307: importer split by sub-component for credit (the principal: Codex1 13 %, Codex3 20 %, Codex2 0 %) (UTC 2026-10-22 11:09:20Z)

**Basis:** the L2 batch needs only the launch-time pieces when it starts (H11 end, about Fri 2–4 pm CDT). The import pieces are needed at campaign planning (Fri night or Sat). Splitting by component keeps each lane's credit on the earliest-needed work.

**Split (0867):**
- **Codex1:** the runtime capture producer, the speculative register writer and the L2_DIRECT envelope. Handoff at about 5 %.
- **Claude3 (author):** the I1 lifecycle/cache, the I2 acceptance entry, and the register binding. It builds from Codex1's state, read-only, in `external_importer_c3/`, with deputy rulings D021–D023 applied.
- **Reviews:**
  - Claude3 reviews Codex1's pieces.
  - Claude4 reviews Claude3's import pieces after its Fri 2 pm CDT reset.
  - Codex3 gives a narrow pass only within its 8 % reserve.
- **Targets:** launch-time pieces reviewed by Fri 12:00 CDT; import pieces review-ready by Fri 18:00 CDT.

**Fallback:** if the launch-time pieces are not ready at H11 end, the batch waits for them (a partial gain). If the import pieces slip, the direct results wait on External1 until the import is adopted.

## A308: use credit fully before resets (principal: "make sure that we fully use lanes when we're close as OpenAI tends to reset earlier than projected typically") (UTC 2026-10-22 11:10:23Z)

- **Reserves** cover critical-path items only, and are released within about 24 h of a lane's expected reset.
- **A standing backlog** of useful deferred work: `lane_backlog_c2/BACKLOG_V001.md`, 8 items, in this order:
  1. relocation with custody;
  2. F5-R2;
  3. the CP-1 QoS successor;
  4. the S1-pair probes;
  5. cw8 N2/N3;
  6. the G26 test successor;
  7. the step7 parent check;
  8. the Phase-2 closure writer.
- **Lanes post `RESET` at once,** early resets included. Claude3 (deputy) assigns from the backlog. All lanes have been told (0868).

## A309: correction to A308 rule 1 (principal: "If the lane is 0%" / "Not if there is still capacity left on it") (UTC 2026-10-22 11:10:39Z)

- **Withdrawn:** releasing reserves before a reset. A lane with capacity keeps its critical-path reserve.
- **The early-reset watch applies to lanes at 0 %** (Codex2 now). They are expected back early, post `RESET` at once, and take backlog work immediately.
- The backlog and the full use of capacity stand (0869).

## A310: no credit floor; rolling handoffs (the principal told a lane to "proceed until it ran out of usage credits") (UTC 2026-10-22 13:39:51Z)

- **The 5 % stop rule is withdrawn** (root's 0858 and others). It stranded credit.
- Lanes work until their credit is exhausted.
- Each lane keeps a rolling, versioned handoff (`handoff_<lane>/HANDOFF_<lane>_V###.md`, exclusive create), updated after every milestone, so an abrupt stop loses nothing.
- Critical-path reserves still hold until their items are done (A309).
- All lanes have been told (0870).

## A311: pre-NGC public snapshot to GitHub (principal: "So wouldn't we want to do the git update today?") (UTC 2026-10-22 14:48:21Z)

**Repo:** `gravacle/universal-network-theory` is PUBLIC. Its last push was 2026-10-08. `UNT_EXCHANGE` (132 GB) has never been in git.

**Plan:**
- Claude3 curates a copy-only snapshot (0872): code, prereg, V005/V006, reviews, certification records, manifests.
- It excludes run outputs, every NGC3198 data file, step-2 outputs and files over 20 MB, and scans for credentials and personal emails.
- Root pushes to a new branch, plus a tagged release, **today, after its 13:00 CDT reset and before the S0 NGC3198 launch, only with the principal's explicit OK** (publishing).

**Purpose:** a server-side timestamp of the predictions and tools that precedes any NGC3198 computation. Commit dates alone are not proof.

## A312: principal approval of the A311 snapshot, with a pre-push validation gate (UTC 2026-10-22 14:49:47Z)

**The principal (verbatim):** "Yes. But check with me before the actual update to github so that we can validate certain data points."

- Approved in principle.
- Root presents the package summary after its 13:00 CDT reset: sizes, categories, scan hits and how each was handled, the key files and their shas, and any data points the principal names.
- **No push before the principal's final OK on that summary.**
- **Timing:** root holds the S0 launch up to about 1 h for the validation. Beyond that, S0 launches and the push follows. It still precedes any NGC3198 read (the seal and scoring come later).

## A313: reproducibility tiers for public release (principal: "Are we providing the data needed to reproduce results, etc.") (UTC 2026-10-22 14:53:24Z)

- **Tier 1, commitment (today):** code, prereg, decisions, certificates, manifests.
- **Tier 2, re-run:** DDO154 inputs plus the environment manifest plus REPRODUCE.md **today**. NGC3198 input files are added **after the seal**, because blinding forbids opening them now; only their paths are listed today.
- **Tier 3, verify without re-running:** run outputs and results on a research archive (Zenodo or OSF, with a DOI), with hashes in GitHub, at S10 and S11.

The GitHub repo is currently about 142 MB. Today's snapshot size is reported by Claude3 (0872/0873) before the principal's check (A312).

## A108 continued

**The principal confirmed at about 00:06Z:** "Please proceed through the completion of Step 2." Root carries on through the seal, the launch and step-2 monitoring, up to the last receipt. Any run failure gets a root ruling (A50 outcome order), and no run is retried automatically.
