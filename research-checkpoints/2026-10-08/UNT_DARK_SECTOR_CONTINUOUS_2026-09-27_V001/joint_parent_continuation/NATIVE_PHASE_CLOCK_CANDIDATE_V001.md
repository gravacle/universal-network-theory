# A writer-referenced native record phase as a local clock candidate

2026-09-28. Prospective analytical definition and saved-state test. This is one
explicit candidate to test, not an identification already contained in the
native Hamiltonian or a new choice of physical time, metric or positive state.

## 1. Owned observable and orientation

Retain the exact 16-state native preparation and held Hamiltonians in
RECORD_ADDITION_RESULTS.json. The writer-referenced raising observable is

    A=A_L+A_R,    A_i=|x><B|_i,
    K=A+A_dagger,    Y=-i*(A-A_dagger),
    a(w)=<A>_w=(<K>_w+i<Y>_w)/2.

Here Y has the inherited minus-Pauli-Y convention. The real copying source
is +gK, as in NATIVE_RECORD_PHASE_PATHWAY.md and the qualified writer pulses.
Choose A, not its adjoint, BEFORE examining the new phase rates. The positive
orientation is set by the owned positive record onsite energy epsilon_r=1.
No source phase is adjusted in time to make a signal advance.

On any interval on which a is nonzero, define the continuous phase lift phi
from a(w)=|a(w)| exp(i phi(w)), with phi(0)=arg a(0). The candidate elapsed
phase time is

    T_phase(w)=[phi(w)-phi(0)]/omega_ref,
    omega_ref=epsilon_r/hbar >0.                           (1)

The inherited units have hbar=epsilon_r=1. Equation (1) is a hypothesis about
a relational readout of the existing native evolution; it does not derive
physical seconds or assume that this phase is the clock T of the covariant
comparison action. A constant change of writer phase shifts phi by a constant
and leaves (1) unchanged. A time-dependent writer rotation would change its
rate and is explicitly excluded.

## 2. Exact phase-rate and amplitude equations

The complete held Hamiltonian, with both record factors retained, is

    H=3I+R-X_a+(9/4-lambda_R R-X_C/2)*n,
    R=q_L+q_R.

Everything except (epsilon_r-lambda_R n)R commutes with A. Consequently

    [H,A]=(epsilon_r-lambda_R n)A,
    z(w)=<nA>_w,
    a_dot=(i/hbar)*(epsilon_r*a-lambda_R*z).               (2)

At nonzero a,

    phi_dot=Im(conj(a)*a_dot)/|a|²
           =epsilon_r/hbar-(lambda_R/hbar)*Re(z/a),
    partial_w |a|²=(2lambda_R/hbar)*Im(conj(a)*z).          (3)

These are actual-state identities. The complex conditional coherence z/a
is not a probability and need not lie between zero and one. Therefore the
positive operator epsilon_r-lambda_R n does NOT prove a positive phase rate.
For example, use the valid pure state

    sqrt(2/5)|n=0>|minus>_L|B>_R
       +sqrt(3/5)|n=1>|plus>_L|B>_R,
    |plus/minus>=(|B>+/-|x>)/sqrt(2),

with the same spectator carrier content. It has a=1/10, z=3/10 and the
native instantaneous phase rate -1/2. This is an analytical counterexample
to a universal positivity inference, not the stored prepared state or a new
preparation being run. The actual prepared state must be evaluated.

## 3. Exact finite spectrum, retaining all bands and degeneracies

For record count R, carrier-X eigenvalue s=+/-1 and link branch beta=+/-1,

    x_Rs=9/4-lambda_R R-s/2,
    d_Rs=sqrt(x_Rs²+4),
    E_Rsbeta=3+R+(x_Rs+beta*d_Rs)/2,
    P_Rsbeta=P_R [I-beta*(2X_a+x_Rs Z_a)/d_Rs]/2
                    *[I+sX_C]/2.

P_R has ranks 4,8,4 before the two other projectors; the full energy-sector
projector ranks are 1,2,1. They resolve the full 16-dimensional identity.
For each R=0,1, both s and both initial/final link bands, define all 16 lines

    c_l=<psi_formed|P_(R+1,s,gamma) A P_(R,s,beta)|psi_formed>,
    d_l=<psi_formed|P_(R+1,s,gamma) nA P_(R,s,beta)|psi_formed>,
    omega_l=[E_(R+1,s,gamma)-E_(R,s,beta)]/hbar.

Then exactly

    a(w)=sum_l c_l exp(i omega_l w),
    a_dot(w)=sum_l i omega_l c_l exp(i omega_l w),
    z(w)=sum_l d_l exp(i omega_l w).                        (4)

No negative-frequency line, upper band, small coefficient or degenerate
sector is dropped. Analytic projectors make the result independent of
arbitrary eigenvectors inside the count-one degeneracy. Equations (2) and
(4), plus direct full-matrix evaluation, give independent consistency checks.

