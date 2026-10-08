# Explicit rotating material Euler and metric-port closure V001

2026-10-06 UTC. AUTHOR_DRAFT=True; root and distinct FULL review required. This expands the existing rotation-capable 110-line action, not a new energy or force law. No operator, coefficient, state, field, source, history, trajectory or numerical function is evaluated. The proper h=.2 Hamiltonian, EPS1e-5 pressure law, all absolute energies and existing evidence remain unchanged. Equations use signature(-+++), c_p=1; the SI momentum conversion is stated separately.

## 1. One action and exact meanings of the remaining derivatives

Retain one joint Berry term and H_reg=Eunit sum_v exp(a_U.R_v) h_v, with the complete endpoint h_v of the pinned candidate, R_v=ell e_I r_v^I, independent unit U and independent ROTATING material u=u_M. The exponential remains a disclosed nonminimal material-source rule, not exact finite Fermi redshift. Periodic logical coordinates do not certify a faithful proper embedding. No scalar-gradient material clock is used.

Let w_q denote the actual weak quantum support: integral sqrt(-g) w_q f equals its registered proper-worldline/material integral. It includes that clock/measure ONCE; do not multiply an already lapse-loaded Hamiltonian again. Multipliers below are densities against sqrt(-g), including their supplied support as in 110. Define the known direct energy vertices

    b_mu=-w_q Eunit sum_v n_v <h_v> R_v,mu,
    F_I,mu=-w_q Eunit ell sum_v n_v r_v^I <h_v> a_U,mu,
    n_v=exp(a_U.R_v), a_U=nabla_U U.                         (1)

Before any average, these are weak sources, not fields obtained by division by a delta function. The reference b=-Eunit ell e_I<G_I>/V requires the SAME supplied proper averaging volume. Direct derivatives hold the joint ket; its evolution and source/encoder connection are retained separately.

Write R_u,R_U,R_eI,R_X and R_g for the ACTUAL derivatives of the remaining registered action: Berry/encoder connection, explicit h_v and readout derivatives, j_A Q_A and P nu n_hat contacts, -P V_x, map/matching/reference, embedding/support and included ports. These symbols are bookkeeping for specified variational derivatives, not adjustable functions. The source block is exactly H_reg,x+j_A Q_A,x+P nu n_hat,x-P V_x plus the map/Berry/measure terms. It is not declared zero when that registration is absent. The displayed acceleration, frame, unit and label terms below are excluded from R to prevent duplication.

The frame/unit/label action being expanded is

    L_con=lambda_U(U^2+1)/2+lambda_M(u^2+1)/2
       +lambda_I U.e_I+lambda_IJ(e_I.e_J-delta_IJ)/2
       +zeta_I u.partial X^I+A_I,mu u^alpha C_I,alpha^mu,
    C_I,alpha^mu=nabla_alpha e_I^mu-U^mu e_I,nu nabla_alpha U^nu,
    lambda_IJ=lambda_JI.                                    (2)

Use either the weak material representation or its first-order worldline registration in 110, with the corresponding clock/momentum contribution in R_u; they are not two independent material energies. A physical encoder/material map and the support weights must be supplied before these R terms become numerical arrays. Choosing the minimal fixed scalar chart does not supply its actual birth, return, Maxwell, junction or many-cell complement.

## 2. Expanded independent frame, U and material equations

Variation of (2) gives the following explicit rows, with sums over I,J:

    0=W_eI,mu=F_I,mu+R_eI,mu+lambda_I U_mu+lambda_IJ e_J,mu
       -nabla_alpha(u^alpha A_I,mu)-(A_I.U) D_M U_mu,
    W_U,mu,tr=-A_I,mu(e_I.D_M U)
                       +nabla_alpha[u^alpha(A_I.U)e_I,mu],
    W_u,alpha,tr=A_I,mu C_I,alpha^mu, D_M=nabla_u,
    W_U,mu,acc=b_nu nabla_mu U^nu-nabla_alpha(U^alpha b_mu). (3)

Thus A_I is a solved transport momentum, not a chosen stress or a permitted zero reaction. The complete independent-U and material rows are

    0=R_U,mu+W_U,mu,acc+W_U,mu,tr
                                  +lambda_U U_mu+lambda_I e_I,mu,
    0=R_u,mu+W_u,mu,tr+lambda_M u_mu+zeta_I partial_mu X^I,
    0=P_M^(nu mu)[R_u,mu+W_u,mu,tr+zeta_I partial_mu X^I],
    0=E_I=R_XI-nabla_mu(zeta_I u^mu), P_M=g+u u.             (4)

