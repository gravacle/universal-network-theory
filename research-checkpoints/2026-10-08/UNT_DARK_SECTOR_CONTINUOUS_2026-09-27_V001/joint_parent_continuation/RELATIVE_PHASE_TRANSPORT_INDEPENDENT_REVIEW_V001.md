# Relative-phase transport: independent action and native-work review

2026-09-29. Analytical only. No operator is adopted, no coefficient is fitted,
and no numerical evolution or frozen-source alteration is performed.

Reviewed in full: `NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md`, SHA-256
`6e9cc504ae81841c55d73c84f91239ce407e84455f11efc10a32ed8724d4b45a`.
The recovered `BS_MICRO_ACTION.md` was also read in full; its held transfer,
current-square and record-occupation terms were used for the independent
native checks below.

**Outcome: accepted in the explicitly declared candidate scope.** The
operator changes the current and clock exchange as well as the spatial
energy. Its coefficient is not supplied by identifying a graph Laplacian.

## 1. Current and stress checks

Let q=u.partial theta, s_mu=P_mu^nu partial_nu theta,
omega=e0,I, W=C beta I omega and lambda=1-alpha. The candidate is

    Delta L=-alpha C beta I*s^2/(2omega).

About aligned FLRW, s_i=omega partial_i(V-pi), so its quadratic term is
-alpha W |grad(V-pi)|^2/(2a^2). It changes the original spatial action to

    W/(2a^2)[lambda |grad pi|^2
              -2lambda grad pi.grad V-alpha |grad V|^2].

The independently varied phase current is

    J_theta^mu=C beta[I u^mu-alpha(I/omega)s^mu].

Thus action conservation uses alpha V+lambda pi, while the preferred-clock
source becomes lambda W kphys(V-pi). The phase equation, intrinsic pressure
and linear momentum remain as stated in the reviewed note. Combining both
currents gives the unchanged total conservation equation with momentum V;
changing only a written gradient sign without changing these currents would
not be consistent.

The exact metric identity at fixed I,T,theta is

    partial(s^2)/partial g^{mu nu}=s_mu s_nu.

It yields the reviewed extra stress
alpha C beta(I/omega)[s_mu s_nu-g_mu nu*s^2/2]. This is zero at first order
about s=0 but has positive normal energy for alpha>0 and nonzero anisotropic
stress at quadratic order. The exact truncated phase equation and its
phase-dependent clock coefficient are

    q=e_I(I,h)+(alpha/2) partial_I(I/omega)*s^2,
    I(1-alpha q/omega)s_mu.

Accordingly alpha=1 does not eliminate preferred-clock dependence at every
order in the truncated action. The square-root phase action in the reviewed
note is a separate all-orders completion. Even in that completion the owned
acceleration contact, soft coordinates and matched vacuum remain.

For the homogeneous aligned and zero-shift static phase branches s=0,
the new operator and its first variation vanish. This verifies that it does
not alter their existing energy, pressure, endpoint or static phase relation.
The same statement cannot be extended to a prepared state with finite relative
phase gradients, nor used to manufacture an isotropic or paired preparation.

## 2. Independent constrained constant-kernel classification

Use the same local quasistatic, frozen-background approximation as
`FINITE_GAP_FLRW_INTERFACE_INDEPENDENT_REVIEW_V001.md`. Write p=kphys,
r=delta rho_H, cI2=I e_II/omega, and take 0<K<Kb to be a CONSTANT retained
polarization coefficient. The high-rate window above soft poles but below
hard response poles has K=KH. Frequency-dependent soft memory cannot simply
be promoted to a constant local action.

The unreduced real-mode Lagrangian is

    L=r(V_dot-Phi)-cI2*r^2/(2W)
        +W*p^2*(pi^2/2-pi*V)
        -alpha W*p^2*(V-pi)^2/2
        -C*Kb*p^2*Phi^2/2+C*K*p^2*(Phi-pi_dot)^2/2.

The added term has no time derivatives here, so lapse/density elimination
keeps the previous kinetic coefficients. Define

    A_K=K/(Kb-K), r_K=1+A_K=Kb/(Kb-K),
    X=V+A_K*pi,
    J=C*K*Kb*p^2/(Kb-K),
    c_eff^2=cI2-W/[C*(Kb-K)*p^2].

