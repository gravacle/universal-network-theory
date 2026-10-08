# Empty-state factorial moments and a fixed-age source-response bound

2026-09-30. Root analytical derivation, pending independent review. No
numerical execution, new formation rule, chosen favorable age or physical
normalization. This extends the already established first-moment formation
bound to the energy-weighted response of the actual prepared state.

## Explicit family and scope

Use the full first-degree-tie parent from the reviewed coupling and response
notes, not its matching projection:

    H = C_N + 2U(C_L+C_R) - h sum_e X_e,
    h=Omega/N,  U,Omega>0,  L=N^2,
    M=sum_e n_e,  d_v=sum_(e incident to v) n_e,
    C_L=sum_(v left) binom(d_v,2),
    C_R=sum_(v right) binom(d_v,2),
    T=2U(C_L-C_R).

The initial edge register is exactly empty; uniform records are held,
carriers are blank and ports are off as in the earlier preparation theorem.
These are conditional premises, not a claimed default cosmological state.
Native age is tau=Omega*t/hbar. The source experiment here is explicitly
linear H+theta(t)T with the initial state independent of theta. A different
source Hamiltonian or source-dependent preparation needs its own contacts.

## 1. Factorial moment bound without a mean-field approximation

Write (m)_r=m(m-1)...(m-r+1), with (m)_0=1, and
mu_r(t)=<(M)_r>_t. For integer m<r the falling factorial is zero.
Let P_m project onto exactly m occupied edges and v_m=||P_m psi||.
The raising block of sum_e X_e between m and m+1 has column sum L-m
and row sum m+1. Its operator norm is at most sqrt[(m+1)(L-m)],
by the maximum row/column norm bound; in fact uniform vectors saturate it.
Thus

    ||P_(m+1) H P_m|| <= h sqrt[(m+1)(L-m)]
                        <= Omega sqrt(m+1).                 (1)

The diagonal parent commutes with every P_m. Arbitrary phases and
correlations within each sector remain in v_m; they were not discarded
in (1). Since (m+1)_r-(m)_r=r(m)_(r-1), the exact commutator and
Cauchy--Schwarz imply

    |dot mu_r| <= (2r Omega/hbar)
       sum_(m=0)^(L-1) (m)_(r-1) sqrt(m+1) v_m v_(m+1)
      <= (2r Omega/hbar) sqrt(mu_r mu_(r-1)).                (2)

For the last line use
`(m)_(r-1) sqrt(m+1)=sqrt[(m+1)_r (m)_(r-1)]`.
The first sum of squares is mu_r; the second is bounded by mu_(r-1).
For r=1 it is bounded by mu_0=1. The statement for r>L is trivially zero.
The same proof applies to a mixed state by purification with an inert
auxiliary register; the block norm is unchanged.

Regularize sqrt(mu_r) by sqrt(mu_r+epsilon) in (2). Starting empty gives
mu_r(0)=0 for r>=1, and induction on r yields

    sqrt(mu_r(t)) <= (r Omega/hbar) integral_0^t
                                sqrt(mu_(r-1)(s)) ds,
    mu_r(t) <= tau^(2r),  t>=0.                             (3)

This holds at every finite age, not just at a Taylor-series order. It is
a bound on exact joint-state moments, not a Poisson-distribution assertion.
The earlier r=1 speed theorem is recovered, not counted as new evidence.

## 2. Local-degree moments and collision expectation

For a fixed vertex there are only N incident edge qubits. Every other
term, including flips of nonincident edges, commutes with its degree d_v.
Repeating (1)--(3) for this sector decomposition replaces Omega by
h sqrt(N)=Omega/sqrt(N). It follows without permutation factorization that

    <(d_v)_r>_t <= (tau^2/N)^r.                             (4)

In particular, with C=C_L+C_R and 2N vertices,

    <C>_t = (1/2) sum_v <(d_v)_2>_t <= tau^4/N.            (5)

This is an expectation over the complete state. No regularity of individual
realized graphs is assumed. Native record/writer couplings commuting with
each n_e would not invalidate the moment inequalities if explicitly restored;
they would change the held-sector model and its source dictionary, however.
Unspecified incidence-changing ports, resets, postselection or changed flip
scaling are not covered by this proof.

## 3. A uniform-in-N, finite-age energy-weighted bound

For a simple bipartite graph, any unordered pair of distinct edges shares
at most one vertex. Therefore the diagonal operator inequality is

    0 <= C <= binom(M,2)=(M)_2/2.

