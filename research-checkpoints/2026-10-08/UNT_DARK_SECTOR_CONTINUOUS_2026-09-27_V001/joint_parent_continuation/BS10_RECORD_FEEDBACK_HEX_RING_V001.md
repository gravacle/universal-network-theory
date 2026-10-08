# Native record-feedback hexagon: prospective exact sixth-order coefficient V001

2026-10-05 UTC. Prospective protocol, written before the new worker. Parent owns the one eventual local launch after source, independent review and fresh ownership checks. No launch is authorized by this file. This is a small exact coefficient calculation in the disclosed fixed-proper-local-bond family, not a replay or replacement of the sealed symmetric ring calculation.

## Frozen question and sector

Use the revised native tuple U_d=1, d*=2, record storage E_R=1, record feedback lambda_R=1/2, link detuning0, and h_proper=1/5. Supply one simple alternating six-cycle in a coordination-four/girth-six eligible support. Exactly one of the two outside eligible bonds at each vertex is occupied and held unchanged, so the alternating starting background has degree2. Number the vertices v=0,...,5 and cycle edges e_i=(i,i+1 mod6); initially absent even edges have epsilon_i=+1 and initially occupied odd edges epsilon_i=-1. Every alternating endpoint has exactly degree2. The opposite endpoint toggles all six edges.

Take N_c=0; all carrier storage/current/hopping/copy terms consequently vanish in this reference. Other writers/copies and ports are OFF. The six record occupancies q_v are fixed independently in {0,1}, and all64 words are retained. Occupied content labels do not change the occupation-only denominators; complementary retained content sectors are not declared a single gapped phase. Record occupancies are conserved here. This calculation neither forms records nor substitutes for the actual carrier/record joint kernel.

Only UNIFORM complete source L=1 is evaluated. At degree2, each record's storage plus feedback is q_v(1-d_v/2)=0. Its absolute complete energy is retained; no per-word energy reference is reset. Both alternating endpoints are degenerate within each fixed-q block. Nonuniform source splits/mixes the appropriate projected objects and needs the common Schur/source action; it is omitted from this gate.

## Actual denominators and leading matrix element

For a flipped subset S of the six edges,

    delta_v(S)=epsilon_(v-1) 1_(v-1 in S)+epsilon_v 1_(v in S),
    Delta_q(S)=sum_v [delta_v(S)^2-q_v delta_v(S)/2].          (1)

At a cycle vertex the two epsilon signs are opposite. Thus a vertex with both or neither incident cycle edge flipped contributes0. A boundary vertex contributes1-q_v/2 for delta=+1, or1+q_v/2 for delta=-1. Every nonempty proper S has at least two boundary vertices and hence Delta_q(S)>=1. The empty/full subsets have Delta=0 and are not intermediate Q denominators. No two-/four-cycle allows another projected endpoint at an earlier order; no proper subset of this hex returns to degree2.

In particular, q=000000 gives Delta=sum delta^2 and single-flip gap2. At q=111111, put a=#added edges, r=#removed edges, b=#selected/unselected cycle boundaries. Then

    Delta_1(S)=b-a+r; single-add gap1, single-remove gap3.    (2)

Let S_j(pi) be the first j edges of a permutation pi. The first nonzero offdiagonal entry is

    <opposite|H_eff^(6)|initial>=-J6(q),
    J6(q)=h^6 c6(q),
    c6(q)=sum_(pi in S6) product_(j=1,...,5) 1/Delta_q(S_j). (3)

Six minus signs from flip vertices and five negative reduced resolvents give the displayed negative matrix element. Lower-order folds cannot connect these endpoints. This statement concerns the offdiagonal entry only, not every sixth-order diagonal term or every lower-order record-dependent contribution.

Independently compute c6 by the64-subset recurrence f(empty)=1 and

    f(S)=[sum_(e in S) f(S minus e)]/Delta_q(S) (1<=|S|<=5),
    c6(q)=sum_e f(full minus e).                            (4)

The path method uses boundary-vertex half-integer weights; the DP method directly constructs delta_v and degree/storage/feedback increments. Both use exact standard-library Fraction arithmetic. Enumerate all720 permutations explicitly, rather than sample them.

Prospective controls: the sealed qblank coefficient is63/8; the NEW independently reviewed hand recursion for qoccupied gives2504/81. The hand q1 classes are: size2 AA1, RR1/9, adjacentAR2/3, oppositeAR1/3; size3 AAA1, RRR1/27, AAR chain7/3/disconnected2/3, ARR chain13/27/disconnected2/9; size4 indexed by the MISSING pair AA13/81, RR7/3, adjacentAR50/27, oppositeAR4/9; size5 missingA362/243, missingR238/27. The full sum is3(362/243+238/27)=2504/81. At h=1/5 the proposed q1 J6 is2504/1265625. These are prospective arithmetic tests; their verification does not control finite h=.2.

