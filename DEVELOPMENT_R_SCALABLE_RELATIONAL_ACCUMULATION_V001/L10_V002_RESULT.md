# L10 V002 relational accumulation result

## Disposition

```text
PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_RESOURCE_BLOCKED
```

The one permitted memory-only V002 target run passes the unchanged `4 GiB`
and `7,200 s` guards. It retains the complete exact
`D_10=binomial(30,10)=30,045,015` basis and changes no physical or numerical
control from V001.

| implementation | wall time | peak RSS | disposition |
|---|---:|---:|---|
| target V002 Lanczos | `2,045.204301958 s` | `4,209,213,440 B` | pass |
| independent Chebyshev--Krylov | `1,420.728120167 s` | `3,913,236,480 B` | pass |

The target has `85,753,856 B` (`81.78125 MiB`) of headroom below `4 GiB`.
The frozen hostile adjudicator passes `42/42`. Maximum target/blind differences
are `1.5987211554602254e-14` for registered observables and
`2.858824288409778e-15` for sector weights.

The L10 one-pass history has:

```text
W = [0.500000000000, 0.500000000000, 0.476585279171,
     0.472549447801, 0.457609090701, 0.446679327326,
     0.430604845736, 0.424349201838, 0.413477137418,
     0.404686199411]
```

Blocking grows from zero to `0.190627601178`; every blocked component remains
in the admission kernel. Final retained `q` is `4.526540529402`, or density
`0.226327026470` on 20 retained sites. The descriptive routed-acceptance
sequence ends at `0.581288144479`; it is not a criticality criterion.

The late-history 99% interval is `q in [0,7]`, density envelope `[0,0.375]`.
Together with the sealed L4, L6, and L8 envelopes, the finite common support is

```text
I_4 intersect I_6 intersect I_8 intersect I_10 = [0,0.375].
```

This interval includes vacuum-adjacent sectors and is not a critical phase or
scale-free claim.

At adjudication, free scratch was `63,078,301,696 B`, below the frozen L12
minimum `64,424,509,440 B` by `1,346,207,744 B` (about `1.254 GiB`). The L12
method gate therefore remains false. No L12 history or spectral interval sweep
was started.

**Empirical/numerically certified:** the finite L4--L10 histories and common
support after hostile pass. **Adopted:** genesis/cursor history, late window,
99% interval, numerical tolerances, and resource guards. **Open:** L12,
L4--L12 support, interval spectra, `z=1`, criticality, continuum behavior,
macroscopic closure, emergence, and gravity.
