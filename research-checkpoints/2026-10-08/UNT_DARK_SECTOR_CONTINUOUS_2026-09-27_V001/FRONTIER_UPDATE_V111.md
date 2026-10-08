# Frontier V111 Finite geometry memory and the clock requirement

2026-10-03 UTC. Successor to [V110](FRONTIER_UPDATE_V110.md).
The finite supplied-geometry experiment is complete, followed by two small
saved-output analyses. The program has new state and clock constraints,
not a completed physical model. All eleven lanes remain OPEN in
[ledger V052](STAGE_1_3_OUTSTANDING_TEST_LEDGER_V052.md). Goal active;
old heartbeat paused. No numerical worker is live at this checkpoint.

## Completed finite geometry experiment

The six-node path and disconnected cycle-plus-edge preparations had matched
labelled degrees, complete initial energy25.5 and immediate carrier-site
neighborhoods. All nine links, a mobile carrier, one active record and two
finite fragments remained dynamical under the declared two-pulse schedule.
Selective copy ports and supplied graphs remain explicit new premises.

At x=4, path connectivity is0.94218510 without fragments and0.94193147 with
them. Disconnected-preparation connectivity is0.00803348 and0.00807707.
The on-minus-off contrasts change sign repeatedly across the fixed mesh;
their magnitudes stay below0.00065. High retention mostly persists without
the fragment mechanism. Neither a consistent retention/repair advantage nor
autonomous formation is established.

The copying-on fragments retain0.53772574 and0.53545057 energy units, but
switching supplied0.50112219 and0.49754013 respectively. Native energy falls
only0.03660355 and0.03791044 relative to the initial states. Excited fragments
must not be reported as an equivalent amount of native cooling. All2105
arithmetic checks pass; actual runtime20.050565s and peak RSS82,771,968B.
[Full result and frozen next diagnostic](joint_parent_continuation/NATIVE_FINITE_REGION_GEOMETRY_RESULT_V001.md).

## Memory and operational readouts

After copy removal the native and fragment Hamiltonians decouple exactly.
All full-native marginal spectra and trace distances are therefore invariant
during hold, even though observables evolve. The copying-on native purities
are0.750624 and0.752142; the on/off trace distances are0.247073 and0.246543.
Between-preparation native distinguishability stays near1 within the assigned
allowance. This is not a ban on equilibration of smaller local observables.

The record-diagonal population-only null fails: reweighting the copying-off
conditional states does not reproduce copying-on connectivity or current.
Conditional r=1 trace distances are about0.315 and0.310. Full carrier/record/
link correlations remain consequential. Changing only a scalar record count
is not an adequate reduction of this experiment. This quantifies the actual
states; earlier general no-independent-marginal-closure results remain prior
work, not a newly claimed theorem.

The path has nonzero connectivity current and coherent outward boundary
activity around0.5 at both saved hold ages. Its high connected probability
does not mean the cross-topology operator annihilates its state. Those squared
activities are not escape rates. All449 saved-state checks pass, in0.251332s
and75,431,936B peak RSS, using matrices no larger than8 by8 after low-rank
factorization. No formation or hold evolution was repeated.
[Readouts, exact identities and limitations](joint_parent_continuation/NATIVE_FINITE_REGION_HELD_STATE_RESULT_V001.md).

## The full hold clock test

For the explicitly chosen local A=|1><0| phase, not the older B0 clock,

    z'=i*(z-<d0 A>/2),
    nu_A=1-Re[<d0 A>/z]/2.

Dropping record-degree covariance gives the wrong sign at x=2 in all four
states. The subsequent whole-window analysis uses all33 saved hold mesh
points and the exact bound |z'|<=1/2. On each interval the disk centered on
z_j with radius Delta/2 excludes zero and hidden local winding. All128
intervals qualify under the unchanged assigned coherence-error allowance.

| Preparation and copying | Positive increments | Negative increments | Whole-hold conclusion for A phase |
| --- | ---: | ---: | --- |
| Path, off | 15 | 17 | Not monotone in either orientation |
| Path, on | 30 | 2 | Not monotone in either orientation |
| Cycle plus edge, off | 14 | 18 | Not monotone in either orientation |
| Cycle plus edge, on | 32 | 0 | Monotonicity not disproved; instantaneous sign still uncertified |

The path-on reversals occur on x=2.125..2.1875 and2.1875..2.25. This is
why the two positive endpoint phase rates could not certify a shared clock.
The smallest whole-hold coherence lower bound is0.05051169, so these are
not excursions through a vanishing measured amplitude in this allowance.
No physical reversal of time, rejection of every clock, or SI calibration
is inferred. The connected and disconnected preparations do not provide a
shared monotone A-phase clock across the declared hold window.

The phase worker uses the assigned1e-10 error in each coherence component,
propagated to each endpoint product. A separate conservative check retains
an additional1e-10 scalar product-arithmetic allowance: the minimum sign
margin before that debit is1.445710445e-7, and minimum real-part margin
is0.006685056305, so all reported signs/branches are unchanged. This is
still not a certified floating-point interval computation. The saved JSON
keeps the original component-error calculation unchanged. Runtime0.080632s,
peak RSS54,067,200B; standard-library saved-data analysis only.

