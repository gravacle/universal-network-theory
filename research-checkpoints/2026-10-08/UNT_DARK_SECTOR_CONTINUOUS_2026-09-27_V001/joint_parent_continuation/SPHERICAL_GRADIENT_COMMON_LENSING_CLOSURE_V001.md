# Changed gradient parent: common weak-field lensing closure V001

2026-10-06 UTC. NEW analytical source/observable join for the changed h=g, ell=100pc parent. Earlier lensing is already substantive: SAVED_POTENTIAL_LENSING_V002 retained20 cases/300 rays and7,891 controls; EFFECTIVE_NO_REFIT_LENSING_V001 retained15 published reduced bins, with inherited7-bin RMS.07949dex versus RAR.07739dex. Those results, numerical failures/repairs and exposed-data limits remain. They do not qualify this changed spatial-gradient law. No field solve, photon integration, data fit or numerical action is performed here.

## 1. A declared minimal completion, rather than a scalar-force assumption

Use the original preferred normal u_mu=-partial_mu T/sqrt(-partial T squared), P=g+uu, spatial modes u.y_delta=0 and v_delta=P nabla_u y_delta. Define the intrinsic spatial derivative

    Dcal_alpha y_delta^mu=P_alpha^beta P^mu_nu nabla_beta y_delta^nu.

In c=1 notation the NEW specified source family is

    S=integral sqrt(-g){M^2 R/2+C integral nu(delta)
       [m_delta v_delta^2/2-V_delta(y_delta)
        +kappa delta a_mu y_delta^mu
        -J_delta(Dcal y_delta)^2/2]d delta}+S_ordinary,
    a=nabla_u u, V_delta=kappa delta^2 y_delta^2/2+u4(y_delta^2)^2/4,
    nu(delta)=A delta, Kb=kappa integral nu d delta,
    C=2M^2/Kb, M^2=(8pi G)^(-1), J_delta=kappa delta^2 ell^2. (1)

Here h_mu=a_mu replaces the former bounded source. The finite endpoint DeltaU is NOT retained, and the Einstein-supplied bare acceleration contact is not added a second time. G and the minimally coupled ordinary massive/light metric dictionary are normalized once. Positive m_delta is held; all normal, mode, constraint and metric variations are included. This is a disclosed effective completion, not a unique relativistic consequence of a nonrelativistic rotation curve or a native microscopic derivation. Extra curvature/clock/source operators would define another completion.

## 2. Leading metric variation includes the gradient stress

Select the stationary aligned branch T=t, zero shift and no independent incoming/excited mode population or large external mode background. On a static slice v_delta=0 and Dcal becomes the intrinsic covariant vector derivative of gamma_ij. Its flat limit is the VECTOR Laplacian, including the radial -2z/R^2 term. With z_s=delta y_delta and s=delta/Lambda, leading mode variation gives

    -ell^2 Delta_vector z_s+z_s+z_s^3/(gc^2 s^4)=grad Phi,
    Z=integral_0^1 2s z_s ds, gc=(3pi/8)a0.               (2)

The SI acceleration fields in (2) are obtained by the SAME c^2 conversion from geometric accelerations. In preferred coordinates N a_i y^i=y^i partial_i N. Its lapse variation supplies the divergence of B=integral nu kappa delta y_delta d delta; B/Kb=Z. Potential/gradient lapse terms instead begin at quadratic field order.

The gradient term has actual spatial stress, including variation of the intrinsic connection. For example, at its leading flat-static quadratic order let y_delta=f_delta(R) Rhat and V_delta=V_delta(f_delta). On the leading mode equations the COMPLETE mode radial/tangential stresses are

    p_r=C integral nu[-V_delta+J_delta f_delta'^2/2
                              +J_delta f_delta^2/R^2]d delta,
    p_t=C integral nu[-V_delta+kappa delta a f_delta
                              +J_delta(2f_delta f_delta'/R-f_delta'^2/2)]d delta. (3)

