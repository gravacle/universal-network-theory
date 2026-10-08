# Common-field two-potential closure and its exact identifiability boundary V001

2026-10-05 UTC. NEW analytical forward construction under the already adopted WTC/RGRL working law. No constitutive completion, source calibration, body profile, parameter, state or metric is selected from numerical outcomes. No calculation, producer import, source mutation or canonical-model change is authorized here. Microscopic RF3 and a junction-dilation law are not prerequisites for using the adopted effective law. The finite bulk NN block remains a modeled-network contribution, not the complete gravitational polarization.

## 1. The leading common action, with signs fixed

Use the common proper chart and the weak, static, zero-shift scalar metric

    ds^2 = -(1+2 eta)c_p^2 dt^2 + (1-2 psi) delta_ij dx^i dx^j,
    eta=Phi/c_p^2, psi=Psi/c_p^2.                              (1)

The following is the static-energy variational convention. On the owned boundary/gauge quotient, the leading Einstein scalar functional is

    Gamma_g = c_p^4/(8 pi G_obs) integral d^3x
                  [2 grad eta dot grad psi - |grad psi|^2].    (2)

The factor two in the mixed term is essential. Varying a nonrelativistic source term integral rho c_p^2 eta gives

    laplacian psi = 4 pi G_obs rho/c_p^2,
    laplacian(eta-psi)=0.                                     (3)

With the same boundary values and negligible additional spatial/anisotropic source, psi=eta and laplacian Phi=4 pi G_obs rho. Thus a positive mass produces negative Phi with the usual zero-at-infinity convention. Equation(2) reduces to +c_p^4 integral |grad eta|^2/(8 pi G_obs). Its negative psi-constraint block is not a mechanical shear instability or a proposed repair of the five preserved negative charging directions.

For prospective proper basis functions f_i(x)=fbar_i(x/ell0), let Sbar_ij=integral d^3xbar grad fbar_i^* dot grad fbar_j. Divide the static functional by Eunit and set

    alpha_g = 4 pi G_obs Eunit/(c_p^4 ell0),
    k_g = alpha_g^-1 Sbar,
    K_g = [[0,k_g],[k_g,-k_g]].                               (4)

Here k_g is a positive operator on the nonzero admitted modes, not a fit to the measured NN eigenvectors. The physical interpolation, volume weights, boundary prescription and proper chart that define Sbar remain part of the declared WTC matching. Bare graph adjacency does not define Sbar by itself. One globally counted alpha_g may remain symbolic; neither parameter-free G nor a new RF3 gate is imposed.

## 2. Proper phases and a normalized physical body

For a disclosed ideal tetrahedral L3 chart, take unit vectors u0=(1,1,1)/sqrt3, u1=(1,-1,-1)/sqrt3, u2=(-1,1,-1)/sqrt3, u3=(-1,-1,1)/sqrt3. The native A(r)-B(r+s_a) links have positions

    x_A(r)=ell0 sum_(i=1..3) r_i (u_i-u0),
    x_B(r)=x_A(r)+ell0 u0,
    K dot ell0(u_i-u0)=2 pi k_i/3.                            (5)

This is a declared common-chart specialization, not an inference of proper distance from the L3 graph. For the seven resident modes k=0,+/-e1,+/-e2,+/-e3, define the scalar nodal mode f_k(v)=exp(i K dot x_v)/sqrt54. Relative to the saved sublattice Fourier normalization 1/sqrt27, its source column is a_k=(1,exp(i K dot ell0 u0))^T/sqrt2. Therefore the measured scalar plane contraction is

    r_plane(k)=a_k^dagger R_NN(k) a_k
              =u_k R_NN(k) u_k^dagger/2,
    u_k=(1,exp(-i K dot ell0 u0)).                            (6)

All seven modes and both sublattice energy channels remain. This phase prescription selects a physical source shape, not an observed favorable eigenchannel. Real fields obey eta_-k=eta_k^*. Sum the full +/- census with the standard quadratic factor 1/2; alternatively use sqrt2 Re f_k and sqrt2 Im f_k. Do not introduce another half for the paired real convention.

An imposed body's minimal common-metric insertion is the already permitted proper point-particle action S_body=-M c_p integral ds. To first static order its Hamiltonian/source is M c_p^2 eta(x_body). On a declared coarse body profile p_v with sum_v p_v=1, the dimensionless Fourier load is

    j_eta(k) = (M c_p^2/Eunit) sum_v p_v f_k(v)^*.             (7)

A point profile is p_v=delta_(v,v_body); a resolved profile and its proper-volume weights must instead be fixed independently. Equation(7) is inertial body-energy normalization, not a noisy sample of the homogeneous environmental energy. The mean component is real physical energy/source work. A periodic contrast calculation must declare its mean background/constraint convention; it cannot silently remove the body's mass. An isolated-body calculation requires its corresponding physical boundary prescription.

