# EPS5 linear exterior, conserved transport and native clock admission V001

2026-10-06 UTC. AUTHOR_DRAFT=True. Guarded analytical continuation of the existing SAME uncompressed S_cross action, released for root and independent full review. No scientific function, background, mode, matrix, operator, clock, state, transport history or trajectory was evaluated. The closed temporal inventory is used only for its retained qualification and normalization scope. No inertia, preparation, shell, emission profile, extra birth budget, exterior force or physical boundary is selected.

## 1. Background and the retained linear variables

Use c_p=1, signature(-+++), M^2=(8pi Gbare)^-1, KB=.02, C=1.98 and g=M^2 C. The actual EPS1e-5 homogeneous member retains the full physical A,I0,Q0, ordinary inventory, Hunit67.49711988577813 and rG=.98/.99. Its background has Ubar=n_cos, phibar_dot=Qbar, a^3 nbar=I0, zbar_j=abar=Fbar=rbar=0, and the Friedmann/current equations of the junction note. No H(1) division, new abundance or old-action perturbation is imported.

For clarity use the comoving background chart and an orthonormal spatial coframe. D is its physical spatial derivative, Delta=D_i D_i, and a dot is cosmic proper time. Use Newtonian/Poisson gauge scalar potentials Phi,Psi; vector shift and tensor perturbations remain in the full Einstein equation below. Let u_i be the first-order physical tilt of the independent U relative to the ADM normal, V=delta phi/Qbar, d=delta nbar/nbar=delta rho_phi/W, W=Qbar nbar, s=W/(Qbar^2 P_XX), and

    A_i=delta a_U,i=dot u_i+H u_i+D_i Phi,
    Z_i=sum_j w_j z_j,i, P_i=M^2 KB A_i+g Z_i,
    r_i=delta(P_U dphi)_i=Qbar(u_i+D_i V).                  (1)

The unit-U equation fixes its temporal perturbation; each z_j is spatial in the background coframe. Scalar tilt u_i=-D_i pi gives A_i=D_i(Phi-dot pi), including dot D=-H D. Thus the scalar reduction of(1) reproduces V003 Eq(7), with its own canonical polarization. Tilt is not set equal to the phase velocity or to cosmic flow in the nonlinear interior.

## 2. Explicit exterior material equations in all three spatial components

The linear zero-background material rows are

    dot P_i+2H P_i=-M^2 KB(curl curl u)_i
                                  -g Qbar^2(u_i+D_i V),
    dot d=3dot Psi+Delta V+(g Qbar/nbar)D_i(u_i+D_i V),
    dot V=Phi+s(d+3H V),
    ddot z_j,i+3H dot z_j,i+omega_j^2(1-ell^2 Delta)z_j,i
                                                =omega_j^2 A_i. (2)

Here curl curl u=grad div u-Delta u; for a transverse Fourier coordinate it is +q^2 u, and for a longitudinal coordinate it vanishes. Every z_j and dot z_j is retained. The modal quadratic kinetic energy exists at zbar=0; its contribution to local energy is second order, which does not remove its linear Euler equation, acceleration contact or polarization density. The quartic derivative vanishes only in this exterior linearization. It remains literal in the finite interior action.

Covariantly the modal equation is -Tbar^*(omega_j^-2 Tbar z_j)+ell^2 Dbar^*Dbar z_j+z_j=Pbar_U delta a_U, with Tbar=Pbar_U nabla_Ubar and Dbar=Pbar_U Pbar_U nabla. In the parallel transported proper spatial coframe this is(2). Derivatives of the projectors/connection multiplying zbar,Tzbar,Dzbar vanish at first order. About a finite interior z, they do not vanish: delta(Tz) contains T delta z, delta U, delta connection and projector contacts, and the kinetic/gradient Hilbert variations contain the actual retained native momenta. The local potential classes are 1+|z|^2/k_j and 1+3|z|^2/k_j, not a replacement for these spatial/current contacts.

