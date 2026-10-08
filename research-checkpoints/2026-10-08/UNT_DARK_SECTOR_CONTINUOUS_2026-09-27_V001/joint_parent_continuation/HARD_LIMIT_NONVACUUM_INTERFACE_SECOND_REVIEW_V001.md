# Independent parent-to-stress review of the hard-limit interface

2026-09-29. Complete analytical source read; no numerical worker or new
preparation. Reviewed `HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md`, SHA-256
`c501fc2aeebe0cf389ad9c21c5c7fdd3240209a1d9dd0ae710ed45d67bb8003d`.
The focus is its covariant parent, hard action normalization, stress and total
metric interpretation; this is not a duplicate certification of the entire
finite-band clock stability calculation.

**Accepted for the expressly declared leading phase-averaged hard-limit
action and its linear scalar sector.**

## 1. Action and state

For e=Omega I-kappa h^2/2, the inherited phase action
C beta[I u.dtheta-e], theta=Omega phi, becomes precisely

    rho(u.dphi-1)+C KH h^2/2,
    rho=C beta Omega I,  KH=kappa beta.

The source contact has a plus sign in the Lagrangian and is independent of
the retained excitation abundance. Splitting beta into two weights beta/2
does not double either term. Opposite phases may share the slow phi with
fixed phase offsets at this leading order; additional evolving phase or
orientation degrees of freedom are not eliminated by this notation.

The separate paired-state review checks its exact finite-R algebra. It is
a new two-copy state space and a new preparation, not a conversion of the
saved common pulse. Pairing cancels B and Bdot at zero source, but leaves
oscillatory quadratic/quartic stress. The stated rapid-phase, isotropic or
equal-axis and controlled metric/clock averaging assumptions are material.
At finite source the collective response and finite-R couplings survive.

## 2. Normalized-clock variation, independently checked

Hold T and phi fixed in an inverse-metric variation. For
u_mu=-T_mu/X and X=sqrt(-g^{ab}T_a T_b),

    delta u^mu = u_nu delta g^{mu nu}
                 +(u^mu/2)u_alpha u_beta delta g^{alpha beta}.

Varying rho gives u.dphi=1. With s_mu=P_mu^nu partial_nu phi,
the on-shell density term then has

    T_mu nu = rho u_mu u_nu-2rho u_(mu s_nu).

Its normal-frame energy is rho, its energy flux is -rho s_mu, and its
spatial stress vanishes. Independently varying T gives
div[(rho/X)P^{mu nu}partial_mu phi], with the sign in equation (5).
Variation of phi gives div(rho u)=0. Treating u as an independently varied
dust velocity would lose this relative flux and change the clock equation.
The acceleration contact and soft-mode stresses remain additional terms;
equation (6) is correctly identified as the density term alone.

## 3. Linear metric and current closure

In Newtonian gauge the normal velocity is -grad(pi)/a and
s_i=partial_i(V-pi) to first order. The hard energy current is therefore

    -rho grad(pi)/a-rho grad(V-pi)/a=-rho grad(V)/a.

The contact and soft polarization are quadratic about the zero-acceleration,
zero-soft-field background: their linear source contribution is the signed
density -p Pcal, with no additional first-order pressure or momentum.
The displayed lapse/shift constraints consequently give

    Psi_dot+H Phi=rho V/(2Mpl2),
    delta_rho_N=-3H rho V-2Mpl2 p^2 Psi+p Pcal.

Adding delta_rho_pol=-p Pcal yields exactly equation (15), not a rescaled
Newton constant. The hard current equation gives
delta_N_dot=3Psi_dot-p^2 pi, while
(delta_rho_pol/rho)_dot=-p^2(V-pi). Their sum is the stated total dust
continuity equation. These signs also verify the compensated-density
interpretation without deleting either density contribution.

The single-component Rc identity follows directly from
zeta_dot-H v_dot=Hdot v; its restriction when adding independent baryon
relative modes is appropriate. Minimally coupled pressureless baryons add
their own density and momentum, while photon pressure and anisotropic
stress require separate equations. No acoustic/CMB result follows from
the pressureless reduction alone.

The total linear metric equivalence does not identify the nonlinear parent
with ordinary dust: the normalized-clock sector, its initial data, the
relative flux, and the retained contact remain. Nor does the reduction
prove that averaging commutes with the full fast lapse/clock constraints.
The note expressly retains these qualifications and does not reassign the
saved coherent pulse to the new pair sector.
