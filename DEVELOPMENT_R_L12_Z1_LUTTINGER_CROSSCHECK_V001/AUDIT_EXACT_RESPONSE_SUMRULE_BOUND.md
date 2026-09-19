# Hostile audit of the exact response sum-rule bound

Date: 2026-09-16

Disposition: `PASS`

## Scope and custody

This is an independent, read-only audit of
[`EXACT_RESPONSE_SUMRULE_BOUND.md`](EXACT_RESPONSE_SUMRULE_BOUND.md) at
SHA-256
`5734cda284e85ae0b51ff60b85664f470a407c95daf91b47835963539398e2f8`.
It independently recomputes the local Fourier relabeling, finite operator
identity, every displayed combinatorial factor and inequality constant, the
counterexample, the exclusion-operator distinction, and the stated missing
theorem. The exact result uses only the Hamiltonian, observable, density band,
and elementary finite-dimensional estimates defined in the theorem note. It
does not consume an earlier verdict, fit, threshold, Stage-6 classification,
or theorem from another proof surface. The cited literature is checked only
for the note's comparison and non-transfer statements. This audit does not
modify the theorem note or any frozen artifact.

## Independent Fourier, operator, factor, and constant checks

Write the shifted lower-rail stored coordinate as `x_old` and the ordinary
prism coordinate as `z=x_old-1`. The stored total-rail coefficient on that
site becomes

```text
exp(i*k*x_old) = exp(i*k) exp(i*k*z).
```

Thus, in the relabelled local prism, the coefficients are exactly
`f_(0,x)=exp(i*k*x)` and `f_(1,x)=exp(i*k)exp(i*k*x)`, as stated in the
theorem. Direct evaluation on upper-leg, lower-leg, and rung edges gives in
all three cases

```text
|f_u-f_v|^2 = 2(1-cos(k)).
```

For one hopping edge
`H_e=-(b_u^dagger b_v+b_v^dagger b_u)`, direct commutator evaluation gives

```text
(1/2) <[O^dagger,[H_e,O]]>
  = -(1/2)|f_u-f_v|^2 <H_e>.
```

Because the Hamiltonian and Perron--Frobenius ground vector are real, complex
conjugation identifies the `k` response moment with the `-k` moment of the
adjoint probe. The half double commutator is therefore the stated
positive-frequency moment. Summing the edge identity gives, without a missing
factor of two,

```text
m_1 = (1-cos(k))(-E_0).
```

For one base edge, the number of q-subsets occupying exactly one endpoint is
`2 binomial(2L-2,q-1)`. Multiplication by the prism's `3L` edges and division
by `binomial(2L,q)` gives

```text
3L * 2 binomial(2L-2,q-1) / binomial(2L,q)
  = 3q(2L-q)/(2L-1).
```

The constant trial vector therefore gives the stated lower bound on the token
adjacency spectral radius. The maximum token-graph degree is at most `3q`, so

```text
3q(2L-q)/(2L-1) <= -E_0(L,q) <= 3q.
```

Under `7/48 <= q/(2L) < 13/48`, the substitutions
`q>=7L/24`, `2L-q>35L/24`, and `q<13L/24` give the deliberately loose but
valid bounds

```text
(245/384)L <= -E_0(L,q) < (13/8)L.
```

The elementary bounds
`8/L^2 <= 1-cos(2*pi/L) <= 2*pi^2/L^2` are valid for `L>=4`. Their product
with the energy bounds gives exactly

```text
245/(48L) <= m_1(L,q) < 13*pi^2/(4L).
```

Gershgorin/operator-norm control places the spectrum of `H=-A` in
`[-3q,3q]`, hence every excitation is at most `6q`. Thus
`m_1<=6qS`, and the upper density bound gives the correctly simplified weak
consequence

```text
S >= 245/(156 L^2).
```

## Independent numerical spot checks

The audit independently enumerated fixed-q occupation bases, constructed the
ordinary-prism Hamiltonian, and used the local coefficients
`f_(0,x)=exp(i*k*x)` and `f_(1,x)=exp(i*k)exp(i*k*x)`. It independently
verified the common edge difference above, evaluated
`<0|O^dagger(H-E_0)O|0>` directly, and formed the half double commutator.

