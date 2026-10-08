# BS11 dynamic carrier and whole-node source: prospective V001

2026-10-05. Root approved the prospective mathematics; launch requires a
separate source review and fresh execution-ownership approval. This is one
new small local worker, with no scheduler or coordination framework.

## Question and limits

Restore the actual BS09 carrier hopping on the previously supported hexagon.
Does the full native Hamiltonian predict carrier correlations, incidence and
source-eligible low modes, rather than choosing a held carrier pattern? All
records remain held, all copy couplings remain zero and the source remains the
previously declared operational affine nodal-lapse port. Ground-state spectra
are not record formation, a cosmological preparation or physical gravity.
No deformation h(s), volume energy, pressure, physical ruler, universal
gravitational normalization, criticality, galaxy fit or superiority is claimed.

## Frozen supported graph and sectors

The six active vertices occupy R_v=(cos(2pi v/6),sin(2pi v/6)); internal edge
e=v joins v to v+1. Each vertex has one fixed occupied exterior edge to a
distinct blank vertex at 2 R_v. Exterior degrees are one. All other incidence
bits are clamped absent. External hopping and external flips are explicitly
excluded by the support, while their complete diagonal energies are retained.
The twelve-vertex bipartite normalization is N=6 per side and Omega=6h.

The internal incidence Hilbert space is all 64 bit states n. Carrier registers
contain one fixed content x or blank B, with fixed count Nc=1,3,6. Their basis
is all six-bit p masks of the selected count; no statistics sign is introduced
into the BS07 tensor-register transfer. The full dimensions are 384,1280,64.
Record occupations are held q_v=q, q=0 or1; exterior records/carriers are blank.

Freeze U_d=1, Delta=0 on internal and exterior links, d_*=2,
lambda_R=1/2, lambda_J=1/4, epsilon_r=epsilon_psi=1,
epsilon_w=0, h=t=1/10, all copy couplings zero. Six rows are (Nc,q)=(1,0),
(1,1),(3,0),(3,1),(6,0),(6,1). The seventh control is Nc=3,q=0 with BOTH
lambda_R=lambda_J=0, with every other parameter unchanged. No fit or outcome
selection is permitted. This Delta=0 supported branch does not inherit BS13
extensive stability or any unconstrained-support ground-state claim.

## Complete Hamiltonian and absolute normalization

For active vertices d_v=1+n_(v-1)+n_v. Set

    a_e = p_v+p_(v+1)-2p_v p_(v+1) = (J_e^psi)^2,
    C(Nc,q) = 6 U_d +6q epsilon_r +Nc epsilon_psi
              +lambda_J Nc -6lambda_R q,
    H_diag = U_d sum_v(d_v-2)^2
              +sum_e n_e(lambda_J a_e-2lambda_R q)+C,
    H_flip = -h sum_e X_e,
    H_hop = -t sum_e n_e T_e^psi.

T swaps occupied/blank carrier endpoints with amplitude one and annihilates
equal endpoints. It conserves Nc. C owns six exterior degree penalties,
record/carrier storage, the external current-square energy lambda_J Nc and
external record feedback. Absolute C is retained as Nc changes. A numerical
eigensolver may subtract C times identity and must restore it in all complete
energies; no source or source mean is recentered. Added q storage is not a
halo mass prescription. The q=0/1 ground energies need not match.

The joint rotation rotates both n and p. The unified Hamiltonian retains C6
and reflection. For positive h,t its fixed-Nc stoquastic graph is connected
(and the Nc=6 incidence cube is connected). Its ground state should be unique,
positive and k=0. The old held cluster/loop labels are not assigned to new
mixed modes. Actual gaps, C2 parities and C6 projector weights are saved.

## Owned source and decomposition

Each node owns its degree and onsite storage. Every internal edge term,
including -hX, -t nT and both feedback terms, is allocated HALF to each endpoint.
An exterior edge owns lambda_J p_v-lambda_R q and is allocated HALF to its
active/exterior endpoints. Delta=0 has zero incidence energy everywhere.
This fully defines twelve nodal energies before any projection:

    H[N]=sum_nodes N_v h_v,
    G_i=sum_nodes R_v,i h_v,
    N_v=1+eta_i R_v,i, eta=(1e-6,-2e-6).

These are proposed operational ports, not an earned physical lapse coupling.
All absolute source means are retained. Check full nodal ownership, positive
weighted arms, independent weighted assembly, affine G and uniform N=0.93.
The chart has direct second source contact zero. Uniform lapse gives 0.93 H
and zero offdiagonal transitions. No finite-difference eigenvalue derivatives
are needed.

