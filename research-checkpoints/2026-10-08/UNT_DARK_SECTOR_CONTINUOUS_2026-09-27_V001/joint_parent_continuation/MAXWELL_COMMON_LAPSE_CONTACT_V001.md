# Common-lapse Maxwell source and exact reduced contact V001

2026-10-05 UTC. New analytical result, reviewed within the current local
continuation. This file was explicitly assigned to readonly_science_review
by the root agent. No scientific numerical worker was launched and no
numerical receipt, script or result file is claimed. Numerical worker:
UNSTARTED. All older reports and failed attempts remain intact.

## Physical source and accounting

Use one minimally coupled particle/Maxwell action, with actual material
constraints, supports and reference terms included in that same action.
For a static metric

    ds^2 = -N(x)^2 c^2 dt^2 + gamma_ij dx^i dx^j,

keep the spatial metric, domain and charge inventory fixed for the source
derivative. Freeze the source chart N=1+b f(x), with N positive. For a
physical acceleration component b along x, the weak source is f=x/c^2;
the origin and support/boundary conditions are part of the protocol.
For the existing dimensionless chart theta=b ell/(2c^2), the corresponding
lapse profile is N=1+theta*(2x/ell), rather than an unspecified source
contact. This is a physical-source proposal, not adoption of the native
phase/clock/metric dictionary.

The full canonical minimally coupled Hamiltonian is affine in N at fixed
canonical fields, spatial metric and constraints:

    H[N] = integral N H_density dV + constraint terms.

Its direct second lapse derivative is zero. A constant lapse rescales the
complete Hamiltonian and coordinate time: for a stationary eigenstate,
H'=f H, H''=0 and E''=0 when f is spatially constant. This uniform-lapse
identity does not impose unit gravitational susceptibility. A different
source chart, such as N=sqrt(1+2b f), has its own fixed kinematic N'' term
and must not be interchanged after seeing a result.

Each actual constituent rest energy couples as mc^2 N. An actual constant
energy per material cell couples at that cell and has dust-like volume
accounting; it is not automatically a constant vacuum energy density.
Physical support/reference energy must retain its own source and stress.
A degree-rezeroed identity is insufficient to determine those couplings.
Count the global Maxwell energy once: pair Coulomb energy and its already
represented Maxwell field energy must not be added as independent sectors.

## Continuum reduced electrostatic contact

For fixed charge density rho_q and fixed spatial geometry, eliminating the
electrostatic constrained field gives, in flat spatial notation,

    L_N = -epsilon0 div(N^-1 grad),
    phi = L_N^-1 rho_q,
    U_N = (1/2) <rho_q, L_N^-1 rho_q>.

Use an invertible grounded problem or a neutral quotient with the gauge
zero mode removed. Curved spatial geometry uses its proper measure and
covariant divergence. At N=1,

    L'  = +epsilon0 div(f grad),
    L'' = -2 epsilon0 div(f^2 grad),
    U'  = -(1/2)<phi,L'phi>
        = (epsilon0/2) integral f |grad phi|^2 dV,
    U'' = <L'phi,L_0^-1 L'phi> -(1/2)<phi,L''phi>.

These are derivatives of the reduced Coulomb Hamiltonian. The second term
and Green return already include redistribution of the eliminated Maxwell
sector. Do not then count that same redistribution a second time as
separate Maxwell relaxation or spectral poles.

## Exact positive-graph theorem

This finite-domain theorem supplies a transparent source/contact check
without choosing any critical cancellation or numerical tolerance. Let D
be edge-by-node incidence, fixed r_e>0, C=diag(1/r_e), and

    R_e(b)=r_e(1+b f_e),
    L(b)=D^T diag(1/R_e(b)) D,
    phi=L(0)^-1 q, U(b)=(1/2)q^T L(b)^-1 q.

All retained R_e must stay positive. The inverse again means a grounded
problem or the neutral gauge quotient. This is the Thomson minimum

    U(b)=min_{D^T j=q} (1/2) sum_e R_e(b) j_e^2.

Put

    v=C^(1/2) D phi,
    F=diag(f_e),
    Pi=C^(1/2) D L(0)^-1 D^T C^(1/2).

Pi is the orthogonal projector onto weighted potential gradients. Since

    L'=-D^T C F D, L''=2D^T C F^2 D,
    2U=v^T v,

the exact source derivatives are

    U' =(1/2) v^T F v,
    U''=||Pi Fv||^2-||Fv||^2
        =-||(I-Pi)Fv||^2 <= 0,
    |U''| <= 2U max_e(f_e^2).

