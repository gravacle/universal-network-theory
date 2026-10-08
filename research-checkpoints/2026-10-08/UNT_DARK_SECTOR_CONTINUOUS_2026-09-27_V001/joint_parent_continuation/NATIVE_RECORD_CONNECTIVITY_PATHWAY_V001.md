# Native records, sparse degree and connected preparation

2026-09-29. Additive analytical result; no numerical worker, changed source,
parameter fit, physical length assignment or assertion of a geometric phase.

## What this establishes

There are two distinct constructive routes, and the inherited coefficients
select which one is presently available.

1. **Records can select an extensive, finite-degree branch in the native
   parameter family.** Below is an exact open parameter interval, an
   extensive lower energy bound, and a finite-size quantum bound showing
   `M=kN+O(sqrt(N))` in a fixed occupied-record sector. This is stronger than
   a mean-field suggestion, but does not select global connectivity or a
   geometric dimension. Its example parameters are not the inherited ones.
2. **At the inherited coefficients, connected excited preparations can
   persist without changing the Hamiltonian.** A connected backbone with
   `M0=O(N)` edges has loss probability at most
   `Omega^2 M0 t^2/(hbar^2 N^2)`. Thus a family of prepared connected
   backbones survives with probability tending to one at fixed microscopic
   time, and more generally at `t=o(sqrt(N))`.
3. **Preparation has a genuine timescale and energy obligation.** From
   incidence blank the native flips cannot build more than
   `(Omega t/hbar)^2` expected edges, regardless of record coherence or
   incidence-diagonal record formation. Connection with order-one
   probability consequently takes at least order `sqrt(N)` microscopic
   time. The existing record formation has not been shown to prepare such
   connected states.

The inherited held ground branch remains sparse in a stronger sense:
its expected number of edges is bounded independently of N even with
arbitrary record occupation and carrier coherence. Hence the constructive
next question at those coefficients is **formation and persistence of a
connected active state**, not a presumed connected equilibrium vacuum.

## 1. Stated native scope and full energy

Use one BS04--BS11 bipartite slab, N vertices per side and N squared
possible links. Write `M=sum_e n_e`, `d_v=sum_(e incident v)n_e` and
`h_N=Omega/N`. There is no metric or spatial distance in these definitions.
The graph considered below is the underlying undirected incidence graph;
its connectivity is not a Lorentzian causal theorem for the directed
composition schedule.

For the held results, turn record-copy couplings and external ports off.
Keep every onsite term. In a sector of fixed record occupations, total
carrier occupation and held writer/reservoir occupations, these uniform
onsite terms have a constant value `E_on`. Record coherences between
patterns with the same total occupation can be retained. Held evolution
does not mix the record-occupation sectors. No record-storage cost is
discarded in comparing preparations.

The inherited numbers, as used by `record_addition_compute.py`, are

    Omega=1, Delta=4, U_d=1, d_star=1,
    epsilon_r=epsilon_psi=1, epsilon_w=0,
    t_hop=1/2, lambda_R=1/2, lambda_J=1/4.

The one-link `h=1` therefore extends by the already defined `h_N=1/N`,
not by keeping every link at unit flip strength as N grows.

## 2. Exact record-bearing positive-cost bound

For the native qutrit transfer operators, `T_e^2=J_e^2=P_e`, where `P_e`
projects onto the edge's one-occupied-carrier subspace. On that subspace
`T_e` has eigenvalues plus/minus one, and both operators vanish on its
complement. Therefore, with `lambda_J>=0`,

\[
 -t_{\rm hop}T_e+\lambda_J J_e^2\succeq-c_\psi I,
 \qquad c_\psi=\max(0,|t_{\rm hop}|-\lambda_J).
 \tag{1}
\]

This uses the actual positive current term, rather than dropping it.
Different edges need not commute for their individual lower bounds to add.
Also `0<=q_v^r<=1`, so record feedback lowers the energy of an occupied
edge by no more than `2 lambda_R`. Expanding the degree squares gives

\[
 H\succeq E_{\rm ref}+\kappa_R M
 +2U_d\sum_v\sum_{e<f\ni v}n_en_f
 -\frac{\Omega}{N}\sum_e X_e,
\]
\[
 E_{\rm ref}=E_{\rm on}+2NU_d d_*^2,
 \qquad
 \kappa_R=\Delta+2U_d(1-2d_*)-2\lambda_R-c_\psi.
 \tag{2}
\]

