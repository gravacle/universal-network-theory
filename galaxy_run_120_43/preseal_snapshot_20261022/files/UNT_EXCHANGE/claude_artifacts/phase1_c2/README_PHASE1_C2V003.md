# phase1_c2v003: the A133 Phase-1 tool, A144 successor of v002

**Labels.** TESTED = run here on synthetic fixtures, with the result shown. FORMAL = follows from the cited code or text. UNTESTED = not run; the deciding test is named.

**Text of record.**
- A144 (R1, R2, R3; errata E_A133_2(a) and (b)) and A135 item 10, in `CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md`.
- Claude3 0204 (the v002 review of record: N1, N2, N6) and its evidence in `claude_artifacts/review_phase1_v002_c3/`.
- The three-lens refutation wf_d6eb5084 (math, protocol, code), whose amended texts A144 adopts.
- `CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` (`cd92ef91`), sections 1.5 and 4.

**Scope.** v003 changes `phase1_c2v002.py` (`d64351ec`) at these sites only: MODULE, E_Q_READING, the docstring, `at1_rows`, `cmd_at1`, `cmd_handoff`, and new helpers (`band_region`, `region_violation`, `band_region_extent`, `member_eps`, `check_member_eps`, `certificate_maps`, three constants). `band_rows`, `cmd_band` and `linear_model` are AST-identical to v002 (TESTED, T35). v001 and v002, their tests, READMEs, HASHES, NO_FIX_NEEDED files and `test_runs/`, `test_runs_v002/` are untouched; T00 re-hashes v001, v002 and both test files in every run. No production run was made. No campaign, cache, run tree, C5H, `UVT_*` path or NGC3198 target was opened.

## Files (all new, created exclusively)

| File | Role |
|---|---|
| `phase1_c2v003.py` | The tool. Same commands, arguments, exit codes, schema strings and output file names as v002. |
| `test_phase1_c2v003.py` | 142 checks: 96 ported (part 1), 9 regression (part 2), 37 new (part 3). 54 MUST_FAIL, 88 MUST_PASS. |
| `mutation_phase1_c2v003.py` | Mutation check: 12 single-site mutants of the A144 / A135-item-10 code. |
| `DIFF_PHASE1_C2V002_TO_V003.diff` | Unified diff of the tool (+218 / −33 lines). |
| `DIFF_TEST_PHASE1_C2V002_TO_V003.diff` | Unified diff of the tests (+1193 / −129 lines). |
| `test_runs_v003/RUN_20261019T161630Z_50059/`, `test_runs_v003/RUN_20261019T161739Z_55769/` | The two record runs, each 142/142. Each holds `RESULTS.json` and `SHADOW_REGRESSION_V002_V003.json`. |
| `test_runs_v003/MUTATION_20261019T161856Z_62456/MUTATION_RESULTS.json` | Mutation run: 12/12 killed. |
| `HASHES_V003.txt` | sha256 of each object, computed from its bytes. |

**Pins.** Unchanged from v002: orchestrator `c75a889f`, engine `6ec8b2d0`, freeze v003g `48a1e48a`, KMAX `dbddc02c`.

**Usage.** As in v002, with `phase1_c2v003.py`. No argument was added or removed. Two input contracts are new:
- the Phase-2 members file for `agree at1` carries `eps_km_s` on every member point (R3);
- `handoff` also accepts root fields with `certificate_pins_by_member` in place of `certificate_pins` (A135 item 10).

## R1 (E_A133_2(a)): the box-slice category, label only

- **Rows.** `band_region(L)` builds A and b_band with band_rows' own expressions, plus the family slices LINEAR_DDO [0, 2N), BOX [2N, 2N+6), TRUST_RADIUS [2N+6, 2N+6+2m_id). T30 captures the arrays band_rows actually hands to the LP and checks them bitwise against the helper's, on 6 fixtures (TESTED).
- **Test.** Row i is violated iff (A c)_i − max(b_band_i, 0) > E._LP_EPS, with c = V_I Δ_m. The clip is _lp_max's (engine L1787). The tolerance is the pinned engine's `_LP_EPS` = 1e-12 (engine L181), read from the module; T00 asserts its value.
- **Printed on each failing (member, row):**
  - `region_rows_violated`: the violated families in the order [TRUST_RADIUS, BOX, LINEAR_DDO], or [];
  - `region_max_violation`: {family: max_i ((A c)_i − max(b_i, 0))} for all three families;
  - `category`: the first violated family, mapped to OUTSIDE_TRUST_RADIUS, OUTSIDE_BOX_SLICE or OUTSIDE_LINEAR_DDO_REGION; NGC_NONLINEAR only when the list is [];
  - `geometric_part` = K_q·V_Iᵀc − (hi_q − g_A) on an upper miss, or (lo_q − g_A) − K_q·V_Iᵀc on a lower miss; `residual_part` = excess − geometric_part.
