# Held hexagon: complete carrier/copy ground certificate V001

2026-10-05 UTC. Prospective protocol. One new bounded calculation on this Mac,
after root and both independent source reviews and a fresh ownership check.
The root owns the only launch. No numerical execution is authorized by this
document alone. Preserve all earlier results, partial attempts and failures.

## Question and fixed complete action

Can the actual held six-cycle carrier plus all record-copy configurations be
given a rigorous ground-energy interval, and what is its matched addition
above the already certified complete Nc0 background? This is an energy gate,
not a matter pole, transport curvature, physical ruler, bulk phase or cosmic
history. Copying is retained rather than replaced by a q1 proxy.

Use the supplied degree2/q4 collar in
`HELD_HEX_NATIVE_DIPOLE_SOURCE_GATE_V001.md`, all exterior records occupied,
one occupied and one blank outside bond at each active vertex. Outside flips
and carrier hops are clamped. Their occupied exterior current energy remains
`+j` at every carrier site. Inside records use the B/x alphabet aligned with
the chosen carrier content x. Every inside q word is included; no memory
sector is projected out. Nc1, EP=1, j=1/4, t=g=1/10, local h=1/5.

Order `i=6(64q+n)+v`, q,n=0,...,63 and v=0,...,5: DIM=24576.
Set `delta_u=n_(u-1)+n_u-1`, and TOTAL degree
`d_v=1+n_(v-1)+n_v`. The exact integer matrix M=20H has

    M_ii = 20 sum_u[delta_u^2-q_u delta_u/2]+20+5d_v,
    M_(q,n,v),(q,n xor2^e,v) = -4,
    M_(q,n,e),(q,n,e+1) = -2 n_e,
    M_(q,n,v),(q xor2^v,n,v) = -2.                 (1)

Cycle indices are modulo6. Record parity `S=(-1)^popcount(q)` changes the
native +g copying to -g by a unitary transformation only. Sources/readouts
would also require conjugation if later used. This packet evaluates energies
only. It does not change a coupling, subtract a second background identity,
drop current/record energy or introduce a volume law. All diagonal physical
work is kept once. The state graph is connected: flips reach any incidence
word; temporary all-occupied incidence permits carrier motion; moving the
carrier and copying reaches any record word. The transformed ground is
strictly positive by Perron-Frobenius.

The frozen parent mathematical contract is
`HELD_HEX_FULL_COPY_GROUND_CERTIFICATE_GATE_V001.md`. The actual vacuum input
is `BS10_RECORD_FEEDBACK_HEX_VACUUM_V001_RESULT.json` and its receipt; use the
global vacuum interval only after authentication and arithmetic qualification.
q63 may serve as its minimizing sector only because the completed all64-q
certificate earned that selection. No base matrix, eigensolve, Bareiss test,
old worker import or ancestor calculation is replayed.

## Exact certificate, independent controls, and trial-only optimization

For any positive INTEGER z, apply (1) with Python arbitrary-precision integers.
Save the entire z and Mz. Exact fractions give

    L = min_i (Mz)_i/(20 z_i),
    U = (z^T Mz)/(20 z^T z),
    U_CW = max_i (Mz)_i/(20 z_i).                  (2)

Then L <= E_ground <= U <= U_CW. The lower bound is Collatz-Wielandt on
`cI-M` for c>=max(M_ii); irreducibility and nonpositive offdiagonals select
the actual ground. The upper bound is full Hermitian Rayleigh/minmax.
No floating residual, optimizer convergence or selected record state is a
certificate. Ratio extrema are located by exact integer cross-products;
the index, raw integers and exact fraction are saved. Independently assemble
the quadratic form by the diagonal plus each UNDIRECTED flip/hop/copy edge
once, and verify its exact equality to z dot Mz. Check the full row census,
reciprocal ports, total-degree source ownership and four hand reference
diagonals. A uniform-vector float action is compared against its exact
integer row sum with a disclosed 1e-12 arithmetic tolerance. These are action
and arithmetic checks, not tests selecting favorable physical signs.

Floating H=M/20 is applied matrix-free in shape (64,64,6). No 24576-square
matrix, sparse eigensolver, dense joint eigensolve or propagation is built.
The ONLY eigensolve is a projected dimension at most3 trial proposal.
Freeze this optimizer before outcomes:

1. Initial x is uniform positive with Euclidean norm1; p_previous=0.
2. At each iteration form r=Hx-(x dot Hx)x. In order x,r,p_previous,
   perform ONE modified Gram-Schmidt pass. Drop a column with norm<=1e-14;
   normalize each retained column. Form the symmetric projected matrix by
   computing its upper triangle and mirroring it; use its lowest NumPy
   eigenvector to form a trial in that subspace.