For c_eff^2>0 the reduced kinetic action is

    W*X_dot^2/(2*c_eff^2)+J*pi_dot^2/2,

and is positive. The potential-energy Hessian, divided by W*p^2, is

    [[alpha,              1-alpha*r_K],
     [1-alpha*r_K, alpha*r_K^2-2*r_K+1]].                (1)

Its determinant is exactly alpha-1. Therefore, within this positive-kinetic
and quasistatic domain:

* alpha<1 leaves an indefinite potential and a growing local direction;
* alpha=1 makes the potential positive semidefinite, proportional to V^2,
  with a neutral clock direction rather than complete clock elimination;
* alpha>1 gives a positive-definite potential and oscillatory nonzero
  normal modes of this constant-coefficient reduction.

These statements are not a classification below c_eff^2=0, nor a full
nonlinear or expanding-background stability theorem. The domain is

    p^2>W/[C*(Kb-K)*cI2].                               (2)

With Gamma=W/(C*Kb), L_K=W/(C*K), direct variation gives the same
characteristic polynomial as the independently checked density matrix:

    s^4-[Gamma+lambda*L_K-alpha*cI2*p^2]*s^2
          +lambda*[Gamma*L_K+cI2*p^2*(Gamma-L_K)]=0.    (3)

At alpha=1 its roots are s^2=0 and s^2=Gamma-cI2*p^2; (2) is a sufficient
domain for the latter to be negative. A zero root can permit a secular
coordinate in the frozen system and is not strict asymptotic stability.

For alpha>1 the high-p propagating branch has speed squared approximately
alpha*cI2 in the adopted c=1 metric units. Positivity alone therefore does
not establish a physical causal cone. The other branch, the actual hard
frequency, soft memory, coefficient evolution, spatial cutoff and retained
initial data must still be respected. In particular no unlimited-p conclusion
follows from the averaged source expansion.

## 3. Independent native checks and the remaining matching

For the BS one-carrier compression the exact identity is

    H_car=epsilon_psi I+t_hop L_G+(lambda_J-t_hop)D_G.

The degree-dependent onsite term is required. It is not removed by rewriting
the hopping as a positive graph-gradient energy. The inherited coefficients
do not cancel it.

For A_e=|v><u|, J_e=i(A_e-A_e^dagger), and the actual joint state,
U_phi^dagger A_e U_phi=exp(-i*dphi_e) A_e. Hence

    Delta E=t_hop sum_e[<n_e T_e>(1-cos dphi_e)
                              +<n_e J_e> sin dphi_e].

This independently verifies the positive current-work sign and the phase
Hessian edge coefficient t_hop<n_e T_e>. The diagonal incidence and feedback
terms commute with the carrier occupation twist; current squared is diagonal
in the relevant transfer occupancy sectors. No factorization of n_e and the
carrier is needed. Current-carrying states can have linear work, and the
Hessian weights are state dependent rather than automatically positive.

The added source-conjugacy subsection also passes independently. For the
Hamiltonian twist H(phi)=U_phi H U_phi^dagger, H'=-t_hop*nJ and
H''=+t_hop*nT, whereas the fixed-H state-twist linear work has the opposite
sign. Every covariantly transported eigenbranch has zero total energy
curvature; its contact cancels the full state/current response in the stated
second-derivative identity. Degenerate projectors and actual nonstationary
states require their own response treatment. Thus a positive instantaneous
contact is not by itself a nonzero relaxed transport stiffness. Fixed
boundaries, loop holonomy and finite-time work are distinct experiments, not
exceptions that can be silently assumed. This qualification is essential to
using the native test as a physical matching rather than just a graph identity.

I also checked the separate held record-phase null: with copying/ports off,
local record-occupation phases commute with the declared held Hamiltonian.
A native carrier stiffness is therefore not immediately a stiffness of the
record-raising clock phase. The Berry normalization theta_car=-arg(psi) is
consistent with +hbar sum p_v theta_car_dot, but its identification with the
new hard collective phase still needs the temporal/source map.

The reviewed spatial-tensor matching has the right Z^-2 factor when
theta=Z theta_car. An independently measured/derived physical edge geometry,
volume, canonical phase normalization and retained source energy are required
before it determines alpha. None is supplied by choosing alpha=1 or by the
local stability classification (1). Thus the note provides a precise candidate
and a native same-state matching test, not a silent repair of the original
parent or an observed dark-sector success.
