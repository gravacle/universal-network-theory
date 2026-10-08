# Conditional network growth: the acceleration requirement

2026-09-27. Construct ID: `CONDITIONAL_NETWORK_GROWTH_ACCELERATION_SCREEN_V001`.
Analytical necessary-condition screen; no numerical run, new native rule,
cosmological fit, adopted volume/clock map, or replacement of the primary
active/maintenance hypothesis.

## Resident inputs and adoption ceiling

The following resident notes were read completely after flag checks; no
dataless source was read or hydrated:

- `NATIVE_INCIDENCE_FORMATION_SPEED_BOUND_V001.md`, SHA256
  `8118207e2da4bdae41143f6a90d48dd3be9f450371c688f508eabe776ccc6229`:
  native BS flip normalization h_N = Omega/N, its exact incidence bound,
  and the required port/commutator assumptions.
- `Q4_FIXED_CELL_VOLUME_SCREEN_V001.md`, SHA256
  `f9995fcb2bb09c1f517f4537ce734376485ea9571662e347430a33feaa331b39`:
  an explicitly adopted covariance-to-metric map and its fixed-cell range.
- `NATIVE_RECORD_CURRENT_AND_ENERGY_INTERFACE_AUDIT_V001.md`, SHA256
  `5fd894d41f10eb446d73c575b379caa84fa189c539e0fb6a1e49c2de4f4bd359`:
  conserved retained occupations during source-off hold, local formation
  sources, the distinct carrier current, and the complete energy ledger.

These sources do not identify retained-record count, link incidence, cell
count, graph width, or physical volume with one another. The conditions
below test an additional proposed geometric completion, not an implication
already owned by those sources.

## 1. What physical cell growth would have to accomplish

Declare a fixed comoving domain with positive physical volume V(tau), a
proper-time clock tau, and an isotropic volume scale factor

    a(tau) = [V(tau)/V_ref]^(1/3).

Without homogeneity/isotropy this is a domain-volume scale, not automatically
the scale inferred from cosmological light propagation. Declare identical,
nonoverlapping, consistently glued physical cells, with effective cell
count K and physical cell volume nu, so that

    V = K nu,       Gamma_K = d ln K/dtau,
    Gamma_nu = d ln nu/dtau,       Gamma = Gamma_K + Gamma_nu.       (1)

Smooth K is a coarse-grained or expectation-level description requiring its
own justification; a finite integer birth process need not be differentiable.
Subdivision of the same physical region is not expansion: if refinement
increases K while nu falls as 1/K, Gamma remains zero. New graph edges are
not by definition new physical cells.

On any smooth interval, exactly,

    H := a'/a = Gamma/3,
    a''/a = Gamma'/3 + Gamma^2/9.                              (2)

Thus an expanding accelerating branch requires

    Gamma > 0,             Gamma' + Gamma^2/3 > 0.             (3)

Primes denote the declared proper time throughout. Neither monotonic count
growth nor increasing volume alone guarantees the second inequality.
For fixed nu and K proportional to tau^p on tau > 0, expansion has p > 0
and acceleration occurs precisely when p > 3. The case p = 3 coasts;
0 < p < 3 decelerates. In particular:

    K = K_0 + r tau, r > 0:
        a''/a = -2 r^2/[9(K_0+r tau)^2] < 0;
    K = K_0 exp(g tau), g > 0:
        H = g/3,   a''/a = g^2/9 > 0.                        (4)

Constant absolute cell production and constant fractional production are
therefore physically different candidate laws. The exponential example is
kinematically sufficient only under its declared volume/clock assumptions;
it supplies no energy, work, cell-creation mechanism or stress law.

For nonidentical cells with a fixed membership, V = sum_i nu_i. Setting
w_i = nu_i/V and gamma_i = nu_i'/nu_i gives

    Gamma = sum_i w_i gamma_i,
    Gamma' = sum_i w_i gamma_i' + Var_w(gamma_i).               (5)

Creation/removal contributes an additional physical-volume source J_V to
V', so Gamma = sum_i w_i gamma_i + J_V/V between suitably coarse-grained
events. This is bookkeeping until cell gluing and that source are owned.
Changing a boundary or recounting cells must not masquerade as J_V.

If the prior q4 interface is additionally chosen for each identical cell,
nu = ell^3 sqrt(det F), then

    Gamma_nu = 3 ell'/ell + (1/2) tr(F^(-1)F').                (6)

The fixed-ell, fixed-cell covariance bound limits its endpoint volume, but
does not impose a universal finite expansion ratio from arbitrarily small
positive initial F. Cell creation or a varying ruler is an additional law,
not an unlogged way around the fixed-cell screen.

