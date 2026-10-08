# Same-state finite-gap photon budget — saved-result review

2026-09-29. Accepted as the declared conditional density comparison. No producer,
orbit, action solve, quadrature, propagation or fit was rerun. The additive
stdlib reproducer recombines the saved scalar values only.

Authenticated result SHA256:
`23feee802337320fde647fe87ff3ff24b1006c935cc3f31d9cf6a4a9574dba10`;
freeze `ba3c38436520d88daca6ffebd94fe359e0b389977537bf56ec18cf1aabf7d126`;
payload `0a08b471561a46d424efb58158d7adf53eb7506c697a50e66a4240c5074bf8a1`.
All 60 unique input files and 243 member occurrences across 11 manifests pass.
All 360 distinct labels, five gaps, four inherited quadratures and 18 reference
mappings remain present. The old source/calibration and central photon constants
are unchanged.

Production: 2,182 controls, zero failures; maximum reported discrepancy
5.762e-16; 0.00192679 s, 25,821,184 bytes peak process-self RSS. Independent
saved arithmetic: **6,171 checks, zero failures**, maximum relative difference
1.074e-15. This is algebraic corroboration, not 6,171 new physical tests.

The audit independently evaluates C through log-Beta normalization, Q and D,
every finite/asymptotic photon ratio, pressure and action labels, both exact
finite-A inequalities, sufficient approximation epochs and all family extrema.
It additionally reconstructs the finite ratio as

    rho_exc(1101)/rho_gamma(1101)
       = Omega_exc/[1101 Omega_gamma] * saved_early_dust_ratio,

which makes the matter-like versus radiation-like distinction explicit.

| Gap R | Formal asymptotic coefficient / photons | Actual saved A1101 excitation / photons | Saved A1101 w |
|---:|---:|---:|---:|
| 32 | 503.915–653.779 | 503.935–653.802 | 0.333306–0.333310 |
| 128 | 79.401–103.026 | 79.531–103.174 | 0.332248–0.332381 |
| 512 | 12.505–16.226 | 13.315–17.151 | 0.293342–0.297840 |
| 2048 | 1.9694–2.5554 | 5.4292–6.6375 | 0.02621–0.03107 |
| 8192 | 0.31016–0.40245 | 5.28028–6.41959 | 0.0001165–0.0001417 |

Each range retains 72 rows. In particular, the R8192 finite-epoch value is
mostly matter-like excitation, **not** 5–6 photon densities of extra radiation.
Its formal later-in-the-backward-continuation quartic coefficient is a different
quantity. The sufficient 1% asymptotic certificate for this gap requires
A about 157,795–168,413, not 1101; it is a sufficient bound rather than a sharp
transition epoch. The loose upper bound at 1101 is retained, while the finite
value comes from the already solved exact state, not that bound.

The low-gap rows do have nearly radiation-like saved pressure and a large
conditional density relative to photons. That is a genuine consequence to
carry into self-consistent early-expansion testing, not an observational
acceptance/exclusion assigned by this arithmetic. Ordinary photon A^4 dilution
and the scalar action/volume/clock domain are imported assumptions. The result
does not identify these modes with photons, establish a thermal hum, predict
neutrino behavior or acoustic spectra, propagate BBN uncertainty, or validate
the adopted standard-BBN baryon references under changed expansion. The matched
vacuum remains unchanged and is not relabeled as excitation radiation.

Reproduction and detailed custody/ranges:
`finite_gap_photon_budget_saved_audit_v001.py` and
`FINITE_GAP_PHOTON_BUDGET_V001_SAVED_AUDIT.json`.
