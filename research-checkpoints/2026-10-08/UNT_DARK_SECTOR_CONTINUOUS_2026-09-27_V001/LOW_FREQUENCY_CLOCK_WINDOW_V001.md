# A native frequency window, without discarding the upper population

2026-09-27. Exact analytical continuation after resident checks and complete
reads of `NATIVE_TWO_CHANNEL_CLOCK_SCREEN_V001.md` and
`TWO_BAND_ANALYTICAL_BRIDGE.md`. No new Hamiltonian parameters, preparation,
damping, cooling, simulation, population projection or metric assignment.

**Result.** The fixed native parameters DO admit an observable frequency
window containing both lower carrier lines and none of the upper or
interband carrier lines. This statement survives the unconditioned q mixture
and the full 13.05% upper population. A finite observation has a precisely
computable relative response error; upper population alone cannot determine
that error. The window supplies only one clock gap per q sector, and the
bare link supplies no second oscillating clock there. A common low-frequency
clock is consequently a possible restricted description, not an established
universal physical clock.

## 1. Exact line isolation in the frozen native model

Keep h=1, j=1/2, b_0=9/4, b_1=7/4. Write

    L_q=nu_L(q), U_q=nu_U(q),
    F_q=omega_lo(q), G_q=omega_hi(q).

The inherited radicals give

    L_0=(4+sqrt(113)-sqrt(185))/8,
    L_1=(4+sqrt(89)-sqrt(145))/8,
    U_q=1-L_q,
    F_0=(sqrt(113)+sqrt(185)-4)/8,
    F_1=(sqrt(89)+sqrt(145)-4)/8,    G_q=F_q+1.             (1)

Their exact order is

    0<L_0<L_1<1/2<U_1<U_0<1<F_1<F_0<G_1<G_0.            (2)

The previously established detuning monotonicity gives the within-band
inequalities. Each link gap is at least 2h=2, so F_q>=3/2>U_q.
The sum M(b)=d_+(b)+d_-(b) has 0<M'(b)<2 at these positive detunings;
therefore 0<F_0-F_1<1/2, which proves F_0<G_1. No carrier lines from
different q sectors coincide. q mixing creates additional distinct lines,
not a hidden upper-line overlap with the lower window.

Define the pass edge r=L_1 and stop edge u=U_1=1-r. Then

    u-r=(sqrt(145)-sqrt(89))/4>0.                          (3)

An ideal readout filter with cutoff 1/2 isolates BOTH lower lines exactly.
It acts on the measured signal; it does not project or renormalize the
quantum state. All upper energy and population remain in the full ledger.
An ideal sharp frequency filter requires an indefinitely long record; a
finite experiment must report its actual transfer function or estimator.

The q separation L_1-L_0 is much smaller than (3). A finite record may
separate low from high frequencies while failing to distinguish the two
lower q components. Their existing amplitudes must then be retained as an
unresolved mixture, rather than fitted as a single homogeneous clock.

## 2. Exact relative readout error, with actual formed-state coefficients

Aggregate spectator labels but retain the UNNORMALIZED q density blocks.
Use the known band matrix elements to write the exact bare carrier signal

    Z(t)=sum_(q,J=L,U,F,G)
           [c_(q,J) exp(-i omega_(q,J)t)+complex conjugate]. (4)

For instance |c_(q,L)|=|cos(delta_q) rho_(q,L+;L-)| and
|c_(q,U)|=|cos(delta_q) rho_(q,U+;U-)|; the two interband
coefficients carry |sin(delta_q)|. Complex conjugation conventions only
assign positive versus negative frequencies. The actual saved density
matrix fixes all coefficients and phases. Let

    C_L=sum_q |c_(q,L)|^2,
    C_H=sum_(q,J=U,F,G) |c_(q,J)|^2.                        (5)

If C_L=0 there is no lower oscillating clock in this readout, regardless of
its lower-band population. Otherwise its infinite-record mean-square norm
is 2 C_L because every positive line in (2) is distinct.

For any time-translation-invariant observation filter W(omega), the relative
mean-square error against the ORIGINAL lower component Z_L(t) is exactly

    E_W^2 = {
      sum_q |c_(q,L)|^2 |W(L_q)-1|^2
      +sum_(q,J=U,F,G)|c_(q,J)|^2 |W(omega_(q,J))|^2
             }/C_L.                                      (6)

Use a real symmetric filter, or W(-omega)=W(omega)* with its phase included
in the first term. This norm avoids dividing by an instantaneous oscillation
that crosses zero. It measures the oscillating probability component as
well, since P_R-1/2=-Z/2. It is a signal norm, not a state trace distance.
For pass error epsilon_p and stop leakage epsilon_s, (6) implies

    E_W^2 <= epsilon_p^2+epsilon_s^2 C_H/C_L.              (7)

