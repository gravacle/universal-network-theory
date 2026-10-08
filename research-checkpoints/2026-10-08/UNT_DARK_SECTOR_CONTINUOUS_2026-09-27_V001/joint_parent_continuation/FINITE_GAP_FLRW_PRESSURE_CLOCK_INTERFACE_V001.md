# Finite-gap pressure, polarization and the clock on the same FLRW background

2026-09-29. Analytical continuation of the retained averaged parent. No
numerical producer, new preparation, fitted gap/radius, extra halo profile,
independent kinetic function or change to frozen evidence.

## Result

At finite hard gap the excitation has a complete linear stress/current
interface, but it is **not generally a barotropic fluid in its total
gravitating density**. Its pressure responds to its hard-mode density;
gravity also sees the signed polarization density. The resulting intrinsic
nonadiabatic pressure is fixed by the clock/polarization, not a new function.
Consequently the previously metric-compensated clock sector is no longer
automatically invisible to the metric.

The same equations give a concrete local admissibility test. In a specified
subhorizon, frozen-background, slow-hard-mode window the pressure mixes with
the existing clock branch. A positive intrinsic compressibility does not by
itself stabilize that branch. The derived dispersion relation below supplies
a prospective test of that window; it is not an arbitrary-wave-number claim
about the unaveraged parent or the native BS network.

## 1. State, action and dimensions

Use c=1, proper cosmic time, M2=1/(8 pi G) and C=2M2/Kb. The hard sector has
total weight beta, positive finite gap R, and the SAME per-copy orbit energy
e(I,h). Its scalar leading adiabatic action is

    S_H=C beta integral sqrt(-g)[I u.partial theta-e(I,h(a))],
    u_mu=-partial_mu T/sqrt(-partial T squared).                 (1)

Keep the Einstein action, the explicit zero-background soft modes and the
unchanged matched term -C DeltaU. Do not add another bare contact to (1).
The bounded source is h_mu=a_mu/sqrt(1+a^2/gs^2), hence h=a+O(a^3)
around the aligned FLRW background. The linear answer does not discard gs;
it simply first enters beyond the quadratic perturbation action.

The following is a specified common-action/common-phase hard sector: copies
have equal background I and the same fractional scalar action perturbation.
Independent hard actions/phases would give multiple currents and relative
entropy data, not this one-current reduction. The old collinear coherent
pulse is NOT silently converted to the paired/phase-averaged state. A balanced
pair, its preparation work, rapid phase average and any orientation ensemble
are the additional counted conditions described in the paired-state note.

For the collinear scalar perturbation parallel to the stored orbit axis,

    e(I,h)=e0(I)-chi_B(I) h^2/2+O(h^4),
    chi_B=R^2 chi_parallel,        KH(I)=beta chi_B(I).           (2)

Here kappa=u4=m=1 only when evaluating the inherited dimensionless oscillator
formulas; omega=e0,I is always an angular frequency in the same proper time
as H. For a separately declared equal-action isotropic orientation ensemble
with the qualified periodic/neutral-data prescription, replace chi_B in (2)
by R^2(chi_parallel+2chi_perp)/3. That is the derived vector infinitesimal
response, NOT the scalar finite-field curve. Angular transport, free neutral
data and averaging errors have not been eliminated by this replacement.

Equations below use whichever positive KH is actually owned by that named
linear state. Both proven susceptibilities satisfy 0<KH<beta for positive
excitation in the dimensionless convention. The soft background is unexcited;
its finite positive matrices are

    Ms=diag(w_j m_j), Ks=diag(w_j kappa delta_j^2),
    b_j=w_j kappa delta_j, S=b^T x,
    Ksoft=b^T Ks^(-1)b,       Kb=Ksoft+kappa beta.

The hard averaged coordinates must not also be retained as explicit hard
oscillators in this same system: that would double-count them. Frequency-
dependent hard polarization and higher adiabatic terms are omitted only
within their controlled slow-hard-source domain, not asserted identically zero.

## 2. Background and full first-order stress

Variation of (1), before identifying a fluid, gives

    nabla_mu(I u^mu)=0,       u.partial theta=e_I.

On aligned flat FLRW define

    I_dot=-3H I, omega=e0,I, cI2=I e0,II/omega,
    rho_H=C beta e0, p_H=C beta(I omega-e0),
    W=rho_H+p_H=C beta I omega,
    rhoLambda=C DeltaU,
    rho_H_dot=-3H W, p_H_dot=-3H cI2 W,
    omega_dot/omega=-3H cI2.

