# Exact native shared-link record binding

2026-09-27. Analytical consolidation, not a numerical run or new microscopic interaction. Construct: the existing `F3-QIRN-V001`, restricted to one N=1 slab. Conditional relaxed energies are not actual formed-state energies or spatial forces.

The resident recovered `BS_MICRO_ACTION.md` was read completely after its flag check; SHA256 `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`. Equations BS06, BS09–BS13 supply the terms below. The resident `NATIVE_RECORD_INTERACTION_REVIEW_V001.md` already records independent review of the one-edge storage costs and graph susceptibility. Its two underlying interaction notes are now dataless and were not opened. Thus this is an explicit all-parameter source rederivation and consolidation of that mechanism, not a newly discovered interaction or fresh numerical confirmation.

## 1. Exact invariant reduction, with the common energy retained

Set all formation couplings and ports, including their boundary Hamiltonian, to zero. Let all carrier, writer and reservoir registers be blank. Fix endpoint record occupations q_L,q_R in {0,1}, with any fixed allowed contents. The carrier transfer and current operators annihilate the carrier vacuum, while the remaining action preserves each record occupation. This is an invariant sector; the link remains fully dynamical.

Write U=U_d, lambda=lambda_R, s=q_L+q_R and

\[
 a=\Delta+2U(1-2d_*),\qquad C_s=2Ud_*^2+\epsilon_r s.
\]

Since n²=n and h_N=Omega/N=Omega at N=1, the complete restricted Hamiltonian and its conditional ground energy are

\[
 H_s=C_s I-\Omega X+(a-\lambda s)n,
\quad
 e(s)=C_s+F(a-\lambda s),
\quad F(z)=\frac{z-\sqrt{z^2+4\Omega^2}}2.                \tag{1}
\]

The two eigenvalues are separated by \(\sqrt{(a-\lambda s)^2+4\Omega^2}>0\). The scalar 2Ud_*², positive storage costs, and link energy all remain in (1); no arm-dependent energy reference has been removed. Unlisted decoupled spectators, if included, require the same fixed energy in every arm. This is the ground within the declared invariant sector, not a claim about the ground of every register/port sector.

## 2. Strict binding, enhanced occupation, positive insertion cost

For Omega>0,

\[
 F'(z)=\frac12\left(1-\frac{z}{\sqrt{z^2+4\Omega^2}}\right)
 \in(0,1),\qquad
 F''(z)=-\frac{2\Omega^2}{(z^2+4\Omega^2)^{3/2}}<0.     \tag{2}
\]

Use the smooth interpolation of (1) only as a mathematical external-bias device; record eigenvalues themselves remain binary. Then

\[
 e''(s)=-\frac{2\lambda^2\Omega^2}
 {[(a-\lambda s)^2+4\Omega^2]^{3/2}}<0
 \quad(\lambda\Omega>0).                              \tag{3}
\]

Consequently the native binary cross-cost is exactly

\[
 \boxed{E_{11}-E_{10}-E_{01}+E_{00}
 =e(2)-2e(1)+e(0)
 =\int_0^1\!du\int_0^1\!dv\ e''(u+v)<0.}             \tag{4}
\]

The linear storage and common scalar terms cancel from this cross-cost, not from the individual energies. The mechanism is two records lowering the energy of the **same responsive link**, followed by conditional link relaxation; there is no added record-pair term.

For lambda>0, Hellmann–Feynman gives the relaxed link occupation

\[
 m(s)=\langle n\rangle_s=F'(a-\lambda s),\qquad
 m'(s)=\frac{2\lambda\Omega^2}
 {[(a-\lambda s)^2+4\Omega^2]^{3/2}}>0.                 \tag{5}
\]

For lambda>0, because e'(s)=epsilon_r-lambda m(s), both allowed successive insertions obey

\[
 \boxed{\epsilon_r-\lambda<e(s+1)-e(s)<\epsilon_r,
 \qquad s=0,1.}                                      \tag{6}
\]

Thus epsilon_r>lambda is a sufficient positive-insertion domain despite negative binding. This inequality is an additional sufficient restriction, not implied by the source's weaker positive bare storage gap. It is compatible with BS13; no parameter value is selected here. The second insertion costs less than the first but is not free. At lambda=0 binding vanishes. The Omega=0 limit can have diagonal level crossings and is not covered by the strict smooth proof.

## 3. The valid graph generalization and its limit

In the same finite graph-only hold, replace binary feedback labels by **external** real sources x_v solely to define a response:

\[
 H(\mathbf x)=H_{\rm graph}+\epsilon_r\sum_vx_v I
              -\lambda\sum_vx_v d_v.                 \tag{7}
\]

This does not reinterpret a fractional source as fractional record occupation. For fixed finite N and h_N>0, the full incidence hypercube has connected negative flip off-diagonals. Its ground is unique and gapped. On that branch,

\[
 E_{,uv}=-2\lambda^2\operatorname{Re}\sum_{r>0}
 \frac{\langle0|d_u|r\rangle\langle r|d_v|0\rangle}
 {E_r-E_0}.                                           \tag{8}
\]

For every real vector c, its quadratic form is
\(-2\lambda^2\sum_{r>0}|\langle r|\sum_vc_vd_v|0\rangle|^2/(E_r-E_0)\leq0\). Thus the Hessian is negative semidefinite, **not** entrywise negative: distinct degree operators can compete, as the earlier native sign counterexample records.

If two sources instead couple with the same positive coefficient to the identical operator A, their cross derivative is a negative sum of \(|\langle r|A|0\rangle|^2\). It is strictly negative when A does not act as a scalar on the ground. Integrating that derivative over a unit source square proves strictly negative binary binding if these conditions hold throughout. The single link is exactly this case, d_L=d_R=n. No such identity is assumed for arbitrary distinct vertices.

Native scaling remains h_N=Omega/N. The N=1 formula cannot be copied across an N>1 complete bipartite slab: other flips remain active and the degree penalties couple edges. Binding magnitude, gaps and collective persistence require their own finite-size analysis; this calculation supplies no survival claim in the large-N limit.

## 4. Constructive consequence and next interface

The action already has a genuine storage-mediated energetic association with positive record costs. What remains is to evaluate its relevance on actually formed, unrepinned states with the complete preparation/controller work ledger and existing inclusive carrier/record readouts. Ground relaxation is not an attractor of source-off unitary dynamics. Turning the cross-cost into an operational attraction requires a motion/distance interface, and turning it into pressure requires an owned physical deformation. Neither a metric, stress, cosmological abundance nor a joint dark-matter/dark-energy mechanism is inferred from (4).
