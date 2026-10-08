# Uniform native bounds around a nonempty regular-degree manifold

2026-09-27. Analytical theorem; no numerical work, new interaction, parameter
adoption, preparation or geometric identification. The resident
`NATIVE_RECORD_SELECTED_GRAPH_VIRTUAL_RESPONSE_V001.md` and
`NATIVE_SPARSE_THERMODYNAMIC_BOUND_V001.md` were read after flag checks.
The following strengthens their common-degree ground-state bounds without
using the growing perturbation norm ||V||=Omega N.

**Result.** Away from degree ties, native h_N=Omega/N gives O(1) total squared
degree defects and O(1) ground-energy correction around a feasible preferred
regular graph, for every fixed Omega and sufficiently large N. A separate
sufficient small-Omega condition gives an isolated low-energy subspace
uniformly in N. Neither result proves that the previously derived shrinking
record-dependent arrangement splitting survives every higher-order effect.

## 1. Complete energy and the degree-defect operator

Keep the same carrier-free, source-off, fixed binary record sector on
K_(N,N), including storage and any declared spectator constants. Let H0,V,
Ecl be as in the preceding graph-response note and set

    c=Delta+4U(d0-d_*),
    g=U-max(|c/2|,|c/2-lambda|)>0,
    K=sum_(2N vertices v) (d_v-d0)^2,
    V=-(Omega/N)sum_e X_e.                                (1)

Here 0<=d0<=N is an integer. The common regular manifold P is nonempty.
Explicitly Ecl=2NU(d0-d_*)^2+Delta N d0
+(epsilon_r-lambda d0)D_rec+C_spec, with every declared constant retained.
For an integer deviation k, |k|<=k^2, so the SAME diagonal energy obeys

    U k^2+(c/2-lambda q_v)k >= g k^2,
    H0-Ecl >= g K.                                      (2)

The earlier complete Ecl is retained, not reset. On Q=1-P every graph has
K>=2, since the two layers must have equal total degree. The native extensive
margin and storage assumptions remain in force independently of this bound.

## 2. A state-dependent flip estimate near regular degree

At one vertex let S_v=sum_(e incident v)X_e, P_v project onto d_v=d0,
and Q_v=1-P_v. For a normalized state define

    p_v=<Q_v>,     k_v=<(d_v-d0)^2>.

A flip changes star degree by one, so P_v S_v P_v=0. In its fixed-degree
sector the exact operator norm is

    ||Q_v S_v P_v||^2=N(2d0+1)-2d0^2=:N b_N,
    b_N=1+2d0(1-d0/N).                                  (3)

For a direct proof, P_v S_v^2 P_v has nonnegative matrix entries, diagonal
N, and row sum N+2d0(N-d0). Its constant row sum is the largest eigenvalue,
attained by the uniform degree-d0 star vector. Exterior edges merely tensor
an identity. Thus the two P_v/Q_v cross terms are bounded by
2 sqrt(N b_N p_v), with an optional extra factor sqrt(1-p_v).

For the Q_v component phi, let ||phi||^2=p_v and z_v=<phi|d_v|phi>.
The edge reduced-state Bloch inequality and Cauchy--Schwarz give

    |<phi|S_v|phi>| <= 2 sqrt[z_v(N p_v-z_v)]
                    <= 2 sqrt(N p_v z_v).                (4)

On Q_v, integer d!=d0 implies d<=(d0+1)(d-d0)^2. Hence
p_v<=k_v, z_v<=(d0+1)k_v, and (4) is at most
2 sqrt[N(d0+1)]k_v. This improves the looser d0+2 coefficient.
One may use hole degree N-d instead: set beta=min(d0,N-d0), giving
2 sqrt[N(beta+1)]k_v. Formula (3) is also invariant under this replacement.
All bounds include d0=0,N. For mixed or entangled states, purify the state
and tensor every displayed operator with the identity; the same proof
applies. No product-state hypothesis enters.

Every edge belongs to two stars, so V=-(Omega/(2N))sum_v S_v. With
kappa=<K>, summing the cross bounds and applying sum_v sqrt(p_v)
<=sqrt(2N kappa) proves the statewise inequality

    |<V>| <= Omega sqrt(2 b_N kappa)
                         +Omega sqrt[(beta+1)/N] kappa.  (5)

In particular b_N<=2d0+1 and beta<=d0 yield simpler N-independent constants
where needed. Equation (5) is not an operator-norm assertion about V.

## 3. Uniform energy, total defects and incidence

Define a_N=g-Omega sqrt[(beta+1)/N]. If a_N>0, (2),(5) give, for every state,

    <H>-Ecl >= a_N kappa-Omega sqrt(2 b_N kappa).

A regular computational graph has zero flip expectation. Minimizing the
right-hand side and using E0<=Ecl therefore yields

    Ecl-Omega^2 b_N/(2a_N) <= E0 <= Ecl,
    <K>_0 <= 2Omega^2 b_N/a_N^2.                          (6)

