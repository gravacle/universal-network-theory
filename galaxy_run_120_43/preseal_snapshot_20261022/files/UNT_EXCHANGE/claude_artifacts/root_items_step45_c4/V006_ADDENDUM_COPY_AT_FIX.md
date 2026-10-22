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

## A108 continued

**The principal confirmed at about 00:06Z:** "Please proceed through the completion of Step 2." Root carries on through the seal, the launch and step-2 monitoring, up to the last receipt. Any run failure gets a root ruling (A50 outcome order), and no run is retried automatically.
