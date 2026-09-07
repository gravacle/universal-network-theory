# L12 prefix-lineage representation result

## Disposition

```text
PASS_HOSTILE_SCREEN__EXACT_L12_REPRESENTATION_ONLY__L12_HISTORY_AWAITS_BENCHMARK
```

Owner-once chronology gives an exact support reduction. After `n` admissions,
the spent-lineage mask is a subset of the first `n` event labels. The reduced
block has dimension

```text
D(L,n) = C(2L+n,n),
```

and embeds into the former full array by zero-padding future lineage bits.
The map is injective and reversible. It is not an orbit quotient.

At L12:

| quantity | exact value |
|---|---:|
| former terminal array | `1,251,677,700` amplitudes |
| largest materialized prefix | `417,225,900` amplitudes |
| maximum adjacent live prefix pair | `548,354,040` amplitudes |
| adjacent complex128 storage | `8,773,664,640 B` |
| one-resolution routed volume | `2,453,288,291` amplitudes |

The terminal event is retained as two disjoint children selected by the final
lineage bit. Transport acts identically within each lineage row, so streamed
child currents, occupations, sector weights, and norms add exactly. The saved
preterminal state plus the frozen final gate and route reconstructs any
requested final amplitude without materializing the full terminal array.

The authoritative lineage identifier remains the complete bitmask. A
domain-separated SHA-256 digest authenticates its canonical encoding and is
never used to merge or quotient rows. All `4096` L12 masks and observed
digests are distinct in the finite census.

The frozen target passes `119429/119429`; the separately written reversed-
ordering reconstruction passes `110624/110624`; the hash-pinned adjudicator
passes `40/40`. Terminal amplitude reconstruction error is zero in both
implementations. Registered-observable additivity errors are
`6.661e-16` and `1.110e-15`.

The former L12 full-array obstruction is therefore removed for this finite
history representation. The reduction remains combinatorial rather than
polynomial asymptotically.

The observed free scratch during target preflight was `65,786,908,672 B`, so
the new `20 GiB` representation gate passes. Routed-volume projections from
sealed L10 telemetry are `8,349.93 s` target and `5,800.39 s` hostile. These
are adopted planning estimates only. L12 history remains locked until a
separately frozen reduced-history engine reproduces the sealed L10 history
within its unchanged physics/numerical thresholds and measured resource
guards.

**Proved:** finite prefix support, injective lineage embedding, operator
intertwining, terminal inverse reconstruction, and integer resource census.
**Adopted:** digest domain, stream/cache sizes, new representation resource
guards, and runtime projection. **Conditional:** use in the later L12
history. **Empirical:** finite floating-point control errors. **Open:** the
reduced L10 benchmark, L12 history, common L4--L12 sector, interval spectra,
`z=1`, criticality, continuum/macroscopic closure, emergence, and gravity.
