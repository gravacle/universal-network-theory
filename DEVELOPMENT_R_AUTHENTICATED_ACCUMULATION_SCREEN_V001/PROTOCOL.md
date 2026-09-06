# Draft protocol: Authenticated Accumulation Screen V001

**Status:** `FROZEN_CANDIDATE__USER_AUTHORIZED__PRE_OUTPUT`

**Baseline:** detached commit
`cd1d8b2a47778e8176ebf8f0132fe10853a2ac08`

## 1. Objective and bounded claim

This protocol replaces the rejected top-down `rho=1/4` centerline with a
density interval produced by one completely declared finite history.  The
history begins with the all-blank retained carrier, applies repeated copies of
the authenticated F3-MDC write pulse at one source port, and routes between
pulses with the owner-once native carrier Hamiltonian.  The realized retained
number distribution, source-port uptake, and connector response determine
which density cells, if any, are eligible for a later spectral sweep.

The screen may return a finite `z=1`-compatible accumulation interval.  It
cannot prove a continuum, a thermodynamic phase, a metric, universal coupling,
emergence, Gate B, or gravity.  A null rejects only this declared history,
response channel, and finite scaling window.

No solver, target history, or target eigenspectrum may be evaluated until this
protocol, the target implementation, and the hostile method are hash-frozen in
a pre-output commit.  The user's 2026-09-06 instruction to proceed through
completion supplies the execution authorization after that freeze.

## 2. Type correction and controlling antecedents

`DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001` supplies the typed distinction
among admissibility, a characteristic projector, occupancy, internal dynamics,
and dynamical selection.  It does **not** define a physical write Hamiltonian.
Accordingly this protocol uses:

1. the scope-repair definitions `A_P`, `Pi_P`, `D_P`, and `SELECT` only as a
   type discipline;
2. the audited F3-MDC generator `K_(w->r)` and calibrated pulse
   `Phi=pi/4` as the conditional physical write;
3. the native BS07--BS09 transfers `T_e` as the physical transport; and
4. the Gate A-R owner-once incidence ledger as the conservation rule.

No `ALLOW` or `REQUIRE` predicate is promoted into a causal operator.
`REQUIRE` below always means a universal audit obligation on the declared
history.  `SELECT` means only that the fixed chronological product selects one
occupancy from the admitted enlarged parent.

The target freeze must pin at least these antecedents and their independent
audits:

- `DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/FORMAL_SCOPE_THEOREM.md`;
- `DEVELOPMENT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001/THEOREM.md`;
- `DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/THEOREM.md`;
- `CERTIFICATE_GATE_A_R_RECORD_OWNERSHIP_CONSERVATION_V001/CERTIFICATE.md`;
- the owner-once connected-prism construction; and
- the rejected centerline protocol and final hostile reports at
  `cd1d8b2a47778e8176ebf8f0132fe10853a2ac08`.

Any antecedent hash mismatch is `FAIL_CLOSED`.

## 3. Finite parent and native operators

### 3.1 Retained carrier

For each even `L in {4,6,8,10,12}`, use the audited degree-three periodic
prism with retained sites `(a,i)`, `a in {0,1}`, `i in Z/LZ`.  Its owner list
contains the two rail cycles and the shifted connectors

```text
(0,i)--(1,i+1 mod L).
```

Every physical support edge appears exactly once.  Tuple labels enumerate
finite support and do not define a grid or physical distance.  On the
blank/content sector put

```text
Q_L = sum_v n_v,
H_L = -t sum_(e in E_L) T_e,
[H_L,Q_L] = 0.
```

The zero representative is used for the uniform onsite term.  There is no
write-count-dependent Hamiltonian `H(N)`.

### 3.2 Authenticated write event

Choose one source vertex `s_L=(0,0)`.  Before target execution the structural
audit must prove that all vertices are in one automorphism orbit; otherwise
one complete history is required for every vertex orbit, and all later gates
must pass for every orbit.

For event `n`, introduce its separately owned fixed-content writer `w_n` and
the audited generator

