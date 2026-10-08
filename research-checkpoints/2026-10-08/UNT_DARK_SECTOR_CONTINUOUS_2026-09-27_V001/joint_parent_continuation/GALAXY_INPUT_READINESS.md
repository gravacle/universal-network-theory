# Galaxy density-input readiness

2026-09-28. Read-only resident-file/source discovery. No field calculation,
fit, large archive, image cube or new numerical worker. The only new local
file is this note.

## Decision

Use **NGC 3198 as an explicitly exposed development case**, not a held-out
success test. A public electronic table provides actual stellar, atomic-gas
and molecular-gas surface-density profiles. It is sufficient to begin a
density-input preparation, but not yet a fully specified 44-kpc galaxy
calculation: the retrieved profiles stop at 15.1 kpc and require missing-gas,
outer-profile and vertical-geometry treatment before a physical AQUAL run.

This retains the already selected galaxy rather than choosing another after
viewing rotation-curve agreement. The resident audit has already exposed all
43 observed velocity rows and their residuals. This review also encountered
published kinematic descriptions while discovering sources; it is not blind.

## Resident inputs checked

Only these packet files were read:

- `../NGC3198_OBSERVATION_INFERENCE_AUDIT_V001.md`
- `../ngc3198_sparc_excerpt_v001.txt`
- `../ngc3198_inference_audit_v001.py` (not executed).

They retain 43 SPARC rows from 0.32 to 44.08 kpc, at nominal distance
13.8 Mpc. The excerpt contains stellar surface brightness and Newtonian
velocity contributions, but **no gas surface-density column**. Its original
audit already treats the data as exposed and retains signed gas forces.

## Exact public products and their roles

