# Codex3 internal validation of freeze v003g: adapted Claude4 235-case suite

`date -u`: Sun Oct 18 14:54:21 UTC 2026

**TESTED PASS: 238/238 mapped and additional assertions**, on source SHA-256 `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405`. Peak RSS 77,774,848 bytes. No audit denials. Only synthetic targets were created and scored, after each freeze and logged hash. No scientific forward/route launch, real target read, prohibited run read, network or overwrite occurred.

This is Codex3's replay of the previously independent Claude4 harness, with recorded adaptations. It is not a new Claude4 review or cross-lineage approval of v003g. Source files under review were not edited by this lane.

## Scope and mapping

All 235 original check names have explicit mappings and all 235 mapped assertions execute and pass. These comprise 221 unchanged expectations, nine explicitly updated assertions, three comparisons allowing only the new A65 declaration metadata, and two replacements for now-unreachable downstream score checks. The original omitted-alternative scores were **not executed**: their prerequisite writers now refuse, and the replacement assertions verify that no manifest was created. Three new A65 assertions bring the total to 238.

- **F1 TESTED:** dropping ML_3p6_0.4 or ORIGINAL_K, or reversing declared order, refuses. Exact six-record binding includes STAGE0_GRID_OUTER; the primary remains unchanged.
- **F2 TESTED:** reversing the query-manifest file order preserves query-id radius binding and the independent INVALID-set oracle. Q01 binds to 0.25 kpc in this synthetic fixture, not the last row's radius.
- **F3 TESTED:** an Mpc manifest refuses. The public loader gives `Rad_unit must be the registered unit kpc`; the enclosing roster loader reports its generic mismatch refusal.
- **A65 TESTED:** the full six-record declaration survives the freeze, STAGE0_GRID_OUTER remains NOT_EVALUATED_BEFORE_FREEZE/unscored/non-headline in the score, and its sealed roster cannot be evaluated.
- **Previous contracts TESTED:** GL4 invalid-as-miss; gate and per-theta roster custody; gap/outer cuts and exact boundaries; failed-member behavior; D1 non-vacuity and oracle choice; scorer pins/tamper refusal; PROGRAM radius binding using the target-free manifest only.
- **LADDER regression TESTED:** frozen members, evaluated alternative results, headline, envelope and sensitivity match v003e on the same synthetic world. v003e uses the original five alternatives; v003g uses the exact six. Comparing alternative scores excludes only the new unevaluated STAGE0_GRID_OUTER declaration. Its extra declaration is separately asserted, not silently ignored.

The candidate grid is hash-verified as a v003g dependency, even for the unevaluated fallback. Frozen slots metadata and source-bound pins remain unchanged.

## Limits

**UNTESTED here:** an evaluated STAGE0_GRID_OUTER run, its end-to-end row-restricted scoring on actual predictions, any real score, scientific cut validity, and production two-pass replay. The current slots status is NOT_EVALUATED_BEFORE_FREEZE. Exact binding requires a root-approved immutable slots successor before its status can become EVALUATED; this validation does not authorize or simulate that scientific transition.

F4 metre arithmetic and F5 production ordering are preserved contracts, not new scientific certifications. The prior independent searchsorted oracle still matches all tested cut scenarios. Codex3's source/build lane supplies the RUNBOOK; this test lane makes no launch decisions.

## Harness correction preserved

The first adapted run produced 237/238: its sole failure was a harness diagnostic expectation, because it required the string UNIT or KPC in the enclosing roster exception. The module correctly refused Mpc. The harness successor checks the explicit unit diagnostic from the public loader together with the outer refusal. The reviewed module bytes did not change. Both run directories remain immutable. The final run is selected below.

## Selected byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0545_2026-10-18_codex3_freeze_v003g_small_fixes.md`: `4049a3f81b524f5622e0eda6510eeee60c7a6b10fea97ea6c648d0b9698b84a5`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0548_2026-10-18_codex3_register_stage0_grid_outer_alternative.md`: `7bf03716c95fc9d9ae06ebb038c69b6e9ed8452f2414919b35cae20365decace`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py`: `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json`: `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_freeze_v003f_c4/REVIEW_FREEZE_V003F_C4V001.md`: `72041c9ed10bd89818fafe543c9b5471352bbfb70c53a231d61256194f1203d1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_freeze_v003f_c4/tools/review_v003f_c4v001.py`: `898508c4b3bd8e0579c2a0958474afeee7c9e2b63ecd5a7accac4b2ab532458f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_freeze_v003f_c4/runs/run_20261018T141427Z/REVIEW_RESULTS.json`: `db4343bfdf58162aef13667477a464fb169a192eee8ea1e06a39ebb674d3d38a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/independent235/runs/run_20261018T145307Z/REVIEW_RESULTS.json`: `c8d1a04c4753e4a3bb54d939a054a3a890420f25bcdd5bf3b610f1c09c74b9be`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/independent235/ORIGINAL_235_MAPPING_CX3V002.json`: `4164bba80c7734d5d5ff720800d63367f05b75bc68e6b98711bbc1af35f53971`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/independent235/runs/run_20261018T145307Z/ORIGINAL_235_MAPPING.json`: `005340147df3148ea6e0522923250d2704becadcfc40e13eb6fc7a017ff93c4c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/independent235/review_v003g_c4_adapted_cx3v002.py`: `127b3fda003eecd6f42a4eb1c5da4ecc36052c4a2d4044c1831a67c9a17912ce`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/independent235/ADAPTATION_CX3V001.json`: `5bd3c09d8a6b9d43ab1895845647727bd200d01f9c42ea6b23bd9fb1ed6917c0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/independent235/ADAPTATION_CX3V002.json`: `8f58584a0af8311f32d418c58198e22e37116c863f7e6d81e080a5300fde45ea`
