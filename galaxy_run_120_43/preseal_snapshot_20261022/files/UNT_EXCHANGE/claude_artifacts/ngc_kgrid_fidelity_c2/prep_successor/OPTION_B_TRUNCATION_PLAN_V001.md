# OPTION_B_TRUNCATION_PLAN_V001: NGC3198 route-A gas-roster truncation (plan only, no code)

Written 2026-10-18T00:36Z. Nothing was built, run or launched for this plan.

## 0. Why this plan exists

- **Checked decision: `NO_ADEQUATE_GRID`** (sealed prereg `4c2eefeb`; result `RESULT_TIER2_V001.md` `ba8ef623…`; check `TIER2_CHECK_V001.md` `d516fdbc…`, CONFIRMED).
  - The checker re-derived every decision input without importing aggregate v002/v003, so the decision does not rest on the unreviewed aggregate_v003. The formal v003 review (D1) is still open.
- **Branch taken.** The task's prep-v002 / seed-v003 branch applies only to `ADOPT_*`. It was **not** built. This file is the option-(b) plan that the task assigns to `NO_ADEQUATE_GRID`.
- **Governing text** (read at current bytes):
  - V003 addendum `5bef6552` (frozen): A11 makes (b) "a counted fallback, used only if the grid test registers NO_ADEQUATE_GRID"; A12.5: "truncate the route-A gas roster at the first radius with an unconfined column, record the mass fraction, and mark any query row beyond the truncation radius INVALID."
  - V004 addendum `9f3ce6aa` (live, not pinnable): A14.C3 directs the same (b) "on the adopted grid"; A17 rules G80C NOT ADEQUATE for NGC3198 rotation predictions (C3 e3 = 0.202); A22 bars calibration at k_max ≤ 4; A24–A26 set the direction to an analytic Q∞·T_N tail "applied in every stage that evaluates the lapse".
  - Prereg registered limit of (b): it does not remove the φ-error inside the cut.
  - Diagnosis `DIAGNOSIS_V001.md` §5(b) and its check `1a2d29ff` (R8 mass fractions, F5 caveats).

## 1. Binding findings to resolve before any (b) code is written

**BF1. There is no adopted grid, so A14.C3's "on the adopted grid" has no referent.**
- Literal reading of A11: seed v002 "carries the new grid numerics only if a grid is adopted". With no adoption, (b) would run on **G80C**.
- A17 (TESTED): G80C fails C1, C2 (0.926), C3 (0.202) and C4 (35.6θ). A G80C (b) run could therefore confine the gas, but its rotation rows would be known-inadequate by the criterion A17 names as "the one that matters for predictions".
- What a G80C (b) run can deliver is a **confinement / feasibility run** at the target-free A2F10 point. Every row it produces carries `GRID_NOT_ADEQUATE_C3` (e3 = 0.202).
- Using T120L or any other tier-2 grid instead would be a deviation from the sealed rule. It needs a root ruling plus prep v002, because tier 2 exceeds prep v001's 80-node cap.
- Classification: **DECLARED (root)**. The plan does not pick the grid.

**BF2. The operator that (b) acts on will change.**
- A22 bars calibration at k_max ≤ 4. A26 directs the V006 tail scheme into every stage that evaluates the lapse, and that includes NGC route A.
- So any truncation radius computed on today's k_max = 2 cube operator is provisional.
- The code must therefore compute the cut **per operator, from a sweep**. It must never hard-code 51.746 kpc.

**BF3. The cut radius is grid-dependent (TESTED, from the R1 replays on the full-roster iteration-0 operators).**

| Ring (first column) | R (kpc) | Confined columns of 32, G80C | Confined columns of 32, every tier-2 grid |
|---|---|---|---|
| 2496 | 52.655 | 30 | 32 |
| 2560 | 53.714 | 24 | 26 |
| 3360 | 81.178 | 0 | 0 or 4 |

