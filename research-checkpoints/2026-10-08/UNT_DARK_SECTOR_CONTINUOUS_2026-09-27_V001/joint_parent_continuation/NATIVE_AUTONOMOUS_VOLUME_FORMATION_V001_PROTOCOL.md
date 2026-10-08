# Autonomous finite volume and formation: prospective A/B protocol V001

2026-09-30. Source-only prospective candidate. Root is the sole producer.
No run, result, astronomical fit, native metric identification, or change to
the frozen BS parent is asserted by this document. Preserve both outcomes,
including failures. An independent source review must precede freezing/running.

## 1. Question and physical boundary

Do the two already declared operational dilation laws predict distinct
autonomous formation and volume-controller recoil when the full finite
apparatus energy is retained? This is a conditional apparatus discrimination,
not proof that either dilation law is nature's law. No fixed-background
trajectory can decide the omitted physical choice of volume coupling.

The new premises are (i) three calibrated volume labels with V/V0=1/2,1,2,
(ii) the finite controller hopping energies below, and (iii) either A's
uniform native homothety or B's allocation of the original degree baseline
to volume and full transport term to inverse ruler. There is no fitted c(V),
vacuum offset, halo profile, gravitational acceleration source, or parameter
chosen using astronomical observations. V0 and the microscopic energy unit
would require independent physical calibration. The numerical ratios J=Omega=g=1
are declared apparatus benchmark choices, not derived physical constants.

## 2. Exact basis, operators and native reference

The ordered basis is Q tensor C tensor (rL,rR,a,c), dimensions 3*2*16=96.
Q labels are minus,zero,plus; C is the formation controller, not the native
carrier c. Every two-state native factor has basis blank/occupied (for c:
left/right), X=[[0,1],[1,0]], n=diag(0,1), and conventional Pauli Y. This
matches record_addition_compute.py's native factor order. Its saved Y uses
the opposite convention, but Y squared is identical. No saved state is
replaced by a passive ground state; the new apparatus starts from the same
original native blank vector |0,0,0,0> in all four cases.

With all original held-cell terms and constants retained,

    R=qL+qR, K=XL+XR,
    Hh=3I+R-Xa+n(9/4-R/2-Xc/2),
    T=n(I/4-Xc/2), Eb=2.

The independent term reconstruction uses h=1, Delta=4, Ud=d*=1,
epsilon_carrier=epsilon_record=1, epsilon_writer=0, t=1/2,
lambda_R=1/2, lambda_J=1/4. Both degree penalties are included. T includes
both carrier hopping and current-square feedback. The reference formation
Hamiltonian is Hh+K, recovered at q=0 with C clamped on.

## 3. One time-independent finite Hamiltonian per candidate

Set q=(-ln2/3,0,+ln2/3), v_j=exp(3q_j), Pc=|1><1| and

    HQ=J sum_nearest (|j>-|k>)(<j|-<k|),
    HC=Omega (I-X_C),       J=Omega=g=1.

The full 96D Hamiltonian is HQ+HC+sum_j |j><j| tensor E_X(q_j), where

    E_A(q)=exp(-q)[I_C tensor Hh + g Pc tensor K],
    E_B(q)=I_C tensor[Hh-T-Eb I+exp(-q)T+Eb exp(3q)I]
              +g Pc tensor K.

The Hamiltonian and initial states are real. No clock quench, hidden bath,
repeated reset, irreversible formation rule, or mean-field factorization is
used. C's dynamics, interaction energy and Q recoil remain coherent parts
of the 96D state. The finite volume support makes B's small-volume
unboundedness outside this window irrelevant to this finite experiment;
it does not establish an autonomous unbounded volume theory.

The four cases are exactly A/minus, A/plus, B/minus, B/plus, initially
|Q_endpoint> tensor |C=1> tensor |native blank>. Their initial energies are

    E_A,j=J+Omega+3 exp(-q_j),
    E_B,j=J+Omega+1+2 exp(3q_j).

Thus B's initial energies are 4 and7 in the chosen units, not equal-energy
preparations. Different preparation energies are retained and cannot be
misreported as energy created by an expanding controller. All times use
the same externally calibrated microscopic boundary time, hbar=1 here.
These are not equal-energy interventions isolating density as a sole cause.
K is reversible: early growth of R is not permanent record accumulation,
SEALED formation, autonomous thermalization, or a selected late-time attractor.

## 4. Prospectively derived distinguishing coefficients

Let P0 project onto Q=zero. For either endpoint j, define the operator on
C tensor native space

    Delta_j=E_X(q_j)-E_X(0)-J I.

The diagonal difference -J is compulsory: HQ has endpoint diagonal J and
middle diagonal2J. For the stated initial state,

    <P0>(t)=J^2 t^2/hbar^2
       -[J^2 <Delta_j^2>/12+2J^4/3]t^4/hbar^4+O(t^6).

