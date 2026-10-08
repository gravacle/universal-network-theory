# A clock defined test of joint energy and phase work

2026-10-03 UTC. Frozen before output. One exact finite NODE experiment
tests the actual detuned state, its energy-to-phase response and a necessary
two-control passivity condition. No source profile is fitted. This is not
native graph formation, physical metric/ruler calibration, or a galaxy test.
It continues V118 rather than rerunning its failed resonant source model.

## State and complete energy

Use K3,3 on left vertices0,1,2 and right3,4,5; all nine cross edges exist.
Q=2 same-content carriers, the uniform fixed-Q mixture, actual blank records
and uniformly content-0 writers. Fragments and unused record content remain
inactive as in the invariant native branch. Coefficients are unchanged:
epsilon_psi=epsilon_r=U_d=d_star=g_w=g_p=1, Delta=4, t=1/2, j=1/4,
lambda_R=1/2, writer storage zero. Degree3 gives delta=-1/2 natively.

The bulk dimension is15*64=960. There is NO conserved-X-sector reduction
off resonance. Its complete allocated local energy is

    h_v=10I+(7/4)p_v-(1/4)sum_(u~v)p_v*p_u
           -(1/4)sum_(u~v)T_uv-(1/2)r_v+(1+p_v)X_v,
    H=sum_v h_v.

The graph baseline is60I and the initial mean energy is316/5. Each h_v
has mean158/15 at every unforced age by vertex symmetry and conservation.
These constants remain in switch work even if a scalar is centered for
matrix-action accuracy. The initial state is represented by its15 blank-
record columns A0, divided bysqrt(15); its autonomous rank stays15.

## Clock and fixed controls

Use the already supplied isolated reference clock with physical lapse1,
source perturbation0, phaseTheta=sqrt(5)*x and nonzero amplitude1/sqrt(5).
It is separate from the bulk eigensolve. Let A=2*pi/sqrt(5), one reference
clock period. Formation-age windows are [0,A] and [A,2A], with no choice
based on the observed signs. The source pulse duration isT=A/2.

For each actual bulk age a, turn on the complete local source alpha*F,
F=h0, for durationT and switch it OFF before the phase operation. Apply
the carrier phase U_lambda=exp(+i*lambda*P), P=p0. Both controls are
infinitesimal, with no new dynamical coefficient. The work includes source
on, source off and phase operation. Own prepared replicates or response
reconstruction if implementing this diagnostic; an average of readouts
does not reset or dephase a single trajectory.

Let I=i[H,P], D=[P,[H,P]]=t*sum_(u~0)T_0u. Source-on operators obey
I_alpha=(1+alpha/2)I, D_alpha=(1+alpha/2)D, so D'=D/2 is mandatory.
At fixed age, compute baseline endpoint kappa=<D(T)>_a and the source
derivatives R_OF=delta_alpha<O(T)> for O=D,I,F, retaining all records.
Report phase response both ON (R_DF+kappa/2) and OFF (R_DF).

Unforced symmetry gives <I>=0 and <F> constant, so first-order cyclic
work is zero in every actual age, not merely the diagonal comparator.
The complete small-control work is

    W=alpha^2 W_F2+alpha*lambda R_IF+lambda^2*kappa/2+O(3),
    W_F2=-R_FF,
    M=[[2 W_F2,R_IF],[R_IF,kappa]].

A negative eigenvalue of M is extractable work within these declared
controls. Positive M qualifies this quadratic pulse/kick family ONLY;
it does not prove general spectral passivity, an attractor or gravity.
The sign of R_DF alone is not a passivity condition. A phase kick while
the source is on has a contact which cancels against its additional
source-off work in the full closed cycle; report this boundary distinction.

## Actual ages and coarse comparisons

Compute actual-age rows at129 equally spaced ages over EACH clock period
(257 unique ages). These are a frozen interval census, not a favorable-age
selection. Also compute the EXACT uniform-age averages over both periods
using the spectral sinc factor. Do not average the running clock state:
the comparison is an average of age-tagged readouts with the same elapsed
clock phase; the isolated clock remains coherent on each trajectory.

The bulk diagonal ensemble is a comparison only. Retain whole numerically
degenerate energy blocks and report cluster widths and gap resolution. It
is independent of formation age and must not be interpreted as an actual
aged Gibbs state. Report finite-average minus comparator errors for every
retained response, and phase-curvature observable-weighted sinc-envelope
error. No small averaging error or physical stationarity is presumed.

Positive averages do not hide negative instantaneous rows. For scalar
matrix-entry histories m(a)=Tr[rho_a O], use the exact spectral second-
derivative bound B2=sum_ij |rho0_ij O_ji|*(E_i-E_j)^2. Linear interpolation
between adjacent ages of step h has entry error at most B2*h^2/8.
For the work matrix use its Frobenius entry-error bound as an operator-
norm error. A minimum sampled eigenvalue larger than that error+1e-8
certifies positivity throughout that window for this quadratic family.
A sampled eigenvalue below-1e-8 is a negative witness; otherwise label
the interval UNCERTIFIED. This is not a time-average stability inference.

If the frozen actual-age census has a negative work-matrix eigenvalue,
validate its most negative row/eigenvector using the SAME source pulse
and phase operation, with both signs of amplitude1/64,1/128,1/256.
These are finite-control checks of the predicted work direction, not
new fitted profiles or an age selected for a favorable result. Report
both exact work and quadratic prediction; do not require or manufacture
extraction if higher-order work changes the sign. Use absolute work
error1e-8 and report relative quadratic discrepancy without changing gates.

## Numerical controls and resource bounds

One installed-runtime NumPy worker, single threaded, dimension960 only.
Prospective soft limits are180seconds and512MiB peakRSS. Save a stage
checkpoint and stop safely if exceeded between stages; no parallel job,
new software or larger graph. No special source fit or tolerance changes.

Use Hermitian eigendecomposition and an analytic, degeneracy-safe sinc
Frechet derivative for the source pulse. Numerical control tolerance1e-9;
scalar result/sign guard1e-8. Group energies within1e-9 of each cluster
anchor only for the comparator; minimum intercluster gap must exceed1e-7
to call that comparator resolved. Near-degenerate coherences in finite
age averages are always retained with the actual eigenvalues.

Check H=sum h_v, Hermiticity, eigen residual/orthogonality, rank15 norm,
initial and conserved total energy, h0 and p0 symmetry, zero current,
D and D' commutators, exact contact relation, and source energy/work
identities. Independently check action at a=A and delayT by a centered
sparse Taylor propagator (no new eigensolve required), and source
derivatives by central difference with step2^-14 and tolerance2e-6.
Keep the source constant in the work even if centered for this check.

Store all scalar rows, average/comparator values, bounds, implementation
controls and evidence hashes. Do not store a speculative gravitational
parameter or adopt a passing microscopic result as observational support.
Any negative, unresolved or positive result has the same unchanged
Stage1-to-Stage3 obligations and evidence ceilings.