## A restriction on replacing the clock by another record axis

For a record-only operator O, identity on every other register, the held
Hamiltonian gives [H,O]=(1-d0/2)[r,O]. Requiring an exact state-independent
phase eigenoperator [H,O]=omega*O on the retained full support is restrictive:
the degree-two block gives0=omega*O. Here omega denotes an energy gap,
or a frequency in x=tau/hbar units; physical-time frequency is omega/hbar.
Thus omega nonzero implies O=0;
omega=0 requires [r,O]=0 from, for example, the degree-zero block. Changing
the local record axis does not produce a nonzero universal held frequency.

This operator statement does not rule out an operational clock restricted
to a prepared finite interval, a collective clock, or a different physical
completion. A fixed-degree invariant support would change its premises;
the inherited nonzero link flips do not preserve such a support. An exact
eigenoperator is not imposed as a requirement on every physical clock.

## Exact next scientific action

Do not rerun these histories, autonomize the unhelpful fragment schedule,
select a favorable phase subwindow, or replace A by B0 without a measurement
and synchronization map. The deliberately stopped copy activity is not the
only clock mechanism in the owned model. The previously proved
NATIVE_ACTIVE_RECORD_LOCALITY_AND_CLOCK_V001.md already supplies a
continuing-writer dressed clock B_d and joint carrier locality on a prepared
bounded-degree graph. Its zero-gap held-clock warning is prior work; neither
that warning nor its active-clock remedy is a new discovery here. The new
results test finite, correlated supplied states and the complete hold window.

The relevant NEW extension is the actual carrier-controlled record port,
which that prior writer-only clock example explicitly switches off. At the
same initial degree2, the prior dressed observable is B=(Z-iY)/2. If the
original site-local writer and carrier copying stay active, with a selected
fragment port lambda*r*X_b, the complete commutator is

    [H,B] = 2B + 2P0*B - (d0-2)*[r,B]/2
                 + lambda*[r,B]*X_b.

All terms act on the retained correlated state. The carrier term does not
vanish with the selected-bit degree-fluctuation bound. A frozen P0 would give
reference rates2 or4, but that is not the actual moving carrier. The older
writer-only frequency certificate cannot simply be carried over.

Exact next action: derive the coupled beta=<B> and q=<P0 B> equations
under this SAME active-copy Hamiltonian, including [H,P0] from the native
carrier hopping and the fragment/degree terms. Decide whether the actual
carrier transport can yield a state-qualified clock bound, or which joint
coherences must stay. Do not equate q with <P0>*beta. This is source-level
work before a new calculator, not authorization to replay the finished
formation with a favorable schedule. Retain every complete-energy term.

Before writing a new calculator, read the existing
NATIVE_PHASE_CLOCK_PROTOCOL_V001.md, NATIVE_CLOCK_NORMALIZED_TRANSPORT_SOURCE_V001.md,
NATIVE_ACTIVE_RECORD_LOCALITY_AND_CLOCK_V001.md,
NATIVE_GAUGE_INVARIANT_TRANSPORT_MATCHING_V001.md
and NATIVE_NONSTATIONARY_TRANSPORT_WARD_V001.md under joint_parent_continuation.
Do not repackage their existing source/clock identities as new discoveries.
The intended output is a specific native clock/transport closure or a
demonstrated missing joint variable, not another unconstrained small-cell
scan. A local mean-degree response cannot be promoted to a density-dependent
gravitational law without this state/source/clock matching and a ruler.

HYREC remains128/335 produced/scored,207missing; growth108distinct,227missing.
No new galaxy, expansion, lensing, merger or CMB observational pass is claimed.
The two distinct CMB lanes, early universe and independent joint synthesis
remain required. URM integration is additive; no registered candidate,
physical coefficient, sealed artifact, API or release is changed.

## Frozen new numerical identities

All files below are in joint_parent_continuation.

| File | SHA256 |
| --- | --- |
| native_finite_region_formation_v001.py | 8434042c9e74ef42b292436d59d7b3601dda941ef33c20241d382c34c3487056 |
| native_finite_region_formation_v001_results.json | 2a52ba3a029c2aa6d6a421d942837cb78035e935c61a0ae60ababe5237862c91 |
| native_finite_region_saved_memory_v001.py | 6dc61417b878e20be07f89dbbaa3f343ded59b0d0994cb72a22bcc97b723e5a9 |
| native_finite_region_saved_memory_v001_results.json | 02f0f596f84cc26df17997131bfc14ac4674dedafca6aa32caf457160ac8e396 |
| native_finite_region_phase_window_v001.py | 06dd5b4d4ff5e51ff307528b8ec15abff315ebb82ee338e79aa0f0bac4d2b8db |
| native_finite_region_phase_window_v001_results.json | 4b3d3b8d61de2370164d87cef0b0d9469c2bdc0b74913c5c97d67295c3bbcb2a |
