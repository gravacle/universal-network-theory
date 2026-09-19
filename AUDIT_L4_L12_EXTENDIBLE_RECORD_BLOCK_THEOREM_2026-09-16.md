# Hostile audit of the L4--L12 extendible record-block theorem

Date: 2026-09-16

Disposition: `PASS`

## Scope

This is an independent, read-only audit of
[`L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md),
audited at SHA-256
`2439e1c36a053fccd57155a858d666f9ecbe0e46ded0a79f3ec3b86cb473f5cc`.
It checks the finite structural theorem, authenticated masses, and stated claim
ceiling. It does not audit the separately applied `ARGER-GATE-1` classification or
the conditional thermodynamic dynamical-`z=1` theorem.

The authenticated manifest was read at SHA-256
`292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a`.
Every Target and Blind history named by that manifest matched its recorded
digest before use. The accumulation protocol also matched the manifest-bound
digest `d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95`.

## Independent structural recomputation

The `A009--A016` intervals are contiguous and have union
`[7/48,13/48)`. Reapplying the manifest's exact midpoint map gives the rank
sets below. Basis dimensions were recomputed as
`binomial(L,q) binomial(2L,q)`. Eligibility histograms were recomputed
combinatorially, independently of the theorem text.

| L | selected ranks | basis dimensions in rank order | minimum eligible sites | terminal dark states |
|---:|:---|:---|:---|---:|
| 4 | `1,2` | `32,168` | `2,0` | `6` |
| 6 | `2,3` | `990,4400` | `2,0` | `20` |
| 8 | `2,3,4` | `3360,31360,127400` | `4,2,0` | `70` |
| 10 | `3,4,5` | `136800,1017450,3907008` | `4,2,0` | `252` |
| 12 | `4,5,6` | `5259870,33663168,124366704` | `4,2,0` | `924` |

For a basis pair `(S,C)`, the audit independently obtains

```text
|E_L(S,C)| = L - |S union (C intersect A_L)| >= L - 2q.
```

For every selected rank below `L/2`, this is strictly positive. At the upper
rank `q=L/2`, the all-dark states are exactly
`C=A_L minus S`, giving `binomial(L,L/2) = 6,20,70,252,924` states. As an
additional check, the complete L12 q5 eligibility histogram is

```text
eligible sites  count
2                  16,632
3                 471,240
4               3,769,920
5              11,309,760
6              13,194,720
7               4,900,896
```

It sums to `33,663,168`, the independently recomputed q5 basis dimension.

## Mass recomputation and branch agreement

The audit recomputed `pbar` directly from each hash-verified raw history by
averaging `sector_weights` from event `ceil(L/2)` through event `L`, then
deduplicating the selected q ranks. Decimal parsing was used so the comparison
did not depend on binary summation order.

| L | Target recomputation | Blind recomputation | absolute difference |
|---:|---:|---:|---:|
| 4 | `0.7260206189754993433` | `0.7260206189754996200` | `2.77e-16` |
| 6 | `0.5846615608350368350` | `0.5846615608350343450` | `2.49e-15` |
| 8 | `0.7373965730354165900` | `0.7373965730354126430` | `3.95e-15` |
| 10 | `0.6500987927669427322` | `0.6500987927669437047` | `9.73e-16` |
| 12 | `0.5695649839332783763` | `0.5695649839332793110` | `9.35e-16` |

All five independently recomputed Target and Blind masses are strictly greater
than `0.50`. Summing the manifest's stored `pbar_q` decimal values reproduces
the theorem's displayed values to its stated precision; the sub-`4e-15`
Target/Blind differences are consistent with the authenticated numerical
custody.

## Implementation and ancestry inspection

The audit inspected the cited seed, streamed, q-sharded, and cache-backed
implementations. The seed representation maps the complement of its loaded
low word to `S`; the streamed representation stores fixed-weight `S` rows and
`C` columns explicitly; and the q-sharded representation stores exact
`binomial(prefix,q) x binomial(2L,q)` blocks. In each case, accepted admission
sets the same fresh event bit in `S` and `C` through injective maps.

The authenticated L10 V002 wrapper changes only the Krylov memory batch and
binds the inspected streamed base implementation. The L12 cache builder and
consumer independently assert injective destination maps and exact add-event
identities. Every authenticated history row has
`reverse_support_probability = 0.0`. Therefore the theorem's actual-ancestry
statement is valid: a realized rank-q lineage contains exactly q accepted
fresh events and has executed ancestors at every lower rank.

The audit also confirms the theorem's deliberate distinction between executed
ancestry and non-darkness to the complete family of frozen admissible actions.
It does not reinterpret a rejected past site as a future event in the declared
one-pass chronology.

## Disposition and claim ceiling

`PASS`: the rank sets, dimensions, eligibility bounds, terminal dark-state
counts, ancestry scope, and authenticated majority masses are correct.

The result proves bounded extendible membership separately at the five frozen
sizes. It does **not** prove that every history completed the upper transition,
that distinct lineage rows are one common realized lineage, or that the five
finite systems share an inter-size state embedding. It supplies the exact
membership and majority-mass premises used by `ARGER-GATE-1`; finite visibility
and the conditional thermodynamic dynamical-`z=1` theorem are separately
authenticated.
