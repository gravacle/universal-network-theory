# Native graph-mediated record energy: susceptibility, null mode, and binding

Date: 2026-09-27. Status: exact conditional graph-ground-energy analysis of existing BS couplings, not a new microscopic record-pair term or an executed numerical test.

Source: resident recovered [BS microscopic action](recovered_sources/BS_MICRO_ACTION.md), SHA256 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec. Flags were checked before rereading BS06/BS10/BS11. Those terms supply link flips, degree penalties, storage, and the occupation–degree coupling; they contain no direct logical-content or record-pair interaction. This extends the [uniform-feedback ground-response result](NATIVE_RECORD_FEEDBACK_GROUND_RESPONSE_V001.md), without assuming its selected N=4 coefficient example.

## 1. Conditional energy and exact response kernel

Fix one finite N+N slab, no carriers, all formation/copy couplings g=0, and no graph-dependent ports. For physical record occupations q_v∈{0,1}, the same native Hamiltonian restricted to a fixed q pattern is

\[
 H(\mathbf q)=U\sum_v(d_v-d_*)^2+\Delta M-h\sum_eX_e
 -\lambda\sum_vq_vd_v+\epsilon\sum_vq_v+E_{\rm other},\qquad
 M=\sum_e n_e,\quad h=\Omega/N>0.                                     \tag{1}
\]

Here λ=λ_R>0 and ε=ε_r. Let x_v be independent real auxiliary source parameters replacing q_v solely to differentiate the conditional ground energy. This does not turn binary record occupations into continuously variable eigenvalues. Write E(x) for the complete conditional ground energy, including storage.

All link configurations are connected by negative off-diagonal flip amplitudes. At finite N≥1 and h>0 the graph ground state |g_x⟩ is unique and positive on every bit string. Its spectral derivatives are therefore

\[
 \partial_{x_v}E=\epsilon-\lambda\langle d_v\rangle_x,\qquad
 \partial_{x_v}\partial_{x_w}E=-\lambda^2\chi_{vw},
\]
\[
 \chi_{vw}=2\,\operatorname{Re}\sum_{\nu>0}
 {\langle g|d_v|\nu\rangle\langle\nu|d_w|g\rangle
  \over E_\nu-E_g}.                                                   \tag{2}
\]

This is the static degree susceptibility: for a Hamiltonian perturbation −Σ_w b_w d_w, ∂⟨d_v⟩/∂b_w=χ_vw. Consequently ∂⟨d_v⟩/∂x_w=λχ_vw. The kernel has inverse-energy units; the occupation-energy Hessian −λ²χ has energy units.

An equivalent exact ground-connected representation is

\[
 \chi_{vw}
 =2\operatorname{Re}\int_0^\infty d\sigma\,
 \langle g|\delta d_v\,e^{-\sigma(H_g-E_g)}\,\delta d_w|g\rangle,        \tag{3}
\]

where H_g is the graph Hamiltonian with the scalar storage term removed, E_g its ground energy, and σ has inverse-energy units. This is not a physical-time evolution formula or an identification with equal-time covariance alone.

For any real vector c, D_c=Σ_v c_vd_v gives

\[
 \mathbf c^T\chi\mathbf c
 =2\sum_{\nu>0}{|\langle\nu|D_c|g\rangle|^2\over E_\nu-E_g}\ge0.        \tag{4}
\]

Hence the complete energy is concave in these auxiliary controls. Storage is linear and does not change the Hessian.

## 2. Exact bipartite null mode and the uniform response

Every graph satisfies

\[
 \sum_{v\in L}d_v-\sum_{w\in R}d_w=0.
\]

Thus η=(1_L,−1_R) is an exact null vector of χ. It is the only null direction under the assumptions above. Indeed equality in (4) requires D_c|g⟩ to be proportional to |g⟩. Full support then requires D_c to be constant on every graph bit string. The empty graph fixes that constant to zero; a graph with one edge (i,j) forces c_i+c_j=0. For the complete possible-link set K_(N,N), this means all left coefficients equal one constant and all right coefficients its negative:

\[
 \ker\chi=\operatorname{span}\{\eta\},\qquad
 \operatorname{rank}\chi=2N-1.                                      \tag{5}
\]

Since the equal-size layers also give Σ_vη_v=0, E(x+sη)=E(x) exactly when storage is uniform as in (1). This is a redundancy of this control coupling, not a derived spacetime gauge symmetry. If h=0, links are removed, extra constraints are imposed, or fields couple to additional operators, the stated exact null-space result need not apply. In particular, projecting first to an exactly regular-degree manifold sets every d_v to a constant and discards the virtual degree-changing states needed in (2).

Uniform x_v=x has D_1=Σ_vd_v=2M and a=Δ−2λx. Therefore

\[
 {d^2E(x\mathbf1)\over dx^2}
 =4\lambda^2 E_g''(a)
 =-\lambda^2\mathbf1^T\chi\mathbf1<0,\qquad
 {d\langle M\rangle\over dx}=-2\lambda E_g''(a)>0.                    \tag{6}
\]

This recovers the prior strict uniform-feedback theorem as one non-null direction of the full kernel.

## 3. Concavity does not mean every record pair attracts

