# Finite response modes with the lapse, shift and clock retained

2026-09-28. Analytical continuation of EXPLICIT_MODE_COSMOLOGY_PATHWAY.md.
No numerical worker, extra spatial-gradient operator, fitted kinetic function,
or modification of the frozen static model.

## Decision

For a finite positive band, the unexcited conditional parent has a regular
constrained longitudinal oscillator sector. Its nonzero frequencies are
positive and interlace the individual mode frequencies. The structural
contact cancellation leaves a **conserved static polarization sector**, not
a negative-gradient oscillator. A frozen-source susceptibility test alone
would miss the shift/clock constraint and give the wrong mode equation.

There is also an exact expanding-de-Sitter extension: the conserved quantity
becomes a comoving polarization charge; the internal modes are damped, while
its linear gravitational density decays as a^-3 and its metric potentials
as a^-1. No positive mean dust abundance follows from that signed linear
polarization. These results concern the specified finite-band classical
vacuum scalar sector, not full nonlinear or continuum hyperbolicity.

## 1. Fix the parent and the background comparison

Take N positive weights w_j, gaps delta_j, inertias m_j, and kappa>0.
Retain the complete action (1) of EXPLICIT_MODE_COSMOLOGY_PATHWAY.md, with

    K_b=kappa*sum_j w_j,
    C=2M²/K_b,   M²=1/(8 pi G),
    b_j=w_j*kappa*delta_j,
    M_jl=w_j*m_j*delta_jl,
    K_jl=w_j*kappa*delta_j²*delta_jl.

Bold M and K below are these positive matrices; M² without bold denotes
the gravitational coefficient. The quartic and bounded-source corrections
begin beyond this zero-field quadratic problem. Their absence from its
linear determinant is not permission to omit them from nonlinear motion.
The finite-band contact is the contact of THESE SAME retained modes. Keeping
the contact of absent modes would define another theory with a response floor.

The matched positive DeltaU makes de Sitter, not Minkowski, the exact empty
background. Sections 2–4 first give the zero-curvature quadratic comparison:
it is exact if the homogeneous constant is set to zero in that comparison,
or a local short-scale diagnostic with background curvature terms neglected.
It must not be used to certify arbitrarily slow modes of the positive-J(0)
universe. Section 5 retains its actual constant positive H and closes that
particular background limitation without changing DeltaU.

Use periodic perturbations or boundary conditions removing the displayed
spatial surface terms. Consider nonzero spatial wave number k. Homogeneous
k=0 perturbations require their own constraints and are not obtained by
dividing these equations by k and then taking its limit.

## 2. Unreduced local scalar action

In unitary clock gauge T=t choose

    N=1+n,   N_i=partial_i beta,
    gamma_ij=exp(2 zeta)*delta_ij,
    y_j,i=partial_i sigma_j.

The y constraint gives y^0=0. At first order its projected normal derivative
is grad sigma_dot, and a_i=partial_i n. The full quadratic scalar action is

    S2 = integral dt d³x {
       M²[-3*zeta_dot²+2*zeta_dot*Delta beta
            +(grad zeta)²-2n*Delta zeta]
       +C*sum_j w_j [m_j*(grad sigma_dot_j)²/2
             -kappa*delta_j²*(grad sigma_j)²/2
             +kappa*delta_j*grad n.grad sigma_j] }.             (1)

The Einstein terms agree with the directly checked ADM expansion in
K0_FLRW_SCALAR_DECISION.md at H=0 before any constraint elimination.
No -j*(grad n)² term is appended: the explicit modes generate that static
term when eliminated. Appending it would double-count the response.

Define S=b^T sigma. The shift, lapse, mode and zeta equations give

    zeta_dot=0,
    2M²*zeta+C*S=0,  hence zeta=-S/K_b and S_dot=0,
    M*sigma_ddot+K*sigma=b*n,
    beta_dot=-zeta-n.                                        (2)

The last equation uses the shift convention N_i=partial_i beta. In
Newtonian gauge the scalar potentials are Phi=n+beta_dot and Psi=-zeta,
so Phi=Psi=S/K_b is time independent in this local vacuum comparison.
The lapse n may oscillate relative to the preferred clock; it is not by
itself the gauge-invariant metric potential.

For prescribed conserved S, differentiating the constraint twice fixes

    n=(b^T M^-1 K sigma)/(b^T M^-1 b).                         (3)

The denominator is strictly positive. Thus the system is a finite constrained
ordinary differential equation, not an unsolved lapse division by zero.

## 3. Positive constrained energy and the exact determinant

For a Fourier mode, substituting lapse and shift constraints gives the
following local reduced Lagrangian, restricted to S_dot=0:

    L_red=(C*k²/2)[sigma_dot^T M sigma_dot
                      -sigma^T K sigma+S²/K_b].               (4)

Weighted Cauchy–Schwarz gives

    (sum w_j*kappa*delta_j*sigma_j)²
        <= (sum w_j*kappa)*(sum w_j*kappa*delta_j²*sigma_j²),
    sigma^T K sigma-S²/K_b >= 0.                              (5)

