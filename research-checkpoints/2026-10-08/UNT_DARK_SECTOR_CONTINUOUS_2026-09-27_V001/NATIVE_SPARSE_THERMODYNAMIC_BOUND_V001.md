# Native sparse-limit and empty-degree ground-state bounds

Date: 2026-09-27. Status: exact analytical screen; no numerical physics run. This is the carrier-free, source-off, fixed-record, one-slab BS parent, not a formed-state or full-UNT result. The native normalization is **h_N = Ω/N with Ω fixed**, not fixed h across different N. N counts vertices per layer; it is not identified with physical volume or a clock.

## 1. Owned parent and complete energy convention

Source: recovered_sources/BS_MICRO_ACTION.md, BS06 (incidence Hamiltonian and h_N), BS10–11 (record storage and feedback), BS13–14 (sufficient bounds). Source SHA256: 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec. The source was read after checking that it was resident. Finite-N conventions and strict ground response are also recorded in NATIVE_RECORD_FEEDBACK_GROUND_RESPONSE_V001.md, SHA256 6d3d2008e69a2cf1f55637fe2155c94b4d954bdba01e8604e6d103461b72de22.

There are N left and N right vertices and N² independent possible edges. Write n_e for the binary edge projector, X_e for its flip, d_v = Σ_{e incident to v} n_e, and M = Σ_e n_e. Set U = U_d ≥ 0, λ = λ_R ≥ 0, and fix every record occupation to the same q ∈ {0,1}. Remove carriers, turn record-target formation off, and take ports absent or graph-independent. Then

\[
 H_g=U\sum_{v=1}^{2N}(d_v-d_*)^2+a_qM+V_N,
 \quad a_q=\Delta-2\lambda q,
 \quad V_N=-\frac{\Omega}{N}\sum_eX_e.                 \tag{1}
\]

The complete energy includes 2N ε_r q in addition to H_g. Any other identical spectator constant must be declared separately. In particular, the empty-graph contribution 2NUd_*² is retained throughout. BS13 implies a_q ≥ δ_E > 0 in this carrier-free sector. All coefficients and d_* are fixed as N varies. These are the assumptions used below, not an optimization over them.

## 2. Statewise flip bound and finite energy density

For any graph density matrix, including an entangled or mixed one, set p_e = ⟨n_e⟩ and m = ⟨M⟩. The reduced edge Bloch bound and Cauchy–Schwarz give

\[
 |\langle X_e\rangle|\le2\sqrt{p_e(1-p_e)},\qquad
 |\langle V_N\rangle|
 \le\frac{2\Omega}{N}\sqrt{m(N^2-m)}
 \le2\Omega\sqrt m.                                  \tag{2}
\]

The operator norm remains ||V_N|| = ΩN. Equation (2) is a state-dependent improvement, not an operator-norm claim.

The nonnegative degree penalty and native norm bound imply E ≥ a_q m − ΩN. The empty computational graph has energy 2NUd_*², so any ground state satisfies

\[
 \frac mN\le D_q:=\frac{2Ud_*^2+\Omega}{a_q}.           \tag{3}
\]

More generally, any family with energy expectation bounded above by a constant times N has m = O(N), under these same positivity assumptions. On a ground state, (2) and (3) improve the flip-energy bound to 2Ω√(ND_q) = O(√N). Thus its contribution to energy per N vanishes. This does not exclude quantum correlations or subleading selection among the many diagonal configurations.

## 3. Exact leading energy and quantized preferred degrees

Define, for an integer k ≥ 0,

\[
 w_q(k)=U(k-d_*)^2+\frac{a_q}{2}k,
 \qquad \phi_q(k)=2w_q(k).
\]

Since Σ_v d_v = 2M, the diagonal part of (1) equals Σ_v w_q(d_v). For every integer 0 ≤ k ≤ N a k-regular simple bipartite graph exists. Consequently its exact classical minimum is

\[
 E_{\rm cl}(N,q)
 =2N\min_{0\le k\le N,\ k\in\mathbb Z}w_q(k)
 =N\min_{0\le k\le N,\ k\in\mathbb Z}\phi_q(k).        \tag{4}
\]

A minimizing regular computational graph is a trial state with zero flip expectation. Applying (2) to the quantum ground state yields the rigorous sandwich

\[
 E_{\rm cl}-2\Omega\sqrt{ND_q}\le E_0(N,q)\le E_{\rm cl}.
                                                               \tag{5}
\]

