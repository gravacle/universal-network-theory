# VERIFY: lens targetfree finding B-2, adversarial verification (verify_targetfree_2)

- **Written:** 2026-10-18T19:31:12Z (`date -u`). A Claude4 helper wrote it, refuting by default. Authority: dispatch 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`), checked under 0592.
- **Object:** `claude_artifacts/miss_reading_prereg_c4/r2/round1/`. All 10 entries of HASHES_R2.txt match `shasum -a 256`, among them:
  - PREREG_MISS_READING_R2.md `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143`;
  - ROOT_ITEMS_R2.md `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f`.

  The object was not edited.
- **Finding under test:** B-2 (SHOULD_FIX) in `checks/targetfree/REVIEW.md`, L66–94.
- **V005 at verify:** `50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477`. It now runs to A92. A snapshot is in `V005_AT_VERIFY.md`. No entry after r2's assembly defines "radial support". A66.2 (L635) is the only rule that uses the term.
- **What was not touched:**
  - No path containing rotmod, Vobs, MassModels or SPARC was opened, and no NGC3198 data table.
  - runs_ext/KMAX_A2F10_C5H_RUN_V001 was not touched, and no `UVT_*` file was read.
  - Nothing was launched, and there was no network.
  - The NGC inputs read were: query ids and radii (slots V003 query block), N-test model numerics, and the registered GL nodes.
  - Python ran with `-I -B`, numpy-free, single-thread env.

## Verdict: CONFIRMED (not refuted). Severity SHOULD_FIX is right. The fix works in direction but needs six refinements (§5).

The finding's core holds from bytes:
- The record of record stores the failing ring's support as a point.
- M-7's "exactly as stored" interval rule therefore flags nothing, or cannot be executed.
- The flagged set depends on a definition that r2 leaves open until the freeze step, after the step-5 predictions exist.

Two wording over-statements in the finding are noted in §3. Neither changes the result.

## 1. Is the quoted r2 text there? Yes.

| quote | file:line | exact bytes |
|---|---|---|
| support | ROOT_ITEMS_R2.md L138 | "the radial support [r_lo, r_hi], exactly as stored in that record;" |
| rule | ROOT_ITEMS_R2.md L140 | "A query q is flagged if and only if r_lo ≤ R_q ≤ r_hi. This is a closed interval, with R_q bound by id." |
| source | ROOT_ITEMS_R2.md L136 | "The record is produced from the production-K_big (32) N1 record of the registered NGC N-test compare" |
| timing | ROOT_ITEMS_R2.md L141 | "The record is registered with the rosters (RUNBOOK_V001 step 4), before any target access" |
| binding | PREREG C-1.4 L126 | "A row carries the flag if and only if the root-pinned flag record of root item M-7 lists it." |
| self-check | PREREG C-9 L371 | "The definition of a ring's radial support decides which rows are flagged. \| Root fixes it before the seal (M-7)." |

Cosmetic points:
- The finding's quote splices L138 and L140 with an ellipsis, and writes "≤" as "<=".
- The quoted words are in ROOT_ITEMS M-7, not in C-1.4.

None of this misrepresents the text.

## 2. Is it defective? Yes. Both possible readings of M-7 fail on the actual record.

**What the record stores.**
- `ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` (`6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9`, pinned by Codex1 0056 `4b67319d…` and recorded in A90, V005 L936–939), L160–162:
  - `"radial_support": {"kind": "sampled_ring", "R_kpc": 10.540847190215317}`;
  - its keys are `[R_kpc, kind]`, so there is no `r_lo` and no `r_hi`.
- The N1 record `K32_RECORDS_COMPLETE_V001_N1.json` (`8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70`, pinned by manifest `cf8dc2c9…`) has **no `radial_support` key at all** (grep count 0). It has only `ring_radii_kpc`, 100 points (L153).
- So under either referent of "that record", no interval is stored.

**The point form is by design:**
- producer `ntests_compare_k32_cxv003.py` (`283193be…`, equal to the compare's producer pin), L2: "Failing ring support is the sampled radius, not an invented finite radial interval.";
- the same file, L26, hard-codes `'radial_support':{'kind':'sampled_ring','R_kpc':radii[i]}`;
- `BUILD_K32_COMPLETE_V001.md` (`b4444eff…`), L9: "Its support is the sampled ring, not an invented radial interval.";
- root's own request was for the support itself, not for an interval. Dispatch 0550 (`5c686ae8…`), L11: "The compare output must list the failing TRUNCATION_SHAPE rings, with S/θ and radial support. The freeze flags the overlapping rows".

**Consequences:**
- **Literal reading (r_lo = r_hi = 10.540847190215317).** No query radius equals it; the nearest are Q25 at 10.04 and Q26 at 11.04. So the flag set is ∅. P10 (L161, "at least one MISS row carries TRUNCATION_SHAPE_RESIDUAL") can never hold, and R-TSR (L207) is vacuous.
  - Synthetic check: over 20,000 random synthetic tier draws, P10 was true 0 times under the point rule. Under the neighbour-ring rule it was true 4,933 times (`runs/TSR_FLAGSET_RECOMPUTE_VT2.json`).
- **Strict-schema reading.** The rule cannot be executed, because the fields do not exist. r2 has no fail-closed stop for this:
  - the §1.1 stops cover only the fields named in §1.1;
  - so whoever writes the flag record at RUNBOOK step 4 must improvise an interval.

**Independent corroboration:**
- Codex1's steps 6–7 rehearsal, `REHEARSAL_COMPLETE_V001.json` (`19807bb3…`), L165: "No sealed TSR flag carrier/radial support rule. P10 only synthetic classification fixture; do not infer physical flagged rows."
- Dispatch 0606 (`dbb80c77…`, 18:59Z, after round 1 was assembled), item 2: "A carrier for the TSR flag and radial support."
- The author's own ACK, Claude4 0091 (`118fab4b…`), row 2: "The K32 compare stores the failing ring's support as a single point (10.5408 kpc) … the point and the midpoint cell flag nothing."
  - So the author has already accepted the fact.
  - The round-1 bytes under review still carry the defective M-7.

## 3. Does the cited evidence say what the finding claims?

Everything material checks out. Two over-statements are noted.

| finding claim | check | result |
|---|---|---|
| compare 6f095f64 stores `{kind: sampled_ring, R_kpc: 10.540847190215317}` | sha and bytes, L160–162 | **confirmed** |
| chain Codex1 0056 → A90 | 0056 pins 6f095f64; A90 L936 "NGC K32 N-tests (Codex1 0056): N_FAIL_N1, tests_read = true." | **confirmed** |
| N1 8867c376: neighbouring rings 9.9018 and 10.9117 kpc | `ring_radii_kpc[14]` = 9.901810628740723, `[16]` = 10.911721936765339; failing ring = `[15]` exactly | **confirmed** |
| Q25 at 10.04 kpc, Q26 at 11.04 kpc | slots V003 (`d3859b42…`) query block: `Rad_text` "10.04" and "11.04", Rad_unit kpc, `float(Rad_text)` == `radius_kpc` | **confirmed** |
| flag sets by definition (lens `runs/TSR_FLAG_SET_BY_DEFINITION.json`) | independent recomputation over all 43 rows (table below) | **confirmed, all 5 rows** |
| "Q25 misses ±0.5 kpc by 0.0008 kpc" | 10.040847190 − 10.04 = 0.000847 | **confirmed** |
| "Any interval chosen later changes the flagged set" | the midpoint cell and ±0.25 kpc give ∅, the same as the point | **over-stated.** Correct form: the set depends on the rule chosen, ∅ / {Q25} / {Q26} / {Q25, Q26} / {Q24, Q25, Q26}. The defect is unaffected. |
| "M-7 places that choice at RUNBOOK step 4, after the predictions exist" | see the timing notes below | **substantively confirmed.** Literally, M-7 places the record's registration at step 4, and C-9 places the definition at the seal. |

**Timing evidence for the last row:**
- M-7 L141 puts the record at step 4.
- C-9 L371 puts the definition "before the seal". A60 (V005 L513) has root rule and seal "before targets are opened, in the freeze step".
- RUNBOOK_V001 L9 (step 1) saves every member's raw forward result before step 4 (L15).
- So under r2, every placement of the choice can fall after the predictions exist.

**Independent recomputation** (`tools/recompute_tsr_flagsets_vt2.py`, `4d6e13e4…`; output `runs/TSR_FLAGSET_RECOMPUTE_VT2.json`, `c2c6c68d…`). Inputs were sha-verified: compare, N1, slots V003, and the registered GL nodes.

| candidate support of ring 15 | interval (kpc) | flagged | kpc = metre? |
|---|---|---|---|
| point, as stored | [10.5408, 10.5408] | none | yes |
| midpoints to the neighbour rings | [10.2213, 10.7263] | none | yes |
| neighbour rings, closed | [9.9018, 10.9117] | Q25 | yes |
| linear-interpolation footprint, open (see §5 R1) | (9.9018, 10.9117) | Q25 | yes |
| two rings each side | [9.0001, 11.6560] | Q24, Q25, Q26 | yes |
| ±0.25 kpc | [10.2908, 10.7908] | none | yes |
| ±0.5 kpc | [10.0408, 11.0408] | Q26 | yes |
| ±1.0 kpc | [9.5408, 11.5408] | Q25, Q26 | yes |

The smallest distance from any query radius to any interval endpoint is 0.00085 kpc. So the kpc and metre comparisons cannot diverge here.

## 4. Is the severity right? Yes, SHOULD_FIX.

**Not BLOCKING:**
- The flag is disclosure-only: "A flagged row is classified by M-T like any other row" (C-1.4 L127; I-5). No tier, count, headline or score changes.
- Target-freeness is unaffected.
- The fix can still be made blind to the predictions, because NGC step 5 has not launched:
  - 0594 L3: "Step 5 launches after the V007 adoption (step 3) and the DDO recalibration (step 4)";
  - A90 L942 leaves a root item open "before any NGC route A/B launch".

**Not NOTE:**
- If root adopts M-7 as recommended, the sealed rule is vacuous or cannot be executed, and A66.2's flag (and 0550's "flags the overlapping rows") becomes dead letter.
- M-7's harmlessness argument is weaker than it states. L145 says "A broader flag cannot ease any reading", yet a flag does two things to a MISS row:
  - it attaches the R-TSR "may reflect the residual cube-corner anisotropy" reading;
  - it allows "consistent" for that row (C-3.2 L207).
- So a definition chosen with the predictions in view is a live steering channel, if a small one, on rows Q24–Q26 next to the INNER/TRANSITION cut.

## 5. Does the fix work, and does it create a new problem?

Fix items 2 and 4 (list the flagged ids in C-1.4, so that the record is a pure lookup) close the channel. No target information is involved: only ids, radii and model numerics. Six refinements are needed for the fix to be complete and to avoid new gaps:

- **R1. Derive the rule; do not pick it.** Item 1 ("fix the support rule from the target-free ring list") names no rule, and the table shows that the choice decides the set. A registered, target-free derivation exists:
  - the 100 N-test rings are bitwise the 100 registered GL4 route-B nodes (`REGISTERED_ROUTE_B_GL_NODES_CX3V001.json`, `ec1dcca5…`; `radii_m/kpc_m` == `ring_radii_kpc` for all 100);
  - the registered observation rule (slots V003 L233) is "HI-weighted mean of R*Omega, then piecewise-linear interpolation of mean onto the supplied 43 manifest radii";
  - so the rows whose frozen value can depend on ring 15 are exactly those with R_q in (r14, r16), which flags **Q25 only**. This is the lens's "neighbour rings" row, and the interval the author proposes in 0091.
  - The point and midpoint rules make A66.2 vacuous.
  - The ±x kpc rules add a free number, which M-1's reasoning and A48 argue against.
- **R2. Bind the list, and fail closed.** The listed ids must be bound to the compare (`6f095f64…`), N1 (`8867c376…`), GL nodes (`ec1dcca5…`) and slots (`d3859b42…`) shas. Add a stop, for example TSR_FLAG_TABLE_MISMATCH, mirroring ZONE_TABLE_MISMATCH (C-1.3 L117). It fires if:
  - the registered compare at the freeze is a different record;
  - it lists different failing rings;
  - or the M-7 flag record (or a v003h field) does not equal the listed set.

  This matters because a successor compare is not excluded. GQ_NGC at M_s 96 is PASS (`GQ_NGC_91_MS96_V001.json`, `be148bab…`), so the M_s 128 recompute is not triggered. But A90 L942 still has a step-5 root item open.
- **R3. Arithmetic wording.** Item 3 says "no metre conversion". That reads against RUNBOOK_V001 L31: "The metre form is the implemented authority" for cut/support comparisons. In practice it does no harm here: all 8 candidates give the same set in kpc and in metres, with a 0.00085 kpc margin. Suggested wording: "computed in kpc from `Rad_text`; the metre form (R_kpc·kpc_m) gives the same set, checked". With the ids listed, the arithmetic is documentation only.
- **R4. Timing (ties to B-1).** "Fixed at the seal" is not enough on its own, because A60 L513 seals "in the freeze step", after step 1 saves the predictions. The M-7 ruling should be made before any step-5 NGC output exists. If root rules later, the r3 rule is adopted as written, with no switching to another option.
- **R5. Sources and checks.**
  - C-1.4 L128 cites "A66; Codex1 0031", the diagnostic, and D-3 (L320–321) cites A66 only. Both should also cite the record of record, A90 / Codex1 0056 / `6f095f64…`, which postdates r2's assembly copy of V005 (`17cb4fd4…`, last entry A89).
  - Any new numbers (9.9018, 10.9117) need NUMBER_PROVENANCE entries, or T4 fails.
- **R6. A48.** State why the chosen rule is consistent with A48: it is the minimal set that is not empty, and the flag never changes a tier. M-7 L145's "broader is safer" argument cuts the other way under A48 for readings.

## 6. Consequences beyond the finding (for the fix round)

- C-9 L366 claims the "flagging after seeing misses" risk is closed ("root-pinned and target-free before the freeze"). That holds for targets. It does not cover predictions, and the record's content is not yet determined. The row should point to the r3 id list.
- r2 has no fail-closed stop for a flag record that lacks an interval. M-12's sealed classifier, built to M-7 as written, would crash or improvise on the real record.
- K-1 does not interact: no TSR number sits in a code span in round 1.

## Files (this folder only)

- `PARTIAL.md`: the progress log.
- `V005_AT_VERIFY.md`: a byte copy of V005 at `50fe0f1c…`.
- `tools/recompute_tsr_flagsets_vt2.py`: the independent recomputation. It verifies its inputs by sha256 and writes with exclusive create.
- `runs/TSR_FLAGSET_RECOMPUTE_VT2.json`: its output.
- `REVIEW.md`: the summary; it pins this file.
- `HASHES.txt`: sha256 of every file here, from bytes.
