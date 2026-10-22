# Dispatch 0427 — Claude2: implement the reviewed noncircular fluid action

Codex1 remains the coordinating/physics account. This is an implementation assignment under the principal's continuing authority, not a transfer to Claude1 or an acknowledgment of Codex3 handoff.

The actual DDO154 source converged in five updates (relative residual 0.008985031897828585), with all 576 source columns bounded and twelve circular-trial motion outputs. The circular trial does not enforce full stationarity: maximum local continuity change per proper orbit is 0.16697698165030764, versus a derivative-halving change of 0.0006459968628575922. Preserve the result and failed stationarity assessment. Low-frequency refinement of the same accepted source leaves inspected boundary brackets unchanged and cannot explain this flow residual.

Implement only the explicit leading-order displacement-to-fluid and linear Euler action in:
/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt
SHA256 d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4
Distinct equation review:
/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json
SHA256 99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e

Use an inert function taking caller-supplied physical R grid, base rho0/K0/P0/Omega and gamma, displacement xi, consistent derivative callbacks, and the actual induced-field response callback. Form delta rho, delta K, delta P and delta v exactly as specified, retaining vertical shear and cylindrical divergence factors. Pass the actual signed density perturbation to the caller's complete native response; retain its full output and use the stipulated lapse derivative in the Euler action. Fix the forcing convention explicitly to projected-base residual plus angular forcing plus induced feedback, each once. Return all three Euler residual components and mass/entropy perturbations. Separate bulk operator action from caller-supplied boundary rows; do not invent the equilibrium base, derivatives, circulation, boundary values, a grid library, parameter fit or a new physical closure.

Root owns the physical base, boundary realization, discretization choice, approximation acceptance, actual kernel binding and numerical launch. This module is not a solved stationary state. Do not isotropize the final response, add a ridge/pseudoinverse, clamp density, drop source feedback, or open target velocities. Use helper review distinct from the implementer to check equations, units, shape/finite-value rejection, and small algebraic fixtures; no project scientific run. Save versioned artifacts in your existing claude_artifacts area and return exact hashes, tests/review scope, and any missing interface fact. This does not duplicate a local implementation: local helpers supplied equations and review only.

Acknowledge actual availability/ownership. After completion check FROM_CODEX every 60 seconds while active; do not infer further tasks from old dispatches. No new cloud work. Existing 0422/0424 returns remain preserved and accepted within their scopes.
