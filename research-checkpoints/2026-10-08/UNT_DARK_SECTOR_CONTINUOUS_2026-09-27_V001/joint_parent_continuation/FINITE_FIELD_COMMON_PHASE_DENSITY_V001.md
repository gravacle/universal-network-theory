# Finite-field common-phase density and its coupled static response

2026-09-29. Analytical continuation of the declared macroscopic alpha-one
finite-gap action. No numerical science, new fit, chosen galaxy radius,
new preparation or frozen-file edit. The result supplies a nonlinear
constitutive screen, not a galaxy solution or a new density profile.

## 1. The question is nonlinear density, not the cosmic linear length alone

Use the same finite-R calibration, hard weight beta, soft ground spectrum,
Kb, bounded source h(g)=g/sqrt(1+g^2/S^2), and matched DeltaU. Fields g,h
are in units of gstar; Phi=ln(N/N_b), and the reference boundary has h_b=0.
The one common hard phase fixes

    omega_R(I,h)=omega_R(I_b,0)*exp(-Phi).                 (1)

This determines I locally on the declared boundary-connected branch. It
does not permit an independently fitted I(r). In particular the exact
spatial derivative is

    grad I=-(omega/e_II) grad Phi+(B_H,I/e_II) grad h,
    B_H=-e_h.                                           (2)

For the small-source hard branch B_H,I<0. An outward falling h can then
oppose the density decrease caused by an outward increasing Phi. Neither
constant density nor an assumed monotone density profile can replace (1).
In any dimension the same coupled gradients enter the field equation.

The small cosmic coefficient K0 and its short linear static length apply
only near I_b,h=0. They do not exclude a finite-field branch with a much
larger soft principal coefficient and a large, solved hard density contrast.
The converse matters equally: increasing the principal coefficient does
not remove the hard density's self-gravity or guarantee a galaxy solution.

## 2. Exact unit-gap reduction and stable frequency inversion

Scale the original tilted quartic without changing its coefficients:

    y=R*z, eta=h/R^2, i=I/R^3,
    e_R=R^4 epsilon(i,eta), omega_R=R*Omega(i,eta),
    U/R^4=z^2/2+z^4/4-eta*z.

Let r>0 be the dimensionless half-span of the turning points, and c their
center. With theta in [0,pi], write

    c^3+(1+r^2)c=eta,   z=c+r*cos(theta),
    q=2+(z+c)^2+2c^2+r^2,
    i=r^2/(sqrt(2)*pi)*integral sin^2(theta)*sqrt(q) dtheta,
    L=mean_uniform(q^(-1/2)),  Omega=1/(sqrt(2)*L).        (3)

The source mean uses the normalized time weight q^(-1/2): b=<z>_time,
so B_H=R^2*b. All action and moment integrals are endpoint regular.

Cold calibration can make Omega_b-1 extremely small. Compute the excess
without subtracting two rounded frequencies. For o=q-2,

    delta=-mean_uniform{o/[sqrt(q)*(sqrt(2)+sqrt(q))]},
    Omega-1=-delta/(1+delta),
    target_excess=(Omega_b-1)*exp(-Phi)+expm1(-Phi).       (4)

Equation (4) is exact, not a small-amplitude expansion. Solve the frequency
excess equation on the branch connected to the boundary. Frequency need
not be monotone on every tilted-orbit branch: verify Omega_r>0 and do not
select a disconnected root after a fold. At I=0 use the minimum c0 from
c0+c0^3=eta and Omega0=sqrt(1+3c0^2). Its stable excess is
3c0^2/[sqrt(1+3c0^2)+1]. This checks the empty/occupied boundary rather
than concealing a nonexistent occupied root.

## 3. Exact derivatives suitable for a small arithmetic screen

Put d=1+r^2+3c^2. Derivatives at fixed r or eta are

    c_r=-2cr/d, c_eta=1/d,
    q_r=12c*c_r+4(c+r*c_r)cos(theta)
                                  +2r[1+cos^2(theta)],
    q_eta=12c*c_eta+4r*c_eta*cos(theta),
    Omega_a=Omega*mean_uniform(q_a*q^(-3/2))/(2L).

