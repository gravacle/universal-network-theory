# Exact retarded radiation moment operator for the admitted S_cross source

2026-10-06 UTC. Accepted analytical interface after root and independent full mathematical/pin reviews; sealed read-only. No operator, kernel, source, background, state or trajectory is evaluated. This derives the original collisionless radiation operator and a prospective mathematical witness. It neither adopts a new prepared universe nor relabels any old failure. The separate repaired FINE worker retains its original finite angular rule; this note supplies a different, explicit operator route for later review.

The source references are `cross_u_full_flrw_source_constraint_v001.py`: `phase_nodes` at132, `radiation_weights` at138, `radiation_map` at151, `rate_matrix` at171, `panel_step` at203, `original` at248, `preparation` at267 and `metric_increment` at273. Proper-time units and the two prepared columns are the original ones. The stored background field `cs` is already s=c_s^2, not c_s; write C_p=s Gamma_phi, A=qV, R=Psi+hV and dtheta=q dt=(q/h)dx with x=log a.

## 1. Exact shifted characteristic and retained initial distribution

The original physical brightness satisfies Fdot+iq mu F=4 Psidot-i4q mu Phi. Its stable angular chart is Y=F+4hV+i4qVmu. Using qdot=-hq, Vdot=Phi+C_p and the full derivative of R gives

    Ydot+iq mu Y = 4 Rdot - 4q^2 mu^2 V + i4q mu C_p,
    Y_theta+i mu Y = 4 R_theta - 4 mu^2 A + i4 mu C_p.       (1)

Thus Y_l=(i^l/2)integral P_l Y, Y_0=Gamma_r, Y_1=F_1-4qV/3=4q w_r/3 and Y_l=F_l for l>=2. The qdot and Vdot contacts cannot be removed by freezing q or by omitting s Gamma_phi. The actual initial Y_i(mu), including both original columns, enters

    I_l(T)=(i^l/2)integral_-1^1 P_l(mu)
                         exp[-i mu(T-theta_i)]Y_i(mu)dmu.   (2)

The owned preparation makes Y_i a constant Gamma_r,i in mu, so I_l=Gamma_r,i j_l(T-theta_i). This is a consequence of that full initial chart, not permission to reset a later angular state. More generally a specified polynomial angular preparation uses the corresponding derivatives/Gaunt kernels; arbitrary incoming angular information must remain in(2). Seven saved low moments alone do not determine its later free propagator.

## 2. Locally anchored derivative-free source panels

