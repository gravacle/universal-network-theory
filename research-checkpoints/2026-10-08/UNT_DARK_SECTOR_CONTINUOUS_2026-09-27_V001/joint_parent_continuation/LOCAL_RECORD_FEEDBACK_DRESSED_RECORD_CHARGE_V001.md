# Exact abstract record-countercharge lift and its physical boundaries

Date: 2026-10-05. Status: independently reviewed analytical charge/code result, preserved as a new bounded candidate note. No candidate adoption, numerical job, producer replay, old-note change or physical calibration. The charge lift does not remove the positive record energy of the offset/elastance constructions.

## 1. Native record and proposed charge

Use the complete native local record alphabet \(\{|B\rangle,|x\rangle:x\in\mathcal A\}\), where B is blank and the distinct occupied content labels span the occupancy projector
\[
 q=\sum_{x\in\mathcal A}|x\rangle\langle x|,\qquad q^2=q.
\]
This includes all content labels; it is not a single selected label or a classical record probability. The BS copy is a blank-target, content-controlled Hermitian transfer, not a universal cloning operation.

For a specified proposed record-associated charge \(\kappa_v q_v\), introduce one two-level countercharge register at v:
\[
 N_{R,v}=|1\rangle\langle1|,\quad Q_{R,v}=-\kappa_vN_{R,v},
 \quad T_{R,v}^+=|1\rangle\langle0|,\quad T_{R,v}^-=(T_{R,v}^+)^\dagger.
 \tag{1}
\]
The charge \(\kappa_v\) is an input to this abstract construction, not a calibration derived from native occupancy.

## 2. Exact code and dressed copying

Define the isometry
\[
 W_v|B\rangle=|B\rangle|0\rangle_R,\qquad
 W_v|x\rangle=|x\rangle|1\rangle_R\quad(x\in\mathcal A).
 \tag{2}
\]
Its image is the complete code \(N_R=q\). There is one encoded state per original record state; occupied labels use the same countercharge value without being identified with each other. Direct multiplication gives
\[
 qW=Wq,\quad N_RW=Wq,\quad(\kappa q+Q_R)W=0.
 \tag{3}
\]
Let \(R_x^+=|x\rangle\langle B|\), \(R_x^-=(R_x^+)^\dagger\). The dressed operator
\[
 D_x=R_x^+T_R^+,\qquad \widetilde K_x=D_x+D_x^\dagger
 \tag{4}
\]
preserves the code and obeys \(\widetilde K_xW=W(R_x^++R_x^-)\). Native carrier/writer content projectors commute with q and the counter register, so the same relation holds for the actual content-controlled copy sum. Operations within the occupied content subspace preserve q and inherit without a countercharge shift.

The charge commutator is exact:
\[
 [q,R_x^+]=R_x^+,\quad [Q_R,T_R^+]=-\kappa T_R^+,
 \qquad [\kappa q+Q_R,D_x]=0.
 \tag{5}
\]
Tensoring (2) over records and combining it with the previously saved single-link endpoint encoder provides an isometry of the whole original record/incidence space. The score is on that code, not on independent new record states. Pure operator equivalence is exact for a Hamiltonian constructed by these substitutions; it is not proof that a physical countercharge sector has the required energy or source.

For the actual positive-sign native copy convention \(H_{\rm copy}=\gamma\sum_x(D_x+D_x^\dagger)\), with its content gates retained inside \(D_x\),
\[
 \dot q=\dot N_R=\frac{i\gamma}{\hbar}\sum_x(D_x^\dagger-D_x),
 \quad I_{R\to r}:=\dot Q_r=\frac{i\gamma\kappa}{\hbar}
                     \sum_x(D_x^\dagger-D_x),
 \quad \dot Q_R=-I_{R\to r}.
 \tag{6}
\]
A different sign convention is included by the actual signed \(\gamma\); no extra Pauli normalization is used. Diagonal charging/storage terms commute with q and do not change this transfer identity. This is the copy contribution; other charge-changing ports require their own terms.

## 3. Bare record readout is different from encoded readout

