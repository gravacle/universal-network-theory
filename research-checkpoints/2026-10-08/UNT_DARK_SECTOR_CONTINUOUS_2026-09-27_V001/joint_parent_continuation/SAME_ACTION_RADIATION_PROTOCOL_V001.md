# Same-action radiation coefficient: prospective arithmetic census V001

2026-09-29. Stdlib-only positive sums and Gamma functions. No quadrature, action
root, ODE, source preparation, optimizer, changed state or new observational
number. The parent owns freeze, execution and publication. The worker prints
JSON only in `freeze` or `run` mode and writes no files.

## Complete authenticated inputs

Use ALL36 original returned-action rows and ALL6 fine high-gap pulse states,
with their actual spectral nodes and weights. Authenticate their pinned outer
result bytes, canonical payload digests, referenced freezes and recursively
every frozen member. Authenticate the completed252-row homogeneous dilution
result and648-row original-spectrum calibration the same way, including its
18 historical reference/BBN alternatives. Independently preserve and verify
the plain historical closure source's producer and input hash ledger.

Original rows must match the complete two-cutoff, two-duration, three-amplitude,
three-resolution census. Pulse rows must match gaps32,64,128 and amplitudes1,4,
with129 modes each. Cross-identify each dilution row, its six A values
{1,2,4,11,101,1101}, and each original calibration template/reference pair.
No duplicate, absent, mismatched or selected row is allowed.

The earlier calibration has a late-flat, radiation-omitted reference, with
model-dependent BBN inputs. Preserve its exact scope, assumptions, reference
metadata and qualifications. No ordinary photon or neutrino density,
temperature, observational bound or likelihood is introduced here.

## Fixed arithmetic and output

In the saved m=u=1 units evaluate independently

    C=[pi/B(1/4,3/2)]^(4/3)
     =[(3sqrt(pi)/2) Gamma(3/4)/Gamma(1/4)]^(4/3),
    q_j=C I_j^(4/3),
    Q=sum w_j q_j,  D=sum w_j delta_j^2 sqrt(q_j),
    E1=sum w_j e_j(1),  S4=sum w_j delta_j^4.

Save all modal q_j, weighted Q and D contributions, aggregate Q,D,Q/E1,
S4, and explicit soft/hard splits for pulse states. Keep every zero-action
mode with its index/reason and exactly zero q,D. A fully zero-energy state
has undefined relative Q/E1 and relative certificates, represented by null
with an explicit reason, not dropped. A positive reference excitation cannot
be normalized by such a state. An inconsistent nonzero saved energy at zero
action fails its retained inherited-state control.

For every existing dilution row save E,P and the signed certificate residuals

    E-A^4Q,  A^4Q+A^2D-E,  E-3P,  2A^2D-(E-3P).

All must be nonnegative within inherited numerical accuracy. Save the
dimensionless relative-energy certificate D/(A^2Q) and pressure certificate
2D/(3A^2Q), with explicit null reasons when Q=0. The sufficient inverse scale
factors for conservative1% and10% asymptotic energy accuracy are
max[1,sqrt(D/(epsilon Q))]. These are mathematical certificates, not
observational tolerances or a claim of a physical epoch.

Retain ALL648 original calibration mappings. For each reference fraction,

    Omega_extra_rad,asympt=Omega_exc Q/E1,
    finite_A_upper_error=Omega_exc D/(E1 A^2).

Also retain the252 existing finite-A normalized densities, linked into each
mapping at all six factors. For original calibration rows independently check
the density normalization using their frozen gstar, I0 and H0. The original
Q field denotes a VACUUM matching endpoint, not this new radiation moment;
never substitute one for the other.

Additionally retain ALL108 six-pulse by18-reference mappings, labeled
`CONDITIONAL_EXTENDED_REFERENCE_ONLY`. They do not inherit a completed
soft-spectrum calibration, gstar, vacuum solve or new abundance. If any domain
is nonpositive, retain its row with its reason instead of fabricating a ratio.

## Prospective controls and scope

Algebraic sums, dual Gamma constants, action scaling, coefficient identities,
cross-census identities and Cauchy D^2<=S4Q use2e-12 normalized tolerance.
Comparisons with saved orbit energy/pressure and the finite-gap certificate
use the inherited2e-8 energy-scaled tolerance. Reconstructing the independently
frozen original calibration uses its inherited2e-11 relative tolerance.
No asymptotic radiation fraction is a scientific pass/fail criterion.

Before processing the table, qualify Gamma equivalence; pure quartic scaling
at actions {0,1e-6,.1,1,10} and the six A values; and the trial-potential
identity at k={1e-6,1,16384}, b0={.01,1,10}, y/b0={0,.5,1}. These are only
arithmetic controls of the proved formulas, not new physical input modes.

Publish every case, mapping and failed check, with all maximum/count summaries.
The compact JSON target is2MiB; report actual bytes and excess without
truncating or deleting outcomes. This is a small rerunnable postprocess, not
a checkpointed production calculation. No package or external data is needed.

The normalized radiation consequence remains conditional on the same
late-calibrated, homogeneous isotropic/triad, adiabatic parent. Physical H(a),
tau_star and validity of the volume/redshift mapping are not supplied by this
arithmetic. Preserve the old matched DeltaU, and do not call radiation-like
mode stress photons, a CMB spectrum or an observational dark-sector success.
