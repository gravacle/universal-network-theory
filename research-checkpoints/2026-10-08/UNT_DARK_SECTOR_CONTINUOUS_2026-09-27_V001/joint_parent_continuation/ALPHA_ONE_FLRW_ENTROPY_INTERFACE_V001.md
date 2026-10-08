# Alpha-one transport: conserved polarization entropy and linear growth

2026-09-29. Analytical consequence of the explicitly **conditional** alpha=1
relative-phase transport completion. No operator is adopted as native UNT,
no initial state is selected, and no fit, propagation or CMB calculation is
performed. This is a leading linear interface of the declared averaged
parent, not an all-orders identity for the truncated spatial operator.

The reviewed sources are `NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md`
(SHA-256 `6e9cc504ae81841c55d73c84f91239ce407e84455f11efc10a32ed8724d4b45a`)
and `FINITE_GAP_FLRW_PRESSURE_CLOCK_INTERFACE_V001.md`
(`a8d0c3773eb3f95d5920e3ba7c83822c1af6ae1d0c72b8ec36cb533eb9ba6f94`).
Their positive-action, slow-hard-source, phase-averaging, finite-band and
background-state assumptions remain in force. Ordinary species retain
their own equations and initial conditions.

## 1. A conserved, gauge-invariant amplitude

Use Newtonian-gauge/Bardeen potentials Phi and Psi, a nonzero comoving wave
number k, p=k/a, T=t+pi and delta theta=omega(t)V. Set

    n_H=C beta I,   W=rho_H+p_H=n_H omega,
    cI2=I e0,II/omega,   d=delta I/I=delta rho_H/W,
    U=Phi-pi_dot,   S=b^T x,
    Pcal=C[S+KH(t) p U].                              (1)

The homogeneous relations are I_dot=-3HI,
rho_H_dot=-3HW, p_H_dot=-3H cI2 W and
W_dot=-3H(1+cI2)W. No constancy of cI2, omega or KH is imposed.

At alpha=1 the full retained clock equation is

    Pcal_dot+2H Pcal=0.

Consequently, with a fixed normalization of a,

    Q_k=a^2 Pcal = constant,
    sigma_k=p Pcal=k Q_k/a^3,
    epsilon_k=sigma_k/n_H = constant.                 (2)

The physical polarization density is **minus** sigma. Its background is
zero. The acceleration and mode polarization also vanish in the background,
so Pcal, sigma and epsilon are first-order gauge-invariant variables. The
constant epsilon is a convenient normalization by the conserved hard action
density, not an independently introduced matter abundance. In contrast,
sigma/W is generally not constant: its derivative is 3H cI2 sigma/W.

Time-dependent KH does not spoil (2): the conserved quantity is the complete
S+KH pU, not any of its pieces separately. Zero initial Pcal stays zero
under the linear equations, including in the presence of ordinary metric
forcing. This is an invariant initial-data branch, not a preparation law.
The homogeneous k=0 perturbation problem is not obtained by dividing (1)
by p and requires its separate constraints.

## 2. Closed metric and structure-growth interface

The hard action/current equations now are

    d_dot=3Psi_dot-p^2 V,
    V_dot=Phi+cI2(d+3HV).                             (3)

The total excitation-plus-polarization stress is

    delta rho_D=Wd-sigma,
    delta p_D=cI2 Wd=cI2(delta rho_D+sigma),
    delta T_D^0_i=-W partial_i V,
    delta anisotropic stress_D=0.                    (4)

Equations (2)-(4), the unmodified Einstein constraints/evolution, and the
ordinary species equations are a closed linear metric interface. In
particular,

    delta rho_D_dot+3H(delta rho_D+delta p_D)
                                  =W(3Psi_dot-p^2 V). (5)

For rho_H>0, write w=p_H/rho_H and delta_D=delta rho_D/rho_H,
leaving the homogeneous vacuum coefficient separate. An explicit form
suited to a growth/transfer calculation is

    delta_D_dot=-3H(cI2-w)delta_D
                  +(1+w)(3Psi_dot-p^2 V)
                  -3H cI2 sigma/rho_H,
    V_dot=Phi+3H cI2 V
                  +cI2[delta_D/(1+w)+sigma/W],
    sigma_dot=-3H sigma.                             (6)

