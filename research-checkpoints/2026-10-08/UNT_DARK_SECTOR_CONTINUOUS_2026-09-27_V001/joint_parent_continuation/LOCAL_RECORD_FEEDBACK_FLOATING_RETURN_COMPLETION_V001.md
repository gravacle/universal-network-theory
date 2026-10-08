# Conditional floating-return completion of the passive five-island circuit

Date: 2026-10-05. Claim class: exact neutral-capacitance quotient, finite all-content record/return charge code and explicit charging-source comparison. Root, native and observer independently reviewed the prospective algebra. This is a bounded new circuit-class construction, not adoption of a universe, physical metric, canonical full-record source, volume law or dynamical strain. No job, matrix reconstruction, pseudoinverse calculation or old-file mutation was used.

## 1. Circuit domain and one floating return

Use the declared balanced simple bipartite q4 support with V=2N native vertices, eta_A=+1 and eta_B=−1. Retain the exact shared-link endpoint code from the earlier note. Each vertex has the five passive terminal/record islands of the frozen five-island construction, with its complete grounded matrix \(C_{5,v}>0\) and inverse \(\mathcal E_{5,v}\). Its exact nonnegative ground-capacitor weights are retained.

Let m=5V and set
\[
 C_{\rm rel}=\bigoplus_v C_{5,v},\quad
 c=C_{\rm rel}\mathbf1,\quad s=\mathbf1^TC_{\rm rel}\mathbf1,
 \quad
 C_{\rm full}=\begin{pmatrix}C_{\rm rel}&-c\\-c^T&s\end{pmatrix}.
 \tag{1}
\]
The previous grounds are joined to one finite floating return conductor. Because every row sum of each passive grounded block is nonnegative, c consists of nonnegative capacitances to that conductor. All port/record mutual capacitor branches remain unchanged.

This is a specified ideal passive capacitor network with one common return and the stated shielding/block-domain assumptions. A complete unrestricted Maxwell/exterior-field geometry need not have this matrix. No hidden exterior capacitance, ground reservoir, connector kinetic energy or mechanical support is assumed absent by physics; the present claim is conditional on the stated static circuit domain.

## 2. Exact quotient and included return field energy

Define \(B=\begin{pmatrix}I_m\\-\mathbf1^T\end{pmatrix}\). Then
\[
 C_{\rm full}=B C_{\rm rel}B^T.
 \tag{2}
\]
Since \(C_{\rm rel}\) is positive definite, \(C_{\rm full}\) is positive semidefinite of rank m and has precisely the common-potential gauge kernel \(\operatorname{span}\{\mathbf1_{m+1}\}\). Equivalently, its potential quadratic form is
\[
 (v,v_0)^TC_{\rm full}(v,v_0)
 =(v-v_0\mathbf1)^TC_{\rm rel}(v-v_0\mathbf1).
\]
For any actual island-charge vector x, the neutral complete charge is
\[
 Q_{\rm full}=(x,-\mathbf1^Tx)=Bx.
\]
Choose \(w=(C_{\rm rel}^{-1}x,0)\). Direct substitution gives \(C_{\rm full}w=Q_{\rm full}\), using \(c^TC_{\rm rel}^{-1}=\mathbf1^T\). The Moore--Penrose solution differs from w only by a common gauge potential, which drops out of its pairing with the neutral charge. Therefore
\[
 \boxed{\quad\tfrac12Q_{\rm full}^TC_{\rm full}^{+}Q_{\rm full}
             =\tfrac12x^TC_{\rm rel}^{-1}x.\quad}
 \tag{3}
\]
This is an algebraic quotient proof, not a numerical pseudoinverse tolerance or an assumption about near-zero eigenvalues. All scored charges lie in the neutral domain.

In **this specified circuit**, the return conductor's electrostatic field energy is already in (3). An independent extra generic countercharge self-energy would change the circuit or double count that field contribution. This does not contradict the earlier generic countercharge note: that note had not specified a complete physical field-energy kernel. Any genuinely additional donor, chemical, Josephson/tunnel, gauge, support, exterior or controller term still requires its own energy and sources.

## 3. Charging compression and record cost

