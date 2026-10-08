# Shared static-attraction and radiation necessity: V001

2026-09-29. Analytical only; no orbit solve, quadrature, producer, data fit,
new gap, altered preparation, or frozen-source edit. This is a conditional
necessary test of the declared finite-gap, aligned-static common-phase
branch. It is not a no-go for the network proposal, a full galaxy solution,
or an abundance calculation.

## 1. The exact finite-field static test

Keep the existing soft ground spectrum, one hard atom of weight beta and
gap R, bounded h(g)=g/sqrt(1+g^2/S^2), common frequency
omega(I,h)=omega_b exp(-Phi), and the same matched DeltaU. At the cosmic
reference the soft modes are unexcited and E=beta e_b. Write

    chi=e_b/R^4=E/(beta R^4), eta=h/R^2, eta_m=S/R^2,
    epsilon=gstar*a/c_light^2,
    gstar=c_light*H sqrt[3 Kb Omega_exc/(2E)].                 (1)

The last equality is the existing present-energy calibration, not an
independent gravity normalization. The source length a is the already
declared physical scale of the synthetic test, not a fitted halo radius.

For an everywhere attractive solution v=-u>=0 on the original cylindrical
patch, T=E+3Pi satisfies

    T(-epsilon v,g)-Tb=Tc(g)+epsilon v Jsec(v,g),
    Tc(g)=T(0,g)-Tb,
    Jsec=integral_0^1 J(-s epsilon v,g) ds.                   (2)

If the branch is occupied and elliptic, 0<mu=K_T/Kb<=1, and the effective
source B_eff defined in the existing eigenfunction identity is positive,
then

    epsilon^2 inf(Jsec)/Kb < lambda_1(mu) <= lambda_Lap,
    lambda_Lap=[j_01^2+pi^2/4]/L^2.                         (3)

The mixed boundaries are Dirichlet at top/outer wall, homogeneous flux at
axis/bottom for the eigenfunction, and the actual strictly positive bottom
sheet flux for the candidate. Equation (3) concerns an attractive elliptic
branch, not all sign-changing roots, Newton convergence, or time evolution.

## 2. A global upper action-curvature bound gives a lower reaction bound

Use the exact unit-gap orbit

    c^3+(1+r^2)c=eta,
    q_+,-=2+6c^2+r^2(1+x^2) +-4crx,  0<=x<=1,
    Omega=1/[sqrt(2) mean(q^(-1/2))],
    i_r=r[d-4c^2 r^2/d]/Omega,  d=1+r^2+3c^2.

Here r is half the turning span in units of R, not a spatial radius. Pair
the two angular points. For their q^(-3/2) weights,

    |w_+-w_-|/(w_++w_-) <=3|c|rx.

The paired weighted radial derivative of q is at most
4r(1+3c^2). Since q>=2, this proves Omega_r<=Omega r(1+3c^2).
Also

    d-4c^2 r^2/d >= (1+r^2)(1-c^2),
    Omega^2/(1+r^2) <=1+3 eta_m^2+eta_m.

Consequently, throughout the globally hardening domain eta_m^2<1/12,

    epsilon_ii=Omega_r/i_r <= Ecap,
    Ecap=(1+3 eta_m^2+eta_m)(1+3 eta_m^2)/(1-eta_m^2),
    J=beta R^4[Omega^2/epsilon_ii+3i Omega]
                                      >=beta R^4/Ecap.       (4)

The r=0 inequality follows by the continuous occupied limit. It does not
assign occupied J to a genuinely empty copy. A sufficient occupancy test
over the entire attractive phase segment is

    Omega_b > Omega_0(eta_m),
    Omega_0(eta)=sqrt(1+3c_0^2), c_0+c_0^3=eta.              (5)

The stable excess-frequency formulas should be used to authenticate (5)
for a cold numerical input. Conditions (4)-(5) involve no local-density
linearization: an arbitrarily large I/I_b does not invalidate the bound.

Substitution of (1) and (4) into (3) gives the exact necessary inequality

    chi > chi_crit,
    chi_crit=3 Omega_exc (H*a/c_light)^2
                                      /[2 Ecap lambda_Lap]. (6)

The explicit gstar, beta and Kb cancel. Ecap still depends on the actual
matched S/R^2, and occupancy, source sign, geometry, ellipticity and weak
metric validity remain hypotheses. A changed normalization can also change
whether those hypotheses hold; the cancellation is not a universal claim
that every parameter dependence has disappeared.

