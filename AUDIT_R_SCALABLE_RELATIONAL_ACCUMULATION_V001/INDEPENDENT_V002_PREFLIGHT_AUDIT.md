# Independent hostile V002 pre-output audit

```text
PASS_FREEZE_L10_V002_MEMORY_REPAIR
18/18
```

The hostile replay verified the final preflight byte-for-byte before any L10
V002 output. The scientific execution change is only the target's maximum
retained Krylov basis per row batch, from `1,400,000,000` to
`1,000,000,000` bytes. The complete basis, operators, history, tolerances,
quadrature, wall limit, and RSS limit are unchanged.

The final L8 freeze validation contains exactly events `1..8`, has exact
dimension `735,471`, resolves internally, and is bit-identical to the V001
streamed target on every common numerical row field. The wrapper was also
tested to reject an existing output before compute.

The frozen adjudicator requires complete ordered ten-event target and blind
histories, exact `D_10=binomial(30,10)`, frozen and embedded wrapper/base/
protocol custody, target/blind agreement, strict owner-once conservation and
norm gates, and the unchanged `4 GiB`/`7,200 s` limits. L12 requires both a
passing L10 gate and `60 GiB` free scratch.

Frozen hashes:

```text
wrapper       3cbc6c68d06e24eb6a7293649fa393af9b89dc8776868e29340f0b31a3422647
adjudicator   a6fa9567b4097f37d41ed619e2ebc97778d49ebf3e468a2181d2fa6416a1e271
L8 validation 900c94a92f07871dbb4ca6eadba7da2354076aa6f9cd30882d8a22637e9eb7e8
preflight     80cbca1ca30db000bed08be31fe4adf48a3c4f1c973fe80b0b9902ab6e64d46a
```

This authorizes one non-overwriting L10 V002 target run. Failure authorizes no
additional tuning in this packet and promotes no L10/L12, scaling, continuum,
emergence, or gravity claim.
