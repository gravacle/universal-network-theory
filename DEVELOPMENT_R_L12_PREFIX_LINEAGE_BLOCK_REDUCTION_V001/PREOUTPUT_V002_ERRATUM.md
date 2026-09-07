# Pre-output V002 compatibility erratum

The frozen V001 target invocation stopped before creating
`PREFLIGHT_RESULT.json`: the host is Python 3.9.6, which does not provide
`int.bit_count()`.

V002 replaces only

```text
word.bit_count()
```

with

```text
bin(word).count("1")
```

in the target verifier. The represented basis, lineage encoding, transitions,
resource counts, thresholds, checks, hostile implementation, and claim
boundary are unchanged. A new manifest is frozen before a second invocation.
