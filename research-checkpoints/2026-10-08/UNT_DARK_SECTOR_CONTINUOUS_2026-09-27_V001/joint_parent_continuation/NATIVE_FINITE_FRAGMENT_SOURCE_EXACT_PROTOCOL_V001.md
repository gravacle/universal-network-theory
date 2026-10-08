# Prospective exact source check: original blank, finite fragments, order four

This is one bounded symbolic check of the distinct family in
`NATIVE_FINITE_FRAGMENT_SOURCE_CURRENT_V001.md`. The author and independent
reviewers must not import or execute the producer. Root alone may freeze and
run after full source review, a source-only syntax check, and an external
resource/capture wrapper. No output existed when this protocol was written.
No next-order calculation or numerical time/parameter scan is authorized by
a zero or unfavorable fourth-order result.

## Fixed model and exact coefficient convention

The basis order is Q3, C2, rL2, rR2, n2, carrier2, bL2, bR2. The integer
index is `128*Q+64*C+32*rL+16*rR+8*n+4*carrier+2*bL+bR`.
The native carrier left state is zero. Four original initial basis states
have Q=0 or 2, C=1 and every remaining bit zero, in A or B. Each is examined
under both the original Hamiltonian tensored with fragment identity and the
specified extended Hamiltonian: exactly eight cases, no mixed-state witness.

The unchanged native parameters are J=Omega=g=1. HQ is the three-site path
Laplacian; HC=I-X_C. Native quantities are

    Hh=3I+R-X_n+n(9/4-R/2-X_carrier/2),
    T=n(I/4-X_carrier/2), Eb=2, K=X_rL+X_rR.

Use the exact coefficient field Q[a]/(a^3-2), with the positive real root
selected analytically. Q endpoints are represented by
`s=(a^2/2,1,a)`, `s^-1=(a,1,a^2/2)` and `s^3=(1/2,1,2)`.
No rounded cube root, logarithm or fitted normalization is evaluated.
Lambda and nu remain independent polynomial variables; nu>=0 is the stated
physical-gap domain, not a substituted test point. Retain every identity
energy and both controllers, including the original unequal endpoint energies.

The energies and dipoles are exactly those of equations (1)-(3) of the note:
H_A=HQ+HC+s^-1(Hh+Pc*K),
H_B=HQ+HC+Hh-T-Eb+s^-1*T+Eb*s^3+Pc*K,
with F_v=nu*q_bv+lambda*q_v*X_bv and the same A/B factors on every added term.
The symbolic source factor is removed only for calculation:
`Z=gamma0*z`, never by assigning a numerical physical value to gamma0.
The reported moment coefficients obey

    S_Z(t)/gamma0^2 = hbar^-2 sum_(n=0)^4 m_n (t/hbar)^n + O(t^6).

The remainder is even for these real Hamiltonians, real observables and
real basis preparations. It is a Taylor statement, not a finite-time error
estimate. Energies and native coefficients use the inherited common energy
unit. A polynomial result is not a physical calibration.

## Primary calculation and independent crosscheck

Build sparse real Hamiltonian/source actions independently from the displayed
bit layout; import no old producer or stored numerical matrices. Let
`v_k=H^k psi0`, formed through k=5. The primary moment bilinear is

    <v_j|M|v_k> = 2<z v_j|H z v_k>
                 -<z^2 v_j|H v_k>-<H v_j|z^2 v_k>,
    M=[z,[H,z]].

Convolve this with the exact phases `i^j*(-i)^k/(j!*k!)`, j+k=n. For the
independent method, apply the operator commutator directly as
`M v=z(H z v-z H v)-(H z-z H)(z v)`, then recursively compute
`(ad_H^n M)H^k psi0=H*(ad_H^(n-1) M)H^k psi0
                    -(ad_H^(n-1) M)H^(k+1) psi0`.
Its expectation multiplied by i^n/n! must match each primary coefficient.
This is an independent action/commutator evaluation, not an independent
physical Hamiltonian or a second propagation algorithm.

Report all coefficients n=0,1,2,3,4, including required zeros, not just a
selected favorable coefficient. Retain the extended-minus-original moment
polynomial for every original preparation and the boolean stating whether
the fourth-order difference is identically zero. Do not evaluate or score
its sign at a rounded a or a chosen lambda/nu. Any later algebraic sign
claim requires exact root isolation/inequalities or remains unevaluated.

## Prospectively fixed exact controls

All comparisons are equality of canonical rational polynomials. There are
no tolerances and no positive-moment target.