- The category says where c lies. It does not apportion the excess.
- **Label only (TESTED).** With ε = 0 everywhere, the failing set, excess, norm_n and outcome are byte-identical to v002: in process on 4 fixtures, and through the CLI on 2 (T30).
- **Disclosed (from A144):** labels can change at the ulp level against v002's LINEAR test, and a pair violating both BOX and LINEAR_DDO now reads BOX.

## R2: the band region's extent (print only)

`agree at1` adds three keys to `reported`:
- `band_region_extent`: per identified c_j, `{direction, extent: [min, max], lp_status: [min, max]}`, solved by E._lp_max over the band region's own rows (trust rows included);
- `band_region_single_point`: true iff every extent is OPTIMAL and exactly [0.0, 0.0]; `NOT_AVAILABLE` if any program is not OPTIMAL;
- `band_region_single_point_reason`: BOX_CORNER iff the box rows alone give [0.0, 0.0] on every j, otherwise OTHER_ROWS; null unless the region is a single point.

These keys never refuse and never change a row. `band`, `band_rows`, `cmd_band` and the L1 schema are unchanged. The name is distinct from `identified_projection_vs_linear_region`, which leaves out the trust rows. **A band of any width, zero included, is never read as a spread, a zero spread or a confidence statement.**

## R3 (E_A133_2(b)): the full noise bound (a physics-reading change, A115 (b))

- **The formula.** e_q(m, q) = ε_m + ε_q·(|1 − Σ_k Δ_m,k/du_k| + Σ_k |Δ_m,k|/h_k).
  - du_k is the signed fdplan step; h_k = |du_k|.
  - ε_q is L1 `eps_q` (A137, unchanged).
  - ε_m is the member's own `eps_km_s[q]`.
- **Contract.** `cmd_at1` refuses MEMBERS, writing no out-dir, when a member point lacks `eps_km_s` or the list's length is not 43. at0b is not affected (`members_values` is unchanged).
- **A bad entry** (None, bool, non-finite, negative, or not a number) keeps every bounded term, e_q = ε_q·(…), and flags that pair MEMBER_POINT_NOISE_NOT_BOUNDED.
- **A row with no ε_q** reads FD_NOISE_NOT_BOUNDED with e_q = 0, whatever ε_m is, as in v002.
- **Printed:**
  - `failing[]` gains `flag_reason`;
  - `e_q_per_member_row[]` gains `eps_m`, `flag` and `flag_reason`;
  - the new list `reported.pairs_member_point_noise_not_bounded` holds {log_index, id, flag_reason};
  - `rows_fd_noise_not_bounded` stays per row;
  - `e_q_reading` states the formula.

## Custody and A135 item 10

- **L1 custody.** at1 refuses (`L1`) an L1 whose `module` is not `phase1_c2v003`. TESTED (T33): an L1 written by v002's band is refused, and no out-dir is written.
- **Handoff successor.** The root fields may carry `certificate_pins_by_member` instead of `certificate_pins`: {member log_index as a string: certificate map}.
  - The keys must be exactly the v003g member log indices.
  - Each map follows v002's `certificate_pins` rules: {path, sha256} pins are hash-verified, and non-pin placeholders are allowed.
  - A pin that binds another admitted point (its theta key or spec sha, by exact token, as provenance `_scope`) is refused with CERTIFICATE_MAP, before any output.
  - A pin that binds no admitted point is allowed. This covers shared custody pins such as LO_NGC_K32_CERT_V001 (A136).
  - Each member's handoff carries its own map, still 10 fields.
  - The receipt gains `certificate_map` and one check line, in this form only.
- **Unchanged paths.** The shared-map form and S0 (`fdplan --s0-only`) are byte-identical to v002 except the `module` field (TESTED, T36 and R01).

