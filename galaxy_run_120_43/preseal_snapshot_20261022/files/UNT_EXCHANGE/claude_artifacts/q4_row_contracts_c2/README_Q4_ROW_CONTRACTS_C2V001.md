# Q4 canonical row-contract records (C2V001)

Requested by Codex1 in 0141 (`87b4263f`) and 0152. Ruling: A134 Q4 (rulings `56774ba7` L90-111).

This folder holds the three records that `lo_core_r5_cx2v001` (`12d36305`) `produce_current_lo` L225-231 matches each Q4 row-reference policy approval against. An approval passes only if:
- `review.verdict == 'APPROVED'`, and
- `review.row_contract_sha256 == ctx['details']['custody']['row_contract_sha256']`.

`ctx` comes from response producer `a1dcdea8` `point_context` and then `custody_cx2v002` (`6810b7c3`) `derive_details`. That function builds the row record at L119-128 and hashes it at L139. There is one record per distinct D, because `distance_Mpc` is inside the record (L125).

## The three values

| Label | D (Mpc, JSON float) | row_contract_sha256 = file sha256 | Used by |
|---|---|---|---|
| DLO | 3.9810717055349722 | `fefbfe66b5de66f9927c15f6ba36335046e90006e9c7ef7dbeaa3f727ac2578e` | SENS_LO, 9 tail-ON calls (DIII LOW is tail-OFF and needs no LO acceptance) |
| D404 | 4.04 | `f9bb13a92b43ca49cf5012b10d4d90b75f52dabbe80484920e60a173aed9ebea` | HEADLINE11 (TAIL_REANCHOR included), POST_S1 (2 calls), every campaign point |
| DHI | 4.111497211045223 | `a14024eaa9876b43ac52af5d3d1f4f8cb6ee988251fecf0e6e4238465cf45b14` | SENS_HI, 9 tail-ON calls (DIII HIGH is tail-OFF) |

Tail-ON direct calls: 11 + 9 + 9 + 2 = 31.

## File format

Each `ROW_CONTRACT_<label>_C2V001.json` is exactly `custody.canonical(record)`: sorted keys, compact separators, no trailing newline. To verify, any of these equals the row_contract_sha256:
- `sha256(file bytes)`;
- `custody_cx2v002.digest(json.load(file))`;
- the `digest` of adapter c3v003 or of row producer v003.

## Where D comes from (step 1, TESTED from bytes)

- **Direct calls.** Params C2V003A (`4adc296b`) supersedes A139's C2V003 (`b7fdaf10`). The template pins and case orders are identical in both. The `calls[].distance_Mpc` values are taken from the pinned step-4 templates (HEADLINE `2e9a3cb2`, SENS_HI `fdb96200`, SENS_LO `ea97f536`, DIII `f14514fe`).
- **Final-spec producer v004** (`fcbf1c3e`, `step4_launch_readiness_c4/handoff_v004/tools/`; A139 gives only its sha):
  - SENS D comes from `float(engine_coordinates[distance_Mpc].lower/upper)` (L551-565);
  - HEADLINE requires `d == 4.04` (L576-577).
- **Coordinate spec** `50e7288e`: the box is [3.9810717055349722, 4.111497211045223] with trial 4.04. This equals the region file `13c16a63` `distance_summary.reported68_low/high`.
- **Campaign.** Addendum `9962b2aa` uses mode `DDO154_DISTANCE_FIXED_AT_REGISTERED`, with `fixed_engine_coordinates.distance_Mpc = 4.04`.
- **POST_S1 (DERIVED).** C2V003A has no template for it. The S1 pair is at the campaign point u_A, so it is at D = 4.04 by the campaign rule.

## How the records were built (step 2)

`build_row_contracts_c2v001.py` ran under the codex runtime with `python3 -I -B`. Every module was imported by path and checked by sha. An audit hook refused any open or listdir of a hard-rule path or of a `__pycache__` file.

- **A. Rebuild.** The record is rebuilt with the pinned custody's own functions, following L118-128 statement for statement:
  - `point_geometry` (driver r5 `b5cc62af` `derive_geometry` at float(D) and 66.0);
  - `cc.pin('prereg_v005')` (certs_common `c75aaa5a`);
  - `read_pin`;
  - `digest`.
- **B. Byte-equality proof.** The real `custody.derive_details` ran on a spec built the way producer v004 builds one: A2F10 template `a93c95b9`, plus run-config `numerics.block`, plus `physical.distance_Mpc = D`. Its `row_contract` equals A's record byte for byte, and its `custody.row_contract_sha256` equals A's digest.
- **C. Cross-checks.** All of these held:
  - custody, adapter c3v003 (`211a3220`), row producer v003 (`67fddd24`) and hashlib all give the same digest;
  - row producer v003 `row_reference()` accepts each record on a synthetic call (its L116 check);
  - the lo_core L69-72 `row_values` checks pass (emulated: lo_core is hashed, never imported);
  - τ = 0.25 σ, matching the region file's `quoted_random_sigma_km_s`;
  - the rows are unchanged when the non-D physical coordinates move to the box upper corner;
  - the geometry guards all hold;
  - the D404 rows equal the registered column-mean binding.