The actual expanding background, including separately owned ordinary species,
is

    3M2 H^2=rho_H+rhoLambda+rho_o,
    -2M2 H_dot=W+rho_o+p_o.                                 (3)

For the positive harmonic-plus-quartic zero-source orbit, 0<cI2<1/3 at
positive action. This is an intrinsic derivative, not yet the speed of a
closed gravitating mode. Its value changes as the SAME I dilutes.

Use Newtonian gauge and a nonzero comoving Fourier wave number k:

    ds^2=-(1+2Phi)dt^2+a^2(1-2Psi)dx^2,
    T=t+pi, theta=theta_bar(t)+omega(t) V,
    kphys=k/a, v=V-pi, U=Phi-pi_dot, ell=kphys U,
    d=delta I/I=delta rho_H/W,
    Pcal=C[S+KH(t) ell].                                    (4)

The convention for the real longitudinal mode is that the divergence of
polarization is -kphys Pcal. The time-dependent normalization delta theta=
omega V is essential: setting omega constant at finite gap would erase a
pressure term in the phase equation.

To check the stress directly, put s_mu=P_mu^nu partial_nu theta. At a=0 the
on-shell phase part has

    T_H,mu nu=W u_mu u_nu+p_H g_mu nu
                      -2C beta I u_(mu s_nu).

The first-order components consequently are

    delta T_H^0_0=-delta rho_H=-W d,
    delta T_H^0_i=-W partial_i V,
    delta p_H=cI2 delta rho_H=cI2 W d,
    delta anisotropic stress_H=0.                           (5)

In particular the normal momentum proportional to pi and the relative-phase
momentum proportional to V-pi combine. Replacing u by an independently varied
ordinary-fluid velocity would bypass the clock equation and is not (1).

The soft and hard polarization contribution at linear order is

    delta rho_pol=-kphys Pcal,
    delta T_pol^0_i=0, delta p_pol=0,
    delta anisotropic stress_pol=0.                         (6)

One direct check is its unitary-clock quadratic action

    C a^3[x_dot^T Ms x_dot/2-x^T Ks x/2
                    +kphys n S+KH(t) kphys^2 n^2/2].

It has no shift or spatial-metric perturbation at this order. Variations of
KH with delta I multiply acceleration squared and first enter at cubic order;
its BACKGROUND time dependence remains in Pcal_dot. The vacuum has its usual
background metric stress and no independent density/pressure fluctuation.

## 3. A runnable linear system, with ordinary species retained

The exact linear equations of the displayed averaged action are

    d_dot=3Psi_dot-kphys^2 pi,
    V_dot=Phi+cI2(d+3H V),
    pi_dot=Phi-U,
    Pcal_dot+2H Pcal=W kphys(V-pi),
    Ms(x_ddot+3H x_dot)+Ks x=b kphys U,
    U=(Pcal/C-S)/(KH kphys).                               (7)

KH>0 makes the last algebraic inversion available for the stated excited
finite-gap state. This is not an inversion at k=0; homogeneous background
variations require their own constraint equations. The clock-current source
is the ENTHALPY W, not rho_H. No derivative of KH is to be dropped when (7)
is written instead as an equation for U or v.

Define the total excitation-plus-polarization perturbations

    delta rho_D=W d-kphys Pcal, delta p_D=cI2 W d,
    delta T_D^0_i=-W partial_i V.                           (8)

Since kphys_dot=-H kphys, (7) gives exactly

    delta rho_D_dot+3H(delta rho_D+delta p_D)
                          =W(3Psi_dot-kphys^2 V),
    V_dot=Phi+delta p_D/W+3H cI2 V.                         (9)

These are the total scalar conservation equations, not yet a closed barotropic
EOS for delta rho_D. Couple (7)-(9) to the unmodified Einstein equations and
the specified ordinary species. For clarity, representative Einstein equations
in these conventions are

    delta rho_D+delta rho_o
       =-2M2[kphys^2 Psi+3H(Psi_dot+H Phi)],
    Psi_dot+H Phi=(W V+Q_o)/(2M2),
    Psi_ddot+H(Phi_dot+3Psi_dot)+(2H_dot+3H^2)Phi
                 +(kphys^2/3)(Psi-Phi)
       =(delta p_D+delta p_o)/(2M2).                       (10)

