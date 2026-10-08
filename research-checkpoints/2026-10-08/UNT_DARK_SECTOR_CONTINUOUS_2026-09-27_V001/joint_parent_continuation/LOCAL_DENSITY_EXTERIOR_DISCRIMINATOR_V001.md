# A restricted exterior test of the density dependent gravity hypothesis

2026-09-30. This analytic discriminator addresses the user's hypothesis that
the network responds differently in a galaxy's sparse outskirts. It does
not assume that records are an extra gravitating substance. Its conclusion
is limited but useful: in the specific local constitutive model below,
dependence on ordinary matter density alone cannot sustain a flat rotation
curve outside a compact source. A network state, field strength, gradient
or history dependence remains possible and needs its own formation law.
This is a necessary-condition test, not a galaxy fit or a new UNT derivation.

## The restricted model and its exterior solution

Assume a static spherical baryonic source of total mass M_b, with density
rho_b(r)=0 for r>R_b, no external field, and the following phenomenological
field and test-particle laws:

    div[mu(chi) grad Phi] = 4 pi G rho_b,
    chi = rho_b/rho_star,
    acceleration = -grad Phi,
    v_c^2 = r g,                 g = dPhi/dr > 0.

Here mu is dimensionless, rho_star is fixed, and G is fixed by the chosen
dense-regime calibration. Assume a regular central solution and no extra
singular source, so spherical flux integration gives

    r^2 mu(chi(r)) g(r) = G M_b(<r).

For every r>R_b, chi=0. If 0<mu(0)<infinity, the exact exterior is

    g(r) = G M_b / [mu(0) r^2],
    v_c^2(r) = G M_b / [mu(0) r].

A lower positive mu(0) enhances the normalization but does not change the
inverse-square acceleration falloff. Setting mu(0)=0 instead makes the
exterior flux zero for every finite g and is incompatible with M_b>0 in
this class; it does not supply a regular flat-curve solution. Singular,
distributional, negative-mu or otherwise different equations are outside
the stated assumptions, not established alternatives.

Real galaxies need not have exactly compact matter support or spherical
geometry. This theorem does not exclude finite radial windows in a
noncompact density profile, nor all theories that use density. It exposes
an elementary failure mode before a large fit: a constant exterior state
cannot change the radial power in this particular flux law. Replacing zero
density by a uniform background contrast leads to the same conclusion
only if the appropriately subtracted field equation has this same form.
It is not a derivation of a cosmological boundary prescription.

## What an independent network state would have to supply

Now allow chi to be a dimensionless network state that need not vanish
when local baryons do. Keep the same spherical field and test-particle
laws solely for this diagnostic. A flat circular speed satisfying the
target normalization v_flat^4=G M_b a_0 would require

    g_target(r) = sqrt(G M_b a_0)/r,
    mu_required(r) = sqrt(G M_b/a_0)/r.

Both the radial scaling and the mass normalization are necessary. For an
illustrative power-law state and response over a finite exterior window,

    chi(r,M_b) = A(M_b) (r/r_star)^(-n),
    mu(chi) = C chi^beta,

where C, beta and r_star are the same for all sources, the necessary
conditions are

    n beta = 1,
    C A(M_b)^beta r_star = sqrt(G M_b/a_0).

Thus A(M_b)^beta must scale as sqrt(M_b), not arbitrarily with galaxy age,
accumulated record count or source mass. If beta is fixed and nonzero,
A(M_b) is proportional to M_b^(1/(2 beta)). These equations are an inverse
target for testing a separately formed state; choosing A, n or C to enforce
them would be a fit, not an explanation. No values are assigned here. The
same limitation applies to inserting an archive profile by hand.

The distinction from ordinary local density is substantive. An acceleration
dependent coefficient mu(g/a_0) can vary in a baryon-free exterior because
the gravitational field is not zero there. Bekenstein and Milgrom's
nonrelativistic action gives such a modified Poisson equation; in spherical
symmetry its low-acceleration limit yields the mass-dependent flat-speed
relation. It also illustrates why MOND should not be dismissed as a
nonconserving curve fit. It does not derive UNT's source operator, state,
or a_0. See their [field equations and exterior solution, equations 3 and
6–8](https://adsabs.harvard.edu/pdf/1984ApJ...286....7B).

## Consequence for the current native program

This test neither establishes nor rejects the broader UNT hypothesis. It
rules out the narrower substitution chi=rho_b/rho_star as a sufficient
exterior mechanism within the stated flux model. A retained network
configuration could in principle provide a varying chi outside the matter,
but the current program must derive that configuration and its response
from the same physical source, clock, volume and formation rules. A count
of low-energy modes is not enough; the complete source must couple to them.

The current native shared-work discriminator and energy-dipole bridge
remain prerequisite checks. They require source contacts, transported
state and support energy, and do not yet supply this continuum field law.
Even a successful radial condition above would leave metric lensing,
expansion stress, stability, formation and the other mandatory Stage 3
tests open. In particular, no statement about cosmic negative pressure
follows from an outer-galaxy density change alone.

Local evidence read: NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md, section 6;
NATIVE_SHARED_WORK_INTEGRABILITY_V001.md and its independent review;
COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md, the qualified zero-response
branch discussion. This note adds no numerical worker, fitted parameter,
physical promotion or change to the sealed V003 handoff.
