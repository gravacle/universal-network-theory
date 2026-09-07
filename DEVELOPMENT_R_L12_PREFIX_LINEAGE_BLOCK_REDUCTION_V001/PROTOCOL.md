# L12 Prefix-Lineage Block Reduction V001

**Status:** `FROZEN_CANDIDATE__PRE_L12_HISTORY_OUTPUT`

**Sealed input:** `4fcaef02d0708a4e12a9648c0f423b8159deb267`

## 1. Scope

This packet changes only the exact representation of the authenticated
relational history frozen in
`DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md`. The prism,
genesis state, one-pass cursor, admission angle, transport Hamiltonian,
observables, tolerances, sector rule, and claim boundary do not change.

No L12 history may be generated until this representation and a separately
written hostile reconstruction both pass their frozen finite controls.

## 2. Exact prefix-support block

Index events by `n=0,...,L-1`. Immediately before event `n`, only lineage bits
`0,...,n-1` have been addressed. Let

```text
H_n = direct_sum_(q=0)^n C[Subsets({0,...,n-1},q)]
                         tensor C[Subsets({0,...,2L-1},q)].
```

The canonical embedding `E_n:H_n -> H_full` pads the lineage mask with
`L-n` zero bits and leaves the carrier word unchanged. The full bitmask, not
its hash, is the authoritative lineage identity.

The owner-once schedule gives the exact support law

```text
Psi_n belongs to range(E_n),
dim(H_n) = sum_q C(n,q) C(2L,q) = C(2L+n,n).
```

Transport has the form `I_lineage tensor T_q` and preserves every `H_n`.
Fresh event `n` maps `H_n` into `H_(n+1)` by

```text
|S,C> -> |S,C>                              if n is in C,
|S,C> -> cos(Phi)|S,C> - i sin(Phi)|S+{n},C+{n}>  if n is not in C.
```

Therefore `E_(n+1) A_n^prefix = U_A(n) E_n` and
`E_n H_T^prefix = H_T E_n`. No state, branch, lineage mask, or amplitude is
identified by this reduction.

## 3. Terminal direct-sum stream

Materialize prefix blocks only through `H_(L-1)`. At the final fresh event,
the bit-`L-1=0` and bit-`L-1=1` outputs occupy orthogonal lineage rows.
Transport never mixes those rows. The final actual route is therefore
evaluated as two streamed direct-sum children and their lineage-diagonal
registered observables are added.

The retained preterminal state, final admission descriptor, frozen transport
operator, and numerical resolution are an inverse reconstruction recipe for
every final amplitude. A query for full lineage mask `S` selects exactly one
child by its last bit and exactly one preterminal row by clearing that bit.
The final full array is not required to exist simultaneously.

The null route retains `H_(L-1)` and is streamed separately. Cross-lineage
interference is not discarded: it is absent for every registered operator
because those operators act as identity on lineage. A future operator that
mixes sealed lineage is outside this reduction and would require reopening
the physical protocol.

## 4. Canonical and cryptographic lineage

Each row retains `(L,n,full_mask)` with high future bits exactly zero. Its
custody digest is

```text
SHA256("R-PREFIX-LINEAGE-V001\0" || u16(L) || u16(n) || u64(full_mask)).
```

The digest authenticates the canonical row address; it is never used as a
mathematical quotient key. The screen must enumerate all `2^12` full lineage
masks, verify distinct canonical encodings and observed digests, and verify
that every prefix row round-trips through `E_n` and its inverse.

## 5. Matrix-free sharp-number carrier blocks

Carrier words remain separated by exact `q`. A colex combinadic address

```text
rank({c_1<...<c_q}) = sum_(j=1)^q C(c_j,j)
```

replaces Python hash-table addresses. Edge exchange toggles one occupied and
one blank endpoint and recomputes the exact combinadic address. Implementations
may cache integer source/destination pairs, but must process one `q` block at
a time and may not omit a pair.

This addressing change is a bijective reordering. It supplies no physical
symmetry, averaging, tensor truncation, or macro closure.

## 6. Frozen representation checks

The target screen must pass all of the following before L12 execution:

1. Vandermonde prefix dimensions for every `L in {4,6,8,10,12}` and every
   prefix `n`.
2. Exact `D_(L-1)=D_L/3` and the L12 census below.
3. Exhaustive canonical-mask/digest custody for all L12 lineage masks.
4. Exhaustive rank/unrank and edge-exchange checks for declared finite
   controls.
5. Exhaustive L4 and L6 embedding, admission, transport, predicate, norm,
   sector-weight, occupation, and owner-once reconstruction.
6. Exact terminal two-child reconstruction on deterministic complex controls.
7. A representation written independently with reversed combination and edge
   orders, importing no target module or arrays.
8. Exact target/hostile agreement on every integer census and discrepancy at
   most `2e-12` on normalized numerical controls.
9. Hash custody over this protocol, theorem, target implementation, hostile
   methodology, and hostile implementation.

Any failure returns `L12_PREFIX_LINEAGE_REDUCTION_REJECTED`; no threshold may
be relaxed after output.

## 7. L12 resource gate

The exact L12 counts are preregistered as

```text
D_12 full terminal                 = 1,251,677,700
D_11 largest materialized state   =   417,225,900
maximum adjacent live entries     =   548,354,040
maximum adjacent complex128 bytes = 8,773,664,640
one-resolution routed entries     = 2,453,288,291
```

Final children are limited to a `512 MiB` amplitude window. Cached carrier
exchange arrays are limited to `2 GiB`; numerical Krylov storage remains
limited to `1 GiB` target and `1.4 GiB` hostile. The future L12 execution gate
is `16 GiB` RSS, `20 GiB` free scratch, and six wall hours per method. These
are new bounds derived for the new representation, not a retroactive pass of
the old representation.

The preflight runtime estimate uses the sealed L10 V002 telemetry and the
exact routed-entry ratio only. It is an adopted planning estimate, not a
complexity theorem. A separately frozen L10 reduced-history benchmark must
pass before L12 solver output is authorized.

## 8. Claim boundary

**Proved if the screen passes:** the finite prefix-support theorem, injective
lineage embedding, exact owner-once admission/transport intertwining, and
finite representation/resource censuses. **Adopted:** canonical digest
domain, streaming windows, cache limits, and resource guards.
**Conditional:** use of the reduction for a later numerical L12 history.
**Empirical:** finite floating-point controls and future telemetry.
**Open:** the L12 history, L4--L12 common sector, interval spectra, `z=1`,
criticality, continuum/macroscopic closure, emergence, and gravity.

No external reservoir, privileged boundary, grid, graviton, Ward axiom,
continuum assumption, lineage quotient, or gravity claim is introduced.
