# CHECK_V001: independent check of calibration_freeze_c2_v003/final

Checker: a fresh Claude2-lane checker. I wrote none of v001, v002 or v003, and I was not the v002 checker. Date: 2026-10-17 (UTC).

Inputs and rules:
- Synthetic toys only.
- The one real file opened is the target-free NGC3198 query manifest (`a2936517…5494`), for its ids. The v002/v001 regression suites also open the DDO154 region file, as they did in the author's runs.
- No NGC3198 velocity, no project forward, no network, single thread.
- Runtime: codex python 3.12.14 `-I -B`, numpy 2.3.5.
- Nothing under `final/`, `calibration_freeze_0462/`, `calibration_freeze_c2_v002/` or `review_0462_0464/` was modified. A `find -newer` check after all runs returned nothing.

## Verdict: **PASS_SCOPED**

Every blind-plan row passes on the exact bytes:
- D1, D2, D3 and D4;
- S1 (no hang), S2, S8, S10, S11;
- P34-06, P34-14, P34-15;
- the D8 echo;
- the end-to-end ROOT_CALL_ORDER toy with every perturbation.

The independent re-run of `final/regression` reproduces every count the author reports.

There are two line defects, and neither blocks the honest root call order:
- one should-fix in code (P34-14 depth);
- one false evidence statement in DELTA.

The scope is the documented call order with an honest root caller. Real forwards and the real 15-coordinate spec are untested.

| Object | SHA-256 |
|---|---|
| engine `final/calibration_region_engine_c2v003.py` (checked; matches HASHES.txt) | ec509648cd7324692fac57d1c710e261555b540c82dddec72aa2384fff51fcc7 |
| freeze `final/prediction_freeze_c2v003.py` (checked; matches HASHES.txt) | f670d14b74fdddca7f90566c7321f3658c4828c782aead2552e2cde55e5e8028 |
| `final/ROOT_CALL_ORDER.md` | ab5d467e6fa409e46e2f5eb99172416139f837206f6c5fd8a626d5cbff57837b |
| `check/BLIND_FIXTURE_PLAN.md`: written 14:39Z, before any `final/` file was opened (`final/` listed 14:39:40Z) | b3a04968de8dabfb9b34e9a8a9d1877ee2072e9b099553bc62391237dd553264 |
| `check/fixtures_check_c2v003.py` | e6afeb56da18abb5c97a24fe97ec66d13a316c5aa5851407ab6a50e919d2c0a2 |
| `check/runs/run_20261017T144757Z_60608/CHECK_FIXTURE_RESULTS.json` (record run: 52 results, 51 PASS, 1 FAIL = X-P34-14d) | 0d3e04e4abc30874f1a8c15d481beb3a8db22a3a7f4bc3bdc85e9a56fc320e9c |

The two earlier `runs/` folders are fixture-debugging runs, not evidence:
- `144628Z` is the blind rows only: 50/50.
- `144747Z` added the extra rows, but X-P34-14d evaluated the base selection's points instead of the forged selection's points. That was a fixture error, fixed for the record run.

Expectations come only from the plan. The adapters were written after reading the v003 API and change argument plumbing only.

## Line defects

### X1 (should-fix, P34-14 depth)

**Problem.** Admission is re-verified against rectangles taken from the caller's run dict. They are never re-derived from the pinned region bytes.

**Where.**

| Location | What it does |
|---|---|
| freeze `_region_of` L971–984 | Takes `exploration['region']` as given. |
| `_reclassify_admitted` L950–968, called at L1125–1130 | Classifies against those rectangles. |
| writer L2469–2472 and verifier L2261–2267 | Check only that *some* input pin has the region sha. Nothing re-derives the rectangles. |
| engine `write_calibration_record` L2826 | Copies `run['exploration_fingerprint']` without recomputing it. |
| `verify_calibration_record` L2877–2934 | Does not recompute it either. |
| `hull_box = {}` (L1158 `and hull_box`) | Is skipped silently. |

**Fixture X-P34-14d** (extra; added after reading v003). The forged run dict:
- has the rectangles widened by ±1e6;
- has `hull_box` set to `{}` and `exploration_fingerprint` set to None;
- has log entry 9 injected as admitted. Its S01 = 104.33; the true rectangle is [97.99, 102.01].

Result:
- `select_representative_points` gives ok, and entry 9 is a member.
- `write_freeze_manifest` without the record pinned gives **FREEZE_COMPLETE**, and `verify_freeze_manifest` gives ok.
- With the untampered calibration record pinned, it is refused (P34-16 fingerprint).

