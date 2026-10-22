# phase1_c2v002: the A133 Phase-1 tool, A137 successor of v001

**Labels.** TESTED = run here on synthetic fixtures with the result shown. FORMAL = follows from the cited code or text. UNTESTED = not run; the deciding test is named.

**Text of record.**
- Ruling A137 in `CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` (L5 and N-B).
- Claude3 0191 (review of v001; L5 and the N-B flip probe P8).
- `CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` (`cd92ef91`), sections 1.2, 1.5 and 4.

**Scope.** v002 makes exactly two changes to `phase1_c2v001.py` (`34eaef36`): L5 and N-B. v001, its tests, README, HASHES, NO_FIX_NEEDED and `test_runs/` are untouched. T00 re-hashes v001 and its tests in every run. No production run was made, and no campaign, cache, run tree, C5H, `UVT_*` path or NGC3198 target was opened. The tests are synthetic only.

## Files (all new, created exclusively)

| File | Role |
|---|---|
| `phase1_c2v002.py` | The tool. Same commands, arguments, exit codes, schemas and output file names as v001. |
| `test_phase1_c2v002.py` | 103 checks: the 71 v001 checks ported, plus 32 new ones. 43 are MUST_FAIL. |
| `DIFF_PHASE1_C2V001_TO_V002.diff` | Unified diff of the tool (+133 / −53 lines). |
| `DIFF_TEST_PHASE1_C2V001_TO_V002.diff` | Unified diff of the tests. |
| `test_runs_v002/RUN_20261019T132307Z_43825/`, `test_runs_v002/RUN_20261019T132349Z_46255/` | The two record runs, each 103/103. Each holds `RESULTS.json` and `SHADOW_REGRESSION_V001_V002.json`. |
| `HASHES_V002.txt` | sha256 of each object, computed from its bytes. |

**Pins.** Unchanged from v001: orchestrator `c75a889f`, engine `6ec8b2d0`, freeze v003g `48a1e48a`, KMAX `dbddc02c`.

**Usage.** As in `README_PHASE1_C2V001.md`, with `phase1_c2v002.py` in place of v001. No argument was added or removed.

## Change L5: B_P1 on any first non-prefix family

**Definition (A137).** B_P1 is the number of forward calls before the first call whose orchestrator Probe family is not in `PREFIX_FAMILIES = (seed, jacobian, repair, gd_pre)`. Every v001 `march0` dependency now reads "the first non-prefix-family wave".

| Site | v001 | v002 |
|---|---|---|
| Prefix detection, `Campaign.prefix` | first WAVE_PLAN whose families hold `['march0']` | first WAVE_PLAN with a family outside PREFIX_FAMILIES |
| Replay stop, `replay`/`b_p1` | `march0` is the boundary. Any other non-prefix family refuses (`FAMILY_x_BEFORE_MARCH0`). | The first non-prefix family is the boundary. Its family and engine stage are carried on the stop. |
| NOT_READY rule, `snapshot` | B_P1 reached and no march0 plan gives NOT_READY | B_P1 reached and no first-non-prefix-family plan gives NOT_READY. If that wave does not plan the replay's boundary family, the result is PREFIX_MISMATCH. |
| Stage check, `check_snapshot_run` | `stage_reached == 'march'` | `stage_reached` must equal the boundary call's own engine stage: `'march'` for march0, `'global_design'` in the corner case |
| Recorded wave, snapshot doc | `march0_wave` | `march0_wave` when the family is march0, exactly as v001. Otherwise `march0_wave: null` plus `first_non_prefix_wave {wave, plan_sha256, families}`, `boundary_call {log_index, family, stage_reached}` and `b_p1_rule`. |
| PREFIX_MISMATCH, `handoff` | march0 wave and plan sha | the recorded first non-prefix-family wave and plan sha |
| AT-0a | B_P1, replay, march0 plan, next requested = march0 plan | the same, against the recorded wave, plus the recomputed boundary family must equal the recorded one |
| `load_snapshot` | stage `'march'` | the stage of the recorded boundary. A doc that carries both forms, or neither, refuses (`SNAPSHOT`). |

**When the first non-prefix family is march0:** behaviour and outputs match v001 byte for byte, refusal texts included (R01 below).

