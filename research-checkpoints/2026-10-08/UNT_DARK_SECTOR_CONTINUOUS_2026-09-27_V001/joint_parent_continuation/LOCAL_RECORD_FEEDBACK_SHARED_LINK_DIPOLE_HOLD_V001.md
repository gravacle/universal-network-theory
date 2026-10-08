# Conditional shared-link dipole encoding on a grounded q4 closed hold

Date: 2026-10-05. Claim class: exact Hilbert-space/current/capacitance construction under a declared closed hold. Root and observer independently reviewed the prospective algebra before this note was written. This is not a selected physical realization, canonical full-record adoption, visible electromagnetism, ruler/metric law or dynamical expansion model. No job or producer replay was used.

## 1. Hold and recovered ancestry

Take a declared balanced periodic simple bipartite q4 graph with A/B vertices, \(V=2N\) and \(M=4N\) eligible links. Orient every link from A to B. All physical record occupancies are held at \(q_v=1\); record-changing copying, count ports and exterior charge ports are off. The scored parent is the incidence-only Nc0 sector. All incidence words remain present; degree-two projection is not imposed. No carrier hopping/current or formation sector is inferred from this hold.

GA03--13 already proves a minimal fixed-charge encoder and the conditions for preserving source-off and source operators on its complete code. This note gives one explicit endpoint placement of that algebra and a passive grounded-star realization of the offset construction. The physical endpoint placement, shielding and grounded reference are counted new premises.

Use the FU incidence convention \(n_e=(1-Z_e)/2\), \(c_v=d_v-2=-\frac12\sum_{e\ni v}Z_e\). The independently physical parameters obey
\[
 e_d>0,\quad e_m>0,\quad r=e_d+4e_m,
 \quad U=2q_*^2e_m,
 \quad b_0=-\frac{\lambda_R}{2q_*^2r},
 \quad A=\frac{\lambda_R^2}{2q_*^2r}.
 \tag{1}
\]
The positive ratio \(\alpha=e_d/e_m\) remains underdetermined by matching \(U\) and \(\lambda_R\). At the present tuple \(A=\lambda_R^2/[U(\alpha+4)]\) lies strictly between zero and \(1/16\). Neither charge nor length is calibrated here.

## 2. One encoded endpoint pair per original link

For \(e:u\in A\to v\in B\), introduce endpoint two-level charge registers with involutions \(S_{u,e},S_{v,e}\). Define
\[
 V_e|Z_e=+1\rangle=|+,-\rangle_{u,e;v,e},\qquad
 V_e|Z_e=-1\rangle=|-,+\rangle_{u,e;v,e}.
 \tag{2}
\]
The code projector is \(\Pi_e=(1-S_{u,e}S_{v,e})/2\). With endpoint raising/lowering operators define
\[
 F_e=\sigma^+_{u,e}\sigma^-_{v,e},\quad
 T_e=F_e+F_e^\dagger.
\]
Direct multiplication gives
\[
 S_{u,e}V_e=V_eZ_e,\quad S_{v,e}V_e=-V_eZ_e,
 \quad T_eV_e=V_eX_e.
 \tag{3}
\]
Both the charging operators and \(T_e\) preserve the pair code. Thus \(V_E=\bigotimes_eV_e\) is an isometry from the original \(2^M\)-dimensional space onto the \(2^M\)-dimensional simultaneous code. Every original polynomial in incidence \(Z_e,X_e\) has the exact encoded intertwiner on all virtual/off-ice sectors.

For the current declared L3 support, 108 original link factors use 216 endpoint registers, but the scored code still has dimension \(2^{108}\), not \(2^{216}\). The original link is encoded once; its two endpoints are not two independent original bits.

## 3. Passive local capacitance and full shared-link energy