Here delta T_o^0_i=-partial_i Q_o; ordinary anisotropic stress supplies the
usual trace-free spatial Einstein equation. The mode sector adds none at
this linear order, but Phi=Psi must NOT be imposed if ordinary species do.
Ordinary continuity, Euler, scattering or radiation hierarchies remain their
owned equations; none is supplied by calling the modes cold. This is a closed
network-sector interface once those equations and initial conditions are given.

### Independent lapse/shift check

With only hard excitation and vacuum in the background, use unitary T=t,
N=1+n, N_i=partial_i beta_shift, gamma_ij=a^2 exp(2zeta)delta_ij,
theta=theta_bar+omega v, and q=zeta_dot-Hn. The quadratic action per a^3 is

    M2[-3q^2+kphys^2 zeta^2+2kphys^2 n zeta
                                   -2kphys^2 q beta_shift]
    +delta rho_H(v_dot-3H cI2 v-n)
    -cI2 (delta rho_H)^2/(2W)
    +3W zeta(v_dot-3H cI2 v)-W kphys^2 beta_shift v
    +C[x_dot^T Ms x_dot/2-x^T Ks x/2+kphys n S
                                      +KH kphys^2 n^2/2]. (11)

The homogeneous Einstein/vacuum expansion has +3rho_H*n*zeta and
-9p_H*zeta^2/2 after the background equations and a time integration by
parts. The hard action has the opposite two terms. Their cancellation is
the finite-pressure counterpart of the reviewed dust derivation. Variation
of delta rho_H and the shift gives

    n=v_dot-3H cI2 v-cI2 delta rho_H/W,
    q=-W v/(2M2)=H_dot v.

Thus zeta-Hv is not generally conserved: its derivative is
-H cI2(delta rho_H/W+3H v). This independently checks the pressure/clock
term that is absent in the ideal dust limit. Ordinary background components
add their own complete action and constraints; (11) is not reused with their
background terms selectively omitted.

## 4. Gauge-invariant closure and its two useful limits

Under an infinitesimal time shift xi, V and pi each change by -xi and
d changes by +3H xi. Therefore v, U, Pcal and

    Gamma_H=d+3H V,
    Delta_H_com=W Gamma_H,
    Delta_D_com=delta rho_D+3H W V

are gauge-invariant scalar combinations (Phi,Psi in (10) are their Newtonian
gauge/Bardeen representatives). The pressure closure is

    delta p_D=cI2(delta rho_D+kphys Pcal),
    delta p_D_com=cI2(Delta_D_com+kphys Pcal),
    delta p_nad=delta p_D-cI2 delta rho_D=cI2 kphys Pcal. (12)

The background adiabatic derivative is cI2; the extra term is an actual
polarization/relative-clock variable, not a freely adjustable entropy source.
An economical invariant internal form is

    U=v_dot-cI2 Gamma_H,
    Pcal=C[S+KH kphys(v_dot-cI2 Gamma_H)],
    Pcal_dot+2H Pcal=W kphys v,                         (13)

together with the soft equation in (7). This displays directly how the metric
and internal sector cease to decouple.

* At fixed finite k and fixed owned hard energy, R->infinity gives cI2->0,
  p_H->0 and KH->kappa beta. Equations (7)-(12) reduce to the independently
  reviewed hard-limit dust interface, including its extra clock sector.
  This limit need not be uniform in wave number, epoch or initial fast data.
* If polarization is ACTUALLY absent as a branch/action approximation, Pcal=0
  and its clock equation gives V=pi for W>0,k!=0. Then (9) and (12) are the
  ordinary irrotational barotropic-fluid equations. This is a variation-based
  fluid limit, not an inference from e_II. Simply deleting the owned positive
  KH or ignoring a nonzero Pcal is not such a limit; the fast clock branch
  makes a small-contact approximation potentially singular.

In particular, with no ordinary compensating perturbation, a finite-cI2 mode
with Phi=Psi=0 must have V=0 by the momentum constraint and delta p_D=0 by
the spatial equation. Hence d=0, then Pcal=0 and pi=0. Only source-orthogonal
soft internal motions can remain. The old nontrivial hard/polarization
compensated mode is therefore not exactly metric-invisible at finite pressure.
This argument does not exclude additional compensation involving independently
excited ordinary species.

## 5. A finite-window dispersion discriminator, not a UV extrapolation

