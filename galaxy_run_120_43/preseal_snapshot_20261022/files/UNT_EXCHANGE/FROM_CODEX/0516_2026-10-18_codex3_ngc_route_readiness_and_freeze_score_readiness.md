# 0516 — Codex3: two parallel lanes. (A) NGC3198 route A/B readiness under v010 with the tail; (B) freeze and score pipeline readiness. Source, build and dry-run only; no launches.

From: **Claude2**, coordinator and single scientific launch owner since 2026-10-16 (CURRENT_INSTRUCTIONS.md). UTC ~12:35Z. The principal assigned Codex3 to take work.

**Scope.** This dispatch alone is your assignment. Do not act on STANDING_ORDER or older queues.
- Post start, finished and blocker packets in `FROM_CODEX3/`, continuing its numbering.
- Run lanes A and B in parallel, in separate output directories.
- Other lanes are active:
  - Codex1 builds the NGC N-test evaluators (`ngc_ntest_eval_cx/`, dispatch 0510);
  - Codex2 does DDO154 calibration readiness and a review of v010 (0511).
  - Do not duplicate them or write into their folders.

## Context

The galaxy run (120/43) seals V007 today. V007 adopts the tail-corrected lapse: a K = 4 kept cube plus the analytic Q∞·T_N tail. The steps after it are:
1. DDO154 recalibration;
2. NGC3198 N-tests, then NGC route A/B at admitted points;
3. freezing the 43 NGC3198 predictions with bands;
4. opening the targets and scoring in LADDER format.

**Root decisions:**
- frozen `Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V002_ADDENDUM.md`, `…V003_ADDENDUM.md` and `…V004_ADDENDUM.md`;
- open `…V005_ADDENDUM.md`.
- **Read:** A12 (finite reach), A14 C3 / A12.5 (outer-gas truncation rule), A15 (expectations, which the pipeline must never read), A16 (NGC freeze inputs), A27 (NGC tier 2), A41 (UT-1), A46–A54.

## Lane A — NGC3198 route A/B readiness (output `claude_artifacts/ngc_route_tail_readiness_cx3/`)

**Inputs:**
- driver v010 r4 `claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py` (b9ae92d5); its K16 NGC handling (v002-lineage worker; lineage-swap record);
- RO1 c2v002 NGC workers/binding and the NGC reader hunk, in `claude_artifacts/ro1_readout_c2/`;
- NGC tail config and roster from the R1 prereg's `ngc3198_N_tests` block (`tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json`);
- NGC route work so far: `claude_artifacts/ngc_route_impl_c2/`, `ngc_route_a_freeboundary_c2/`, `ngc_kgrid_fidelity_c2/` (phase23 T120L), `ngc_freeze_inputs_c3/` (slots V002 4c5951cb), `absorb_c2_0473/ngc_route_a`;
- the NGC seed (pins V002 17c26616).

**Tasks:**
1. **NGC tail-ON call specs for v010 r4.**
   - T120L grid, cube K = 2 kept, continuum_v001 tail, cylinder K_big 16 (the R1 NGC value, which N3 tests), RO1 armed, NGC quadrature per R1, certificate slots.
   - Apply the A14 C3 / A12.5 truncation rule for unconfined outer columns: truncate the route-A gas roster at the first unconfined radius, record the dropped HI mass fraction, and mark query rows beyond it INVALID.
   - Dry-run with 0 blockers apart from pending certificates and V007 adoption.
2. **NGC route-B result assembly under v010.** The R1 label L3 marks this UNTESTED. Specify the deciding test: the first NGC route-B result under v010 against a v009 parent. Build its comparator, and test it on synthetic or saved NGC stage outputs.
3. **The admitted-point launch plan for NGC** once calibration has an admitted region: caps, memory (design K15), wall-time projections from the saved NGC runs, and how many points can run concurrently on 18 cores.
4. A typed blocker list, each item with its owner and its deciding step.

## Lane B — freeze and score readiness (output `claude_artifacts/freeze_score_readiness_cx3/`)

**Inputs:**
- freeze v003d and engine v003b: `claude_artifacts/calibration_engine_freeze_v003b_v003d/` (freeze 74e0d406), with `calibration_freeze_c2_v003b/` (guard_check v003c);
- NGC freeze inputs `ngc_freeze_inputs_c3/`;
- A16 freeze inputs;
- LADDER format: grep the program for the LADDER spec (`LADDER.md` in the program root).

**Tasks:**
1. Run the freeze and scorer end to end on **synthetic** NGC route-B results in v010's result schema, including the `ro1` block, `uv_tail` records and nodes/continuum tail fields. Check:
   - the 43-prediction manifest;
   - the bands and alternatives;
   - the hash-lock;
   - refusal on tamper, on a missing row, and on an INVALID truncated row;
   - the LADDER-format score output against a **synthetic** target file you create.
2. **Never open the real NGC3198 target velocities.** Check the freeze refuses any target field. Report anything in v003d that does not accept v010 output, and propose the successor fix (build it under a new name, with tests).
3. A typed blocker list.

## Rules (binding)

- **No launches of any kind:** no forward, route-A or route-B runs. Dry runs, synthetic tests and replays on saved states are allowed. Claude2 is the only launcher.
- **Never open NGC3198 observed or target velocities.** Lane B uses synthetic targets only.
- Do not read `/Volumes/External1/…/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001` (blinded) or any `runs_ext/UVT_*` run.
- No deletion, moves, renames or overwrites. Successors under new names; never edit a reviewed file.
- Never touch `~/.codex` session logs. No network. No git writes.
- Python: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (numpy only).
- **Resources:** single-thread BLAS, at most 2 processes in total for the account, and under 8 GB per process. If the sandbox refuses `nice`, run at default priority (0514 waiver).
- Keep outputs small; disk is tight.
- Hashes from bytes. Labels TESTED / UNTESTED. Never fabricate.
- Some old folders under /Users/bgm/Research are symlinks to External1; read through them normally.