## Tests (TESTED; 2 identical record runs: 142/142, MUST_FAIL 54/54, MUST_PASS 88/88, audit denials 0, 64 shadow calls each)

**Part 1 (96 checks): every v002 check, ported, with v002's ids in v002's order.**
- Port changes:
  - every Phase-2 members file carries `eps_km_s` (0.01);
  - T22's category oracle and T25's region lists use an independent A144 R1 re-implementation;
  - T29 (the A137 N-B checks) re-runs the same fixtures under E_A133_2(b), with ε_m present;
  - T27/T28 (L5) now also run under the shadow;
  - T00 adds one check: v002 and its tests are untouched, and the engine's `_LP_EPS` is 1e-12.
- v002's 8 R01 checks targeted v001. They are replaced by part 2, which targets v002.

**Part 2 (R01, 9 checks): regression against v002.** Every part-1 CLI call also runs v002 on the same inputs into the same out-dir path; v002's directory is moved aside to `<out>.V002_SHADOW`. Results are under "Declared regression differences" below.

**Part 3 (37 checks).**

| Group | What is shown (TESTED) |
|---|---|
| Fixtures | NEARCORNER: a march0 case at u_A = (0.97, 0.03, 0.5), m_id 1, 0204-style. CM2: an m_id = 2 corner at (1, 0, 0.5), V_I = (1, 1, ±√2)/2, boundary at `design`. Both are built on the real orchestrator. |
| R1 | The helper's A and b_band are bitwise equal to band_rows' on 6 fixtures. |
| R1 | With ε = 0, v002 and v003 are byte-identical in process on 4 fixtures (seed 301 failing pairs, corner 344, NEARCORNER grid 8256, CM2 86) and through the CLI on seed and corner. |
| R1 | **T27 corner:** v002's 316 NGC_NONLINEAR pairs all relabel as `['BOX']`. v003's own CLI at1 has 320 pairs, all OUTSIDE_BOX_SLICE `['BOX']`. |
| R1 | **NEARCORNER grid** (310 in-box, DDO-linear members, exactly linear toy): 6662 failing pairs on 174 members, all OUTSIDE_BOX_SLICE `['BOX']`, all with c outside the box interval ±0.0424. At ε = 0, v002 labels all 8256 NGC_NONLINEAR. |
| R1 | **Along-face members** at the corner, curvature toy: 859 pairs on 20 members, all NGC_NONLINEAR, max BOX violation 2.9e-17. The rejected exact, unclipped test would label 15 of the 20 BOX. |
| R1 | **On-face members at m_id = 3:** none is BOX (max violation 4.2e-17). The exact test would label 5 of 8 BOX. |
| R1 | c at the band optima gives [] on every AVAILABLE row of 6 fixtures (514 optima). |
| R1 | **CM2:** v002's 68 OUTSIDE_TRUST_RADIUS failures keep OUTSIDE_TRUST_RADIUS, with region list [TRUST_RADIUS, BOX]. |
| R1 MUST_FAIL | A member outside both the trust radius and the box lists TRUST_RADIUS then BOX, never BOX alone. |
| R1 MUST_FAIL | A member 1e-6 outside the box slice is OUTSIDE_BOX_SLICE, never NGC_NONLINEAR (v002 says NGC_NONLINEAR). |
| R1 MUST_FAIL | f = hi to one ulp (b = −8.9e-16): a member at c ≈ 0 is never LINEAR_DDO (v002 says OUTSIDE_LINEAR_DDO_REGION). |
| R1 MUST_FAIL | b = −1e-9 is read with _lp_max's clip. |
| R1 | excess = geometric_part + residual_part, and residual_part = ±ρ − a_q − e_q, on 621 failing pairs. |
| R2 | The m_id = 1 corner gives [0.0, 0.0], true, BOX_CORNER. CM2 gives false and null (extents ±0.1433). The interior gives false. |
| R2 | The extents equal an independent bound/vertex computation (difference 0.0). |
| R2 | A single point made by two zero-slack DDO rows with the box not binding reads OTHER_ROWS. |
| R2 MUST_FAIL | Injected non-OPTIMAL programs read NOT_AVAILABLE, and every row and failing entry is unchanged. |
| R3 | e_q equals the independent formula within 1e-12 relative: interior CLI (516 pairs, ε_m varying by member and row), corner CLI (430 pairs, signed du with a minus side), face in process (301). |
| R3 | The u_A member's e_q is exactly ε_m + ε_q. |
| R3 | **Honest noise at the bound** (|δ| = (1 − 1e-9)ε), adversarial signs, exactly linear NGC, in-region members: v003 COVERED on corner, interior and face. At the corner v002 reads SUPERSEDED with 201 pairs. The designated pairs sit 1e-9·e_q inside the bound, and a_q = 0. |
| R3 | **Random noise** within the certificates, 45 trials: no in-region pair fails. |
| R3 MUST_FAIL | A members file without `eps_km_s`, or with length 42, 44, a scalar or an object, refuses MEMBERS with no out-dir; at0b on the same files PASSes. |
| R3 MUST_FAIL | None, NaN, −1, True, 'x' and inf at single pairs flag only those pairs, with bounded terms kept. |
| R3 | A row with no ε_q reads FD_NOISE_NOT_BOUNDED / NO_ROW_EPS_Q whatever ε_m is. An independent recomputation of the §4 inequality reproduces the 301-pair failing set exactly. |
| Custody MUST_FAIL | A v002-written L1 is refused. |
| A135 item 10 | Per-member maps are accepted, and each of 7 handoffs carries its own map. |
| A135 item 10 MUST_FAIL | Refused: a member mapped to another member's certificate (CERTIFICATE_MAP), a missing key, an extra key, a non-object map, a bad pin sha (PIN_MISMATCH), and both forms at once (ROOT_FIELDS). |
| Scope | Only the declared AST nodes changed. |
| Identity | S0, the shared-map handoff and L1 are byte-identical to v002 except `module`. |

