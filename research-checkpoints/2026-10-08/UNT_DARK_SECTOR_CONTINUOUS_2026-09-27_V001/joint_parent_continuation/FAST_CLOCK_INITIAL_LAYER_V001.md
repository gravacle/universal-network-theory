# Fast soft-clock limit: conserve the initial charge, not the initial slow velocity

2026-09-29. Analytical continuation of the finite-band compensated-clock
equations. No new ODE evolution, mode preparation, fit or change to frozen
evidence. The final small numerical illustration is arithmetic on an already
saved slow-reference fundamental matrix, not a rerun.

## Result

For a fixed positive finite soft band and fixed initial scale factor, the
eta->0 limit has an effective slow initial derivative different from the
unadjusted slow reference. The conserved leading-layer quantity is

    Q=sum w z+beta Y,       Y=u'+Hbar u,

not Y alone. For the actual zero-soft initial data, the phase-averaged slow
matching is

    u_s,i=u_i,
    (u_N)_s,i=f (u_N)_i-(1-f)u_i,     f=beta/Kb.          (1)

Fast oscillations retain positive energy. They do not decay to the static
manifold just because eta is small. The tilt u and total charge Q admit a
slow limit on fixed finite intervals, while their source/derivative and soft
coordinates need not converge pointwise. This is a matched initial-value
limit, not a mechanism selecting cosmological initial data.

## 1. Exact equations and which limit is being taken

Keep the same hard-limit averaged parent and its balanced-state assumptions.
Let tau=H0*t, primes denote tau derivatives, N=ln a, H=H/H0 in this note,
and let z_j=delta_j x_j/H0, u=(k/a)v. Define

    Kb=beta+sum w_j,      D=diag(delta_j^2),
    b(tau)=1.5Kb Omegaexc a^-3,
    Y=u'+Hu,             Q=w^T z+beta Y.

