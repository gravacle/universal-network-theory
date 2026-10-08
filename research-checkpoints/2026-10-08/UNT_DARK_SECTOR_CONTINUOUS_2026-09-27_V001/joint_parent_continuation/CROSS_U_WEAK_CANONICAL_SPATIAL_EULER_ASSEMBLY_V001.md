# Weak canonical spatial Euler assembly V001

AUTHOR_DRAFT=True. Root-requested bounded mathematical assembly, held for full review. Static differentiation only; no scientific function, array, operator, Gram, inverse, solve or evolution is evaluated. This uses the same EPS1e-5 action and sigma1 diagnostic member, KB=.02,C=1.98, all32 owned nodes/weights and ell=.1. New source additions remain held. It computes no metric correction, physical rate, formation history or geodesic prediction.

## 1. The actual new calculation and its seed

The CLOSED weak99 solution supplies a genuine nodal native rate and its R/Z derivatives. The four immutable Q1/WHOLE columns supply configurations, spatial first jets, the earlier owned covariant time jets and the prescribed instantaneous L2 metric rate kstar=2N Hbar h. Keep kstar distinct from a rate in the newly registered23048-coefficient metric basis. Replacing only the native time jets by the CLOSED weak99 rate is an explicit conditional instantaneous seed; it does not project kstar or claim a complete nodal Cauchy solution.

The shortest new executable is the complete local native99 and six-metric value/R/Z configuration-force coefficient fields on this seed, then their genuine weak nodal loads. This is a nonlinear spatial Euler calculation. It needs no105 kinetic replay, CG, metric target, extra source, physical history or chosen exterior. It does not rename the four lapse/shift constraints as spatial metric forces. The full force for acceleration still requires section5's no-acceleration momentum derivative.

## 2. Exact constrained chart and all its derivative contacts

Use u_i=U_i and z_ji as independent covectors. Write up=h^-1 u, gamma=sqrt(1+u.up), U0=gamma/N, Usp=up-beta U0 and z_j0=-Usp.z_jsp/U0. Let D denote any actual spacetime first derivative or configuration differential. Then

    D ih=-ih(Dh)ih,
    D up=ih Du-ih(Dh)up,
    D gamma=[up.Du-up.(Dh)up/2]/gamma,
    D U0=Dgamma/N-gamma DN/N^2,
    D Usp=Dup-(D beta)U0-beta DU0,
    D z_j0=-[(D Usp).z_jsp+Usp.Dz_jsp]/U0
                                      +(Usp.z_jsp)DU0/U0^2.       (1)

All four derivatives, including time and azimuth connections, remain even for axisymmetric probes. The raw partial-coordinate azimuth derivatives of the configuration are zero, not their covariant derivatives. Metric compatibility recovers dg from the saved Gamma; dhi=-hi dg hi, DN=N^3 dhi00/2 and D beta=2N DN hi0i+N^2 dhi0i. This does not introduce second metric jets.

Define the already owned JU=U_,u, JzU=z0_,u, Jzz=z0_,zsp. Their complete derivatives are

    JU0=up/(N gamma), JUsp=ih-beta tensor JU0,
    D JU0=Dup/(N gamma)-JU0(DN/N+Dgamma/gamma),
    D JUsp=Dih-(D beta)tensor JU0-beta tensor D JU0,
    Jzz=-Usp/U0, D Jzz=-DUsp/U0+Usp DU0/U0^2,
    JzU_j=-z_j.JU/U0,
    D JzU_j=-[(Dz_j).JU+z_j.DJU]/U0+z_j.JU DU0/U0^2.     (2)

For a fixed symmetric coordinate metric tensor E_a, put t=up.E_a.up. At fixed N,beta,u,zsp,

    embed_a,sp=E_a, embed_a,0i=(E_a beta)_i,
    embed_a,00=beta.E_a.beta,
    Uh_a,0=-t/(2N gamma), Uh_a,sp=-ih E_a up-beta Uh_a,0,
    zh_ja=-z_j.Uh_a/U0,
    D t=2(Dup).E_a.up,
    D Uh_a,0=-Dt/(2N gamma)-Uh_a,0(DN/N+Dgamma/gamma),
    D Uh_a,sp=-Dih E_a up-ih E_a Dup-(D beta)Uh_a,0
                                                    -beta D Uh_a,0,
    D zh_ja=-[(Dz_j).Uh_a+z_j.DUh_a]/U0+z_j.Uh_a DU0/U0^2. (3)