Reversing the initial alternating orientation sends delta to minus delta; complementing/reversing the six-flip order proves the same coefficient. Cycle rotations/reflections map the local motif and may reverse that orientation, so the coefficient is invariant under the12 dihedral transformations of the record word. Freeze and test every word, every transform and orientation reversal without selecting outcomes. Global record complement is NOT declared a coefficient symmetry.

## Frozen input ancestry

All paths below are relative to the sole project root. Authenticate exact bytes before calculation and again before final receipt. Old sources are READ as bytes only; no import, execution, producer, solver, propagation, Hamiltonian action or NPZ access.

| Input | SHA256 |
|---|---|
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/DEGREE_TWO_JOINT_MATTER_REFERENCE_GATE_V001.md | 84e889f6148b43c91c2ef1a0e3194a8723e190bcf5f9a16407013e85b6a02a83 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/recovered_sources/BS_MICRO_ACTION.md | 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec |
| program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/THEOREM.md | f75edcb115c3f7c86c6598f4597366b36e363df2d03ad919cc607b57dfb6b20c |
| program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/verify_sixth_order_hamiltonian.py | 6cd1c8533821012e3281310ec0dadc95f8788ecf74729ba912f56d46f5a9b271 |

GL6AN/AO compute the symmetric pure-degree coefficient and formal complete effective Hamiltonian. They do not prove the present q1 detuned coefficient, diagonal cancellation, all-order remainder or local-family phase. Reading their verifier as an input does not rerun it. Independent hand review on the new q1 recursion passed before this worker.

## Execution, outputs and controls

Own ONLY this new protocol, bs10_record_feedback_hex_ring_v001.py, future BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.json/.md, BS10_RECORD_FEEDBACK_HEX_RING_V001_RECEIPT.json and new bs10_record_feedback_hex_ring_v001_checkpoints/. No existing files, logs or ledger are edited. Refuse any existing output/checkpoint directory. Exactly one tiny standard-library local process is proposed; no NumPy, other model, grid, diagonalization, or time evolution. Parent launches only after reviews and a fresh safe-ownership check. No automatic retry/resume.

Save an exclusive manifest/start event with PID/source/protocol/input hashes and frozen constants before arithmetic, then one small row JSON/journal commit per completed qword. Retain all rational numerators/denominators, each gap range, coefficient, J6, orientation check and each scalar check. Flush/fsync new JSON/report bytes before their journal commits. Save partial error/journal if an exception occurs. Final JSON/report/receipt are exclusive; never replace failed or partial work. Record ordinary elapsed time and resource diagnostics only.

Checks:64 words;64 subsets per word; all positive proper gaps and empty/full zeros; exact equality of the two independently coded denominator forms; exact720-order/DP equality; all reversal and dihedral symmetries; q0/q1 frozen coefficient controls; positive c6/J6 and exact h^6 scaling; complete input-byte equality at finish; output schema/report checks and seals. Any failed check is preserved as a failed arithmetic gate. Report all64 rows, extrema and per-record-count ranges. Displays use directed20-significant-digit Decimal intervals; exact Fractions remain authoritative. No response/passivity/energy advantage sign is an acceptance criterion.

## Scientific ceiling and concrete missing remainder

This earns a finite linked sixth-order offdiagonal coefficient on the supplied collar, with every record word retained. It does not earn a finite-h effective-Hamiltonian error bound, all-orders local/volume-uniform linked-cluster convergence, a selected degree-two ground phase, a Coulomb photon or3D material transport, a physical clock/ruler, negative pressure, acceleration, lensing or Stage3 closure. The old symmetric order6 diagonal scalar cancellation cannot be inherited without a new record-feedback census and canonical folds. Even if each proper six-edge denominator is positive, larger defect sets and the full local-family phase need separate control. h=.2 is the declared reference value, not an a posteriori smallness proof.

The next useful physical gate after this exact coefficient is an actual finite-h local/linked-cluster or complementary-defect bound for the SAME occupied-record local family, including its complete diagonal/record-dependent terms and absolute work. No standalone pure-ring remainder or fitted interpolation is inserted here. The root continues the full degree-two matched-matter/source analysis in parallel; this coefficient is a bounded input to it.
