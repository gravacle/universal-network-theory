# Native q4 covariance metric and energy: exact identification and envelope

2026-09-27. Conditional analytical comparison; no numerical run, adopted new state-selection law, deformation law, physical pressure, or cosmological inference.

Read in full after resident flag checks: program-worktree/LANE_CROSS_RFT_GRA_GL6U_F3_DEGREE_INTERACTION_Q4_RESPONSE_V001/THEOREM.md (GL6U, U04–U13), and Q4_FIXED_CELL_VOLUME_SCREEN_V001.md. The former supplies the native active-star Hamiltonian; the latter supplies the explicitly adopted metric g = ell² Cov(PZ)|_(1-perp), with a fixed ruler ell and P = I−11^T/4. Applying that metric prescription to GL6U remains a conditional interface, not a result of its rank-six response theorem.

## 1. Same-parent Hamiltonian and the metric's missing information

Set J_i = (1/2)Σ_{a=1}^4 σ_i^(a), U = U_d, and d = Σ_a n_a = 2−J_z. Expanding the complete active block U04, without dropping its scalar, gives

\[
 H=-2hJ_x+U J_z^2-BJ_z+C,
 \quad B=\Delta+U(5-4d_*),
\]
\[
 C=2\Delta+U(6-8d_*+5d_*^2)+C_{\rm spec}.            \tag{1}
\]

C_spec denotes the branch-independent spectator/reference scalar left unspecified by U04. It must be owned before claiming an absolute physical energy. As a check, the active all-blank value is C+4U−2B = 5Ud_*²+C_spec, agreeing with U04. No baseline has been reset between compared states.

For any permutation-invariant four-qubit density matrix, write ⟨Z_a⟩ = z and ⟨Z_a Z_b⟩ = c for a ≠ b. Then ⟨J_z²⟩ = 1+3c and projection removes the uniform mean. With q = ⟨J_z²⟩,

\[
 \boxed{F=\operatorname{Cov}(PZ)|_{1^\perp}
       =fI_3,\qquad f=1-c=\frac{4-q}{3}.}            \tag{2}
\]

Here q is a spin second moment, not a record occupation label. Its range is 0 ≤ q ≤ 4 and 0 ≤ f ≤ 4/3; a positive metric excludes f = 0. Permutation invariance of a density matrix need not imply support only in the symmetric spin-two subspace. The native all-blank unitary history does remain in that subspace, as GL6U proves.

Equation (2) contains neither ⟨J_x⟩ nor ⟨J_z⟩ separately, while

\[
 E=C+Uq-2h\langle J_x\rangle-B\langle J_z\rangle.    \tag{3}
\]

Even the full Z probability distribution omits the transverse coherence needed by the first term in (3).

## 2. Exact equal-metric counterexample and a native energy readout

Take |ψ_+⟩ = |+x⟩^⊗4 and |ψ_-⟩ = |−x⟩^⊗4. Both have the identical uniform distribution over all sixteen Z strings, z = c = 0, q = 1 and F = I_3. Nevertheless

\[
 \langle J_x\rangle_\pm=\pm2,\quad
 E_\pm=C+U\mp4h,\qquad E_- - E_+=8h.               \tag{4}
\]

The permutation-invariant diagonal unitary Π_a Z_a interchanges these states while preserving every Z statistic. Thus graph phases hidden from this covariance metric carry native energy. The pair is a kinematic counterexample within the same active Hamiltonian, not a claim that both states arise from the same frozen blank-writing history or can be interchanged without work. Source-off energy conservation would itself preclude such a free change when h > 0.

The source already identifies a way to resolve this particular missing energy datum. GL6U U09/U13 use x_link = ⟨X_1⟩ = ⟨J_x⟩/2 and the native pair-response eigenvalue D_T2 = −8h x_link. Hence

\[
 \boxed{E=C+U(4-3f)+\tfrac12D_{T_2}-2Bz.}           \tag{5}
\]

Measuring the same-state single-Z mean and transverse-sensitive response, with their native normalization and the scalar ledger, would reconstruct this finite-block energy. This is an exact energy-tomography relation, not identification of D with the covariance metric or with physical mechanical stress. In particular, the equal-F states (4) have opposite D_T2.

## 3. A complete constrained-energy envelope, without assuming it is realized

One possible extra state-selection rule would minimize native energy at fixed metric second moment. Define it explicitly rather than identifying it with the actual formed state:

\[
 \mathcal E_{\min}(q)
 =\min_{\rho\ge0,\ \operatorname{Tr}\rho=1,
                  \operatorname{Tr}(\rho J_z^2)=q}
                          \operatorname{Tr}(\rho H).            \tag{6}
\]

Permutation averaging changes neither constraint nor objective, so a permutation-invariant minimizer is available. Introduce the formal dual energy

\[
 e_0(\eta)=\lambda_{\min}(H+\eta J_z^2).
\]

For every η and feasible state, E ≥ e_0(η)−ηq. In finite dimension the exact lower boundary is

\[
 \boxed{\mathcal E_{\min}(q)
       =\sup_{\eta\in\mathbb R}[e_0(\eta)-\eta q].}  \tag{7}
\]