On the endpoint code, each port charge is \(\eta_v q_*Z_e\), and the record-island charge is \(\eta_vq_Rq_v\). Every original link has opposite endpoint charges, so the ports sum to zero globally. Let
\[
 K=\sum_v\eta_vq_v,
 \qquad Q_0=-q_RK
 \tag{4}
\]
be the return charge. Substituting these charges in (3) gives exactly the frozen five-island charging polynomial:
\[
 H_{\rm cap}
 =U\sum_vc_v^2-\lambda_R\sum_vq_vc_v
       +A_R\sum_vq_v^2+2q_*^2e_dVI,
 \quad U=2q_*^2e_m,\quad
 \lambda_R=2q_*q_Rg,\quad A_R=\tfrac12q_R^2e_R.
 \tag{5}
\]
The global return does not add a favorable negative term or remove \(A_Rq_v\). The passive five-island bounds remain \(A_R\ge\lambda_R^2/(4U)\) and \(A_R\ge\lambda_Rq_R/(4q_*)\); at the present tuple the first is \(A_R\ge1/16\). qR, alpha=e_d/e_m and the complete absolute reference are not selected here.

At fixed all-q1 and fixed census, the record/self contribution is a common held-block reference. It remains in inclusive source/count/geometry work. For changing records it is a real operator cost. Neither this positive charging cost alone nor its bound determines a complete microscopic record detuning after all physically owned donor/binding/support terms are included.

## 4. Finite all-content return code and copy

Use a return charge-number basis \(|n_0\rangle\), \(n_0=-N,\ldots,N\), with \(Q_0=q_Rn_0\). For every original record/incidence word, retaining all occupied content labels, define
\[
 W|\mathrm{word}\rangle
 =|\mathrm{word}\rangle\,|n_0=-K(\mathrm{word})\rangle.
 \tag{6}
\]
Different original words remain orthogonal even when they have the same K; thus W is an isometry onto its code. It supplies no independently selected record preparation. Combine W with the unchanged endpoint link encoder.

Define nonwrapping shifts \(T_0^+|n\rangle=|n+1\rangle\) for n<N and zero at N, and similarly \(T_0^-\) with zero at −N. For blank-to-content \(R_{v,x}^+=|x\rangle\langle B|\), the exact charge-conserving dressed operator is
\[
 D_{v,x}=R_{v,x}^+T_0^{-\eta_v},\qquad
 [q_RK+Q_0,D_{v,x}]=0,
 \quad D_{v,x}W=WR_{v,x}^+.
 \tag{7}
\]
The shift boundaries never clip an allowed logical move. At an A blank, the A occupancy is at most N−1, so \(n_0\ge-N+1\) before the lowering shift. At a B blank, the B occupancy is at most N−1, so \(n_0\le N-1\) before the raising shift. The occupied inverse moves are safe by the same inequalities. No cyclic wrap is introduced.

The Hermitian copy \(\gamma\sum_x(D_{v,x}+D_{v,x}^\dagger)\), with the actual commuting carrier/content gates retained, intertwines with the old logical copy on this code. Its charge rates satisfy
\[
 \dot q_v=\frac{i\gamma}{\hbar}\sum_x(D_{v,x}^\dagger-D_{v,x}),
 \quad I_{0\to v}=\eta_vq_R\dot q_v,
 \quad \dot Q_0=-\sum_v I_{0\to v}.
 \tag{8}
\]
The existing link exchange leaves all records/K/n0 unchanged, so it needs no return shift. These are exact charge/code statements, not derivations of the physical transfer amplitude, locality or native copying hardware.

## 5. Bare versus joint readout

Let \(\Pi_k\) project original record words onto total staggered occupancy K=k. Tracing out the single return gives
\[
 \operatorname{Tr}_0(W\rho W^\dagger)
       =\sum_{k=-N}^N\Pi_k\rho\Pi_k.
 \tag{9}
\]
It dephases **K sectors**, not every local record occupancy independently. Content coherences and collective record coherences with unchanged K remain. A local blank--occupied matrix element changes K by eta_v, however, and disappears from a bare local readout. Its faithful joint query uses the same \(T_0^{-\eta_v}\) dressing as (7), with the inverse shift on the reverse matrix element.

Thus the return code does not preserve the old bare record clock by assertion. Joint query accessibility, clock/readout calibration, physical retention and the collateral/source ledger must be tested. The logical coherence remains in the whole code; (9) is not irreversible decoherence.

## 6. Exact declared positive-L charging source

One complete **new circuit charging-source class** can be specified for L_v>0 by
\[
 C_{\rm rel}[L]=\bigoplus_v C_{5,v}/L_v,
 \qquad C_{\rm full}[L]=B C_{\rm rel}[L]B^T.
 \tag{10}
\]
Every capacitor weight in a star scales by 1/L_v and stays nonnegative. The same neutral quotient gives
\[
 H_{\rm cap}[L]=\sum_vL_vE_{5,v},
 \qquad \partial_{L_v}H_{\rm cap}=E_{5,v},
 \qquad \partial_{L_v}\partial_{L_w}H_{\rm cap}=0.
 \tag{11}
\]
Here E5v includes its record/self and return-field contribution through the complete kernel. The zero second contacts belong only to this **affine charging source**. State response, connected free-energy curvature, other terms and genuine physical deformation contacts need not vanish. L is not thereby a physical lapse, elastic strain or metric coordinate.