For any original density operator \(\rho\), tracing out the countercharge gives exactly
\[
 \operatorname{Tr}_R(W\rho W^\dagger)
 =\Pi_0\rho\Pi_0+\Pi_1\rho\Pi_1,
 \quad \Pi_0=|B\rangle\langle B|,\quad\Pi_1=q.
 \tag{7}
\]
Thus blank--occupied coherences disappear from the **bare reduced record**; coherences between occupied content labels remain. Equivalently,
\[
 W^\dagger(B\otimes I_R)W=\Pi_0B\Pi_0+\Pi_1B\Pi_1.
 \tag{8}
\]
The faithful joint readout instead dresses those matrix elements:
\[
 \widetilde B=\Pi_0B\Pi_0+\Pi_1B\Pi_1
   +\sum_x\left(B_{xB}R_x^+T_R^+
                     +B_{Bx}R_x^-T_R^-\right),
 \quad W^\dagger\widetilde BW=B.
 \tag{9}
\]
Identity action on the countercharge in the first two terms is understood. Equation (9) applies to general complex B and does not assume it is Hermitian. A record phase/clock query with blank--occupied components therefore requires a joint countercharge-dressed readout. No claim that the old bare record clock is preserved follows from (4).

This partial-trace distinction is not an irreversible decoherence theorem: the logical coherences remain in the joint code and can be recovered by its specified joint readout. Their physical accessibility, retained-record qualification and complete collateral ledger are further obligations. No atomic clock, proper time, Fisher/SLD metric or RGRL memory realization is selected by the encoding.

## 4. Energy and field costs survive

The offset construction's compulsory record term is unchanged:
\[
 W^\dagger(Aq)W=Aq.
 \tag{10}
\]
A generic counter Hamiltonian \(E_R(N_R)\) pulls back to \(E_R(q)\), not a common identity. For example, a positive local charge-storage term \(Q_R^2/(2C_R)\) yields \(\kappa^2q/(2C_R)\). More generally, two counter levels with actual energies E0/E1 add \(E_0I+(E_1-E_0)q\). Physical cross-field interactions can modify record storage, record/degree feedback and cross-node terms.

Full-code scalar energy/source inheritance is a separate premise of the same kind as GA's closed-full-code-scalar hold. A conserved-charge encoder alone does not establish it. Countercharge neutrality or co-location does not license omission of the counter/reference/self/cross-field energy, nor the subtraction of an arbitrary \(-Aq\) binding term to restore the old zero degree-two record detuning. A genuine compensating interaction would have to be derived and sourced as part of the complete parent.

## 5. Two physical charge interpretations remain distinct

**Four-terminal offset candidate.** The saved offset/shared-link construction has physical terminal charges \(\eta_vq_*[Z_e-b_0q_v]\), so the record-associated star charge is
\[
 \kappa_vq_v=-4\eta_vq_*b_0q_v.
 \tag{11}
\]
Here the copy changes the offset charge at four separated terminals, each by \(\kappa_v/4\). A countercharge of \(-\kappa_vN_R\) can balance the total abstract charge. It does not by itself supply the four physical transfer paths, currents, field energy or source contacts. If the counter is remote, a connector/boundary current is needed; if it is within the star, the resolved terminal-field geometry still matters. Under the conditional whole-geometry fixed-charge Coulomb dilation, b0 and these charge increments stay fixed while their electrostatic energies scale; no unowned charge rescaling is inserted.

**Actual fifth record island.** A separate passive five-terminal candidate assigns \(\eta_vq_Rq_v\) to a distinct record island. The same algebra works with \(\kappa_v=\eta_vq_R\); it is not the distributed four-terminal offset. That candidate has its own complete capacitance and mandatory record self-energy, whose value and cross-field/source terms must remain. Neither construction selects qR, alpha, a ground/reference energy or a donor. The countercharge construction is compatible with either specified algebra but does not prove their physical equivalence.

In particular, changing record content/occupancy in either candidate is a charged physical process only after its charge assignment is justified. Native recordhood is not by itself that charge assignment.

## 6. Compact charge and local gauge conditions

If the proposed physical interpretation uses a locally resolved compact U(1) with one charge unit q0, all admitted dynamical charge differences must have the corresponding integer charge-lattice representation. This includes the link transfer \(2q_*\), the counter transfer \(\kappa_v\), and, if interpreted as separate actual terminal-charge transfers, \(\kappa_v/4\). Absolute background/ground sectors must also be physically owned.