At each vertex freeze a four-terminal grounded star with elastance
\[
 \mathcal E=e_dI+e_m\mathbf1\mathbf1^T,
 \qquad
 C=\mathcal E^{-1}=\frac1{e_d}I-\frac{e_m}{e_dr}\mathbf1\mathbf1^T.
 \tag{4}
\]
This is a passive circuit: a capacitor \(C_g=1/r>0\) from each terminal to the held reference and \(C_m=e_m/(e_dr)>0\) between every pair of its four terminals give diagonal \(C_g+3C_m\) and off-diagonal \(-C_m\), exactly (4). The complete inverse, including its common mode, is essential; a neutral-quotient inverse does not establish the off-ice Hamiltonian.

The declared global capacitance domain is block diagonal in these grounded stars. This requires an ideal shielded/held-reference circuit premise; it is not automatic for terminals interacting through the unrestricted Maxwell field. Each terminal register belongs to one star, while each pair of endpoint registers belongs to the single link code.

Set \(\eta_A=+1,\eta_B=-1\), and assign physical terminal charges
\[
 Q_{v,e}=q_*[S_{v,e}-\eta_vb_0q_v].
 \tag{5}
\]
Their encoded restriction is \(\eta_vq_*[Z_e-b_0q_v]\). Therefore both stars obtain the same feedback sign. Summing the complete star energies gives
\[
 \sum_v\tfrac12Q_{v,\rm ports}^T\mathcal E Q_{v,\rm ports}
 =U\sum_vc_v^2-\lambda_R\sum_vq_vc_v
       +A\sum_vq_v^2+2q_*^2e_dVI.
 \tag{6}
\]
There is one star term per original vertex, exactly as in the original degree Hamiltonian. Shared use of \(Z_e\) at its two endpoints does not double that original Hamiltonian. Self, reference, shield, support and held-source energies must nevertheless be included in the physical whole energy once.

At fixed \(q_v=1\), the last two terms in (6) are one common identity. A single explicitly retained fixed-N reference assignment can match the old q1 incidence Hamiltonian. It does not remove the relative record cost \(Aq_v\) when records change, nor its count/geometry/source derivatives. The original offset note remains unchanged.

## 4. Exact endpoint and node charge continuity

The held offsets are time independent. Each link has \(Q_{u,e}+Q_{v,e}=0\), and balanced A/B sizes give total offset charge \(-4q_*b_0\sum_v\eta_v=0\). The star total is
\[
 Q_v=-2\eta_vq_*c_v-4\eta_vq_*b_0.
 \tag{7}
\]
For \(H_{{\rm flip},e}=-h(F_e+F_e^\dagger)\), define the A-to-B current
\[
 I_e=\frac{2ihq_*}{\hbar}(F_e^\dagger-F_e).
 \tag{8}
\]
Then
\[
 \dot Q_{u,e}=-I_e,\qquad \dot Q_{v,e}=+I_e,
 \qquad \dot Q_v+\sum_{e\ni v}s_{ve}I_e=0,
 \tag{9}
\]
where \(s_{ve}=+1\) at an A endpoint and \(-1\) at a B endpoint. Charging terms commute with all endpoint charges. This is exact spatial node-charge continuity under the declared endpoint/connector placement. It is a stronger placement statement than an unspecified co-located reservoir exchange, but does not by itself supply connector momentum, mechanical recoil or stress continuity.

## 5. Exact fixed-record source hold and its guard

For the operational scalar source \(L\), declare the complete closed-hold prescription
\[
 H_{\rm cap}[L]=\sum_vL_vE_{{\rm cap},v},\qquad
 H_{\rm flip}[L]=-h\sum_e m_e T_e,
 \quad m_e=(L_u+L_v)/2.
 \tag{10}
\]
The encoded compression is
\[
 \sum_vL_v[Uc_v^2-\lambda_Rc_v]
 -h\sum_em_eX_e
 +(A+2q_*^2e_d)\sum_vL_vI+H_{\rm ref}[L].
 \tag{11}
\]
Consequently it matches the current uniform-q1 midpoint family modulo its explicitly owned reference source on all incidence words. Reference cancellation in a matched transition is distinct from discarding that energy in complete work/stress.

