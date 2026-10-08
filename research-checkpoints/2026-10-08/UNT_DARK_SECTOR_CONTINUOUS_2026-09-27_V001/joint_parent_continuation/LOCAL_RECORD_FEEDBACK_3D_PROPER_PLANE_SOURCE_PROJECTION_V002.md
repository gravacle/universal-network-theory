# Proper-plane source projection on the existing L3 support V002

Prospective saved-data calculation; V0017a5cd43... remains as a reviewed draft. It contracts every measured mode on a fixed
tetrahedral proper chart. It introduces no new sampler, field solve, empirical
eigenbasis, proper spacing calibration, environment contrast or metric adoption.
The two beta4 conditions are different M discretizations of ONE environment.

Use proper bond length ell and port normals u0=(1,1,1)/sqrt3,
u1=(1,-1,-1)/sqrt3, u2=(-1,1,-1)/sqrt3, u3=(-1,-1,1)/sqrt3.
Set B=(u1-u0,u2-u0,u3-u0), A_r=ell B r and B_r=A_r+ell u0.
Then every supplied A_r -> B_(r+s_a) has physical displacement ell u_a.
The signed determinant is -16/(3sqrt3); primitive volume is its absolute value.
The chart is a disclosed undistorted support hypothesis, not measured geometry.

For each of the seven supplied cell modes k, define Kell=2pi B^-T k/3.
Then Kell dot u0=-pi sum(k)/6 and
|Kell|^2=pi^2[sum(k_i^2)-sum(k_i)^2/4]/3.
The six nonzero resident modes have |Kell|=pi/2 and proper wavelength4ell.
They are microscopic proper-plane probes; no long-wavelength/continuum window
is thereby qualified. The k0 mode remains the uniform control.

The normalized physical node Fourier source is
E_phys(k)=[E_A(k)+a_k E_B(k)]/sqrt2, a_k=exp(+i pi sum(k)/6).
Here E_A/B already have the saved cell normalization1/sqrt27.
Let c_k=(1,a_k)/sqrt2 and T_k=diag(1 six times,a_k six times,1,a_k),
which carries the twelve pair and two coordination primitives to their physical
sublattice phases. Qhat=T Q retains EACH sublattice channel's per-cell1/sqrt27
normalization; the mixed block below is Qhat-versus-per-node-Ephys. It is not
a fourteen-channel per-node-density block. Also report Qtilde=T Q/sqrt2,
with mixed block chi_QtildeE=chi_QhatE/sqrt2 and
chi_QtildeQtilde=T chi_QQ T^dagger/2. Neither Qhat nor Qtilde is identified
as memory geometry. Real cos/sin planes use sqrt2 times the complex plane's
real/imaginary parts; all six nonzero signed modes remain.
Compute R_phys=c R_NN c^dagger, chi_Ephys= c chi_EE c^dagger,
C2_phys=c C2 c^dagger, chi_QEphys=T chi_QE c^dagger, and
chi_EQphys=c chi_EQ T^dagger. Mandatory finite-M contact remains:
R_phys=-chi_Ephys-C2_phys/beta. No response inverse is taken.
The zero sampled constant c0=AR+Sself is restored symbolically as
E_phys_full(0)=E_phys_dynamic(0)+sqrt54 c0; connected responses do not change.
Nonzero finite-chain energy means are retained as fluctuations, never body loads.

Use all128 pooled32-sweep block raw moments per condition. Reconstruct native
central R/chi/QE/contact from those moments and compare the full saved estimates
at unchanged3e-11*max(1,Frobenius_reference) criteria. Contract the central and
each direct leave-one-block-out reconstruction; give correlated real/imag
jackknife standard errors, not quadrature of marginal component errors.
Retain all14 signed mode/channel projections per reported scalar and all14
mixed channels. Compare all +/- conjugate partners, k0 scalar density guard,
source-contact identity, mixed reciprocity and chart/incidence/volume controls.
All signs are reported; a negative or positive result is not an arithmetic fail.
Cross-M differences retain both signs and combine only the independently sampled
conditions' errors. They are discretization comparisons, not environmental evidence.

For a DECLARED continuum common-chart Galerkin dictionary only, take the
complex normalized plane f=exp(i Kx)/sqrt54 over the periodic27-cell domain.
Its dimensionless gradient integral is Sbar=(|det B|/2)|Kell|^2.
This is an analytical chart integral, not a measured gravitational stiffness.
A two-potential common-field solve still needs matched retained/reduced action,
actual normalized body source and spatial/mixed source contacts. No raw R_phys
is added to calibrated total G without that reference/action prescription.

Root alone executes the exclusive new source/output paths after review and
ownership verification. Original source/results/checkpoints/failures stay sealed.

Frozen inputs (relative to this directory):

- local_record_feedback_3d_local_energy_source_response_v001.py: cc10b0836b9105192e210a5e17d877044fa2a64fa0ba826863bebcb521924167
- LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001.md: ed426216edd6788537c3149d0a85c5d26d670ac1d7279a085bdf387435059f58
- LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_RESULT.json: 389df141d19e496c5989d114b67025605f248c4b1aad80f145400e2395a5cfca
- LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001_RECEIPT.json: 7e67d3ce3c2f9f4cb8f76d6f3f69dfad1427dd550a2e99339067051292148e33
- LOCAL_PROPER_BOND_NORMALIZATION_V001.md: 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b
- LOCAL_RECORD_FEEDBACK_COMMON_METRIC_SOURCE_RESIDUAL_V001.md: 665545ea6e674105e77b5977eecf9fd37287f19d7f1b273be8116867d2fc4bad

Preserved prospective draft SHA256: 7a5cd43ab9e7ae896fd7a3e83a988564a6a2fab00741411f362fb734fcf2ecfe.
