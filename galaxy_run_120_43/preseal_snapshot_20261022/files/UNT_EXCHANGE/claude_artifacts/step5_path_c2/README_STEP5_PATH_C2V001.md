# step5_path_c2: the step-5 NGC launch path for the first Phase-1 runs (S0) at T0

**Who and what.** This is a root (Claude2) workflow build, built 2026-10-19 11:55–12:10Z. A133 assigns this build to root workflows, with Claude3 as reviewer. Nothing was launched, and every output sets `launch_authorized: false`. Root rules and launches.

**Labels.**
- **TESTED:** run here, with the result shown.
- **FORMAL:** read from the cited bytes.
- **UNTESTED:** not run; the deciding test is named.
- **RECOMMENDATION:** a proposal for a root ruling.

**Text of record.**
- `A133_TWO_PHASE_PROTOCOL_V001.md` (`cd92ef91`), §§1.4, 3, 5 and 6.
- The V006 addendum, entries A132, A133, A134 and A115.
- `ROOT_ITEMS_STEP45_V002.md` (`417de6fe`): RI45-02, RI45-08, RI45-12 and RI45-20.

## 1. Bottom line

- **Interface A is ready for S0, TESTED dry.** The four S0 points (the seed and its three Jacobian plus points, fixed now) go through this chain:
  1. `phase1_c2v001 fdplan --s0-only`
  2. `phase1_point_handoffs_c2v001`
  3. `fill_step5_c2v001`
  4. a cx3r008 dry plan: 0 executed stages, no binding blocker; with real certificate pins, no blocker at all.

  Each fill emits the serial call of record and its column_workers-8 identity twin. The two specs differ only in `numerics.route_a.column_workers`; their normalized specs differ only at that leaf (TESTED, D04).
- **Physics inputs are byte-identical to the registered cx3r008 spec `05760326`** (in SPEC_REGISTRY_CX3R008_V002 `2c3f421d`). The serial normalized spec differs from it only in the label, the four theta-mapped physical fields and the two certificate pins (TESTED, D05). This holds for the driver `577f8c94`, K_big 32, M_s 96, the T120L grid, the A2 grid `2e3a36d8`, and the NGC geometry of 13.8 Mpc and 72° (TESTED, D06).
- **Tests.** 83/83 in each of two record runs: 40 MUST_PASS and 43 MUST_FAIL. Each run made 10 dry plans with 0 executed stages, made 0 launches, and opened no protected path (the fence denied nothing, Z01).
- **Root still has to rule on 11 items before the first NGC launch** (§7). The critical ones:
  - the S0 certificate pins (RI45-06);
  - the V007 adoption pin (RI45-05);
  - the caps;
  - the slot for the identity pair (memory);
  - the r3a SEAL CANDIDATE hard gate (A133 §2).

## 2. What changed and why (successors change only what the item requires; diffs in `diffs/`)

