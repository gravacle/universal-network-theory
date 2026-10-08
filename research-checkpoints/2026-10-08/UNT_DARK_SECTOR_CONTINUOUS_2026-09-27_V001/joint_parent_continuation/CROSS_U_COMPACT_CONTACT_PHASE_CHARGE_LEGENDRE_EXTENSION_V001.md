# Compact contact: phase charge Legendre correction

AUTHOR_DRAFT=True. Analytical extension only; no phase profile, correction or physical preparation is selected.

1. Keep the same configuration, EOS, literal action and current phase covector `phi_a`. Let `v^a=hi^{ab}phi_b`, `X=sqrt(-phi_a hi^{ab}phi_b)`, and `P_a{}^b=delta_a{}^b+u_a U^b`. The action current is `J_act^a=-(P_X/X)v^a-(P^T hi P phi)^a`; the saved registered current is `J_reg^a=-(P_X/X)v^a-(hi P phi)^a`. Their finite base/contact/density bridge is already saved by compact54248. Do not combine a derivative from one current with the other's density measure.

2. At fixed configuration the exact local temporal Hessians are
`H_act=dens[(P_XX/X^2-P_X/X^3)(v^0)^2-(P_X/X)hi^{00}-(P^T hi P)^{00}]`,
`H_reg=dens[(P_XX/X^2-P_X/X^3)(v^0)^2-(P_X/X)hi^{00}-(hi P)^{00}]`.
They follow from `delta X=-(v^0/X)delta phi_t`; no mixed native/metric velocity Hessian is introduced. The fixed-rate native/metric response cannot change phase canonical density.

3. With the exact ADM/chart identities and the present `phi_i=0`, `X=phi_t/N` and `norm_b=u_i ih^{ij}u_j`, these reduce to `H_phi=sqrt_h(P_XX-norm_b)/N`. The fixed-phi metric contact is `Q_phi=sqrt_h[(ih:Q)(P_X-X norm_b)/2-X delta norm_b]`, with `delta norm_b=-up^i Q_ij up^j`. The literal readout must retain the inverse/projector/clock gaps instead of replacing its full Hessian/contact by this simplified formula.

4. If `H_act>0` is actually admitted and each current local action canonical density is fixed, the unique infinitesimal correction is `delta phi_t=-Q_phi_act/H_act`. Using the registered target instead requires its own consistent `H_reg` and contact, or explicitly retaining the action-to-registered bridge. For an existing finite stationarity defect `epsilon_phi=P_target-p_act`, the combined linearized equation is `H_act delta phi_t=epsilon_phi-Q_phi_act`; keeping only the homogeneous first variation preserves rather than removes that finite defect. Neither operation is executed here.

5. A global scalar charge `I0` alone supplies only one integral condition and does not determine a spatial `delta phi_t` profile. If a phase nodal test/velocity space `S` and boundary class are registered, the fixed-local-weak-target correction is the positive global mass equation `<S^T H_act S> delta dotphi=-<S^T Q_phi_act>` (plus any retained weak `epsilon_phi`). Pointwise division is not automatically that finite element solve; its projection remainder must remain. No new phase basis or local charge-target profile is selected by this note.

6. A charge-preserving phase-rate contact reacts back on phase normal/force rows. It is an instantaneous partial, with no phase history, spatial mixed continuation, global I0 recalibration or change of the owned physical phase budget. The single frozen native/metric response remains a separate diagnostic, and does not claim phase charge preservation.
