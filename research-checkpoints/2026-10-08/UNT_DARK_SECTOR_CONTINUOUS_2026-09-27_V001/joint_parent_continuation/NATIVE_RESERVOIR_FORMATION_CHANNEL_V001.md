# Native reservoir copying and a prospective formation channel

2026-09-30. Analytic source and protocol note. No numerical producer,
propagation, import, bath fit or new state preparation was executed.

The native reservoir-copy operator has a sharper limitation than simple
energy conservation. After all record-target formation is switched off, it
preserves every spectral population of the held network energy. Keeping
formation on opens exchange channels, but does not itself establish cooling:
ideal copy-and-trace channels, and a precise degenerate-fragment case, are
unital and have their own obstruction. A nontrivial passive formation test
therefore needs an explicitly completed fragment and work ledger.

## What is new and what is already fixed

`NATIVE_PHOTON_SOURCE_PATHWAY_V001.md` already proves that a held record-count
probe cannot extract held network energy. `NATIVE_ENERGY_SOURCE_PRESERVATION_V001.md`
already distinguishes copying into records from copying out of them. The
new deductions below extend that commutant statement to full energy spectral
projectors and reduced formation channels. The inspected reservoir, writer,
thermal, phase and source notes did not contain this full channel argument.

The record-addition protocol fixes its writer pulse at g=1 for duration1,
then copying off, in microscopic hbar=1 units. It explicitly adds no reservoir
copy. The autonomous 96D A/B apparatus fixes its own formation and controller
terms but contains no fresh-fragment supply. BS10 permits reservoir gaps and
copy couplings; it does not fix their values or a replenishment schedule.
The proposed thermal calorimeters instead use incidence-coupled two-level
probes with their own explicit gaps and switching. Those values and operators
are not inherited parameters of a BS record-copy reservoir.

## Exact held energy population obstruction

Let H_h be the complete held NETWORK Hamiltonian after writer/carrier-to-record
copies and other record-changing ports are off. Retain its record onsite,
incidence, carrier, feedback and any commuting controller terms. For each
record-content projector P_vx=|x><x|, require exactly

    [H_h,P_vx]=0.                                           (1)

This holds for the declared copying-off BS parent; conservation of record
occupation alone would not suffice if another port rotated record content.
For a fragment define X_bx=|x><B|+|B><x|. With arbitrary fragment-only H_B(t),
scalar copy envelopes g_vbx(t), and no additional noncommuting network ports,

    H_tot(t)=H_h tensor I + I tensor H_B(t)
                   +sum_vbx g_vbx(t) P_vx tensor X_bx.       (2)

If Pi_E is a FULL spectral projector of H_h, (1) implies

    [Pi_E tensor I,H_tot(t)]=0,
    Tr[Pi_E rho_S(t)]=Tr[Pi_E rho_S(0)] for every E.         (3)

The proof is the finite spectral calculus: an operator commuting with H_h
commutes with each Pi_E, hence with the time-ordered unitary. Partial trace
preserves this identity. It requires neither an initially independent fragment
nor a Markov approximation. Degenerate energy-BLOCK populations are invariant;
an arbitrary eigenvector population within a degenerate block is not asserted.
All moments of H_h and its full energy distribution are preserved.

This excludes changing an inverted nondegenerate energy population, and
excludes a unique attracting distribution independent of those conserved
populations. With degeneracies, an inversion of the mean population per state
between two energy blocks is already an obstruction to global passivity.
Removing energy coherences CAN passivate a state whose only nonpassivity was
coherence. Thus (3) is not a no-go theorem against every form of passivation,
nor against a restricted low-frequency source channel.

H_B generally fails to commute with its own copy target X_bx. Fragment energy
can change; switching/interaction energy must pay for it. Equation (3) concerns
H_h, not conservation of H_h+H_B during arbitrary switching. It also does not
apply to ongoing record-target formation, to a network-dependent copy envelope
such as g(Q) that fails to commute with H_h, or to an added exchange port.

## Two unital controls with formation present