For the present four-terminal tuple,
\[
 |\kappa_v|/q_*=2/(\alpha+4),\qquad\alpha>0.
 \tag{12}
\]
An unselected continuous alpha does not guarantee commensurability. If q* were itself the elementary charge unit, the nonzero fractional offset transfer could not simply be renamed an elementary integer transfer. Continuous induced gate/polarization charge is a different possible interpretation, requiring its full physical fields and reservoirs. This is a qualification of that literal charge assignment, not a no-go for every compact gauge or effective charge completion.

A total-charge commutator and (6) are not a local gauge completion. Spatially separated record and countercharge operations require the appropriate Wilson-line/Peierls factors, gauge/reference fields, local constraints and boundary transformations. In the distributed-offset case the terminal-resolved paths are also required. Global charge conservation does not provide field momentum, support recoil, a metric Ward identity or universal gravitational coupling.

## 7. Complete source, pulse and count obligations

Let a physical source/strain parameter be \(\xi\). An exact encoded source hold would require
\[
 \widetilde H[\xi]W[\xi]
  =W[\xi](H[\xi]+c[\xi]I)
 \tag{13}
\]
on the **whole** code, including all virtual incidence/record sectors. Then differentiating retains
\[
 \widetilde H_\xi W+\widetilde H W_\xi
 =W_\xi(H+cI)+W(H_\xi+c_\xi I),
 \tag{14}
\]
and its second derivative contains both first-derivative products and \(W_{\xi\xi}\). Source independence alone is not the scalar condition: a constant counter chemical energy can already pull back to a nonidentity record term. Equations (13)--(14) are conditional tests, not established source inheritance for either physical charge interpretation.

A physical local pulse must include the complete counter, record, connector, gauge/reference, support and controller source, with its actual direct contacts and state response. Old saved clock/source responses cannot be transferred merely by asserting charge conservation. The prescribed scalar L is not thereby an elastic strain or physical lapse.

Similarly, the logical inclusion \(F\) has a code-level extension \(W_{N+1}FW_N^\dagger\) between encoded count sectors, but that identity does not construct the physical creation operation. Actual new terminals, countercharges, fields, grounds and references have inventory and work. The full conserving count controller must retain supply/load/port/source terms and the complementary inclusion force; the count resource \(\widehat N+\widehat M\) is distinct from electric charge. Inclusive energy is conserved for an autonomous complete Hamiltonian; a prescribed time-dependent source contributes its actual \(\langle\partial_tH\rangle\) work.

No physical cell volume, donor spectrum, census dynamics, energy-reference function, ruler calibration, selected 3D phase or expansion law is specified here. Existing conditional RGRL working closure is preserved at its declared scope.

## Frozen resident inputs

All paths are relative to the sole project root. Existing dirty MODEL is read only. These input bytes were verified on 2026-10-05; the preceding notes remain unchanged.

| Input | SHA256 |
|---|---|
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_SHARED_LINK_DIPOLE_HOLD_V001.md` | `f461558f0ddf330cad6758824e9d1efed45697c4bc8ad46bf540251fcde71e70` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_OFFSET_ELASTANCE_COMPLETION_V001.md` | `e8233446d3de84ae2832f4f41f63aba3b09c0d6bd60f48a1c8e9842af0551c7b` |
| `program-worktree/MODEL.md` | `3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607` |
| `program-worktree/LANE_GRA_GA_F3_Q4_FU09B_ENCODED_CHARGE_CURRENT_LIFT_V001/THEOREM.md` | `374168c75f928cdbce55ca790157ba00df2d3a7f2045611d805d1b1b3c090336` |
| `program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md` | `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md` | `e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md` | `9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b` |
| `program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md` | `cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2` |

Ancestry: GA's encoder/current and full-code source hold; BS physical register/copy algebra and feedback; the unchanged offset/shared-link notes; the current creation-source identities; MODEL's conditional source/metric/grounded-field lineage and the explicit RGRL working-theory hypotheses. This note extends the abstract conserving algebra without claiming a completed physical reservoir or unchanged bare clock.
