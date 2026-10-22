# INTERFACE: gal_c2v005 stage successors, schema V005, driver c2v009 (Claude2 lane `stage_successor_gal_c2v005`)

## Status

READY_FOR_CHECK. Nothing real was launched. All evidence comes from guarded dry runs, in-process admission calls on the pinned stage bytes, run-mode calls that are BLOCKED or captured before any stage, and synthetic comparator fixtures. The deciding tests below are for root to run.

Decision files:
- Pinned (FROZEN): V003 addendum `5bef6552` (A13: "Deciding work: the stage successor gal_c2v005 and schema V005").
- Cited by name only: the open `ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md` A23. It is not pinned.

## What changed (and nothing else)

| Artifact | sha256 | Change |
|---|---|---|
| `schema/GALAXY_CONFIG_SCHEMA_V005.json` | `f9b8d48e…042a` | V004 `8fc7ef48` plus `per_call_geometry.DDO154.fields` = the 5 fields; `admission_rules_v005`; identity keys. Every field and member entry is byte-equal to V004, so the DDO154 literals are still the 4.04 Mpc files. |
| `stages/*_gal_c2v005.py` (11) | see `stages/BUILD_STAGES_C2V005.json` | Built by `build_stages_c2v005.py` from the gal_c2v004 bytes v008 pins, using asserted edits to the shared admission block only (details below), plus a header comment. |
| `configs/GALAXY_CONFIG_*_GAL_C2V005.json` (3) | DDO `c21f1272`, NGC `299ce971`, GL10 `0873b6a4` | The c2v006 files with only `schema`, `generator` and `note` changed. Format and fields are unchanged. |
| `driver/galaxy_m0_forward_c2v009.py` | `237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb` | v008 `f8e47701` plus the pins, via `make_driver_c2v009.py` (23 asserted edits). The diff is `driver/DIFF_V008_V009.diff` (7 hunks). |

### The edits to the shared admission block

They are identical in all 11 stages:
- Head comment.
- Schema pin moved to V005.
- New constant: `PER_CALL_GEOMETRY={'DDO154':('source.profile','source.monotone_source','radial.outer_edge_kpc','observation.binding','observation.query_rows')}`.
- The PER_CALL rule gains one conjunct:
  `and not (n in PER_CALL_GEOMETRY.get(galaxy,()) and n in ((schema.get('per_call_geometry') or {}).get(galaxy) or {}).get('fields',()))`

The rule therefore has two locks: the stage constant AND the pinned schema declaration. The five fields are exactly v008's `GEOMETRY_CONFIG_FIELDS`, which are what v003c's `derive_geometry`/`geometry_inputs` produce. Inclination is not included, and NGC3198 has no entry.

### The driver diff (v009 vs v008)

- docstring;
- `BIND7`;
- the 11 `SCRIPTS` stage pins;
- `GC_SCHEMA` and `GC_SCHEMA_NAME`;
- the 3 `GALAXY_CONFIG_FILES`;
- `ADMISSION_HEAD` (this is what `binding_blockers` locates);
- 2 record texts: the probe `rule` and the `GEOMETRY_NOT_ADMITTED` refusal.

The following are unchanged: `GENERALIZED` (bases and formats), the producer rules, the geometry path, custody, and the comparator.

The NGC `blockers` note at L347 still says "gal_c2v004". This is left on purpose, so that the NGC reports stay identical under T. It is documentation only.

The other diffs are in `diffs/`:
- 11 stage diffs, each 5 hunks: header, admission head + schema + constant, docstring ×2, rule line;
- the schema diff (3 hunks);
- the config diffs;
- the config-generator diff.

## Proofs (TESTED-POSITIVE unless marked)

Results files:
- `tests/runs/final/COMPARE_DRY_2.json` (`41c50d02`; harness `01cc8867`): **53/53**.
- `unit/TEST_RESULTS.json` (`1a8f9005`): **77/77**.
- `compare_distance/FIXTURE_RESULTS.json` (`a41a4d55`): **9/9**.