An ideal copy to orthogonal blank-target pointer states followed by tracing
the target gives the pinching channel

    D(rho)=sum_alpha P_alpha rho P_alpha,  D(I)=I,          (4)

where alpha includes the blank and both contents. The BS copy generator alone
with degenerate target and pulse area integral(g dt)/hbar=pi/2 implements
such a copy, up to
irrelevant conditional pointer phases. This ideal limit is not the existing
finite-gap pulse without qualification. Interleaving (4) with any closed
formation unitaries remains unital.

There is also an exact simultaneous control using the invariant single-content
block already owned by the two-endpoint preparations. For one blank fragment,
zero fragment gap, and its actual BS operator q_r tensor X_b, let

    H_tot(t)=H_S(t) tensor I+g_b(t)q_r tensor X_b.            (5)

H_S(t) may retain record-target formation and need not commute with q_r.
Resolving X_b into its two eigenstates gives exactly

    Phi(rho)=1/2 U_+ rho U_+^dagger+1/2 U_- rho U_-^dagger,
    U_+/-=T exp[-i integral (H_S(t)+/-g_b(t)q_r)dt/hbar].   (6)

Thus Phi(I)=I even with simultaneous formation. Independent fixed-content
fragments with commuting target X operators give the corresponding larger
random-unitary mixture. This proof does NOT cover simultaneous full-qutrit
content shifts X_b0 and X_b1, which need not commute, or a nonzero fragment
gap epsilon_b q_b, since [q_b,X_b] is nonzero.

A unital channel that attracts every state to one fixed point must attract
to I/d, since I/d is already fixed. In that state every commutator expectation
vanishes by cyclicity of trace. This is a null retarded commutator response,
not zero noise, absolute energy, pressure or explicit nonlinear source contact.
It does not supply the desired nontrivial passive polarization spectrum.
For maximally mixed invariant sectors with different weights the null extends
only to sources preserving those sectors; cross-sector sources must be kept.
Unitality alone does not prove mixing, a unique fixed point, or finite-time
stationarity. The signed old results are not replaced by I/d.

## Minimal prospective formation channel

Keep the already declared autonomous A/B Hamiltonians H_S and all four blank
endpoint preparations. Append one native fragment b at a prospectively anchored
record site j, initially |B>. In the common-content invariant block the
prospective zero-source total Hamiltonian is

    H_tot(t)=H_S+epsilon_b q_b+u(t)g_b q_j tensor X_b.       (7)

Here q_j is the RECORD occupation, not carrier density or total record count.
Use the left and right attachments as a complete mirror census if this
candidate is instantiated; neither may be selected for a favorable outcome.
Each zero-probe cycle of length Delta defines, at a decoupled boundary,

    Phi(rho)=Tr_b[U_Delta(rho tensor |B><B|)U_Delta^dagger]. (8)

Fresh means a distinct fragment prospectively prepared in that blank and
uncorrelated with the retained input. Reusing a correlated old fragment is
not iteration of (8). A sequence may be represented by independent unused
fragments in one larger initial state; preparation and outgoing correlations
remain in its ledger. No infinite fresh supply, free reset, thermostat or
irreversible limit is assumed by this finite candidate.

Nonzero epsilon_b and formation on evade the two particular proofs above;
they do not prove that (8) cools, mixes, obeys detailed balance or even fails
to be unital. Those properties must be derived from the actual completed map.
The existing BS coefficient domain permits epsilon_b>=0; choosing its value
or a pulse duration to match a desired response would not be a native prediction.

## Energy and source custody

For fixed epsilon_b,g_b and no other external source, the total work is

    W=integral dt u_dot(t)g_b <q_j tensor X_b>_t.

With sudden on/off switching this becomes W_on=g_b<K>_in and
W_off=-g_b<K>_out, K=q_j tensor X_b. At decoupled endpoints,

    Delta E_S+Delta E_b=W_on+W_off.                        (9)

