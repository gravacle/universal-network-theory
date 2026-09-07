# Exact prefix-lineage theorem

Let the full fixed-content basis be labelled by pairs `(S,C)` with
`S subset {0,...,L-1}`, `C subset {0,...,2L-1}`, and `|S|=|C|`. Here `S`
is the set of spent genesis cells and remains the canonical cryptographic
lineage record.

## Theorem PLB-1 — owner-once prefix support

After the first `n` fresh admissions of the frozen one-pass history,

```text
S subset {0,...,n-1}.
```

### Proof

The initial state has `S=empty`. Transport acts only on `C`, hence cannot
change `S`. At event `n`, the admission generator has support only between
`(S,C)` and `(S union {n}, C union {n})` when `n` is absent from both. It can
change no other lineage bit. Induction proves the claim. The bit `n` is never
addressed again in the declared one-pass history, so the result is also the
owner-once custody statement. QED.

## Theorem PLB-2 — exact block and dimension

Define `H_n` and `E_n` as in `PROTOCOL.md`. `E_n` is injective and its range is
exactly the support permitted by PLB-1. Moreover

```text
dim H_n = sum_q C(n,q) C(2L,q)
        = C(2L+n,n).
```

The first statement follows because zero-padding is reversible on its range.
The second is Vandermonde's identity after replacing `C(2L,q)` by
`C(2L,2L-q)`. No orbit representatives or equivalence classes occur. QED.

## Theorem PLB-3 — operator intertwining

The frozen transport generator satisfies

```text
H_T E_n = E_n H_T^(n)
```

because it changes only `C`. The fresh admission satisfies

```text
U_A(n) E_n = E_(n+1) A_n^(prefix)
```

by the two explicit occupied/blank cases in the protocol. Thus replacing the
full array by the prefix block before the terminal event changes neither the
state nor any derived ledger value. QED.

## Theorem PLB-4 — terminal streamed reconstruction

At event `L-1`, the two admission images have different values of the last
lineage bit and are orthogonal. Every frozen transport or registered
observable is `I_lineage tensor O_carrier`. Consequently its quadratic form
on the direct sum is the sum of the two child quadratic forms; every oriented
current, occupation, sector weight, norm, and owner ledger reconstructs by
addition.

For a requested final lineage mask, the last bit uniquely selects a child;
clearing it yields the unique preterminal row. Applying the frozen carrier
transport to that row reconstructs every requested terminal amplitude. This
is an inverse recipe, not a trace over lineage. QED.

## Corollary PLB-5 — L12 bound

For `L=12`, the largest state that must be materialized for continuation is

```text
dim H_11 = C(35,11) = 417,225,900 = C(36,12)/3.
```

The largest simultaneous adjacent pair before the terminal streamed event is
`dim H_10 + dim H_11 = 548,354,040`, or `8,773,664,640` complex128 bytes.
This reduction is exact but finite; it is not a polynomial asymptotic
representation and makes no continuum or gravity statement.