`COMPARE_DRY.json` in the same folder is the first compare pass. It was made with harness `46fb39d1`: 52/53, and the DEC3 normalization was fixed afterwards. It is superseded; it is kept, not deleted.

Run conditions:
- 51 dry runs (46 exit 0; the 5 non-zero ones are the expected refusals);
- every run under `guard_gal_c2v005.py` (a lane-root copy of the v008 guard): 0 denials over 56 logs;
- no velocity-like path was opened;
- the only CLAUDE2/runs entry read was `A2_ANCHOR_F10_RUN_V001`.

**T** is the declared substitution gal_c2v004 → gal_c2v005: the stage paths and shas, the schema path/sha/name, and the config paths/shas.

### At D = 4.04, v009 is identical to v008 after T

- **D1** (16 specs): every request, every generated input file, the normalized spec, the remaining refusals and the identity are equal after T. Both runs exit 0, and there is no geometry record.
  - The 16 specs are: deciding (i) `4ac5527a`, both deciding-(ii) specs, ADMIT_ROUTE_A, ADMIT_PREFIX_C2V001, PINNED_FULL, RULE_FULL, A2F10, RA1/2/8/64, ADMIT_ROUTE_A_RA1, the NGC templates ×2 and the NGC seed.
- **P0**: T is well formed. Every key occurs in the v008 outputs, no old value occurs in the v009 outputs, and the pairs are distinct.

### The saved inputs reproduce

- **S1**: v009's dry run against the saved CODEX1 launches matches v008's exactly. Examples: ADMIT_PREFIX 17/17 stages with all inputs identical, PINNED_FULL 20/20. Every generalized call is accepted by its own gal_c2v005 admission, and there are no binding blockers.
  - RULE_FULL gives 12/15, the same per-stage list as v008. The rule brackets for the LE columns are by design not the saved manual controls.
- **S2**: the saved anchor `A2_ANCHOR_F10_RUN_V001/inputs` against the v009 A2F10 dry run:
  - `fs_controls_00..03` are byte-identical;
  - `fs_manifest` is equal except the PENDING finish shas;
  - the seed is equal except `c2_changed_fields` (lineage);
  - v008 gives the same result.

### Admission at the registered geometry (all 11 stages)

**AR**: every stage's 4.04 config is accepted by both gal_c2v004 and gal_c2v005, with equal returned values and equal config bytes after T.

### At D ∈ {3.98107, 4.1115, 4.07}, v009's inputs equal v003c's

- **G1**: the 4 per-call files (profile, binding-V003 copy, monotone source, column-mean binding) are byte-identical to v003c's after <RD>.
- **G2**: the route-A delta against 4.04 is the same as in v003c: only the prep patch `C`.
- **G3**: v003c's `PROFILE`/`PROFILE_SHA`/`SOURCE`/`SOURCE_SHA` equal v009's stage globals, reuse patch and config fields. The fields travel only to their consumers: reference/body/offset/rotations/column mean, and never columns or feedback.
- **G4**: `outer_edge = sqrt(last v003c edge)`, and the query rows equal v003c's binding rows.
- **G5**: all 6 consumers' own gal_c2v005 admission accepts the per-call config, and the returned values equal the per-call values. The controls are accepted. The only remaining refusal class is PRODUCED_BY_THIS_CALL (pending route A).
- **G6**: v009 at D equals v008 at D after T, except the probe outcome (v008 is refused by all 6 stages). This is the before/after.
- **G7**: v009 at D against v009 at 4.04 shows only the named geometry deltas.
- **G8**: a missing distance equals 4.04, and parallel route A plus D gives only the `C` delta.
- **DEC3**: the deciding-(iii) spec copy (`2029f26a`) plans identically.
- **Unit tests:**
  - **AG**: each consumer accepts under gal_c2v005 and refuses under gal_c2v004 with exactly the geometry fields. Each of the 5 fields was also tested alone.
  - **C**: at all 3 D:
    - `radial_truncation` returns the last edge in all 5 truncation stages (profile edges for reference/body/offset; monotone edges for the rotations);
    - the body full-form guard holds;
    - the D4 domain edge `math.sqrt == np.sqrt`;
    - column-mean `check_binding` passes.