| Object (new) | Supersedes | Change | Item |
|---|---|---|---|
| `POLICY_C2V001.json` | POLICY_CX3V001 `4f0d7d03` | `drivers` → cx3r008 only (driver `577f8c94`, registry `2c3f421d`, acceptance = review `7ff20c1d`); r006/r007 gone | RI45-08 (a) |
| | | + `coordinate_mode` (DDO154_DISTANCE_FIXED_AT_REGISTERED, addendum CX2V006 `9962b2aa`, fixed distance 4.04, free = s, γ/Eref, ℓ_F) and `admitted_campaign_coordinate_pairs` (CX2V006 `50e7288e`/`9962b2aa`; V002 `89e7d33e`/V005A `ff438ed1`; engine coordinates and engine parameters byte-equal, TESTED by the builder) | RI45-02 (a) |
| | | `templates` → interface A only: the call of record and the cw8 twin; + `identity_pair` | RI45-12 (a); A132; A133 §1.4 |
| | | + `phase1_source_lists` and `phase1_root_admission_required` | A133 §1.4 |
| `templates/TEMPLATE_A_K32_A2_HEADLINE_C2V001.json` | TEMPLATE_A_K32_A2_HEADLINE_CX3V001 `f130e6df` | `call_spec.numerics.route_a = {column_workers: 1}` (the driver default, so normalized numerics are unchanged; TESTED D05) + schema, id, role, supersedes | RI45-12 (a) |
| `templates/TEMPLATE_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json` | same | `route_a = {column_workers: 8}`, role IDENTITY_TWIN, adoption status IDENTITY_TWIN_ONLY_NEVER_A_MEMBER_RESULT | A132; A133 §1.4 |
| `tools/fill_step5_c2v001.py` | fill_step5_cx3v003 `2348974f` | (1) the 3-u fixed-distance mode, exactly the orchestrator's `_apply_coordinate_mode` (only the role of `distance_Mpc` changes); u has 3 entries and θ.distance_Mpc = 4.04 | RI45-02 (a) |
| | | (2) driver cx3r008 only; a non-synthetic handoff's `driver_acceptance_pin` must be review `7ff20c1d` | RI45-08 (a) |
| | | (3) a second handoff schema, `UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001`, for S0 points (`PHASE1_S0_C2V001`) and FD points F (`PHASE1_FDPLAN_C2V001`); point selected by theta key, recomputed here; the S0 campaign config must name an admitted coordinate pair, and a real handoff needs `synthetic_test: false` | A133 §1.4 |
| | | (4) the identity-pair guard: nothing is written unless the two specs differ only in the leaf | A132 |
| | | (5) label `step5 <template> theta_key=<key>`: no handoff sha or mode in the spec (both are in the receipt), so the same theta and certificates give the same spec bytes in Phase 1 and Phase 2 (TESTED D08) | A133 §3 re-binding |
| | | Otherwise unchanged: pins from bytes, exact fields, finite numbers, the certificate sentinel, exclusive output | |
| `tools/phase1_point_handoffs_c2v001.py` | new | Writes one 10-field Phase-1 handoff per S0/F point from root fields, with **certificates per point**; decides nothing | A133 §1.4; RI45-09 |
| `tools/compare_identity_pair_c2v001.py` and `IDENTITY_PAIR_COMPARISON_SPEC_C2V001.md` | new (I4 producer idea, `707395ba`) | Byte-equality of iteration-k START/columns/COMPLETED payloads, blobs, checkpoint identity and sidecar; booleans only | A132; A133 §1.4 |
| `carriers/POLICY_CARRIERS_C2V001.json` | carriers POLICY_CX3V001 `311ceedd` | driver, registry and adoption review → cx3r008 | RI45-08 (a) |
| `tools/extract_carriers_c2v001.py` | extract_carriers_cx3v005 `50c7db5f` | only `POLICY_SHA` (+ 4 docstring lines; TESTED P06) | RI45-08 (a) |
| `tools/dry_one_c2v001.py` | cx3r008 harness dry_one_cx3v001 `68e58bb9` | stricter read fence: also denies CLAUDE2 runs/runs_ext, UNT_INTERNAL_RUNS, `uvt_` components and the C5H marker | RI45-13 dry plans |
| `STEP5_REGISTRY_C2V001.json` | STEP5_REGISTRY_CX3V002 `85b1e66a` | cx3r008 only; no fallback (default `null`); pins every object above and both test RESULTS | RI45-08 (a) |
| `CAPS_FIRST_NGC_POINT_C2V001.json` | new | root_monitor caps for the call of record and the twin (§5) | RI45-12; A133 §1.4 |

**Not built (A115: none is reachable by honest producers, or none is needed for S0).**
- **RI45-20 (shared fence/IO).** Every tool keeps its reviewed guards, and its findings are NOTE class under A115.
- **The step-4 writer v010 binding.** In Phase 1, `phase1_c2v001 handoff` is the writer.
- **The extractor fixes of RI45-19/RI45-22.** They are BEFORE_FIRST_RESULT.
- **STAGE0 templates.** A133 §3 sets them to NOT_EVALUATED in Phase 1.
- **Interface B.**

## 3. Interface with phase1_c2v001 (`34eaef36`, not duplicated)

| phase1 output | consumer here | TESTED |
|---|---|---|
| `fdplan --s0-only` → `S0_C2V001.json` (4 points: u, u_hex, θ, θ_hex, key, role) | `phase1_point_handoffs` → filler, Phase-1 schema | F01: S0 recomputed independently from CX2V006 equals phase1's S0 bit for bit. F02: all 4 phase1 S0 points fill |
| `fdplan` → `FDPLAN_C2V001.json` (F list) | same, list `F` | F04: phase1's FD_SEED and FD_JAC F points fill (3 + 3) |
| `handoff` → `TARGET_FREE_EXPORT_C2V001.json` + 10-field handoffs | filler, export schema (3-u) | F03: phase1's export (7 admitted points) fills every member. X01: phase1's handoff as emitted (synthetic policy, `r006_fallback`) is refused |

