# 0390 author notes, V001: V002 domain correction for the 0384, 0385 and 0387 modules

Author: Claude helper (AUTHOR role). A different helper does the static review. No V001 file was touched.

## Sources (sha256 from bytes)

| Source | sha256 |
|---|---|
| FROM_CODEX/0390_2026-10-15_remove_unneeded_zero_r_coefficient_restriction.md | e831496dcad7b8909a329bf154239603140c4ef305eace89eb47d35d67d68acf |
| helpers/response_packet_audit/POPULATED_EXACT_R_LOCAL_GROUND_DEFECT_HEX_AND_CONTACT_EXTENSION_PROPOSED_V001.md (read-only) | 843b34954d7e2b4eee17f5081af6ca9f5ac6736ba14d375c0e71d1e930628969, which matches the pin in 0390 |

## Why the change applies

**What the source says.** Section 1 keeps the actual four-state H_2(r) with r exact, including r > 0. In the common gauge the chain A0–B0–B1–A1 is connected for every finite r, g > 0 and κ ≠ 0. So H_2(r) has a unique ground χ(r) and a positive local gap. H(2+a) = H(2) + aV holds for every r.

**What the V001 modules already did.**
- They build the complete H(d) from epsilon_r for every needed d, and take χ and e2 from a 4×4 eigh.
- They never use the r = 0 closed forms that the source's section 4 lists as r = 0-only: the X_q reduction, D_±, e_±, ⟨q⟩ = 1/2, the population inverse, and the clock sinusoid.

**What the gate was.** `if not abs(r2) <= ref_tol` was the only place r2 was restricted. Elsewhere r2 is computed, reported, and included in the existing finiteness check. Removing the gate changes no formula, and every other gate stays as it was.

**What V002 does not do.** It does not implement or generalize the r0 scalar or noncommuting q-minus oracle, or the closed hopping D-minus and clock identities. Those keep their r0 scope.

## Every changed line, per module

Line numbers are V001 → V002. These line lists are exhaustive; nothing else changed.

### square_source_coefficient (0384)
1. **L1 → L1, comment.** Header label `v001` → `v002 (task 0390: |r2| gate removed)`.
2. **— → L185–188, added.** The `_new_result` key `"ref_tol_note"` (a constant string) documents that ref_tol is a legacy admitted argument and no longer restricts r2. It sits next to `declared_tolerances` in the output.
3. **L198 → L202–204, string.** `scope` now reads "exact-r pure-flip reference coefficients only (square off-diagonal J and its uniform-source derivatives), not full-parent validity; …".
4. **L254 → L260–263, docstring.** The ref_tol description now says it is a legacy admitted argument, validated finite and ≥ 0, that no longer restricts r2. The exact-r basis is cited.
5. **L272–273 → L281–282, docstring.** The Scope paragraph now uses the exact-r pure-flip reference wording and says "not full-parent validity".
6. **L347–348 → removed, code.** The `|r2| <= ref_tol` failure gate.

### square_spatial_source (0385)
1. **L1 → L1, comment.** Header label `v001` → `v002 (…)`.
2. **— → L239–242, added.** The `"ref_tol_note"` key.
3. **L260 → L264–265, string.** The first clause of `scope` becomes the exact-r pure-flip reference wording plus "not full-parent validity". The rest of the scope string is unchanged.
4. **L321 → L326–329, docstring.** The ref_tol description, as in item 4 for 0384.
5. **L340–342 → L348–350, docstring.** The Scope paragraph.
6. **L416–417 → removed, code.** The `|r2| <= ref_tol` failure gate.

### diagonal_spatial_coefficient (0387)
1. **L1 → L1, comment.** Header label `v001` → `v002 (…)`.
2. **— → L342–345, added.** The `"ref_tol_note"` key.
3. **L370 → L374–375, string.** The first clause of `scope` becomes the exact-r wording plus "not full-parent validity". The rest is unchanged.
4. **L434 → L439–442, docstring.** The ref_tol description.
5. **L453 → L461–462, docstring.** The Scope paragraph.
6. **L533–534 → removed, code.** The `|r2| <= ref_tol` failure gate.

## Confirmation that nothing else changed (AST parse only)

For each module I parsed V001 and V002 and applied three normalizations:
- every string constant and f-string was replaced by "";
- the single `If` whose test is `not abs(r2) <= ref_tol` was removed from V001;
- the single `"ref_tol_note"` dict entry was removed from V002.

**Results**
- The `ast.dump` outputs are identical for all three modules (`AST_EQUAL_after_normalization: True`). Exactly one gate was removed and exactly one note key was dropped per module.
- V002 contains no `If` that tests ref_tol.
- All three V002 files pass `ast.parse`.

**What this means.** Every other change is in comments, docstrings, or the scope and note string constants. The full textual changes are in the three unified diffs.

The following are byte-identical in logic:
- the public signatures (ref_tol is still a required keyword-only argument);
- input admission, including ref_tol's finite and ≥ 0 validation through `_tolerance_input`;
- the r2, mu0 and delta computation and reporting;
- the finite, g > 0, κ ≠ 0 and delta > 0 checks;
- the local blocks, eigh, residual, orthonormality and gap checks;
- every denominator and pos_tol check;
- every formula, jet, history and output gate.

**One kept line.** The rebinding `ref_tol = tol["ref_tol"]` is now unused (0384 L335, 0385 L403, 0387 L521 in V002). It was kept unchanged to keep the diff minimal.

## Deliverables in this directory (created exclusively)

- square_source_coefficient_v002.py, square_spatial_source_v002.py, diagonal_spatial_coefficient_v002.py
- DIFF_square_source_coefficient_v001_to_v002.diff, DIFF_square_spatial_source_v001_to_v002.diff, DIFF_diagonal_spatial_coefficient_v001_to_v002.diff (`diff -u`, V001 → V002)
- this file

## Execution statement

No module was executed or imported. The only Python run on the modules was:
- `ast.parse`;
- the AST normalization and comparison described above;
- a read of the exact-r source.

The V002 files were made as copies of V001 in the session scratchpad, edited only at the lines listed above, and then created here exclusively (noclobber). No network was used, and nothing was written under /Users/bgm/Research/Universal Network Theory.
