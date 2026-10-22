# REVIEW — Lens R2-A (CLOSURE): miss-reading prereg r2, round 2

A helper of lane Claude4, round-2 recheck lens R2-A, under dispatches 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`) and 0606 (`dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e`), with the 0592 refute-by-default pattern. Claude4 owns the fix round; nothing in the object was edited. Started 2026-10-18T19:56:24Z; this report written after 20:24Z (`date -u`; stamps in PARTIAL.md).

**Verdict: FAIL — 2 BLOCKING, 5 SHOULD_FIX, 9 NOTE.** Of the 59 closure rows (57 round-1 findings, Codex1 0058, Codex2's prep checklist), **38 are CLOSED, 21 PARTLY_CLOSED, 0 NOT_CLOSED.** The closure table marks all 59 as FIXED/ADDRESSED/ANSWERED (B-7 "FIXED in part"); that over-states 21 rows.

The two BLOCKING items are residues of round-1 BLOCKING L-C01 and SHOULD_FIX A-04:
1. **The binding three-way reading of an outer-row failure is registered only for P1.** P2 and P11 are OUTER_FAILURE (and read TESTED-NEGATIVE), but R-REACH, R-HIST and R-UT1 are not registered for them. This is against A15 E3, A12.3, A20, the slots SA-REACH-01 note and the refuter's better fix. No reason is given.
2. **Undefined-sign rows break the E3 trigger and the coverage property.** These are null-ratio rows and LATE-gate rows. OUTER_FAILURE has two definitions that disagree when S(OUTER) is UNDEFINED, and "a late gate can never remove a pattern" is false. Root has already ruled an r3 for this class: V005 A98.2 and dispatch 0619, from Codex2 0490.

## 1. Bytes verified

**The object, `r2/round2/`.** All 10 entries of `HASHES_R2.txt` match `shasum -a 256` (19:56Z):

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407` |
| CLAUSE_SOURCE_MAP_R2.md | `38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201` |
| ROOT_ITEMS_R2.md | `4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500` |
| NUMBER_PROVENANCE_R2.json | `ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf` |
| INDEX_R2.md | `0d24b8fe778fb704398a7039f579977d92e51dfd152994d6e68048cffa03b926` |
| TARGET_FREE_CHECK_R2.json | `624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9` |
| TARGET_FREE_MUTATION_TEST_R2.json (26/26) | `4445a9bf014e0cabe6d49cd0f45e4df1c388ac7c2c443df0d6f1d3a62214ec02` |
| tools/check_target_free_c4v002.py | `4ae4f7053f18aa13416ad4e3d118d9250a959e72035c6e5f0c5f92305d8511aa` |
| tools/test_check_target_free_c4v002.py | `dc812342fa7c363e71949e3ecb2a206d68786ff5973280cf98909d03dd114f92` |
| tools/make_miss_reading_c4v003.py | `2132078f9779b01d5ad05c01b0280c218d160f6380f75ed5b99af893a1a2f9ab` |

HASHES_R2.txt itself is `2e3cf0c6…`.

**V005, the open addendum, read three times:**
- `991cc242e30eeea5118058e0f60862f7f50f1cb2cf434a85d92f4055413848c8` at 20:00:50Z. These are the assembly bytes. I read the whole file in this version.
- `cf9bbf19eae3d2fb0262c31c3a0af43ecc2f100b9295c4075a591716b6ebb9dc` at 20:10:24Z, which adds A97 and A98.
- `ff7980e8b9b0c9f7552c551fe1507a2689dfc1357c1f0bf0cdb57e3703c7b6ce` at 20:21:37Z, which adds A99.

All three are kept as `V005_SNAPSHOT_<sha8>.md`. All 14 §11 section pins still match in `ff7980e8`. T7 now lists A97, A98 and A99; A98 touches the reading (it orders r3).

**Other sources** (sha256 from bytes):
- V004 `487d4449…` (A14–A17, A20, A21, A27) and V003 `5bef6552…` (A10–A13).
- V001 `6aecf0cb…`.
- Dispatches 0512 `adac97bb…`, 0550 `5c686ae8…`, 0585, 0592, 0606, 0619 `238858d1…` and 0621 `7ab78e6a…`.
- Codex1 0032 `3e8c9fc9…`, 0056 `4b67319d…` and 0058 `fc5af831…`.
- REHEARSAL_COMPLETE_V001 `19807bb3…`.
- Codex2 CHECKLIST_CX2V001 `020ef3f1…`.
- Codex3 0618 `8939c004…`, with its carrier contract `252ef9e1…` and extractor `50c7db5f…`.
- Freeze v003g module `48a1e48a…`, slots V003 `d3859b42…` and RUNBOOK `9557b5aa…`.
- K32 compare `6f095f64…`, K32 N1 record `8867c376…` and GL4 nodes `ec1dcca5…`.
- CURRENT_INSTRUCTIONS `59ada35c…`.

Round 1 was read in full: the three lens REVIEW.md files and all six VERIFY.md files, plus round1/PREREG `6437ea33…` and round1/ROOT_ITEMS.

**Rules kept.**
- No NGC3198 target or observed-velocity data was opened, and no path containing rotmod, Vobs, MassModels or SPARC.
- runs_ext/KMAX_A2F10_C5H_RUN_V001 was not read, listed or stat'ed, and no UVT_* file was read.
- Nothing was launched, and no project calculation was run. There was no recursive content search, and no network.
- Python ran as `-I -B` with the four thread variables set to 1, on synthetic data and target-free records only.
- Writes went only to this folder. `runs/adv_work/` is an aborted first attempt: my own hook refused case directories whose names held deny-list words. It is kept and unused.

