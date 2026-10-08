# Prospective connected-subdivision falsifier V001

2026-09-29. This freezes a small, **conditional added-port** test, not a claim
of spontaneous native growth, physical expansion, gravity, or CMB production.
The analytical candidate and its independent review are inputs. No outcomes
were computed to select these definitions. Root owns the freeze and execution.

## Source, Hilbert space, and fixed parameters

Use BS06 exactly in its invariant all-register-blank sector:

    H_N = -(Omega/N) sum X + Delta M
          + U_d sum_left/right (degree-d_star)^2.

Omega=U_d=d_star=hbar=1, Delta=4, N=2 and 3. The bit index of edge
(i,j) is i*N+j; integer basis bit 1 means occupied. All carrier, record,
writer and reservoir registers are blank, so BS07–BS11 annihilate them.
The source document is read and hashed, never executed. A separately expanded
degree polynomial checks the builder against the degree-square definition.

Anchor (0,0). J annihilates an absent anchor. Otherwise it removes that edge,
retains every other old link, and occupies (0,2),(2,2),(2,0), leaving the
other new links blank. J maps 16 to 512 dimensions and has rank eight.
The full conserved-charge block is old-size/excited-supply plus
new-size/empty-supply, dimension 528; no eligibility projection is made in
the evolution. In particular native flips remain able to feed an initially
ineligible anchor. Charge n_size+n_supply is exactly three.

Source B=M counts all occupied links, so B_3 J-J B_2=2J. Clamp
g=.5, gamma=.2, V=4, v_cell=1, K_g=2, K_V=1, C=.2. These are declared port
examples, not measured physical coefficients. With z_N=V-2N v_cell,
U_N=K_g*g^2/2+C*g*z_N+K_V*z_N^2/2, U_2=.25, U_3=2.05.
Thus d=2, p_2=-.1, and the elastic jump is 1.8. The fixed positive supply
gap is 10-.2+1.8=11.6, chosen from the operator constants, not a state mean.
The remaining paired-block detuning is sum_rest X/6.

The complete time-independent Hamiltonian is

    diag(H_2-.1 M_2+U_2+11.6, H_3-.1 M_3+U_3)
        + epsilon [[0,J^dagger],[J,0]].

This is a clamped-controller test; neither dynamical piston evolution nor
full record/carrier propagation is asserted. Native, insertion, elastic,
supply, and interaction energy are reported separately and sum to the
conserved total. No switching-off work is hidden or performed.

## Census fixed before outcomes

Port strengths epsilon=0,1,8. Times are the deduplicated sorted union of
0,.25,1,2 and pi/(2 epsilon) for each positive strength. Four normalized
old-sector inputs, always with excited supply:

1. four-cycle |15>;
2. tree |7>, with edges (0,0),(0,1),(1,0);
3. real coherent (|15>+|7>)/sqrt(2), supported on that same tree backbone;
4. empty graph |0>, ineligible at preparation.

All strengths, inputs, and readouts are retained: 56 state/time rows.
There is no minimum desired growth, mean energy, or connectivity success
criterion. Exact identities and rigorous applicable bounds are numerical
checks; small transfer itself is a scientific outcome.

## Qualification and independent propagation

Before readouts, verify J^dagger J=P, JJ^dagger=Q; all eight basis images'
edge counts, connected-component counts (including isolated vertices),
cycle ranks and exact reverse support; source jump; compression, both
leakage directions, full intertwiner including +h J X_a(1-P), and target
variance from candidate equations (2)–(7). Check all four old left/right
label permutations with jointly transformed anchor. No sum over anchors
is used to enhance coupling. Direct degree and expanded-polynomial native
builders must agree. Check the source-response double commutator, charge
current, connectivity and backbone port commutation, matched scalar supply
detuning, and the initial target probability's second-order coefficient.

One real symmetric eigendecomposition per strength supplies propagation.
Independently use a sparse Hamiltonian **action on the four input vectors**:
native flips are integer-XOR gathers, diagonal terms are multiplication,
and the port is indexed scatter/gather. Compare this action with the dense
matrix on a fixed deterministic complex probe before propagation. For each
readout, scaled Taylor action uses substeps 2^s with
s=max(0,ceil(log2(t*norm_inf(H)/.5))). In each substep the vector recurrence
term_k=(-i dt H term_(k-1))/k is summed until the scalar exponential-series
tail is <=1e-18. Maximum 200 series terms is an algorithm-failure guard,
not a physical run deadline. Report substep/term counts and accumulated
analytic truncation bounds `expm1(sum(log1p(substep_tail)))`; symmetry gives
norm_2(H)<=norm_inf(H), and exact substep propagation is unitary. These
bounds do not include floating-point roundoff.
No repeated dense matrix exponential or matrix-squaring Taylor method is used.

Operator entrywise absolute tolerance: 2e-11. Propagated-vector, norm,
probability, applicable bound and total-energy absolute tolerance: 2e-9.
The independent dense-action test uses 2e-11. Energy conservation is checked
in the frozen native energy units, not a rescaled outcome-dependent norm.
No tolerance will be enlarged after outcomes without a separately preserved
attempt and an explicit numerical justification.

At each row retain both sector probabilities, source eligibility, exact
target Q/reverse support, target probability outside Q, connectivity in each
sector, backbone support, signed creation current and incidence response
moment, the complete energy ledger and its changes, and eigen/Taylor error.
The empty input has no connected-backbone guarantee. For each eligible input
test the candidate Eq.(14) readout bound using M0=4 (cycle) or 3 (tree/coherent).
At the positive-strength swap readout test Eq.(15) with delta=.5 and
ell=sqrt(2/3). Bounds with value zero remain in the report. Neither bound is
a first-passage probability, permanent-growth statement, or native port proof.

## Custody and resources

Only `connected_subdivision_v001.py` and this protocol are new implementation
files. `freeze` prints the full configuration and hashes to stdout without
calculating outcomes. Normal execution requires the exact parsed
CONNECTED_SUBDIVISION_V001_FROZEN.json snapshot and prints a JSON wrapper
with source-freeze hash, canonical payload hash, all checks and failures,
actual elapsed time and process peak RSS. Root redirects output additively;
the script never writes or replaces result files. Hashes cover itself,
this protocol, candidate, both independent analytical reviews, inherited controller/volume/
connectivity notes, and the exact resident original BS action. Every path
must resolve inside the project root. No input code is imported or executed.

Set the five numerical thread environment variables to one before NumPy.
The largest dense matrix is 528 square; no new packages, large-register
worker, checkpoint infrastructure, or arbitrary wall-clock cutoff is added.
All physical/numerical choices above precede the outcomes. Previous evidence
is untouched, and this test cannot update a galaxy or cosmological parameter.