| L | q | `E_0` | direct `m_1` | half double commutator | `(1-cos(2*pi/L))(-E_0)` |
|---:|---:|---:|---:|---:|---:|
| 4 | 2 | `-5.291502622129181` | `5.291502622129181` | `5.291502622129183` | `5.291502622129180` |
| 5 | 2 | `-5.493743222088744` | `3.796083203731145` | `3.796083203731143` | `3.796083203731141` |
| 6 | 3 | `-7.741361512479797` | `3.870680756239904` | `3.870680756239899` | `3.870680756239898` |

All displayed comparisons agree to at worst `6.7e-15`; the largest numerical
deviation of an edge value from `2(1-cos(k))` was `1.6e-15`. These are
independent finite-size checks, not premises of the analytic proof. They
confirm the phase convention, normalization, and absence of a missing factor
of two in the edge f-sum identity.

## Logical-gap and operator checks

For

```text
mu_L = exp(-L) delta_(exp(-L)) + delta_(20/L),
```

the audit obtains exactly

```text
S    = 1+exp(-L),
m_1  = 20/L+exp(-2L),
w_*  = exp(-L),
M_-2 = exp(L)+L^2/400.
```

For `L>=4` its support is uniformly bounded, so it is a valid counterexample
to deriving the desired residue and inverse-moment estimates from positivity,
an `O(1/L)` f-sum, bounded support, and a low pole alone.

The token adjacency Hamiltonian and the symmetric-exclusion generator are
also correctly distinguished:

```text
L_excl = D_conf-A,
H      = -A = L_excl-D_conf,
D_conf(X) = 3q-2e_G(X).
```

`D_conf` is nonconstant in the density band, so an exclusion-Laplacian gap
theorem cannot be imported as an adjacency-Hamiltonian response theorem.

The proposed sufficient response-sector lower bound gives
`S <= (L/c)m_1 <= 13*pi^2/(4c)` and then
`M_-2 <= (L^2/c^2)S <= 13*pi^2 L^2/(4c^3)`. A separate nonvanishing acoustic
projector weight is still required. Conversely, a residue bound alone does not
exclude a weaker lower pole. The theorem note correctly identifies both
obligations and correctly requires a residual-independent exact pole or
projector definition before an all-L statement.

## Primary-source scope

None of the following papers is used to prove the finite operator identity or
its bounds. The cited primary papers support only the limited comparison and
scope descriptions used in the note:

- [Caputo--Liggett--Richthammer](https://arxiv.org/abs/0906.1238) proves the
  interchange/random-walk spectral-gap conjecture, a Markov-generator result.
- [Dalfó et al.](https://arxiv.org/abs/2012.00808) studies token-graph
  Laplacian spectra and spectral inclusions.
- [Reyes--Dalfó--Fiol](https://arxiv.org/abs/2310.16929) studies adjacency and
  Laplacian spectra and spectral radii, not the required fixed-density,
  momentum-resolved pole-weight and inverse-moment bound.
- [Mastropietro](https://arxiv.org/abs/cond-mat/0502415) treats the
  one-dimensional Hubbard model at small repulsive coupling away from half
  filling.
- [Benfatto--Falco--Mastropietro I](https://arxiv.org/abs/1303.3681) and
  [II](https://arxiv.org/abs/1303.3684) establish response and Luttinger-liquid
  results for specified one-dimensional fermion models, not this
  strong-coupling hard-core-boson ladder.
- [Crépin et al.](https://arxiv.org/abs/1103.5988) studies the same clean
  two-leg hard-core-boson ladder using field theory, RG, QMC, and DMRG; it is
  the appropriate physical phase source but not an unconditional
  repository-internal proof.

## Disposition and claim ceiling

`PASS` at theorem SHA-256
`5734cda284e85ae0b51ff60b85664f470a407c95daf91b47835963539398e2f8`:
the exact all-band statement `m_1=Theta(1/L)`, its Fourier convention, and its
constants are correct and locally self-contained. The note also correctly
leaves `S=Theta(1)`, uniform acoustic residue, `M_-2=O(L^2)`, and unconditional
internal registered `z=1` open. It does not import machinery from another
surface or promote the f-sum theorem into a Stage-6, continuum, emergence, or
gravity classification.