For an independent blank input <K>_in=0; switch-off work need not vanish.
During a constant-coupling interval H_tot is conserved. If formation or other
couplings are externally changed, add their work; if switching is autonomous,
retain the controller energy instead of counting the same exchange twice.
Zero blank internal energy does not make blank preparation or disposal free.

The extension H_tot(a,eta) must separately assign fragment, copy, controller
and interaction energies to the adopted lapse and dilation sources. Neither
their spatial assignment nor their volume dependence is fixed by (7).
Different assignments are different physical completions. Source differentiation
must include every assigned term and contact, both end couplings and the
complementary propagator of the reviewed source-preservation construction.
For a source-dependent input, retained map or switching controller, retain
those derivatives too. Fixed-state held response and driven channel response
are distinct experiments; a source-dependent repeated map cannot be replaced
by a Kubo kernel with its environment response dropped.

## Prospective falsification and unresolved inputs

Before any execution, freeze the following missing boundary-completion inputs:
epsilon_b, g_b, u(t), Delta and the number/identity of supplied fragments;
their independent preparation and no-return assumption; attachment geometry;
complete source and controller dictionary; conserved sectors and admissible
input family; target readout age, frequency window, and numerical/error bounds.
Do not select a window or replace a state after observing its response sign.
BS10/12 and the existing pulses do not choose these inputs. This is presently
an UNINSTANTIATED candidate, not an execution-ready protocol or uniquely
predicted formation rule.

After completion, the smallest tests are:

1. Prove (3) in the copying-off control; recover the unforced closed H_S
   channel at g_b=0 and (6) at epsilon_b=0 in its stated invariant block.
   Preserve all old evidence.
2. Identify every conserved sector, fixed point and nondecaying source-visible
   mode of the actual channel before claiming an attractor. A remaining
   conserved population falsifies uniqueness across that population family,
   not legitimate sector-conditioned dynamics. A unital globally mixing
   result triggers the null-response control above, not a gravity promotion.
3. Evaluate the actual formed output with the complete energy/volume sources.
   For a proposed held stationary closure require [rho,H_S]=0, or a frozen
   bound on its source-visible aging over the claimed window. Retain the
   source work and correlations. A permitted weak cyclic source with negative
   net work beyond the declared error falsifies passivity in that source
   class; this is not inferred from one positive moment or from dephasing.
4. To claim a local low-frequency closure, bound the omitted source-dependent
   memory on the same window. A fixed point or a spectral gap by itself is
   not that bound. Growing-size locality, retained slow modes and uniform
   errors are later continuum obligations, not conclusions of one finite map.

No new physical flag is earned here. Native passive continuum, physical
source/clock/volume mapping, galaxy formation, observational superiority and
Stage 3 completion remain unestablished; all eleven mandatory lanes remain
open. The missing boundary completion blocks this proposed formation test,
not independent useful work elsewhere in the program.

## Read source identities

- `../recovered_sources/BS_MICRO_ACTION.md`, BS08–14a:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- `RECORD_ADDITION_PROTOCOL.md`:
  `2021e117b74d760cd3d731018cd91f3cba6ef92415beda9d951f9d6a42daff49`.
- `NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_PROTOCOL.md`:
  `724f8d8c4a7bbcc7ce4ba9fa37f750e92d96b732db78ef1cc1347fcd52a7a7d5`.
- `NATIVE_PHOTON_SOURCE_PATHWAY_V001.md`:
  `e6bdd502ae6e31c1bc318a49aea98f5db2c882e82143ca99d849587919fd4049`.
- `NATIVE_THERMAL_PACKET_MECHANISM_AND_PORT_TEST_V001.md`:
  `3fd418d5674018b7f115cce6b8bfe0b8fa0c5d1e82531e4cbcdf51c744396e65`.
- `NATIVE_ENERGY_SOURCE_PRESERVATION_V001.md`:
  `d0991dd4fd79b77ecb705f384c1b805d9923d132405a384c85168a98f4be1a2e`.

These identify the inspected premises. The new channel deductions above are
analytic results, not numerical or observational verification of a reservoir.
