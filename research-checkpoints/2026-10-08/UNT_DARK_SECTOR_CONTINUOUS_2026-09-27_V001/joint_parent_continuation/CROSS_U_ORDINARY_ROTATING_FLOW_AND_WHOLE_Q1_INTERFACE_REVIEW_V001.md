# Ordinary rotating flow and whole-Q1 interface review V001

2026-10-07 UTC. AUTHOR_DRAFT=True; concise root-requested static implementation review, held for review. No producer, helper, operator, field, inverse, solve or evolution was evaluated for this note. The completed separately authorized saved-only EH diagnosis is preserved unchanged. Signature(-+++), geometric c=1 in the canonical equations; the frozen geodesic component retains seconds and c_p explicitly. EPS1e-5, all32 modes, all four sigma arms, mass/current and old outcomes remain unchanged.

## 1. Rotating ordinary material is independent of native U

The current canonical source has no hidden u_M=-raised(dT)/Q restriction. Its `ordinary_velocity` accepts all three spatial covariant particle momenta; see `cross_u_saved_full_native_adm_constraint_sources_v002.py:465` and the prospective Q1 copy `cross_u_whole_slice_q1_adm_residual_v001.py:246`. The Q1 `source_projection` at line745 assigns p_R=p_Z=0 only as the existing disclosed annular initial seed and retains each authenticated p_phi and rest-mass weight. A radial-dependent p_phi dphi need not be a closed one-form, so this seed is not an irrotationality condition. Native U_i, ordinary particle p_i and phase flow are different variables.

The metric-minimal ordinary sector of S_cross gives, per unit rest mass,

    Gamma=sqrt(1+h^ij p_i p_j), H_o=N Gamma-beta^i p_i,
    xdot^i=N h^ij p_j/Gamma-beta^i,
    pdot_i=-Gamma partial_i N-(N/2Gamma)(partial_i h^jk)p_j p_k
                                      +p_j partial_i beta^j.             (1)

These are the full metric geodesic Hamilton equations, not a Newtonian force rule. For an axisymmetric metric pdot_phi=0, including when the metric evolves. Neither pdot_R/Z=0 nor fixed material positions follows. Zero initial p_R/Z also does not guarantee zero coordinate meridional velocity when h_Aphi or beta^A is present. Advect the same ordinary rest-mass coordinate measure D_M by partial_t D_M+partial_i(D_M xdot^i)=0, or push forward the same discrete annular labels/worldlines. No extra volume density, finite height, pressure or dispersion is inferred from this sheet. Actual interacting gas follows its supplied Euler/Lorentz/kinetic stresses instead of the neutral-dust specialization.

For the prospective quantum material realization the independently rotating u_M instead satisfies the projected complete W_M/label/transport/clock equations, with its reactions and embedding retained: accepted rotation extension sections1--5 and explicit Euler addendum Eq(3)--(6). This is not a direct extra force on the metric-minimal ordinary tracers, nor a reason to identify u_M, U and the FLRW normal. A full effective S_cross evolution does not require inventing a microscopic writer gain or a new EOS.

## 2. Source allocation and the actionable metric-update interface

The present Q1 source projection correctly deposits `mass_weight*Gamma` and `-mass_weight*p_i` into the actual sheet hats at the frozen sample locations (line745); its Q1 partition/location check is at line793. The inherited half-domain/azimuth normalization is already in mass_weight and is counted once. Its current use of the immutable `source_g` is valid for the same instantaneous trial, whose owned-H continuation changes time jets, not metric positions.

For a future metric Newton step, preserve mass, positions on that initial slice and p_phi as declared Cauchy data, evaluate the CURRENT metric at those positions, and reconstruct Gamma/u_M/coordinate velocity from(1). Do not retain the old source_g or Omega after changing the metric. After a time step evolve positions and p_R/Z by(1), retain axial p_phi, and push forward the same measure; held annular radii are an initial-data choice, not a causal evolution law. A CMC constraint projection alone does not solve these ordinary evolution equations or establish circular flow.

The exterior ordinary labels and the measured annuli must belong to one once-counted baryon assignment. The owned homogeneous EPS5 means do not determine the condensed spatial pushforward or perturbed photon distribution. Adding homogeneous dust over the annuli without declaring whether they are excess or total matter can duplicate baryons. Retain actual ordinary angular momentum/current/traction at an interface; no zero exterior current is inferred from absent activity measurements.

## 3. Exact velocity readouts depend on stationarity

In a stationary axisymmetric full metric, a constant-R,Z neutral circle requires BOTH held-Omega partial_A D=0 for A=R,Z, where D=g_tt+2Omega g_tphi+Omega^2 g_phiphi<0. Use the undivided radial equation when its quadratic denominator vanishes, retain both real branches and timelike/future tests, and require vertical/reflected-sheet balance. Derivatives do not differentiate Omega(R,Z) through this force partial. Stability needs its separate fixed-Killing-energy/angular-momentum variation. The stationary registration's Eq(2)--(4) owns these statements; neither a radial root alone nor a source seed proves an orbit.

