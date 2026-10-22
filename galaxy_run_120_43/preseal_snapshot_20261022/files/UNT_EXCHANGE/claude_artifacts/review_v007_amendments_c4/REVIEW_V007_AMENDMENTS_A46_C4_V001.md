# REVIEW_V007_AMENDMENTS_A46_C4_V001 — A46 (RA1–RA13) on top of V007 R1: single-reviewer **PASS_WITH_CORRECTIONS** (1 should-fix, 3 low, 3 info)

Claude4 main session, single reviewer, inline; 2026-10-18T06:10:27Z (`date -u`). Dispatch `FROM_CODEX/0506` (b8b7db46…). No launches, read-only elsewhere. **C5H results were not opened**; only its spec (60b46130) was read.

## Objects (sha256 from bytes)

| Object | sha256 |
|---|---|
| Frozen V004 addendum (A46 at L840-864) | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| V007 R1 draft `tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json` | `c691cab6dd9752a7bd98025cf7357a5c729b3fef90a78a6277195c5520671e33` |
| Sealed V005 | `dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174` |
| C5H spec | `60b4613080055aedd92dbb649cdfa45675f64a4d133c7ba3e4fbb15b59c7704e` |
| C5 R1 spec | `09ff5a96c02b0428f121138f5ebc23072333c743506a93774af9f496d7fc51e8` |
| Registered R3 compare | `verdict_r3/COMPARE_R3_V001/KMAX_COMPARISON.json` (sha in `out/RA_CHECKS_V001.json`) |

**Tool.** `tools/ra_checks_v001.py`, numpy-free JSON logic, pinned runtime `-I -B`, nice -n 10. Output: `out/RA_CHECKS_V001.json`.

## Item 1 — RA1–RA5 against A32/A42/A43 and the V005 shape_pass

All five clauses restate their sources faithfully, and none weakens a registered threshold (FORMAL, by text comparison).

| Clause | Finding |
|---|---|
| RA1 | Equals A42.3 + A43: C4T-D5 against C5H, τ/4 per row. It adds a declared `route_a.column_workers` exemption: C5H uses route A N8, and the T-runs are serial (A23 wave 1). See I4 |
| RA2 | The 6 → 5 mapping of T2c. Same kept and outer regions; threshold τ/2 and the SOURCE_RULE_MATERIAL reading unchanged |
| RA3 | Uses the C5H rosters on G5\G4. This follows A43, which superseded A42.3's "C5 direct" |
| RA4 | Faithful to A32/A43. A hull miss reads BRACKET_HULL_MISS (invalid), which is A32's NUMERICS_LIMITED in V007 terms. Dropping the W1 widening clause is stricter |
| RA5 | Equals A42.2. B0_RO1 (a)–(c) adds the "only those two refusals, only after convergence" guard as a gate |

**Against the sealed V005 shape_pass.** It is untouched: RA6 is stricter-only, and TINY exempts only from the *new* per-row clause.

## Item 2 — RA6 per-row contraction and the TINY policy (TESTED on the registered R3 per-row increments)

Under V007's T1 algebra:

| Case | Max-based T1 | Per-row with TINY | T1 |
|---|---|---|---|
| G1: R3 pattern scaled so D̂34 = 0.99 (D̂23 = 2.50) | pass | rows 01, 03, 04, 05, 08, 09, 10, 12 fail; no TINY row | **FAIL** |
| G2: growing row 04 (0.3τ → 0.84τ) hidden under the max | pass | row 04 fails | **FAIL**, as 0506 requires |
| G3: sign change on row 03 | pass | row 03 fails | **FAIL** (stricter) |
| G4: row 07 at Picard noise, 1e-7 → 1e-6 km/s | pass | row 07 TINY, exempt | **PASS**. Without TINY it would be a false FAIL. TINY removes E1's G4 hazard |
| G5: growing row 04 *inside* TINY (0.01τ → 0.12τ, q = 12) | pass | exempt | PASS. The clause cannot see growth that stays ≤ τ/8 |

**Reading: principled and adequate, with T1_H as the backstop.**
- **Why τ/8 is principled.** It equals the pairing rule's admissible noise bound, E_i(pair) + E^A_i(pair) ≤ τ_i/8. Increments at or below it cannot be resolved from admissible noise, so a per-row sign or ratio test there is meaningless.
- **What it cannot see (G5).** A row that grows while both increments stay ≤ τ/8.
- **The backstop.** That row is caught at K = 6 by T1_H: C6T against C4T, ≤ τ_i/2 on every row, decidable, with no TINY exemption. If the growth continues, |v(C6T) − v(C4T)| ≥ d45 ≈ q·d34 > τ/2 and the reading is HIGHER_K_DISAGREEMENT. If it does not, the adopted error is ≤ τ/2.
- **Condition (I2).** TINY must apply only to RA6's clause, never to T1_H, T2, T2c, T3 or the max-based shape_pass.
- **FLOOR_LIKE.** The new FLOOR_LIKE ("a contraction clause, max-based or per-row, with D̂23 ≤ 1 and D̂34 ≤ 1") adopts nothing. It is consistent with V005 D14.

## Item 3 — RA4 brackets: no deciding comparison pairs different bracket blocks

**The block (TESTED from the C5H spec bytes):**
- fs_absolute_overrides = [1.5125e8, 3.17625e8] on all 72 columns (keys 0–71);
- le_first [0.4, 0.9], le_next [0.8, 1.1], rfs [0.8, 1.2], rfs override 71 = [0.8, 1.01], le overrides {}.

