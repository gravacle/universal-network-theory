# L4--L12 extendible record-envelope theorem

Date: 2026-09-16

Status: `EXACT_STRUCTURAL_THEOREM_PROVED__BOUNDED_UPPER_ENDPOINT`

## 1. Scope

This note generalizes the structural part of the L12 extendible-record theorem
to the fixed Stage-5 density envelope `A009--A016` at every authenticated size

```text
L in {4,6,8,10,12}.
```

It proves that every realized probability component in the envelope's selected
charge sectors has its rank-resolved role in a bounded record block: lower
endpoint, bridge where present, or completed upper endpoint. It also proves
that the upper endpoint is sharp: the full upper sector contains basis states
dark to every further admission, so it cannot be promoted to another bridge.

This is a theorem about the frozen basis, owner-once history, and admission
operators. It proves the exact bounded-membership and majority-mass inputs to
the adopted finite ARGER Gate. The separately authenticated finite probe
visibility supplies the Gate's remaining evidentiary input.

## 2. One basis and admission law in all three implementations

For a fixed even `L`, put

```text
A_L     = {0,...,L-1},
Omega_L = {0,...,2L-1}.
```

The fixed-content sector of carrier charge `q` has the canonical basis

```text
|S,C>,  S subset A_L, C subset Omega_L, |S|=|C|=q,
```

where `S` records the spent active cells and `C` records occupied carrier
sites. Its dimension is

```text
dim H_(L,q) = binomial(L,q) binomial(2L,q).
```