**Behaviour change on a v001 fixture (TESTED, R01).** In T10.NOID the boundary is m_id = 0 at the `design` wave. v001 had no march0 wave, so it listed every planned wave (1–4) in `prefix_waves`. v002 lists waves 1–3 and records wave 4 as `first_non_prefix_wave`. The status (NO_IDENTIFIED_DIRECTION), the exit code (20) and every other field are unchanged.

**Refusal texts changed** (paths with no march0 boundary only):
- `no committed WAVE_PLAN with a family outside (...)`
- `replay ended X with no call outside (...)`
- stop code `FIRST_NON_PREFIX_<family>` (it replaces the v001 refusal `FAMILY_<family>_BEFORE_MARCH0`)

## Change N-B: AT-1 e_q, the member-displacement bound

- **The formula.** For each member m and row q: e_q(m) = Σ_k 2 ε_k |Δ_m,k| / h_k.
  - Δ_m = u_m − u_A, in engine u.
  - h_k = |du_k| of F_k, from the fdplan.
  - ε_k = the row's L1 `eps_q`.
- **What it replaces.** v001 used max(noise at the band's lo and hi optima) + Σ 2ε|(V_Nᵀn_m)_k|/h_k. v002 removes it. The band (L1) still prints its §1.5 `fd_noise` at the two optima, unchanged.
- **Reporting.**
  - `reported.e_q_per_member_row` lists `{log_index, id, e_q}` for every tested (member, row).
  - `e_q_reading` states the reading.
  - A row with no ε reports `FD_NOISE_NOT_BOUNDED`. It gets e_q = 0 and the failing entry is flagged, as in v001.

**[D] The choice of ε_k.** The task says to use "the per-axis FD noise the tool already estimates". The only per-row ε the tool holds at at1 is L1 `eps_q`, which is the largest certificate ε over u_A and the three F points. So ε_k = `eps_q` for every k.
- This is ≥ max(ε(u_A), ε(F_k)), the noise that actually enters K_q,k, so the bound holds.
- It is looser than the tightest per-axis value by at most the ratio of those maxima.
- The tighter per-axis value would need at1 to read the Phase-1 values file. That would be a new input, so it was not built.
- This is for Claude3 to confirm in review.

## Tests (TESTED; 2 identical record runs: 103/103, MUST_FAIL 43/43, audit denials 0, 48 shadow calls each)

### Part 1: the v001 checks, ported
All 71 v001 checks are present with the same ids and in the same order (checked against v001's record `RESULTS.json`). Only two port changes were needed:
- `tool()` now shadow-runs v001 (see part 2);
- `Camp` accepts an optional toy `speeds` argument for the corner fixture.

### Part 2: regression against v001 (R01, 8 checks)
**Method.** Every CLI call in part 1 also runs v001, on the same inputs and into the same out-dir path. v001's directory is first moved aside to `<out>.V001_SHADOW`. The two runs must then match:
- the exit codes are equal;
- stdout is equal;
- every output file is byte-identical after v001's value is substituted for exactly these fields:

| Fields | Why they differ |
|---|---|
| `module`, `tool_sha256` | tool identity |
| the engine record's `created_utc`, and `record_sha256`, `record_file_sha256` and the registry `line_sha256` that hash it | they differ between any two v001 runs too |
| at1 only: `outcome`, `failing`, `e_q_reading`, `reported.e_q_per_member_row` | N-B |

**Results.** All 48 calls pass:

| Command | Calls |
|---|---|
| snapshot | 16 (15 identical, plus NOID, which differs as stated above) |
| fdplan | 6 |
| handoff | 9 |
| band | 5 |
| at0a | 5 |
| at0b | 4 |
| at1 | 3 |

**N-B effect on the v001 at1 fixtures.** C1 is COVERED in both versions. Q1 is SUPERSEDED in both, with the same 301 failing (member, row) pairs; only the excess values move. The defect fixture reads AGREEMENT_DEFECT in both.

### Part 3: new checks (T27–T29, 23 checks)

**T27: L5 MUST_PASS, the corner seed u = (1, 0, 0.5).** This is Claude3 0191 verifier P7. The toy depends on a0 + a1, so m_id = 1.
- The waves are seed, jacobian, jacobian, design. Both round-0 sides are `COMPUTATIONAL_BOX_FACE_NO_EVALUATION`. The campaign never plans march0, and later plans design, lp and axis.
- **v001 refuses** with `REPLAY_STOPPED: FAMILY_design_BEFORE_MARCH0 at log index 5` (0191 reproduced).
- **v002's snapshot succeeds:**
  - B_P1 = 5. That equals an independent oracle that classifies every direct-engine call with the orchestrator's own `Probe.context`.
  - `boundary_call` = {5, `['design']`, `global_design`}, and the recorded wave is 4.
  - u_A is the seed, which is the oracle's primary anchor.
  - The record is BUDGET_EXHAUSTED and verifies, and its log equals the oracle's first 5 entries.
  - The work dir is unchanged.
- **Before the design plan is written:** NOT_READY.
- **Also passing on the corner:**
  - fdplan: S0, and F with face sides minus/plus/plus taken from the record;
  - at0a: PASS, with next requested = the committed design plan;
  - handoff, band and at0b;
  - at1 (SUPERSEDED, not a defect);
  - after the campaign completes, the snapshot is unchanged and at0a still passes.

**T28: L5 MUST_FAIL, a non-prefix family before the recorded boundary.** Each case refuses:

| Case | Result |
|---|---|
| Replay to a claimed B_P1 + 1 | `B_P1_WRONG ... ('FIRST_NON_PREFIX_design', 5)` |
| B_P1 − 1 | `B_P1_WRONG` |
| A self-consistent forged snapshot at B_P1 + 1 (a re-registered direct run whose log index 5 is the design call), through **handoff** | `B_P1_WRONG` |
| The same forged snapshot, through **at0a** | AGREEMENT_DEFECT (`B_P1 B_P1 5 != snapshot 6`) |
| The prefix plan of wave 3 edited to plan `['lp', 1]` (a non-prefix family below the recorded wave 4), through **at0a** | AGREEMENT_DEFECT |
| The same edit, through **handoff** | `PREFIX_MISMATCH (now wave 3, recorded 4)` |
| The same edit, through **snapshot** | refused, and nothing is written |
| The corner record presented in the march0 form | `B_P1_WRONG` (stage) |
| A doc carrying both forms | `SNAPSHOT` |

**T29: N-B.**
- **Both flip directions** (0191 verifier P8, ε = 1 km/s, row 0). A far member at t = 3r fails under v001 (e = 13.78) and passes under v002 (e_q = 25.47). A near member at t = 1e-4 passes under v001 and fails under v002 (e_q = 0.0048). The reported e_q equals the independent sum.
- **No ε:** a row reports `FD_NOISE_NOT_BOUNDED` per (member, row), and its failing entry is flagged.
- **CLI at1 on Q1:** 516 (member, row) e_q values, each equal to an independent Σ 2ε|Δ|/h.

## FORMAL notes for the reviewer (Claude3)

1. **Where B_P1 can fall under V002 parameters.** The first non-prefix family is either march0 (stage `march`) or, when every round-0 side closes at a face, the post-march global design (family `design`, stage `global_design`; engine L2365–2398).
   - The local design is skipped, because its points coincide with u_A when every round-0 width is 0.
   - A pre-march global design anchor is a Halton point, which is interior, so it cannot produce that case.
   - If a first non-prefix call ever fell in stage 8 (lp/axis), the budget-B_P1 run would end COMPLETE and the tool would refuse with B_P1_WRONG. It fails closed.
2. **What is unchanged for forged records.** A self-consistent forged record at B_P1 + 1 passes `load_snapshot`, so `fdplan` and `band` read the record only. handoff and at0a refuse it, which is TESTED in T28. This is the same as v001 for march0, and is a forged-input NOTE under A115.
3. **How the stage is read.** The boundary's engine stage is read from the engine's own `_explore_impl` frame (`out['stage_reached']`), through the same frame walk the orchestrator's Probe uses. If it is absent, the stage check refuses.
4. **What is not in scope.** No other v001 NOTE (N-A, N-C, L1, L2, notes 1–12) is addressed here, per the scope "Changes, and ONLY these".

## UNTESTED
- The real campaign: run `snapshot` on DDO154_CALIBRATION_ORCH_V005 once its first non-prefix-family plan exists.
- Real NGC ε certificates feeding `eps_q`: the first `band` and `at1` on Phase-1 values after the seal.