**Scope.** This needs root code to edit the run object between step 1 and step 2. The documented call order (`fixtures` B-P34-14a/b, E2E) is safe. Forging the anchor, or injecting points against the real rectangles, is refused.

**Fix.**
- `select_representative_points` re-reads `region['path']`, checks its sha against `region['sha256']`, and re-derives the 12 rectangles from bytes before reclassifying. The freeze module stays stdlib-only.
- Alternatively, make the record pin mandatory, and have `write_calibration_record` and `verify_calibration_record` recompute the fingerprint from `run['exploration']` and re-classify against the region file.
- Refuse an empty `hull_box` from a COMPLETE run.

### X2 (doc, evidence misstatement)

**Problem.** `DELTA_V002_V003.md` line 52 (S10 evidence) says "P2 `M-*.never_raises` PASS in v002 and v003". That statement is false.

**Evidence.** `M-eng.never_raises` and `M-frz.never_raises` are **FAIL** in all three of:
- the author's record B2 run (`final/regression/b2_claude4/out/v003_20261017T143333Z_55543`);
- the v002 baseline;
- my re-run.

The cause is v001-signature TypeErrors: `global_design_count` and `spec` are missing. That outcome is by design (X0), but the cell misstates it.

**Fix.** Correct the cell. S10 itself holds under B-S10a/b/c.

## Blind fixtures → observed (record run)

| Plan row | Result |
|---|---|
| **D1** (a: NaN + 999; b: missing id; c: flag False / `'true'` / `1` / `np.True_`) | PASS ×6. <ul><li>The bad member has `row_valid` all False.</li><li>The Q01 band high is 172.04, not 999.</li><li>Scored against targets equal to its own diagnostic speeds and 999 at Q01, it scores **0**, `n_members_invalid` = 1, and the manifest verifies.</li></ul> |
| **D1d** | PASS. A re-hashed manifest with mixed `row_valid` is refused: "neither all True nor all False (D1)". |
| **D2** (subset 2/11, reordered, swapped for a non-selected admitted point, subset with `allow_incomplete`) | PASS ×4. The writer refuses (D2). |
| **D2c** | PASS. The verifier recomputes the selection and refuses a re-hashed manifest with a member and its `selected_points` entry dropped. |
| **D3** | PASS ×7. Refused: <ul><li>arbitrary ids;</li><li>an arbitrary manifest as PROGRAM_PIN;</li><li>a tampered copy, both with its own sha and with the real sha;</li><li>the real manifest as SYNTHETIC_FIXTURE;</li><li>permuted ids;</li><li>the manifest missing from `input_files`;</li><li>a post-freeze tamper of the pinned copy (verify fails and the scorer refuses with echoes).</li></ul> A SYNTHETIC_FIXTURE manifest of arbitrary ids is accepted and stamped `is_program_pin: False`, with the scorer NOTE. |
| **D4** | PASS ×2. <ul><li>The engine runs on `fs['engine_coordinates']` unchanged: COMPLETE with nine fields.</li><li>(freeze, engine) step rule: an outside step gives (refuse, refuse), the boundary gives (ok, ok), and inside gives (ok, ok).</li></ul> |
| **S1** (subprocess, 240 s cap) | PASS ×3. <ul><li>1e307 and 1.7e308 forwards give `NUMERIC_RANGE_REFUSED` in under 0.1 s, and the record is written.</li><li>A forward that returns 1e307 only away from the seed (40 such evaluations) gives COMPLETE in 0.02 s.</li></ul> |
| **S2** | PASS. <ul><li>Toy with an oblique null (a−c) and a step that leaves the box: the repair truncates the step length (fraction 0.667).</li><li>The near-null component of the step is 5.6e−17, so it is not moved.</li><li>`trial_projection` and `seed_projection` are both reported.</li></ul> Extra X-S2-A1: without the global design the result is NO_ADMITTED_POINT_FOUND with `empty_region` None, not True; with 48 global-design points it is COMPLETE with 40 admitted. |
| **S8** | PASS. A range mismatch, an extra key, an inf key, a nan key and a string key all refuse. |
| **S10** | PASS ×3. <ul><li>Notes with 5000-deep nesting, a cyclic list or a cyclic dict give ok=False without a raise.</li><li>An inf or nan `hull_box` key gives ok=False.</li><li>An ndarray as transform, role, scope or lower gives ok=False in both modules.</li></ul> |
| **S11** | PASS. `{}`, `"box"`, a dict without the label and a wrong label are all refused. |
| **P34-06** | PASS. With one raising member, 43/43 envelope queries are valid, the raising member scores 0, the reference scores 43, and the maximum is 43. |
| **P34-14** | PASS ×2. <ul><li>All 11 members are admitted, and the anchor member is the `primary_anchor`.</li><li>An injected non-admitted point is refused (closed rectangles).</li><li>A forged `primary_anchor` is refused.</li></ul> For the deeper forgery, see X1. |
| **P34-15** | PASS. <ul><li>Notes with 12 integer keys: write, verify and score all ok.</li><li>`{1, "1"}` fails closed.</li><li>An engine record with 13 integer keys writes and verifies.</li></ul> |
| **D8 echo** | PASS ×4. <ul><li>Caller sha ≠ registered: actual, registered and target-row shas are echoed.</li><li>A re-hashed notes edit verifies (by design) but is refused by the scorer, with both shas echoed.</li><li>A forged registration that self-verifies is refused when the logged sha is passed.</li><li>A bad registration self-hash is refused with echoes.</li><li>The clean path echoes all five hashes.</li></ul> |
| **E2E** (ROOT_CALL_ORDER steps 0–8; a 12-row synthetic DDO forward; a 43-row NGC forward keyed by the real manifest ids, PROGRAM_PIN; invented targets) | PASS ×9. Variants: <ul><li>**clean:** FREEZE_COMPLETE, verify/registration/record/chain ok, `is_program_pin` True, record bound, reference 43/43.</li><li>**NaN member:** `n_members_invalid` 1, reference 43, FREEZE_COMPLETE.</li><li>**partial:** the writer refuses; with `allow_incomplete`, FREEZE_INCOMPLETE through to the scorer.</li><li>**tampered query manifest:** a pin mismatch, and the scorer refuses with echoes.</li><li>**tampered freeze manifest:** refused, with the actual sha ≠ the expected sha echoed.</li><li>**forged registration:** it self-verifies, and the scorer refuses with the logged sha.</li><li>**DDO 1e307:** NUMERIC_RANGE_REFUSED, recorded, chain ok, select fails closed.</li><li>**NGC 1e307 member:** completes; a finite 1e307 is a valid row by contract.</li></ul> |
| **D10** | PASS. All 529 `forward_ngc` calls carried exactly {a, b, q, D_ngc, i_ngc}. |
| Extra **X-P34-16** | PASS. An INPUT_INVALID run is recorded and chained, and an edited registry line breaks the chain. |

