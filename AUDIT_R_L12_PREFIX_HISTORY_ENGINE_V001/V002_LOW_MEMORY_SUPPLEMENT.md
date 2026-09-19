# V002 recurrence-replay memory supplement

## Frozen defect and bounded repair

V001 correctly batches lineage rows, but its Chebyshev action retains all 97
degree vectors. At L12 a single carrier row therefore exceeds the adopted
`1,400,000,000 B` numerical-workspace cap beginning at `q=9`:

```text
q     carrier columns       V001 degree-96 basis bytes
9       1,307,504                 2,029,246,208
10      1,961,256                 3,043,869,312
11      2,496,144                 3,874,015,488
12      2,704,156                 4,196,850,112
```

V002 changes only the numerical workspace. It selects the same frozen
Chebyshev degree by an endpoint recurrence with rolling vectors, then replays
that recurrence for Gauss--Legendre nodes in groups of at most 12. A
conservative allocation certificate charges 20 full vectors per row batch:
the input, output, endpoint accumulators/checkpoint, recurrence temporaries,
up to 12 quadrature accumulators, and guard slack. Batch size is chosen before
allocation and the process hard-fails if even one row would exceed the
`1,400,000,000 B` bound. The L12 one-row certificates for `q=9..12` are
`418,401,280`, `627,601,920`, `798,766,080`, and `865,329,920 B`.

The recurrence-replay path is used for every V002 transport control and is
therefore forced on the terminal `q=9` and `q=10` blocks of any later L10 run.
The rough/sharp degrees, tolerances, quadrature orders, Hamiltonian, current
orientation, owner-once admissions, ledgers, sector rule, reversed ordering,
and terminal child streaming are unchanged.

## Terminal support census

The retained preterminal state and the bit-zero admission child each have

```text
dim(H_11) = C(35,11) = 417,225,900 entries.
```

The bit-one child's nonzero admission input has

```text
sum_q C(11,q) C(23,q) = C(34,11) = 286,097,760 entries.
```

Transport workspaces use one bounded lineage-row window and a complete
carrier block for that row. Neither child is assembled globally and no
`D_12=1,251,677,700` amplitude array is allocated. The bit-one post-transport
logical carrier space can be larger than its admission support; this is why
the memory certificate is imposed per transported row rather than inferred
from the nonzero admission census.

## Locks and claim boundary

V002 preserves the V001 control outputs. Its L4/L6/L8 outputs use distinct
filenames and must be frozen before comparison. L10 requires a future
hash-pinned `CONTROL_GATE_V002.json`; L12 additionally requires a future
`SEALED_L10_GATE_V002.json` and the adopted scratch gate. Missing or failed
gates stop before state allocation. This supplement makes no L10 or L12
history, spectrum, scaling, criticality, continuum, emergence, or gravity
claim.
