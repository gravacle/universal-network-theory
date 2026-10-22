# CHECK_V001: independent check of galaxy_m0_forward_c2v003 against c2v001

**Verdict: PASS_WITH_CORRECTIONS.** The code changes are exactly the four listed items and they work as claimed. The three corrections are to documentation only. None of them blocks the KMAX C3, C4 or R calls under v003, and none touches the v001 runs in progress.

## What was done

**Nothing launched.** Everything ran in one of three ways:
- the driver's dry-run (simulate mode), in a process where every process-spawning call raised an error and every file open was logged;
- synthetic tests on toy packets, a toy stage worker and a fake stage runner;
- one read-only check of the saved cube offset files.

**Nothing written outside `check_v003/`.**
- `find -newermt 08:47` over `Universal Network Theory/` shows only the running `CLAUDE2/runs/*` and `CODEX1/OWNED_L4_WORM_LOOP_RUN_V001/*`, neither from this checker.
- In all 18 dry-runs, no file was written outside the report directory.
- The `CLAUDE2/runs` directory was not touched.

**Files checked.** Every sha256 below was recomputed from bytes, and every line of the author's `HASHES.txt` verifies.

| File | sha256 |
|---|---|
| `galaxy_m0_forward_c2v003.py` | `b052e3ae43fcf8782cc9cca99dec2cdc8f7fcbf479af7b92738feb196c00033b` |
| base `galaxy_m0_forward_c2v001.py` | `75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22` |
| prep V007 | `ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42` |
| prep V008 | `bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62` |
| V008 review JSON | `aa12d69f4119983fdcfceb4809971ec08c596aeaf5630c85a51823b36332182e` |
| `KMAX_MATRIX_PREREG_V001.json` | `d5acfc2fea1c99adf7709ab509eb95bf966c0b3d6db7398b091ec2bd305538be` |

**Evidence files** (all in `check_v003/`):

| Script | Result |
|---|---|
| `chk_static_v001.py` | `STATIC_V001.json`, `CHECK_DIFF_V001_V003.txt` |
| `chk_simulate_v001.py` + `chk_dryrun_runner_v001.py` | `SIMULATE_V001.json`, `sim_V001/` |
| `chk_synthetic_v001.py` | `SYNTH_V001.json` (31 of 31 flags true), `synth_V001/` |

## 1. Line diff: only the four items. PASS

- **Size.** v001 has 1581 lines and v003 has 1745. The diff adds **170** lines (164 non-blank, 6 blank) and removes 6.
- **Diff files agree.** Body of `diff -u` = author's `DIFF_V001_V003.txt`, byte for byte (sha256 of lines 3 onward: `bdf94266…`). `CHECK_DIFF_V001_V003.txt` (difflib) has the same added and removed lines; only the hunk boundaries differ.
- **30 change blocks, every one mapped** (`STATIC_V001.json` `change_blocks`):
  - item 1 (prep V008): 11 blocks;
  - item 2 (grid gate): 1 block;
  - item 3 (mask check): 2 blocks;
  - item 4 (CHECK_V001 fixes): 13 blocks;
  - shared: the constants block (items 1+2) and the dry-run summary block (items 1+4);
  - the module docstring.
- **Each removed line has its replacement in the same block:**
  - the docstring line;
  - the `truncation_mask` docstring end;
  - the `route_a_custody` return;
  - the route-A patch target (`AUX['prep']` → `prep_path`);
  - the dry-run override condition;
  - the V007 note.
- **Unchanged from v001:** `SCRIPTS`, `GALAXIES`, `FIXED_ARGS`, `LE_RULE_DEFAULTS`, the schemas and every v001 `AUX` entry. The only `AUX` change is the new key `prep_v008`.
- **No new launch path:** the set of imports is identical, and there is one `Popen` (in `run_stages`), as in v001.

## 2. Prep V008 pin and the only-diff claim, from bytes. PASS