For distinct v,w and a fixed binary background with these two sites empty, define the exact finite insertion interaction

\[
 V_{vw}(\mathbf q_{\rm rest})
 =E_{11}-E_{10}-E_{01}+E_{00}
 =-\lambda^2\int_0^1dr\int_0^1ds\,
 \chi_{vw}(\mathbf q_{\rm rest}+r\mathbf e_v+s\mathbf e_w).             \tag{7}
\]

Negative V means subadditive insertion energy relative to this specified background. A positive-semidefinite χ need not have nonnegative individual off-diagonal entries. Thus (4) neither proves V_vw≤0 for all pairs nor supplies a universal attractive force.

This distinction occurs within the native family, not only in abstract matrices. The separate [finite-h native sign counterexample](NATIVE_RECORD_INTERACTION_SIGN_COUNTEREXAMPLE_V001.md) uses N=2, U=λ=1, Δ=3, d_*=7/8, ε=3 and h=1/64: a same-layer pair on an occupied opposite-layer background has positive V, while an opposite-layer pair on the blank background has negative V, with analytic sign margins. That note owns the exact matching minimization and norm-bound proof. No new pair interaction, frozen link, or numerical fit is used.

The full binary energy table can contain background-dependent pair coefficients and higher-order occupation interactions. Replacing it by a universal sum of pair potentials is another approximation, not a consequence of the Hessian.

## 4. One native edge: exact attractive insertion interaction

For N=1, d_1=d_2=n. Put

\[
 a_0=\Delta+2U(1-2d_*),\qquad
 f(a)={a-\sqrt{a^2+4h^2}\over2}.
\]

The exact complete conditional ground energy is

\[
 E(q_1,q_2)
 =2Ud_*^2+\epsilon(q_1+q_2)
 +f\!\left(a_0-\lambda(q_1+q_2)\right)+E_{\rm other}.                  \tag{8}
\]

No small-h approximation is made. Since

\[
 f'(a)=\frac12\left(1-{a\over\sqrt{a^2+4h^2}}\right),\qquad
 f''(a)=-{2h^2\over(a^2+4h^2)^{3/2}}<0,
\]

the storage terms cancel from the inclusion-exclusion combination:

\[
 V_{12}=f(a_0-2\lambda)-2f(a_0-\lambda)+f(a_0)
 =\int_0^\lambda du\int_0^\lambda dv\,f''(a_0-u-v)<0                  \tag{9}
\]

for h,λ>0. The susceptibility is rank one here, with null vector (1,−1).

Binding does not eliminate insertion cost. In the general slab,

\[
 H(\mathbf q+\mathbf e_v)-H(\mathbf q)
 =\epsilon I-\lambda d_v
 \succeq(\epsilon-\lambda N)I.                                      \tag{10}
\]

Thus ε≥λN makes each insertion nonnegative as an operator comparison. At equality, finite h>0 and λ>0 still give a strictly positive conditional ground-energy increment: full support implies ⟨d_v⟩<N throughout the interpolation. For N=1, each sequential insertion cost is

\[
 \epsilon+f(a-\lambda)-f(a)
 =\epsilon-\int_{a-\lambda}^{a}f'(z)\,dz,
 \qquad \epsilon-\lambda<\Delta E_{\rm insert}<\epsilon.              \tag{11}
\]

As an illustrative fixed native point, set N=1, U=1, λ=1, Δ=3, d_*=1, h=1/2, ε=2, t=0, g=0 and ports absent, with U defining the energy unit and E_other=0 for the displayed absolute energies. Then

\[
 E_{00}={5-\sqrt2\over2},\quad
 E_{10}=E_{01}={7\over2},\quad
 E_{11}={11-\sqrt2\over2},\quad
 V_{12}=1-\sqrt2<0.                                                  \tag{12}
\]

The two insertion costs are 1+√2/2 and 2−√2/2, both greater than 1; their sum is 3. This point meets Δ≥2λ+δ_E with δ_E=1 and ε−λN=1. It is an analytic example, not parameter inference from observations.

## 5. Exact energy table versus actual record dynamics

The table E(q) is the exact lowest energy of each invariant fixed-q sector. Because g=0, one can define a graph-dressed invariant subspace by mapping each record occupation basis state to that same state tensored with its conditional graph ground state |g_q⟩. On that specifically dressed subspace the Hamiltonian is diagonal with entries E(q). This is a precise effective occupation-energy description, not an added microscopic pair term.

A generic formed state or bare record superposition need not occupy that subspace. Conditional graph excitations, graph overlaps in reduced record coherences, preparation energy, and actual source/relaxation history cannot be dropped. The resulting energies depend on occupations, not the 0/1 logical contents within an occupied record, in agreement with the native label-blind coupling.

All q_v remain conserved in this source-off hold. An induced negative insertion interaction therefore supplies no record transport, no demonstrated clustering trajectory, and no position-dependent force. Nor does negative binding energy determine pressure: no physical distance/volume deformation has been varied here. The constructive result is an exact native, generally non-pairwise occupation-energy kernel and a controlled attractive one-edge example, with the positive storage ledger intact. Promoting it to a dark-matter mechanism still requires an independently owned transport/relational-position and dynamical preparation route; promoting it to a dark-energy stress requires the corresponding physical work variation.
