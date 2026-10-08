# Rotation-capable material clock and source extension V001

2026-10-06 UTC. AUTHOR_DRAFT=True; exclusive analytical extension held for root and distinct review. No operator, numerical function, state, source, metric, history or trajectory is evaluated or selected. This replaces ONLY the hypersurface-orthogonal material kinematics of the pinned 126-line candidate. Its H_reg, endpoint allocation, one joint Berry term, proper h=.2 and all first/second acceleration jets are retained. Signature(-+++); c_p=1 in the material equations, with seconds and c_p explicit in the orbit equations.

## 1. Independent rotating flow and proper clocks

A material velocity u_M=-raised(dT)/Q_M is hypersurface orthogonal. Replace that restriction by an independently varied future unit timelike u_M, distinct from the independent shared-action U. On its registered material worldlines and labels use

    u_M^2=-1, dz^mu/dlambda=e0 u_M^mu(z), e0>0,
    d tau_M=e0 dlambda, u_M^mu partial_mu X^I=0.               (1)

The unit equation implies e0=sqrt(-g z_dot z_dot). Rest planes may have vorticity P_M P_M nabla_[mu u_M,nu]!=0. Three advected labels do not require these rest planes to form hypersurfaces. For example, a timelike circular flow proportional to partial_t+Omega(R,Z)partial_phi advects (R,Z,phi-Omega(R,Z)t); this is a symbolic kinematic example, not an adopted galaxy flow. Proper age along a flow is different from a scalar whose gradient defines that flow.

No global quantum time slicing is derived from u_M. One finite cluster retains its registered reference chronology and one joint ket. A many-cell extension retains one inclusive Hamiltonian and unique energy allocation on its supplied chronology, with the actual proper-rate conversion for each material support. It cannot introduce one copy of the global Berry term per cell, assume product preparations, or identify the FLRW normal, material u_M, independent U and phase v_phi without a supplied constraint and its reaction.

## 2. Worldline clock variation keeps the same energy function

Keep the candidate S_q and its faithful D_lambda connection exactly. A first-order worldline representation can use independent e0,z,u_M and momentum/constraint multipliers:

    S_link=integral dlambda [p_mu(z_dot^mu-e0 u_M^mu(z))
                                      +e0 lambda_M(u_M^2+1)/2].           (2)

This enforces (1) rather than postulating u_M from dT. In the clock block, -e0<H_reg> and the existing scalar constraint phases remain in S_q. Vary e0 before imposing those constraints. On their algebraic constraint surface, absent an additional e0-dependent contact, the clock row gives p.u_M=-<H_reg>; otherwise use the complete delta(S_q+S_link+S_frame+S_ports)/delta e0=0. Momentum and clock reactions are solved by this same action; no new rest-energy law, mass function or force gain is supplied. The coordinate state generator remains e0[H_reg+j_A Q_A+P nu n_hat], together with the already owned connection and scalar phases.

The worldline representation and the weak Eulerian description below are registrations of the SAME material constraint, with their measure/support accounted for once. Do not append their energy or unit reaction twice. Vary the actual material measure, V[g,X], embedding, endpoints, frame, maps, proper-rate factors and reference support before restriction to a solved orbit or frame.

## 3. Independent material Euler row and optional age coordinate

In a weak Eulerian chart let W_M,mu be the bare material-velocity Euler vertex after integrations by parts, including all actual Berry/frame/encoder/map/support terms but excluding the displayed unit and label multipliers. The unit/advection action is represented as integral sqrt(-g)d^4x[lambda_M(u_M^2+1)/2+zeta_I u_M.partial X^I]. All weak vertices and multipliers in (3)-(7) denote coefficients against sqrt(-g)d^4x after absorbing the supplied material measure; distributional worldline support is handled weakly without dividing by it. Where dmu=w sqrt(-g)d^4x has smooth positive w, an equivalent UNdensitized scalar row uses w^-1 nabla_mu(w zeta_I u_M^mu), and likewise for the age reaction. Vary the actual w/support/embedding before imposing constraints; no measure or volume-work term is discarded. Its rows are

    W_M,mu+lambda_M u_M,mu+zeta_I partial_mu X^I=0,
    P_M^(nu mu)(W_M,mu+zeta_I partial_mu X^I)=0,
    E_I=E_I,bare-nabla_mu(zeta_I u_M^mu)=0.                 (3)

