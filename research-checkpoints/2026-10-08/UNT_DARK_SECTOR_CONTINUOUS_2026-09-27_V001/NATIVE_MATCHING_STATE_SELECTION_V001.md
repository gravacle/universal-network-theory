# Arrangement energy is not a state-selection mechanism

2026-09-27. A conditional ensemble calculation, analytically checked by the
root and the GPT-6 Astra Ultra record-response agent. No numerical run,
temperature fit, new microscopic interaction, or physical state adoption.

The connected fourth-order result favors record/blank segregation in its
balanced attractive ground-state branch. The following identifies an explicit
obstacle to treating that minimum as an automatically realized macroscopic
state. It does NOT assert that the actual isolated UNT network is thermal.

## 1. Exact degree-one counting

Take the strict common-degree sector with d0=1, N vertices per layer, and
n occupied records on each layer. The regular graphs are precisely the N!
perfect matchings. Let L=L11 count occupied-record to occupied-record links.
Under the uniform distribution on these matchings,

    P0(L=l)=choose(n,l) choose(N-n,n-l)/choose(N,n),
    max(0,2n-N) <= l <= n.                              (1)

Proof: the n occupied left vertices map to a uniformly chosen n-element
subset of right vertices; l of that subset lie among the n occupied right
vertices. Multiplicities of complete bijections cancel in the probability.
This is a combinatorial count, not an assumed spatial graph ensemble.

The second-order effective Hamiltonian is C2+K_N L with
K_N=kappa Omega^2/N^2. In the attractive branch kappa<0, define a
CONDITIONAL Gibbs family on this regular manifold by

    rho0=exp(theta L)/Tr_P exp(theta L),
    theta=beta |kappa| Omega^2/N^2,     beta>=0.          (2)

Beta has inverse-energy units in the native energy calibration. No physical
temperature, bath, cooling rule, or approach to this family is supplied by
(2). It is a specified alternative to simply declaring the ground state.
Its L distribution is exactly proportional to (1) times exp(theta l), and

    Ptheta(l+1)/Ptheta(l)
      = exp(theta)(n-l)^2/[(l+1)(N-2n+l+1)].             (3)

All record counts and microscopic coefficients are held fixed in this test;
it is not an abundance-selection calculation.

## 2. Macroscopic density and the necessary scaling

Let n/N -> f with 0<f<1, and theta_N -> theta finite. For x=l/N,
Stirling's formula gives the log weight divided by N, up to a shared constant,

    s_theta(x)=f H(x/f)+(1-f)H((f-x)/(1-f))+theta x,
    H(y)=-y log y-(1-y)log(1-y),
    max(0,2f-1) <= x <= f.                              (4)

Its derivative is theta+log[(f-x)^2/(x(1-2f+x))]. The derivative decreases
strictly across the interior, so the unique maximizing density satisfies

    exp(theta)(f-x)^2=x(1-2f+x).                         (5)

The distribution concentrates there: every fixed closed set excluding the
maximizer has probability at most exp[-c N+o(N)] for some c>0, by the strict
gap of (4), its compact domain, and only O(N) possible values of l.
In particular, theta=0 gives x=f^2, not the segregated maximum f. An order-one
change in x therefore requires beta of order N^2/Omega^2 at fixed nonzero
kappa. Fixed beta, or beta Omega^2/N^2 -> 0, gives the uniform-matching
density f^2. There remain O(N) mixed record/blank links:

    (E10+E01)/N -> 2f(1-f).                             (6)

At f=1/2, the solution is especially transparent:

    x=1/[2(1+exp(-theta/2))],
    (E10+E01)/N=1/[1+exp(theta/2)].                      (7)

There is no finite-theta jump or full segregation. Density approaches its
maximum only as theta grows without bound. Equation (5) can also be inverted:
theta=log[x(1-2f+x)/(f-x)^2]. Thus a measured association fixes a required
ensemble bias, not the record-formation/cooling mechanism that would supply it.

For H2 alone, even maximal density and exact subspace occupation differ.
The exact probabilities obey

    Ptheta(n-k)/Ptheta(n)
      =choose(n,k) choose(N-n,k) exp(-theta k).           (8)

Writing a_N=n(N-n)exp(-theta), the k=1 term proves that Ptheta(L=n)->1
requires a_N->0. Conversely, the sum of all k>=1 ratios is bounded by
sum_(k>=1) a_N^k/(k!)^2, which tends to zero if a_N->0. At fixed f this
is equivalent to theta-2 log N -> +infinity. This exact-subspace criterion
is specific to H2, not established for noncommuting H4.

## 3. Including the checked fourth-order graph mixing

Let R4=H4-C4 P with the proven norm bound ||R4||<=C Omega^4/N^2, where
C is uniformly bounded at fixed gap and degree. Consider only the declared
FOURTH-ORDER TRUNCATED Gibbs state

    rhoR=exp[-beta(K_N L+R4)]/Z_R.                       (9)

R4 need not commute with L. A partition-function bound alone is not a
pointwise bound on L probabilities. Instead, eigenvalue shifts bounded by
||R4|| imply |log Z_R-log Z_0|<=beta||R4||. Consequently

    D(rhoR || rho0)
      =-beta Tr(rhoR R4)+log Z_0-log Z_R
      <=2 beta ||R4||.                                 (10)

Measuring L cannot increase relative entropy here: pinching rhoR into L
blocks contributes the nonnegative entropy increase, and each remaining
block's relative entropy to the uniform rho0 block is also nonnegative.
Hence the classical relative entropy of the measured L distributions is at
most (10). The reference distribution here is the TILTED Ptheta from (2),
not the untilted P0 in (1). Coarsen further into an event A and its complement. Its binary
relative entropy is at least

    PR(A) log[1/Ptheta(A)] - log 2.

For A outside a fixed neighborhood of the maximizing density, (4) gives

    PR(A) <= [2 beta ||R4||+log 2]/[c N+o(N)].           (11)

At finite theta and fixed Omega, beta||R4||=O(Omega^2), so (11) tends to
zero. Thus the same macroscopic density law survives this noncommuting
fourth-order truncation. No false operator monotonicity of matrix
exponentials was used. This does not turn a finite-order expansion into a
full-Hamiltonian theorem or prove equilibration.

## 4. Scientific consequence and scope

The ground-selection result and the conditional ensemble result are
compatible. The first says where the energy minimum lies; the second shows
that an entropically broad state need not concentrate there, despite that
minimum. At fixed energy-scale beta, the weak native arrangement energy
does not generate macroscopic association in this conditional family.
Keeping the native h=Omega/N normalization makes this distinction essential.

A constructive next mechanism must therefore derive state preparation,
effective cooling/scaling, a nonequilibrium selection process, or another
response of the actual formed state. No such process is supplied by
changing the label from records to gravity. Conversely, this calculation
does not forbid a nonequilibrium history-selected graph or direct carrier
response and does not refute UNT as a whole.

All statements concern a fixed-record, carrier-free, degree-one regular
manifold (and the explicitly named truncated operator). Higher-order
arrangement terms, the dressed full-space observable, dynamic record
abundance, physical volume, temperature, gravity and cosmology remain
separate unclosed questions. The verified finite-order coefficients are
evidence for the mathematics, not observational evidence for dark matter
or dark energy being unnecessary.
