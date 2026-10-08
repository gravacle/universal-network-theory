# Same-q4 conditional new-star query and shared memory V001

2026-10-06 00:31:53 UTC. NEW analytical theorem and prospective mathematical controls for the frozen F2 and T=F2 b_w laws. No prepared-state outcome, operator action, trajectory, sampler, solver or numerical worker was evaluated for this note. The computational-basis verification census is operator bookkeeping, not a physical metric history. This note neither selects a cosmic preparation nor changes the adopted WTC/RGRL effective route.

## 1. The successful state, including donor conditioning

Use cut bits n_i=(1-Z_i)/2, i=0,1,2,3, with integer word=sum_i 2^i n_i. F2 replaces each cut bit by the pair (n_li,n_ri)=(n_i,n_i). It appends blank records at the two new stars and retains the other registers. The held-copy donor map is T=F2 b_w, with T^dagger T=q_w. For any incoming density rho, let

    p_w=Tr(rho q_w), sigma=P_w rho P_w/p_w, P_w=q_w.       (1)

When p_w>0, T rho T^dagger/p_w is the conditional successful state; p_w=0 gives no successful branch and no conditional query. Trace the spectator registers in sigma to obtain sigma_cut. Its diagonal probabilities are

    pi_z=Tr(rho q_w P_z)/p_w, z in {+1,-1}^4.             (2)

P_z is the cut-word projector, commuting with q_w. Replacing (2) by an unconditioned cut law is valid only when the actual donor conditioning leaves that law unchanged. Donor-cut correlations remain part of the state.

The two new stars' joint reduced state is V sigma_cut V^dagger, where V|z>=|z>_a|z>_b. Each separate star has the diagonal marginal sum_z pi_z |z><z|. Cut coherences survive in the joint repeated-bit code, while every equal-time query below depends only on pi_z. This is a linear isometry and entanglement, not two copies of an arbitrary qubit state.

## 2. Complete local and cross-star query

Use the registered operational tetrahedral chart n_port,0=(1,1,1), n_port,1=(1,-1,-1), n_port,2=(-1,1,-1), n_port,3=(-1,-1,1). Write Nmat for its four columns. Then Nmat 1=0, Nmat Nmat^T=4I and Nmat^T Nmat=4I4-11^T. With matched labels, A outward vectors are n_port,i and B outward vectors are -n_port,i. Define

    X_A=Nmat Z/2, X_B=-X_A, m=<X_A>,
    B_ij=(n_port,i n_port,j^T+n_port,j n_port,i^T)/4,
    C_ij=<Z_i Z_j>,
    G=Cov(X_A)=I+sum_(i<j) B_ij C_ij-m m^T.               (3)

All expectations use (2), including the mean dyad. Directly X_A X_A^T=I+sum B_ij Z_iZ_j. The complete joint covariance is

    Cov((X_A,X_B))=[[G,-G],[-G,G]].                        (4)

Its rank is rank(G), its nonzero eigenvalues are twice those of G, and X_A+X_B supplies three exact nulls. In a common internal frame the offdiagonal sign is positive instead. A registered port permutation gives X_B=-R X_A for an orthogonal tetrahedral registration R, hence blocks G,-G R^T,-R G,R G R^T. These are chart transformations, not independently chosen physical coframes.

Each pair primitive is also repeated exactly: Y_A,ij=Y_B,ij=Z_iZ_j on the F2 image, and both coordination variables equal c=S-2, S=sum_i n_i. Their pair differences vanish and their cross moments equal the corresponding single-cut moments. New records remain blank; this incidence memory is not an assertion that fresh record islands already contain retained content. Equations (3)-(4) are instantaneous inclusion-image identities. The full target Hamiltonian can leave that image.

## 3. Exact rank and isotropy conditions

For x_z=Nmat z/2, G=sum_z pi_z(x_z-m)(x_z-m)^T. Therefore

    rank(G)=dim aff span{x_z: pi_z>0}.                     (5)

It is positive definite exactly when the supported vectors are not contained in an affine plane. Full cut support suffices, without supplying a quantitative eigenvalue floor. Rank zero occurs when every supported x_z is the same. In particular the all-blank and all-full words both give x_z=0, so even their coherent superposition has G=0.

The degree classes give x=0 at S=0,4, x=-n_port,i at S=1, x=+n_port,i at S=3, and the six vectors +/-2e_x,+/-2e_y,+/-2e_z at S=2. Consequently

    tr G=4-<(S-2)^2>-|m|^2.                              (6)

Nondegenerate isotropy means the traceless part of G vanishes and g=tr(G)/3>0. Degree two alone does not imply either condition. A probability law uniform within each degree class, with class weights w_d, has

    m=0, G=[w_1+w_3+(4/3)w_2]I.                          (7)

It is nondegenerate iff there is weight in degrees 1,2 or 3. Equation (7) is a sufficient symmetric family, not a claim that all isotropic distributions have this symmetry; biased distributions must be tested using (3).

