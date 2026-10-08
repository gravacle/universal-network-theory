# Native homogeneous record-feedback diagonal through sixth order V001

Prospective protocol, 2026-10-05 UTC. PREPARED; no calculation launched.
This new packet owns only this protocol, `bs10_record_feedback_diagonal_sixth_v001.py`, the new `_RESULT.json`, `_RESULT.md`, `_RECEIPT.json`, and `bs10_record_feedback_diagonal_sixth_v001_checkpoints/`. Existing inputs, including the sealed hex calculation, remain unchanged. Parent root owns any single launch after root/native/independent read-only source reviews and a fresh execution-ownership check. No retry, resume, automatic scheduling or old-producer execution is authorized.

## Scientific question and fixed reference

Compute the complete FORMAL homogeneous diagonal energy coefficients through h^6 under the SAME native degree plus record-feedback action on a supplied simple bipartite degree-four support of girth at least six. There are 2N vertices and 4N eligible edges. A reference incidence word has degree two at every vertex; each vertex has two occupied/removal edges and two absent/addition edges. Records are uniformly blank q=0 or uniformly occupied q=1. Nc=0, so the carrier copying operator vanishes; other ports, writers and controllers are off. Ud=1, d*=2, ER=1, lambda_R=1/2 and link detuning zero. Reference degree/storage/feedback energy is zero for either uniform record sector. The physical local flip normalization is the separately declared proper-bond family, h=1/5.

This is a coefficient construction around h=0. It is not a finite-h energy approximation with a remainder, a convergent linked-cluster expansion, a selected loop phase, a matter pole, a physical clock, an operational ruler, gravity or expansion result. It does not replace the full Nc1 copying/memory calculation. Local q1 denominators must not borrow the qblank symmetric denominator or its remainder. The leading offdiagonal six-cycle remains owned by the sealed hex packet; no diagonal sixth-order term is assigned a flippability dependence.

For a selected colored tree C and flipped edge subset S, eps_e=+1 for addition and -1 for removal. Define

    delta_v(S) = sum_(e incident v, e in S) eps_e,
    Delta_q(S) = sum_v [delta_v(S)^2 - q delta_v(S)/2].       (1)

All external incidences are held: the number of occupied outside edges at a vertex is 2 minus its selected removal-edge count. The selected addition/removal counts at a vertex are at most two each. Every nonempty tree subset has positive Delta. Single gaps are 2,2 for q0 and 1,3 for q1. A second independent gap form is `2|S| + 2 sum_(adjacent selected pairs) eps_e eps_f - q sum_(selected edges) eps_e`.

Any length-six diagonal flip word uses each participating edge an even number of times, hence at most three distinct edges. Girth six excludes cycles in these sets. Its connected components are single edges, adjacent pairs, three-edge stars or three-edge paths. Disconnected clusters factorize; their connected weights must cancel exactly. A six-edge alternating cycle can occur only as a different final locked state at this order and belongs to the separate offdiagonal calculation.

## Frozen colored-tree census

Representatives use consecutive vertices along a path; a star has edges (0,1),(0,2),(0,3). Every path sign word is identified up to reversal, never by addition/removal exchange in q1.

| Class | Edge signs in representative order | Embeddings / N |
|---|---|---:|
| single_add | + | 2 |
| single_remove | - | 2 |
| pair_add_add | ++ | 2 |
| pair_remove_remove | -- | 2 |
| pair_add_remove | +- | 8 |
| star_add_add_remove | ++- | 4 |
| star_add_remove_remove | +-- | 4 |
| path_add_add_add | +++ | 2 |
| path_remove_remove_remove | --- | 2 |
| path_add_add_remove | ++- | 8 |
| path_add_remove_remove | +-- | 8 |
| path_add_remove_add | +-+ | 8 |
| path_remove_add_remove | -+- | 8 |

The worker independently derives these counts from each vertex's two add and two remove slots and the middle-edge path construction. The vertex count factor is 2N; each sign of middle edge has 2N choices. Girth six means the two path ends are distinct and nonadjacent. No global incidence word is selected or simulated.

## Primary coefficient method

