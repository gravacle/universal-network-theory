# Galactic smoothness, cold history and retained spatial stress V001

2026-09-29. Analytical same-state continuation; no new numerical producer,
observation, threshold, fit, preparation or spectrum is introduced.

## Result and domain

The inherited positive-quartic hard mode has a precise tradeoff: making its
SAME action sufficiently cold far back in an adiabatic homogeneous history
also makes its present intrinsic pressure weak. A finite gravitational
potential can then require a substantial galactic concentration. This is a
test of **whether that energy may be omitted as automatically smooth**, not
a prohibition on network clustering. A concentration derived from the common
cosmic state and its full field equations is a legitimate constructive route.
Its energy/stress must remain counted; it is not an independently fitted halo.

The exact inequality below concerns the scalar fixed-action hard sector of
the declared conditional parent. It is not a derivation from native BS,
an isotropic-vector susceptibility result, or a universal observational
exclusion. The nonzero-source correction is essential before applying it to
an actual static galaxy. The final section identifies a separate spatial
stress already suggested by native hopping but absent from a phase-only
truncation.

## 1. One action fixes both intrinsic support and homogeneous history

Use the existing dimensionless hard oscillator, with inertia and quartic
coefficient one,

    U(y)=R^2 y^2/2+y^4/4,   r=b^2/R^2,
    epsilon(r)=r/2+r^2/4,
    e=R^4 epsilon(r),       I=R^3 f(r),
    f(r)=(2/pi) r integral_0^(pi/2) cos^2(theta)
             sqrt[1+r(1+sin^2(theta))/2] dtheta,
    omega=R Omega(r),
    Omega(r)=pi/[2 j(r)],
    j(r)=integral_0^(pi/2) [1+r(1+sin^2(theta))/2]^(-1/2) dtheta. (1)

The existing orbit pressure is p=I omega-e, w=p/e, and the common-action
compression coefficient is c_I^2=I e_II/omega. These are phase-averaged
quantities, requiring the already stated clock/adiabatic and homogeneous
state assumptions. They are not independently established native sound
speeds. The proven w(r) increases from zero to 1/3, and f is increasing.

Let A be a specified inverse scale factor and let 0<w_c<1/3 be a specified
early-pressure tolerance. Neither is selected here from a desired outcome.
Define r_c by w(r_c)=w_c. Conserving the SAME action gives

    f(r_A)=A^3 f(r_b).

Coldness through that epoch is therefore exactly

    r_b <= r_cap=f^(-1)[f(r_c)/A^3].                         (2)

Subscript b denotes the homogeneous outer state at the present matching
epoch, not a new galactic abundance. For a single hard atom of weight beta,
its dimensionless intrinsic energy is E_H,b=beta R^4 epsilon(r_b).
Any other retained populated modes keep their own energy and history.

## 2. A potential-depth test for an automatically smooth hard component

For a stationary scalar phase the common chemical-frequency condition is

    N(r) omega(I(r),h(r))=N_b omega(I_b,h_b).                 (3)

First isolate intrinsic zero-source pressure: replace omega by omega(I,0).
This is a diagnostic limit, not permission to set the actual acceleration
source to zero in a nontrivial gravitational field. Define a specified
positive lapse depth

    Psi=ln(N_b/N).

In a weak, static spherical metric this depth is the integral of the local
circular-speed square divided by c^2 over a specified logarithmic-radius
interval. An absolute potential or an unobserved outer extension must not
be silently supplied. No observed speed, boundary radius or Psi is used here.

Suppose the proposed omission of hard clustering requires its intrinsic
energy density to stay within a declared fraction s>0 of the outer value:

    e(I(r),0) <= (1+s)e(I_b,0).

For Psi>0 the hardening oscillator requires I(r)>I_b. Let r_t satisfy
epsilon(r_t)=(1+s)epsilon(r_b). Exact local feasibility is

    Psi <= ln[Omega(r_t)/Omega(r_b)],
    r_b <= r_cap.                                          (4)

This formulation is usable without choosing a fitted radial action function.
It uses the phase condition to determine the action response. Equality at
a given depth predicts the actual contrast, instead of imposing smoothness.

There is also a rigorous algebraic necessary bound. With
q=1+r(1+sin^2(theta))/2 and positive time weights q^(-1/2),

    d ln Omega/dr=(1/4)<(1+sin^2(theta))/q>
                  <= 1/[2(1+r)].

