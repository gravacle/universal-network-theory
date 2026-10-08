# Nonlinear native flow and circular acceleration: same S_cross V001

2026-10-06 UTC. AUTHOR_DRAFT=True; root and distinct FULL review required. NEW explicit nonlinear independent-U projector row and exact circular-flow consistency test of the adopted uncompressed macro action. No array, field, coefficient, operator, helper, source, state, trajectory or numerical function is evaluated. EPS1e-5, the registered pressure/source normalization, all32 modes and all four conditional inertia labels remain unchanged. This does not add an activity force or select U, a Cauchy state or a history.

## 1. Actual macro calibration and complete held-variable action

Use signature(-+++), c_p=1, k=M^2 KB, g=M^2 C, KB=.02,C=1.98 and the once-only Gbare/GN=.99 matching. For independent contravariant U and independent covector modes z_j, write P_mu^nu=delta_mu^nu+U_mu U^nu, Q_U=U.dphi, r=P dphi, X=sqrt(-dphi^2), a_U=nabla_U U,

    q_j,nu=U^alpha nabla_alpha z_j,nu, V_j=P q_j,
    D_j,mu nu=P_mu^alpha P_nu^beta nabla_alpha z_j,beta,
    Z=sum_j w_j z_j, f_j=1+z_j^2/k_j,
    L=-k F^2/4-g r^2/2+P(X)
       +g sum_j w_j[V_j^2/(2omega_j^2)-z_j^2/2
              -(z_j^2)^2/(4k_j)-ell^2 D_j^2/2+a_U.z_j],
    L_con=lambda(U^2+1)/2+sum_j mu_j U.z_j.                 (1)

F=2nabla_[mu U_nu]. The EH term M^2R/2 and the complete ordinary action are retained. The literal off-unit projector is varied first; unit/transverse reactions are solved afterward. In kpc geometric coordinates k_j=(B0 GC)^2 xi_j^4, B0=a0 L0/c_p^2, GC=3pi/8, ell=.1; the code's weighted components are sqrt(w_j) times its unweighted mode. Equations below use physical unweighted covectors, not the code's scaled array entries.

The macro pressure scale is owned: full-slice89 and the closed common four-EPS parent fix Q0/Hstar=100 and Hunit=67.49711988577813 km/s/Mpc. Thus eta=HstarSI L0/c_p=Hunit/c_pSI for L0=1kpc and the physical geometric field is Q_background*=100 eta q_norm, where q_norm=Qphysical/Q0 is the SAME EPS5 background's normalized clock. Also H*=eta h and D_t Q_background*=-3H*cs^2 Q_background*. No Q=1 or fiducial EPS1e-6 q history is substituted. The quantum Eunit/proper-clock mapping remains a different matching question, not a missing macro Q0 calibration.

On the admitted charged branch, q=X/Q0, s=(q^2-1)/(eps-q^2+1), N_eps=eps^-1-log(1+eps^-1), P=A[(log(1+s)-s/(1+s))/N_eps-1] and P_X=(A/Q0)2q s/(eps N_eps). The same absolute A and ordinary inventory are retained. The nonlinear domain and charge/normal constraints must be enforced; changing U does not change X at held metric/phase. Older narrower-EPS stationary failures do not establish an EPS5 domain failure.

## 2. Explicit native mode, phase and independent-U equations

At the unit/transverse constraint surface, the actual mode derivative momentum and complete off-shell mode equation are

    Pi_j^alpha beta=g w_j[U^alpha V_j^beta/omega_j^2
                                           -ell^2 D_j^alpha beta],
    E_j^beta=g w_j(a_U^beta-f_j z_j^beta)
                               -nabla_alpha Pi_j^alpha beta,
    E_j^beta+mu_j U^beta=0, U.z_j=0,
    mu_j=U_beta E_j^beta.                                 (2)

Projecting (2) gives the accepted exact adjoint wave equation; the normal contraction gives its ACTUAL reaction, not an arbitrary zero. Its covariant connections, moving projectors, expansion, nonlinear quartic and spatial ports remain. No stationary Tz=0 restriction is made. With fixed local U/coframe it reduces to z_j,tt/omega_j^2-ell^2 Delta_vec z_j+f_j z_j=a_U, but that imposed-source reduction is not the coupled galaxy solution.

Define the following algebraic mode vertex by variation at held covectors and metric:

    A_j,rho=g w_j{omega_j^-2[V_j^nu nabla_rho z_j,nu
                                     +(U.q_j)V_j,rho]
       -ell^2[D_j,rho nu V_j^nu
                         +D_j,mu rho U^nu nabla_mu z_j,nu]}.