Equality means delta_j*sigma_j is the same for all j. Put
d_j=1/delta_j and sigma0=(S/K_b)*d. Then b^T d=K_b, K d=b,
and sigma=sigma0+z with b^T z=0 has potential exactly z^T K z.
Both this potential and z_dot^T M z_dot are strictly positive for nonzero
finite-band tangent variations. The equality family is static because
S_dot=0; it is not an oscillator allowed to drift along the null direction.
The local conserved quadratic Hamiltonian on each fixed-S sector is

    H2=(C*k²/2)[z_dot^T M z_dot+z^T K z] >= 0.                 (6)

For exp(-i omega t) with omega nonzero, the constraint is b^T sigma=0.
The exact characteristic determinant is

    D(y)=det [[K-y*M, -b], [b^T, 0]],   y=omega²,
         =det(K-y*M)*chi(y),
    chi(y)=b^T(K-y*M)^-1 b
          =sum_j w_j*(kappa*delta_j)²
                           /(kappa*delta_j²-m_j*y).           (7)

The determinant, not an expression with uncanceled pole denominators, is
the characteristic polynomial. In particular the condition is chi(y)=0
where that expression is finite, **not K_b-chi(y)=0**. The latter would
freeze out a metric/clock constraint and describe another source problem.

To count all roots set Omega_j²=kappa*delta_j²/m_j and
c_j=sqrt(w_j)*kappa*delta_j/sqrt(m_j). Up to the positive constant det M,

    D(y)=sum_j c_j²*product_(l!=j)(Omega_l²-y).                (8)

This degree N-1 polynomial has all its roots strictly positive. For distinct
ordered poles, chi is strictly increasing between them, from minus infinity
to plus infinity, giving one root in every adjacent interval and none below
the first or above the last pole. Equivalently these are eigenvalues of the
positive mass-normalized stiffness restricted to the codimension-one
constraint, so they lie between the smallest and largest Omega_j².

Coincident poles need an explicit qualification. If a distinct frequency has
multiplicity r, its r-1 source-orthogonal combinations remain eigenmodes at
that positive frequency. Combining the squared source weights at each
distinct pole leaves one bright root between neighboring distinct poles.
Those dark modes plus bright roots give N-1 in total. The scalar rational
function's visible zeros alone would miss the dark modes. For N=1 there is
no independent oscillatory longitudinal mode, only the conserved sector.

## 4. What kind of response is well posed?

For a finite-band linear forcing f on the tangent system with S fixed, the
constrained retarded resolvent is, away from removable pole expressions,

    A(omega)=K-(omega+i0)²*M,
    R(omega)=A^-1-A^-1*b*[b^T A^-1 b]^-1*b^T A^-1.            (9)

It maps to b^T sigma=0 and has only the positive-frequency physical poles
just counted. Its apparent singularities must be evaluated through the
matrix system, retaining dark modes at repeated poles. This is a finite
causal response statement; f must itself come from an owned source before
being assigned a physical interpretation.

No growing exponential and no negative spatial-gradient oscillator appear
in this finite nonzero-k longitudinal vacuum sector. There is nevertheless
no quadratic spatial restoring energy for its conserved S family. The
collective internal frequencies do not increase with k because the proposed
parent supplied no independent spatial mode-gradient operator. Transverse
mode components do not couple to grad n at this order and retain their
positive local oscillator frequencies.

Thus this is not a proof of a uniform continuum energy norm, a propagating
sound speed or nonlinear hyperbolicity of gravity plus the clock. As
delta_min tends to zero, internal frequencies can accumulate at zero and
the finite-band inverse estimates are not uniform. The finite-time/source
window and actual inertia still have to be matched. Constraint solving is
spatially nonlocal, and ordinary matter, excited backgrounds or a different
spatial operator require their own linear system.

## 5. The actual positive-J(0) de Sitter branch

Now retain the same DeltaU and take H>0 constant with
3M²H²=C*DeltaU, ordinary perturbations absent, and background y_j=0.
Let x_j denote physical longitudinal components, with real Fourier phases
chosen so that the acceleration coupling is +(k/a)*n*b^T x. Define S=b^T x.
The scalar ADM Einstein action is its previously verified de Sitter form:

    M²*a³[-3(zeta_dot-Hn)²+(grad zeta)²/a²
             -2n*Delta zeta/a²
             +2(zeta_dot-Hn)*Delta beta/a²].

The shift imposes n=zeta_dot/H. The remaining Einstein spatial terms cancel
up to the stated endpoint boundary term, as in the pure-Einstein check of
the earlier K0 calculation. The EXACT retained-mode quadratic action becomes

    L2=C*a³[ x_dot^T M x_dot/2-x^T K x/2
                          +(k/(aH))*zeta_dot*b^T x ].         (10)

