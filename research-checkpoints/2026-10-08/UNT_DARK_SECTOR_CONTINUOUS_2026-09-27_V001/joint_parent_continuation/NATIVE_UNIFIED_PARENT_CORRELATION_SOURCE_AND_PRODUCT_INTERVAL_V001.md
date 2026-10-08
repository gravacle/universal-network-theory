# One native parent: exact correlation sources and the product-interval limit V001

2026-10-06 UTC. NEW static theorem for the SAME finite autonomous H16/canonical-Maxwell fixture. No state, source, coupling, temperature, energy allocation or running calculation is changed. No producer, operator, vector, eigensolver or trajectory is evaluated.

## Exact reduced dynamics retains both mean fields and correlations

Use ONE inherited physical Eunit and proper time t: HN=Eunit times the native source matrix, B=2Eunit Omega K0 and H=HN tensor I+I tensor B+n tensor W. Here n is the incidence projector, Kx=(Kplus+Kminus)/2 and

    W=Eunit Omega[a K0+b Kx],
    a=kappa^2/(1+kappa), b=kappa(2+kappa)/(1+kappa).

This is the exact positive-Z canonical interaction, not a gap-filtered port. The declared fixture has h=1 in native units, Omega=1, kappa=0,+/-.001 and M=8/12/16; the theorem below applies to the admitted finite h!=0,Omega>0,kappa>-1,kappa!=0,M>=1 branch. Absolute vacuum and interaction storage remain in the complete H.

For the actual normalized joint density rho, define rhoN=Tr_gamma rho, rhoGamma=Tr_N rho, chi=rho-rhoN tensor rhoGamma, meanW=Tr(W rhoGamma), meann=Tr(n rhoN). Exact unitary evolution gives

    rhoN_dot=-(i/hbar)[HN+meanW n,rhoN]
                         -(i/hbar)Tr_gamma[n tensor W,chi],
    rhoGamma_dot=-(i/hbar)[B+meann W,rhoGamma]
                         -(i/hbar)Tr_N[n tensor W,chi].             (1)

These are identities of the SAME state. Zero mean component powers constrain only scalar traces of (1); they do not remove the mean fields, off-diagonal coherence, correlation sources or conditional-state memory. In particular, bare-field stationarity [rhoGamma,B]=0 is a distinct observable and is not a temperature or fluid criterion.

Let D_N and D_gamma denote the correlation terms in (1). Since the commutator of Hermitian H_int and chi is anti-Hermitian, partial trace contracts its trace norm after multiplication by i. Thus

    ||D_a||_1 <= 2||n||_infinity||W||_infinity||chi||_1/hbar. (2)

For a reference marginal evolved from the SAME initial marginal with the ACTUAL time-dependent mean-field coefficients in (1), unitary Duhamel gives ||rho_a-rho_a,meanfield||_1<=integral ||D_a||_1 dt. This bounds the correlation contribution only. A proposed free radiation generator B must additionally control the meann W term; a prescribed phase action must retain its actual source and memory contacts. No new preparation or autonomous closure is defined by this reference.

## No sustained exact pure product in the closed nonzero-coupling fixture

At a pure product point psiN tensor psiGamma, the interaction derivative orthogonal to the product tangent is -(i/hbar)(n-meann)psiN tensor (W-meanW)psiGamma. Its squared norm is Var(n)Var(W)/hbar^2. The reduced linear entropy obeys

    1-Tr(rhoN(t)^2)=2 Var(n)Var(W)(t-t0)^2/hbar^2
                          +O((t-t0)^3).                         (3)

The original n0 preparation has Var(n)=0 and hence zero instantaneous quadratic curvature. This does not prevent later entanglement: -h Xlink immediately leaves the n0 block. Equation (3) is a product-point expansion, not a temperature, monotonic entropy law or finite-time error bound.

Suppose the exact globally PURE evolution remained a native-field product on a connected open interval. Its finite-H density and variances are real analytic, and product tangency requires Var(n)Var(W)=0 everywhere. The analytic product-zero identity forces one variance to vanish identically; isolated variance zeros cannot alternate these alternatives.

A persistent native n eigenstate is impossible: the incidence off-diagonal block is -hI, and no other retained term cancels that cross-block derivative. The other alternative is a persistent field W eigenstate. W is an irreducible finite Jacobi matrix, with off-diagonal entries Eunit Omega b sqrt((j+1)(j+2))/2 nonzero. An eigenvector's first coordinate cannot vanish, and the recurrence fixes every other coordinate from it, so its eigenvalues are simple. A continuous zero-variance field therefore stays on one fixed W eigenray. Its product-state evolution under B+meann W then requires that ray also be an eigenvector of B.

But B=2Eunit Omega K0 is nondegenerate, and every one of its basis vectors has a nonzero neighbor under W for M>=1. There is no common eigenvector. The assumed positive-duration pure-product interval is impossible.

Instantaneous products, possible revivals, kappa0, h0, M0, mixed-global states and changed support are different cases. No assertion about the selected fixture's revival time or asymptotic state is made.

## What an effective radiation-plus-phase limit would need

Microscopic factorization is NOT necessary for approximately autonomous fluids. Entangled sectors may admit controlled current/stress closure. The decisive quantities are the complete reduced interaction generators, integrated absolute exchange/current sources and source-dependent conditional/Berry memory, rather than a zero endpoint net-energy change or covariance sign. The exact carrier quotient already retains these contacts; it does not allocate an independent P(X) energy budget.

Outgoing-support separation, ordinary plasma redistribution/number-changing equilibration, or a controlled collective phase reduction can differ from this closed finite fixture. They must retain the common energy/current/Hilbert-stress inventory and actual preparation/memory. Native Gibbs/KMS is not an entrance requirement. Neither the obstruction nor (2) excludes those routes or the physical cold P(X) postulate. No macroscopic phase action, photon escape, thermality, matter fraction or cosmological matching is earned here.

## Actual input bindings

| Input relative to J | SHA256 |
|---|---|
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| native_unified_parent_component_exchange_v001.py | 2da75f9a6c20643a7d6b4288a821fe64e72ceb9961495f9dc167949d3d2459a2 |
| NATIVE_UNIFIED_PARENT_COMPONENT_EXCHANGE_V001_RESULT.json | e47f1ec7031dc540412b185cf6c2d0e6441131f3b59befdc1c254eb49b8fae8b |
| NATIVE_UNIFIED_PARENT_COMPONENT_EXCHANGE_V001_RECEIPT.json | cf88622b4c2c7806577f8cd3c74ac81a5bb3a0b57faeb143265b12d5acac6688 |
| NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md | f3dad63532285add3f890b0c15e9fad4c4968226904e66cf43e6e110966eb6fa |
| NATIVE_CANONICAL_MAXWELL_POSITIVITY_AND_VACUUM_GROWTH_V001.md | 3f57f9b9b0844903aa8dac4bd31c76372e5f6ce613e123b1c535270e03fb43f3 |
| NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md | 7e5cf9d3651de4471b52c9a3769f23cdd5457726c8354ff42ecee3c2a4034c7b |
