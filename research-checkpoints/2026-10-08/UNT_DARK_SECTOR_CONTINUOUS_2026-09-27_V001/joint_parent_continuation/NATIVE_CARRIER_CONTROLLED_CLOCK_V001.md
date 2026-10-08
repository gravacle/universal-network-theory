# An active record clock coupled to moving matter

2026-10-03 UTC. Source-level continuation of the finite geometry results.
No new evolution, parameter fit or physical clock adoption. The earlier
continuing-writer clock remains a constructive result; the new issue here
is the carrier-controlled record term that its explicit example omits.
The exact clock equation contains a carrier-weighted coherence and a
transport current. Positive conditional frequencies alone do not guarantee
a monotone phase for an unresolved mixture.

## The prior result and the actual additional interaction

NATIVE_ACTIVE_RECORD_LOCALITY_AND_CLOCK_V001.md proves a finite-window
continuing-writer clock on a supplied bounded-degree graph, with writer
copying active, carrier-to-record and fragment copying off. Its clock is
B_d, not the held A raising operator. The finite-region experiment instead
uses one active site with writer and carrier copying both present during
the pulses, plus a selected fragment. It then removes these copy ports.
Their two physical protocols and clock statements must remain distinct.

Use inherited generator units x=tau/hbar, record occupation r, site0 carrier
projector P=P0, local degree d=d0 and conventional record Pauli matrices.
At declared initial degree2 the prior dressed clock is

    B=(Z-iY)/2,    [X,B]=2B,    ||B||=1.

During a fixed active pulse, write the COMPLETE Hamiltonian as

    H=H_gc+(1-d/2)r+(1+P)X+H_fragments+lambda*r*X_b.

H_gc retains the graph flip, all diagonal degree/incidence energy, carrier
storage/current-square energy and hopping. No absolute energy is removed
from the physical ledger. Only the displayed commutators allow terms to
drop out of these specific derivative equations. A switched lambda still
has its full switching work; this derivation is inside a constant pulse.

Define R=-(d-2)[r,B]/2+lambda*[r,B]*X_b. Since graph, carrier, record
and fragment operators act on distinct registers,

    [H,B]=2B+2PB+R.

For beta=<B> and q=<PB>, exact evolution is

    beta'=2i*beta+2i*q+i<R>,
    q'=4i*q+<J0 B>+i<P R>,
    J0=i[H,P0]
      =-i*t_hop*sum_(v adjacent possible to0)
           n_0v*(|v><0|-|0><v|).

The actual incidence is an operator; no static graph or mean link is used.
All other terms commute with P0. In deriving q', use P0^2=P0; the native
carrier hopping supplies the new clock-weighted current <J0 B>. Replacing
q by <P0>*beta or that current by <J0>*beta is an additional closure, not
an identity. The active-copy marginal-closure obstruction was already known;
these equations identify its concrete clock and transport variables.

The old selected-bit degree bound can control the degree part of R on
its stated preparation. It does not make 2PB or the fragment contribution
small as N increases. Thus the prior writer-only frequency certificate is
not automatically a certificate for this larger active-copy mechanism.

## Exact control showing the unresolved phase problem

This is a separate analytical control, NOT a replacement for the actual
moving-carrier dynamics: freeze d=2, turn incidence flips and carrier
hopping off, set lambda=0, and leave writer and carrier recording active.
Take the record initially blank and the carrier diagonal with probability
p at site0 and1-p elsewhere. Retain all its diagonal storage/current energy;
it does not change the following reduced record expectation.

Conditional on P=0 or1, B has frequency2 or4 respectively. Nevertheless
the unconditioned coherence is exactly

    beta(x)=[(1-p)*exp(2ix)+p*exp(4ix)]/2
           =exp(3ix)*[cos(x)+i*(2p-1)*sin(x)]/2.

Where beta is nonzero its phase rate is

    nu_B=3+(2p-1)/(cos(x)^2+(2p-1)^2*sin(x)^2).

For example p=2/5 gives |beta(pi/2)|=1/10 and nu_B(pi/2)=-2, while
the initial rate is14/5. More generally at x=pi/2 the rate is negative
for1/3<p<1/2. At p=1/2 the amplitude instead vanishes there. For p=0
and1 the respective rates are the expected2 and4. No numerical run or
selected fitting parameter is needed: the whole p-family is explicit.

