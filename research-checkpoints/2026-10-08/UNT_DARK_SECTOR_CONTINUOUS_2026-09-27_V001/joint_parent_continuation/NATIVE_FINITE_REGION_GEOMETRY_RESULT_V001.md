# Finite geometry retention and the work supplied by copying

2026-10-03 UTC. The four histories in the frozen finite-region protocol
completed once. Added fragment copying does not consistently improve
connectivity over the declared window. The connected preparation remains
mostly connected with copying either on or off; the disconnected preparation
remains mostly disconnected. These are finite preparation-dependent results,
not autonomous formation, a physical geometry, or a rejection of UNT.

## What was measured

All nine links, the mobile carrier, the active record and both fragments
were retained in the 24,576-dimensional state. Every history has 68 rows:
the fixed x=0,1/16,...,4 mesh plus both sides of the three switches. No
parameters, observation ages or tolerances were selected after seeing output.
Both supplied graph states have the same labelled degrees and initial energy
25.5. Their immediate carrier-site neighborhoods agree, but more distant
geometry differs; this does not isolate topology from all local differences.

| Preparation and fragment copying | Connected probability at x=4 | Connected and five edges at x=4 | Sampled connected probability range |
| --- | ---: | ---: | ---: |
| Path, off | 0.942185099539 | 0.932262087483 | 0.922673829507 to 1 |
| Path, on | 0.941931471618 | 0.931956401510 | 0.922701107379 to 1 |
| Cycle plus edge, off | 0.008033477429 | 0.003031829817 | 0 to 0.026602346013 |
| Cycle plus edge, on | 0.008077074127 | 0.003018913151 | 0 to 0.026601738568 |

Connected-and-five-edge probability is unnormalized joint probability, not
postselection. Sampled ranges are not continuous-window bounds. The path's
on-minus-off connectivity varies from -0.000613988347 to +0.000642323103;
the disconnected preparation's varies from -0.000117228701 to +0.000169438364.
There are seven and nine sampled strict sign changes respectively. No
universal connectivity threshold was specified or is now fitted. The tiny
raw total-energy sign changes near machine precision in the JSON are not
physical effects. All the connectivity sign-change endpoints just counted
exceed the assigned 1e-10 arithmetic allowance in magnitude.

## Fragment energy is mostly supplied work in this experiment

All entries below are inherited generator energy units, not SI values.
After x=2 all copy ports are off and each displayed energy is conserved.

| Preparation and copying | Total switching work | Final fragment energy | Native energy change from 25.5 |
| --- | ---: | ---: | ---: |
| Path, off | 0.005940280616 | 0 | +0.005940280616 |
| Path, on | 0.501122188880 | 0.537725740474 | -0.036603551594 |
| Cycle plus edge, off | 0.003150685463 | 0 | +0.003150685463 |
| Cycle plus edge, on | 0.497540132273 | 0.535450572437 | -0.037910440164 |

For every row, Delta E_native + E_fragments = W_switch. In particular,
the path's native cooling is not 0.5377: it is 0.03660 relative to its
initial energy, or 0.04254 relative to its copying-off control. The
disconnected values are 0.03791 and 0.04106. Copying changes carrier
probabilities appreciably more than connectivity in this finite experiment,
but none of those probabilities is an acceleration or a force measurement.
Switch-on has zero mean work; preparing graphs, blank fragments and the
schedule is still an input, not a free physical resource.

## Exact reason not to mistake the hold for continuing relaxation

For s=x-2>=0 the complete Hamiltonian factorizes as

    H_hold = H_native tensor I_b + I_native tensor (b1+b2).

Consequently, even with preexisting native-fragment entanglement,

    rho_native(2+s) = U_native(s) rho_native(2) U_native(s)^dagger.

Tracing the fragments for a diagnostic does not remove their energy from
the full ledger. The native marginal's eigenvalues, purity and its trace
distance from any other native marginal evolved with this same H_native
are exactly constant during hold. There is no continuing dissipation into
the decoupled fragments. Native observables can still change through unitary
motion. This is a stronger statement for this decoupled interval than the
older finite-fragment recurrence result; it is not a ban on finite-window
geometry or on a different autonomous environment.

