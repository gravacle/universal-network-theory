# L6/L8 localized-write response run observations

Environment: the declared 48 GiB Darwin/arm64 host with Python 3.9.6.

- L6 canonical-result creation run: `24.111255334 s`, `28,655,616` bytes
  maximum RSS. The optimized current-contraction replay passed the same
  canonical result within tolerance in `22.340707750 s`, with `28,819,456`
  bytes maximum RSS.
- L8 canonical optimized run: `451.841224708 s`, `88,162,304` bytes maximum
  RSS.
- A prior allocation-heavy L8 implementation also passed `24/24` in
  `492.273888208 s`, with `85,032,960` bytes maximum RSS, before the optimized
  replay was selected as canonical.

The first L6 attempt failed closed before result emission because Python 3.9
lacks `int.bit_count()`. The already audited repository-compatible
`bin(word).count("1")` implementation replaced it. No value from that failed
attempt is promoted.

These are single-environment observations, not runtime or memory-complexity
laws.
