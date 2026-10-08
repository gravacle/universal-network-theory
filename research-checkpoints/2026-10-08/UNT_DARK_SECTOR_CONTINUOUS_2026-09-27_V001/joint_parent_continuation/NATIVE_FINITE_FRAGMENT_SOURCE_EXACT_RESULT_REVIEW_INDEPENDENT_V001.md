# Independent review of the finite fragment source result

Verdict: PASS for saved-result custody and the narrow exact-algebra
interpretation. The completed packet contains 730 check rows, all passing,
eight original/extended cases and four difference polynomials. The finite
fragment extension changes the signed source moment at order four but does
not alter its leading order-two coefficient. This is not physical, formation,
passivity or Stage 3 qualification.

The reviewer read the saved coefficients and receipts, rehashed their bytes,
and checked the sign inequalities below by hand. No producer import, syntax
compilation, rerun, propagation or independent machine recomputation of the
scientific coefficients was performed. The sign analysis is explicitly
post-result analysis, not a newly imposed acceptance criterion.

## Evidence and custody

All file names here are relative to
`/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation`.

- `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_RESULTS.json`:
  `8c35b7b7e987113dc82577b5e496bc5bf690e49fb70fe1ffde05e64476b39ae5`.
  Canonical payload digest independently matched:
  `86381307f1ff7dfefee7b6a8332493c77f259605150ba1d9d0016981cd5f2e4b`.
- `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_RUN.json`:
  `ad9f0b0ab9b5e7488fab52bd61648db65347faac3684c1a0c09c26a403ea8af4`.
  Canonical payload digest independently matched:
  `2cdd16e1b019a17baef2fc5783de50981cb6ecd9d4c5ab1e31234322b674624e`.
- `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_FROZEN.json`:
  `63ff96de66ce5802d29e5034c688a5996b724003ca800d5b43d822b06cc1864d`.
- Child intent: `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_INTENT.json`,
  `ab608bdb6c58a582f87e9668771ae5278606cee57aef77ad1a8f377537b4b0ba`.
- Monitor intent: `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_RUN_INTENT.json`,
  `03ff71864118c4c06fb06354a49bc329488426bf553201633ce09d542b774596`.
- Producer: `native_finite_fragment_source_exact_v001.py`,
  `e701bcfec5328caa2a32e30b1dcc1e17c86c6e7e5e047a55aa64942292b575e9`.
- Protocol: `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_PROTOCOL_V001.md`,
  `e3932a026d963527150b68d6e439d8e5e922ddc8f3ef95e83f385d2b9a25c17f`.
- Prior full source review:
  `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_PREFLIGHT_INDEPENDENT_V001.md`,
  `4ca8f6f2251dde8abb54e10032ecd479610bbae57642ff3bee0ce7da84ad16f6`.

All twelve run-intent file pins matched current bytes. The frozen source,
child intent, monitor intent, result identity and decoded publication stdout
agree. The complete diagnostic supervisor and relevant sampled-monitor path
were inspected read-only. Return code is zero, stderr is empty, and exception,
stop reason and monitor-error fields are clear. The result is 79,261 bytes.
The receipt reports 2.8544067919719964 seconds for the monitored invocation
and 48,660,480 bytes sampled peak process-group RSS, not an unsampled-memory
guarantee or a separately measured analysis phase. The child reports 563,240
monomial products, maximum 27 polynomial terms and maximum vector support
273, within the frozen bounds.

The saved checks cover both all-384-column current identities, all eight
coefficient cases, the two moment methods, norm and complete energy ledgers,
the original absolute energies and the prospective population controls.
The census was checked from the retained rows, not inferred only from the
summary counts. No failed row or missing prescribed case was found.

## Exact coefficients and hand sign bounds

Let `a` be the positive real cube root of 2, `u=t/hbar`, and normalize as
the frozen protocol does:

    S_Z(t)/gamma0^2 = hbar^-2 [m2*u^2 + m4*u^4 + O(u^6)].