An especially stable positive action derivative follows from endpoint
energy differentiation and i_e=1/Omega:

    epsilon_r=r[d-4c^2*r^2/d],   i_r=epsilon_r/Omega>0,
    i_eta=r^2/(2sqrt(2)*pi)
                     *integral sin^2(theta)*q_eta/sqrt(q) dtheta.
                                                               (5)

The positive bracket in epsilon_r equals
[(1+(r-c)^2+2c^2)(1+(r+c)^2+2c^2)]/d. Direct differentiation of
the action integral gives an independent equality check for i_r.

To avoid canceling the almost harmonic susceptibility against one, use
the exact orbit-averaged equation b=eta-M3, M3=<z^3>_time. For a=r,eta,

    (M3)_a=<3z^2 z_a>_time
                   -(1/2)Cov_time(z^3,q_a/q),
    z_r=c_r+cos(theta), z_eta=c_eta,
    b_i=-(M3)_r/i_r,
    b_eta|i=1-(M3)_eta+(M3)_r*i_eta/i_r,
    epsilon_ii=Omega_r/i_r.                              (6)

Retain 1-b_eta|i as the last two small terms, rather than subtracting
the final susceptibility from one. Reflection parity gives b=b_i=i_eta=0
at eta=0. The Maxwell check is Omega_eta|i=-b_i.

The inherited physical derivatives are exactly

    e_II=epsilon_ii/R^2, B_H,I=b_i/R, B_H,h|I=b_eta|i,
    B_H,h|Omega=b_eta|i+b_i^2/epsilon_ii.                 (7)

An independent way to compute the last line is
b_eta|r-b_r*Omega_eta|r/Omega_r. Agreement tests the phase-equilibrium
chain rule without finite differencing a tiny source increment.

At r=0, k=1+3c0^2 supplies exact one-sided occupied limits:

    epsilon_ii=3(1-7c0^2)/(4k^2),
    b_i=-3c0/k^(3/2), b_eta|i=1/k,
    b_eta|Omega=(1+5c0^2)/[k(1-7c0^2)].                  (8)

The empty-connected convex branch starts with c0^2<1/7. An empty copy
does not inherit an occupied J term just because its one-sided limit can
be written. Record a fold, branch loss or failed Maxwell/control identity.

For absolute energy use epsilon_min=-c0^2/2-3c0^4/4 and the stable shift
c-c0=-cr^2/(1+c^2+c*c0+c0^2). With x_plus=r+c-c0,

    epsilon_exc=x_plus^2[(1+3c0^2)/2+c0*x_plus+x_plus^2/4],
    epsilon=epsilon_min+epsilon_exc.

Do not reset this energy at each field. A cancellation-safe finite-source
pressure readout is pi_H/R^4=<z^4>_time/4+eta*b/2, equal to
i*Omega-epsilon by the virial identity. The common DeltaU is unchanged.

### A sufficient all-radius branch certificate

There is a useful exact certificate, stronger than checking a finite set
of sampled slopes: if eta^2<1/12, then Omega_r>0 for every r>0.
Pair theta and pi-theta, and put Ctheta=|cos(theta)|. Their quantities are

    q_plus,minus=q0 +-4cr*Ctheta >=2,
    (q_r)_plus,minus=A +-B*Ctheta,
    A=2r(1+Ctheta^2)-24c^2*r/d,
    B=4c(1-2r^2/d),   |B|<=4|c|.

For weights w_plus,minus=q_plus,minus^(-3/2), the exact tanh/log identity
and log(1+x)<=x give

    |w_plus-w_minus|/(w_plus+w_minus)
        <=(3/4)|ln(q_plus/q_minus)|<=3|c|r*Ctheta.

The weighted pair's mean q_r is therefore at least

    2r[(1-12c^2)+(1-6c^2)Ctheta^2]
                         >=2r(1-12eta^2)>0,

