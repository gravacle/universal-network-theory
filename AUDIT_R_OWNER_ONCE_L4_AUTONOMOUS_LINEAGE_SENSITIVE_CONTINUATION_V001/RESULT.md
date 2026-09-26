# Independent result: L4 lineage-sensitive continuation

## Disposition

```text
PASS_INDEPENDENT_L4_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION
```

An independently written route reproduces the frozen target classification

```text
RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION
```

for the single prospectively frozen L4 continuation.

## Reproduced effect

| quantity | independent value |
|---|---:|
| post-transport carrier trace distance `Delta_C` | `0.14761185701903007` |
| numerical scale `tau` | `1e-10` |
| `T_dyn = Delta_C/tau` | `1476118570.1903007` |
| post-transport occupation-profile RMS | `0.006009875541368592` |
| maximum target/independent registered-observable difference | `1.1102230246251565e-16` |
| independent coarse/fine maximum | `1.2490009027033011e-15` |
| maximum independent control residual | `4.6629367034256575e-15` |

The actual and same-sector product arms begin with equal full carrier
marginals to `6.94e-18`, equal full lineage marginals to `1.39e-17`, and equal
sharp-sector weights to `1.11e-16`.  The subsequent carrier-state difference
therefore is not inherited from a pre-existing carrier-marginal difference.

The trace distance is unchanged by the common carrier-only transport to
`1.11e-16`, as it must be.  That invariance is a control, not a second piece of
evidence.  In contrast, the fixed occupation profile is transport-sensitive:
its RMS difference is at roundoff immediately after admission and is
`0.006009875541368592` after transport.

## Warning adjudication

The frozen target execution emitted Apple/Accelerate divide, overflow, and
invalid warnings on dense matrix-multiplication calls.  Those warnings were
not accepted on faith and were not suppressed as a substitute for validation.

The independent implementation:

- imports neither the target continuation nor the historical parent;
- reconstructs the 495-state basis and the 128-substep checkpoint, reproducing
  their frozen SHA-256 fingerprints exactly;
- uses explicit `numpy.einsum(..., optimize=False)` contractions and contains
  no Python matrix-multiplication operator, `dot`, `matmul`, or Kronecker
  helper;
- configures divide, overflow, and invalid floating-point events to raise;
- captures every runtime warning and fails if any warning is present;
- rejects every nonfinite scalar or array recursively; and
- independently recomputes the input comparator, revisit pulse, autonomous
  transport, partial traces, trace norm, occupation profile, and all controls.

This route produced zero warnings and no floating-point exception.  Every
stored value is finite, density minima are only roundoff-negative
(`>= -1.57e-16`), and the full registered target output agrees within
`1.12e-16`.  The original warning stream is therefore not being used as a
premise for acceptance: the numerical result survives a separate contraction
path that bypasses it.

## Exact interpretation and ceiling

For this exact L4 terminal checkpoint, symmetric sharp-sector dephasing,
same-sector quantum-product comparator, event-zero revisit, and common
transport, retained joint lineage--carrier association changes the subsequent
carrier state in a way the separate marginals do not determine.

This establishes a finite L4 mechanism only.  It establishes neither
finite-size persistence nor scaling.  It does not define or prove record
curvature, geometry, RGRL/WTC response, a continuum, alpha selection, metric
dynamics, or gravity.