Equation (10) is a specified mathematical operational source. It is not a derived physical lapse or elastic strain. Grounding, shield, reservoir and support additions preserve old source inheritance only if their full-code restrictions and derivatives meet GA's common-scalar hold. Real geometry changes capacitances and transfer amplitudes and may change backgrounds or source-dependent encoding. All such direct and mixed contacts must be kept. Neither positive capacitance nor (9) selects this geometry/source prescription in nature.

## 6. Local gauge and full-record boundaries

Global total-charge conservation and the continuity equation do not establish a local gauge completion. Under independent local phases, the charge transfer \(F_e\) carries the phase for moving \(2q_*\) between endpoints. An appropriate Wilson-line/Peierls factor, the dynamical gauge/reference fields, their local constraint/Gauss law, field energy, boundary transformation and source-work terms must be supplied together. No such local gauge packet or visible electromagnetic identification is adopted in this note.

If records change, the two offsets on an edge no longer cancel automatically:
\[
 Q_{u,e}+Q_{v,e}=q_*b_0(q_v-q_u),\qquad
 Q_{\rm offset,total}=-4q_*b_0\sum_v\eta_vq_v.
 \tag{12}
\]
A lone copy can change this charge. Its compensating charge/reservoir transfer remains open; the link-exchange operator (8) cannot cure it. Additional record and reservoir energies need not be common identities. Their spatial placement can change cross-field interactions and clock/query operators. The retained \(Aq_v\) cost is not removed by a charge-conserving algebraic encoder.

Likewise, a count port changes terminal, ground and support inventories. Its absolute reference/supply/load work and source-dependent inclusion and complement must be derived as in the current creation-contact note. No physical cell volume, autonomous census law, ground preparation, continuum propagation or selected 3D phase follows here.

The construction is a concrete conditional spatial charge placement for the fixed-record closed hold. The full canonical record parent, momentum/Ward/source completion and common proper probe/ruler/metric binding remain separate obligations. Existing RGRL working closure and the distinction between active coordination/pairs and qualified retained memory remain intact.

## Frozen resident inputs

Paths are relative to the sole project root; all bytes were rehashed on 2026-10-05. No existing file was edited.

| Input | SHA256 |
|---|---|
| `program-worktree/LANE_GRA_FU_F3_Q4_PAIR_RESOLVED_MAXWELL_DPAR_DERIVATION_V001/THEOREM.md` | `f088346f72861b3b11ae737fe6b882d43da9e747fc1d1d1f6bd446a7fd2b6272` |
| `program-worktree/LANE_GRA_GA_F3_Q4_FU09B_ENCODED_CHARGE_CURRENT_LIFT_V001/THEOREM.md` | `374168c75f928cdbce55ca790157ba00df2d3a7f2045611d805d1b1b3c090336` |
| `program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md` | `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec` |
| `program-worktree/MODEL.md` | `3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607` |
| `program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md` | `cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_COORDINATION_MEDIATOR_CANDIDATE_V001.md` | `d9ead9c618f13d237aabbb6586b371187521febbf97be52e35bacc3dce959876` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md` | `e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md` | `9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_OFFSET_ELASTANCE_COMPLETION_V001.md` | `e8233446d3de84ae2832f4f41f63aba3b09c0d6bd60f48a1c8e9842af0551c7b` |

Precise ancestry: GA03--05 (encoder), GA06--10 (current/placement), GA11--13 (common full-code source hold); FU08--14 (full grounded inverse and physical charge completion); the offset note's exact expansion/contact equations; BS11 and BS20--23; MODEL's conditional grounded source/Ward lineage. The new endpoint placement and passive blocked-star assumptions are explicit prospective premises rather than a derived native physical phase.