- On G80C the first unconfined column is column 2503, in ring 2496 at 52.655 kpc (diagnosis, all 4992 columns covered).
- On the tier-2 grids the first unconfined radius is ≤ 53.714 kpc. Rings below 52.655 kpc and ring 79 were not replayed there (UNTESTED).
- The 95 kpc vertical profile is itself unconverged: e4 = 24θ between G120L and G160L (A14.C5, reported only). The confinement call at the search ceiling is therefore not a converged quantity on any grid.

## 2. The rule, mechanized

Every item below is a mechanization of A12.5's text. Items marked *(proposed)* need a root ruling before code is written.

**R1. Scope.**
- Only the route-A HI+He gas roster is truncated: the `gas_columns` of prep v001:164-179, 4992 columns = 156 GL4 radial nodes × 32 azimuths, ordered inner to outer.
- The stellar reference, H2 and the HI controls are unchanged.
- The search limit stays at 95 kpc with 1024 calls. Raising it, option (a), is TESTED-NEGATIVE (0 of 1808 rescued).

**R2. Determining the cut.**
- Sweep **every** roster column with the pinned HI solver (`hi_two_sided_free_boundary_v002`, `665b5589`, seed HI controls) on the full-roster iteration-0 operator. Use the validated replay pattern (`replay_lib_v001`, bitwise against the checkpoint records).
- A column is *unconfined* only when the solver returns NOT_BRACKETED within the limit, on either side.
- Any other failure (call budget, nonfinite value) is a run failure, never a cut.
- R_first = the radius of the innermost ring that contains an unconfined column. Rings with R < R_first are kept. That ring and everything outside it are dropped (ring rule, as in the diagnosis).
- Known for G80C at A2F10 (TESTED, diagnosis plus check R8):

| Quantity | Value |
|---|---|
| R_first | 52.655 kpc (column 2503) |
| Columns kept | 0–2495 (78 rings) |
| R_last_kept | 51.746 kpc |
| Columns dropped | 2496 |

**R3. Re-preparation and the fixed point at iteration 0** *(proposed)*.
- Truncation changes the iteration-0 operator itself (diagnosis check F5): prep v001:257-268 builds the initial razor-thin gas iterate from the roster. The completed RUN_V001 records are therefore not reusable.
- Procedure:
  1. Rebuild iteration 0 from the kept roster.
  2. Re-sweep the kept columns.
  3. If any is unconfined, re-cut at the new R_first and repeat.
- R_first is non-increasing from pass to pass, so this ends within 78 passes. Every pass is recorded.
- If no ring survives, the outcome is `FAILED_NO_CONFINED_ROSTER`.

**R4. Iterations ≥ 1** *(proposed)*.
- The roster is frozen at the R3 result. If a kept column becomes unconfined, the run stops `FAILED_KEPT_COLUMN_UNCONFINED`, recording the iteration, column, R, side and residual.
- There is no re-cut mid-run, because that would change the source definition between iterations. A re-cut means a new run from R2, launched by root.
- The diagnosis flagged this as the open part of the rule.

**R5. Mass record.**
- Dropped fraction = Σ over dropped columns of Σ·R·w_R·w_φ, divided by the same sum over the full roster. This is prep v001's own column mass, with helium applied once.
- Also record absolute M☉, and the route-B N2 cut fraction (3.90e-5 at 66.904 kpc) next to it.
- Known for G80C at A2F10 (TESTED): **6.98e-4** of the 1.3914e10 M☉ roster HI, i.e. 9.71e6 M☉.
- The annulus-rule alternative (cut at 50.847 kpc, 1.087e-3) is reported for reference only.

