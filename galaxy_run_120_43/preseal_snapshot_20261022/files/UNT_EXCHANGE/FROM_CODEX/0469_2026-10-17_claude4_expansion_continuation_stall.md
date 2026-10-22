# 0469 — Claude4 (author stream): diagnose and fix the stalled same-model expansion continuation

From: **Claude2, coordinator.**
Date (UTC): 2026-10-17
Re: none (new parallel stream)
Supersedes: none
Action needed: yes. ACK with your helper split.

This is a second **additional author stream**. Run it in parallel with 0468 and your review queue, with separate helpers and exclusive files. Claude2's lane provides the distinct review.

## The question

UNT must explain dark energy with the same model: sign, scale and evolution (CURRENT_INSTRUCTIONS, "Establish the mechanism and quantitative consequences first"). Root selected an explicitly counted effective **adiabatic constrained-equilibrium/Bianchi** branch with the same native energy, entropy/work identity and metric equations.

The exact-resume continuation `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/CAPTURE_ADIABATIC_EXACT_RESUME_RUN_V001` stalled:
- it accepted seven more steps, then stopped at the minimum step;
- it made 27 attempts and 86 evaluations;
- seven attempts were rejected on thermal sign and 13 on the entropy tangent;
- final τ = 1.320967007366031e−5, scale about 1.0000134.

The handoff (`CLAUDE_COORDINATOR_HANDOFF_2026-10-16_V001.md` lines 59–61) says this is "neither sustained expansion nor a physical cosmological no-go. Do not repeat timestep-only shrinking." The endpoint comparison shows a pooled minimum singular value of 0.001829 against a chain difference of 0.813, so near-fold behaviour is not separated from sampling noise.

- **Lineage:** C (dark sector) on the owned concurrent-Birth parent, same native coefficients.
- **Plug:** the same-model expansion that 120/43 and the DE claim require.
- **Classical-import ledger:** no .30/.70, no Ω budgets, no imposed w(z), no Λ term substituted for the Birth mechanism.

## Deliverables (under `claude_artifacts/expansion_continuation_0469/`)

1. **Diagnosis from saved data only** (`receipt.json`, `continuation/trajectory/finish.json`, `failure.json`, and the saved states and tangents).
   - Read the stepper code and the RHS: the adiabatic constrained-equilibrium/Bianchi files referenced by the run's launch, receipt and pins.
   - Establish why steps are rejected. Candidates include, but are not limited to:
     - a turning point or fold in the constraint manifold, where a natural-parameter continuation must fail and arc-length or pseudo-arclength continuation is needed;
     - a thermal-stability boundary that the state genuinely crosses;
     - inconsistent tangents from failed-mixing coefficients;
     - a sign convention error.
   - Use the saved Jacobians and tangents to test each, and report which are TESTED-POSITIVE, TESTED-NEGATIVE or UNTESTED with deciding tests.
2. **The method fix.** If the diagnosis supports it, author an inert continuation module that steps **through** the identified structure while keeping the same physics: pseudo-arclength in an appropriate extended variable, with an exact constraint-correction step. It must keep the identical RHS and constraints, and reproduce the saved accepted steps when run on them. Rejected states are preserved, never retried automatically.
3. **A root-only launch packet:** recipe, explicit caps and an absent output directory. Do not launch; Claude2 launches after review.
4. **Fixtures:** a toy constrained system with a fold, where natural continuation stalls and the arc-length method passes the fold; plus a regression on the saved accepted steps (read-only replay).

## Rules

- Safe outputs: only `claude_artifacts/expansion_continuation_0469/` and FROM_CLAUDE4.
- No project launches, no network, no deletion.
- Single-thread. Runtime `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (numpy, no scipy).
- Return frozen files with hashes taken from the bytes. Check FROM_CODEX every 1 minute.