Then the full independent-U equation and its momentum are

    Pi_U^alpha_rho=-k F^alpha_rho+g U^alpha Z_rho,
    W0_rho=k nabla_alpha F^alpha_rho
       -g[Q_U r_rho+(U.r)partial_rho phi]
       +g Z_nu nabla_rho U^nu-nabla_alpha(g U^alpha Z_rho)
       +sum_j A_j,rho,
    0=W_rho=W0_rho+lambda U_rho+sum_j mu_j z_j,rho,
    U^2=-1, lambda=U^rho W0_rho.                           (3)

The last expression is the normal-contraction solution, evaluated from W0; it is not an independently supplied multiplier law. The projected equation P W=0 still includes the mu_j z_j reactions. Only AFTER variation may one use U.q_j=-a_U.z_j and U^nu nabla_mu z_j,nu=-z_j,nu nabla_mu U^nu. The two projector terms in A_j are consequently not deleted by holding a proper spatial mode chart. Neither mode projection supplies an additional explicit nabla U momentum in (3).

The physical phase row is independently

    nabla_mu J_phi^mu=0,
    J_phi^mu=P_X v_phi^mu-g P^mu_nu r^nu,
    v_phi=-raised(dphi)/X; on U^2=-1, J_phi=P_X v_phi-g r.   (4)

P(X) has no direct U Euler derivative. No ordinary enthalpy anchor, S_dual holonomy, record-birth source or extra matter current replaces (3),(4). The phase and native energies exchange through their complete Hilbert/constraint sources; ordinary matter is minimally coupled to that SAME metric and satisfies its own Euler/kinetic equations, independently of U.

## 3. Exact circular-Killing acceleration, including differential rotation

The ordinary circular geodesic force formula is already owned by orbit96; no new orbit law is claimed. Here it is applied to the independent native U and compared with its NEW explicit nonlinear source row (3).

Let K=partial_t and M=partial_phi be commuting stationary/axisymmetric Killing vectors. A circular timelike native flow has U=(K+Omega_U(x^A)M)/sqrt(D), D=-g(K+Omega_U M,K+Omega_U M)>0 and U^A=0. Its exact covariant meridional acceleration is

    a_U,A=-(partial_A g_tt+2Omega_U partial_A g_tphi
                    +Omega_U^2 partial_A g_phiphi)/(2D)
           =(partial_A D)_held_Omega/(2D),
    a_U,t=a_U,phi=0.                                      (5)

No derivative of Omega_U enters this FORCE partial: U.partial Omega_U=0 along a circular orbit even when the neighboring circles rotate differentially. A total spatial derivative of D would require subtracting D_,Omega partial_A Omega_U; replacing the held partial by that total derivative is wrong. Differential rotation DOES enter F, mode transport and the independent-U equation (3).

For the circular metric ds^2=-N^2dt^2+h_AB dx^A dx^B+rho^2(dphi+beta dt)^2, set v_U=rho(Omega_U+beta)/N=tanh chi. With a=D lnN,b=D lnrho,t=(rho/N)D beta, (5) is precisely

    a_U=cosh^2(chi)a-sinh^2(chi)b
                               -cosh(chi)sinh(chi)t.       (6)

Geodesic U requires the full meridional vector a-v_U^2 b-v_U t=0, not merely one Newtonian radial estimate. Cold ordinary material on an exact circular geodesic can rotate while its proper acceleration is ZERO. Thus identifying the native U with that u_M would remove the direct a_U driving in (2), rather than create a source v_obs^2/R. Neither that identification nor geodesic U follows from (1). The ADM normal instead has a_n=D lnN; its proposed alignment must satisfy the same independent-U row, including the accepted odd94 Eq(6) forcing test.

If a_U vanishes throughout an admitted retarded interval and the full incoming/Cauchy modes vanish, zero z_j is a consistent homogeneous mode solution. If modes were previously driven or arrive from the exterior, they can persist/oscillate and gravitate when a_U later vanishes. Even at a_U=0 the VARIATION of a_U.Z leaves the terms g Z.nabla U-nabla(g U Z) in (3), and its metric improvement; it is not legitimate to delete those terms for nonzero Z. A geodesic-U ansatz must therefore pass (2)-(4), unit reactions and the Einstein constraints, rather than be imposed as a preferred-flow rule.

## 4. A coupled implementation route, with genuine state and junction data