- **Only-diff claim holds.** V007 and V008 are both 14575 bytes and 247 lines. They differ at line 130 only, at byte offsets 7125–7126: `nk>80` → `nk>96`.
- **Guard blocks, executed from bytes** (only the grid block, `nk = …` up to `waves = np.array(`):
  - **G2:** V007 and V008 build a bitwise-identical 72-node axis.
  - **G3, G4, GR:** V007 refuses ("Composite node budget/order mismatch"). V008 builds 84, 96 and 92 nodes, each reflection-symmetric.
  - **G2 nested bitwise:** for G3 and G4, the G2 72-node axis sits bitwise inside the larger axis.
- **The route-A worker matches the shim's assumptions:**
  - `LOCAL['prep']` is a `(Path, sha)` tuple;
  - `paths = dict(LOCAL, …)` is built inside `main()`, after the shim's replacement;
  - pins are verified in `main()`;
  - prep is loaded through `spec_from_file_location`, so the module patch keyed on the V008 path applies;
  - the binding accepts modules by `Path(__file__).resolve()` in that same pin dict.
- **No other module in the loaded chain hard-codes the V007 prep** (grep).

## 3. REPRO simulated plans equal v001's. PASS

v001 and v003 were dry-run here on the same specs. The comparison normalizes only two things: the report-dir prefix, and each generated manifest sha (mapped to its manifest content with that prefix normalized).

| Spec | Stages v001 / v003 | Stage rows | `DRYRUN_PLAN.txt` | Generated inputs | Final rows |
|---|---|---|---|---|---|
| `REPRO_PINNED_ADMIT_PREFIX` | 19 / 19 | identical | identical | identical | identical (12) |
| `REPRO_PINNED_FULL` | 22 / 22 | identical | identical | identical | identical (12) |
| `REPRO_RULE_FULL` | 20 / 20 | identical | identical | identical | identical (12) |
| `KMAX_C2` | 12 / 12 | identical | identical | identical | (none; planning stops at RFS) |

- **Plan text matches the author's runs.** The `DRYRUN_PLAN.txt` bytes for ADMIT_PREFIX (`2addf0aa…`) and FULL (`67c5b208…`) are equal across all four runs: checker v001, checker v003, author's v003 and author's V001REF.
- **Override counts:** 50 of 52 (ADMIT_PREFIX) and 56 of 58 (FULL). The two that are not no-ops are the `le1`/`le2` column-mean `PINS`.
- **The other report fields that differ are exactly the ones DELTA §1 lists:**
  - `driver_sha256`;
  - `identity.route_a.prep` and `custody.prep_code_pins`;
  - the static pins of V008 and the review;
  - `transitive_pins.verified_files`, 45 → 46 (the added file is V008);
  - the route-A recorded-pins note;
  - `summary.overrides_wording`, `overrides_not_noop` and `route_a_prep`.

## 4. G3/G4/GR specs simulate correctly with 84/96/92 nodes per axis. PASS

- **Grids match the preregistration.** `DECLARED_LARGE_GRIDS` equals `KMAX_MATRIX_PREREG_V001.json` for G3, G4 and GR in breaks, orders and total.
- **Dry-runs of the shipped wave-1 specs** (all exit 0, 12 stages, `pin_problems []`, `scipy_imports []`):

| Spec | Normalized nodes | Seed `fourier_points_per_axis` | Seed kmax | Route-A prep | V008 axis |
|---|---|---|---|---|---|
| C3 | 84 | 84 | 3.0 | `LOCAL[prep] :=` V008, patch on V008 | 84 |
| C4 | 96 | 96 | 4.0 | `LOCAL[prep] :=` V008, patch on V008 | 96 |
| R | 92 | 92 | 2.0 | `LOCAL[prep] :=` V008, patch on V008 | 92 |
| C2 | (seed) 72 | 72, seed reused bitwise | 2.0 | V007, no dict item, patch on V007 | 72 |

- **C3, C4 and R against v001 on the same spec.** The plans differ only in two places:
  - **Route A:** the V008 dict item, the patch path and sha, and the seed sha.
  - **Downstream stages:** `SEED_SHA` only.
