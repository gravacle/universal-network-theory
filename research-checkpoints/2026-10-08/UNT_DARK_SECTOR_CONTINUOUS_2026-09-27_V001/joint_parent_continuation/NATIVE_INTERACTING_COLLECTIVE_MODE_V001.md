# Exact interacting native incidence sector: a collective-mode discriminator

2026-09-29. Analytical derivation only. No new propagation, fit, formation,
microscopic term or edit of the existing frozen evidence.

The original degree penalty supplies a genuinely interacting test that is
still tiny: the full N=2 incidence space has dimension16, and its exactly
invariant symmetry-bright space has dimension6. Its weak-flip spectrum is
anharmonic, but the first correction is SOFTENING and its source ladder is
not the ladder of a positive-mass quartic oscillator. The inherited h=1/2
must be checked with the exact matrix, not inferred from that asymptote.

## 1. A restriction of the actual parent, not a frozen two-link toy

Use one N=2 bipartite slab. Keep all four incidence qubits and all four native
flip terms. Carriers, writers and reservoirs are blank; all copy/port
couplings are off. Choose a fixed uniform record occupancy q=0 or q=1 at
all four nodes, with a fixed content in the occupied case. These are exact
held sectors because the held Hamiltonian does not change the record
registers. They are declared comparison preparations, not a demonstration
that the occupied sector has formed or a replacement of the saved formed
states by ground states.

The inherited coefficients are

    Omega=U_d=d_*=epsilon_r=1, Delta=4, lambda_R=1/2,
    h=Omega/N=1/2.

Carrier transfer and current-square terms both annihilate the genuinely
blank-carrier sector; their removal here is therefore exact, not an omission
of a nonzero current cost. Record onsite energy remains. Write the four
incidence bits as the vertices of the rook graph C4: two bits are adjacent
when their bipartite arrows share one endpoint. Expanding BS06 and BS11 gives

    H_q=C_q I + kappa_q M + 2U sum_<ij> n_i n_j - h sum_i X_i,
    M=sum_i n_i,
    C_q=4U d_*^2+4 epsilon_r q=4+4q,
    kappa_q=Delta+2U(1-2d_*)-2lambda_R q=2-q.           (1)

Here U=U_d=1 and the pair sum has FOUR terms. The candidate uniform source
is the already-owned incidence diagnostic H_q-f(t)M: f has energy units,
the bare second source contact is zero, and its work rate is -dot(f)<M>.
No physical strain, mass density, clock redefinition or volume is assigned.

Changing the uniform record sector at a fixed incidence state changes the
Hamiltonian by 4I-M. It is not a free source of energy or a preparation
protocol. For initially blank links the absolute energy is 4 or8 and the
held energy variance is 4h^2 in either case. Subsequent source-off evolution
of those states is well defined, but is not needed for the spectral test.

Holding only two sharing links and suppressing the other flips would NOT be
an invariant restriction of (1). A two-link model would need a separately
owned projection or changed Hamiltonian. The four-link construction avoids
that ambiguity.

## 2. The exact six-state bright block and all source entries

The restricted operator and M have the square's dihedral permutation
symmetry. This is a symmetry of this uniform, blank-carrier restriction,
not a declaration that layer exchange is a physical gauge equivalence of
the general directed parent. Normalized orbit sums give the basis

    0: empty (1 configuration),
    1: one occupied link (4),
    o: two opposite occupied links (2),
    a: two adjacent occupied links (4),
    3: three occupied links (4),
    4: four occupied links (1).

In that order H_q=C_q I+D-hF, where

    D=diag(0,kappa,2kappa,2kappa+2U,3kappa+4U,4kappa+8U),

          [ 0  2    0      0    0    0 ]
          [ 2  0  sqrt2    2    0    0 ]
    F =   [ 0 sqrt2 0     0  sqrt2  0 ] ,
          [ 0  2    0     0    2    0 ]
          [ 0  0  sqrt2    2    0    2 ]
          [ 0  0    0     0    2    0 ]

    M=diag(0,1,2,2,3,4).                                (2)