## 3. A rigorous cold-domain source-sign certificate

The source Tc in (2) must not be discarded. The following conservative
bound establishes its sign for a checkable subset of the existing cold
branches, without replacing the hard oscillator by a harmonic model.

Assume

    eta_m<=d_*=1/100,
    2(Omega_b^2-1)<=d_*^2,
    Omega_b>Omega_0(eta_m).                                (7)

Along the Phi=0 constant-frequency path, q>=2+r^2 implies
r^2<=2(Omega_b^2-1); also |c|<=|eta|. Thus |c|,r<=d_* over
the whole path 0<=h<=S, not just at sampled values.

Let z=c+r cos(theta), M3=<z^3> with the exact time weight, and
b=<z>=eta-M3. At fixed Omega, the exact thermodynamic identity is

    partial_eta(epsilon+3pi)|Omega
                              =2b-Omega (M3)_r/Omega_r.    (8)

For clarity an explicit bound on the last ratio follows. Put u=rx,
Hpair=(sqrt(q_+)+sqrt(q_-))^2>=8 and Wpair=(q_+^(-1/2)+q_-^(-1/2))/2.
The conditional paired third moment is

    m=c^3+3cu^2-8cu^2(3c^2+u^2)/Hpair,
    M3=mean(Wpair*m)/mean(Wpair).

Pair differentiation and |c_r|<=2|c|r give

    |partial_r ln Wpair| <=(1+9c^2)r,
    |partial_r ln Hpair| <=(2+14c^2)r.

With v_*=d_*^2, direct differentiation of m and the covariance term in
the normalized mean give the explicit conservative bound

    |(M3)_r|/(|c|r)
                  <=6+30v_*+108v_*^2+128v_*^3 <6.01.        (9)

The continuous limits at c=0 or r=0 are intended; no division by a
computed zero is required. For example, |m|<=|c|(4v_*+4v_*^2),
|m_r|/(|c|r)<=6+22v_*+28v_*^2+56v_*^3, and twice the product of
the first bound with the weight-score bound supplies the remaining
covariance estimate. These are inequalities of exact quadratures.

The paired hardening inequality, retaining the angular mean x^2=1/2,
and q<=Q_*=2+12d_*^2=2.0012 prove

    Omega_r >= (3/4)r(1-12d_*^2)/(Q_*/2)^(3/2) > .748r,
    Omega <=sqrt(Q_*/2)<1.001.

The paired first moment is c[1-8u^2/Hpair]>=c(1-r^2)>=0. Hence
(8)-(9) imply partial_eta(epsilon+3pi)|Omega >=-8.05 eta.
Integrating from eta=0 and restoring beta R^4 gives the deliberately
looser, simple certificate

    Tc,hard(h) >= -5 beta h^2.                              (10)

For each soft minimum, delta^2 y+y^3=delta h and
e_min=-delta^2 y^2/2-3y^4/4. Exactly

    -2 e_min >=h delta y,
    [delta y/h]=delta^2/(delta^2+y^2) decreases with h.

Thus, for the actual positive soft weights,

    Tc,soft(h)=-2 Esoft,min(h) >=[Bs(S)/S]h^2,
    Tc(h) >=[Bs(S)/S-5 beta]h^2.                            (11)

The three input inequalities (7) and Bs(S)/S>=5 beta are therefore
sufficient to establish Tc>=0 on the full source interval. Strictly
positive prescribed sheet flux then makes B_eff>0 independently of the
unknown candidate potential and eigenfunction normalization. This closes
the source-sign hypothesis of (3); it does not prove existence, material
ellipticity, or the remaining weak-metric approximation.

The constant 5 is conservative and not fitted to a numerical outcome.
Failure of this sufficient certificate does not show that Tc is negative.
The exact material remains unchanged. Apply these tests to authenticated
baseline/source inputs; do not infer them from rounded tiny frequencies.

## 4. Exact radiation consequence of the same present energy

Let A_unit(chi) denote the action of the unit-gap, zero-source oscillator
z''+z+z^3=0 at energy chi. Then I_b=R^3 A_unit(chi). Define

    C4=[pi/B(1/4,3/2)]^(4/3),
    X(chi)=C4*A_unit(chi)^(4/3)/chi.                        (12)