- **Why `SEED_SHA` changes.** The seed now carries the top-level `c2_changed_fields` annotation. Its `numerical_inputs` differ from the base seed only in `composite_grid_spec`, `fourier_points_per_axis` and `kmax_inverse_kpc` (no `kmax_inverse_kpc` change for R).
- **Grid gate** (`normalize_spec`, `SYNTH_V001.json` D):
  - **Accepted by v003:** the declared G3, G4 and GR, an undeclared 80-node grid, and G2.
  - **Refused by v003:** an 84-node grid with altered orders, an 88-node GR-like grid, 128 nodes, and the 96-node G2-breaks/order-8 grid.
  - **v001 accepted all of them;** it had no gate.
- **Unchanged behaviour.** The `cube`-with-kmax refusal still holds. All 9 shipped specs normalize identically under v001 and v003, and NGC3198 is refused by both.
- **Synthetic sphere and cylinder plans** (S2, Y2 from C2; S4, Y4 from C4):
  - **masked:** offset, fs columns, rotation and feedback;
  - **unmasked:** route A, reference and body;
  - `identity.truncation` carries the mixed-field scope note, and `mask_check` is `PENDING` in simulate mode;
  - G4 plans route A with 96 nodes.

## 5. Mask assertion fires on a synthetic leak and passes on a clean mask. PASS

**Toy packets on the real composite node sets:**

- **Clean masks pass on G2 2/kpc.**
  - Sphere keeps 344048 of 373248 nodes and cylinder keeps 362592. Both equal the CHECK_V001 figures.
  - `vacuous` is false.
- **These all refuse with `StageFailed('MASK_NOT_FIRED …')`, and each message names the file and the count:**
  - one outside row at `1e-300` in `offset_prepared.npz` only;
  - the same in `unit_response.npz` only;
  - an unmasked packet (29200 rows);
  - a NaN outside row;
  - wavevectors that differ by 1 ulp between the two files;
  - a missing `offset_prepared.npz`;
  - a row count that differs from the node count;
  - a cylinder packet checked as a sphere.
- **`-0.0` outside the mask passes.**
- **Large grids:**
  - G4 with a 4/kpc sphere: 755080 of 884736 kept;
  - GR with a 2/kpc cylinder: 762864 of 778688 kept;
  - both pass clean and refuse a one-row leak.
- **The driver's own `_wrap_cache` on a toy cache module.** The wrapped `prepare` passes and records the same 344048 kept nodes. The bypassed `prepare` refuses.

**Call level** (`cmd_run` with every stage replaced by a fake that writes only the toy offset npz files):

- **Sphere with a leak:** ends `FAILED_AT_STAGE`. The reason is `MASK_NOT_FIRED: unit_response.npz has 1 nonzero rows …`. The stages called are route_a, reference, body and offset only, so **no column stage starts**.
- **Sphere, clean:** continues to the fs columns. `identity.truncation.mask_check` records kept 344048, both file shas and `vacuous` false, and there is exactly one `mask_check` progress event.
- **Cube:** the offset request has `mask=None`, and there is no check and no event.

**Real bytes, read-only.** The saved cube offset (`DDO154_BODY_SOURCE_OFFSET_RUN_V001/offset`) was checked as if a sphere or cylinder call had produced it:
- sphere: refused, 29200 nonzero rows outside the mask;
- cylinder: refused, 10656 rows;
- cube: vacuous;
- the files are unchanged after the read.

## 6. Shim dict-item replacement (item 1 mechanism). PASS

The test runs the driver's `_stage` on a toy worker that has the same structure as route-A v002.

- **`LOCAL['prep']` replaced with the V008 toy, plus a patch on V008:**
  - the worker loads V008 and gets the patched `COEFFICIENT`;
  - `LOCAL` order is kept (`first, prep, last`);
  - the worker's own pin dict holds the V008 path in position 2.
