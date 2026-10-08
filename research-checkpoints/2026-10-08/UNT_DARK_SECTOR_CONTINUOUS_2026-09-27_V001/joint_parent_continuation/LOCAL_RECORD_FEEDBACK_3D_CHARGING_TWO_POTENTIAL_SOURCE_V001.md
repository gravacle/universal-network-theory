# Charging-only spatial source and complete NN comparison V001

2026-10-05 UTC. Prospective NEW saved-statistics packet. No sampler, Hamiltonian action, propagation, eigensolver, old-producer import, new physical state, inverse, field solve or parameter selection. Root alone launches the reviewed new source. All 10 accepted beta4 datasets and all seven resident modes are retained. This is an explicitly conditional charging-source block, not a complete two-potential gravity or material closure.

## 1. One explicit source action and chart

On the same q1/Nc0 L3 parent, c_v=d_v-2, D_v=c_v^2-c_v/2 and J_v=D_v+c0 I. Retain c0=AR+Sself symbolically; its sampled intercept is zero, its physical value is unselected. Define the NEW operational source

    N_v=1+eta_v, a_v=sqrt(1-2 psi_v),
    H[N,psi]=sum_v N_v J_v/a_v
               -h sum_(e=uv) (N_u+N_v) X_e/2, h=.2.        (1)

The metric chart is ds^2=-N^2 c_p^2 dt^2+a^2 dx^2, with g_ij=(1-2psi)delta_ij. This explicitly applies the resident ideal shielded-plate J_v/a_v law star by star. Actual flip amplitudes are CLAMPED with respect to psi in this conditional source class. Their N allocation is the inherited affine midpoint source. This does not derive physically strain-independent h or the spatial source of connectors, donors, material supports, readout or Maxwell dynamics. Gauss/return charging energy is included once in J; no second electrostatic field energy is added.

At reference, the local vertices/direct contacts are

    H_,eta_v = E_v = D_v+c0-h/2 sum_(e incident v) X_e,
    H_,psi_v = J_v,
    H_,eta_v eta_w=0,
    H_,eta_v psi_w=J_v delta_vw,
    H_,psi_v psi_w=3 J_v delta_vw.                           (2)

The 3 follows a_psi=a_psi psi=-1 at zero: H_psi psi=H_aa-H_a=2J+J. In the distinct affine-coframe chart a=1-psi the last contact is 2J. Save its d_affine=d_metric-diag(meanD+c0) as a coordinate comparison only. A complete stationary total background could cancel a total first-stress chart term; this individual charging sector is not declared stationary and its J/c0 term cannot be dropped.

## 2. Finite-M fixed-coordinate-beta response

Use the accepted beta4, M64/M128 ensembles, not a thermal alias of the separate D_rel prepared control. The NN source retains the full old finite-M transfer second score C2. With connected susceptibilities defined by beta times covariance of the owned time-average score observables, at zero source

    A=R_NN=-chi_EE-C2/beta,
    b=diag(mu_D+c0)-chi_ED,
    b_reverse=diag(mu_D+c0)-chi_DE,
    d_metric=3 diag(mu_D+c0)-chi_DD,
    d_affine=2 diag(mu_D+c0)-chi_DD.                          (3)

mu_D,s=mean_D(k0,s)/sqrt27 is the per-node charging intercept. These direct contacts are present at EVERY k, not just k0. Forward/reverse complex responses are saved separately; b_reverse=b^dagger is a checked equilibrium/source identity, not permission to discard imaginary parts. The full modeled source block is [[A,b],[b_reverse,d_metric]]. No positivity or force-success gate is imposed on any entry/eigenchannel. No inverse or measured-mode deletion is computed.

The mixed and psi second log-weight scores are respectively -beta J_v delta_vw and -3 beta J_v delta_vw. Psi changes only the diagonal charging factor in(1), so no extra transfer psi contact is invented. The NN transfer C2 remains mandatory. Constants c0 drop from connected covariance, but remain in all first means/work and in the b,d direct contacts.

Let L_D be the 2x14 matrix with coefficient 1/2 on each of the six Y entries of its sublattice, -1/2 on its coordination entry, and zero elsewhere. The saved identity is D_s(k)=L_D Q(k)+sqrt27 delta_(k,0). Reconstruct

    chi_ED=chi_EQ L_D^dagger,
    chi_DE=L_D chi_QE,
    chi_DD=L_D chi_QQ L_D^dagger.                            (4)

Independently compare chi_DD with beta(second_D-mean_D mean_D^dagger), and compare mean_D with the Q affine identity, at every central and delete-block replica reconstructed from the parent raw moments. Anchor the inherited central means/susceptibilities/NN block and their component SE against the stored parent estimates/errors. This is moment arithmetic, not a producer replay or operator action. Keep biased central moments and the parent's correlated delete-block jackknife convention unchanged.

## 3. Proper plane, affine constant and means

Use exactly the phase-normalized source of the reviewed common-field note: a_k=(1,exp(i K dot ell0 u0))^T/sqrt2, K dot ell0(u_i-u0)=2pi k_i/3 for the disclosed tetra chart. Native sublattice analysis uses 1/sqrt27. Contract all A,b,b_reverse,d matrices by a_k^dagger M a_k. All +/- modes are saved, with their conjugacy checked; use the full paired convention or sqrt2 real modes, without an extra half.

Every output is an intercept plus explicit c0 slope: b and b_reverse have I2 slope, d_metric has 3 I2 slope, d_affine has 2 I2 slope. Their plane slopes are 1,3,2. A and connected susceptibilities have zero slope. First eta/psi local means have slope1, and their homogeneous mode source is sqrt27 per sublattice (sqrt54 after proper scalar-plane contraction). Homogeneous q1 data supplies no nonuniform physical body j_psi or j_eta. Absolute mean/contact work is retained symbolically, not calibrated into a new G or environmental function.

