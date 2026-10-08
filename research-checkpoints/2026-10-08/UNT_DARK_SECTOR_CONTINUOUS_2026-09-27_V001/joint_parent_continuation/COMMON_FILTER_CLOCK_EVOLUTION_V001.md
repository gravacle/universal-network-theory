# One averaging rule for acceleration and expansion

2026-10-05 UTC. New conditional dynamical hypothesis, separate from the
constant unfiltered trace regulator. Root and two internal analytical
reviewers checked the scalar, forced-response and propagation conclusions.
No numerical test or fit is claimed by this analytical note.

## Constructive change

Keep the bounded-source static response and physical ell, and add

    Delta L=-(M² beta/2) <S K,S K>,
    S=(1-ell² Delta_leaf)^(-1), M²=1/(8piG), beta>0.

The same spatial averaging acts on clock expansion and acceleration. This
is a new operator choice and one new dimensionless constant, not a second
length and not a native theorem. Inner products use the leaf volume; a
fully varied curved-time realization remains required. At aligned static
K=0 the value and first variations vanish. In homogeneous FLRW S1=1, so
G_cosmo/G=1/(1+3beta/2), with the same inherited endpoint qualification.
There is still no newly selected positive homogeneous dust abundance.

## Exactly constrained zero-field scalar

For k!=0 about Minkowski let f=(1+ell²k²)^(-1), alpha_k=2f²,
beta_k=beta f². Eliminating lapse and shift gives

    S2=M² integral [C_k |zeta_dot|²-D_k k²|zeta|²],
    C_k=(2+3beta f²)/(beta f²), D_k=(1-f²)/f²,
    omega²/(c²k²)=beta[(1+q²)²-1]/[2(1+q²)²+3beta], q=ell k.

Both reduced coefficients are positive for beta>0, ell>0 and finite k!=0.
The k=0 and singular parameter limits are separate. The tensor principal
speed stays c. This zero-field principal check is not a full finite-field
or nonlinear constraint/stability theorem.

Writing y=1+q², the exact group speed is

    v_group/c=sqrt[beta(y²-1)/(2y²+3beta)]
                 *[1+2y(2+3beta)/((y+1)(2y²+3beta))].

For 0<beta<=2, the second term inside the bracket is at most one:
the inequality reduces to (y-1)[2y(y+2)-3beta]>=0. Also v_phase/c<=sqrt(beta/2).
Therefore 0<beta<=1/2 is a rigorous sufficient, not necessary, range for
v_group<=c at every real k on this background. No beta is selected by it.
The old constant-trace beta<=1.23e-26 diagnostic does NOT transfer.

At long wavelength omega approximately c ell k² sqrt[2beta/(2+3beta)];
at short wavelength omega approximately c k sqrt(beta/2). The common
averaging removes the previous unbounded real-k speed growth. It retains
a potentially slow long-wavelength response, which must be treated in the
actual expanding background rather than imported into CMB equations.

## Ordinary sources can generate response, but it rings

In the same flat slow-motion ordering as CLOCK_STATE_FORMATION_V001,

    rho_T_dot+div(rho_T v_T)=M² beta Delta S² K,
    K=-Delta pi-3Psi_dot,

with the metric time derivative omitted only at the declared leading PN
order. The spatial integral is still a boundary flux. Uniform acceleration
alone has K=0; the global external-clock selection has not disappeared.

There is an exact held Fourier-probe solution (c=1). Take a signed weak
ordinary density rho cos(k.x), with support/work treated as an external
probe. Its linear stress is conserved about empty Minkowski; embedding it
in positive cosmological matter requires its own motion and conservation.
The reduced equation and constraints are

    C_k zeta_ddot+D_k k² zeta=rho/(M² alpha_k),
    n=-2zeta/alpha_k+rho/(M² alpha_k k²),
    B_shift=-C_k zeta_dot/k²,
    Phi=n+B_shift_dot=-zeta  (on shell).

Zero initial clock response means n(0)=0, not an arbitrary zero metric.
Choose zeta_dot(0)=0 and define zeta_N=rho/(2M²k²). Then

    zeta_stat=zeta_N/(1-f²),
    zeta(t)=zeta_stat+(zeta_N-zeta_stat)cos(omega t),
    rho_T(t)/rho=f²/(1-f²) [1-cos(omega t)].

Thus ordinary-source inhomogeneity drives response from zero initial clock
charge in this changed theory. It is not an independently imposed halo
profile. But there is no damping or attractor in this probe: it rings
indefinitely. A time average is not a formation/relaxation proof. Amplitude
must stay in the linear weak-response window; this is not a whole MOND
galaxy, an observed rotation curve, or a primordial perturbation solution.

## Bounded group speed is not microscopic causality

Let P=1-ell²Delta. The exact reduced PDE is

    [2P²+3beta] zeta_ddot-c²beta(P²-1)Delta zeta=0.

Putting A=2P²+3beta gives

    zeta_ddot=(c²beta/2)Delta zeta
       -[c²beta(2+3beta)/2]Delta A^(-1)zeta.

A^(-1) has an exponentially decaying, oscillatory kernel with infinite
spatial support. Generic compact reduced initial zeta with zero velocity
therefore has noncompact acceleration immediately; the complex poles do
not cancel. This is not a ghost diagnosis—the reduced energy is positive.
It means the real-k speed bound is not a finite-domain-of-dependence proof.
Constraint-compatible localized source preparation and gauge-invariant
readout must determine operational causality. The full metric constraints
may already make naive compact reduced data nonlocal. Neither that caveat
nor a preferred foliation proves a causal completion.

## Consequential next tests

Derive the FLRW quadratic action, retaining the homogeneous beta term and
variations of the leaf filter/measure; do not replace beta by beta f² in
background equations by analogy. Check long modes relevant to structure and
the acoustic peaks before importing a quasistatic force enhancement.

Separately, the compact-dwarf result still applies to its specified external
state. Compute or bound its ISOLATED fixed-state counterpart to determine
whether removing the uniform external response could even remove the
observational warning. This is a discriminating physical-state test, not a
new fit or a claim that the freefall state has formed. The two investigations
can proceed analytically in parallel with only one small numerical worker.

The shared background normalization, regular source-selected clocks,
relaxation, native identification and all Stage 3 observational requirements
remain unresolved. This note establishes a limited constructive dynamical
advance, not UNT superiority or completion.
