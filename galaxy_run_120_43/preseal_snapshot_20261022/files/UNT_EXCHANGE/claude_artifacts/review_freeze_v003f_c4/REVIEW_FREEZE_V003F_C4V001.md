# Review: freeze v003f (Codex3), delta against the v003e review

Claude4, dispatch 0544 item 1 (v003f from 0531; gap rows A60 / 0535). Written Sun Oct 18 14:20:03 UTC 2026 (`date -u` at write).
Synthetic targets only. No real target, velocity or C5H/UVT file was opened; no launch. The only program data file opened is the target-free query manifest, for the in-process PROGRAM-scope probe.

## VERDICT: PASS_WITH_FINDINGS (0 blocking, 1 SHOULD_FIX, 5 NOTE)

Scope: the exact bytes of `prediction_freeze_c2v003f_cx3v003.py` (sha256 `debc254744a40e9d5cb9f856dc922f24b398b6a77c71eb4c71709c98ce398306`), under the synthetic probes below.

- The v003e blocking finding B1 is closed, and so are S1–S4 and N1–N3.
- The roster consumes the A60 gap rows (`QUERY_OUTSIDE_RETAINED_SUPPORT`) and the cut-bound rows (`QUERY_BEYOND_OUTER_GAS_CUT`) exactly as ruled, at every boundary I could construct.
- Scores on admissible inputs are identical to v003e.
- One new SHOULD_FIX (F1): the declared alternative set is not bound to slots V002, so a freeze can silently drop a declared alternative. It cannot change the headline.

## What was reviewed (sha256 from bytes)

| File | sha256 | Role |
|---|---|---|
| `calibration_region_engine_c2v003b.py` | `6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3` | DDO calibration of my synthetic world |
| `prediction_freeze_c2v003e_cx3v002.py` | `42a01b048d3e534f37c13cca59400a9c522c7dbb3476a95eeb5e6042adb86cbf` | P10 LADDER regression baseline |
| `prediction_freeze_c2v003f_cx3v003.py` | `debc254744a40e9d5cb9f856dc922f24b398b6a77c71eb4c71709c98ce398306` | under review (0531 successor) |
| `NGC3198_FREEZE_SLOTS_C3V002.json` | `4c5951cbef9aa2c1cf7e7e4c859b59a7aafb5476bd7e59c20caef769376f6c7e` | hard-pinned in v003f (alternatives, GL4 Q01/Q02, query rows) |
| `REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` | `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` | hard-pinned in v003f (GL4/GL10 node radii) |
| `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` | `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494` | PROGRAM-scope probe only, in process |
| `annular_bernstein_source_kernel_v001.py` | `2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e` | pinned by slots or nodes; hash-checked by the module |
| `GALAXY_CONFIG_NGC3198_C2V006.json` | `64b6f1fadb432b1d5e2ee5b54620fb0c4d2cdb59e425e8034458e0dcd58ee441` | pinned by slots or nodes; hash-checked by the module |
| `NGC3198_ROUTE_A_A2F10_SEED_C2V002_DEFAULT.json` | `88ef386d2bd4e14be23709d21b23fd3b7b57a2cc85adcc09d6a0459bcbc108da` | pinned by slots or nodes; hash-checked by the module |
| `build_registered_radii_cx3v001.py` | `3db13f6eea538fb4084fff9fc6caf8fca5dcae64e3024429835b89ab763738ac` | pinned by slots or nodes; hash-checked by the module |
| `ngc_uvt_route_b_binding_cx3v006_r5cx3v001.py` | `f348d0ca9fb052549f2cd219e040afd294e2ad6da02cf659d9b0bfb27325bca7` | pinned by slots or nodes; hash-checked by the module |
| `GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` | `f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b` | pinned by slots or nodes; hash-checked by the module |
| `review_freeze_v003e_c2/REVIEW.md` | `da287f7ee05ff1cae172848fde5701b252cda85dd4645af17a70cd77caf648e9` | baseline review (Claude2) |
| `v003f/API_INTEGRATION_V001.md` | `da7a67e54b2a752594e470ab18050551e28bc5f7359a1021d8026ea232abafef` | Codex3 API statement |
| `ROOT_DECISIONS_…_V005_ADDENDUM.md` | `0c45cf7a5b282a4a72e7ccc348e4e6a884c0b171d55f691e098990f2c9361a47` | A60 gap-row and cut-binding rulings |

## Method