At this linear weak-field ceiling a prescribed static dust T00 and its declared source are available under WTC. A holding apparatus, nonlinear reaction stress, body preparation or source translation must carry their full additional stress/work if included. Homogeneous q1/Nc0 data contains no such nonuniform body J(k) and supplies neither a body history nor a profile calibration. It can supply environmental response to a separately declared source.

## 3. Exact retained constraint and connected energy

At one real scalar plane, or as operators with the displayed order retained, let the owned matched environmental completion be [[R,b],[b^dagger,d]]. With the two-potential field column (eta,psi), write

    Gamma2/Eunit = 1/2 (eta,psi)^dagger
                 [[R,k_g+b],[k_g+b^dagger,-k_g+d]] (eta,psi)
                 + Re(j_eta^dagger eta+j_psi^dagger psi).      (8)

The actual R must have the same source/state/matching convention as b,d and both source columns. Let C=k_g-d and assume an owned inverse on the specified constraint quotient. Then

    psi = C^-1[(k_g+b^dagger)eta+j_psi],
    K_eff = R+(k_g+b)C^-1(k_g+b^dagger),
    j_eff = j_eta+(k_g+b)C^-1 j_psi,
    Gamma2,eff/Eunit = 1/2 eta^dagger K_eff eta
                   + Re(j_eff^dagger eta)
                   + 1/2 j_psi^dagger C^-1 j_psi.             (9)

The last term follows from eliminating a negative constraint block. It is positive when C>0 and belongs to connected energy. For an owned invertible K_eff, eta=-K_eff^-1 j_eff; the stationary functional is -j_eff^dagger K_eff^-1 j_eff/2+j_psi^dagger C^-1 j_psi/2. Two prescribed body loads have the cross term -Re(j_eff,1^dagger K_eff^-1 j_eff,2)+Re(j_psi,1^dagger C^-1 j_psi,2), with the same complete reference/source convention. Source-dependent K,b,d and body profiles also contribute their actual first/second contacts to forces. This expression is not a force-versus-separation law until those sources and positions are owned.

The more general retained field y has the same action-level reduction A-B D^-1 B^dagger and J_eta-B D^-1 J_y, with -J_y^dagger D^-1 J_y/2 retained. A causal prepared reduction uses its ordered retarded operators, initial/boundary forcing and actual contacts; it is not the static equation(9). Current finite-beta NN data does not determine the mixed/spatial block b,d, j_psi, other retained fields or that causal completion.

## 4. Reference matching counts the total G once

WTC-H3 defines complete stress once, including fast, matching and retained terms. WTC16 fixes the matched TOTAL Ricci coefficient 1/(16 pi G_obs), without a microscopic decomposition. Hence adding the full measured R_NN to a gravitational action already calibrated including that contribution would double count.

One legitimate explicit split is Gamma_match=Gamma_EH,total(G_obs)-P_(0,2) Gamma_ret,ref plus the other owned matching terms, followed by Gamma_ret,state added once. P_(0,2) denotes the same prospectively specified local zero/two-derivative reference projection, not a fitted subtraction chosen after a sign failure. Its vacuum/reference energy and boundary contacts remain. An alternative is an explicitly owned complete reduced reference law plus its environmental change; the reference law must then already account for its finite-k remainder. These two conventions cannot be mixed silently.

The L3 seven-mode measurement alone does not determine a controlled zero-momentum derivative expansion or this matching projection. Its fixed-coordinate-beta uniform variance is not a Ricci coefficient and is not removed by declaring it gauge. Whole-action proper-bath rescaling is a separate source-class identity. The symbolic AR/self constants drop from connected covariance but remain in source means, background/reference energy and count work. This note chooses no numerical AR/self or vacuum counterterm.

## 5. Counterfamily: the same NN block does not determine the field

This is an algebraic identifiability witness, not a proposed physical fit. In a flat scalar plane write p=|K ell0|, k_g=kappa p^2, kappa>0. Suppose an owned reference matching has left the SAME NN remainder r(p)=O(p^4). For real constants beta,delta consider

    R=r(p), b=beta p^4, d=delta p^4, j_psi=0.
    C=p^2(kappa-delta p^2),
    K_eff=r(p)+p^2 (kappa+beta p^2)^2/(kappa-delta p^2),
    psi/eta=(kappa+beta p^2)/(kappa-delta p^2).                (10)

Every member has the same NN component r(p) and the same leading calibrated kappa p^2. Nevertheless K_eff and the ratio psi/eta change at finite p. In particular beta=0, delta unequal to zero already changes both the force kernel and the light/clock ratio. These are mixed/spatial O(p^4) completions invisible to an NN-only measurement, not changes to the matched leading G.