There is a direct proof of equality here for h > 0, with no numerical minimization. H+ηJ_z² is real with strictly negative single-bit-flip off-diagonals on the connected sixteen-state cube. Its unique ground vector is strictly positive and permutation symmetric, hence lies in the native j = 2 subspace. There its exact matrix, indexed by m = −2,…,2, is

\[
 (H_\eta)_{mm}=C+(U+\eta)m^2-Bm,\qquad
 (H_\eta)_{m,m+1}=-h\sqrt{6-m(m+1)}.                 \tag{8}
\]

The derivative q(η) = e_0′(η) obeys

\[
 q'(\eta)=-2\sum_{r>0}
 \frac{|\langle r|J_z^2|0\rangle|^2}{E_r-E_0}<0.     \tag{9}
\]

Strictness follows because the full-support ground vector is not an eigenvector of J_z². The limits are q(η) → 0 as η → +∞ and q(η) → 4 as η → −∞; bounded remaining terms cannot change the leading preference of ηJ_z². Continuity therefore supplies a unique η for each 0 < q < 4. Its ground state saturates the lower bound, proving (7); endpoints follow by limits or direct constrained states. In particular,

\[
 \frac{d\mathcal E_{\min}}{dq}=-\eta,
 \qquad \frac{d\mathcal E_{\min}}{df}=3\eta          \tag{10}
\]

on the interior. This exact five-state criterion can supply an energy envelope and its conjugate constraint response once that state-selection question is genuinely posed. η is presently a Lagrange multiplier, not an owned physical strain, controller, or microscopic change of coupling. Equation (7) does not show cooling, equilibration or preparation.

## 4. Sharp special cases

### Diagonal comparison, h = 0

This is a mathematical zero-flip comparison, not the frozen formed-KEEP protocol with h > 0. If B = 0, every state at fixed q has

\[
 E=C+Uq=C+4U-3Uf.                                   \tag{11}
\]

If B ≠ 0, q still does not determine energy. The sharp maximum possible |⟨J_z⟩| at fixed q is

\[
 z_{\max}(q)=
 \begin{cases}q,&0\le q\le1,\\(q+2)/3,&1\le q\le4.\end{cases}
\]

These are the upper convex-hull boundary segments through (m²,m) = (0,0),(1,1),(4,2), attained by distributions on the corresponding Dicke states. Thus the exact energy range is C+Uq ± |B|z_max(q). Even a diagonal Hamiltonian needs the first moment unless B vanishes.

### B = 0 with the native transverse term h > 0

For U > 0, B = 0 requires d_* = (5+Δ/U)/4. This is a prospective subfamily of U04, not an adopted point or the U21 witness. It is outside U19's positive-δ_1 small-prewait domain because δ_1 = −3U there. None of U19's particular response-sign conclusions is transferred to it.

In the even spin-two basis |s_2⟩ = (|2⟩+|−2⟩)/√2, |s_1⟩ = (|1⟩+|−1⟩)/√2, |0⟩, J_x has off-diagonals 1 and √3. A minimizing biased ground state has nonnegative amplitudes a,b,c in this basis. With A = a², the norm and second-moment constraints give b² = q−4A and c² = 1−q+3A. Hence the following one-variable formula is exact, not a product-state ansatz:

\[
 X_{\max}(q)=
 \max_{\max(0,(q-1)/3)\le A\le q/4}
 2\sqrt{q-4A}\,[\sqrt A+\sqrt{3(1-q+3A)}],
\]
\[
 \boxed{\mathcal E_{\min/\max}(q)
           =C+Uq\mp2hX_{\max}(q).}                  \tag{12}
\]

The opposite endpoint follows by the same Z-phase unitary that reverses J_x. For every 0 < q < 4, X_max > 0 and the equal-metric energy interval is nonzero. At q = 1, X_max = 2, so (4) attains both sharp bounds; at q = 0 or 4 it is zero. Thus even in the zero-detuning subfamily the transverse native term prevents a single energy function of F without specifying the state-selection rule.

## 5. What this closes, and what stress still needs

The adopted q4 covariance metric is not an energetically complete coarse-grained variable. Equation (5) supplies an exact native finite-block energy reconstruction, and (7) supplies a well-defined conditional equilibrium envelope. Neither supplies the absent mechanical work coupling.

To turn either into stress, the parent must specify the physical metric-deformation source, including the full derivative of its Hamiltonian/action, identity/reference terms, and retained state or justified adiabatic/equilibrium selection. A derivative of (11) along changed state statistics, or the multiplier slope (10), is not automatically pressure. Treating an actual formed state as the minimizer in (6) would change the scientific question. The source explicitly leaves physical six-source dilation and metric calibration open.

This is a concrete discriminant for the proposed explanatory chain: native record-gated degree interaction and a finite pair response are supported by GL6U; neither historical record density, macroscopic rigidity, a Newtonian/low-acceleration force law, nor topology-driven accelerated expansion follows from that response or from F alone. Those links require the independently owned stress, dynamics, continuum/probe and formation interfaces. No extrapolation to a physical volume or clock, no numerical experiment, and no new model choice is made here.