For fixed d0,g>0,Omega, these are uniform O(1) bounds once N is sufficiently
large; no small-Omega assumption is required. They strengthen the prior
O(sqrt N) energy error and defective-fraction estimate in this strict common
degree regime. They do not replace the sharper existing empty-phase theorem.
The hole notation improves finite-N constants; it does not infer a dense
d0=N-beta phase at fixed native coefficients.

Integer deviations also give two useful consequences:

    (1/(2N))sum_v <1_(d_v!=d0)>_0 <= <K>_0/(2N)=O(1/N),
    |<M>_0-N d0| <= <K>_0/2=O(1),   M=sum_e n_e.          (7)

The second bound follows from 2(M-Nd0)=sum_v(d_v-d0). A vanishing fraction
of defective vertices does not by itself imply that the entire measured
graph is regular with probability approaching one.

## 4. An additional uniform small-Omega isolation theorem

On normalized states in global Q, kappa>=2, so (5) implies

    |<V>| <= Omega[sqrt(b_N)+sqrt((beta+1)/N)] kappa.

Let A=Q(H0-Ecl)Q>=gamma Q with gamma=2g, and define

    r_N=(Omega/g)[sqrt(b_N)+sqrt((beta+1)/N)].

Then the Q-block form inequality is

    -r_N A <= QVQ <= r_N A.

If r_N<1, the complete complementary block D=Q(H-Ecl)Q satisfies

    D >= (1-r_N)A >= delta_N Q,
    delta_N=2g(1-r_N)>0.                                (8)

This controls a weighted quadratic form, not ||QVQ||. It admits a uniform
large-N domain whenever Omega sqrt(2d0+1)<g, with a strict margin.

There is also an exact normalization improvement:

    PVP=0,  PV^2P=h_N^2 N^2 P=Omega^2 P,
    ||QVP||=Omega.                                     (9)

Two distinct flips cannot restore all prescribed degrees, which proves the
middle identity. Write B=QVP. For Omega>0, Schur inertia of the block matrix
[[0,B^dagger],[B,D]] shows that precisely rank(P) eigenvalues lie below Ecl:
-B^dagger D^-1 B is negative definite because B^dagger B=Omega^2 P.
Principal-submatrix interlacing puts every remaining eigenvalue at least
Ecl+delta_N. Thus this is a uniform isolated low band, not a claim that each
bare regular graph is an eigenstate. At Omega=0 the low band is exactly P.

For the ground E=Ecl-x, x>=0, Feshbach elimination gives

    x(delta_N+x)<=Omega^2,
    x<=[sqrt(delta_N^2+4Omega^2)-delta_N]/2,
    ||Q psi||^2/||P psi||^2 <= Omega^2/(delta_N+x)^2.      (10)

These are uniform energy/leakage controls despite ||V||=Omega N.

For completeness a uniform effective-operator error is also available.
Let M(-x)=-B^dagger(D+x)^-1 B and M2=-B^dagger A^-1 B.
Set W=A^-1/2 QVQ A^-1/2, so ||W||<=r_N. Expanding the inverse in
I+W+xA^-1 and using link-number parity to cancel the cubic sandwich yields

    ||M(-x)-M2|| <= Omega^2 x/gamma^2
       +(Omega^2/gamma)(r_N+x/gamma)^2/(1-r_N).           (11)

Using (10), this is uniformly O(Omega^4) for sufficiently small Omega at
fixed g,d0. It does NOT yet resolve the earlier arrangement preference:
its total second-order contrast can be only O(Omega^2/N), and one L11 step
is O(Omega^2/N^2). A uniform error larger than those shrinking contrasts
cannot certify their eventual signs or which graph arrangement wins.

## 5. Feasible unequal preferred degrees and scope

The same proof applies to specified target degrees k_v, provided their
bipartite lists are feasible and

    g=min_v {U-|2U(k_v-d_*)+Delta/2-lambda q_v|}>0.

Replace K by sum_v(d_v-k_v)^2. With K0=max_v k_v fixed, use
b_N<=2K0+1 and beta+1<=K0+1 in (5)-(8). The resulting O(1) energy bound
therefore also sharpens the balanced-record leading-energy theorem away
from degree ties, when its preferred lists are feasible. If two such sectors
share a uniform correction bound E0-Ecl in [-C,0], their excess-energy
difference differs from its classical value by at most C, not 2C. This is
a bound on conditional ground energies, not an actual insertion process.

The theorem controls degree and a low-energy subspace, not spatial locality,
connectivity, dimension, clock universality or gravity. It supplies no cooling
or formation history and does not alter the conserved record populations.
Degree ties, infeasible target lists, added carriers or graph-dependent ports
need a separate treatment. N still counts vertices rather than a physical
volume; no physical pressure has been obtained by differentiating these bounds.