Since 1+r=sqrt(1+4epsilon), integration gives

    Psi <= (1/4) ln{[1+4(1+s)epsilon_b]/[1+4epsilon_b]}.

Put x=f(r_c)/A^3. The exact inequality f(r)>=r/2 implies
epsilon_b<=x+x^2, and hence the joint necessary condition

    Psi <= (1/4) ln{[1+4(1+s)(x+x^2)]/[1+4(x+x^2)]}
         <= s(x+x^2).                                      (5)

The sharper middle inequality before substitution is
Psi<=s epsilon_b/(1+4epsilon_b). No optimization over an unreported state
or a selected radius occurs in (5).

In the uniformly cold limit, the actual leading expansions are

    w=3epsilon/8+O(epsilon^2),
    c_I^2=3epsilon/4+O(epsilon^2),
    ln Omega=3epsilon/4+O(epsilon^2).

Thus the leading smoothness/coldness relation is

    Psi <= 2s w_c/A^3 [with the corresponding cold corrections]. (6)

Equation (6) is an asymptotic statement, not the rigorous finite-amplitude
replacement for (4)-(5). It exposes why a present cold component is not
automatically resistant to a galactic potential.

For a fixed positive E_H,b, (5) can be expressed as a necessary gap window.
If 1<exp(4Psi)<1+s, define

    epsilon_req=[exp(4Psi)-1]/[4(1+s-exp(4Psi))].

Then intrinsic support and cold history require

    E_H,b/[beta epsilon(r_cap)] <= R^4
                                   <= E_H,b/(beta epsilon_req). (7)

The exact frequency relation (4) can be stricter. If exp(4Psi)>=1+s,
the upper-bound argument itself admits no finite epsilon_b for that
particular smoothness demand. This does not forbid a larger predicted
contrast or support from the other retained stresses. Changing R at fixed
energy is a redesign unless an actual preparation supplies that same energy;
the matched vacuum and calibration must also be recomputed, not held by an
independent offset.

## 3. What must change in the full polarized galaxy problem

The source h(a) is nonzero where the aligned preferred clock accelerates.
Equation (3), not its h=0 shorthand, is the actual phase equation. Exactly,

    Delta_src(I)=ln[omega(I,h)/omega(I,0)]
                 -ln[omega(I_b,h_b)/omega(I_b,0)],
    Psi-Delta_src(I)=ln[omega(I,0)/omega(I_b,0)].              (8)

The intrinsic bound applies to the LEFT side of (8). Delta_src is computed
from the same action, field and outer state; it is not an adjustable force.
For small I/R^3 and h/R^2, the original hard normal form gives

    omega/R=1+3I/(4R^3)+3h^2/(2R^4)
               +O((I/R^3)^2, I h^2/R^7, h^4/R^8).           (9)

The h-dependent shift may compete with an extremely small pressure shift.
Consequently a pressure-only no-go claim would be unwarranted even before
including soft polarization.

Moreover, the smoothness variable in (4) is the intrinsic e(I,0), NOT the
entire gravitating density. The fully retained static parent has

    rho=C[E+DeltaU+a.F+div F],
    T_ij=C[(Pi-DeltaU)gamma_ij-a_(i F_j)],
    F parallel a,

with the same phase condition and metric/source equations. Source changes,
polarization divergence, pressure anisotropy and the calibrated absolute
baseline cannot be erased in a comparison with observed gravity. In a
full stationary solution, the common outer state can determine a central
concentration through (3); that is precisely a possible prediction to test.
Neither (5) nor the earlier isolated n=1 support length is a substitute for
that boundary-value solution or for its formation history.

## 4. A retained spatial term can separate support from homogeneous dilution

There is a distinct constructive route, not a new pressure parameter. The
native carrier hopping already contains amplitude as well as phase energy.
For an owned fixed occupied graph and a scalar carrier amplitude
psi_v=sqrt(P_v)exp(-i theta_v), the exact edge identity is

    t |psi_u-psi_v|^2
      =t[(sqrt(P_u)-sqrt(P_v))^2
             +2sqrt(P_u P_v)(1-cos(theta_u-theta_v))].        (10)