**For the Phase-1 members (not S0), phase1's root fields must be:**
- `policy_pin` = POLICY_C2V001;
- `driver_branch` = `cx3r008`;
- `driver_acceptance_pin` = review `7ff20c1d`;
- `coordinate_pin` = the CX2V006 or the V002 coordinate spec.

phase1's `handoff` applies one `certificate_pins` object to every member, so per-point certificates need one `handoff` run per member (root item 10).

## 4. How root launches S0 and the identity pair (the commands)

Use `PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, with `-I -B` everywhere. In the commands, D is the cx3r008 driver path and A is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2`.

0. **Gates (root).**
   - The V006 entries of §7, batched (FB-3).
   - The r3a SEAL CANDIDATE is published (A133 §2 row 1, hard gate).
   - RI45-24 (PAR8-SF1) is pinned.
   - RI45-05: the V007 verdict pin.
   - The S0 certificate records exist (RI45-06).
1. **S0 thetas.** `$PY -I -B phase1_c2v001.py fdplan --s0-only --config <C1> --config-sha256 <H> --out-dir <NEW>`, then log the sha of `S0_C2V001.json`. C1 must name an admitted coordinate pair (root item 7).

   The S0 theta keys are fixed now and identical under either pair:

   | point | theta key |
   |---|---|
   | seed | `968c915bece706ea…` |
   | J0 | `3d7785669b549d6f…` |
   | J1 | `ab7bf95317b37652…` |
   | J2 | `4b9b4ec88eb2d94c…` |

2. **Root fields.** Write `PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001` with:
   - `mode` `PHASE1_POINT`;
   - `root_admission` `A133_PHASE1_POINT_THETA_FIXED_TARGET_FREE`;
   - `policy_pin` POLICY_C2V001 (`0c781a17…`);
   - `v007_adoption_pin` (RI45-05);
   - `driver_branch` `cx3r008`;
   - `driver_acceptance_pin` {REVIEW_NGC_V011_CX3R008_C4V001.md, `7ff20c1d…`};
   - `certificate_pins_by_point` {theta key: {eps_certificate, lo_certificate}} for all 4 keys.
3. **Handoffs.** `$PY -I -B A/tools/phase1_point_handoffs_c2v001.py --source S0 --source-sha256 H --root-fields RF --root-fields-sha256 H --out-dir <NEW>` writes 4 handoffs and a receipt.
4. **RI45-09.** Root publishes each handoff sha in V006.
5. **Fill.** `$PY -I -B A/tools/fill_step5_c2v001.py --handoff <H> --expected-sha256 <published> --output-dir <NEW>` writes `CALL_A_K32_A2_HEADLINE_C2V001.json` and `CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json`. The twin is launched for the seed only.
6. **RI45-13, per spec to launch.**
   - Run `$PY -I -B A/tools/dry_one_c2v001.py D 577f8c94… SPEC SPEC_SHA <NEW report dir> <NEW log>`. It must show 0 executed stages, `binding_blockers []`, `source_build_blockers []` and future dependencies only `PENDING_ROUTE_A_OUTPUTS`.
   - Read the blocker lists, not the readiness label: with zero blockers the driver's label still reads PENDING_CERTIFICATES, because of `all([])` (NOTE).
   - Register the spec sha in V006, and verify the driver sha from bytes.
7. **The first NGC launch is the identity pair at the seed** (A132; A133 §1.4). Admit both under the memory gate (§5), then run:
   ```
   $PY -I -B root_monitor_c2v001.py --driver D --driver-sha256 577f8c94… --spec <CALL_A_K32_A2_HEADLINE_C2V001.json> \
       --outdir <runs_ext/NGC_P1_S0_SEED_SERIAL_RUN_C2V001> --receipt <same>.receipt.json \
       --wall-cap-s 610324 --rss-cap-bytes 34359738368 --output-cap-bytes 68719476736
   $PY -I -B root_monitor_c2v001.py --driver D --driver-sha256 577f8c94… --spec <CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json> \
       --outdir <runs_ext/NGC_P1_S0_SEED_CW8_TWIN_RUN_C2V001> --receipt <same>.receipt.json \
       --wall-cap-s 22752 --rss-cap-bytes 92341796864 --output-cap-bytes 34359738368
   ```
   Run directory names use `NGC_`, with no `ngc3198` or `uvt_` component.
