# Same-action weak momentum derivative without acceleration V001

AUTHOR_DRAFT=True. Held analytical implementation plan, root/distinct full review pending. Static derivation only; no numerical source, helper, operator, field, inverse, solve or evolution is evaluated. Keep EPS1e-5, sigma1, all32 registered modes, the original action and fixed coordinates/units. No physical gauge, formation history, metric rate solution, exterior or source is selected.

## 1. Exact function and the conditional seed

Let q=(u_i,z_ji,h_ij) be the constrained covector/metric configuration, v=(u_dot_i,z_dot_ji) and k=h_dot_ij. Use the complete reduced ADM/GHY action, including native connection/chart reactions. Its mechanical momenta at a point are p=(p_native,Pi_metric)=c(q,partial_i q;N,beta,partial_i N,partial_i beta)+H(q,partial_i q;N,beta,partial_i N,partial_i beta)(v,k). Absolute P and ordinary canonical first-order actions have no mechanical native/metric velocity Hessian; their forces and current evolution remain separate. The relative-phase term stays in the action once.

Weak p_h pairs these coordinate densities against the fixed native E and regular metric F bases with weight reference_volume/R. The densities already contain N sqrt(h) and cylindrical R. E,F and the reference quadrature are time independent; do not vary a second volume measure or insert an extra R, mirror2 or2pi. Neither old copied target p nor old WHOLE metric momentum is identified with actual current p_star or a solved metric target.

The weak99 solution owns native v and v_R,v_Z. The authentic point metric rate is kstar=2N Hbar h, so its exact instantaneous spatial jets are

    partial_i kstar=2Hbar[(partial_i N)h+N partial_i h].       (1)

Hbar is spatially constant at this registration. These jets use saved metric compatibility and the actual lapse; they are not derivatives of a fitted field. kstar remains an L2 point seed, not a rate in F's genuine Q1 coefficient space. The derivative below is therefore initially a conditional seed test. It becomes the true discrete time derivative only when a compatible metric rate representation and its spatial jets are supplied. Do not differentiate kstar=2NHbar h in time as an imposed continuing isotropic law; k_dot is the independent unknown acceleration.

## 2. No-acceleration directional derivative and gauge coefficients

Define n=N_dot and b=beta_dot, retaining their spatial derivatives n_i,b_i. For any complete reduced momentum function p, define

    D0 p=p_,q (v,k)+p_,q_i partial_i(v,k)
          +p_,N n+p_,N_i partial_i n
          +p_,beta b+p_,beta_i partial_i b+p_,t|explicit.  (2)

All indices and densities are evaluated in the same constrained chart. Only v_dot=k_dot=0 is used in this algebraic partial derivative; it is not an equation or physical acceleration choice. Thus

    p_dot_h=H_h(v_dot,k_dot)+D0 p_h,
    D0 p_h=dot c_h+dot H_h(v,k),
    F_h=E_spatial,h-D0 p_h.                              (3)

Native dot and metric dot blocks are differentiated together; bare EH momentum cannot replace Pi_total. Every JU,JzU,Jzz,Uh,zh,embedding/projector, inverse metric, connection, N sqrt(h), quartic and affine acceleration.Z contact is included. Holding these Jacobians fixed would omit their Hessian contractions with the seed rates. Fixed mode xi,w,omega and calibration units are not varied with the local expanding H; omega uses the owned Hstar normalization, not H(t).

First show whether the fully reduced action is independent of N_dot,beta_dot after all chart/connection cancellations. The proposed output must retain the explicit coefficients of n,b,n_i,b_i instead of assigning them values. Any surviving dependence of p itself on gauge velocities requires the corresponding higher gauge derivative terms; it cannot be discarded or setzero by the stationary ancestor. Spatial derivatives of the native rates are saved; (1) earns only kstar spatial jets. No unowned physical second jet or time history is needed for this conditional algebraic decomposition, and none is silently supplied.

## 3. Bounded actual successor and temporal representative

