# Weak nodal six-metric temporal map and CMC extension V001

AUTHOR_DRAFT=True. Root-requested held analytical/implementation contract; no numerical producer, helper, field, tensor, operator, Gram, inverse, solve or evolution is evaluated. This extends the same EPS1e-5 action and the accepted119-line CMC equations, keeping KB=.02,C=1.98,ell=.1, all32 original modes and the unchanged proper clock. The first bounded kinetic test uses the already declared sigma1 member; the four parent arms remain unchanged conditional outcomes. The user hold on new source terms remains in force.

## 1. Genuine six-metric temporal basis and canonical pairing

Keep the authentic87x45 nodes,86x44 cells and four3784-point columns. E is exactly the accepted85-line native99 temporal basis. Define a new fixed coordinate metric evaluation map F from six scalar coefficient fields(a,b,c,d,e,f) by

    H_RR=a+R^2 b, H_ZZ=f, H_phiphi=R^2 a,
    H_RZ=R d, H_Rphi=R^3 c, H_Zphi=R^2 e.                (1)

The symmetric off-diagonal entries occur twice in the tensor. With X=R dR=x dx+y dy and Y=R^2 dphi=x dy-y dx, (1) is a(dx^2+dy^2)+b X^2+2c XY+2d X dZ+2e Y dZ+f dZ^2. Thus the shared a and the indicated powers are the regular Cartesian axisymmetric tensor tangent, not six unrelated cylindrical diagonal/off-diagonal hats. Coefficients are prospective Q1 fields: all are axis-even with node0 tied to node1; a,b,c,f are reflection-even in Z, while d,e are odd/value0 at Z=0. Outer instantaneous coefficients remain free. There are4*86*45+2*86*44=23,048 independent metric coefficients, and403,340 native-plus-metric coefficients. No dense matrix of that size is proposed.

Use the affine offset h(x,t)=h_seed(x)+F(x)b_h(t), b_h(t0)=0. F and E depend only on the fixed coordinates/hats, not on the evolving metric or a moving tetrad. No immutable seed or old temporal trace is overwritten or retroactively declared to satisfy the new basis. Metric positivity is required at the evaluation instant; finite amplitudes would need a separate domain check. All R powers use the existing geometric-kpc coordinates, with the corresponding coefficient units; they are not source gains.

The original local six-coordinate order is(RR,ZZ,phiphi,RZ,Rphi,Zphi), with unit tensors E_a having both off-diagonal entries1. Pi_a=pi_total^ij E_a, so Pi_RZ=2pi_total^RZ, and similarly for the other off diagonals. F maps(1) into that local order. Pair F^T Pi_a once; do not add another2 or differentiate the basis with respect to h. Its radial jets retain2R a+R^2 a_R,3R^2 c+R^3 c_R,d+R d_R and2R e+R^2 e_R. These jets are needed in later weak forces even though the instantaneous kinetic mass has no spatial derivative of the velocity unknown.

Coordinate momentum densities already contain cylindrical R. Define brackets <v>=sum_q omega_q v(q), omega_q=reference_volume_q/R_q. No additional R,2pi,reflection2 or action mass lumping is allowed; all quadrature points have R_q>0.

## 2. Available affine momenta and exactly new kinetic columns

At each unchanged point let v_star be Q1 owned_chart_old_velocity and k_star the six-coordinate hdot from its authentic copied_q{iq}_owned_hdot_tensor/new_owned_hdot_tensor partitions. Native p_star is assembled from copied_q{iq}_native_p/new_native_p. Q1 owned_native_canonical_density is the copied old target, not the actual p_star. Retain the certified finite gap. Metric Pi_star comes from owned_metric_native_p plus the six-coordinate contraction of owned_EH_p; equivalently contract owned_metric_total_p. WHOLE metric_total_canonical_density is the distinct old seed, not a target implied by K=3H.

The complete same-action affine map is

    [p_n;Pi_m]=[p_star;Pi_star]
         + [[M,B],[B^T,T]] [v-v_star;k-k_star],
    T=T_native+T_EH.                                    (2)