The complete-action proper-bath uniform guard from the parent is retained separately from this fixed-coordinate response. It does not quotient the energy covariance. Only previously proved charge-odd/gauge qualifications are inherited; both A/B energy channels remain. This packet selects no AR/self value, interpolation volume, metric scale, constituent slope or favorable parameter window.

## 4. Frozen census, errors and acceptance

Ordered datasets: c0_I01,c0_I02,c0_B,c0_R,c1_I01,c1_I02,c1_B,c1_R,condition0,condition1. Use the accepted 32 raw blocks per chain and 128 pooled blocks per condition, all 512 correlated delete-block replicas. Retain modes (0,0,0),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1). Report 10 dataset rows and 70 proper-plane rows. Preserve parent finite-grid diagnostics, old beta8 mixing/inverse refusals and the accurate distinct-method authored acceptance status.

Use fixed 3e-11 max(1,Frobenius norm of reference) for moment/response/normalization identities, as in the accepted arithmetic lineage. All arrays and components must be finite. Store each central matrix, all correlated replicas and separate real/imaginary component SE. Compute jackknife replicas from the same raw blocks, never treat a contact and covariance SE as independent. Save raw mode means, susceptibilities, direct contacts and source-block intercepts/slopes. No data-driven criterion or fallback/refinement is permitted.

Before any reconstruction authenticate all 13 direct inputs below, all accepted audit input seals, producer canonical/report/receipt/journal/checkpoint maps, named 10 dataset checkpoint duplicates and full ordered census. The accepted V002 audit must be PASS/failed0 and match the exact raw producer result/receipt/source/report; V001 failure bytes remain in ancestry. Recheck every consumed input before outputs and with a non-counting strict guard before receipt.

Prospective source: /private/tmp/local_record_feedback_3d_charging_two_potential_source_v001.py; root may protect/run a byte-identical J copy only after final hash/full peer reviews and ownership checks. Reserve NEW stem LOCAL_RECORD_FEEDBACK_3D_CHARGING_TWO_POTENTIAL_SOURCE_V001_{RESULT.json,RESULT.md,RECEIPT.json,ERROR.json} and local_record_feedback_3d_charging_two_potential_source_v001_checkpoints exclusively. No overwrite, automatic recovery, launch or previous mutation. Save manifest plus 10 dataset lossless NPZ/JSON pairs (21 checkpoint files), initial journal plus 20 file commits and result/report/receipt commits (24 events). Failure preserves the actual input/active-dataset/check prefix and exceptional ERROR; a completed arithmetic result is distinguished from an incomplete exception. Source/protocol hashes and all input seals are in receipt.

## 5. Physical ceiling

This earns a measurable charging contribution to b,d on an explicit common source chart, paired with the already complete modeled NN contribution. It does not derive full h/t/copy/material/Maxwell/support spatial stress, choose a stable background, eliminate retained constraints, produce a body source or settle the total-G/reference split. Existing negative charging directions, common-field underdetermination and Stage3 duties remain. A WTC effective calculation can use an explicitly supplied complete reduced constitutive law without a new RF3 requirement; this packet does not silently supply that law.

## Frozen direct inputs

Paths are relative to joint_parent_continuation. The 13 direct seals are actual current bytes, not absent artifacts.

| Input | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_COMPLETE_STRAIN_SOURCE_CONTRACT_V001.md | cc363bf1885917a9beededadb8d49b5d898c951bd54a1e2d2ad6ce5003ebaf63 |
| LOCAL_RECORD_FEEDBACK_COMMON_COFRAME_OPTICAL_BINDING_V001.md | 585d9a20fb0c2bec5dccd3f8dac726a5b57b8b0c9cdad90744f4ce7d5f22c9c4 |
| LOCAL_RECORD_FEEDBACK_COMMON_FIELD_TWO_POTENTIAL_CLOSURE_V001.md | 0e4c9a8e47d8570c53761ba5d605764f145ffdc398c52d047b5f39f63c143459 |
| LOCAL_RECORD_FEEDBACK_WEAK_FIELD_CONSTRAINT_AND_BULK_SOURCE_JOIN_V001.md | 0ae61eb4f616133ad07fbca38d33b6a6193b404f00dcd9e76cbf09fcf5d635ab |
| local_record_feedback_3d_local_energy_source_response_v001.py | cc10b0836b9105192e210a5e17d877044fa2a64fa0ba826863bebcb521924167 |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001.md | ed426216edd6788537c3149d0a85c5d26d670ac1d7279a085bdf387435059f58 |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_RESULT.json | 389df141d19e496c5989d114b67025605f248c4b1aad80f145400e2395a5cfca |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_RESULT.md | be19640343895de1624c1c7963abe9987fb6da978a7feb33366854762661bb2e |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_RECEIPT.json | 7e67d3ce3c2f9f4cb8f76d6f3f69dfad1427dd550a2e99339067051292148e33 |
| local_record_feedback_3d_local_energy_source_response_v001_saved_authored_acceptance_v002.py | fb81052f8c9ead0f1deccc432986cf185968329df3c09f44e9670063a3d90c73 |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_AUTHORED_ACCEPTANCE_V002.json | 77d307619ebdff976dc6e1c47b25af129f641df83e12a81bf6a37aedd0b84399 |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_AUTHORED_ACCEPTANCE_V002.md | 18cece480c9445f5c2004332d6e68b504f09b6c7c83b204bf5a3c2332fc156dc |
| LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_AUTHORED_ACCEPTANCE_RECEIPT_V002.json | 85d067a77e22bb14a2890db9e76218ba7c482bc68bc5ded2d5df086c1ec1af2a |
