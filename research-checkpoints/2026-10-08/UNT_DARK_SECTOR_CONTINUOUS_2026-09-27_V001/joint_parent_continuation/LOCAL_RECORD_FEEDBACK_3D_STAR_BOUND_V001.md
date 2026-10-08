# Current three-dimensional record-feedback parent: overlapping-star bounds V001

2026-10-05 UTC. Prospective bounded finite-h certificate, after root and
independent protocol/source reviews and root execution-ownership checks.
No calculation is launched here. The supplied diamond support, record
preparation and every previous held-cell result remain separate evidence.
This packet introduces no new Hamiltonian, energy reference or volume law.

## Exact same-parent sector and local sum

Take a supplied simple periodic bipartite degree-four diamond graph with
V=2N vertices and M=2V=4N eligible edges. Its specified degree-two incidence
word exists; graph supply and that preparation are premises. Keep Nc0,
all occupied B/x records q_v=1, native Ud=ER=1, lambdaR=1/2 and local
proper flip h=1/5. Copying, carrier current and hopping vanish by their
actual Nc0 operators, rather than changing their couplings. Record words
are conserved in Nc0; all-occupied records are an owned sector, not an
already proved global vacuum or an autonomously formed record state.

At each vertex let d_v=sum_(e incident v)n_e and delta_v=d_v-2. Retain

    D_v=delta_v^2-delta_v/2,
    H0=sum_v D_v-h sum_e X_e.                            (1)

D_v already contains the complete onsite degree, occupied-record storage
and feedback at this tuple. Its degree0,...,4 values are

    5, 3/2, 0, 1/2, 3.                                 (2)

Zero at degree2 is this actual action's value, not a post-outcome energy
subtraction. In n_e=(1-Z_e)/2 conventions,

    D_v=I+(1/2)sum_(pairs of incident edges) Z_e Z_f
          +(1/4)sum_(incident edges) Z_e.

Pairs have one shared-vertex owner and edges have two endpoints, hence

    H0=V I+(1/2)sum_pyrochlore_neighbors Z_e Z_f
          +(1/2)sum_e Z_e-(1/5)sum_e X_e.

The longitudinal term stays; the zero-longitudinal transverse-ice phase
literature and old pure-degree-lock remainders are not certificates here.

Define the overlapping four-edge star operator

    h_v=D_v-(h/2)sum_(e incident v)X_e.

Because each edge belongs to exactly two stars,

    sum_v h_v=H0                                        (3)

as an exact operator identity, even though adjacent stars do not commute.
No independent product of star ground states or common saturation is
assumed. Each star uses ALL16 incidence bit states, including every
charged degree. Records remain the declared occupied sector spectators.

## Two fixed local operator certificates

Only a=1/2 is used; it is a mathematical comparison coefficient, not a
new physical stiffness or a fitted parameter. Compute exact outward
intervals for

    mu=min spec(h_star),
    k=min spec(h_star-a D_star),    b=-k,
    a=1/2, h=1/5.                                     (4)

The two comparison coefficients are a=0 and a=1/2; no other a is run.
The common integer scale20 matrices in bit order0,...,15 are

    (20 h_star)_ss=20D_(popcount s),
    (20(h_star-aD_star))_ss=10D_(popcount s),
    either matrix offdiag=-2 for one-bit flips.

They are16x16 real symmetric complete hypercube matrices. Their
connected negative offdiagonal ports make the finite lowest eigenvalue
simple. The two NEW NumPy eigh calls provide positive ground trials only; exact
integer Collatz-Wielandt/Rayleigh endpoints certify the minima. Neither matrix
is a selected global state or a replacement for overlapping stars.

For every actual V-volume sector state, including its normalized ground,

    H0 >= V mu I,
    H0 >= a sum_v D_v-b V I.                            (5)

These inequalities follow by tensor-extending each local spectral bound
and summing positive operators; noncommutation changes no inequality.
They are volume-uniform and require no large Hilbert-space calculation.

## Independently owned matching trial and occupied control

Here blank/occupied describes the bond bit; ALL records remain occupied
q1 throughout both trials. These are not blank-record q0 alternatives.
In the declared degree-two incidence word, blank edges also have degree2
at every vertex. Their components are even cycles because the supplied
graph is bipartite. Choose one alternating perfect matching, V/2 blank
edges, and retain every other incidence bit in its original basis state.
Every matching endpoint is disjoint from every other matching endpoint.

Adding one chosen blank edge changes both endpoint deltas0 to+1; each
endpoint costs1/2 by (2), so the COMPLETE two-endpoint gap is1. The trial
factor is the normalized lower eigenvector of

    B_blank=[[0,-h],[-h,1]].

All other edge flips remain active operators of H0 but have expectation0
in this specified trial. Because no vertex sees two matching toggles,
the diagonal expectation factorizes exactly, including storage/feedback.
Thus its full H0 expectation per vertex is

    e_blank=(1-sqrt(1+4h^2))/4
           =(5-sqrt(29))/20.                            (6)

This is an independently derived variational upper bound, not the true
energy density, formed state, new energy function or finite-h expansion.

Keep the occupied alternative as an explicit control. Occupied edges
likewise have a perfect matching; removing one changes both deltas0
to-1 and costs3/2 at each endpoint, COMPLETE gap3. Its trial per vertex is

    e_occupied=(3-sqrt(9+4h^2))/4
              =(15-sqrt(229))/20.                       (7)

The chosen primary upper bound is blank before outcomes. The occupied
trial is not discarded or renamed; for h>0 the lower2x2 eigenvalue is
monotonically increasing with its positive gap, hence e_blank<e_occupied.
No native common identity, record energy or extensive background is
recentered in either trial.

