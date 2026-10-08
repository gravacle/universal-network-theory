# S_cross general metric orbits and FLRW time dependence V001

2026-10-06 UTC. AUTHOR_DRAFT=True. Static analytical continuation pending root/peer review. No metric, Christoffel symbol, orbit, field/operator, source, trajectory or observational score has been numerically evaluated. The existing ordinary metric coupling, same action and all historical readouts/dispositions remain unchanged. This derives the full orbit equations, not a completed galaxy metric, physical preparation or FLRW junction.

## 1. Full metric, ordinary coupling and observer

Use the accepted +shift sign, signature -+++, seconds t, meridional length coordinates x^A=(R,Z), and angle phi. Let i=(A,phi), with every coefficient axisymmetric but possibly time dependent:

    ds^2=-N^2 c_p^2 dt^2+h_ij(dx^i+beta^i dt)(dx^j+beta^j dt),
    g_ti=h_ij beta^j, g_tt=-N^2 c_p^2+h_ij beta^i beta^j,
    n=N^-1(partial_t-beta^i partial_i), n.n=-c_p^2.             (1)

N>0 and h is positive definite. Meridional shifts beta^A and spatial h_Aphi are retained; no circularity/block-orthogonality theorem is imposed on a general axisymmetric state. The retained S_ordinary[g] gives neutral pressureless freely falling tracers u^mu nabla_mu u^nu=0. Pressure, electromagnetic forces or velocity dispersion require the actual ordinary Euler/kinetic equations; native stress acts through the SAME metric, not an additional tracer force.

For w^i=dx^i/dt and timelike proper time tau, the normal-observer spatial velocity and normalization are

    v^i=(w^i+beta^i)/N, v^2=h_ij v^i v^j<c_p^2,
    Gamma=(1-v^2/c_p^2)^-1/2, u^t=Gamma/N,
    u=Gamma(n+v^i partial_i).                                (2)

Put rho_c=sqrt(h_phiphi)>0 and e_phi=partial_phi/rho_c. The signed velocity projection on the axial unit vector is v_parallel=h_phi_i v^i/rho_c; the complementary meridional speed satisfies v_perp^2=v^2-v_parallel^2. These projections, not just coordinate dphi/dt, define the local rotation measured by the specified normal observer. Other emitter/observer tetrads require their actual Lorentz transformation.

## 2. Geodesic evolution from all metric derivatives

For W^mu=(1,w^i), dots now mean d/dt along the worldline. From the full affine geodesic equation,

    Gamma^alpha_munu=(g^alpha lambda/2)
       (partial_mu g_lambda nu+partial_nu g_lambda mu
                                      -partial_lambda g_munu),
    dot w^i=-Gamma^i_munu W^mu W^nu
                       +w^i Gamma^t_munu W^mu W^nu,
    d ln u^t/dt=-Gamma^t_munu W^mu W^nu.                      (3)

The t index is the seconds coordinate, with its own dimensional Christoffel components. Equation(3) includes g_tA, spatial connections, explicit partial_t g and radial/vertical motion. It is the applicable massive-tracer initial-value system on a supplied evolving metric. The same coordinate-time form holds for a null geodesic where t is a valid monotone parameter, with null normalization and a separate affine/frequency variable.

Axisymmetry preserves L=u_phi for a geodesic even when the metric evolves. A stationary timelike Killing field also preserves E=-u_t; without stationarity,

    d(-u_t)/d tau=-(1/2) partial_t g_munu u^mu u^nu.            (4)

No constant Killing energy, instantaneous potential minimum or circular velocity can replace (3) in a general time-dependent state.

## 3. Exact stationary coordinate circles, including meridional shift

A stationary constant-x^A worldline has w^A=0 and constant Omega=w^phi. Define, at held Omega,

    D=g_tt+2Omega g_tphi+Omega^2 g_phiphi<0,
    J=g_tphi+Omega g_phiphi, M_A=g_At+Omega g_Aphi.

Then u^t=c_p/sqrt(-D). For a stationary axisymmetric metric, the independent meridional equations reduce exactly to

    partial_A D=0, A=R,Z.                                    (5)

One radial root is insufficient without the vertical condition, future timelikeness, and any needed stability test. Equatorial reflection can supply the vertical condition. Even nonzero stationary g_tA/g_Aphi does not create a separate term in (5): their contracted covariant momenta are constant along this orbit. They still enter g_tt/g_tphi, the normalization, full stability problem and observer velocity. If g_phiphi,R is nonzero,

    Omega_+-=(-g_tphi,R +- sqrt(g_tphi,R^2
                              -g_tt,R g_phiphi,R))/g_phiphi,R.

Use (5) without division in the degenerate case. Real roots need D<0; stability requires the separate geodesic/held-Killing-invariant perturbation equations, not the radial discriminant alone.

For this coordinate circle, normal-observer v^A=beta^A/N and

    v_parallel=[h_phi_A beta^A+h_phiphi(Omega+beta^phi)]
                                                    /(N rho_c). (6)

A coordinate circle is therefore not necessarily a zero-meridional-velocity orbit relative to n. If beta^A=0 and h_Aphi=0, (6) becomes the old exact v_ZAMO=rho_c(Omega+beta^phi)/N, with no sign or unit change.

## 4. Instantaneous circular balance in an evolving metric

Consider constant x^A but allow Omega(t). Define D,J,M_A as above and f=d ln u^t/dt. On that candidate circle all partial_t derivatives below hold x^A and Omega fixed, so

    f=-(partial_t D+2J dot Omega)/(2D),
    partial_t M_A+g_Aphi dot Omega+f M_A=(1/2) partial_A D,
    partial_t J+g_phiphi dot Omega+f J=0.                     (7)

