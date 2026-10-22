# REVIEW — verify_closure_2: adversarial verification of closure-lens finding F2 (round 2)

A helper of lane Claude4, under dispatches 0585 and 0606 with the 0592 refute-by-default pattern. The full analysis is in `VERIFY.md` in this folder; this file is its summary. Nothing outside this folder was edited. Written after 20:46Z (`date -u`; stamps in PARTIAL.md).

## Verdict on F2

- **NOT REFUTED. Severity BLOCKING confirmed.**
- **Fix:** sufficient only with both halves plus the additions below; not sufficient as written.

**Why it stands.** PREREG r2 (`97d5ce33…`) gives OUTER_FAILURE two statements at [C-2] L209. They disagree whenever every non-INVALID OUTER row has an undefined sign: a null ratio by [C-1.1] L119, or a LATE-gate row by [C-4] L324.
- In that case E3 reads TESTED-NEGATIVE under one statement and NOT_NEGATIVE_AT_OUTER under the other ([C-5.3] L358–L359).
- R-MF reads TESTED-NEGATIVE (L250) while its own status tuple reads NOT_ADDRESSED (L241).
- The coverage property [C-2] L212 is false, for OUTER and for INNER.

This reintroduces round-1 BLOCKING L-C01's defect class: the one registered verdict has two triggers that disagree. Root ruled the same item blocking and ordered r3 (V005 A98.2 in `7f552858…`, L956–L959; dispatch 0619 `238858d1…`; Codex2 0490 `3a922168…`).

**Reproduced independently.** `tools/verify_f2_patterns_vc2b.py` → `runs/F2_PATTERNS_VC2B.json`, on synthetic data only:
- U1N, U1L and U1Lc give [P0] only, with the E3 split;
- U2L and U2N give [P0] only;
- late against on-time pairs remove P5, P7, P8 and P9;
- the random sweep gives 6231/20000 definition mismatches, every one with no defined OUTER row.

**Refutation attempts that failed:**
- reading the first sentence as the definition;
- applying L201 to the first sentence;
- the A48 gap-filler;
- M-12 agreement;
- the pre-score stops.

**Partial refutations, recorded as precision corrections:**
- null-ratio rows are practically unreachable on v003g inputs;
- "every gate row is LATE" holds only for gates first registered at RUNBOOK step 4;
- late-gate removals all go against the model, except through U1.

## Items for the fix round (from this verification)

### V2-1 — SHOULD_FIX — F2's fix: "Alternatively" lets root pick a fix that does not close the hole

**Quote.** The F2 fix: "Define OUTER_FAILURE on counts only … and delete 'It holds exactly when one of P1, P2 or P11 holds'. Alternatively, add P14 OUTER_UNSIGNED and P15 INNER_UNSIGNED".

**Defect.** Option (a) alone leaves L212 false, INNER unread, and R-MF TESTED-NEGATIVE while its tuple reads NOT_ADDRESSED.

**Evidence.** The FIXA sweep: 91/20000 L212 failures, 6991 uncovered miss-dominated zones, and 6196 R-MF TESTED-NEGATIVE with tuple NOT_ADDRESSED. With both halves, all of these are 0/20000.

**Fix.** Adopt both halves:
- restate L209 as "…P1, P2, P11 or P14";
- extend L212 with P14 and P15, and assert coverage per zone;
- key R-MF and the E3 readings 2–3 (F1) to P14.

### V2-2 — SHOULD_FIX — [C-4] L324: late rows also ADD patterns

**Quote.** "A late gate can therefore never remove a pattern or create P9."

**Defect.** F2's restatement lists removals only. Late rows also add:
- **P10**, when Q25 is gated late. R-TSR ([C-3.2] L290) then cites a row with no prediction.
- **P13** and zone patterns.
- **P5** with an unsigned OUTER. P5 then imports P1's deficit readings (L284 "as P1") onto rows with no sign.

**Evidence.**
- The P10G → P10L pair adds P10 and P7.
- U1Lt holds P5 with S(OUTER) UNDEFINED.
- The sweep shows P5 with an unsigned OUTER in 35/20000 outcomes, under R2 and under the fix alike.

**Fix.**
- Restate L324 as: "late rows add MISS rows only; relative to on-time registration they can remove P0, P5, P7, P8 and P9, and add zone patterns, P5, P10 and P13, always toward the less favourable reading".
- Bar R-TSR and P7's row-level R-MF from citing a row with no prediction.
- Re-key P5's OUTER readings to the OUTER pattern that holds.

### V2-3 — SHOULD_FIX — [C-4] L322: LATE-ness has no byte carrier

**Quote.** "A root-listed gate registered after any step-5 output value exists is a LATE gate."

**Defect.** M-12 cannot decide from bytes whether a gate is LATE or on time:
- the gate schema `REGISTERED_INVALID_ROW_GATE_CX3V001` has no time field (module `48a1e48a…` L1578, L1713–L1716);
- the producer's gate pin is "optional redundant metadata, never authority" (L1848);
- RUNBOOK_V001 approves gates at step 4 (L15), after step 1 saves the forward results (L9).

**Fix.**
- A gate is on time if and only if its document sha256 is pinned in a root entry stamped (`date -u`) before the first step-5 output exists.
- The seal or freeze entry lists those shas, and M-12 takes the list as input.
- Every other root-listed gate is LATE, including every gate first registered at RUNBOOK step 4.

### V2-4 — NOTE — [C-5.3] and [C-9] L500: a consequence to record so that root rules knowingly

**Defect.** With F2's fix, an OUTER zone whose non-INVALID rows are all late-gate rows reads P14 and TESTED-NEGATIVE, although no OUTER prediction exists. The same rows gated on time read P9 and NOT_TESTABLE (U1L against U1G).

**Fix.**
- Print n_defined(OUTER), the late-gate count and the null-ratio count on the E3 line.
- Add this as consequence (iv) at [C-9] L500, ruled under M-3.

### V2-5 — NOTE — outside F2: [C-I6] L79 and D-4 L451 are stale against V005 A101

**Defect.** A101 (in `70a48f51…`) closes the A90 step-5 LO I1-T precondition as TESTED PASS (Codex1 0066). The text still describes it as to be ruled.

**Fix.** M-6 item 4 needs a revision or a no-change note.

## Rules kept

- No target or observed-velocity data was read. runs_ext/KMAX_A2F10_C5H_RUN_V001 was not read, listed or stat'ed, and no UVT_* file was read.
- There was no recursive content search, no launch and no network.
- Python ran as `-I -B`, numpy only, single-threaded, on synthetic data.
- Writes went only to this folder.