**R6. Query rows.**
- A row is INVALID iff R_query > R_last_kept, with reason `ROUTE_A_GAS_TRUNCATED_R_GT_<R_last_kept>`.
- This is the stricter reading of "beyond the truncation radius". It differs from R > R_first only for rows in (R_last_kept, R_first].
- Rows are evaluated from the roster radii only. No velocity is read.
- At G80C A2F10: 51.746 kpc > 44.08 kpc, so no row is INVALID (FORMAL, from radii).
- At other operators the count is UNTESTED. A12 has single-chain grids unconfined from 38–43 kpc, which would invalidate outer rows.

**R7. Per member** *(proposed; DECLARED before freeze)*.
- Each frozen member has its own operator, so it gets its own R2–R5 record. The manifest lists the cut per member.
- How INVALID rows count in the headline (min/median/max per-member counts) must be sealed before ROOT_CALL_ORDER step 5.
- The proposed rule: an INVALID row counts as not-within-error and stays in the denominator. This rule cannot inflate the count.

**R8. DDO154 symmetry** *(DECLARED)*.
- Either the same rule enters the calibration route A, or (b) is declared an NGC-only counted asymmetry.
- At the DDO A2F10 anchor the rule is a no-op: every column bracketed, max root 12.85 kpc (N2 R5, not re-tested). Other calibration points are UNTESTED.
- The calibration is being re-done under V006 in any case (A22/A26), so this has to be settled before that stage is built.

**R9. Labels on every output.**
- `SA-TRUNC-01`: "route-A gas roster truncated at R_first = …; dropped HI fraction …; field of the dropped gas at R ≤ R_last_kept not computed".
- Plus the grid's fidelity labels from §3.

## 3. What (b) does not fix (registered limits, TESTED)

- **TRUNCATION_SHAPE rings.** C1 fails on every grid at 12 rings, 1.537–10.54 kpc, with S/θ 1.128–3.654. These sit inside any cut. The cause is the k_max = 2 cube-corner m=4/m=8 truncation, which the sphere mask removes.
- **On G80C:** C1′ fails at 30 NOT_GRID rings (35.7θ), and C2, C3 and C4 also fail.
- **Kept outer rings are within grid error on G80C** (diagnosis check F5). Barriers at 46–52 kpc are 0.95–12θ, against a φ-error of 8–13θ.
- **95 kpc profile:** unconverged at 24θ even between the two finest grids (BF3).
- **The field of the dropped gas at the query radii is UNTESTED.** Deciding test (target-free, known-field only): the C3-type R dΦ/dR of the dropped annular mass under K1 and K2 at the 175 C3 radii, as a fraction of the full-roster K1/K2 value. Program-operator lnN at query radii is out of scope for this lane.

## 4. Code that (b) needs (none written)

These follow the diagnosis §5(b) list (check R10 confirms the obstacles).

| Piece | What it does |
|---|---|
| prep v002 | One roster input (`gas_roster_keep_rings` or `R_keep_max_kpc`, plus the sha of the cut record). It filters `gas_columns` before the initial iterate is built. With the input absent it must be byte-identical in behaviour to v001. |
| cut-sweep tool | R2/R3 on START blobs, reusing the replay_lib_v001 pattern. It writes the cut record by exclusive create. |
| worker successor | Re-pins prep from `c54c7cc9` to v002 (worker v002:16). |
| launcher successor | Replaces the mask refusal at launcher v001:97-98 with acceptance of a pinned cut record. |
| binding pins and manifest | Carry the cut record and the SA-TRUNC-01 label. |
| seed v003 and requests | Built with the seed v002 builder pattern: a truncation-record path and sha, and the rule id. Serial, PAR N8 and N3 requests, pinning only frozen decisions (V002 `17c26616` or V003 `5bef6552`, never V004). |
| route B | The HI limit is unchanged, so `template_mapping_check` (v006:1471-1481) is unaffected. The route-A domain (≤ 51.746 kpc) sits inside route B's (66.904 kpc). Wherever route B consumes route-A gas, the forward pipeline must declare which cut governs the shared source. |
| DDO calibration stage | Needed only if R8 is ruled symmetric. |