The exact static admissibility conditions are p>0, kappa-delta p^2>0 and K_eff>0. They make C invertible and the reduced scalar functional elliptic; the unreduced psi block remains a constraint. For example, if |r(p)|<=C_r p^4, then |beta|p^2<=kappa/2, |delta|p^2<=kappa/2 and C_r p^2<kappa/6 imply K_eff>0 by the lower bound K_eff>=kappa p^2/6-C_r p^4. A zero beta,delta or C_r omits its corresponding restriction. This is a symbolic existence domain, not an outcome-selected physical parameter window.

Arbitrary b,d are not automatically covariant metric-only realizers. A physical environmental completion needs its declared material/foliation fields, retained constraints, Ward contacts and common-probe source. Higher-derivative covariant or covariant-medium actions can supply mixed/spatial vertices, but none is adopted here, and no coefficient is inferred from this counterfamily. The finite-beta current R_NN is not assumed to be the covariant r(p) in(10). The algebra alone identifies the missing data even before a realization is selected.

## 6. One field predicts mass, clock and light

With proper inertial M, proper clock omega_p and common proper c_p fixed as the adopted working-law probes, equations(1) and(9) give, to first order,

    acceleration = -c_p^2 grad eta,
    omega_clock=(1+eta)omega_p,
    massive kinetic coefficient C^ij=hbar^2/(2M)
                                      [1+eta+2psi]delta^ij,
    Omega_light^ij=c_p^2[1+2(eta+psi)]delta^ij.                (11)

Light deflection/time delay probes eta+psi, while slow matter acceleration and static proper-clock redshift probe eta. The existing common-metric derivative residual consequently vanishes for this shared dictionary. That is a conditional WTC consequence, not a new empirical qualification of a native ladder clock, band mass or arbitrary TEM line. Complete readout/encoder/path/reference and changing-probe contacts remain when the physical probes themselves vary.

The new bulk mixed block provides the SAME-field background query response delta<Q(k)>=-chi_QE(k)a_k eta(k), for the plus additive lapse source. Bare pair/coordination queries are not automatically the qualified RGRL memory fields, and this response does not supply b,d by taking an unearned inverse. No old inverse or mixing refusal is waived.

The defensible minimal baseline is b=d=j_psi=0 with a separately owned matched R: then K_eff=k_g+R and psi=eta. Without environmental R it is simply the already adopted leading WTC field. Including measured R with this baseline is an ADDED reduced-law/retained-state/source premise. Its covariant medium/stress and reference matching must be supplied; it is not derived from q1/Nc0 homogeneous data. It cannot be called the complete action merely because all three probes are coupled to its metric.

The shortest forward calculation, once this physical datum is specified, is to evaluate(9) for an independently normalized body and the complete signed seven-mode response, reconstruct both potentials, and predict(11) and the query response together with connected energy and all source contacts. Global Eunit,ell0,alpha_g and body mass can remain counted symbolic parameters. The unavoidable decision is the complete retained/reduced constitutive block and reference matching, not an invented h_R, favorable support function, record-mass halo, arbitrary E(V) or new microscopic RF3 prerequisite. No galaxy, expansion, lensing, continuum or Stage3 closure follows from NN alone.

## Frozen resident inputs

The bulk result/receipt are sealed producer evidence. No pending acceptance artifact is invented or consumed by this analytical note. Paths are relative to joint_parent_continuation except the program-worktree row.

| Input | SHA256 |
|---|---|
| program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md | cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2 |
| LOCAL_RECORD_FEEDBACK_WEAK_FIELD_CONSTRAINT_AND_BULK_SOURCE_JOIN_V001.md | 0ae61eb4f616133ad07fbca38d33b6a6193b404f00dcd9e76cbf09fcf5d635ab |
| LOCAL_RECORD_FEEDBACK_COMMON_METRIC_SOURCE_RESIDUAL_V001.md | 665545ea6e674105e77b5977eecf9fd37287f19d7f1b273be8116867d2fc4bad |
| LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
| LOCAL_RECORD_FEEDBACK_COMMON_COFRAME_OPTICAL_BINDING_V001.md | 585d9a20fb0c2bec5dccd3f8dac726a5b57b8b0c9cdad90744f4ce7d5f22c9c4 |
| NATIVE_SPATIAL_MATTER_SOURCE_CORRESPONDENCE_V001.md | 6d626c6d9716aae6b951da7efecd0d8fe56f29c250b0575c9282dec63843ff6a |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001.md | ed426216edd6788537c3149d0a85c5d26d670ac1d7279a085bdf387435059f58 |
| local_record_feedback_3d_local_energy_source_response_v001.py | cc10b0836b9105192e210a5e17d877044fa2a64fa0ba826863bebcb521924167 |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_RESULT.json | 389df141d19e496c5989d114b67025605f248c4b1aad80f145400e2395a5cfca |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_RECEIPT.json | 7e67d3ce3c2f9f4cb8f76d6f3f69dfad1427dd550a2e99339067051292148e33 |