The macro action actually supplies the coefficients and functional equations: (2)-(4), M^2 G_mu nu=T_phi+T_Maxwell+T_modes+T_constraints+T_ordinary and the ordinary rotating Euler/kinetic action. As a concrete weak metric contact, the acceleration/mode-connection block has coefficient [g Z_lambda U^alpha U^beta-sum_j Pi_j^(alpha beta) z_j,lambda]delta Gamma^lambda_alpha beta; its integration by parts supplies the corresponding Hilbert improvement and conormal port. Add the ACTUAL algebraic projector, potential, phase, Maxwell, measure and reaction metric variations from (1), not a chosen stress function. Field ports are n.Pi_U delta U,n.Pi_j delta z_j and n.J_phi delta phi, together with the same EH/ordinary metric/current ports. These are the same quantities needed by the retarded axial exterior95 and rotating material109, not a second energy population.

For a stationary circular benchmark the exact odd94 Eq(1),(2) functional already retains arbitrary chi,shift and stationary modal V_j. Its nonlinear chi derivative is (3) on that restriction. The accountable interior extension varies chi AS AN UNKNOWN alongside every retained mode and the independent lapse/spatial/shift/phase rows, rather than imposing chi=0, U=u_M or a_U=0. General material transport or nonstationary formation uses the unrestricted equations (1)-(4) and its complete Cauchy data. The four sigma families remain all omega_j=sigma xi_j Hstar with ell=.1kpc; no one label, damping or initial kinetic population is selected.

The present action imposes only unit/transverse constraints, plus Einstein and phase/current constraints. It does not algebraically fix U to a phase normal, ordinary worldline, Killing vector or geodesic congruence, and it does not determine nonzero z_j/Tz_j from a static baryon footprint. The latter are independent constrained evolution data or outcomes of a supplied earlier source/boundary history. Static solver iterations are not that history. For a physical rotating solve retain the ordinary density/current/stress, full metric/extrinsic Cauchy data, U momenta, phase charge/domain, all projected mode positions/momenta and their constraint-compatible incoming/outer data. Solve multipliers; do not supply them twice. A disclosed no-independent-incoming exterior is a conditional branch, not a measured preparation.

The useful next consistency calculation is therefore the JOINT mode/projected-U/phase/Einstein residual and paired ports on one complete admitted rotating state, using the known macro Q0 normalization and actual full metric. The geodesic-U hypothesis is rejected if its residual (3) is nonzero; it is not rescued by an activity gain. A conditional forward/coupled stationary solver can use these explicit rows without waiting for a microscopic sigma calibration, while reporting that calibration/state/junction qualification separately. A quantum realization replaces this native sector through the actual rotating109 reduction and its count/Berry/support reactions; it is never appended to (1) as duplicate energy.

Undefined activity beyond .3--15.1kpc remains unknown, not zero; that endpoint neither truncates the baryons nor chooses an FLRW matching tube. Final physical velocities use exact geodesics of the CALCULATED full metric and observer registration, not an extra native force, smoothed lapse gradient or held-background orbital diagnostic. No EPS5 closure, physical state, stability, full junction or observational success follows from these equations alone.

## Actual input seals

Complete actual bytes were checked before and after exclusive creation. Paths are relative to J; no ancestor was changed or evaluated.

| Input | SHA256 |
|---|---|
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md | c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986 |
| CROSS_U_EPS5_TRANSVERSE_AXIAL_CAUSAL_EXTERIOR_AND_PORTS_V001.md | 47ab4d4281345ea69c01e3d063d63c05cbdd56706aa4920c02ddf6d0418e841b |
| NATIVE_ROTATING_MATERIAL_EXPLICIT_EULER_AND_METRIC_PORT_CLOSURE_V001.md | 161781870e4615825486f4df6cfb1406a6d248a9f79cb10ef31406a8b64cf4e9 |
| CROSS_U_NATIVE_RETARDED_RESPONSE_AND_STATIONARY_HISTORY_V001.md | 662a0eb290057bf0d7f5160e64c38edf17257b4073c1b07f4fa15ef1e1c710c7 |
| CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md | 048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2 |
| CROSS_U_GENERAL_METRIC_ORBIT_AND_FLRW_TIME_DEPENDENCE_V001.md | b3fd1355c03ed78cb702844cb05e34accb9e51d648d89c21db1bafd47dfcef59 |
| CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md | b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5 |
| cross_u_ngc3198_nonlinear_disk_v001.py | ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1 |
| CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json | e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f |
| CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json | df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6 |