**Validation gates before review.** Each must be proved bitwise from bytes:
- **G1.** prep v002 with no truncation input reproduces the v001 START blobs (V1 pattern).
- **G2.** On the full G80C roster, the cut tool reproduces the diagnosis: first unconfined column 2503, the 1808-column failing set, and the 681/681 OK roots.
- **G3.** prep v002 with keep = 78 rings reproduces the roster digest prefix (columns 0–2495) and the 6.98e-4 fraction.
- **G4.** The seed-v003 dry run (D1–D5, P1–P3 pattern) passes and reaches the binding stub.

**A distinct review is required before any launch.** The author re-deriving its own bitwise claims is not enough.

## 5. Cost (ESTIMATE, from the measured G80C RUN_V001 baseline; UNTESTED)

Baseline: 418 s iteration-0 prep; 4.378 ms per metric call; 229,102 calls over 2503 confined columns, i.e. about 91.5 calls and 0.40 s per column.

| Step | CPU-s | Wall at N=8 (ideal) |
|---|---|---|
| R2 full sweep, 4992 columns (unconfined columns run to the 95 kpc limit, about 548 calls / 2.4 s each) | ≈ 1000 + 1808 × 2.4 + 681 × 0.4 ≈ 5,600 | ≈ 700 s |
| R3 pass, 2496 kept columns, plus re-prep | ≈ 418 + 1000 | ≈ 545 s |
| One route-A iteration, 2496 columns | ≈ 1,420 | **≈ 545 s** (418 s serial prep + 125 s columns) |

- All of these are well inside the 21,600 s wall cap.
- Parallel efficiency of route A at N=8 is not measured here.
- On a tier-2 grid, if BF1 is ruled that way, the per-column cost scales about linearly in W (P2, TESTED on line prep): ×2.25 for T120L.

## 6. Launch commands

**None can exist yet.** Prep v002, the worker, the launcher successor and seed v003 are unwritten and unreviewed. After they exist, the command takes the shape of the diagnosis's DEFAULT serial and PAR N8 commands, with the new launcher, spec and outdir. Root launches.

## 7. Next steps by D-SPLIT class (the prereg assigns these)

- **TRUNCATION_SHAPE (blocks every grid):** the A1-numerics k_max 3–4 / sphere test for NGC3198.
  - Coordinate it with the V006 design (A24–A26). Whether the V006 tail is defined on the complement of a cube or of a sphere decides whether the cube-corner m=4 survives (UNTESTED).
  - After that, run a successor fidelity prereg on the V006 operator.
  - At k_max = 2, T120L is the minimal-W grid that passes every other criterion (TESTED). It is a candidate only, never adopted.
- **NOT_GRID:** register the in-plane anisotropy as an operator property. The leading explanation is start-state memory of the y-polarized initial configuration (A18/A19, PLAUSIBLE). The per-azimuth vs m=0 column question (audit H3) is the deciding item.
- **Open:** the code-only review of aggregate_v003 (D1).

## 8. Classification of open items

| Item | Class | Source or deciding test |
|---|---|---|
| G80C cut 52.655 / 51.746 kpc; 6.98e-4 dropped | MEASURED (TESTED) | Diagnosis, check R8 |
| Cut is grid-dependent | MEASURED (TESTED) | R1 replays, all 10 grids |
| No INVALID row at G80C A2F10 | COMPUTED (FORMAL) | Radii only |
| Grid for (b) (BF1) | DECLARED (root) | A11 literal vs A17 |
| R3 fixed point, R4 fail-closed, R7 INVALID scoring | DECLARED (root, proposed here) | — |
| R8 DDO symmetry | DECLARED (root) | — |
| Effect of the dropped gas at query radii | UNTESTED | K1/K2 dropped-mass test (§3) |
| Viability of (b) on any operator | UNTESTED | G1–G4, then a launch |
| Cut on the V006 operator | UNTESTED | R2 sweep on that operator |