Also |C_L-C_R|<=C. By Cauchy--Schwarz on the commuting nonnegative C,

    W_T(t):=<T^2>_t <= 4U^2 <C^2>_t
                   <= 4U^2 sqrt[<C>_t <C^3>_t].            (6)

The exact falling-factorial identity is

    [(M)_2]^3 = (M)_6 +12(M)_5 +38(M)_4 +32(M)_3 +4(M)_2.

All coefficients are positive. Define

    Q(x)=x^6+12x^5+38x^4+32x^3+4x^2.

Equations (3) and (5)--(6) now give the explicit bound

    <C^3>_t <= Q(tau^2)/8,
    W_T(t) <= sqrt(2) U^2 tau^2 sqrt[Q(tau^2)/N].           (7)

This is not sharp: the known fixed-N leading coefficient is proportional
to tau^4/N, whereas (7) bounds it by a constant times tau^4/sqrt(N).
Its useful property is a proved all-time inequality for each finite N and
an N-uniform remainder-free estimate at fixed tau. At ages growing with N,
the polynomial also grows and no vanishing conclusion is implied. The bound
does not impose an upper limit on allowable physical ages or supply a clock.

## 4. Actual-state two-time response and finite-window work

For the above linear source and the fixed empty initial state, use

    chi(t,s)=(i/hbar)<empty|[T_H(t),T_H(s)]|empty>, t>=s,
    delta<T(t)>=-integral_0^t chi(t,s) theta(s) ds.

Cauchy--Schwarz gives |chi(t,s)|<=2 sqrt[W_T(t)W_T(s)]/hbar.
Inserting (7), with tau_t=Omega*t/hbar and tau_s=Omega*s/hbar,

    |chi(t,s)| <= (2 sqrt(2) U^2/(hbar sqrt(N))) tau_t tau_s
                        [Q(tau_t^2)Q(tau_s^2)]^(1/4).      (8)

Consequently the complete two-time kernel tends to zero at least as
N^(-1/2) over every fixed native-age window 0<=s<=t<=T_window.
At s=0 it is exactly zero, consistent with T|empty>=0. This is a statement
about the actual prepared state, not the stationary ground susceptibility;
there is no contradiction with the earlier strictly positive finite-N
ground response. No long-time or static limit has been exchanged with N.

For a differentiable compactly supported fixed source pulse, the expectation
of T in the unperturbed exchange-even state is zero. Write
theta=epsilon*f(t). With no explicit theta^2 contact in this linear H,
the coefficient of epsilon^2 in source work is

    W^(2)=-integral dt dot(f(t)) integral_0^t ds chi(t,s)f(s).

For support in [0,T_window], if K_N is the right-hand side of (8) at
t=s=T_window (a bound, not the equal-time kernel), then

    |W^(2)| <= K_N ||dot f||_1 ||f||_1 = O(N^(-1/2)).       (9)

No positivity or passivity follows from (9). Discontinuous pulses require
explicit quench work or a justified limiting procedure. N-dependent pulse
duration, amplitude or shape changes the bound's scaling premises.

## Evidence ceiling and next decision

At any fixed native-age window, the initially empty fixed-scaling candidate
does not recover a nonvanishing bare opposite-layer response by waiting a
constant time. A formation time increasing with N, a different explicitly
owned preparation, or a changed model must be analyzed on its own terms.
This is stronger than the occupation bound alone because it controls the
source-weighted second moment and causal kernel without an inverse-gap limit.

Physical Z=(ell/(2c^2))T and physical volume would rescale the response by
ell^2/(4c^4 V). Neither ell, V nor a conversion of native age to cosmic time
has been derived here; no conclusion about that physical scaling follows.
The within-layer source is also a different operator. No galaxy fit,
cosmological pressure, photon spectrum, observational superiority or Stage 3
completion follows. All eleven program lanes remain open.

Ancestry (all relative to this note):

- ../NATIVE_INCIDENCE_FORMATION_SPEED_BOUND_V001.md,
  SHA8118207e2da4bdae41143f6a90d48dd3be9f450371c688f508eabe776ccc6229.
- NATIVE_DEGREE_TIE_FULL_PARENT_COUPLING_V001.md,
  SHAdef8c842be9bd1bbd21ae8cd0a6338160ac28d81aaab2851371b519b75205390.
- NATIVE_DEGREE_TIE_FULL_PARENT_ODD_RESPONSE_V001.md,
  SHAac17bd126aa2f05032b674180b36caa72faa6164879aa3ab8b9960e57b86a815.
- NATIVE_FORMATION_OR_ACTUAL_STATE_DECISION_V001.md,
  SHA513ed019e9081542c8053cb9fd99944eacec16bac35708c628ee965717ed0379.