For transverse tilt u_T and Z_T, A_T=dot u_T+H u_T and dot P_T+2H P_T=-(M^2 KB q^2+g Qbar^2)u_T. At fixed ADM lapse with g_ti=a S_i and U_i=a u_i, the linear shift terms in a_U cancel. The restricted quadratic material action is independent of transverse S. This gives zero additional linear transverse Hilbert momentum only on the corresponding independent-U/mode equations with their reaction/pullback contacts retained; it is not an off-shell stress claim from imposing a chart. No stationary finite-interior odd-sector equation is removed by this exterior observation.

## 3. Explicit scalar gravity and the full metric continuation

On those material equations, the first-order sources measured by the ADM normal are

    delta E=delta rho_o+W d+D_i P_i,
    delta j_i=delta j_o,i-W D_i V,
    delta S_ij=delta S_o,ij+s W d delta_ij.                 (3)

The divergence is -q Ptot in the longitudinal convention of V003 Eq(8). Ordinary anisotropic stress is retained. Reconstruct the covariant stress using its background energy/pressure and the perturbed normal/projector; the background metric contacts are not deleted by displaying orthonormal components. The native kinetic energy does not become a new homogeneous population at this order.

For an explicitly cold ordinary component and massless collisionless radiation, the normalized scalar equations can be implemented directly. Put tau=Hstar t, h=H/Hstar, q=c_p k/(a Hstar), b=rho_b/(2M^2 Hstar^2), r=rho_r/(2M^2 Hstar^2), w=W/(2M^2 Hstar^2), p=Ptot/(2M^2 Hstar), Kbar=KB/2 and Cbar=C/2. In these variables

    n_U=(p-Cbar Z)/(Kbar q), dot pi=Phi-n_U,
    dot p=-2h p-Cbar Q^2 q(V-pi),
    dot d=3dot Psi-q^2[V+(Cbar Q^2/w)(V-pi)],
    dot V=Phi+s(d+3hV),
    dot z_j=v_j, dot v_j=-3h v_j-Omega_j^2(1+ellhat^2 q^2)z_j
                                                    +Omega_j^2 q n_U,
    dot delta_b=3dot Psi-q^2 u_b, dot u_b=Phi,
    dot F(mu)+iqmu F(mu)=4dot Psi-i4qmu Phi,
    E=b delta_b+r F0+w d-q p, Pi=r F0/3+s w d,
    S=b u_b+4r u_r/3+w V, u_r=3F1/(4q),
    dot Psi=S-h Phi, q^2(Psi-Phi)=2r F2,
    N=q^2 Psi+3h S+E=0, dot N+3h N=0.                    (4)

The full angular distribution or its exact retarded representation remains. These are the SAME equations with the actual EPS5 background; the saved EPS1e-6 manufactured preparations/trajectories are not EPS5 data. At q=0 use the un-divided homogeneous constraints. Cold matter/collisionless radiation is a disclosed exterior constitutive scope, not a plasma, primordial spectrum or actual galaxy-assembly certificate.

For other ordinary stress, vector/tensor components or a different gauge, the full linear metric equation is M^2 delta G_mu nu=delta T_mu nu with(3) and its actual ordinary sources. Its operator is explicit:

    delta Gamma^rho_mu nu=(gbar^rho sigma/2)
           [nablabar_mu h_nu sigma+nablabar_nu h_mu sigma
                                      -nablabar_sigma h_mu nu],
    delta R_mu nu=nablabar_rho delta Gamma^rho_mu nu
                                  -nablabar_nu delta Gamma^rho_mu rho,
    delta R=gbar^mu nu delta R_mu nu-h^mu nu Rbar_mu nu,
    delta G_mu nu=delta R_mu nu-h_mu nu Rbar/2-gbar_mu nu delta R/2. (5)

Here h_mu nu is the metric perturbation, not H/Hstar. Match a common gauge, keep normal/momentum constraints and the material equations, and supply the actual ordinary vector/tensor stress. Formula(5) does not choose an elliptic metric inverse, incoming gravitational data or lapse wall. The coupled characteristic symbol is built from(2),(5), current and ordinary transport modulo constraints; the isolated native front ell omega_j alone is not that symbol.

## 4. Moving interface fields, phase charge and characteristic momenta