## 2. A native bound applied only through an explicit incidence-volume map

Write m(t) = <M(t)> for total expected occupied incidence, not a record
count or a realized classical graph. The resident speed theorem already
proves, for fixed Omega and the verified native unitary bulk/ports,

    |sqrt(m(t))-sqrt(m(s))| <= (Omega/hbar)|t-s|.               (7)

It needs [H_rest(t),M] = 0, includes the listed native formation terms,
and excludes unverified incidence-changing ports, resets and postselection.
No derivation is repeated here.

Now impose TWO additional premises for this test: physical volume is
V = v_m m with fixed v_m > 0, and native time equals proper time up to a
fixed conversion absorbed into Omega. This identifies volume with the
first moment specifically; it is not an assertion about nonlinear ensemble
averages or individual graph outcomes. Starting with m_0 > 0,

    m(tau) <= [sqrt(m_0)+(Omega/hbar)tau]^2,
    a(tau) <= (v_m/V_ref)^(1/3)
              [sqrt(m_0)+(Omega/hbar)tau]^(2/3).              (8)

Under this completion there cannot be an indefinitely sustained expanding
branch with a'' >= 0. If at some tau_1 the slope is a'_1 > 0 and a'' >= 0
thereafter, convexity requires

    a(tau_1+T) >= a_1 + a'_1 T.

That positive linear lower bound eventually exceeds the sublinear upper
bound obtained by restarting (8) at tau_1. More usefully, any proposed
finite interval of nonnegative acceleration must satisfy

    (1+H_1 T)^3 <= [1+(Omega/(hbar sqrt(m_1)))T]^2,
    H_1 = a'_1/a_1 > 0.                                     (9)

The cubic left side eventually defeats the quadratic right side. This is
a finite-duration necessary test, not a sufficient trajectory or an
empirically calibrated lifetime. It is stronger than merely rejecting an
exact positive exponential continued forever.

**No pointwise acceleration bound follows from (7) or (8).** For example,
a positive trial m = m_1 exp(3H tau) has a proportional to exp(H tau).
Choosing 3H sqrt(m_1)/2 < Omega/hbar makes this accelerating trial compatible
with (7) on a sufficiently short interval. This only shows compatibility
with the displayed necessary bound, not realization by the native
Hamiltonian or satisfaction of every stronger finite-occupancy condition.
Finite accelerating episodes, even repeated ones separated by sufficient
deceleration, have not been excluded.

At fixed finite BS width, m <= N^2 is a further, stronger late-time ceiling.
The uniform-in-N bound (7) additionally prevents rescuing (8) simply by
choosing a larger fixed slab. A growing Hilbert space N(t), new graph ports,
or a changed flip normalization is a different dynamical premise. If
native time is instead t(tau), (8) contains t(tau); a nonconstant lapse can
alter its proper-time consequence and must be derived, not selected after
seeing the desired acceleration. In particular

    d^2a/dtau^2 = [a_tt - (L_t/L)a_t]/L^2,
    L = dtau/dt > 0.                                        (10)

## 3. What must be supplied before this can explain the inferred effect

Native source-off retained occupations satisfy [H,q_v^r] = 0 individually.
Their count therefore cannot itself be a growing K in that hold. During
formation their local sources are not incidence sources; writing records
does not bypass (7). A source-off network can nevertheless evolve its link
correlations and cell interpretation, if the latter is independently owned.
No equality between retained storage, ongoing maintenance power, and
physical volume has been established here.

Passing (3) is only kinematics. A physical completion still needs the full
metric/deformation and energy/work ledger, including formation donors,
ports, storage, interaction and reference terms. If K is an independent
population variable, varying it can carry chemical/generalized work in
addition to mechanical -p dV. One cannot set p = -dE/dV along an arbitrary
cell-creation path while dropping those terms. Nor is an expanding cell
count automatically the vacuum-like maintenance stress in the primary A/M
allocation law.

**One implementable next acceptance test:** before another growth run,
freeze a single proposed same-parent cell/gluing map, its proper-clock
conversion, and its actual growth evolution with a complete energy ledger.
Use its predicted K(tau), nu(tau) to test (3), without a fitted expansion
history; if it identifies V with fixed multiples of native incidence, also
test (9) on the claimed accelerating interval. A model that cannot yet
specify those inputs has not supplied an expansion prediction. A model
that passes this gate still needs a stress/observable bridge; this optional
screen neither replaces primary A/M nor rejects other network completions.