Zeros of a make the candidate phase undefined. Even without zeros, beating
can make Im(conj(a)*a_dot) change sign. Nonzero addition gaps alone do not
exclude either outcome. Conversely, a sum of several lines can retain a
strictly positive phase rate on the entire declared window; a single pure
frequency is not required for a useful local candidate.

## 4. Two exact controls and one prospective decision

All three saved preparations remain in the census:

* Native formed state: lambda_R=1/2; no phase rate sign is presupposed.
* Feedback-off formed state: lambda_R=0. Equation (2) gives exactly
  a(w)=a(0) exp(iw). Its saved formation has nonzero a(0), so its phase rate
  is exactly +1 and amplitude constant. This is a control, not evidence that
  record-incidence feedback is necessary for phase coherence.
* Copying-off blank-record control: its held state stays entirely in R=0,
  while A maps R=0 to R=1. Thus a(w)=0 for every w and no phase clock is
  defined. Numerical noise must not be unwrapped into a purported phase.

Use the inherited ages {0,.25,.5,1,2} and the full interval [0,2]. A narrow
prospective success means that the NATIVE state has nonzero signal and a
strictly positive phase rate on this entire interval. A wholly negative
orientation would be reported as such, not repaired by replacing A by its
adjoint. Failure of a sufficient bound is reported as unresolved unless an
actual zero/reversal is independently established. Any outcome concerns this
specific state/readout/window, not all possible network clocks.

## 5. Continuous-window bounds rather than selected samples

From the unaltered coefficients in (4), define

    M_k=sum_l |c_l|*|omega_l|^k, k=0,1,2,
    N_phi(w)=Im(conj(a)*a_dot).

The exact triangle bounds imply

    |a_dot|<=M_1,
    |N_phi_dot|=|Im(conj(a)*a_ddot)|<=M_0*M_2.

On uniform endpoint grids covering [0,2] with respectively 512 and 1024
intervals, every time is within Delta_w/2 of a grid point. With the fixed
numerical allowance eta=1e-10, compute

    A_low=min_grid |a|-M_1*Delta_w/2-eta,
    N_low=min_grid N_phi-M_0*M_2*Delta_w/2-eta,
    N_high=max_grid N_phi+M_0*M_2*Delta_w/2+eta.            (5)

Positive orientation is certified under this numerical error allowance only
if A_low>0 and N_low>0. Negative orientation similarly requires A_low>0 and
N_high<0. A conservative positive-rate lower bound is
N_low/(M_0+eta)². More generally, when A_low>0 the signed rate bounds are
min(N_low/A_low²,N_low/(M_0+eta)²) and
max(N_high/A_low²,N_high/(M_0+eta)²). Neither 512 nor 1024 is a new physical observation window:
they certify the SAME interval between the five inherited ages. Retain both
resolutions even if the coarser bound already resolves the sign.

The Lipschitz statements are analytic. The eta treatment is an explicit
numerical error model, corroborated by inherited-tolerance crosschecks, not
a claim that ordinary double arithmetic is directed interval arithmetic.
No unresolved near-zero case is declared positive by a branch convention.
Where the lower amplitude bound exists, M_1*Delta_w/A_low<pi is a sufficient
check that neighboring phase samples cannot hide an additional winding.

## 6. The smallest saved-state calculation and the remaining calibration

The worker uses only authenticated old formed vectors, their owned matrices
and the old pulse readouts. It does not repeat formation, add a pulse, search
parameters, enlarge the lattice or extend hold ages. At each inherited age
it reports a,z,a_dot, amplitude, N_phi, phase rate and continuously lifted
phase. It checks both spectral and original-commutator expressions and
compares full-matrix eigensolver and scaled-Taylor readouts. The existing
pulse values of K and Y provide an additional saved-data identity.

The mathematical Y readout has an owned operational link: the already
qualified plus-K pulse has delta<R>=delta_g*tau*<Y>/hbar+..., while its
switch work reads K. No unreported independently rotated Y port is assumed
to have been implemented. Turning that into a physical phase measurement
still needs the source strength, timing, quadrature sensitivity and writer
reference calibrated together, with the complete switching work retained.

A local phase that passes (5) could supply a definite native record-based
clock observable with a calculable state-dependent rate. It would not yet
fix its physical seconds, the source-to-metric map or a covariant kinetic
term. In particular, a spacetime clock must also have a smooth timelike
gradient and compatible spatial phases/constraints; monotonicity in the
native evolution parameter alone does not establish that. The full coupled
comparison action and its actual-state/volume matching remain separate.

This advances a precise part of the native bridge: test whether the SAME
records whose source response was measured also supply a nonvanishing,
oriented phase reference. No positive phase, free clock function, added dark
population, new vacuum constant or arbitrary physical conversion is inserted.
