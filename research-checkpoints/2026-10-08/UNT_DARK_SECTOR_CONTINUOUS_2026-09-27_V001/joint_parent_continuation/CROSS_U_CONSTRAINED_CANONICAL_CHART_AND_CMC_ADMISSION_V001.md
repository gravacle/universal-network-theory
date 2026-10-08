# Constrained canonical chart and expanding CMC admission V001

AUTHOR_DRAFT=True. Held analytical review companion. No field, array, source, Hamiltonian, operator, velocity map or trajectory is evaluated. This supplies the exact chart and prerequisite for a conditional late-epoch Cauchy continuation of the same EPS1e-5 action, with all32 modes and all four sigma arms; it does not select a physical formation history or certify an exterior/galaxy solution.

## 1. Reduced variables and complete differentiated constraints

Use c_p=1, signature(-+++), ds²=-N²dt²+h_ij(dx^i+beta^i dt)(dx^j+beta^j dt), n=(partial_t-beta^i partial_i)/N and the inherited K_ij=(partial_t h_ij-Lie_beta h_ij)/(2N). Expansion has K=+3H. Work with independent spatial COVECTORS u_i=U_i and z_ji, not a scalar-gradient material clock or a prescribed U=n.

Put u^i=h^ij u_j, gamma=sqrt(1+h^ij u_i u_j), v^i=u^i/gamma. The exact constrained chart is

    U^0=gamma/N, U^i=u^i-beta^i gamma/N,
    U_0=-N gamma+beta^i u_i,
    z_j0=beta^i z_ji-N v^i z_ji.                         (1)

Thus U²=-1 and U.z_j=0 identically. Differentiate (1) in EVERY spacetime direction before forming F, acceleration, Tz or Dz. In particular partial_t z_j0 contains the u_i and metric velocities; it is not an independent zero. Reconstruct connections from complete metric first jets. The chart is regular for N>0 and positive definite h, without selecting the independent material u_M or its current.

At fixed N,beta and spatial position, (1) defines a Jacobian J from (dot h_ij,dot u_i,dot z_ji,dot phi) to the primitive first jets. For the actual first-order matter action, p_a=J_Aa p_primitive,A and its velocity Hessian is J^T H_primitive J. Include all metric/normalization/projector/temporal-covector columns, plus the EH ADM kinetic term. This is105 mechanical velocities (6+3+96) plus one phase velocity; a fixture using frozen metric may expose99 matter velocities and six metric directions separately. A singular un-reduced unit/transverse Hessian is not cured by clipping or a pseudoinverse.

The raw time densities in the owned held-variable action are p_U,rho=sqrt(-g) Pi_U^0_rho, p_zj^nu=sqrt(-g) Pi_j^0nu and p_phi=sqrt(-g) J_phi^0. Apply the chart Jacobian before fixing their reduced values. For example, p_u includes sum_j p_zj^0 * partial z_j0/partial u_i. The metric momentum includes the corresponding U and z_j0 chart contacts and the native connection coefficient, not only the Einstein momentum. Choose one declared EH boundary/canonical representative; changing a time-divergence representative changes canonical coordinates and cannot be hidden while fixing momentum densities.

## 2. What an aligned cancellation proves, and what tilt retains

For the special U=n chart with spatial covector z, define V_i=(partial_t-Lie_beta)z_i/N-K_i{}^j z_j. Its modal temporal term is N sqrt(h) g w h^ij V_i V_j/(2omega²). Hence

    p_z^i=sqrt(h) g w V^i/omega²,
    pi_native^ij=-p_z^(i z^j)/2,
    (partial_t-Lie_beta)z_i/N=K_i{}^j z_j
                                      +omega² p_z,i/(sqrt(h)g w). (2)

Here symmetrization has weight1/2. Eliminating the temporal modal velocities at fixed p_z cancels their quadratic connection Gram contribution to the metric Schur block and leaves this linear momentum shift. It does not justify copying dot z=0 after inserting K=3H. For U=n the projected spatial Dz is the intrinsic spatial covariant derivative; general tilt has additional contacts.

A concrete exact local counterexample uses N=1,h=delta,K_ij=k delta_ij, U=gamma(1,v,0,0), z_mu=(0,0,z,0), and vanishing coordinate spatial first jets at the point. In the U-rest spatial frame e_X=gamma(v,1,0,0), e_Y=(0,0,1,0), put c=dot z_y-kz. Then

    V_Y=gamma c, D_XY=gamma v c, D_YX=-gamma v kz,
    L_mode,vel=g w gamma²[(omega^-2-ell²v²)c²
                                        -ell²v²k²z²]/2.       (3)

The unit/transverse first jets hold: U^0 nabla_y z_0+z_y nabla_y U^y=0. Eliminating dot z_y removes the c-square metric mixing but retains -g w ell²gamma²v²z²k²/2; other temporal velocities cannot cancel this fixed spatial D_YX component. Thus tilted native gradients can change the reduced metric kinetic operator. In the spatial-covector u_i chart Maxwell F_0i=dot u_i-partial_i U_0 contains no dot h by itself; acceleration.Z is linear in velocities. Their complete chart and native interactions still belong in the joint map. No four-arm smallness, invertibility or ellipticity follows from (2) or (3).

## 3. Canonical normal and momentum constraints before CTS assumptions

Use the complete ADM first-order action, retaining its paired EH and material ports, absolute P(X), relative phase, Maxwell, every nonlinear mode and the unchanged ordinary action. Legendre-transform the REDUCED fields, including total pi^ij=pi_EH^ij+pi_native/chart^ij. Verify lapse/shift velocity primary cancellations. After spatial integration by parts with ports retained, write H_can=integral(N C+beta^i C_i)+boundary/primary terms; equivalently obtain C and C_i by the complete variational lapse/shift rows if such a local canonical representative has not yet been admitted.