```text
K_(w_n->s_L) = |x><x|_(w_n) tensor
               (|x><B|_(s_L)+|B><x|_(s_L)).
```

With network transport terms off, apply exactly

```text
U_W,n = exp[-i (pi/4) K_(w_n->s_L)].
```

The calibration remains the adopted F3-MDC attachment

```text
r0 = 14441248/6075,
epsilon_* = pi/(4 r0),
Phi = pi/4.
```

The first event acts on a certainly blank target and therefore has exactly
`W_1=Delta<Q_L>=1/2`.  Later events use the same authenticated operator and
pulse, but the source site need not be blank.  Their signed source ledger
terms

```text
W_n = integral (i/hbar)<[H_W,n(t),Q_L]> dt
```

must be calculated from the actual pre-write state.  They may not be replaced
by `1/2`, clipped, or called successful writes by assumption.  A negative or
oscillatory `W_n` is retained and can falsify the accumulation classification.

Because each `w_n` starts in the projector eigenstate `|x>` and remains there
under the displayed generator, the writer factors separate analytically from
the retained-carrier state.  The preflight audit must prove this factorization
and preserve the complete writer/controller outcome alphabet.  If an added
controller, feedback rule, or port entangles with the retained carrier, the
reduced pure-state representation is invalid and execution halts for a new
resource review; the enlarged tensor product may not be silently discarded or
brute-forced.

### 3.3 Chronological accumulation history

Start with

```text
|Psi_L,0> = |B>^(tensor 2L).
```

After each write, turn the source off and route under the complete owner-once
Hamiltonian for the already used conditional interval

```text
kappa = t tau_T/hbar = pi/2,
U_T,L = exp[-i H_L tau_T/hbar].
```

The frozen recurrence is

```text
|Psi_L,n> = U_T,L U_W,n |Psi_L,n-1>,
n=1,...,N_max(L),
N_max(L)=4L.
```

`kappa`, the common source vertex, and `N_max` are adopted finite-history
choices.  They are not selected constants of nature.  No result-dependent
change of pulse, dwell time, source site, edge support, or stop count is
allowed.

This chronological product is the protocol's `SELECT` map.  Density is never
an input.  At every event report

```text
p_L,n(q) = <Psi_L,n|P_(L,q)|Psi_L,n>,
rho_bar_L(n) = sum_q q p_L,n(q)/(2L),
var_rho_L(n) = sum_q (q/(2L)-rho_bar_L(n))^2 p_L,n(q).
```

The full `p_L,n(q)` distribution is primary.  `rho_bar` alone is not a sharp
sector and may not be substituted for one.

## 4. Owner-once ledger and routing-capacity record

### 4.1 Event ledger

For every event retain separate write-slice and transport-slice ledgers.  With
the stored incidence matrix `B`, the eventwise node identity is

```text
Delta q_v,n + sum_e B_(v,e) J_e,n - delta_(v,s_L) W_n = r_v,n.
```

The write slice has all network edges off.  The transport slice has the source
off and contains each support edge once.  Internal currents must telescope
exactly by incidence before numerical evolution.  Report raw `r_v,n`, its L1
and Linf norms, norm drift, number balance, and energy drift on each applicable
slice.  Numerical remainders are unassigned terms, not physical defects.

Every required event must satisfy

```text
||r_n||_1 <= max(1e-10, 100 epsilon_prop),
||r_n||_inf <= max(1e-11, 20 epsilon_prop),
norm error <= 1e-10,
```

where `epsilon_prop` is the independently measured coarse/fine or last-two-
Krylov propagation disagreement.  A failure makes that size `UNRESOLVED`.

### 4.2 Marginal source and connector capacity

The source-port uptake is

```text
c_W,L(n) = W_n/W_1 = 2 W_n.
```

Retain its sign.  For boundary finding only, put

```text
c_W,L^+(n) = max(0,c_W,L(n)).
```

To measure routed capacity, fork the exact same pre-write state into two
calculation branches:

```text
actual:     U_T,L U_W,n |Psi_L,n-1>,
null-write: U_T,L       |Psi_L,n-1>.
```

The null branch is a counterfactual calculation, not another physical
lineage.  Over the fixed transport slice define

```text
delta J_e,L(n) = J_e,L(actual)-J_e,L(null-write),
c_J,L(n) = sum_(e connector)|delta J_e,L(n)| /
           sum_(e connector)|delta J_e,L(1)|.
```

The signed connector sum is retained separately.  The operational serial
bottleneck is the adopted statistic

```text
c_L(n) = min(c_W,L^+(n),c_J,L(n)).
```

This statistic does not assert a thermodynamic capacity.  It says only that a
new record must both enter at the source and be carried through the declared
connector set.  If either denominator is not positive above error, the size is
`UNRESOLVED`.

Set

```text
epsilon_c,L = max(1e-8,
                  50 * maximum relative propagation/ledger disagreement).
```

The accumulated history is admissible for sector extraction only if
`|c_L(1)-1|<=epsilon_c,L`, the first three `W_n` are positive above error, and
the complete signed and L1 capacity trajectories are retained.

## 5. Accumulation-generated sector boundaries

### 5.1 Depletion window

For `alpha in {0.75,0.25}`, define the first sustained upper-confidence
crossing

```text
n_alpha(L) = min n such that
             c_L(m)+epsilon_c,L <= alpha
             for m=n,n+1,n+2.
```

The finite depletion window is

```text
N_dep(L) = {n_0.75(L),...,n_0.25(L)+2}.
```

It exists only if both crossings occur by `N_max`,
`n_0.25>n_0.75`, all event ledgers resolve, and no raw negative `W_n` occurs
before the `0.25` crossing.  Failure to cross is
`NO_BOUNDED_DEPLETION_WINDOW_L`; ambiguity within `epsilon_c` is
`UNRESOLVED_DEPLETION_WINDOW_L`.  Neither result authorizes a spectral sweep
for that size.

The `0.75/0.25`, three-event persistence, `N_max=4L`, and error multipliers are
adopted operational boundaries.  The densities at their crossings are
outputs.  They are not called critical densities.

### 5.2 Number-sector support

Average the history-generated sector weights only over the depletion window:

```text
pbar_L(q) = |N_dep(L)|^(-1) sum_(n in N_dep(L)) p_L,n(q).
```

Let `[q_-(L),q_+(L)]` be the shortest contiguous integer interval carrying at
least `0.99` of `pbar_L`.  Resolve ties first by larger enclosed mass and then
by smaller `q_-`.  Its finite density-cell envelope is

```text
I_acc(L) = [(q_-(L)-1/2)/(2L),
            (q_+(L)+1/2)/(2L)] intersect [0,1].
```

The cross-size eligible region is

```text
I_acc = intersection_(L in {4,6,8,10,12}) I_acc(L).
```

If `I_acc` is empty or disconnected after numerical uncertainty is included,
return `NO_COMMON_ACCUMULATION_SECTOR_L4_L12`.  Do not choose a favorable
density afterward.  Report the discarded `0.01` tail and all individual
`I_acc(L)` boundaries.

This is an accumulation-generated **candidate sector**, not a macroscopic
phase.  Sharp `q` calculations below are diagnostic components of the actual
history distribution; they are not claimed to be post-selected physical
histories.

## 6. Staged interval Krylov sweep

### 6.1 Freeze between history and spectrum

After target and blind history implementations agree, freeze their raw hashes,
`N_dep(L)`, `pbar_L`, every interval endpoint, and all eligible `q` values.
No spectral output may be inspected before this intermediate freeze.  The
history calculation is first run at `L={4,6,8}`.  `L10/L12` history and any
eigenspectrum work are authorized only if the L4--L8 accumulation intervals
have a nonempty connected intersection under the rules above.

Partition `I_acc` at every boundary

```text
(q+1/2)/(2L),  L in {4,6,8,10,12}.
```