This is exactly Q_rad/E for the single occupied hard atom with the soft
reference in its zero-action state. It is not an additional radiation
population. I omega=e+p and I_e=1/omega imply

    d ln X/d ln chi=(1-3w)/[3(1+w)]>0                       (13)

at every finite positive chi. The limit is zero at chi=0 and one in the
pure-quartic high-energy limit. At fixed E and beta, increasing R lowers
chi and X, but raises the cold static reaction proportional to R^4.

If all static hypotheses above hold, (6), (12) and (13) require

    Omega_extra,rad/Omega_gamma
      > (Omega_exc/Omega_gamma)*X(chi_crit).                 (14)

This is the exact action-function version of the shared tradeoff. At small
chi, A_unit(chi)=chi[1-3chi/8+O(chi^2)], so

    X(chi)=C4 chi^(1/3)[1-chi/2+O(chi^2)].                  (15)

Only in this qualified cold limit may (14) be displayed as a cube-root
power law. The exact function should be retained for any arithmetic test.
An explicit radiation upper limit, if later independently qualified, would
provide a necessary interval in chi. No such numerical limit or abundance
threshold is selected here.

A simple all-energy area certificate avoids a new orbit quadrature. Let
b be the zero-source turning amplitude, so
b^2=4chi/[1+sqrt(1+4chi)]. On |z|<=b the exact potential lies below
(1+b^2/2)z^2/2, while it lies above z^2/2 everywhere. The ellipse of
frequency sqrt(1+b^2/2) and energy chi is inside the exact energy region;
the exact region is inside the unit-frequency ellipse. Their canonical
areas give

    chi/sqrt(1+b^2/2) <= A_unit(chi) <= chi,
    C4 chi^(1/3)(1+b^2/2)^(-2/3)
                  <= X(chi) <= min[1,C4 chi^(1/3)].          (16)

The extra upper bound one follows from the positive quadratic term and
the pure-quartic action comparison. The lower bound in (16), evaluated at
chi_crit, can replace X(chi_crit) in a rigorously conservative version of
(14). This is arithmetic from an exact area inclusion, not a quadrature
estimate or an asserted harmonic equality.

Equations (12)-(15) describe the same action-scaled cosmological history
I(a)=a^(-3)I_b and its asymptotic radiation coefficient. Applying it during
a finite physical epoch still requires the declared isotropic/paired state,
rapid-mode/adiabatic clock conditions and the correct photon/thermal
normalization. It neither turns mode radiation into photons nor converts a
proxy nucleosynthesis table into an exact scalar abundance calculation.

## 5. What this does and does not decide next

An attractive root violating a qualified necessary inequality cannot be
rescued by changing Newton iterations or using the locally larger finite-g
soft mu. Conversely, failed Newton seeds do not establish violation or
nonexistence. The prescribed clamps remain externally supported; their
scale is not an owned isolated-galaxy exterior.

The result argues for checking the complete necessary hypotheses and
shared radiation coefficient before repeating a static-clamp search. If
that branch is inadmissible, the same macroscopic action still contains
the geodesic-clock, zero-polarization GR-plus-hard-fluid branch. A physical
next comparison must either supply a cosmological state/current exterior
for the aligned static branch, or evolve explicitly specified baryon and
hard-phase initial data on the dynamical branch. It cannot add a fitted
halo profile, discard excitation energy, or impose a new vacuum offset.

## Source custody and independent algebra

- `FINITE_FIELD_COMMON_PHASE_DENSITY_V001.md`, SHA256
  `cb8ec369a4e70f78b0bd54e2142f746bdf414c8982b141ba9027bd4958d7bb59`.
- `CLAMPED_PHASE_EXISTENCE_AND_CONTINUATION_V001.md`, SHA256
  `ccd005abb0c74c736d06cda8cd961f01982d46801a205bb0c4b28cea164282af`.
- `FINITE_GAP_CALIBRATION_STATIC_LENGTH_V001.md`, SHA256
  `e8c4622d1f86a97f63b24499e21c134100edcad5e30e74208503f4af3cd62d36`.
- `SAME_ACTION_RADIATION_ASYMPTOTE_V001.md`: exact action normalization and
  radiation coefficient, read in full for this derivation.

The paired-moment small-domain bound was derived independently with the
results-audit agent; the explicit constants above include the exact
Q_*=2.0012 bound rather than a rounded stronger claim. No saved numerical
outcome was recomputed in preparing this note.
