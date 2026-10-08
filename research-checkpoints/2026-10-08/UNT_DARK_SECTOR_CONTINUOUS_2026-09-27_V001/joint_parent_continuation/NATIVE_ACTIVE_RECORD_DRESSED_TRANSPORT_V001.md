# Active records and the propagation of mobile matter

2026-10-03 UTC. Exact analytical continuation, not a new native law or a
replacement preparation. The active record interaction changes both matter
propagation and the energy of its environment. Here its exact record-basis
rotation separates a calculable lower-record contribution from the record
excitations that a reduced model would discard. A local energy gap alone
does not justify discarding those excitations.

This uses equation11 of NATIVE_FORMATION_CLOSURE_ALGEBRA_PROPOSED_V001.md,
with occupied same-content writers and fragment ports explicitly off. It
extends the mobile-matter question previously treated with records blank
and copying off in NATIVE_MOBILE_CARRIER_EFFECTIVE_INTERACTION_V001.md.
No halo, source-dilation function, mean record density or fitted force is
inserted. The graph and carrier configurations below remain quantum variables.

## Exact conditional record basis

Let c=(G,p) label incidence and a fixed-number hard-core carrier configuration.
At vertex v, p_v is0 or1, d_v is its degree in G, and the local record block is

    h(d,p)=delta_d*r+g_p*X,
    delta_d=epsilon_r-lambda_R*d,  g_p=g_wr+g_psi_r*p,
    Delta_p(d)=sqrt(delta_d^2+4*g_p^2),
    e_p^sigma(d)=(delta_d+sigma*Delta_p(d))/2, sigma=+1 or -1.

The gaps and this elementary diagonalization are prior ingredients; the
new question is what happens to native carrier hops and link flips under
the same configuration-dependent change of basis. For g_p>0 define

    theta(d,p)=atan2(2*g_p,-delta_d),
    U(d,p)=exp[-i*theta(d,p)*Y/2].

