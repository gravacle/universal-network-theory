# BS11 dynamic-carrier thermal response: prospective V001

2026-10-05. New local postprocessing of sealed full states; root and independent
source review are required before one execution. No old producer is imported
or executed, and no eigensolver is called. No scheduler or new framework.

## Scientific premise and frozen scope

Test whether the large cold operational response survives thermal population
of the actual native mixed modes. The same seven supported fixed-Nc BS09/BS11
Hamiltonians, held records, twelve-node half-edge source and absolute energies
are retained from BS11_DYNAMIC_CARRIER_SOURCE_V001_RESULT.json and its sealed
per-sector arrays. The canonical ensemble is a NEW, disclosed equilibrium
preparation/bath premise. It does not derive thermalization from the held-copy
Hamiltonian. Carrier number is fixed separately in each sector; no grand
canonical count weights or chemical potential is invented. All record copy
couplings and external hops remain zero, and support is imposed.

Freeze kB=Ud=1 and dimensionless T={0,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1}
for every sealed sector, 56 cells. Absolute physical Ud/temperature conversion
is unresolved. This is not a CMB temperature fit, photon thermal-origin test,
physical lapse-temperature law, physical gravity, pressure, volume work,
cosmological preparation, galaxy fit or superiority evidence. The retained
cold mode labels do not restrict finite-T transitions; EVERY state pair enters.

## Canonical thermodynamics and complete response

For T>0, beta=1/T, epsilon_a=E_a-E0 and

    p_a=exp(-beta epsilon_a)/Z_relative,
    F=E0-T log Z_relative, E=E0+sum_a p_a epsilon_a,
    S=log Z_relative+beta sum_a p_a epsilon_a,
    Cv=beta^2 Var(epsilon), chi_uniform=beta Var(epsilon)=T Cv.

The constant is retained in complete F/E and source means; its cancellation
in probabilities, entropy and covariance is the exact identity-shift rule.
T=0 uses the previously resolved unique ground state: F=E=E0,S=Cv=0.

For the fixed-temperature static affine source H(eta)=H+eta_i G_i,
the direct second source contact is zero. In the SEALED eigenbasis,

    chi(A,B)=sum_ab L_ab A_ab B_ba-beta <A><B>,
    L_ab=(p_a-p_b)/(E_b-E_a),
    L_ab=beta p_a for E_a=E_b, INCLUDING offdiagonal exact degeneracy.

Use the symmetric stable divided difference

    L_ab=beta max(p_a,p_b) f(|E_b-E_a|/T),
    f(x)=-expm1(-x)/x, f(0)=1.

There is no artificial degeneracy grouping or gap threshold. At T=0 compute
2sum_(m>0) A_0m B_m0/gap_m and crosscheck the sealed cold receipt. A diagonal
thermal term and degenerate offdiagonal terms are essential; a cold-only pole
sum cannot represent finite temperature. All source means remain explicit.

Use G_car=epsilon_psi sum_v R_v p_v, G_rest=G-G_car. Compute independent
full/carrier/rest and BOTH ordered carrier-rest bilinears; their sum is the
signed cross response. Preserve tiny negative numerical or physical cross
terms with their actual values; never clip, reweight or declare positive
fractions. Check full=carrier+rest+cross. Sources are reconstructed directly
from frozen native operators, including hop and external identities, then
transformed by sealed eigenvectors. No deformation or physical source is added.

Uniform lapse still has zero offdiagonal H transitions. At FIXED bath temperature,
changing H to N H changes canonical populations, giving beta Var(H)=T Cv.
This is not failure of the cold uniform-time Ward control. A co-transformed
temperature, a Tolman temperature prescription or fixed local temperature is a
different source/preparation protocol and is not silently substituted here.

## Independent mathematical controls

The Duhamel form is beta integral_0^1 ds Tr[rho^s A rho^(1-s) B] minus the mean
product. Its logarithmic-mean weights obey

    beta sqrt(p_a p_b) <= L_ab <= beta(p_a+p_b)/2,
    0 <= chi(A,A) <= beta Var(A).

Check the complete pair weights, 2x2 PSD/covariance bounds, C6 isotropy and
source decomposition at every positive T. Six fixed representative actual
pairs per temperature also compare f(x) with independent composite-Simpson
integration of exp(-u), 4096 intervals over [0,min(x,40)], divided by x.
The omitted tail is bounded by exp(-40)/x; use absolute f tolerance 2e-9.
Exact x=0 uses the analytic integral one. No quadrature eigensolver is used.

The high-temperature analytic coefficient is the maximally mixed covariance

    chi_T(A,B)=beta[Tr(AB)/dimension-Tr(A)Tr(B)/dimension^2]+O(beta^2).

Check this coefficient independently in the original and sealed eigenbases.
One disclosed arithmetic probe beta=1e-6 verifies the expansion with frozen
tolerance 10 beta spectral_span times max(1,coefficient_scale)+1e-10.
Require beta spectral_span<1e-3. This is an asymptotic arithmetic control,
not a ninth scientific/observational temperature or a fitted thermal history.
The fixed grid's T=1 need not be asymptotic high temperature.

## Gates, memory and resumable custody

Freeze operator maximum-entry tolerance1e-11; complete sealed eigen residual
tolerance2e-10 max(1,||H||infinity); cold transition/action tolerance2e-10 source
scale; susceptibility/decomposition/isotropy/PSD tolerance2e-8 max(1,chi scale).
Logmean pair inequalities use1e-11 max(1,beta max p). Probability/thermodynamic
identity tolerance2e-10 times max(1,quantity scale). Source trace coefficient
custody tolerance2e-9 times max(1,coefficient scale). No scientific survival,
monotonicity, dominance, enhancement or sign of cross response is a pass gate.
All exact original/row NPZ hashes and input anchors must match the cold receipt
and journal. Reconstructed H/G byte hashes must match their cold source hashes.
Check all sealed eigen residuals in blocks, without solving again.

One local bundled NumPy process, BLAS threads1, peak RSS<512MiB, target<60s per
sector. No twelve-node/edge dense copies or installations. Eigenbasis full,
carrier and rest sources plus compact observables are saved in one exclusive
per-sector NPZ, then each temperature cell and high-T control in exclusive JSON.
Sector/cell receipts are committed with SHA256 in an append-only journal.
The directory is NEW bs11_dynamic_carrier_thermal_v001_checkpoints/.

--execute exclusively creates the directory and final output destinations.
Separately authorized --execute --resume requires no final receipt, matching
input hashes/manifest and no live latest worker PID. Completed cells and
operator arrays are reused only with journal SHA256 authentication. An orphan
complete operator NPZ is validated from embedded input/cold-array/source hashes
and cold-result consistency, without a transform rerun. Partial files block
recovery and are preserved. A sector begun without an operator NPZ requires a
parent decision before repeating transforms. Unfinished thermal cells resume
only from the authenticated complete source arrays; completed cells are never
recalculated. Errors/failures seal; no automatic retry, scheduler or resubmission.

Owned ONLY this protocol, bs11_dynamic_carrier_thermal_v001.py,
BS11_DYNAMIC_CARRIER_THERMAL_V001_RESULT.json/.md and the NEW checkpoint directory.
Root owns log/ledger reconciliation. Row timing includes operator arrays and
cell calculations before the small sector receipt; total run timing includes
sector metadata but final report persistence follows. Preserve failed outputs
and list exact unfinished sector/cell. No prior states, source or receipt edits.