Connection-variation divergence terms are necessary for (3); treating three vector components as independent scalars would give a different stress. The positive spatial-gradient energy is C integral nu J_delta[f_delta'^2+2f_delta^2/R^2]/2. At this flat order the lapse source also contains C div B and C integral nu V_delta. These displayed terms illustrate the source/order counting, not a complete next-order metric solution: metric/lapse corrections, ordinary stresses and nonlinear Einstein terms must accompany a post-Newtonian calculation.

Write ds^2=-(1+2Phi/c^2)c^2dt^2+(1-2Psi/c^2)dx^2 after the common background/frame subtraction. Require small metric potentials, nonrelativistic ordinary stress, controlled stationary radial gradients and the stated mode branch. Integrated potential/coupling stress is of acceleration-squared order; gradient stress adds ell^2 times derivative-squared terms. In a smooth exterior these are of geometric order M^2[(g/c^2)^2+ell^2(g/(c^2R))^2], one weak-metric order beyond the leading spatial Einstein equation. Small g/a0 is NOT the weak-metric expansion parameter; the nonlinear constitutive response in (2) is retained.

Consequently the leading lapse AND spatial equations are

    Delta Psi-div Z=4pi G rho_b,
    (delta_ij Delta-partial_i partial_j)(Phi-Psi)=0.         (4)

The difference is at most affine on a regular connected patch; the SAME background/frame/boundary matching removes it. Thus Phi=Psi at retained c^(-2) metric order and the leading spherical force is the one already solved. This is conditional leading equality, not exact zero slip. Equation(3), ordinary kinetic stress and nonlinear Einstein terms source the next order together. Preferred-foliation alignment is a physical branch premise, not a demonstrated formation attractor or a proof of all coupled characteristics. The static time-independent aligned branch is consistent with the normal-clock equation; that fact does not select it dynamically.

## 3. Same spherical force, bending and mass crossover

At that metric order the positive lens-equation deflection is

    alpha_hat(b)=c^(-2) integral grad_perp(Phi+Psi) dz
               =2c^(-2) integral g(sqrt(b^2+z^2)) b/sqrt(b^2+z^2) dz. (5)

The ray itself bends inward; alpha_hat is outward in impact-coordinate convention. There is no independent leading light/slip normalization to fit. The known changed-parent exterior is

    g(R)=A_M/R+B_M/R^2+o(R^(-2)),
    A_M=sqrt(GMa0), B_M=beta GM-a0 ell^2, beta=32/(9pi^2). (6)

Taking the weak-metric expansion FIRST, its formal isolated asymptotic projection is

    alpha_hat^(weak)(b)=2pi A_M/c^2+4B_M/(c^2 b)+o(b^(-1)),
    DeltaSigma^(weak)=A_M/(4G b)+B_M/(pi G b^2).           (7)

The DeltaSigma relation uses the circular thin-lens metric identity c^2[alpha/b-alpha']/8piG and the SAME normalized G. It is a geometric excess-surface-density diagnostic, not added halo matter or a raw-shear likelihood. Actual distance/stacking/background assumptions are still required for observational use. B_M changes sign at the SAME Mcrit=a0 ell^2/(beta G) already found in the force law; cancellation there makes neglected terms material.

The o(b^-1) describes the leading weak-field projection, not the exact full deflection: omitted post-Newtonian corrections can include a constant term. A logarithmic isolated potential cannot stay globally weak to infinity. Use the asymptotic only in a window exterior to the actual source, with rM/b and ell^2/(rM b) small, weak potential, negligible external field and actual environmental/cosmological matching radius well beyond the sampled ray. Finite source/observer geometry is not furnished by (7).

## 4. A new bounded saved-state prediction, without a PDE rerun

A finite-aperture contribution avoids inventing the missing tail. Reuse ALL12 sealed SPHERICAL_GRADIENT_FORWARD states (three masses times four fixed arms), their matched local fields and source alternatives. Predeclare b/rM={5,10,20,50}, spherical Rcap=150rM, and

    Zcap=sqrt(Rcap^2-b^2), Ucap=acosh(Rcap/b),
    alpha_ap=4b/c^2 integral_0^Ucap g(b cosh u)du.          (8)

This is a physical partial bending contribution in the adopted Born/weak branch, not the whole observed angle or an asymptotically flat tail closure. Split at every saved radial knot crossed by the ray; use the declared log-radius interpolation and independent Gauss8/16 per interval. Integrate the saved matched delta g separately, preserving the small-gradient signal rather than subtracting two large total angles afterward.

The independent manufactured field g=A/R+B/R^2 has EXACT finite-aperture

    alpha_ap=4/c^2[A atan(Zcap/b)+B Zcap/(b Rcap)].         (9)

For delta g_asym=-a0 ell^2/R^2 the descriptive finite coefficient is

    -delta alpha_ap c^2 b/(4a0 ell^2)=sqrt(1-b^2/Rcap^2).  (10)

Numerical controls can keep the old .02 absolute mesh/spectral/domain tolerance for this normalized gradient-angle coefficient, now at ALL four impacts rather than infer it from the old point readouts. Gauss8/16 coefficient agreement<=1e-10 and total-angle agreement normalized by the fixed 2pi A_M/c^2<=1e-10 separate quadrature from saved-state uncertainty. All arms, signed results and failures remain; closeness to(10) is descriptive, not an acceptance gate. No new source coefficient, length fit, force solve, observed-lensing score or imported vacuum is authorized by this analytical note.

## Frozen direct sources

Paths are relative to this directory; all earlier evidence is preserved.

| Input | SHA256 |
|---|---|
| EXPLICIT_MODE_COSMOLOGY_PATHWAY.md | 5a99341c9abb3a35f3f6b59f54bf07cdc5f623016f8bdc9b1c2327f749d52067 |
| LINEAR_SOURCE_GALAXY_REFERENCE_V001.md | 399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801 |
| SPHERICAL_GRADIENT_FORWARD_V001.md | 5c0419a5590e91d980611bbcd0fd4199be9274a037553023ab06bb67f0352e86 |
| WEAK_FIELD_LENSING_PATHWAY.md | d79f9f32c39555d65085f9420536b6c912330559950897c4416a535dc4ffb06e |
| SAVED_POTENTIAL_LENSING_V002_RESULTS_REVIEW.md | 0e2873f9a103ec7150969a01632cb75fedf909f9418f8da097e6679a9c0429ef |
| EFFECTIVE_NO_REFIT_LENSING_V001_RESULT.md | c5089842a6802ec5a67fe50d14da8c7d276cc39e00a082dc272bf965c3dc07b2 |