For a completed phase panel[a,b], target T>=b and DeltaR(s)=R(s)-R(a), the exact contribution to Y_l is

    B_l(T;a,b)=4 j_l(T-b) DeltaR(b)
      +4 integral_a^b [j_l'(T-s)DeltaR(s)
                      +j_l''(T-s)A(s)-j_l'(T-s)C_p(s)]ds.  (3)

This follows integration by parts of 4 integral j_l(T-s)R_s ds. The constant R(a) terms cancel analytically; DeltaR(a)=0. If that anchor condition is not used, retain the a-end boundary as well. A current partial panel ends at its actual target b=T, giving 4delta_l0 DeltaR(T). Each older panel retains its own nonzero Bessel endpoint and source; replacing its endpoint by the current-panel delta would be wrong. Full transport is I_l plus the sum of all completed panels and the current partial panel.

This is exactly the phase-cubic source representation already used in the original `radiation_map`: use its four actual nodes theta_0,theta_G1,theta_G2,theta_E. Interpolate the node PRODUCTS q_j V_j and s_j Gamma_phi,j in the same Lagrange basis, and R_j-R_0. Do not interpolate V and then freeze q, square the already-squared `cs` field, or identify the log-a Gauss fractions with the nonlinear phase fractions. Current stage/end values remain simultaneous unknowns in the same33 core rows. An implementation retains every completed source panel and the full initial angular preparation, rather than adopting a seven-moment reflecting wall.

For low-l weights W_(lj)^(m)=integral_a^b j_l^(m)(T-s)L_j(s)ds, m=1,2, the R_j column is 4j_l(T-b)(delta_jb-delta_j0)+4[W_(lj)^(1)-delta_j0 sum_k W_(lk)^(1)], A_j has4W_(lj)^(2), and C_p,j has-4W_(lj)^(1). Here delta_jb refers to an actual source node b; for a general b use L_j(b). Normalize the interpolation coordinate on the panel to avoid unnecessary inverse powers of a small width. Use stable accumulated phase differences and retain independent phase quadrature comparisons.

## 3. Stable kernels and independent low rows

For l>=1, j_l'=l j_(l-1)/(2l+1)-(l+1)j_(l+1)/(2l+1), with j_0'=-j_1. For l>=2,

    j_l''=l(l-1)j_(l-2)/[(2l+1)(2l-1)]
      -[l^2/((2l+1)(2l-1))+(l+1)^2/((2l+1)(2l+3))]j_l
      +(l+1)(l+2)j_(l+2)/[(2l+1)(2l+3)].                  (4)

Use j_0''=(2j_2-j_0)/3 and j_1''=(2j_3-3j_1)/5. At zero, j_l=delta_l0, j_l'=delta_l1/3, j_l''=-delta_l0/3+2delta_l2/15. Therefore low moments0..6 need analytic j0..8. No small-argument recurrence divides by the phase; a factorial series supplies the values and these combinations supply their derivatives. Large-argument low-order sin/cos recurrence remains separately checked arithmetic, not an interval certificate.

The exact shifted low rows are

    Gamma_r_dot=4Rdot-qY_1-4q^2V/3,
    w_r_dot=h w_r+Gamma_r/4-F_2/2-C_p,
    F_2_dot=q(2Y_1-3Y_3)/5+8q^2V/15.                    (5)

The last V term is required by the physical F_1 shift. Phi_dot still retains the actual rdot/qdot contacts in the original shear equation. These differential identities and source/density/metric constraints must be independently checked against a numerical representation; exact kernel algebra alone does not qualify the coupled discrete solution.

## 4. Radiation balance quadrature is separate from evolution

The original `metric_increment` integrates delta_r_dot/h at only the two log-a Gauss nodes, whereas radiation evolution integrates the phase-cubic characteristic source with16/32 nodes. A fast radiation balance can underresolve that separate two-node diagnostic even when the transport is consistent; this is a hypothesis to test, not a promotion of the failed radiation gate or a causal conclusion from the small whole-density error.

Since delta_r=Y_0-4hV and Psi=R-hV, the exact derivative-free contrast balance is

    Delta(delta_r)=4Delta(Psi)
                 -integral_a^b [Y_1(s)+4A(s)/3]ds.        (6)

The endpoint hV contact and the varying q/h phase conversion remain. Fubini applied to(3), j_1(0)=0 and j_1'(0)=1/3 give the equivalent flux expression

    integral_a^b [Y_1+4A/3]ds = Y_0(a)-I_(0,a)(b-a)
       +4 integral_a^b [j_1(b-s)(DeltaR-C_p)
                       +j_1'(b-s)A]ds,                  (7)

where I_(0,a) is the free propagator of the FULL incoming Y(a,mu). The -4integral A/3 generated by integrating Y_1 cancels the explicit streaming shift in(6). The radiation contrast is not the absolute background energy: a^4 r is constant in this admitted fixture, so its weighted contrast balance follows by the same fixed factor. No source-temperature or absolute-vacuum assumption is added.

For an independent diagnostic, evaluate the incoming propagator and source/flux integrals by a separate quadrature/reference, not by rearranging the final Y_0 from the same computation. The latter would force a tautology. Retain the original1e-6 functional threshold and its failed dispositions; an independently converged alternative quadrature must be prospectively qualified before changing a numerical diagnostic.

## 5. Modest independent source-operator witness

The closed old pure-kernel packet already controls low-l opacity/Bessel/primitive identities; it has a S_dual physical parent and supplies no S_cross state. Its exact `complex_moment(p,z)=integral_0^1 exp(-zu)u^p du` helper can be reused literally with its52-term series/expm1 recurrence. The cubic p=3 extension and the new l0..8/large-past/source-panel scope need new controls, not a rerun or promotion of the old census.

For normalized panel coordinate u=(s-a)/delta and cubic coefficients R_m,A_m,C_m, the independent characteristic source is

    4 exp[-i mu(T-a)] {sum_(m>=1)m R_m I_(m-1)(-i mu delta)
        -delta mu^2 sum_m A_m I_m(-i mu delta)
        +i delta mu sum_m C_m I_m(-i mu delta)}.           (8)

For a partial current panel, use its actual upper fraction in those polynomial moments. This route uses neither a Bessel helper nor temporal Gauss quadrature. An independent high-order angular projection can compare the full signed R/A/C cardinal-source tensors with(3) at time16/32/64. Actual saved phase-node fractions, disclosed manufactured widths<=12, large fixed past phases, exact zero/contact and full owned initial-column controls are a bounded mathematical test. No trajectory, source-history replay, angular reset, numerical fit or new physical normalization is authorized by that test.

## Protected input bytes

| Input relative to J | SHA256 |
|---|---|
| cross_u_full_flrw_source_constraint_v001.py | 8e2860917a75c44ada5be0df18ac43809dc7fe454846b3787d8a3d3017d1e5c1 |
| CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md | c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986 |
| CROSS_U_FULL_FLRW_FINITE_SLICE_V001_ERROR_RAW.npz | 06646ec193334c46d84586c84814e5ad2f58f96ce7624a7dde019f8ba226c5a2 |
| CROSS_U_FREE_STREAMING_ANGULAR_QUADRATURE_WITNESS_V001_RESULT.json | e17f6e658c72db576945f865c72aa5886f90d64f130112d8f0af5ee9d949bad3 |
| CROSS_U_FREE_STREAMING_ANGULAR_QUADRATURE_WITNESS_V001_RECEIPT.json | a0974c6337ee1c39d054b135f6817a08197d064718410ace9f2ef847d1c6411b |
| constrained_u_retarded_radiation_kernel_controls_v001.py | dc7885ee0349145f05a7e18bf9ce48bf257626ebbc4bd48ebc366791fe456db2 |
| CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001_RESULT.json | b541b0a5e3f2ea1827f166907f96e9b76bf2d2ad4c6366c3a0efbf15a7661530 |
| CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001_RECEIPT.json | 9e845b9a18035b4b199ac0f3a6153b4123f1816c353bdec0e0ef7fdaddaf19dc |
| CROSS_U_EXACT_RETARDED_RADIATION_MOMENT_OPERATOR_REVIEWED_95_LINE_DRAFT_V001.md | c3c02df69e7311ae5981d29a7a5df9693a97ba68094e44f12d2885b76833e525 |