This is a bound on the full held operator, not a replacement of the
physical record operators by their mean occupations. For the inherited
values `c_psi=1/4` and **`kappa_R=3/4>0`**. Dropping the current term would
give the valid but weaker value one half.

Every allowed fixed-occupation sector admits incidence blank with energy
`E_ref`. Its ground energy is thus no higher than that reference. For any
state, the individual Bloch bounds and Cauchy--Schwarz give

\[
 |\langle\sum_eX_e\rangle|
 \le 2\sqrt{m(N^2-m)},\qquad m=\langle M\rangle.
\]

Combining this with (2) for `U_d>=0,kappa_R>0` proves

\[
 \boxed{m_0\le
 \frac{4\Omega^2N^2}{\kappa_R^2N^2+4\Omega^2}.}
 \tag{3}
\]

At the inherited parameters its large-N upper bound is `64/9`, independent
of N. A measured graph connected on all `2N` vertices requires at least
`2N-1` edges, so

\[
 \Pr_0({\rm connected})\le\frac{m_0}{2N-1}\longrightarrow0.
 \tag{4}
\]

The same conclusion holds for a ground state over held record patterns
with a fixed total record count: the reference and bound are common to
those sectors. Occupation coherence cannot evade `q<=1`. This says
nothing against the independently demonstrated record phase clock; its
off-diagonal coherences remain real dynamical observables, but do not
increase the magnitude of this feedback operator.

If one instead minimizes over the entire ports-off held register space,
the nonnegative onsite operator can be dropped in the lower bound and
the all-register-blank state supplies the upper trial energy
`2N U_d d_star^2`. Equation (3) then holds for that full held ground state
as well. This statement requires the native nonnegative storage gaps and
zero copy couplings; it is not an assertion that an actual prepared
coherent state is a ground state.

An active state is different. If its conserved held energy is
`E_ref+mathcal E`, it need only satisfy

\[
 \kappa_R m-2\Omega\sqrt m\le\mathcal E.
 \tag{5}
\]

For `mathcal E=O(N)`, this permits `m=O(N)`. In particular, a graph of
bounded degree and O(N) occupied registers has an extensive preparation
energy in this action. Equation (3) must not be applied to that prepared
state as if it had relaxed to the ground state.

## 3. A nonempty record-selected sparse-degree regime

There is an exact held invariant sector with all records occupied and all
carriers blank. Records can have either content, and their onsite energy
`2N epsilon_r` remains in `E_on`. Hopping and current terms annihilate
this sector. Put `Delta_eff=Delta-2 lambda_R`. Its link Hamiltonian is

\[
 H=E_{\rm on}+\sum_{v=1}^{2N} f(d_v)
 -\frac{\Omega}{N}\sum_eX_e,
 \quad f(d)=U_d(d-d_*)^2+\frac{\Delta_{\rm eff}}2d.
 \tag{6}
\]

At zero flip strength an integer `k>=1` is the strict per-vertex minimum
precisely when

\[
 \boxed{4U_d(d_*-k-\tfrac12)<\Delta_{\rm eff}
       <4U_d(d_*-k+\tfrac12).}
 \tag{7}
\]

For `N>=k`, a simple bipartite k-regular graph exists and realizes all
vertex minima simultaneously. For instance, edges from left i to right
`i+j mod N`, `j=0,...,k-1`, give such a graph. This realizes `M=kN`
without a mean-field approximation. The graph labels are only a way of
writing an allowed state; the Hamiltonian remains permutation covariant.

With `Delta=4,U_d=d_*=1`, the interval `5<lambda_R<7` gives `k=3`;
`lambda_R=6` is an illustrative interior point. This example changes the
record-feedback coefficient relative to the inherited one half. It is a
mathematical nonempty regime, **not** a fitted or adopted new parameter.
The inherited all-record/carrier-blank sector instead minimizes at zero
degree. For an arbitrary fixed record pattern, the exact per-vertex
linear coefficient in (6) is `Delta/2-lambda_R q_v`, not a uniform
coefficient inferred from total record density. The pattern and graphical
compatibility of its preferred degrees matter.

### Degree stabilization outside BS13

