# Native causal response and stationary history: same S_cross V001

2026-10-06 UTC. AUTHOR_DRAFT=True; analytical and unexecuted, pending root and independent full review. This derives response from the existing effective action; no history kernel, stiffness reservoir, source halo, inertia, geometry, preparation or physical unit is added. Existing producers and evidence remain unchanged. No scientific helper, action, operator, matrix, field, kernel or trajectory was evaluated.

## 1. What the stationary calculation contains

On the current aligned even branch with Tz_j=0, the native stationary functional at fixed physical acceleration a_U, U and spatial geometry is g sum_j w_j integral[|z_j|^2/2+|z_j|^4/(4k_j)+ell^2|D_U z_j|^2/2-a_U.z_j], with g=M^2 C>0, w_j>0 and k_j=gc^2 xi_j^4>0. Its fixed-boundary native Hessian is

    A_j=ell^2 D_U^*D_U+(1+|z_j|^2/k_j)I+2z_j z_j^T/k_j.       (1)

On the admitted fixed finite domain it is strictly positive, so this fixed-source native minimization has at most one root. The quartic curvature, every positive weight, ell-gradient and cylindrical vector connection are already in the actual code. Its Newton/preconditioner iterations do not increment proper time, source age, count, phase charge or a physical mode momentum. An additional accumulated-stiffness term would change this functional unless derived from the same microscopic/state reduction.

This native convexity does NOT make the coupled metric/clock Hessian positive or unique: the physical Schur is K-Mclock-B^T D^-1 B. Ordinary source, clock loading and all metric/U equations remain. Different full stationary branches or a Jeans mode cannot be excluded by the positive native subblock; numerical convergence failure is not a history measurement.

## 2. Causal equations are already present in the full action

Use signature(-+++), c_p=1 and the normalized physical covectors of the matching note. With Tz=P_U nabla_U z and Dz=P_U P_U nabla z, the literal mode action is

    S_m=g sum_j w_j integral sqrt(-g){|Tz_j|^2/(2omega_j^2)
           -|z_j|^2/2-|z_j|^4/(4k_j)-ell^2|Dz_j|^2/2+a_U.z_j}.

Define formal adjoints by the SAME spacetime measure and actual boundary ports. Independent transverse variation gives

    -T^*(omega_j^-2 Tz_j)+ell^2 D^*Dz_j
                       +(1+|z_j|^2/k_j)z_j=P_U a_U.          (2)

The vector connection, projections, expansion and port terms are inside these adjoints; unit-U and U.z_j constraints and their reactions are retained. For example T^*=-P_U nabla_U-theta_U on transverse fields, theta_U=nabla.U, so even a stationary coordinate chart need not have Tz=0. The accepted odd action's V_j=chi(d.z_j)+(t.z_j)/2 and V_j^2/(2omega_j^2) are actual covariant kinetic contacts, not deleted stationary inertia.

At fixed flat local coframe, aligned U and fixed coefficients, (2) is the concrete nonlinear hyperbolic row

    z_j,tt/omega_j^2-ell^2 Delta_vec z_j
                              +(1+|z_j|^2/k_j)z_j=a_U.        (3)

Use the vector Laplacian; its cylindrical radial connection is not a scalar Laplacian. In SI, omega_j is s^-1, ell is proper length, z and a_U are inverse length (a_U=a_SI/c_p^2). The modal front speed is ell*omega_j. This is one material characteristic, not a statement that every coupled phase/gravity signal has that speed or that the phenomenological kinetic coefficients are physically registered.

The independent source rows remain nabla.J_phi=0 with J_phi=P_X v_phi-g r, r=P_U dphi, v_phi=-raised(dphi)/X, X=sqrt(-dphi^2); the projected U Euler row and its unit reaction; and M^2 G_munu=T_total, with ordinary matter, full mode/phase energies and boundary/exterior contacts. U derivative momentum at held independent covector modes is -M^2 KB F^mu_nu+g U^mu Z_nu, Z=sum w_j z_j. The projected mode derivatives depend algebraically on U; they do not supply another explicit nabla U vertex. Holding a_U externally in (3) is a response fixture, not this coupled galaxy closure.