- **External corroboration (D404).** A historical custody record, `certificates_per_point/CUSTODY_KB064_C000_CX2V001.json` (`92b54db5`, produced by custody_cx2v001 `3b29dff5` at D = 4.04), carries the same row_contract bytes and the same hash, `f9bb13a9`.

The source of each field is in `ROW_CONTRACTS_INDEX_C2V001.json` under `field_sources`. In short:
- `rows` = driver `query_rows(D)`, where radius_m = radius_reference_kpc × D / 4.04 × KPC_M, over the calibration-input response rows;
- `tau_km_s` comes from prereg V005 `dbddc02c`;
- `distance_Mpc` is the spec value, taken verbatim;
- the two policy strings and `schema` are custody literals;
- `prereg` is the certs_common pin.

## What the reviews must carry (for Codex1)

- Each review is a JSON object with `verdict: "APPROVED"` and `row_contract_sha256` set to one value above.
- Each row reference names its review as `policy_review` {path, sha256}.
- The review's sha must be in `trusted_row_policy_review_sha256` (adapter L681-683).
- The record's literal strings `speed_reference_policy: PENDING_REVIEWED_LO_COVERAGE_OBJECT` and `uncertainty_carrier_policy: PREREG_V005_TAU; CALIBRATION_CARRIER_PENDING_ROOT` are custody L126-127 bytes inside the hash. They cannot change without a new custody pin.
- The A134 Q4(a) policy is carried in two places:
  - the row reference's `speed_reference_policy` (`A134_Q4A_OWN_CALL_MAX_ABS_OVER_EVERY_RECORDED_READOUT`);
  - the review text.

## Deviations and disclosures

1. **`derive_details` was not run exactly as published.** Its `uvt_static_pins` (custody L129; driver L341-345 and L1215-1223) hashes `CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json`, which the hard rules forbid. In proof B a proxy intercepted that one attribute. It feeds only `modules_sha256`, never the row record. The `modules_sha256`, `custody_sha256` and `point_sha256` of those calls are not production values and are not reported.
2. **The specs are not the launched final specs.** No final-spec bytes were opened. Each spec was built as producer v004 builds it. The record depends only on `physical.distance_Mpc` and pinned inputs (invariance TESTED).
3. **Files opened beyond the explicitly named sources.**
   - By the pinned functions:
     - the derive_geometry inputs: CODEX1 `GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` (a multi-galaxy profile; nothing from it was printed), `GALAXY_STELLAR_3D_REFERENCE_SOURCE_V001.json`, `DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json` and `DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json` (a pinned CODEX1 source record, not one of the forbidden run trees);
     - from helpers/recovered_packet_audit: the calibration input, the photometric profile and the monotone reducer;
     - `GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json` (sha only);
     - the A2 coefficient npz `2e3a36d8` (CLAUDE2/CRITICAL_PATH_EVALUATION).
   - By me:
     - non-recursive listings of `step4_launch_readiness_c4/`, its `handoff_v004/` and `handoff_v004/tools/`, used to find producer `fcbf1c3e`;
     - non-recursive listings of `step4_launch_packet_cx1/impl/`, `step4_prelaunch_cx1/v005/` and `certificates_per_point/`;
     - the step-4 templates, coordinate spec, addendum, A2F10 template and REGISTERED_ANCHOR (each cited by explicit path in a source);
     - several certificate JSONs in `certificates_per_point/`, grepped for `row_contract_sha256`.
   - The full list from the record run is in `BUILD_RUN_C2V001.json` `opened_research_paths`.
4. **Bytecode cache during the dry runs.** Two dry runs (no writes) loaded the driver and certs_common through existing `__pycache__` .pyc files, via custody's importlib loader. The record run refused all pyc reads and compiled the hashed sources. Its values are identical to the dry runs'.
5. **How the files were created.** The folder was created with `mkdir` without `-p`.
   - The script and this README are new files.
   - The records, INDEX and BUILD_RUN were created with `open(..., 'xb')`.
   - BUILD_STDOUT was copied with `cp -n`.
   - HASHES were created with `'xb'`.
   - The script was edited only before the record run.

## UNTESTED, with deciding tests

- **That the launched final specs carry exactly these D floats.** Decided by custody `derive_details` on each launched spec: the first real TAIL_REANCHOR acceptance (D404) and the first SENS acceptances (DLO, DHI). Any other float changes the hash, and lo_core then blocks with `ROW_REFERENCE_POLICY_REVIEW_SCOPE_MISMATCH` (fail-closed).
- **That POST_S1 S1_UA_C3T (K=3) uses the D404 contract.** Decided when the KS1 custody successor (V006 A160) is built and run on the S1 spec. The successor must build the same row record.