For a spherical diagnostic tube the actual EPS5 background has Vb=Rbdot-HRb, s=gamma_b(Vb n_cos+e_R). Its nonzero background phase flux is Jbar.s=-gamma_b nbar Vb. At first order retain delta(s.J)=sbar.delta J+delta s.Jbar, with

    delta J_phi=delta nbar Ubar+nbar delta v_phi-g delta r,
    delta nbar=P_XX delta X, delta X=Qbar s d,
    delta J_sp=-nbar D V-g Qbar(u+D V).                   (6)

A metric/interface perturbation therefore changes the phase port even when native background momenta vanish. Charge excess evolves by the moving current balance; it is not an independently fitted interior charge profile.

The explicit native derivative ports linearized about this exterior are

    delta Pi_U^mu{}_nu=-M^2 KB delta F^mu{}_nu
                                         +g Ubar^mu delta Z_nu,
    delta Pi_zj^mu nu=g w_j[Ubar^mu(Tbar z_j)^nu/omega_j^2
                                         -ell^2(Dbar z_j)^mu nu]. (7)

For the spherical tube, its modal outward port is g w_j gamma_b[-Vb dot z_j/omega_j^2-ell^2 D_R z_j], in the common proper spatial frame. Match admitted field pullbacks, phase flux and these momenta; match the induced metric/extrinsic curvature and complete material connection ports, with the same ordinary traction/Ward balance. The nonlinear interior uses its FULL versions of these momenta. No extra shell, independent outer traction, artificial zero cosmic flux or imposed comoving interior U is introduced.

## 5. A finite matching operator that retains incoming history

Choose an actual exterior discretization/gauge and spatial multipoles after physical registration. A constraint-compatible finite realization of(2),(4),(5) with the admitted ordinary transport has a retained state Y containing native positions/momenta, phase/U coordinates, metric data and ordinary radiation/transport. Its boundary lifting b_Sigma and flux p_Sigma can be written

    dot Y=A_E(t)Y+B_E(t)b_Sigma(t),
    p_Sigma=C_E(t)Y+D_E(t)b_Sigma(t),
    p_Sigma(t)=C_E(t)U_E(t,t_i)Y_i+D_E(t)b_Sigma(t)
              +integral_ti^t C_E(t)U_E(t,s)B_E(s)b_Sigma(s)ds. (8)

U_E is the time-ordered propagator of the retained equations. The matrices are their variational discretization, not fitted response coefficients. Gauge constraints, moving-interface geometry/ports and the chosen lifting must be retained; an algebraic constrained realization uses its corresponding DAE propagator rather than discarding constraints to obtain(8). This is a usable finite causal boundary operator once its actual incoming/initial state and exterior registration are given. None has been assembled/evaluated here. Y_i or a no-independent-incoming condition is physical information, not a zero initial guess or a stationary omega rescaling. Native initial velocities are required even at zero homogeneous field.

## 6. Active ordinary emission supplies stress and transport, not a second budget

The current S_o is metric-minimal. Its complete ordinary stress is conserved; stellar/gas/photon emission can redistribute that SAME inventory. A resolved radiation equation has p^mu nabla_mu f=C_emission+ C_absorption+ C_scattering, with its reservoir losses and all momenta included in the ordinary sum. In particular sum_species integral p^nu C_species dP=0 for an internal ordinary transfer. The resulting energy, flux, pressure and anisotropic stress enter(3)-(5) and their interface ports. A cold circular surface-density slice does not contain this full emission/assembly history.

If a physically registered microscopic interaction exchanges ordinary, record, phase or native energy, its SAME interaction action fixes equal/opposite Q^nu exchange terms and any actual phase-charge source. Total stress/Ward and conserved carrier charge remain accounted once. Merely observing record formation does not add a phenomenological J_phi, identify record count with carrier N_c, or supply an independent birth energy reservoir. An emission/SFR profile is not a derived force law. The proper full phase/current/Hilbert registration in the accepted matching note remains necessary.

## 7. Necessary temporal-normalization admission before a physical history