The full equations can be written exactly as

    u'=Y-Hu=(Q-w^T z)/beta-Hu,
    Q'=b u-2H Q,
    eta^2(z''+3H z')+D z=D 1 Y.                         (2)

The second equation is the retained normalized-clock equation. Its exact
integrated form is

    a^2 Q-(a_i^2 Q_i)=integral_(tau_i)^tau a^2 b u d tau. (3)

Ordinary pressureless baryons contribute to H, not b. The same derivation
allows a smooth specified ordinary-radiation background; the illustrative
saved worker intentionally uses only its dust-plus-vacuum background.

Here eta tends to zero at fixed a_i>0, finite interval a_i<=a<=a_f, positive
weights, fixed positive delta_min, beta>0 and fixed normalized initial data.
The physical inertia is m=tau_star^2, eta=H0*tau_star. This parameter is NOT
fixed by acceleration calibration. The limit is not uniform as a_i->0,
delta_min->0, beta->0, or an uncontrolled physical wave number goes to infinity.

## 2. Exact leading fast layer and the matching rule

Use theta=(tau-tau_i)/eta. The leading fast equations have u=u_i and
Q=Q_i constant: the right sides of their theta equations are O(eta).
This is the local leading form of (3), not an assertion that Q is conserved
over the full expanding solution. Eliminating Y gives

    z_theta_theta+L z=(D 1) Q_i/beta,
    L=D(I+1 w^T/beta).                                  (4)

L is similar to a positive symmetric matrix. For
A=diag(sqrt(w_j)/delta_j),

    A L A^-1=D+r r^T/beta,       r_j=sqrt(w_j)delta_j.

Its finite positive frequencies therefore have a bounded oscillatory
propagator in the corresponding weighted norm. The equilibrium is

    z_star=1 Q_i/Kb,           Y_star=Q_i/Kb.             (5)

For the prescribed z_i=z_N,i=0, the leading fast solution is

    z(theta)=z_star-cos(sqrt(L)theta) z_star,
    Y(theta)=Q_i/Kb+w^T cos(sqrt(L)theta)z_star/beta.      (6)

This is a matrix-function identity, not a numerical diagonalization.
Fast-phase averaging removes the cosine but not its quadratic energy.
Initially Q_i=beta H_i[u_i+(u_N)_i]. Substituting the averaged Y of (5)
into u_N=Y/H_i-u gives exactly (1). More generally nonzero initial soft
displacement contributes w^T z_i to Q_i and must be retained.

There is no distinguished physical instant when the oscillations have
ceased. Matching means averaging on an intermediate window with many fast
periods but vanishing cosmic duration. Such a window exists as eta->0 for
the fixed positive band; it does not exist uniformly for a gapless band.

An explicit local correction makes the distinction clear:

    u(theta)=u_i+eta(Q_i/Kb-H_i u_i)theta
          +(eta/beta)w^T L^-1/2 sin(sqrt(L)theta)z_star
          + higher slow-variation terms.                (7)

The fast tilt ripple is O(eta) at fixed band, but Y and z have O(1)
oscillatory amplitudes and z' may be O(eta^-1). One must not assign the
instantaneous source the averaged value without this qualification.

## 3. The fast energy was retained, not dissipated

At fixed leading-layer Q_i the exact conserved quadratic layer energy is

    E_layer=1/2 sum_j (w_j/delta_j^2)(z_theta,j)^2
             +1/2 sum_j w_j z_j^2
             +(Q_i-w^T z)^2/(2beta).                   (8)

It is the soft kinetic/potential plus hard-contact kinetic contribution in
the corresponding reduced action units. The fixed-u gravitational term is
constant on the layer and does not affect this difference. Initial zero-soft
data have E_initial=Q_i^2/(2beta). The stationary value in (5) is
E_star=Q_i^2/(2Kb). Hence the persistent fast excess is

    E_osc=Q_i^2(1/beta-1/Kb)/2 >=0.                     (9)

Replacing the initial derivative by (1) while declaring this fast energy
absent would be incorrect. In linear perturbation theory it is quadratic
in the overall perturbation amplitude and does not create a new background
abundance. Its later nonlinear backreaction or coupling is a separate
calculation. Expansion may damp it; neither phase averaging nor the local
layer proof supplies instantaneous dissipation or thermalization.

## 4. Outer equations and a finite-interval justification

The leading slow variables obey

    u_s'=Q_s/Kb-Hu_s,
    Q_s'=b u_s-2H Q_s,
    u_s''+3H u_s'+[H'+2H^2-b/Kb]u_s=0,                (10)

with u_s,i=u_i and Q_s,i=Q_i. Equation (10) is exactly the same slow
reference generator used in the worker, but with the matched data (1).
It includes baryons through the actual H and retains only the hard density
in b/Kb. It does not replace that coefficient by the total matter density.

