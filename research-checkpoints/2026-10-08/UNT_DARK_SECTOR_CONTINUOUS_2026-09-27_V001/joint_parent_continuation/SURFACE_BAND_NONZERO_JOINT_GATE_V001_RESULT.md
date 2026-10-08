# Nonzero held-source roots exist; material relaxation and formation remain separate

2026-10-05 UTC. SAME complete surface-band action and fixed coefficient
example as the frozen prospective protocol. Root and an independent reviewer
approved the final source before execution. Arithmetic: 814/814 checks passed.
The sealed source-zero anisotropic failure is preserved, unchanged.

All five nonzero held-shape roots have positive source Hessians and lower
energy than b=0 at the SAME shape. They remain above the fixed isotropic
reference energy. Field-relaxed material curvature in the declared log-strain
chart is positive through epsilon=.3 but has negative tracefree directions
at epsilon=.5. Every anisotropic row has nonzero material support gradients,
and every row has a positive true-volume support gradient. No unforced
static affine material minimum or formed physical phase is established.
These static conclusions are not an exclusion of cosmological expansion.

## Complete action, units and frozen example

The complete energy is retained without subtraction:

    E=R+Sigma<|cof(F)n|>-B<r+x^2/(r+x)>+V|b|^2/(8piG),
    a=sqrt(u^T(E_t^T F^T F E_t)^-1u),
    x=(d0/Lambda0)|F^T b|, r=sqrt(a^2+x^2), V=V0 det(F).

Critical A_ref=1 and B=V0 C0 Lambda0^3/3 fix
4piG=V0/[3B(d0/Lambda0)^2]. Thus field energy is not independently
normalized. The prospectively chosen arithmetic units B=V0=d0/Lambda0=1
give field coefficient (3/2)det(F)|b|^2. Sigma=8 and R=1 were fixed before
outcomes. They are a constitutive example, not an observational calibration.

The isotropic reference has E=8, h=7/3, G=31/15 and M=8/15, satisfying the
earlier frozen-material gates with speed squares 31/35 and 8/35. That formal
example does not qualify the quantum/clock/gravity kinetic action or remove
the independently counted tension amplitude and native matching premises.

## Execution, checkpoints and independent saved-only review

One local NumPy worker executed the frozen source. PID 24267, PPID 11865,
exec session 94047, exit 0. Recorded start was
2026-10-05T11:36:30.380482+00:00. Runtime including initialization was
27.24990179098677 seconds. Peak RSS was 181,125,120 bytes, approximately
172.73 MiB, below 512 MiB. All four specified BLAS/thread variables were 1
before NumPy import; PYTHONDONTWRITEBYTECODE was 1. NumPy version: 2.3.5.

Before computation the worker created the exclusive owned checkpoint
directory, sealed its PID/input manifest and began its journal. Each of the
six rows sealed its complete state/check JSON before the next row started.
Row times were approximately 3.79,4.62,4.70,4.68,4.66,4.61 seconds.
The journal ends with the final receipt seal. There is no error record,
failed attempt, repaired gate, replay, resume or repeat. No worker remains
active on behalf of observer_cosmography.

Independent saved-only review verified the source/protocol/input custody,
receipt canonical seal, manifest and all six state seals against the journal,
814/814 checks, declared thread environment and resource cap. It agrees with
the held-source, Schur, energy and support-gradient interpretation. The
immutable receipt retains its prospective pending-root-review status; this
report records the completed independent saved-only review separately.

SHA-256 custody:

| Artifact | SHA-256 |
|---|---|
| Frozen protocol | a922c3ecce723242cf086f71cf33e62e6e69be4145185a5395c8e2b3f12fb513 |
| Frozen worker | 9e77df5009f0f7e61139f3b82b1b21c64c2df13b6f129ad3f99efec5aa756926 |
| Raw final JSON receipt | 36b153bf959fa9054629232de753a782998aaf3223cb69bef8d82988960e00c6 |
| Canonical final payload | 542d00e660c46e0be61d79ee3e0f7b464a017462dbd042e5b39aad4b8497907a |
| Unchanged prior source-zero failure receipt | 2ecf65f2ca2402372a535931cac307e9ea1df356cde0e59f38b859079f0f7bf3 |
| Checkpoint manifest, raw | d573f76fa19fb9ed786374824feb643b9cac96298e3ee6628e50e8bb5c7de953 |
| Completed journal | 7675e8a890f421d18105226ccfc04d445b22bd3e52230a2ea636bb234f785763 |

All four anchored input hashes still match the final receipt. Canonical
hashes exclude only their own hash field and were independently recomputed
from sorted compact JSON. Completed per-state raw seals are:

