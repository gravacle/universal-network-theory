# Mean-link geometry versus graph correlations: exact finite BS screen

Date: 2026-09-27. Status: additive analytical diagnostic; no physics run or new physical-volume rule. This does not replace the primary active/maintenance dark-sector construct or silently redefine BS16.

Source: the fully read resident recovered [BS microscopic action](recovered_sources/BS_MICRO_ACTION.md), SHA256 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec. Relevant anchors are BS03 (within-layer permutation symmetry, not a gauge quotient), BS06 (degree energy and nonzero link flips), BS09–BS12 (carrier/record/port terms), and BS16–BS18 (mean-link Laplacian and separately tested spectral dimension). Lines 369–407 explicitly call this an elliptic diagnostic, not spacetime or a causal cone.

## 1. An exact distinction already available in the source algebra

Work on one slab with N nodes in each layer and a fixed incidence map for all possible bipartite edges. For an edge e=(u,v), set

\[
 B_e=(|u\rangle-|v\rangle)(\langle u|-\langle v|),\qquad
 L(n)=\sum_e n_e B_e,\qquad
 \bar L=\sum_e\langle n_e\rangle B_e.
\]

This is the unblocked finite comparison. Applying it at a blocked scale additionally requires the frozen BS blocking/incidence map; a configuration-dependent blocking map cannot be pulled through the average without a separate argument.

Two different, permutation-invariant static quantities are

\[
 K_{\rm mean}(s)=\operatorname{Tr}_{v}e^{-s\bar L},
 \qquad
 K_{\rm corr}(s)=\mathbb E_n\operatorname{Tr}_{v}e^{-sL(n)}.                 \tag{1}
\]

Here s≥0 is the BS elliptic spectral parameter, not cosmological or real probe time. For an arbitrary quantum link state, the simultaneous commuting n_e measurements define the exact Born probabilities of n. Equivalently K_corr is the expectation of the native diagonal operator Tr_v exp[−s Σ_e n_e⊗B_e]. Thus (1) is well-defined even for coherent link states; treating their subsequent dynamics as a classical graph ensemble does NOT follow.

For finite Hermitian matrices and s>0,

\[
 K_{\rm mean}(s)\le K_{\rm corr}(s),                                    \tag{2}
\]

with equality only if L(n) is almost surely the same matrix. A direct proof avoids assuming operator convexity of the exponential: along A+tB,

\[
 {d^2\over dt^2}\operatorname{Tr}e^{A+tB}
 =\int_0^1\operatorname{Tr}
 [e^{(1-u)(A+tB)}B e^{u(A+tB)}B]\,du>0
\]

for nonzero Hermitian B. In the instantaneous eigenbasis every summand is a positive exponential times |B_ij|². Scalar Jensen for this strictly convex trace functional gives (2). No corresponding matrix ordering of the two exponentials is asserted.

The first discrepancy is

\[
 K_{\rm corr}-K_{\rm mean}
 ={s^2\over2}\mathbb E\operatorname{Tr}(L-\bar L)^2+O(s^3).               \tag{3}
\]

For the fixed simple-graph incidence above,

\[
 \mathbb E\operatorname{Tr}(L-\bar L)^2
 =4\sum_e\operatorname{Var}(n_e)
  +2\sum_{\{e,f\}:\ e\ne f,\ e\cap f\ne\varnothing}
       \operatorname{Cov}(n_e,n_f).                                    \tag{4}
\]

The second sum is over unordered distinct incident-edge pairs. Its terms need not be positive; the full expression is nonnegative. One-edge means therefore do not determine the nonlinear heat diagnostic.

## 2. Permutation-invariant cycle ensemble: branch locality survives averaging of labels

Take the alternating cycle C_(2N), N≥3, and uniformly relabel the left and right vertices independently. This is an explicitly declared admissible state ensemble, not a state derived to be formed or stationary by BS06. Every branch is the same unlabeled cycle and has degree 2, but

\[
 \langle n_{ij}\rangle={2\over N}.
\]

The mean graph is weighted K_(N,N), with spectrum

\[
 \operatorname{spec}\bar L=\{0,\ 2\ {\rm(multiplicity}\ 2N-2),\ 4\},
 \quad
 K_{\rm mean}=1+(2N-2)e^{-2s}+e^{-4s}.                                  \tag{5}
\]

Every branch instead has

\[
 \lambda_k=2-2\cos(\pi k/N),\quad k=0,\ldots,2N-1,
 \qquad K_{\rm corr}=\sum_k e^{-s\lambda_k}.                             \tag{6}
\]

The cycle's first nonzero eigenvalue is asymptotic to π²/N²; the mean graph's remains 2. The cycle has graph diameter N, while the support of the mean weighted graph has diameter 2. These are combinatorial/spectral statements, not physical-distance or causality claims.

The cycle has a controlled one-dimensional heat-scaling window. Its normalized heat sum approaches

\[
 {1\over2\pi}\int_{-\pi}^{\pi}e^{-2s(1-\cos\theta)}\,d\theta
 ={1\over\sqrt{4\pi s}}\,[1+O(s^{-1})].
\]

A bounded-variation Riemann-sum estimate gives absolute finite-N error O(1/N), hence relative error O(√s/N). Applying the same estimate to −s∂_s of the sum gives

\[
 d_{\rm spec}=1+O(s^{-1})+O(\sqrt{s}/N)
 \quad\hbox{for}\quad 1\ll s\ll N^2.                                  \tag{7}
\]

By contrast, at fixed s the normalized mean heat sum tends to e^(−2s) as N grows, so its spectral slope tends to 4s, not a one-dimensional plateau. At finite N it eventually saturates at its single zero mode. Label homogeneity has erased the cycle geometry from BS16's one-edge-mean diagnostic, not from the full state.