## Earned energy and defect envelopes only

Let normalized sector ground energy density be e0=E0/V. Then exactly

    mu <= e0 <= e_blank <0,
    0 <= <sum_v D_v>/V <= (e_blank+b)/a
                          =2(e_blank+b).               (8)

The defect expectation bound uses (5), the SAME full ground energy and
the variational upper bound. It does not insert a ground projection into
a prepared history. D_v>=0 and D_v=0 precisely at degree2. Separately,
for the local defect projector Q_v=1_(d_v!=2),

    D_v >=delta_v^2/2,
    (1/2)Q_v <= D_v <=5Q_v,
    <sum_v delta_v^2>/V <=2 <sum_v D_v>/V,
    <sum_v Q_v>/V <=2 <sum_v D_v>/V.                     (9)

The first inequality follows from
D_v-delta_v^2/2=delta_v(delta_v-1)/2>=0 for integer delta_v.
Save both raw implied bounds even if the nonice bound exceeds1 or the
mean-square bound exceeds4; retain the independent probability0..1 and
mean-square0..4 identities explicitly without clipping the
computed certificate or calling a weak bound strong. No lower positive
defect-density claim is inferred from (8). A bound too loose to constrain
local defects remains an inconclusive scientific outcome, not a failed
arithmetic test or a reason to choose a different a after the outcome.

Given certified mu in[muL,muU], k in[kL,kU], and trial interval[eL,eU],
save raw e0 envelope[muL,eU] and b interval[-kU,-kL]. The rigorous raw
D upper is2(eU-kL); raw Q and mean-square-delta uppers are both
4(eU-kL). Keep the inner local intervals
and all exact endpoints. Check order, the two operator-bound definitions,
the nonnegative nature of D, and complete matching gap1/3 independently.
The exact trial bound uses every physical constant already in (1).

These bounds can earn finite-h, volume-uniform ground energy and local
defect expectation envelopes for the CURRENT supplied 3D parent. They do
not earn a Coulomb phase, compatible/dressed global GNS state, transverse
structure or dynamic pole, preparation, selected graph, matter lifetime,
rank-three curvature, physical clock/ruler, absolute gravity coefficient,
volume stress/creation history or galaxy-and-expansion fit. The source
Ward/contact and supply/controller energy duties remain. All Stage3 and
fair-comparison obligations remain open.

## Frozen numerical and custody policy for the future source

One modest NEW worker only after protocol and source reviews; root alone
owns launch. The source is independent, with no ancestor import/action,
old eigensolve/inertia/evolution or changing-support calculation.

For each NEW16x16 matrix, one NumPy eigh supplies one lowest-vector trial.
Store all16 trial eigenvalues as proposal metadata and the chosen vector as
lossless float hex. Take absolute components, floor to1e-100, normalize;
round x*10^60 by exact float.as_integer_ratio/divmod nearest ties-even,
floor any rounded zero to1. This is the one prospectively fixed positive
integer proposal z, not an eigenstate certificate or an iterative solver.
Save z and exact integer Mz, ratio witnesses and quadratic forms.

With M=20(h_star-aD_star), connected stoquastic ports and z_i>0,

    L=min_i (Mz)_i/(20z_i),
    U=z^T Mz/(20z^T z),
    U_CW=max_i (Mz)_i/(20z_i)

certify L<=min spec(h_star-aD_star)<=U<=U_CW. Verify Mz against an
independent undirected-edge quadratic form, all16 bit-flip reciprocity,
negative ports and exact popcount diagonals. Freeze requested width
U-L<=1e-11 for EACH matrix. A wider valid interval remains explicitly
precision-unearned; no second proposal, refinement, Bareiss calculation,
iteration or changing a/h is authorized. Integer rounding controls are
mandatory. Floating proposals supply no numerical authority; every bound
remains exact Fraction arithmetic for any strictly positive z.

For sqrt29 and sqrt229 use exact Fraction interval bisection with fixed80
iterations, initial[5,6] and[15,16], updating by exact midpoint squared
comparison. Retain exact bounds and directed Decimal20 displays; check
squared endpoints and trial formula intervals. No rounded sqrt is an
energy certificate. Preserve both positive proposals, integer certificates, minima,
sqrt-control and final assembly as exclusive resumable checkpoint rows.

Reserve only this protocol, local_record_feedback_3d_star_bound_v001.py,
LOCAL_RECORD_FEEDBACK_3D_STAR_BOUND_V001_RESULT.json, _RESULT.md,
_RECEIPT.json and local_record_feedback_3d_star_bound_v001_checkpoints/.
Refuse existing outputs, flush/fsync before journal commits, save PID,
source/protocol/input hashes and private checks; compare every input and
new source/protocol byte before final seal. A receipt binds raw/canonical/
report/checkpoint/journal-prefix evidence. Preserve partial errors and no
arithmetic-failed receipt earns a physical bound. Record ordinary runtime
and peak RSS; same root-supplied single-BLAS/no-bytecode environment.

## Recovered current input bytes

The future source pins only these three current operator/normalization/
matching notes. They authenticate the declared action and trial ancestry
without a new coordination or expansive ancestry framework. No old producer
executes.

| input relative to this directory unless stated | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_3D_ICE_OPERATOR_CROSSWALK_V001.md | 7f755bbae58c40583f784d469376792cece209193113504136f20e86259b3371 |
| LOCAL_PROPER_BOND_DRESSED_VACUUM_V001.md | e8b34c02e8d0002f4ab0d8d287f8aa7e74ec5592a856ef5ffcfaf703e129b71f |
| LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