8. **The other three S0 calls.** Serial only, with the call-of-record caps, each launched when the memory gate admits it.
9. **Identity verdict.** When the twin has stopped (its planned WALL_CAP) and the serial has finished the compared iterations, run `compare_identity_pair_c2v001.py … --iterations 1` (or `2`; root item 4). Read only the verdict (§ spec).
   - If the verdict is `SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON`, the identity is TESTED. A cw8 call of record would need a one-leaf policy successor. Even so, Claude4 0174 shows that concurrent serial points give more throughput than N8.
   - If not, every call stays serial.
10. **After every result.** Check that `driver_sha256` = `577f8c94` (A77.1 N8). Reads stay validity-only until r3a and the M-12 classifier are sealed (A133 §2).

## 5. Caps (`CAPS_FIRST_NGC_POINT_C2V001.json`; RECOMMENDATION, value-relevant under A133 §3(f))

| | wall_cap_s | rss_cap_bytes | output_cap_bytes | basis |
|---|---|---|---|---|
| call of record (serial) | **610,324** (2 × U 305,162 s) | **34,359,738,368** (32 GiB) | **68,719,476,736** (64 GiB) | A133 §1.4 sets wall ≥ 2 × the forecast. Claude4 0174/0179 and Claude3 0181 support each value. RSS meets A61 at 1.5 × 20.11 GB; the N4 condition holds (TESTED: seed `88ef386d` has hi_panels_per_side 8 and source_azimuth_count 32). Output: 2.3–2.6 GB per iteration |
| identity twin (cw8) | **22,752** (2 × U 3.16 h to the end of iteration 1) | **92,341,796,864** (86 GiB ≥ 1.5 × 61.3 GB) | **34,359,738,368** (32 GiB) | A planned stop after iterations 0–1 (Claude4 0174 option 1); its values are never read |

**0174's 381,500 s wall cap (1.25 × U)** is below the A133 2× rule, so it is not used.

**Memory gate (A133 §1.4; arithmetic 103 − 27 − peaks):**
- A serial point peaks at 20.11 GB (U), not 14 GB.
- **A single serial S0 call** is admitted at a measured footprint ≤ 55.9 GB (U).
- **The pair** needs ≤ 26.0 GB (E) or 8.7 GB (U). During iterations 0–1 the serial spikes at ≤ 5.91 GB, and the twin at 45.2/61.3 GB.
- In practice the pair fits only after step 2, in a window with no DDO route-A call in flight.
- The watch prints GiB labelled as GB, and its v002 pattern does not count NGC processes. Extend it first (Claude3 0181, items 3–4).

## 6. Tests (`tests/test_step5_path_c2v001.py`; record runs `tests/runs/RUN_20261019T115738Z_85732`, `RUN_20261019T115753Z_87136`)

| group | MUST_PASS | MUST_FAIL | covers |
|---|---|---|---|
| P: successors against their predecessors | 8 | 0 | only the declared keys or lines change; every policy pin verifies from bytes; `POLICY_SHA` matches the policy bytes |
| F/H: phase1 interface and handoffs | 10 | 2 | §3 above; per-point certificate entries; exclusive outputs |
| X: filler controls | 0 | 22 | see below |
| D: dry plans under cx3r008 | 16 | 0 | 8 synthetic (PENDING) and 2 with real certificate pins (EPS `1d5eef1b`, LO `07745bbf`): 0 executed stages, no binding blockers, and no blockers when the pins are real; planned worker and solver per side; pair leaf-only; physics equals the registered spec; θ mapping; Phase-1 = Phase-2 spec bytes |
| C: identity comparison | 3 | 17 | see the comparison spec |
| K: carriers successor | 2 | 2 | cx3r008 readout accepted; r007 readout `DRIVER_CUSTODY`; old policy refused |
| Z: fence | 1 | 0 | no protected open, write outside the run, delete, link or chmod, and no subprocess except the dry harness |

**The X controls, each refused with its own code:**
- **RI45-02's four controls:**
  - a four-u point;
  - distance 4.0365;
  - an invented fourth entry;
  - a mode/addendum mismatch, plus a non-admitted export coordinate pin.
- **RI45-08:**
  - `r007` and `r006_fallback` branches;
  - the r007 review as the acceptance pin;
  - the superseded policy.
- **Point, mode and output rules:**
  - an unknown or mismatched theta key, or bad θ bits;
  - a synthetic handoff carrying real certificates or V007 pins;
  - a PHASE1_POINT handoff from a synthetic config;
  - the mode fence and the root admission string;
  - a handoff sha mismatch, an output directory that exists, an extra field, and a twin that differs in a second leaf.