The universal spatial generator in this covector chart is

    C_i=-2h_ij D_k pi^jk+p_phi D_i phi
        +p_u^j D_i u_j-D_j(p_u^j u_i)
        +sum_j[p_zj^k D_i z_jk-D_k(p_zj^k z_ji)]+C_i,o. (4)

The momenta are density weight1; D includes that density connection. A fixed ordinary particle/annulus has H_o=N sqrt(m²+h^ij p_i p_j)-beta^i p_i and C_i,o=-p_i delta, with the already owned rest-mass sheet measure once. These are phase/current and angular-momentum data, not an observed velocity fit or a new three-dimensional density. Its Euler/worldline row still evolves the material; substituting an orbit root Omega(g) before the action variation changes the Cauchy prescription.

Fixing canonical DENSITIES fixes charge/momentum in the declared coordinate cells, not proper density after a conformal change. Recover phase velocity by its full conserved-current map, keeping the strict unchanged EOS band and relative-Y contribution. In the grad phi=0 circular subchart p_phi/sqrt(h)=P_X(X)-g X sinh²chi; simply retaining old dot phi/N or replacing this by P_X alone is generally a different state. Test the full derivative/rank, rather than assuming a dust scaling. The ordinary mass/phase/native inventories are not combined or renormalized.

## 4. Exact geometric identities and the conditional CMC solve

For the full on-shell Hilbert source define rho=T(n,n), S=h^ij T_ij and j_i=-T(n,e_i). With Kplus and A_ij=K_ij-Kh_ij/3,

    R3+2K²/3-A²=2rho/M²,
    D_j A^ij-2D^i K/3=-j^i/M²,
    (partial_t-beta.D)K=Delta N
                         -N[A²+K²/3+(rho+S)/(2M²)].          (5)

These remain geometric identities; connection-dependent Hilbert rho,j,S are not thereby K-independent prescribed matter functions. The canonical constraints (4) and normal C, with the reconstructed velocities/reactions, are the safe admission route. Preserve the CMC condition through the FULL coupled Hamiltonian/evolution equations, retaining temporal improvement contacts rather than declaring S an algebraic old-state table.

If h=psi^4 htilde, Atilde^ij=psi^10 A^ij, Ntilde=N psi^-6 and u_tilde=(partial_t htilde)^TF with its indices raised by htilde, the geometric thin-sandwich identity is Atilde=(u_tilde-Ltilde beta)/(2Ntilde). Its Hamiltonian equation is Delta_tilde psi-Rtilde psi/8+|Atilde|²psi^-7/8-K²psi^5/12+rho psi^5/(4M²)=0. The CMC conformal lapse identity has

    Delta_tilde(N psi)=(N psi)[Rtilde/8+5K²psi^4/12
             +7|Atilde|²psi^-8/8+(rho+2S)psi^4/(4M²)]
                                      +psi^5(partial_t K-beta.DK). (6)

The final sign is PLUS for Kplus. On the owned background K=3Hbar, partial_t K=3Hdotbar. These five geometric equations can guide a solve, but the matter/native Schur and full CMC preservation must determine their actual principal/source dependence. Do not hold old total pi_h simultaneously with newly prescribed K, nor infer a physical tracefree velocity/history from stationary iterations. Any retained conformal metric and tracefree velocity are explicitly disclosed free Cauchy data of this conditional branch.

The direct modest prerequisite is the exact local reduced Legendre map at the four saved trials: preserve all raw/mixed blocks and source/clock data, verify the pullback/unit/transverse first jets, aligned cancellation and tilted retained block, and certify reconstruction plus the canonical lapse/shift generator. This can admit a subsequent coupled CMC constraint solve without a220-direction spatial inverse. Physical incoming radiation/native states, perturbed-FLRW boundary/DtN and worldtube metric/extrinsic/current/traction matching remain separate unknown data. Homogeneous cancellation is not an actual galaxy junction. Activity outside0.3--15.1kpc stays undefined, and final physical velocities require exact geodesics of a calculated same-action metric.

## Actual read-only input seals

All paths are relative to J. Bytes were read/hashed before and after exclusive creation; no producer or scientific definition was imported or evaluated.

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- CROSS_U_NONLINEAR_NATIVE_FLOW_AND_CIRCULAR_ACCELERATION_CLOSURE_V001.md — f7fc8138a9683a677851bdf9241c82ca942d4153db1254f513e28eca9f912a21
- CROSS_U_FULL_METRIC_CONSTRAINED_WEAK_VARIATION_SCOPE_V001.md — 2b927d54354eec7f8e8018960c7920c12d8099c070c42c2577cae1af8fe4dad7
- cross_u_saved_full_metric_native_source_residual_v001.py — 23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68
- CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md — 087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523
- CROSS_U_EPS5_FLRW_REFERENCE_METRIC_REGISTRATION_V001.md — 9f75874dc7e8ef2bc937bd20532f9d7ccb5fa333e4fa4d117153412b287d7fd6
- CROSS_U_EPS5_FLRW_REFERENCE_METRIC_REGISTRATION_V001_RESULT.json — ad1d2619c1328386bc20842418f97a47262e3d2646435c52e1e9ab403213fd95
- cross_u_saved_rotating_sheet_frechet_v001.py — ab56dd280d6317699fe38e7b5499d1e25b214197b1d3d1db8a598ad271dc72da
- CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001.md — e1ea987af25cf02dab2460e555f59b13691fefee254e83e1789a1c3a28281f05
- CROSS_U_EPS5_FLRW_GALAXY_JUNCTION_V001.md — baa25990f0b2d4ca925e1a74fb65b40c2968890bd552e9f64541e620e07c6965