The current native midpoint source has instead the exact record diagonal
\[
 H_{{\rm native},r}[L]
 =\sum_v q_v\left[\epsilon_rL_v-
           \tfrac{\lambda_R}{2}\sum_u n_{vu}(L_v+L_u)\right]
 =\sum_vL_v[(\epsilon_r-2\lambda_R)q_v-\lambda_Rq_vc_v]
   +G_{\rm mid}[L],
\]
\[
 G_{\rm mid}[L]=\tfrac{\lambda_R}{2}
       \sum_{e:u,v} n_e(L_u-L_v)(q_u-q_v).
 \tag{12}
\]
Each edge is counted once. This is the preserved earlier midpoint-versus-node allocation identity, not a changed native source. At the present \(\epsilon_r=1,\lambda_R=1/2\), comparing (11) with the native **degree plus record** diagonal yields
\[
 H_{\rm cap}[L]-H_{{\rm native},d+r}[L]
 =A_R\sum_vL_vq_v+2q_*^2e_d\sum_vL_vI-G_{\rm mid}[L].
 \tag{13}
\]
The gradient term vanishes for uniform L and for fixed all-q1, but is generally a nonzero operator for varying records and nonuniform L. Uniform L does not turn the remaining record cost into an identity when q varies. Consequently the newly complete circuit charging source is not automatically the old all-record midpoint source. Their record-clock/source contacts must be compared explicitly, including state/readout response. Hopping/current/copy and all other complete sources are not inferred from this charging comparison.

## 7. Deformation, dynamics and count boundaries

A conditional common physical Coulomb homothety with all lengths/boundaries scaled by a, fixed charges and dielectric, gives \(C_{\rm full}(a)=aC_{\rm full}(1)\) and neutral charging energy \(H_{\rm cap}(a)=H_{\rm cap}(1)/a\). This is only the stated electrostatic sector. It does not supply the derivatives of h, copying, carrier hopping/rest energy, return-connector transfer, Josephson/chemical terms, source map, physical clock, support or gauge field. No pressure/radiation law or cosmological consequence is introduced here.

A physical remote copy must have its actual record-to-return charge path and Wilson-line/Peierls factor, local gauge transformations/constraints, boundary and field momentum, source work and support recoil. A conserving total-charge operator is not that local gauge/Ward packet. Compact U(1) charge units for qR and the link transfer must be owned independently. The ideal shielded/block circuit must also be realized or replaced by its complete physical capacitance kernel.

A count operation changes island/capacitor/return and support inventories and its charge-number range. A logical inclusion into the larger code does not supply the physical creation operation. The existing inclusion/complement/source and full conserving supply/load/port work remain required. The return field energy already counted in (3) cannot be counted again, but actual additional microscopic terms cannot be discarded as identities. No arbitrary reference, cap value, donor spectrum, volume-energy function, physical cell volume or geometry/metric binding is chosen.

The construction closes one precise charge/field-energy omission in the specified finite circuit class and supplies a prospective exact all-record code. Mandatory record storage, different all-q nonuniform source and the remaining physical transfer/source/deformation obligations prevent declaring it the completed canonical parent or shared galaxy-and-expansion law. Existing RGRL working closure remains at its declared conditional scope.

## Frozen resident inputs

Paths are relative to the sole project root; seven current byte streams were verified before this exclusive new note. Earlier notes and dirty MODEL remain unchanged.

| Input | SHA256 |
|---|---|
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md` | `124f68b600130afcb3935e11c43c1f939a804892b2794c25f89c29a0892f8693` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_DRESSED_RECORD_CHARGE_V001.md` | `e1742a5a3f7f68734f91c563fe04696b8d7664522e830ed8e261c708b7c83cb1` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_SHARED_LINK_DIPOLE_HOLD_V001.md` | `f461558f0ddf330cad6758824e9d1efed45697c4bc8ad46bf540251fcde71e70` |
| `program-worktree/MODEL.md` | `3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607` |
| `program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md` | `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_MIDPOINT_SOURCE_CLOCK_CONSTRAINT_V001.md` | `1c0cf577cbc9124b8c3f28fa6d639c8e06dfea25426bf015c9340215f571723a` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md` | `e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43` |

Exact ancestry is the five-island inversion/passive/storage construction, the unchanged record-countercharge readout and shared-link code notes, midpoint note equations1--5, BS register/copy/feedback/source templates and the current creation-source identities. The quotient, global return code and new positive-L charging source above are analytical extensions inside an explicit circuit class, not observational evidence or a new scheduler/framework.