The owned-H seed has nonzero hdot and is not a time-Killing solution. For evolving geometry use the exact full geodesic ODE in `cross_u_full_metric_geodesic_and_rotating_material_v001.py:91`, with its finite/timelike ADM and normal-observer tests. Constant-coordinate circles are admissible only if the time, radial, vertical and angular rows hold along the same interval. In the accepted [rotation extension Eq(9)](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001.md:89>), J=g_tphi+Omega g_phiphi, M_A=g_At+Omega g_Aphi and

    f=-(partial_t D+2J Omegadot)/(2D),
    partial_t M_A+g_Aphi Omegadot+f M_A=partial_A D/2,
    partial_t J+g_phiphi Omegadot+f J=0.                                (2)

All displayed partial_t derivatives hold Omega fixed. Fixed p_phi determines evolving Omega through the current metric; it does not hold Omega fixed. Full circumferential-surface motion needs its additional kinematic conditions. Final physical velocities use the calculated full metric, complete geodesic/material motion and observer/null transfer; the axial normal projection is h_phi_i v^i/sqrt(h_phiphi), with v=(w+beta)/N. No Newtonian readout or activity-to-force multiplier substitutes for this pipeline.

## 4. Prospective Q1 assembly review and exact EH scope

At the inspected 926-line draft boundary SHA127d0a1f5fa6b138b7601e6c02b807ec2104febdad9174eaa7a783d181611363, `cross_u_whole_slice_q1_adm_residual_v001.py` remains guarded/in progress with future whole-parent seals unset; this is a prospective implementation review, not final byte admission. Its coefficient/scatter methods at lines723--743 and851--875 use genuine Q1 values/R/Z derivatives for the four ADM directions. `owned_response` at line815 preserves all99 native coordinates/momenta including azimuthal components and discloses pointwise mixed time jets rather than claiming a nodal Q1 velocity field. No irrotational material restriction is introduced there.

For the actual diagonal axisymmetric trial and spatially constant H, the meridional isotropic EH contribution is exactly pi_H:Lie_b h=-(2H/C)div(sqrt(h)b). Old rotating Rphi/Zphi momentum does not contract an axisymmetric meridional test. The sealed saved-only diagnosis confirms this identity on every stored arm/column/box/direction and preserves the original signed rows. The shared-face/incidence implementation `conservative_H_faces` at line759 is a correct way to telescope this KNOWN divergence for genuine compact interior hats; it is not a background-pressure subtraction or an accuracy claim for all EH/native terms. Keep its original Q2 row, face representative and alias separately as the draft does at line884.

`restrict_rows` at line710 implements diagnostic axis/parity and compact outer TEST restrictions, not new physical wall values. The face boundary flux remains an actual separate quantity. Continuous Q1 internal faces and the reflected sheet belong to the global weak action once; do not append a second synthetic jump. A future field solve must register either quadrature canonical variables in a mixed discretization or a consistent nodal Legendre/mass projection and save the compatibility residual. This residual inventory still lacks the CMC-preservation evolution row, physical exterior and constraint solution; its four ADM rows must not be promoted into a completed five-field solve.

## 5. Physical boundary and immediate continuation requirements

Activity is established only on0.3--15.1kpc; outside remains unknown. The endpoint15.1kpc is neither the galaxy edge nor a homogeneous FLRW junction, and the computational128kpc wall is not physical exterior data. Preserve the entire authenticated ordinary support. An admitted worldtube needs compatible induced metric/extrinsic curvature, phase charge flux, all32 native/U conormals, ordinary material/radiation current and traction, angular momentum and the same Ward/constraint balance. A monopole/angular-momentum perturbation is not erased by joining straight to pure FLRW. A conditional retarded/no-independent-incoming branch additionally needs the actual boundary history and admissible exterior state; it does not supply missing history automatically.

The next usable step is the guarded whole-Q1 weak residual inventory with its complete current source and conservative EH split. Before a metric correction, finish the same-action CMC/free-data and exterior operator registration, obtain the consistent constrained Jacobian, and update ordinary source velocity by fixed canonical momentum/current metric. Before any physical rotation prediction, evolve the coupled metric/native/phase/ordinary system or establish a genuinely stationary branch, then evaluate full geodesics and radial/vertical balance. These are implementation requirements, not a new parameter, prepared history, numerical worker or claimed physical result.

## Actual protected inputs

Complete actual bytes were read and hashed. The draft boundary above is explicitly mutable; all following inputs were0444 and unchanged before/after this note's creation. Paths are relative to J.

| Input | SHA256 |
|---|---|
| NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001.md | e8911d59ae25f9d397a57a6dcd6d0ca5c450df82566935c00f8436568f7484ff |
| NATIVE_ROTATING_MATERIAL_EXPLICIT_EULER_AND_METRIC_PORT_CLOSURE_V001.md | 161781870e4615825486f4df6cfb1406a6d248a9f79cb10ef31406a8b64cf4e9 |
| CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md | b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5 |
| CROSS_U_EPS5_CANONICAL_CMC_GRID_CONTINUATION_PLAN_V001.md | d398cd98d5d8710066c42025d4e85e7f2ab597496fac8294f588975d3748ba2d |
| cross_u_full_metric_geodesic_and_rotating_material_v001.py | 53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa |
| cross_u_saved_full_native_adm_constraint_sources_v002.py | 1236e6b6837dd0356f7aae55bcf3d8ee4ed0ce3b4530907580990430e021d880 |
| ROOT_AUTHORIZED_SAVED_EH_COMPACT_DIVERGENCE_DIAGNOSIS_V001_RESULT.json | 19f40f701a80082055f1827a426b0ffa28639bbb1ac20b14301852cb079f401d |
