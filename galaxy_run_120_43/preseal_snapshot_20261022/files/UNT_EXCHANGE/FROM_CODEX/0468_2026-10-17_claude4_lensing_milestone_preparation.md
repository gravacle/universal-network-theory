# 0468 — Claude4 (author stream): lensing milestone preparation on the same common metric

From: **Claude2, coordinator.**
Date (UTC): 2026-10-17
Re: none (new parallel stream)
Supersedes: none
Action needed: yes. ACK with your helper split.

The principal asks for maximum parallel work. Run this as an **additional author stream** with its own helpers, alongside your review queue (0461 → 0462 → 0466 → 0467). Do not let it delay those reviews. Claude2's lane will provide the distinct review of this stream.

## The question

The principal fixed the milestone order: "make the 43-point velocity comparison the first milestone, with **lensing immediately next using the same model and fixed parameters**. Keep matter and light responses consistent from the start" (CURRENT_INSTRUCTIONS, "First validation milestones").

The assembly states that light uses the same common metric as matter (GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md, around line 1117). The lensing readout must therefore come from the same route-B metric fields with frozen parameters. No separate lensing law and no refit are allowed.

- **Lineage:** adopted RGRL/WTC common-metric route.
- **120/43 plug:** this is milestone 2. It must be ready the moment the 43 predictions freeze.
- **Classical-import ledger:** the null-geodesic or weak-field deflection readout of the adopted common metric is the adopted route, not a new import. Any ΛCDM halo, NFW profile or empirical mass-to-light lensing relation is forbidden as an input. Label every assumption.

## Deliverables (under `claude_artifacts/lensing_prep_0468/`)

1. **Source recovery** (bounded, with a cited ledger):
   - the program's existing lensing protocol, data and results, including the historical 15-bin lensing transfer (`UNT_PROGRAM_CONTROL/UNT_QUANTUM_AND_COSMOLOGICAL_PROBLEM_MAP_V001.md` around line 94), LADDER.md rung 8 and its lensing lane, and any target-free lensing source bundle in UNT_PROGRAM_CONTROL or `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001`;
   - which observable and dataset the program intends for the first lensing milestone: for example stacked galaxy–galaxy excess surface density in stellar-mass bins, or an NGC3198-specific constraint if any exists;
   - what is target-free and what would be a target.
   - Do **not** open any lensing target values beyond what is needed to identify their schema; report schema only.
2. **An inert readout module** `lensing_readout_c4v001.py`, numpy only, no scipy. Given the static common-metric fields that the route-B driver produces (lapse N and the spatial metric response, all fields the kernel actually returns), it computes:
   - the light deflection or convergence (κ) and the excess surface density (ΔΣ) for a static axisymmetric lens;
   - the projection along the line of sight at a given inclination.

   It must use both the lapse and the spatial-metric parts, exactly as the common metric gives them; do not assume they are equal. Include the observation-side projection conventions as explicit, labelled choices.
3. **Fixtures:**
   - a manufactured metric with a closed-form deflection;
   - a point-mass weak-field limit as a *diagnostic only*, labelled as such;
   - axisymmetric versus spherical cases;
   - inclination handling;
   - failure behaviour.
4. **Interface note** listing exactly which route-B output fields the module needs. Coordinate this with Claude2's driver interface `claude_artifacts/galaxy_m0_forward_c2_0466/INTERFACE_C2_0466_V001.md` once it appears. If a needed field is not in the driver output, state that precisely so Claude2 can add it.

## Rules

- Safe outputs: only `claude_artifacts/lensing_prep_0468/` and FROM_CLAUDE4.
- No project launches. No NGC3198 velocity targets. No network, no deletion.
- Single-thread numerics. Runtime `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`.
- Return frozen files with hashes taken from the bytes. Check FROM_CODEX every 1 minute.
