# Owner-once joint lineage--carrier witness protocol V001

Date: 2026-09-22

Status: `FROZEN_CANDIDATE__PRE_IMPLEMENTATION_AND_PRE_OUTPUT`

## 1. Single question

The exact carrier-marginal closure theorem shows that the frozen owner-once
accumulation history has a carrier-only channel reproducing every
unconditional carrier observable when the lineage register is unread.  This
protocol asks the complementary finite question:

> Does the same terminal state contain a resolved correlation between the
> canonical spent-lineage label and the current carrier location that cannot
> be reconstructed from the unconditional carrier marginal?

Only the one joint observable frozen below may answer this question.  No
alternative operator, checkpoint, normalization, sign choice, density window,
or best-size selection may be introduced after output is opened.

## 2. Frozen parent and chronology

Do not alter the parent in
[`DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001`](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md).
For each size, use its periodic two-rail degree-three prism, blank carrier
initial state, loaded active cycle, event order, admission angle
`phi=pi/4`, transport dwell `pi/2`, and first owner-once pass.  Event labels
are zero based and coincide with their co-located carrier targets on the first
rail.

The mandatory seed schedule is:

| Size | Events, in order | Primary checkpoint |
|---:|---|---|
| `L=4` | `0,1,2,3` | after event `3` transport, before revisit |
| `L=6` | `0,1,2,3,4,5` | after event `5` transport, before revisit |
| `L=8` | `0,1,2,3,4,5,6,7` | after event `7` transport, before revisit |

For audit only, record the same quantities before admission, after admission,
and after transport at every event.  Those intermediate rows cannot replace,
average with, or rescue the primary terminal checkpoint.

The dense seed target retains the frozen order-12 Taylor propagation at 64
and 128 substeps per dwell.  A separately written reconstruction must use an
independent basis order, edge order, admission implementation, transport
implementation, and marginal accumulator.  It may not import target arrays,
matrices, code, or result values.

## 3. Existing joint representation

At the primary checkpoint write the exact state in the already proved basis

\[
  |\Psi_L\rangle
   =\sum_{q=0}^{L}\ \sum_{S\in { [L]\choose q}}\
      \sum_{C\in { [2L]\choose q}}
      A_{L,q}(S,C)|S,C\rangle .                 \tag{1}
\]

`S` is the canonical set of spent genesis cells and `C` is the carrier
configuration.  Define

\[
  p_{L,q}(S,C)=|A_{L,q}(S,C)|^2,\qquad
  p_{L,q}=\sum_{S,C}p_{L,q}(S,C).               \tag{2}
\]

Let

\[
  F_e(S)={\bf1}_{e\in S},\qquad
  n_e(C)={\bf1}_{e\in C},\qquad e=0,\ldots,L-1. \tag{3}
\]

`F_e` is the spent-lineage bit already stored by the engine; in the original
loaded-bit representation it is `1-loaded_e`.  `n_e` is the existing carrier
occupation at the event's first-rail target.  Equation (1) already enforces

\[
  Q_S=\sum_e F_e=Q_C=\sum_{x=0}^{2L-1}n_x=q       \tag{4}
\]

inside every sharp sector.  No new dynamical degree of freedom is added.

## 4. The one frozen joint observable

Define the centered terminal overlap operator

\[
  \widehat W_L={1\over L}\sum_{e=0}^{L-1}
       \left(\widehat F_e-{\widehat Q\over L}\right)\widehat n_e,
  \qquad \widehat Q=\sum_e\widehat F_e.          \tag{5}
\]

All factors in (5) are commuting diagonal operators in the existing basis.
The `Q/L` term removes the overlap expected solely from the number of spent
labels in a sharp-`q` sector.  The observed value is

\[
 w_L={1\over L}\sum_{q,S,C}p_{L,q}(S,C)
       \sum_{e=0}^{L-1}\left(F_e(S)-{q\over L}\right)n_e(C). \tag{6}
\]

This observable is lineage diagonal, so the frozen final two-child streaming
representation evaluates it by exact addition.  No cross-lineage term is
discarded because (5) has no such term.

### Why the carrier marginal cannot determine it

For any `L>=2`, consider the two normalized `q=1` states

\[
 |\Psi_{\rm match}\rangle=
 { |\{0\},\{0\}\rangle+|\{1\},\{1\}\rangle\over\sqrt2},
 \quad
 |\Psi_{\rm cross}\rangle=
 { |\{0\},\{1\}\rangle+|\{1\},\{0\}\rangle\over\sqrt2}. \tag{7}
\]