Equation (7) may lie outside the seed's simple sufficient BS13 domain.
Here is the required separate lower bound, rather than an assumed
permission to drop that stability question. For `U_d>0`, use
`sum_v d_v^2>=2M^2/N`, (1), and `||sum X||=N^2`. The general held model
obeys

\[
 H\succeq E_{\rm on}+2NU_dd_*^2
 +\frac{2U_d}{N}M^2+aM-\Omega N,
 \quad a=\Delta-2\lambda_R-c_\psi-4U_dd_*.
\]
\[
 \boxed{H\succeq E_{\rm on}
 +N\left[2U_dd_*^2-\Omega-
 \frac{\max(0,-a)^2}{8U_d}\right].}
 \tag{8}
\]

All fixed coefficients therefore give an extensive lower bound when the
positive degree penalty is retained. The fixed number of bounded local
formation terms or allowed extensive ports can add their own O(N) lower
bound, but are not silently included in the held-state phase proof.

### Finite-size quantum sparse-degree bound

The `Omega/N` flips do not invalidate the extensive-degree conclusion.
Define `d0=d_star-Delta_eff/(4U_d)` and, in the interior interval (7),

\[
 \gamma=U_d(1-2|k-d_0|)>0,
 \quad C=d_0+\sqrt{(k-d_0)^2+\frac{\Omega}{2U_d}}.
\]

For `N>=k+1`, convexity on integer degrees gives
`f(d)-f(k)>=gamma |d-k|`. A classical k-regular basis state is a trial
state with energy `E_on+2N f(k)`. First, the quadratic lower bound and
the coarse flip bound `Omega N` give `m_0<=C N`. Then use the sharper
state-dependent coherence bound to obtain

\[
 \boxed{
 \left\langle\sum_v|d_v-k|\right\rangle_0
 \le\frac{2\Omega\sqrt{CN}}{\gamma},
 \qquad
 |m_0-kN|\le\frac{\Omega\sqrt{CN}}{\gamma}.}
 \tag{9}
\]

These are controlled finite-size bounds at fixed coefficients; the
relative degree error vanishes. They do not prove global connection.
Degree one gives disjoint matched pairs. Degree two permits both a single
cycle and unions of cycles. Larger fixed degrees likewise allow
connected and disconnected graphs. The quantum flips can lift classical
graph degeneracies through virtual transitions; (9) does not determine
which topology they favor. Neither O(N) edges nor connectedness determines
a local heat-kernel dimension, physical distance or gravitational action.

## 4. Exact persistence of a prepared connected backbone

Return to the unchanged inherited coefficients. Let an initial state be
supported on the subspace where every edge of a connected backbone G0 is
occupied. Other edges and all matter/record correlations may be arbitrary.
Set `P=product_(e in G0)n_e`, `Q=1-P`, and let `M0` be the number of
backbone edges. Every native term except incidence flips commutes with P;
this includes incidence-weighted carrier transfer and record copying.
Only flips of the `M0` original edges leave P, and the corresponding
one-missing-backbone-edge images are mutually orthogonal. Exactly,

\[
 \|QHP\|=\frac{\Omega\sqrt{M_0}}{N}.                 \tag{10}
\]

To make the time bound explicit, compare H with its block diagonal part
`H_D=PHP+QHQ`. The off-diagonal block operator has norm `||QHP||`.
Duhamel's identity for unitary evolution and `Q exp(-itH_D/hbar)P=0`
then give

\[
 \boxed{\Pr_t(\hbox{any backbone edge absent})
 \le\min\left(1,\frac{\Omega^2M_0t^2}{\hbar^2N^2}\right).}
 \tag{11}
\]

The mixed-state result follows by linearity. Every graph in P is connected,
so (11) is also an upper bound on disconnection probability. For a sparse
backbone `M0<=cN`, the survival probability tends to one whenever
`Omega t/hbar=o(sqrt(N))`. Additional links cannot invalidate connectivity,
although they can change distance or spectral geometry.

A degree-two bipartite cycle is one explicit O(N)-energy example. A
permutation average over the prepared cycles retains this bound without
introducing physically preferred node labels. Neither construction is
asserted to have been produced by the existing record-formation protocol.
Its input graph, source work and formation time must still be supplied.
The result is unitary retention, not dissipation toward a minimum, a
macroscopic lifetime in seconds, or protection of a preassigned dimension.