All original and extended initial, order-one and order-three coefficients
are zero. The following m2 is identical in each original/extended pair;
`delta4` is extended minus original at order four. Minus and plus mean
the original Q=0 and Q=2 preparations, not altered initial energies.

| Preparation | Common m2 | delta4 |
| --- | --- | --- |
| A minus | `265/32 - 6*a` | `lambda^2*(7 + 7*nu/3 - 4*a^2/3)` |
| A plus | `265/128 - 3*a^2` | `lambda^2*(7/4 + 7*nu/12 - a/6)` |
| B minus | `49/8 + 129*a/64 - 6*a^2` | `lambda^2*a*(17 + 7*nu)/12` |
| B plus | `-23/8 + 6*a - 639*a^2/128` | `lambda^2*a^2*(17 + 7*nu)/6` |

These entries were checked against all four saved difference polynomials
and all eight saved moment series. The original fourth-order coefficients
are retained in the result; the table does not substitute the difference
for the complete extended coefficient.

Since `(5/4)^3=125/64 < 2 < 64/27=(4/3)^3`, the exact positive-root bounds
are `5/4 < a < 4/3`. Substituting the appropriate endpoints separately into
positive and negative terms gives

    m2(A minus) > 265/32 - 8 = 9/32 > 0,
    m2(A plus)  < 265/128 - 75/16 = -335/128 < 0,
    m2(B minus) < 49/8 + 43/16 - 75/8 = -9/16 < 0,
    m2(B plus)  < -23/8 + 8 - 15975/2048
                = -5479/2048 < 0.

For nu>=0, factor out lambda squared and call the remaining factor c4.
Then

    c4(A minus) > 7 - 64/27 = 125/27 > 0,
    c4(A plus)  > 7/4 - 2/9 = 55/36 > 0,
    c4(B minus) = a*(17+7*nu)/12 > 0,
    c4(B plus)  = a^2*(17+7*nu)/6 > 0.

Thus delta4 is positive for nonzero real lambda and is zero at lambda=0.
The frozen producer correctly left signs unevaluated; these exact rational
inequalities supply the separate post-result argument without a rounded
cube root or a selected parameter value.

## What the result establishes and what it does not

For each fixed finite real lambda and fixed finite nu>=0, the finite matrix
evolution is analytic. Its nonzero m2 therefore determines the sign for a
sufficiently small nonzero time: one positive and three negative normalized
moments, in both the original and extended cases. For a nonzero physical
source normalization gamma0 and hbar>0 the physical prefactor is positive,
so it does not change those signs. No uniform early-time interval over
unbounded parameters, numerical crossing time, or finite-age error estimate
has been obtained. A parameter that scales with time would be a different
protocol, not an exception to this fixed-Hamiltonian statement.

The positive quartic difference is a genuine conditional change in the
displayed source response, including the nu=0 boundary. It does not erase
the negative leading coefficients in three original preparations. Neither
that positive correction nor the positive A-minus leading coefficient proves
passivity, a stationary spectral measure, positive physical inertia or an
attractor. These are evolving nonstationary preparations; an instantaneous
signed moment is not by itself a full stationary passivity test. The result
also does not exclude a later state, a different explicitly derived physical
source completion, or UNT generally.

The source family still assumes node-owned fragments, their initial blank
states, symbolic gap/coupling, and the stated A/B volume/lapse assignments.
Complete on-Hamiltonian energy accounting does not supply fragment renewal,
an irreversible sink, free preparation, physical volume/clock calibration or
the common galaxy/expansion solution. No numerical time scan or higher-order
search follows automatically from this result. All physical promotion flags
remain false and all eleven mandatory program lanes remain open.

Reviewer: `urm_dark_integration`, independently of the producer author and
the root numerical runner. This review preserves the frozen computation and
its earlier source review without changing either.
