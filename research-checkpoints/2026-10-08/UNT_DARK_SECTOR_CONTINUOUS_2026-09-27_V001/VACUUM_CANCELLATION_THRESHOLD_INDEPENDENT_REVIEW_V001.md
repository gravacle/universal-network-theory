# Independent review of vacuum cancellation threshold test

2026-09-27. Read-only analytical review; no numerical run or historical edit.
Reviewed `VACUUM_CANCELLATION_THRESHOLD_TEST_V001.md`, verified SHA256
`935fe48989b6de5c8dba765c888db76af0734fdbfc071a8cbe8fe689cff2d410`.
Also read the resident corrected spectral census and convention-reconciliation
review. Their external primary sources were not independently reauthenticated
in this review; the checked identities follow from the displayed integral.

**Verdict:** the main theorem and leading residual are correct in the declared
finite, fixed-mass class and RIEHB coefficient convention. One targeted
finite-splitting clarification is recommended below. This is a diagnostic
mechanism class, not a derived UNT spectrum or observed dark-energy result.

## Checks that pass

- Integrating the exponential Taylor terms gives precisely the quartic,
  quadratic and logarithmic moments displayed. For nonnegative masses the
  absolute third-order remainder is bounded by
  `(sum |w_i| lambda_i^3)(mu^-2-kappa^-2)/6`. The bound is valid without a
  light-mass approximation; smallness is needed only for useful truncation.
- The `(1,-3,3,-1)` example has zero first three moments and positive
  `Z0=(1-exp(-m^2 s))^3`, so those moment cancellations do not cancel a
  finite shell. The negative action prefactor has not been lost.
- Vanishing on **every subinterval** forces the continuous integrand to
  vanish. Combining degenerate masses and taking derivatives gives an
  invertible exponential-weighted Vandermonde matrix. Therefore it is
  equivalent to zero aggregate weight at each distinct mass. Cancellation
  on just one selected shell is correctly not claimed equivalent.
- For the split pair, `C0=+hbar w delta I1/[2(4pi)^2]+O(delta^2)` and
  `CR(0)=-hbar B I1/[2(4pi)^2]`. Thus
  `Lambda=-C0/(2CR)=w delta/(2B)+O(delta^2/mu^2)`. The ratio has mass-square
  units. With the denominator sign protected, healthy stiffness requires
  `B<0`, and positive Lambda requires `w delta/B>0`. No raw statistical
  rank is silently substituted for convention-matched volume weights.

## Make denominator control explicit for a finite splitting

The existing fixed-finite-weight-ratios qualification is sufficient for the
asymptotic big-O statement. It is not by itself a numerical smallness bound
when B is a near-cancellation. Let beta be the shifted member's fixed curvature
weight, q=|delta|/mu^2, and

    I0=integral_a^b s^-1 exp(-m^2 s) ds <= I1/mu^2.

Taylor's bound, uniformly for either sign of delta, gives

    |C0-hbar w delta I1/(2L)|
      <= hbar |w| delta^2 exp(q) I0/(4L),
    |CR(delta)-CR(0)|/|CR(0)|
      <= eta := |beta/B| q exp(q).

Require eta<1 (or eta<=1/2 for a convenient robust bound) before asserting
the finite-splitting curvature coefficient retains its sign. Then

    |Lambda-w delta/(2B)|
      <= |w delta|/(2|B|) * [q exp(q)/2+eta]/(1-eta).

This makes the stated remainder and its dependence on near-cancellation
explicit without adding a mode, fit or cutoff adjustment. For a low-curvature
application, small `|w/B| |delta|/mu^2` is also relevant; a small splitting
alone does not bound curvature when that ratio is very large.

These bounds assume the proposed pair's curvature weights are fixed while
its one mass shifts. If couplings, weights or other matching terms change,
their derivatives belong in the same expansion. The note already excludes
unaccounted dominant contributions; that restriction must be retained.

No further blocker was identified. The protecting identity, actual field
operators, breaking law, full matching ledger and stability remain unearned
physical inputs, correctly not presented as consequences of retained records.

## Final hash-bound recheck

2026-09-27. The root incorporated the finite-splitting clarification. Verified
the revised note SHA256 as
`996959d2531e39ac233f4a1e90f0f6eef4b53965f8eaabdc408f50b7c3e1981e`
and read the added bounds. Its r is the eta defined above. The numerator,
relative denominator and exact ratio bounds agree with this independent
derivation; fixed curvature couplings and r<1 are now explicit.

**Final verdict: accepted as a conditional analytical threshold/protection
test; no remaining blocker identified.** The original reviewed identity and
recommendation remain above as history. This does not authenticate a UNT
field spectrum, protecting symmetry, breaking scale, observational magnitude
or complete matched vacuum solution. No numerical execution or historical
source edit was performed.
