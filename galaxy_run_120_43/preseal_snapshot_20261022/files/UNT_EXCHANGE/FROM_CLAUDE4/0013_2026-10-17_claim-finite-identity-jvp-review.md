# 0013 — Claude4 takes the pending distinct implementation review of the finite identity candidate JVP

From **Claude4**, the independent review lane. UTC 2026-10-17T11:45Z. Status: ACTIVE.

The principal gave this instruction directly to Claude4 at about 11:40Z: "Proceed we must move through model construction and move on the the Galaxy Run 120/43 as quickly as possible."

## Why this item

CLAUDE_COORDINATOR_HANDOFF_2026-10-16_V001.md (3dad81ed…) names the next flow dependency: differentiate the actual finite residual, including eliminated S, the transported nonzero base residual and the observed-Sigma constraints.

CLAUDE_COORDINATOR_POST_HANDOFF_UPDATE_2026-10-16_V002.json records what Codex1's local helpers had done toward it:

- integration_review authored the JVP;
- recovered_packet_audit returned the algebra review, with implementation review still pending.

Those helpers cannot continue, because their chat state does not transfer. No implementation review and no run directory exist for this JVP. The work is review, which is Claude4's lane, and it needs no launch.

## Pins (verified 11:43Z; the core hash matches INPUTS_V001)

All paths are relative to UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/.

| File | SHA-256 |
|---|---|
| integration_review/owned_finite_identity_candidate_jvp_v001.py (core) | cfb988f4707d2296026174295802296b2d83b0bda873d67d4fe950f88d13d554 |
| integration_review/ddo154_finite_identity_candidate_jvp_root_v001.py (root driver) | 2b89fa0cab9a8f4213e2d7eab60d6fa18c11b02455378cbad6c9f17029bda4e7 |
| integration_review/FINITE_IDENTITY_CANDIDATE_JVP_INPUTS_V001.json | d0c194f07f55c7b89444fbbd651c81712796628149cdda2f93cda9b8f7e40ecb |
| integration_review/owned_finite_material_residual_v001.py (finite core) | 6f73d0755192b223fa9421cf94629a7029938945153be4caeddae9cabc83b540 |
| integration_review/FINITE_MATERIAL_RESIDUAL_SPECIFICATION_V001.json | 4bd679df10a4dc1b6f41de413abac00e4a33defe4830afcae02a7260108f6a8e |
| recovered_packet_audit/FINITE_MATERIAL_IDENTITY_JVP_ALGEBRA_REVIEW_V001.json | 44e6341259c1c423575caee6dc483d1bf68433e1311fe1ee8ab570aa9ca5ff0c |
| coefficient_method/owned_body_fitted_displacement_binding_v002.py | 87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462 |

## Scope

An exact-byte implementation review of the core and the root driver, checked against the residual specification and the algebra review. It covers:

- every derivative term: geometry, kinetic test, pressure, the force with the full total-field Hessian, the material source, the S elimination including nonzero delta_s0 and Hdot, and the Sigma moments;
- signs, conjugation and the 2π count;
- the base-residual transport, which must be neither dropped nor double-counted;
- driver custody and limits.

The evidence will come from separate helpers: an independent algebra/sign derivation, and manufactured fixtures on synthetic states. The fixtures compare the JVP with directional finite differences of the finite core and check linearity. The JVP will also be tested against deliberate mutants.

## Not doing

- No run of the root driver and no project calculation on the saved DDO154 arrays. Root, now Claude2, launches.
- No galaxy data, calibration or target velocities opened.
- No edits to author files.

Outputs go only to claude_artifacts/finite_identity_jvp_review_c4/ and FROM_CLAUDE4.

## For the coordinator

Claude2 can redirect or stop this. Claude4 will follow a coordinator dispatch as soon as it arrives.

One item on the path to 120/43 is unowned and is the coordinator's call: the nonlinear finite-residual solver that would use this JVP. The handoff says no next nonlinear solver is claimed implemented, and it suggests the old linear operator as a possible preconditioner. Claude3 reports itself idle (FROM_CLAUDE3/0010).
