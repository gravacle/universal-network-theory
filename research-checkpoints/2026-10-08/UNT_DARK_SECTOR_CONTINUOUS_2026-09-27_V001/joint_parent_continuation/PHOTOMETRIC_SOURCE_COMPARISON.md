# Stellar-source consistency and exact distance scaling

This is an exploratory, source-only audit after the first coarse fixed-source
galaxy result was visible. It computes no force, chooses no best-fitting mass
or distance, and changes none of the four frozen galaxy models. The complete
radial arithmetic and input/source hashes are in
`PHOTOMETRIC_SOURCE_COMPARISON.json`; the executable source-only calculation
is `photometric_source_comparison.py`.

## 1. The two nominal 0.5 mass-to-light choices are different

Leroy's Appendix C converts its median 3.6-micron profiles through the
empirical intensity ratio `I3.6=0.55 IK` and K-band mass-to-light ratio 0.5.
The resulting published equation C1 is

`Sigma_Leroy = 280 cos(i) I3.6`,

with mass surface density in solar masses/pc² and intensity in MJy/sr.
These are not direct stellar mass measurements independent of population
and photometric assumptions. [Leroy et al. 2008, Appendix C](https://arxiv.org/pdf/0810.2556)

SPARC instead uses solar absolute magnitude `M_sun,3.6=3.24`; its mass-model
surface-brightness columns are luminosity densities, and the 0.5 adopted in
the prior reference diagnostic is in solar 3.6-micron units. Its published
stellar force uses a finite-thickness stellar disk, not the razor-thin disk
used for the current explicitly declared field calculation.
[SPARC paper, sections 3 and 5](https://arxiv.org/pdf/1606.09251)

The IRAC channel-1 Vega zero-point is `F0=280.9 Jy`.
[IRAC Instrument Handbook, Table 4.2](https://irsa.ipac.caltech.edu/data/SPITZER/docs/irac/iracinstrumenthandbook/14/)
At 10 pc, one solar luminosity supplies flux `F0*10^(-0.4 M_sun)`;
one pc² subtends 1/100 steradian in the small-angle limit. Therefore

`C3.6 = 10^4 * 10^(0.4 M_sun,3.6) / F0
       = 703.7983766863 L_sun,3.6 pc^-2 /(MJy sr^-1)`.

This gives, for identical intensity and inclination,

- SPARC's chosen 0.5: `Sigma = 351.8991883432 cos(i) I3.6`;
- Leroy's effective 3.6-micron M/L: `280/C3.6 = 0.3978412132`;
- the fixed mass-conversion ratio: `351.8991883432/280 = 1.2567828155`.

Thus a 25.68% normalization difference exists before any gravity law is
used. It is not legitimate to equate the two 0.5 labels or silently combine
the SPARC stellar force with the Leroy density. The conversion above is
an exact arithmetic comparison of the specified published conventions,
not an assertion that the two underlying reduced images are identical.

## 2. The saved radial profiles largely, but not exactly, reflect this

Both resident inputs adopt distance 13.8 Mpc. Interpolate only the existing
SPARC `0.5*SBdisk` values linearly to the Leroy radii; use no extrapolation,
velocity, optimized normalization, or fitted radius. All 22 comparable
Leroy rows are retained in the JSON. The 0.3 kpc row is excluded because the
SPARC excerpt begins at 0.32 kpc.

| R (kpc) | Leroy Sigma | SPARC 0.5 Sigma | ratio | ratio / 1.25678 |
|---:|---:|---:|---:|---:|
| 1.0 | 164.2 | 200.38 | 1.2204 | 0.9710 |
| 3.0 | 77.2 | 101.54 | 1.3153 | 1.0466 |
| 3.7 | 71.8 | 101.04 | 1.4072 | 1.1197 |
| 5.0 | 54.2 | 71.97 | 1.3279 | 1.0566 |
| 6.4 | 34.8 | 43.93 | 1.2623 | 1.0044 |
| 7.7 | 21.4 | 23.31 | 1.0891 | 0.8666 |
| 10.4 | 10.3 | 12.31 | 1.1950 | 0.9508 |
| 15.1 | 2.5 | 2.31 | 0.9233 | 0.7346 |

Surface densities are solar masses/pc². Exact annular integration of these
piecewise-linear profiles gives:

| Common annulus (kpc) | Leroy mass (solar) | SPARC 0.5 mass (solar) | ratio | ratio / 1.25678 |
|---:|---:|---:|---:|---:|
| 0.32–15.1 | 1.467211914e10 | 1.792803740e10 | 1.22191 | 0.97225 |
| 2–15.1 | 1.269272023e10 | 1.571354234e10 | 1.23800 | 0.98505 |
| 3–8 | 7.427846133e9 | 9.546097868e9 | 1.28518 | 1.02259 |
| 8–15.1 | 3.960815747e9 | 4.491700679e9 | 1.13403 | 0.90233 |

The inner 3–8 kpc **annular mass** difference is 28.52%; after accounting
for the independently published conversion difference it is only 2.26%.
This identifies a specific substantial part of the source-normalization
discrepancy. It does not remove local profile differences: the corrected
point ratios at the Leroy radii in that interval span 0.844–1.120.

The published geometries and reductions are not identical. Leroy uses
72 degrees inclination, while the resident SPARC catalogue convention is
73 degrees (with quoted uncertainty 3 degrees). For identical uncorrected
light a hypothetical inclination change alone contributes
`cos(73)/cos(72)=0.9461347112`; it has **not** been applied to either saved
profile. Radial averaging, masking, sky subtraction and profile extraction
also differ. This comparison therefore cannot uniquely assign every
remaining discrepancy to mass-to-light calibration.

The current Leroy profile is internally used with its own density, annular
mass, boundary mass and force calculation. Its separately documented
profile-versus-rounded-aperture-mass mismatch remains unresolved; no
renormalization to that rounded total has been made. Nor should the
SPARC profile be adopted solely because it might move an inner residual
in a favorable direction. A same-law comparison must preserve both
specified source reconstructions, their endpoint/height choices, and
their original outcomes.

## 3. Distance cannot independently repair a radial residual shape

For the adopted source-free-environment AQUAL equation

`div[mu(|grad Phi|/a0) grad Phi] = 4*pi*G*rho`,

let every physical source length follow distance, with fixed angular
surface-brightness profile, mass-to-light conversion, inclination and
`a0`. Write `d=D/D0`, and transform the entire boundary problem consistently:

`rho_D(x)=rho_0(x/d)/d`,
`Phi_D(x)=d*Phi_0(x/d) + constant`,
`grad Phi_D(x)=grad Phi_0(x/d)`.

The differential operator acquires exactly the required `1/d`; its
dimensionless `mu` argument does not change. Thus this is an exact scaling
identity for the stipulated family, not a spherical approximation. A thin
disk obeys `Sigma_D(R)=Sigma_0(R/d)` and `M_D=d² M_0`; if thickness is
retained, it too must scale with D. At fixed observed angular radius,

`v_D(theta)=sqrt(d)*v_0(theta)`.

Distance alone changes the overall speed amplitude, not the relative
radial shape. This statement does not cover a change in which some
physical scale, imposed boundary, external environment or `a0` is held
inconsistently fixed. It also does not treat inclination changes, warps,
or a new stellar radial profile as distance rescaling.

For reference, a later explicitly post-hoc amplitude diagnostic with fixed
nonnegative weights would have
`a_hat = sum(w*v_obs*v_pred)/sum(w*v_pred²)` and `D_hat=D0*a_hat²`.
No such fit has been run here; a claimed independent prediction must not
quietly incorporate this use of the observed velocities.

## 4. Consequence for the active calculation

The running fixed-source four-case study must finish with its original
inputs and numerical qualification. The calibration result above gives
a concrete source-consistency experiment once those outputs qualify,
without modifying the gravitational constitutive law. It does **not**
yet show that a different stellar conversion fixes the measured rotation
curve. In particular, raising the total mass is not automatically a remedy
for an outer overprediction, and a local density ratio is not a velocity
ratio in a nonlocal nonlinear disk problem.

The most informative next comparison is therefore one explicitly declared
stellar-input substitution or calibration comparison at unchanged law,
distance and gas model, with full radial outcomes retained—not a search
over several coupled choices until one curve agrees. This audit provides
no new observational success or rejection of UNT and no new native
derivation of the adopted gravity interface.
