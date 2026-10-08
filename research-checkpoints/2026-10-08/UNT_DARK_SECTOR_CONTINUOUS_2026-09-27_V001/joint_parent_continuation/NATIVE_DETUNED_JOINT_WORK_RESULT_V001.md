# Actual and averaged joint work in the detuned network

2026-10-03 UTC. The frozen 960-dimensional K3,3/Q2 experiment completed
in 3.325 seconds on one single-threaded worker, with peak RSS 328679424
bytes. All implemented numerical controls passed their prospective
tolerances. No initial-state reset, fitted source profile, new coupling,
larger graph or changed acceptance criterion was used.

The result is mixed and operationally specific. The phase operation alone
has positive work curvature throughout both tested endpoint-age intervals.
The joint energy-source and phase operations nevertheless have negative
quadratic work directions in both formation-age windows. Both exact
window-averaged work matrices are positive. This distinguishes an
age-unresolved response from the actual clock-resolved response; it is
neither an energy-conservation violation nor a gravitational prediction.

## Frozen experiment and work accounting

The supplied graph, actual rank-15 carrier mixture and all 64 blank-record
states are retained. This is not the earlier resonant sector reduction.
The unchanged local detuning is delta=-1/2. Complete bulk energy is
H=sum_v h_v, with the 60I graph baseline retained, initial mean316/5,
and symmetry-fixed mean h0=158/15 at all autonomous ages.

The isolated reference clock defines A=2*pi/sqrt(5)=2.8099258924162904.
Formation ages are a in [0,A] and [A,2A], sampled at 257 unique ages.
After formation, the source alpha*F, F=h0, acts for T=A/2. It is
switched OFF before the carrier phase operation exp(+i*lambda*P), P=p0.
The clock is separate, coherent and untouched by this source.

For I=i[H,P] and D=[P,[H,P]], the complete cycle obeys

    W_on=alpha <F>_a,
    W_off=-alpha <F>_after_source,
    W_phase=(1-cos lambda)<D>+sin lambda<I>,
    W_cycle=alpha^2 W_F2+alpha*lambda R_IF+lambda^2*kappa/2+O(3),
    M=[[2 W_F2,R_IF],[R_IF,kappa]], W_F2=-R_FF.          (1)

Here kappa is evaluated at a+T, not at a. Consequently positive endpoint
curvature below does not contradict the previously proved negative
curvature at sufficiently early physical ages. The mandatory source-on
contact is D'=D/2. Source-on response is R_DF_off+kappa/2; it cannot be
silently equated with the source-off response. Applying a kick before
switch-off changes both its work and switch-off work; the contact cancels
in their sum. The worker explicitly checks this identity.

## Results with fixed controls and time windows

| Quantity | Formation ages 0 to A | Formation ages A to 2A |
| --- | ---: | ---: |
| Mean kappa at endpoint a+T | 0.0327330053 | 0.0229149820 |
| Mean W_F2 | 0.0350856358 | 0.0266015863 |
| Mean R_IF | -0.00757346560 | -0.00507802818 |
| Eigenvalues of mean M | 0.0312589879, 0.0716452890 | 0.0220862882, 0.0540318664 |
| Minimum sampled eigenvalue of actual M | -0.117502653 | -0.0209061945 |
| Negative actual rows out of 129 | 33 | 48 |
| Negative rows with both individual diagonals positive | 10 | 21 |
| Minimum sampled endpoint kappa | 0.0152116924 | 0.0109815954 |

The two windows share their boundary row. Counts refer to each window,
not distinct trajectories or independent astronomical observations.

The frozen spectral second-derivative bound gives scalar interpolation
error 0.000144825267 for kappa and matrix operator error at most
0.000897368679. Thus endpoint kappa is positive throughout BOTH intervals,
not merely at sampled ages, subject to the assigned numerical error guard.
This is an analytic interpolation bound evaluated numerically, not
interval-arithmetic certification. The negative joint rows require no
interpolation assumption: they are explicit finite-time witnesses.

The cross term matters even when both diagonal entries are positive.
For example, at formation age0.5049085588 the two diagonals are
0.00661729648 and0.0675239340, but the cross term is-0.0487238545 and
the minimum joint eigenvalue is-0.0203873575. In the second window,
age5.3783737785 has positive diagonals0.000403767401 and0.0223332301,
yet minimum eigenvalue-0.0130999961. These are post-run interpretations
of the frozen census, not new fitted protocols or favorable-age passes.

## Finite controls confirm actual energy extraction

As prospectively specified, the most negative sampled row was checked
with both signs of three amplitudes along its same normalized eigenvector.
Its age is0.06585763810, eigenvalue-0.11750265268 and direction
(alpha,lambda)/amplitude=(-0.9879305486,-0.1548974858).

| Amplitude magnitude | Actual work for positive amplitude | Actual work for negative amplitude |
| --- | ---: | ---: |
| 1/64 | -1.43841741e-5 | -1.42799184e-5 |
| 1/128 | -3.59168870e-6 | -3.57866097e-6 |
| 1/256 | -8.97242856e-7 | -8.95614733e-7 |