- **Without the dict item:** the worker loads V007, and the V008 patch is not applied. This is why the driver keeps the patch target equal to the prep choice.
- **Refused with a nonzero exit and no output:**
  - an absent entry;
  - a pin mismatch;
  - a target that is not a dict.

## 7. Item 4 fixes. PASS

| Fix | Result |
|---|---|
| `require_bracket_source` | `{0:1.0}` with n=3 raises `StageFailed('rfs column(s) [1, 2] failed; no bracket source')`. v001's `rule_brackets` raised a bare `KeyError`. |
| Absolute paths | Relative paths are refused by v003 at normalization; v001 accepted all of them. Checked for coefficients, pinned controls, and admit `route_a` attempt/checkpoint, reference and body. |
| `picard_bound_met` | Correct by code reading (`None` if no bound or no change, else `chg <= bnd`). Not exercised here; the author's t10 covers it. |
| Annotations, docstrings, summary wording | Present as described in DELTA §4. |
| `c2_changed_fields` | Only `numerical_inputs` and `pins` are read from the seed by any of the 13 stage scripts (grep), so the annotation has no computational effect. |

## 8. No scipy, no target, no launch. PASS

- **No scipy.**
  - v003 imports no scipy, and its import set equals v001's.
  - Every dry-run reports `scipy_imports []`, with 46 transitively verified files.
- **No target access.**
  - No added line references NGC, SPARC, observed or target data. The new path literals are only the V008 prep and the review JSON.
  - None of the 18 dry-runs opened any file whose path contains NGC, SPARC or target.
- **No launch.**
  - Every dry-run ran with process spawning disabled and created no `stages/` directory.
  - `executed_stages` was 0 in every report.

## Corrections (line-specific)

1. **`INTERFACE_V003_DELTA.md:9`.** "164 lines added, 6 removed" should read "170 lines added (164 non-blank), 6 removed".
2. **`galaxy_m0_forward_c2v003.py:75–76` and `INTERFACE_V003_DELTA.md:17–20`: the review's scope is not stated.**
   - **What the review covers.** The V008 review (`aa12d69f…`, PASS_SCOPED) reviewed V008 as used by `ddo_current_source_motion_derivative_audit_v001.py`, on G2 breaks with all panel orders 8. That is a 96-node grid that v003 refuses.
   - **What it does not cover.** Its `limits` say it does not certify 96³ memory or runtime fit.
   - **What the G3/G4/GR route-A use actually rests on:**
     - V008 being byte-identical to V007 except the budget literal (verified here);
     - V007's existing route-A review.
   - **Fix.** State this, and do not cite the review as covering route-A use.
   - **Open:** 96³ route-A memory under the campaign's 4 GiB per-call RSS cap is UNTESTED. The deciding test is the C4 route-A stage's peak RSS in the monitor log; the cap makes failure loud.
3. **`INTERFACE_V003_DELTA.md:112` / §5 (125–129): the admission consequence is not stated.**
   - **Background.** The `c2_changed_fields` annotation is not byte-neutral. For every non-reused seed (any changed Eref, ℓ_F, γ or grid), the seed sha and therefore the route-A identity differ from v001's. §4 says this.
   - **Consequence.** v001 and v003 route-A checkpoints at non-base parameters cannot be admitted across versions: `route_a_custody` gives BLOCKED on the seed sha, which fails loudly.
   - **Fix.** §5 should say so next to the V3 driver-sha note. C2 and the reproduction specs are unaffected, because their seeds are reused bitwise.

## Notes

- **Mask assertion scope.** The assertion proves that rows outside the mask are exactly zero, which is what CHECK_V001 §3.2 asked for. It does not prove the mask is exactly the declared one: over-masking appears only in the recorded `kept_rows_all_zero`. Example: a sphere-masked packet checked as a cylinder passes, with 18544 kept rows all zero. Refusing `kept_rows_all_zero > 0` on `unit_response.npz` would close that, but it is optional.
- **`picard_bound_met` is in `result.json` only.** The campaign record half of CHECK_V001 further defect 2 is still open, because `campaign_c2v001.py` is reused unchanged.
