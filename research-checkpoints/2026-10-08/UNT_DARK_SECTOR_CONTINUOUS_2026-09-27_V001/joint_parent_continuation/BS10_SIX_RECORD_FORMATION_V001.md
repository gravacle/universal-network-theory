# BS10 all-six-record formation: prospective matrix-free V001

2026-10-05. New local supported native extension, not a restart. Root/independent
source review and fresh ownership approval precede ONE numerical process.
No prior producer/eigensolver/trajectory is replayed. No scheduler/framework.

## Native change and frozen inputs

Restore the original positive BS10 copy operator at ALL six active nodes,
replacing the externally clamped four record registers of the sealed two-record
calculation. No parameter is changed or fitted. Retain the same supported
hexagon, six clamped occupied exterior links to blank vertices at2R, all other
incidence clamped absent, external flips/hops excluded. Nc=1 carrier of content
x, all records initially blank, internal ice starts n=21 and42, carrier start0.
Index=((n*6)+carrier)*64+r; r has six binary {B,x} record bits. Dimension24576.

Freeze Delta0,d*=2,Ud1,ER=EP1,h=t=.10,lambdaR=.5,lambdaJ=.25, g=0 or.10.
All other copy/writer/reservoir couplings zero. Times0,1,2,5,10,20,50 and
the previously frozen auxiliary ±.001,±.002 are retained for both starts/g.
This is44 full states, with no favorable initial state or time selection.
The Nc1 subspace is closed under the original content-preserving hopping and
copy operators; each copied record carries the orthogonal carrier content.
The supported Delta0 domain does not inherit extensive BS13 stability.

## Exact matrix-free law and source

For d_v=1+n_prev+n_v and p_v=1 only at the carrier vertex, the complete diagonal
is

    D=6Ud+EP+lambdaJ+Ud sum_v(d_v-2)^2
      +sum_v q_v(ER-lambdaR)
      +sum_e n_e[lambdaJ(p_u+p_v)-lambdaR(q_u+q_v)].

The complete H matvec is D times vector, minus six h n-bit-flip gathers,
minus t carrier-neighbor gathers gated respectively by n_carrier and n_prev,
plus ONE g record gather r xor(1<<carrier). Copy sign is positive; record
occupations and their feedback are operators, not assigned environments.
No energy donor, pumping supply, gamma-energy term, fitted mass or volume term
is added. Six exterior degree/onsite/current/record-feedback terms are retained.

The previous operational affine nodal source is inserted before propagation.
Each active node owns degree, carrier/record storage and its copy term.
Internal flip/hop/current-square/record-feedback terms are half at each
endpoint; external edge is half at active/exterior endpoints, with exterior
positions2R. Diagonal G and its gathers keep all identity/exterior terms,
including ideal-hex sums that happen to cancel. No source is recentered.
Check independent weighted H[N] at affine arm(1e-6,-2e-6), uniform N=.93,
and exact reflection v->-v (edges e->-e-1, record bits likewise). Reflection
swaps the two retained ice starts. Nonstationary source means are not a static
gravitational susceptibility. No physical ruler, clock or source normalization.

## Propagator and certified truncation/alias control

Exact diagonal range Dmin7.5,Dmax16.25 is checked over the full finite basis.
Row offdiagonal absolute sum6h+t(n_carrier+n_prev)+g<=.8+g. Set c=11.875,
a=4.375+.8+g+1e-12, then round a outward with nextafter(+infinity).
This declared arithmetic pad is not a scientific parameter. A=(H-cI)/a
has absolute row sum<=1 and Hermitian spectrum in[-1,1]. No dense full H.

For each frozen tau, z=a tau, the exact Chebyshev expansion has coefficients
c0=J0(z),cm=2(-i)^m Jm(z). Obtain complex coefficients from the normalized
N-full-angle FFT of exp[-iz cos(theta)], keeping both complex parts. Freeze
M=400,N=4096 and coefficient refinementN=8192. Keep exp(-ic tau) complete phase.
A single recurrence per start can accumulate all prescribed times. At tau0,
the identity propagator is exact. No Bessel library/install is required.

For alpha=1 define the rigorous Fourier tail bound

    tail(K)=2 exp(|z|sinh(alpha)-K alpha)/(1-exp(-alpha)).

The exact mathematical truncation PLUS FFT alias bound is

    tail(M+1)+(2M+1)tail(N-M), N>2M.