## 2. Closure table, row by row

The finding numbers F1–F16 refer to §6.

| row | sev (r1) | claimed | verdict | evidence (round-2 bytes) |
|---|---|---|---|---|
| A-01 | BLOCKING | FIXED | CLOSED | [C-I6] L65–L75: record of record named; gate rule; 0512's actual words; 0512 and 0550 pinned (§11). Record re-verified: N_FAIL_N1, gate OPEN, TRUNCATION_SHAPE_RESIDUAL_ONLY_A66. Refuter residue in F12. |
| A-02 | SHOULD_FIX | FIXED | **PARTLY** | Derived rule correct (Q25 only, verified). No FLAG_TABLE_MISMATCH stop; two sources of truth (F5). |
| A-03 | SHOULD_FIX | FIXED | CLOSED | [C-1.1] L113–L115: NEAR is a flag, with the corrected gloss, and stays a MISS. M-1 (d) added. |
| A-04 | SHOULD_FIX | FIXED | **PARTLY** | P11 and the E3 line were added, but P11 lacks the R-REACH/R-HIST/R-UT1 that the finding's own fix asked for (F1). The trigger is inconsistent for undefined signs (F2). |
| A-05 | SHOULD_FIX | FIXED | CLOSED | [C-4] L302–L315: built-in versus gate; a gate authorizes but does not require; per member (PER_THETA). |
| A-06 | SHOULD_FIX | FIXED | CLOSED | [C-I6] L76–L82; D-4 L444–L451; 0606 tables. Coverage-row nit in F12. |
| A-07 | SHOULD_FIX | FIXED | CLOSED | [C-I6] L85–L89; R-GRID L277 with A27 against; M-13. |
| A-08 | SHOULD_FIX | FIXED | CLOSED | D-1 L417–L426; D-2 L428–L436 (single-chain span). |
| A-09 | SHOULD_FIX | FIXED | CLOSED | [C-4] L330; [C-8] item 6. |
| A-10 | SHOULD_FIX | FIXED | **PARTLY** | A50, 0512 and 0519–0523 are pinned, but the new citations A47, A71 and A80 are unpinned (F3). |
| A-11 | SHOULD_FIX | FIXED | CLOSED | M-6 items 3–4 (section shas; later V005/V006 entries). T7's holes are in F4. |
| A-12 | NOTE | FIXED | CLOSED | The CSM points to the §11 list. The list's derivation is in F3. |
| A-13 | NOTE | FIXED | CLOSED | [C-6.1] L370–L372; M-10. |
| A-14 | NOTE | FIXED | CLOSED | I-4 L60. |
| A-15 | NOTE | FIXED | CLOSED | DT-S1 L263; DT-GEO L260; R-GEFF L279. |
| A-16 | NOTE | FIXED | CLOSED | M-12 L218–L222. A71 is unpinned (F3). |
| A-17 | NOTE | FIXED | **PARTLY** | For NOT_DECIDED, part 2 of the tuple reads "NOT_DECIDED" under C-3 but "OPEN" under §6.3 (F10). |
| A-18 | NOTE | FIXED | CLOSED | The §11 A65 row ends before `**Lanes.**`. Side effect in F4 (X7). |
| B-1 | SHOULD_FIX | FIXED | **PARTLY** | The timing rule was adopted. The refuter's pre-prediction-sha fallback was not, nor were the attestation contents (F6). |
| B-2 | SHOULD_FIX | FIXED | **PARTLY** | As A-02: the refuter's R2 stop was not adopted (F5). |
| B-3 | SHOULD_FIX | FIXED | **PARTLY** | The LATE-gate claim is false and the rule creates undefined-sign zones (F2). §6.3 and M-14 disagree on STAGE0 (F11). |
| B-4 | SHOULD_FIX | FIXED | CLOSED | [C-3] L236–L250 (tuple, precedence); against-cells decidable; descriptive lines L292–L294; M-12 binding. Dead R-MF cell in F13. |
| B-5 | SHOULD_FIX | FIXED | CLOSED | I-7 L91–L92; [C-1.1] L130–L134; [C-3] L247. |
| B-6 | SHOULD_FIX | FIXED | **PARTLY** | T7 misses suffix and amendment headings; in-place edits are invisible (F4). |
| B-7 | SHOULD_FIX | FIXED in part | **PARTLY** | Agreed in part. INDEX still over-claims; identifier- and §-glued numbers are hidden; INDEX is not scanned (F7). |
| B-8 | SHOULD_FIX | FIXED | **PARTLY** | 15 of lens B's T1/T2/T3 cases still pass; the provenance JSON and INDEX are not scanned (F7). |
| B-9 | NOTE | FIXED | **PARTLY** | truncate, mkdir, symlink, chmod and listdir are allowed; the path test is lexical only (F8). |
| B-10 | NOTE | FIXED | CLOSED | Provenance for 0.03/0.51 cites A10 (V003); 0519/0521/0523 are pinned. |
| B-11 | NOTE | FIXED | CLOSED | The test uses 987654.321, 999999 and NGC3198-Q99. |
| B-12 | NOTE | FIXED | CLOSED | The "Flat" sentence is gone; the P1 label reads "expected: A15 E2". |
| L-C01 | BLOCKING | FIXED | **PARTLY** | The verdict line was adopted, but E3 readings 2–3 are missing for P2/P11 (F1), the undefined-sign trigger conflicts (F2), and the dead against-cell remains (F13). |
| L-C02 | NOTE (refuted) | ADDRESSED | **PARTLY** | The tuple was adopted. The refuter's better fix was not, with no reason; DT-T1a timing is unfixed (F10). |
| L-C03 | SHOULD_FIX | FIXED | CLOSED | As A-01. |
| L-C04 | SHOULD_FIX | FIXED | **PARTLY** | P11–P13 added, but the coverage property is false for undefined-sign zones (F2). |
| L-C05 | SHOULD_FIX | FIXED | CLOSED | [C-2] L197–L199: a strict hit majority, and a tie reads miss. |
| L-C06 | SHOULD_FIX | FIXED | CLOSED | As A-03. |
| L-C07 | SHOULD_FIX | FIXED | CLOSED | [C-1.1] L116–L118; [C-8] item 2. |
| L-C08 | SHOULD_FIX | FIXED | **PARTLY** | (a)–(d) are fixed, but the new TWIN_INPUT_DEFECT state is unruled for R-DRIFT, the same class as (d) (F10). |
| L-C09 | SHOULD_FIX | FIXED | CLOSED | Against-cells are defined or removed. |
| L-C10 | SHOULD_FIX | FIXED | CLOSED | As A-07. |
| L-C11 | SHOULD_FIX | FIXED | CLOSED | As A-06 and A-11. |
| L-C12 | SHOULD_FIX | FIXED | **PARTLY** | As A-10 (F3). |
| L-C13 | SHOULD_FIX | FIXED | CLOSED | [C-1.1] L120–L134. |
| L-C14 | NOTE | FIXED | CLOSED | P10 L229; L232. |
| L-C15 | NOTE | FIXED | CLOSED | [C-5.2] L352. |
| L-C16 | NOTE | FIXED | CLOSED | I-7 L94; M-8. |
| L-C17 | NOTE | FIXED | CLOSED | [C-8] L465, L471, L475. |
| L-C18 | NOTE | FIXED | **PARTLY** | M-5 omits `pointwise_envelope.rows[].valid` (F14). |
| L-C19 | NOTE | FIXED | **PARTLY** | The chosen "MISS with sign UNDEFINED" route causes the F2 contradiction. |
| L-C20 | NOTE | FIXED | CLOSED | As A-05. |
| L-C21 | NOTE | FIXED | CLOSED | [C-1.4] L162–L185. |
| L-C22 | NOTE | FIXED | CLOSED | M-1. |
| L-C23 | NOTE | FIXED | **PARTLY** | The scope of P6 and P7, which name no zone, is undefined (F15). |
| L-C24 | NOTE | FIXED | CLOSED | [C-P] L30. |
| L-C25 | NOTE | FIXED | CLOSED | NEAR counts as MISS. |
| L-C26 | NOTE | FIXED | **PARTLY** | [C-9] L487 and L492 claim closures that the bytes refute (F2). |
| L-C27 | NOTE | ANSWERED | CLOSED | [C-9] L500; M-9 median \|r\|. |
| Codex1 0058 | — | FIXED/itemized | CLOSED | Each rough edge has text or a root item: STAGE0 → M-14 (F11); M7 → C-1.4 (F5); M11, M12, P8/M-13, I6 and GEOMETRY are all present. |
| Codex2 checklist | — | FIXED | **PARTLY** | M-12 lists 4 of its 10 case classes (F16). |

