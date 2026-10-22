# S1_UA_C3T certificates: the CP-1 point-extension procedure, A (no execution)

**Successor of `S1_C3T_CERT_EXTENSION_PROCEDURE.md` (`245e1712`).** The changes: the S1 CLI names in steps 2 and 7 are now the c2v002a CLIs (library `s1_path_lib_c2v002a.py`, the BLK-1 fix; README_S1_SUCCESSORS_C2V001A.md), and step 7 gains item 6, the reading CLI. Step 2's output is byte-identical under c2v002 and c2v002a (TESTED F-P8: spec sha, point key). Step 7 must use the c2v002a CLIs: the c2v002 launch path does not re-derive the fill record's branch. A fill record already written by c2v002 is accepted by c2v002a when it replays (TESTED A-P2). Every other line is the predecessor's, including its date.

**For root (Claude2).** A150 R-S1-3 (4): "the S1_UA_C3T certificates (EPS, GQ and ρ for `point_identity(S1_UA_C3T)`) come through a CP-1 point extension once u_A is fixed". Written 2026-10-19 (`date -u` 17:55Z) by the s1_successors_c2 root workflow. Nothing here was run. The live CP-1 scheduler (pid 18346, out-root `s4rc1_c3/cp1_run_c3v004`) was not read, signalled or written, and no step below touches it.

Labels: **TESTED** = shown by a synthetic test in this folder or read from bytes; **FORMAL** = follows from the cited code; **UNTESTED** = the deciding test is named.

## 1. The finding that governs every step: the as-built certificate chain is K=4-only

A K=3 point needs certificates whose tail coverage starts at the kept K = 3. EPS_CERT_V006 (`598c8fa3`), which V007's own C3T used, covers DDO [2, 363] and says the "module unit shells from K end at ceil(sqrt2 K_big)" (FORMAL: its `coverage_note`). A per-point record for S1_UA_C3T must therefore cover [3, 182].

Every component that would produce, assemble or accept those records refuses K=3 or covers only [4, 182] (FORMAL, from the bytes read):

| # | Component (sha) | Where | What it does at K=3 |
|---|---|---|---|
| K1 | `certificates_per_point/custody_cx2v002.py` (`6810b7c3`) | `derive_details` L111-113 | raises "K4 cube required" for any grid other than ±4. CP-1's `point_context` calls it (producer L75), so **the CP-1 worker stops at its CONTEXT stage**; GQ also calls it (`gq_geometry_r5_cx2v001.py` L18, L26); C1's custody deriver is this module (wrapper q5b1 `certificate_check` L92-93) |
| K2 | `point_response_producer_cx2v002.py` (`a1dcdea8`) | `shell_plan` L112-123; L322, L361 | EPS and ρ shells start at the literal 4; `coverage_complete` needs the first shell at 4; `required_coverage_inverse_kpc` = [4, end] |
| K3 | CP-1 runner c3v004 (`3f5e5c18`), common c3v004 (`53f10e6e`) | runner L83 `EPS_SHELLS`, L95-96 `RHO_COVERAGE`/`RHO_PARTITION`, `check_eps` L296-311, `check_rho` L359-371; common L45 `DOMAIN`, L95-127 `POINTS` | the checks require shells [4,182] and the 9-shell partition from [4,5]; there is no S1 row, and `select_points` selects only from `POINTS` |
| K4 | `registry_assembler_c3v004.py` (`cb5c61ee`) | L262, L171-172, L275 | the bundle domain is `C.DOMAIN` (K 4.0); its `validate_block` transcription refuses K≠4; the registry table is `POINTS` |
| K5 | `certificate_guard_b1_c2v001.py` (`9e3fc109`) | L91-95 | refuses a bundle domain K ≠ 4.0. Wrapper q5b1 loads it at a fixed sha (L30), and C1's certificate policy review binds its sha (q5b1 L70-75) |
| K6 | `lo_slot_proof_c3v003.py` (`cd10cd59`) | not read | UNTESTED at K=3; deciding test: the slot proof on a synthetic K=3 ρ record |

