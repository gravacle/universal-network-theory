# CLAUSE_SOURCE_MAP_R2 — where each clause of PREREG_MISS_READING_R2 (round 2) comes from, and how each round-1 finding was closed

Claude4, dispatches 0585 and 0606. One row per clause tag in the r2 text.

**Change classes**, relative to V001 (`6aecf0cb…`):
- **UNCHANGED:** the same rule, possibly reworded.
- **CLARIFIED:** the same intent, with a tie or a vacuous case closed.
- **CHANGED:** the rule changed because of the ruling or finding named.
- **NEW:** not in V001.

"Code" means the v003g freeze module (`48a1e48a…`). Every source's sha is in §11 of the text.

| tag | clause | V001 origin | change | sources |
|---|---|---|---|---|
| C-S | status; the seal and its timing | head, status | NEW: the seal before anyone reads a step-5 output value, validity-only reads until then, and the fallback | A60 (the seal "before targets are opened, in the freeze step"); A47 I3 (validity-only pattern); A80 (step 5 "more than a day away"); 0585; 0606; round-1 B-1; root item M-6 |
| C-P | binding principles | head, principles | CHANGED: OUTER_FAILURE and the E3 verdict line; the A48 gap-filler is phrased against the model, since no reading is adopted (A20) | A10, A12.3, A15 E3, A20, A23, A41, A48; round-1 L-C24 |
| C-I1 | the rows; denominators 43 and 8 | I-1 | CHANGED: the STAGE0 denominator 8 | 0518 item 1; A65; RUNBOOK_V001 step 10; code `_alternative_score_scope`, `_score_members_on_rows` |
| C-I2 | quoted values only | I-2 | UNCHANGED | V001 I-2; 0518 |
| C-I3 | frozen quantities only | I-3 | CHANGED: v003g fields; radii bound by id; the envelope label matched by prefix; the §1.4 flag rule | 0531 (ruled in A56); 0545 (v003g F2/F3); code REFERENCE_RULE, `_score_members`, `_band_rows`; A66.2; 0550; round-1 A-16 |
| C-I4 | the alternatives | I-4 | CHANGED: the six slots V003 alternatives; the recorded distance alternative; the A16.2 contingency | slots V003 `alternatives.declared`; A13; A16.2; 0518 item 5; A65; 0548; round-1 A-14, L-C18 |
| C-I5 | headline | I-5 | UNCHANGED (now cites v003g HEADLINE_RULE) | code HEADLINE_RULE |
| C-I6 | numerics conditions | — | NEW: K_big 32; the N-test record of record; the 0550 gate with 0512's actual words; the certificates and I1-T; M_s 96 as TESTED; the two numerical readings | A64.1–A64.3; A66.1–A66.3; 0512 (N_PASS licenses nothing by itself); 0550 (`n_route_ab_gate`); A52 (NGC I1-T before any N-test is read); A81 RI-22, RI-23; A90; Codex1 0032, 0056; 0546; round-1 A-01, L-C03, A-06, A-07, L-C10 |
| C-I7 | freeze status; the score of record | — | NEW: FREEZE_COMPLETE; the first successful score only; later scores EXPLORATORY; RUNBOOK step 9; PROVISIONAL; NEAR under an incomplete freeze | code FREEZE_COMPLETE / FREEZE_INCOMPLETE, `incomplete_reasons`; RUNBOOK_V001 step 9; A50 (PROVISIONAL, by analogy); round-1 B-5, L-C16 |
| C-1.1 | tiers, NEAR flag, sensitivity band, null ratio, pre-score checks | §1.1 | CHANGED: three tiers plus a NEAR flag with a corrected gloss; NEAR counts as MISS; the sensitivity band in a fixed column; a null ratio is a MISS with sign UNDEFINED; binding pre-score checks; post-target rulings limited | code `_score_members`, `_band_rows`, `_ladder_row` (NON_FINITE_SIGMA_RATIO), `score_after_freeze`; WITHIN_ERROR_RULE; REFERENCE_RULE; round-1 A-03, L-C06, L-C25, L-C07, L-C13, L-C19, B-5; Codex1 0058 (GEOMETRY); root item M-1 |
| C-1.2 | sign | §1.2 | CLARIFIED: sign 0 allowed; UNDEFINED for a null ratio | V001 §1.2 |
| C-1.3 | zone rule and membership by id | §1.3 | CHANGED: membership fixed by id; edge radii; a mismatch stops before target access; the "Flat" sentence dropped | A15 E1, E2; slots V003 `query_block.rows`; manifest `a2936517…`; code `_alternative_score_scope`; 0545 F2; round-1 B-12; root item M-2 |
| C-1.4 | the TRUNCATION_SHAPE_RESIDUAL flag | — | NEW: the derived overlap rule; the formal result; the flagged ids fixed by id (Q25); the carrier | A66.2; 0550; A64.3; A90; Codex1 0056; the K32 compare (`radial_support` of kind `sampled_ring`); the K32 N1 record (ring radii); the registered GL4 nodes (`ec1dcca5…`, bitwise equal to the rings); slots V003 observation rule ("piecewise-linear interpolation of mean onto the supplied 43 manifest radii"); round-1 A-02, B-2, L-C21; root item M-7 |
| C-2 | summaries, trend, OUTER_FAILURE, patterns | §2 | CHANGED: NEAR in M(Z); exclusive dominance (strict hit, ties to miss); OUTER_FAILURE; P11, P12, P13 and the coverage property; P8 renamed and guarded; P10 on non-INVALID rows; trend and median over defined ratios | V001 §2; A15 E3; A60 and code REGISTERED_INVALID_REASONS (P0); A66.2 (P10); round-1 A-04, L-C01, L-C04, L-C05, L-C14; Codex2 r2 prep checklist (P8); root item M-3 |
| C-3 | rules for every reading | §3 rules | CHANGED: the status tuple, with against taking precedence; post-target deciding tests support only through unopened data; scope for every reading; R-MF's verdict through OUTER_FAILURE | V001 §3; round-1 B-4, L-C02, B-5, L-C23, L-C01 |
| C-3.1 | deciding tests | §3 table | CHANGED: DT-U12 is NOT SCHEDULED in full; DT-S1 cites A21; DT-GEO cites A16 item 4, and post-freeze geometry is EXPLORATORY; DT-T1a moves no prediction; new DT-S0G and DT-TSR | 0524; A63; A65.2; A21; A16 (items 1 and 4); A10; A16.3; Claude4 0071 N2; A66.2; round-1 A-15, B-4 |
| C-3.2 | readings by pattern | §3 readings | CHANGED: R-MF under OUTER_FAILURE; prior evidence in its own column; against-conditions decidable at the score step only; ORIGINAL_K dropped from R-GRID (an entropy-K state alternative, not a k-grid one); R-GRID is the in-use T120L grid with A27/A90 evidence against; R-ML reads NOT_AVAILABLE; the onset radius is descriptive; P6 "removing the offset" dropped; P7 reports both readings; P8 a mandatory report; P11–P13 rows; R-TSR with A66.2 evidence against | V001 §3; A15 E2/E3; A17; A27; A41; A42; A63; A65; A66.2; A90; round-1 A-04, A-07, B-4, L-C09, L-C10 |
| C-3.3 | BH-T1a, diagnostic only | §3 BH-T1a | UNCHANGED | A10; A16.3 |
| C-4 | INVALID-as-miss rows | §4 | CHANGED: built-in versus gate reasons; gates authorize but do not require; the reference member's set (PER_THETA); LATE gates count as MISS rows; the cut's truncation radius and mass fraction restored | 0518 items 1–4; 0531 (ruled in A56); A60; A62; code `_authorized_row_registration`, `root_gates` (ROOT_ROSTER_BUILTIN_REASON_MUST_DERIVE_FROM_RULE), `_invalid_registration_ok`; RUNBOOK_V001 steps 1–8; 0545 F5; round-1 A-05, L-C20, B-3, A-09 |
| C-5.1 | A15 E1 comparison | §5 E1 | CHANGED: (a) the named deciding observable, with the Q03–Q15 sub-table; (b) model-internal, NOT_AVAILABLE without a carrier | A15 E1; code (no baryonic field); root item M-11 |
| C-5.2 | A15 E2 comparison | §5 E2 | CHANGED: OUTER_FAILURE, OUTER_NO_MISS, P9, and the INVALID counts per reason | A15 E2; A60; round-1 L-C15 |
| C-5.3 | E3, the verdict line | §5 E3 | CHANGED: one always-reported line (TESTED-NEGATIVE / NOT_NEGATIVE_AT_OUTER / NOT_TESTABLE) with its counts | A15 E3; round-1 L-C01 (its refuter's better fix) |
| C-5.4 | never an adjustment | §5 last item | UNCHANGED | V001 §5 |
| C-6.1 | the twin rule | I-4 ("classified the same way") | CHANGED: the twin exists by construction; a valid twin means `member_valid`; the id check against scope; no NEAR flag | code `score_after_freeze` and the writer/verifier that require alternative members to equal the selected representatives; A65.2; round-1 A-13, L-C08; root item M-10 |
| C-6.2 | NOT_EVALUATED alternatives | I-4 | UNCHANGED in effect | code (the NOT_EVALUATED note text); A13; A16.2; 0518 item 5 |
| C-6.3 | STAGE0_GRID_OUTER | — | NEW: the receipt rule; post-freeze results EXPLORATORY; the comparison rule with median \|r\|; TWIN_INVALID and NOT_DECIDED leave R-DRIFT OPEN; the SENSITIVITY label only when evaluated | A65.1–A65.3; 0548; slots V003 STAGE0 record; code `_alternative_score_scope`, `_score_members_on_rows`; RUNBOOK_V001 L5 and step 10; A63; round-1 B-3, L-C08, L-C17, L-C26, L-C27; root items M-9, M-14 |
| C-7 | disclosures D-1 to D-4 | — | NEW: D-1 with R-LIT/R-MA/background and a corrected antecedent; D-2 with the single-chain range and the stage-0-SE note; D-3 with the flagged and bracketing rows; D-4 with the current numerics records | A63; A65 (incl. "A2's own single chains span −5.20 to −1.76"); A66; 0550; A90; Codex1 0032; A81; round-1 A-06, A-08 |
| C-8 | report format | §6 | CHANGED: header items (classifier sha, timing attestation); the per-row table with flags, the sensitivity column and notes; the E3 line; status tuples; the cut report; the words rule's quoting exception | V001 §6; A63; A65.4; A66.2; round-1 L-C07, L-C17, B-4 |
| C-9 | self-check | §7 | CHANGED: rewritten against the round-2 rules; new closed risks; three recorded consequences | V001 §7; round-1 L-C26, L-C27 |
| C-10 | root items list | §8 | CHANGED: M-1 to M-5 kept and updated; M-6 to M-14 new | V001 §8; `ROOT_ITEMS_R2.md` |
| C-11 | sources | §9 | CHANGED: v003g replaces v003d/v003f; per-entry V005 pins with end-markers; the uncited list computed at assembly; new dispatches, lane posts, node and certificate records | sha256 from bytes at assembly (`HASHES_R2.txt` covers the r2 files); round-1 A-10, A-12, A-18, B-6 |

## Dispatch 0585 coverage

| 0585 item | where it is in r2 |
|---|---|
| A60, gap rows | C-4 (QUERY_OUTSIDE_RETAINED_SUPPORT; cut binding); C-2 (P0 per reason); C-I3 |
| A63/A65, the stage-0 outcome | C-3.1 (DT-U12); C-7 D-1 |
| A63/A65, STAGE0_GRID_OUTER with its disclosure | C-I1, C-I4, C-3.1 DT-S0G, C-3.2 R-DRIFT, C-6.3, C-7 D-1/D-2, C-9 |
| A64/A66, NGC K_big 32, N3′, and the N1 consequence | C-I6; C-1.4; C-2 P10; C-3.2 R-TSR; C-7 D-3/D-4 |
| the freeze v003g INVALID-as-miss rule | C-1.1; C-4; C-I3 |
| A81 RI-23, the conditional NGC M_s 128 | C-I6 (with Codex1 0032: M_s 96 holds, TESTED); C-7 D-4 |

## Dispatch 0606 coverage (the steps 6–7 rehearsal rough edges, Codex1 0058)

| 0606 item | where it is in r2 |
|---|---|
| 1. An evaluated STAGE0 needs an adopted successor | C-6.3 (the receipt rule), C-3.1 (DT-S0G); root item M-14 |
| 2. A TSR flag and radial-support carrier | C-1.4 (the derived rule; Q25); root item M-7 |
| 3. An E1b Newtonian carrier | C-5.1; root item M-11 |
| 4. A P8 C3 consistency carrier | C-3.2 (P8 row: the T120L record of A27); root item M-13 |
| 5. Adoption of the prereg and the production classifier | C-S; C-10; root items M-6 and M-12 |
| 6. I6, the A66 versus 0512 wording | C-I6 (the 0550 gate and 0512's actual words) |

## Closure table for round 1 (57 findings; three lenses, six refuters)

The lens reports are in `r2/checks/{fidelity,targetfree,consistency}/REVIEW.md`, and the refuter reports in `r2/checks/verify_*/VERIFY.md`.

**Refuter outcomes:**
- not refuted: A-01 (BLOCKING), A-02, B-1, B-2 and L-C01 (BLOCKING);
- refuted to NOTE: L-C02, but it is addressed anyway by the status tuple;
- the other 26 serious findings were checked inline by Claude4 against the bytes cited, and all are taken as real.

| finding | severity | disposition |
|---|---|---|
| A-01 | BLOCKING | FIXED. C-I6: the 0550 gate; 0512's actual words; the N-test record of record named; 0512 and 0550 pinned; provenance corrected. |
| A-02 | SHOULD_FIX | FIXED. C-1.4: the derived rule (the refuter's better fix); Q25 fixed by id; 0550 and A90 cited; the carrier pinned among the freeze input files; M-7 states the trade-off. |
| A-03 | SHOULD_FIX | FIXED. NEAR is a flag with a corrected gloss and counts as MISS (C-1.1, C-2; M-1). |
| A-04 | SHOULD_FIX | FIXED. OUTER_FAILURE is sign-agnostic; P11; the E3 verdict line (C-2, C-3, C-5.3). |
| A-05 | SHOULD_FIX | FIXED. C-1.1 and C-4 rewritten: built-in versus gate; gates authorize; the reference member's set. |
| A-06 | SHOULD_FIX | FIXED. C-I6 and D-4 record 0550, Codex1 0032, A52 (I1-T), A90 and the I1-T ruling; 0606 coverage tables added. |
| A-07 | SHOULD_FIX | FIXED. R-GRID restated, with A27 and A90 evidence against; I-6 names two numerical readings; M-13 uses the T120L record. |
| A-08 | SHOULD_FIX | FIXED. D-1 and D-2 made two-sided; the antecedent fixed. |
| A-09 | SHOULD_FIX | FIXED. C-4 restores the cut's truncation radius and dropped mass fraction. |
| A-10 | SHOULD_FIX | FIXED. The §11 sentence corrected; A50 and 0512/0519/0521/0523 pinned; 0.51 and 0.03 cited to A10. |
| A-11 | SHOULD_FIX | FIXED. M-6 items 3–4 (section-sha check; later V005 and V006 entries); check T7. |
| A-12 | NOTE | FIXED. The uncited list is computed at assembly in §11; this map points to it. |
| A-13 | NOTE | FIXED. The twin exists by construction; TWIN_INVALID uses `member_valid` (C-6.1; M-10). |
| A-14 | NOTE | FIXED. The A16.2 contingency reads NOT_AVAILABLE (C-I4). |
| A-15 | NOTE | FIXED. DT-S1 cites A21, DT-GEO cites A16 item 4, and 0.51/0.03 cite A10. |
| A-16 | NOTE | FIXED. M-12 binds A71 strictness and label-prefix matching, and names Codex1's rehearsal classifier as implementation B (rehearsal-only). |
| A-17 | NOTE | FIXED. The status tuple (C-3), with the DT-S0G outputs mapped to R-DRIFT (C-6.3). |
| A-18 | NOTE | FIXED. The A65 pin ends before its "**Lanes.**" line (the end-marker column in §11). |
| B-1 | SHOULD_FIX | FIXED. C-S timing rule; M-6 item 1; validity-only reads; fallback adoption. |
| B-2 | SHOULD_FIX | FIXED. As A-02. |
| B-3 | SHOULD_FIX | FIXED. The STAGE0 receipt rule (C-6.3; M-14); LATE gates count as MISS rows (C-4). |
| B-4 | SHOULD_FIX | FIXED. Status tuple with precedence; every against-condition decidable or moved; R-ML NOT_AVAILABLE; P6 offset removal dropped; onset descriptive; M-12 binding. |
| B-5 | SHOULD_FIX | FIXED. C-I7 score of record; RUNBOOK step 9 restated; post-defect rulings limited (C-1.1); post-target deciding tests (C-3). |
| B-6 | SHOULD_FIX | FIXED. Check T7 lists every heading outside the cited and no-change lists; M-6 item 4. |
| B-7 | SHOULD_FIX | FIXED in part. T4 scans every text file, writes an occurrence census with context, and strips hex only when it contains a letter or is 64 long; INDEX wording narrowed. Still a limit, stated: categories are self-declared and verified by review. |
| B-8 | SHOULD_FIX | FIXED. NFKC and Cf stripping; extended term, extension, unit and symbol lists; every text file scanned. |
| B-9 | NOTE | FIXED. The check runs as its own process with the hook installed; the mutation test installs a hook limited to its work folder. Stated limit: T5 judges target-freeness by path. |
| B-10 | NOTE | FIXED. As A-10 and A-15. |
| B-11 | NOTE | FIXED. Mutation sentinels use implausible values and a non-existent query id. |
| B-12 | NOTE | FIXED. The "Flat" sentence removed; P1's expected label cites A15 E2 only. |
| L-C01 | BLOCKING | FIXED. As A-04, plus the E3 verdict line (the refuter's better fix). |
| L-C02 | NOTE (refuted) | ADDRESSED. The status tuple makes the precedence explicit. |
| L-C03 | SHOULD_FIX | FIXED. As A-01. |
| L-C04 | SHOULD_FIX | FIXED. P11, P12, P13; the coverage property; the P8 guard. |
| L-C05 | SHOULD_FIX | FIXED. Hit-dominated is strict, so the two are exclusive. |
| L-C06 | SHOULD_FIX | FIXED. As A-03. |
| L-C07 | SHOULD_FIX | FIXED. The sensitivity band in a fixed column, never a tier or reading. |
| L-C08 | SHOULD_FIX | FIXED. As A-13, plus the id check against scope; R-DRIFT stays OPEN on NOT_DECIDED and TWIN_INVALID. |
| L-C09 | SHOULD_FIX | FIXED. Against-conditions defined or removed (ORIGINAL_K out of R-GRID; R-ML NOT_AVAILABLE; onset descriptive; P8 a report). |
| L-C10 | SHOULD_FIX | FIXED. As A-07. |
| L-C11 | SHOULD_FIX | FIXED. As A-06 and A-11. |
| L-C12 | SHOULD_FIX | FIXED. As A-12; A50 pinned and listed in M-6. |
| L-C13 | SHOULD_FIX | FIXED. Pre-score checks are binding; post-target rulings are limited (C-1.1). |
| L-C14 | NOTE | FIXED. P10 uses non-INVALID MISS rows; the flagged-row list is a disclosure. |
| L-C15 | NOTE | FIXED. OUTER_NO_MISS defined (C-5.2). |
| L-C16 | NOTE | FIXED. NEAR under an incomplete freeze (C-I7). |
| L-C17 | NOTE | FIXED. Notes column; the quoting exception; the SENSITIVITY label only if evaluated. |
| L-C18 | NOTE | FIXED. The recorded distance alternative; the A16.2 contingency; the M-5 field list. |
| L-C19 | NOTE | FIXED. A null ratio is a MISS with sign UNDEFINED (C-1.1). |
| L-C20 | NOTE | FIXED. As A-05. |
| L-C21 | NOTE | FIXED. C-1.4 gives the rings, the derived rule and the flagged ids. |
| L-C22 | NOTE | FIXED. M-1 no longer says P7 uses NEAR. |
| L-C23 | NOTE | FIXED. A scope rule covers every reading (C-3). |
| L-C24 | NOTE | FIXED. The principle is phrased against the model as registered (C-P). |
| L-C25 | NOTE | FIXED. As A-03. |
| L-C26 | NOTE | FIXED. C-9 rewritten; a post-freeze STAGE0 result is EXPLORATORY, and R-DRIFT stays OPEN. |
| L-C27 | NOTE | ANSWERED. The consequences are recorded (C-9; M-3, M-9); the DT-S0G AGAINST rule now uses median \|r\|. |
| Codex1 0058, the rehearsal rough edges (STAGE0, M7, M11, M12, P8, I6, GEOMETRY) | — | FIXED or itemized. M-14, C-1.4/M-7, M-11, M-12, M-13, C-I6, C-1.1 (an invalid sensitivity row is invalid, not zero-width). |
| Codex2's r2 prep checklist (P8 versus "all hit"; the boundary cases) | — | FIXED. P8 renamed and guarded; the boundary cases go into the M-12 agreement suite. |
