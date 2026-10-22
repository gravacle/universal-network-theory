# Review: NGC driver v011 cx3v005 (final cx3r004), delta against the v011 review

Claude4, dispatch 0544 item 2, with 0547 (K_big 16/32) and 0548 (STAGE0_GRID_OUTER). Written Sun Oct 18 15:16:18 UTC 2026 (`date -u` at write).
In process, plus dry runs only.
- No stage was executed and nothing was launched.
- No target, velocity, C5H or `runs_ext/UVT_*` file was opened.
- Nothing was written outside this folder.

## VERDICT: PASS (0 blocking, 0 SHOULD_FIX, 3 NOTE)

Scope: the exact bytes of `stage0_alternative/galaxy_m0_forward_c2v011_cx3v005_cx3r004.py` (sha256 `39c505175905576ff1029ede4be20be765ba47967b5a6eedf1298bd7c4305895`), on r5 pins.

- F1–F5 and N3–N5 of `review_ngc_v011_c2/REVIEW.md` (`7052a33e0c90218bab1138a9e3514f1baa1974d4cafcd51dc958069a19f8f5a3`) are closed.
- The 0547 K_big 16/32 specs and the 0548 STAGE0_GRID_OUTER isolation behave as ruled.
- B0 shows 0 differences.
- The driver and freeze v003f derive identical gap and cut rows on every cut I constructed.

## What was reviewed (sha256 from bytes)

| File | sha256 |
|---|---|
| `ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/galaxy_m0_forward_c2v011_cx3v005_cx3r004.py` | `39c505175905576ff1029ede4be20be765ba47967b5a6eedf1298bd7c4305895` |
| `tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` | `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` |
| `ngc_route_tail_readiness_cx3/v011/r5/galaxy_m0_forward_c2v011_cx3v004.py` | `984fb50580e702446c0ff30830bd4f751ef6e8baa9bc5e84e8f6b79918b3b904` |
| `ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_grid_cut_cx3v001_cx3v005.py` | `5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353` |
| `ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` | `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` |
| `ngc_f10_c2/route_b_v006/configs/GALAXY_CONFIG_NGC3198_C2V006.json` | `64b6f1fadb432b1d5e2ee5b54620fb0c4d2cdb59e425e8034458e0dcd58ee441` |
| `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` | `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494` |
| `freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` |
| `stage0_grid_gate_c2/candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz` | `bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5` |
| `freeze_score_readiness_cx3/v003f/prediction_freeze_c2v003f_cx3v003.py` | `debc254744a40e9d5cb9f856dc922f24b398b6a77c71eb4c71709c98ce398306` |
| `ngc_freeze_inputs_c3/NGC3198_FREEZE_SLOTS_C3V002.json` | `4c5951cbef9aa2c1cf7e7e4c859b59a7aafb5476bd7e59c20caef769376f6c7e` |
| `ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/SPEC_REGISTRY_V001.json` | `c5abc2d5bbb501b71c9b192919f799879aae4bb09d309915ff9a26f99a111e07` |
| `review_ngc_v011_c2/CUT_WIRING/CUT_TEST_FIXTURE_30KPC.json` | `9e5901da7fd2e94375dd1eeda12cf3e67d0f1603e223b9ee425aa5b30f069633` |

Codex3's `HASHES_V001.json` (`9c4a4c4e0540691599a55143342734cdf943b5473fe7d5036cabb8fc461634c4`) lists 2888 entries. All re-verify from bytes, with 0 mismatches (`runs/HASH_MANIFEST_CHECK_C4V001.json`, `5a2605fb7aeb2aef1226ca032bb44eba681ba94d39717ef59e8f90f1b8eb7e3c`).

## Method

My own tools are in `tools/`:
- `review_cx3v005_c4v001.py` (`16432eb709243f23ddfa8e2a81ca5ceb6bebb05e9138339cceba8da3b58d013d`): in process. It loads the author modules from pinned bytes and calls them with my own synthetic inputs.
- `guarded_dry_run_c4v001.py` (`c0f4e314b73a7c3ee7e541a55ad4846dc77cdf0c85ce63b122d022b0fff157af`): one fresh guarded process per dry run.
- `b0_and_dry_c4v001.py` (`176dc0311d99f4a512a57961a8bf4a14b8330207820daeafe7084e8c95c89930`): the B0 checks and the parametric dry runs.

