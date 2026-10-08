# Complete energy source response with active records at finite density

2026-10-03 UTC. This advances the next test in frontier V114. On the SAME
prepared regular-graph family, the complete normal energy source has a
nonzero native response with active carrier recording. Its sign cannot be
inferred from the carrier kinetic energy alone. A local expectation bound
also qualifies a finite-time, fixed-density comparison with the full changing
incidence model. This is more than a limit of isolated Taylor coefficients.

The graph, initial population, normal spatial embedding and external source
are still supplied. The result is not an endogenous gravitational field,
a reversible cubic work law, BTFR, expansion or an observational pass.
No numerical job, fitted parameter, new microscopic interaction or physical
calibration is used. Internal algebra review is not external peer review.

## Complete source and the declared preparation

There are N vertices in each BS layer, V=2N in total, and N^2 potential
incidence bits. Let eta_v be +1 on the first layer and -1 on the second.
Prepare a definite balanced bipartite d-regular G, the uniform carrier
density I_Q/binom(V,Q) in one fixed-content hard-core sector, blank records,
uniform occupied same-content writers and invariant blank fragments.
This is the preparation of the preceding population note, not free-band
filling, a ground state or a derived formation process. Write x=tau/hbar.

Use EXACTLY the previously owned node allocation h_v in
NATIVE_ACTIVE_RECORD_MECHANISM_AND_STATE_V001.md. The conditional normal
lapse chart is L_v=1+alpha*eta_v, |alpha|<1, so

    H_alpha=H+alpha*F,    F=sum_v eta_v*h_v.                  (1)

This chart is the normal component of the proposed split-position energy
source. Its spatial ruler and the production of alpha by matter are not
derived here. The source is dimensionless; F has microscopic energy units.

The symmetric edge storage, hopping and flip allocations cancel from F
because their endpoint signs sum to zero. They remain in H. The current
allocation gives j*n_uv*(eta_u*p_u+eta_v*p_v): the pair interaction cancels
from this dipole, NOT from the Hamiltonian. With delta_d=epsilon_r-lambda_R*d,
delta d_v=d_v-d, and occupied writers w_v=1, define the bounded onsite operator

    A_v=(epsilon_psi+j*d)*p_v+epsilon_w
              +delta_d*r_v+(g_w+g_p*p_v)*X_v.

The full source is exactly

    F=F_G+U_d*sum_v eta_v*(delta d_v)^2
             +sum_v eta_v*delta d_v*(j*p_v-lambda_R*r_v),
    F_G=sum_v eta_v*A_v.                                    (2)

The term linear in delta d in the degree energy cancels since
sum_v eta_v*delta d_v=0 as an operator. The initial degree and writer
constants cancel between equal layers. They have not been removed from
absolute energy or from other spatial source components.

The frozen-G NODE comparison is

    H_G=E_G+sum_v[epsilon_psi*p_v+epsilon_w
                       +delta_d*r_v+(g_w+g_p*p_v)*X_v]
                       +sum_(uv in G)[j*C_uv-t*T_uv],
    C_uv=p_u+p_v-2*p_u*p_v.                                 (3)

All record dynamics and hard-core carrier interactions remain in (3).
It is a comparison justified below, not a replacement of actual incidence
by its mean. Put K=-t*sum_G T_uv and S=sum eta_v*p_v. Exactly,

    [H_G,F_G]=[K,sum_v eta_v*p_v*(epsilon_psi+j*d+g_p*X_v)]. (4)

Thus the energy source current includes record operators. It is not merely
a constant multiple of the sublattice carrier current.

## A local finite-time bound without dilute carriers

For the proof keep the complete graph degree/storage/flip Hamiltonian
H_inc and set H_ref=H_inc+H_node,G. The two reference factors commute.
The node factor retains all onsite copying and bounded-degree interactions.
At alpha=0 the difference from the ACTUAL Hamiltonian is

    H-H_ref=sum_e Delta n_e*W_e,
    Delta n_e=n_e-n_e(G),
    W_e=j*C_e-t*T_e-lambda_R*(r_u+r_v).

Only native incidence flips change a selected bit. The previously proved
Dyson parity bound, valid for the full dynamics, gives

    <Q_e>_s <= q_s^2,   <Q_e Q_f>_s <= q_s^4 (e!=f),
    Q_e=(Delta n_e)^2,   q_s=sinh(|Omega|*s/N).               (5)