## 3. Retardation follows from the equations, without a new memory law

Linearize (3) about a fixed admitted native equilibrium, retaining its actual A_j from (1). On a fixed positive-domain realization, Omega_j^2=omega_j^2 A_j. The exact frozen-coefficient response is

    delta z_j(t)=cos(Omega_j t)delta z_j(0)
       +Omega_j^-1 sin(Omega_j t)delta z_j,t(0)
       +integral_0^t omega_j^2 Omega_j^-1 sin[Omega_j(t-s)]delta a(s)ds.
    delta z_j(lambda)=omega_j^2(lambda^2+omega_j^2 A_j)^-1 delta a(lambda)
       +the actual initial-data terms, lambda>0.              (4)

Equation(4) defines a causal Green operator of the owned action, not a selected phenomenological integral. The positive-Laplace forced susceptibility decreases with rate relative to its static limit. Its real-time kernel oscillates and is not a positive accumulating measure. Changing U, source, metric or coefficients needs the actual time-dependent propagator and all source/constraint equations, not the frozen formula with a guessed history pasted into it.

The explanatory one-mode constant-source step with zero displacement/velocity gives z=a0(1-cos(Omega t))/A: initially it lags, then overshoots and oscillates. This is an identity of the linear equation, not an adopted galaxy ramp or preparation. The conservative local action supplies no damping-to-equilibrium theorem. FLRW yields its action-owned 3H friction; outgoing radiation/ports may dissipate local energy only through an admitted exterior, while a closed reflecting box can retain transients. Numerical line searches are not that friction.

At a fixed imposed acceleration, delayed Z reduces the instantaneous critical cancellation a-Z. In the controlled negligible-clock quasi-static scalar analogy this reduces the static MOND enhancement rather than automatically strengthening it. Later coherent overshoot, incoming modes and clock/metric response can change the sign. The full signed coupled problem has no earned theorem that history specifically cures an inner deficit while reducing the outer excess. Increased quartic curvature also lowers the local forced compliance; stiffness and stronger polarization are different statements.

## 4. Existing inertia labels and nonlinear rates

The only declared effective kinetic family is omega_j= sigma xi_j Hstar for sigma=.1,1,10,100. In proper kpc time t*=c_p t_SI/L0, L0=1kpc, eta=Hstar_SI L0/c_p=Hunit/[1000 c_p(km/s)]=Hunit/c_p(SI) numerically, and omega_j*=sigma xi_j eta. Hunit remains the actual inherited67.49711988577813 km/s/Mpc; neither H(1) nor a native phase clock is substituted. Proper/coordinate stationary rates differ by lapse and, for tilted flow, the actual convective generator.

At a locally homogeneous equilibrium, with s_j=|z_j|^2/k_j, transverse and parallel curvatures are 1+s_j and 1+3s_j. For a proper spatial Fourier inverse length q,

    Omega_j,perp^2=omega_j^2(1+s_j+ell^2 q^2),
    Omega_j,parallel^2=omega_j^2(1+3s_j+ell^2 q^2).             (5)

The inverse linear zero-field rates are (10,1,.1,.01)Hstar^-1/xi_j across the four labels; these are inverse angular rates, with periods2pi times larger. Nonlinear curvature may make local response much faster, so the zero-field rates alone cannot date a formed galaxy. It does not change the principal ell*omega_j front speed. Proper gradients, vector mixing, boundaries and moving constraints make a global response different from these local curvatures.

The current inertias are conditional sensitivity benchmarks, not values derived from the finite q4 donor, TEM vacuum spectrum, an Eunit-to-seconds conversion or the old passive-response fixture. The latter already shows state/clock-dependent signed response; it cannot supply one universal continuum inertia. No favorable sigma, damping, duration or incoming state is selected here.

## 5. What the existing cosmic history earns