**Audit hooks.** They refuse subprocesses inside the driver, network, deletes, renames, forbidden paths, and writes outside my run directories.

**Final runs:**
- `runs/run_20261018T151351Z/REVIEW_CX3V005_RESULTS.json` (`31506b0974256b642358c28de5d693102dab6d09aa3e9393739aea3dd50690ad`): **123/123 checks PASS**, 0 denials.
- `runs/b0_run_20261018T151147Z/B0_AND_DRY_C4V001.json` (`98b7b0327142a70be8870e9e9b4677429ee3da3a952ae09bdfb2000c1be01eba`).
- `runs/run_20261018T151145Z` is superseded. It is an earlier final run with the same results, made before the N1 note check was added (122 checks).

## Structure

- **Prefix.** The driver is byte-identical to v010 r5 (b5cc62af) up to the parent's `__main__` guard, so the DDO code paths are unchanged.
- **Appendix delta against cx3v004.**
  - Added: `=STAGE0_GRID_PIN`, `=STAGE0_SLOTS_PIN`, `=V011_STAGE0_PINS`, `_cmd_run_ngc_cx3v005`, `_ngc_v011_stage0_context`, `_ngc_v011_stage0_flag`.
  - Changed: `=V011_B_STAGES`, `=V011_PINS`, `_ngc_v011_dispatch`, `_ngc_v011_seed`, `cmd_run`, `final_rows_check`, `normalize_spec`.
  - Removed: none.
- **NGC run copy.** `_cmd_run_ngc_cx3v005` differs from the r5 `cmd_run` in 8 lines, all of them scoped:
  - `final_rows_check(..., nspec)`;
  - the STAGE0 result label;
  - the headline text.
- **DDO calls.** These still take the original `_V010_RUN`.

## Results against the v011 review findings

| Item | cx3v005 | Evidence (all PASS) |
|---|---|---|
| **F1**: outer-cut rows not tied to the cut | **CLOSED** | 69 S2 checks over 7 cuts (the Claude2 30.347 kpc fixture, a node radius, three exact row radii, 21.0 and 50.0). The exact pinned rows are accepted. Every perturbation refuses: an interior OUTER or GAP label, an outer or gap row reported valid or finite, OUTER/GAP/INNER relabels, reorder, a dropped row. Special reasons with no pinned cut refuse, and so does a cut on a tail-OFF spec. The GL10 member uses order-10 nodes (cut 2.0283 kpc: GL4 makes NGC3198-Q05 a gap row, GL10 does not). A degenerate cut that leaves every row INVALID is refused. |
| **F2**: a real cut fails the whole call | **CLOSED** | `QUERY_OUTSIDE_RETAINED_SUPPORT` is registered. The route-B column mean's own `query_partition`, extracted by AST, equals the assembly rule on 571 cuts: 549 agree, 22 refused by both, 0 mismatches. At the 30.347 kpc fixture, the gap is NGC3198-Q36 and the outer rows are NGC3198-Q37–NGC3198-Q43. |
| **F3**: route A accepts empty evidence | **CLOSED** | `normalize_spec` refuses empty evidence before any solve (`NGC_CUT_CONFINEMENT_EVIDENCE_REQUIRED`). `apply_cut` requires a non-empty dict. Both preps, A2 and STAGE0, load the cx3v005 helper by its pinned path, which is the r003 loader fix. |
| **F4**: K_big drift against A55 | **CLOSED as ruled** (A60/A64; 0549 fixes production at 32) | The 8 specs (route A/B × K16/K32 × A2/STAGE0) all have gas M_s 96 and all normalize. All 8 dry runs exit 0 with an 11-stage plan, empty `executed_stages`, 0 binding blockers, exactly the two pending certificates (EPS, LO), and K_big in the plan equal to the spec. **B0 (r5 against r004):** re-comparing Codex3's saved trees gives 41/56 completed and identical, 15 equal refusals (no evidence) and 0 bad. My own re-execution gives 41/56, 15 and 0. The derived plans give 6/6. |
| **F5**: unused `k_domain` | **CLOSED** | It is refused with tail ON and with tail OFF. |
| **N3**: headline names one reason | **CLOSED** | The headline text names INNER, OUTER and GAP. |
| **N4**: list spec raises AttributeError | **CLOSED** | A list, None, int, str or float spec gets a typed Refusal (`SPEC_OBJECT_REQUIRED`), both at normalize and at dispatch. |
| **N5**: fe5 with NGC tail-OFF | **CLOSED** | fe5a2f06 is refused with tail ON and tail OFF. Missing coefficients are refused in both modes. |