Uniform f gives U''=0 because v is already in the projected space.
Every connected tree has U''=0 for arbitrary f: its charge-constrained
edge flux is unique. A cycle or chord is required for a nonuniform-source
redistribution test. A cycle can still give zero when Fv happens to remain
a weighted gradient. Nonpositive curvature is therefore a relaxation
identity, not evidence that every source profile has a nonzero effect.

For physical f_e=x_e/c^2 and cell volume V, the existing normalization
P=-4piG E_b/V gives this Maxwell-sector bound

    0 <= chi_Maxwell=-4piG U_bb/V
       <= 8piG U x_max^2/(V c^4).

U here is the complete positive Maxwell field energy for the declared
finite system. A signed cross-pair energy, a selected subset of pairs, or
a degree-rezeroed term cannot replace U in this norm bound. The bound
applies only to the eliminated Maxwell sector; it does not bound separate
matter, support or material relaxation. Numerical calibration of chi=1
is neither performed nor implied.

## Retained matter response and common-action identities

For a specified nondegenerate reduced quantum ground branch,

    E_bb=<H_bb>-2 sum_{n>0}|<n|H_b|0>|^2/(E_n-E_0).

Only retained degrees appear in this sum. Frozen or driven/nonstationary
states require their own protocol and causal response. Positive-pole ground
passivity cannot be assigned to an arbitrary formed native state.

The complete on-shell action obeys covariant stress conservation, with
external support/source work included when a subsystem is clamped. On a
smooth shared energy branch at fixed bare G,

    p=-partial_V E, rho=E/V,
    partial_V(V P)=4piG partial_b p.

Pressure, source, clock and stress follow from the same action. These
identities do not select the old native critical contact, its volume
scaling, a deep-response law, a cosmic population, or an accelerating
expansion history. No observational or Stage 3 qualification follows.

Read anchors: FU_LOCAL_COULOMB_BORN_CONTACT_V001.md (in the parent directory),
KINETIC_COULOMB_SHARED_STRAIN_V001.md, KINETIC_COULOMB_BOND_RIGIDITY_V001.md,
UNT_SHARED_INTERACTION_RESEARCH_HYPOTHESIS_V001.md. The first fixes only a
local physical distance contact; this new theorem requires the global
field/domain source and preserves that distinction.

The root reports that the user's later steering permits at most two small
local workers. This note uses no numerical worker because the all-graph
proof is sufficient, not because that later allowance is unavailable.
No worker is currently owned or active under this note. Numerical
authentication remains optional: freeze a positive cycle graph, a tree/
uniform-source control, steps and tolerances before any future execution.

## Optional counted material-acceleration interaction

Minimal coupling alone does not supply the old critical cancellation. A
network with an owned physical material rest frame can admit a NEW
effective interaction, not derived here from ordinary Coulomb:

    S_lambda = integral sqrt(-g) lambda q_mu a^mu d^4x,
    a^mu = u^nu nabla_nu u^mu, q_mu u^mu = 0.

The material velocity u must be dynamic or derived from the material
coordinates, with its constraints, reference energy and stress owned.
The term requires physical matching of lambda and of the internal q
normalization. It is not a choice chi=1. An isolated freely falling
minimally coupled local cell has no invariant internal source from a
removable first metric gradient; a material frame/support or an additional
interaction is therefore a substantive premise.

In a static frame a_i=c^2 partial_i ln N and sqrt(-g)=N sqrt(gamma).
Consequently this interaction is affine in the lapse:

    H[N]=integral [N epsilon-lambda c^2 q.grad N] dV,
    H'_f=integral f[epsilon+c^2 div(lambda q)] dV,
    H''_f=0,

with the integrated boundary term explicitly owned. A proper local
potential W=K q^2/2, K>0, gives upon static elimination

    E_reduced = -lambda^2 |grad Phi|^2/(2K),
    Phi=c^2(N-1), chi=4piG lambda^2/K.

The derivative contact and this relaxation must not both be assigned to
the same eliminated q. Cosmic comoving FLRW has a^mu=0, so this coupling
alone does not provide cosmic acceleration. Complete W(0,B), physical
tension/reference energy and formation determine homogeneous stress. A
galaxy response derivative cannot fix an otherwise arbitrary vacuum
integration constant.

### Coupled kinetic and spatial-gradient gate (c=1)

