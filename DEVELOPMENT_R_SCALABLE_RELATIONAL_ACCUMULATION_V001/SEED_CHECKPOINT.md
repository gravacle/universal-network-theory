# Scalable Relational Accumulation seed checkpoint

## Disposition

```text
PASS_RELATIONAL_ACCUMULATION_SEED_L4_L8
NEXT: FREEZE_L10_L12_HISTORY_METHODS
```

Target and independently reversed-layout histories resolve at L4, L6, and L8.
The frozen comparison passes `205/205`; the maximum target/blind disagreement
is `8.846256505101735e-10`.

| L | exact dimension | final retained density | maximum blocked probability | minimum `W_n` | 99% late-history `q` interval | density envelope |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | `495` | `0.241698698965` | `0.104425958986` | `0.447787020507` | `[0,4]` | `[0,0.5625]` |
| 6 | `18,564` | `0.222520331120` | `0.177888839743` | `0.411055580129` | `[0,5]` | `[0,0.458333333333]` |
| 8 | `735,471` | `0.228575893727` | `0.171812051415` | `0.414093974293` | `[0,6]` | `[0,0.40625]` |

Every admission remains nonnegative, every fresh cell has zero reverse support
before first use, and all content, bandwidth, lineage, transport, norm, and
number guards pass. L4 reproduces the sealed intrinsic-admission trace within
`1.333e-15` on `W_n`.

The common finite density support is

```text
I_4 intersect I_6 intersect I_8 = [0,0.40625].
```

This broad support includes vacuum-adjacent sectors and is not a criticality
claim. Every positive-width density atom must still be screened; no favorable
density may be chosen.

## Runtime telemetry

| L | target wall | target peak RSS | blind wall | blind peak RSS |
|---:|---:|---:|---:|---:|
| 4 | `0.598 s` | `26,132,480 B` | `1.013 s` | `25,690,112 B` |
| 6 | `19.141 s` | `37,388,288 B` | `32.556 s` | `38,600,704 B` |
| 8 | `1503.396 s` | `380,289,024 B` | `2516.975 s` | `404,520,960 B` |

The L8 measurement rules out naïvely enlarging the global action-list
quadrature. Before L10 output, the target and blind streamed-block propagation
methods, benchmark projection, storage layout, and resource abort must be
separately hash-frozen. L12 remains conditional on the L4--L10 interval and
the frozen six-hour exact-history cap.

**Empirical/numerically certified after hostile pass:** the table, exact finite
histories, and common candidate support. **Adopted:** the late half-cursor
window and 99% interval rule. **Open:** L10/L12 histories, final common support,
every spectral atom, `z=1`, criticality, continuum behavior, emergence, and
gravity.