The whole S_cross FLRW equations retain actual native displacements AND velocities, independent U/phase, density Wd-qPtot, mode inertia and Einstein moving constraints. The owned coupled radiation-history512/1024 pair transported its two manufactured ai=.01 Cauchy columns through a=1, keeping all past source panels, incoming angular distribution and the same proper background/phase origin. Physical model time advanced; preparation/current clock was not reset at each numerical panel. It did not evolve network birth/count, a measured galactic assembly, or a primordial state.

Its saved result is NUMERICAL_FAILED:297/305 predicates pass; both arms retain failures in normal, trace, original two-log-a radiation balance and proper-trace increment. Independent complete-history flux errors are about1.54e-14 and1.20e-14, but those do not promote the failed gates. This earned a concrete radiation transport/history calculation and its numerical diagnostics, not a complete native formation solution, galaxy memory fit or physical inertia identification. Its EPS1e-6 fixture does not inherit the EPS1e-5 SPARC field's state/source history.

## 6. The accountable next physics input and test

A dynamical NGC calculation needs the same source's conserved ordinary density/current/stress history, complete initial z_j and Tz_j plus phase/U/metric data satisfying normal/momentum/current constraints, the admitted boundary/incoming mode data, and one physical kinetic/clock registration. Present baryonic footprints and a converged static field supply none of those velocities or assembly times. The physical finite network reduction must also show how count/growth changes the retained mode coefficients/state if such change is asserted; fixed quadrature points are not independently accumulating records or new species.

A useful bounded first comparison is the actual local curvature/rate inventory of every saved mode at all admitted radii, with all four existing sigma labels and the exact proper units; it can falsify a claimed fast/slow local-scale estimate without choosing a ramp. It remains a local diagnostic, not a retarded inverse, stability or physical formation prediction. A subsequent causal forward problem may use a supplied history or an explicitly labelled implementation pulse, with the full same-action current/Hilbert constraints and no Vobs tuning. The sign and radial pattern must be outcomes; no added halo, memory reservoir or EOS is licensed by the stationary solver's omission of physical time.

## Actual direct input seals

All paths are relative to J; existing bytes and permissions are unchanged.

| Input | SHA256 |
|---|---|
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| NATIVE_TO_CROSS_PHASE_COEFFICIENT_CURRENT_AND_STRESS_MATCHING_V001.md | d95ad4155144f102243e14082faf1e5b6b7b193eef0c753c88864534ec302d40 |
| CROSS_U_RETARDED_RESPONSE_AND_BACKGROUND_EQUIVALENCE_V001.md | 78d369efb4efe4bab1f3885c2b11e37959e0860f449e839fa9d447da829ab9f6 |
| CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md | 048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2 |
| CROSS_U_CONFORMAL_COLD_CIRCULAR_NEXT_ORDER_SOURCE_CLOSURE_V001.md | f8365d7bff3f420efe7d30746fd8fe3983a88e62dda1442c00ad73329e087979 |
| CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md | c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986 |
| CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001.md | f06a5fd890ccae9e2f0e0f08c29a48f8222a2ed6d51176ab61652750f0f219b4 |
| CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_RESULT.json | c91fd50725e1d770881a13ba60615aa04d2fba8899bf4fefe34d1f8b733978aa |
| CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_RECEIPT.json | d7507bc37c4880089fe4a70716ceff226bd251a5fa437329581d044620f31913 |
| CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_REPORT.md | aae7a6b2a75d4ce23ae981ea53d96c4f5a0ea48eb139c39afe066e7b99b66bfc |
| cross_u_ngc3198_nonlinear_disk_v001.py | ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1 |
| NATIVE_PASSIVE_INERTIAL_RESPONSE_V001.md | 56183a0baccc805aa67bd553a908983ddc714afef0824eecc80f465182e76981 |

| reviewed_CROSS_U_NATIVE_RETARDED_RESPONSE_AND_STATIONARY_HISTORY_V001_98_54aa815b.md | 54aa815b173dfb7c87f0962c2157f66af8188b9417b44c56d15b75047a62c620 |

Guard remains AUTHOR_DRAFT=True pending root and independent mathematical/text review. All listed bytes were hashed before and after exclusive creation. This is symbolic analysis and saved scalar readout only; no scientific function or new numerical experiment was evaluated.
