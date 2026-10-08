# Active native formation: exact onset and a finite-window error bound

2026-09-30 local / 2026-10-01 UTC. Source-only calculation, for independent
review. No trajectory, microscopic coefficient, favorable age, physical
source deformation or cosmological preparation is selected. This concerns
the actual BS08–11 copy operators with both record-writing routes retained.

## Conditional domain, not an unannounced preparation

Fix a finite slab, a single content x, individually fixed writer basis
states B or x, and a fixed total carrier count P. All other content states
are absent from this sector. Retain every incidence qubit and every record
and finite reservoir register. Write p_v for carrier occupation, r_v for
record occupation, b_vk for fragment occupation, and w_v=0 or1 for the
fixed writer label. Reservoir labels k are not a wave number here.

For this analytical onset question only, take every incidence, record and
fragment initially blank and let the carriers have any density matrix in
the specified fixed-P sector. The pure blank factors preclude hidden initial
correlations with them. Writer values, P and coefficients remain symbols;
this conditional family is not claimed to be a derived cosmological state.
It is not the already evolved 16D preparation, nor the old N=2 held 64D
incidence/carrier experiment. No fresh-fragment sequence or reset is added.

Use the time-independent ports-off native Hamiltonian, with all storage,
degree, feedback, current-square and carrier energies retained. Define

    G_v = g_psi_r p_v + g_wr w_v I.

The exact record-target terms in this sector are G_v X_rv; the fragment
terms are g_rbk r_v X_bvk. X swaps B and x. The copy control is not consumed.
This is a restriction of the original operators, not a replacement rate law.
Nonpreserving ports or additional content require a larger sector.

## Leading amplitudes without a chosen age

Let Pi0 project onto the conditional blank factors with unrestricted carrier
state and let rho0=Pi0 rho0 Pi0. The original finite matrices give

    r_v H Pi0 = G_v X_rv Pi0,
    b_vk H Pi0 = 0,
    b_vk H^2 Pi0 = g_rbk G_v X_bvk X_rv Pi0.             (1)

In the last identity only the order record-write then fragment-write
survives. Blank-gated carrier hopping, diagonal energy and feedback terms
cannot replace either of these two target changes. Incidence creation can
occur at first order but cannot produce a fragment in just two actions.
Consequently, for each fixed finite system,

    <r_v>_tau = tau^2 <G_v^2>_0 / hbar^2 + O(tau^3),
    <b_vk>_tau = tau^4 g_rbk^2 <G_v^2>_0/(4 hbar^4)
                                                       + O(tau^5). (2)

For real initial density in the native real basis both occupations are
even in tau, improving the respective remainder orders to four and six.
The generic bounds below do not rely on reality or a chosen sign.

Since p_v and w_v are binary,

    <G_v^2>_0 = (g_psi_r^2 + 2 g_psi_r g_wr w_v)<p_v>_0
                                                   + g_wr^2 w_v. (3)

The two same-content writing amplitudes interfere. An independent-rate sum
g_psi_r^2<p_v> + g_wr^2 w_v omits the cross term. This is coherent interference
of two Hamiltonian pathways, not a superposition of writer contents or a
claimed loophole in the prior coherent-writer unitality result. Either
constructive or destructive signs are possible for the allowed real
couplings; a zero coefficient is retained, not removed from the census.
For all writers occupied and homogeneous couplings, summing (3) over m nodes
gives m g_wr^2 + P(g_psi_r^2+2 g_psi_r g_wr). Local spatial predictions still
depend on the actual carrier preparation and later joint correlations.

## Explicit finite-window control

Let K=H-cI for any declared real scalar c and take kappa >= ||K||. This is
only centering for an error bound: the physical H, all absolute energies and
all source derivatives remain intact. The exact occupations are unchanged
by its common phase. Set z=kappa*|tau|/hbar. Hermiticity gives the integral
Taylor remainders

    ||exp(-iK tau/hbar)-I+iK tau/hbar|| <= z^2/2,
    ||exp(-iK tau/hbar)-I+iK tau/hbar
                         +(K tau/hbar)^2/2|| <= z^3/6. (4)

The bound uses the unit norm of the unitary integral kernel; it needs no
exponential prefactor. Centering leaves all leading projections in (1)
unchanged, since b_vk Pi0=b_vk H Pi0=r_v Pi0=0. Define

    a_r = |tau| sqrt(<G_v^2>_0)/hbar,      e_r=z^2/2,
    a_b = tau^2 |g_rbk| sqrt(<G_v^2>_0)/(2 hbar^2),
    e_b=z^3/6.

Applying (4) to r_v U sqrt(rho0) and b_vk U sqrt(rho0), using the
Hilbert–Schmidt norm and ||sqrt(rho0)||_HS=1, gives absolute controls

    |<r_v>_tau-a_r^2| <= 2 a_r e_r+e_r^2,
    |<b_vk>_tau-a_b^2| <= 2 a_b e_b+e_b^2.              (5)

These hold for mixed and coherent carrier states and include cases with
vanishing leading amplitudes. They are not relative-error guarantees for
tiny populations. A finite upper norm bound can be obtained term by term
from the actual finite Hamiltonian; no numerical value is selected here.
Its size dependence matters. These are not uniform large-system/long-time
formation or transport guarantees.

## Scientific consequence and limits

Equations (1)–(5) supply source-derived controls for a formation-inclusive
native model. They explicitly retain which process writes a record and
which process copies it into finite storage; they do not turn retained
records into an extra gravitational substance. Subsequent dynamics requires
carrier/record/incidence/fragment correlations, not these counts alone.
The initial onset does not establish monotonic accumulation, permanent
records, cooling, a passive state, an attractor or a gravitational response.
Complete fixed-H energy is conserved; any later switching needs its own
work and controller ledger. No volume/metric/clock conversion is derived.

The next mathematical test is an exact formation-inclusive sector embedding
that preserves H and every specified source insertion, before discarding
any of these registers. A numerical run would require a separate frozen
preparation and bounded protocol; none is authorized or executed by this
analytical note. All eleven program lanes remain OPEN.

Source: `../recovered_sources/BS_MICRO_ACTION.md`, BS07–12, SHA-256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
Existing conservation/current identities are in `NATIVE_TEMPORAL_KERNEL.md`;
the earlier writer-only invariant block is in `RECORD_ADDITION_PROTOCOL.md`;
held-copy and fragment-channel limits remain in
`NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md`. Their results are not new
discoveries in this note and their assumptions are not silently changed.