At fixed coefficients the minimizing integers remain bounded; therefore

\[
 \lim_{N\to\infty}\frac{E_0(N,q)}N
 =\min_{k\ge0,\ k\in\mathbb Z}
       [2U(k-d_*)^2+a_qk].                            \tag{6}
\]

Add 2ε_r q for the complete energy per N. For U > 0 the continuous quadratic center is d_c(q) = d_* − a_q/(4U); the minimizing nonnegative integer is nearest to this center, with two adjacent minimizers at a nonnegative half-integer tie. Record feedback shifts the center by λ/(2U) from q = 0 to q = 1. It changes bounded-degree plateaus, not the N-scaling of the preferred degree. Finite-N strict ground response is compatible with these limiting plateaus.

The following statements concern measured degrees, not merely their mean. Let K_q be the minimizing integer set, and let δ_q = min_{k not in K_q}[w_q(k) − min w_q] > 0. For sufficiently large N, (5) implies

\[
 \frac1{2N}\sum_v\langle\mathbf1_{d_v\notin K_q}\rangle
 \le\frac{\Omega\sqrt{D_q}}{\delta_q\sqrt N}.          \tag{7}
\]

If the minimizer k_0 is unique, define δ_dist = min_{k ≠ k_0}[w_q(k) − w_q(k_0)]/|k − k_0| > 0. Then

\[
 \left|\frac mN-k_0\right|
 \le\frac{\Omega\sqrt{D_q}}{\delta_{\rm dist}\sqrt N}.  \tag{8}
\]

These follow by bounding the sum of the nonnegative vertex energy excesses by 2Ω√(ND_q). Equation (7) bounds the fraction of defective vertices; it does not prove that the entire measured graph is regular with high probability. At a tie it only concentrates degrees on the two minimizing values, without selecting their mixture or graph correlations. U = 0 with a_q > 0 is an empty-degree case covered next.

## 4. Sharper theorem in the empty-degree phase

Suppose

\[
 G_q:=a_q+2U-4Ud_*>0.                                 \tag{9}
\]

For U ≥ 0 this is precisely the strict first-step condition making degree zero the unique classical minimum. Define the nonnegative collision operator

\[
 C_{\rm inc}=\sum_v\sum_{e<f\ni v}n_en_f
             =\frac12\sum_vd_v(d_v-1).
\]

The exact operator decomposition is

\[
 H_g=E_{\rm cl}+G_qM+2UC_{\rm inc}+V_N,
 \qquad E_{\rm cl}=2NUd_*^2.                          \tag{10}
\]

Combining (2), (10), and the empty trial gives, at every N,

\[
 m\le\left(\frac{2\Omega}{G_q}\right)^2,
 \qquad
 E_{\rm cl}-\frac{\Omega^2}{G_q}\le E_0\le E_{\rm cl}.
                                                               \tag{11}
\]

This is O(1) total incidence, stronger than bounded mean degree. It does not depend on a perturbative gap estimate uniform in N.

The asymptotic constants are also fixed. Put c = (Ω/G_q)² and use a positive product link trial with p = c/N², for sufficiently large N. Its exact energy is

\[
 E_{\rm prod}-E_{\rm cl}
 =G_qc+\frac{2Uc^2(N-1)}{N^2}
      -2\Omega\sqrt c\sqrt{1-c/N^2}
 =-\frac{\Omega^2}{G_q}+\eta_N,                        \tag{12}
\]

where

\[
 \eta_N=\frac{2Uc^2(N-1)}{N^2}
    +2\Omega\sqrt c\,[1-\sqrt{1-c/N^2}]=O(N^{-1}).
\]

The lower bound for an arbitrary state is F(m) = G_qm − 2Ω√m, whose unique minimum is at m = c. The matching variational upper bound therefore proves

\[
 E_0-E_{\rm cl}\longrightarrow-\frac{\Omega^2}{G_q},
 \qquad \langle M\rangle_0\longrightarrow
                   \left(\frac{\Omega}{G_q}\right)^2. \tag{13}
\]

No product-ground-state assumption is made. The product state supplies only an upper bound, and the lower bound applies to every state. For U > 0 there is the further exact estimate

\[
 2U\langle C_{\rm inc}\rangle_0\le\eta_N.             \tag{14}
\]

