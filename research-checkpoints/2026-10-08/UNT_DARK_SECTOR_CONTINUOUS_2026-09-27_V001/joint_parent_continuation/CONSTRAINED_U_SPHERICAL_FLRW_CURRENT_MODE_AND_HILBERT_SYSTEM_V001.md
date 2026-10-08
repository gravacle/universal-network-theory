# Same-action spherical phase, vector, modes and FLRW source system V001

2026-10-06 UTC. Root-requested STATIC reduction of the CURRENT uncompressed S_dual. No source helper, field, coefficient, matrix, state, solver or trajectory is evaluated. Effective calibrated P(X), A/I0, KB=.02, C=2-KB, one Gbare=.99GN and the declared mode family remain. This is a concrete variational initial-boundary system, not a solved galaxy, microscopic-origin derivation or new abundance. The resident COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001 has a different geodesic-clock/saturating-source/no-gradient action; its Hamiltonian and invariant GR branch are not imported.

## 1. Exact angular reduction of the owned nonlinear action

Use signature(-+++), c_p=1, a general two-metric h_ab and areal scalar R(t,r): ds²=h_ab dx^a dx^b+R²dOmega². Retain lapse N, radial shift beta and radial scale L through h_ab dx^a dx^b=-N²dt²+L²(dr+beta dt)² before varying them; n_ADM=(partial_t-beta partial_r)/N and e=partial_r/L. A future unit independent U and its radial spatial unit E have U=cosh(chi)n_ADM+sinh(chi)e, E=sinh(chi)n_ADM+cosh(chi)e. The rapidity is physical vector tilt; setting chi=0 or N=1 before its equations would select a branch.
Define U f=U^a partial_a f, E f=E^a partial_a f, A_U=E.nabla_U U, K_U=E.nabla_E U, a_R=UR/R and b_R=ER/R. Spherical transverse vector modes are y_delta=f_delta E; Q=U phi, p=E phi, X²=Q²-p² on the admitted future pressure branch. The exact projected derivatives are
    |P_U nabla_U y_delta|²=(U f_delta)²,
    |Dcal y_delta|²=(E f_delta)²+2 f_delta² b_R²,
    F_U²=-2 A_U².                                                        (1)
The second term in the spatial norm is the radial VECTOR's angular derivative. Treating f_delta as a spatial scalar would change both its PDE and angular Hilbert stress. No independent angular modes are added within spherical symmetry.
Write integral nu for the inherited proper mode measure, B=sum_or_integral nu*kappa*delta*f_delta, Kb_mode=kappa*integral nu, J_delta=kappa*delta²*ell² and V_delta=kappa*delta²*f_delta²/2+u4*f_delta^4/4. A finite positive regulator replaces that integral by its actual fixed weights, without minimizing or deleting modes. Set g_sigma=C_m Kb_mode=M²C, and sigma=Sigma_E/C_m for the physical vector multiplier Sigma_E E. Thus all ordinary, gravity and material terms share the same factored 4pi:
    S_4=4pi*S_2+metric_boundary,
    S_2=integral sqrt(-h){M²/2[R² R_2+2(nabla R)²+2]+R² L_D}+S_o,2,
    L_D=M²KB A_U²/2+P(X)
       +C_m integral nu{m_delta(Uf_delta)²/2-V_delta
            -J_delta[(Ef_delta)²+2f_delta²b_R²]/2+kappa*delta*A_U*f_delta}
       +C_m sigma(B-Kb_mode*p).                                        (2)
The EH boundary is retained consistently with the chosen metric boundary data. P keeps its absolute reference P(Q0)=-A. There is no old DeltaU, compression term, separate acceleration contact, barotropic replacement or phase abundance. The nonlinear u4 force, spatial connection and their metric derivatives remain. If the unscaled multiplier Sigma_E is used instead, the last term is Sigma_E(B-Kb_mode*p) and every displayed sigma below means Sigma_E/C_m.

## 2. Closed phase/vector/modal rows

Let Div_R V=R^(-2) nabla_a(R² V^a), with nabla the TWO-metric derivative. The complete phase current and multiplier condition are
    J_phi=(n Q/X)U-(n p/X+g_sigma*sigma)E, n=P_X,
    Div_R J_phi=0, B=Kb_mode*p.                                        (3)
The reaction current is retained; the bare constituent n v_phi alone is not conserved separately. For every retained delta,
    m_delta Div_R[U(Uf_delta)]-J_delta Div_R[E(Ef_delta)]
       +kappa*delta²*f_delta+u4*f_delta³+2J_delta*b_R²*f_delta
          =kappa*delta*(A_U+sigma).                                    (4)
