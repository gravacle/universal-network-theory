# Weak nodal native Legendre map and basis registration V001

AUTHOR_DRAFT=True. Root-requested analytical extension, held for FULL review. No scientific array, producer, helper, operator, Gram, inverse, eigenproblem, solve or evolution is evaluated. This registers a finite instantaneous velocity map of the same EPS1e-5 action, KB=.02, C=1.98, ell=.1kpc, original32 modes and four conditional sigma arms. A first executable compatibility test may use the predeclared sigma1 member; it cannot select physical inertia or a galaxy solution.

## 1. Fixed quadrature, constrained chart and new temporal basis

Use the authentic87x45 coordinate grid,86x44 cells and four existing Q2 columns,15,136 points in total. Copy the actual corner hats, cell indices, R_q and dv_q=R_q dR dZ weights from the CLOSED whole-slice geometry. No quadrature replacement, mass lumping, reflected factor2 or additional2pi is introduced. Coordinate canonical densities already contain sqrt(-g), including cylindrical R. Their weak contraction therefore uses omega_q=dv_q/R_q exactly once. R_q>0; no cylindrical inverse is evaluated at an axis node.

The independent native configuration is the accepted spatial-covector chart u_i=U_i and all z_ji, i=(R,Z,phi). U0,Ui and z_j0 are rebuilt by chart(1) of the canonical companion, with all unit/transverse and metric-chain contacts. All three components of every mode remain: initial z_jphi=0 does not set its velocity or conjugate momentum to zero. Native U is independent of ordinary rotating u_M and of the phase.

Register fixed coordinate temporal basis maps E_U(q), E_j(q) from nodal coefficients to the three spatial covector velocities. R and Z components use genuine bilinear hats; at R=0 impose radial value0 and tie the even Z coefficient node0 to node1. At Z=0 the Z component is odd/value0, while R and phi are even. The azimuthal COVECTOR uses R^2 times an axis-even bilinear coefficient, whose axis node0 is tied to node1. This is the regular first-cell representation of R^2 dphi=x dy-y dx, rather than the axis-even scalar beta^phi basis of Q1's shift tests. Its derivative is 2R N+R^2 N_R, not R^2 N_R alone.

These are explicit prospective temporal approximation spaces. The old65-field mask only enforced radial-axis0 and Z-sheet0 (old core lines103--105); it did not tie the old Z-axis configuration. No immutable configuration is overwritten or retroactively claimed to satisfy the new temporal tie. At the test instant use the affine chart q_native(x,t)=q_seed(x)+E(x)a(t), a(t0)=0; the frozen seed is an exact offset, and E is fixed while differentiating. Thus the finite map below is the actual derivative of this restricted instantaneous action, not a relabeling of old pointwise velocities as nodal coefficients. Full Cartesian smoothness beyond the registered axis approximation is not inferred.

Retain outer temporal coefficients as independent unknowns for this kinetic mass map. A seed configuration's finite wall value is not a physical future velocity trace. This mass solve has no spatial derivative of its velocity unknown, hence requires no exterior Dirichlet data for mathematical invertibility. If a later branch keeps a wall for an interval, its time trace must be supplied and the basis/RHS explicitly reduced before execution. No unknown exterior state is set to zero. With this registration one three-component block has11,524 coefficients and all33 native blocks have380,292; the matrices remain sparse or matrix-free, not dense380,292-square arrays.

## 2. Complete fixed-metric kinetic block

At fixed configurations, spatial jets, N,beta,h and their prescribed time jets, let v=(v_U,v_j) be the99 native coordinate velocities. The accepted chart gives S=[Jzz;I_3], T_j=P_.^0 JzU_j and T_j=S L_j, with

    L_j,ki=P_k^0 JzU_ji=u_k U0 JzU_ji,
    kappa_j=(U0)^2/omega_j^2-ell^2 P^{00}>0,
    D_j=sqrt(-g) w_j kappa_j S^T g^-1 S,
    M0=sqrt(-g) (KB/C) h^-1/N^2,
    L_kin=1/2 v_U^T M0 v_U
             +1/2 sum_j(v_j+L_j v_U)^T D_j(v_j+L_j v_U). (1)

L_j is not JzU_j alone. The negative projected-spatial-gradient velocity contribution is retained in kappa_j, not dropped. Positivity here is conditional on its strict actual native-cone gate, positive original w_j, N and spatial metric. Acceleration.Z is affine in native velocity and remains in the baseline momentum. Relative phase and quartic potential have no99 velocity Hessian but their configuration/Euler forces remain. This fixed-metric99 result does not assert positivity of the full105 native/metric Hessian or eliminate the accepted tilted-gradient metric-Schur term.

Let p_star(q),v_star(q) be the authoritative CLOSED Q1 owned-H native density and chart velocity at each point. Its fixed metric/time jets include the disclosed hdot increment2N Hbar h. Since the native map is affine at this fixed instant,

    p(q;v)=p_star(q)+M(q)[v-v_star(q)].                    (2)

Using(2) avoids reconstructing completed105 Grams or repeating the old affine/connection solve. The parent target p_target is its immutable stationary native canonical density; its equality to p_star is a stored certified parent fact, not a new assumption that the whole physical history is stationary. Save both densities, the velocity, implicit baseline p_star-M v_star and each uncancelled contraction envelope before refusal. Do not replace a pointwise density with a nodal load without applying the adjoint basis.

## 3. Genuine weak map and the projection remainder

Using the same evaluation maps E for configurations and velocities, form

    p_h=sum_q omega_q E(q)^T p_target(q),
    r_h=sum_q omega_q E(q)^T
                         [p_target-p_star+M v_star],
    M_h=sum_q omega_q E(q)^T M(q) E(q), M_h v_h=r_h.        (3)