Use half-open cells, closing only the final right endpoint.  Each resulting
positive-width density atom `A_j` selects exactly one sharp sector `q_L(A_j)`
at every size.  Boundary-only intersections have zero width and are discarded.
Every eligible atom is swept; no best-density optimization is allowed.

### 6.2 Response-active Krylov record

For each `(L,q_L(A_j))`, use the already frozen total-rail `m=1` density mode
and compute

```text
Delta_act = lowest positive pole with authenticated response weight,
chi_tau   = sqrt[sum_a w_a/omega_a^2 / sum_a w_a],
R_low     = w_(Delta_act)/sum_a w_a.
```

L4/L6/L8 use complete sector spectra.  L10/L12 use independently constructed
translation blocks and fully reorthogonalized response-cyclic Krylov spaces at
dimensions `16,32,64,96,128`.  Dense L10/L12 conversion is forbidden.  Reuse
the centerline residual, Hermiticity, orthogonality, threshold-stability,
matvec, and target/blind disagreement guards without relaxation.

## 7. Exact preregistered `z=1` falsification rule

For every density atom fit the five L4--L12 rows to

```text
fixed-z1:      a/L + b/L^2,
free-gapless:  a L^(-z),
positive-gap:  Delta_inf + a L^(-z),
```

with the same domains and leave-one-size-out relative-error score used by the
sealed centerline screen.  Fit `chi_tau=c L^y` on the log scale.

An atom passes if and only if **all** of these frozen checks pass:

1. `Delta_act` strictly decreases and `chi_tau` strictly increases with `L`;
2. fixed-`z=1` held-out SSE is strictly smaller than positive-gap SSE and no
   larger than `1.25` times free-gapless SSE;
3. `z,y in [0.90,1.10]` and `|z-y|<=0.10`;
4. over `L={8,10,12}`, the relative ranges of `L Delta_act` and `chi_tau/L`
   are each at most `0.05`;
5. `R_low>=1e-6` at every size and its L8--L12 relative range is at most
   `0.35`; and
6. no threshold, density-cell, or response-pole identity ambiguity exceeds
   its frozen numerical guard.

Passing atoms are joined only when they share a boundary.  A connected
component is an `AUTHENTICATED_ACCUMULATION_Z1_INTERVAL_CANDIDATE` only if:

1. every atom in the component passes;
2. the component contains the centers of at least two adjacent L10 sectors
   and at least two adjacent L12 sectors;
3. for every `L`, its sectors carry at least `0.50` of `pbar_L`; and
4. target and blind implementations agree within `2e-8` for energies/gaps,
   `5e-7` for `chi_tau`, `5e-6` for residues, and exactly on every Boolean
   classification.

The complete screen returns exactly one of:

```text
AUTHENTICATED_ACCUMULATION_Z1_INTERVAL_CANDIDATE_L4_L12
AUTHENTICATED_ACCUMULATION_Z1_REJECTED_L4_L12
NO_COMMON_ACCUMULATION_SECTOR_L4_L12
UNRESOLVED_AUTHENTICATED_ACCUMULATION_SCREEN
```

Any failed required check yields the rejection or unresolved result; thresholds
may not be loosened after output.  A passing candidate authorizes only a newly
frozen next-stage protocol.  It is not a proof of exact `z=1` or a continuum.

## 8. Independent hostile implementation

Before target output is opened, freeze a second implementation that does not
import target code or raw matrices.  It must independently reconstruct:

- owner topology, source and transport generators, and source-factor proof;
- every event state or certified reduced equivalent;
- `W_n`, all node/current ledgers, `p_L,n(q)`, and capacity curves;
- both depletion crossings and all sector boundaries;
- every density atom and sharp-sector mapping;
- every Krylov pole, weight, fit, and final Boolean; and
- all resource and claim-boundary checks.

The first audit may fail and be repaired only through a separately recorded,
bounded change followed by a complete replay.  Promotion requires a fresh
hostile pass.  If the source factors do not separate or the minimum exact
boundary record grows beyond the resource guards, halt and report that
obstruction rather than inserting an unreviewed tensor-network truncation.

