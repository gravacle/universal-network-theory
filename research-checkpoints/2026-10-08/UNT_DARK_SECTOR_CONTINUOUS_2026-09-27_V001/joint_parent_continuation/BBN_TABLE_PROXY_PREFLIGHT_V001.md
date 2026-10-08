# BBN table proxy V001: independent source-only preflight

Accepted 2026-09-29. Full worker, protocol, interface audit and prospective
BBN design read; the relevant pinned PRIMAT plasma, background, constants,
neutrino-history, generator and table-header mappings were checked directly.
No producer/module import, interpolation run, orbit calculation, nuclear
evolution, abundance scoring or external download was performed.

Settled bytes:

- `bbn_table_proxy_v001.py`:
  `96059bdb6f236b84e4d82edf2d6dc7c8d6c61b59504fab84831515a636d3a4c0`.
- `BBN_TABLE_PROXY_PROTOCOL_V001.md`:
  `43227176ed42d0580116e672228aa0cd45ff4b1aec043c4b5e8601977b9d0e98`.
- `PRIMAT_2026_INTERFACE_AUDIT_V001.md`:
  `dd5f14980d2c5a9a7d9a9f552a7f873274348e73c1d933da85eb52df6f472c51`.

## Formula and numerical-method checks

The primary table's columns, nucleon-number helium convention, D/H ratio,
Monte-Carlo marginal errors and DeltaNeff mapping are correctly retained.
The late photon conversion is (7/8)(4/11)^(4/3). Local tensor-cubic and
bilinear-sigma index order, no-extrapolation behavior, all-node recovery,
three withheld-node controls and polynomial controls are consistent. The
fixed 360 labels and 18 matched-zero baselines are retained, with out-of-table
rows unsupported rather than rejected or extrapolated. No best row is fitted.

Independent elimination of the endpoint second derivatives gives the same
not-a-knot tridiagonal equations. Local polynomial shifting, Bernstein hulls
and division by positive T powers have the correct normalization. Their
floating padding is explicitly an arithmetic envelope, not directed interval
arithmetic or a bound on unknown continuous nuclear physics. The final
version checks both interpolant and supplied heat capacities, positivity,
nonempty intersections and nontrivial raw/factored synthetic identities.

With sigma=s/T³, Ct=T^-2 ds_interpolant/dT and Cs the supplied counterpart,
the independently expanded log-density-ratio derivative is

    (4/3) Ct/sigma - 4 Cs/(3sigma+N)
      = (4/3)[N Ct/(sigma(3sigma+N)) + 3(Ct-Cs)/(3sigma+N)].

This matches the implementation, including the signed derivative mismatch.
The original source clips the signed NEVO numerical heating tail and
interpolates it in photon temperature; the worker follows and discloses that
prescription. It does not infer the actual history from a variable's name.

The pinned endpoint is a_end*T_end/T0=(sigma_end/s_gamma)^(-1/3).
Consequently its fourth power cancels the endpoint extra-density entropy
factor exactly. The final worker retains both and uses their combined log,
without adding a spurious entropy correction. The same relation yields
A=(T/T0)(sigma/s_gamma)^(1/3)exp(-L/4). Using global sigma/L bounds therefore
gives a conservative A lower bound for the 10-keV finite-gap correction,
rather than silently treating T/T0 as an exact scale factor during heating.
The plasma-only ordinary-density lower bound gives the stated conservative
H-ratio envelope for the fixed ordinary history.

## Custody and scientific scope

Recursive inherited freezes, exact table bytes, the inert source receipt,
observational products and new sources are bound before execution. No code
download is imported. The source is stdout-only. The final protocol and
source receipt both enumerate **eleven** official snapshots after constants.py
was added. Their complete hash/byte verification is retained.

The public generator supplies source/API provenance, not proof of the exact
invocation producing the published table. The thermal envelope retains fixed
ordinary-neutrino heating and is not an abundance-response error bar or a
self-consistent altered decoupling solution. The conserved-scalar abundance
status remains NOT_YET_QUALIFIED even if every numerical check passes.
Inherited standard-BBN baryon values are conditional inputs; deuterium is an
exposed consistency channel, not independent validation. Marginal residuals
and separate uncertainty budgets do not become joint significance or an
exclusion claim. These boundaries are explicit; no load-bearing defect remains.