No independence of bits or of carriers and records is assumed.
For a node-only observable O_X with support X, exact Heisenberg interpolation
expresses its full/reference difference as the integral of expectations
of i*Delta n_e*[W_e,O_G(T-s)] in the ACTUAL evolved state. Crucially,
Q_e commutes with this node commutator, and Delta n_e=+/-Q_e, so

    |<Delta n_e*[W_e,O_G]>| <= <Q_e>*||[W_e,O_G]||.          (6)

The probability q_s^2, rather than its square root, controls this expectation.
The estimate does not claim global-state trace-norm convergence.

Let D bound the initial graph degree, b=|j|+|t| and
ell=b+2*|lambda_R|. Removing onsite evolution in an interaction picture
preserves support and edge norm b. The commutator-chain bound is

    sum_(all potential e) ||[W_e,O_G(u)]||
           <=2*ell*||O_X||*|X|*N*exp(4*b*D*u).

One way to verify the count is to sum the commutator recursion first over
reference edges. There are at most D*|X| initially touching edges and at
most 2D reference edges touching any edge, giving the exponential above.
Each reference edge touches at most 2N potential edges; the initial
potential-edge sum is at most 2*||O_X||*N*|X|. Integrating the reference-edge
recursion yields the stated potential-edge sum. This argument is in the
full local hard-core tensor-product algebra before restriction to Q.

Consequently

    |<O_X(T)>_full-<O_X(T)>_ref|
       <=2*ell*||O_X||*|X|*N
                   *integral_0^T q_s^2*exp[4*b*D*(T-s)] ds
        =O_T(1/N).                                         (7)

This holds for any initial node density, including the correlated fixed-Q
mixture. H_inc retains its possibly large degree-energy spectrum; its norm
was never used as a small parameter. T and D are fixed in this limit.

For (1), the endpoint averages of L remain one, so the actual flip and
hopping amplitudes do not change. Alpha*F_G is onsite. Uniformly for
|alpha|<=alpha_bar<1, replace ell by

    ell_bar=b+2*|lambda_R|+alpha_bar*(|j|+|lambda_R|).

The difference operator is explicitly
W_e,alpha=W_e+alpha*eta_u*[j*(p_u-p_v)-lambda_R*(r_u-r_v)].
The same proof accommodates bounded, prescribed time-dependent alpha(s),
with its graph and node reference propagators both time dependent.

## The complete source and source work are intensive on this interval

Let ||A_v||<=a_D, uniformly in N, and

    w_N(T)^2=N*q_T^2+N*(N-1)*q_T^4.

Equation (5) bounds <(delta d_v)^2> by w_N^2. Since node operators commute
with incidence projectors, their linear wrong-degree expectation is bounded
by their norm times N*q_T^2. Applying (7) to each A_v in (2) gives

    |<F(T)>_full-<F_G(T)>_node,alpha|/V <= E_N(T),
    E_N(T)=|U_d|*w_N(T)^2+(|j|+|lambda_R|)*N*q_T^2
       +2*ell_bar*a_D*N*integral_0^T q_s^2*exp[4*b*D*(T-s)]ds
       =O_T(1/N).                                         (8)

The comparison includes graph storage and record feedback. No source term
has been thrown away because its initial expectation vanishes.
For a finite-variation source history, the exact controlled-source work is
W=integral <F> d alpha, including switches. Its per-node full/comparison
error is at most total_variation(alpha)*sup_(s<=T) E_N(s).

These are finite-source expectation and work bounds. Uniform convergence
of real-source functions alone does NOT prove convergence of their source
derivatives or of connected fluctuations. Such exchanges are not asserted.

An actual infinite-size node limit additionally requires a locally convergent
SUPPLIED graph family, for example periodic honeycombs of increasing linear
size. For Q/V->rho, finite-site marginals of I_Q converge to independent
Bernoulli occupation with probability rho. Bounded local interactions and
the same commutator bound then yield a finite-time local limit. No physical
volume or graph-formation conclusion follows from this per-declared-node limit.

## A common small operational-clock interval

Use the SAME fixed readout as the prior work,

    B_d=[(delta_d*X+2*g_w*Z)/Delta_d-i*Y]/2,
    Delta_d=sqrt(delta_d^2+4*g_w^2),    beta_0=g_w/Delta_d.

