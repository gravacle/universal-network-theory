# Independent hostile L10 V002 audit

The frozen V002 adjudicator independently replays:

```text
PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_RESOURCE_BLOCKED
checks 42/42
```

It verifies the target result SHA-256
`928498a703457fd4c268ffa95bedf3704d6467add5082bd9fc7a5f6e4e327af5`,
the blind result SHA-256
`7dcaf32ed06a37e976dad88fd5d6d8dae5afcc3df88d573b70af486954ef3e29`,
and all six pre-output wrapper/base/protocol/adjudicator/validation custody
hashes.

Independent replay reproduces:

- target/blind observable difference `1.5987211554602254e-14`;
- sector-weight difference `2.858824288409778e-15`;
- maximum admission residual `2.220446049250313e-14`;
- maximum transport-number drift `1.2434497875801753e-14`;
- maximum node-continuity L1 residual `7.261552470438914e-15`;
- maximum norm error `3.3306690738754696e-15`;
- minimum write `0.4046861994111275`; and
- maximum blocked probability `0.19062760117771718`.

The target wall and RSS are `2,045.204301958 s` and `4,209,213,440 B`,
leaving `85,753,856 B` below the frozen memory ceiling. The late-history
sector is `q in [0,7]`; the finite L4--L10 common density support is
`[0,0.375]`.

The hostile audit also confirms the conjunctive L12 gate is false: the stored
scratch reading `63,078,301,696 B` is `1,346,207,744 B` below `60 GiB`.
Transient scratch fluctuation cannot substitute for a separately frozen L12
method gate. No L12 or spectral output exists.

The pass promotes only the finite L4--L10 relational history. L12, interval
spectra, `z=1`, criticality, continuum behavior, emergence, and gravity remain
open.
