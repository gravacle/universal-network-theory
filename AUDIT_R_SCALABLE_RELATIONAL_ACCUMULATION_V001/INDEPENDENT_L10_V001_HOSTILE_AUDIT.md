# Independent hostile L10 V001 audit

The frozen adjudicator at method commit
`9f81115b251f207e4f54a09b489f705202d2377b` replays deterministically as:

```text
FAIL_CLOSED_L10_STREAMED_HISTORY
checks 28/30
```

The two failed checks are `target internally resolved` and `target RSS guard`.
The former is the target's required consequence of the latter. Target RSS is
`4,439,965,696 B`, exceeding `4 GiB` by `144,998,400 B`. Every physical,
ledger, numerical-convergence, target/blind agreement, interval, wall-time,
and independent-method check passes.

The hostile audit independently reproduced maximum target/blind observable
and sector differences `1.509903313490213e-14` and
`2.7478019859472624e-15`, and confirmed the provisional `[0,0.375]` common
L4--L10 density support. These data are retained as an empirical failed-run
record, not promoted as a passing L10 gate.

The `L12_execution_authorized` Boolean in the hostile JSON reports the later
scratch-only condition. It is not the complete protocol authorization. Since
L10 failed, L12 remains prohibited even though scratch space recovered above
`60 GiB` after the parallel processes exited.

Result hashes:

```text
target L10  6df84bf01cd743a682dea646a727698e25ea1da48590a1df66224b03bc10421c
blind L10   7dcaf32ed06a37e976dad88fd5d6d8dae5afcc3df88d573b70af486954ef3e29
hostile     774b3d554b7cf66b0efdd2e5dbcfbb51712b4a38f029d3f2bf45fe544401224e
```

Hostile disposition: preserve V001 as fail-closed; promote no L10/L12 or
scale-free/continuum/gravity claim from it.