Indeed E_0 − E_cl = F(m) + 2U⟨C_inc⟩ + T, with T = 2Ω√m − (Ω/N)Σ_e⟨X_e⟩ ≥ 0. Subtract min F and use (12). Since C_inc is integer-valued, the probability of any measured vertex having degree at least two is at most ⟨C_inc⟩ = O(1/N). Thus this phase has a finite expected number of edges with asymptotically vanishing collision probability. For U = 0, (13) still holds but (14) supplies no collision control.

## 5. Arbitrary retained patterns: a uniform sufficient bound

No balanced-count assumption is needed for the following corollary. Fix any binary q_v and let D_rec = Σ_v q_v. Restoring storage,

\[
 H=C(\mathbf q)+\sum_{e=(u,v)}G_en_e+2UC_{\rm inc}+V_N,
 \quad C(\mathbf q)=2NUd_*^2+\epsilon_rD_{\rm rec},
\]

with G_e = Δ + 2U − 4Ud_* − λ(q_u + q_v). If

\[
 G_{\min}:=\Delta-2\lambda+2U-4Ud_*>0,
\]

then every conditional-record ground sector obeys

\[
 \langle M\rangle_0\le(2\Omega/G_{\min})^2,
 \quad C(\mathbf q)-\Omega^2/G_{\min}
                 \le E_0(\mathbf q)\le C(\mathbf q). \tag{15}
\]

The graph ground correction is uniformly O(1), while record storage remains ε_r D_rec. This neither predicts record-pattern probabilities nor supplies their formation cost or preparation. Balanced nonempty-degree patterns are treated separately in NATIVE_BALANCED_RECORD_LEADING_ENERGY_V001.md.

## 6. Consequence for the inherited carrier-free benchmark

The finite N = 2 experiments used U = 1, d_* = 1, Δ = 4, λ = 1/2, ε_r = 1 and h_2 = 1. Their native fixed-Ω extension is therefore Ω = 2, not h_N = 1 for every N. At these unchanged coefficients,

\[
 G_q=2-q>0,\qquad
 \langle M\rangle_{q=0}\to1,\quad
 \langle M\rangle_{q=1}\to4.                           \tag{16}
\]

The complete ground energies, retaining the same reference and storage, are

\[
 E_{q=0}=2N-2+o(1),\qquad
 E_{q=1}=4N-4+o(1),\qquad
 E_{q=1}-E_{q=0}=2N-2+o(1).                           \tag{17}
\]

For any binary record pattern at these coefficients, (15) gives ⟨M⟩ ≤ 16 and 0 ≤ C(q) − E_0(q) ≤ 4. This diagnoses the **carrier-free conditional equilibrium** continuation of this benchmark: increasing N alone does not produce an extensive connected incidence structure in its ground sector. It is not a statement about the actual writer-formed state, the occupation-weighted source-control experiment, a carrier-populated phase, a physical spacetime, or all UNT mechanisms.

For U > 0, a strict preference for nonzero degree in the uniformly occupied classical sector requires d_* > 1/2 + (Δ − 2λ)/(4U); equality is a zero/one-degree tie. This is a prospective native phase criterion, not authorization to retune coefficients or evidence that nonzero degree suffices for geometry. At the inherited values its threshold is 5/4, whereas d_* = 1.

## 7. Limits and next scientific use

- Ground-state bounds do not show that source-off unitary evolution cools or prepares any ground state. The separate NATIVE_INCIDENCE_FORMATION_SPEED_BOUND_V001.md constrains real-time incidence preparation.
- At Ω = 0 diagonal minimization is exact, but finite-flip uniqueness and strict response claims do not apply. At Ω > 0, the present proof does not use finite-N degenerate perturbation theory: its earlier sufficient isolation condition h_N N²/U < 1 is not uniform under h_N = Ω/N.
- Carriers, graph-dependent ports, or formation donors can change the energetic sector and must be included before exporting this result to their states. A fixed h > 0 across N is a different, nonnative coefficient sequence; it cannot diagnose failure of the native fixed-Ω limit.
- No derivative with respect to N is assigned physical pressure. These results establish neither volume, stress, propagation, stability of an emergent metric, nor a dark-sector abundance.

The constructive checkpoint is now sharp: any claimed extensive-incidence geometry from this unchanged carrier-free ground benchmark must confront (15)–(17). A continuation must specify the actually occupied dynamical/energetic sector or a separately declared native parameter phase, and then test its geometry. Merely enlarging the current empty-degree ground-sector calculation is not that continuation.
