# NGC 3198: the measured motion and the inferred missing response

2026-09-27. Exploratory reference-inference audit, not a UNT prediction,
halo fit, observational significance calculation, or A0/A2/B0/F4 pass.
This galaxy and these outputs are now exposed development material, not
held-out validation data. No UNT equation was adjusted to match them.

## Source and scope

The primary [SPARC mass-model table](https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt)
supplies all 43 NGC3198 rows. Their numerical columns are transcribed in
`ngc3198_sparc_excerpt_v001.txt`; this is not an original-byte download.
Local excerpt SHA256:
`58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900`.

The [sample catalogue](https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt)
gives D = 13.8 +/- 1.4 Mpc (Cepheid method), inclination 73 +/- 3 degrees,
quality flag 1 and rotation-source references Da06, Be91, Be87. These are
catalogue inputs, not newly estimated uncertainties. Underlying images and
velocity cubes have not been re-reduced. The tabulated circular speeds
already involve kinematic modeling and deprojection; they are not raw
spectral pixels.

The [SPARC paper, section 3.3 and equation 2](https://arxiv.org/pdf/1606.09251)
defines the component calculation. Gas includes helium already; signed
component squares retain outward central forces. Stellar templates have
mass-to-light ratio one. We adopt 0.5 for illustration, not as a measurement
or an inferred UNT constant. Disk geometry and nonuniform measured profiles
are already in these templates. Their ordinary-matter modeling, including
molecular-gas treatment, remains an assumption to audit in a scored analysis.

## Exactly what the arithmetic does

Use the radial inward acceleration convention and the same circular-orbit
interpretation as the table. Write S(v) = v |v|. Then

    V_bar^2 = S(V_gas) + Upsilon_disk S(V_disk)
                         + Upsilon_bulge S(V_bulge),
    g_bar = V_bar^2/R,      g_obs = V_obs^2/R,
    Delta g = (V_obs^2 - V_bar^2)/R,
    response_ratio = g_obs/g_bar = V_obs^2/V_bar^2.

Here V_bulge is zero throughout this galaxy's table. The calculation never
uses a spherical enclosed-mass formula for the disk and does not fit a
dark halo. A positive residual is the extra inward response needed under
these inputs; interpreting it as additional mass also assumes a gravity
law and mass geometry. It is not a direct detection or inventory of particles.

The three display rows are nearest to radii 10, 20, 40 kpc; this display
rule was written before the arithmetic run. All 43 rows were evaluated.
This rule does not make the already public galaxy a blind or representative
population test. The galaxy was chosen as a familiar extended-rotation
example, not sampled randomly from SPARC.

| R (kpc) | Published V_obs (km/s) | Calculated V_bar at Upsilon=0.5 (km/s) | g_obs/g_bar |
| --- | --- | --- | --- |
| 10.04 | 152 | 93.624502 | 2.635774 |
| 20.05 | 154 | 78.948774 | 3.804965 |
| 40.10 | 150 | 66.003509 | 5.164740 |

For example the last row is simply

    V_bar^2 = 47.48^2 + 0.5 * 64.84^2 = 4356.4632 (km/s)^2,
    V_obs^2 = 22500 (km/s)^2,
    V_obs^2 - V_bar^2 = 18143.5368 (km/s)^2.

Thus the velocity shortfall is only a factor about 2.27, while the required
acceleration is about 5.16 times the calculated ordinary-matter contribution.
This is how a large dynamical discrepancy arises without assuming uniform
matter. It does not give the cosmic dark fraction or the galaxy's integrated
dark mass fraction.

## Nuisance inputs are not optional

The same display rows, with only the illustrative stellar normalization
changed, give these response ratios:

| R (kpc) | Upsilon=0.2 | Upsilon=0.5 | Upsilon=0.7 | Upsilon=1.0 |
| --- | --- | --- | --- | --- |
| 10.04 | 6.012495 | 2.635774 | 1.917747 | 1.361433 |
| 20.05 | 6.884138 | 3.804965 | 2.930977 | 2.179902 |
| 40.10 | 7.269331 | 5.164740 | 4.329164 | 3.483740 |

This is sensitivity arithmetic, not a prior, confidence interval, or proof
that all possible baryonic models fail. The whole-disk template multiplier
that would remove the residual at each single radius is respectively
1.373784, 2.381326, 4.815548. They cannot all be one multiplier at these
nominal inputs. They are NOT a local Upsilon(R) profile: changing stellar
mass at one radius changes gravity elsewhere and requires recomputing the
disk potential. They must not be supplied to UNT as fitted record profiles.

At fixed inclination and angular shapes, a uniform distance rescaling
D -> sD makes R -> sR and each baryonic squared-speed template -> s V^2.
Consequently g_bar is unchanged at corresponding angular positions,
g_obs -> g_obs/s and the ratio -> ratio/s. This is an exact scaling of that
reference template prescription, not a full distance/photometry likelihood.
Inclination changes also affect velocities and the reduction: the kinematic
factor is sin(i_old)/sin(i_new), but a consistent treatment must reconsider
deprojection/warps and photometry, not just multiply every output independently.

The published velocity error excludes inclination systematics. No covariance,
full baryonic uncertainty, distance prior, or significance is calculated here.
The baseline actually has NEGATIVE residuals at R = 0.32, 0.64, 0.96 kpc;
these are retained, not clipped or silently dropped. The corresponding
published velocity errors are large. No claim that every radius requires
positive additional attraction follows from this simple baseline.

## The useful UNT target

Predict the motion from the ordinary-matter information and independently
defined network state/dynamics. A response ratio is a diagnostic, not an
acceleration-dependent constitutive function measured without assumptions.
For a disk, even a local nonlinear gravity equation generally requires a
field solution; setting mu(R)=g_bar/g_obs at each point is not that solution.

A shared dark-sector explanation must derive its spatial response and its
homogeneous stress/evolution from the same network law. Neither a fitted
halo template nor an arbitrary time-dependent background term is an earned
network mechanism. This audit locates the galaxy-side quantity to explain;
it does not yet supply the missing UNT matter/probe and gravitational map.

## Reproduction and execution record

`ngc3198_inference_audit_v001.py` is a read-only standard-library program.
It bounds input to 16 KiB/100 rows and CPU time to five seconds, uses exact
rational intermediate arithmetic, retains signed gas contributions and
checks reconstruction identities. It creates no files or child processes.

Executed once on the originating machine:

    /usr/bin/python3 -B UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/ngc3198_inference_audit_v001.py

Exit code 0. This was small table arithmetic, not a physics simulation, production retry, sweep,
statistical fit, or remote job. Its complete row results are reproducible
from the saved input and code; the tables above record the display outputs.
No packages, external settings or historical files were changed.

Independent review compared all 43 rows and all retained numeric columns
against the primary table, confirmed the signed-square/helium conventions,
and checked the three display calculations by hand. No discrepancy found.
This is independent arithmetic/source review, not independent observational
evidence or a replay of the original astronomical data reduction.