Each modal diagonal block D_jh=sum omega E_j^T D_j E_j is SPD on the independent axis/reflection basis. Genuine2x2 Gauss evaluation of a nonzero bilinear field is injective per cell; multiplying the azimuthal basis by positive R_q^2 preserves that rank. Positive point blocks and positive weights then prove the global native map is SPD, without an empirical positive-eigenvalue fit. Axis identifications are applied by a lift and its exact adjoint; no redundant constrained node is kept as a zero pivot.

Write A_h=sum omega E_U^T(M0+sum L_j^T D_j L_j)E_U and B_jh=sum omega E_U^T L_j^T D_j E_j. The exact native reduction is

    S_Uh=A_h-sum_j B_jh D_jh^-1 B_jh^T,
    v_Uh=S_Uh^-1(r_U-sum_j B_jh D_jh^-1 r_j),
    v_jh=D_jh^-1(r_j-B_jh^T v_Uh).                       (4)

The pointwise Maxwell-only arrowhead is NOT a valid substitute for(4). For every nodal u,

    u^T(S_Uh-M0h)u
       =sum_j min_z sum_q omega_q
          ||E_j(q)z+L_j(q)E_U(q)u||^2_Dj >=0,
    M0h=sum_q omega_q E_U^T M0 E_U.                       (5)

This is the discrete projection remainder. It vanishes only if the coefficient-multiplied U field lies in each modal basis range; spatially varying L and the component/parity spaces do not generally preserve that range. A constant-L cancellation fixture is admissible only when its spaces are explicitly closed under that L. Save the signed original weak actions and the nonnegative quadratic remainder with its independent minimizer/residual certificate; do not discard it because local arrowhead certificates passed. This statement concerns native99 at fixed metric; the full discrete metric Schur T_h-B_h^T M_h^-1 B_h also remains nonlocal and generally signed.

## 4. Bounded executable implementation and earned result

The next guarded producer can assemble only the sparse block mass entries, or their quadrature evaluation/scatter actions, for the predeclared sigma1 trial. Admit the CLOSED Q1 owner/maps and exact four COLUMN schemas after natural closure. Reuse its authoritative chart old_velocity, native densities, metric time jet and primitive coefficients; reconstruct only the finite matrix coefficients and new nodal operations. Keep every original32 frequency/node/weight and source parent, with the unchanged geometric clock. Preserve the Q1 producer and all old refusals.

Solve32 modal SPD mass systems and the exact U Schur(4), using positive Maxwell/block-mass preconditioning solely for arithmetic. A matrix-free full-native solve with the SAME original M_h is an alternative implementation, provided its recovered modal equations and projection remainder are independently certified. Predeclare finite iteration caps and original weak residual tolerance in the numerical protocol; retain incomplete iterates, residuals and every available operand on refusal. No jitter, clipping, pseudoinverse, diagonal replacement of M_h or favorable residual sign is permitted. A failed cap is a failed finite-map outcome, not a physical exclusion.

Independent controls must cover lift/adjoint and quadrature measure, scatter versus independently assembled sparse action, symmetry, manufactured nodal action/recovery, a range-closed constant-L case, a varying-L nonzero projection-remainder case, and the actual original99 weak equations. Save M_h v_h-r_h against uncancelled operation envelopes and a true norm gate; save the pointwise defect p_star+M(E v_h-v_star)-p_target and its weak orthogonality separately. Nodal velocity value/gradient and original momentum projections are new readouts. Their nonzero pointwise defect is a measured approximation consequence, not silently repaired momentum data.

The fixed metric time jet is a supplied L2 forcing in this first native projection. hdot=2N Hbar h is not automatically a nodal metric velocity, because its factors are spatially varying; phase velocity/current and ordinary mass/p_i remain their separate canonical blocks. At this unchanged instantaneous metric the native mass projection does not alter the phase or ordinary configuration/momenta. A subsequent joint nodal metric/phase evolution must project all their temporal maps and rebuild the complete spatial force/constraint/CMC rows from these velocities, rather than reuse old pointwise source rows as an evolved solution. This is the shortest finite bridge to the accepted CMC extension's actual fifth row.

Unknown local cosmic-ordinary allocation, photon/native incoming state, physical preparation, paired time/exterior ports and metric/current/extrinsic worldtube matching remain explicit. The mass solve needs none of those to test this conditional instantaneous map, but earns none of them. Activity outside0.3--15.1kpc remains undefined; that radius is not a galaxy edge. No new source, inertia, SFR gain, pressure subtraction or exterior extension is selected. No full metric or exact-geodesic galaxy velocity is predicted.

## Actual static input seals

Paths are relative to J; every input below was0444 and hashed before exclusive creation. The Q1 numerical receipt is pending natural closure and is not bound to live outputs here.

- CROSS_U_FULL_CANONICAL_CMC_PRESERVATION_EXTENSION_V001.md — 60a222d80500b01771092919ede0d1374969ee769471964aec911929aad9e424
- CROSS_U_CONSTRAINED_CANONICAL_CHART_AND_CMC_ADMISSION_V001.md — 872ca230d040bfca08ac127c117e741e81549a4316e62dd5de8df8e8732f7e98
- reviewed_cross_u_whole_slice_q1_adm_residual_v001_1001_3338e243.py — 3338e243e9f5365e47cd2f4a150c425cc4240fe01575994b0e9b1d8584e7ff03
- CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001.md — e5c7762d97fc6f2cd759cab4f303aa3a7463ab33e45001161d25bdf80c1ec440
- cross_u_ngc3198_nonlinear_disk_v001.py — ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1
- CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RECEIPT.json — 88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9
- CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md — 087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523
- CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001_RECEIPT.json — f24459d3dfffbfd773323ba69c375ac8f08bda5e121d2f530dc156c1955fb6d7