| State | epsilon | Raw SHA-256 |
|---|---:|---|
| state_000.json | 0 | ab5004cd9a2b07550f125efa8e7b51677f33b0554b246958bf71808b5e6c4619 |
| state_001.json | .005 | e6de4a022f494cb34e3ddabe17e2f44b1a247c019db08eb289bbf7bb48c0f70a |
| state_002.json | .02 | 52681953d4555f65682f2e8635d64eda7f13aaf2fa0422ea768291703ca00fc6 |
| state_003.json | .1 | eee6b00f4c20c72a2b718ea119af45075b150362ee3e490516c687632f3cb1da |
| state_004.json | .3 | b89900d89928903d04bed721ad08506a5398200097b1933d1a3235a971447ee7 |
| state_005.json | .5 | 69b5567a13d476e387093dce347fb0d64970f6cebef4d50dfdcfa4d9781e2846 |

These outputs authenticate the completed attempt; their existence does not
authorize automatic resume or another worker.

## Exact branch, curvature and energy comparisons

Shapes are the fixed F=diag(exp(epsilon),exp(-epsilon),1). The positive
source is along the largest left singular axis. Its exact stationary
coefficient f(x)=lambda_max^2<1/(r+x)>/det(F) decreases from f(0)>1 to zero,
so each anisotropic shape has one positive root and its opposite-sign partner.
The isotropic reference remains b=0 with a degenerate quadratic source block;
no Schur inverse was assigned there.

The strain chart is F(q)=exp(sum q_A S_A)F, with all five orthonormal
tracefree symmetric matrices plus S_V=I/3, making q_V exact log volume.
All nine physical strain/source gradients and all 81 entries of the exact
joint Hessian were checked independently against the full energy. The source
radial/transverse identities and nested field relaxation along EACH tracefree
direction independently check the source and Schur blocks. Prestress/chart
curvature and finite-strain effects are retained.

| epsilon | positive b* | E-E_same_shape,b0 | E-E_isotropic | min H_bb | min STF Schur | min six-strain Schur |
|---:|---:|---:|---:|---:|---:|---:|
| .005 | .009953508289 | -4.967618246e-7 | .0001028367064 | .02985049875 | 4.036840118 | 3.443820295 |
| .02 | .03926452394 | -.00003118008426 | .001622187792 | .1176316825 | 3.760079044 | 3.428411812 |
| .1 | .1827325062 | -.003517463039 | .03783751336 | .5438077408 | 2.565276241 | 2.441497613 |
| .3 | .4699284894 | -.07482198303 | .2989663775 | 1.353565092 | .8496335041 | .4652639839 |
| .5 | .7050860721 | -.2856956835 | .7619482955 | 1.896361676 | -.3859093276 | -1.071876043 |

The source eigenvalues are positive in every nonzero row. However, field
relaxation exposes TWO negative tracefree curvature directions at epsilon=.5:
STF Schur eigenvalues begin -.3859093276 and -.3240842139. Thus held-field
stability does not extend automatically to the material/source system.

Even where the Schur matrix is positive, the nonzero material gradient means
that curvature is a result in the DECLARED strain chart, not invariant proof
of an unforced or physically supported equilibrium. Real supported mechanical
stability needs the actual load/support potential and its second variation.
None was introduced, chosen to match a galaxy or supplied by the worker.

The exact cubic invariant was also tested rather than discarded. For STF e,

    E_area/Sigma=1+(4/15)tr(e^2)-(8/63)tr(e^3)+...,
    <a>=1+tr(e^2)/15+(32/315)tr(e^3)+...,
    <1/a>=1+tr(e^2)/15-(32/315)tr(e^3)+... .

The complete source-zero cubic coefficient is
-(40Sigma+32B)tr(e^3)/315. The fixed S2 direction has nonzero tr(S2^3),
and its independent odd-cubic control passes on both grids. The full exact
integral, not these expansions, supplied every finite-strain result.

Maximum recorded errors:

| Check family | Maximum normalized/declared error | Frozen tolerance |
|---|---:|---:|
| Cross-grid energy/gradient/Hessian/Schur | 2.949511969426045e-8 | 2e-6 |
| Full-energy FD Hessian entries | 2.876348053930887e-6 | 2e-5 |
| Full-energy FD gradients | 2.660089200018075e-10 | 2e-5 |
| Nested relaxed STF curvatures | 4.596208687612495e-6 | 5e-5 |
| Cubic coefficients | 7.179171284399377e-7 | 2e-6 |
| Exact energy/volume/radial identities | 1.016964290556643e-12 | 2e-11 |

## Actual support and the true volume direction

At a stationary source field,

    E_field=(3B/2)<z>,
    partial_ln(s)E=2E_area+B<r-z/2> > 0,
    partial_ln(V)E=[2E_area+B<r-z/2>]/3.

