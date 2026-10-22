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

**The principal confirmed at about 00:06Z:** "Please proceed through the completion of Step 2." Root carries on through the seal, the launch and step-2 monitoring, up to the last receipt. Any run failure gets a root ruling (A50 outcome order), and no run is retried automatically.
