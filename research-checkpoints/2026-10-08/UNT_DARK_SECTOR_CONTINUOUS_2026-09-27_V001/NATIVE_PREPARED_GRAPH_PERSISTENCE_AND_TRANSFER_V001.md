# Native prepared incidence: local persistence and carrier transfer

2026-09-27. Construct `BS_PREPARED_MATCHING_TRANSFER_V001`. Exact analytic
bounds; no numerical execution, preparation claim, new interaction, hard
degree projection, or metric interpretation.

Source: resident `recovered_sources/BS_MICRO_ACTION.md`, BS06 and BS09--11;
SHA256 `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
Resident flags were checked before reading. N is the number of nodes in each
layer, with N^2 possible links. The existing action uses h_N=Omega/N.

## 1. Exact persistence of a prepared local incidence pattern

Start from |G><G| tensor an arbitrary nongraph density matrix. G is a graph
computational-basis state, not a ground state or a newly formed graph. Let
g_e in {0,1} denote its edge bits and Q_e be the projector onto the wrong
bit: Q_e=n_e for g_e=0, and Q_e=I-n_e for g_e=1. Assume

\[
 H(s)=-\frac{\Omega}{N}\sum_eX_e+H_{\rm rest}(s),
 \qquad [H_{\rm rest}(s),n_e]=0\quad\hbox{for every }e.       \tag{1}
\]

The listed native incidence, carrier, record-feedback, and onsite formation
terms satisfy this premise, even with time-dependent formation schedules.
Unspecified ports, resets, postselection, and additional incidence-changing
controls are not included.

For y_e(s)=<Q_e>, reduced-link positivity gives

\[
 |\dot y_e|\le\frac{2\Omega}{N\hbar}
       \sqrt{y_e(1-y_e)},\qquad y_e(0)=0.
\]

Integration, with endpoint regularization, yields

\[
 y_e(s)\le\sin^2\frac{\Omega s}{N\hbar}
 \quad\left(0\le\frac{\Omega s}{N\hbar}\le\frac\pi2\right),
 \qquad
 y_e(s)\le\left(\frac{\Omega s}{N\hbar}\right)^2
 \quad\hbox{for all }s\ge0.                            \tag{2}
\]

The sine bound must not be continued into its decreasing branch. Summing
the unconditional wrong-bit probabilities gives

\[
 \left\langle W_G\right\rangle
 :=\left\langle\sum_eQ_e\right\rangle
 \le(\Omega s/\hbar)^2.                               \tag{3}
\]

For a specified vertex v, the projector onto any wrong incident link is
I-product_{e incident v}(I-Q_e), bounded above by the sum of those Q_e.
Hence its probability is at most (Omega s/hbar)^2/N. The expected number
of vertices whose incident pattern has changed is at most
2(Omega s/hbar)^2; their expected fraction is at most
(Omega s/hbar)^2/N. These conclusions are independent of carrier/record
entanglement and need no energy estimate.

This is persistence of local incidence readouts, not a statement that the
whole graph has high survival probability. At fixed s the total expected
wrong-link count can be O(1), while each prescribed local star remains
unchanged with probability 1-O(1/N).

## 2. A controlled comparison with frozen-graph carrier dynamics

Small wrong-link populations alone do not justify replacing the Hamiltonian
by a frozen graph. A further native structural property supplies a direct
readout bound. With no additional ports, write BS06 and BS09--11 as

\[
 H(s)=H_{\rm graph}-\frac{\Omega}{N}\sum_eX_e
       +H_{\rm site}(s)+\sum_e n_e B_e,
 \qquad
 B_e=-t_{\rm hop}T_e+\lambda_JJ_e^2
                 -\lambda_R(q_u^r+q_v^r).             \tag{4}
\]

H_graph is graph-only and diagonal; H_site contains the nongraph onsite
energies and permitted local copying. The edge operators act only on their
two endpoint nongraph factors, with

\[
 \|B_e\|\le b:=|t_{\rm hop}|+\lambda_J+2\lambda_R.       \tag{5}
\]

Define the comparison Hamiltonian on nongraph factors by replacing n_e with
the *specified initial bit* g_e:

\[
 H_G(s)=H_{\rm site}(s)+\sum_e g_e B_e.                 \tag{6}
\]

This defines a comparison dynamics, not a new physical intervention. For a
nongraph readout A, let A_G(T,s)=U_G(T,s)^dagger A U_G(T,s). Differentiating
the exact full-state expectation of A_G(T,s) gives the identity

\[
 \langle A\rangle_{\rm full}(T)-\langle A\rangle_G(T)
 =\frac{i}{\hbar}\int_0^T ds\sum_e
   \left\langle(n_e-g_e)[B_e,A_G(T,s)]\right\rangle_{\rm full,s}.
                                                               \tag{7}
\]

Crucially, n_e-g_e is plus or minus Q_e, and Q_e commutes with the
nongraph commutator in (7). Positivity therefore gives

\[
 \left|\left\langle(n_e-g_e)C\right\rangle\right|
 \le y_e(s)\|C\|,                                    \tag{8}
\]

not merely a square-root-probability bound. No factorization of the evolved
joint state is used.

## 3. Explicit prepared matching: no propagation theorem imported

Choose G to be a perfect matching, so M=N and every vertex has degree one.
Let A be supported on the nongraph factors of one matched pair. H_G is a
sum of disjoint two-vertex-component Hamiltonians. Thus A_G(T,s) remains
supported on that same pair, even with arbitrary onsite formation schedules.
Exactly 2N-1 possible bipartite edges meet this pair; all other commutators
in (7) vanish. Equations (2), (5), (7), and (8) prove

\[
 \boxed{
 |\langle A\rangle_{\rm full}(T)-\langle A\rangle_G(T)|
 \le\min\!\left\{2\|A\|,
 \frac{2b\|A\|(2N-1)\Omega^2T^3}{3N^2\hbar^3}\right\}.
 }                                                        \tag{9}
\]

The initial nongraph state may be mixed or entangled across pairs. All graph
flips and all native possible-edge carrier couplings remain in the full
dynamics on the left. The comparison error is O(1/N) at fixed coefficients
and fixed elapsed time. It is not a uniform long-time estimate.

For a direct transport example, turn formation off, take fixed binary record
occupations, and place one carrier of fixed content at the left vertex u of
the selected matched pair (u,v), with other carrier registers blank. In the
frozen comparison, epsilon_psi and lambda_J contribute constants on this
one-carrier pair; record and graph energies do not move that carrier. Thus

\[
 \Pr_G(\hbox{carrier at }v;T)
       =\sin^2(t_{\rm hop}T/\hbar).                    \tag{10}
\]

Taking A=q_v^psi in (9) gives the same transfer probability in the full
native model up to the explicit O(1/N) bound. For nonzero fixed t_hop,
T=pi hbar/(2|t_hop|) therefore produces order-one transfer and asymptotically
unit transfer probability on that prepared edge. Native graph flips have
not been disabled to obtain this conclusion.

## 4. Scope and constructive consequence

Slow creation of an extensive graph from the empty state does **not** imply
that carriers cannot move on already prepared incidence. Equations (9)--(10)
give one exact controlled counterexample to that inference using the same
native normalization and action. They do not establish that the matching is
a selected phase, can be prepared within a proposed mission budget, or
persists for times growing without bound with N.

The readout comparison uses the endpoint-local form (4), not merely the
commutation premise (1). An arbitrary graph-diagonal but nonlocal port could
make a local readout depend on distant changed links and invalidate Section
3. General bounded-degree prepared graphs require an additional explicit
propagation estimate; none is assumed here. A matching is disconnected and
supplies neither a metric nor a recovered macroscopic locality, signal cone,
gravitational law, or cosmological expansion model. Its value is the rigorous
distinction between incidence formation and transport on owned initial
incidence, with the latter comparison error fully controlled.