U has the upper and lower record eigenvectors as its two columns. The
convention here is Z=1-2r and conventional Pauli Y, not the opposite
Z_r and record-current convention used in equation12 of the sector note.
Explicitly h=(delta/2)*I+(Delta/2)*U*Z*U^dagger.
The controlled product W=sum_c |c><c| tensor product_v U(d_v,p_v) is unitary.
Transforming the COMPLETE Hamiltonian by W retains both record bands.
Every diagonal graph/carrier energy and its identity terms remain, and the
record diagonal is sum_v e_pv^sigma_v(d_v). An allowed carrier hop u to v
has the exact off-diagonal block

    -t*n_uv(G) * product_(a=u,v)[U(d_a,p'_a)^dagger U(d_a,p_a)].

A link flip on e=(u,v), changing each endpoint degree by zeta=+1 or-1,
has the exact block

    -h_N * product_(a=u,v)[U(d_a+zeta,p_a)^dagger U(d_a,p_a)].

Other record factors are identity. Each factor is a real two-dimensional
rotation, including its off-diagonal sine entries. Keeping only its cosine
is a projection, not the exact transformed parent. At fixed native
coefficients this is a time-independent unitary change of basis; a source
that changes that basis needs the corresponding connection terms and
complete source work. No physical energy baseline is subtracted.

## What the lower-record compression actually predicts

Let P_L retain the local lower eigenvector at every vertex for each c.
This is a proposed reduced subspace, not a prepared state or a spectral
band known to be isolated from all other configurations. In P_L H P_L,
the carrier-hop magnitude is

    t_eff(u,v)=t*s(d_u)*s(d_v),
    s(d)^2=(1+(delta_d^2+4*g_0*g_1)/(Delta_0*Delta_1))/2.

At inherited g_0=1,g_1=2, differentiating the squared positive overlap
shows its minimum occurs at delta_d^2=8 when degree is allowed continuous.
Thus, also for every integer degree,

    (3+2*sqrt(2))/6 <= s(d_u)*s(d_v) <= 1.

The leading compressed hopping amplitude is therefore between about
0.9714*t and t. This specific overlap does not enhance the hopping or
supply a large low-density change by itself. It does not bound all long-time
transport, localization, collective response or gravitational effects by
2.86 percent. The compulsory onsite terms and discarded sectors remain.

In particular the complete compressed diagonal is

    E_inc,diag(G)+epsilon_psi*sum_v p_v+epsilon_w*sum_v w_v
      +j*sum_(edges uv)n_uv*(p_u+p_v-2*p_u*p_v)
      +sum_v e^-_pv(d_v).

Here e^-_p(d)=e^-_0(d)+p*mu(d), where

    mu(d)=[Delta_0(d)-Delta_1(d)]/2.

This record contribution reaches its minimum -1 at delta_d=0, inherited
degree2, and tends to0 as |delta_d| grows. It is not a monotone function
of degree on both sides of2. This minimum alone does not select degree2
for the full energy, which includes current-square and graph penalties.
These elementary functions are smooth and their local gaps are nonzero;
calling this local projection a demonstrated phase transition is unearned.
A precise restriction is that these coefficients have no local gap closing,
zero hopping overlap or singularity at finite degree.
A many-body transition or a nonanalytic collective limit is a different test.

There is also an exact equilibrium control at degree2, with incidence
frozen. For fixed carrier number Q and positive g_wr,g_psi_r,

    H=H_carrier,G+sum_v(g_wr+g_psi_r*p_v)*X_v
      >= H_carrier,G-g_wr*V-g_psi_r*Q.

Every carrier state tensored with all records in |-x> saturates the record
part of this operator bound. Therefore its exact lowest energies obey

    E_Q(active records)=E_Q(carrier,G)-g_wr*V-g_psi_r*Q.

The carrier energy includes graph/writer baselines and all current-square
terms. Pair-addition energies and comparisons between equal-size degree2
topologies are unchanged by the affine shift. In particular active copying
in this conditional equilibrium control does not remove the earlier
fragmentation preference at inherited j<t. This does not cover other
degrees, dynamic incidence or the actual nonequilibrium blank records.

## The discarded record excitations are calculable

For a particular all-lower configuration |c,->, each distinct single link
flip or allowed carrier hop reaches a different incidence/carrier label.
Those outgoing labels are orthogonal, so their squared excitation norms
add without an interference assumption. Define

    a_(v,e)=cos([theta(d_v+zeta_e,p_v)-theta(d_v,p_v)]/2).

The exact initial coefficient for leaving the global P_L subspace is

    L_c=||(1-P_L)H|c,->||^2
       =h_N^2*sum_(all possible e=uv)[1-a_(u,e)^2*a_(v,e)^2]
        +t^2*sum_(occupied allowed carrier-hop e=uv)
                  [1-s(d_u)^2*s(d_v)^2],
    Pr(outside P_L at x)=L_c*x^2+O(x^3).

This is an initial-state coefficient, not an escape rate or a finite-window
error estimate. General coherent superpositions require the full Q_L H P_L
operator, rather than adding these configuration probabilities.

There is a useful exact supplied-cycle control. Take degree2 everywhere,
one carrier, inherited h_N=1/N, and all records in their conditional lower
states. At delta=0 all those record states are |-x>, independent of carrier
occupation. Carrier hopping then contributes zero to L_c. A link flip
changes each endpoint detuning to plus or minus1/2. Put

    A_0=(1+4/sqrt(17))/2,
    A_1=(1+8/sqrt(65))/2.

There are N possible edges touching the one carrier and N^2-N others, so

    L_N=(1-1/N)*(1-A_0^2)+(1/N)*(1-A_0*A_1),
    lim_(N->infinity)L_N=35/68-2/sqrt(17)>0.

Hence the initial global lower-record excitation coefficient does not
vanish merely because each link-flip amplitude is1/N. This is a warning
against eliminating the entire excited-record sector on that argument.
It neither proves a nonzero limiting leakage at each fixed later time
(the short-time remainder need not be uniform in N) nor disproves a
controlled local-observable approximation. A local record gap is not a
uniform many-body isolation or a preparation theorem.

## A blank-record benchmark without a ground-state substitution

As a separate exact control, freeze a degree2 graph and turn incidence
flips off, leaving writer and carrier recording active. This is not the
full dynamic-link parent. Every record X_v then commutes with H. For
initially blank product records and any independent carrier state rho_C,
tracing the retained records gives exactly

    rho_C(x)=2^(-V)*sum_(sigma in {+1,-1}^V)
                   U_sigma(x)*rho_C(0)*U_sigma(x)^dagger,
    U_sigma(x)=exp[-i*x*(H_carrier,G+g_psi_r*sum_v sigma_v*p_v)].

The writer contribution g_wr*sum_v sigma_v is constant within each branch
and cancels only from this carrier marginal, not from total energy or work.
The branch weights follow from the specified blank records, not a fitted
disorder ensemble. This is a mixture of carrier evolutions in different
static onsite potentials, generally not evolution under their mean.
The initial blank-record product has all-lower weight 2^(-2N) on this
cycle. Diagonalizing the Hamiltonian does not prepare that lower sector.
Actual incidence flips break the frozen-degree premise; this control does
not replace the full parent or imply permanent classical disorder.

## A transport comparison in actual blank records

The first transfer correction can be determined without assuming lower
records or freezing the dynamic links. Start from a definite G, one carrier
at u, blank records and fixed same-content writers. Compare g_psi_r=g with
g_psi_r=0, keeping all other native coefficients unchanged. For an initially
occupied edge u-v the exact probability contrast is

    P_v^g(x)-P_v^0(x)=-(t^2*g^2/6)*x^4+O(x^6).

If the only carrier-record port is at u, the coefficient is instead
-t^2*g^2/12. These are two declared port patterns, not interchangeable models.

At fourth order every contributing probability term needs at least two
hops and an even total number of record flips. Thus any g-dependent term
has precisely two hops on this edge and two copy insertions. There is no
remaining insertion for a link flip, record feedback or an onsite energy.
Those other native fourth-order terms remain in each absolute probability;
they cancel only from this on/off contrast. In the relevant two-position
block, write the environment diagonals as A and B. The transfer expansion is

    P_v(x)=t^2*x^2-(t^2/12)*<(B-A)^2+4*t^2>*x^4+O(x^5).

This identity does not require A and B to commute. Carrier copying adds
g*X_u to A and g*X_v to B. The common writer term cancels; blank records
give <(X_v-X_u)^2>=2 and zero cross terms with the diagonal detuning.
Real full Hamiltonians and basis preparation make the probabilities even,
giving the O(x^6) remainder above. This is reduced initial transfer, not an
all-time slowdown or a force law.

For comparison per reference-clock phase, equal initial rates alone are
insufficient. If theta_g=nu_0*x+a_(3,g)*x^3+..., the fourth-order contrast
includes both the term -t^2*g^2/(6*nu_0^4) and
-2*t^2*(a_(3,g)-a_(3,0))/nu_0^5. The cubic clock coefficients must therefore
be kept or proved equal before using this as a relational comparison.

## Fixed exact arithmetic check

Use a single new algebra check, not a new propagation or large-network run.
N=2, all four links of K2,2 initially occupied, carrier at L0=0, all four
records blank, all four writers occupied, fragment ports off. Keep the
complete inherited coefficients Delta=4, Ud=d*=epsilon_psi=epsilon_r=1,
h=1/2, t=1/2, j=1/4, lambda_R=1/2, g_wr=1 and epsilon_w=0.
Use precisely three carrier-record arms: all ports off, uniform g=1, and
only the initial-site port g=1. There are1024 basis states in each arm.

Compute exact rational H^k|initial> for k=0,1,2,3 without an eigensolve or
time propagation. The complete initial energy is43/2 in all arms. For each
initially adjacent target R0=2 and R1=3, obtain the exact quadratic and
quartic arrival coefficients from these vectors; compare the on/off
contrasts to -1/24 and -1/48 respectively. Independently calculate the
initial derivatives through cubic order of B_w=(Z_w-iY_w)/2 for every
record site w, retaining both its real matrix entries and its complex
Heisenberg derivative convention. The remote same-layer clock w=L1=1
must be distinguished from the colocated and adjacent clocks.

Compute each clock's initial phase coefficients from its derivatives.
Where initial rates and cubic phase coefficients agree, compare the
relational fourth-order arrival contrast using those actual coefficients;
otherwise report the clock correction, not the unqualified generator-time
coefficient. Preserve all arms and clock sites. Exact Fraction arithmetic
requires no fitted tolerance; numerical conversion is display only.

## Decision and next physical calculation

Active record formation genuinely dresses matter motion with no added
substance. The simplest all-lower replacement, however, provides only a
bounded local hopping change, mandatory onsite energy and nonzero discarded
record excitation. It has not produced a density-selected gravitational
coupling, the baryonic mass scaling or cosmic acceleration.

The next useful comparison must retain or control these record excitations
and use an actual supported preparation. A source response or transport
calculated from P_L H P_L alone is not promoted to the native model until
its error and preparation are owned. In particular, the lower-record cycle
and the earlier blank-record reference clock are different preparations;
their favorable properties cannot be combined as if proved for one state.
No new numerical history, density scan, coefficient change or observational
claim was required for the present analytical screen.
