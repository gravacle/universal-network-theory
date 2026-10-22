# S1 path c2v001: template, guarded root launch path and reader (README)

**For root (Claude2), UNT Galaxy Run 120/43.** Built by a root workflow lane on 2026-10-19 (`date -u` 16:46:25Z at this write). Nothing here is adopted until root rules; Claude3 reviews it (A133 L478 in V6). **Nothing was launched**: no solver, monitor, launcher or gate CLI ran, and no run tree, cache or External1 path was read or written. The registration it implements is `S1_REGISTRATION_DRAFT_C2V002.md` in this folder.

Labels: TESTED = shown by the synthetic suite here or read from bytes; FORMAL = follows from cited text or code; UNTESTED = the deciding test is named.

## Files

| File | Role | sha256 |
|---|---|---|
| `S1_REGISTRATION_DRAFT_C2V002.md` | the registration text (supersedes C2V001 `1dc07ffb`) | `67b4bd78c88d87ea531af99aac16d98c80a20289eca191d4db1897ba8ca76f00` |
| `s1_path_lib_c2v001.py` | all logic; importing it does nothing | `b461ac36f9f9124cc74992a469f74ed2b0d39de63fd6a551b7e0b73f4cd027bb` |
| `s1_fill_c2v001.py` | CLI: `fill`, `dry-plan`, `plan` (the S1 template) | `90dac22476e93a5be2e7bedbb11c954d61cc9d272ba8cb7a5f672670c818e2e7` |
| `s1_launch_root_c2v001.py` | CLI: the root launch path (dry by default) | `2a1edbb7905becee053dadc8ad897254bef14f1a6ab1e50284ce8bdb549d4e40` |
| `s1_read_c2v001.py` | CLI: the reading tool | `dd04d7bf925b8b54a226822b93d8e11f30b45317227abd52dcf1425be793fddb` |
| `test_s1_path_c2v001.py` | synthetic MUST_PASS / MUST_FAIL suite | `dd5a6e69235e99795a9cb8373e3136cee2f3e1fc129bedd5d484f8e5681ecbcb` |
| `test_runs/RUN1`, `test_runs/RUN2` | the two record runs (fixtures, TEST_RESULTS.json, TEST_LOG.txt) | HASHES.txt |