**Mutation (TESTED, 12/12 killed).** Each of these mutants is killed:
- no clip;
- exact comparison;
- A137 e_q;
- BOX before TRUST_RADIUS;
- no L1 custody;
- no certificate-map scope check;
- no eps contract;
- negative ε_m accepted;
- single point ignoring LP status;
- e_q without ε_m;
- unbounded pair at e_q = 0;
- unsigned du.

## Declared regression differences (R01, TESTED, both record runs)

| Command | Calls | Result |
|---|---|---|
| snapshot | 20 | identical up to tool identity and the engine record's volatile fields (as in v002's R01) |
| fdplan | 8 | identical except `module` |
| handoff | 12 | identical except the receipt `module` |
| band | 6 | identical except `module` |
| at0a | 9 | identical except `module` |
| at0b | 5 | identical except `module` |
| at1 | 4 | differs only in the declared A144 fields: `outcome`, `failing` (`category`, `flag`, `flag_reason`, the region keys, `geometric_part`, `residual_part`, and `excess` through e_q), `e_q_reading`, `reported.e_q_per_member_row`, and the new `reported` keys. `norm_n` is equal on every pair failing in both. |

The two corner (L5) snapshots and NOID are identical up to tool identity.

**The four at1 fixtures:**
- **C1:** COVERED in both.
- **Q1:** SUPERSEDED in both, with the same 301 pairs, all OUTSIDE_TRUST_RADIUS; excess moves with e_q.
- **DEFECT:** AGREEMENT_DEFECT in both.
- **CORNER:** 316 pairs (v002) become 320 (v003). The 316 are relabelled NGC_NONLINEAR → OUTSIDE_BOX_SLICE. The 4 new pairs fail because the exact e_q is smaller than A137's there (FORMAL note 1). All 320 are OUTSIDE_BOX_SLICE.

## CHOICES not forced by A144 (for the reviewer)

