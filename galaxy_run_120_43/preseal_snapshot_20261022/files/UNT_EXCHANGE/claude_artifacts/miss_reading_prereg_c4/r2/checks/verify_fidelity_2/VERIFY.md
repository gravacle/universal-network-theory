# VERIFY — adversarial verification of fidelity finding A-02 (verify_fidelity_2)

- Reviewer: a helper of lane Claude4, one of the dispatch-0592 refute-by-default verifiers. Authority: 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`, from bytes) and 0592.
- Started 2026-10-18T19:19:03Z; this file written after 19:36:32Z (both `date -u`).
- Lens report: `checks/fidelity/REVIEW.md`, `41cbea3bb48839fa384b9878a247b6e53adbaeba216dd7d76b5b469e59bc3ed0`.
- The object was not edited. No target, observed-velocity, rotmod/Vobs/MassModels/SPARC path, `UVT_*` path or `runs_ext/KMAX_A2F10_C5H_RUN_V001` was opened, listed or statted. Nothing was launched.

## Verdict

**NOT REFUTED. The core defect is confirmed from bytes.**
- **Severity:** SHOULD_FIX is right.
- **Proposed fix:** the direction is right, but it is **not sufficient as written**. It has three gaps (§6), and a refined fix is in §7.
- **Over-statements:** three secondary claims are over-stated (§2, C-4 to C-6). None of them changes the verdict.
- **Corroboration:** after the round-1 freeze, the author's own posts concede the core point: FROM_CLAUDE4 0090 L35–39 (`226c1c57…`, 18:52:44Z) and 0091 L12 (`118fab4b…`, 18:59:25Z).

## 0. Object and sources (sha256 from bytes)

All 10 object files match `round1/HASHES_R2.txt`:
- PREREG `6437ea33…43`
- CLAUSE_SOURCE_MAP `b105b55d…4b`
- ROOT_ITEMS `1d7af792…7f`
- NUMBER_PROVENANCE `c81b5a7a…32`
- INDEX `6c1919a9…9b`
- TARGET_FREE_CHECK `aab68323…0b`
- TARGET_FREE_MUTATION_TEST `2a8202b8…c1`
- the three tools `85457a43…cc7`, `fc403648…a1` and `8c0d9fc2…6a`

| source | sha256 | used for |
|---|---|---|
| `ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` | `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9` | failing ring; `radial_support`; S_over_theta |
| `ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json` (the N1 record of record) | `8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70` | `ring_radii_kpc[100]` |
| `ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_MANIFEST.json` (pinned in Codex1 0056 L17) | `cf8dc2c9827848685027c0675ee436ee35394a7aa91fd737773451d37f147d53` | maps N1 to the record above |
| `ngc_ntest_eval_cx/ntests_compare_k32_cxv003.py` (the compare producer) | `283193be92330805733f865943b01624f1dfb28f22177d18dc06370d2829fa2d` | how `radial_support` is built |
| `ngc_ntest_eval_cx/BUILD_K32_COMPLETE_V001.md` | `b4444eff6c93e8e6da5a12b3aea65a28f948aa78f56176443a7deb84f8ca12b9` | L9 |
| FROM_CODEX1/0056 | `4b67319dddb4799e71420881f6624fdcd1640cd5f560a4adce06cd2030af72aa` | L7, L16 |
| FROM_CODEX/0550 | `5c686ae8fd82cea995fcdd1ed5bff2d0d688514c45582871cb2b97f231b8b457` | L11 |
| FROM_CODEX/0606 | `dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e` | L7 |
| slots V003 (target-free query block only) | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` | query ids and `Rad_text` |
| freeze v003g | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` | L1658–1660, L3491–3506, L3657–3659, L3778, L3875–3885 |
| RUNBOOK_V001 | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` | steps 4, 5 and 8; L31 |
| V004 (frozen) | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` | L372 |
| V005 (open) | `50fe0f1c…` at 19:20:35Z (newest A92), then `6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c` at 19:34:37Z (newest A93) | A66 L618–638; A90 L934–946 |
| `steps6_7_rehearsal_cx1/REHEARSAL_COMPLETE_V001.json` | `19807bb3bca7279e6af71fee40dfefa4ba474ebcdc1289b06dc4598394c35d36` | rough edge M7 |

**V005 check.** No V005 entry up to A93 rules on M-7 or on the meaning of "radial support". A93 and dispatches 0607–0611 do not touch it. 0610 only queues a later Codex2 review of r2.

## 1. Is the quoted r2 text there?

**Yes, verbatim.**

| quote | where |
|---|---|
| "the radial support [r_lo, r_hi], exactly as stored in that record" | ROOT_ITEMS_R2.md L138 |
| "A query q is flagged if and only if r_lo ≤ R_q ≤ r_hi. This is a closed interval" | ROOT_ITEMS_R2.md L140 |
| "A broader flag cannot ease any reading, because R-TSR stays OPEN (DT-TSR is NOT SCHEDULED) and may cite only flagged rows." | ROOT_ITEMS_R2.md L145 |
| "The definition of a ring's radial support decides which rows are flagged. \| Root fixes it before the seal (M-7)." | PREREG L371. The finding drops the row's prefix "Residual risk (not closed).", which does not change the meaning. |

The binding clause that depends on M-7 is PREREG [C-1.4] L126: "A row carries the flag if and only if the root-pinned flag record of root item M-7 lists it. For each flagged row, the record gives … the ring's radial support".

## 2. Is it really defective? Claim by claim

**C-1. The record of record stores no interval. CONFIRMED, and stronger than stated.**
- The compare output `6f095f64` lists `failing_TRUNCATION_SHAPE_rings[0].radial_support = {"kind": "sampled_ring", "R_kpc": 10.540847190215317}`. Its only keys are `R_kpc` and `kind`.
- The N1 record of record `8867c376` stores `ring_radii_kpc` (100 points). No key carries an interval: a search for lo, hi, edge, support or width returned nothing.
- The omission is deliberate.
  - Producer `ntests_compare_k32_cxv003.py` L2: "Failing ring support is the sampled radius, not an invented finite radial interval."
  - L26 always emits `'radial_support':{'kind':'sampled_ring','R_kpc':radii[i]}`.
  - BUILD_K32_COMPLETE_V001.md L9: "Its support is the sampled ring, not an invented radial interval."
- So M-7's "[r_lo, r_hi], exactly as stored in that record" cannot be met. Any finite interval would be a new root definition, which the producer of record explicitly declined to make.

**C-2. Read as a point, the rule flags no row. CONFIRMED** (§4, RULE0).
- The ring is at 10.540847190215317; Q25 is at 10.04 and Q26 at 11.04.
- The ring minus the Q25/Q26 midpoint is +0.000847190 kpc, so the nearest query is Q26.
- My reproduction matches the lens's R3 output exactly.

**C-3. The M-7 reasoning is unsound. CONFIRMED.**
- The P10 row at PREREG L207 has "consistent with the reading if: P10 holds, for the flagged MISS rows only".
- §8 item 5 (L340) reports each reading as "consistent, inconsistent or OPEN".
- M-7's own premise, "may cite only flagged rows" (also [C-3] L172, "R-TSR cites only flagged rows"), makes the breadth of the flag exactly the scope of R-TSR.
- [C-P] L21 chooses "the reading less favourable to any adopted hypothesis". A broader flag registers a possible numerical cause for more misses, which is the more favourable direction.
- So "a broader flag cannot ease any reading" does not follow.
- **An extreme illustration (hypothetical; not a reading anyone proposed).** The raw φ-spread S/θ in the compare increases strictly over all 100 rings and is ≥ 1 on rings 15–99. Only ring 15 fails formally, because rings 16–99 are judged by C1′. If "support" were taken as the region where the residual exceeds θ, the flag would cover Q26–Q43. That is 18 rows, all 8 OUTER rows among them, and it would put R-TSR beside R-MF for every outer miss. Breadth matters.

**C-4. "Read as a point interval it flags no row, which empties the flag A66.2 mandates." PARTLY OVER-STATED.**
- A66.2 (V005 L635) reads: "Every NGC row whose radius lies within the radial support of a failing TRUNCATION_SHAPE ring is flagged". An empty set satisfies that letter when the support is a point. It is also the producer's explicit semantics.
- The real defect is that r2 neither determines nor discloses the resulting set. §1.4 "At writing" (L128) and D-3 (L321) read as if a live flag on ring 15 exists. If the set is empty, P10 can never hold and R-TSR is registered but vacuous, and r2 does not say so.

**C-5. "Any cell-width alternative is knife-edge." OVER-STATED.**
- It is true for cells built from query spacing: the nearest-query cell, and the ring ± half the local query spacing. Both are decided by 0.000847 kpc.
- It is false for supports built from the ring geometry, with margins of 0.128 to 0.499 kpc (§4).
- Even the knife-edge cases are not a precision or steering risk. Both radii are fixed before targets, and 0.000847 kpc (about 2.6e16 m) is far above double resolution at these radii, so the RUNBOOK L31 kpc-versus-metre caveat does not apply.
- The knife-edge is an arbitrariness concern, not a defect in itself.

**C-6. The finding's own first fix example also empties the flag.** The interval between the midpoints to the neighbouring rings is [10.2213, 10.7263], and it contains no query (§4, RULE1). The finding criticises the point reading for exactly this outcome and does not say that its example has the same result.

**C-7. 0550 is not cited. CONFIRMED.** A grep for "0550" over all seven r2 text and JSON files (PREREG, CLAUSE_SOURCE_MAP, ROOT_ITEMS, NUMBER_PROVENANCE, INDEX and the two TARGET_FREE JSONs) returns 0 in each. 0550 L11 is the dispatch that created the compare's ring/support listing and the freeze flag.

## 3. Does the cited evidence say what the finding claims?

| evidence | check |
|---|---|
| K32 compare `6f095f64` (Codex1 0056) | **Yes.** 0056 L16 pins `6f095f64`, and L7 says "sampled R=10.540847190215317kpc". One labelling imprecision: the finding calls the compare output "the production-K32 N1 record". The N1 record of record is `K32_RECORDS_COMPLETE_V001_N1.json` (`8867c376`, via manifest `cf8dc2c9`). It also stores only sampled radii, so the conclusion is unaffected. |
| Repro R3 | **Yes.** It is reproduced independently with shell, jq and awk (§4). |
| 0550 | **Yes.** L11: "The compare output must **list the failing TRUNCATION_SHAPE rings**, with S/θ and radial support. The freeze flags the overlapping rows TRUNCATION_SHAPE_RESIDUAL." |
| [C-3.2] P10 | **Yes** (PREREG L207). |
| v003g L1658 | **Yes.** L1658 defines `keys = {'schema', 'scope', 'alternative', 'slots', 'query_manifest', 'query_mapping', 'root_gates', 'outer_cut'}`, and L1659–1660 refuse any other key set (`ROOT_ROSTER_SCHEMA_REQUIRED`). A flag cannot ride in the roster. "Must be a separate pinned input" holds for v003g. M-7 option (b), a successor, is the other route. |
| lens report: "rehearsal M7 and 0606 item 2 flag the same gap" (in REVIEW.md, not in the finding JSON) | **Corroborative, not identical.** Rehearsal M7 reads: "No sealed TSR flag carrier/radial support rule … do not infer physical flagged rows". 0606 L7 reads: "A carrier for the TSR flag and radial support." Both note that a carrier and rule are missing. Neither says that M-7's interval rule cannot be applied to the record. |

## 4. Independent reproduction (target-free inputs only; every input sha checked by the scripts)

The scripts are `tools/repro_R3_vf2.zsh`, `repro_R3b_vf2.zsh` and `repro_R3c_vf2.zsh`. Their outputs are `REPRO_R3_VF2_OUT.txt`, `REPRO_R3B_VF2_OUT.txt` and `REPRO_R3C_VF2_OUT.txt`. They use only shell, jq and awk, and read only the compare, the N1 record and the slots query ids/`Rad_text`.

**Structure check.** The 100 N1 rings are the registered GL4 nodes: 25 contiguous panels, uniform in R with width 2.676 kpc, and Gauss–Legendre-4 nodes in s = R². The middle-node residual is 4.1e-15 of the panel width. Ring 15 is node 4 of panel 3, whose R range is [8.028514559, 10.704686079].

| rule (candidate definition of "radial support") | interval (kpc) | flags | smallest margin (kpc) |
|---|---|---|---|
| RULE0: M-7 literal, the stored point read as [R, R] | [10.540847, 10.540847] | none | — |
| RULE1: midpoints to neighbouring rings 14/16 (finding's fix example 1) | [10.221329, 10.726285] | none | 0.181 outside |
| RULE6: GL4 quadrature-weight cell of node 15 | [10.289352, 10.704686] | none | 0.249 outside |
| RULE7: open interval (ring 14, ring 16), the author's 0090/0091 recommendation | (9.901811, 10.911722) | **Q25** | 0.138 inside, 0.128 outside |
| RULE3: query cell (nearest query) | Q26 cell | **Q26** | **0.000847** (knife-edge) |
| RULE4: ring ± half the local query spacing | [10.040847, 11.040847] | **Q26** | **0.000847** at both ends (knife-edge) |
| RULE2: the two bracketing query rows, by id (finding's fix example 2) | — | **Q25, Q26** | 0.499 |
| RULE5: the GL4 panel containing ring 15 | [8.028515, 10.704686] | **Q23, Q24, Q25** | 0.0115 at Q23 |

Seven plausible definitions give **five different flag sets**:
- none;
- {Q25};
- {Q26};
- {Q25, Q26};
- {Q23, Q24, Q25}.

The choice of definition, not the knife-edge, is what matters. Every choice is target-free and can be made before the seal.

## 5. Severity

**SHOULD_FIX is confirmed. It is neither BLOCKING nor a NOTE.**
- **Why not BLOCKING.** The flag is disclosure only: A66.2 says "not INVALID", and [C-1.4] says "A flagged row is classified by M-T like any other row". It changes no tier, no score and no other pattern, because flagged rows stay in M(Z). The flag record is produced target-free before target access (M-7, RUNBOOK step 4), so no choice can be steered by targets.
- **Why not a NOTE.**
  - The binding clause [C-1.4] defers to a record built under a rule that cannot be applied to the record of record.
  - Whether P10 and R-TSR are live, and which rows R-TSR may cite, would be decided outside the sealed text.
  - 0585 requires the N1 consequence to be integrated.
  - 0606 L7 requires a carrier and a radial-support rule before step 6.

## 6. Would the proposed fix work without creating a new problem?

**Mostly, but not as written.** The direction is right: define the support, compute the flagged ids now, state the vacuous case, cite 0550 and A90, restate the reasoning as a trade-off, and pin the record through `input_files`. Three gaps remain:
1. **The wrong record for example 1.** "The neighbouring sampled N1 rings of the same record" cannot be computed from the compare record `6f095f64`, which lists only failing rings. The neighbour radii are in the N1 record of record `8867c376` (`ring_radii_kpc`). The fix must name both records and both shas.
2. **The examples' outcomes are not stated.** Example 1 flags none and example 2 flags Q25 and Q26. Root's choice therefore decides whether R-TSR is live at all. The fix offers both as "for example" without saying so. The author's own option (RULE7) gives a third answer, {Q25}.
3. **A possible second source of truth (a new problem the fix can create).** §1.4 L129 says "The flag record follows the formal reading, never this paragraph." If the flagged ids are also listed in §1.4, as the fix proposes, the text and the record could disagree, and nothing says which governs.

**The `input_files` route works.**
- `_pin_files` (L3491–3506) accepts any regular, non-empty file.
- At verification, v003g re-hashes every `input_files` pin from bytes and refuses a mismatch (L3875–3885).
- RUNBOOK step 5's list of bytes that must be retained (L16) should name the flag record.
- **Optional.** The manifest's `notes` (L3778) are free-form apart from the required keys and the FORBIDDEN-name scan (L3657–3659, L190–199). A copy of the flag table there would satisfy A66.2's "in the freeze manifest" literally. Keys such as `query_id`, `ordinal`, `R_kpc` and `S_over_theta` do not hit FORBIDDEN.

## 7. Refined fix (for Claude4's fix round; the object is not edited here)

1. **M-7 inputs.** Name the inputs exactly:
   - the registered compare `6f095f64…`, for the failing ordinals and S/θ;
   - the N1 record of record `8867c376…`, for `ring_radii_kpc`.

   Record both shas in the §8 header.
2. **M-7 options with their outcomes, computed now from target-free bytes.**
   - (i) The point, which is the producer's semantics, gives no rows.
   - (ii) The open interval between the neighbouring rings gives Q25.
   - (iii) The two bracketing query rows, by id, give Q25 and Q26.

   Mark the query-spacing cells as rejected (knife-edge at 0.000847 kpc). Recommend one option. Label the definition "fixed after the N1 diagnostic, before any target" (the A66 precedent).
3. **The rule stated without ambiguity.** State the rule by ordinals or ids, with explicit open or closed ends. Take the union over failing rings. Add a tie rule for a ring exactly at a query radius.
4. **§1.4.** List the expected flagged ids (or "none") together with both record shas. Make the list binding by adding a stop, FLAG_TABLE_MISMATCH, analogous to ZONE_TABLE_MISMATCH (§1.3, L117), and replace "never this paragraph". If the set is none, add: "P10 cannot hold; R-TSR is registered but vacuous; D-3 still discloses the residual."
5. **The reasoning as a trade-off.** A broader flag means more disclosure. It also widens R-TSR's "consistent" scope, because R-TSR cites only flagged rows and P10 makes it consistent on flagged misses. Under [C-P]/A48, the narrower set is the less favourable reading. Root rules.
6. **Citations.** Cite 0550 (L11) and A90 (V005 L946, "The A66 consequence applies at step 5"). Pin both in §11.
7. **Carrier.** Pin the flag record through `write_freeze_manifest` `input_files` at step 8, and add it to step 5's retained bytes. Optionally, copy the table into `notes`.
8. **Follow-ons.**
   - Add NUMBER_PROVENANCE entries for any new number or id.
   - Re-run the target-free check.
   - Turn the [C-9] L371 residual-risk row into a closed row.

## 8. Refutation attempts that failed

- **Is "radial support" defined somewhere else, so that M-7's interval exists?** No. A66 is the only source; V004 has only the TRUNCATION_SHAPE ring set, "12 rings (1.5–10.5 kpc)" (L372). 0550 asks for "radial support" without defining it. The producer chose the point and said why.
- **Is the N1 record different from the compare output, and might it carry intervals?** It is a different file, `8867c376`, and it also carries points only.
- **Does "R-TSR stays OPEN" make the breadth harmless?** No. P10's "consistent" column, §8's vocabulary, and the cites-only-flagged-rows scope all make breadth matter. The lens's NOTE A-17 (the ambiguity between consistent and OPEN) does not remove this, because either reading lets a broader flag register a numerical cause for more misses.
- **Has root already ruled M-7 (V005 through A93; dispatches through 0611)?** No.

## 9. Compliance notes

- **Python.** `-I -B` with the four thread variables was used only to list keys and print id/radius fields of target-free records: the slots query block, the structure of the CUBE32 and C1PRIME annotated records, and the N1 record keys. No velocity field was printed, and no project calculation was run. The reproductions use shell, jq and awk.
- **zsh.** One command contained `echo ====`. zsh tried `=`-expansion, printed "=== not found" and stopped; nothing was written. It was not repeated.
- **Writes.** Only inside `checks/verify_fidelity_2/`.