M is the accepted fixed99 map. Exactly six NEW local metric time jets, y_native=0 and k=E_a, suffice for B and T_native. Use the accepted JU/JzU/Jzz/Uh/zh/embed chart and the full deltaGamma,deltaF,deltaV_j,deltaD_j, reduced-momentum and connection-momentum pullbacks. Unit/transverse reactions are thereby retained. Do not replay105 columns or copy an eight-point matrix as a whole-slice field. The acceleration.Z vertex is affine and remains in the saved baseline; it is not added to the kinetic Gram. Every32 mode contributes, including the negative projected-gradient term. The independent EH term is

    T_EH,ab=sqrt(h)/(4NC) [Tr(E_a ih E_b ih)
                                  -Tr(ih E_a)Tr(ih E_b)]. (3)

This is the admitted ADM/EH representative with its paired ports. Phase and ordinary first-order canonical actions have no hdot/native-dot velocity cross block, but their metric/U/current forces remain in CMC evolution. No pressure subtraction or bare-EH replacement of T_native is made.

The four Q1/WHOLE configurations, native fixed-p targets, actual point stars and all32 spectra are available. No metric nodal canonical target, five trace-free metric rates, continued wall trace or temporal force is earned by those snapshots. Selecting Pi_target=old WHOLE Pi AND K=3H would be an additional generally incompatible pair of data; neither is silently imposed.

## 3. Global weak map and signed Schur, with projection remainder

Define c_n=p_star-Mv_star-Bk_star and c_m=Pi_star-B^T v_star-Tk_star. Then

    M_h=<E^T M E>, B_h=<E^T B F>, T_h=<F^T T F>,
    c_nh=<E^T c_n>, c_mh=<F^T c_m>,
    r_n=p_n,target,h-c_nh,
    M_h v_h+B_h k_h=r_n,
    Pi_m,h=c_mh+B_h^T v_h+T_h k_h.                      (4)

The CLOSED weak99 RHS held the L2 k_star fixed. The new r_n therefore equals that exact old RHS PLUS <E^T B k_star>; it is not copied unchanged into (4). Preserve the old solve residual rather than replacing its numerical certificate by exact equality. Rebuild metric Pi_star in the same actual chart; canonical densities are not tensors without the off-diagonal conversion.

Eliminating native temporal coefficients means genuine GLOBAL solves,

    G_h=T_h-B_h^T M_h^-1 B_h,
    Pi_m,h(k_h)=c_mh+B_h^T M_h^-1 r_n+G_h k_h.           (5)

For a supplied metric canonical target the RHS would be Pi_target,h-c_mh-B_h^T M_h^-1 r_n. G_h is signed and need not be regular merely because local six-component tests passed. No positive-metric gate, jitter, pseudoinverse or physical stability claim is permitted. A target-free computation of(5)'s action is already well defined.

At fixed positive native M, put G_loc=T-B^T M^-1 B. Completing the SAME square gives the exact relation

    k_h^T[G_h-<F^T G_loc F>]k_h
       = min_vh <||E v_h+M^-1 B F k_h||^2_M> >=0.        (6)

This is another retained finite-basis projection remainder. The full local G_loc contains the already accepted tilted native metric-gradient term and is generally signed; (6) does not reduce it to EH. Pointwise six elimination followed by scatter would omit(6). Neither the local one-negative/five-positive EH signature nor the eight-point full-Schur signature fixes the global signature.

## 4. Nodal CMC trace and its complete evolution row

Use the scalar axis-even/reflection-even Q1 test basis S_A (3,870 independent tests), mu_q=sqrt(h_q) and the same omega_q. With Kplus=tr(ih[hdot-Lie_beta h])/(2N), register

    C_Aa=<mu S_A Tr(ih F_a)/(2N)>,
    d_A=<mu S_A [3Hbar+Tr(ih Lie_beta h)/(2N)]>,
    C_Aa k_h^a=d_A.                                    (7)

Use full tensor traces, including off-diagonal multiplicity. The equivalent saved-star RHS is d_A=<mu S_A[3Hbar-K_star+Tr(ih k_star)/(2N)]>; this needs no new spatial-gradient replay. Keep the saved finite K_star-3Hbar gap. A weak trace equation does not imply pointwise constant K or zero gradients. It leaves five metric rate fields per point to be supplied/solved rather than hiding them in an old total momentum.

For fixed coordinate tests the exact time derivative of the weak trace residual is

    dot C_K,A=<mu S_A [Kdot-3Hdotbar
                                      +theta(K-3Hbar)]>,
    theta=Tr(ih hdot)/2.                                (8)