These equations retain time derivatives, proper gradients and quartic response. They are not a static constrained minimum or the early quadratic DAE pasted onto a nonlinear geometry.
Set D_A=M²KB A_U+C_m B. Varying rapidity at fixed two-metric gives delta U=E delta chi, delta E=U delta chi and delta A_U=U(delta chi)+K_U delta chi. Since Div_R U=K_U+2a_R, its exact independent radial vector equation is
    (U+2a_R)D_A=C_m integral nu[(m_delta-J_delta)(Uf_delta)(Ef_delta)
                              -2J_delta*f_delta²*a_R*b_R]
                        -g_sigma*Q*sigma.                              (5)
The projected unit/mode constraints are carried by the parametrization; their solved reactions still enter the full metric variation. In an unparametrized implementation retain U²=-1, U.y_delta=0 and their multipliers instead. Differentiating (3)'s constraint with the admitted time evolution supplies its tangent condition; sigma is a coupled reaction, not an initial profile or fitted radial force. The positive quadratic formula for sigma in the early fixture is a validation limit, not a general nonlinear inverse.

## 3. Full Hilbert source and the gravity equations

Equations (2)-(5) supply all source derivatives. For S_mat,2=S_2-S_EH,2, define its COMPLETE on-shell metric source by
    delta S_mat,2=integral sqrt(-h)[R² T^(ab)delta h_ab/2
                                         +2R p_perp delta R+Euler terms]. (6)
Perform these functional variations before fixing R=r, beta=0 or solving the multipliers. Vary U/E, projector/connection, proper measure and constraints as prescribed by the covariant parent. Equivalently vary the parametrized action at fixed chi/f and retain its vector/modal equations: the frame-dependent pullback agrees on shell, not by silently holding a physical vector/coframe fixed. This definition includes acceleration divergences, mixed momenta, gradient connection stress, multiplier and unit reactions. It is an explicit derivative of (2), not an unspecified EOS or rho_P appended to a mode energy.
The exact remaining warped Einstein equations are
    M²{-2 nabla_a nabla_b R/R
       +h_ab[2 box_h R/R+((nabla R)²-1)/R²]}=T_ab,
    M²[box_h R/R-R_2/2]=p_perp.                                        (7)
The ADM normal and normal-radial projections are the Hamiltonian and momentum constraints; the radial and angular projections give metric evolution. In spherical gravity there are no freely propagating tensor-wave data, but its constraints and mass/boundary data still must be solved. Equations (3)-(7), the actual ordinary equations and gauge preservation are the minimal retained 1+1 system. Using only rho_P, omitting (7)'s angular row or substituting a prescribed metric discards the same-action source contacts.
The exact pressure-constituent ADM chart remains qtilde=Pi_phi/sqrt(gamma)+g_sigma*N*sigma^t=n sqrt(1+p_ADM²/X(n)²), with its positive held-reaction inversion. This assists a coupled solve; it does not supply the vector/modal/Einstein constraints or turn qtilde into the full conserved Noether density.
For the complete on-shell once-only stress, its radial Ward identity is nabla_a(R² T^a_b)=2R p_perp partial_b R. An actual external source force adds R² f_b on the right. This is the exact angular-pressure work contact; an expanding volume's energy is not a separately conserved oscillator sum. It supplies a source/constraint check independent of the phase charge law.

## 4. A source and boundary that actually conserve

The smallest ordinary assembly model is one existing irrotational pressureless baryon stream before shell crossing: S_b=-integral sqrt(-g)rho_b0[(nabla psi_b)²+1]/2, u_b=-raised(dpsi_b), nabla(rho_b0 u_b)=0, u_b.nabla u_b=0. Its rest weights and incoming velocity are physical input; its density is evolved with its current. The calibrated ordinary radiation/neutrino inventory and its owned transport/stress remain where nonnegligible. A supported galaxy requires the actual ordinary pressure/velocity-dispersion or phase-space stress and its conserved work; prescribing growing density alone is not that source. A spherical source is a declared reduction, not the already exposed NGC3198 thin disk.
At a regular centre use R=O(r), R'/L->1, smooth scalar phi and baryon density, radial chi,f_delta,sigma=O(r), and finite sources. There is no point charge, central sink or implicit inner mass. On a worldtube r=r_b(t),
    C_phi=4pi integral_0^r_b N L R² J_phi^t dr,
    dC_phi/dt=-4pi N L R²[J_phi^r-r_b_dot J_phi^t]_b.                   (8)