1. **Reason key.** `band_region_single_point_reason` is null unless the band region is a single point. A144's "OTHER_ROWS otherwise" is read as applying inside the single-point case. A non-OPTIMAL box-only program gives OTHER_ROWS, which is the literal reading.
2. **Extent statuses.** Each extent side prints NOT_AVAILABLE when its own LP is not OPTIMAL. −0.0 counts as 0.0 (IEEE equality) for "exactly [0.0, 0.0]".
3. **Flag reasons.** The `flag_reason` vocabulary is NO_ROW_EPS_Q and MEMBER_EPS_{NONE, BOOL, NOT_A_NUMBER, NON_FINITE, NEGATIVE}. MEMBER_EPS_LIST_MISSING occurs only in process; the CLI refuses first.
4. **Non-numeric entries.** A non-numeric entry, such as a string, is treated like A144's listed bad entries (flagged, bounded terms kept), not refused.
5. **Contract coverage.** `eps_km_s` is required on every member point of the file, including points with `member_valid` false. A non-list value is refused like a missing list.
6. **Row precedence.** A row with no ε_q gives FD_NOISE_NOT_BOUNDED whatever ε_m is. Such pairs are not listed in `pairs_member_point_noise_not_bounded`.
7. **Print-only additions.** `e_q_per_member_row[]` carries `eps_m`, `flag` and `flag_reason`, and `region_max_violation` is printed for all three families. Both are print only.
8. **Geometric part.** residual_part := excess − geometric_part, so the identity holds up to one rounding. geometric_part uses L1's measured K_q, as K_q·(V_Iᵀc).
9. **Handoff form.** A135 item 10 uses a new key in the same S_ROOT schema; the key set selects the form, and both keys together are refused.
   - The scope rule is "binds no other admitted point". A pin that binds no point (a shared custody pin) is allowed, and a pin is not required to name its own member.
   - The refusal code is CERTIFICATE_MAP.
10. **Unchanged names.** Schema strings and output file names are unchanged (v002 practice), and the L1 custody refusal uses code `L1`. The ROOT_FIELDS key-set message is extended to name the second form.
11. **Mutation script.** `mutation_phase1_c2v003.py` is an extra file, not in the task list. It is dev evidence and pins nothing.

## FORMAL notes

1. **e_q(v003) and e_q(v002) are not ordered.** e_q(v003) < e_q(v002) iff ε_q·Σ|t_k| > ε_m + ε_q·|1 − Σt_k| (t_k = Δ_k/du_k), which happens for far members. A137 bounded only the slope noise, Σ|δ_Fk − δ_A||t_k| ≤ 2ε_qΣ|t_k|. The exact worst case of the full noise collects δ_A's slope and offset terms into one coefficient |1 − Σt_k|. So a v002 COVERED pair can read SUPERSEDED in v003, and the reverse. Seen: T27 corner, 4 pairs.
2. **The R3 guarantee holds up to the LP tolerance.** "In region" means every violation is ≤ 1e-12. A member at that edge can exceed the band by about |K_q V_Iᵀ|·1e-12 (about 1e-10 km/s on these fixtures). This is below any certificate ε.
3. **Exact-zero flag.** `band_region_single_point` is exact-zero by design. A near-corner anchor reads false with tiny printed extents.
4. **Unclipped exact comparisons misread the band's own optima.** They would flag 385 of the 514 band optima on the 6 fixtures: all of them on seed, JAC, CM2 and the m_id = 3 synthetic, 43/86 at NEARCORNER, and 0 at the corner. The optima sit on binding rows only to within rounding. The tolerance A144 adopts removes this.

## Process disclosures

- Development and dev runs were in the session scratchpad. The final files were copied with exclusive create (`open(..., 'x')`), and their shas were verified against the dev bytes. The record runs and the mutation run were made from the final location.
- Read beyond the task's named list, all as permitted citations:
  - Claude3's `probe_cat2.py`, cited by explicit path in `review_phase1_v002_c3/REVIEW_PHASE1_V002_RESULT_C3V001.txt`, to see how 0204 built NEARCORNER. Its fixture directory was not opened, and NEARCORNER here is rebuilt independently.
  - v002's record `test_runs_v002/RUN_20261019T132307Z_43825/RESULTS.json`, cited in HASHES_V002, to confirm the port keeps v002's check ids and order.
- No recursive grep, find or ls was run on the artifact tree.

## UNTESTED (deciding test named)

- **Real ε inputs.** The members-values producer (A144 R3) writes `eps_km_s` from each point's EPS certificate. Decided by the first real at1 on its output; until then, only synthetic members files are tested.
- **M-12 classifiers.** Classifiers A and B must accept the v003 encodings (the fourth category value, the region keys, `flag_reason`, the per-pair list, the band_region keys). Decided by both classifiers on a v003 AT1 file before the seal.
- **Codex1's pass** on the E_A133_2(b) formula (A144, distinct lineage).
- **Real maps.** Real per-member certificate maps (S0/S1 EPS records, the A136 LO custody pin). Decided by the first `handoff` after u_A with root's real fields.
- **The real campaign and NGC values.** As in v002.
