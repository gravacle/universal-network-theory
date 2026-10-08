# Existing density formation bound applied to the empty-edge tie state

2026-09-30. Root source-only specialization, pending independent review. No
numerical trajectory, physical time calibration or modification of the parent.
This tests actual evolving occupation rather than substituting a ground state.
Equations (1)--(4) are not a new formation theorem: the enclosing dark-sector
directory's NATIVE_INCIDENCE_FORMATION_SPEED_BOUND_V001.md (2026-09-27)
already proves them in greater generality, including sharper finite-occupancy
and local-degree bounds. This note connects that result to the current tie
preparation and adds the elementary Markov-tail consequence (5).

## Family and initial state

There are L=N^2 candidate edge qubits with occupation n_e=(1-Z_e)/2.
Use the same fixed closed first-degree-tie parent and explicitly empty edge
register as NATIVE_DEGREE_TIE_EMPTY_PREPARATION_BOUND_V001.md:

    H=H_diag-h sum_e X_e,  h=Omega/N,  Omega>0,
    H_diag=C_N+2U(C_L+C_R),
    M=sum_e n_e,  m(t)=<M>_t,  m(0)=0.

Uniform records are held, carriers blank, ports off. The proof actually uses
only [H_diag,M]=0, so it does not depend on the penalty U or the ground-state
approximation. It does not cover added interactions that change M or a changed
flip coefficient. Native BS10 record/writer copies commute with M: although
they leave the held-record sector used here, the older general theorem still
covers them and they do not evade its incidence-speed bound. Other ports must
have their commutators checked, not be included implicitly.

## Exact occupation-speed bound

For the reduced density matrix of edge e, positivity of its 2-by-2 matrix
gives |rho_01|^2<=p_e(1-p_e), p_e=<n_e>. Hence

    |<Y_e>| <= 2 sqrt[p_e(1-p_e)].

No assumption of an unentangled state is used. The Heisenberg equation and
Cauchy-Schwarz, with 0<=m<=L, imply

    |dm/dt| <= (h/hbar) sum_e |<Y_e>|
             <= (2h/hbar) sqrt[m(L-m)]
             <= (2Omega/hbar) sqrt(m).                 (1)

The coefficient uses sqrt(L)=N exactly. Integrating the last inequality
from an empty register yields

    0<=m(t)<=min[N^2, (Omega*t/hbar)^2],  t>=0.         (2)

To avoid dividing by zero at the initial state, apply (1) to
d sqrt(m+epsilon)/dt<=Omega/hbar for epsilon>0 and then let epsilon go to
zero. Finite-dimensional unitary evolution supplies differentiable m(t).
Monotone occupation growth is not assumed: (1) bounds its absolute speed.

## Degree density and necessary time

Each occupied edge contributes two to the total node degree. Since there
are 2N nodes, the actual mean degree averaged over nodes is m/N, so

    <d>_nodes <= (Omega*t/hbar)^2/N.                   (3)

Permutation symmetry additionally makes each same-layer node expectation
equal to this value in the declared preparation, but the averaged statement
does not require that symmetry. At any fixed dimensionless age Omega*t/hbar,
the mean degree tends to zero as N grows. For a separately declared target
mean degree d_target>0, any first attainment must obey

    t >= (hbar/Omega) sqrt[N*d_target].                (4)

This is a necessary bound, not a predicted formation time or sufficient
mechanism. It neither assigns a physical density to graph degree nor selects
d_target from galaxy data. A nonzero initial edge population changes the
bound to sqrt(m(t))<=sqrt(m(0))+Omega*t/hbar and is a different preparation.

For completeness, if P_{>=q} projects onto M>=q for any integer q>0, then
positivity gives

    Prob_t(M>=q) <= min[1, (Omega*t/hbar)^2/q].         (5)

Thus at a fixed age the probability of an extensive edge count q proportional
to N also tends to zero. This does not constrain high-degree rare states
strongly enough to bound every energy-weighted source moment or susceptibility.
Do not infer a source-response bound from (5) without that missing control.

## Consequence, distinct from the ground-population theorem

The earlier bound p_ground<=8/(N+8) excludes spontaneous ground selection
under the fixed closed evolution. The already established density bounds,
with the tail application (5), constrain the actually evolving density without
any ground-state assumption. A fixed
late-time snapshot cannot be called a formed finite-degree growing network
from this empty register at arbitrarily large N. Choosing an age scaling
with sqrt(N) avoids this particular necessary obstruction, but supplies no
attractor, ground selection, physical clock, energy export or pressure law.
It must be an explicitly derived formation timescale, not a fitted age.

Other preparations, native ports and alternative already specified dynamics
remain separate possibilities. This is not a theorem against a general
network cosmology or a prediction for galaxy-edge gravity. It gives a precise
test for the current conditional preparation and fixed microscopic scaling.

Ancestry: NATIVE_DEGREE_TIE_EMPTY_PREPARATION_BOUND_V001.md,
SHA d24a466fa69f1e613f7cea7d59eff1a15d881c7b1016a57a62e29a0d59451257;
NATIVE_DEGREE_TIE_FULL_PARENT_COUPLING_V001.md,
SHA def8c842be9bd1bbd21ae8cd0a6338160ac28d81aaab2851371b519b75205390.
Primary theorem: ../NATIVE_INCIDENCE_FORMATION_SPEED_BOUND_V001.md,
SHA 8118207e2da4bdae41143f6a90d48dd3be9f450371c688f508eabe776ccc6229.