**Test input reads.** The tests read phase1's own record-run fixtures, the real step-4 config v006r9 (`721c7230`, coordinate pins only), and the existing NGC anchor certificates (pins only). A V007 stand-in (`V007_ADOPTION_STANDIN_TEST_ONLY.json`) fills the one pin that does not exist yet.

**Never launch the test specs.** The specs under `tests/runs/*/DRYTEST_ONLY_*` are dry-test outputs and are never launched.

## 7. What root must still rule (before the first S0 launch unless noted)

1. **Adopt in V006:** POLICY_C2V001, the two templates, fill_step5_c2v001, STEP5_REGISTRY_C2V001, the Phase-1 handoff schema with its admission string, and the theta-key label rule. Claude3 reviews first (A133 §5); RI45-02 (a) and RI45-08 (a) are then closed for interface A. Also mark LAUNCH_ORDER_CX3V002 step 1 and ROOT_ITEMS_CX3V002 R3 as superseded (A103).
2. **S0 certificate pins (RI45-06).** Which EPS record each S0 point carries: Claude4's per-point S0 EPS (after r3a and the EPS policy review; 0178 C1 requires recomputing the anchor-only shells), and which record fills `uv_tail.lo_certificate`. Under A134, LO acceptance is per-state post-run acceptance for DDO; the NGC LO field still needs a pinned record. With PENDING, the driver blocks run mode. The dry plans used the anchor records only as existing real pins; they are not point-scoped.
3. **The caps in §5,** including that a twin WALL_CAP stop is the planned stop and not a failure under A133 §3(c), since the twin is not a member.
4. **`--iterations` for the identity verdict:** 1 (the iteration-0 minimum) or 2 (adds the first warm-state transfer; recommended).
5. **The identity pair's memory slot (§5),** and extending the watch pattern and units. The pair cannot run while step 2 (R2) runs.
6. **RI45-05:** the V007 adoption pin is the sealed compare's verdict report (the same {path, sha256} as C1's `numerics.verdict_artifact`).
7. **The step-4 config of record (C1) for `fdplan --s0-only`.** Both admitted pairs give the same S0 bits (TESTED F01). A133 §3 names "run config V005A" (V002/V005A), while the tail-era configs (v006r9 `721c7230`, sched s45) name CX2V006. Root states which one C1 is.
8. **RI45-24 (PAR8-SF1)** V006 entry (BLOCKS_START), and RI45-25 (ST8-N2) before the first step-5 result: how a REFUSED (exit 3) step-5 run enters the freeze.
9. **RI45-13 per spec:** a fresh dry plan with the real pins, V006 registration of the spec sha, and a driver sha check.
10. **phase1 `handoff` uses one certificate map for every member.** Rule one run per member, or a phase1 successor, before the members after u_A launch (not needed for S0).
11. **The carriers successor:** adopt it before any carrier is extracted from a step-5 result (BEFORE_FIRST_RESULT). RI45-19 and RI45-22 (point_key binding, the fences) remain open.

## 8. Conduct and limits

**Read paths.**
- **Read as data:** the cited code, policies and templates; phase1's tool and its synthetic test outputs; the step-4 configs; the coordinate files; and the two certificate files (by sha, plus their top-level keys).
- **Read as two fields only:** `hi_panels_per_side` and `source_azimuth_count` from the driver-pinned target-free NGC seed `88ef386d`, for the cap condition (Claude4 0174 N4).
- **Never read or opened:** NGC target velocities, C5H, `UVT_*` directories, `runs`/`runs_ext` trees, or any run value.
- **The driver's own dry planning** reads its pinned target-free inputs, the same set as the cx3r008 registry dry plans (each log lists them under `opened_read`).

**Writes.**
- Everything was written in this folder by exclusive create, through the builder (`build/build_step5_path_c2v001.py`; sources in `build/src/`).
- Development ran in the session scratchpad first.
- **Disclosure.** `IDENTITY_PAIR_COMPARISON_SPEC_C2V001.md` was edited once, two minutes after its creation and before any hash, to correct one overclaiming sentence (an over-strong "never a false EQUAL"). No other file was modified after creation.

**UNTESTED.**
- The first real runs, specifically the scientific runtime and the identity verdict.
- Real per-point certificates.
- The real C1 config.
- The real phase1 snapshot handoffs.

The deciding test for each is the step listed in §4.

**Hashes.** `HASHES.txt` lists the sha256 of every file here, from bytes, except files inside the test run directories (only their `RESULTS.json` are listed).