For positive inherited copy coefficients, the reference initial rate at
clock site w is

    nu_alpha(0)=(1+alpha*eta_w)*Delta_d*(1+g_p*rho/g_w).     (9)

The full commutator is the reference local commutator plus
-(1+alpha*eta_w)*lambda_R*delta d_w*[r_w,B_d]. Thus both the amplitude
and its first time derivative converge to their node-reference values:
(7) controls the bounded node parts, and N*q_T^2 controls the extra term.

There is a fixed small interval independent of N with a nonvanishing clock.
For clarity, let M1,M2 be uniform reference bounds on |dot beta| and
|ddot beta|, and nu_min,nu_max positive bounds on (9) over the chosen source
and filling range. Such bounds follow from one onsite and its D neighboring
bounded interactions; they do not use the full Hamiltonian norm. A sufficient
choice is

    T_* <= min{beta_0/(2*M1),
               beta_0*nu_min/[4*(M2+nu_max*M1)]}.

Then |beta_ref|>=beta_0/2 and nu_ref>=nu_min/2 on [0,T_*]. For sufficiently
large N the full floors are at least beta_0/4 and nu_min/4 on that interval;
the exact boundary floors of the reference are not automatically transferred.
This bounded-second-derivative certificate is for constant-source segments,
not an assertion of a smooth rate across arbitrary source jumps.
On a smaller common phase interval, inverse clock times
and <F>/V converge with O(1/N) error. This uses the bounded reference
source-mean derivative as well as the clock comparison. It is not a
long-time synchronization theorem, a single-shot apparatus or SI calibration.

For a constant alpha the two source protocols really are the same under
this endpoint comparison. For a time-dependent source, holding its external
age schedule fixed and holding its measured-phase schedule fixed are
different protocols and must not be interchanged.

## Complete two-time response of the actual prepared node state

Take the node limit only as qualified above, or first calculate at finite G.
The PLUS-source convention is

    chi_FF(x,y)=i*< [F_G(x),F_G(y)] >,
    delta<F_G(x)>=-integral_0^x chi_FF(x,y)*alpha(y)dy.

For m=d*V/2 edges and c=2*Q*(V-Q)/[V*(V-1)], the new leading result is

    chi_FF(x,y)=-(2/3)*c*m*t^2*delta_d*g_p^2
                    *(x-y)*(2*x^2-x*y+2*y^2)+O_5(x,y).     (10)

O_5 means total time degree at least five for the frozen node model. Local
commutator counting controls each fixed-order coefficient per node uniformly
on bounded-degree families. Explicitly let a=sup_v ||A_v|| and
kappa=sup_v (||h_v,onsite||+sum_(e touching v)||h_e||). A nested commutator
starting onsite has a sum-of-term norm at most a*(2*kappa)^n*n!, with
support at most n+1 sites per term. The second F insertion intersects only
that support. In i*<exp(iHy)[F(x-y),F]exp(-iHy)>, summing both expansions
gives the normalized majorant

    2*a^2*sum_(l>=0) (l+1)*[2*kappa*(|x-y|+|y|)]^l.

Thus a sufficiently small common time neighborhood has a uniform remainder.
Real matrices/preparation make the kernel odd under (x,y)->(-x,-y).
This statement is not an unproved derivative-limit claim for the full parent.

Here is a reproducible local algebra check. At cubic order the carrier trace
requires two hops on the SAME edge. Conditional on unequal occupations,
the carrier on that edge is I/2. Use its Pauli Xc,Yc,Zc and write

    H_local=A+Zc*B-t*Xc,       F_local=C+Zc*E,
    A=delta_d*(r_1+r_2)+(g_w+g_p/2)*(X_1+X_2),
    B=(g_p/2)*(X_1-X_2)+b_s*I,
    C=delta_d*(r_1-r_2)+(g_w+g_p/2)*(X_1-X_2),
    E=epsilon_psi+j*d+(g_p/2)*(X_1+X_2).

The spectator/current detuning b_s cancels; it has not been set to zero.
Put C1=[H_local,F_local], D1=[H_local,C1], E1=[H_local,D1]. In the
carrier I/2 and blank-record state, directly

    C1=2*i*t*Yc*E,
    <[C1,D1]>=-4*t^2*delta_d*g_p^2,
    <[E1,F_local]>=-8*t^2*delta_d*g_p^2.