The record occupation also commutes with H_native. Writing H_gc for the
graph-carrier terms, the two record sectors evolve under

    H_r = H_gc + r*(1 - d0/2),    r=0,1.

For a graph-carrier observable O, the exact expectation is the sum of its
expectations in the two subnormalized blocks rho_r, evolved under H_r.
No independent-marginal factorization is used. Off-diagonal record coherence
does not enter such an O during this hold, although it remains in the full
state and matters for record-sensitive probes or reactivated copy ports.

Only the native link flips fail to commute with the connectivity projector
C. In protocol units its exact current is

    d<C>/dx = -i*h*sum_e <[X_e,C]>,    h=1/3.

The copies and record feedback alter the state that carries this current;
they are not an additional direct connectivity current. This does not prove
a causal energy-barrier explanation of retention from four finite histories.

## Next saved-state discriminator fixed before its calculation

This is exploratory analysis prompted by the completed result, not a new
held-out prediction or a rerun of formation. Use all eight saved full states
at the original x=2 and x=4 endpoints, with the same 1e-10 assigned arithmetic
allowance. Ask whether the small geometry effect can be represented solely
by changed record populations, or requires different conditional states.
For each preparation, record sector and endpoint, compare the explicit null

    rho_on,r = (p_on,r / p_off,r) * rho_off,r.

This null concerns only the record-diagonal native blocks. It does not
constrain cross-record coherences rho_01 and must not be described as a
full-native population-only equivalence. Connectivity commutes with r,
so this limitation does not affect the proposed connectivity comparison.

If either required population is at most 1e-10, conditional quantities are
undefined rather than zero. This guard defines reporting, not a new physical
threshold. Divide by sector populations only for explicitly conditional
diagnostics; do not renormalize evolved states or project their evolution.

Calculate actual joint C and C-and-five-edge probabilities and connectivity
current in each sector; predict them under the population-only null by
reweighting the off-sector values with the on-sector populations. Keep both
signs and both endpoints. Compute conditional trace distances D_r and the
bound |<C>_on-<C>_null| <= sum_r p_on,r D_r. A resolved nonzero residual or
conditional trace distance rejects this specific null, not a coarse-grained
theory with retained memory. No current bound follows from the projector
bound without including the current operator norm.

Each fragment trace is a sum of four outer products, not a dense native
density matrix. Use a four-column Gram matrix for nonzero native eigenvalues
and a thin QR of at most eight columns for trace distances. Compute full
native on/off and between-preparation distances as well. The exact hold
identities above predict invariant distances and eigenvalues between x=2,4;
they do not predict time-independent connectivity. Source checks must be
reported separately from scientific-null outcomes. No propagator or producer
imports, new formation ages, parameter changes or new dependencies are needed.
Use one root-owned worker, 120 seconds and 256 MiB maximum as before.

Do not autonomize the ineffective copying schedule merely to acquire a
larger model. First determine what state information actually bears its
observed effect. Native source/ruler/volume and a finite-window formation
mechanism remain the program's physical requirements. An asymptotic ground
state or universal attractor is not imposed as an extra requirement.

## Reproducibility and evidence ceiling

The producer exited0 in 20.050565 seconds, with 82,771,968 bytes peak self RSS.
All 2105 assigned checks pass; the largest residual is 2.77112e-13. The
analytic propagation truncation bound is 2.55428e-18 per complete history;
it excludes floating-point error, which is not interval-certified. No state
renormalization was applied. All eight full endpoint states are saved.
Independent internal source review found no blocking operator, indexing,
switch-work or Taylor-bound issue. This is not external peer review or an
observational test.

- Frozen protocol SHA256: 49db143bee98adc6077640f162401baaca9d8851adc3947bd77fda031aa2a8ee.
- Producer native_finite_region_formation_v001.py SHA256:
  8434042c9e74ef42b292436d59d7b3601dda941ef33c20241d382c34c3487056.
- Result native_finite_region_formation_v001_results.json SHA256:
  2a52ba3a029c2aa6d6a421d942837cb78035e935c61a0ae60ababe5237862c91.

All eleven scientific lanes remain OPEN. No URM candidate, sealed API,
physical parameter, Stage3 completion or superiority claim is promoted.