More generally, uniform relabeling of any d-regular bipartite graph gives mean weights d/N and mean spectrum {0,d repeated 2N−2 times,2d}. Its branch and mean second moments are

\[
 \operatorname{Tr}L(n)^2=2N(d^2+d),\qquad
 \operatorname{Tr}\bar L^2=2Nd^2+2d^2.
\]

Consequently (3) starts at d(N−d)s², or d(N−d)s²/(2N) after vertex normalization. For the cycle it is 2(N−2)s². This gap witnesses lost fluctuations, not by itself a geometric phase.

## 3. Smallest loop witness, with exactly matched native initial energy

At N=4 compare two diagonal link ensembles: uniform relabelings of C8 and uniform relabelings of two disjoint C4s. Both have degree 2 at every node and every mean link 1/2. They therefore have the same BS16 operator. The native four-link invariant

\[
 \widehat C_4=
 \sum_{i<k}\sum_{j<l} n_{ij}n_{il}n_{kj}n_{kl}                           \tag{8}
\]

counts simple bipartite squares. Its expectation is 0 for the C8 ensemble and 2 for the two-square ensemble. These are products of existing commuting link projectors, not new Hamiltonian interactions. A four-cycle is the shortest simple cycle allowed by a simple bipartite graph.

For either degree-2 ensemble,

\[
 \operatorname{Tr}L^4=140N+8C_4.                                      \tag{9}
\]

Indeed Tr A⁴=12N+8C_4, Tr A²=4N, and odd adjacency traces vanish. At N=4, the fourth Laplacian moments are 560 and 576. The heat moments through order 3 agree; the normalized configuration-resolved heat sums first differ by

\[
 {K_{\rm two\ squares}-K_{\rm cycle}\over8}
 ={s^4\over12}+O(s^5).                                                 \tag{10}
\]

This example also admits an exact initial BS energy match, not merely a count match. Choose product preparations of each diagonal graph mixture with identical fixed uniform record occupation q∈{0,1}, identical other onsite states, and a fixed-content single-carrier state I_v/(2N). Set all formation couplings g=0, and choose zero/graph-blind ports or separately verified equal port-energy expectations. Identical unspecified port symbols alone are insufficient if they probe higher graph correlations. Then

\[
 \langle X_e\rangle=0,\quad
 \sum_e n_e=2N,\quad
 d_v=2,\quad
 \langle H_{\rm hopping}\rangle=0,\quad
 \sum_e n_e(J^\psi_e)^2=2I
\]

on the one-carrier sector. The common complete energy is

\[
 \langle H\rangle=
 2N\Delta+2NU_d(2-d_*)^2-4N\lambda_R q
 +\epsilon_\psi+2\lambda_J+E_{\rm identical\ other\ storage/ports}.       \tag{11}
\]

All coefficients are the same on both sides, including the BS06 flip coefficient Ω/N; its expectation vanishes here, not its operator. No constant is reset between states. Uniform carrier mixing preserves permutation covariance; a localized alternative requires a prospectively owned port anchor. Equality of energy and means neither makes these states stationary nor makes their later dynamics equal.

## 4. What a carrier can probe, and what is not frozen in the native parent

For a genuinely fixed link configuration in the one-carrier, fixed-content sector, the BS09/BS11 carrier generator is

\[
 H_\psi(n)=tL(n)+[\epsilon_\psi+(\lambda_J-t)d]I                         \tag{12}
\]

on a d-regular branch, apart from independently owned carrier-independent terms. Thus the λ_J degree contribution is a known scalar on these examples; no new λ_J=t identity is needed to access Laplacian spectral differences through the native hopping term. A response/readout protocol is still required; this is not a claim that real-time hopping is diffusion.

The actual BS parent has Ω>0 and the term −(Ω/N)Σ_e X_e. Graph sectors are therefore not exact conserved sectors. A classical fixed-graph average of probe channels requires an explicitly owned preparation and either an appropriate frozen-control protocol or a controlled timescale approximation. In the one-slab hold with all other terms commuting with n_e, removing only that flip term changes the unitary by at most

\[
 \|U(\tau)-U_0(\tau)\|
 \le {|\tau|\over\hbar}\,\|H_{\rm flip}\|
 \le {|\tau|\Omega N\over\hbar}.                                       \tag{13}
\]

This is a conservative finite-N sufficient bound, not a derived useful large-N window. Ports that also change links require additional bounds. Preparing the graph ensemble, extracting the readout, and probe backreaction must be owned. Even when the frozen approximation is valid, averaging branch channels is generally not evolution under the averaged Hamiltonian.

## 5. Constructive next test and claim boundary

The N=4 comparison (8)–(11) is the smallest connected-cycle versus disconnected-cycle comparison within simple degree-2 bipartite graphs: equal native initial energy and equal BS16 means, but unequal native square correlations and fourth heat moments. It falsifies any claim that mean-link data plus total energy uniquely determine these relational spectral observables. It introduces no physical volume, dark density, spatial embedding, or fitted target.

For an actual authenticated BS state, the next scientific datum is its joint link correlations and the matched native probe response, not an assumed cycle preparation. The action's degree-only diagonal energy does not distinguish these two candidate ensembles at the displayed initial states; the real flip/formation/port dynamics must select or maintain any useful correlation structure. A successful small motif test would not establish macroscopic dimension, a causal cone, gravity, or dark-sector phenomenology.

Information can therefore preserve graph-local structure despite homogeneous mean links. Recovering it operationally is a genuine additional requirement. If mean BS16 is retained as the declared geometry, its limitations stand; changing to a correlation-sensitive or conditional geometry needs an explicit versioned construction, not a silent reinterpretation.
