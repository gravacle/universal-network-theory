# Independent finite-gap FLRW interface review and local action check

2026-09-29. Analytical review only; no numerical evolution, new preparation,
observational fit or alteration of frozen evidence.

Reviewed in full:
`FINITE_GAP_FLRW_PRESSURE_CLOCK_INTERFACE_V001.md`, SHA-256
`a8d0c3773eb3f95d5920e3ba7c83822c1af6ae1d0c72b8ec36cb533eb9ba6f94`.

Result: accepted within its stated averaged-parent and state assumptions.
No mathematical correction was identified. The independent calculation below
also identifies a positive-kinetic, indefinite-potential realization of its
local growing branch. This is not a full-parent hyperbolicity theorem.

## 1. Independent stress, current and constraint checks

Write the hard phase action as

    C beta [I u.partial theta - e0(I)] + C KH(I) a^2/2,
    u_mu = -partial_mu T / sqrt(-partial T squared),
    omega=e0,I, W=C beta I omega, cI2=I e0,II/omega.

The normalized-gradient clock is held fixed under metric variation, rather
than replacing its normal by an independently varied ordinary-fluid velocity.
With s_mu=P_mu^nu partial_nu theta the phase stress is

    T_mu nu = W u_mu u_nu + p_H g_mu nu
                 - 2 C beta I u_(mu s_nu).

For theta=theta_bar+omega V and T=t+pi this gives momentum
delta T^0_i=-W partial_i V. Since omega_dot/omega=-3H cI2, the phase and
action-current equations are exactly

    V_dot = Phi + delta p_H/W + 3H cI2 V,
    (delta I/I)_dot = 3Psi_dot - kphys^2 pi.

The clock equation and the polarization stress, with the reviewed Fourier
sign convention, are

    Pcal_dot + 2H Pcal = W kphys (V-pi),
    delta rho_pol=-kphys Pcal,
    delta p_pol=delta T_pol^0_i=anisotropic stress_pol=0.

Consequently, for d_D=delta rho_H+delta rho_pol,

    d_D_dot+3H(d_D+delta p_H)=W(3Psi_dot-kphys^2 V),
    delta p_H=cI2(d_D+kphys Pcal).

These checks verify the enthalpy factor W, all pressure signs, and the
nonadiabatic term cI2*kphys*Pcal. The latter is fixed by the retained internal
state, not an adjustable extra pressure function. A nonzero compensated
clock mode therefore need not remain metric-invisible at finite pressure.

The susceptibility is KH=beta*chi_owned(I), not the unexcited beta by
definition. Its background time dependence remains inside Pcal_dot. Its
perturbation times a^2 first enters at cubic order about acceleration-free
FLRW. Retaining explicit hard oscillators again in this already averaged
sector would double-count their response. The main note correctly separates
the collinear scalar susceptibility from its specifically prepared isotropic
vector counterpart and does not promote either to an arbitrary finite-field
state.

I also independently checked the finite-pressure ADM cancellation, lapse and
shift equations, gauge-invariant pressure closure, and the static normalization
C*J_H=W(1/cI2+3). The actual finite-gap background must evolve e0(I), p_H(I)
and I proportional to a^-3; it is not automatically the old exact-dust
background. Multiple independently perturbed actions require additional
currents, not an unannounced single effective cI2.

## 2. A local quadratic action reproduces the dispersion

This is a SEPARATELY DECLARED leading quasistatic, frozen-background diagnostic.
Use c=1, proper time, physical wave number p, W>0, cI2>0 and
C=2M2/Kb. Let K be a positive constant retained polarization coefficient.
For the high-rate window above the soft band but below hard response poles,
K=KH. More general frequency-dependent soft response must be retained through
its actual coordinates or the rational kernel; it is not a constant local
action obtained by substitution.

Let r=delta rho_H and keep the Newtonian lapse Phi until its constraint is
varied. Up to the declared expansion and relativistic derivative corrections,
the real-mode quadratic Lagrangian is

    L = r(V_dot-Phi) - cI2*r^2/(2W)
          + W*p^2*(pi^2/2-pi*V)
          - C*Kb*p^2*Phi^2/2
          + C*K*p^2*(Phi-pi_dot)^2/2.                 (1)

The W terms follow directly by expanding the normalized u(T) in the phase
action: its second-order spatial contribution is
W[(grad pi)^2/2-grad pi.grad V]. The negative bare lapse gradient in (1)
is the Newtonian Einstein term, not a second added mode contact. Its source
constraint has the usual attractive Poisson sign.

For 0<K<Kb define

    A_K=K/(Kb-K), J=C*K*Kb*p^2/(Kb-K),
    c_eff^2=cI2-W/[C*(Kb-K)*p^2],
    X=V+A_K*pi.

Lapse elimination gives

    Phi=-r/[C*(Kb-K)*p^2]-A_K*pi_dot.

Eliminating r where c_eff^2 is nonzero then gives

    L = W*X_dot^2/(2*c_eff^2) + J*pi_dot^2/2
                + W*p^2*[(1/2+A_K)*pi^2-pi*X].       (2)

In particular, if

    p^2 > W/[C*(Kb-K)*cI2],                           (3)

both kinetic coefficients in (2) are positive. The potential-energy Hessian
in (X,pi), however, has determinant -(W*p^2)^2. Thus one unstable direction
remains in this controlled local reduction even with a positive kinetic
Hessian. The growing branch is not, on this evidence, a negative-kinetic
ghost. Nor should (2) be extrapolated below (3) to classify the full
gravitational constrained theory: its derivation has a separate domain.

Define Gamma=W/(C*Kb), L_H=W/(C*K). The equations from (2) are

    X_ddot=-c_eff^2*p^2*pi,
    pi_ddot=(L_H+Gamma)*pi-(L_H-Gamma)*X.

Their characteristic equation is exactly

    s^4-(Gamma+L_H)*s^2+Gamma*L_H
                       +cI2*p^2*(Gamma-L_H)=0.       (4)

This independently reproduces the main note's constant-kernel result,
including the Gamma*L_H term and the difference L_H-Gamma controlling the
high-p rate. With explicit soft modes, replace the determinant by the
reviewed rational characteristic equation; (4) is not an exact quartic
after making L frequency dependent.

## 3. Domain and what the result decides

The growth asymptote s^2 approximately sqrt(cI2)*p*sqrt(L_H-Gamma) requires
a nonempty window with H and fractional coefficient rates much less than s,
s much less than p, and s much less than the relevant hard orbital/response
frequencies; using K=KH additionally places s above the retained soft band.
The underlying spatial domain, owned phase/neutral-state prescription and
small perturbation amplitude still apply. No available gap, physical time
scale, preparation or unlimited spatial cutoff has been inferred.

The approximate frozen equations are not an exact Minkowski Einstein system
with an unsupported nonzero matter background. At finite H the full equations
in the main note supply the constraints. Independently grouping the intrinsic
density delta rho_H=d_D+kphys*Pcal confirms that the dangerous leading
expansion-gradient terms cancel: the leading high-p coupling proportional to
L_H-Gamma is not generated by dropping one uncancelled H*s*p^2 term. This
does not promote every subleading frozen coefficient to an exact finite-H
result.

The scientific advance is a definite same-state interface and an admissibility
test: finite positive pressure couples a previously compensated internal
clock channel to gravity, and positive intrinsic compressibility alone does
not remove it. A finite-time test must now keep that pressure, the owned
state-dependent susceptibility, the actual background, and the clock together.
The review does not claim an observed lensing/CMB outcome, a native BS metric
dictionary, or a general failure of network-based gravity.