Use (8) also for baryon rest current; energy/momentum use the stress Ward law in section3, including angular-pressure/geometry work and actual support/boundary work. In homogeneous spatially flat FLRW comoving coordinates N=1,L=a,R=a*r,chi=f=sigma=0, phi_dot=Q(a), a³n=I0. In areal coordinates beta=-HR, J^r=nHR. A fixed-areal zero-flux wall is therefore not the cosmological boundary. The exterior/incoming characteristic data are inherited from the same cosmological evolution/compensation history; outgoing data are computed. Junctions require continuous induced geometry and extrinsic curvature unless an actual surface stress is supplied.
The bare mode principal speed relative to U is sqrt(J_delta/m_delta); metric/null and ordinary characteristics remain distinct. A slice and boundary must be noncharacteristic for the actual constrained branch. No continuum hyperbolicity or positivity of the complete Einstein/reaction system follows just from m,J>0. Boundary data are specified on incoming physical characteristics and constraints, not all fields independently at a reflecting wall.

## 5. Finite input count and an implementable discriminating sequence

For N_m retained modes, a raw material Cauchy inventory is N_m coordinate/velocity pairs, one phase/charge pair, one U-tilt/electric-momentum pair and one baryon density/velocity pair: 2N_m+6 radial profiles. They must be supplied JOINTLY on the constraint manifold. On an initially U-orthogonal nondegenerate canonical slice, B=Kb_mode Ephi and its preserved first jet restrict two combinations, giving at most 2N_m+4 admitted material profiles before residual coordinate choices or added ordinary streams. This conditional inventory count is not a global nonlinear rank theorem; in a tilted ADM chart the constraint contains phi_dot and the full constrained Legendre system must be used. Gravity contributes constraints/gauge and centre/outer matching, not an independent chosen dark halo. Sigma has no additional freely prescribed pair.
A declared common regular adiabatic cosmological preparation can fix these relative mode/entropy data from one spatial primordial-curvature realization and ordinary inventory, followed by the actual assembly history. The saved single-k early trajectory alone does not provide all radial wavelengths or a mature galaxy's outer state. If those data are instead independently supplied, their number/state hypothesis must be exposed. The effective calibrated pressure, gravity and mode coefficients may be used without first deriving microscopic photon origin; the quadratic code's normalized omega/weights alone do not fix a nonlinear quartic amplitude convention. Freeze the already declared nonlinear mode calibration and its units once before a nonlinear run, with no radius-dependent retuning.
The concrete implementation sequence is: (i) reproduce the exact charged zero-mode FLRW solution and moving charge flux of (8) with the same background Friedmann source; (ii) recover the retained all-mode quadratic current/normal/phase DAE and Einstein trace/momentum limits from this action; (iii) evolve one predeclared compensated spherical baryon initial state with the SAME cosmologically inherited phase/U/mode data and boundary history, preserving (3), its tangent, both Einstein constraints and total energy flux. Read out the radial geodesic/light response and full current/modes together. The charge, preparation and baryon assembly are inputs; no favorable current profile or phase mass is fitted to the resulting force. An observed rotating disk then needs its actual geometry, not automatic spherical inheritance.
This bridge does not adopt the old stationary pole inverse. It can test whether a finite-duration shared state produces a galaxy-like response while evolving with expansion. Numerical constraint/source convergence is separate from observed force/lensing agreement, microscopic common-origin matching and a fluid/thermal interpretation. Existing static-cap/pole failures, cosmological failed gates and the separate microscopic t^4 correlation evidence are preserved.

## Actual inputs, checked before and after exclusive creation

| Input relative to J | SHA256 |
|---|---|
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| CONSTRAINED_U_NONLINEAR_ADM_PHASE_CHARGE_INVERSION_AND_SOURCE_CONTACTS_V001.md | c5cf5f19f6a7333d4f807a771bf7033b694924b28f5624980c5050fd8b7d5b82 |
| CONSTRAINED_U_GALAXY_WORLDTUBE_AND_STATIC_BOUNDARY_DISCRIMINATOR_V002.md | a7598cc79c7e3bdaa83ad31f32826e7cf439b0f28c6f79fda9a09ea98c5ab90b |
| NATIVE_LOCAL_PROPER_MATERIAL_NORMAL_AND_PHASE_SOURCE_MATCHING_V001.md | 40978c4874ea478c1ce03c7bfcaee0e8304f8bd1c80aebf0742282266209b64b |
| SPHERICAL_GRADIENT_COMMON_LENSING_CLOSURE_V001.md | a4221d6ed0d5b0fed266e9fc8e27fa190b3f911e39cc7d218912418d1cc69b57 |
| COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md | fba2461a4c03c6dbf2495bb22c48bcfb5a3d63c0f02d1a708b175aefb274ffd0 |
| CONSTRAINED_U_FINITE_RATE_DENSITY_CEILING_AND_HUBBLE_MATCHING_V001.md | 6531e74a991e5ff5729d1494d4261013c8c470f9fc80bca77016f1daff90861c |
