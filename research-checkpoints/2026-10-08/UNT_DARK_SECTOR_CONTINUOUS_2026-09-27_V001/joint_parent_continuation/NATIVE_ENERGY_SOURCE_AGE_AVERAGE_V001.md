# Bounded source age averaging for the native energy and volume response

2026-09-30. Analytic readout construction using the existing 96D autonomous
A/B Hamiltonians and all four specified initial preparations. No numerical
worker, eigensolve, propagation, new preparation, bath or fitted response
function was used. Averaging is a declared measurement protocol, not physical
dephasing, equilibration or a formation rule.

The complete dipole/volume packet has so far evaluated saved-state means,
contacts and moments, not this two-source spectral reduction. The writer K
age average in `NATIVE_RECORD_PHASE_PATHWAY.md` section6 and the carrier P
low-frequency bound in `NATIVE_FINITE_MEMORY_TRANSPORT_REALIZATION_V001.md`
section5 are precedents, not results for the present energy sources. The new
question is whether their ACTUAL signed inverse-gap response has a controlled
low-frequency readout, with finite-age coherence errors retained.

## Source and readout definitions

Keep each full owned H=H_Q+H_C+h_L+h_R, including formation and both controller
dynamics. Let alpha=gamma0*a_ext, gamma0=ell0/(2c^2), without assigning a
numerical physical ruler. The dimensionless source vector is lambda=(alpha,eta)
and its energy insertions and contacts are

    G=(Ztilde,-B_eta),   Ztilde=Z/gamma0,
    H(lambda)=H+sum_i lambda_i G_i
                         +1/2 sum_ij lambda_i lambda_j C_ij+O(lambda^3),
    C_alphaalpha=0, C_alphaeta=H_aeta/gamma0,
    C_etaeta=H_etaeta.                                     (1)

These are precisely the adopted bridge/apparatus sources, not incidence n
or carrier chemical potential. The zero alpha contact is restricted to this
affine source family. The microscopic metric/volume premises remain adopted.
For chi_ij=(i/hbar)theta(t-s)<[G_i(t),G_j(s)]>, response to the PLUS source
lambda_j G_j is minus chi. The conjugate-energy response kernel is C-chi,
including the direct contact, not chi alone.

For an original initial rho0 and U(w)=exp(-iHw/hbar), define rho_w=U(w)rho0U(w)^dagger.
An experiment averaging its start age uniformly over [w0,w0+T], T>0, has

    rho_T=1/T integral_w0^(w0+T) rho_w dw.                  (2)

This is bookkeeping for averaged LINEAR readouts from the same specified
preparation at different ages. It does not replace the actual trajectory or
authorize resetting a single disturbed system between probes. Multiple
preparations or their noninvasive response reconstruction must be declared
if the protocol is physically implemented. No astronomical clock is assumed.

Let Pi_E be the full exact spectral projectors of H and rho_EF=Pi_E rho0 Pi_F.
Then exactly

    rho_T=sum_EF exp[-i(E-F)(w0+T/2)/hbar]
                    sinc[(E-F)T/(2hbar)] rho_EF,
    rho_d=sum_E rho_EE,       sinc(0)=1.                   (3)

Whole degenerate blocks remain intact. All original conserved energy
populations are unchanged; there is no Boltzmann population assignment.
rho_d is the infinite-age-average comparator, not a prepared passive state.
Finite rho_T is generally NOT stationary. In particular the full averaged
two-time kernel is (i/hbar)theta(t-s)Tr rho_T[G_i(t),G_j(s)], not automatically
a lag-only law.

## Exact finite age error bound

The trace norm and triangle inequality give

    ||rho_T-rho_d||_1 <= b(T),
    b(T)=min(2, sum_(E!=F) ||rho_EF||_1
                             min[1,2hbar/(|E-F|T)]).       (4)

The sum is over ordered unequal energy blocks. An exact sinc envelope can
replace its second min for a tighter bound. For the owned pure initial states,
||rho_EF||_1=sqrt(p_E p_F), p_E=Tr rho_EE. Bound (4) is uniform in w0;
it does not select a favorable formation age. It provides a function of T,
not a chosen averaging duration or an assertion that a required T is physical.

For bounded Hermitian observables A,B,C, the same difference obeys, uniformly
in the observation/source times,

    |delta <A(t)>| <= ||A|| b(T),
    |delta <C(t)>| <= ||C|| b(T),
    |delta chi_AB(t,s)| <= 2||A||||B|| b(T)/hbar.            (5)

Here the difference compares finite age averaging to rho_d, and the second
line covers every contact in (1). The proof uses trace/operator norm duality
and ||[A(t),B(s)]||<=2||A||||B||. No damping or environmental loss is assumed.

For a lag integral over 0<=tau<=L with unit-modulus Fourier weight, multiply
the last bound by L. For the explicitly resolved transform with weight
exp[(i nu-kappa)tau], kappa>0, its integral bound is instead

    2||A||||B|| b(T)/(hbar*kappa).                         (6)

The first comparison is to the SAME finite-window stationary transform;
it does not discard the stationary transform's own endpoint terms. Those
terms can be evaluated exactly from the finite spectral sum. Kappa in (6)
is a readout convergence/resolution parameter, not a fitted relaxation rate.
Both T and L or kappa remain symbolic until a readout requirement is frozen.

## Why the order of limits and source work matter

Finite-T residual coherences can contribute zero-lag-frequency pieces even
when the stationary comparator has no such term. Consequently small b(T)
does not justify an undamped zero-frequency limit at fixed T. In particular
(6) is not uniform as kappa tends to zero. To use it in a joint limit one
must control b(T)/kappa; otherwise retain the finite-window residual exactly.
Taking T to infinity first and then using a stationary static response is
a conditional diagnostic, not an automatically valid physical order of limits.