Kdot is the complete CMC119 Eq(6), including hddot, Lie_betadot h, Lie_beta hdot, inverse-metric and Ndot terms. If written with D_t^beta K=Kdot-beta.grad K, retain beta.grad K explicitly in(8). The theta(K-3Hbar) term cannot be dropped merely because the nodal weak trace residual is zero. Weak trace preservation and a strong CMC field are distinct qualifications.

At the discrete action level let F_n,F_m be the complete weak Euler forces minus the no-acceleration derivatives of c_h and H_h. Eliminate native ACCELERATIONS globally:

    G_h kdot_h=F_m-B_h^T M_h^-1 F_n,
    vdot_h=M_h^-1(F_n-B_h kdot_h).                       (9)

Insert (9) into(8), retaining all current E/F velocity values and spatial derivative contacts. This is the genuine discrete counterpart of CMC119 Eqs(3)--(7); a pointwise Schur acceleration inserted into nodal trace tests is not equivalent. Exact phase-charge/current evolution and independent rotating ordinary worldline xdot/pdot accompany it. The old phase pdot0 applies only to its original circular seed; axisymmetry conserves ordinary p_phi without freezing p_R/Z or positions.

Needed for(9), not supplied by the kinetic map: the full untruncated spatial force/fluxes and their sheet/internal/time ports; actual gauge Ndot/betadot or a checked canonical gauge reduction; phase-current/clock inversion and photon/material canonical data; and an admissible exterior/current/extrinsic matching state. These are action derivatives or physical data, not permission to add a source function. A weak kinetic extension alone cannot solve the five normal/momentum/CMC rows or predict velocities.

## 5. Shortest bounded executable continuation

First compute only six metric kinetic columns per genuine quadrature point, their uncancelled operation bounds, B/T actions and the complete C/affine vectors in(4),(7). Reuse CLOSED weak99 coefficients/basis/targets; no105 replay or dense403,340-square allocation. As six predeclared arithmetic probes take each of the six coefficient unit hats at the fixed interior node(43,22), preserving its registered reflection basis. They are metric tangent tests, not physical rates or a favored radial profile.

Six original weak native solves M_h y_a=B_h e_a give the6x6 sampled GLOBAL matrix e_a^T T_h e_b-(B_h e_a)^T y_b. Save every original RHS/action/residual, the affine native RHS correction, signed metric projections, C trace columns, all current iterates and raw bounds. Normalize for conditioning by the positive proper-tensor metric Gram <mu Tr(ih F_a ih F_b)>, while preserving original units/actions. No metric correction is applied. This finite test measures the actual coupled kinetic/trace interface and whether the sampled signed block is regular; it does not certify the full G_h rank, ellipticity or stability.

Independent prospective controls should cover the Cartesian polynomial/six-coordinate/offdiag pairing; F lift/adjoint and authentic R-power derivatives; EH trace/shear and tilted same-action metric-gradient witnesses; B/T symmetry and independent kinetic Gram; each original M_h solve; and the exact weak CMC trace/star identity. The numerical producer requires its own held protocol, finite caps and original residual gates before root execution; no new producer is authored or run here. Next self-consistent rate/evolution requires a declared metric target/free shear plus(8),(9)'s forces, gauge and physical ports.

Unknown activity outside0.3--15.1kpc remains undefined;15.1 is neither the baryon edge nor a FLRW matching tube. No baryons are truncated, cosmic population duplicated, active gain inferred, ordinary flow identified with U, or source term added. Final physical velocities remain exact geodesics of a subsequently calculated full metric. This extension is an instantaneous same-action mathematical bridge, not a physical galaxy/exterior solution.

## Actual immutable input bindings

The weak99 terminal pins were None while its worker was live; they are now bound only after root28469 naturally CLOSED. Its21 arithmetic controls and10 pairs are terminal metadata, not a full physical qualification. A future producer must additionally require the root/distinct saved-data admission and exact terminal maps before numerical evaluation. All inputs below were0444 and hashed before this exclusive write; no payload array was evaluated.