To expose ordinary carrier storage/redistribution define diagonal

    G_car,i=epsilon_psi sum_active R_v,i p_v,
    G_rest,i=G_i-G_car,i.

G_rest includes degree, flips, carrier hopping, internal/exterior current-square
and record feedback, including constants. For each excited state m,
v_car,i=<m|G_car,i|0>, v_rest,i=<m|G_rest,i|0>. Save

    chi_car,ij=2sum v_car,i v_car,j/gap_m,
    chi_rest,ij=2sum v_rest,i v_rest,j/gap_m,
    chi_cross,ij=2sum (v_car,i v_rest,j+v_rest,i v_car,j)/gap_m,
    chi_full=chi_car+chi_rest+chi_cross.

The cross term is signed; separate positive fractions are not implied. Real
ground states have zero mean BS07 current, while their current-square activity
can be nonzero. The dipole transition vectors must occupy joint C6 k=+/-1;
soft k=3 modes can remain source-ineligible. Save lowest-gap groups, actual
source residue sums and complete chi without relabeling gaps as gravity.

## Arithmetic and custody gates, frozen before outcomes

Operator maximum-entry tolerance 1e-11; eigen residual and orthogonality
tolerance 2e-10 times max(1,||H||_infinity) for the residual, 2e-10 for norms.
Ground gap must be >1e-10 max(1,||H||_infinity). Ground C6/reflection and
ground-source mean tolerances are 2e-8 with source scale max(1,||G||_infinity).
Dipole allowed-projector residual tolerance 2e-9 times that source scale.
Susceptibility decomposition/isotropy/PSD tolerance 2e-8 times max(1,||chi||).
Probabilities, fixed count, pair-correlation diagonals, native energy
decomposition and finite full spectra are checked; no positive scientific
effect, particular correlation, enhanced response or small gap is a pass gate.
Energy-group reporting tolerance is 1e-9 max(1,||H||_infinity), descriptive only.

For Nc=3,q=0/1 extract selected p=010101 and p=111000 64D diagonal blocks;
hopping leaves those blocks only through off-block elements. Reconstruct
the corresponding SEALED held h=.10 Hamiltonians using their saved complete
eigenvalues/eigenvectors, then check these blocks directly. Check each new
source-block action on the OLD saved ground vector against the OLD saved
source means and transition vectors. No old solver, producer or trajectory is
executed. Custody includes SHA256 of the sealed old protocol/source/result.

Run only on this Mac using bundled NumPy, one BLAS thread. Highest dimension
1280; avoid twelve nodal dense matrices or six edge dense matrices. Target
<60seconds/row; treat elapsed >60s/row or peak process RSS>=512MiB as failed
resource gates and stop subsequent rows. Only one numerical process is owned.

## Exclusive row checkpoints and interrupted recovery

Owned paths are this protocol, bs11_dynamic_carrier_source_v001.py,
BS11_DYNAMIC_CARRIER_SOURCE_V001_RESULT.json/.md and the NEW directory
bs11_dynamic_carrier_source_v001_checkpoints/. Nothing existing is overwritten.
--execute requires absent final results and creates the directory exclusively.
A fixed-input manifest and an append-only event journal identify inputs/PID.
Each row saves exclusive started metadata, an exclusive full eigensystem NPZ
(basis, complete eigenvalues and eigenvectors, source/matrix custody), then
an exclusive JSON row receipt. The row receipt seals the NPZ hash. Completed
rows are reused without solving again. Failed/error rows are preserved and
do not authorize an automatic repair or rerun.

Only --execute --resume, separately approved after live ownership verification,
can reuse an interrupted directory whose manifest matches every source/native
input hash. A live original PID prevents resume. A complete NPZ left before its
row receipt is validated from its frozen metadata, operator hashes and full
eigen residual, then finishes analysis without diagonalization. An incomplete
NPZ or foreign bytes block recovery; they are never overwritten. A row with
only started metadata has no recoverable eigensystem and remains unfinished
until parent explicitly decides whether a new solve is admissible. Thus resume
does not silently repeat a partially executed solve. No old receipt is replayed.

Every failure/error is sealed in a final receipt and journal, with exact next
unfinished row. There is no automatic resubmission. Final receipt source/input
hashes, array hashes, checks, wall time, RSS, PID and status support independent
saved-only review. Root owns all continuation-log/ledger reconciliation.