My own harness: `tools/review_v003f_c4v001.py` (`898508c4b3bd8e0579c2a0958474afeee7c9e2b63ecd5a7accac4b2ab532458f`). The fixtures are my own, not Claude2's or Codex3's:
- a DDO-shaped region (12 rows) and 8 selected members;
- 43 query ids `C4R-Q01..43`, with radii placed against the real registered GL4 nodes:
  - for cut A = 20.3 kpc: a row at the exact last retained node (text `19.65668333391535`, its product with kpc_m equals the node bitwise), a gap row (20.00) and a row at the cut (20.3);
  - for cut B = 30.0 kpc: a gap row (29.80) and a row at the cut (30.00);
- a v010-shaped forward that derives its INVALID rows from its own cut registry, as a producer would;
- my own gates, cut documents, root rosters and targets.

**Order.** Targets are built only after the freeze, the registration and the logged manifest hash. On every row the reference leaves null, the target is the unseen base value, so a leaked value would score a hit.

**Independent oracles.**
- Registered INVALID sets by `numpy.searchsorted` on the node array: inner by slots position; outer R_m ≥ cut_m, overriding inner; gap last_retained_m < R_m < cut_m.
- The D1 reference, the LADDER within-error flags and the envelope band.

**Audit hook.** It refuses reads outside the pinned files and the run directory, subprocesses, network, deletes, renames, links, mkdir outside the run directory, and any write to an existing file. Denials: 0.

**Final run.** `runs/run_20261018T141427Z/REVIEW_RESULTS.json` (`db4343bfdf58162aef13667477a464fb169a192eee8ea1e06a39ebb674d3d38a`):
- **235/235 checks behaved as recorded**;
- 6 of them demonstrate findings: F1 ×4, F2, F3;
- peak RSS 73.3 MB.

## Results against the v003e findings

| v003e item | v003f | Evidence (checks, all passed) |
|---|---|---|
| **B1** (blocking): INVALID roster never bound | **CLOSED** | 41 P1 checks. 6 Q01/Q02 contradiction shapes refuse: finite and valid, finite in the map only, finite with `valid:false`, `valid:true` with null, missing from `invalid_rows`. A missing, null, wrong-sha or extra-key pin refuses. 15 malformed rosters refuse. A roster bound to another query manifest is refused at the writer. 13 v003e S2 regression probes still refuse (non-finite valid rows, row/map disagreement, raw-result target keys). 12 P9 checks: the scorer refuses missing, other, swapped and 4-of-5 pins; rehashed manifests (finite Q01, no roster binding, unpinned rosters, a gate on an uncovered row) fail verification. |
| **S1**: built-in reasons on any row | **CLOSED** | 10 P2 probes. INNER/OUTER/GAP reasons on rows the rule does not derive refuse. A root gate may not list a built-in reason or relabel Q01. |
| **S2**: gate authority from the producer | **CLOSED** | 16 P3 probes. A REGISTERED but unlisted gate refuses. The producer pin is optional and must equal the root pin. DRAFT, wrong schema, target key or alias, unknown id, two gates on one (row, reason), and a sha mismatch all refuse at roster load. |
| **S3**: gate field types | **CLOSED** | 11 P4 probes. Strings, mixed types, empty lists, duplicates and empty strings refuse. A substring of a listed reason refuses. |
| **S4**: `valid:false` refused the whole freeze | **CLOSED as ruled in 0531** | 30 P5 checks. 5 failed-member shapes become MEMBER_INVALID with no frozen predictions. 6 contradiction shapes refuse: finite on a mandatory row, map-only, valid-finite on Q02, unregistered reason, off-roster built-in, target field. Full freezes with one member failed, and with the nearest member failed: D1 equals the oracle, the envelope excludes the member, which scores 0/43. |
| **N1**: stale module stamp | **CLOSED** | Constant and manifest `module` = `prediction_freeze_c2v003f_cx3v003`. |
| **N2**: D1 vacuous for an all-INVALID member | **CLOSED** | 3 P6 probes. An empty registered-valid set refuses, in every member or in one member. A cut leaving no valid row also refuses (P8). |
| **N3**: GL10 guard by name prefix | **CLOSED for GL10 identity** | GL10 rosters marked EVALUATED or renamed refuse. The exact GL10 roster cannot evaluate. The writer refuses GL10 EVALUATED, renamed, or as primary. The alternative **set** is a separate gap: F1. |

## A60 gap rows and cut-bound rows

A60 rules that a query between the last retained route-B node and the pinned cut is INVALID `QUERY_OUTSIDE_RETAINED_SUPPORT`, and that the outer set equals {R_q ≥ first_unconfined_R}. v003f does this:

- **Boundaries** (my radii against the real nodes):
  - cut A: the row at the exact last retained node stays valid; 20.00 is GAP; the row at 20.3 is OUTER;
  - cut B: 29.80 is GAP; 30.00 is OUTER;
  - a cut exactly at a node radius excludes that node (unit test);
  - outer overrides inner when they overlap (unit test).
