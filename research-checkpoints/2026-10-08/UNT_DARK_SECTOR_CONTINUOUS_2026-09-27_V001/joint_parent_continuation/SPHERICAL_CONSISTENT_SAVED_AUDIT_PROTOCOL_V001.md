# Saved state audit of the consistent inertia experiment

This is a prospective, bounded postprocessing audit of the exact two V002 spherical cases, not a trajectory rerun. It reconstructs finite-state inertia and acceleration with different assembly and solve arithmetic, checks the saved canonical states and work budgets, and reports signed pressure-on/off profiles. The auditor shares the producer's author; **distinct arithmetic is not independently authored replication**. Independent source review and root syntax checking are required before root alone executes the auditor.

The methodological source was drafted without importing or running numerical code and before inspecting case result contents. Root supplied the completed freeze and result hashes, which are execution pins, not new numerical choices. The V001 producer syntax failure and V002 technical repair remain frozen ancestry; the auditor neither overwrites nor reruns either producer.

## Fixed inputs and custody

All files are under `/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation`.

| Input | SHA256 |
| --- | --- |
| V002 producer freeze | `319322787bda24ca11b842c35f74d65a5dbca15f0d0b5eb351e0d71955f0d9d5` |
| V002 supervisor freeze | `1591736f2714a63d2f082a90d5b447f1b1da88ccd9ef5c47b44f36bdbfce6c5d` |
| V002 freeze invocation receipt | `31d54e2c77167b12929bfd03e0ba7f3c3c83657b06d7e840cec84c898046e3e0` |
| V002 case 000 raw result | `5c77c9463ca5e2bff408bf71197d4ce19ca7fc3e931bec498a70b869e429c607` |
| V002 case 001 raw result | `5904e43e52c20663b4013821372a058e72a888fcdce60db1a1380e0c50f1acbd` |
| V002 case 000 invocation receipt | `2bf68d2670ba89c5cbf80c8c485bb52dbde683a9ab068244b2346e471095894b` |
| V002 case 001 invocation receipt | `eb810e99c90c393b03dea67746717002a6c7a95c10a2698ba3cf593a57b3cd9b` |
| V002 serial result | `e4e0c44e73c0dd10f6d80b8946391dc3a97d50e308c973a52666c654b303c559` |

The source pins the V002 producer, exact kernel, state maps and inherited old numerical definitions. It rehashes every member of the V002 science freeze before loading any definitions. It checks the producer/supervisor/freeze-capture lineage and recomputes canonical payload hashes for the actual case results and their case invocation receipts. Other freeze/serial objects are authenticated by their pinned file hashes, not by a separate payload recanonicalization. It also checks case identity, invocation capture hash and byte length, and exact base64-decoded stdout equality to the corresponding raw result. All inputs are rehashed at the end. A numerical reconstruction pass never waives inherited producer failures or resource/custody failures.

Only initialization and `Model.read` from the authenticated producer are used, to obtain unchanged fixed masses, physical units, EOS and original pressure/gravity forces. The audited module is loaded under a non-main name; inject NumPy and the auditor's resource guard into its namespace. No producer `main`, `inputs`, `rhs`, controls, `run_case`, snapshot or integrator is called. Re-evaluation of the same finite material/force readouts is postprocessing, not new propagation. It is not an independent physical-force derivation.

## Distinct finite shell arithmetic

For each non-origin shell, independently form the dense two-by-two mass block from the polynomial numerators

`NLL=5q³+6q⁴+3q⁵+q⁶`, `NLR=q²+3q³+q⁴`, `NRR=1+3q+6q²+5q³`,

where `q=L/R`, `S=1+q+q²`, and the coefficients are `3/5,9/10,3/5`. Use `m c N/S³`. Differentiate with the quotient rule `m c (N' S−3N S')/S⁴`, not the kernel's simplified derivative coefficients or factored quadratic geometric force. The constrained origin contributes its single constant `3m/5` entry.

Assemble a dense 128-by-128 matrix and use NumPy's dense solve for `v=M^-1p/A`, rather than the producer's tridiagonal LDL solve. Assemble `g_j=vᵀM_,jv/2` from the local derivative blocks and `Mdot=M'[v/A]` from their directional derivative. Compute kinetic energy directly by `vᵀMv/2`. This is a binary64 cross-check, not interval arithmetic, a new symbolic proof, or an exact degeneracy/conditioning certificate.

For each saved state, separately reconstruct gravity/pressure responses, geometric kick response, inertia-motion and Hubble terms, and their sum

`vdot=M^-1(f+g)/A−M^-1(Mdot v)−H v`.

