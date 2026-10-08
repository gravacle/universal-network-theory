# Same-action spherical baryon-isocurvature Cauchy contract V001

2026-10-06 UTC. STATIC initial-state construction for the owned nonlinear spherical S_dual/ADM system. No field, background helper, inverse, coefficient, constraint solve or trajectory is evaluated. The calibrated pressure, absolute reference, ordinary inventory, one Gbare and all native modes remain. This is one exposed baryon-isocurvature preparation, not the cosmological adiabatic growing state or an observed galaxy fit. Numerical epoch, amplitude, scale, radial domain and duration must be declared before results.

## 1. Physical inputs and a regular compensated spatial geometry

Select one admitted spatially flat homogeneous FLRW state of the SAME action at t_i: Hbar>0, Qbar in [Q0,Qcap), nbar=P_X(Qbar)>0, rho_bbar>0 and the actual remaining ordinary background. Its total source includes e_phi=nbar*Qbar-P(Qbar) with the retained absolute reference and obeys 3M²Hbar²=rho_totalbar. This fixes phase charge from the calibrated I0; no new dark abundance is assigned. Use c_p=1, geometric densities, and factored4pi conventions of the ADM proof.
Let A_b>0 and R_c>0 be the PREDECLARED baryon contrast amplitude and initial areal length. Define x=r²/R_c² and
    delta rho_b=A_b*rho_bbar*(1-x/3)*exp(-x/2),
    u(r)=L_i(r)^(-2)=1-[A_b*rho_bbar/(3M²)]*r²*exp(-x/2).             (1)
The actual initial baryon density is rho_bbar+delta rho_b. The central overdensity and compensating outer underdensity are one fixed profile, not independently fitted source pieces. Its areal constraint mass satisfies
    r²*delta rho_b=M²*partial_r[r(1-u)],
    integral_0^infinity r²*delta rho_b dr=0.                            (2)
Since (1-x/3)exp(-x/2) has its minimum -(2/3)exp(-5/2) at x=5, strict positive baryon density follows from A_b<(3/2)exp(5/2). Since r²exp(-x/2) has maximum 2R_c²/e, the complete nondegenerate spatial metric condition is
    2*A_b*rho_bbar*R_c²/(3e M²)<1.                                    (3)
These are analytic domain bounds, not selected numerical amplitudes or outcome gates. At the centre L_i=1+A_b*rho_bbar*r²/(6M²)+O(r^4); at infinity L_i->1 exponentially. Both constraints and all angular vector terms use their regular weighted centre limits.

## 2. Complete initial fields, momenta and gravitational constraints

Initially choose synchronous gauge N_i=1, beta_i=0, R_i=r and k_L,i=k_R,i=Hbar. Thus R_dot_i=Hbar*r and L_dot_i=Hbar*L_i. The radial coordinate labels this initial areal slice; it is thereafter a comoving gauge coordinate, not a permanently fixed areal radius. The asymptotic homogeneous solution has R=(a/a_i)r and L=a/a_i. In the conventional K_ij=-Hbar gamma_ij notation the extrinsic curvature is uniform and isotropic.
Set phi_i spatially constant, q_phi,i=Qbar, p_phi,i=0, chi_i=0, A_U,i=0, every z_j,i=0 and U z_j,i=0. All physical radial mode/multiplier fields are regular and vanish initially. Give the single pressureless baryon stream u_b,i=n_ADM, rest density rho_bbar+delta rho_b and zero radial momentum; equivalently its owned dust velocity potential has psi_b,i constant and q_psi_b,i=1. Ordinary radiation/neutrino fields initially retain their actual homogeneous isotropic source and zero radial momentum. Their subsequent transport and exchange are included once where applicable, rather than prescribing the initial source profile for all time.
The initial material canonical state per factored4pi is
    Pi_phi,i=L_i*r²*nbar, Pi_chi,i=0, Pi_j,i=0,
    P_L,i=P_L,i^g=-2M²*r²*Hbar,
    P_R,i=P_R,i^g=-4M²*L_i*r*Hbar.                                  (4)
The material metric-momentum shifts vanish at this initial state, although they must be retained subsequently. The lapse, shift and sigma primary momenta vanish. Dust rest charge density is L_i*r²*(rho_bbar+delta rho_b); its source and current evolve by the actual dust continuity and geodesic equations before shell crossing.
The mode/acceleration/reaction energy and momentum vanish initially, so rho_i=rho_totalbar+delta rho_b and j_i=0. For R_i=r, the exact three-curvature is 2[partial_r(r(1-u))]/r². Equations(1)-(2) therefore imply
    (3-curvature)_i=2*delta rho_b/M²,
    M²[(3-curvature)_i/2+3Hbar²]=rho_i,
    H_r,i=0.                                                        (5)
The last equality follows from uniform Hbar and zero total material momentum, including the complete phase current. It is not a constraint solved by inserting a phase-density profile. Absolute background pressure remains in the initial metric evolution and is not reset by (5).
For as long as synchronous N=1,beta=0 is a regular dust-comoving gauge, u_b=n_ADM remains geodesic and the exact source law is rho_b(t,r)*L(t,r)*R(t,r)²=[rho_bbar+delta rho_b(r)]*L_i(r)*r². Thus the ordinary density changes with the solved proper-volume Jacobian; keeping its initial radial profile fixed in time would violate the source equation. A particle-label caustic, rather than a repaired density prescription, ends this single-stream description.