Unit/triad/advection/transport variations also impose U^2=u^2=-1, U.e_I=0, e_I.e_J=delta_IJ, u.partial X^I=0 and u^alpha C_I,alpha^mu=0. The unit multipliers follow normal contractions; for example lambda_M=u.(R_u+W_u,tr) because u.dX=0. The frame multipliers follow its longitudinal/triad contractions. They are not independent fitted initial functions. On smooth positive undensitized support w, every divergence in (3),(4) becomes w^-1 nabla(w times the corresponding momentum); worldline support remains weak.

When this candidate REALIZES/replaces the native L_m sector of the adopted S_cross, the unchanged Maxwell/Y contribution is retained in R_U once. With Q=U.dphi and r=(g+UU)dphi its held-variable row is M^2 KB nabla_alpha F^alpha_mu-g[Q r_mu+(U.r)partial_mu phi], where g=M^2 C, KB=.02,C=1.98. The second term reduces to -g Q r_mu only after the unit constraint. The full phase row retains nabla_mu(P_X v_phi^mu-g r^mu)=0 and its actual matched source contacts; it does not acquire a source proportional to record formation. The candidate cannot be stacked onto the old g L_m energy or g a_U.Z response. A failure to match those retained sources is a reduction failure, not permission to append another force.

## 3. Proper clock, state, labels and constrained momenta

The first-order worldline action is the retained p_mu(z_dot^mu-e0 u^mu)+e0 lambda_M(u^2+1)/2, with d tau=e0 d lambda. Its multiplier and state rows are

    z_dot=e0 u, e0>0,
    i hbar D_tau Psi=(H_reg+j_A Q_A+P nu n_hat)Psi,
    y_A=<Q_A>, V=nu<n_hat>, gamma=L(y),
    j=L_y^dagger Lambda+the actual other y derivatives.       (5)

The normalized ket and its scalar constraint phases remain in the normal/spatial work. The e0 row gives p.u=-<H_reg> on the displayed algebraic constraint surface ONLY when the actual additional clock contacts vanish there; otherwise solve the complete e0 derivative. All pressure/map, reference and absolute-energy derivatives remain. The embedding row delta S/delta z=0 must be solved alongside (3),(4), not replaced by a supplied rotation curve.

For the restricted worldline block with its actual remaining u vertex Acal_mu excluding -p_mu and the unit term, variation gives p_mu=Acal_mu+lambda_M u_mu. If the stated clock row applies, this implies

    p_mu=<H_reg> u_mu+P_M,mu^nu Acal_nu.                    (6)

Here Acal includes frame, label, Berry and support vertices actually present, not a new mass or drift function. In SI the first term is <H_reg> u_mu/c_p^2 with u^2=-c_p^2. Only when those projected vertices truly vanish does the momentum become pure energy times u. One may not impose that limit on the rotating frame system or turn the clock-energy term alone into its complete stress. Material vorticity is independent admissible data; no irrotationality follows from (5),(6).

## 4. Paired field and metric connection ports

The exact derivative momenta from the displayed native acceleration/transport block are

    Pi_eI^alpha_mu=u^alpha A_I,mu,
    Pi_U^alpha_mu=U^alpha b_mu-u^alpha(A_I.U)e_I,mu,
    K_lambda^alpha beta=b_lambda U^alpha U^beta
       +u^(alpha A_I,lambda e_I^beta)
       -u^(alpha(A_I.U)e_I,lambda U^beta),
    D^alpha mu nu=K^(mu|alpha|nu)-K^alpha mu nu/2,           (7)

where K^rho alpha beta=g^rho lambda K_lambda^alpha beta and the parentheses in D symmetrize mu,nu. Thus delta S_connection=integral sqrt(-g) D^alpha mu nu nabla_alpha(delta g_mu nu), with bulk Hilbert improvement -2 nabla_alpha D^alpha mu nu and boundary port n_alpha D^alpha mu nu delta g_mu nu. The direct displayed metric stress is

    T_alg^mu nu=2a_U^(mu b^nu)-2(A_I.U)e_I^(mu D_M U^nu)
       +lambda_U U^mu U^nu+lambda_M u^mu u^nu
       +2lambda_I U^(mu e_I^nu)+lambda_IJ e_I^mu e_J^nu.     (8)