- **Per-θ freeze.** 8 members: cut A on M002, M005 (the D1 reference M002 is among them), cut B on M000, M003, M006, no cut on M001, M004, M007.
  - The frozen sets equal the oracle for every member.
  - ORIGINAL_K uses its own roster (cut B), and its sets also equal the oracle.
  - Each sensitivity entry carries its own context's set.
  - The cut documents are pinned in `input_files`.
- **Scoring.**
  - Gap and cut rows score INVALID_AS_MISS at the worst tier, with their reason.
  - The 19 bait targets on the reference's INVALID rows never hit.
  - Within-error counts and the envelope equal the oracle.
  - With every member under cut A, the 17 gap and cut rows (C4R-Q27–C4R-Q43) have no band and score as band INVALID_AS_MISS.
- **Producer hints never decide.** Each of these refuses:
  - finite or valid values on a gap row, an outer row, or the exact-cut row;
  - GAP and OUTER labels swapped;
  - GAP on the exact last-node row, or OUTER below the cut;
  - a failed member carrying a finite value on a gap row;
  - a producer that reports no cut at all.
- **Context custody.**
  - Missing, one-ulp-off and ambiguous θ contexts refuse.
  - A member whose forward raises passes evaluation as MEMBER_INVALID; its missing context is then refused at the writer (`ValueError: ROOT_ROSTER_MISSING_OR_AMBIGUOUS_CUT_THETA`).
  - Sensitivity θs need contexts too (`FREEZE_CONTRACT_REFUSED: S000`).
  - 10 malformed cut documents refuse, as do a cut below the first node and a cut that leaves no valid row.
- **Tamper.** Rehashed manifests fail verification in three cases: a finite gap row, a gap row relabelled OUTER, and cut rows restored as valid.
- **PROGRAM scope** (real 43 radii, slots/program-manifest pins, illustrative cuts, in process only).
  - Every set equals the oracle. The slots `invalid_primary_GL4` equals the rows inside the first registered node (NGC3198-Q01, NGC3198-Q02).
  - Synthetic ids on the program manifest refuse; so does the program manifest under SYNTHETIC scope.
  - The real cut comes from the v011 run; these cuts only show the mechanism:

| Cut (kpc) | Gap rows | Outer rows |
|---|---|---|
| 20.3 | NGC3198-Q31 | NGC3198-Q32–NGC3198-Q43 (12) |
| 21.0 | none | NGC3198-Q32–NGC3198-Q43 (12) |
| 30.08 | none | NGC3198-Q36–NGC3198-Q43 (8) |
| 40.1 | none | NGC3198-Q41–NGC3198-Q43 (3) |
| 44.08 | none | NGC3198-Q43 |
| 50.0 | none | none |

## LADDER regression (P10)

I ran v003e and v003f on identical inputs: GL4 Q01/Q02 plus root-gated rows, with the same targets.
- Identical: the frozen members (including `row_registration`), envelope, admitted region, reference, sensitivity and alternative results.
- Identical scores: members, envelope, sensitivity, alternatives and headline.
- Score top-level differences: headline_rule, manifest_file_sha256_actual, manifest_file_sha256_expected, manifest_file_sha256_registered, manifest_sha256_self, registration_file_sha256 only.
- Manifest top-level differences: created_utc, headline_rule, manifest_sha256, module, notes, pins, row_registration_rosters, schema.
  - `notes` differ only by the raw-result custody of the two runs.
  - `pins` differ only by the module file (prediction_freeze_c2v003e_cx3v002.py vs prediction_freeze_c2v003f_cx3v003.py), by each run's 20 raw results, and by v003f's 13 root dependencies (5 rosters, the gate, the node artifact, the route-B config and the node sources).

## Findings

### F1 (SHOULD_FIX): the declared alternative set is not bound to slots V002

`_root_rosters_for_alternatives` (L1868) checks three things:
- the pin keys equal the **caller's** declared names;
- each roster carries the exact slots record for its name;
- the primary equals the slots primary.

It never checks that the caller declared all five slots alternatives. API_INTEGRATION states that the writer and scorer require "an exact mapping from all five slots V002 alternative names".

**TESTED.** I dropped one alternative from both the alternatives and the pins. The freeze writes and verifies, and the score lists only the rest:
- without ML_3p6_0.4: BR_A_F10_PRIMARY, ORIGINAL_K, ML_3p6_0.6, GL10_SOURCE_GAUSS_ORDER, DDO154_DISTANCE_NUISANCE;
- without ORIGINAL_K, an EVALUATED alternative: BR_A_F10_PRIMARY, ML_3p6_0.4, ML_3p6_0.6, GL10_SOURCE_GAUSS_ORDER, DDO154_DISTANCE_NUISANCE.