## 3. Multiplier consistency and the first evolution tangent

The holonomic constraint Z=Ephi is initially zero. The exact kinematic identity U(Ephi)=E(Q)+Q*A_U-K_U*(Ephi) gives its first tangent zero, because E(Qbar)=A_U=0. Phase continuity gives U n=-3Hbar*nbar and U Q=-3Hbar*c_s²(Qbar)*Qbar, spatially uniform on this slice. Thus the radial derivative of the first phase evolution is also zero initially.
To obtain the initial reaction rather than assign it freely, let alpha_omega=sum_j w_j*omega_j²>0 with the actual inherited positive regulator. At the zero-mode state the mode equation gives U²Z=alpha_omega*sigma, while the independent rapidity row gives U A_U=-(C/KB)*Qbar*sigma. The second constraint tangent U²(Ephi)=Qbar*U A_U therefore gives
    [alpha_omega+C*Qbar²/KB]*sigma_i=0,
    sigma_i=0, U A_U,i=0.                                           (6)
All quartic, spatial-mode and angular-gradient contacts vanish at this zero-mode state. Their subsequent variations do not vanish by assumption. The positive coefficient in (6) establishes the initial reaction on this slice; it is not a nonlinear reaction inverse, a proof of all higher consistency jets, or an invariant zero-mode branch in the inhomogeneous geometry. Einstein evolution can generate spatially varying expansion, followed by phase gradients, U tilt, modes and reaction. Full constraint preservation must be tested with the actual first-order system.

## 4. The proper charges are NOT compensated

The homogeneous phase density on the curved slice has finite positive excess over the flat background measure:
    Delta C_phi=4pi*nbar*integral_0^infinity r²*(L_i-1)dr>0.           (7)
This is part of the declared Cauchy state, not an independently added halo. It cannot be called zero excess phase charge merely because (2) vanishes. Likewise the ordinary rest charge is
    Delta C_b=4pi*integral r²*[L_i*(rho_bbar+delta rho_b)-rho_bbar]dr
       =4pi{rho_bbar*integral r²*(L_i-1)dr
             +M²*integral[u^(-1/2)+u^(1/2)-2]dr}>0.                  (8)
The second equality follows by integration by parts in (2); the endpoint term r*(sqrt(u)-1) vanishes. Its integrand is (1-sqrt(u))²/sqrt(u). Areal gravitational compensation and proper conserved charge are different observables. Requiring zero proper phase/baryon excess would be a different physical preparation requiring jointly revised fields/geometry and a new constraint solve, not a routine normalization correction.
At finite moving worldtubes record both actual enclosed charges and their reference subtraction, and use the exact flux NLR²(J^r-r_b_dot J^t). Initially the total phase and baryon currents are normal; comoving flux vanishes at that instant. A fixed-areal worldtube has the cosmological advective flux. Subsequent relative currents and source work are computed. Conservation concerns the complete actual charge/stress and its moving-boundary flux, not a fixed comoving-density picture.

## 5. A bounded first numerical discriminator

This contract fixes a Cauchy seed, not a force profile or an imposed assembly history. Freeze actual t_i/A_b/R_c, the finite positive mode regulator and noncharacteristic branch, radial grids/refinements, outer characteristic treatment and a finite proper duration before an implementation run. Ages and incoming data must follow that declaration, without choosing them from a favorable force curve. Initially uniform phase/native fields are an isocurvature hypothesis; they are not inferred from the earlier single-k adiabatic history or microscopic photon preparation.
First test (1)-(6), centre/asymptotic limits, the full canonical/Hilbert sources, charge excesses(7)-(8), and zero-perturbation charged FLRW using the independently fixed action. Then evolve the baryon stream and ALL phase/U/modes/reactions/gravity together, monitoring both Einstein constraints, multiplier/tangent, radial/angular Ward work, total-current flux and numerical refinement. Stop the pressureless source at shell crossing, loss of the admitted phase/noncharacteristic domain or a constraint inconsistency; no invented support pressure or late density reset is supplied. A supported mature galaxy requires its actual material stress beyond this seed test.
The Gaussian has no finite exact vacuum/FLRW matching wall. On the infinite domain it is asymptotically matched; at a finite numerical boundary retain its nonzero tail and the computed asymptotic incoming/constraint data, or disclose a separate jointly solved compact compensation construction. Imposing all fields homogeneous at an arbitrary finite cutoff changes this Cauchy state. Finite-domain charge and stress-tail errors must be stated. No full nonlinear well-posedness, microscopic matching, thermal/primordial origin, observed galaxy success or current failed-gate promotion follows from this contract.

## Actual source inputs

| Input relative to J | SHA256 |
|---|---|
| CONSTRAINED_U_SPHERICAL_ADM_SOURCES_AND_CANONICAL_EVOLUTION_V001.md | cafaff537e994e1c71f24f3786f5f74850de689837012e147c011ad8356b5e1a |
| CONSTRAINED_U_SPHERICAL_FLRW_CURRENT_MODE_AND_HILBERT_SYSTEM_V001.md | 110b2f23ae79c808090f79c60655b7c64c7b38e2edd7773e6aa4965ed4e399b1 |
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| CONSTRAINED_U_GALAXY_WORLDTUBE_AND_STATIC_BOUNDARY_DISCRIMINATOR_V002.md | a7598cc79c7e3bdaa83ad31f32826e7cf439b0f28c6f79fda9a09ea98c5ab90b |
