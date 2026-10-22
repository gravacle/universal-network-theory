# REVIEW — verify_fidelity_1: fidelity finding A-01

Written 2026-10-18T19:31:04Z (`date -u`). The full evidence, refutation attempts and line references are in `VERIFY.md` in this folder.

**Verdict: NOT REFUTED. A-01 is CONFIRMED, at severity BLOCKING.**

**What is wrong.** PREREG [C-I6] L56 reads: "Under the 0512 ruling logged in V005, only N_PASS is an input to route A/B. So any other outcome … also gives no route-A/B run." L57 adds: "With no route-A/B run there is no score, and this document is not applied."
- **It mis-cites 0512.** 0512 L16 reads: "`N_PASS` licenses nothing by itself. It is an input to the NGC route-A/B step." V005 L1269 reads: "N_PASS is only an input to NGC route A/B." r2 has turned "N_PASS is merely an input" into "N_PASS is the only input".
- **It contradicts L54 and A66.2.** V005 L634 reads: "N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block NGC route A/B." 0550 L10 says the same, and 0550 is cited nowhere in r2.
- **The realized case triggers it.** The K32 compare `6f095f64` reads N_FAIL_N1 with `n_route_ab_gate` OPEN, for the reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66 (A90, V005 L937–L940).
- **Every reading inherits it.** [C-P] makes every reading conditional on I-6.
- **Nothing in r2 resolves it.** r2 has no precedence rule, and its A48 clause covers only silence.
- **The contradiction was found independently** by Codex1's rehearsal (`19807bb3`, rough edge I6) and by 0606 item 6.

**Severity.** BLOCKING is right. As sealed, the text would mis-state a root ruling, and the clause that decides whether the document applies would contradict itself on the live case. After the seal, the only remedy would be a root ruling made once the score is known.

**Fix: correct in substance, but not sufficient as written.**
- **F1 (required).** Pin the NGC N-test compare record of record at the seal: `K32_COMPARE_COMPLETE_V001.json` (`6f095f64…`; producer `283193be…`), or a successor that root registers before any target is opened.
  - Several compare records exist. `K16_COMPARE_COMPLETE_V001` (`8ff95be3…`) has no gate field, and the K32 partials read BLOCKED.
  - Without the pin, the fix's "registered compare's gate" leaves a choice of record open until score time.
- **F2 (required).** Say the gate is necessary, not sufficient: "OPEN only for …", plus the record's own "this gate is not launch authorization", plus the separate step-5 conditions such as the A90 LO I1-T ruling.
- **F3 (required).** Attribute exactly:
  - 0550 and A66.2–A66.3 rule which failures block;
  - BLOCKED for N_INCOMPLETE and N_NO_RUN is the producer's behaviour (L18–L19), consistent with 0512's "never a pass".
- **F4 (optional).** Replace L57 so that an existing score is never disapplied: label it PROVISIONAL (N_GATE_NOT_OPEN) instead.
- **F5 (housekeeping).**
  - Add T4 provenance entries for new tokens such as "0550".
  - Fix the map row and the coverage row.
  - Pin 0512 and 0550 in §11.

**Accuracy nits in the finding (verdict unchanged).**
- "Inverts" is loose; the scope of "only" is transposed.
- The explicit allowance is in the parent bullet L54.
- The V005 line numbers L916 and L1245 refer to `0753f2d8`. They are L940 and L1269 in `50fe0f1c`, and L946 and L1275 in the final read.

**V005 final read** (19:31:48Z): `6145a1f9…`, which adds A93 (NGC cx3r007 accepted; the step-5 launch registry). Nothing about the N-test gate or I-6 changes, and the A64, A65 and A66 pins still MATCH.