Stream the four genuine quadrature columns. Build the current native time jet by replacing Q1 owned_chart_old_velocity with the recovered weak99 rate while keeping the authentic kstar and primitive configuration/spatial jets. Q1 owned_du_increment,owned_dz_increment,owned_connection_increment are increments, not full first jets; add them once to WHOLE, then apply the recovered-minus-owned native rate correction. Preserve the actual current momentum, old target and finite gap separately.

An exact directional jet implementation of (2) differentiates the reduced momentum pullback, not105 new kinetic columns. Its mixed first jets obey partial_t(partial_i q)=partial_i(v,k); differentiate every chart and metric embedding accordingly. Keep lapse/shift gauge coefficients and their gradients symbolic. First output D0 p_native,h,D0 Pi_metric,h and each signed contribution with positive operation bounds; combine with the forthcoming spatial Euler loads only after their own admission. The actual mechanical acceleration equations then use the full weak block, not a pointwise Schur substitution.

Use the same ADM/GHY representative as the kinetic map and spatial Euler loads. A raw4D Hilbert/connection source cannot replace this derivative without its paired temporal/spatial improvement. The fixed reference volume and regular basis remove basis-motion terms, not the native metric momentum or boundary terms. Unknown time/GHY, sheet, outer and moving-worldtube ports remain named. The instantaneous first output need not solve those ports, but cannot qualify global canonical evolution while they are unknown.

## 4. Phase and independent ordinary evolution beside the mechanical row

The exact phase current is J^alpha=P_X v_phi^alpha-r^alpha, v_phi^alpha=-g^{alpha beta}phi_beta/X, and p_phi=dens J^0. On fixed coordinate scalar tests S, the charge equation is

    partial_t p_phi+partial_i(dens J^i)=0,
    <S p_dot_phi>=<partial_i S dens J^i>-boundary(S dens J^i). (4)

Keep the full relative-current term, signed spatial flux and boundary term. Strict X/phase-band and positive clock slope admission must precede inversion of the current to phi_dot. The saved stationary scalar current is an operand, not ownership of its future history. Its nonlinear clock row is not inserted into the105 affine mechanical Hessian. The ordinary variables are independently rotating material positions and covariant momenta: x_dot=N ih p/Gamma-beta and p_dot_i=-Gamma N_i-N(partial_i ih)pp/(2Gamma)+p_j partial_i beta^j. No physical U=u_M identification, new cosmic ordinary volume density, photon state or active writer gain is chosen.

This enables actual F and the complete weak CMC derivative once compatible rates and gauge/current/port data are earned. Retain <sqrt(h)S[K_dot-3Hbar_dot+theta(K-3Hbar)]>, theta=Tr(ih k)/2; a vanishing weak trace gap does not remove its theta term or beta.gradK. The sampled signed6 Schur and49 arithmetic gates do not certify the full metric inverse, free shear, physical Cauchy history or exact metric geodesic prediction. Activity outside0.3--15.1kpc remains undefined and supplies no artificial edge or zero-source junction.

## Actual input byte bindings

All ten files were hashed with stdlib only before this exclusive write. The metric extension below is currently0644; the other nine are0444. These are byte bindings, not new state qualification.
- CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_ASSEMBLY_V001.md — 5e025effae0a5029df1cbe1935137263e5b27c442cca4fe3ced46a992566b84d
- CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_AND_CMC_EXTENSION_V001.md — 78491aa4158dec6152a19136d5b3265cc63cdc965ebf4002d8df371074b46806
- CROSS_U_FULL_CANONICAL_CMC_PRESERVATION_EXTENSION_V001.md — 60a222d80500b01771092919ede0d1374969ee769471964aec911929aad9e424
- cross_u_whole_slice_q1_adm_residual_v001.py — c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a
- cross_u_whole_slice_cauchy_data_v002.py — 6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7
- cross_u_weak_nodal_native_legendre_v001.py — e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json — e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5
- cross_u_weak_nodal_metric_temporal_cmc_v001.py — e11bb7ec123971998fbdd64d1e2171627aae9202804d1c625202f412b5f85b6c
- CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RESULT.json — 2210b4993989d6cb432d9981cc8819f1c21c394ded9d349f6d34b009adb92528
- CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RECEIPT.json — f74d4d67ba87838b4902dc53eebd38812c9b723870ef57528144a7b3a22151cf
