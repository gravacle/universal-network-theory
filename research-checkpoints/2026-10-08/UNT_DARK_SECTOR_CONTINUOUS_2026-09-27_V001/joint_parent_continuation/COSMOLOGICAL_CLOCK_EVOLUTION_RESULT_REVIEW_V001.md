# Saved-result review: complete finite-band clock census

2026-09-29. Accepted saved custody, census and arithmetic. No ODE,
eigensystem, mode propagation or producer-function import was performed.
This reviewer authored the original evolution implementation; this is a
separately coded saved-data reconstruction, not an independent-author
replication of the integrator. The prior independent peer preflight remains
`COSMOLOGICAL_CLOCK_EVOLUTION_PREFLIGHT_V001.md`.

## Identities and complete coverage

* Freeze: `8fb4aa8b949ba4cab4eb8df5d3e9c9e97b1ab77df6fd35aa93c6f5cff9351d2f`.
* Collected file: `fda785cbe929472399d067149abb20ed744f252fe126dafe8c6d98557dc45999`.
* Collected payload: `52125bd2588818c241c1b6f36056032d5a2ec912ab1c14c281f0ac398a9bc7e7`.
* Read-only collector: `a258be84623b564009e1cabea9613aa08fefd70a849899572e3f8dc1e8c9feda`.
* Audit source: `86d6f7e17de7c489c682c92c2b3116f59647054042bc86e790d2d9ab465be4d1`.
* Audit data: `COSMOLOGICAL_CLOCK_EVOLUTION_SAVED_AUDIT_V001.json`, SHA-256
  `c20427fb88624e7058341a57bb5d872df8db4e55150bd5bacfc82a7ea25cdf62`.

All 51 frozen input members and all 12 case wrappers/payloads authenticate.
The exact epsilon=.001,.002; order=64,128; eta=.001,.1,1 census is present.
Every case has both prescribed clock basis columns, 64 common sampled epochs
and all five complete modal-state milestones. The old spectrum copies agree;
the reference retains its baryon fraction. All six 64/128 contrasts contain
all eight scalar channels and every signed epoch difference.

The producer recorded exactly **2,640 check calls**, all passing. The saved
audit performed **55,954** custody, shape, finite-value and arithmetic checks,
all passing. Those counts are not separate physical experiments. Sixty-digit
decimal reconstruction checks the actual saved Hubble, source, lapse, clock,
density and amplitude formulas, all contrast channels, and fast-limit
postmultiplications. Its largest normalized arithmetic discrepancy is
1.091e-15, against 2e-12; signed contrast reconstruction is exact at the
represented binary input values.

## Numerical controls and what is not independently reproduced

The largest saved primary-versus-tighter DOPRI error is 1.30113e-8 versus
the frozen 2e-7 target. The largest transformed-coordinate RK4 contrast is
3.55086e-6 versus 2e-5. Every saved coordinate/basis error and aggregate
maximum was checked, along with the complete numerical-gate census.

These errors use the declared full-sampled-trajectory coordinate peak scale;
they are not relative errors near every zero. Secondary solver trajectories
were not saved, so their error summaries are authenticated and checked for
internal consistency and thresholds, **not regenerated independently** here.
The retained primary modal states at all five milestones do independently
reconstruct the output clock charge and its physical scalars.

Quadrature contrasts were descriptive from the outset. At eta=.001 their
largest peak-normalized differences across the two cutoff choices are:

| Channel | Maximum 64/128 difference |
|---|---:|
| Physical tilt u | 1.20978e-4 |
| Logarithmic tilt derivative u_N | 2.70572e-3 |
| Unitary lapse times k/H0 | 6.51298e-4 |
| Acceleration/H0 | 2.12969e-5 |
| Conserved-source combination Q | 2.97876e-8 |
| Hard/polarization density contrast per k/H0 | 5.09278e-7 |

The clock-shift channel has maximum 5.04710e-5. Do not report all fields as
converged to the tilt's precision. The complete eta=.1 and 1 contrasts also
remain in the audit data, without selecting a preferred spectrum.

The sequential producer runtimes sum to 778.411 seconds; largest reported
self RSS is 40,435,712 bytes. This is process self-memory, not a measured
whole-machine reserve or enforced aggregate quota.

## Actual finite-eta result and its scale

For the initial unit-tilt column, all four spectra give sampled peak gains
approximately 6.239e9, 1.162e24 and 3.044e30 for eta=.001,.1,1 respectively.
The corresponding unit-logarithmic-derivative column gives approximately
5.068e8, 9.445e22 and 2.475e29. Their sampled peak scale factors are
.8239670, .2321337 and 1.0615591 respectively. Every exact value and its
normalization is retained, including present and final epochs.

These are arbitrarily normalized linear transfer columns, not actual cosmic
perturbation amplitudes or formation outcomes. The stated .01/peak rescaling
controls only sampled tilt, not lapse, density, unsampled extrema or nonlinear
validity. Only a two-dimensional initial subspace was evolved; this is not
the full state transfer matrix or an all-sector stability classification.

The eta/H0 conversion independently gives approximately 13.285 million,
1.3285 billion and 13.285 billion Julian years. These are illustrative
cosmological timing controls, not inferred microscopic network clock rates.
The synthetic history omits radiation even at a=.001. The result identifies
a large response for these particular zero-soft initial data and rates; it
does not exclude a much faster physical clock or establish an observed
early-universe instability.

## Fast-limit matching was also checked

The full analytical `FAST_CLOCK_INITIAL_LAYER_V001.md` was read at SHA-256
`d13d329c1a9c4b0acf4604cebddbc49f94a0cbe0fe4842ea440580429925a613`.
Its charge-based matching, positive rank-one fast operator, layer-energy
accounting and fixed-positive-band finite-interval O(eta) argument pass.
In particular Q, not the initial slow derivative alone, is retained, giving

    (u,u_N)_slow,initial = (u, (beta/Kb)u_N-(1-beta/Kb)u).

The arithmetic file and all four-spectrum, 64-epoch matched matrices were
independently authenticated and multiplied. For epsilon=.001 their a=2
tilts are 4.4639032583 and .04722522903; sampled peaks are 5.821619682 and
.06158897740. These are limiting-reference predictions, NOT a newly evolved
smaller-eta result or proof that eta=.001 has reached the fast regime.

The limit keeps positive fast quadratic energy. It permits convergence of
the slow tilt and charge without pointwise convergence of soft coordinates,
their derivatives or the instantaneous source. Its constants depend on the
fixed band, beta and background interval, and it is not uniform as the
initial epoch or lower gap tends to zero. No existing state was reset or
its coherent energy discarded to obtain the comparison.