D embed retains both beta derivatives; E_a itself is fixed. These formulas retain the exact differentiated unit/transverse constraints. The earlier longitudinal metric lift deltaU=(qUU/2)U is not this canonical fixed-u chart.

## 3. Native first-jet weak coefficient without a strong divergence

For each independent native component qA let C_U,A=U_,qA and C_zj,A=z_j_,qA. For u_i they are JU_i and delta_nu0 JzU_ji. For z_ji they are0 and delta_nui+delta_nu0 Jzz_i. Let A_U,Pi_U and Pi_j be the full untruncated owned raw first-jet coefficients; A_zj=w_j(a_U-f_j z_j^raised), f_j=1+z_j^2/[(B0 GC)^2 xi_j^4]. The exact canonical coefficient density is

    A_can,A=dens[A_U.C_U,A+sum_j A_zj.C_zj,A
               +Pi_U:nabla C_U,A+sum_j Pi_j:nabla C_zj,A],
    P_can,A^alpha=dens[Pi_U^alpha.C_U,A
                                      +sum_j Pi_j^alpha.C_zj,A]. (4)

Here dens=N sqrt(h), and nabla C includes (2) plus the actual vector/covector connection. The alpha0 row must agree with the current exact constrained momentum; do not declare old target and actual point momentum bit equal. Quartic, relative phase, acceleration.Z, both modal projector vertices and normal/unit reaction pullbacks all remain. No lambda or mu is setzero.

The spatial weak Euler load for a fixed native basis E is

    E_n,h=<A_can E+P_can^R E_R+P_can^Z E_Z>.              (5)

Native covector phi uses R^2 times its coefficient: its value coefficient is R^2 A_phi+2R P_phi^R; R/Z gradient coefficients are R^2 P_phi^R/Z. Apply the authentic axis/reflection masks and hats. Sum with reference_volume/R once; no extra R,reflection2,2pi or separate synthetic sheet jump.

## 4. Full fixed-chart metric configuration forces and ADM/EH representative

For one scalar test f in metric coordinate a, at delta hdot=0 set

    q_g=embed_a f, eta=Uh_a f, delta z_j0=zh_ja f,
    dq_g=(D embed_a)f+embed_a df,
    d eta=(D Uh_a)f+Uh_a df,
    d(delta z_j0)=(D zh_ja)f+zh_ja df, df_t=0.             (6)

The native action derivative is metric_native(q_g,dq_g,eta,deta) PLUS variation(eta0,deta0,delta z,d delta z). The second contribution is indispensable because metric_native holds the mode covector fixed. It retains the full connection and measure contacts once.

Use the admitted ADM/GHY time representative, not the legacy4D Gamma-Gamma Euler row. With K=(hdot-Lie_beta h)/(2N), Q=Kij K^ij-K^2, the kinetic metric variation at fixed N,beta,hdot is

    deltaK=-Lie_beta(delta h)/(2N),
    delta L_EH,kin=N sqrt(h)/(2C){Tr(ih delta h)Q/2
       +2(K^ij-K ih^ij)deltaKij
       -2[K^i_k K^jk-K K^ij]delta hij}.                  (7)

The spatial curvature uses the same first-derivative reference-connection representative: C3=Gamma[h]-Gamma[barh], trC_i=C3^k_ik, V=N sqrt(h)h^-1/R and barD its cylindrical flat-reference derivative,

    L_R/R=[-(barD_k V^ij)C3^k_ij+(barD_j V^ij)trC_i
       +V^ij(C3^k_ij trC_k-C3^l_ik C3^k_jl)]/(2C).       (8)

Differentiate every V,barDV,C3 and trace factor using delta h and its complete spatial jet. Its paired spatial divergence and ADM/GHY temporal port are retained as unknown data, not setzero. No strong second derivative of Q1 fields or pointwise comparison with unreduced R4 is needed.

Absolute phase adds dens[P_X deltaX+P Tr(hi q_g)/2], deltaX=-delta(hi)phi.phi/(2X). It has no mechanical velocity Hessian, but its metric/U forces are present. Ordinary rest-mass elements retain their fixed covariant p_i: Gamma=sqrt(1+ih^ij p_i p_j), H_o=dM(N Gamma-beta.p) and the configuration action force is +dM N p^i p^j delta hij/(2Gamma), at the unchanged owned annular support. There is no3D density, new mass or frozen-Omega substitution.