## 3. Coverage tables (0585, 0606)

**0585.** Every minimum item maps to clauses that hold it:
- A60 gap rows and cut binding: [C-4];
- A63/A65 stage 0 and STAGE0_GRID_OUTER with its disclosure: DT-U12, D-1, D-2, §6.3, I-1, I-4;
- A64/A66 K_big 32, N3′ and the N1 consequence: I-6, §1.4, P10, R-TSR, D-3, D-4;
- the v003g INVALID-as-miss rule: [C-1.1], [C-4], I-3;
- A81 RI-23: I-6, D-4, plus Codex1 0032.

Deliverables 1–4 are present. One nit: the A64/A66 coverage row does not name 0550 or A90, as A-06's and A-01 F5's fixes asked (F12).

**0606.** All six items map, and the CSM and ROOT_ITEMS tables agree:
- item 1 → §6.3 and M-14 (see F11);
- item 2 → §1.4 and M-7 (see F5);
- item 3 → §5.1(b) and M-11;
- item 4 → the P8 row and M-13;
- item 5 → C-S, M-6 and M-12;
- item 6 → I-6.

## 4. V001's five root items survive in substance

- **M-1:** the tier question; σ-multiples are still rejected as a free number. The recommendation changed to (a′), a flag, for stated reasons.
- **M-2:** cuts 10/30, with the 2.2 R_d alternative kept in the reasoning.
- **M-3:** thresholds fixed at the seal.
- **M-4:** NOT SCHEDULED, with a later prereg needed. "Stay OPEN whatever it shows" is now carried by part 2 of the tuple.
- **M-5:** bound to the adopted freeze, with field maps only and the rules never changed.

## 5. Refuters' better fixes: adopted, or rejected with a reason?

The closure table names a refuter's fix only for A-02 (the derived rule) and L-C01 (the E3 line). No rejection reason is given anywhere.