The last conjugate gradient rises from 5.666666667 at the reference to
6.492910940 at epsilon=.5. The tracefree gradient norms at the five nonzero
states are .02901747522,.1136737632,.5181853063,1.395684641,2.326629086.
They are saved with all gradient components and conjugate support stresses.

Thus no freely relaxing static affine-strain/volume minimum is established
within this same action/domain. Held strains require owned boundary,
topological or loading constraints in that static interpretation. A constant
local constitutive stress does not alone prove a nonzero interior body force;
the full material divergence equation and boundary conditions still matter.
Integrability of b as grad(Phi), metric/clock constraints and compatibility
with actual ordinary sources remain uncomputed.

Nonzero E_s is NOT an acceleration failure: pressure and an expanding cosmic
solution need not satisfy the equilibrium condition E_s=0. Moreover the static
gravitational field-energy functional used here is not automatically the
homogeneous FLRW matter stress. Neither a cosmological stable phase nor its
absence follows from these supported-static matrices.

## Exact global-domain limitation of the unchanged effective action

This additional analytical corollary needs no new numerical run. If the
declared effective action is extended to every nonsingular deformation,
consider F=diag(L,L^-1,1), L>=1, and b=(L/2,0,0) in the frozen units.
Then det(F)=1, x=L^2/2, and

    K(a,x)=r+x^2/(r+x) >= 3x/2.

The last inequality follows because K increases with r>=x and equals
3x/2 at r=x. Jensen's inequality gives

    E_area <= Sigma sqrt[(L^2+L^-2+1)/3].

Therefore the SAME complete energy obeys

    E <= R+Sigma sqrt[(L^2+L^-2+1)/3]-3B L^2/8 -> -infinity.

This is a mathematical large-strain limitation of THAT declared action over
its global domain, separate from the completed finite local tests. It is
not a proof about actual native network physics outside an earned effective
regime. No post-outcome strain cutoff, retuning or compensating volume law
is imposed to rescue the effective action. A genuinely derived microscopic
domain or a different native operator would be new physical evidence, not
a reinterpretation of this failure.

## Same-candidate thermal and strain limitations are connected

The subsequently read analytical note
SURFACE_BAND_THERMAL_ENERGY_RESPONSE_V001.md has SHA-256
e4d72e1f0379112370dc5a664b1a0304d481cebd31bdcfef5cd648bd7a4f914b.
It was not an input to this numerical worker; its equations were reviewed
separately after the sealed result.

For the same {-Delta,+Delta,+Delta,+Delta} source-off spectrum at canonical
temperature T, r_occ=(exp(2Delta/T)-1)/(exp(2Delta/T)+3). The mode energy
obeys U_mode/Delta=1/2-(3/2)r_occ. Under the original cold critical
calibration, chi_T is the uniform gap average of r_occ, while U_band/B
uses its Delta^2-weighted average. Since r_occ increases with Delta,

    U_band/B <= 1/2-(3/2)chi_T.

The root note's exact integral and monotonic-weight argument are consistent
with this complete action. Positive canonical band energy requires chi_T<1/3;
near-critical response retains nearly the original negative ground-energy
inventory. Warming is therefore not a free simultaneous cure for the cold
energy budget and the critical galaxy response. Critical recalibration or a
new identity energy would change the physical premises.

Adiabatic deformation with conserved census has T proportional to s^-1,
just like Lambda, leaving Lambda/T and the suppressed response fraction
constant. Dilation alone cannot choose a later cold critical population.
At finite positive T the exact four-state free energy is analytic at small
source; it does not inherit the zero-temperature |b|^3 cusp by retuning its
quadratic coefficient. A real entropy-exchange/formation mechanism and its
work must be owned separately.

These thermal restrictions and the anisotropic/global strain limitations
belong to the SAME candidate. Neither is evidence against every native
record-feedback mechanism, and neither is repaired by choosing a favorable
occupation, source port or volume function.

## Exact next scientific action and remaining evidence

The completed effective gates now constrain what a native BS10--11 matching
must supply: physical deformation/source operators, a genuine surface/census
limit, source-weighted gaps and residues, absolute storage/interaction energy
and actual formation. Native carrier rest storage is a possible fixed-mass
source, but the full nodal interaction and signed cross residues cannot be
dropped to enforce criticality. The next work is analytical matching of those
operators to the actual native Hamiltonian, rather than another volume law
or a repeat of this worker. No such new numerical worker is active here.

The finite-gap crossover, large-field constant residual and Solar obligation,
internal acceleration-coupled kinetic bound, complete material/clock/gravity
action, ordinary ruler/redshift map and formation remain unqualified. Lensing,
growth, mergers, early-universe/CMB, thermal-origin, fair joint comparisons
and URM integration remain open. No superiority or Stage 3 completion is claimed.
