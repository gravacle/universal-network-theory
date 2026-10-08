# Actual empty-state response: first nonzero kernel and signed source work

2026-09-30. Independent hand derivation by `short_path_adversarial`, with
root independently checking the leading coefficient and the work kernel.
No numerical evaluation, import, new preparation, bath, selected age, fitted
coefficient or physical normalization. This concerns the specified finite-N
held-record first-degree-tie parent, not every native construction or UNT.

## Premises, ancestry and genuinely new content

Keep precisely

    Hbar=H-C_N=2U(C_L+C_R)-h sum_e X_e,
    h=Omega/N,  N>=2, U,Omega>0,
    T=2U(C_L-C_R),  H_theta=H+theta(t)T,
    |e>=the empty-edge initial basis state.                 (1)

Uniform records remain held, carriers blank and ports off. The initial state
does not depend on theta. The source is the adopted opposite-layer affine
source; H_thetatheta=0 in this chart. No physical ruler/volume is inferred.

The actual-state controls in `NATIVE_FORMATION_OR_ACTUAL_STATE_DECISION_V001.md`
are correct: T|e>=T Hbar|e>=0; the preparation-time impulse is exactly zero;
the source variance first appears at fourth order; its positive weight does
not establish passivity. The earlier `NATIVE_TEMPORAL_KERNEL.md` treats
record-copy currents and held-source questions, while the 96D
`NATIVE_ENERGY_SOURCE_AGE_AVERAGE_V001.md` treats a different apparatus and
bounded age averaging. Neither inspected note gives the coefficient below.
No claim is made to have independently re-audited every formation mechanism
listed in the decision note. The new result is this parent's unaveraged
two-time coefficient and its finite-window work sign, without ground-state
substitution. Root's separate factorial-moment note supplies complementary
uniform-in-N bounds, not the Taylor remainder used here.

## 1. Two-time expansion, with all contributing sectors retained

Use a=t/hbar and b=s/hbar; these have inverse-energy units, not an assigned
physical age calibration. Define

    phi(t)=T_H(t)|e>,  v=T Hbar^2|e>,  w=T Hbar^3|e>,
    A=-v/2,  B=w/6-Hbar v/2.

Expanding both exponentials, with the two null identities above, gives

    phi(t)=a^2 A+i a^3 B+O_N(a^4).                        (2)

Each unordered two-edge graph in Hbar^2|e> has coefficient 2h^2. Only
two-edge stars survive T. Their number is

    M_star=2N binom(N,2)=N^2(N-1),
    ||A||^2=4U^2 h^4 M_star.                              (3)

Every star has diagonal Hbar energy 2U. Its T sign distinguishes the layer,
but does not change that energy. A flip changes edge-number parity, so
v^dagger Hbar v=2U||v||^2. The two-edge projection of w is 2U v: before
two flips the diagonal energy is zero, and the remaining diagonal action
after those flips is exactly 2U. It follows that

    B_star=(4U/3)A,   A^dagger B=(4U/3)||A||^2.             (4)

Other components of B have odd edge number and are orthogonal to A. They
have not been dropped from the state or later response; they simply cannot
contribute to this first scalar cross coefficient.

For the PLUS-source convention

    chi(t,s)=(i/hbar)<e|[T_H(t),T_H(s)]|e>, t>=s,
    delta<T(t)>=-integral_0^t chi(t,s)theta(s) ds,

the commutator is twice i times the imaginary part of phi(t)^dagger phi(s).
Equations (2)--(4) therefore yield

    C_*=(32/3)U^3 h^4 N^2(N-1)>0,
    chi(t,s)=(C_*/hbar) a^2 b^2(a-b)
                         +O_N((|a|+|b|)^7)/hbar.         (5)

Reality of Hbar,T and |e> makes chi odd under simultaneous reversal
(t,s)->(-t,-s), so there is no total-degree-six term. Antisymmetry and the
double zero in each argument also give an analytic factor a^2 b^2(a-b).
This is a fixed-N, fixed-U/Omega Taylor statement. No N-uniform Taylor
remainder or numerical useful-age interval is asserted. At s=0 the exact
kernel is zero, not merely its leading coefficient. A later-age impulse or
a held source is different. A lag-only or ground susceptibility cannot
replace the explicit a,b dependence in (5).

## 2. The work functional, not just the sign of chi

Layer exchange sends T to -T and preserves H and |e>. Consequently the
unforced mean <T(t)> is exactly zero at every age. First-order source work
is zero here by this symmetry, unlike a generic nonstationary preparation.
For theta=epsilon f(t), complete external work is

    W=integral dot(theta)<T>_theta dt,
    W^(2)=-integral dt dot(f(t)) integral_0^t ds chi(t,s)f(s).
                                                               (6)

