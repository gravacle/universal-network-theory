# Observational / statistical adversarial review of joint plan V002

Reviewed 2026-09-27, read-only. Draft SHA256:
`46017381d95a8ba8a1773b0f1e05a2811f20ad2dfbc7cadbc045bb019e9d11fd`.
No numerical execution or draft edit was performed.

**Verdict:** support the research direction and clarified elimination-through-
network-explanation claim. The plan no longer mistakes PPF for stability,
CPL contour inclusion for a full model test, or record number for a continuum
error theorem. Its bounded conditional findings and mandatory multi-domain
tests preserve falsifiability. The following small repairs should precede
approval; they require no new experiment now.

## Blocking statistical clarifications

**1. Calibration is inventoried, but its uncertainty and reuse need an explicit
rule.** A universal parameter fixed using dark-sector observations may support
new predictions. Treating its fitted value as an exact, zero-cost constant and
then scoring the same observations again would inflate evidence. It could also
turn the prohibition on unexplained answer-setting inputs into a naming rule.

Add to I0.5 or F0.4:

> For every empirical calibration, record its likelihood/data and uncertainty.
> Propagate that uncertainty into predictions, or evaluate calibration and test
> data in one joint likelihood with each datum counted once. A parameter fitted
> elsewhere remains an inferred input; calling it universal or fixing its point
> estimate does not make its calibration observations independent predictions.
> State separately which outputs are derived from externally fixed inputs and
> which are calibrated fits or genuinely independent predictions.

This preserves permitted calibration; it does not demand a parameter-free
theory or forbid network-derived effective matter/stress.

**2. A future release is not automatically independent of existing data.** F5
correctly requires uninspected products, but a later DESI release can reuse
earlier objects, sky coverage and calibration. SN compilation overlap is
already recognized; the same protection must apply across release epochs.

Add to F5:

> Identify overlap and shared systematics between each prospective product and
> calibration/development data. Assess new information conditionally on the
> earlier data or with a joint likelihood/covariance; do not multiply evidences
> or significances as independent when the measurements overlap. If the needed
> dependence cannot be quantified, report predictive compatibility without an
> independently calibrated “strong new discrimination” claim.

This leaves a clear pass/fail test and permits useful overlapping releases;
it changes the evidential accounting, not the target predictions.

## Execution requirement to make explicit before F4

F0.4 includes numerical precision but does not explicitly require reference
likelihood reproduction. Add one bounded validation sentence:

> Before scored candidate fits, reproduce a published reference likelihood
> point with the pinned data/software and verify relevant numerical convergence
> against the frozen error allowance. Recover a known physical limit where the
> candidate has one; otherwise validate shared solver components independently.
> A numerical/likelihood mismatch is an execution failure, not model rejection.

This is a pre-scoring implementation check, not a demand that UNT contain
Lambda-CDM as a limit or prove all gravity first. Its precision must be small
enough for the planned statistical decision; an unspecified “agreement” is
insufficient.

## Remove an unnecessary process blocker

Making different-model-family availability a hard A0/B0 condition is not a
scientifically justified proxy for independence. Different families can share
mistakes; same-family reviewers can use independent algebra, representations,
code paths and adversarial counterexamples. Neither arrangement is independent
empirical validation.

Replace the family gate in the minimal-process section and I0.7 with:

> Require an independent derivation or implementation plus focused adversarial
> review. Record shared assumptions, methods, code and reviewer/model provenance.
> Prefer reviewer-family diversity when available, but its absence alone does
> not block A0/B0. Resolve substantive findings; do not label internal review
> independent observational evidence.

The new plan should identify this as an explicit procedural revision of V001,
not falsely report the old family-specific condition as fulfilled.

## Minor improvements / retained strengths

- Include cross-covariance between DESI BAO and RSD/full-shape products from
  shared samples in the existing F4 covariance requirement, not just within
  each likelihood. Compression validity also needs checking for the candidate.
- Keep thresholds and the exact mandatory test set deferred to I0.6/F0.4 until
  the construct is specified. Their absence in this roadmap is not itself a
  blocker; no scored gate may activate while they remain undefined.
- Keep galaxies optional only for the expressly restricted cosmological claim.
  The finite merger/galaxy/structure set for the broad claim is appropriate;
  it need not become a requirement to solve every astrophysical system.
- “Strong new discrimination” must remain separate from explanatory economy.
  A network derivation may explain previously postulated effective components
  while sharing predictions with an effective dark-sector model. Lack of a
  discriminatory observable limits the empirical preference claim, not the
  validity of the derivation itself.

No additional blanket phantom-crossing prohibition, arbitrary universal
Delta-chi-squared cutoff, unbounded simulation requirement, or proof of dark
component nonexistence should be reintroduced.

## Final recheck — 2026-09-27

Read-only recheck of the revised plan, SHA256 verified as
`6b2a8bee520e828f4ccc583db920f289fe0c0a9eefd85fd78c22b6db90da2ccc`.
The preserved review draft has SHA256
`46017381d95a8ba8a1773b0f1e05a2811f20ad2dfbc7cadbc045bb019e9d11fd`,
matching the original review above. Checked the revised text and the complete
diff against that draft. No numerical work or plan edits were performed.

**Verdict: the requested repairs are resolved; no remaining observational,
statistical or perturbation-planning blocker identified in this review.**

- Calibration uncertainty propagation and once-only data accounting are now
  explicit after I0; F4 also forbids recycling a calibration posterior while
  counting the same measurements again. I0.1 correctly forbids an abundance
  setting its own purported prediction without forbidding declared external
  baryon or calibration inputs. These are inputs, not independent successes.
- F5 now treats reused observations and shared systematics conditionally or
  jointly. Unquantified dependence limits evidential claims rather than
  blocking useful compatibility tests.
- F0 requires bounded reference-likelihood and convergence checks before
  scoring, without demanding that UNT contain Lambda-CDM as a limit.
- Methodological independence and resolved substantive findings replace
  model-family availability as the A0/B0 gate. Provenance and shared inputs
  remain disclosed, and internal review is not empirical validation.
- The minor BAO/RSD cross-covariance and candidate-valid compression concerns
  are addressed. Ordinary inference within frozen priors is distinguished
  from changing the construct; early screens remain bounded rather than
  requiring the complete observational program in advance.

This approves the roadmap at its stated level, not a physical construct,
A0/B0 freeze, statistical threshold, implementation or observational result.
Exact mandatory products, priors, error allowances and pass/fail thresholds
must still be filled in before their scored gates activate. The plan keeps
that obligation explicit and retains the broader multi-domain target,
conditional-interface labels and distinction between explanatory economy
and strong new empirical discrimination. No extra administrative phase or
new experiment is requested by this recheck.