## 9. Resource model and hard bounds

### 9.1 Accumulation-history representation

The intended first implementation is a matrix-free retained-carrier pure
state.  Its dimension is `2^(2L)`.  The exact central-sector and conservative
storage figures are:

| L | retained sites | full history dimension | one complex128 state | largest `q=L` sector | translation-zero block | 128 block vectors |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 8 | 256 | 0.004 MiB | 70 | 20 | 0.04 MiB |
| 6 | 12 | 4,096 | 0.063 MiB | 924 | 160 | 0.31 MiB |
| 8 | 16 | 65,536 | 1 MiB | 12,870 | 1,620 | 3.16 MiB |
| 10 | 20 | 1,048,576 | 16 MiB | 184,756 | 18,504 | 36.14 MiB |
| 12 | 24 | 16,777,216 | 256 MiB | 2,704,156 | 225,440 | 440.31 MiB |

The history engine may retain at most six full complex work vectors.  Raw
state storage is therefore at most `1.5 GiB` at L12; edge maps, current
quadrature, checkpoints, and allocator overhead give a conservative
`6 GiB` expected peak.  Hard limits are `12 GiB` per process and `40 GiB`
aggregate on the 48 GiB host.  Target and blind L12 histories may run together
only after measured L10 peaks show their combined upper bound below `36 GiB`.

Transport uses adaptive matrix-free Krylov exponential action at retained
dimensions `16,32,48,64`, with last-two norm/observable agreement at `1e-10`.
No dwell may exceed 64 Hamiltonian matvecs; no size may exceed `4L` dwells.
Failure at the cap is `UNRESOLVED`, not permission to enlarge the basis.

### 9.2 Estimated processing time

These are planning bounds, not measured complexity claims:

| phase | target CPU estimate | independent CPU estimate | parallel wall estimate |
|---|---:|---:|---:|
| L4/L6/L8 history and ledgers | 0.5--1.5 h | 0.5--1.5 h | 0.5--2 h |
| L10 history | 1--4 h | 1--4 h | 1--5 h |
| L12 history | 6--14 h | 6--14 h | 6--16 h |
| history comparison/freeze | 0.5--1 h | 0.5--1 h | 0.5--1 h |
| **accumulation phase total** | **8--20.5 h** | **8--20.5 h** | **8--24 h with two implementations in parallel** |

The later sector sweep is separate.  Sequential reuse of one translation
block keeps expected per-process memory below `4 GiB` for most intervals and
below the same `12 GiB` hard cap at the L12 central sector.  Its runtime scales
with the number of history-selected density atoms and must be estimated again
from the frozen accumulation output before authorization.

Abort rather than continue if projected runtime exceeds `24` wall hours for
one history wave, RSS exceeds a guard, a writer/controller factor fails to
separate, or an exact lineage/boundary record requires exponential storage not
represented by the declared pure-state factorization.

## 10. Claim classification

**Proved inputs:** finite owner-once topology and incidence telescoping; native
number-conserving transfer; the conditional authenticated write unitary and
its first blank-target `W=1/2` ledger; and the scoped distinction among
admissibility, occupancy, and dynamics.

**Adopted by this protocol:** the prism parent, common source vertex, repeated
chronology, `Phi=pi/4`, `kappa=pi/2`, `N_max=4L`, connector L1 bottleneck,
`0.75/0.25` depletion crossings, three-event persistence, `0.99` sector mass,
`0.50` candidate-mass coverage, response mode, fit families, and every
numerical threshold.

**Conditional:** F3-MDC `alpha=r0`; the complete controller/source parent;
writer-factor separation; support, pulse and dwell selection; and future
numerical implementations.

**Empirical after execution only:** the eventwise densities, uptake and
connector trajectories, depletion windows, generated sector boundaries,
Krylov records, fits, and finite-window classification.

**Open:** a physical autonomous source-site or schedule selector; a
thermodynamic phase or critical density; exact `z=1`; continuum behavior;
macroscopic closure; universal coupling; attraction; metric behavior;
emergence; and gravity.