This counterexample rejects the proposed universal inference that positive
conditional gaps make the unresolved record phase monotone. It does not
claim a reversal in an uncomputed active finite-region history. It does
not invalidate the prior writer-only clock, a carrier-resolved clock, a
finite-window state-qualified readout, or any physical direction of time.

## Relocating the carrier changes the clock

Introduce a fresh degenerate position pointer initialized at vertex u and
ideally SWAP its state with the carrier. The old carrier correlations move
into the retained pointer. The graph, record and fragment marginal stays
unchanged; the new carrier is at u. For one carrier, the complete bulk work is

    W_swap(u) = -<H_hop>
      + j*[<d_u>-sum_(edges ab)<n_ab*(P_a+P_b)>]
      + delta_(u,0)*<X_r>-<P0*X_r>.

The first two terms were already derived for a larger graph in
NATIVE_TWO_HOP_CORRELATION_GEOMETRY_V001.md. Only the last, active
carrier-record term is new here. All graph, writer, record, feedback and
fragment energies are unchanged in this ideal instantaneous intervention;
carrier storage is unchanged because its number remains one. Pointer
degeneracy does not supply its preparation, finite-duration controller or
reuse for free. Work is signed, not necessarily a positive cost in every state.

Although beta is unchanged, q_new=delta_(u,0)*beta. R acts on the unchanged
environment marginal. Consequently the immediate unperturbed-H derivatives
before and after the ideal intervention obey

    beta'_new-beta'_old=2i*[delta_(u,0)*beta-q_old].

The old copying-off SWAP clock identity is therefore not valid with this
interaction active. A post-SWAP probe measures the newly prepared system,
not the original matter trajectory. This is no erasure or postselection, but
it is still a physical intervention requiring a supplied apparatus.

## Reading position without relocating it

For binary position P=P0, Q=I-P, an ideal retained pointer can produce
branch states with real overlap eta in [0,1]. Its reduced-system channel is

    D_eta(rho)=P*rho*P+Q*rho*Q+eta*(P*rho*Q+Q*rho*P).

This is a proposed measurement instrument, not an extra native interaction.
With zero pointer self-energy and the interaction switched off at its
boundaries, define H_star=-t_hop*sum_(edges incident0)n_e*T_e. Every other
term of the present H is block diagonal in P, hence the exact bulk change is

    W_read=(eta-1)*<H_star>.

The pointer retains the missing coherences globally. The quantities beta,
q, p=<P>, <R> and <PR> are unchanged at the intervention. In particular its
immediate beta' is unchanged, unlike SWAP. However <J0 B> becomes
eta*<J0 B>, so the subsequent joint clock and carrier motion generally differ.
This is not a nondisturbing observation of an unchanged future trajectory.

For p>0, let b_P=q/p describe the conditional record expectation in the
instantaneous P sector of an unmeasured evolution. Its exact equation is

    p'=<J0>,
    b_P'=4i*b_P+i*<PR>/p+<J0 B>/p-(p'/p)*b_P.

Resolving a sector does not remove its incoming and outgoing coherence.
A partially distinguishing pointer with eta>0 does not by itself realize
this exact P-conditioned ensemble; q/p is the mathematical present-sector
conditional expectation, not a claim about that pointer's outcomes.
A one-time pointer labels the carrier's position at the readout, not its
position at every later age. Repeated fresh projective readouts are a
different dynamics: for constant bounded H and K=||QHP||, the probability
of a sector change in one interval delta_x from a sector-supported state
is at most K^2*delta_x^2. Summing over T/delta_x intervals bounds the
probability of any recorded sector change by T*K^2*delta_x. The fixed-H,
continuous-readout limit suppresses transport across this boundary rather
than providing a free clock that follows the original transport. No such
monitoring experiment has been run or adopted as the cosmological model.
Hopping within Q can continue. On the full one-carrier possible-graph space
K^2=t_hop^2*N, not t_hop^2 times the supplied initial degree. The limiting
argument holds at fixed N; no uniform large-N monitoring limit is claimed.

## A distant reference clock with carrier recording still active

There is a constructive alternative to repeatedly measuring the carrier.
Use the previously proved prepared-graph locality bound while retaining
writer and carrier recording. Explicitly leave fragment ports off in this
clock protocol. Supply a definite bounded-degree graph G, a blank clock
record at vertex u with d_G(u)=2, and the carrier initially at v0 a graph
distance R away. This is a different preparation from the completed
six-node histories; no result for those histories is changed.