These are the meridional Euler-Lagrange and conserved axial-momentum equations; the t equation follows from them and normalization. Equivalently, (3) requires Gamma^A_munu W^mu W^nu=0 and dot Omega=-Gamma^phi_munu W^mu W^nu+Omega Gamma^t_munu W^mu W^nu. Equation(7) is necessary at each event and gives a geodesic circle only if its equations hold along an interval with the same fixed x^A. A family of frozen radial roots must have its actual derivative dot Omega consistent with the last row; independently selecting a new root at each time is not evolution.

If g_tA=g_Aphi=0 throughout the interval, the meridional row again gives partial_A D=0 instantaneously, but the axial/time compatibility remains. General meridional shift or spatial twist adds the displayed time/normalization terms. Instantaneous radial balance does not establish a persistent orbit, adiabaticity or radial/vertical stability.

The definition of circle is also physical-coordinate dependent. Constant circumferential radius requires d rho_c/dt=partial_t rho_c+w^A partial_A rho_c=0, which is not constant x^A when rho_c evolves. For any desired surface F(t,x^A)=0, tangency and retained acceleration require

    F_t+w^A F_A=0,
    F_tt+2w^A F_tA+w^A w^B F_AB+dot w^A F_A=0.                (8)

Insert the FULL (3) in (8), along with axial evolution and the other meridional condition. Zero normal-meridional velocity is a different condition v_perp=0, not a substitute for (5),(7),(8).

## 5. Recovery of the existing static diagnostic

For beta^A=h_Aphi=0, beta^phi=0, N=exp(Phi) and h_phiphi=R^2 exp(-2Psi), (5),(6) give exactly

    v_ZAMO^2/c_p^2=R Phi_R/(1-R Psi_R).                       (9)

For general static h_phiphi this is v^2/c_p^2=d ln N/d ln rho_c where the undivided equation is nondegenerate. With only an axial shift retained, the old exact contact is

    v^2 partial_R ln rho_c+(rho_c/N)v partial_R beta^phi
                                           =c_p^2 partial_R ln N.

The leading weak limit v_N^2=c_p^2 R Phi_R is the saved Newtonian/Q1 diagnostic. All historical slopes, signed readouts, scores and failures remain preserved; they are not promoted to a physical final prediction. Exact orbit readout uses a solved full metric and its derivatives. The existing constructed stationary odd metric qualifies only that specific conditional geometry, not an evolving FLRW/retarded galaxy.

## 6. FLRW matching, retarded state and observation

For illustration of coordinate/observer bookkeeping only, flat FLRW with areal R=a(t)r has ds^2=-c_p^2dt^2+(dR-HRdt)^2+R^2dOmega_2^2. Thus beta^R=-HR and N=1. A constant-areal-R candidate has normal radial velocity -HR, whereas a comoving tracer has dot R=HR and zero normal radial velocity. This is a coordinate identity, not an adopted galaxy exterior or a proof that the candidate is a geodesic circle. Its metric time derivatives/meridional shift must enter (3),(7); no extra hand-added Hubble force is required.

A physical shared-law evolving prediction needs the actual S_cross metric/U/phase/mode and ordinary state, the retained retarded radiation/history variables, initial constraints, and consistent metric/current/extrinsic outer matching. The qualified homogeneous EPS1e5 background does not supply a mature galaxy Cauchy state, matched temporal inertias or its exterior/homogeneous metric modes. The conditional EPS1e6 manufactured perturbation histories do not transfer as that state. Small H R/c_p alone does not certify adiabaticity of a near-null or slowly responding native/clock branch.

If there is no compatible timelike circular solution, or time changes/radial motion/ordinary pressure invalidate the supplied circular approximation, integrate (3) or the appropriate ordinary dynamics with declared initial data. An adiabatic circular approximation requires its explicitly checked orbital/metric/material-response time hierarchy and controlled radial drift. A frozen metric is a declared approximation; a sequence of frozen snapshots is not automatically the retarded solution.

The measured photon shift uses (-k.u)_emitter/(-k.u)_observer along a null geodesic of the SAME metric; comparison with tabulated rotation additionally retains distance, inclination, optical radius, observer and tracer-motion registration. No Vobs, fitted projection, native stress force, missing state or metric boundary is selected here. Q1/weak-sheet metric derivatives require their actual one-sided/interface prescription and convergence controls; a smoothed lapse slope is not a complete Christoffel certificate.

## Actual read-only inputs

The following actual bytes were read and hashed before and after exclusive creation; no input was modified or executed.

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md — b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5
- CROSS_U_EVEN_SPATIAL_METRIC_WEAK_RESIDUAL_AND_COMPATIBILITY_V001.md — 9cc67c01fd4d9227e80514fed699ef92e57d917723015fb7e51b58e3f7301451
- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md — 6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b
- CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md — c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986
- CROSS_U_EXACT_RETARDED_RADIATION_MOMENT_OPERATOR_V001.md — c4fcedb21d45274bc6632b755e87c6eacf566f5d84268d103e625990bc299752
- NATIVE_TO_CROSS_PHASE_COEFFICIENT_CURRENT_AND_STRESS_MATCHING_V001.md — d95ad4155144f102243e14082faf1e5b6b7b193eef0c753c88864534ec302d40
- CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001.md — f511db085e290e3287902e20f9e0eb9cf2679febc4a9af01061f30f10068645b
