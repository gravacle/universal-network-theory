# Intrinsic Admission Parent L4 protocol V001

**Status:** `FROZEN_CANDIDATE__PRE_OUTPUT`

**Base:** `2a21705a935d348085be18bc154c618b0d126ef4`

## 1. Objective

Test the smallest ether-free repair of the sealed same-port accumulation
obstruction. The test asks whether a complete internal admission parent can
make occupied or bandwidth-exhausted attempts null while retaining unitary
dynamics, owner-once accounting, and relational lineage.

This is a finite L4 admission trace. It cannot establish background
independence in the continuum sense, a critical sector, `z=1`, macroscopic
closure, universal coupling, metric dynamics, emergence, or gravity.

## 2. Type discipline

`ALLOW`, `REQUIRE`, and `SELECT` retain the meanings fixed by
`DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001`:

- `ALLOW` is a predicate on configurations of a completely declared parent;
- a characteristic projector exists only after the Hilbert representation is
  supplied;
- `REQUIRE` is an audit condition within the declared domain, not a production
  operator; and
- `SELECT` is the proposition that the declared dynamics and initial state
  produce the reported history, not an extra force.

The physical admission generator below is separately supplied. No modal word
is promoted into a Hamiltonian.

## 3. Uniform relational parent

The retained carrier is the owner-once periodic L4 prism with eight vertices
and twelve native transfer edges. Every prism vertex has the same local
three-state admission cell:

```text
I = inactive/empty,
R = loaded, bandwidth available, lineage open,
S = spent, bandwidth depleted, lineage sealed.
```

The uniform availability of the cell is part of the parent. The initial state,
not a distinguished boundary coupling, selects the connected genesis cluster
on four adjacent vertices of one rail. Node numbers are finite bookkeeping;
the cluster is defined relationally as a connected four-cycle and may be moved
by a prism automorphism without changing the trace observables.

The carrier begins blank. The four genesis cells begin in `R`; all other cells
factor in `I`. This is a localized dense internal initial subgraph, not an
external reservoir. Define the complete content count

```text
Q_total = Q_retained + number_of_R_cells.
```

Admission transfers content from `R` into the retained carrier. It does not
create total content ex nihilo.

## 4. Intrinsic admission generator

For a loaded cell `w` co-located with retained target `r`, define

```text
K_rel(w,r) = |S,x><R,B| + |R,B><S,x|.
```

The accepted pair includes the depleted bandwidth and sealed `(w,r)` lineage
state. The configuration predicate is

```text
ALLOW(w,r) = 1 iff cell_w=R and target_r=B.
```

Its projector is represented explicitly in the finite basis, but it does not
generate the motion. `K_rel` is Hermitian and conserves `Q_total`. In
particular,

```text
K_rel |R,x> = 0,
K_rel |I,B> = K_rel |I,x> = 0.
```

Thus an occupied-target or inactive-cell attempt is exactly null. No
measurement, clipping, nonlinear state-dependent map, or discarded outcome is
used. On an allowed component the calibrated finite test pulse is

```text
U_A = exp[-i (pi/4) K_rel].
```

It gives one-half expected retained uptake on a certainly blank target. On
each accepted branch

```text
Delta Q_retained = -Delta Q_genesis
                  = -Delta B
                  = Delta L_sealed = 1.
```

The expectation-value identities must hold at every event.

## 5. Relational chronology

A single internal cursor occupies a prism vertex and follows the adjacent
Hamiltonian cycle

```text
0 -> 1 -> 2 -> 3 -> 4 -> 7 -> 6 -> 5 -> 0.
```

Only the first four cursor events are evaluated. The same autonomous local
rule is used at every event: apply the admission exchange at the occupied
cursor vertex, route the retained carrier with the complete owner-once
Hamiltonian

```text
H_T = -sum_(e in E_L4) T_e,
kappa = pi/2,
```

and advance the cursor along one adjacent edge. The cursor position is a
relational event record in the parent, not an absolute global clock or a
boundary schedule. Along this one-pass trace every genesis cell is encountered
at most once, so a spent cell is never recoherently driven backward.

The numerical implementation may omit cursor and inactive-cell tensor factors
because they remain in known orthogonal basis states on this selected trace.
It must retain all sixteen reachable loaded/spent states of the four active
cells and all 256 retained-carrier basis states.

## 6. Required L4 outputs

For each of four events report:

- the pre-event `ALLOW` and blocked probabilities;
- reverse-support probability before the cell's first use;
- signed retained uptake `W_n`;
- the exact norm of `(U_A-I)` on the blocked component;
- `Delta Q_retained + Delta Q_genesis`;
- `Delta B + W_n` and `Delta L_sealed - W_n`;
- native transport node-ledger residuals, norm drift, and number drift; and
- retained density and remaining internal bandwidth.

Pass requires

```text
all W_n >= -1e-12,
max blocked-null error <= 1e-12,
max reverse-support probability <= 1e-12,
max admission accounting residual <= 1e-12,
max transport node L1 residual <= 1e-9,
max norm and number drift <= 1e-10,
at least one dynamically blocked component has probability > 1e-6.
```

The last condition prevents a vacuous null-state test. Target and independent
constructions must agree on every `W_n`, `ALLOW` probability, blocked
probability, and final retained charge within `1e-9`.

## 7. Decision rule and claim boundary

If all requirements pass, report

```text
PASS_L4_INTRINSIC_ADMISSION__COHERENT_UNWRITING_ELIMINATED_ON_DECLARED_TRACE
```

This means only that fresh, single-use internal admission cells eliminate the
negative-write mechanism on the declared four-event L4 trace while paying
explicit content, bandwidth, and lineage costs. It does not authorize the
L4--L12 accumulation-sector or gravity pipelines. A new preregistration would
be required to define repeated autonomous genesis, common-sector extraction,
and larger-size scaling.

Any failed numerical, ownership, null-branch, or independence check is
`FAIL_CLOSED`. No grid, external reservoir, privileged boundary, graviton,
Ward axiom, continuum assumption, or gravity claim is introduced.