The same proof permits time-dependent incidence-diagonal formation terms.
An extra port that changes incidence contributes to `QHP`; its norm/work
must be included rather than hidden in the preparation.

## 5. A companion lower bound on building connection from blank

For any native evolution whose only incidence-changing terms are
`-Omega sum X/N`, including local record formation, the Bloch bound gives

\[
 |\dot m|\le\frac{2\Omega}{\hbar N}
 \sqrt{m(N^2-m)}\le\frac{2\Omega}{\hbar}\sqrt m.
\]

Starting with incidence blank, continuity at `m=0` and integration yield

\[
 \boxed{m(t)\le(\Omega t/\hbar)^2,\qquad
 \Pr_t({\rm connected})\le
 \min\left(1,\frac{(\Omega t/\hbar)^2}{2N-1}\right).}
 \tag{12}
\]

For example, probability at least p of connection requires
`t>=(hbar/Omega)sqrt(p(2N-1))`. This is a necessary, not sufficient,
formation time. The record feedback may alter actual transition phases
and probabilities, but cannot defeat this bound while its terms commute
with the incidence occupations. There is no assertion that the bound is
saturated, or that a record-rich state inevitably connects.

There is a direct growth corollary to the earlier blank-pair inclusion.
When one new node on each side is appended to an N-per-side slab, its
`K=2N+1` new incidence qubits start blank and the new flip coefficient is
`Omega/(N+1)`. Applying the same derivative bound to their occupation
`M_new` gives

\[
 \langle M_{\rm new}(t)\rangle
 \le\frac{\Omega^2(2N+1)t^2}{\hbar^2(N+1)^2}.
\]

Connecting both new vertices to the old network requires at least two
new occupied edges, even if the old graph stays connected. Consequently

\[
 \boxed{\Pr_t(\hbox{full enlarged graph connected})
 \le\min\left(1,
 \frac{\Omega^2(2N+1)t^2}{2\hbar^2(N+1)^2}\right).}
 \tag{13}
\]

Adding blank node count is therefore not instantaneous incorporation into
connected volume. These bounds establish necessary scaling and a
retention window; they do not guarantee that one protocol forms the new
connections while preserving all old ones over the required time.

## 6. Smallest discriminating continuation

The ground-state and survival results above are analytic; no size sweep
is needed to establish them. A compact future implementation check can be
fixed before execution as follows:

- Links only, `N=2,3` (16 and 512 amplitudes), all carriers blank, and two
  held record controls: every record blank versus every record occupied.
  Use exactly the inherited coefficients and `Omega/N`; count the
  occupied-record onsite energy. Do not use the illustrative `lambda_R=6`.
- In each case evolve both incidence blank and an explicitly declared
  connected cycle. Record all original times `0,1/4,1/2,1,2`, without
  dropping times where a rigorous bound becomes uninformative.
- Measure full-graph connection probability, original-backbone survival,
  M and degree distribution; check unitarity, conserved full energy,
  (11)--(12), and agreement of two numerical propagators. Anchor the cycle
  as a declared preparation or average over relabelings. These are
  numerical/theorem checks, not proof of physical formation or size scaling.

The scientifically decisive follow-on is to derive an owned, covariant
formation/controller state that creates a connected active backbone on
the permitted timescale while retaining its complete work ledger. If the
native degree-only Hamiltonian cannot select a local geometric window,
that is a precise result about this microscopic seed; adding a topology
term would be a new physical proposal, not an invisible repair. Testing
the active route does not require a new dark abundance, but it does require
an actual preparation rather than assuming it.

## Source custody and review status

Read-only source identities used for this derivation (SHA-256):

- `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- `NATIVE_VOLUME_INCREMENT_PATHWAY.md`:
  `c60b04d6584bf12b7db9ce5b52815c0010aeb13fe0a2a86324cbedd929cf4c6a`.
- `NATIVE_CANONICAL_INCIDENCE_CLOSURE_V001.md`:
  `e6bfa4b392c5131c2367e115866e83a4344dfea73982236ce56fdc090026b56a`.
- `record_addition_compute.py`:
  `4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10`.

These hashes identify reviewed sources, not a preregistered numerical run.
The proposed small continuation has not been executed in this note.
