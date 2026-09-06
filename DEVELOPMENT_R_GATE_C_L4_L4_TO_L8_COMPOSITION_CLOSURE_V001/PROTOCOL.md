# Frozen protocol: L4 + L4 to L8 composition-closure screen V001

## Scope and stop rule

This packet asks only for the minimum authenticated coherent boundary record
needed to reconstruct the conditional uniform-source L8 connected component
from an explicit L4-plus-L4 owner composition. It does not run L6 or L12,
derive a continuum map, or search for gravity.

If the exact interface dimension saturates the full half-component Hilbert
dimension and therefore grows exponentially between the L4 and L8 validation
cuts, the packet must stop after recording and hostile-auditing that
obstruction. It may not introduce a truncation, tensor-network ansatz, or
additional machinery to force closure.

## Conditional physical parent

Use the already audited connected-cycle record parent:

- two length-`L` cycles with owner-once internal edges;
- shifted connectors `(0,i)--(1,i+1 mod L)`;
- uniform F3-MDC preparation, blank on every even site label and
  `(B+x)/sqrt(2)` on every odd site label;
- source-off simultaneous `H=-sum_e T_e` evolution at `kappa=pi/2`;
- complete failure-inclusive product read.

The connected support, source routing, `kappa`, and separate hopping/clock
calibration retain their existing conditional status. The F3-MDC
`alpha=r0` attachment remains adopted, not bare-F3-derived.

## Exact owner composition

Label the canonical L8 component by Rail 1 sites `0..7` and Rail 2 sites
`8..15`. Define blocks

```text
A = {0,1,2,3,8,9,10,11}
B = {4,5,6,7,12,13,14,15}.
```

Each isolated block is a relabeled periodic L4 connected component. Compose
them into the canonical L8 owner set by removing the six L4 wrap owners

```text
(3,0), (11,8), (3,8),
(7,4), (15,12), (7,12)
```

and adding the six canonical L8 owners

```text
(3,4), (7,0), (11,12),
(15,8), (3,12), (7,8).
```

The verifier must prove that this surgery changes no other owner and produces
exactly the canonical 24-edge degree-three L8 support. This interscale surgery
is an adopted conditional join for the screen; the frozen repository does not
derive it as an autonomous cross-scale physical operation.

## Closure object and minimum dimension

At the declared final time, reorder the complete L8 pure-state amplitudes as
a coefficient matrix

```text
M_L[left block word, right block word].
```

For L8, both block word spaces have dimension `2^8=256`. The exact coherent
interface dimension is

```text
D_L = rank(M_L),
```

equivalently the Schmidt rank across `A|B` or the rank of either block reduced
density operator. By the Schmidt decomposition theorem, `D_L` is the minimum
linear boundary-channel dimension capable of exact coherent state
reconstruction across this cut. Reconstruction with fewer than `D_L`
channels is impossible; the singular-value tail supplies the optimal
rank-truncation error.

Apply the identical construction to the L4 component split into two
length-two axial blocks. Each half then has four sites and dimension 16. Report

```text
D_4, D_8, D_8/D_4,
D_L / 2^L,
smallest retained singular value,
coarse/fine and independent-solver rank stability,
optimal tail error for every D < D_L or sufficient decisive checkpoints.
```

`D` is the interface/bond dimension, not the number of real parameters in a
chosen serialization. Also report the full boundary-state and full-state
dimensions so those notions cannot be conflated.

## Lower-order boundary-record attack

Separately screen the tempting equal-time record consisting of total retained
`Q`, the complete four-port reduced density matrix, incident owner currents,
and all port-port connected occupation correlations. It is sufficient for
instantaneous port-local expectations but is not presumed sufficient for
future joined evolution.

The adversarial screen must either:

1. produce two lawful finite-block density operators with the same proposed
   equal-time boundary record but a different future joined output under the
   declared owner action; or
2. prove the record closes for the declared complete coherent output.

Lawful adversarial density operators may be constructed as positive trace-one
states within the complete finite block algebra used by the physical parent.
They are closure counterexamples, not claims that the uniform F3-MDC source
selects those roots.

## Pass, obstruction, and claim rules

The target passes only if it verifies owner surgery, source factorization,
complete L8 reconstruction at `D_8`, rank minimality, numerical controls, and
the lower-order closure verdict. Independent hostile work must rebuild the
owner surgery and use a propagation/rank method materially distinct from the
target.

- **Bounded closure:** exact `D_L` remains demonstrably submaximal with
  non-exponential L4-to-L8 scaling. Stop and report the dimension before any
  L6-to-L12 work.
- **Exponential obstruction:** `D_4` and `D_8` saturate their respective
  half-Hilbert dimensions (`16` and `256`), or an equivalent exact lower bound
  forces the complete coherent record. Stop, preserve the worktree, and report
  the obstruction for theory-level review.
- **Unresolved:** numerical rank cannot be separated from solver error or the
  independent reconstruction disagrees. Fail closed and stop.

Exact topology, Schmidt minimality, and algebraic identities are proved.
Finite evolved singular values and numerical ranks remain numerical unless an
exact certificate is supplied. No continuum, Ward identity, metric, graviton,
macroscopic emergence, or gravity claim follows.