Let h=rho+p>0 be COMPLETE solid inertia and I>0 internal q inertia. For
material displacement xi, a_i=xi_ddot_i+partial_i Phi to linear order.
Integration by parts changes lambda q.xi_ddot to -lambda q_dot.xi_dot.
The q.u constraint contributes no extra quadratic term. Thus the flat/
external-metric quadratic kinetic matrix is

    [[h,-lambda],[-lambda,I]],
    D=hI-lambda^2>0.

For a material longitudinal or transverse branch A=M or G, A>0, with
internal gradient energy kappa|grad q|^2/2, kappa>0, set Q=K+kappa k^2.
The exact coupled material dispersion is

    D omega^4-(hQ+I A k^2)omega^2+A k^2 Q=0,
    omega_+/-^2=[hQ+I A k^2
       +/- sqrt((hQ-I A k^2)^2+4lambda^2 A k^2 Q)]/(2D).

Both squared frequencies are positive for k nonzero under the above
conditions; the material translation is a zero mode at k=0. Define
a=A/h, d=kappa/I and zeta=lambda^2/(hI). High-k squared speeds are

    v_+/-^2=[a+d +/- sqrt((a-d)^2+4zeta a d)]/[2(1-zeta)].

Both speeds are at most the common light speed exactly when the principal
matrix kinetic-minus-spatial-stiffness is positive semidefinite:

    a<=1, d<=1, (1-a)(1-d)>=zeta.

Together with positive coefficients this is a concrete test, not a generic
stability assertion. The exact rational DEVELOPMENT control
a=d=1/4, zeta=1/4 has v_+^2=1/2 and v_-^2=1/6, away from kinetic
degeneracy. These values are not physical fits or native calibrations.

Critical static normalization K=4piG lambda^2 requires the CLAMPED bare
frequency Omega_0^2=K/I=4piG h zeta<4piG h. The free coupled k=0 pole is
instead Omega_dressed^2=K/(I-lambda^2/h)=4piG h zeta/(1-zeta); it can be
fast near zeta=1. Do not turn bare softness into an observable-pole no-go.
Near that limit kinetic degeneracy and perturbative control require their
own tests. Native_deformation_review independently checked these kinetic
signs, the quadratic constraint and bare/dressed distinction.

The same declared spatial stiffness makes static chi(k)=
4piG lambda^2/(K+kappa k^2). At critical normalization,

    mu(k)=1-chi(k)=kappa k^2/(K+kappa k^2)>0 for k nonzero.

The quadratic potential stiffness is k^2 mu(k)/(4piG). This is a spatially
dispersive k^4 long-wave response, not a derivation of a local MOND cubic.
Complete ordinary material work also includes -h psi div(xi), psi=deltaN;
its fixed-domain uniform mode vanishes, while finite-k compressional
relaxation gives E_psi_psi=-h^2/(K_bulk+4G_shear/3). Do not confuse this
potential response with the q gradient coupling. Full selfgravity,
metric constraints, stress/anisotropy, Jeans behavior and cosmological
formation remain untested. The dispersion above is only the controlled
material principal test in an external metric.

An actual tensile action supplies a conditional counterexample to a
blanket elastic-acceleration no-go: cold isotropic affine even-junction
membranes with fixed physical tension have E proportional to physical
area, hence w=-2/3, shear/energy=4/15, a_T=4/5 and a_L=2/5. Those values
come from [Battye et al., 2005](https://arxiv.org/abs/hep-th/0501244), which
explicitly leaves formation/freezing unresolved. With the new q action's
DEVELOPMENT values d=1/4 and zeta=1/10, the principal squared speeds are

    transverse: (21 +/- sqrt(153))/36,
    longitudinal: 1/2 and 2/9.

All lie strictly between zero and one, with critical K=4piG lambda^2
compatible and no kinetic near-degeneracy. This is an uncalibrated
effective-action control, not a wall interpretation adopted for UNT or
full stable gravity. Different anisotropic/non-affine lattices can have
different instabilities ([Battye et al., 2006](https://arxiv.org/abs/hep-th/0512207));
tested field-theory junction models approached scaling rather than frozen
frustration ([Avelino et al., 2006](https://arxiv.org/abs/astro-ph/0612444)).
Do not replace their formation problem with selected wall abundance.

Exact next scientific action: match this counted action's lambda, h, I,
K and kappa to the SAME physically normalized positive native poles and
stress, test both polarizations and finite-k response, and retain its
homogeneous W/reference source. The Maxwell projection theorem can be
used directly; no new scheduler, coordination mechanism or observational
qualification has been created.