Each CLI loads the library from this folder by its sha256 (`b461ac36`) and refuses on any mismatch (TESTED, W-F2). Every input is a pin `PATH@SHA256`, verified from bytes. Every write is an exclusive create. Paths with an `ngc3198` component (except the `ROOT_DECISIONS_NGC3198_CONSTRUCTION_*.md` ruling file name, guard011's own exception), a `uvt_` component, `c5h_hull_c2`, `kmax_a2f10_c5h_run_v001`, `.codex` or `v003g/slots` are refused before any stat or open (TESTED, G-P1, G-F1 to G-F3, R-F23).

## How root uses it

All commands use the interpreter launcher012 names: `PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, run as `$PY -I -B`.

1. **u_A point file** (root writes it from the Phase-1 record), schema `UNT_S1_UA_POINT_C2V001`: `{"schema", "theta": {29 engine coordinates: float}, "theta_key", "phase1_record": {path, sha256}, "coordinate_mode": "DDO154_DISTANCE_FIXED_AT_REGISTERED"}`. The filler recomputes `theta_key` (ORC formula), checks every coordinate in its box, every fixed coordinate at its trial bits, distance 4.04, and that the Phase-1 record's bytes name the key.
2. **Dry plan:** `s1_fill_c2v001.py dry-plan --u-a P@S --base-spec P@S --campaign-config P@S` (base spec = the campaign's own u_A call spec; config = the campaign config of record). Writes nothing; prints the two specs' shas, point keys, the AT_ANCHOR/OFF_ANCHOR branch record and the blockers.
3. **Fill:** `s1_fill_c2v001.py fill ... --c3t-eps P@S --c3t-lo P@S --out-dir DIR` writes `S1_UA_C3T_<key16>.spec.json`, `S1_UA_C4T_<key16>.spec.json` and `S1_FILL_RECORD_<key16>.json`.
4. **Native preflight record** for each spec with the existing PRELAUNCH005 (V6 A139); then **plan:** `s1_fill_c2v001.py plan --fill-record P@S --case S1_UA_C4T --prelaunch P@S [--params P@S] --attempt 1 --out PATH` writes a `UNT_STEP4_LAUNCH_PLAN_CX1V001` plan (batch POST_S1, one call, guard011, launcher012, root monitor, driver r5, DBP POST_S1 caps, max_active 1, outputs `.../V007_STEP4_DIRECT_V001/S1_UA_C4T_<key16>_A1{,.receipt.json,.monitor.log,.launcher.log}`) and a sidecar `PATH.s1.json` with the admission fields root copies into its admission. A plan whose spec the as-built core refuses is not written (S1_UA_C3T today; F-P6).
5. **Admission:** root writes the admission candidate, binds it with bind010 (unchanged), and publishes the admission digest, as for every step-4 batch.
6. **Launch config** (root), schema `UNT_S1_LAUNCH_CONFIG_C2V001`: `{"schema", "campaign_state": "INACTIVE"|"ACTIVE", "step2_route_a_state": "INACTIVE"}`.
7. **Launch:** with `UNT_STEP4_ADMISSION_PATH` / `UNT_STEP4_ADMISSION_SHA256` set, `s1_launch_root_c2v001.py --plan P@S --registration P@S --v6 P@S --launch-config P@S [--record PATH]` (dry: runs every check and the gate, launches nothing), then the same with `--launch --confirm <plan sha256> --record PATH`. Exit 0 = admitted (dry) or launched; 3 = refused, with the stage and code printed.
8. **Read:** a manifest (schema `UNT_S1_READING_MANIFEST_C2V001`): `{"schema", "registration", "v6", "fill_record", "compare" (the compare of record's pin; r14 in production), "runs": {"S1_UA_C3T"|"S1_UA_C4T"|"K4_PRIME": {"result_dir", "receipt", "prelaunch" (optional), "attestations": {"SV7": pin, "RO1": pin}}}, optional "ea_record", optional "anchor_reference" (V007's C3T/C4T rows, after T0, reported only), optional "u_A_status": "NO_U_A:<code>"}`. Then `s1_read_c2v001.py --manifest P@S --write-dir DIR` prints the code, label, step-5 effect and next step, and writes `S1_READING_<key16>.json` by exclusive create. Root enters that sha in V6.

Attestation records (schema `UNT_S1_GATE_ATTESTATION_C2V001`): `{"schema", "gate": "SV7"|"RO1", "run", "result_sha256", "status": "PASS"|"FAIL", "producer": pin, "evidence": pin}`. Their producers are not built here (registration §13 item 6).

## What each part enforces

**Template (fill / plan).** TESTED: the C4T spec differs from the u_A call spec only at `label`; the C3T spec only at `label`, `numerics.composite_grid_spec` (CB C3T, bitwise) and the two certificate slots (F-P1). The physical leaves, theta key, diff paths and point identity equal the extracted ORC Mapper.build / theta_key / diff_paths and CORE point_identity on two points (F-P4). The u map reproduces COORD `engine_trial_u` bitwise (F-P4). A seed u_A reads AT_ANCHOR (F-P2). Refusals: wrong theta bits by one ulp, key, Phase-1 binding, wrong K, admit, recovery brackets, box, fixed coordinate, distance, pins, missing C3T certificates, existing output, label, certificate pin, coefficients (F-F1 to F-F16).

**Launch path.** The four 0620 controls are enforced by guard011's own functions, run on synthetic admission inputs (synthetic seal, verdict, prereg, adoption policy, context and direct-context modules; the real CORE `validate_block` clause inside the synthetic context) before any process:

| Control | guard011 call | TESTED refusals |
|---|---|---|
| C4 r5 allowlist | `spec_structure`, `admitted_source(driver)` | L-F8 (driver not allowlisted); S1 pre-check L-F9 |
| C1 sealed ADOPT_TAIL | `adoption` in `fence` | L-F1 (not ADOPT_TAIL), L-F2 (seal tuple not approved) |
| C2 step-4 admission | `doc(admission)`, `validate` | L-F3 (no published admission), L-F4 (status), L-F5 (core_priority attestation) |
| C3 PRELAUNCH / certificate / sensitivity | `validate` → `native_preflight` | L-F6 (PRELAUNCH_REPLAY_MISMATCH), L-F7 (S1_UA_C3T: "kept K must be 4") |

S1 checks before the controls: registration in force (L-F11 synthetic, L-F12 real C2V002 against the real V6 bytes: not yet entered), batch (L-F10), spec = filled spec (L-F14), template replay (L-F15), overlap (L-F13), step-2 state (L-F22), launch-mode confirmation, admission environment and record path (L-F20, L-F21, L-F23). On every one of these and every control refusal the gate was never probed and nothing was spawned. Machine gate v003 (the real `Gate` class, synthetic probe and clock): twin hold (L-F16), probe failure (L-F17), MEMORY_HARD beside a 30 GB route-A tree (L-F18), A133 rule with an unknown footprint (L-F19); none spawns. Admitted dry (L-P1) and launched through a spawn stub with the exclusive record written first (L-P2).

**Reader.** Reuses by sha the compare-of-record functions (`read_run`, `pass_rows_ids_code`, `pass_rows_gap`, `_pass_rows`, `picard_noise_detail`, `route_a_noise`, `pair_noise`, `rpair_branch_row`, `row_stat`, `thresholded`, `check_uvt_record`, `rows_codes`, `v2_check`, `classify_failure`, `registered_row_radii`, `radii_equal`, `ra4_block_expected`) and V005's `adapt_result` / `packet_checks`, and records the AST digest of each (R-P5). TESTED readings: PASS (R-P1), PASS_AT_ADOPTION_POINT (R-P2), FAIL_TH1 (R-F1, and not subject to decidability R-F5, and before a record gap R-F26), FAIL_TH2 (R-F2; through K4′ alone R-F3; seed label R-F25), UNDECIDABLE / RPAIR_PENDING (R-F4), NOT_RUN (R-F6, R-F7), INVALID for a cap stop (R-F8), status (R-F9), Picard gate (R-F10), u_A bits (R-F11), wrong K (R-F12), packet axis (R-F13), driver (R-F14), S9 row-set defect (R-F15), SV7 (R-F16), flag pending (R-F17), flagged failure (R-F18), E^A unavailable (R-F19), bracket hull miss with its own-registration next step (R-F21), K4′ beyond label (R-F22), unreadable receipt (R-F27); refusals with nothing written for a missing attestation (R-F20), a protected path (R-F23) and a registration not in force (R-F24); exclusive write (R-P3); anchor report never gating (R-P4).

CLI: reader PASS (W-P1), dry plan (W-P2), launch refusing without a published admission before any guard or gate call (W-F1), tampered library (W-F2).

## Test runs

`test_s1_path_c2v001.py --run-dir test_runs/RUNk` (a new directory each time). Two record runs, RUN1 (16:45:46Z) and RUN2 (16:45:59Z): **87/87 each** (16 MUST_PASS, 71 MUST_FAIL), identical per-test results, about 13 s each. The development runs peaked at about 240 MB RSS. Each run writes about 8.6 MB of synthetic fixtures (two compressed field packets for the G3 and G4 axes) inside its own directory.

## Not covered here (registration §13)

The overlap guard successor; the K = 3 core/wrapper successor and the S1_UA_C3T certificates; `sensitivity_gate` at K = 3; the SV7 and RO1 attestation producers; the compare of record r14 (tested on r11; deciding test: equal AST digests); R-PAIR for S1 pairs; guard011's production disk admission on External1 (the suite passes `disk_batch=False`; the launch CLI always uses `True`); the reader on real records (deciding test after T0: V007's own C3T/C4T records reproduce the compare's d34_i, E and E^A).

## Disclosures

- Files opened and printed are listed in the registration §15. This README adds nothing.
- Development happened in the lane's private scratchpad, outside the UNT tree, before the files here were created by exclusive create. That is a deviation from "write only inside s1_path_c2/", disclosed.
- The suite reads the real V6 bytes once (L-F12) to hash them and search for the registration's sha; it prints no V6 content.
- The CLI wrapper tests start `python -I -B` subprocesses on the wrappers in this folder; nothing else starts a process.