## 0548 STAGE0_GRID_OUTER isolation

- **Flagged spec.** It normalizes with `coefficient_alternative`, the slots-successor registration pin and coefficients bdb9016c. The A2 headline spec normalizes with neither key.
- **Refused, 8 cases** (`S6_*_refused`):
  - an unflagged STAGE0 grid; a flagged A2 grid; a flagged fe5 grid;
  - an unknown alternative name;
  - a flag on a tail-OFF spec, a GL10 member, a non-headline entropy K, or a DDO154 spec.
- **Table swap.** The pin and galaxy tables are swapped only inside the context, and restored by identity after both a normal and an exceptional exit.
- **Slots CX3V003 registration.** STAGE0 is `headline: false` and `NOT_EVALUATED_BEFORE_FREEZE`, with the bdb9016c grid pin. Its OUTER rows are NGC3198-Q36–NGC3198-Q43, which equals the manifest rows with R ≥ 30 kpc.
- **Sources.** The STAGE0 prep differs from the A2 prep only in `COEFFICIENT` and `COEFFICIENT_SHA`. The STAGE0 workers and manifest writer differ only in pin strings.
- **Dry reports.** bdb9016c appears only in the flagged reports; fe5a2f06 in none.

## Cross-lane check (my v003f F4)

- **Same radii.** The route-B config's 43 query radii are bitwise equal to the manifest `float(Rad_text)·kpc_m`.
- **Same rows.** v003f's `_row_contract` equals the driver's rows on 571 cuts, refusals included: 0 mismatches.
- **Nodes.** The registered nodes regenerate bitwise: GL4 100 and GL10 250.
- **Admissible cuts.** `apply_cut` accepts only roster radii.
  - The full GL4 layout has 204 radii. The 30.347 fixture is registered node 45.
  - Claude2's cut-wiring check (`CUT_WIRING_C2R.json`) found the route-B full prefix equal to the route-A roster prefix (156 radii).
  - At every one of the 204 layout radii, the metre and literal-kpc forms of A60 classify all 43 rows the same: 0 differences.
- **Result.** The one-ulp edge noted in v003f F4 cannot be reached by an admissible cut.
- **Screen.** The full cut-record key set passes v003f's root target screen.

## Notes

**N1 (TESTED).** With no cut pinned, the driver's inherited v010 rule accepts `QUERY_INSIDE_INNERMOST_NODE` on an interior row (Q20). The binding of inner rows to Q01/Q02 is enforced by the freeze's root roster (v003f/v003g; my v003f P2 refuses Q20), not by the driver. Unchanged from v010.

**N2 (source).** `_ngc_v011_stage0_context` swaps the module globals `V011_PINS` and `GALAXIES` for the length of a call. That is safe with one call per process (the CLI). A threaded, multi-call in-process use would need a lock.

**N3 (Codex3 limitation, confirmed).** The 8 specs keep source-readiness fixture coordinates. They do not show that those coordinates are the headline admitted DDO154 calibration points. Root must supply those points, for the headline and for STAGE0, which is defined at those points.

## TESTED / UNTESTED

**TESTED:** everything above. These are in-process calls on synthetic finals, and dry plans; no stage ran.

**UNTESTED:**
- real stage execution;
- physical confinement, or a real cut record from a run;
- route-A cut-edge stencils and nonlinear feedback;
- runtime I1-T;
- K_big 32 certificate coverage (EPS, LO and GQ to 91 /kpc; root workflow, 0549);
- the GL10 continuum;
- any score.

## Next step

No fix is required for cx3v005. Production uses K_big 32 (0549) once its certificates land, with the root-supplied admitted coordinates (N3).

## Files

- `tools/` (5 scripts, including this generator: `183b1fb5c56530025ec862f94df2c7f33336dbb62a5198ac6d09160ca71369a9`)
- `runs/` (the final and superseded in-process runs, and the B0/dry run with every dry-run report tree)
- `HASHES_REVIEW_NGC_V011_CX3V005_C4V001.txt`: sha256 of every file here, given in my outbox post