### Refusals kept

- **AN**: a DDO154 PER_CALL on a non-geometry field (physical inclination, n_phi, n_columns, eta_order, Gauss order) is refused with the gal_c2v004 message after T. NGC3198 per-call geometry is refused.
- **AL**: either lock alone refuses (schema without the declaration; stage constant emptied), and a schema that lists an extra field does not admit it.
- **G9**: inclination 64, NGC 14 Mpc, and an admitted 4.04 route A at 4.1115 (`ROUTE_A_GEOMETRY_MISMATCH`) are still refused.

### Run mode

- **R**: at 4.1115, 3.98107, and 4.1115 with RA8, v009 passes the geometry gate and reaches route A (captured, with the `C` patch). v008 is BLOCKED `GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING` with 0 stages.
- **K**: run-mode capture at 4.04, v008 against v009, after T: first requests and inputs are equal for A2F10, the N8 spec and 4ac5527a. The run-mode offset config that v009 wrote for 4ac5527a is accepted by the gal_c2v005 offset stage.

## UNTESTED, with the deciding test

1. **v009 run mode on real stages at 4.04** (bitwise to the saved chain). Deciding test (i).
2. **v009 run mode at D ≠ 4.04 past route A.** This covers the stages executing with per-call configs, and v009 per-call outputs equal to v003c's. Deciding test (iii).
3. **Code fact, not run: admitted upstream outputs that gal_c2v004 produced are no longer admissible under v009.** The cause is that `producer_pin` whitelists only {gal_c2v005 successor, reviewed base}. Example: a v008 deciding-(ii) run cannot be admitted into a v009 call. Saved CODEX1 (base) outputs stay admissible (S1).

## Deciding tests for root (commands in `deciding/`; nothing launched)

Every run sets the environment `OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS_NUM_THREADS=1`.

### (i) DDO ADMIT_PREFIX, bitwise at 4.04, under v009

Launch record: `deciding/LAUNCH_DECIDING_I_C2V009.json` (`902dd494`).

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py \
  --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py \
  --driver-sha256 237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb \
  --spec /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json \
  --outdir "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001" \
  --receipt "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001.receipt.json" \
  --wall-cap-s 14400 --rss-cap-bytes 3221225472 --output-cap-bytes 8589934592 --poll-s 2.0
