# Independent spherical dust-shadow result audit V001

2026-09-29. **Accepted as the declared moving-source dust reference and
same-state finite-R residual census.** No defect was found in saved custody,
sample algebra or the fixed numerical qualification. This is not acceptance
of an actual finite-R trajectory, a halo, or a lensing prediction.

## Exact evidence and audit scope

| Artifact | SHA256 |
|---|---|
| `SPHERICAL_DUST_SHADOW_V001_RESULTS.json` | `171fb246a4716f5b769c420cb6680a8c474cbc59f676bd10279d1e300a1b8c5d` |
| `SPHERICAL_DUST_SHADOW_V001_FROZEN.json` | `5b966f80569a25a5e3317e944af530671244cdf097bf29a0872069ce2cfc8868` |
| producer payload | `d1be24c0cfb47773e0dd020dfe71cb90c3591976c8cedb046e143f67a0dcde62` |
| `spherical_dust_shadow_saved_audit_v001.py` | `be861c06c1530586d8e4a37f72c2730037051279be172414aafaae151906a844` |
| `SPHERICAL_DUST_SHADOW_SAVED_AUDIT_V001.json` | `ba1af762fdf2c7a41f3310468bbd5dfcab49ca25e45e8be6d3b185ab6ad61985` |

All 85 frozen member hashes agree. The two selected source states agree with
both thickness-labelled copies in the old release certificate. Complete
census: R=128 and 8192, 257 shell labels, four fixed sample times, three
method vectors at each time, and 65 fine-path vectors per state. Original
64,826 numerical/arithmetic entries all pass their **unchanged** gates.
These counts are scalar numerical entries, not independent physical tests.
Root's recorded producer time is 3.93209 s and peak self RSS 55,607,296 bytes.

The independent saved-data reproducer passes 93,148 entries. It recombines
method-vector differences (maximum 3.7146e-12 against 2e-8), dimensions,
polynomial source derivatives, f/s/J/J_z, action-current density, virial
identity, pressure/sound-speed factors, signed pressure force, velocity,
internal/active stress readouts, worldtube mass/excess labels, path-domain
minima and endpoint/work-ledger identities. All published worst errors are
also checked against their actual frozen gate categories, including the
separate 2e-6 sensitivity and 2e-10 material tests.

No ODE, orbit root, quadrature, parameter finite difference or scientific
producer was rerun/imported. Material-dependent forcing integrals over all
65 times cannot be independently rebuilt from this receipt alone without
new material evaluations: full path state vectors are saved, but all path
material fields are not. Their signed arrays, alternate-node differences,
endpoint energy changes and algebraic defect identities are retained and
audited without pretending to re-evaluate those integrals.

## What the result actually establishes

The output ends at tau=1/16, or 1.663434 Myr for the fixed ell=3.2 kpc
preparation. Both saved dust paths have min J=0.9477617362 and min radial
Jacobian=0.9822749233. All saved path nodes remain in the positive-map
domain. The producer additionally tested its ODE evaluation domain; saved
nodes alone are not a continuous-time interval certificate.

The baryonic source moves with the shadow, and both closed comoving mass
labels are conserved. At the final time, the hard rest-mass excess divided
by baryonic rest-mass excess is approximately 3.45e-9 throughout the five
reported worldtubes. This small early response starts from a newly declared
uniform cosmic hard density; it is neither a long-lived galactic halo nor
an observational test of a formed galaxy. Enclosed excess is not the same
quantity as total enclosed hard rest mass or relativistic active density.

| Shadow residual diagnostic | R=128 | R=8192 |
|---|---:|---:|
| max absolute pressure acceleration / gstar | 2.22878468 | 1.32847393e-7 |
| max accumulated free-kernel velocity / vdyn | 0.04556638 | 2.71599754e-9 |
| max accumulated free-kernel comoving displacement / ell | 7.05451951e-4 | 4.20486727e-11 |
| minimum signed pressure-source work / (rest mass vdyn²) | -0.00517492136 | -3.08452744e-10 |
| max internal-energy increment / (rest mass vdyn²) | 0.577879728 | 3.44445889e-8 |
| sampled characteristic travel / ell | 0.293321133 | 0.00491283920 |

The warmer shadow therefore cannot be justified by merely describing its
instantaneous omitted pressure force as small. The colder residual is much
smaller, but a free Hubble-kernel forcing diagnostic is not a perturbation
bound for the coupled self-gravitating two-current system. The required
actual-force/Lipschitz tube remains `NOT_PROVED` for both.

Pressure-source work and thermodynamic volume work are different ledgers,
not two terms required to cancel at each material label. Pressure-energy
transport contributes to the full fluid energy balance. The volume-work
integral differs from the endpoint internal-energy change by at most
6.11339e-6 and 3.64391e-13 in vdyn² units respectively; these are descriptive
trapezoid defects, not a complete fluid-conservation certificate. The
fine/alternate forcing differences remain exposed in the audit receipt.

Both states are weak in the reported compactness/velocity senses
(epsilon=1.53780249e-7, sampled max peculiar v²/c²=3.72029191e-9).
That does not close the omitted active-energy, metric, ordinary-radiation
or acoustic-boundary errors. The inherited omitted ordinary-radiation
H² fraction today is 7.72104039e-5; its inhomogeneous brightness envelope
is still uncomputed. Positive prospective interface travel margins are
shadow diagnostics, not proof of the finite-R acoustic domain.

## Smallest concrete physical continuation

Keep this completed reference unchanged. Implement the already declared
conservative spherical **two-current finite-R system** with the same
initial state, a moving ordinary source, the exact hard pressure/internal
energy and mutual gravity. Retain mass flux, pressure work and energy
ledgers, radial/time refinement, positive-density/single-stream conditions,
and an owned exterior acoustic domain. Compare that solution with these
saved shadows; do not extend outcome-selected dust endpoints to substitute
for it. A certified coupled error tube would be an alternative, but has not
been supplied here. Full metric/null-ray and radiation controls would still
be needed before any claim about lensing or a relativistic galaxy solution.
