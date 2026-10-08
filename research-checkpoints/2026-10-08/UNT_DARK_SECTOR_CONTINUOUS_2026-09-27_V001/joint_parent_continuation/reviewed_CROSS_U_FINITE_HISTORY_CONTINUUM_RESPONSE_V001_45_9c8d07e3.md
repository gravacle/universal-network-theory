# Finite-history continuum response of the existing native law V001

2026-10-06 UTC. Analytical result in the unchanged S_cross action. Full review pending; no producer, source profile, state, numerical function or trajectory evaluated. No infrared cutoff, inertia, damping or volume-energy law is added.

At a fixed aligned proper coframe and positive held native operator A_xi, the existing equation is delta-z-double-dot+omega_xi^2 A_xi delta-z=omega_xi^2 delta-a_U. Retain the same incoming Cauchy state when varying the source. With omega_xi=omega_star*xi, omega_star=sigma*Hstar, and the already stipulated normalized measure2xi dxi on(0,1), the forced primitive response is

    K_xi(t)=omega_xi^2 Omega_xi^-1 sin(Omega_xi t),
    Omega_xi^2=omega_xi^2 A_xi,
    delta Z(t)=integral_0^t ds integral_0^1 2xi dxi K_xi(t-s)delta a_U(s).

The omega_xi^2 numerator is mandatory. The action's conjugate acceleration source is B_native=g Z, g=M^2 C; its response is g times the displayed primitive response. It is not the full relaxed metric/boost kernel or the graph's PLUS-affine commutator. Moving U, geometry, coefficients, reactions and expanding-background adjoints require their actual coupled propagator.

For every positive fixed A_xi, the spectral bound ||Omega_xi^-1 sin(Omega_xi t)||<=|t| gives

    ||K_Z(t)||<=omega_star^2 t/2,
    ||delta Z(T)||<=omega_star^2 T^2 ||delta a_U||_infinity/4.

Thus finite-duration bounded source variation is infrared finite without choosing a window or cutoff. Initial-data terms remain; this bound does not replace the physical preparation by zero or reset its clock.

For the zero-native-background, frozen spatial Fourier block, A=1+ell^2 q^2 is independent of xi. At real positive Laplace rate lambda the exact continuum forced susceptibility is

    chi(lambda)=(1/A)[1-lambda^2/(A omega_star^2)
                         *log(1+A omega_star^2/lambda^2)].

It tends to1/A at lambda=0, but has a lambda^2 log(lambda) correction rather than a finite second Taylor moment. The divergence of integral2xi/(omega_xi^2 A^2)dxi therefore does not make the finite causal response ill defined. It invalidates that local low-frequency Taylor truncation.

For a constant step VARIATION of the source with its incoming variation held zero, y=omega_star*sqrt(A)*t gives the exact aggregate response divided by step amplitude

    R(t)=(1/A)[1-2sin(y)/y-2(cos(y)-1)/y^2],
    R(t)=(y^2/4-y^4/72+y^6/2880+...)/A near zero,
    K_Z(t)=(2omega_star/sqrt(A))[-cos(y)/y+2sin(y)/y^2+2(cos(y)-1)/y^3].

The apparent quotients at y=0 are removable. R tends to1/A through continuum dephasing, with oscillatory overshoot; at y=pi it is(1+4/pi^2)/A. This step is an analytical response test, not an adopted galaxy assembly or primordial source history. Individual conservative modes retain energy; a finite32-mode quadrature does not inherit a damping/relaxation theorem or irreversible entropy production.

There is a separate nonlinear local qualification. In a nonzero, homogeneous, held-acceleration equilibrium, z+z^3/(gc^2 xi^4)=a>0 implies z~(a gc^2)^(1/3)xi^(4/3). Thus s=z^2/(gc^2 xi^4)~(a/gc)^(2/3)xi^(-4/3), and both local curvatures1+s and1+3s diverge with that power. Their second temporal integrand2xi/(omega_xi^2 kappa_xi^2) then scales as xi^(5/3), which is locally integrable. The zero-field/exterior moment remains divergent. This continuum asymptotic is a derived homogeneous/local limit, not a measurement from the saved32 nodes or proof about a spatially varying coupled galaxy, zeros of a, boundary layers or global eigenmodes.

Proper Hstar remains the inherited67.49711988577813 km/s/Mpc. The four sigma benchmarks remain conditional; no physical native inertia, graph-to-seconds conversion or galaxy duration is selected. This removes one apparent mathematical obstruction to finite causal history. It does not supply the missing material/coframe/U source identification, observational history, stable records or a successful galaxy–expansion prediction. All Stage3 obligations remain open.

Exact resident input seals (relative to this directory):

| Input | SHA256 |
|---|---|
| CROSS_U_NATIVE_RETARDED_RESPONSE_AND_STATIONARY_HISTORY_V001.md | 662a0eb290057bf0d7f5160e64c38edf17257b4073c1b07f4fa15ef1e1c710c7 |
| CROSS_U_EPS5_LINEAR_EXTERIOR_PHASE_NATIVE_AND_METRIC_MATCHING_V001.md | a7fc7786b42fa46ca5ec268eaba5ee2e581f3ebcdb48bffb83e8cfc6a5ef54d4 |
| CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_RESULT.json | 1f00f801492401811f5c39790e43e8b07379362f02698f12a9d29e45374dfdd9 |
