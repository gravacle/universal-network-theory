# S_cross stationary axisymmetric orbits and ordinary-matter registration V001

2026-10-06 UTC. AUTHOR_DRAFT=True. Guarded analytical companion, pending root and independent full mathematical review. No field solve, source fit, optical projection, numerical kernel or orbit evaluation was performed to write this note. All existing galaxy/source/metric qualifications remain unchanged. The same S_cross law and ordinary coupling are retained.

## 1. The actual ordinary-matter coupling

Protected V003 Eq(5) has S_cross = S_EH + S_U,phase,modes + S_o + S_constraints. The inherited bounded-clock action explicitly writes S_ordinary[g]; the physical common-metric dictionary is retained. There is no supplied direct ordinary current coupling to phi, U, a native mode or its stress. The phase Noether current is not the ordinary tracer velocity/current. No such force or disformal metric is added here.

For a neutral freely falling pressureless tracer the metric-minimal point action is -m c_p integral ds, giving u^mu nabla_mu u^nu=0. On the ordinary equations, metric-only diffeomorphism invariance gives nabla_mu T_o^{mu nu}=0. Ordinary electromagnetic/plasma interactions can exchange momentum internally or give their usual Lorentz/pressure forces; an individual interacting gas element is not automatically a geodesic. Those actual ordinary stresses must be supplied, rather than attributed to native T as an extra tracer force.

The lapse equation already includes the varied phase/clock source delta rho_phi+3delta P and leading native polarization. The complete Hilbert stress changes the metric through the Einstein/vector/phase/mode equations. Adding a term proportional to that same T directly to a solved circular velocity would count the action twice and would change the supplied ordinary coupling.

## 2. Exact circular-orbit equations and units

Let t have seconds, phi be an angle and R,Z be length coordinates. On a circular stationary axisymmetric metric (no meridional shift), write

    ds^2 = -N^2 c_p^2 dt^2 + h_AB dx^A dx^B
           + h_phi_phi (dphi + beta^phi dt)^2,  A,B=R,Z.       (1)

The signed shift beta^phi and Omega=dphi/dt have inverse-time units; g_tphi=h_phi_phi beta^phi and g_tt=-N^2 c_p^2+h_phi_phi(beta^phi)^2. N>0 and h_phi_phi>0. Meridional metric h_AB need not be conformally flat. A genuinely noncircular stationary geometry needs the full normal/spatial velocity dictionary, not merely (1).

A constant-R,Z orbit has u^mu=u^t(1,0,0,Omega). The R,Z Euler-Lagrange equations of the geodesic action give independently

    partial_A g_tt + 2Omega partial_A g_tphi
                       + Omega^2 partial_A g_phi_phi = 0.     (2)

A reflection-symmetric equatorial plane makes the Z condition automatic; otherwise a radial root alone does not establish an orbit. When partial_R g_phi_phi is nonzero, the two algebraic angular roots are

    Omega_+- = [-partial_R g_tphi +- sqrt((partial_R g_tphi)^2
                   -partial_R g_tt partial_R g_phi_phi)]
                  / partial_R g_phi_phi.                     (3)

Require a nonnegative discriminant and the timelike condition -(g_tt+2Omega g_tphi+Omega^2 g_phi_phi)>0, with future u^t. The zero derivative case must use (2) without division. Radial/vertical stability requires the separate effective-potential second-variation test at held Killing energy/angular momentum; (2) alone does not assert stability.

The normal observer is n=N^-1(partial_t-beta^phi partial_phi) with n.n=-c_p^2. Its orthonormal azimuthal basis is e_phi=h_phi_phi^-1/2 partial_phi. Decomposing u=gamma(n+v_ZAMO e_phi) gives the signed physical speed

    v_ZAMO = sqrt(h_phi_phi)(Omega+beta^phi)/N,
    |v_ZAMO|<c_p.                                            (4)

With c_p=1 this is the requested dimensionless formula. A constant coordinate rotation changes Omega and beta^phi oppositely; their sum is invariant.

## 3. The static scalar limit and the exact shift contact

Set beta^phi=0, N=exp(Phi), h_phi_phi=R^2 exp(-2Psi). Phi and Psi here are dimensionless logarithmic metric functions, not SI velocity-squared potentials. Substitution into (2)-(4) gives

    v_ZAMO^2/c_p^2 = R partial_R Phi/(1-R partial_R Psi).      (5)

This is exact for that metric chart, rather than exact for every static metric. In general static h_phi_phi, v^2/c_p^2=2 partial_R lnN/partial_R ln h_phi_phi = d lnN/d ln rho_c, with rho_c=sqrt(h_phi_phi). Require the appropriate positive orbit branch and timelikeness; an extremum of circumferential radius requires the undivided equation.

The Q1 code uses the leading weak limit Phi_0=B0 psi and v_0^2=c_p^2 R partial_R Phi_0=R a0 L0 partial_R psi, with dimensionless code R measured in L0. Its A0_V conversion yields (km/s)^2 once; no additional c_p factor multiplies that saved readout. The R-tabulated observational radius is the inherited distance/projection registration, not an already solved circumferential metric radius.

For nonzero shift, define rho_c=sqrt(h_phi_phi). Eliminating Omega gives the exact contact

    v^2 partial_R ln rho_c + (rho_c/N) v partial_R beta^phi
                           = c_p^2 partial_R Phi.             (6)