It is not obtained by taking H to zero after division by H. The cyclic
zeta equation and the mode equation give

    d[a²*S/H]/dt=0,    S=S0*a^-2,
    M(x_ddot+3H*x_dot)+K*x=b*ell,
    ell=(k/a)*n=(k/(aH))*zeta_dot.                            (11)

This explicitly retains the clock/polarization charge. In its zero-charge
sector, choose any fixed basis B with b^T B=0 and write x=B*q. Then

    (B^T M B)(q_ddot+3H*q_dot)+(B^T K B)q=0.                  (12)

Both matrices are positive. The normal coordinates have the SAME collective
Omega² determined by (7)-(8), with temporal exponents

    s=-3H/2 +/- sqrt(9H²/4-Omega²).

Every real part is negative for a finite positive band. For nonzero charge,
write x=x0+z with x0=(S/K_b)*d and b^T z=0. The tangent equation has forcing

    B^T M(z_ddot+3H*z_dot)+B^T K z
                              =2H² B^T M x0,                 (13)

which decays as a^-2. If Omega²=2H² it produces t*a^-2 rather than a growing
resonance. Thus the physical finite-band internal coordinates remain a
sum of decaying modes in both charge sectors.

The first-order stress here comes only from the acceleration coupling:
the kinetic and V0 energies start at quadratic order in y. Its lapse
variation is delta L/delta N=-C*div B, so its energy perturbation is

    delta rho=+C*div B,
    delta p=0,    delta momentum=0,    delta anisotropic stress=0.

For the phase convention of (10), div B=-(k/a)S. It follows that
delta rho scales as a^-3, Phi=Psi=a*S/(K_b*k) scales as a^-1, and all
nonzero-frequency zero-charge internal modes have zero metric stress at
linear order. On a periodic domain this polarization density has zero
mean; it is not a positive cosmological material background.

### Physical clock tilt, including very slow internal modes

The preferred-coordinate lapse n can grow when an internal mode decays more
slowly than a^-1. Its physical significance can be decided explicitly,
rather than assumed away. In Newtonian gauge write T=t+pi and

    ds²=-(1+2Phi)dt²+a²(1-2Psi)dx².

The spatial velocity of the unit normal relative to the Newtonian-frame
orthonormal observers is, at first order,

    v_hat_i=-partial_i pi/a,
    a_hat_i=v_hat_dot_i+H*v_hat_i+partial_i Phi/a.             (15)

This follows directly from normalizing -partial T: its temporal component
is u_0=-(1+Phi), with no remaining pi_dot in that component. Thus (15)
measures the physical tilt, not the normalization of a clock label.
For the real longitudinal phase convention used in (10),

    v_dot+H*v=ell-(k/a)*Phi,
    v(t)=a(t)^-1 {a(t0)*v(t0)
                    +integral_t0^t a(t')[ell-(k/a)Phi]dt'}.  (16)

Every homogeneous internal solution has ell proportional to exp(s*t)
with Re s<0, with polynomial factors at a repeated root. For s!=-H its
particular tilt is ell_s*exp(s*t)/(s+H). If s=-H, the resonance is
ell_s*t*exp(-H*t), which also decays. The metric-gradient term and the
charged forcing scale as a^-2, possibly multiplied by a polynomial in t,
and yield decaying particular tilts plus the homogeneous a^-1 term.

In particular, for a finite very slow mode Omega<<H,

    s_slow=-Omega²/(3H)+O(Omega^4/H³),
    v_slow approximately ell_slow/H,

so the physical tilt decays slowly even when n=a*ell/k increases. There
is no growing physical tilt in this finite-band linear calculation. The
decay is not uniform as the smallest Omega tends to zero; its exact zero
limit permits bounded persistent tilt rather than this strict decay.

The gauge relation zeta=-Psi-H*pi and momentum equation Psi_dot+H*Phi=0
also give n=Phi-pi_dot=zeta_dot/H, confirming that the two calculations
describe the same normal. Large clock-label derivatives can invalidate a
particular perturbative T-coordinate expansion; the result above concerns
the linear metric and unit-normal invariants. It is not a proof of global
nonlinear foliation regularity or of uniform validity for arbitrary initial
amplitude and infinite time.

### Independent low-frequency consistency check

If all relevant time derivatives and H are slow compared with the finite
band, algebraically eliminating x in (10) gives

    x approximately K^-1*b*(k/(aH))*zeta_dot,
    b^T K^-1 b=K_b,
    L2 approximately M²*a*k²*zeta_dot²/H².                   (14)

This is exactly the positive j=-1 reduced K0 action already derived from
the static J theory. The full finite system supplies its resonances and
memory instead of interpreting a truncated higher-derivative expansion
as a fundamental new degree of freedom.

The new conclusion is therefore specific and constructive: in this common
finite-mode completion, structural criticality is compatible with a positive
constrained response and a decaying de Sitter vacuum scalar sector. It does
not itself supply an excitation abundance, native source matching, nonlinear
stability, or an observational cosmology.