Save both log bounds and their sum; underflow does not imply a zero exact error.
Require the certified bound<1e-12 at every time, and coefficient-refinement
sum|c_N-c_2N|<2e-11. Use N8192 coefficients for actual propagation. Measured
tails alone are not a certificate. This bound concerns exact polynomial/FFT
arithmetic; floating-point roundoff is separately controlled by coefficient
refinement, norms, conservation, reflection/time-reversal and sealed-state
lineage checks. No claim of a rigorous floating-point error certificate.

## Sealed two-record lineage without its solver

The subspace P has records1,2,4,5 blank, record0/3 free. Reconstruct its H
from the sealed two-record eigenvalues/eigenvectors. Project the new primitive
matvec/maps to P and compare the complete1536D H. Authenticate projected G
against the old source operator hashes; old eigenstates alone do not determine
source operators. Compare source means on the old saved states as well.
An explicitly clamped-copy control at only nodes0,3 uses this NEW Chebyshev
algorithm and must reproduce the sealed old44 full states, within2e-8 maximum
amplitude. It never diagonalizes or calls the old producer. P H_full P matches
the old H, while actual full-copy dynamics exits P; no false subspace claim.

## Records, content coherence and thermodynamic ceiling

Save each full state, all six carrier/record/incidence/degree means, complete
energy/source decomposition and unrounded reduced64x64 record density.
The physical record alphabet is {B,0,1}^6 of dimension729. Save explicit
isometry indices for content0 and1; their supports intersect ONLY in allblank.
Squared Uhlmann record fidelity is exactly P_allblank^2. Independently evaluate
the singular-value fidelity of sqrt(rho64_0) P_overlap sqrt(rho64_1); the
isometries preserve its nonzero singular values in the full729D alphabet.
This avoids repeatedly allocating the physical zero-filled density matrix.
Save density eigenvalues, entropy and small-negative square-root diagnostics
without altering actual rho/states. The two-record full9D fidelity remains
an independently sealed lineage result.

As a derived coherent-content witness, pair the two content-exchange-related
branches of the SAME spatial/blank seed in |+>. Directly contract their
physical record-label intersection and trace position/incidence. This gives

    rho_content=1/2 [[1,P_allblank],[P_allblank,1]],
    visibility=P_allblank, purity=(1+P_allblank^2)/2.

Save this derived density/purity/entropy and direct overlap, without another
solve. Squared visibility=gamma_rec holds for THIS pure symmetric witness,
not generic mixed influence=fidelity. Copy entangles an orthogonal alphabet;
it does not clone arbitrary qubit states or prove irreversible decoherence.

## Prospective gates and exclusive recovery

Source/operator tolerance1e-11; source/energy/probability/norm/trace/reflection
checks2e-8 times max(1,quantity scale); Hermiticity tolerance2e-10 and density
PSD tolerance1e-11. Fidelity agreement2e-8. In square-root diagnostics ONLY,
negative density eigenvalues within PSD tolerance can be zeroed; all raw
eigenvalues/rho are saved. Early coefficient relative tolerance1e-5, and
sum record occupation away from0<=1e-7 g^2 tau^2+1e-20 (no tau² coefficient).
Direct H|seed> coefficients must be q0=g², all other q=0, before finite time.
At g0 all records stay blank and gamma/visibility1 within frozen tolerance.
No formation, spread, monotonicity or information-loss outcome is a pass gate.

One modest local NumPy process, one BLAS thread, no installation/remote work.
Existing512MiB/60seconds-per-H safeguards retained; focus reporting on science.
The new directory bs10_six_record_formation_v001_checkpoints exclusively stores
manifest/journal, primitive/operator coefficient custody, full state NPZs and
per-state/per-H JSON commits. Final results also exclusive. --resume requires
separate root authorization, absent final receipt, matching inputs/commit hashes
and no live latest worker PID. Recover complete unfinished arrays before any
new calculation; partial/foreign bytes block and remain preserved. Completed
states are never re-propagated. No automatic retry, scheduler or background loop.
An existing bundle without its completed SHA256 journal commit also blocks for
separate manual recovery; embedded metadata alone does not authenticate it.
Before skipping a completed Hamiltonian, verify every unique referenced bundle
against live bytes and its journal commit, plus all recorded input/hash references.
Own ONLY this protocol, bs10_six_record_formation_v001.py,
BS10_SIX_RECORD_FORMATION_V001_RESULT.json/.md and the new checkpoint directory.
Root owns continuation log/ledger. All required scientific lanes remain open.