Local six-coordinate force coefficients must finally pull through the regular metric F basis and its R derivative. In particular its value coefficient includes F^T A_metric+F_R^T P_metric^R, with gradient coefficients F^T P_metric^R/Z. The symmetric offdiagonal tensor and factor2 momentum pairing occur once.

## 5. What this enables and what it does not yet supply

The saved nodal native rate supplies both value and spatial derivatives. The analytic instantaneous metric law supplies partial_i kstar=2Hbar[(partial_i N)h+N partial_i h]; it remains the separately declared L2 seed. A subsequent exact derivative of the same weak momentum map gives F=E_h-(D_t p_h)_noacc; retain spatial rate jets, gauge-rate coefficients and paired temporal improvements. Only then does the global signed reduction G_h kdot=F_m-B_h^T M_h^-1 F_n apply. The six sampled Schur columns do not establish full G_h regularity, free shear or a metric canonical target.

The weak CMC derivative remains <sqrt(h)S[Kdot-3Hdotbar+theta(K-3Hbar)]>, with inverse-metric, lapse and both shift Lie derivatives from119 Eq6. Keep the theta term and beta.gradK unless strongCMC is established. No bare-EH stress table replaces the native connection/metric momentum.

Phase charge evolves by its exact current, and independent ordinary worldlines satisfy xdot=N ih p/Gamma-beta, pdot_i=-Gamma N_i-N(partial_i ih)pp/(2Gamma)+p_j partial_i beta^j. Axisymmetry conserves p_phi without freezing R/Z positions or meridional momenta. The old circular phase pdot0 is not copied after meridional changes. The homogeneous aligned zero-mode check gives2Hdot+3H^2=-C p_total and3H^2=C rho_total, hence Kdot=-3C(rho_total+p_total)/2=-3eta^2[b+4r/3+w], the ownedEPS5 result; it supplies no local cosmic material/photon state.

Needed for an actual evolution/metric solution: full regular metric rate or canonical/free-shear data, force-convective and phase-current rows, checked gauge reduction, full signed weak map admission, and physical induced-metric/extrinsic/current/traction/incoming-state ports. The immutable lapse/shift residuals remain constraints at their own earlier mixed seed; updating native time jets requires evaluating their new current rows. Boundary hats remain mathematically defined tests with explicitly unknown physical ports, not wall conditions. Reflected sheet/internal weak contacts occur once; neither15.1kpc nor128kpc is an automatic FLRW tube. Unknown activity outside0.3--15.1 staysunknown, baryons are not trimmed, and no new force/source gain is introduced. Final velocities remain exact geodesics of a calculated full metric.

## Exact unchanged bindings

All hashes below were read with stdlib only before exclusive creation; no source definition or payload was evaluated. The new producer requires complete terminal admission and its own prospective arithmetic controls before root-only execution.
- CROSS_U_FULL_CANONICAL_CMC_PRESERVATION_EXTENSION_V001.md — 60a222d80500b01771092919ede0d1374969ee769471964aec911929aad9e424
- CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_AND_CMC_EXTENSION_V001.md — 78491aa4158dec6152a19136d5b3265cc63cdc965ebf4002d8df371074b46806
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_MAP_AND_BASIS_V001.md — faf6d1d5cccb9266cde70c1a6264745da2cea9e1f3ceaab871a760ee1d0bada9
- cross_u_whole_slice_q1_adm_residual_v001.py — c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a
- cross_u_saved_full_native_adm_legendre_v002.py — 9185f2dcd981d7599023858dd8c533b13a510c150ad994b5ea3f569b947d9de0
- cross_u_weak_nodal_native_legendre_v001.py — e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json — e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RECEIPT.json — 00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae
- cross_u_weak_nodal_metric_temporal_cmc_v001.py — e11bb7ec123971998fbdd64d1e2171627aae9202804d1c625202f412b5f85b6c
- CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RESULT.json — 2210b4993989d6cb432d9981cc8819f1c21c394ded9d349f6d34b009adb92528
- CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RECEIPT.json — f74d4d67ba87838b4902dc53eebd38812c9b723870ef57528144a7b3a22151cf
- NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001.md — e8911d59ae25f9d397a57a6dcd6d0ca5c450df82566935c00f8436568f7484ff