For each q and each actual edge subset of each representative, use at most eight scalar basis amplitudes indexed by flip masks. These are formal coefficient lists, not a Hamiltonian matrix or a propagated quantum state. Intermediate normalization is a_empty^(0)=1, a_empty^(r>0)=0 and a_nonempty^(0)=0. For perturbation -h sum_e X_e,

    E_r = - sum_e a_single_e^(r-1),
    a_S^(r) = [sum_e a_(S xor e)^(r-1)
                + sum_(k=1..r) E_k a_S^(r-k)] / Delta_q(S).  (2)

Compute r=1,...,6. Odd E_r vanish exactly. Save every E_r and every scalar amplitude coefficient, including subclusters; no eigenproblem, evolution, old module import, NPZ input or phase simulation occurs.

## Independent Q-only return words and canonical folds

Enumerate all four- and six-letter words on each selected cluster (at most 3^6). Require the final parity mask empty and every intermediate mask nonempty. With a_e=1/Delta_q({e}), set

    b = -sum_e a_e,   A2=sum_e a_e^2,   A3=-sum_e a_e^3,
    T4 = -sum_(Q-only 4 words) product_(j=1..3) 1/Delta(S_j),
    T6 = -sum_(Q-only 6 words) product_(j=1..5) 1/Delta(S_j),
    X4 = +sum_(Q-only 4 words) [product_(j=1..3) 1/Delta(S_j)]
                                      * sum_(j=1..3) 1/Delta(S_j),
    d = T4 - b A2,
    c = T6 - b X4 + b^2 A3 - d A2.                      (3)

All b,d,c agree exactly with E2,E4,E6 from (2). The X4 term owns all three placements of the squared resolvent. Q-only paths alone are not the full diagonal coefficient; canonical folds remain retained. Immediate returns to the reference are excluded only from Q words and are owned by the folds.

For every selected set C and even order r=2,4,6, compute its connected weight in two independent forms:

    W_r(C)=E_r(C)-sum_(nonempty proper T subset C) W_r(T),
    W_r(C)=sum_(T subset C) (-1)^(|C|-|T|) E_r(T).        (4)

Each subset retains its actual graph and signs. Disconnected weights vanish, and disconnected energies equal the sum of their connected-component energies. Additional frozen controls comprise all four sign patterns of two disjoint edges, all eight of three disjoint edges, and all eight of an adjacent pair plus a disjoint edge, for each q (40 control rows). No disconnected component is counted in the homogeneous assembly.

Assemble

    E_diag/N = c2 h^2 + c4 h^4 + c6 h^6 + formal higher orders,
    cr = sum_(13 classes C) (embeddings(C)/N) W_r(C).    (5)

The q0 controls are c2=-2, c4=-7/6, c6=-893/270, exactly the recovered complete GL6AO diagonal with M=4N. The q1 controls are only c2=-8/3 and c4=5/9. q1 c6 is an UNKNOWN output with no expected-sign or favorable-value acceptance gate. Single-edge E2=-1/Delta, E4=1/Delta^3 and E6=-2/Delta^5 are independent controls. Orders below 2|C| have zero connected weights. The h=1/5 polynomial may be displayed only as a formal truncated value, without an actual finite-h energy conclusion.

An independent two-edge secular-polynomial control is

    E(E-C)(E-A)(E-B)-h^2(2E-C)(2E-A-B)=0,              (6)

where A,B are the single gaps and C the double gap. Substituting the computed formal E must annul every coefficient through h^6. Independently reviewed raw E6 for q1 AA,RR,AR are -10,-7/243,-128/243, and their linked W6 are -6,-1/81,40/27. q0 same-sign raw/linked values are -1/4,-1/8 and opposite-sign +1/4,+3/8. These local controls do not set the unknown homogeneous q1 sixth-order output. Since homogeneous orders2/4 are scalar, the first order6 diagonal is not changed by an analytic near-identity P-basis rotation with U_P(0)=I preserving the declared incidence basis at h=0. A constant rotation may mix the hex operator and change that diagonal. The result still is not the phase-selected ground coefficient once offdiagonal hex terms are included.