The headline is unaffected, because the primary stays bound to slots. The omission is decided before targets, but it lets a freeze silently drop a root-declared alternative from the record.

**Fix (one line).** Require `alternatives == slots['alternatives']`, exact records and order. This also binds the declared order, which is currently free (reversed order accepted; cosmetic).

### F2 (NOTE): query radii are bound by file position, not by query id

`_load_row_roster` zips the ids (sorted by `data_row_index`) with `qm_doc['rows']` in **file** order.

**TESTED.** A synthetic manifest with its rows listed in reverse binds Q01 to 34.00 kpc instead of 0.25. Under cut A the module then flags 17 rows; the by-id oracle flags 19.

PROGRAM scope is unaffected: the pinned program manifest is in index order, and its radii are re-checked against the slots rows. Fix: use `load_query_manifest(...)['radii_text'][q]`.

### F3 (NOTE): `Rad_unit` is not checked

**TESTED.** A synthetic manifest in Mpc is read as kpc (Q31 bound as 0.023 kpc). Under cut A the module flags only Q01/Q02 (2 rows), while the cut rows silently stay valid; the unit-aware oracle flags 19.

PROGRAM scope is unaffected: kpc, re-checked against slots. Fix: require `Rad_unit == 'kpc'`.

### F4 (NOTE): the A60 inequality is evaluated in metres

A60 states {R_q ≥ first_unconfined_R} in kpc. The module compares `R_kpc·kpc_m ≥ cut_kpc·kpc_m`.
- They agree except when the cut is within one rounding step of a row radius. On the real table, 8 of the 43 radii have such a one-ulp neighbour where the two forms differ.
- They agree for every cut placed at a registered GL4 node radius (node_m/kpc_m): 0 differences.
- Any mismatch with the producer refuses (fail-closed); it cannot change a score.

Item 2 checks that the v011 `apply_cut` uses the same arithmetic.

### F5 (NOTE): PER_THETA contexts must cover every evaluated θ, which fixes the production order

A context is required for:
- every member θ, including a member whose forward raises (enforced at the writer);
- every evaluated sensitivity θ, including failed NGC-nuisance entries.

The sensitivity θs depend on the D1 reference, which is known only after the member results. The same roster pin must serve both the evaluation and the sensitivity (the writer checks both). A production PER_THETA freeze is therefore two-pass:
1. run the members;
2. find D1;
3. run the sensitivity θs;
4. obtain the cut records;
5. root registers the roster;
6. evaluate by replaying the saved raw results.

The alternative is to pre-list the plans of every candidate reference. This belongs in the launch plan.

### F6 (NOTE): small custody points

- A redundant producer gate pin must equal the normalized root pin. The same file named by a non-normalized path refuses (fail-closed).
- At every verify and score, the verifier re-reads and hash-checks 8 hard-pinned dependencies: slots V002, the node artifact, the route-B config and the node artifact's 5 sources. With the rosters, gates and cut records they must stay byte-identical at their paths until scoring.

## TESTED / UNTESTED

**TESTED (synthetic targets):** everything above.

**UNTESTED:**
- the real v011 cx3v005 producer (item 2):
  - its cut-record keys against the root target screen;
  - its `first_unconfined_R_kpc` arithmetic (F4);
  - whether its INVALID rows equal v003f's derivation;
- the node artifact's own derivation from the profile bytes (Codex3 reproduced it; I did not);
- physical certification of any cut, and scientific adoption of any gate;
- any real score.

## Next step

1. Codex3: F1, in `_root_rosters_for_alternatives` (F2 and F3 optional). Re-run my harness by changing the `V003F` path and pin; the four F1 checks must flip to refusals.
2. Root: put the F5 two-pass order for PER_THETA rosters into the launch plan.
3. Claude4: item 2 (v011 cx3v005) once Codex3 posts its finish; it includes the F4 cross-check.

## Files

- `tools/review_v003f_c4v001.py` (`898508c4b3bd8e0579c2a0958474afeee7c9e2b63ecd5a7accac4b2ab532458f`)
- `tools/make_review_c4v001.py` (`9db31efc1460547a154b8053672b9664e5ba5a03edc38c23eedc4dbce1fcd6b7`)
- `runs/run_20261018T141427Z/REVIEW_RESULTS.json` (`db4343bfdf58162aef13667477a464fb169a192eee8ea1e06a39ebb674d3d38a`), with every fixture, roster, cut, gate, manifest and score of the run
- `HASHES_REVIEW_FREEZE_V003F_C4V001.txt`: sha256 of every file in this folder, given in my outbox post
