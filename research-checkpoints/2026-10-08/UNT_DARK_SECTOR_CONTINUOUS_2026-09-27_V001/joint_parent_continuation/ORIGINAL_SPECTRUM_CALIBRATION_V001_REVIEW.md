# Independent shared-calibration result review

2026-09-29. Accepted within the declared conditional original-spectrum
calibration. No changed actions, new roots, quadrature, propagation or fitting
were used in this audit.

The complete 648-row census, all 37 frozen identities and canonical payload
authenticate. Producer: 7,327 checks passed, 0.751219 s, 39,976,960 bytes peak
self RSS on Darwin, not whole-job memory. Independent saved-data arithmetic:
13,338 checks passed; largest relative discrepancy 8.69e-16. Source and protocol
were independently preflighted before this outcome inspection.

- Result: `1b155c6caf7ceb721db2f8766fa282b456b8c5f40d49555052ab4b0dc9a06abd`
- Freeze: `e98ef00c43006d8003e5cacb894373cfc6f8952dc9dd02b13bfb4c01a0021bcb`
- Payload: `66aa76a6a1dee311f452094b5f0380de6aac748bd36df4bf737ad69db376d02d`

All unchanged templates admit the positive density-matching solution. Across
all retained references and numerical controls, `g*` is 2.24246e-8 to
6.63737e-7 m/s² and `S` is 0.00152547 to 0.0458026; their product `gs` is tightly
restricted to 9.82690e-10 to 1.05819e-9 m/s² by the shared positive endpoint.
The retained excitation pressure ratio remains 0.000609954 to 0.0172207;
present-reference `Delta q0` is 0.000250214 to 0.00808985, not silently set to zero.

The quadratic-window upper scale divided by the finite-cutoff scale ranges
0.342687 to 1235.75. Values below one have no such intermediate window, and a
ratio merely greater than one does not establish a broad asymptotic window.
The inherited relaxed `a0` reference is consequently a diagnostic, not a
predicted galaxy acceleration. Changing `S` changes the actual source map:
none of the old galaxy curves can be reused by a simple rescaling.

Template 6/reference 0 illustrates the relation: `g*=3.5838333e-7 m/s²`,
`S=.00282344215`, `gs=1.01187460e-9 m/s²`, retained `P/E=.0006099645`, and
quadratic-window/cutoff ratio 4.6958. The same parameters reproduce the adopted
present density fractions by construction; they do not test expansion history.
The standard-BBN input and late-flat reference retain their original model
assumptions and omitted radiation; reference errors are not propagated here.

The reproducible audit is `original_spectrum_calibration_saved_audit_v001.py`
with output `ORIGINAL_SPECTRUM_CALIBRATION_V001_AUDIT_DATA.json`. It recombines
old modal energies/pressures, all scale/contact/fraction identities, units,
bounds, and independence from the historical reference `a0`. New modal roots
are not stored: their numerical oracle remains the producer's checked evidence,
not an independently reconstructed full modal calculation in this review.