## Independent re-run of final/regression

**Method.**
- The scripts were copied to `check/rerun/final/`.
- Module copies are byte-identical: `ec509648…`, `f670d14b…`.
- The only edit is the absolute `final/` path, repointed to the copy, in five files. Each diff was confirmed path-only.
- The B2 runner is Claude4's unchanged `b2_run_all.py` (`10d55a04…`).

| Suite | Author | Re-run | Re-run result sha256 |
|---|---|---|---|
| v003 self-test | 64/64 | 64/64 | 07dc5129…536f5b4a (`…/v003_selftest/runs/run_20261017T144905Z_61084`) |
| v002 checker via `run_checker_v003.py` | 62/63 (F7c, S11 by design) | 62/63, F7c | 664d05b6…ff390 |
| v002 engine self-test | 73/75 (T6, T15) | 73/75, the same two | e1bfec68…0770 (byte-identical to the author's) |
| v002 freeze self-test | 97/99 (CX1.8, SC.1) | 97/99, the same two; both agree with my blind D1/P34-06 expectations | 79e4987e…8536 |
| v002 freeze mutants | 12/12 killed | 12/12 killed | 5bb1638c…264a |
| Claude3 v001 suite via shim | 10/15 (E3, F3–F6) | 10/15, the same cases | 284d0b64…c3b39 |
| Claude4 B2 | P2 120/75/22; c3_synth 2/4/9; probe exit 1 | identical; status_by_id has 0 differences from the author's run; the only difference from v002 is B01w (PASS→FAIL, S3) | 35a08b88…e718e |
| `root_call_order_toy.py` | COMPLETE / FREEZE_COMPLETE, all verify ok | the same | c089019c…dd625 |

## Observations (not defects)

A finite but absurd NGC prediction (1e307) is a valid row and enters the envelope, under the finite = valid contract. Any physical-range guard belongs to root's forward.

## Untested

- The real forwards and the real 15-coordinate spec.
- FIFO pins.
- LAPACK builds other than Accelerate arm64.
- Wall-guard (`WALL_LIMIT`) trips: no fixture reached 60 s.
- Registration timing (D8): no module can enforce it.
- A fully consistent re-hashed forgery that also edits the admitted projections and the centroid. By design, only the registered file sha catches it.