3. Take absolute components, floor each at 1e-100, and normalize. Taking
   absolute values cannot increase the exact Rayleigh quotient of the
   negative-offdiagonal operator. Set
   `p_previous=x_new-(x_old dot x_new)x_old`.
   Nonfinite/zero numerical state is a preserved failure, not a trigger for
   another optimizer, altered threshold or restart.
4. Maximum4096 iterations; exact certificate stages16,64,256,1024,4096.
   At each stage convert each finite positive float x_i using its exact
   `as_integer_ratio()` a/b. Round `a*10^60/b` to nearest integer, ties even,
   by divmod; replace a rounded zero by1. This is mathematically the exact
   decimal-from-float product, so no finite Decimal precision chooses a tie.
   Positive-vector floors/rounding define the trial only, not H or data.
5. Stop at the FIRST certified U-L<=1e-6 if all controls earned so far pass.
   Otherwise continue only through the declared4096 stage. Retain all raw
   stage intervals and the valid final interval if requested precision is
   unearned. No best-row selection, fallback, parameter tuning or added grid.

Save an initial lossless x/p hexadecimal checkpoint and one lossless x/p
checkpoint at each certificate stage, together with that stage's z/Mz,
raw norm/dot integers, exact L/U/U_CW, pointwise extrema, float residual and
projected diagnostics. One iteration can be reconstructed from the saved
hex floats, but this attempt refuses preexisting outputs and does not resume
automatically. Interrupted optimization is not a scientific result unless
the saved exact certificate qualifies. Preserve any partial stage/error.

## Matched addition and independent held theorem

With authenticated complete vacuum Ebg in [Lbg,Ubg], save RAW

    E_ground-Ebg in [L-Ubg,U-Lbg].                 (3)

Do not clip it to an independent theorem or change the baseline. The common
frozen support offset cancels in the difference only. The independent held
theorem from the parent contract is

    23/20 <= E_ground-Ebg <= 19/10-sqrt(53)/20.    (4)

The lower follows from `tL_internal+(j-t)D_internal+jI>=jI` and copy U^2=I.
The upper is the two-vector full-action trial, not an invariant two-state
subspace. Its displayed sqrt is bounded by128 fixed rational bisections of
[7,8], with squared rational endpoint controls. Keep this theorem separate
from the numerical interval. Incompatibility of two purported rigorous
bounds is an arithmetic/model implementation failure; a broad raw interval
or unearned 1e-6 precision is not a physical theory failure. Earned statuses
require the final failed-control count zero. Raw candidate intervals and
precision flags remain visible even if a control fails.

Uniform full-action L scales the joint H, vacuum and matched addition once;
no nonuniform source response is calculated here. Ground energy alone does
not earn a pole/residue, internal clock, physical time/ruler, 3D Coulomb
phase, gravity, expansion or superiority.

## Exclusive outputs, custody, and launch boundary

Owned NEW files only: this protocol, `bs10_record_feedback_hex_joint_v001.py`,
`BS10_RECORD_FEEDBACK_HEX_JOINT_V001_RESULT.json`, `_RESULT.md`, `_RECEIPT.json`,
and `bs10_record_feedback_hex_joint_v001_checkpoints/`. Existing files are
read-only. Refuse if any reserved output/checkpoint directory exists.
Input hashes include the final vacuum source/protocol/result/receipt and
frozen collar/parent contract. Authenticate the vacuum raw/canonical/report,
source/protocol, inherited input maps, checkpoint maps, manifest/start seal,
every checkpoint commit, journal prefix and final receipt; also authenticate
the inherited finite parent and its preserved structural-check alias prefix.
No input source is imported or executed. Repeat all current input-byte checks
before the final result. Source/protocol hashes must remain unchanged.

New writes are exclusive and flush/fsync before journal commits. Record PID,
one-BLAS environment, NumPy version, all stage elapsed/runtime data and
ordinary peak RSS. Save stage evidence before advancing, then result/report,
canonical/raw hashes and final receipt. Use privately copied stage-check
lists. A caught exception saves a new ERROR.json and append journal event;
preserve earlier stages and never repair/replay silently. The report has one
DATA row per completed fixed stage and displays raw joint/addition bounds,
the independent theorem and earned/unearned status. Arithmetic controls
and scientific precision are separate.

Root launch after final input pins and three static reviews supplies
OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1, MKL_NUM_THREADS=1,
VECLIB_MAXIMUM_THREADS=1 and PYTHONDONTWRITEBYTECODE=1 before NumPy imports.
No worker by this author, heavy model, installation, remote job, Goal,
heartbeat, replacement framework, publication, spending or automatic rerun.