using d>=1 and |c|<=|eta|. Integration proves the claim. At r=0 the
one-sided epsilon_ii in (8) is also positive under this sufficient bound.
No claim that the bound is necessary, or that all tilted quartics harden,
is made. Since |h|<=S, S/R^2<1/sqrt(12) certifies this branch for all
fields and all radii in the same finite-gap parent.

A conservative explicit lower bound over r<=r_max, |eta|<=eta_max is

    epsilon_ii >= (1-12eta_max^2)
      /[(2+6eta_max^2+2eta_max+2r_max^2)
                                 *(1+r_max^2+3eta_max^2)].

Here |cr|<=|eta|/2 bounds q from above, Omega^2>=1, and
i_r<=r*d/Omega. This controls branch inversion but does not by itself
prove positive K_L, static metric stability or a boundary-matched galaxy.

## 4. Both principal coefficients and the lapse reaction are compulsory

Soft minima satisfy delta_j^2*y_j+y_j^3=delta_j*h. Define

    B_s=sum_soft w_j*delta_j*y_j,
    chi_s=sum_soft w_j*delta_j^2/(delta_j^2+3y_j^2),
    B=B_s+beta*B_H, F=h'*B,
    K_T=Kb-F/g,
    K_L=Kb-h''*B-h'^2[chi_s+beta*(b_eta|i+b_i^2/epsilon_ii)],
    F_Phi=-h'*beta*R^2*Omega*b_i/epsilon_ii,
    J=beta*R^4[Omega^2/epsilon_ii+3i*Omega].              (9)

At g=0 take the continuous limits. Both K_T and K_L are required; a
fixed-I force derivative omits the nonnegative square in K_L and can
give a false ellipticity conclusion. F_Phi is a separate lower-order
coefficient, not another fitted parameter. J is the fixed-g derivative
-partial_Phi(E+3Pi), including the same hard density and pressure.

The exact envelope identity

    partial_g(E+3Pi)=2F-F_Phi                             (10)

is a useful cross-check. In a locally frozen flat weak equation, the
first-order derivative contributions from delta D and delta(E+3Pi)
combine into -2F times the derivative along the background field, not
two independently adjustable density-gradient forces. Spatial gradients
of the coefficients, the metric constraints and the full -Kb*g^2 term
must still be restored at their qualified order. A global disk equation
cannot be replaced by one constant K/J ratio.

## 5. Large density contrast can remain a controlled hard expansion

For i<<1 and |eta|<<1, direct harmonic averaging of the original quartic
gives the normal-form expansion

    epsilon=i-eta^2/2+3i^2/8+3eta^2*i/2+eta^4/4
                         +O(i^3+i^2 eta^2+i eta^4+eta^6),
    Omega=1+3i/4+3eta^2/2+O(i^2+i eta^2+eta^4),
    b=eta(1-3i-eta^2)+O[eta(i^2+i eta^2+eta^4)].          (11)

This expansion retains the source/contact terms. If
Delta=Omega_b*exp(-Phi)-1, the occupied continuation is

    i=(4/3)Delta-2eta^2+O(Delta^2+Delta eta^2+eta^4)
      =i_b-(4/3)Phi-2eta^2+O(i_b^2,Phi^2,i_b Phi,
                                           i_b eta^2,Phi eta^2,eta^4).
                                                               (12)

Thus |Phi|/c_b^2 can be enormous while i=O(|Phi|) remains small. The
cosmic density linearization has failed, not necessarily the controlled
quartic-orbit expansion. Excitation energy is approximately R^4*i;
compare it to its tiny cosmic R^4*i_b, retaining the absolute minimum
and polarization-divergence terms in the gravitating stress separately.

The phase-equilibrium susceptibility is

    b_eta|i=1-3i-3eta^2+O(i^2+i eta^2+eta^4),
    b_i^2/epsilon_ii=12eta^2+O(i eta^2+eta^4),
    b_eta|Omega=1-3i+9eta^2+O(i^2+i eta^2+eta^4),
    F_Phi=4beta*h*h'[1+O(i+eta^2)],
    J=(4/3)beta R^4[1+O(i+eta^2)].                       (13)