Inserting these into
(x^3-y^3)<[E1,F_local]>/6-x*y*(x-y)<[C1,D1]>/2 gives (10).
Different-edge two-hop paths have zero diagonal carrier trace. The factor
c*m is the exact fixed-Q probability sum, not an independence assumption.

Three exact comparison controls prevent a favorable-sign substitution:

- At g_p=0, chi_FF is zero for ALL two times in (3): the carrier is the
  identity in its conserved sector and local record energies commute.
- At t=0, F_G commutes with H_G for every state.
- At delta_d=0 with active copying, each X_v is conserved. Resolving their
  eigenvalues leaves a carrier identity in every record block, so the
  source commutator trace vanishes at all times, even under prescribed
  normal-source histories. This last null is for the stated mixture and
  frozen-node comparison; changing native degrees can evade it at finite N.

## Fixed-clock signal and complete pulse work

Require an ACTUAL automorphism of G exchanging its layers and preserving
the preparation, as on the stated periodic honeycomb. Balanced regularity
alone does not imply this. Then <F_G> at alpha=0 is identically zero.
The fixed-clock linear-response correction proportional to dot<F_G> is
therefore zero, although the clock response itself is not zero.

For a constant small source switched on at zero, (10) integrates to

    (1/V)*partial_alpha <F_G(x)>|_0
       =(2/3)*d*[V/(V-1)]*rho*(1-rho)*t^2*delta_d*g_p^2*x^4
                                                         +O(x^6). (11)

At inherited d=3, t=1/2, delta_d=-1/2, g_p=g_w=1, in the qualified
fixed-density node limit this is -rho*(1-rho)*x^4/4. In elapsed clock
phase Theta it becomes

    partial_alpha f(Theta)|_0
       =-4*rho*(1-rho)*Theta^4/[289*(1+rho)^4]+O(Theta^6),
    f=<F_G>/V.                                             (12)

The sign is opposite to the positive kinetic onset in the preceding note.
There is no contradiction: the complete source includes record and current
energies. This is a driven, nonstationary response, not proof of equilibrium
passivity, a static susceptibility or the required soft spectral measure.

The finite-source full-parent values and clock endpoints approach this node
response by (8)-(9). A rigorous linear-response reading takes N->infinity
at fixed finite source first, then differentiates the locally defined node
limit. It does not silently exchange those operations on the finite-N Kubo
kernel. A finite-source difference at fixed N inherits error O(1/(N*|alpha|)).

For a square pulse, switch alpha on at zero and off at a specified T. The
complete source switching work is EXACTLY

    W=alpha*<F>_initial-alpha*<F>_alpha(T)
      =-alpha*<F>_alpha(T).                                (13)

All baseline and storage energies remain in this equality. At fixed T,
layer-exchange symmetry makes W even in alpha. In the same node limit,

    W/V=-(2/3)*d*rho*(1-rho)*t^2*delta_d*g_p^2*alpha^2*T^4
                               +O(alpha^2*T^6)+O_T(alpha^4).

At inherited degree three this is positive alpha^2*rho*(1-rho)*T^4/4.
If switch-off is instead at one endpoint clock's ACTUAL elapsed phase,
the leading coefficient is
4*alpha^2*rho*(1-rho)*Theta^4/[289*(1+rho)^4]. An alpha^3 correction
can then occur because that clock's endpoint changes with the source;
the fixed-T evenness must NOT be transferred to this different protocol.
The coupling work is energy supplied by the controller, not free extraction
or an uncounted thermal reservoir. Apparatus preparation/readout costs are
additional obligations, not claimed zero by (13).

For the affine chart H_alpha, F is the source-conjugate readout and has no
bare alpha contact. A different readout, such as sum eta_v*L_v*h_v=F+alpha*H,
has an explicit contact <H>. Such a coordinate-energy readout must not be
silently identified with F. The source-work calculation used (1) throughout.

## A matter intervention must actually change this prepared state

There is an exact preparation constraint on the next endogenous-source test.
Any carrier-only unitary preserving Q leaves I_Q/binom(V,Q) unchanged.
Thus a swap or coherent relocation of carriers applied at initial age zero
to this uniform mixture produces NO matter contrast. Running such a test
and interpreting its null as failure of gravity would test an unchanged
state. A physical inhomogeneity requires a different preparation or an
intervention after carrier and record correlations have developed.