This formula does not assume commuting E blocks. The common HC cancels
from Delta_j. Reality gives the even-time expansion for this basis-state
preparation. Check the coefficients directly by nested commutators and,
independently, by the state-vector power series, not a finite-time fit.

With a=2^(1/3), b=2^(-1/3), J=1,

    coefficient_t4[<P0>_minus-<P0>_plus]_A
           =(a-b)(5/2-a-b)>0,
    coefficient_t4[<P0>_minus-<P0>_plus]_B=-1/4.

The native formation readout obeys

    <R>_A=2g^2 exp(-2q_j)t^2/hbar^2+O(t^4),
    <R>_B=2g^2 t^2/hbar^2+O(t^4).

The compressed/expanded t^2 coefficient ratios are 2^(4/3) and1. This
uses common boundary time; comparing equal native ages would be a different
experiment. No finite-time probability is graded against its truncated
asymptotic polynomial. Raw finite-time contrasts and signed remainders are
reported without requiring the early-time signs to persist.

## 5. Census, numerical methods and criteria fixed before results

For each of the four cases store t=0 and t={.01,.02,.04,.08}; never select
an observation phase. Store the complete complex96-vector, Q probabilities,
R, incidence n, carrier-right, formation-controller occupation, volume,
the actual expectation <R/V> (not <R>/<V>), each component's energy and
current, total energy and norm. Publish the real total and component
Hamiltonian matrices for independent saved-only arithmetic reconstruction.

Spectral propagation is cross-checked against a separate scaled Taylor
matrix exponential. For Taylor scaling choose ||-iHt/2^s||_infinity<=1/2.
The scalar exponential-tail majorant exp(x) x^(k+1)/(k+1)! must be <=1e-18
before squaring; propagate its exact-arithmetic bound as e -> e(2+e) for
each squaring and retain it as an operator-2-norm bound. The scaled generator
is anti-Hermitian, its 2-norm is bounded by the input infinity norm, and its
exact propagator has 2-norm1. Floating-point roundoff is tested independently.
No scipy, external solver, installation, multiprocess worker or network use.

Frozen numerical gates, absolute unless explicitly scale-normalized:

- Native operator reconstruction, Hermiticity/reality, source/block identities,
  norm, probability normalization and projector identities: 2e-11.
- Spectral versus Taylor propagators and states: 5e-11.
- Total/component energy and current identities: 5e-10 times
  max(1, magnitudes of the compared quantities).
- Exact Taylor coefficients, two independent algebraic routes and the
  analytic formulas: 2e-10 times max(1, compared coefficient magnitudes).
- Positivity of probabilities permits only -2e-11 roundoff; no clipping.

These bounds allow conservative accumulated double-precision rounding for
96D products, four nested commutators and several squarings; they are not
observational tolerances or fitted to observed errors. Retain every raw
residual. A failure is preserved, not repaired by loosening these gates.
Current for a fixed component Ha is i<H Ha-Ha H>/hbar, independently checked
as 2 Re<(-iH psi)|Ha psi>. The sum of all component currents must vanish.
No component current is a product of separately averaged controller/native
operators. Component-energy sum and total-energy conservation are distinct.

## 6. Resource, custody and promotion boundary

Exactly two96D real Hamiltonians and four initial states, one process with
all BLAS/OpenMP threads fixed to1. Limits:30 seconds CPU,60 seconds elapsed,
256 MiB maximum self RSS,4096 maximum checks. The producer uses the process
CPU limit plus elapsed/RSS guards between bounded operations. A parent
supervisor may enforce the wall bound externally; the producer does not
claim to interrupt an unreturning library call at an exact wall deadline.
No heavy remote job, other-Mac access, software installation or credit use.

Before a run, --freeze creates the previously absent fixed-name freeze with
the exact protocol, producer and cited-input hashes plus this entire numeric
contract. --run verifies all identities and refuses an existing result path.
--output accepts only the fixed new result file in this directory and uses
exclusive creation. Without --output the full result goes to stdout. The
freeze and result are never overwritten. A technical failure returns a
failure packet; no successful-physical-result flag follows from execution.

All of these remain false even if every arithmetic check passes: physical
volume mapping qualified; source equals metric strain; gravity derived;
vacuum density predicted; passive quartic continuum derived; native state
formation for galaxies qualified; observational validation; Stage3 complete.

## Immutable resident inputs

- ../recovered_sources/BS_MICRO_ACTION.md:
  00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec
- record_addition_compute.py:
  4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10
- NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md:
  fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b
- NATIVE_SOURCE_BRIDGE_DECISION.md:
  c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a
- NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md:
  335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c

The current protocol and producer are pinned by the exclusive prospective
freeze. Their mutable pre-freeze development status must not be mistaken
for an already authorized/executed scientific artifact.