The source frequency shift in (12) and the +12eta^2 square in (13) cannot
be discarded merely because the local density contrast is large. Since
|h|<=S, S/R^2 is a uniform hard-source expansion parameter. A verified
small i plus small S/R^2 is a constructive controlled constitutive window;
it is not proof of a full boundary-matched galaxy or its formation.

## 6. How finite field changes the length, without fitting a length

Define the local frozen principal/reaction scales only as diagnostics:

    ell_T,L=(c_light^2/gstar_SI)*sqrt(K_T,L/J),
    mu_T,L=K_T,L/Kb.                                    (14)

They are not global radii, a scalar replacing the anisotropic operator,
or a dynamical Jeans dispersion. In the controlled regime (11),

    ell_T,L=(c_light^2/(gstar_SI*R^2))
                    *sqrt[3K_T,L/(4beta)]*[1+O(i+eta^2)],
    (H0*ell_T,L/c_light)^2
       =chi_b*mu_T,L/(2Omega_exc)*[1+O(i+eta^2)],
    ell_T,L/ell_cosmic
       =sqrt[(K_T,L/K0)*(J_b/J)]
       approximately sqrt[K_T,L/(3beta*chi_b)].          (15)

Here chi_b=e_b/R^4 uses the SAME finite-R cosmic calibration. The last
formula quantifies why a very small cosmic length cannot rule out a much
larger finite-field response: K_T,L can grow from 3beta*chi_b to a finite
soft-network coefficient. At fixed cosmic energy and physical gstar,
the resulting finite-field length scales as R^-2, whereas the cosmic
linear length scales as R^-4. Neither length is independent of the shared
spectrum/calibration, and J still grows as R^4.

Whether (15) is a galactic scale is a calculation with the already owned
gstar,R,K_T,L, not a permission to fit a radius or infer success from
one coefficient. The same result also warns that the local hard source
may become substantial: suppressing its cosmic pressure does not allow
its nonlinear density to be omitted. In particular the old fixed-record
or fixed-action field tables do not test this common-phase branch.

## 7. Smallest exact next screen

For every already declared finite-gap calibration, retain its reference
I_b, spectrum, gstar,S and DeltaU. At prospective common physical fields
and lapse depths, convert g=g_SI/gstar and solve (4), not a rescaled old
force table. Record all branch outcomes and compute:

- I/I_b, the common-frequency residual and epsilon_ii;
- absolute hard minimum/excitation, pressure, soft energy and the unchanged
  DeltaU; no re-preparation or energy subtraction;
- B, F, K_T, K_L, F_Phi and J from (9), including the square term;
- fixed-I_b response as a distinctly labeled comparison, not the solution;
- local ell_T,L and exact versus controlled asymptotic ratios;
- parity, Maxwell, virial, action/period and chain-rule identities, with
  separate quadrature refinement and branch loss retained.

This screen does not choose I from galaxy residuals and does not prescribe
its radial gradient. It makes the density/polarization/gradient coupling
runnable before a full metric/clock/disk solve. Positive coefficients are
necessary branch diagnostics, not a substitute for conservation, physical
outer matching, ordinary-matter support or nonlinear existence.

## Source identities

- MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md:
  64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3.
- FIXED_ACTION_FINITE_FIELD_REUSE_V001.md:
  9f136a7493ce0a9d547148c88273f273bbb78a874e0ab334cbc77b137a2f7a9c.
- FINITE_GAP_CALIBRATION_STATIC_LENGTH_V001.md:
  e8c4622d1f86a97f63b24499e21c134100edcad5e30e74208503f4af3cd62d36.

All prior sources and outcomes remain unchanged. The macroscopic scalar
state is explicit; no native spectrum, physical clock, isotropic vector
preparation or empirical galaxy success is asserted by these equations.
