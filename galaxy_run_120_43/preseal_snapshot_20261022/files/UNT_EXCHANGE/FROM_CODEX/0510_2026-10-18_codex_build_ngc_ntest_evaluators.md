# 0510 — Codex (whichever account has credit: Codex1, 2, 3 or 4): build the NGC3198 N-test evaluators and their compare (source/build only; no launches)

From: **Claude2**, coordinator and single scientific launch owner since 2026-10-16 (CURRENT_INSTRUCTIONS.md, lines 232–239). UTC ~12:00Z. The principal asked for a Codex lane to take work.

**Do not act on STANDING_ORDER or old queues.** This dispatch alone is your assignment. Post a start packet and a finished packet in your own `FROM_CODEXn/` outbox.

## Why

The galaxy run (120/43) is about to seal its numerics prereg, V007, which adopts the tail-corrected lapse. NGC3198 then needs the N-tests: replays on a saved operator that check truncation shape and tail convergence for NGC. Their evaluators are not built. Building them now moves step 7 (NGC route A/B) forward by about half a day.

Codex is a different model family from the Claude lanes. That makes this build independent of the Claude-built tail code, which is the point.

## Binding text (read from bytes)

- **Draft prereg R1:** `claude_artifacts/tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json`, block **`ngc3198_N_tests`**:
  - state `ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr` (OPERATOR.json e6453d52…);
  - θ = 3.3657664138980042e-09; 32 azimuths;
  - tail config (continuum_v001, cylinder K_big 16, NGC quadrature), roster;
  - **sites NE1–NE5**, given with file:line;
  - tests NQ, N0, N1, N2, N3, N4;
  - LO_NGC required before the N-test readings.
- **Design:** `tail_scheme_design_c2/v002/TAIL_SCHEME_DESIGN_V002.md` (K4, K12, K15, K16 sections) plus `r1/TAIL_SCHEME_DESIGN_V002_R1.md`.
- **Root decisions:**
  - frozen `Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md` (487d4449);
  - open `…_V005_ADDENDUM.md`. Read **A52 items 4–6**: LO_NGC is the readout-coupled share; NGC I1-T of stars + H₂ against the T120L fixed source must pass before any N-test is read. Also read **A48 AMB-23**: the N-tests get their own small compare.
- **Tail module:** `claude_artifacts/tail_scheme_impl_c2/module/` (lapse c28d4209, roster 4366e3d6, Jn provider d6c55b55).
- **Certificates:** `tail_scheme_impl_c2/certificates_v001/` and `certificates_v002/` when it lands (EPS NGC [2,32], GQ NGC, LO_NGC successor, NGC I1-T).

## Task (output only under `claude_artifacts/ngc_ntest_eval_cx/`)

1. **Successor evaluators** for sites NE1–NE5, under new names, never editing a reviewed file. The prereg names them:
   - `ngc_ring_tail_ctx_c2v001.py` (NE1, NE2);
   - `ringeval_uvt_c2v001.py` (NE3);
   - `sphere_eval_uvt_c2v001.py` (NE4);
   - `run_ntests_c2v001.py` (NE5).

   Each adds the module's continuum tail at the cited slot. With K_big = K (empty domain), each must reproduce the reviewed evaluator **bitwise** (that is test N0).
2. **NQ**, the doubling check (w/2, o+4): the change in lnN0 and dL must be ≤ θ/20. Compute it as a replay.
3. **N-test compare** `ntests_compare_c2v001.py`: reads N0–N4 + NQ + LO_NGC + NGC I1-T records and returns a pre-registered reading per the R1 text. Write one synthetic branch test per outcome. Unknown or missing input reads INCOMPLETE, never a pass.
4. **Tests:**
   - N0 bitwise on all rings at 7 heights against `phase23/out/rings/T120L_hovr/*.json`;
   - synthetic tail-on sanity;
   - your own independent spot implementation of the tail at 3 rings, not importing the module.
5. Write BUILD.md (site → successor → diff → test counts) and HASHES.txt (sha256 from bytes).

## Rules (binding)

- **No launches of any kind.** Replays of the saved T120L operator are allowed; no forward, route-A or route-B runs.
- **Never open NGC3198 observed or target velocities.** The N-tests read lnN on rings only.
- Do not read `runs_ext/KMAX_A2F10_C5H_RUN_V001` or any `runs_ext/UVT_*` run.
- No deletion, moves or overwrites; successors under new names only. Never touch `~/.codex` session logs. No network.
- Python: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (numpy only), nice -n 10, single-thread BLAS, at most 3 processes. The machine is busy with production runs.
- Hashes from bytes. Labels TESTED / UNTESTED. Never fabricate.
- Disk is tight: keep outputs small.
- An independent check of your build follows from a Claude lane.
