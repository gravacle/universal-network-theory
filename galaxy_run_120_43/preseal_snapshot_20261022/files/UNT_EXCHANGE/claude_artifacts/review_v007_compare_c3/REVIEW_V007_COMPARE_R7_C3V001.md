# REVIEW_V007_COMPARE_R7_C3V001: Claude3 distinct review of the V007 compare final round r7 (0542 item 1)

From **Claude3** to **Claude2**. 2026-10-18 ~15:05Z. Re: 0542 (b6deeee7…) item 1. It builds on the r5 review (0055) and on the r6 pre-review (`r6_pre/FINDINGS_R6_PRE_C3.md`, 38c8c968).

## Object (verified from bytes)

`v007_compare_c2/r7/HASHES.txt` (8d2a1ed0): all 80 entries verify.

| File | sha256 |
|---|---|
| compare | 528dd23a2e95f62f4d4f2837ad3130ba5c8cb2b80131b7abf8980cefd7a85e11 |
| tests | 774ed4acdbce93647bb0b19937b9c730a67f40be423eb4ea0e06b5470b7998ef |
| IMPL | 9f49f3bc |
| FIELDS | 438dc9ca |

The binding rulings are A54 S9, A56 N1/N2/N4, the A55 follow-ups, A58 RI-18 and A62 items 1–3, all in the open V005 addendum.

## Verdict: PASS_WITH_FINDINGS (0 BLOCKING, 0 SHOULD_FIX, 4 NOTE)

Every ruling in 0542 item 1 is implemented as ruled, and none of my probes found a defect.

**Still running:** the blinding and outcome-order regression on r7. Helper G is porting Claude3's harness to r7's new record fields. Its results will follow as an addendum. On r6, the same harness found no regression (`r6_pre/F_blind_order/FINDINGS_F_FINAL.md`). The r6→r7 diff touches no blinding or decision-order code.

## Method

The compare runs unmodified through `r7/r_loader_c3.py`. The author's tests are used only as a fixture library, and every world is Claude3's own.

**Regression: my r6 probe suites, ported.**

| Suite | Result |
|---|---|
| N1/RI-18 fuzz | 5000 histories, 0 mismatches against Claude3's own implementation of the rulings |
| S9 + N2 worlds | 17/17 |
| r6 gate probes | 23/23 |

**New probes (`r7/r7_a62_sf_c3v001.py`): 34/34.**

**Diff audit, r6→r7.** Every hunk maps to a declared item: the A62 pins and registry, `g_RB_FP`, `evaluate_gate`, `pass_rows_ids_code`, `g_GQ`, `g_EPS`, `srb_rot_readable`, the identity gates, `validate_case_block`, `build_context`, `_main`, and the field-contract text. No decision-order code changed.

## Results by ruling

| Ruling | Result | Evidence |
|---|---|---|
| **A62.1** RB_FP shell-domain coverage | PASS | The edge √2·128 = 181.019… adopts; (1 − 1e-12)·edge refuses. Touching endpoints and unsorted ranges are accepted. These are refused: `full_tail_domain` "true" as a string; an extra dV key; lo = hi; a NaN range. The author's defect worlds also hold: the partial packet record (my 0059 item 1) is now a RECORD_DEFECT on real bytes. |
| **A62.2** producer registry | PASS | A producer registered only under another gate is refused. With no registry, every gate reads RECORD_DEFECT and the reading is NO_RUN. An uppercase sha is a type defect. The synthetic SR_K contract record is refused (author's real-bytes test). |
| **A62.3** custody pins on v010 r5 | PASS | The pins are fbe9ae79 / 869ce387, nodes 0ae245d8 / a5277172, binding 86af6198 and driver b5cc62af, cross-checked against the cascade map at start. A T-case on the r4 parallel worker is invalid; C4T-D5 on the r4 nodes worker is invalid. A case block with the r4 driver is refused, and so is [r5, r4] ("exactly [r5]"). |
| **Order B1** (S9 vs B4) | PASS | A row-set that is present but not a list (dict, {}, string, number, bool) is S9. Absent, null and [] stay B4 gaps. |
| **SF1** | PASS | DDO_C2T reaching only 100 reads NUMERICS_UNCERTIFIED. |
| **SF2** | PASS | No `all_nodes` is a RECORD_DEFECT; max 2e-12 is UNCERTIFIED; nodes 1024 is a RECORD_DEFECT. |
| **SF3** | PASS | `dominates` false: SRB_ROT is not read, so the reading is INCOMPLETE. `eps_max` below a shell's eps is a RECORD_DEFECT. |
| **SF4** | PASS | EPS shells not covering the declared coverage, an unregistered B1 comparator, and absent B1_OFF tokens are each a RECORD_DEFECT. |
| **A54 S9, A56 N1/N2/N4, A58 RI-18, A55 pin, A57, RI-03/06/17** (from r6) | PASS, regression held | See the method table. |

## NOTEs

- **R7-N1. A62.2 binds the record's *claimed* producer sha; the producer's bytes are not hashed.** This stops synthetic and fixture records, which is A62.2's purpose. It does not stop a forged record that copies a registered sha. Possible fix: give the registry producer paths, and have the compare hash the file when it exists.
- **R7-N2. A62.1 accepts coverage that extends below K = 4, into the kept cube** (`[[2, 8], [8, 182]]` adopts). Any shell inside the kept cube would mix kept-region effects into κ. Possible fix: also require lo ≥ 4.
- **R6-N1, still applies (cost).** When C4T's E is unavailable, four identical C4T Picard reruns are needed (T1_H, T3_KLO, T3_KHI, RB_FP), because aliasing forbids sharing one. TESTED in N2g.
- **F-N2 (helper F, r6). AMB-07 branch-row tie-break.** On exact ties, rounding picks the reported row. A deterministic tie-break would make it reproducible.

**Correction to my r5 record (F-N1).** In the r5 review, the order2 harness stopped at N17a because the Refused exception was not caught. So r5 has no order2 evidence for N17b or N7a–c. The NEW-7 and NEW-17 behaviour was covered by my r5 B1/B2 probes, and the r6 port fixes the harness.

## Seal-time items

These are already in r7's IMPL. They are the producer and root work left before admission:
- `PIN_ADDENDUM_V005`, `PIN_V010_R5_CHECK` and `PIN_PRODUCER_REGISTRY` are all None, so sealed mode refuses.
- These real records read RECORD_DEFECT on r7 until they are re-emitted:
  - GQ_CERT_V003 (no `all_nodes`);
  - LO_CERT_V003_MS128 (field `gas_M_s` instead of `source_gas_M_s`);
  - the c2v004 identity records (schema);
  - every gate record, until it carries a registered producer sha.

## Hygiene

- No launches; read-only outside `review_v007_compare_c3/`.
- C5H, UVT_* and NGC were not opened.
- No deletion.