The original diagonal current-square energy leaves the additional onsite
term (lambda_J-t)D_G; it must be retained. For quantum conditional graph
states the corresponding identity uses projected vector amplitudes
n_e sqrt(P_v)exp(-i theta_v)chi_v and their squared norm difference.
The conditional-state overlap and its memory are not automatically unity.
Thus dropping amplitude gradients and then declaring the phase truncation
spatially complete is not an exact native reduction.

An explicitly conditional illustration makes the distinction quantitative.
Suppose a justified local mode reduction retained

    L_spatial=-(m c_g^2/2)|grad y|^2.

This operator, its physical metric and c_g are NOT newly adopted here.
For a fast scalar orbit y(I,theta), with the turning-point phase convention,
the parity-vanishing cross term gives the averaged spatial energy

    (1/2)K_I|grad I|^2+(1/2)K_theta|grad theta|^2,
    K_I=m c_g^2<y_I^2>,
    K_theta=m c_g^2<y_theta^2>=c_g^2 I/omega.                (11)

The last identity follows exactly from I=m omega<y_theta^2>. In the harmonic
limit K_I=c_g^2/(4omega I). At an occupied uniform state, the canonical
quadratic action is

    deltaI delta(theta_dot) -(e_II/2)deltaI^2
       -(K_theta/2)|grad delta theta|^2
       -(K_I/2)|grad delta I|^2.

It has the local dispersion

    Omega_pert^2=K_theta e_II k^2+K_theta K_I k^4
        =c_g^2 c_I^2 k^2+c_g^4 k^4/(4omega^2)
                       [harmonic leading amplitude metric]. (12)

The gradient contribution is zero in an exactly homogeneous state. It can
therefore provide finite-wavelength restoring stress without replacing the
same homogeneous energy/action dilution by a different equation of state.
This is an avenue to derive and test, not evidence that its required scale
has been obtained. Increasing omega suppresses this particular dispersive
term at fixed c_g, so the high-gap route does not automatically solve the
spatial problem either.

If a phase-gradient term is already present in an alpha=1 effective action,
(11)'s phase part must be MATCHED to it, not added a second time. The
amplitude-gradient term, source derivatives, stress and boundary work must
be retained together. Native hopping, physical ruler/clock matching and
the retained-memory kernel must fix or measure their coefficients; no
arbitrary stabilizing coefficient follows from (10). A spatial continuum,
fast orbit averaging and the scale window of the derivative expansion
remain stated premises, not native conclusions.

## 5. Concrete next interpretation

For the existing scalar static candidate, use the already declared common
cosmic outer action and the full polarized field equations. Read the action
contrast and Delta_src from that SAME solution; then (2), (4) and (8) become
an internal check of pressure support versus predicted clustering. No new
halo normalization or fitted I(r) is necessary or allowed by this test.

If a derived concentration fails an independently specified galaxy test,
the exact native amplitude/phase identity and source-qualified memory name
the next missing term to derive. They do not authorize silently modifying
the tested phase-only theory. The present analysis makes no observational
pass/fail declaration and runs no extra toy example.

## Read-source identities

- HARD_MODE_COLD_HISTORY_CONSTRAINT_V001.md:
  `c4f80c78a6af1fadb472bc6bef9d3fb54302cc9b00ef0ae728a149b70b0bf067`.
- FINITE_GAP_STATIC_SUPPORT_AND_EARLY_HISTORY_V001.md:
  `a72f1e6c0a4fbd2ebabd38a9ac1d3fe91e2aebcd92144c5d8e51487547a32439`.
- SAME_ACTION_RADIATION_ASYMPTOTE_V001.md:
  `913160e3e485d3b6ddc64a66a47a0c06c40b6cd350bb8764df5629f848b49002`.
- FIXED_ACTION_MODE_INTERFACE_V001.md:
  `efb24d5e2758704fd62a760e13391e22ebfc2890430f1bcf352d6f08c2e64fc2`.
- POLARIZED_STATIC_RADIAL_REDUCTION_V001.md:
  `fbfcf8ac1b4a2d9c9e15a95512d026231376a1f42ca6d4714f156ba828064b5f`.
- NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md:
  `f3dad63532285add3f890b0c15e9fad4c4968226904e66cf43e6e110966eb6fa`.
- NATIVE_GAUGE_INVARIANT_TRANSPORT_MATCHING_V001.md:
  `8b924fac55a8809afeed7289a4293c2ab479c2ae8b0ddc1ce1f912387dd537b3`.

No frozen source or numerical result was changed.
