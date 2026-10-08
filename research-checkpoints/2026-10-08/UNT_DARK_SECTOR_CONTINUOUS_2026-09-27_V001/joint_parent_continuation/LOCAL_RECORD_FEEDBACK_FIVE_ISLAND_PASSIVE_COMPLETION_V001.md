# Conditional five-island passive record completion

Date: 2026-10-05. Claim class: exact finite-dimensional charging/circuit construction with explicit physical charges and retained record cost. Root, observer, native and readonly independently checked the prospective inversion and bounds. This is a NEW alternative completion, not an adoption or amendment of the frozen offset construction, shared-link hold or completed Coulomb pullback. No numerical worker, Hamiltonian reconstruction, producer import or replay was used.

## 1. Hold, charges and distinct physical premise

Use a simple balanced bipartite q4 support, with incidence convention
\[
 n_e=(1-Z_e)/2,\qquad c_v=d_v-2=-\tfrac12\sum_{e\ni v}Z_e.
 \tag{1}
\]
The shared-link note encodes each original link once into two endpoint registers: \(S_{A,e}=Z_e\), \(S_{B,e}=-Z_e\) on its pair code. Its transfer \(\sigma_A^+\sigma_B^-+\mathrm{h.c.}\) restricts to the original \(X_e\). That exact algebra is retained here; no second independent original bit is introduced.

Let \(\eta_A=+1\), \(\eta_B=-1\). At vertex \(v\), assign four actual port charges and one actual record-island charge
\[
 Q_{v,a}=q_*S_{v,a}=\eta_vq_*Z_{e_a},\qquad
 Q_{R,v}=\eta_vq_R q_v,
 \qquad q_*>0,\ q_R>0,\ q_v^2=q_v.
 \tag{2}
\]
The record occupancy projector is the original blank/occupied record variable. The relative physical charge \(q_R/q_*\) is not established by its logical alphabet and is not chosen in this note. Both charge types have the same node sign \(\eta_v\); omitting that sign on the B record would reverse the feedback there. There is no record-dependent displacement of the port charge in (2). Replacing such an offset by an actual charged record island is a new physical premise.

The reference is a held grounded capacitance domain, with shielding/block separation as in the prior conditional hold. This is a local passive-circuit realization, not a derivation from an unrestricted global Maxwell kernel, a visible electric-charge identification or a selected network phase.

## 2. Exact elastance, inverse and capacitor weights

Declare the symmetric five-terminal elastance
\[
 \mathcal E_5=
 \begin{pmatrix}
 e_d I_4+e_m\mathbf1\mathbf1^T & g\mathbf1\\
 g\mathbf1^T & e_R
 \end{pmatrix},
 \quad e_d>0,\quad e_m>0,\quad g>0,
 \quad r=e_d+4e_m,
 \quad S_R=e_R-\frac{4g^2}{r}.
 \tag{3}
\]
All elastances have the same physical units. Positive definiteness is equivalent to \(S_R>0\), since the port block has eigenvalues \(e_d\) and \(r\). Its complete inverse, including the common charge mode, is
\[
 C_5=\mathcal E_5^{-1}=
 \begin{pmatrix}
 \dfrac1{e_d}I_4+
 \left[\dfrac{g^2}{r^2S_R}-\dfrac{e_m}{e_dr}\right]\mathbf1\mathbf1^T
 &-\dfrac g{rS_R}\mathbf1\\
 -\dfrac g{rS_R}\mathbf1^T&\dfrac1{S_R}
 \end{pmatrix}.
 \tag{4}
\]
For an ordinary lumped circuit with nonnegative capacitors between islands and from islands to the held ground, its Maxwell capacitance matrix must have nonpositive off-diagonal entries and nonnegative row sums. Equation (4) is exactly realized by the following weights:
\[
 \begin{aligned}
 C_m&=\frac{e_m e_R-g^2}{e_d r S_R}
       &&\text{between each pair of distinct ports},\\
 C_{pR}&=\frac g{rS_R}
       &&\text{between each port and the record island},\\
 C_{gp}&=\frac{e_R-g}{rS_R}
       &&\text{from each port to ground},\\
 C_{gR}&=\frac{r-4g}{rS_R}
       &&\text{from the record island to ground}.
 \end{aligned}
 \tag{5}
\]
Thus a port diagonal is \(C_{gp}+3C_m+C_{pR}\); its off-diagonals are \(-C_m\) and \(-C_{pR}\). The record diagonal is \(C_{gR}+4C_{pR}=1/S_R\). In particular the port grounding row sum simplifies exactly:
\[
 \frac1r+\frac{g(4g/r-1)}{rS_R}
       =\frac{e_R-g}{rS_R}.
 \tag{6}
\]
Consequently, within this declared five-island circuit class, the necessary and sufficient passive conditions are
\[
 \boxed{\quad e_R\ge\max(g^2/e_m,g),\qquad 4g\le r,\qquad e_d,e_m,g>0.\quad}
 \tag{7}
\]
Necessity follows from the signs of the port-port, port-ground and record-ground weights. Sufficiency follows by constructing the circuit with (5). The first inequality already guarantees strictly positive Schur complement:
\[
 S_R\ge\frac{g^2}{e_m}-\frac{4g^2}{r}
       =\frac{g^2e_d}{e_m r}>0.
 \tag{8}
\]
Zero values of individual capacitors at the allowed boundaries do not make \(C_5\) singular. Equation (8) retains its complete positive inverse. The uncoupled \(g=0\) limit separately requires \(e_R>0\), but it cannot match the positive feedback tuple and is not the scored branch.