Add R_g, the full clock/state/constraint-phase and measure variation; before imposing constraints the actual L_con also supplies g^mu nu L_con. Equations(7),(8) do not double-count the clock and lambda_M stresses of equivalent representations. Field boundary terms are n_alpha Pi_U^alpha_mu delta U^mu, n_alpha u^alpha A_I,mu delta e_I^mu and n_alpha zeta_I u^alpha delta X^I. Retain the parent's Maxwell momentum -M^2 KB F^alpha_mu, EH boundary momentum and every other owned field/encoder/support port once. Zero external traction or zero conormal momentum is not inferred from a finite computational wall.

The resulting common-source Ward equation is exactly 110(7), with the EXPANDED rows (3)-(5), actual embedding/state/ports and separate independent U,u. Einstein normal, momentum and spatial rows use that same full Hilbert tensor. Ordinary minimally coupled tracers follow their full geodesic or actual ordinary Euler/kinetic equation; native stress is not an added tracer force.

## 5. Minimal data and the next physical calculation

A closed conditional evolution first requires ONE complete material/encoder/support and physical map/volume/connection registration, the single Eunit/ell/charge normalization and its once-only S_cross reduction. These are constitutive inputs already named by the parent, not a new EOS or an outcome-selected energy function. Then supply: an admissible joint ket on its actual chronology and retained complements; material worldlines/labels and vortical timelike velocities; constrained triads and their independent transport momenta; the same metric Cauchy geometry/extrinsic curvature, independent-U momenta and phase charge/domain; and the ordinary distribution/stress. In the effective representation use the full native coordinates/velocities INSTEAD of a second independent quantum population; if both descriptions are compared their states obey the actual reduction map. Specify only independent constraint-compatible components modulo the chosen gauges. Solve algebraic multipliers from their rows instead of supplying them again. A continuum of independent copied kets would be a different, unadmitted preparation.

At a worldtube use the actual induced metric/extrinsic curvature, phase/current and native/material weak ports, with supplied incoming/outgoing state data and the same EPS5 exterior. Do not impose redundant homogeneous values plus arbitrary zero momenta. Activity data stop at 15.1kpc; they neither end the baryons/galaxy nor provide a zero active source outside. Missing history, optical tracer registration and exterior data remain unknown. Final physical velocities require the calculated full metric and exact geodesic/observer transfer, not a Newtonian readout.

The next finite-state matching calculation is to solve (3)-(6) and its normal/memory/count constraints on ONE prospectively admitted proper h=.2 member/state/support, evaluate the paired (7),(8) vertices and inclusive angular/energy flux, and test b=g Z plus the complete Kubo-minus-Born and charge/dilation targets on that SAME state. Check the joint multiplier Jacobian on its actual gauge quotient; the prior source-jet PASS proves neither its invertibility nor evolution well-posedness. This tests the actual transport and reactions beyond the completed lapse/boost coefficient checks; it requires no graph diagonalization merely to define its equations. The existing h=.1 states cannot be relabeled as that preparation. The adopted effective S_cross can instead be evolved directly with its ordinary dynamics and admissible Cauchy/junction data; a microscopic realization is not a new hardware entrance gate. Neither route is yet a registered physical rotating-galaxy solution.

## Actual read-only input seals

Complete actual bytes were checked before and after exclusive creation; no input was modified or executed. Paths are relative to J.

| Input | SHA256 |
|---|---|
| NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001.md | e8911d59ae25f9d397a57a6dcd6d0ca5c450df82566935c00f8436568f7484ff |
| NATIVE_PROPER_BOND_COVARIANT_ACCELERATION_MATERIAL_LIFT_CANDIDATE_V001.md | af1fab1ab22cc9cac29582348a7eaeb89309ba09a230ff0ed7067d1e778b7cd2 |
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| NATIVE_LOCAL_PROPER_MATERIAL_NORMAL_AND_PHASE_SOURCE_MATCHING_V001.md | 40978c4874ea478c1ce03c7bfcaee0e8304f8bd1c80aebf0742282266209b64b |
| LOCAL_RECORD_FEEDBACK_DYNAMIC_MEMORY_COUNT_COMMON_METRIC_ACTION_V001.md | 522a6098bfb28339e64bfd4a4469dec990258e61ed0192afc0804ca5c8d7e4b9 |
| CROSS_U_EPS5_FLRW_GALAXY_JUNCTION_V001.md | baa25990f0b2d4ca925e1a74fb65b40c2968890bd552e9f64541e620e07c6965 |
