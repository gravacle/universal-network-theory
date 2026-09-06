# Independent hostile audit report

## Disposition

**PASS, 67/67.** No material custody, topology, path, numerical, conservation,
periodic-comparison, trend, or claim-boundary discrepancy was found. No L
greater than 8 was run.

Target and immutable antecedent hashes are pinned in
`INDEPENDENT_RESULT.json`. The audit uses a unitary fourth-order
Suzuki--Yoshida edge factorization; the target uses an order-ten Taylor
polynomial. Both 1,024-step and 2,048-step audit evolutions are independent
runs.

Audit runtime was `9.452289250 s`; maximum RSS was `31,506,432 bytes` on the
recorded 48 GB environment. A separate target replay passed `21/21` in
`16.483160666 s` with `33,062,912 bytes` maximum RSS.

## Exact topology and paths

The reconstructed periodic support has 24 owner edges. Removing exactly

```text
(7, 0, rail_1)
(15, 8, rail_2)
```

leaves 22 owner-once edges, including all eight connectors. No other owner is
changed. Degrees are two at nodes `0,7,8,15` and three at the other twelve
nodes.

The unique shortest probe-to-target path is

```text
0 -> 1 -> 2 -> 3 -> 4
```

of length four. Blocking nodes `1,2,3` still leaves exactly two shortest
length-six bypasses:

```text
0 -> 9 -> 8  -> 7  -> 6  -> 5  -> 4
0 -> 9 -> 10 -> 11 -> 12 -> 13 -> 4
```

Thus this is an exact rail-wrap removal control, not a unique-route ladder.

## Writes, conservation, and complete currents

All eight authenticated terms-off write ledgers are exact:

```text
Delta Q = k/2,  edge flux = 0,  total W_R = k/2,
Delta Q + edge flux - total W_R = 0.
```

The complete eight-history transport-ledger L1 remainder is at most
`1.363e-10`; the four probe-difference ledgers are at most `7.229e-11`.
Capacity/search norm errors are `3.660e-13` and `1.597e-12`; retained-number
errors are below `3.805e-12`. Capacity/search energy drift is `1.237e-11` and
`1.571e-11`.

Every stored current component was checked. The maximum discrepancy is
`5.628e-12` across all 32 connector components and `8.256e-12` across all 88
complete marginal-current components. Signed connector sums, marginal L1
values, and both unsubtracted connector throughputs also agree. Maximum
complete-current coarse/fine separation is `2.345e-10`.

## Open-support arrival and periodic comparison

| N | independent `tau_open` | peak `delta q4` | connector L1 | sealed periodic tau | open minus periodic |
|---:|---:|---:|---:|---:|---:|
| 0 | `1.1974061136070784` | `0.00024629732373514837` | `0.5339977312830155` | `1.222689868854405` | `-0.025283755247326622` |
| 1 | `2.9482687345235066` | `0.11666068263297018` | `0.4087555596072887` | `1.3455677498194254` | `1.6027009847040812` |
| 2 | `3.040639390594083` | `0.10676888200320925` | `0.31286880342458007` | `2.971600967337824` | `0.06903842325625886` |
| 3 | `3.096778890253325` | `0.1057672031079738` | `0.278339239076679` | `2.86146468598496` | `0.2353142042683647` |

Maximum target error is `1.206e-10` for `tau_open` and `7.247e-12` for peak
amplitude. Maximum coarse/fine separation is `1.902e-5` for time and
`4.404e-9` for amplitude.

`tau_open` is strictly increasing. In particular,

```text
tau_open(3) - tau_open(2) = 0.05613949965924192 > 0.
```

The periodic `N=3 < N=2` inversion therefore disappears under the declared
two-edge removal. The connector L1 values also decrease strictly over
`N=0..3`.

## Hostile classification boundary

Because the periodic and open packets differ by exactly the two rail-wrap
owners, the result supports the predeclared finite classification
“ring-mediated in this periodic-versus-open comparison.” It does not establish
a general microscopic mechanism, a unique route, or a claim about other
boundary cuts. The two longer connector/second-rail bypasses remain active.

Background subtraction is an ensemble contrast, not an individual carrier
tag. The finite graph peak time is not a physical metric or clock and cannot
be promoted to time dilation or Shapiro delay. No macroscopic emergence or
gravity follows.

**Proved:** exact two-owner removal, open-support/path census, authenticated
write ledgers, and owner-once continuity identities.

**Adopted:** literal Option-B removal, common phase, subtraction, finite
windows, and first-positive-peak rule.

**Conditional:** all-blank parent, finite solver, and ensemble difference.

**Empirical:** the four open arrival/current rows and the declared finite
periodic/open comparison.

**Open:** other boundary cuts, connector patterns, phases, windows, individual
lineage, a physical metric/clock, macroscopic emergence, Gate R-C, and Gate
A-P.

## Discrepancies

None material. The independent split method has larger raw energy drift than
the target Taylor calculation, but solver agreement, coarse/fine stability,
and all owner-once ledger remainders are comfortably inside the hostile
thresholds.
