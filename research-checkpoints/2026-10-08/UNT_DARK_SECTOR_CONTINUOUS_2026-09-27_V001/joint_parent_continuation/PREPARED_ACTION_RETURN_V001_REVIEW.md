# Independent review: one prepared state, retained energy and pressure

2026-09-28. All 36 saved preparations and 3,840 retained modal entries were
reviewed. No new trajectory, finite-duration unloading, galaxy solve, population
fit or change of the vacuum baseline was made.

## Result

The same actions that determine the held response also predict a definite,
positive residual energy after the specified ideal adiabatic return to zero
source. The return extracts some energy, but not all the preparation work.
The complete-cycle work equals the remaining excitation energy. This closes
the energy ledger for this conditional state map without inventing a new
independent population or resetting the modes to their minima.

For the main gap=0.001, 128-mode, dt=0.005 preparations:

| Ramp duration | Final source amplitude | Returned excitation energy | Mean p/e at zero source |
|---|---:|---:|---:|
| 8 | 0.0025 | 8.77869337e-7 | 0.0006099645 |
| 8 | 0.01 | 1.37405800e-5 | 0.0023011366 |
| 8 | 0.04 | 2.02371280e-4 | 0.0080195802 |
| 16 | 0.0025 | 2.80833218e-7 | 0.0017596263 |
| 16 | 0.01 | 4.21742058e-6 | 0.0060197854 |
| 16 | 0.04 | 5.39186266e-5 | 0.0172206803 |

The energies and times are in the inherited dimensionless classical model
units. The ratios describe a mostly quadratic, low-pressure excitation
mixture. They are **not** a sound-speed measurement, a clustering calculation,
a cosmological abundance, or proof that this actual return history occurred.
Individual modal ratios span approximately 1.06e-10 to 0.332817 across the
whole retained census: a small total p/e does not mean every mode is dustlike.

## Mathematical audit

The general turning-point action has the correct normalization:
I = r²/(sqrt(2) pi) integral sin²(theta) sqrt(Q) dtheta. At zero source the
symmetric-turning-point formula and period use the same canonical momentum
p=y_dot (m=1). The inverse I0(b)=I is unique because dI/de=T/(2pi)>0 and
de/db>0. The harmonic upper bracket sqrt(2I/delta) is valid since the positive
quartic term increases I0 at fixed amplitude.

Pressure p0=I omega0−e0 equals the mean quartic potential exactly. The virial
identity gives 0≤p0/e0≤1/3. The original I omega=2 mean(kinetic) identity also
passes. The code does not discard a numerically negative pressure; its stated
tolerance is in energy units. None occurred in these saved cases.

The ledger explicitly retains the source contact Kb G²/2, the tilted modal
energy, and the complete preparation work. At the final zero source the
contact vanishes, and the same additive baseline cancels between endpoints.
Thus W_return=E_final−W_preparation and W_cycle=E_final; all cases have
W_return<0 and E_final>0. Holding actions fixed during the return is the stated
adiabatic idealization, not a demonstrated finite-time control protocol.

The production calculation verifies the action/kinetic relation and return
map. The fixed-action force identity e_h=−delta mean(y) is supported by the
separate exact action differentiation; this worker does not independently
finite-difference that derivative at every mode.

## Independent numerical and custody audit

All frozen inputs were authenticated recursively, including the phase and
trajectory ancestry; 30 distinct recorded files were checked. All 36 rows and
their original 216 row-level gates passed. I independently used uniform
midpoint quadrature with 512 and 1,024 angles, rather than the production
64/128-node Gauss rules, for every held action, zero-source inverse condition,
period, pressure and virial identity. Monotonicity plus the independently
verified inverse condition certifies the supplied return amplitude without
rerunning a physical evolution.

Maximum independently scaled identity discrepancy: 1.49311e-14.
Maximum ledger discrepancy: 1.07067e-14. Every original mode and numerical
variant was retained. Expanded held energies were recomputed directly from
the saved y and velocity, not copied from the production work ledger.

Reproducible additive audit:
`prepared_action_return_independent_audit.py` and
`PREPARED_ACTION_RETURN_INDEPENDENT_REVIEW_DATA.json`.

SHA-256 identities:

- Production source: `599b12e2a6cc9e7f5807492399b86b959a76ddcef1c7a4ab9b6b0f401ad94293`.
- Freeze: `231053248cd6ed2922bb35dd055f9d70bb0c8a2bc583a8202da50bbfe830089d`.
- Production result: `b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678`.
- Independent audit source: `8f63920f63cbccc92d5b4b9e6017d407bd53713a89a9ae9c16354e1d45dd7a76`.
- Independent audit result: `11c4cd08b8170bf86b194dcf1c9f6778551171895512d70f6604efb7f8f47a00`.

This is a constructive shared-state calculation: force, retained energy and
pressure can no longer be adjusted independently for these preparations.
The next physical test must retain that state while solving the common
metric/clock/matter constraints. A low-pressure output alone neither derives
the native preparation nor supplies its physical volume and time normalization.