| Product | What it supplies | What it does not supply |
|---|---|---|
| [SPARC mass-model table](https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt) | R, Vobs, velocity error, Vgas/Vdisk/Vbul, SBdisk/SBbul | Gas density profile, resolved vertical density, full covariance |
| [SPARC main data page](https://astroweb.case.edu/SPARC/) | Links to photometric profiles and non-parametric decompositions, plus sample geometry | A complete observed 3D baryonic density in the mass-model table |
| [Leroy electronic catalogue ReadMe](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/AJ/136/2782?format=html&tex=true) | Exact schema for table2, table4 and table7; radial stellar/HI/H2 columns and uncertainties | A prescription for missing outer matter or 3D thickness |
| [Leroy table7.dat](https://cdsarc.cds.unistra.fr/ftp/J/AJ/136/2782/table7.dat) | Direct density-profile rows, including NGC 3198 | A full HI profile out to the SPARC endpoint |
| [Leroy table4.dat](https://cdsarc.cds.unistra.fr/ftp/J/AJ/136/2782/table4.dat) | Galaxy geometry and adopted global quantities | The unsmoothed observed velocity curve |

The CDS catalogue identifies table7 as 687 fixed-width records of 82
characters. A bounded, read-only network retrieval succeeded; only its
NGC 3198 rows were displayed. They comprise **23 rings from 0.3 to 15.1 kpc**.
HI and stellar densities are populated throughout. H2 is populated through
6.4 kpc; from 7.0 kpc outward those two fields are blank. Preserve blanks as
missing/unresolved, not measured zero. The original metadata/limit semantics
must be reconciled before numerical use. No original-byte input file/hash
was staged in this task.

SPARC's SBdisk/SBbul units are solar luminosities per square parsec;
stellar templates use M/L=1 and Vgas already includes helium 1.33. Its velocity
error does not include inclination systematics. The main page distinguishes
uncorrected sky photometry from inclination-corrected stellar profiles in the
mass-model product. These conventions must not be applied twice.
[SPARC schema](https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt)

For force reconstruction retain

    Vbar^2=Vgas|Vgas|+Upsilon_disk Vdisk|Vdisk|
                        +Upsilon_bulge Vbul|Vbul|.

A negative Vgas encodes an outward radial contribution from a nonnegative
gas distribution, not negative gas mass or density. In the density input,
add HI and H2 surface densities with a single declared helium convention;
do not add another 1.33 or 1.36 multiplier to these already corrected values.

## Geometry and physical nuisance conventions

[Leroy et al. (2008), tables 2–4 and appendices A/C/E](https://arxiv.org/pdf/0810.2556)
give NGC 3198 D=13.8 Mpc, inclination 72 degrees, PA=215 degrees and
r25=13.0 kpc. Its working resolution is 12 arcsec/about 800 pc; profiles
use 10-arcsec rings. Gas densities already include helium 1.36. Molecular
conversion assumes X_CO=2e20 cm^-2/(K km/s) and CO(2–1)/(1–0)=0.8.
Stellar densities use a K-band M/L of 0.5 through a calibrated 3.6-micron
intensity relation, **not** SPARC's 3.6-micron M/L=0.5. Quoted ring scatter
does not contain those conversion systematics.

The resident SPARC convention is inclination 73+/-3 degrees and distance
13.8+/-1.4 Mpc. Pick a consistent geometry and transform both imaging and
kinematics; do not splice two reductions as if they had identical conventions.
The Leroy table4 smooth rotation-fit parameters are not a substitute for
observed velocities or their errors.

The matching THINGS kinematic primary reference is
[de Blok et al. (2008), section 4.8, table 2 and figure 75](https://arxiv.org/pdf/0810.2100).
It uses radius-dependent tilted-ring geometry; its tabulated mean values
for NGC 3198 include inclination 71.5 degrees and PA 215.0 degrees at
D=13.8 Mpc. A directly downloadable original numerical THINGS curve was
not verified in this bounded discovery pass. For immediate development the
existing SPARC 43-row curve is therefore the verified numerical velocity
source, with its distinct reduction and geometry declared. A simple constant-
inclination sensitivity rescales V by sin(73deg)/sin(72deg), but this is not
a replacement for the original warped-ring deprojection or imaging update.

An axisymmetric source can be assembled as

    rho_b(R,z)=Sigma_star(R) p_star(z|R)
               +Sigma_HI(R) p_HI(z|R)+Sigma_H2(R) p_H2(z|R),
    integral p_j(z|R) dz=1.

Choosing p_j=delta(z) is an explicit thin-disk approximation. Finite thickness,
flaring/warps, central continuation, molecular upper limits, inclination,
distance, stellar normalization and gas conversion must remain named inputs.
Do not infer thickness from a Newtonian hydrostatic mass relation while
claiming it was an independently measured geometry for modified gravity.
The SPARC paper's exponential stellar height prescription is a possible
declared comparison, not a direct measurement.
[SPARC mass-model method, section 3.3](https://arxiv.org/pdf/1606.09251)

## Why velocity-component tables cannot close the density input

This is a mathematical information issue, not a criticism of those useful
Newtonian templates. At m sampled radii each component supplies m linear
functionals L_i[rho]=R_i partial_R Phi_N(R_i,0)=V_i|V_i|. Choose m+1 smooth
annular density perturbations. The m by (m+1) matrix of their L_i values has
a nontrivial null vector, yielding a nonzero density perturbation invisible
to all m samples. On support where a baseline density is positive, a small
enough multiple preserves positivity. Extra finite brightness constraints
can be included by adding more independent basis functions. Unknown vertical
profiles increase this freedom.

Therefore finite, noisy, truncated component curves cannot uniquely fix the
source for a new nonlinear 3D field equation. A regularized inversion would
add density/boundary priors, not recover missing measurements. This does not
deny special inversion theorems for a complete exact curve under fixed thin-
disk geometry; those stronger inputs are absent here. In particular,
M(<R)=RV^2/G is a spherical inversion and is not a disk-density reconstruction.

Nor may the Newtonian component velocities be fed separately through the
mechanical response and added: the nonlinear equation must act on the total
source, with its spatial solution computed before extracting radial motion.

## Smallest useful next preparation

1. Stage and hash the original table7/ReadMe plus the selected geometry row;
   retain missing/limit fields and units, with no selected-row deletion.
2. Recover or explicitly bound the outer HI profile beyond 15.1 kpc and its
   central continuation. Disk outer mass influences inner forces too, so
   merely restricting scored radii does not eliminate the tail obligation.
3. Freeze a declared thin-disk first comparison, nuisance choices and tail
   alternatives from baryonic information, before any agreement scoring.
4. Reproduce the corresponding Newtonian field from that SAME density as an
   input/geometry check; then solve the mechanical AQUAL equation. Use the
   exact Kuzmin benchmark to qualify the solver first.

The public profile route is real and small; obtaining it does not require
copying a telescope cube or a repository. An explicit truncated-profile
experiment could run sooner, but would be a controlled modeled-galaxy test,
not a data-complete explanation of NGC 3198's extended rotation curve.

## Additive raw-table reconciliation

The parent subsequently staged the original small files in this directory.
Read-only byte hashes on 2026-09-28:

| File | SHA-256 |
|---|---|
| `leroy2008_table7.dat` | `43165045c50d534ff7789dda05627328c23ba71c708ded9cf87cf0773fe02d99` |
| `leroy2008_table4.dat` | `938104d0289f93f9fed0843028555e92f63a61889d623ee5b5f132e9d6ea1f44` |
| `leroy2008_ReadMe.html` | `cbd9a431c5ef4d9ae1bcda8bc141210bd03360a4d2b0ea5d8dd40e9079763c48` |

Direct inspection finds 687 rows: 622 have 82 characters, and 65 have only
68 because their final blank columns are omitted. Fixed-width parsing should
right-pad to 82 and retain blanks, not split on whitespace. The documented
HI/star field positions correctly recover NGC 3198's populated values.

The CDS note saying `1.0 = upper limit` cannot be applied to every numeric
error equal to one. The original printed example explicitly gives NGC 628
at 0.9 kpc as stellar density 313.6 with RMS 1.0, and at 5.1/5.5 kpc as HI
8.2/8.5 with RMS 1.0. These match the raw bytes. Thus NGC 3198's populated
stellar density 105.0 and RMS 1.0 at 1.7 kpc is not a limit flag. In contrast,
raw HI limits have blank density and 1.0 in the error slot. Blank/blank H2
still needs contextual treatment; the printed NGC 628 H2 upper limits
become blank/blank in the electronic file, while galaxies without CO also
have blank/blank. Do not invent a universal zero or limit from that encoding.
[Original profile example and conventions, Appendix E](https://arxiv.org/pdf/0810.2556)

The same paper's section 3.3 specifies that table4 masses integrate to
1.5 r25, not infinity. For NGC 3198 this is 19.5 kpc, beyond the 15.1-kpc
profile endpoint. The tabulated log masses 10.1 (stars), 10.1 (HI), and 8.8
(H2) can constrain the total within that aperture, with rounding and the
stated tracer conversions; they do not determine where the missing annular
mass lies or constrain all material beyond 19.5 kpc. The gas conventions
already include helium. Do not multiply it in again.
[Integrated-property definition, section 3.3](https://arxiv.org/pdf/0810.2556)