Both low-band smearing and high-band leakage matter. Equation (6), evaluated
with the saved state, is the response-specific diagnostic still needed;
an upper occupation percentage cannot substitute for those coefficients.

There is also a sharper population-assisted bound on the numerator. For
eta=Tr(P_U rho), positivity of each density block gives

    C_H <= eta^2/4+sigma_max^2 eta(1-eta),
    sigma_max^2=max_q sin^2(delta_q)
                =[1-109/sqrt(12905)]/2.                   (8)

Indeed |rho_ij|^2<=p_i p_j; summing the upper intraband terms gives at most
eta^2/4, and summing the interband terms gives at most
sigma_max^2 eta(1-eta). The maximum mixing is at b_1, since
|theta_--theta_+| decreases with positive b>j. Bound (8) includes the
observable's small interband overlap. It gives no nonzero lower bound on
C_L, so it cannot alone promise a relative accuracy.

For the existing symmetric boxcar observation of duration T,
W_T(omega)=sinc(omega T/2), equation (6) becomes an exact finite-window
relative error. In particular, with xi=C_H/C_L,

    E_T^2 <= (r^2 T^2/24)^2+4 xi/(u^2 T^2).              (9)

The first term follows from |1-sinc x|<=x^2/6 and the second from
|sinc x|<=1/|x|. A declared pass tolerance epsilon_p and relative leakage
tolerance epsilon_h have a sufficient common window exactly when

    2 sqrt(xi)/(u epsilon_h) <= T <= sqrt(24 epsilon_p)/r. (10)

This is a sufficient bound, not a necessary restriction; the exact sinc
weights in (6) may be better. Sending T to infinity erases the lower
oscillation too, so mere waiting is not the proposed effective dynamics.

## 3. Finite-record extraction can separate the lines without cooling

A resolved response coefficient can instead be estimated over a finite
record. Let signed low frequencies be lambda={+L_0,-L_0,+L_1,-L_1}, with
signed high frequencies kappa consisting of the other twelve values.
For centered observations t in [-T/2,T/2], write their actual complex
coefficient vectors as a and b. Define

    G_ij=sinc[(lambda_i-lambda_j)T/2],
    K_ij=sinc[(lambda_i-kappa_j)T/2].                       (11)

Least-squares extraction using all FOUR signed low functions, but omitting
the high ones, gives exactly

    a_hat-a=G^(-1)K b,
    E_extract^2 = b^dagger K^dagger G^(-1)K b
                         /(a^dagger G a).                 (12)

Distinct finite exponentials make G positive definite for T>0; small T can
still make inversion poorly conditioned. Equation (12) is the relative
mean-square error of the reconstructed lower waveform ON THAT RECORD.
The denominator is zero only for no lower signal. A different record center
changes coefficient phases and must be included. Every low-high matrix
element has |K_ij|<=min(1,2/[T(u-r)]), while G approaches I as all distinct
low differences are resolved. Thus the upper leakage converges to zero
without reducing its population, at a cost in observation time and noise
conditioning. This is retrospective spectral measurement, not instantaneous
local equilibration or a new propagation equation.

## 4. What clock claim survives this window?

For one fixed q the retained lower carrier block is two dimensional, with
one nonzero gap L_q. Its spectrum can always be written as a scalar offset
plus (L_q/2) times a fixed two-level generator after an identified basis
choice. Therefore a rate factor L_q/L_0 is compatible with this restricted
spectral description. That compatibility is automatic for a single gap.
The q-dependent observable dressing, amplitudes, formation state and
retained population still have to be transformed consistently; arbitrary
bare readouts do not thereby become pure time-rescaled copies.

The independent bare link observable n preserves carrier parity and has
only interband oscillation frequencies d_(q,+/-), all at least sqrt(89)/4,
apart from its static population contribution. It supplies NO second free
oscillation in |omega|<1/2. Its stationary low-frequency susceptibility is
an off-resonant analytic response, not another clock pole. Actual coherent
formation can also make a driven response depend on the preparation time;
stationarity must not be assumed from this frequency selection.

Consequently the present one-carrier block cannot nontrivially verify a
common lapse for two independent clocks inside this window. Identical
carrier contents follow the known content symmetry, rather than furnishing
two independent intrinsic clock gaps. Including the existing upper clock
reinstates the already-proved failure of pure common rate scaling.

The minimal same-parent next test is concrete: extract the formed-state
coefficients in (4), evaluate (6) or (12) for the declared observation, and
jointly check the link and carrier response poles AND residues under their
existing probes. A stronger restricted common-clock claim then needs an
independently specified accessible composite with a second intrinsic gap
and the same source-dependent rate ratio. No such second low-frequency
clock, physical ruler or universal geometry has been produced by selecting
the first clock's spectral window.