One transparent description of the full admissible family, without selecting any physical values, is
\[
 \alpha=e_d/e_m>0,\quad \kappa=g/e_m>0,\quad
 \kappa\le(\alpha+4)/4,\quad
 \zeta=e_R/e_m\ge\max(\kappa^2,\kappa).
 \tag{9}
\]
These inequalities supply explicit positive or zero capacitor weights and a strictly positive complete elastance. They are an algebraic parameter domain, not a calibration, occupation choice or favorable energy function.

## 3. Exact native charging polynomial and storage bounds

On the complete link code, for every incidence word including off-ice states and both record occupancies,
\[
 \begin{aligned}
 \tfrac12 Q_v^T\mathcal E_5Q_v
 &=\tfrac12q_*^2\left[4e_d+e_m\Big(\sum_aZ_{e_a}\Big)^2\right]
   +gq_*q_R q_v\sum_aZ_{e_a}+\tfrac12q_R^2e_Rq_v^2\\
 &=U c_v^2-\lambda_R q_vc_v+A_Rq_v^2+2q_*^2e_d I,\\
 U&=2q_*^2e_m,\qquad
 \lambda_R=2q_*q_Rg,\qquad
 A_R=\tfrac12q_R^2e_R.
 \end{aligned}
 \tag{10}
\]
The two factors of \(\eta_v\) cancel in the cross term, giving the same \(-\lambda_R q_vc_v\) at A and B. The self term is one term per original node, not a duplicate link Hamiltonian. Absolute ground, shield, support and reference energies remain owned once.

The passive inequalities in (7) imply the two independent lower bounds
\[
 \boxed{\quad A_R\ge\frac{\lambda_R^2}{4U},\qquad
 A_R\ge\frac{\lambda_R q_R}{4q_*}.\quad}
 \tag{11}
\]
The first follows from \(e_R\ge g^2/e_m\); the second follows from \(e_R\ge g\). For specified \(U,\lambda_R,q_*,q_R\), choose no charge units: instead matching imposes
\[
 e_m=\frac{U}{2q_*^2},\qquad
 g=\frac{\lambda_R}{2q_*q_R},\qquad
 \frac{q_R}{q_*}\ge\frac{4\lambda_R}{U(\alpha+4)}
 \tag{12}
\]
as the remaining record-ground admissibility condition. With that condition and \(e_R\ge\max(g^2/e_m,g)\), the construction is exact. Neither matching \(U,\lambda_R\) nor the old logical record convention determines \(\alpha\), \(q_R/q_*\) or \(e_R\).

At the unchanged current tuple \(U=1,\lambda_R=1/2\), every member of this passive five-island class has
\[
 A_R\ge\frac1{16}.
 \tag{13}
\]
Only if an independent physical dictionary establishes \(q_R=q_*\), the second bound strengthens this to \(A_R\ge1/8\). Equal charges are not inferred, chosen or used as an input here.

The frozen four-port offset family instead has \(A=\lambda_R^2/[U(\alpha+4)]\), strictly between zero and \(1/16\) at the present tuple. It therefore cannot be silently relabeled as this passive actual-record-charge completion. The new bound excludes that relabeling within this specific circuit class; it is not a no-go for other circuit, gauge, screened or native physical completions.

## 4. Fixed record hold versus copy, charge and count work

At \(q_v=1\) on a fixed node census, \((A_R+2q_*^2e_d)V I\) is a common energy in that held block, where \(V\) denotes native node count. A separately owned reference may permit comparison to the old q1 incidence Hamiltonian. Fixed-state ray dynamics or gaps do not determine this absolute assignment. It must still be included in source, geometry, controller-path and creation work.