One explicitly mathematical preparation tangent is

    sigma_epsilon=exp(epsilon*M)/Tr_Q exp(epsilon*M),
    M=sum_v m_v*p_v,    sum_v m_v=0.

It stays in fixed Q and is normalized there. At epsilon=0, its exact tangent
and initial occupation contrast are

    partial_epsilon sigma|_0=sigma_0*M,
    partial_epsilon <p_v>|_0
                 =rho*(1-rho)*V*m_v/(V-1).                 (14)

The covariance proof uses Var(p_v)=rho*(1-rho) and
Cov(p_u,p_v)=-rho*(1-rho)/(V-1) for different sites. On a regular graph,
the initial COMPLETE energy has zero first derivative for this zero-sum
tangent: storage is fixed by Q, blank record means vanish, and
Cov(sum_edges C_e,p_v) is independent of v, so its contraction with m_v
vanishes. This is not a zero-cost preparation theorem: higher energy changes,
entropy, correlations, normalization and a physical preparation apparatus
must still be accounted for. Equation (14) is a declared response direction,
not a generated matter profile or an adopted source law.

For a compact zero-sum profile supported on Y, the initial tangent of EVERY
observable outside Y is zero. In the uniform fixed-Q state its covariance
with p_v is the same for each v in Y, so sum_Y m_v=0 cancels it; record
marginals remain blank. This supplies a nonvacuous localized redistribution
direction for a spatial response calculation without silently importing an
instantaneous distant signal from the fixed-Q constraint. The possible
metric interpretation of its subsequent response remains to be tested.

For a pair a,b in a specified local region, choose M=p_a-p_b and the
number-preserving operator L=|10><01| on that pair. An EXACT finite local
channel, not a proposed dissipative evolution law, has Kraus operators

    K1=sqrt(eta)*L,    K0=sqrt(I-eta*L^dagger*L),   0<=eta<=1.

On this identity-carrier preparation its output is exactly
sigma_eta^channel=sigma_0*(I+eta*M); using L^dagger gives the negative
direction. It is a different finite family from the exponential tilt above,
with the SAME tangent. The tangent can equivalently be written

    D_L(sigma)=L*sigma*L^dagger-{L^dagger*L,sigma}/2,
    D_L(sigma_0)=sigma_0*(L*L^dagger-L^dagger*L)=sigma_0*M.

This is a declared preparation intervention requiring an apparatus/environment,
not a newly adopted native Lindblad law, a reset of the subsequent record
dynamics or a claimed BS implementation. On a regular graph the initial
complete MEAN energy stays exactly constant along this linear channel family,
by the preceding zero-covariance argument. This does not make it free. Its
carrier entropy change, using natural logarithms, is

    Delta S=-(c/2)*[(1+eta)*ln(1+eta)+(1-eta)*ln(1-eta)],
    c=2*Q*(V-Q)/[V*(V-1)].

Use 0*ln(0)=0 at the endpoint. This entropy decrease must be reconciled
with the retained apparatus state and correlations in any physical dilation.
No minimum energy cost or bath
temperature is invented. Energy variance and full energy distributions need
not be unchanged merely because their mean is unchanged.

In the following traces sigma_0 includes the unchanged blank records and
writer preparation. The subsequent node-model response of a Hermitian local
probe O_X obeys

    b_O(x)=Tr[sigma_0*M*O_X(x)]
          =Tr[sigma_0*D_L^dagger(O_X(x))],
    D_L^dagger(O)={L^dagger*[O,L]+[L^dagger,O]*L}/2,
    |b_O(x)|<=||L||*||[O_X(x),L]||.                        (15)

Thus the already qualified bounded-degree dynamics gives a spatial
propagation bound with active records. For example a conservative
commutator-chain estimate is, for any mu>0 and graph distance r(X,Y),

    |b_O(x)|<=2*||O_X||*||L||^2*|X|*|Y|
                  *exp[4*b*D*exp(mu)*|x|-mu*r(X,Y)].

The estimate is capped by the trivial trace-norm bound when large. It is
an exponential tail, not a strict light cone or a calibrated speed. For a
complex clock readout B, replace the last bound in (15) by
||L||*(||[B(x),L]||+||[L^dagger,B(x)]||)/2, or apply the Hermitian
bound to its two quadratures. If the intervention sites are far apart,
that nonlocal preparation itself
must not be described as a local causal operation.