- CROSS_U_FULL_CANONICAL_CMC_PRESERVATION_EXTENSION_V001.md — 60a222d80500b01771092919ede0d1374969ee769471964aec911929aad9e424
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_MAP_AND_BASIS_V001.md — faf6d1d5cccb9266cde70c1a6264745da2cea9e1f3ceaab871a760ee1d0bada9
- CROSS_U_CONSTRAINED_CANONICAL_CHART_AND_CMC_ADMISSION_V001.md — 872ca230d040bfca08ac127c117e741e81549a4316e62dd5de8df8e8732f7e98
- cross_u_weak_nodal_native_legendre_v001.py — e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001.md — 2c9da869068cf3d2ae9269395b111ec1d0e71f26e0ffef6ff0afb50e40995a0e
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json — e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5
- CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RECEIPT.json — 00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae
- cross_u_whole_slice_q1_adm_residual_v001.py — c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a
- CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001.md — e5c7762d97fc6f2cd759cab4f303aa3a7463ab33e45001161d25bdf80c1ec440
- CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RESULT.json — 6c323ea0b01169c37c6c6c9960d7469ed57386148ff6022cc3d2bbc6da0b493b
- CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RECEIPT.json — 2919b4ab5715a7cff10a73836b6db65018520b234f65d1fb00f40c4581854f13
- cross_u_whole_slice_cauchy_data_v002.py — 6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7
- CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RESULT.json — af0365e378a46c727108c7df57f527994a22b7428d72b1f67c6f1bbac93667ed
- CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RECEIPT.json — 88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9
- cross_u_saved_full_native_adm_legendre_v002.py — 9185f2dcd981d7599023858dd8c533b13a510c150ad994b5ea3f569b947d9de0
- CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002_RECEIPT.json — 4a21c59742252d7fcaaccfd7b9371fa846bc1d248579ae9408a9838ae971b99e
- CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md — 087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523
- CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json — 3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c

The following actual sigma1 canonical column pairs fix every primitive/chart/point-star partition and point order. Their COMMIT metadata were read; no numerical payload was loaded.

- q0 CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00007_COLUMN.npz — 4bb27bb455e2e5ef78b73a05d63d28811c102f45e406635257ef6f534ca9e3bf; CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00007_COLUMN.npz.COMMIT.json — 96be68906712c7083cca956b6cbd99dea68ed9e02d1a6e1595c788e6819ffb66
- q1 CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00008_COLUMN.npz — d95ec4e4ee869d6f2ed018ad1b24268f0aef10c1f256b5f03a5d4f0ebfd938be; CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00008_COLUMN.npz.COMMIT.json — c4b6cece4f13caebc3e82f29073cad03c5bf42ccc706e219888aa05ec081fff4
- q2 CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00009_COLUMN.npz — b94fc8cd59dabc3ec4590f02d32f39622e5f16ffbce24cd4fefe21c8d2275c17; CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00009_COLUMN.npz.COMMIT.json — 2d43da93ff949739c85e0fd325b3b6b2bb4ec908bbd9daa70b18f3bc5a2a3b33
- q3 CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00010_COLUMN.npz — 6adb8b68019216ccb3bf30b050fb180990afb96382632b461b7b66993ea99f4f; CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00010_COLUMN.npz.COMMIT.json — bc2d50a304b0d262e53920122fe432fc215686c75abb33a854d561f08cb662f3
- q0 CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00008_COLUMN.npz — 55a3148feeb2180059e750be7ef5f1a42ded242d51a41293c1f09cf863ec41bb; CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00008_COLUMN.npz.COMMIT.json — f2a93550458a9d370c1ac6b38eb27445191999fe175d82f437c117124883b09e
- q1 CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00009_COLUMN.npz — 2beb7d7849465d4a713b73a2041aead672e97dd2979aa09990013cbf56ab9928; CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00009_COLUMN.npz.COMMIT.json — 65a26810e86ef7c056b2d667b34f43e6316071809ed1d0b42d361ff277386bb3
- q2 CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00010_COLUMN.npz — fec329f3a3037f22336bf8066a1146511027da84cea6ed38b09fc59711acc38d; CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00010_COLUMN.npz.COMMIT.json — e82c64d673f84e88af1e7b92a180d4c66579dae4a7f2aa02be54f0116444d432
- q3 CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00011_COLUMN.npz — 56761c8f1298bb6118f3292882f4d9c2660ed17c6593a8437cf8d0bd4dab23e5; CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_00011_COLUMN.npz.COMMIT.json — e48fb694699c4e8b9d4510cc324d98c63f12cdb425624e10a620be146ff7b8c5