The normal contraction fixes lambda_M; the projected row is the material force/transport equation. It is not automatically a geodesic equation, nor an independently added acceleration force. Where an independent worldline embedding is retained, its own Euler row and support contacts also remain.

An OPTIONAL scalar age s may be attached through p_s(u_M.partial s-1), with no identification u_M=-ds/|ds|. Then

    u_M.partial s=1,
    E_s=E_s,explicit-nabla_mu(p_s u_M^mu)=0,
    W_M,mu+lambda_M u_M,mu+zeta_I partial_mu X^I
                                            +p_s partial_mu s=0.        (4)

This age equation is not the old gradient-normal chain E_T=nabla(P_M W_M/Q_M)+E_T,explicit. If no age scalar is used there is no such E_T row: proper-clock variation is the worldline/reparametrization row in (2). Neither choice creates the conserved phase I0 or turns record formation into a phase-charge source. No age zero, duration or incoming history is selected here.

## 4. The retained triad can be transported along a rotating material flow

The existing triad is transverse to U, not necessarily to u_M. Retain its unit/orthogonality multipliers and the same no-extra-rotation transport rule, now along the independent material flow:

    D_M=nabla_(u_M), e_I.U=0, e_I.e_J=delta_IJ,
    D_M e_I^mu=U^mu(e_I.D_M U).                            (5)

Equation(5) preserves both triad constraints on shell even when u_M has vorticity. It defines a U-rest triad carried by the material flow; it is not silently a u_M-rest endpoint embedding when u_M!=U. That physical embedding/relative boost, if claimed, is a supplied part of the same candidate. Additional physical rotation/strain is not fabricated by changing frame gauge. A basis rotation transforms the joint state, operators, connection and preparation together.

For the transport multiplier A_I,mu of the candidate, its explicit material vertex and derivative momenta include

    W_M,alpha,transport=sum_I A_I,mu[nabla_alpha e_I^mu
                             -U^mu e_I,nu nabla_alpha U^nu],
    Pi_eI^alpha{}_beta=u_M^alpha A_I,beta,
    Pi_U,transport^alpha{}_beta=-u_M^alpha
                                      sum_I(A_I.U)e_I,beta.              (6)

Retain their weak connection/boundary ports, metric lowering and constraint/measure variations. The acceleration contribution Pi_U^alpha{}_beta=U^alpha b_beta and the candidate's complete acceleration Hilbert improvement remain unchanged; (6) adds the actual transport rows rather than deleting them by an on-shell frame substitution. The same H_reg and Kubo-minus-Born contacts are used without another endpoint lapse or force multiplier.

## 5. Ward identity with two independent timelike fields

For complete Euler vertices, after accounting for the registered weak/worldline measure, the common-source identity is

    nabla_mu T^mu{}_nu=E_I partial_nu X^I
      +sum_(A=M,U)[W_A,mu nabla_nu u_A^mu
                               +nabla_mu(u_A^mu W_A,nu)]
      +sum_I[W_eI,mu nabla_nu e_I^mu
                               +nabla_mu(e_I^mu W_eI,nu)]
      +E_s partial_nu s (ONLY if s is included)
      +actual state/embedding/map/encoder/port/support/boundary Euler terms. (7)

Here u_U=U. W_A includes the solved unit, advection, clock and transport reactions appropriate to the chosen representation. Equation(7) replaces the scalar-normal material term E_T dT; it cannot omit the independent u_M vertex. The total on-shell divergence vanishes only when all included sectors and ports satisfy their rows. The lambda_M u_M^mu u_M^nu stress, proper-clock energy, scalar phases, frame/metric derivative terms and material-volume contacts are part of one full Hilbert variation, not separately assigned matter energies. Existing donor/count conservation, return/Gauss energy and phase/current matching remain once-only.

## 6. A rotating readout needs the evolving metric or actual material Euler law