On the full record Hilbert space \(q_v^2=q_v\), so \(A_Rq_v\) is an actual positive record-storage operator, not a removable scalar. At fixed \(c_v\), the charging cost of a blank-to-occupied record is \(A_R-\lambda_R c_v\). At degree two \(c_v=0\), its extra cost is \(A_R>0\). Subtracting it to restore the old copying resonance would change the physical completion and its source/work; no such subtraction or retuning is made.

The original endpoint exchange conserves the two port charges on each edge. The added record islands have total charge \(q_R\sum_v\eta_vq_v\). At the balanced fixed-q1 hold this total is zero. A record flip, however, changes an island charge by \(\eta_vq_R\). A closed implementation of the old logical record-copy operator must now include an opposite donor/counterelectrode charge transfer, its state space, energy and source. A grounded static capacitance supplies no such dynamical operator automatically. Ground charges and compensating fields must not be removed from the complete conservation/work accounting.

Likewise a count-changing port changes the inventory of ports, record islands, ground and shields. The existing creation-source contact conditions on the inclusion, its complement, supplies and controller still apply. This packet owns no autonomous count law, phase preparation or physical cell-volume calibration.

## 5. Conditional dilation and response boundary

If the complete fixed-dielectric, grounded five-island geometry undergoes a common length dilation \(a\), with all actual charges and charge encoding held fixed, the Coulomb homogeneity postulate is
\[
 C_5(a)=aC_5(1),\qquad
 \mathcal E_5(a)=a^{-1}\mathcal E_5(1).
 \tag{14}
\]
It implies common \(1/a\) scaling of \(e_d,e_m,g,e_R\) and thus of \(U,\lambda_R,A_R\) and the self term. This is conditional on the complete reference, shielding, dielectric and charge prescription. It does not fix the strain dependence of native \(h\), carrier hopping, copying, rest energy, donor operators, source encoding or clocks.

The charging numerator is
\[
 J_{0}=U\sum_vc_v^2-\lambda_R\sum_vq_vc_v
        +A_R\sum_vq_v^2+2q_*^2e_d V I,
 \qquad H_C(a)=J_0/a+R_{\rm raw}(a)I.
 \tag{15}
\]
The separate absolute reference \(R_{\rm raw}(a)\) is not assigned \(1/a\) scaling without its own physical premise. For a fixed-beta canonical clamped sector, the exact curvature uses the direct contact and the Kubo response of \(H_{C,a}\), not merely the second derivative of an arbitrary mean energy.

At the present fixed-q1 tuple, the nonidentity numerator is the old \(D_{\rm total}\). If only this block deforms and the same held ensemble is actually owned, its symbolic canonical contribution is
\[
 K_D+2(A_R+\alpha)+R_{\rm raw}''/V,
 \qquad K_D=2\langle D_{\rm total}\rangle/V-\chi_{DD,\rm density},
 \quad \alpha=e_d/e_m.
 \tag{16}
\]
Equation (16) is an analytical identity, not a newly evaluated five-island model. The completed 200/200-control Coulomb pullback remains the distinct offset-family saved-data diagnostic, with its original \(A=1/[4(\alpha+4)]\), signed matrices and inherited mixing qualifications unchanged. Neither its measured nonidentity response nor a positive circuit proves full mechanical stiffness, stability, pressure or accelerated expansion. Other operator strain contacts and their mixed responses, the record donor, absolute reference and operational clock/ruler binding remain missing.

## Frozen resident evidence

Paths are relative to the sole project root. These seven existing byte streams were rehashed directly on 2026-10-05 before saving this new note; none was modified.

| Input | SHA256 |
|---|---|
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_SHARED_LINK_DIPOLE_HOLD_V001.md` | `f461558f0ddf330cad6758824e9d1efed45697c4bc8ad46bf540251fcde71e70` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_OFFSET_ELASTANCE_COMPLETION_V001.md` | `e8233446d3de84ae2832f4f41f63aba3b09c0d6bd60f48a1c8e9842af0551c7b` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md` | `9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md` | `e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43` |
| `program-worktree/MODEL.md` | `3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001_RESULT.json` | `679c40e69cca152498af8af9763467467ad48315286bf150a45f813dce614b0a` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001_RESULT.json` | `a0ed403a7bbd41ed460605c568a8b57260897d31e0e2218286b649c83c1871d5` |

The new constructive result is the exact five-island admissibility domain and unavoidable storage floors. No physical charge equality, reference energy, compensating copy term, favorable volume function, observation map, gravity law or completed shared galaxy-and-expansion model is selected by it.