| refuter | adopted | not adopted, no reason stated |
|---|---|---|
| verify_fidelity_1 (A-01) | F1 (record of record pinned); F2 in substance; F5 mostly | F2's "gate is not launch authorization" sentence; F3's attribution of BLOCKED-for-N_INCOMPLETE/N_NO_RUN; F4 (optional) (F12) |
| verify_fidelity_2 (A-02) | items 1–3, 5–8 (both records named, options with outcomes, open ends, trade-off, 0550/A90, input_files) | item 4: the FLAG_TABLE_MISMATCH stop, and which source governs; both record shas in the §8 header (F5) |
| verify_targetfree_1 (B-1) | items 1, 2, 4, 5 (tag, timing, "anyone", decisions at the freeze) | item 3: the pre-prediction-sha fallback; attestation contents; "step 5 never delayed" (F6) |
| verify_targetfree_2 (B-2) | R1 (derived rule), R4–R6 | R2: the TSR_FLAG_TABLE_MISMATCH stop; R3: arithmetic wording (F5) |
| verify_consistency_1 (L-C01) | item 1 (the E3 line, NEAR counted as a miss) | item 2 (delete the dead against-cell; F13); item 3 (R-UT1/R-HIST/R-REACH on P11, E3 readings 2–3 on P2, P11g; **F1**); item 4 (a root item with options; F13) |
| verify_consistency_2 (L-C02) | — (the lens's tuple was adopted instead) | the whole better fix: status order, closed caveat list, deciding-test map, score-step timing (F10) |

## 6. Findings (most severe first)

### F1 — BLOCKING — PREREG [C-3.2] (L271–L278), with [C-P] L24: E3's three readings are registered only for P1, not for the P2/P11 outer-row failures

**Quote.**
- [C-3.2] L271: "| **P1, P1g, P2, P11** (OUTER_FAILURE; expected: A15 E2) | **R-MF:** … TESTED-NEGATIVE for exactly this scope when OUTER_FAILURE holds."
- L272–L274: "| P1, P1g | **R-UT1:** …", "| P1, P1g | **R-HIST:** a missing Bind-history or collective component …" and "| P1, P1g | **R-REACH:** …".
- L276–L278: P2 and P11 carry only R-S1, R-GRID and R-NAX, besides R-MF and R-DRIFT.
- [C-P] L24 lists "Binding principles (A10, A12.3, A15 E3, A20, …)".

**Defect.** Round 2 makes P2 and P11 outer-row failures: OUTER_FAILURE reads TESTED-NEGATIVE for them. But it registers the other binding readings of an outer-row failure only for P1/P1g (and for P5 through "as P1"):
- finite reach (R-REACH);
- the missing Bind-history or collective component (R-HIST);
- the k = 0 typing (R-UT1).

Under P2 or P11, including the E2-shaped crossing case (excess near 30 kpc, deficit near 44 kpc), these readings are unregistered. After targets they could only be EXPLORATORY ([C-3] L248).

Both round-1 fixes asked for exactly these readings:
- A-04's fix: "Add P11 … to §3 with the R-MF, R-REACH, R-HIST, R-UT1 and R-DRIFT readings as for P1";
- the L-C01 refuter (verify_consistency_1 §5 F-c and better fix 3): P11 "carries R-MF, R-UT1, R-HIST and R-REACH … Now that P2 becomes an E3 failure, the P2 row should also state E3 readings 2–3 explicitly".

The closure rows A-04 and L-C01 say FIXED and give no reason for the omission.

**Evidence.**
- V004 A15 E3, L44–L49 (binding): "An outer-row failure would be TESTED-NEGATIVE … Three readings stay open, each with its own deciding test: 1. a model failure at L=4; 2. finite reach …; 3. a missing Bind-history or collective component".
- V004 A20, L158–L160: "A failure of the NGC3198 outer rows is therefore read two ways: 1. … (UT-1); 2. a missing history or collective component (BH-D)."
- V003 A12 decision 3, L91: "Pre-declared reading of the NGC3198 outer rows. A miss reads three ways".
- The same text is in slots V003 `notes_block_for_manifest.structural_assumptions.SA-REACH-01.pre_declared_reading_verbatim`, which goes into the freeze manifest.
- V003 A10, L38: "Every 120/43 miss is therefore read two ways: as a model failure, or as the missing history/species dependence."
- CURRENT_INSTRUCTIONS L305: "every miss is read two ways: model failure, or the missing Bind-history component".
- Reproduction `runs/READINGS_E3_R2A.json`: P2, P11-crossing and P11-alternating all give E3 TESTED-NEGATIVE, with registered readings {R-DRIFT, R-GRID, R-MF, R-S1, (R-NAX)}. R-REACH, R-HIST and R-UT1 are absent; P1 has all of them.

**Fix.**
1. Change the pattern cell of the R-UT1, R-HIST and R-REACH rows to "P1, P1g, P11".
2. For P2, register them explicitly with status OPEN, or as "NOT_ADDRESSED by an excess (E3 readings 2–3)" with that reason written in the text.
3. Add the refuter's P11g flag (Δ_out < 0).
4. Under A10 SA-BH-01 and CURRENT_INSTRUCTIONS, give P13, P6 and P7 the model-failure and history/species readings (R-MF and R-HIST or R-SPEC), or state why not.
5. Add P2, P11-crossing and P11-alternating to the M-12 agreement suite.
6. Re-mark A-04 and L-C01 PARTLY in the closure table.

### F2 — BLOCKING — PREREG [C-2] L209/L212, [C-1.1] L119, [C-4] L324, [C-9] L487/L492: undefined-sign MISS rows break OUTER_FAILURE, the coverage property and the late-gate claim

**Quote.**
- [C-2] L209: "OUTER is miss-dominated, whatever its sign class. It holds exactly when one of P1, P2 or P11 holds."
- L212: "**Coverage.** Every outcome with at least one MISS satisfies at least one of these: a zone pattern (P1, P2, P11, P3, P4, P12 or P13), or P7."
- [C-1.1] L119: a null-ratio row "is a MISS with sign UNDEFINED. It counts in N_v(Z) and M(Z), and it is left out of m(Z)".
- [C-4] L324: "each LATE-gate row counts as a non-INVALID MISS row with sign UNDEFINED. A late gate can therefore never remove a pattern or create P9."

**Defect.** If every non-INVALID OUTER row has an undefined sign, OUTER is miss-dominated but m(OUTER) and S(OUTER) are UNDEFINED. Then P1, P2 and P11 are all false ([C-2] L201: a condition that uses an UNDEFINED quantity is false). So:
- the two definitions of OUTER_FAILURE disagree;
- the one registered verdict reads TESTED-NEGATIVE under one definition and NOT_NEGATIVE_AT_OUTER under the other;
- the coverage property is false, and INNER has the same hole.

A LATE gate removes P5, P7 or P8 relative to on-time registration, so "can never remove a pattern" is false. [C-9] L487 ("The coverage property holds") and L492 claim these risks closed.

The undefined-sign case is not exotic. In RUNBOOK_V001 steps 1–4, gates are approved after the first pass has saved every forward result. So on the registered procedure every root-listed gate is LATE, and every gate row is an undefined-sign MISS.

**Evidence.**
- `runs/PATTERNS_UNDEFINED_SIGN_R2A.json`, from an independent implementation of round-2 §1.1/§2/§4/§5.3 on synthetic rows:
  - U1, OUTER all undefined: patterns [P0] only; OUTER_FAILURE is True by definition 1 and False by definition 2; E3 reads TESTED-NEGATIVE versus NOT_NEGATIVE_AT_OUTER; coverage False.
  - U2, INNER all undefined: no pattern; coverage False.
  - L1/L2: 12 producer-INVALID INNER rows read as on-time INVALID give {P0, P1, P13, P5}; read as LATE they give {P0, P1, P12, P13}, so P5 is removed.
  - L3/L4: P8 is removed and P7 appears.
- Corroboration: V005 A98.2 (20:04Z) and dispatch 0619. Codex2 0490 found the same blocking item, and root ordered r3: "undefined-sign coverage, OUTER_FAILURE equivalence and late-gate behaviour, all made consistent."

**Fix.**
1. Define OUTER_FAILURE on counts only (N_v(OUTER) ≥ 1 and M(OUTER) ≥ N_v(OUTER)/2) and delete "It holds exactly when one of P1, P2 or P11 holds". Alternatively, add P14 OUTER_UNSIGNED and P15 INNER_UNSIGNED (miss-dominated, S UNDEFINED), each carrying that zone's readings, so that coverage holds.
2. Replace L324's claim with the true one: late-gate rows add MISS rows only; they can remove P5, P7, P8 and P9 relative to on-time registration, and never add a HIT.
3. State that under RUNBOOK_V001 all gates are LATE unless they are registered before step 5 launches.
4. Correct [C-9] L487 and L492.
5. Add U1, U2 and L1–L4 to the M-12 agreement suite.

### F3 — SHOULD_FIX — PREREG [C-S] L19/L21, ROOT_ITEMS M-12 L219 and M-6 L128, PREREG [C-11] L584: A47, A71 and A80 are cited but unpinned; the "read with no change" list is computed, not read

**Quote.**
- [C-S] L19: "A80 put step 5 more than a day away."
- [C-S] L21: "…the pattern of A47 I3."
- M-12 L219: "**Strict parsing (A71).**"
- M-6 L128: "The cited entries are A48, A50, A52, A56, A60, A62, A63, A64, A65, A66, A70, A81, A82 and A90."
- [C-11] L584: "**Read with no change to this text:** A47, … A71–A80, … A91–A96."

**Defect.** The binding seal clause rests on A47 I3, yet A47, A71 and A80 are neither pinned nor in M-6's seal-check list. They are declared "read with no change", a contradiction. This repeats round-1 A-10/L-C12 (A50 cited, not pinned), which the closure calls FIXED.

The cause is the generator: make_miss_reading_c4v003.py sets `unc = [n for n in heads if n not in cited_n]` from its fixed 14-entry CITED list. Every uncited heading becomes "read with no change" by construction, so the list is not an attestation.

**Evidence.**
- `runs/T5_T7_PROBE_991cc242.json` X8: an in-place edit withdrawing A47 I3 passes T5 and T7 on the assembly bytes.
- A99.3 (V005 `ff7980e8`) sets, for the V007 prereg, an entry-by-entry "revised here" / "no change, because …" table.

**Fix.**
1. Pin A47, A71 and A80 by section sha in §11 and add them to M-6 item 3, or drop the citations.
2. Make the generator derive the cited set from the text and fail on any cited-but-unpinned entry.
3. Replace the computed list with an entry-by-entry table that gives a reason for each entry (the A99.3 pattern).

### F4 — SHOULD_FIX — check tool T5/T7 (L130, L151–L152), ROOT_ITEMS M-6 item 4 L129, CSM row B-6: the currency check misses reading-relevant V005 edits

**Quote.**
- CSM B-6: "FIXED. Check T7 lists every heading outside the cited and no-change lists; M-6 item 4."
- M-6: "Check T7 lists them mechanically."
- The tool: `re.findall(r'^## A(\d{1,3})\b', …)`.

**Defect.** `## A81a:` does not match. `## A66 amendment:` is counted as the cited A66. In-place edits of no-change entries are invisible, and so is the A65 trailing block, which the A-18 end-marker leaves unpinned. Lens B's B-6 fix 1 ("in any suffix form") and fix 4 (whole-file sha against the frozen V005 copy at the seal) were not adopted.

**Evidence.** `runs/T5_T7_PROBE_991cc242.json`, run with the tool's own functions on the assembly bytes, where the baseline passes both checks. Six variants pass both T5 and T7:
- X3: A91 edited to withdraw A66.2;
- X4: a `## A81a:` heading;
- X5: a `## A66 amendment:` heading;
- X6: an append at EOF;
- X7: the A65 trailing block changed to "N_PASS is the only input to NGC route A/B.", the A-01 misreading;
- X8: A47 I3 withdrawn.

Only X1 (a new `## A99:`) and X2 (an edit inside A66) are caught.

**Fix.**
1. T7 lists every `^##\s` line and fails on any heading not literally equal to a cited or listed one.
2. Pin each no-change entry by section sha, or have the seal check compare the frozen V005 whole-file sha with the bytes read at the last revision.
3. Pin the A65 trailing block.
4. Add X3–X8 to the mutation test.

### F5 — SHOULD_FIX — PREREG [C-I3] L46, [C-1.4] L178–L183, [C-1.1] stop list, [C-8] L459: the TSR flag set has two sources of truth and no fail-closed stop

**Quote.**
- [C-I3] L46: "the TRUNCATION_SHAPE_RESIDUAL flag rule of §1.4, applied to the pinned production N-test and node records".
- [C-1.4] L178: "**The flagged rows, fixed here by id.**"
- L183: "The flag record … lists the failing rings, the rule above and the flagged ids".
- The §1.1 stops have no flag-table entry.

**Defect.** The classification uses the rule applied to records (I-3), while §1.4 fixes ids and the carrier lists ids. Nothing says which governs, and no stop fires on disagreement. Both refuters asked for that stop:
- verify_fidelity_2 §7 item 4 and §6 gap 3: FLAG_TABLE_MISMATCH;
- verify_targetfree_2 R2: TSR_FLAG_TABLE_MISMATCH, firing on a different compare, different failing rings, or a flag record that does not equal the listed set.

Neither was adopted, and no reason is given. The §8 header lists "flag-record shas", not the N1 record (`8867c376`) or the GL nodes (`ec1dcca5`) that refuter item 1 asked for.

**Evidence.**
- `TSR_FACTS_CLOSURE.json`: the rings equal the GL4 nodes bitwise; (r14, r16) = (9.901811, 10.911722) flags Q25 only. So the text's id is right today.
- Codex3's carrier contract `252ef9e1…` takes literal kpc bounds with inclusive flags, independently of §1.4's ids.

**Fix.**
1. Add the §1.1 stop TSR_FLAG_TABLE_MISMATCH, checked before target access. It fires when the compare, N1 or nodes shas differ from §11, when the failing-ring list differs, or when the flag record's ids differ from §1.4's.
2. State that §1.4's ids govern.
3. Add both record shas to the §8 header.
4. State the comparison in kpc from Rad_text. The metre form gives the same set, with a 0.128 kpc margin.

### F6 — SHOULD_FIX — PREREG [C-S] L21–L22 (and ROOT_ITEMS L13, M-6): the timing fallback covers only root items

**Quote.**
- L22: "If the timing is not met, every root item is adopted exactly as this text recommends, with no option switching, and the report header discloses the deviation."
- L21: "The seal entry attests to this."

**Defect.** verify_targetfree_1 (§4.1 items 2 and 6, §4.2 item 3) showed four gaps, and none was adopted:
- the fallback leaves wording changes and the classifier free;
- "this text" is undefined once a value is read, because no pre-prediction sha is registered;
- the attestation does not list the validity information that was seen;
- "step 5 is never delayed for the seal" is not stated.

No reason is given. This is live: A98 and 0619 order an r3 wording round now, before step 5.

**Fix.** Adopt the refuter's §4.2 item 3:
1. Before the first read of any step-5 value, root registers the sha of the current text and classifier. The fallback applies to that version.
2. Every later ruling or wording change is POST-PREDICTION. It is listed with its diff, and the report also gives the classification under the pre-prediction text.
3. A status that holds only under a later text is EXPLORATORY.
4. The attestation lists the validity facts seen, and each lane that touched the text or classifier after step 5 launched states that it read no step-5 value.

### F7 — SHOULD_FIX — check tool T1–T4 (L17–L20, L71–L73, L85–L96), INDEX_R2 "Checked from bytes", CSM rows B-7/B-8: most of lens B's adversarial cases still pass

**Quote.**
- CSM B-8: "FIXED. NFKC and Cf stripping; extended term, extension, unit and symbol lists; every text file scanned."
- INDEX: "no target term, data-source name, data extension, velocity value or target symbol value appears in any text file (T1–T3)".

**Defect.** Of lens B's 38 round-1 cases rerun on check v002, **24 still pass** (37 did in round 1).

T1 misses:
- C01 `…/data/NGC3198_observed_curve.txt` and C02 `NGC3198_OBSERVED_VELOCITIES.json`;
- C03 `.data` and C04 `.dat_v2`;
- C06 THINGS, de Blok and van Albada, the very names lens B's fix listed;
- C09 "Mass Models" and "Mass_Models";
- C10 a forbidden term in the provenance JSON;
- C11 "V obs" and "v-obs";
- C12 the C5H and UVT_ run names.

T2 misses A06 "km∕s" and A07 "1.48e5 m/s". T3 misses B11 "`v_q` = 778", B12, B13b and B14.

T4 still hides identifier- and §-glued numbers (B06, B07, B09), and it accepts listed values anywhere (A01, A02) and self-declared categories (B17). Three new cases also pass: E01 (a forbidden term in INDEX, which is not scanned), E02 ("778 m/s") and E03 ("`σ_q` = 93.6"). TEXT_FILES (L20) is three files; the provenance JSON is parsed but never scanned.

A targeted scan of the actual round-2 files found none of these patterns, so the object's own PASS stands. The finding is about the check's power and the INDEX and closure wording.

**Evidence.** `runs/ADVERSARIAL_R2_RESULTS.json` (`tools/adversarial_r2_closure_c4.py`): 28 of 42 cases pass, 24 of them from lens B's 38.

**Fix.**
1. Extend the deny-list (things, de blok, van albada, observed_curve/velocit, mass model(s), v obs/v-obs, c5h, uvt_).
2. Treat NGC3198-named paths with .txt/.data/.dat_*/.xlsx extensions as forbidden.
3. Catch the units m/s, cm/s and U+2215.
4. Catch symbol forms in code spans, escaped, indexed, with ≃, and with "is"/"of".
5. Scan INDEX and the provenance JSON in T1.
6. Stop stripping identifier- and §-glued numbers.
7. Add all 42 cases to the mutation test.
8. Reword INDEX ("checked against a deny-list and a listed-value inventory; not exhaustive"), and mark B-8 "FIXED in part".

### F8 — NOTE — check tool hook (L12, L25–L41), CSM row B-9: the hook still allows filesystem changes and tests only the lexical path

**Quote.** "An audit hook refuses any open whose path contains a forbidden term, any write other than --out, and process/network/delete events."

**Evidence.** `runs/HOOK_PROBE_R2_RESULTS.json`:
- under the round-2 `_hook`, `os.truncate` on a canary in this folder succeeded (17 → 0 bytes);
- `os.mkdir`, `os.symlink`, `os.chmod` and `os.listdir` were allowed;
- an open through a symlink was allowed, because the path test is lexical (L30–L33);
- remove, rename and subprocess were refused, which is new.

**Fix.** Also refuse os.truncate, mkdir, symlink, link, chmod, utime, exec and fork, plus listdir/scandir of deny-listed paths, and test `os.path.realpath`. Otherwise state these limits in INDEX.

### F9 — NOTE — PREREG [C-S] L6, and the CSM closure table: the closure claim over-states

**Quote.** "Every round-1 finding is closed or answered in the closure table of `CLAUSE_SOURCE_MAP_R2.md`."

**Evidence.** §2 of this report: 21 of 59 rows are PARTLY_CLOSED.

**Fix.** Re-mark these rows as "PARTLY: <residual>", carry them into r3's closure table, and reword the bullet.

### F10 — NOTE — PREREG [C-3] L242, [C-6.3] L411, [C-6.1] L374, DT-T1a (L259): residual ambiguities in the status tuple (L-C02, A-17, L-C08)

**Quote.**
- L242: "OPEN when the deciding test is NOT SCHEDULED or has not run; otherwise the test's registered outcome."
- L411: "TWIN_INVALID and NOT_DECIDED leave R-DRIFT OPEN."
- L374: "A mismatch reads TWIN_INPUT_DEFECT."

**Defect.**
- After a NOT_DECIDED comparison, part 2 of R-DRIFT's tuple reads "NOT_DECIDED" under [C-3] but "OPEN" under §6.3.
- TWIN_INPUT_DEFECT is not ruled for R-DRIFT.
- For R-ML and R-SPEC, whether DT-T1a has run by the report, and what its part-2 word is, are not fixed.

The L-C02 refuter's better fix (verify_consistency_2 §4) was not adopted, and the closure gives no reason. That fix included the status order, NOT_DECIDED → OPEN, a closed caveat list, a deciding-test map, and the rule "Test statuses are those at the score step…".

**Fix.**
1. In [C-3], map DT-S0G's outcomes, TWIN_INVALID and TWIN_INPUT_DEFECT explicitly. The last two and NOT_DECIDED leave R-DRIFT OPEN.
2. Define DT-T1a's part-2 word as REPORTED (diagnostic) if it has run before the report, otherwise OPEN.
3. Freeze test statuses at the score step.
4. Make the C-3.2 "prior evidence" column the closed list.

### F11 — NOTE — PREREG [C-6.3] L391 against ROOT_ITEMS M-14 L257/L263: the STAGE0 receipt rule is stated two ways

**Quote.**
- §6.3: "…has a FINISHED receipt before the freeze manifest is written, and an adopted successor admits it."
- M-14 rule 1 drops "and an adopted successor admits it".
- M-14 rule 2: "It is adopted exactly when rule 1 says STAGE0 is evaluated."

**Defect.** With every receipt FINISHED but the successor not adopted (for example, its review is not done), the binding text reads NOT_EVALUATED and M-14 rule 1 reads evaluated. The reason for non-adoption is not fixed in advance. The slots record also requires "a root-approved immutable slots successor".

**Fix.** In §6.3, say the prepared successor is adopted mechanically when the receipt rule holds. If its pre-registered review has not passed, STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (SUCCESSOR_NOT_ADOPTED) and R-DRIFT stays OPEN. Mirror this in M-14.

### F12 — NOTE — PREREG [C-I6] L70–L74, CSM "Dispatch 0585 coverage": what is left of the A-01 refuter's fixes

**Quote.** "It is BLOCKED for any of these: … N_INCOMPLETE or N_NO_RUN." and "With the gate BLOCKED there is no route-A/B run and no score, and this document is not applied."

**Defect.** The refuter's fixes F2–F5 are partly unmet, with no reasons given:
- F3: BLOCKED for N_INCOMPLETE/N_NO_RUN sits under "(0550; A66.2–A66.3)", but 0550 lists only failures. It is the producer's behaviour, plus 0512's "Unknown or missing input reads N_INCOMPLETE, never a pass".
- F2: "the gate is not launch authorization" is not stated, although the compare's own `n_route_ab_ruling` says it.
- F4: the disapplication sentence is kept.
- F5 and A-06: the A64/A66 coverage row does not cite 0550 and A90.

**Fix.**
1. Cite the producer and 0512 for the BLOCKED cases.
2. Add the not-authorization sentence.
3. Replace the disapplication sentence with: "If a route-A/B score exists, this document applies in full. PROVISIONAL (N_GATE_NOT_OPEN) if the record of record's gate was not OPEN."
4. Add 0550 and A90 to the coverage row.

### F13 — NOTE — PREREG [C-3.2] L271 (R-MF against-cell), ROOT_ITEMS M-3 L71: what is left of the L-C01 refuter's items 2 and 4

**Quote.** The against-cell "OUTER not miss-dominated, with N_v(OUTER) ≥ 1", and "OUTER_FAILURE := OUTER miss-dominated, of any sign, as the A15 E3 trigger".

**Defect.**
- The row is triggered only by patterns that require OUTER miss-dominated, so the cell can never hold when the row is reported (the refuter counted 0 of 1,679,616). The refuter said to delete it.
- M-3 gives root only option (α). It omits the refuter's (γ), "any failing OUTER row", and the V5 consequence: 2 of 8 OUTER misses read TESTED-NEGATIVE under (γ) and NOT_NEGATIVE_AT_OUTER under (α).

No reasons are given.

**Fix.** Write "—" in the cell, and list (α) and (γ) in M-3 with their consequences.

### F14 — NOTE — ROOT_ITEMS M-5 L109: the bound field list is incomplete (L-C18 c)

**Quote.** "`pointwise_envelope.label` (matched by prefix) and `rows[].band_overlaps_error_bar`;"

**Defect.** I-7 L94 and M-8 require the report to say when envelope rows are invalid. That needs `pointwise_envelope.rows[].valid`, which L-C18 (c) listed. The sensitivity column's "invalid" value needs `sensitivity.rows[].valid`.

**Fix.** Add both fields to M-5.

### F15 — NOTE — PREREG [C-3] L249: patterns with no named zone have no scope (L-C23)

**Quote.** "A reading may cite only rows of the zones named by the pattern that triggers it."

**Defect.** P7 (SCATTERED) names no zone. P6 ("R-MF at all radii"), P8 and P9 name none explicitly. Read literally, their readings may cite no row.

**Fix.** Add: "P6 and P7: all non-INVALID rows; P8 and P9: none; R-TSR: flagged rows only."

### F16 — NOTE — ROOT_ITEMS M-12 L231; CSM row "Codex2's r2 prep checklist": the checklist is only partly carried into M-12

**Quote.** "the boundary cases Codex2's r2 prep checklist lists: half-count ties, the trend split, missing carriers, and status changes of alternatives."

**Defect.** CHECKLIST_CX2V001 (`020ef3f1`) also lists:
- missing, wrong-type or non-finite fields;
- duplicate or reordered ids;
- "wrong reference member/custody";
- the invalid/NEAR boundary and P8/P9 coexistence;
- residual-sign thresholds;
- unregistered flag scope;
- missing twins.

M-12 names only four classes. No §1.1 stop compares the score's `reference_member_id`/`log_index` with the frozen manifest.

**Fix.** List every checklist class in the M-12 suite, and add a stop for a reference-member/manifest mismatch.

## 7. Tested and artifacts (this folder)

| artifact | what it shows |
|---|---|
| `TSR_FACTS_CLOSURE.json` (`tools/tsr_facts_closure_c4.py`) | The compare and N1 record facts; rings equal the GL4 nodes bitwise; the derived rule flags Q25 only; zones 24/11/8, from pinned target-free bytes |
| `runs/CHECK_RERUN_R2A.json` | The object's check, with its hook: target-free PASS; currency FAIL (A97, A98 after assembly) |
| `runs/ADVERSARIAL_R2_RESULTS.json` (`tools/adversarial_r2_closure_c4.py`) | F7 |
| `runs/HOOK_PROBE_R2_RESULTS.json` (`tools/hook_probe_r2_closure_c4.py`) | F8 |
| `runs/T5_T7_PROBE_{991cc242,cf9bbf19,ff7980e8}.json` (`tools/t5_t7_probe_r2_closure_c4.py`) | F3, F4; the 14 pins still match on every snapshot |
| `runs/PATTERNS_UNDEFINED_SIGN_R2A.json` (`tools/patterns_r2_closure_c4.py`) | F2 |
| `runs/READINGS_E3_R2A.json` (`tools/readings_e3_closure_c4.py`) | F1 |
| `V005_SNAPSHOT_*.md` | The three V005 versions read |

**Not tested:** real score outputs or any target, and the semantics of the BH-T1a prereg. Codex2's own round-2 review folder (`review_miss_reading_r2_cx2/round2/`) was not read, to keep this lens independent; its result is known only through A98 and 0619.