These first-order equations retain all background time dependence; a
second-order growth equation must not discard derivatives of cI2 or w.
There is no replacement of G by G/mu. Radiation, scattering, neutrino stress
or other ordinary physics enter through their own stress/transport system.
In particular, ordinary anisotropic stress can give Phi different from Psi.
The equations do not supply a photon origin, a CMB spectrum or a physical
wave-number cutoff.

## 3. Exact entropy interpretation and the barotropic branch

The background adiabatic derivative of the mode-plus-constant-vacuum sector
is cI2. Its gauge-invariant intrinsic nonadiabatic pressure is exactly

    delta p_nad,D=delta p_D-cI2 delta rho_D=cI2 sigma. (7)

Equivalently, Delta_D_com=delta rho_D+3HWV obeys
delta p_D_com=cI2(Delta_D_com+sigma). Thus a nonzero Q is a conserved
polarization-density seed with an evolving pressure effect. It is not
ordinary barotropic-fluid initial data merely because its density scales
as a^-3. Nor is it a separately positive-background dust species: its
signed density has zero background and its momentum/pressure vanish at
this order. The usual two-fluid relative-entropy formula that divides by
each background enthalpy cannot be applied to it.

For example, one can initially compensate the density by choosing
delta rho_H=sigma, so delta rho_D=0. At finite cI2 its pressure is still
cI2 sigma. Without additional specified compensation this is an
isocurvature seed that subsequently sources the metric, not a permanently
invisible density rearrangement. More generally, for the total stress
including ordinary species and constant vacuum,

    zeta_tot=-Psi+delta rho_tot/[3(rho_tot+p_tot)],
    zeta_tot_dot=-H delta p_nad,tot/(rho_tot+p_tot)
                                      -p^2 V_tot/3, (8)

where total momentum is -(rho_tot+p_tot) grad V_tot. The term cI2 sigma
contributes to delta p_nad,tot along with ordinary intrinsic and relative
entropy; it must not replace those other terms. On sufficiently long
wavelengths it can source curvature even though Q itself is conserved.

On the actual Q=0 branch, (4)-(6) are precisely the ordinary irrotational
barotropic-fluid linear metric equations for the **same** e0(I), background
density, pressure and initial density/velocity. This statement allows
arbitrary separately conserved ordinary species and time-dependent cI2.
It does not require removing the contact/memory sector. Alternatively, in
the strictly pressureless cI2=0 limit, even nonzero Q can be absorbed into
the initial total dust density perturbation for the linear metric problem.
Neither equivalence is a claim that the required state, spectrum or
transport coefficient has been supplied by native formation.

## 4. Nonzero internal modes can remain linearly invisible

Keeping KH(t)>0, Ms, Ks and b as in the retained finite-band parent, eliminate
U using (1). The exact remaining linear equations are

    Ms(x_ddot+3H x_dot)+[Ks+b b^T/KH(t)]x
                                      =b Pcal/[C KH(t)],
    pi_dot=Phi-Pcal/[C KH(t)p]+S/[KH(t)p].            (9)

Thus the system is triangular: Q and the hard/ordinary metric system fix
the forcing; the soft modes and clock may then be reconstructed. On Q=0,

    Ms(x_ddot+3H x_dot)+[Ks+b b^T/KH(t)]x=0,
    pi_dot=Phi+S/[KH(t)p].                          (10)

Consistent nonzero x, x_dot and pi initial data can therefore remain with
zero *combined linear* polarization stress. They need not satisfy S=0
and they do not require pi=V. Metric forcing changes pi through Phi but
cancels out of U=-S/(KH p); it does not regenerate Q. Enforcing (9) or
(10) continuously includes the KH time dependence automatically, rather
than treating KH as fixed when differentiating the original definition.

For positive Ms, Ks and KH the instantaneous stiffness in (10) is positive.
That observation is not a global, nonlinear or parametric-stability proof:
time dependence, validity of averaging, and finite-amplitude clock
regularity still require their own tests. These modes also carry quadratic
energy/stress, so linear invisibility does not remove their work or
backreaction at higher order. The all-orders square-root phase completion
and the isolated quadratic alpha operator are not interchangeable there.

The constructive conclusion is exact but conditional: alpha=1 removes the
linear hard-to-clock entropy production, leaving one conserved entropy
amplitude and a well-defined Q=0 fluid metric branch. It does not require
setting every internal degree of freedom to zero, and it does not establish
native coefficient matching or empirical cosmological success.