Thus a rigid coordinate rotation contributes no derivative force. In the same near-static weak chart, first variation about v_0 and Phi_0 gives

    delta v/v_0 = (1/2)[delta Phi'/Phi_0' + R Psi'
                    - R rho_c beta^phi'/(N v_0)]
                    + radius/projection/nongeodesic contacts. (7)

Equation(7) is a conditional linearized diagnostic, not an evaluated correction. Full tensor spatial geometry enters through h_phi_phi, not only a scalar Psi. Uncomputed meridional shift/time dependence requires the general geodesic or ordinary Euler equations.

## 4. What could establish an order-ten-percent correction

At held lapse, (5) gives (v/v_0)^2=(1-RPsi')^-1. A +1/10 speed change from this denominator alone requires RPsi'=21/121; a -1/10 change requires RPsi'=-19/81. A smooth nonrelativistic weak metric with Psi comparable to Phi and scale comparable to R instead has RPsi' of order v_0^2/c_p^2. Thus changing the orbit readout alone is not an established ten-percent mechanism. Small Psi amplitude with a much shorter gradient scale is a distinct possibility requiring its actual metric/regularity evidence.

A speed change epsilon_v requires a squared-speed change 2epsilon_v+epsilon_v^2. An actual force explanation can arise from delta Phi'/Phi_0', a supplied shift derivative, actual radial/projection registration or pressure/dispersion/noncircular ordinary dynamics. For a perfect ordinary fluid in c_p=1 units, (rho_o+p_o)a_alpha+P_u,alpha^beta partial_beta p_o=0; the measured density profile alone does not supply this pressure/velocity tensor or its dynamical history.

For the same native/phase branch, the response to omitted source contacts uses the ORIGINAL signed physical linearization and boundary data. Its lapse Schur block is S=K-M_clock-B^T D^-1 B, with D the positive native Hessian. A small weak-source load is not a bound on the derivative of S^-1 at the observed radii. A near-zero mode, noncoercive pressure loading, incompatible exterior or unresolved short-scale derivatives can amplify it. Conversely, solver failure or a small directional Rayleigh quotient alone does not establish that amplification. A response certificate needs the full source residual, resolved inverse/action residual, fixed metric boundary/junction and derivative readout, with all signed contacts retained.

The accepted V006-only weak meter reports native weak-load summary ratios: Q2 signed 2.19455888796947e-7 and envelope 2.508414335685563e-9, with Q3 agreeing at its stored precision. Its force_correction, metric_inverse_bound, ordinary_spatial_stress and background_Einstein_remainder are explicitly None; all physical-stress/metric/exterior flags are false. These selected finite weak-load comparisons are neither inverse bounds nor measured velocity corrections, and cannot be transferred silently to the refined full field. They supply no positive evidence for a ten-percent correction and do not prove it impossible.

## 5. Observed registration and the immediate evidence test

The protected resident SPARC excerpt contains 43 tabulated radii/observed velocities/errors at inherited D=13.8Mpc, plus signed gas and stellar/bulge mass-model velocity columns. It expressly is a transcription, not the original-byte download. Those columns are not themselves a complete three-dimensional conserved baryon stress/current or the metric optical pipeline. In particular a signed component velocity contribution is not a negative material density. Actual photometric/HI/H2 footprint normalization and thickness, source support/exterior and distance/inclination ancestry must be compared without choosing a profile to improve these residuals.

Photon frequency comparison is governed by -k.u at the emitter/observer and the same null-geodesic metric. Equating the tabulated rotation estimate to (4) additionally needs its projection/distance/observer/tracer-motion registration. No fitted inclination, distance, asymmetric-drift correction or new ordinary/native coupling is selected here.

The completed saved Q1 audit keeps all original smoothed rows and exact cell slopes. None of the 43 observed radii is exactly a mesh node in any of its six fields, so the saved left/right slopes agree at every observation; their general two-sided node ambiguity cannot be chosen to improve these rows. Fine Q2/Q3 agreement does not prove spatial/exterior/metric convergence. The actual fine-Q3 readout retains substantial velocity residuals and all fit/full-metric/refinement/formation qualifications are false.

The shortest same-law discriminator is therefore paired: authenticate the actual baryon footprint/projection once, and evaluate the omitted full source/current/metric correction with the same fixed source/wall and original signed operator, retaining ordinary stresses and background/exterior contacts. Compare the resulting circular/null readout at all 43 rows. If it supplies the required signed delta v with a controlled remainder, the residual explanation is earned; if not, neither a source claim nor a tensor-force addition rescues the current prediction. This note chooses no metric boundary, physical state, source fit or result.

## Actual protected inputs

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- BOUNDED_CLOCK_ACTION_AND_RESULT_V001.md — cf308c536629640fc5594b49b47447dc0c370e5e61e8fa622efa954ba975902b
- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md — 6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b
- cross_u_ngc3198_saved_q1_readout_audit_v001.py — 5160984364381366e989f6858560ef18b09d1655d951a14e0f66669ff5240134
- CROSS_U_NGC3198_SAVED_Q1_READOUT_AUDIT_V001_RESULT.json — d55e6b14f78023c3dc5b06ff6a9914610ef5ca1fc4fbdfb51146fe982a01f079
- CROSS_U_NGC3198_SAVED_Q1_READOUT_AUDIT_V001_RECEIPT.json — 5ac945edcebb4e8f67cc8f6b3b73c51f02bcc088705662dbda7246b669241079
- cross_u_ngc3198_saved_weak_stress_meter_v002.py — af1c2f0826380c714220e090f755fc20773c76804f2b0952e1f6400f9cd6eee6
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RESULT.json — d8d7de0d9f2faf7545c400230d116ad1dc2fe3488471982e3c1c01d3aac582c1
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RECEIPT.json — 12d150e67f3da4f36714e52480d5c7e90f7b7b0fd3dac919787e021503312018
- ../ngc3198_sparc_excerpt_v001.txt — 58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900