The one-point source means must also remain in the work ledger. At rho_d they
are constant, so their first-order work vanishes for a cyclic probe. At finite
T, their residual drift can give first-order work bounded by

    |delta W^(1)| <= b(T) sum_i ||G_i|| ||lambda_i_dot||_1. (7)

This is O(probe amplitude*b(T)), whereas quadratic response work is O(amplitude^2).
Subtracting the unforced mean is legitimate for a response diagnostic, but not
for declaring physical passivity after ignoring an available first-order
work channel. Keep switch/initial-boundary terms, contacts and the exact
two-time remainder. Never restart each impulse in rho_d by convention.

## The smallest new signed low frequency discriminator

For the present real symmetric H and G_i, the original basis-vector rho0 is
real and each rho_EE remains real symmetric. Same-energy commutator traces
therefore vanish. This is an explicit property of this packet, not a general
rule allowing degenerate zero-frequency response to be dropped.

For E<F, Delta=F-E>0, define the real symmetric two-source residue matrix

    M_ij^(EF)=Tr(rho_EE G_i Pi_F G_j)
                         -Tr(rho_FF G_j Pi_E G_i).        (8)

Group ALL equal-gap contributions into M_Delta before judging the sign of a
resolvable absorption line. Neither an individual eigenvector in a degenerate
block nor a weak negative line may be discarded. These residues use the
actual conserved populations and coherences within exact degeneracies.

The stationary comparator has the exact susceptibility, for Im z>0,

    chi_d(z)=sum_Delta 2 Delta M_Delta
                                      /(Delta^2-hbar^2 z^2),
    chi0=2 sum_Delta M_Delta/Delta,
    chi2=2 hbar^2 sum_Delta M_Delta/Delta^3.                (9)

Thus chi_d(z)=chi0+z^2 chi2+R4(z). For |hbar*z|<Delta_*, where Delta_* is
a certified smallest positive contributing gap, a matrix norm bound is

    ||R4(z)|| <= [2 hbar^4 |z|^4/(1-|hbar*z/Delta_*|^2)]
                                      sum_Delta ||M_Delta||/Delta^5. (10)

No numerical small-gap merging or line deletion is implicit. If a gap or
degeneracy cannot be resolved within certified arithmetic, report that limit
rather than produce an unjustified low-frequency certificate. The work
curvature includes the actual averaged contact: <C>_d-chi_d(z).

The averaged first moment weights residues as 2 sum Delta*M_Delta/hbar^2;
chi0 and chi2 weight them by INVERSE gaps instead. Consequently a negative
first moment does not determine their signs. The saved negative instantaneous
moments do not themselves even fix the sign of the infinite-age-average
moment. All these quantities must be kept distinct.

Positive chi0 or chi2 is NOT passivity, a mechanical mass, hardening or a
gravitational constitutive law. A negative eigenvalue of a grouped M_Delta
witnesses active linear absorption in an accessible source combination at
that line. Conversely, positive grouped matrices only qualify that linear
source channel, not arbitrary operations or a Gibbs state. Strictly below
every finite transition line the stationary absorptive response is zero even
for inverted populations; that null is vacuous evidence for passivity.
Finite-duration pulses generally have above-gap frequency tails, which must
be retained or bounded before applying a nominal subgap claim.

## Prospective calculation and decision boundary

The smallest new packet would authenticate the two existing A/B Hamiltonians,
the complete G/C operators and all four initial preparations, then compute
their full spectral projectors once per Hamiltonian. It would report every
grouped signed 2-by-2 M_Delta, chi0, chi2, <C>_d, the bound functions (4),(10),
and any zero-frequency term rather than generate another propagation grid.
Saved later vectors can check conserved spectral data without replacing the
initial states. No physical frequency, averaging age or favorable population
is calibrated from a desired result.

Before such a root-only numerical run, separately freeze source identities,
degeneracy/error rules, matrix/projector reconstruction and sum-rule controls,
resource limits and complete output census. An observational or effective-law
error target would subsequently specify admissible (T,L) or (T,kappa,nu).
Until then, the output is a parameterized native-unit error certificate,
not a selected physical window. This note is not a numerical run protocol.

Failure to obtain a nonempty, adequately bounded readout window means retain
the actual source-dependent finite memory; it does not license a bath or
state substitution. Success would qualify only a finite conditional readout.
It would not create a passive attractor, establish a continuum/soft spectrum,
derive the physical source dictionary, select a galaxy state, or eliminate
dark matter/dark energy empirically. All existing physical flags and the eleven
mandatory outstanding lanes remain unchanged.

## Read source identities

- `NATIVE_RECORD_PHASE_PATHWAY.md`, section6:
  `ab58e978623ceb6c04e3f4e43f7f10e87fac025a88ac76cc8e46bad891b80a19`.
- `NATIVE_FINITE_MEMORY_TRANSPORT_REALIZATION_V001.md`, sections3–5:
  `5ffeccf4fe4041348a3e3b74571be43f607cb89908bc65940d68deb10781e64c`.
- `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`:
  `81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96`.
- `NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_PROTOCOL.md`:
  `0cce4c0169b45fd1452b87fe262eb5abf79d17fb1821670fbcfe8f665f1f9d7d`.
- `NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_RESULT.md`:
  `84eeaedfbadb91730a24c60abc1f8116ea13f384e65eed377780346e3f3afcae`.
- `NATIVE_ENERGY_SOURCE_PRESERVATION_V001.md`:
  `d0991dd4fd79b77ecb705f384c1b805d9923d132405a384c85168a98f4be1a2e`.

The bounded averages and inverse-gap formulas are analytic deductions from
these premises, not completed numerical measurements of their coefficients.