There is no direct quadratic contact in (1). A different source chart or
source-dependent preparation would change this ledger. Switching terms must
be included for discontinuous sources. The endpoints below use the same H.

For a smooth cyclic source let q(a)=f(hbar*a), compactly supported in the
short window 0<a<L. Substituting (5) and integrating by parts gives

    W^(2)_lead=(C_*/2) integral_0^L da integral_0^L db
                         q(a) K(a,b) q(b),
    K(a,b)=3a^2 b^2-2 max(a,b) min(a,b)^3.                 (7)

For example, before symmetrization the integrand on a>b is
q(a)q(b)[3a^2 b^2-2ab^3]. This follows by differentiating
a^2 b^2(a-b) with respect to the later argument; the equal-time term is
zero. For a fixed smooth rescaled shape q(a)=q_0(a/L), the leading work is
O_N(L^6) and the next kernel contribution O_N(L^8). These are symbolic
small-window statements, not a chosen experimental time.

Crucially, the kernel in (7) is not positive semidefinite. At 0<a<b its
two-point diagonal entries are a^4,b^4 and its determinant is

    a^4 b^2 [b^2-(3b-2a)^2] < 0.                         (8)

By continuity, smooth disjoint sufficiently narrow pulses centered at two
distinct positive fractions of the window inherit a negative quadratic
direction. The corresponding pulse areas have opposite signs. This is an
existence proof for a bounded smooth cyclic source shape, not a selected
formation pulse, reset or numerical protocol. For each fixed finite N one
can first choose such a fixed shape, then take a sufficiently short window
so the L^6 term dominates, and finally sufficiently small source amplitude
so the quadratic-response sign controls the actual work. Equivalently the
quadratic coefficient is defined by the amplitude-to-zero limit before its
short-window limit. No uniform N-dependent control family is asserted.

Thus this particular empty preparation is not passive even against every
weak cyclic probe in this one source channel. A positive leading chi for
t>s is not a passivity theorem. This is not a claim that every pulse extracts
work: a rectangular source held from 0 to T and switched off has, including
both switch works,

    delta<T(T)>_linear=-theta_0 C_* (T/hbar)^6/12
                                      +O_N(theta_0(T/hbar)^8),
    W_quadratic=+theta_0^2 C_* (T/hbar)^6/12
                                      +O_N(theta_0^2(T/hbar)^8). (9)

The initial switch costs theta_0<T(0)>=0 and the final switch contributes
-theta_0<T(T)>. Equation (9) is a sign/control example, not an adopted pulse.

## 3. Conservation and decision boundary

Negative cyclic work means the external source actuator receives energy;
the final unforced-H mean energy decreases by the same amount. The empty
state is not the ground state, so this violates neither total energy
conservation nor the earlier fixed-H ground-overlap bound. During an imposed
probe the Hamiltonian is not fixed. This mathematical controllability result
does not install an autonomous energy destination, prepare the ground, specify
a native source controller, or eliminate formation costs. Its finite source
work would have to be owned in any proposed preparation protocol.

The shortest substantive conclusion is therefore to retain an age-dependent,
potentially active actual-state kernel. Neither the original empty state nor
its ground comparator may be silently promoted to a passive constitutive
medium. Root's independent fixed-age factorial bound additionally constrains
the size of this response as N grows, without changing the sign result.
Any finite-age constitutive limit must control its memory and work, or supply
a separately owned formation/boundary mechanism. Physical radius, density,
volume, clock and astronomical normalization remain absent. All eleven lanes
and all physical-promotion flags remain unchanged.

## Read source identities

- `NATIVE_FORMATION_OR_ACTUAL_STATE_DECISION_V001.md`:
  `513ed019e9081542c8053cb9fd99944eacec16bac35708c628ee965717ed0379`.
- `NATIVE_DEGREE_TIE_FULL_PARENT_ODD_RESPONSE_V001.md`:
  `ac17bd126aa2f05032b674180b36caa72faa6164879aa3ab8b9960e57b86a815`.
- `NATIVE_DEGREE_TIE_EMPTY_PREPARATION_BOUND_V001.md`:
  `d24a466fa69f1e613f7cea7d59eff1a15d881c7b1016a57a62e29a0d59451257`.
- `NATIVE_TEMPORAL_KERNEL.md`:
  `ad3b095e8a687e76bc7581d79cbb125e92f8b5a61a75e9c8f785a2ebe00fc534`.
- `NATIVE_ENERGY_SOURCE_AGE_AVERAGE_V001.md`:
  `764bb3f333aab4750fcb564c043ad715343dfaf15a5519e9fafa3b7cb18cf4d6`.

The full-parent coefficients and kernel/work formulas here are hand-derived,
not numerically verified measurements. Source searches across the enclosing
dark directory found no earlier statement of this empty-tie degree-five
coefficient; this is a scoped novelty check, not a literature-priority claim.
