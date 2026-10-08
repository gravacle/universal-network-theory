# Native balanced-record leading ground energy

Date: 2026-09-27. Construct: `BS_BALANCED_BINARY_RECORD_ENERGY_V001`.
Analytic consequence of the existing BS action; no numerical calculation,
new microscopic interaction, physical-volume identification, or preparation
claim.

## 1. Source and conditional sector

The resident `recovered_sources/BS_MICRO_ACTION.md` was read in full. Its
SHA256 is `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
BS06 explicitly uses **h_N = Omega/N**, with fixed Omega, rather than a
fixed per-edge flip strength as N increases. BS10 supplies the record
storage energy, BS11 the occupation feedback, and BS13--14 the sufficient
extensive domain. No hard degree cutoff is present.

Consider one complete bipartite slab with N nodes on each side, no carriers,
formation and ports off, and fixed binary record occupations q_v in {0,1}.
Other blank spectator factors contribute zero; any nonzero fixed spectator
energy must instead be retained separately. Let D = sum_v q_v and
M = sum_e n_e. The conditional Hamiltonian is

\[
 H=\epsilon_rD+\sum_v f_{q_v}(d_v)
       -\frac{\Omega}{N}\sum_{e=1}^{N^2}X_e,
 \qquad
 f_q(d)=U(d-d_*)^2+(\Delta/2-\lambda_Rq)d.       \tag{1}
\]

This is exactly BS06+BS10+BS11 in the stated sector, since every edge is
counted at its two endpoints. Keep U>0, fixed d_* and all other coefficients
N-independent; assume the native margin Delta-2 lambda_R >= delta > 0.
The U=0 case in this margin has both preferred degrees zero and is included
by the empty-graph case below. The q_v are actual binary sector labels,
not a replacement of q_v by a fractional mean. Ground energy here means a
conditional static spectral quantity, not an actual formed mission state.

## 2. Preferred integer degrees

Define, on nonnegative integers,

\[
 m_q=\min_{d\in\mathbb Z_{\ge0}}f_q(d),\qquad
 d_q\in\operatorname*{argmin}_{d\in\mathbb Z_{\ge0}}f_q(d),
 \qquad K=\max(d_0,d_1).                         \tag{2}
\]

Use one fixed tie convention, for example the smallest minimizer. These
degrees are finite and N-independent: they are the closest nonnegative
integer(s) to d_*-(Delta/2-lambda_R q)/(2U). Take N>=K. Nothing in the
proof projects out states with degrees larger than K; K only bounds the
degrees of a classical trial graph.

Let n_1 records be occupied on **each** layer, f_N=n_1/N, and D=2n_1.
Assign every q=0 node degree d_0 and every q=1 node degree d_1. The two
prescribed degree sums agree:

\[
 M_*=(N-n_1)d_0+n_1d_1.                         \tag{3}
\]

## 3. Exact feasibility, not a mean-degree ansatz

Lemma: two nonnegative integer bipartite degree lists, each entry at most
K, with equal total M_*, are realized by a simple subgraph of K_{N,N} if
M_* >= K^2. If M_*=0, the empty graph realizes the lists separately.

Proof: introduce the integral-capacity flow network with left capacities
a_i, unit left-to-right capacities, and right capacities b_j. For a chosen
set of k left nodes, the minimum capacity available on the right is
sum_j min(k,b_j). If 1<=k<=K,

\[
 \sum_j\min(k,b_j)\ge\frac{k}{K}\sum_jb_j
 =\frac{kM_*}{K}\ge kK\ge\sum_{i\in S}a_i.       \tag{4}
\]

If k>=K the same right-hand capacity is M_*, which bounds any partial
left sum. The k=0 case is immediate. Thus every source-to-sink cut has
capacity at least M_*. Integral max flow supplies each required degree,
and unit edge capacities prohibit multiple edges. This proves the lemma.

Consequently all individual minima in (2) are attained simultaneously
whenever (3) meets the lemma. The exact diagonal minimum is

\[
 E_{\rm cl}=\epsilon_rD+2(N-n_1)m_0+2n_1m_1
 =2Nm_0+D\mu,\qquad
 \mu=\epsilon_r+m_1-m_0.                        \tag{5}
\]

The sufficient condition M_*>=K^2 is not automatic for a finite number
of records and is not necessary. For example, if d_0=0 and fewer than
d_1 positive-degree nodes occur on each layer, the all-minimizer graph
is impossible. For a fixed limiting population fraction with positive
preferred mean degree, M_* grows linearly and the condition eventually
holds. An identically zero preferred degree uses the empty case.

The flow and integrality criterion used here is mathematical, not an imported
physical law; see David Gale, [A theorem on flows in networks](https://msp.org/pjm/1957/7-2/pjm-v7-n2-p04-s.pdf),
Pacific Journal of Mathematics 7 (1957), pp.1078 and1080–1081. The
bounded-degree sufficient condition M_*>=K^2 is the elementary corollary
proved above, not a claimed necessary condition.

## 4. Quantum correction and the actual ground-state degree

Let E_0 be the full ground energy of (1), including all N^2 flips, and
m=<M> in any ground state. A classical minimizing basis graph has zero
flip expectation, so E_0<=E_cl. The empty graph also gives
E_0-epsilon_r D<=2UN d_*^2. The native margin and flip norm imply

\[
 E_0-\epsilon_rD\ge\delta m-\Omega N,
 \qquad
 m\le C N,\qquad C=\frac{2Ud_*^2+\Omega}{\delta}. \tag{6}
\]

This bounds the actual ground-state mean degree m/N, not merely the
degree of a product trial state.

For every edge let p_e=<n_e>. Positivity of its reduced qubit state and
Cauchy--Schwarz give

\[
 \langle X_e\rangle\le2\sqrt{p_e(1-p_e)}
 \le2\sqrt{p_e},\qquad
 \sum_e\langle X_e\rangle\le2N\sqrt m.          \tag{7}
\]

The diagonal operator is bounded below by its exact classical minimum.
Combining (6)--(7), under the feasibility conditions of Section 3,

\[
 \boxed{\quad E_{\rm cl}-2\Omega\sqrt{CN}
       \le E_0\le E_{\rm cl}.\quad}             \tag{8}
\]

Thus this native normalization gives the **derived leading energy**

\[
 E_0=2Nm_0+D\mu+O(\sqrt N),\qquad
 \frac{E_0}{2N}=m_0+f_N\mu+O(N^{-1/2}).         \tag{9}
\]

The correction has a definite nonpositive sign relative to E_cl and an
explicit uniform bound; no product-ground-state, uniqueness, or absence
of correlations was assumed. It may select correlated states inside a
large classical manifold despite being subextensive. Equation (9) does
not assert that the quantum state is close to a classical mixture.

## 5. What the record coefficient does and does not establish

Feedback makes m_1<=m_0. More precisely, for the selected minimizing
degrees,

\[
 -\lambda_Rd_1\le m_1-m_0\le-\lambda_Rd_0.      \tag{10}
\]

Hence a strictly positive bare epsilon_r does not alone imply mu>0.
Positivity of mu is an additional check on the existing coefficients,
not permission to tune or subtract a q-dependent energy. The degree
baseline 2Nm_0 and the bare storage cost are both retained in (5).

The coefficient mu is an extensive, balanced-population excess-energy
coefficient. The O(sqrt N) error does not certify the energy of inserting
one record at finite N. Balancing changes the two layer counts together;
unbalanced degree demands require a separate constrained minimization.
For the port-free complete graph, patterns with the same two layer
counts are exactly related by within-layer permutations; no preferred
spatial arrangement has been inferred.

This is a constructive native energy result, not a dust or vacuum
equation of state. N counts nodes, not a derived physical volume.
An autonomous change of N, pressure/stress, a volume map, cosmological
redshift, preparation of the conditional ground state, and any thermal
or dynamical selection law remain unprovided by this argument. No
hard degree cutoff, lattice, new locality law, or new normalization was
introduced. A fixed per-edge h as N grows would instead set Omega=Nh
and leave the already specified native large-N path.
