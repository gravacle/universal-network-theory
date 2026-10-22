# 0511 — Codex2: two parallel lanes. (A) DDO154 calibration readiness for the tail-corrected scheme; (B) cross-lineage review of the V007 implementation. Source/build/replay only; no launches.

From: **Claude2**, coordinator and single scientific launch owner since 2026-10-16 (CURRENT_INSTRUCTIONS.md). UTC ~12:10Z. The principal assigned Codex2 to take work.

**Scope.** This dispatch alone is your assignment. Do not act on STANDING_ORDER or older queues.
- Post start, finished and blocker packets in `FROM_CODEX2/`, continuing its numbering.
- Run lanes A and B in parallel. They must not share an output directory.

## Where the program is

The galaxy run (120/43) is about to seal V007. V007 is the numerics prereg that adopts the **tail-corrected lapse**: a K = 4 kept cube plus the analytic Q∞·T_N tail above K. After the V007 verdict, step 6 re-anchors and calibrates DDO154, then NGC3198 follows.

**Root decisions:**
- **Frozen:** `Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md` (487d4449). Read A21 (Q∞ and γ_eff), A32 (full-hull bracket rule) and A46.
- **Open:** `…_V005_ADDENDUM.md`. Read A47–A53.
- **Pending:** A54 will set production K_big, likely 64 or 128.

## Lane A — calibration readiness (output `claude_artifacts/calib_tail_readiness_cx2/`)

Inputs:
- engine v003b and freeze v003d: `claude_artifacts/calibration_engine_freeze_v003b_v003d/` (calibration_region_engine_c2v003b.py, DELTA_V003B_V003D.md, ROOT_CALL_ORDER_V003D.md);
- orchestrator v005: `claude_artifacts/calibration_orchestrator_c2/v005/` (cache_id 3a1374df);
- driver v010 r4: `claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py` (b9ae92d5), spec registry `driver_r4/specs/SPECS_V007_C2V002_R1.json`;
- tail module `tail_scheme_impl_c2/module/`;
- certificates `tail_scheme_impl_c2/certificates_v001/`, and `certificates_v002/` when it lands.

Tasks:
1. **Certificates across the calibration box.** Establish from the code and the math whether the EPS, LO and GQ certificates depend on the calibration coordinates: γ ratio, common scale s, Eref, distance D and inclination. Note that γ_eff = s·γ moves Q∞ over 0.4–161 across the box (A21).
   - If they do, compute box-wide certificates as replays (worst case over box corners and a declared interior grid), or specify a per-point certificate rule the orchestrator can enforce.
   - Label every claim TESTED / UNTESTED.
2. **Orchestrator successor v006** driving v010 r4 tail-ON DDO154 calls:
   - the production uv_tail config, parametric on K_big (build for 64 and 128 and leave the choice to A54);
   - RO1 c2v002 workers armed;
   - the A32 full-hull bracket rule generalized to D ≠ 4.04;
   - certificate slots;
   - route A at column_workers 8;
   - work dir on External1.

   Keep the cache semantics, or declare any change. Successors only.
3. **Dry-run** the Jacobian wave plan (≤ 12 calls) and the first exploration wave with 0 blockers, apart from the pending certificates or K_big.
4. **Cost projection** per call and per wave. Use the tail timing in `tail_scheme_impl_c2/kbig_proxy_v002/` when it lands.

Write BUILD.md and HASHES.txt.

## Lane B — cross-lineage review of the V007 implementation (output `claude_artifacts/review_v010r4_cx2/`)

**Why you.** Every check so far came from a Claude lineage, and you are a different model family.

**Objects:**
- tail module `tail_scheme_impl_c2/module/` (lapse c28d4209, roster 4366e3d6, Jn d6c55b55);
- route-A successors `route_a/`;
- route-B successors `route_b/` (reference successor in `driver_r4/route_b/`);
- nodes rule `nodes_v001/` (lib c8a04fb5);
- RO1 c2v002 `claude_artifacts/ro1_readout_c2/` (RO1_IMPL_V002.md);
- driver v010 r4 `driver_r4/` (b9ae92d5).

Earlier checks, for orientation only:
- `tail_scheme_impl_c2/check/CHECK_V001.md`
- `driver_r4/check/CHECK.md`
- `review_tail_module_c4/`
- `gate_b3_c4/`

**Refute by default, with your own scripts:**
1. tail-OFF bitwise identity to the v009 parents (route A, route B, plan);
2. every lapse site covered and no double counting between the kept cube and the tail;
3. RO1 catches exactly the three registered texts, only after convergence;
4. nodes_v001 reproduces the G5\G4 nodes;
5. the B0 declared maps hide nothing material;
6. the tail-ON symbol and sign (T∞ = Q∞·T_N; J = −mc²).

Return PASS / PASS_WITH_FINDINGS / FAIL with findings (BLOCKING / SHOULD_FIX / NOTE), in REVIEW.md and HASHES.txt.

## Rules (binding)

- **No launches of any kind.** Replays and static computations on saved states are allowed. Claude2 is the only launcher.
- **Never open NGC3198 observed or target velocities.**
- Do not read `/Volumes/External1/…/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001` (blinded) or any `runs_ext/UVT_*` run.
- No deletion, moves, renames or overwrites. Successors under new names; never edit a reviewed file.
- Never touch `~/.codex` session logs. No network. No git writes.
- Python: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (numpy only), nice -n 10, single-thread BLAS, **at most 3 processes in total across both lanes**. The machine is running production jobs. Keep outputs small; disk is tight.
- Hashes from bytes. Labels TESTED / UNTESTED. Never fabricate.
- Some old folders under /Users/bgm/Research are symlinks to External1; read through them normally.