The native/material flow follows (3) or its full worldline Euler equations. Neutral freely falling ordinary tracers of the retained minimal metric action obey u^mu nabla_mu u^nu=0; pressure, electromagnetic and support forces retain their actual equations. Identifying an observed tracer with u_M requires the corresponding matter registration, not a new force inferred from q_dot. For a supplied full axisymmetric metric use the frozen orbit convention

    ds^2=-N^2 c_p^2 dt^2+h_ij(dx^i+beta^i dt)(dx^j+beta^j dt),
    W^mu=(1,w^i), w^i=dx^i/dt,
    dot w^i=-Gamma^i_munu W^mu W^nu
                              +w^i Gamma^t_munu W^mu W^nu,
    v^i=(w^i+beta^i)/N, h_ij v^i v^j<c_p^2.                (8)

All time, radial, vertical, shift and spatial-twist derivatives are retained. For a candidate constant-x^A circle with Omega(t)=w^phi, define D=g_tt+2Omega g_tphi+Omega^2 g_phiphi<0, J=g_tphi+Omega g_phiphi and M_A=g_At+Omega g_Aphi. Partial_t below holds x^A and Omega fixed. The complete dynamic circle conditions are

    f=d ln u^t/dt=-(partial_t D+2J dot Omega)/(2D),
    partial_t M_A+g_Aphi dot Omega+f M_A=partial_A D/2,
    partial_t J+g_phiphi dot Omega+f J=0.                  (9)

They must hold along the same interval, with vertical balance and timelikeness; a sequence of frozen radial roots is not a trajectory. For a constant circumferential radius or other evolving surface F(t,x^A)=0, also require F_t+w^A F_A=0 and F_tt+2w^A F_tA+w^A w^B F_AB+dot w^A F_A=0 using (8). The measured axial projection is h_phi_i v^i/sqrt(h_phiphi); emitter/observer photon shifts use (-k.u)_em/(-k.u)_obs in that same metric. No static v^2 recipe, SFR normalization or stress multiplier replaces these equations.

This extension removes the unnecessary irrotational restriction without altering the candidate energy or fixed EPS1e-5 law. The accepted finite-history continuum result establishes finite forced response for admissible incoming data; it does not choose a physical inertia, state, duration, full exterior or source history. No microscopic unit, prepared proper h=.2 state, field, observation or velocity shift is supplied here, and the old h=.1 arithmetic evidence remains distinct.

## Exact actual inputs

All paths are relative to J. Complete bytes were read and checked before and after exclusive creation; none was executed or modified. The 126-line parent is still a held candidate; its 125-line ancestor and the other listed inputs are protected resident bytes.

| Input | SHA256 |
|---|---|
| NATIVE_PROPER_BOND_COVARIANT_ACCELERATION_MATERIAL_LIFT_CANDIDATE_V001.md | af1fab1ab22cc9cac29582348a7eaeb89309ba09a230ff0ed7067d1e778b7cd2 |
| reviewed_NATIVE_PROPER_BOND_COVARIANT_ACCELERATION_MATERIAL_LIFT_CANDIDATE_V001_125_2e2e6430.md | 2e2e643078df75087e4cc5cf08e906b9d264077c316bfebd00869024b1beddf5 |
| CROSS_U_GENERAL_METRIC_ORBIT_AND_FLRW_TIME_DEPENDENCE_V001.md | b3fd1355c03ed78cb702844cb05e34accb9e51d648d89c21db1bafd47dfcef59 |
| NATIVE_LOCAL_PROPER_MATERIAL_NORMAL_AND_PHASE_SOURCE_MATCHING_V001.md | 40978c4874ea478c1ce03c7bfcaee0e8304f8bd1c80aebf0742282266209b64b |
| CROSS_U_FINITE_HISTORY_CONTINUUM_RESPONSE_V001.md | b2e1a6401444a642b47efa0548b89db36c84aea36fd75da4655e9350ddda6ac8 |
| reviewed_NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001_109_aab65a5c.md | aab65a5c2036ed8264a63f0451ab1e400c0f58b543db0e91bb2a1e178f70c9d2 |
