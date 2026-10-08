# An identifiable joint inverse problem for the common record response

2026-09-27. Additive analytical continuation; no data fit, numerical physics
run, new native law, or changed historical source. The three resident notes
`DYNAMICAL_SHARED_RESPONSE_DISPERSION_V001.md`,
`UNIFIED_INTERNAL_RESPONSE_ENERGY_SCREEN_V001.md`, and
`NATIVE_STIFFNESS_TO_FLAT_ROTATION_SCREEN_V001.md` were read completely after
exact-path flag checks. Their physical density, clock, distance, source and
state interfaces remain conditional.

**Result.** Fitting shared response parameters can be a legitimate inverse
solution. This quadratic model has four propagation/response combinations
after internal-coordinate normalization is removed. Static response plus
one dynamical frequency predicts both full dispersion branches with no
additional fit parameters. Propagation eigenvalues alone can leave a
twofold ambiguity, and no such fit fixes the absolute background energy.
The native finite-source spectrum supplies a concrete independent test of
whether the proposed single internal oscillator is an adequate closure.

## 1. Remove the coordinate redundancy before fitting

At one stationary uniform background use the predecessor's coefficients

    alpha = n0/mu > 0,  A = epsilon_nn,  B = epsilon_nchi,
    D = epsilon_chichi > 0,  Z_t > 0,  Z_s > 0.

Under zeta_new = s zeta, for any nonzero real s,

    B_new = B/s,  D_new = D/s^2,
    Z_t,new = Z_t/s^2,  Z_s,new = Z_s/s^2.                 (1)

This is a change of internal units, including orientation, not a different
physical response. A conjugate source must transform as J_new=J/s so that
J zeta is unchanged. Fitting B,D,Z_t,Z_s separately without a calibrated
internal source introduces an exact flat direction in parameter space.
Convenient invariant combinations are

    h = B^2/D >= 0,       ell^2 = Z_s/D > 0,
    tau^2 = Z_t/D > 0,    Omega^2 = 1/tau^2,
    a = alpha A,         b = alpha h,
    c_chi^2 = ell^2/tau^2 = Omega^2 ell^2.                 (2)

The density chemical-response kernel after eliminating the internal field is

    F(k,omega) = A - h/[1+ell^2 k^2-tau^2(omega+i0)^2].    (3)

The retarded prescription specifies the driven solution; independently
prepared homogeneous internal oscillations are initial-condition data.
Except at B=0, the internal parameters modulo (1) are exactly h,ell,tau.
The sign of B has no meaning without an independently fixed orientation.
For propagation the four combinations are a,b,ell,Omega. If alpha is not
independently calibrated, propagation does not split a into alpha and A,
or b into alpha and h.

## 2. What measurements identify, and an eigenvalue ambiguity

Let a calibrated external chemical source j enter the energy as -j delta n.
For k>0 the density transfer function in this same linear model is

    R_nn(k,omega) := delta n/j
       = [F(k,omega)-(omega+i0)^2/(alpha k^2)]^(-1).       (4)

Thus static response measures F(k,0)=R_nn(k,0)^(-1). A resolved range of k
identifies A,h,ell from its rational shape when h>0; alpha is then supplied
by independent inertia/current calibration or the dynamical source gain.
For example R_nn ~ -alpha k^2/omega^2 when the frequency is large compared
with the retained response rates but still inside the justified continuum
window. This is a conditional scale separation, not permission to extend
hydrodynamics to arbitrarily high frequency. Fixed total number excludes
the uniform k=0 density response. An unstable background does not provide
a realizable equilibrium susceptibility; then (4) is a prepared transient
response with its instability and initial state retained.

If only k ell << 1 is available, F=A-h+h ell^2 k^2+... constrains those
combinations; insufficient resolution of higher terms produces practical
degeneracy. The corresponding warning applies when only k ell >> 1 is
available. Ideal structural identifiability is not experimental precision.

Write lambda_+/-=omega_+/-^2. Exact sum and product give

    S(k) := lambda_+ + lambda_-
           = Omega^2 + (a+c_chi^2) k^2,
    P(k) := lambda_+ lambda_-
           = Omega^2(a-b) k^2 + a c_chi^2 k^4.            (5)