For example, one-to-adjacent pairs have eight flip connections and normalized
matrix entry8/sqrt(4*4)=2; one-to-opposite pairs have four and entry sqrt2.
Every entry is inherited. Uniform source strength changes only D to D-fM.
Both (1) and (2) retain the absolute constants.

Let V be the16-by6 normalized orbit-sum isometry. Exactly,

    H_full V=V H_bright, M_full V=V M_bright, V^dagger V=I. (3)

Its orthogonal ten-dimensional complement is invariant and is not discarded
from the full model. It has zero coupling to the bright block under M, but
can have its own transitions and can be populated by other preparations or
nonuniform ports. The blank-link state belongs to the bright block. For
h>0 the connected, strictly negative off-diagonal full incidence matrix has
a unique positive ground eigenvector, which is in this bright block.
The next bright eigenvalues need not be the next eigenvalues of the full
sixteen-dimensional space. Keep that distinction in all labels.

The exact source sum rule is

    [M,[H_q,M]]=h sum_i X_i.                            (4)

For any exact eigenstate a, including dark states,

    2 sum_b (E_b-E_a)|M_ab|^2=h <a|sum_i X_i|a>.         (5)

This includes signed excited-state strengths. It fixes a microscopic moment;
it is not an independently adjustable positive oscillator mass/contact.

## 3. Controlled weak-flip result and its explicit domain

For kappa,U>0, the first three eigenvalues of D within the bright block are
0,kappa,2kappa and are nondegenerate. Denote their analytic continuations
E_0,E_1,E_o. Ordinary nondegenerate perturbation theory applied to the EXACT
matrix (2), without deleting momentum or source terms, gives

    E_0=C-4h^2/kappa+O(h^4),
    E_1=C+kappa+[2/kappa-4/(kappa+2U)]h^2+O(h^4),
    E_o=C+2kappa+[2/kappa-2/(kappa+4U)]h^2+O(h^4).

Consequently

    K_spec=E_o-2E_1+E_0
          =-8U(kappa+6U)h^2/[kappa(kappa+2U)(kappa+4U)]
            +O(h^4).                                   (6)

Its leading coefficient is -4/3 for blank records, -56/15 for full records.
This is a negative DISCRETE TRANSITION-SPACING correction. It is not yet a
continuous classical action derivative, negative kinetic norm, or instability
of the finite bounded quantum Hamiltonian.

There is a genuine controlled small-h domain. Let g_min be the minimum
separation of the six entries of D and use ||F||=4. Resolvent circles of
radius g_min/2 stay separated for |h|<g_min/8, including complex h. Each
branch is analytic there. Product-Z parity maps h to -h, so these energies
are even in h and the first omitted term in (6) is fourth order. For the
two inherited diagonal choices g_min=2 and1 respectively. The sufficient
domains are therefore |h|<1/4 and |h|<1/8. The inherited h=1/2 lies outside
both sufficient bounds: (6) does not assert its native finite-h sign.

An explicit conservative remainder is available if desired. Set
R=g_min/16. For |h|<R, Cauchy's estimate using |E_j(z)-E_j(0)|<=4R on
|z|=R gives the remainder of (6) bounded by

    16R (|h|/R)^4/[1-(|h|/R)^2].                       (7)

This loose bound certifies the negative sign sufficiently close to zero;
it is not a precision estimate at the inherited parameter. Distinct
small-h controls probe this expansion, not a retuning of the native theory.

The corresponding source entries, with eigenvector signs continued from
the positive orbit sums, are

    M_01=2h/kappa+O(h^3),
    M_1o=sqrt2 h/kappa+O(h^3),
    M_1a=2h/(kappa+2U)+O(h^3).                          (8)

