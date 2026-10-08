# Frontier V124 — fixed-parameter direct lensing and type contrast

2026-10-04. Resumed actual scientific execution after the user's status
question. This is new data-facing work, not a rerun of the prior galaxy fit.
Stage 3 and the dark program remain OPEN. No proof of UNT superiority or
absence of DM/DE is claimed.

## New evidence

The galaxy-calibrated older stationary response now has a direct forward
ESD calculation, with the public Brouwer2021 KiDS covariance and calibration
factors. The mass cancels at fixed gbar for the adopted spherical compact
source; no mean-mass substitution or universal SIS conversion is needed.
Its galaxy a0 and inherited shape were held fixed; no lensing halo, slip or
normalization was fitted. The metric bridge and source assumptions remain
conditional, not a formed K(X) result.

Seven primary bins (gbar>=1e-13 SI): Q=64.107 for the inherited response,
62.217 for empirical RAR and 739.567 for Newtonian baryons. These are
statistical-covariance mismatches, NOT full theory likelihoods. The candidate
greatly improves on baryons alone but does not pass nominal precision lensing
or outperform the empirical relation. Bin averaging alternatives do not
remove the central tension. An optimistic conditional bound for arbitrary
positive bin weights gives Q>=30.064 under nominal masses and a monotone
within-bin envelope. A separately declared +.2-dex total-baryon sensitivity
gives centre Q=31.413 and bound>=6.631; not a selected recalibration.

The same saved predictions applied to the spectroscopic GAMA control give
Q=15.943 for the matched seven bins and 20.253 for all15, versus baryons
58.011/95.942 and RAR15.818/20.107. GAMA has larger errors and different
selection. Without cross-covariance/matched catalogues we cannot attribute
the difference to isolation or combine the two as independent evidence.

A new candidate restriction was then tested: this acceleration-only family
predicts zero galaxy-type contrast at exact common gbar. Public cross-type
covariances give seven-bin zero-contrast Q=28.085 for red/blue and 20.939 for
high/low Sersic. All15 give119.926/69.070, including the flagged tail. Primary
log10 arithmetic-mean ESD ratios are .20618/.16165. Type-dependent ordinary
baryon calibration, geometry, bin weighting and environment remain relevant;
these observed correlations are not evidence of a network mechanism by
themselves. No environmental coefficient was tuned to rescue the candidate.

## Evidence and qualification

Detailed equations, source conventions, all outcomes and next action:
`joint_parent_continuation/EFFECTIVE_ESD_FORWARD_V001_REPORT.md`.
New receipts in that directory:

| Receipt | SHA256 |
| --- | --- |
| EFFECTIVE_ESD_FORWARD_V001_RESULT.json | ec9a99b80bebf2a634ae4068407e4ee6767614c43d5376eb6e564076f5b5a433 |
| EFFECTIVE_ESD_BIN_BOUND_V001_RESULT.json | db518cd7d312369250ad02dde0ddecd1280c226ae4be3f4978da715ac1049cfb |
| EFFECTIVE_ESD_GAMA_CONTROL_V001_RESULT.json | 0fdbd4f82b1734bf06c6bb0dac6feee5eec57d8863b4f7a768eb0c8af101959b |
| EFFECTIVE_ESD_TYPE_CONTRAST_V001_RESULT.json | 179e4e129e8f47dfbea3c439c34a39b41bc7af862bddffcc24e25d1c91359659 |

The main worker passed22 frozen controls in .47seconds/~55MB. Independent
source review accepted the force derivative, both projections, units and
covariance. Saved-only audits reproduced135 KiDS and135 GAMA scores to
scaled discrepancies below4.4e-16. All numerical workers ran sequentially
and exited. The type-contrast saved audit also checked all six archive
members, both cross-type covariances and every score/bound to4.44e-16.
The public2.3MB archive is saved intact with provenance; initial
sandbox DNS failure and approved public retrieval are documented. No install.

## Exact continuation and non-duplication

Next: quantify required differential total-baryon calibration through inverse
ESD for the seven primary type-contrast bins with frozen force parameters
and joint covariance. This is an inference diagnostic, not a new prediction
or permission to add per-bin freedom. Compare with independently supported
stellar/gas calibration rather than selecting offsets for agreement. If
catalogue-level weights are unavailable, preserve that evidence ceiling.

In parallel, the shared expansion source/evolution law remains the central
missing join. Do not repeat the existing operational-clock dictionary or
the DESI common-amplitude/AP calculation as new science. The new algebraic
observation T'=R for T=DM/rd,R=DH/rd does not yield an exact sparse-data test
without an interpolation/evolution assumption; no new BAO run was launched.
Preserve the eta=1 no-acceleration result AND the stronger trace-only scalar
kinetic failure, and the separate K(X) abundance/vacuum audit. A new physical
coupling or evolution law must change an identified premise and face both
galaxy/lensing and expansion constraints; mere time relabelling cannot do it.

Outstanding ledgerV065 and URM developmentV043 keep all11 lanes open,
including CMB perturbations/observations and the separate thermal-origin
hypothesis. Explanatory economy is part of the comparison; a lower baryons-
only residual alone is not superiority over the full standard model.

Old heartbeat remains PAUSED and separate Goal unchanged. Same Mac only,
one small numerical worker, no installs/remote/L8/publication/credit spending.
Frozen inputs, failed hypotheses and preexisting tracked URM edits preserved.