## 4. Prospectively fixed state controls and coherence distinction

The following eleven controls are mathematical fixtures. All have an uncorrelated occupied donor q_w=1. Tensor factor i is bit i, |0> has n_i=0, and |+/-Y>=(|0>+/-i|1>)/sqrt2. Strings 0011 and 1100 display MSB to LSB and mean integer words 3 and 12. The six ice words are {3,5,6,9,10,12}. For the stated flip leakage comparison only, the Nc1 carrier is at an old vertex outside the eight cut endpoints, so the hop contribution vanishes. The eligible donor map gives the same conditional control; no physical preparation is thereby established.

| Incoming cut control | m | G | rank G | flip contribution to kappa |
|---|---|---|---|---|
| product +X on all four bits | 0 | I | 3 | 16h^2 |
| product -X on all four bits | 0 | I | 3 | 0 |
| product +Y on all four bits | 0 | I | 3 | 8h^2 |
| product -Y on all four bits | 0 | I | 3 | 8h^2 |
| uniform sixteen-word mixed state | 0 | I | 3 | 8h^2 |
| uniform six ice-word mixed state | 0 | 4I/3 | 3 | 8h^2 |
| equal positive-amplitude coherent six-ice state | 0 | 4I/3 | 3 | 8h^2 |
| fixed ice word 3 | -2e_x | 0 | 0 | 8h^2 |
| equal mixed words 3 and 12 | 0 | 4e_x e_x^T | 1 | 8h^2 |
| (|3>+|12>)/sqrt2 | 0 | 4e_x e_x^T | 1 | 8h^2 |
| (|3>-|12>)/sqrt2 | 0 | 4e_x e_x^T | 1 | 8h^2 |

The leakage column follows from the already derived operator 2h^2 sum_i(I+X_i), with the native link Pauli X_i distinct from the vector query X_A. At the inherited h=1/5, these are symbolic consequences of that law, not new measured outcomes. Product +/-X, uniform mixed and +/-Y states all share G=I but can have different leakage. Equal mixed and coherent ice distributions share G while second moments of the compression defect can distinguish their coherences. The query therefore does not fix the complete formation state, D variance, source responses or causal memory.

Every eligible computational incoming row in the current verification has deterministic cut bits and G=0. A coherent old/new count preparation built from one such row still has G=0 when conditioned on the created stars. If one instead defines an artificial absent-star vector as zero, its unconditioned covariance is p G+p(1-p)m m^T; that is a presence-weighted observable, not the conditional query or a derived physical metric.

## 5. The actual birth-to-common-geometry join

A prepared formation test needs its actual donor-conditioned four-cut density and registered port chart. The existing spatially averaged local pair data does not determine all six cross-cut correlations of this fixture. Once that state is supplied, (3) is an exact observable and (4) retains the duplicated memory rather than introducing independent new-star noise.

The physical WTC/RGRL common metric route is retained. A physical interpretation requires its declared reference, proper coframe/gluing and calibrated memory-to-metric/source map, with the same matter, clock and light dictionary. The uniform controls cannot supply those state or source premises by selection. This is a type distinction between an instantaneous query and an admitted common physical geometry, not a new circuit-engineering or RF3 entrance gate. No field, rate, volume function, donor gap or favorable preparation is chosen here.

## Frozen resident inputs

Paths are relative to J except program-worktree paths, which resolve from the project root. All bytes below were verified during authorship; no new-state outcomes are inputs.

| Input | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_FORMATION_V001.md | 45b99f9642d9cf757460cb8a65ea1d27f1bbb9eac9b23674b1cf879adeabed4f |
| LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md | 07323053b75b947b35712f0ac8fc4ce04c2766131cd4e684fd64167321b51f3c |
| LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_SPARSE_VERIFICATION_V001.md | 9706c0e14a348c701882ff408e94abe2bc452773ef66fbfdd30d135dc92da11d |
| local_record_feedback_native_record_donor_sparse_verification_v001.py | 85dbd31c4f76d493df2394f44a18320ccdb83f170d67efea0109e15c6d69da55 |
| LOCAL_RECORD_FEEDBACK_PROPER_METRIC_MEMORY_JOIN_AND_BODY_LOAD_V001.md | e7f89d032b72946c08a2e9e26a9bd30e6242b97bbef211e773e1e5dae4c84cf8 |
| LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001.md | 784888d9d6ab11d462e40c402fecf86bdda4894b2e23202d021ffa852707abf1 |
| program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md | cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2 |
| program-worktree/GRAVITY_RGRL_ADOPTION_V001.md | bca6146dfa2f2a32cea42db43c85c5d5fb1ee7e6114206e321066809e7c0db1f |
| program-worktree/LANE_CROSS_RFT_GRA_EW_Q4_PAIR_MEMORY_METRIC_DEFORMATION_CLOSURE_V001/THEOREM.md | 495e4e99171f4e3e5809f24e5a9a5b68116e996f4f29115bd22f780127d4714e |
