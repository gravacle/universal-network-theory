# Dispatch0548 independent Stage0 alternative review

date -u: Sun Oct 18 14:54:04 UTC 2026

**TESTED PASS, 115/115**, scoped to r004 source, inert normalization/import probes, and actual result-assembly AST. No defect found in the reviewed delta. No scientific stage or worker main was invoked.

- A/B normalization at K_big 16 and 32 preserves the headline normalized fields except the exact coefficient pin and explicit alternative metadata. The stage-0 grid is admitted only with coefficient_alternative=STAGE0_GRID_OUTER. Missing/wrong/null flags, A2 with the flag, path/hash mismatches, GL10, changed distance/inclination/entropy, DDO misuse, and tail-off all refuse. The fe5 grid refuses under both flag modes and both tail modes on both routes.
- The frozen slots pin independently yields OUTER Q36–Q43 from R >= 30 kpc. It marks the alternative non-headline, coefficient-grid-only, and NOT_EVALUATED_BEFORE_FREEZE as fallback. The driver's actual assembly AST retains all 43 rows, adds the exact pinned OUTER scoring scope to the Stage0 alternative label, and adds no alternative label for the headline.
- Actual prep coefficient-load AST reads the stage-0 bdb9016c grid and the headline A2 grid separately. Both loaded coefficient arrays, background_mu and background_C match their respective files exactly. The Stage0 prep AST differs from headline prep only in COEFFICIENT and COEFFICIENT_SHA assignments. This was an array-load probe, not prepare_inputs or solver execution.
- The selected Stage0 prep, serial worker, parallel worker and manifest-writer bytes match their pins. Source inspection confirms worker/writer LOCAL prep entries point to the Stage0 prep. Route-B stage pins remain unchanged.
- Scoped V011_PINS and GALAXIES changes restore by object identity and value after normalization and after both returning and raising synthetic dispatch callbacks. The NGC script/worker/monitor tables also restore. The DDO galaxy object remains identical within the Stage0 scope. The Stage0 grid is absent from the headline decided-grid table afterward.
- The r5 parent source body remains an exact byte prefix. Only four existing NGC functions change against r003: normalize_spec, _ngc_v011_seed, _ngc_v011_dispatch and _cmd_run_ngc_cx3v005. Seed numerical inputs stay identical and record the actual alternative coefficient pin without adding headline A2 as an active source pin.

Peak recorded RSS: 115,097,600 bytes. Mandatory Python -I -B and single-thread BLAS used. The audit guard rejected destructive actions, subprocess/network operations, forbidden run reads, and nonexclusive writes.

**UNTESTED here:** full forward execution, physical predictions, outer-score arithmetic in the freeze module, production certificate validity, and whether launch-time calibration coordinates actually belong to the admitted headline DDO set. The driver can preserve supplied coordinates; selection/admission of those points remains the coordinator's obligation. This source review does not establish launch readiness. Root owns the eight complete dry plans and DDO B0 comparison.

Cited files, sha256 from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/galaxy_m0_forward_c2v011_cx3v005_cx3r004.py` — sha256 `39c505175905576ff1029ede4be20be765ba47967b5a6eedf1298bd7c4305895`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/BUILD_CX3V005_V004.json` — sha256 `335fe81098511313080844df7b49f4ca5c89b2f25433049885312e391ce2a508`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` — sha256 `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/independent_review/review_stage0_cx3v001.py` — sha256 `63d0858540af9352286877de9c2c65960cde1a68e5557f579272ebe2e84e97b9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/independent_review/RESULTS_V001.json` — sha256 `de37c55d6244af454b8532024f83e006a57fa524767395370e35b696ff1750a7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/independent_review/ASSEMBLY_True.json` — sha256 `bf70ce61de110cddd2e292ebbb1f9f4653cb1ce669031173d98167ca0500f358`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/independent_review/ASSEMBLY_False.json` — sha256 `8ec678099b39b994d30869aa58c3f6c85fefe015ad98ad538864d058e4d411a1`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0548_2026-10-18_codex3_register_stage0_grid_outer_alternative.md` — sha256 `7bf03716c95fc9d9ae06ebb038c69b6e9ed8452f2414919b35cae20365decace`