```

**PASS requires all of:**
- finish COMPLETED;
- `deciding_test.verdict` PASS_BITWISE_EQUAL;
- `route_a_outcome` CONVERGED at 4;
- custody `attempt_link` 98816902… / 01792161909921426000-19994-831a3fbc;
- `source_profile_sha256` f5becd45…;
- no `geometry` key.

**A23 note (classified DECLARED).** A23 says that F-A must be fixed "before any further admit.route_a use", and spec 4ac5527a admits route A. F-A only triggers on an admitted *no-fixed-point* attempt whose checkpoint has no IDENTITY.json. The V002 pair here is CONVERGED, its checkpoint has IDENTITY.json, and the attempt link verifies; this is TESTED in the v009 dry-run identity. Under the A23 text, though, deciding (i) still needs root's reading, or a v010 = v009 + the F-A fix. v009 does not touch F-A or V8c-F1: it is pins only. Test (iii) computes route A serially, so neither item applies to it.

### (iii) One real call at D = 4.1115 under v009, against v003c, same spec

Launch record: `deciding/LAUNCH_DECIDING_III_DISTANCE_C2V009_VS_C2V003C.json` (`902106aa`). The spec is `deciding/CALL_A2F10_D4p11150_DECIDING_GAL_C2V005.json` `2029f26a…`, a byte copy of the v008 test spec: A2F10 a93c95b9 plus distance 4.1115.

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
MON=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py
SPEC=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/deciding/CALL_A2F10_D4p11150_DECIDING_GAL_C2V005.json
RUNS="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
$PY -I -B $MON --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py \
  --driver-sha256 237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb --spec $SPEC \
  --outdir "$RUNS/DDO154_A2F10_D4p11150_C2V009_DECIDING_DISTANCE_RUN_V001" --receipt "$RUNS/DDO154_A2F10_D4p11150_C2V009_DECIDING_DISTANCE_RUN_V001.receipt.json" \
  --wall-cap-s 14400 --rss-cap-bytes 8589934592 --output-cap-bytes 8589934592 --poll-s 2.0
$PY -I -B $MON --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/absorb_c2_0473/driver_f/galaxy_m0_forward_c2v003c.py \
  --driver-sha256 ed326130e89654a377615e46a077764cf3ad39e0bf07bc9d0606225bc69fbdf2 --spec $SPEC \
  --outdir "$RUNS/DDO154_A2F10_D4p11150_C2V003C_DECIDING_DISTANCE_RUN_V001" --receipt "$RUNS/DDO154_A2F10_D4p11150_C2V003C_DECIDING_DISTANCE_RUN_V001.receipt.json" \
  --wall-cap-s 14400 --rss-cap-bytes 8589934592 --output-cap-bytes 8589934592 --poll-s 2.0
$PY -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/deciding/compare_distance_v009_v003c.py \
  --reference "$RUNS/DDO154_A2F10_D4p11150_C2V003C_DECIDING_DISTANCE_RUN_V001" --new "$RUNS/DDO154_A2F10_D4p11150_C2V009_DECIDING_DISTANCE_RUN_V001" \
  --spec-sha256 2029f26a20e0659eacd97a5c8524ea0949df6e80d8bd8705abc8a45f3005c643 \
  --out "$RUNS/DDO154_A2F10_D4p11150_C2V009_DECIDING_DISTANCE_RUN_V001.COMPARE_DISTANCE_V009_V003C.json"
```

**The comparator** is `compare_distance_v009_v003c.py` (`3f585532`). Its verdict PASS_BITWISE_EQUAL_PER_CALL_OUTPUTS needs all of these checks:

| Check | What must hold |
|---|---|
| SPEC | same spec sha, D ≠ 4.04, the driver shas |
| GEOMETRY_INPUTS | the 4 per-call files are byte-equal after <OUT> |
| STATUS | COMPLETED and valid |
| SPEEDS | the 12 speeds, the rows, `final_pass`, every pass |
| STAGES | the stage names are equal, in order |
| ARRAYS | every npz/npy array is equal in dtype, shape and bytes |
| NUMERIC_JSON | every numeric leaf is equal, except timing/process keys |

These lineage differences are not compared: digests, the seed annotation (c2v003 vs c2v006), outdir prefixes, and attempt tokens.

The comparator's own tests are 9/9 fixtures:
- PASS on lineage-only differences;
- FAIL on a 1-ulp change to a speed, an array or a JSON number, on a changed geometry byte, on a missing stage, on a wrong spec sha, and on D = 4.04;
- the real-layout self-test of the anchor against itself gives SELFTEST_ONLY_EQUAL.

**How to read the outcome:**
- PASS: D-varied DDO154 calls run in the successor binding with the v003c per-call outputs. The D Jacobian column can then be computed under v009.
- GEOMETRY_INPUTS or SPEC fails: a driver port defect.
- Only ARRAYS, NUMERIC_JSON or SPEEDS fail while (i) PASSes: stage lineage (base stages plus module globals vs the successors with the stages2 module successors) differs at D. The first differing stage is named in the report.
- Any stage refuses in run mode: TESTED-NEGATIVE for this successor.

## Rule notes

- Superseded outputs of my own try runs stay in place under `tests/runs/try1` and in the first `runs/final/COMPARE_DRY.json`. Nothing was deleted or moved.
- Scratch debug helpers live in the session scratchpad. Their guard logs are in `tests/runs/try1/logs` and `tests/runs/final/logs/debug_dec3.json`.