The static calibration fixes g,gc,ell and the normalized weights, not omega_j. The completed curvature inventory retains four conditional omega_j=sigma xi_j Hstar families and all physical inertia/history flags false. A concrete missing admission is the causal response of a REGISTERED source-conjugate microscopic operator B to the SAME acceleration source, on an actual passive state and physical volume. For a stationary diagonal state, with physical energy gaps Delta_nm=E_n-E_m and source Hamiltonian H-a B, its positive-gap representation is

    chi_B(lambda)=sum_m<n 2(p_m-p_n)Delta_nm |B_mn|^2
                                     /[Delta_nm^2+(hbar lambda)^2],
    chi_B(0)=sum 2(p_m-p_n)|B_mn|^2/Delta_nm,
    chi_B,2=sum 2(p_m-p_n)hbar^2|B_mn|^2/Delta_nm^3.        (9)

chi_B(lambda)=chi_B(0)-lambda^2 chi_B,2+... requires the admitted gap/window and finite moments. Passivity, degeneracies, source-held contacts, moving-volume/normal work and incoming complement forcing cannot be inferred from a static graph coefficient. For the actual registration B/V=g Z the target normalized response is chi_B/(g V)=sum_j w_j/[1+ell^2 k^2+lambda^2/omega_j^2]. Consequently at k=0 a necessary temporal moment match is

    chi_B,2/chi_B(0)=(sum_j w_j/omega_j^2)/(sum_j w_j),
    omega_j=sigma xi_j Hstar =>
    sigma^2=(sum_j w_j/xi_j^2)
               /[Hstar^2(sum_j w_j)(chi_B,2/chi_B(0))].    (10)

Equation(10) is an admission identity, not an adopted sigma or a computed microscopic response. A finite quadrature is not a physical infrared cutoff: w(xi)=2xi and omega proportional xi have a logarithmically divergent zero-frequency second moment as xi approaches0, so the finite32 moment cannot be claimed as a continuum clock theorem. Retain the finite-frequency kernel or an independently supplied physical window/cutoff if that limit matters.

The actual next physical task is to register B, the proper coframe/volume, physical Eunit/hbar clock, one phase-charge dictionary and the complete count/Maxwell/native/support allocation, then compare its finite source response and moment/window with(9),(10) on the SAME member. Static force, a passive TEM cycle or an assumed prepared ramp does not furnish that identification. Once admitted, that inertia and the conserved ordinary emission/current history supply(8); until then the benchmark exterior operator is conditional. No new vacuum offset, mode population, damping, formation age or favorable response is earned.

## Actual read-only input seals

These relative J paths were read/hashed before exclusive authoring. Inputs and their modes are unchanged; no producer/helper was imported or executed.

| Input | SHA256 |
|---|---|
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md | c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986 |
| CROSS_U_EPS5_FLRW_GALAXY_JUNCTION_V001.md | baa25990f0b2d4ca925e1a74fb65b40c2968890bd552e9f64541e620e07c6965 |
| CROSS_U_NATIVE_RETARDED_RESPONSE_AND_STATIONARY_HISTORY_V001.md | 662a0eb290057bf0d7f5160e64c38edf17257b4073c1b07f4fa15ef1e1c710c7 |
| NATIVE_TO_CROSS_PHASE_COEFFICIENT_CURRENT_AND_STRESS_MATCHING_V001.md | d95ad4155144f102243e14082faf1e5b6b7b193eef0c753c88864534ec302d40 |
| CROSS_U_GENERAL_METRIC_ORBIT_AND_FLRW_TIME_DEPENDENCE_V001.md | b3fd1355c03ed78cb702844cb05e34accb9e51d648d89c21db1bafd47dfcef59 |
| CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json | 3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c |
| CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001.md | f511db085e290e3287902e20f9e0eb9cf2679febc4a9af01061f30f10068645b |
| CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_RESULT.json | 1f00f801492401811f5c39790e43e8b07379362f02698f12a9d29e45374dfdd9 |
| CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_RECEIPT.json | ebe0d2051f46349cc16f0b6cb4d918131c4a9f85e16e26bba96eafcd3ae9c660 |

AUTHOR_DRAFT=True remains in force. Root/peer full mathematical review is required before sealing; no numerical exterior or physical inertia has been adopted.