Thus |M_1o|^2/|M_01|^2 tends to1/2, whereas a linearly sourced canonical
oscillator requires2 between its first two ladder steps. The adjacent-pair
branch is compulsory; its ratio is kappa^2/(kappa+2U)^2. For U->0 the pair
branches become degenerate, and the nondegenerate expansion cannot assign
either as the unique oscillator. Their summed ratio tends to3/2, agreeing
with the compact four-spin symmetric ladder, not an unbounded bosonic ladder.

## 4. What this does and does not derive about a mechanical mode

For any fixed finite Hermitian Hamiltonian one can use its exact eigenstate
populations as projective-Hilbert-space actions: with normalized pure state
coefficients c_a, take I_a=hbar|c_a|^2 for a>0 and relative phase angles.
The exact expectation energy is E_0+sum_a (E_a-E_0)I_a/hbar. It is affine
on that simplex. This fact does not make every quantum spectrum harmonic;
the different fixed transition gaps, selection rules, source matrix entries
and compact action domain still carry the interactions. It does mean that
an amplitude-dependent classical collective oscillator is not obtained just
by calling the lowest three exact eigenvalues an action curve.

A three-level quantum effective Hamiltonian can encode (6) as

    E_0+(E_1-E_0) n+K_spec n(n-1)/2, n=0,1,2.

That interpolation is exact on those levels, but neither canonical bosonic
source normalization nor a controlled large-occupation limit follows. The
missing source entries in (8), higher bright levels, compact saturation and
off-block channels remain explicit. A positive constant-mass quartic parent
would need a controlled limit that reproduces these observables and its own
positive normal-form coefficient, not merely a positive coordinate Taylor
coefficient. N=2 spin-coherent factorization has no large-spin parameter
that automatically bounds the discarded entanglement.

Elimination also cannot create an independent free contact. For a retained
projector P, Q=1-P, the exact stationary Feshbach operator is

    H_eff(E,f)=P H(f)P+P H(f)Q[E-QH(f)Q]^-1 QH(f)P.     (9)

Its source derivatives and energy dependence belong to the same parent.
Approximating it requires a specified spectral separation and source bound;
dropping its derivative terms while adding a tunable contact would change
the model. Equation(9) is an energy-domain identity, not time-local dynamics
for an arbitrarily driven eliminated sector.

## 5. Smallest useful prospective calculation

The MAIN cases are q=0,1 at inherited h=1/2,U=1. Build the full16-dimensional
operator directly from degrees/BS terms and independently build (2). No
formation, large lattice or heavy state vector is needed.

Retain all sixteen eigenvalues and all source matrix entries or degenerate
projector-resolved transition strengths; retain the six bright eigenvalues
and the ten-dimensional complement, rather than choosing an oscillator-like
pair. Check (3)-(5), absolute energies and the initially blank-link mean and
variance. Report the actual finite-h spacing K_spec of the first three
ordered BRIGHT levels, their source ladder ratios, all other bright source
strengths, and the exact zero bright-to-dark uniform-source coupling. A
degeneracy is represented by its full projector, not a chosen eigenvector.

Prospective analytical-control cases may use h=1/40,1/80,1/160 with the same
two diagonal sectors and U=1. These explicitly changed flip strengths are
coefficient controls, not additional native physical cases. Check convergence
to (6) and (8) without demanding a chosen sign at h=1/2. The complete matrices
are kilobytes, and no long-run checkpoint or larger propagation is required.

This directly tests whether the first genuinely interacting native source
channel supports the proposed one-mode hardening mechanism. Either result
is useful: the complete source spectral data identifies what a later
controlled collective reduction must actually match. It does not by itself
identify physical strain, gravity, cosmological pressure or a soft continuum.

## Source identities

* `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
* `NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md`:
  `335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c`.
* `native_carrier_ruler_v001.py` (inherited coefficient declaration, not run):
  `00a09a8c3caffc0ffe8df76a54787ddc010ec4d5196bedf773c34258d656b252`.

Hashes bind source bytes, not scientific acceptance or a physical metric map.