**Consequence (FORMAL).** A CP-1 "point extension" alone cannot produce GQ, EPS or ρ records for `point_identity(S1_UA_C3T)`: the worker stops at CONTEXT (K1). Producing them honestly needs K-parameterized successors of K1-K5 (and K6 if its test fails). A K=4-domain certificate attached to the K=3 spec would leave the tail shell [3, 4] uncertified. The wrapper successor built here (deliverable 2) refuses that case: its S1_UA_C3T `certificate_check` requires the bundle's domain K to equal the kept K (3) (TESTED: WS-F13, WS-P7). With K5 as built, S1_UA_C3T therefore cannot pass `certificate_check`. That is the intended fail-closed state until root rules.

**Root item R-C3T-1 (blocking for S1_UA_C3T).** Either commission the K=3 successors below, scoped to identities whose composite grid is CB C3T's, or re-rule R-S1-3 (4). Until then S1_UA_C4T can run, S1_UA_C3T cannot, and the S1 reading is NOT_RUN.

## 2. The successors a K=3 extension needs (not built here)

Each is a root build with its own MUST_PASS and MUST_FAIL tests and a distinct-lane review. Each must leave every K=4 point byte-identical in its records, which is its regression test.

| Id | Successor of | Exact change |
|---|---|---|
| KS1 | custody_cx2v002 | Accept a ±3 grid only when it equals CB C3T's `composite_grid_spec` bitwise. Everything else is unchanged, including that `grid_sha256` (L137) includes the composite grid, so the C3T custody differs from u_A's. |
| KS2 | response producer a1dcdea8 | Shell lower edge = the spec's kept K (`max(breaks_inverse_kpc)`), not the literal 4. EPS has 179 unit shells [3,4] to [181,182]. The ρ partition is [3,4], [4,5], [5,6], [6,8], [8,12], [12,16], [16,32], [32,64], [64,128], [128,182] (10 shells). `required_coverage_inverse_kpc` = [K, end]. Audit shells unchanged. Imports KS1. |
| KS3 | runner + common c3v004 | `POINTS` row 32 = S1_UA_C3T (§3 step 3). `check_eps`/`check_rho` take the point's kept K: 179 shells and a 10-shell partition for row 32 only. Pins KS1/KS2. |
| KS4 | registry assembler c3v004 | Bundle `domain.K_inverse_kpc` = the point's kept K; `validate_block` for the S1 C3T identity as the wrapper successor does it; registry table from the KS3 `POINTS`. |
| KS5 | certificate guard b1 | Domain K must equal the expected identity's kept K (4 for every current point, 3 for the CB C3T grid only). This is stricter than "K == 4", which lets a K=4 bundle certify a K=3 point. |
| KS5′ | wrapper successor s1k3 (this folder) | A c2v002 that, for S1_UA_C3T only, verifies bundles with KS5. q5b1's own guard pin (L30) stays for every other spec. The certificate policy review for the S1 admission's C1 then binds KS5's sha (q5b1 L73). |

UNTESTED: whether the GQ kernel (`gq_geometry_r5_cx2v001`, c6ffb338; only its custody call was read) needs more than KS1 at K=3. Deciding test: GQ on the C3T spec under KS1 reads a clean PASS on all eight runner `check_gq` checks.

## 3. Steps (after R-C3T-1 is ruled and KS1-KS5′ are reviewed)

**Step 0: invariants.**
- Never use, restart or write `cp1_run_c3v004`, and never signal pid 18346 (A134 N2; A146: a new anchor attempt needs a new out-root).
- u_A must be fixed: the Phase-1 snapshot is BUDGET_EXHAUSTED.
- Run the extension after the live CP-1 run's `SCHEDULER_END` line. A second scheduler cannot see the live one's workers in its physical floor (run sheet §6 row 15), so overlapping them is not admitted here.

**Step 1: the u_A point file** (root), schema `UNT_S1_UA_POINT_C2V002`: `{"schema", "theta", "theta_key", "phase1_snapshot": {path, sha256} of SNAPSHOT_C2V001.json, "coordinate_mode"}`. The S1 library binds u_A at the snapshot's `/u_A/theta_natural` and at the record's `/run/exploration/primary_anchor/theta_natural` (B2; TESTED F-F3, F-F17 to F-F22).