Here `vdot` is the derivative of **peculiar velocity**, not physical-radius acceleration. Check instantaneous geometric work cancellation using `vᵀMdot v/2=xdot·g` and `Kdot=xdot·(f+g)−vᵀMdot v/2−2HK`. Pressure-off reconstruction omits only the pressure force; consistent inertia and geometry remain.

## State census and comparisons

The fixed census is two cases, five saved methods per case (`RK4_h`, `RK4_h2`, `RK4_h4`, `DOPRI54`, pressure-off `RK4_h4`) and four readouts `[0,1/64,1/32,1/16]`: 40 states if complete. Exactly eight designated fine pressure-on snapshots are expected. Bind method vectors to their journal sample states with zero tolerance when both are present. A partial journal is audited only over its valid saved prefix, preserving status, missing methods, last accepted state and the producer's failed-state record. Missing or partial output cannot pass the complete census.

Reconstruct each state's full nonlinear chart using its own meshes and scale factor, with only the last three hard-specific ledgers normalized by total hard mass. Compare all three other pressure-on methods against `RK4_h4`, plus separate pointwise velocity, volume and action checks. Preserve raw canonical momentum as momentum, not a locally divided velocity surrogate.

For all available pressure-on methods, check the same total, mechanical, hard-per-rest-mass and ordinary energy/work budgets from the reconstructed kinetic energies and raw saved ledgers. This applies the existing finite criteria to every method, not only the designated snapshot reference; a coarse-method failure remains a failure. Pressure-off fluid-energy qualification is deliberately absent.

For each fine snapshot, bind the saved mesh, canonical momentum, fixed cell mass, inertia entries, velocity, density, volume ratio, kinetic energy, geometric kick, material readouts, pressure, ledger and complete acceleration components to the raw-state reconstruction. Compare the independently assembled dense matrix and geometry against the validated read implementation as separate checks. These checks cannot independently establish the correctness of the physical EOS or gravity source reused from that implementation.

Keep the original thresholds: arithmetic `2e-11`, material `2e-10`, physical-chart state `2e-8`, and velocity/volume/action and work `2e-7`. Unless explicitly normalized, use `|a-b|/max(1,|a|,|b|)`. Inertia, geometry and kinetic comparisons are per fixed total species mass; material/density comparisons use the stated source amplitude scale so tiny hard density is not hidden by an absolute unit floor. No thresholds, signs, initial states or mesh masks are selected from the outcome.

## Signed origin and seed edge diagnostics

At every available paired time, save complete signed pressure-on minus pressure-off arrays for both species' faces, peculiar velocities and cell densities. This includes initial and final profiles when both exist. Also report fixed labels, not outcome-selected locations:

- constrained origin displacement at full-face index 0;
- first free face displacement at full-face index 1, its velocity at free-face index 0, and central-cell density at cell index 0;
- compact-seed edge displacement at full-face index 16 and its velocity at free-face index 15;
- seed-edge adjacent densities at cell indices 15 and 16.

These indices follow the fixed `dx=1/16` initial labels and seed radius 1. They do not identify a late-time physical discontinuity. Bind the whole signed profiles to the producer's saved pressure-on/off differences when available. Do not take absolute values before reporting signs or interpret a numerical displacement as an observational halo fit. There is no spatial extrapolation from two cases at one grid width.

## Resources and publication

Root invokes `spherical_consistent_saved_audit_v001.py --run` only after source review and syntax-only checking, with all five thread environment variables equal to one. It reads only fixed local inputs, installs nothing and spawns no worker. Limits are 90 seconds wall, CPU soft/hard 85/90 seconds, sampled self RSS 512 MiB, 64 MiB per input, 220 input identities, and 16 MiB result output. Source, protocol and complete input identities enter an exclusive intent before numerical postprocessing. The result uses atomic no-overwrite publication with fsync; existing intent or result refuses automatic retry. Resource records refer to analysis before final serialization.

Retain partial reports, every check group, any exception and custody failure. The input existence/hash gate may fail before creating an intent; no missing file is substituted. A failed inherited case is not converted into overall success merely because reconstructing some saved states works. This two-case pinned audit is not a mechanism for silently selecting a different batch.

## Limits and next action

No trajectory is rerun. Distinct dense/quotient arithmetic and a saved-state audit do not establish continuum convergence, certified CFL or no-crossing behavior, a relativistic metric, physical state formation, a common microscopic source or an observational fit. Every physical qualification and Stage 3 completion flag remains false; all 11 mandatory lanes remain OPEN.

The next authorized action is independent review of this inert source/protocol and root syntax checking, then one bounded root-owned execution when no other numerical worker is live. Interpret the complete signed profiles and any failures before considering the already planned interface/spatial refinement. A separate reviewer should assess the saved result; this source's common authorship with the producer must remain explicit.