They have identical carrier marginals, identical lineage marginals, and the
same sharp-`q` weight.  Nevertheless, their observed-minus-sham values defined
below are respectively `+1/(2L)` and `-1/(2L)`.  Thus no function of the
unconditional carrier marginal can reconstruct the frozen witness.  This is
a non-identifiability statement about joint information; it is not an
entanglement test.

## 5. Two frozen controls

### 5.1 Within-`q` lineage shuffle

At fixed `q`, average the lineage register over every permutation of its `L`
event labels while holding the carrier register fixed:

\[
 \rho^{\rm shuffle}_{L,q}={1\over L!}\sum_{\pi\in\mathfrak S_L}
 (U^S_\pi\otimes I_C)\rho_{L,q}(U^S_\pi\otimes I_C)^\dagger . \tag{8}
\]

This preserves the complete carrier marginal and sharp-`q` weights exactly.
Because the permutation orbit of every `q`-element lineage set is uniform,

\[
 {1\over L!}\sum_\pi F_e(\pi S)={q\over L},
 \qquad w_L^{\rm shuffle}=0.                    \tag{9}
\]

Implementations shall evaluate the exact twirl identity directly; they shall
not sample a favorable set of random permutations.  They must also enumerate
the full permutation control at L4 as an implementation check.

### 5.2 Sector-matched sham register

Let `rho_(L,q)` be the unnormalized density operator in sharp sector `q` and
form its unnormalized quantum marginals

\[
 \rho^S_{L,q}={\rm Tr}_C\rho_{L,q},\qquad
 \rho^C_{L,q}={\rm Tr}_S\rho_{L,q}.              \tag{10}
\]

Their diagonal entries are

\[
 P^S_{L,q}(S)=\sum_Cp_{L,q}(S,C),\qquad
 P^C_{L,q}(C)=\sum_Sp_{L,q}(S,C).                \tag{11}
\]

For each sector with `p_(L,q)>0`, define the sham state and its joint diagonal

\[
 \rho^{\rm sham}_{L,q}=
 {\rho^S_{L,q}\otimes\rho^C_{L,q}\over p_{L,q}},\qquad
 p^{\rm sham}_{L,q}(S,C)=
 {P^S_{L,q}(S)P^C_{L,q}(C)\over p_{L,q}}.        \tag{12}
\]

The sham register preserves the complete within-`q` lineage and carrier
density marginals and the sector weight, but makes the two registers a product
inside each `q`.  Its fixed expectation is

\[
 w_L^{\rm sham}={1\over L}\sum_{q:p_{L,q}>0}{1\over p_{L,q}}
 \sum_e
 \left[\sum_SP^S_{L,q}(S)\left(F_e(S)-{q\over L}\right)\right]
 \left[\sum_CP^C_{L,q}(C)n_e(C)\right].          \tag{13}
\]

No pseudorandom seed enters (12).  The primary per-size effect is the
conditional-covariance witness

\[
 D_L=w_L-w_L^{\rm sham}
 ={1\over L}\sum_{q,e}p_{L,q}\,
       {\rm Cov}_{L,q}(F_e,n_e).                 \tag{14}
\]

The shuffle and sham controls answer different objections: (8) removes label
placement while preserving the carrier state; (12) preserves both separate
marginals while removing only their joint association.

## 6. Fixed statistic and falsifier

For each mandatory size let `d_L` be the largest absolute disagreement among:

1. target 64-versus-128-substep values;
2. target-versus-independent values; and
3. independently accumulated row-streaming versus column-streaming values,

for `w_L`, `w_L^sham`, `D_L`, every `q`-resolved contribution to `D_L`, and
every `p_(L,q)`.  Let `r_L` be the largest norm, probability-normalization,
marginal-reconstruction, or `Q_S-Q_C` residual.  Freeze the resolution scale

\[
 \tau_L=\max(10^{-9},\ 50d_L,\ 100r_L).          \tag{15}
\]

The sole seed primary statistic is

\[
 T_{4:8}=\min_{L\in\{4,6,8\}}{|D_L|\over\tau_L}. \tag{16}
\]

This is a two-sided test; the sign is reported but is not selected in
advance.  The fixed seed witness passes only if all numerical and control
conditions in Section 7 pass and

```text
T_4:8 > 1.
```

It then returns

```text
RESOLVED_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L4_L8
```

If every numerical/control condition passes but `T_4:8<=1`, the
preregistered witness is falsified at one or more mandatory sizes and returns

```text
NO_RESOLVED_OWNER_ONCE_JOINT_MEMORY_IN_FIXED_WITNESS_L4_L8
```

That result falsifies this observable and schedule, not every possible joint
observable.  A nonfinite value or numerical/control failure returns

```text
OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED
```