Unlike differentiation with respect to an extensive external source, this
PREPARATION derivative has an immediate full/reference error bound. Its
signed initial tangent has trace norm

    ||sigma_0*M||_1=c=2*Q*(V-Q)/[V*(V-1)]<=1.

Apply (7) separately to the two positive parts of this tangent. Their traces
sum to c, so the bound on b_O,full-b_O,node is c times (7), hence O_T(1/N).
No interchange of source derivatives and size limits is used. The same
argument applies to bounded clock readouts and their node derivative terms;
the wrong-degree term retains its N*q_T^2 bound.

At the common invertible clock branch, the exact preparation response is

    b_O|Theta=b_O-(dot o/nu)*Im[b_B/beta],                  (16)

since the blank initial record amplitude has no preparation tangent here.
Its full/reference convergence follows from the established amplitude/rate
floors and the local derivative bounds. A distant-observable causality
claim in this relational description must also bound the CLOCK response.
If the clock is inside the affected region but the probe is not, its
retiming term need not be small; that is not by itself a distant force.
If both probe and clock are outside the propagation region, both terms
are controlled by the corresponding local bounds. Matching this signal
to one common physical lapse/metric across probes remains a separate test.

## What this resolves and the next physical question

The complete active-record response need not disappear when its owned
energies and actual clock are retained. Its finite-source mean and controlled
work per node have a finite-time comparison theorem at fixed carrier filling.
This resolves the specific V114 gap between a single kinetic Taylor
coefficient and a complete, finite-interval source response on this family.

The result is analytic in a sufficiently small source/time neighborhood,
and the pulse work begins quadratically in alpha. It is NOT the nonanalytic
quasistatic |g|^3 constitutive work needed by the earlier conditional galaxy
construction. A longer-time, collective or otherwise nonuniform physical
limit must be derived if that mechanism is pursued. Also, raw degree changes
per vertex vanish on the present fixed-time comparison interval; this proof
cannot itself supply a finite graph-geometry backreaction there. Geometry
encoded in node correlations, or a different time/size regime, is not excluded.

Next test the SPATIAL, endogenous matter-to-probe response on this active
family against the same complete energy-source channel, retaining the local
clock, the local propagation bound and the source current (4). Avoid the
unchanged-state unitary test above; choose and cost a genuine redistribution
or an intervention on an aged correlated state. A uniform normal pulse is
not a field equation. In particular establish which native
probe correlations can carry the proposed long-range interaction, whether
they respond to matter loading with the required shared source relation,
and what physical geometry/ruler/work that interpretation requires. Do not
fit separate lapse profiles to each readout or substitute a passive band.
If a long-time collective limit is needed, specify it and its observable
before any numerical run. Formation and the galaxy/expansion join remain
open, followed by every mandatory Stage 3 lane.

## Internal checks and provenance

Root derived the normal allocation, local expectation strategy, cubic
two-time kernel and pulse-work consequence. Endpoint_equations_check
independently checked the complete source, local commutators, exact controls,
step coefficient and switching-work sign, and identified the finite-V factor
and phase-ended odd-source correction. V005_resume_review independently
derived and checked the local commutator/probability bound, complete-source
estimate and bounded-source/work extension. It also independently checked
the localized preparation tangent, supplied its exact finite Kraus family,
and verified the signed-state derivative and clock-boundary qualifications.
Handoff_plan_review_v005 independently checked the clock commutator, rate
and small-interval transfer,
and supplied the explicit uniform node-kernel majorant. Its boundary-floor
and source-jump qualifications are retained. No numerical evidence is
claimed here.

The parent action and coefficients remain in BS_MICRO_ACTION.md. The exact
allocation and record influence are in NATIVE_ACTIVE_RECORD_MECHANISM_AND_STATE_V001.md;
fixed-clock response identities in NATIVE_FORMED_STATE_SOURCE_MATCHING_V001.md;
selected-bit locality in NATIVE_ACTIVE_RECORD_LOCALITY_AND_CLOCK_V001.md;
and the previous, distinct kinetic result in NATIVE_RECORD_DRIVEN_BAND_POPULATION_V001.md.
Their frozen statements and limitations are preserved rather than overwritten.
