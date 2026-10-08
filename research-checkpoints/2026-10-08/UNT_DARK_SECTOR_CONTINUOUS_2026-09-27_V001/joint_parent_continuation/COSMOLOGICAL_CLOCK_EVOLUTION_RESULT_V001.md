# Finite-time internal clock response: complete twelve-case census

2026-09-29. All12 frozen cases completed, with2640 prospective numerical
checks passing and all original output files retained. A separately coded
full-census saved-data audit passed55954 checks. That audit's author also
wrote the original integrator; independent-author preflight and the earlier
case00 audit remain separate evidence. No secondary ODE trajectory was rerun
in the saved audit. See COSMOLOGICAL_CLOCK_EVOLUTION_RESULT_REVIEW_V001.md.
No preparation or physical parameter changed in response to the results.

## Result and useful distinction

The adopted hard-limit parent has an internal compensated clock mode even
while its total linear gravitational stress obeys the dust equations. The
specified zero-soft initial conditions can amplify strongly when its soft
response is slow on cosmological times. The opposite fast-response limit
has now been derived with its actual initial-layer matching; it cannot be
obtained simply by keeping the old initial slow velocity unchanged.

For the first normalized initial basis (unit physical tilt, zero logarithmic
tilt derivative), the largest SAVED-sample tilt transfers are approximately:

| eta=H0*tau_star | Illustrative tau_star | Peak transfer across the four spectra |
|---|---|---:|
| .001 |13.285 million Julian years|6.23868e9--6.23916e9|
| .1 |1.3285 billion Julian years|1.16173e24--1.16185e24|
| 1 |13.285 billion Julian years|3.04415e30--3.04451e30|

Both initial basis columns, every time sample and the full modal state at
five prescribed epochs remain in the raw files. The response is not assumed
monotone; saved sign reversals are retained. These are normalized linear
transfer factors, NOT measured cosmic perturbation amplitudes. The unit
initial column is not asserted physically small. Opposite hard/polarization
densities cancel in the metric at this order, but that cancellation does
not bound either separate density, lapse, tilt or nonlinear backreaction.

The tested time scales were illustrative, not inferred microscopic clocks.
In particular eta=.001 is NOT small enough to treat every soft mode as fast
at the chosen synthetic initial epoch a=.001. The calculation omits radiation
there, so this epoch is not a qualified recombination history. The universal
physical time mapping and actual formation perturbations still matter.

## Constructive fast-response result

At fixed positive soft cutoff, fixed finite time interval and positive beta,
the fast initial layer conserves to leading order

    Q=sum w*z + beta*(u' + H*u).

For the same zero-soft initial data, its phase-averaged slow derivative is

    u_N,slow = (beta/Kb)*u_N,initial - (1-beta/Kb)*u_initial.

This changes the correct slow initial data. Applying this derived map to
the already saved slow fundamental matrices gives sampled first-column
maxima about5.82162 and second-column maxima about.061589, across all four
spectra. This is saved-matrix arithmetic, not another finite-eta evolution
or a claim that the existing eta values have reached that regime.

The analytical argument retains the positive fast oscillation energy. It
establishes a fixed-band slow-variable limit, not pointwise convergence of
soft coordinates, acceleration or velocity derivatives, nor instantaneous
dissipation. Separation must include the gravitational response rate and
background derivatives as well as H. A microscopic clock or well-prepared
state cannot be declared derived from native UNT by this continuum result.
Read FAST_CLOCK_INITIAL_LAYER_V001.md and its four-spectrum arithmetic file.

## Numerical scope and reproducibility

The frozen census spans cutoffs.001/.002, quadrature orders64/128 and all
three eta values. Each case uses adaptive Dormand-Prince, a tighter repeat,
and independent-coordinate RK4. The worst tighter-repeat scaled discrepancy
is1.302e-8; worst independent-method discrepancy3.551e-6, below their frozen
2e-7 and2e-5 numerical thresholds. Exact oscillator/matter-power-law controls
and generator flux identities pass. The density compensation check is an
identity by construction, not an independent Einstein evolution.

Every64/128 contrast is saved. For eta=.001 the peak-normalized tilt contrast
reaches1.210e-4 and its derivative contrast2.706e-3, whereas the conserved
charge contrast remains below2.98e-8. These are DESCRIPTIVE quadrature
differences, not an asserted continuum error certificate. The larger eta
cases have much smaller order contrasts; their physical growth is not made
acceptable merely by numerical convergence.

Raw outputs: COSMOLOGICAL_CLOCK_EVOLUTION_V001_CASE_00.json through CASE_11.json.
Read-only complete collector: COSMOLOGICAL_CLOCK_EVOLUTION_V001_COLLECTED.json,
payload SHA-25652125bd2588818c241c1b6f36056032d5a2ec912ab1c14c281f0ac398a9bc7e7.
It binds all12 receipts and51 frozen source/input members, preserves all six
cross-order comparisons, and invokes no ODE. Total sequential producer time
was778.411 seconds; maximum single-worker self RSS40,435,712 bytes. All workers
exited. The original56-file handoff was also rechecked without mismatches.

This closes the defined finite-time diagnostic. It neither closes all-sector
stability nor rejects all physical clock choices. It provides explicit
constraints and a correctly matched fast-response route for the next shared
state/clock model, with no arbitrary clock amplitude chosen to fit the data.
