# Open curvature plus an additional kinetic coefficient: result

2026-10-04. This is a failed observational screen of a specified effective
extension, not a failure of every possible network universe.

The frozen 36-case grid completed in 4.9835 seconds, one process, peak RSS
62.7 MB. All 36 cases are retained: 32 pass the sampled numerical/domain
checks and four are inadmissible at both force quadratures. All 550 recorded
controls pass. No exception, resource-budget omission or refinement
disagreement occurred. Positive local scalar kinetic sign and 0<F'<1 are
necessary screens, not proof of all-mode or nonlinear stability.

The same galaxy-calibrated a0 and inherited r were used throughout. Curvature,
H0 and eta are three exposed development coordinates; kappa follows from the
present constraint. Each scored case has ONE fitted common BAO amplitude.
The complete 13-vector and covariance include both radial and transverse
distances evaluated in the same open geometry. No galaxy force, ordinary
density, per-bin offset or acoustic history was refitted.

## Outcome

Across all 32 qualified cases, the covariance discrepancy Q ranges from
682.3251 to 1652.4775. Their present deceleration parameter ranges from
-0.52941 to -0.13978: these examples really can accelerate while passing
the declared local kinetic screen. Acceleration by itself plainly does not
suffice to reproduce the observed distance shape. The amplitude ranges from
26.2987 to 28.6213 and implies rd=142.316--189.992 Mpc; these are fitted rulers,
NOT predictions of recombination or drag physics. All amplitudes are positive.

The lower endpoint of the reported Q range is a descriptive grid minimum,
not an optimized fit, accepted candidate, held-out prediction, p-value or a
global bound over all parameters. No case has been selected for promotion.
The individual scores, inputs, dense histories and refinements remain in
CURVED_SHARED_GEOMETRY_V001_RESULT.json.

All four inadmissible cases have Omega_K0=.5. At H0=60, eta=100 the kinetic
screen fails despite kappa>1. At (H0,eta)=(70,100), (73.6,100), (73.6,1000),
kappa>1 also fails. These are physical domain outcomes, not numerical errors.

## Independent internal audit and limitations

A separate saved-array audit verified all nine dependency hashes, case
inventory and all 550 controls. It recomputed all 32 amplitudes, full-covariance
Q values and implied rulers with maximum scaled differences 4.0e-16,
1.1e-15 and 5.5e-16. Reconstructing q(z) from the background derivative and
saved lambda_eff agreed within 1.8e-13. No producer rerun was needed.

Source review identified two unused boundary/status weaknesses: the code
would allow a clamped zero amplitude to reach the qualification branch, and
a distance-node-only disagreement of force-order domain signs would be
labelled inadmissible rather than unresolved. Neither occurred in this
receipt. Preserve the frozen source and result; any reuse must correct those
branches under a new source version rather than silently modifying custody.

Result SHA256:
4b45676ea70e41c4c49f241be4895144b9a30b6a0e2282f558130ac6a686e676

## Early-universe consequence, derived independently

For this same constant-kappa action, on a regular continuation to large y,

    kappa H^2 = (8 pi G_N/3) rho_ordinary - K c^2/a^2
                + (a0/c)^2 G(y)/3,
    G(y) -> F_infinity,    G_y -> 0,
    H(T)/H_GR,same-radiation(T) -> 1/sqrt(kappa).

Thus kappa>1 reduces expansion at a fixed physical radiation temperature.
This is a normalization result, not a numerical BBN exclusion. The frozen
low-redshift grid does not prove continuation to BBN or specify its full
temperature-dependent radiation inventory. Finite a0/r changes a bounded
term; spatial curvature scales as a^-2. Neither supplies the missing a^-4
normalization over a radiation-dominated interval. Changing thermometry or
the clock-rate mapping would change reaction and photon observables too.

At fixed physical baryon/photon densities and fixed drag endpoint, a
uniform suppression H=H_ordinary/sqrt(kappa) would enlarge the sound horizon
by sqrt(kappa). Here 'ordinary' means baryons plus radiation, not a CDM
reference. Actual drag/visibility endpoints must be recomputed; total omega_r
alone does not determine the photon/neutrino split or sound speed. The
angular acoustic scale also depends on the curved D_M and has no automatic
sqrt(kappa) rescaling. Old K(X) BBN/HYREC successes do not transfer.

## Scientific decision

Do not launch another nearby curvature grid or a new thermal calibration for
these failed distance shapes. The useful next question is which actual
constraint/clock-state assumption must change. Generalize the trace-only
kinetic restriction, then examine an independently specified dynamical clock
or memory coupling that can evade it while restoring radiation-era behavior.
Such an operator is a new counted completion, not a native UNT derivation or
an implicit permission to choose a free H(z). Retain the successful galaxy
phenomenology separately. Stage 3, both CMB tracks and superiority remain open.