Full eigenvalue curves determine Omega^2, t=a+c_chi^2,
u=a c_chi^2, and L=a-b. The two roots of x^2-t x+u=0 give
the UNORDERED pair {a,c_chi^2}. Each assignment satisfying c_chi^2>0
and b=a-L>=0 is a candidate, with ell^2=c_chi^2/Omega^2.
There can be two admissible assignments, including on stable branches.
Negative u, other sign restrictions, or coincident roots can remove that
ambiguity; it must not simply be ignored in an inverse fit.

Static ell, or mode participation under a density source, labels the pair.
In fact define nu_chi^2=Omega^2+c_chi^2 k^2. Then

    R_nn = alpha k^2 (nu_chi^2-omega^2)
                     /[(omega^2-lambda_+)(omega^2-lambda_-)]. (6)

For b>0 and k>0 its antiresonance locates nu_chi^2 directly. Equivalently,
on a stable nondegenerate branch its two pole weights obey

    R_nn = alpha k^2 [w_+/(lambda_+-omega^2)
                       +w_-/(lambda_--omega^2)],
    w_+ = (lambda_+-nu_chi^2)/(lambda_+-lambda_-),
    w_- = (nu_chi^2-lambda_-)/(lambda_+-lambda_-),
    w_++w_-=1,
    w_+ lambda_+ + w_- lambda_- = a k^2.                  (7)

The relative pole weights therefore recover the bare density stiffness
without requiring the overall source gain. At b=0 the internal pole
cancels from the density response; ell and Omega cannot be determined by
density-only measurements. An independent internal probe would be needed.

## 3. Cross predictions with no additional adjustable parameters

One explicit train/test split is to infer A,h,ell from static source response,
calibrate alpha, and measure the internal gap Omega at very small k. These
inputs predict ALL remaining k-dependent pole positions and density pole
weights through (5)-(7). In particular held-out propagation must satisfy

    S(k)-Omega^2 = [a+Omega^2 ell^2] k^2,
    P(k) = Omega^2 [(a-b) k^2 + a ell^2 k^4].             (8)

These are normalization-independent cross predictions: their coefficients
are fixed by the training observations, with no further fitting to the
held-out branches. They are not claims that no measurement determines any
constant. Conversely, after resolving the eigenvalue ambiguity, propagation
predicts the entire static response shape and range. With calibrated R_nn,
one can reconstruct the induced susceptibility directly as

    T(k,omega) = A - R_nn^(-1) - omega^2/(alpha k^2)
               = h/[1+ell^2 k^2-tau^2 omega^2].           (9)

Away from its poles and with h>0,

    T(0,0)/T(k,omega) = 1+ell^2 k^2-tau^2 omega^2.        (10)

Here T(0,0)=h denotes a local-kernel limit, not an allowed total-number
variation. Curvature of this inverse-response surface beyond the displayed
linear dependence is a direct failure of this constant-coefficient closure.
Finite damping, extra retained modes or background drift would require an
owned extension and new tests, not silently altered residuals.

Additional consequences reuse those same parameters:

    relaxed sound coefficient = a-b,
    stability at all continuum k: a>=b,
    for 0<a<b: k_crit^2 = (b/a-1)/ell^2,
    for a=0,b>0: sup_k gamma^2 = b/ell^2.                (11)

The last supremum and the phrase "all continuum k" describe the mathematical
completion. A finite native cutoff may prevent observing the limit. None
of (8)-(11) separately establishes physical causality, nonlinear viability
or acceptable cosmic structure formation.

## 4. A short native matching test with finite sources

The existing finite-star result already supplies a source-owned starting
point, without calling q physical density or f a gravitational field.
At the conditionally selected ground state of H_eta=H+eta Q, apply a small
probe -j(t)Q. Let Delta_r=E_r-E_0>0 and Q_r0=<r|Q|0>. In the clock of this
finite Hamiltonian, retaining its explicit hbar normalization, its exact
zero-temperature retarded response is

    chi_Q(omega) = sum_(r>0) 2 Delta_r |Q_r0|^2
                      /[Delta_r^2-hbar^2(omega+i0)^2].    (12)

This is a response of the declared selected state, not a claim that native
blank-prewait dynamics prepares it. Below the first coupled transition,

    chi_Q = M0 + M2 omega^2 + M4 omega^4 + ...,
    M0 = 2 sum |Q_r0|^2/Delta_r,
    M2 = 2 hbar^2 sum |Q_r0|^2/Delta_r^3,
    M4 = 2 hbar^4 sum |Q_r0|^2/Delta_r^5.                 (13)

