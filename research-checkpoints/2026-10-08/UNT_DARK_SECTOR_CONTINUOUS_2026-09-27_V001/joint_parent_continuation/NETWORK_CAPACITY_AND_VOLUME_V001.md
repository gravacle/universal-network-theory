# Network interaction capacity and physical volume

2026-10-03. Constructive continuation following the user's request for a
fresh perspective. The useful hypothesis is that gravity changes because
the network's interaction capacity changes, not because stored records
constitute an invisible mass halo. This note derives a concrete coarse
model, its environmental discriminator and the physical-volume equation
still needed to unify it with expansion. No new numerical run is required.

## A capacity mechanism for the galaxy scaling

Let J be a conserved flux with div J=4 pi G rho_b, and k>=0 the local
dimensionless interaction capacity. On an adopted fixed physical geometry,
consider the convex dual functional

    E[J,k] = (1/4 pi G) integral dV
             [ |J|^2/(2k) + a0^2 k^3/6 ].

The first term is the cost of carrying a flux; the second retains the cost
of building capacity. With fixed source flux, varying k gives

    k=sqrt(|J|/a0),  g=partial_J integrand=J/k,
    J=(|g|/a0)g.

The minimized dual density is (2/3)sqrt(a0)|J|^(3/2); its Legendre
potential is |g|^3/(3a0). This is the deep AQUAL response and yields the
BTFR mass dependence through spherical Gauss flux. It is not a linear
two-dimensional Green function: such a Green function would give a
logarithmic potential with amplitude proportional to M, rather than sqrt(M).

This is a mathematical constitutive construction, not an identified native
Hamiltonian or proof that its positive dual functional is the entire
relativistic energy. In particular, the cubic capacity cost is a hypothesis.
For a general cost C(k), stationarity requires C'(k)=g^2/2; the desired
k=g/a0 specifically requires C=a0^2 k^3/6 plus a constant. Naming capacity
connectivity does not derive this exponent or its absolute constant.

A hard bound k<=1 would recover a piecewise Newtonian high-field branch,
but its transition is a new model assumption, not adopted here as a fit.
The earlier source-coupled soft-spectrum construction already supplies a
different smooth completion. Its requirements are preserved in
SOFT_SPECTRUM_ROTATION_SELECTOR.md: a constant weighted density of small
positive stiffness eigenvalues, appropriate source overlaps, quartic
stabilization and an accessible prepared-state window. Merely counting
graph eigenvalues or declaring physical space two dimensional is insufficient.

## A discriminating environmental prediction

For an internal field much smaller than a uniform external field g_e, both
in the deep regime, the SAME vector constitutive law linearizes to

    delta J = (g_e/a0) [I + e_hat e_hat] delta g,
    div{ (g_e/a0)[I+e_hat e_hat] grad phi_internal }=4 pi G rho_b.

It predicts a response linear in internal source mass, effective strength
proportional to a0/g_e, and longitudinal-to-transverse stiffness ratio2.
The isolated sqrt(M) regime must therefore change in a specified external
environment. This is a concrete observable consequence, not a separate
halo assigned to each environment. It distinguishes this constitutive model
from a fixed linear graph propagator or a scalar spherical enhancement.
It does NOT distinguish it from existing theories with the same deep AQUAL
law; independent evidence for UNT still needs its native capacity dynamics
or a further predicted departure. No external-field observations are scored
or claimed unused in this note.

## Why capacity cannot simply be renamed volume

Test the tempting one-variable identification explicitly. Let an isotropic
physical metric have spatial dilation ell=s relative to a fixed reference
chart. Then dV=s^3 dV0, g_phys=g0/s and J_phys=J0/s^2, where J0 is the
conserved reference-area flux. The reference expression

    integral dV0 [J0^2/(2s)+a0^2 s^3/6]

is EXACTLY integral dV [J_phys^2/2+a0^2/6]. Thus its physical constitutive
law is linear, g_phys=J_phys. One cannot eliminate s using reference
gradients, then call those gradients and distances physical and retain
the earlier BTFR derivation. At the flux-balanced reference stationary
point, g_phys=J_phys=a0; it is not a weak-field family.

If the constant volume term alone were promoted to physical mass density
a0^2/(24 pi G c^2), Einstein coupling would give Hv=a0/(3c). This is only
the consequence of that additional energy/gravity assignment. It does not
rescue the lost galaxy law, establish a native vacuum, or permit omission
of transport, curvature, source and boundary work.

The broader ansatz ell=s^p makes the accounting more visible. With a fixed
material-cell inventory, partial variation of the same reference energy
at fixed J0 gives |J0|=a0 s^2 and k_phys=s^(1-p). The pure cost has
E_cost proportional to s^3, V proportional to s^(3p), and w_cost=-1/p.
But at this same stationary point E_transport=3E_cost: its pressure
E_transport/(3pV) cancels -E_cost/(pV) exactly. Total stationary pressure
is zero, not the negative pressure of the isolated cost term. At zero
homogeneous flux the unconstrained energy instead minimizes at s=0.
A populated expanding state requires a dynamical or constraint equation.

There is a separate geometric test. For a spherical reference exterior,
J0=GM/r0^2 gives s=r_M/r0, r_M=sqrt(GM/a0). Its areal and proper radii obey

    R=s^p r0,  dl=s^p dr0,
    dR/dl=1-p,  spatial_scalar_curvature=2p(2-p)/R^2.

p near1, suggested by w_cost near-1, produces strong spatial geometry;
p=1 is a constant-areal-radius cylinder. p=2 is a coordinate inversion
that swaps the usual source center and infinity, not an ordinary exterior.
For p<1, weak-lapse circular balance also gives
v_c^4=GMa0/(1-p)^2. Ignoring this ruler factor incorrectly preserves the
flat-space normalization. These restrictions apply to this specified
isotropic identification and partial energy, not every network geometry.

## Constructive continuation

Keep capacity k and dilation s as DISTINCT properties of the same network,
not distinct substances. The consistently transformed functional is

    integral dV0 [ J0^2/(2ks) + a0^2 k^3 s^3/6 ]
      = integral dV [ J_phys^2/(2k) + a0^2 k^3/6 ].

Varying k at fixed physical geometry recovers the physical deep galaxy law.
Homogeneous zero-flux equilibrium gives k=0, so a nonzero cosmic state is
not fixed by static minimization. The missing bridge is now specific:
the joint capacity-volume evolution in a physical clock, with its energy
supply, metric/source variations and initial state retained. An arbitrary
k(t), a chosen k=1, or an added volume term would count as extra freedom.
The dual static functional alone must not be promoted to a Lorentzian
action without checking the Legendre signs and gravitational constraints.

The shortest useful native calculation would determine that specific
capacity cost or capacity-volume response and thereby change a named
galaxy/environment or expansion prediction. It is not another general
fixed-graph consistency test. Existing active-memory results remain valid;
their phase/work response is not assumed to relax to this convex minimum.

These new algebraic transformations and pressure/ruler checks were worked
through with an independent internal reviewer. They motivate a definite
network mechanism while exposing the physical mapping that still needs
proof. No observational success, Stage 3 closure or superiority is claimed.