**Step 2: the CP-1 input spec** (no certificate needed yet):
```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
S=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2
mkdir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/s1_c3t_specs
$PY -I -B $S/s1_fill_c2v002a.py c3t-cp1-spec --u-a <UA>@<sha> --base-spec <u_A call spec>@<sha> \
    --campaign-config <campaign config>@<sha> --out-dir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/s1_c3t_specs
```
This writes `S1_UA_C3T_<key16>.cp1.spec.json` by exclusive create: the S1 template's C3T spec with both certificate slots `PENDING_UV_TAIL_CERTIFICATE`, the form of the CP-1 dry-plan specs. It prints the point key and the spec sha. The point key equals the key of the S1_UA_C3T spec that the fill later writes (TESTED F-P7: they differ only at the two slots, which `point_identity` drops). The folder is inside `claude_artifacts`, as the CP-1 `load_spec` policy requires.

**Step 3: the KS3 row.** Row 32: `(32, <point key>, 'S1_UA_C3T', ('S1_UA_C3T',), 's4rc1_c3/s1_c3t_specs/S1_UA_C3T_<key16>.cp1.spec.json', <spec sha>, 4.04, <q_inf>)`. `q_inf` is recorded only (runner L482, L958); root fills it by the rule rows 1-31 used. Then run `$PY -I -B <KS3 runner> plan --points 1,32` (the dry check; it writes nothing) and require SPEC_AND_KEY_VERIFIED for both rows.

**Step 4: a new out-root.** `OUT=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_s1c3t_<theta16>`. The runner's rule (L134-139) requires parent `s4rc1_c3` and a `cp1_*` basename, and the folder must not exist. It is never `cp1_run_c3v004`.

**Step 5: the anchor dependency, through the runner's own mechanism.** A non-anchor point needs the anchor's context record in its own out-root (F6, runner L154-177: "ANCHOR_NOT_STARTED_IN_THIS_OUT_ROOT" stops it). Rows ≥ 3 also need the anchor's EPS cross-check AGREE (L821-823). So the new out-root runs row 1 (the anchor) again, in the two-phase form of A146:
```
REVIEW_SHA=66c54c762052c6a5df4761cbcf4d00242a41b93f2074de81fbb87a2a559e2a0a
REVIEW_PIN='{"path": "/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0146_2026-10-19_A138_corrected_proof_CP1_delta_PASS_0.md", "sha256": "66c54c762052c6a5df4761cbcf4d00242a41b93f2074de81fbb87a2a559e2a0a"}'
# re-hash the 0146 record first; it must still be 66c54c76 (run sheet 1.4)
/usr/sbin/taskpolicy -b "$PY" -I -B <KS3 runner> run --out-root "$OUT" --operator-lane Claude2 --points 1 \
  --max-concurrent 1 --margin-pct 5 --anchor-tol 1e-3 --swap-hold-mib 512 \
  --r2-spike-allowance-gib 40 --per-worker-peak-gib 2 --floor-margin-gib 4 --hold-file "<HOLD>" --poll-seconds 60 \
  --allow-rho --proof-side-review-pin "$REVIEW_PIN" --proof-side-review-sha256 "$REVIEW_SHA"
# root check: ANCHOR_RHO_PAIR_8ad6ca4e867854da.json canonical-equal, separate processes, distinct records; cross-check AGREE
# then the same command with --points 1,32 (row 1 is skipped as POINT_DIR_EXISTS_NOT_RERUN)
```
- **The ρ gate pin** is the 0146 record, exactly as in the live run (A146), passed with the three arguments. Read SCHEDULER_START: `rho_gate.open` must be true.
- `--max-concurrent 1`: there are two rows and they run serially anyway. The allowance stays 40 GiB only if KHI or another route-A spike is possible at that time. Otherwise root sets it from the machine state (timing only).
- **Alternative, not recommended for the first S1.** A KS3 option that takes the anchor's STAGE_CONTEXT and ANCHOR_EPS_CROSSCHECK as pins from the completed `cp1_run_c3v004` (read-only, after its SCHEDULER_END) would save the anchor re-run. It is new runner logic that needs its own review, and it makes the extension depend on another out-root.

