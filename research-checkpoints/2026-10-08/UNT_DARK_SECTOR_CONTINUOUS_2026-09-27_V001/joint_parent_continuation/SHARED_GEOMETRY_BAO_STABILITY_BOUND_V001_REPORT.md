# Radial BAO tests the healthy shared-action branch without LCDM q0

2026-10-04. The fixed endpoint diagnostic is complete. Within the declared
flat, conserved-source, common-metric/ruler and regular-principal-window
assumptions, the healthy constant-trace/shear family cannot reproduce the
released radial BAO ratio for the tested ordinary-density/H0 benchmarks.
This is stronger than failure at a q0 imported from LCDM. It is not an
all-UNT exclusion or a claim that the BAO reduction is assumption-free.

The measured central endpoint ratio H(2.33)/H(.51)=2.53291214385. Necessary
positive scalar kinetic sign on the increasing branch implies

    Delta H^2 < 100^2 [omega_b Delta(1+z)^3+omega_r Delta(1+z)^4].

If that branch extends to z=0, the most permissive DECLARED density case
(omega_b=.02235, omega_r=4.18e-5) gives:

| H0 benchmark (km/s/Mpc) | Allowed maximum H2/H1 | Lower bound on full Gaussian BAO Q |
| --- | ---: | ---: |
| 60 | 1.75852648 | 207.3093 |
| 70 | 1.59288568 | 313.7350 |
| 73.6 | 1.54614882 | 348.1939 |
| 80 | 1.47546049 | 404.0989 |

The decreasing branch instead requires H2/H1<=1 and gives Q>=901.7641.
These are distances to a necessary linear half-space in the original BAO
Y=D_H/r_d vector, with the released covariance. They minimize over all
thirteen predicted coordinates; omitted transverse predictions are NOT fixed.
Thus they are genuine necessary lower bounds, not fitted curve mismatches.
No bound from another pair is summed into these numbers, and no significance
or posterior probability is assigned. All fifteen pairs, both omega_b cases,
both radiation cases and all four H0 benchmarks are retained.

Inverting the central endpoint ratio in the same density case gives H0<=
37.29496 km/s/Mpc, or a necessary r_d>=367.6731 Mpc. These are transformed
CENTRAL values, not confidence limits. At H0=70, the central minimum
ordinary dust density would be omega_b=.0791069, not the supplied .02235.
Changing the physical baryon inventory or thermal/ruler interpretation is a
different premise and must be checked against its other observations.

The H0 inequality specifically requires an increasing regular branch on
[0,2.33]; positive H alone is insufficient. Singular branch transitions,
degenerate constraints, frequency-dependent completions or breakdown of the
principal action are not certified by this reduction. Curved geometry or a
different operational clock/ruler model changes the equations and is not
silently ruled out. The BBN baryon values are conditional inputs; the H0
values are sensitivity benchmarks, not fitted or newly adopted priors.
Survey template and distance-reduction assumptions remain explicit.
[Primary data release](https://arxiv.org/html/2503.14738v3).

## Review and consequence

All 520 fixed controls passed in .0112 seconds. Independent review reproduced
all 255 half-space calculations, all transformed quantities, the input
hashes and row ordering. Full-13 Cholesky projection and analytic bounds
agree within 1.1e-14 scaled. The original q0 reference is not used anywhere
in this calculation; neither is a fitted acoustic ruler or DE density.

Receipt SHARED_GEOMETRY_BAO_STABILITY_BOUND_V001_RESULT.json SHA256:
e9d27a262efbc2e26ae92ca7cf7d0bcf44682dd3b12a42767f0161320a3948f4

Do not reopen r/eta/constant-shear fitting on this flat branch. Constructive
continuation must change a named physical premise. In particular spatial
curvature contributes to the background derivative and must be derived before
extending this exclusion to open geometry. The separate K(X) dynamics and
native formation obligations remain, with their earlier failures preserved.

An independent source-only examination also found that a simple two-region
common-clock example a_D^3=A t^2+B t^3 (dust walls plus coasting voids) gives
q_D=2/(2+3Bt/A)^2>0. Volume averaging alone does not accelerate this example.
It is not an exact matched spacetime or a ray prediction. A physical observer
map gamma=dt/dtau, b=a_D/gamma would give H_obs=gamma H_D-gamma_dot; specifying
gamma arbitrarily would add a free function, not establish native expansion.
No LTB integration or new wall/void fit has been launched without an owned
initial profile and photon-observer map.