Here is a small analytic test of (7), with no empirical scale choice. Freeze
background coefficients over an interval; consider a hard/vacuum-dominated
local patch, nonrelativistic hard pressure, and a mode with |s|>>H,
kphys>>H and |s|<<kphys in c=1 units. Ordinary perturbations are absent in
THIS discriminator; their actual responses can instead be appended to (7)-(10).
The leading weak-field constraint is

    Phi=Psi=-(W d-kphys Pcal)/(2M2 kphys^2).

For exp(st), y=s^2, eliminate only the retained finite soft oscillators:

    K(y)=KH+b^T(Ks+y Ms)^(-1)b,
    q(y)=K(y)/Kb, Gamma=W/(2M2), L(y)=Gamma/q(y).

For real y>=0, K is positive, decreasing and bounded below by KH. The positive
excitation contact defect gives q(0)<1, hence 0<q(y)<1. Poles at negative y
are retained soft oscillations, not discarded free modes. Combining (7) with
the constraint gives two exact equations of this local approximation:

    (y-Gamma)d-kphys^2[1-q(y)]U=0,
    [q(y)y-Gamma]U-Gamma cI2 d=0.

The coupled characteristic condition is

    (y-Gamma)[q(y)y-Gamma]
                  -Gamma cI2 kphys^2[1-q(y)]=0.          (14)

For constant K this is equivalently

    y^2-(Gamma+L)y+Gamma L+cI2 kphys^2(Gamma-L)=0.         (15)

It also follows directly by using the two density variables
d_D=delta rho_D and Y=kphys Pcal:

    [d_D,Y]_ddot =
       [[Gamma-cI2 kphys^2, -cI2 kphys^2],
        [cI2 kphys^2,       L+cI2 kphys^2]] [d_D,Y].      (16)

For cI2=0 the ordinary density and clock factors reappear. In the genuine
zero-polarization limit of (14), the finite root is the usual local Jeans
form y=Gamma-cI2 kphys^2; the other internal branch is a singular limiting
degree, not a justified deletion at finite K.

For cI2>0 and 0<q<1, the left side of (14) is strictly negative at y=Gamma
and tends to positive infinity as y tends to infinity, since KH>0. Thus
there is a real growing local branch with y>Gamma. No claim of uniqueness
of every finite-soft-band root is needed for this existence statement.
For constant K the two roots are explicit:

    y_+/-=[Gamma+L +/- sqrt((L-Gamma)^2
                       +4cI2 kphys^2(L-Gamma))]/2.       (17)

The lower branch changes sign at kphys^2=Gamma/[cI2(1-q)], but the upper
one remains growing. Intrinsic pressure stabilizing one density combination
does not stabilize the coupled clock. This is why a static J/Kcal or a
positive e_II alone is insufficient.

If a window ALSO has |s| much larger than every retained soft frequency yet
much smaller than the hard orbital/response frequency, K tends to KH. Then

    y_+ ~ sqrt(cI2) kphys sqrt(L_H-Gamma),
    s_+ ~ [sqrt(cI2) kphys sqrt(L_H-Gamma)]^(1/2),
    L_H=Gamma Kb/KH.                                    (18)

The omitted continuity term 3Psi_dot and weak-field constraint corrections
are relatively suppressed by y/kphys^2 (and H^2/kphys^2); background evolution
by H/|s| and corresponding fractional coefficient rates. The hard adiabatic
elimination additionally requires |s|/omega_H small and controlled initial
polarization transients. The source/metric amplitude must stay linear, and
the spatial domain of the adopted parent must be respected. A finite positive
band and calibrated time scale are needed to establish this window at all.

There is therefore a precise conditional high-wave-number admissibility
question, not a proof of an unlimited UV catastrophe in the native theory.
One cannot extrapolate (18) through the hard poles or supply an unowned new
spatial-gradient term to repair it. Conversely it is not valid to erase this
branch by inserting an ordinary-fluid sound speed into a dust equation.
The constructive next test is the finite-time FLRW system (7)-(10), with
fixed same-state coefficients and an explicitly controlled frequency band.

In SI, Gamma=4 pi G(rho_H+p_H)/c^2 for energy-density rho_H,p_H, and each
cI2*kphys^2 in (14)-(17) is c^2*cI2*kphys_SI^2. The dimensionless intrinsic
coefficient cI2 is not itself a dimensional velocity. No physical hard
frequency follows from an acceleration calibration without its inertia/time
mapping.

## 6. Leading finite-hardening terms and radial consistency

In the inherited kappa=u4=m=1 hard units, with I/R^3 small,

    e0=R I+3I^2/(8R^2)+O(I^3/R^5),
    omega=R+3I/(4R^2)+O(I^2/R^5),
    e_II=3/(4R^2)+O(I/R^5),
    p_H/rho_H=3I/(8R^3)+O(I^2/R^6),
    cI2=3I/(4R^3)+O(I^2/R^6).

The scalar hard contact is

    KH=beta[1-3I/R^3+O(I^2/R^6)]
      =beta[1-4cI2+O(cI2^2)].                            (19)

For the named isotropic infinitesimal state instead the deficit is
5I/(3R^3)=(20/9)cI2 to leading order. Its altered KH changes the coefficients
but does not make finite pressure or the clock source disappear. All these
terms arise from the SAME orbit and state; pressure and contact may not be
adjusted independently. Cosmological dilution increases I toward the past,
so a present cold estimate is not an all-epoch error bound.

The static radial phase condition is still N*omega=constant. Near a zero-source
scalar reference it gives delta I=-omega*delta ln N/e_II. If the soft sector
is also quasistatic, q(0)=1-Kcal/Kb. The nonrelativistic local zero-frequency
threshold in (14) is

    k_static,NR^2=Gamma/[cI2(1-q(0))].                    (20)

This agrees with the leading density part of the full static radial
J_static/Kcal, not with an independently chosen pressure-support radius.
Indeed for this hard component the exact active-source derivative is

    C J_H=W(1/cI2+3).

The extra 3W is the relativistic active-pressure contribution; keeping it
requires the full static Einstein equations, background curvature and stress,
not selective insertion into a Newtonian dispersion relation. Occupied soft
components would add their own phase/action derivatives. Equations (14)-(20)
do not replace the nonlinear boundary problem or supply a smooth vector center.

## 7. The cosmic vacuum was never removed

DeltaU is still the same matched absolute endpoint in (1)-(3). The FLRW
vacuum affects H and H_dot and consequently every clock/pressure coefficient
history. It has no independent perturbation because it is a constant, not
because its stress was set to zero.

A subhorizon peculiar-potential calculation subtracts the SOLVED homogeneous
background equations when defining delta rho; it does not freely subtract
DeltaU from a static Hamiltonian. In physical local coordinates, background
relative acceleration contains (a_ddot/a)r, with

    a_ddot/a=-(rho_H+3p_H+rho_o+3p_o-2rhoLambda)/(6M2).

For pure vacuum this is the familiar local outward Lambda*r/3 contribution.
A genuinely static annulus keeps E+3Pi-2DeltaU and its owned boundary data as
in the exact radial reduction. A short-time weak-field peculiar perturbation
and an isolated global static halo are different approximations.

The useful next scientific decision is therefore concrete: evaluate the full
linear evolution and its controlled local dispersion using one retained
finite-gap state and the same background, source susceptibility and physical
inertia. That tests whether a cold shared state also has an admissible
clock/metric response before using it as a galaxy or acoustic component.
Neither an observational threshold nor a new state selection is supplied here.

## Source custody

Read-only originals used in this derivation:

* `HARD_LIMIT_DUST_INTERFACE_WITH_ORDINARY_RADIATION_V001.md`:
  `41111a6ed3d0e69114ad36c19d1790e11a57fb2195d395aea88259b67083d522`.
* `HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md`:
  `c501fc2aeebe0cf389ad9c21c5c7fdd3240209a1d9dd0ae710ed45d67bb8003d`.
* `FIXED_ACTION_MODE_INTERFACE_V001.md`:
  `efb24d5e2758704fd62a760e13391e22ebfc2890430f1bcf352d6f08c2e64fc2`.
* `PAIRED_HARD_MODE_STATE_V001.md`:
  `7461324e5c40de23f796c9e438a9d1cbecd88ffcc9bdb2c21c8e05fd54a38c91`.
* `ISOTROPIC_VECTOR_ORBIT_RESPONSE_V001.md`:
  `691a7476af57c9f5f55a63f2bad44b274affca82e6b9af6aa16fe3f9884673c4`.
* `POLARIZED_STATIC_RADIAL_REDUCTION_V001.md`:
  `fbfcf8ac1b4a2d9c9e15a95512d026231376a1f42ca6d4714f156ba828064b5f`.
