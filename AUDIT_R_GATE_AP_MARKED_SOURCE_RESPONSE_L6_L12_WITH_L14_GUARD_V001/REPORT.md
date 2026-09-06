# Hostile audit report

## Scope and disposition

The target is the finite marked-source response packet
`DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001`. The target was not edited.
All target artifacts, the sealed finite baselines, the prior authenticated
source-parent audit, and the prior direct L6/L8 hostile reconstruction are
hash-pinned by `verify_audit.py`.

The result is a pass with no target correction. This closes the required
hostile audit of this bounded calculation only. Gate A-P remains open.

## Complete finite parent and source stabilizer

For each even `L` in `{6,8,10,12,14}`, the verifier independently rebuilds
the complete connected support graph with `2L` sites and `3L` owner-once
edges: two oriented `L`-cycles and the `L` connectors
`A_i -> B_(i+1 mod L)`. Every site has degree three.

Rather than copying the target's closed group formula, the verifier generates
the parity-preserving content group from a rotation and a reflection and
closes those generators under composition. Its order is `2L`. The stabilizer
of source label `A_0` is exactly

```text
H_0 = {identity, f},
f(A_s) = A_(-s),
f(B_s) = B_(2-s)                 (indices modulo L).
```

The nonidentity element is an involution, fixes four sites, and has `L+2`
cycles on the `2L` site labels. The Burnside dimension is therefore

```text
dim V^(H_0) = (2^(2L) + 2^(L+2)) / 2.
```

This independently gives orbit dimensions
`2176, 33280, 526336, 8396800, 134250496` for
`L=6,8,10,12,14`. Signed physical-edge orbit reconstruction is complete and
owner-once, giving `10,13,16,19,22` edge orbits.

## Raw source jet to normalized writer

For a configuration orbit `O_x`, the independent basis is

```text
|[x]> = |O_x|^(-1/2) sum_(z in O_x) |z>.
```

An active physical parent edge exchanges the two unequal endpoint bits with
raw hopping coefficient `-1`. Projection between normalized source and
destination orbits gives the representative transition coefficient

```text
-sqrt(|O_x| / |O_y|).
```

The verifier does not merely assume this attachment. At L6 it enumerates all
4096 physical configurations, constructs every normalized orbit, projects
every raw physical hop, and compares the resulting action against the
representative rule. The maximum difference is
`2.220446049250313e-16`; the independently projected action is Hermitian to
machine zero. This is a finite action/ownership result, not a Ward axiom.

## Complete numerical cross-checks

L6 and L8 use the prior independent matrix-free full-space RK4 reconstruction.
All six complete vectors (`q_0`, `q_1`, `delta q`, `J_0`, `J_1`, `delta J`)
agree with the marked-source target within `4e-11`. This is complete parity.

L10 and L12 use `independent_mps_response.py`, a separate formulation that
does not import the target compute implementation. It groups
`(A_i,B_(i+1))` into four-state rungs, evolves a canonical open-boundary MPS
with fourth-order Yoshida splitting, moves the finite cycle cut by exact
local SWAP gates, and integrates every oriented current by composite Simpson
quadrature. Both histories and all six complete vectors are emitted.

The recorded runs used 8 coarse steps, 16 fine steps, bond cap 256, and
relative SVD cutoff `1e-11`:

| L | max target Linf over all six vectors | max coarse/fine Linf | min fine norm | raw differential remainder L1 | runtime (s) | max RSS (bytes, Darwin) |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 4.4054131815088327e-4 | 8.159437729113039e-4 | 0.9983827823814848 | 0.0023506416483911607 | 275.631663250 | 551845888 |
| 12 | 8.632564165723666e-4 | 7.889684564860722e-4 | 0.9956775504259937 | 0.004831736017688479 | 601.258777375 | 599998464 |

These satisfy the declared `1e-3` complete-vector and refinement ceilings,
the `0.995` retained-norm floor, and the `0.005` raw differential-remainder
ceiling. They are approximate empirical corroboration, not exact parity and
not an assertion that the remainder is a physical defect or unnecessary
term.

Replay commands:

```sh
OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 \
PYTHONPYCACHEPREFIX=/tmp/codex-pycache python3 -W ignore \
AUDIT_R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD_V001/independent_mps_response.py \
  --length 10 --coarse-steps 8 --fine-steps 16 --max-bond 256 --cutoff 1e-11

OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 \
PYTHONPYCACHEPREFIX=/tmp/codex-pycache python3 -W ignore \
AUDIT_R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD_V001/independent_mps_response.py \
  --length 12 --coarse-steps 8 --fine-steps 16 --max-bond 256 --cutoff 1e-11
```

## Ledgers, bins, and compilation

For every target row L6--L12, the hostile verifier reconstructs the incidence
matrix, checks its owner-once columns, and recomputes the baseline, perturbed,
and differential ledgers from every saved site and edge value. It reconstructs
the breadth-first finite support-graph distances and recomputes every radial
bin: identity, edge census, signed sum, L1 sum, mean absolute value, and
maximum absolute value. It also recomputes every response summary and every
row of the global compiled result. The pinned target compiler replays at
`23/23`.

The exact target differential remainder L1 values are approximately
`1.64e-12`, `1.62e-12`, `1.66e-12`, and `2.64e-11` for L6, L8, L10, and L12.
They remain raw unassigned numerical ledger terms.

The target's statements about concentration, oscillatory signed edges, and
the decreasing farthest finite-graph shell are accepted only as empirical
descriptions of the four available finite rows. They are not promoted to a
locality law, scaling law, physical radius, or physical boundary behavior.

## L14 pre-allocation rejection

The hostile audit independently obtains full dimension `268435456`, marked
orbit dimension `134250496`, 42 owner-once edges, 22 signed edge orbits, and
transition upper count `5638520832`.

Before including even the small thread-dependent current-reduction buffer,
the fixed-width arrays require a conservative dominant payload of
`101895864328` bytes. This already exceeds the 40 GiB guard
(`42949672960` bytes). The target total is `101895903752` bytes
(`94.89795542508364` GiB). The rejection is therefore insensitive to the
thread-count detail.

No L14 response was allocated or inferred. The compiled `response_row` is
null. A different independently validated representation would be required.

## Claim ledger

- Proved: source-parent audit custody; owner-once incidence telescoping;
  order-two stabilizer; Burnside dimensions; signed edge ownership; normalized
  raw-hop attachment at exhaustive L6; L14 pre-allocation rejection.
- Adopted: `F3-MDC alpha = r0`; canonical local source label.
- Conditional: finite support, kappa, content, routing, read, and the declared
  numerical representations.
- Empirical: exact L6/L8 full-space parity; refined target L10/L12 rows;
  approximate independent L10/L12 complete-vector corroboration.
- Open: exact independent L10/L12 parity; an L14 response under a different
  validated representation; physical distance and boundary semantics;
  locality or scaling law; Gate A-P.

No complete L6--L14 numerical ladder, L14 response, continuum behavior, Ward
identity, phase, graviton, or gravity result is claimed.