All six total works are negative beyond the frozen1e-8 sign guard.
The maximum full work-closure error is3.174e-13. The largest-amplitude
departures from the quadratic approximation are4.06e-8 and6.37e-8;
these are retained nonlinear corrections, NOT agreement to1e-8.
Relative discrepancies fall below0.1percent for the smallest amplitudes.
The worker did not require higher-order corrections to vanish.

The prepared blank-record state supplies finite ordered energy/information
resources. Extractable work is consistent with its closed microscopic
dynamics. It does not establish negative gravitational energy, an unstable
universe, a perpetual source of work or failure of every nonequilibrium
collective description. Controller preparation, clock access and repeated
state supply are not thereby free.

## What time averaging does and does not establish

The reported averages integrate the actual bulk state with the exact
spectral sinc factor; no near-gap coherences were discarded. For a
control vector c=(alpha,lambda) chosen independently of unresolved age,

    mean W = (1/2)c^T mean(M)c+O(|c|^3).               (2)

Both positive mean matrices therefore pass the necessary quadratic
condition for THIS age-blind pulse-and-kick family. They do not prove
general passivity, spectral positivity, a steady state or a physical
metric. Age-resolved operations use M(a), not mean(M). Restricting a
physical observer to unresolved age would require an independently owned
clock resolution and weighting model, not choosing an average because
its sign is favorable. The actual reference clock remains coherent.

There is also a quantitative obstruction to a uniformly accurate passive
replacement. For any positive-semidefinite candidate M_eff(a), the unit
eigenvector z at a negative actual row obeys

    ||M(a)-M_eff(a)||_op >= -lambda_min(M(a)).          (3)

Thus a passive replacement of the complete two-control response must
have error at least0.117502653 somewhere in the first window and
0.0209061945 somewhere in the second, up to numerical guards. This is a
bound on this response dictionary, NOT on arbitrary active effective
models or gravitational theories.

For the particular constant choices mean(M), the sampled maximum
operator errors are0.185450459 and0.0880552375. The interpolation bound
places their full-window suprema no higher than0.186347828 and0.0889526062.
These values follow directly from the saved rows using, for a symmetric
2x2 difference [[a,b],[b,c]],

    ||difference||_op=max(|(a+c)/2 +- hypot((a-c)/2,b)|).

Consequently a positive mean is not a small uniform approximation to the
resolved history. A viable reduction must retain memory/age dependence
or justify a genuinely limited physical measurement protocol.

## Diagonal comparator remains unresolved

The frozen energy clustering produced315 blocks, maximum within-block
spread2.274e-13 and minimum interblock gap1.506e-9. The last value fails
the predeclared1e-7 separation criterion. Its apparently positive work
matrix is therefore NOT a resolved stationary or infinite-time conclusion.
No clustering threshold was changed after seeing the spectrum.

The finite-window averages remain well-defined independently of that
comparator. The reported envelope bounds retain actual eigenvalues and
include a numerical within-cluster spread allowance. They are loose:
the matrix envelope is1.29465738, larger than the comparator's apparent
positive margins. They do not validate replacing the finite history by
the comparator. Its small symmetry residuals are likewise not used as
physical predictions. The running clock was never dephased.

## Verification and scientific consequence

Independent sparse Taylor propagation agrees with spectral propagation
to6.93e-15 at the tested age. The source derivative agrees with central
finite difference to1.66e-7 against the frozen2e-6 allowance; scalar
observable derivative errors are at most5.88e-10. The complete source
energy identity has matrix error4.50e-12. Rank, energy, symmetry,
Hermiticity and explicit contact checks pass. Existing internal reviewers
checked the algebra, source code and saved results without running another
numerical worker. This is internal review, not independent final synthesis.

The outcome advances the decision beyond the previous early-time sign:
late positive phase work does occur, but does not by itself provide the
common passive temporal/spatial response. Active network behavior is not
excluded. Next derive an operational signal/ruler response with the same
actual-state memory and complete source, and state exactly which clock
resolution and source family it predicts. Do not repeat this age scan,
repair it by a passive reset, or fit an arbitrary time-dependent source.
No astronomical density, force law, BTFR scale, absolute expansion stress,
lensing signal or CMB observable has been derived by this experiment.

## Evidence

All files are in this directory. Protocol and code were frozen before
execution; completed result and checkpoint are identical.

- NATIVE_DETUNED_JOINT_WORK_PROTOCOL_V001.md:
  adaa07698f920303718d0861316a32d128f4cbd0488efdc37c96ff2c547017dc
- native_detuned_joint_work_v001.py:
  6a788eea3bd0bfc879d704aa1be4974eeaf84167ea72e357556f067bb4c9138e
- NATIVE_DETUNED_JOINT_WORK_V001_RESULT.json:
  7279232452a626a9d5f983b236c2ec681110e0e863061541b260eaa768a381ec
- Parent BS_MICRO_ACTION.md:
  00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec
