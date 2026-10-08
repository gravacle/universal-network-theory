# A fixed source prediction test for the same content probe

2026-10-03 UTC. Prospective protocol, saved before numerical output. This
tests one necessary, restricted complete-energy representation of the V117
same-content mixed response. It is not a galaxy simulation, a physical
gravity law, a naturally formed graph, or a test of all emergent geometries.
The original preparations and earlier failed reductions remain unchanged.

## Frozen model and observables

Use the fixed-graph NODE reference on the six-cycle with edges
01,12,23,34,45,50. There are Q=2 content-0 carriers in its uniform fixed-Q
mixture, all records initially blank and all writers in content 0.
The separate isolated clock has physical lapse L_c=1 and perturbation
ell_c=0, so x=Theta/sqrt(5) is the common generator age. No full-parent
dynamic-incidence accuracy claim is made for this small graph.

Inherited coefficients are epsilon_psi=epsilon_r=U_d=d_star=g_w=g_p=1,
Delta=4, t=1/2, j=1/4, lambda_R=1/2 and writer storage energy zero.
At degree two the record detuning vanishes. For X-diagonal readouts, the
ACTUAL blank records give the exact equally weighted average of all 64
conserved record-X sectors zeta_v=+1 or -1. Each carrier sector has
dimension binom(6,2)=15. This is not an averaged record potential or a
replacement by lower record eigenstates.

In each sector the allocated local energy is

    h_v=(1+j*2)p_v-j sum_(u~v) p_v p_u
        -(t/2) sum_(u~v) T_uv+zeta_v(1+p_v)+5 I.

Here T_uv transfers a carrier in both directions, without fermionic signs.
The graph constant 5=U_d(2-d_star)^2+Delta*2/2 is retained. H=sum_v h_v
has hopping -t T and pair energy -2j p_u p_v per edge. Fixed graph constants
do not replace the separately dynamical incidence energy of the full parent.

Preparation pairs are A=(0,1), B=(3,4), with M_A=p0-p1 and M_B=p3-p4.
The state is exactly sigma_0(1+eta M_A)(1+xi M_B); mixed coefficients have
no factorial. Source calibration uses only the FIXED conjugate-energy
observable E=h0+h1, not L0*h0+L1*h1. The latter would require an additional
readout contact. Initial mixed energy is zero; control and entropy costs
are not claimed zero.

Reflection v -> 1-v mod 6 makes E even and both preparations odd.
Therefore b_A^E=0. The identity carrier block in each X sector implies
R_E=R_P=0 for fixed X-diagonal observables, but the mixed kernel K_E^B
need not vanish. First probe-induced source corrections multiply R and
are invisible at this order for these readouts, not assumed physically zero.

## Source family fixed before output

Consider a static complete source H+eta sum_v f_v h_v, replacing A while
retaining B. An odd profile has form f=(a,-a,b,c,-c,-b). Exact onset algebra
gives b_AB^E[x^2]=0 and K_E^B[f][x^2]=-(b+c)/120. An exact microscopic
correspondence on an interval reaching x=0 thus requires c=-b. This
analytical condition, not numerical fitting, restricts the source to

    f_A=(1,-1,0,0,0,0),
    f_D=(0,0,1,-1,1,-1),
    f=a*f_A+b*f_D.

No source family, coefficient in H, graph, filling or time window will be
changed after the outputs. Any future enlargement is a separate hypothesis.
The source is an infinitesimal response; finite positive lapse follows
only for sufficiently small eta. No physical acceleration scale is supplied.

Calibration rows: mixed E at x=0.5,1,1.5,2. Source-validation rows:
x=0.75,1.25,1.75. Fit the two coefficients by unweighted least squares
using calibration rows ONLY. Keep the displayed basis normalization.
Acceptance requires maximum absolute calibration AND validation residual
at most 1e-8 in the microscopic energy units. This is a numerical
correspondence criterion, not an observational error bar or whole-window
theorem. Rank cutoff is 1e-12+1e-9*s_max; effective condition number must
not exceed 1e8. Do not present a rank-deficient coefficient vector as unique.

Only after these gates pass, build withheld probe K rows: p3,p4 and the
real/imaginary transfer quadratures on 23,34,45 at x=0.25,0.5,...,2.25.
If the source matrix has a null space, its unit-normalized null vectors
must be annihilated by every probe row to absolute 1e-10 before native
probe targets are evaluated. This is a finite-precision identifiability
check, not exact uniqueness proof. Mixed density symmetry leaves only
one independent occupation history; do not count p3 and p4 independently.
Probe acceptance, if reached, also uses absolute 1e-8, with no refitting.
If source calibration fails, do not evaluate or score withheld targets.

## Computation and independent controls

One local, single-threaded small worker, using the installed NumPy runtime.
No installs, large graph, repeated grid, or other Mac. Evolve each 15 by 15
matrix by Hermitian eigendecomposition. Use the analytic divided-difference
Frechet derivative of exp(-i H x), including degenerate eigenvalues via
sinc, rather than time quadrature. Average all 64 sectors exactly.

Control tolerances: operator/eigen/trace/symmetry identities 1e-10;
central difference of U at x=1 with step 2^-17 versus the Frechet derivative
3e-7 absolute. Check H allocation, Hermiticity, unitary derivative, ordinary
source null, reflection, mixed tangent trace/norm (0 and 4/15), initial
mixed E, and the uniform-source clock identity. Include complete energy
conservation and explicit source work where applicable.

An independent exact-integer commutator calculation supplies Taylor
coefficients through x^8 for E and its three unrestricted odd source
directions. All h_v*4 entries are integers, so average first and store
reduced rational coefficients. These are exact finite-model witnesses,
not a floating-point small-time fit. Verify the x^2 identities above and
retain any independent inconsistency with a static source. Do not use
higher coefficients to modify the two-dimensional family or thresholds.

The result includes hashes of this protocol, code and the source derivation.
Preserve technical failures separately from scientific mismatches. Refuse
to overwrite a result. No framework, registry, release, or sealed evidence
is changed. Regardless of outcome, native formation, physical geometry,
shared galaxy/expansion predictions and all eleven open lanes remain due.