The static note gives M0=chi_Q(0)>0. Low-frequency inversion fixes the
effective single-coordinate coefficients, in this native normalization,

    chi_Q^(-1) = D_Q-Z_Q omega^2+O(omega^4),
    D_Q=1/M0,  Z_Q=M2/M0^2,
    tau_Q^2=Z_Q/D_Q=M2/M0.                              (14)

These values are determined by the same finite spectral response, rather
than freely chosen oscillator parameters. A single oscillator fitted to
M0 and M2 predicts M4=M2^2/M0. Positivity of the spectral weights instead
gives the exact native inequality

    M0 M4 >= M2^2.                                      (15)

To prove it, set p_r=(2|Q_r0|^2/Delta_r)/M0 and
x_r=hbar^2/Delta_r^2. Then sum p_r=1, M2/M0=<x>,
M4/M0=<x^2>, and (15) is Var_p(x)>=0. Equality holds exactly when all
Q-coupled transitions have the same gap. Strict inequality measures the
extra spectral content missed by an exact single-oscillator ansatz; a
low-frequency approximation can still be controlled by its higher terms.
The ratio M0 M4/M2^2 and tau_Q are invariant under Q rescaling when its
source is transformed consistently. No numerical spectrum was run here.

The shortest further matching requirements are specific. A calibrated
density or compression source, with a declared physical volume map, must
determine the mixed response and A on the SAME branch; a uniform conserved
number source in a fixed-number sector cannot do this. For independent
static coordinates and the corresponding sources, an invertible passive
susceptibility matrix has inverse equal to the energy Hessian, so its
off-diagonal entry must be the same B in both force directions. This is a
reciprocity test, not permission to choose two couplings independently.
Cross-cell source response on an owned spatial map must then determine
the k^2 term of the inverse internal response and hence Z_s. One isolated
star cannot supply a physical distance or spatial range. Volume, energy,
clock and source-work calibrations convert (14) to continuum coefficients;
they are not inferred by identifying Q with chi by name.

## 5. What inverse solving would and would not establish

A forward problem fixes the common mechanics and parameters, states,
sources and boundaries, then predicts observations. Its legitimate inverse
uses observations to constrain that same common mechanics. A concrete
joint inference uses one universal vector (a,b,ell,Omega), or a small set of
coefficients for state-dependent functions DERIVED from one energy and
source map, across all systems. Environment-dependent coefficients are
evaluated at each measured state using that shared law. Independently
chosen functions for each galaxy would not test a shared mechanism.

Source mass distributions, inclinations, boundary fields and preparation
can be system-specific nuisance inputs when the forward model requires
them. They need independent constraints and propagated uncertainties;
unconstrained nuisance fields can otherwise absorb the desired prediction.
Fix the training observables and shared functional form before evaluating
held-out modes, source profiles, galaxies or epochs. Propagate calibration,
parameter, initial-state and controlled truncation uncertainties jointly.
The exact sum/product and spectral identities above make concrete tests
available before any claim of a successful astronomical fit.

In particular a positive constant-coefficient Yukawa response from a
localized isolated spherical source gives, outside that source,

    Phi_chi(r) = -C exp(-r/ell)/r,  C>0,
    v_chi^2(r) = C exp(-r/ell)(1/r+1/ell).                (16)

It tends to zero; the infinite-range limit is Keplerian. One such response
therefore does not explain a nonzero asymptotically flat rotation curve.
An extended record distribution, derived nonlinear or varying-background
response, or other owned change would have to supply additional physics.
This note proposes an identifiable test, not a dark-matter success.

Finally epsilon->epsilon+C leaves every perturbation identity above
unchanged while shifting rho by C and p by -C. These experiments cannot
recover the absolute background term or predict its accelerating stress.
That requires complete matched metric/volume response. Internal-coordinate
units and origin remain conventional; a physical internal calibration can
fix the convention but not add a new force parameter. Propagation without
calibrated density/inertia does not recover absolute mu or n0 separately.
An initial cosmic record population, formation history, and the missing
network-to-physical source/geometry maps likewise are not fixed by these
local transfer functions. Inverse fitting can constrain a common theory;
its success would not by itself turn those unearned interfaces into native
derivations.