The averaging has a useful finite-band control argument. Write
e=z-1 Q/Kb. Its exact equation is

    eta^2(e''+3He')+L e
             =-eta^2 1(Q''+3H Q')/Kb.                  (11)

On a fixed finite smooth background interval, the positive weighted fast
energy bounds e and eta e'. The slow equations bound u,Q and their first
derivatives; Q'' involves u', not u'', and is consequently bounded by those
same variables and e. An energy estimate and Gronwall give uniform finite-
interval bounds for sufficiently small eta, with constants depending on the
fixed band, beta, initial data and background interval.

Integrating (11), the leading boundary term in integral e d tau is
-eta^2 L^-1[e'], hence O(eta). The H e' term is integrated by parts and
the remaining bounded terms are O(eta^2). The same estimate holds with a
smooth bounded slow propagator as weight. Variation of constants in the
first two equations of (2) therefore gives u-u_s and Q-Q_s of O(eta) on
the fixed interval. This is not a uniform numerical error constant for
any of the three tested eta values; the constants become poor at an early
singular endpoint or when the spectral gap closes. It also does not imply
pointwise convergence of z,Y or the instantaneous lapse/acceleration.

More explicitly, let xi=A e with A from section 2 and K=A L A^-1>0.
Its fast energy is [eta^2|xi'|^2+xi^T K xi]/2. For expanding H>=0,
the derivative of its square root is bounded by
eta*|A 1|*|Q''+3HQ'|/(sqrt(2)Kb). The latter source contains bounded
linear combinations of u,Q,xi, but no xi'. Coupled Gronwall therefore
provides the stated uniform finite-interval bound. In the weighted integral
against the slow propagator, integration by parts gives a leading endpoint
eta^2 K^-1 xi'=O(eta); a second integration by parts controls the remaining
xi' integral. Bounded first and second derivatives of that slow propagator
follow from the specified smooth background coefficients. The constant in
the resulting O(eta) estimate depends on K^-1, beta, the interval, derivative
bounds and initial energy; it is not asserted small for current test values.

One useful explicit separated scaling is eta*Omega_star/delta_star ->0
with fixed positive beta/Kb, where delta_star is an actual lower bound on
the owned spectrum and Omega_star bounds expansion, gravitational response
and background derivatives. For example require, for r=0,1,2,

    |d^r H/dtau^r| <= Omega_star^(r+1),
    |d^r(b/beta)/dtau^r| <= Omega_star^(r+2).            (11a)

In particular Omega_star includes sqrt(b/beta), not H alone. These are
sufficient fixed-interval scaling assumptions, not a computed error bound
for a finite eta. Higher-order adiabatic matching requires the corresponding
higher derivative bounds. A finite quadrature's minimum node is larger
than its parent measure's cutoff epsilon; a uniform assertion about that
measure must use delta_star=epsilon (or another proved spectral bound),
not silently use the minimum quadrature node instead.

Well-prepared slow initial data instead satisfy z_i=Y_i 1 and the corresponding
slow derivative condition, up to the desired asymptotic order. They avoid
the large homogeneous fast corrector. Such initial data are a different
preparation from z=z_N=0 and cannot be retroactively substituted into the
current twelve-case test.

## 5. Applying the rule to the saved reference is arithmetic, not a new run

Let F_s(N,N_i) be the saved 2-by-2 slow fundamental matrix in (u,u_N).
For the two zero-soft initial columns, the fast-limit prediction is

    F_matched=F_s [[1,0],[f-1,f]].                       (12)

For case00's epsilon=.001, order64 band, f=.009900999901980102.
Multiplication of the already saved slow matrices gives at a=2

    u_matched=[4.463903258299844, .047225229027244325].

The largest values on those SAME saved sample epochs are approximately
5.821619682 and .0615889774. These are leading fast-limit reference values,
not newly evolved finite-eta outcomes, rigorous between-sample maxima or
evidence that the tested eta=.001 has reached this limit. Its actual result
is retained unchanged.

The case00 receipt used for that arithmetic has SHA-256
`526fb8bb4b0cc00e220bb800f361fa86e6f87bfbecaf458b5dd236031bd7443d`;
its slow solution and original fields were not edited.
The companion FAST_CLOCK_MATCHING_ARITHMETIC_V001.json retains the same
postmultiplication for all four owned spectra, all saved sample epochs,
input hashes and the read-only arithmetic script identity. It does not
add a finite-eta solution or a quadrature-convergence claim.

## 6. What the large observed transfer does and does not constrain

For the inherited H0, the illustrative eta values .001,.1,1 correspond to
tau_star approximately 13.285 million, 1.3285 billion and 13.285 billion
Julian years. They are deliberately cosmological timing controls, not an
inference of a microscopic network clock. At case00's initial epoch,
delta_min/H_i is about7.37e-8, already far below its eta=.001. A sufficient
fast regime must separate the modes from expansion AND the pertinent
internal response rates, so this simple ratio is not a full sufficiency
certificate. It uses that finite quadrature's lowest node; the actual
epsilon=.001 lower cutoff gives a smaller expansion-only ratio. The
gravitational rate sqrt(b/beta), the derivative conditions (11a) and the
finite-interval error constant must also be retained.

The large finite-eta normalized transfer cannot therefore exclude a much
faster physical clock regime. Conversely, (12) does not prove that the native
network supplies such a clock, that formation selects well-prepared data,
or that all other internal initial states are controlled. The exact linear
total dust-gravity interface is unchanged throughout; it does not by itself
bound the separate compensated clock, density or nonlinear amplitudes.