All couplings below use x=tau/hbar and inherited values g_wr=g_psi_r=1,
lambda_R=1/2, j=1/4, t_hop=1/2 and incidence flip Omega/N=1/N. The
selected-bit and locality bounds in NATIVE_ACTIVE_RECORD_LOCALITY_AND_CLOCK_V001.md
retain full incidence, record and carrier correlations. Let

    q_x=sinh(x/N),
    w_N(x)=sqrt[N*q_x^2+N*(N-1)*q_x^4],
    a_R(x)=exp[-mu*R+v_mu*x],
    v_mu=|t_hop|*D*sinh(mu).

The reference freezes incidence only in carrier hopping/current-square
terms; actual record feedback and recording remain active. If E_N(x)
bounds the full-state norm difference from that reference, its weighted
locality estimate and the triangle inequality give

    p_u(x) <= p_bar(x)=min(1,[a_R(x)+E_N(x)]^2).

Because P_u commutes with B and ||B||=1, |<P_u B>|<=p_u, without
factorization. Cauchy-Schwarz bounds the degree contribution by w_N/2.
Starting with beta(0)=1/2, define

    F(x)=2*p_bar(x)+w_N(x)/2,
    A(T)=integral_0^T F(x) dx.

Variation of constants and the exact commutator then imply

    |beta(x)-(1/2)*exp(2ix)| <= A(x),
    |nu_B(x)-2| <= F(x)/(1/2-A(x))   if A(x)<1/2.

Thus A(T)<1/2 and sup_[0,T] F(x)/(1/2-A(x))<2 are sufficient for a
nonzero, positively oriented whole-window reference phase. The disturbance
from carrier recording is controlled by its probability of reaching the
clock; no measurement freezes that motion and no record halo is inserted.
For fixed T, bounded degree and increasing supplied separation R, the
existing E_N and w_N bounds vanish with increasing N. This extends the
earlier writer-only clock certificate to a spatially isolated reference
with carrier recording active. It does not justify a clock colocated with
an appreciable moving-carrier population or a freely chosen fragment bath.

The reference is an expectation-level clock, not a single-shot classical
time variable. Existing writer modulation supplies quadrature readouts with
work delta_g*<X>; their calibration, uncertainty, repeated preparation and
synchronization remain requirements. A common distant reference does not
establish local gravitational time dilation or a physical speed of light.

## Fixed scalar evaluation of the sufficient bound

Before evaluating it, fix the following census. It evaluates six scalar
bounds, not any large Hilbert-space evolution. Use supplied bipartite cycles
C_(2N), D=2, T=1, mu=log(8), v_mu=63/16, R=d, where
d=ceil(log(N)/(2*log(2))) and the source-centered radius-d ball has at
most s=2d+1 vertices. Fix N=16,256,4096,65536,1048576,16777216.
These are proposed preparations; their complete physical energy and work
do not disappear when evaluating a scalar inequality.

Since each term is nondecreasing in x, a conservative endpoint bound is

    E_upper(T)=(3/4)*T*{
       sqrt[s*N*q_T^2+(s*N^2+N*s^2)*q_T^4]
       +N*8^(-d)*exp[(63/16)*T]},
    p_upper=min(1,[8^(-R)*exp[(63/16)*T]+E_upper]^2),
    F_upper=2*p_upper+w_N(T)/2,
    A_upper=T*F_upper.

The sufficient conditions are b_lower=1/2-A_upper>0 and
margin=2*b_lower-F_upper>0. A lower frequency bound is margin/b_lower.
Evaluate in ordinary double arithmetic and independently with 60-digit
decimal arithmetic, reporting differences with a fixed 1e-10 allowance.
That allowance is not directed-rounding certification. Do not alter the
six-point census, T or the inequalities after the results are known; failure
of this conservative certificate is inconclusive, not clock failure.

## Scope and next decision

This closes the ideal intervention algebra and offers a specific isolated
reference-clock construction, not an additional dark component, automatic
formation or observational validation. The earlier mixture counterexample
and held-phase failures stand. A viable reference instrument still leaves
physical ruler/volume, source normalization, formation, same-model galaxy
and expansion predictions and every observational lane open.