and is not converted into a physical pass or falsifier.

## 7. Frozen numerical and audit conditions

All of the following are mandatory at each seed size:

```text
target coarse/fine disagreement              <= 1e-8
target/independent disagreement               <= 1e-8
norm and total-content residual               <= 1e-10
probability and marginal reconstruction error <= 1e-10
sharp-sector Q_S-Q_C error                    <= 1e-10
absolute within-q shuffle expectation         <= 1e-12
sham self-covariance residual                  <= 1e-12
```

L4 additionally requires exhaustive direct-basis sums for (6), (8), and
(13), explicit enumeration of all lineage permutations in (8), and agreement
with the streamed accumulators within `1e-12`.

Every implementation must report `w_L`, `w_L^sham`, `D_L`,
`w_L^shuffle`, all `q` contributions, all residuals, `d_L`, `tau_L`, and the
Boolean conditions without clipping.  JSON output must be deterministic and
contain source hashes, fixed parameters, relative paths only, and no host or
timestamp fields.

The independent audit must be written and hashed before it reads target
output.  It may read the frozen protocol and historical model definition but
may not import target code, basis maps, matrices, intermediate arrays, or
result values.  No tolerance may change after either output is opened.

As a mandatory negative control, replacing the actual joint state by (12)
must return `D_L=0` within the sham tolerance.  Replacing it by (8) must return
`w_L=0` within the shuffle tolerance.  Failure to reject either known-null
control makes the implementation unresolved.

## 8. Held-out L10/L12 rule

The dedicated `D_10` and `D_12` witness values and their result records remain
uncomputed and unopened while the seed witness is implemented and run.
Pre-existing L10/L12 history artifacts are historical inputs; their existence
does not make this newly registered readout a new physical experiment.  The
larger-size readout is authorized only after:

1. the complete L4/L6/L8 target and independent records are frozen;
2. `T_4:8>1` and every seed control passes;
3. all code, protocol, result, and audit hashes are sealed; and
4. the existing exact streamed-history resource gate independently permits
   the larger calculation.

The held-out event schedules are `0,...,9` at L10 and `0,...,11` at L12.  In
each case the only primary checkpoint remains after the final event's
transport and before a revisit.  Use the already frozen adaptive target and
independent streamed propagators; do not replace exact lineage rows with the
carrier channel, a macro closure, a fitted distribution, or a sampled
surrogate.

Calculate `D_10`, `D_12`, `tau_10`, and `tau_12` by the unchanged equations
and define

\[
 T_{10:12}=\min\left({|D_{10}|\over\tau_{10}},
                     {|D_{12}|\over\tau_{12}}\right).         \tag{17}
\]

No seed fit or extrapolation enters (17).  If both calculations and controls
resolve and `T_10:12>1`, return

```text
HELD_OUT_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L10_L12
```

If their numerics resolve but `T_10:12<=1`, return

```text
HELD_OUT_OWNER_ONCE_JOINT_WITNESS_NOT_REPRODUCED
```

If exact evaluation exceeds the pre-existing resource gate, return

```text
EXACT_JOINT_WITNESS_SCALING_OBSTRUCTION
```

without approximation.  None of these finite outcomes licenses an all-`L`
limit.

## 9. Claim boundary

A seed or held-out pass would prove only that this existing finite
owner-once engine retains a resolved terminal lineage--carrier correlation
that is absent from its unconditional carrier marginal and from the two
preregistered controls.  It would not prove that the correlation changes
future dynamics, survives a revisit, is an entanglement witness, or has a
thermodynamic or continuum limit.

This protocol does not use or test the ARGER Gate, the Record--Geometry
Realization Law, alpha, a dynamical exponent, spacetime, metric response,
Einstein--Hilbert dynamics, or gravity.  It imports no record-reading operator
from GL6T or any other surface.  Any future dynamical use of the lineage bit
requires a separately frozen same-parent interaction and cannot be inferred
from this terminal diagnostic.

No external reservoir, controller, boundary, clock, lineage quotient,
postselection, truncation, or branch deletion is introduced.

## 10. Source grounding

- [Owner-once parent, event order, admission, transport, and guards](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md)
- [Dense seed implementation and existing diagonal basis data](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py)
- [Exact streamed spent-mask/carrier blocks](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py)
- [Streamed L10/L12 method and independence gate](../DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/STREAMED_METHOD_FREEZE.md)
- [Exact prefix support and terminal two-child representation](../DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PROTOCOL.md)
- [Spent-lineage basis and terminal reconstruction theorem](../DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md)
- [Exact owner-once carrier-marginal closure and boundary](../DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001/THEOREM.md)
