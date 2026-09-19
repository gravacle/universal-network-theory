# Exact response f-sum bound and the remaining all-L theorem

Date: 2026-09-16

Status: `EXACT_THETA_1_OVER_L_F_SUM__RESIDUE_AND_INVERSE_MOMENT_OPEN`

This is a theorem about the Hamiltonian and observable defined below. It does
not consume any earlier verdict, threshold, or classification. Its purpose is
to separate an all-`L` statement that follows exactly from the finite operator
from the two response estimates that still require a new theorem.

## 1. Setting

Let

```text
G_L = C_L square K_2,                 N = |V(G_L)| = 2L,
H_(L,q) = -A(F_q(G_L)),
```

where `F_q(G_L)` is the `q`-token graph of the three-regular prism. This is the
fixed-charge hard-core-boson Hamiltonian identified exactly in
[`README.md`](README.md). Let `E_0(L,q)` be its Perron--Frobenius ground energy,
let `k_L=2*pi/L`, use the unnormalized convention

```text
n_a(k)=sum_(x=0)^(L-1) exp(i*k*x) n_(a,x),
```

with no `1/sqrt(L)` factor, and define

```text
O_L(k_L)=n_0(k_L)+exp(i*k_L)n_1(k_L).
```

Let `w_a` and `omega_a>0` be its exact spectral weights and excitation
energies. In the stored coordinates this is the total-rail density mode; the
phase on the lower rail is induced by the exact lower-rail relabeling. The raw
mode construction is at
[`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py#L466-L474),
in the source file with SHA-256
`e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7`.

For a hopping edge `(u,v)`, direct evaluation of the double commutator gives
the edge contribution proportional to `|f_u-f_v|^2`, where `f` is the
coefficient of the local density in `O_L`. Every leg or rung edge of the
relabelled prism has

```text
|f_u-f_v|^2 = 2(1-cos(k_L)).
```

Summing those edge contributions and using the ground-state expectation of
the hopping Hamiltonian gives the local identity

```text
m_1(L,q) := sum_a w_a omega_a
          = (1-cos(2*pi/L)) (-E_0(L,q)).                 (1)
```

The density convention here is `rho=q/(2L)`. Throughout the theorem below,

```text
7/48 <= rho < 13/48,    L >= 4.                          (2)
```

## 2. Uniform extensive ground-energy bounds

There are `binom(2L,q)` occupation configurations. Use the normalized vector
which is constant on them as a trial vector for the nonnegative adjacency
matrix `A(F_q(G_L))`. For a fixed base edge, exactly

```text
2 binom(2L-2,q-1)
```

configurations occupy exactly one endpoint, and hence admit the corresponding
token move. Since `G_L` has `3L` edges, the average token-graph degree is

```text
3L * 2 binom(2L-2,q-1) / binom(2L,q)
  = 3q(2L-q)/(2L-1).                                    (3)
```

Rayleigh--Ritz and Perron--Frobenius therefore give the lower bound in

```text
3q(2L-q)/(2L-1) <= -E_0(L,q) <= 3q.                     (4)
```

The upper bound follows because each of the `q` tokens has at most three
available moves, so every token-graph row has degree at most `3q`.

Condition (2) implies

```text
q >= 7L/24,              q < 13L/24,
2L-q > 35L/24.
```

Substitution in (4) yields the convenient uniform constants

```text
(245/384)L <= -E_0(L,q) < (13/8)L.                       (5)
```

These constants are deliberately elementary rather than optimized.

## 3. Exact `Theta(1/L)` f-sum theorem

For `L>=4`, `x=2*pi/L` lies in `[0,pi/2]`, and

```text
8/L^2 <= 1-cos(2*pi/L) <= 2*pi^2/L^2.                   (6)
```

Combining (1), (5), and (6) proves, uniformly for every integer sector obeying
(2),

```text
245/(48L) <= m_1(L,q) < 13*pi^2/(4L).                   (7)
```

Thus the exact response f-sum is `Theta(1/L)` on the entire density band. This
is an all-`L` theorem, not a fit to the authenticated `L=4,...,12` rows.

One further exact but weak consequence is useful for locating the boundary of
the argument. Since every row degree of the token graph is at most `3q`, the
spectrum of `H_(L,q)` lies in `[-3q,3q]`. Hence every excitation satisfies
`omega_a<=6q`, and, writing `S=sum_a w_a`,

```text
m_1 <= 6q S
    ==> S >= 245/(156 L^2).                              (8)
```

Equation (8) is only a vanishing lower bound. Neither (7) nor (8) proves the
observed `S=Theta(1)`.

## 4. Why the f-sum does not control the desired quantities

Let

```text
M_-2 = sum_a w_a/omega_a^2.
```

If `w_*` denotes the exact weight of the lowest-support pole group, the
following abstract positive spectral measure demonstrates the logical gap:

```text
mu_L = exp(-L) delta_(exp(-L)) + delta_(20/L).
```

It has

```text
S       = 1+exp(-L),
m_1     = 20/L + exp(-2L) = Theta(1/L),
w_*     = exp(-L) -> 0,
M_-2    = exp(L) + L^2/400.
```

Its support is bounded and it even contains an explicit `O(1/L)` response
pole. Nevertheless the lowest pole-group weight vanishes and the inverse
square moment grows exponentially. This measure is not asserted to be the
ladder's spectral measure. It is a counterexample to deriving the two desired
bounds from positivity, the f-sum scale, bounded spectral support, and the
existence of a low excitation alone.

The finite-volume LSM twist does not repair this gap. Its variational state is
in momentum `2*pi*q/L`, which is generally not the probe's `m=1` momentum
`2*pi/L`, and an energy estimate does not itself give a matrix-element lower
bound.

Perron--Frobenius positivity also supplies no uniform comparison of ground
state amplitudes and hence no uniform lower bound on the projected response
weight.

## 5. Why exclusion-process spectral-gap theorems do not transfer

The Hamiltonian is minus the **adjacency** matrix of the token graph.
The symmetric-exclusion generator instead uses its graph Laplacian,

```text
L_excl = D_conf - A(F_q(G_L)).
```

For a configuration `X`,

```text
D_conf(X) = 3q - 2 e_G(X),
```

where `e_G(X)` is the number of base-graph edges with both endpoints occupied.
This value varies with `X`. Consequently

```text
H_(L,q) = L_excl - D_conf
```

contains a nonconstant diagonal potential; it is not the exclusion Laplacian
plus a scalar. Aldous-type gap results therefore cannot be substituted for a
gap theorem for this Hamiltonian.

This operator distinction is also visible in the primary graph literature:

- [Caputo--Liggett--Richthammer, arXiv:0906.1238](https://arxiv.org/abs/0906.1238)
  proves the interchange/random-walk spectral-gap theorem, i.e. a Markov
  generator statement.
- [Dalfó et al., arXiv:2012.00808](https://arxiv.org/abs/2012.00808) studies
  token-graph **Laplacian** spectra and their inclusions.
- [Reyes--Dalfó--Fiol, arXiv:2310.16929](https://arxiv.org/abs/2310.16929)
  gives adjacency spectral-radius bounds and special exact results, including
  a walk-regular `q=2` case. It does not provide a fixed-density,
  momentum-resolved pole-weight or inverse-moment theorem of the form needed
  here.

Rigorous Luttinger-liquid results also exist for other precisely specified
one-dimensional fermion models; examples include the small-repulsive-coupling
one-dimensional Hubbard theorem in
[Mastropietro, arXiv:cond-mat/0502415](https://arxiv.org/abs/cond-mat/0502415)
and the thermodynamic response/correlation results in
[Benfatto--Falco--Mastropietro I, arXiv:1303.3681](https://arxiv.org/abs/1303.3681)
and
[II, arXiv:1303.3684](https://arxiv.org/abs/1303.3684). Those papers do not
state the required finite-volume pole-projector bounds for this strong-coupling
hard-core-boson ladder, and this note does not assume that their hypotheses
cover it. The same-ladder work cited in [`README.md`](README.md) remains the
appropriate physical phase identification, but its field-theory and numerical
evidence is not an unconditional repository-internal proof of the estimates
below.

## 6. Exact missing theorem

The direct missing statement is: there exist `w_0,C>0`, independent of `L` and
uniform over (2), such that

```text
w_*(L,q) >= w_0,
M_-2(L,q) <= C L^2.                                     (9)
```

A structurally sufficient, stronger pair of results would be:

1. **Response-sector Poincare bound.** Every spectral point reached by the
   `m=1` density probe satisfies `omega_a>=c/L` for a uniform `c>0`.
2. **Acoustic-projector overlap bound.** A precisely specified lowest acoustic
   projector `Pi_*` satisfies
   `||Pi_* n_(2*pi/L)|0>||^2>=w_0` uniformly.

Indeed, result 1 and the upper half of (7) imply

```text
S <= (L/c)m_1 <= 13*pi^2/(4c),
M_-2 <= (L^2/c^2)S <= 13*pi^2 L^2/(4c^3),
```

while result 2 supplies the missing residue. Together with positivity and the
f-sum, these give the desired two-sided `Theta(1/L)` bound for the specified
pole.

Proving only the response-sector lower gap does **not** prove nonvanishing
weight in one pole group; proving only a large residue does **not** prevent a
smaller weak pole from making `M_-2` large. Both controls are substantive.

## 7. Exact-pole definition required before an all-L proof

The finite data files label `Delta_act` using an adaptive numerical floor that
contains an eigen-residual term. That is a valid numerical certification rule,
but it is not a residual-independent mathematical observable across all `L`.

An unconditional theorem must first choose one of the following and keep it
fixed:

- the exact first-support pole
  `min{omega_a>0 : ||Pi_a n_k|0>||^2>0}`;
- a symmetry-defined or adiabatically tracked acoustic projector; or
- a deterministic analytic threshold sequence, together with a proof relative
  to that sequence.

The theorem may then call that precisely defined projector's weight `w_*`.
Silently promoting the finite numerical `w_floor` into an all-`L` exact
definition would mix numerical resolution with physics and is not valid.

## 8. Decision boundary

The exact status after (7) is therefore

```text
uniform all-band m_1=Theta(1/L):             PROVED
uniform S=Theta(1):                           OPEN (finite rows support it)
uniform registered/acoustic w_*>=w_0:        OPEN
uniform M_-2=O(L^2):                         OPEN
unconditional internal registered z=1:      OPEN
```

The new f-sum theorem is a necessary and correctly scaled bridge. It is not a
substitute for the missing response-sector and matrix-element control.