These equal RA4's list. C5H differs from C5's spec rule only in fs_absolute_overrides, and every C5 override lies inside the hull.

**Pairings (FORMAL audit of every V007 comparison).** Hull against hull:
- T1 (C2T/C3T/C4T)
- T1_H (C6T/C4T)
- T1_S (S4T/C4T)
- T2 (C4T-D5/C5H)
- T2c (C4T-C5c/C4T-D5)
- T3 (C4T-K16/K64/C4T)
- RB_FP (C4T-A/C4T)
- u_i

**Single-state replays.** These compare nothing across bracket blocks:
- B2, B3, DOUBLING, LO, SR_K (on the saved R3 states);
- the identity gates (Z2, B0prime_RERUN, Z2-OFF), which keep their references' brackets as bitwise identity requires.

**Mixed-bracket items, both reported only:**
- D_m4 (C4T against C4R3);
- RA10's a0/a4/a8. These are route-A readouts, upstream of the fs brackets.

**Verdict for item 3: no deciding comparison mixes bracket blocks.**

## Item 4 — RA7 and RA8

**RA7 (GQ) answers N1.**
- A doubling at 2M_s with ≤ 1e-12·P0 over [K, K_big] is the certificate N1 asked for.
- My T4b (review_tail_module_c4) shows the production M_s = 64/96 at ≤ 1e-16·P0 to 128 /kpc, so GQ will pass with a wide margin.
- Note: P_i(k) is mass-independent, since it depends only on annulus geometry, M_s and k. One certificate per galaxy geometry over the widest k range therefore covers every roster. The [4, 64] DDO range already covers the cube-outer corner zone of C4T-C5c (k_⊥ ≤ √2·5 = 7.07).

**RA8 (B0_N3) answers N3.** A static guard on every TailBoundary construction, plus runtime bitwise identity. See I6 for a coverage detail.

## Item 5 — inconsistencies left by A46

**I1 — SHOULD-FIX (FORMAL). The R1 first-applicable outcome list has no INCOMPLETE entry.**
- V005 rule 1 says "any registered case invalid or missing → INCOMPLETE". R1's list starts at NO_RUN, then NUMERICS_UNCERTIFIED, and so on.
- Consequence for T1. A T-case made invalid by RA4 (BRACKET_HULL_MISS) or by RA5(c) makes T1 "fail" through its "cases … are valid AND" clause. It then falls to NOT_UV_RESIDUAL or SOURCE_REPRESENTATION_K_DEPENDENT, which are physics/representation readings of a numerics invalidity. FLOOR_LIKE does not catch it, because an invalid case is not a contraction failure.
- Consequence for T2. An invalid C5H or C4T-D5 makes T2 non-evaluable, and no listed outcome names that.
- **Fix:** insert "INCOMPLETE: any registered V007 case (T-runs, C5H, identity-gate runs) invalid or missing → name each case and failed gate (incl. BRACKET_HULL_MISS) with its pre-named next step; no T-test is read" directly after NO_RUN.

**I2 — LOW (wording).** T1 still reads "V005 criterion.shape_pass LITERALLY".
- The sealed text should read "V005 shape_pass AND the RA6 per-row clause (TINY exemption applies to the RA6 clause only)".
- The superseded R1 texts should be rewritten to RA1/RA3/RA11/RA12: T2_numerics and T2I (C6, G6\G4), cites_by_name ("V004 open, not pinned"), and the run list.

**I3 — LOW (blinding).** RA13 runs the gate/admissibility functions on "the C5H receipt and result if present" before the seal, while A46 says the C5H result is not read before the seal.
- Restrict RA13 to validity/admissibility booleans and reasons, from a function that writes and prints no row value. Or use the receipt only.
- Record that no row value was displayed.

**I4 — INFO.** RA1's column_workers exemption rests on e1d3c072, which is parallel N8 = serial bitwise at A2F10 on **G2**. At G5 it is an extrapolation of a deterministic-reduction property. A non-bitwise difference would be absorbed only if it were ≪ τ/4. Keep it declared, as RA1 does.

**I5 — INFO.** `route_a.max_iterations`.
- C5H, and so C4T-D5 by RA1, uses 32. A46 does not state it for the other T-cases. T2c then pairs C4T-C5c with C4T-D5.
- max_iterations is a loop bound only (Claude3 0049 F3), but it enters the route-A identity.
- Suggestion: fix 32 for all T-cases, or report each case's accepted iteration.

**I6 — LOW (coverage).** B0prime_RERUN admits route A and the prefix (spec 4ac5527a), so the route-A tail-OFF path runs only in Z2-OFF, which R1 lists as "fallback only".
- Make Z2-OFF mandatory, or state that route-A tail-OFF identity rests on RA8's static guard plus Z2's tail-ON-empty identity.

**I7 — checked, consistent.** T1_H with C6T is covered by RA5/RO1.
- RO1 firing in a T-run is recorded, and route B decides.
- Route B does not consume the circular-trial readout (A42).
- E^A_i uses route-A packets, not that readout.
- RA10 reports the a4/a8 observable at query 03.

## Verdict (single reviewer)

**PASS_WITH_CORRECTIONS.**
- Items 1–4: PASS. TINY is principled, and the G1/G2 growing row still fails.
- Item 5: I1 is should-fix before the seal. I2, I3 and I6 are low; I4, I5 and I7 are info.