- Elementary a^3=2 and each s*s^-1=1; sparse operators real symmetric.
- The current identities of note (6) are checked on all 384 basis columns
  in both families. A's extended current equals the old current; B's extra
  current is `[HQ,s]*F_Delta` in normalized source units. Only the first
  failing residual, if any, is serialized; the complete column census is
  fixed, not sampled. No full operator matrix export is needed.
- A's Pauli signed-moment correction from note (8) is additionally checked
  on each original endpoint blank and its first H-power. This is explicitly
  a restricted state-span check, not a separate full-matrix certification.
- The two moment methods agree at every order through four. Imaginary
  expectation coefficients and real-observable odd orders vanish exactly.
- Moment m0 is zero for all original and extended blank states. The
  extended-minus-original m0 and m2 vanish. No prescribed m4 value or sign
  is required; it is the new reportable discriminant.
- Setting lambda=0 in every extended moment coefficient recovers the
  original coefficient, even though an unoccupied finite-gap fragment still
  formally exists. Nu=0 is reported symbolically, not mistaken for an
  automatically unchanged physical source response.
- Norm coefficients are (1,0,0,0,0). Total complete energy is constant
  through this order. Its series equals the sum of the original parent,
  added fragment-gap energy and added copying-interaction energy at each
  order. All four series are retained. This is the closed on-Hamiltonian
  balance, not an unrecorded fragment trace-out or physical cooling claim.
- Initial total energy is `2+3*s^-1` for A and `3+2*s^3` for B. The original
  unequal energies are not equalized to produce an environment comparison.
- Record occupation starts with coefficient R2=2*f^2, where f=s^-1 in A
  and f=1 in B. Blank-fragment N_b has zero coefficients at zero and two;
  its fourth coefficient is lambda^2*f^4/2 in the extended family and zero
  in the original family. Both population series are retained in full.

Every comparison adds a retained check row. A mismatch preserves its actual
polynomial/residual rather than changing a criterion. The source note's
uniform-lapse, volume and mixed-contact conventions are part of the fixed
physical family; this algebra does not independently derive those conventions
or provide a new metric/volume closure. It does not claim a full source-jet
export, all-orders response, stationary spectrum or positive inertia.

## Bounded implementation, custody and failure disposition

The stdlib-only source is `native_finite_fragment_source_exact_v001.py`.
Polynomial keys are (a power reduced to 0,1,2; lambda power; nu power), with
exact Fraction coefficients. The maximum lambda+nu degree is seven, maximum
128 terms per polynomial, and numerator/denominator length is at most 512
bits. Sparse vectors have at most 384 entries; each sparse operator has at
most 10,000 entries. The prospective cumulative monomial-product budget is
3,000,000. Exceeding any bound is a technical unready result, not evidence
against the mechanism and not permission to enlarge a limit mid-run.

The child sets CPU soft/hard limits 30/35 seconds and checks a cooperative
45-second wall deadline. Root must additionally use the established external
monitor with wall 45 seconds and sampled process-group RSS 256 MiB, capture
raw streams, and retain an exclusive wrapper receipt. Sampled RSS is not
an unsampled-memory guarantee. One child only; no queued cases or remote
work. The complete result must fit 2 MiB; source/input files are capped at
4 MiB each. No SciPy, NumPy, eigensolve, code-generation execution, external
data retrieval or module installation is involved.

`freeze` and `run` are separate explicit operations and never launch one
another. Both require the sole project root as cwd and the exact owned
source path. Freeze authenticates the original producer/protocol, energy
dipole note, and the independent finite-fragment-current review, then records
its own source, this protocol and the current analytical note. It refuses
an existing intent/result. Run compares that complete freeze, publishes a
new exclusive intent and rechecks every source/input before success.

Atomic same-directory no-overwrite publication preserves frozen predecessors.
Caught failures retain completed case/check output and the error; structured
series not yet finished when an exception occurs may be absent. A hard CPU,
wall or RSS stop may leave only an intent and the root's raw capture. That is
not a pass and cannot be silently rerun under the same identifier. A caught
publication failure likewise cannot be represented as a completed result.

Success is `EXACT_SOURCE_IDENTITIES_COMPLETE_NOT_PHYSICAL_QUALIFICATION`.
It confirms this finite low-order computation only. Physical qualification,
formed-state completion, passivity, thermal qualification, propagation and
Stage3 completion remain false. The finite fragment preparation/gap/coupling,
source and volume assignments are new conditional premises. No original
scientific failure is relabelled, no record degree becomes physical density,
and no higher-order or favorable-age search follows automatically.