## Same-action uniform source

For uniform dimensionless lapse L, scale BOTH the complete gaps and flip amplitudes by L: Delta_L=L Delta and -hL sum X. The reference zero is unchanged because it is the actual full homogeneous reference energy. At L=1/2 and 2 the primary recurrence is independently evaluated and must give E_r(L)=L E_r(1), and hence W_r(L)=L W_r(1). In the word/fold expression b,T4,T6 scale L, A2,X4 are invariant and A3 scales 1/L. This is a homogeneous source identity, not a nonuniform record-only lapse. The uniform direct second source derivative vanishes; the first coefficient-level source derivative equals the complete coefficient. No nonuniform/mixed-q common-Schur source calculation is included.

## Arithmetic and custody gates

Use only Python standard-library integer and Fraction arithmetic. Exact rationals are authoritative; save directed Decimal20 lower/upper displays with ROUND_FLOOR and ROUND_CEILING. No floating criterion selects a coefficient. Arithmetic acceptance comprises agreement of the two gap forms, positive denominators, independent energy methods, all odd-order nulls, actual subset Möbius forms, disconnected factorization/cancellation, single-edge controls, below-minimal-order zero weights, derived embedding counts, q0 recovered coefficients, q1 second/fourth coefficients, source scaling, complete 26 connected rows and 40 disconnected controls, and source/protocol/input bytes unchanged before and after. A failed test is preserved and reported, never reinterpreted as scientific success.

Freeze these input bytes; old sources are read/authenticated as bytes only and never imported/executed:

| Input relative to sole root | SHA256 |
|---|---|
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/DEGREE_TWO_JOINT_MATTER_REFERENCE_GATE_V001.md | 84e889f6148b43c91c2ef1a0e3194a8723e190bcf5f9a16407013e85b6a02a83 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/recovered_sources/BS_MICRO_ACTION.md | 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec |
| program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/THEOREM.md | f75edcb115c3f7c86c6598f4597366b36e363df2d03ad919cc607b57dfb6b20c |
| program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/verify_sixth_order_hamiltonian.py | 6cd1c8533821012e3281310ec0dadc95f8788ecf74729ba912f56d46f5a9b271 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/RECORD_FEEDBACK_LOOP_BACKGROUND_ORDERS_V001.md | 7800587a83941d3c3380af211ba16be584c29f36f26e4c78c5b362c347e1abc9 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001.md | 14a5b2d44887920b7bab1bd32cbc98d1d2395b3f7110a6faed0036037b16fd78 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_record_feedback_hex_ring_v001.py | d9f406d945e8e5350c7d397191d7a26bef1aafabeaaab0f50cf06db87c0b2d62 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.json | 986554b4c2315f214fef98436f285997d6c37a0884ffa1647a5a513b261fbd8f |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001_RECEIPT.json | 265692857646e2e271b16ed3e91be60baaab818b6a890e3d3ca41832ffd90fa1 |

The worker refuses any existing result/report/receipt/checkpoint directory. After authentication it creates an exclusive manifest/PID/start journal and saves/fsyncs each completed connected class before continuing, with exact subcluster data, all checks and row elapsed time. Disconnected controls and final assembly are saved separately. Partial files and exception/error journal remain intact. The final result/report/receipt authenticate raw and canonical result, inputs, source, protocol, all rows and journal prefix. A deterministic report must contain exactly26 connected-class rows and two homogeneous assembly rows; failed arithmetic remains explicit. Record runtime and ordinary resource usage. This modest process does not create new coordination infrastructure or automatic resumption. Parent alone owns the one launch.

## Outcome boundaries

Passing arithmetic earns homogeneous formal diagonal coefficients under this fixed-record local-bond family, extending the already sealed offdiagonal hex result. It does not earn finite-h control, thermodynamic phase selection, full noncommuting record/carrier dressing, physical stiffness, photon/clock/redshift, node-creation supply or shared galaxy-and-expansion evidence. Those remain substantive subsequent requirements. A newly computed q1 coefficient is preserved regardless of sign; no post-outcome baseline, decomposition or volume function may be substituted.
