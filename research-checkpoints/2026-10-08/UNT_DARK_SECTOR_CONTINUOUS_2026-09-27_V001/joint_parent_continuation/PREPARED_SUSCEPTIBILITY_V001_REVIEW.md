# Independent review: same-state scalar susceptibility census

2026-09-29. Accepted. All 36 returned-action preparations and 3,840 mode entries
are retained. The saved arithmetic is consistent with the reviewed exact
scalar susceptibility, and no numerical failure or custody mismatch was found.
No propagation, orbit quadrature, fit, or scientific-source import was performed
in this audit.

## Evidence and recombination

- Result SHA-256:
  `0ce518ac17c84f0d116272597f9abb0ee5ab7bd41db8372699203ec9b7b21f40`.
- Freeze SHA-256:
  `ff4b78da4b8215733ee5ea32a28666fd5fe7fbabba927067376baf9f6bda771e`.
- Payload SHA-256:
  `3fd46667b3463e5637a064e5425861bbb207c6d3ac5d83b079d25a8c54a23be7`.
- All 33 frozen input identities and the three input-result payload/freeze
  wrappers authenticate. The original 42,491 checks report no failures.
- `prepared_susceptibility_saved_audit_v001.py` independently uses 50-digit
  Decimal arithmetic and the old saved mode data. Its 54,600 checks pass;
  output is preserved in `PREPARED_SUSCEPTIBILITY_V001_AUDIT_DATA.json`.
  The alternative susceptibility is reconstructed from the saved quartic
  moment and turning amplitude, not obtained by repeating the producer's
  energy/pressure formula. It is still a saved-data algebraic crosscheck,
  not an independent response experiment.

The audit checks every modal energy, pressure, contact identity, turning-point
bound, Jensen inequality and energy-defect bound; every weighted aggregate;
and all 24 matched numerical-resolution differences. The largest reconstructed
modal q discrepancy is 2.57e-15, and the largest discrepancy in k times the
susceptibility is 2.67e-15. Aggregate mu differs by at most 3.05e-17.
All pressure/contact inequalities hold without clipping a value.

## Result

Every retained preparation has a positive linear coefficient. Across all 36
rows, `mu_linear` ranges from 0.0037250227806973 to 0.0541510274658440.
For the gap 0.001, order 128, time-step 0.005 cases:

| Preparation duration | Source amplitude | mu_linear | P/E |
|---|---:|---:|---:|
| 8 | 0.0025 | 0.00385470013 | 0.000609964535 |
| 8 | 0.01 | 0.01490179535 | 0.00230113656 |
| 8 | 0.04 | 0.05415102747 | 0.00801958021 |
| 16 | 0.0025 | 0.00372799948 | 0.00175962626 |
| 16 | 0.01 | 0.01358962825 | 0.00601978544 |
| 16 | 0.04 | 0.04302765675 | 0.01722068034 |

The shared template is row 6: energy 8.778693373929561e-7,
`mu_linear=0.0038547001277392423`. Its conservative distribution lower bound
is only 5.219029018825614e-6; that bound is necessary, not a sharp prediction.

The largest relative change in mu under the old 64-to-128 spectral refinement
is 3.24e-11; under the old time-step halving it is 1.05e-12. Corresponding
maximum changes in E are 1.08e-12 and 2.26e-11, and in P are 2.05e-10 and
2.15e-12. These are descriptive comparisons of existing calculations, not
an uncertainty estimate for the physical model. Both lower-cutoff families
remain visible and are not a single identical finite-band system.

The producer recorded 0.07933058299 seconds and 26,951,680 bytes peak self RSS;
this is not a measurement of whole-job or computer memory.

## Scientific implication and precise scope

The excitation retained by the already defined preparation and ideal
fixed-action return has a calculable, positive low-field contact defect.
Its pressure and response cannot be assigned independently. For this fixed
positive band and these fixed scalar actions, the strict weak-source law
begins `D(g)=mu_linear*g+O(g^3)`, not with the relaxed continuum quadratic
term. This supplies a concrete common-state constraint for joint inference.

These are zero-source, scalar, phase-averaged derivatives of the returned
actions—not a finite-time source response, an evolved galaxy, or an isotropic
vector susceptibility. Taking a zero-gap limit, varying the preparation with
the source, and holding each action fixed are different operations. In
particular the earlier quench-family quadratic coefficient cannot replace
this derivative. No observational exclusion, native-to-physical dictionary,
cosmic abundance, or stationary clock/metric solution follows from the census
alone. The result also does not rule out a transparently recalibrated shared
state or a separately declared and tested spectral extension.