This is the basis declared by the
[`Scalable Relational Accumulation` protocol](DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md#L70-L94)
and by the
[`Exact prefix-lineage theorem`](DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md#L1-L37).
The three frozen representations implement it as follows.

1. **L4, L6, L8.** The seed engine enumerates the weight-`L` words on `3L`
   bits. Its low `L` bits are the still-loaded cells and its high `2L` bits are
   the carrier word. Taking `S` to be the complement of the loaded low bits
   turns the fixed-weight identity into `|S|=|C|`. The source test and two-bit
   toggle remove the loaded bit and add the co-located carrier bit; see
   [`compute_seed_history.py`](DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py#L55-L106).
2. **L10.** The streamed engine explicitly enumerates `fixed_words(L,q)` for
   spent rows and `fixed_words(2L,q)` for carrier columns. Its admission maps
   set the same event bit in both words; see
   [`compute_streamed_history.py`](DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py#L111-L153)
   and its
   [admission action](DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py#L213-L225).
3. **L12.** The q-sharded engine stores the exact prefix rows
   `binomial(n,q) x binomial(2L,q)`, with no lineage identification or
   truncation; see
   [`Q_SHARDED_TARGET_METHOD_V004.md`](DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md#L18-L41).
   Its cache constructs injective carrier-bit and lineage-bit insertion maps
   explicitly in
   [`build_target_cache.py`](DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py#L2563-L2595),
   and the consumer applies the same `cos(phi)` stay child and
   `-i sin(phi)` accepted child in
   [`consume_target_cache.py`](DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py#L1323-L1363).

Thus these are storage variants of one admission law. For `e in A_L`, define
the accepted insertion

```text
F_e |S,C> = |S union {e}, C union {e}>   if e not in S union C,
              0                          otherwise.
```

The frozen angle is `phi=pi/4`, so every nonzero `F_e` image occurs in the
accepted child with nonzero coefficient `-i/sqrt(2)`. For fixed `e`, `F_e` is
injective on its domain. Consequently

```text
F_e^dagger F_e = P_e,
```

where `P_e` projects onto basis states in which `e` is both unspent and
carrier-blank.

## 3. Uniform no-dark theorem below half filling

For a basis state in sector `q`, its eligible active sites are

```text
E_L(S,C) = A_L minus (S union C).
```

Only the part `C intersect A_L` matters in this union. Hence

```text
|E_L(S,C)|
  = L - |S union (C intersect A_L)|
 >= L - |S| - |C intersect A_L|
 >= L - 2q.
```

Since the sum of the `P_e` is diagonal in the canonical basis, this is the
operator inequality

```text
sum_(e in A_L) F_e^dagger F_e >= (L-2q) I_(L,q).
```

In particular, every sector with `q <= L/2-1` is non-dark to the complete
family of admissible `q -> q+1` actions, with at least two eligible active
sites on every basis vector.

The following census is a direct evaluation of
`binomial(L,q) binomial(2L,q)` and the bound above.

| L | q | role | basis pairs | minimum eligible sites |
|---:|---:|:---|---:|---:|
| 4 | 1 | lower | 32 | 2 |
| 4 | 2 | upper | 168 | 0 |
| 6 | 2 | lower | 990 | 2 |
| 6 | 3 | upper | 4,400 | 0 |
| 8 | 2 | lower | 3,360 | 4 |
| 8 | 3 | bridge | 31,360 | 2 |
| 8 | 4 | upper | 127,400 | 0 |
| 10 | 3 | lower | 136,800 | 4 |
| 10 | 4 | bridge | 1,017,450 | 2 |
| 10 | 5 | upper | 3,907,008 | 0 |
| 12 | 4 | lower | 5,259,870 | 4 |
| 12 | 5 | bridge | 33,663,168 | 2 |
| 12 | 6 | upper | 124,366,704 | 0 |

The zero at each upper endpoint is not merely failure of the lower bound.
Choose `S subset A_L` with `|S|=L/2` and take

```text
C = A_L minus S.
```

Then `|C|=L/2` and `S union C=A_L`, so every `F_e` annihilates `|S,C>`.
There are exactly `binomial(L,L/2)` such displayed dark basis states: `6`,
`20`, `70`, `252`, and `924` at the five sizes. Therefore the `q=L/2`
sector can be the completed upper endpoint of the bounded block, but no theorem
here makes the whole sector a further-extendible bridge.

## 4. Actual ancestry in the owner-once history

The initial state has `S=empty`. Native transport changes only `C`. At fresh
event `e`, admission either stays in the same lineage row or adds exactly the
new bit `e`; no later event addresses that bit again. This is PLB-1 in the
[`Exact prefix-lineage theorem`](DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md#L8-L23)
and is also explicit in the seed and streamed maps cited above.

Induction therefore gives the following pathwise statement for every nonzero
realized component: a component at rank `q` was reached through exactly `q`
accepted insertions and consequently has actual ancestors at every rank
`0,1,...,q-1`. This does not say that a past rejected site will be revisited by
the declared one-pass chronology. Actual ancestry is a statement about the
executed past; non-darkness is a statement about the complete frozen family of
admissible actions.

## 5. Exact A009--A016 rank resolution

The authenticated manifest assigns each density atom to one sharp sector by
the fixed midpoint rule implemented in
[`build_sector_manifest.py`](DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V001/build_sector_manifest.py#L679-L704).
Its explicit `q_by_L` rows for `A009--A016` give:

| atom | L4 | L6 | L8 | L10 | L12 |
|:---|:---|:---|:---|:---|:---|
| A009 | q1 lower | q2 lower | q2 lower | q3 lower | q4 lower |
| A010 | q1 lower | q2 lower | q3 bridge | q3 lower | q4 lower |
| A011 | q1 lower | q2 lower | q3 bridge | q4 bridge | q4 lower |
| A012 | q2 upper | q2 lower | q3 bridge | q4 bridge | q5 bridge |
| A013 | q2 upper | q3 upper | q3 bridge | q4 bridge | q5 bridge |
| A014 | q2 upper | q3 upper | q4 upper | q4 bridge | q5 bridge |
| A015 | q2 upper | q3 upper | q4 upper | q5 upper | q5 bridge |
| A016 | q2 upper | q3 upper | q4 upper | q5 upper | q6 upper |

Equivalently, after deduplicating repeated atom-to-sector assignments, the
selected ranks are

```text
L4:  {1,2}
L6:  {2,3}
L8:  {2,3,4}
L10: {3,4,5}
L12: {4,5,6}.
```

For each size, define the smallest selected rank as the **lower endpoint**, any
strictly intermediate selected rank as a **bridge**, and `L/2` as the
**completed upper endpoint**. Sections 3 and 4 prove, respectively:

- every lower endpoint has actual lower-rank ancestry and a nonzero admissible
  continuation on every basis component;
- every bridge has actual ancestry through the lower endpoint and a nonzero
  admissible continuation on every basis component; and
- every upper endpoint has actual ancestry through all lower selected ranks.

No continuation clause is imposed at the completed upper endpoint, and the
explicit dark states in Section 3 prove why one cannot be inferred. Subject to
that bounded endpoint definition, **every selected sector at every size
qualifies**, and every probability-support component in it has the declared
rank role.

## 6. Authenticated majority mass at every size

The same manifest stores the late-window `pbar_L(q)` values reconstructed by
the frozen rule in
[`build_sector_manifest.py`](DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V001/build_sector_manifest.py#L609-L649).
Counting each selected sharp sector once gives:

| L | selected q sectors | deduplicated stored `pbar` mass |
|---:|:---|---:|
| 4 | 1--2 | `0.7260206189754993` |
| 6 | 2--3 | `0.5846615608350367` |
| 8 | 2--4 | `0.7373965730354166` |
| 10 | 3--5 | `0.6500987927669427` |
| 12 | 4--6 | `0.5695649839332784` |

All five authenticated numerical sums exceed `0.50`. Sector deduplication is
essential because several atoms select the same `q` at a given size. The
structural membership theorem is exact; the displayed masses retain the
numerical status and custody of the frozen histories in the
[`V003R1 manifest`](DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json).

## 7. Nonclaims and exact boundary

This result proves neither that every component has already completed the
upper transition within its finite reporting window nor that distinct lineage
rows are one common realized lineage. The stricter completed-lineage quantity
remains different from bounded extendible membership.

It also supplies no inter-size state embedding. Each `L` has its own prism,
Hamiltonian, history, and reporting window. The common statement is that the
same finite combinatorial theorem applies separately to each authenticated
size and that the fixed manifest envelope selects the rank blocks displayed
above.

This theorem does not itself calculate finite probe visibility or a
thermodynamic dynamical exponent. The former is independently authenticated
for every selected sector and is combined with this theorem by
[`ARGER-GATE-1`](ARGER_GATE_ADOPTION_2026-09-16.md); the latter is a
separately typed conditional same-model result. Under the adopted Gate, this
theorem supplies the exact membership and majority premises of the finite
block `z=1` classification. It does not establish a continuum gravitational
law, a parameter-free numerical value of `G`, or a premise-free uniform
all-`L` response theorem.

## 8. Preservation statement

This note is a read-only deduction from the frozen protocol, implementations,
authenticated atom map, and stored `pbar` values. It does not modify or
supersede any history, cache, manifest, hostile audit, spectrum result, or
running resource.