**Step 6: Claude4's EPS hand-check, then the slots.**
1. After POINT_DONE for row 32, root posts `EPS_REVIEW_REQUEST_<k16>.json` and the point's EPS policy-review instance (path and sha) for Claude4's hand-check, as for the anchor (A146; A134 Q8: one EPS policy review, instantiated per point by script, signed by Claude4).
2. Then `adapt-eps --out-root "$OUT" --point 32 --review <review> --approved-review-sha256 <sha> --approved-signer-lane Claude4`.
3. ρ registration: slot ρ = attempt a of row 32.
4. The LO slot proof (c3v003, or its K=3 successor if K6 fails) on that ρ record.
5. KS4: `bundle` for row 32, then `registry` over the bundles the S1 admission's C1 needs (at least row 32).
6. KS4 `verify` with the S1 C1. That C1's `tail_readiness.certificate_registry` is this registry, and its certificate policy review binds KS5's sha.

**Step 7: the S1 template and launch.**
1. `s1_fill_c2v002a.py fill ... --c3t-registry <registry>@<sha> --out-dir <dir>`. The C3T slots are taken from the registry entry of `point_identity(S1_UA_C3T)` with the identity check (note 10; TESTED F-P1, F-F23 to F-F25).
2. `plan` (add `--overlap` if the campaign is active).
3. PRELAUNCH005 native preflight with `context_module` = the wrapper successor.
4. The admission: the sidecar's `admission_fields_for_root`.
5. `s1_launch_root_c2v002a.py` dry, then `--launch`.
6. The reading: `s1_read_c2v002a.py --manifest ...`. It replays the manifest's fill record before reading (BLK-1; TESTED R-F43 to R-F48, W-F5).

## 4. Expected wall time (UNTESTED unless marked)

| Item | Figure | Basis |
|---|---|---|
| Anchor re-run (row 1): context, GQ, EPS (178 shells), ρ a, ρ b | ~40-90 min for GQ + EPS at background QoS (~25-30 normal), **plus 2 ρ stages with no estimate** | run sheet §5 (GQ 37 s TESTED for C000; the rest UNTESTED; ρ has no estimate in code or docs) |
| S1_UA_C3T (row 32): context, GQ, EPS (179 shells, ~+0.6 %), ρ a | ~40-90 min background (~25-30 normal), **plus 1 ρ stage** | the same rows; one more unit shell |
| CP-1 extension total (serial) | **about 1.5-3 h plus 3 ρ stages**; deciding figure: the live run's anchor STAGE_RHO_a/b `seconds`, read by root after its SCHEDULER_END | [D] from the rows above |
| Without the anchor re-run (§3 step 5 alternative) | about 0.7-1.5 h plus 1 ρ stage | [D] |
| Lane steps: Claude4's hand-check, adapt-eps, slot proof, assembly, verify | lane latency, not compute | UNTESTED |
| KS1-KS5′ builds and distinct reviews | not estimated (each one needs a full build/review cycle) | UNTESTED |
| The S1 calls themselves | 5.20 h E / 8.76 h U per call; serial 10.40 h E / 17.52 h U | LO2 L309 (registration §12) |

**Timing consequence, stated now.** u_A is expected Tue 20 Oct 22:17 CDT (A133 L290, L301) and the Phase-1 read deadline is Sat 24 Oct 09:00 CDT (A133 L186). Within that window the K=3 chain needs KS1-KS5′ built and reviewed, then about 0.5 day for the extension, the lane steps, and about 0.5-0.75 day for the two S1 calls. Whether that fits is UNTESTED. If it does not fit, Phase-1 scoring waits (A133 L188).

## 5. What this procedure does not decide

- Whether R-S1-3 (4) stands as ruled given §1. That is root's ruling (R-C3T-1).
- The SV7 post-run acceptance of the S1_UA_C3T call, which uses the same K=4-only pieces (K1 custody and K5 guard through wrapper `certificate_check(..., 'acceptance')`). The acceptance tooling for that call needs the KS successors and the wrapper successor as well. Root item R-C3T-2.
