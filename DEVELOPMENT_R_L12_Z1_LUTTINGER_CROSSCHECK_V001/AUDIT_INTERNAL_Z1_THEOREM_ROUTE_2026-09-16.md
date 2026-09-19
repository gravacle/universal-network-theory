# Independent audit of the repository-internal z=1 theorem route

Date: 2026-09-16

Verdict: `PASS`

## 1. Audited object and scope

This audit reviewed:

```text
INTERNAL_Z1_THEOREM_ROUTE.md
SHA-256 e85af161082335559a9cc29c4b06090e13f2e403ca69932500bcfd1658b68b2b
```

The review was deliberately restricted to:

1. the periodic two-leg hard-core-boson Hamiltonian in the packet;
2. its occupation-basis representation as minus the prism token-graph
   adjacency matrix;
3. translation and rail-exchange symmetry;
4. the native Fourier-density probe at `k_L=2*pi/L`; and
5. direct Perron--Frobenius, double-commutator, spectral-measure, and
   variational calculations.

No earlier gate, adjudicator, fit rule, disposition label, URM or gravity
criterion, alpha argument, or result for a different Hamiltonian was accepted
as a premise. The separately documented same-model Luttinger-liquid premise
was also excluded from the internal proof.

## 2. Finite-volume visibility check

For even `L>=4` and `0<q<2L`, the token graph of a connected prism is
connected. Its adjacency matrix is irreducible and nonnegative, so the ground
state of its negative has a unique representative with strictly positive real
occupation-basis coefficients. Because translation and rail exchange are
permutation symmetries, uniqueness and positivity make the ground state even
under both.

On the density interval

```text
I=[7/48,13/48),
rho=q/(2L),
```

one has `0<q<L`. A configuration with `q` consecutive occupied sites on one
rail has

```text
|n_s(k_L)| = |sin(pi*q/L)/sin(pi/L)| > 0.
```

Since the ground-state coefficient of that configuration is nonzero, the norm
of `n_s(k_L)|0>` is strictly positive. This vector has nonzero translation
momentum and is therefore orthogonal to the unique zero-momentum ground state.
Moreover,

```text
O_+(k_L)=[(1+exp(i*k_L))/2]n_s(k_L)
```

has a nonzero coefficient for `L>=4`. The claimed strictly positive
positive-frequency support of the rail-even probe is therefore correct. The
note also correctly refrains from turning this strict finite-volume statement
into a uniform residue bound.

## 3. Fourier phase, parity, and first moment

The decomposition

```text
O_L = [(1+exp(i*k))/2] n_s + [(1-exp(i*k))/2] n_a
```

is exact for the packet's native probe. The two terms have opposite rail
parity. Because the ground state is rail-even and the Hamiltonian preserves
rail parity, their spectral measures occupy orthogonal parity sectors and add
without an interference term. The even first moment is consequently bounded
above by the total first moment.

The imported result from `EXACT_RESPONSE_SUMRULE_BOUND.md` is itself a direct
calculation for this same Hamiltonian and probe. Its uniform bound

```text
245/(48L) <= m_1(L,q) < 13*pi^2/(4L)
```

has the correct normalization and factor of two. Only the upper bound is
passed to the even channel; the note explicitly refuses to pass the total
lower bound to that channel. No phase, normalization, or parity error was
found.

## 4. LSM variational calculation

For

```text
U=exp[(2*pi*i/L) sum_x x N_x],
```

rung hopping is unchanged and each periodic leg hopping receives the same
twist modulo `2*pi`. The unique positive ground state is real, so the current
term has zero expectation. Thus

```text
<0|U^dagger H U|0>-E_0
  =(1-cos(2*pi/L))(-E_leg).
```

The leg-adjacency row degree is at most `2q`, hence
`-E_leg<=2q<2L` on the stated density interval. Together with
`1-cos(2*pi/L)<=2*pi^2/L^2`, this gives the displayed `4*pi^2/L` upper bound.

Under one-site translation the twist state acquires momentum
`+/- 2*pi*q/L`, depending on convention. Since `0<q<L`, it is orthogonal to
the ground state. The variational principle in that momentum sector therefore
does imply an exact excitation with energy at most `O(1/L)`.

The note correctly identifies the obstruction: this momentum is generally
not the native probe momentum `2*pi/L`. The LSM state does not establish a
probe-visible acoustic pole and cannot close the z=1 proof.

## 5. Sufficient response theorem

Let `mu_+` be the positive-frequency spectral measure of `O_+` and
`S_+=mu_+((0,infinity))`. At nonzero momentum, uniqueness of the ground state
makes this equal to `||O_+|0>||^2`.

Assume the proposed all-size bounds

```text
S_+ >= s_0,
supp(mu_+) subset [c/L,infinity),
m_(1,+) <= C_1/L.
```

With `C_2=2*C_1/s_0`, Markov's inequality gives

```text
mu_+((C_2/L,infinity)) <= s_0/2.
```

Therefore at least `s_0/2` weight lies in `[c/L,C_2/L]`. This is a correct
sufficient route to a uniformly visible response exponent `z=1`. The note
correctly limits that conclusion to the probe-visible channel rather than all
possible system excitations.

For the alternative exact first-support definition, the proposed pair

```text
w_* >= w_0,
M_-2=sum_j w_j/omega_j^2 <= C*L^2
```

also yields the claimed two-sided bound. Indeed,

```text
M_-2 >= w_*/Delta_*^2
```

gives `Delta_*>=sqrt(w_0/C)/L`, while

```text
m_1 >= w_* Delta_*,
m_1 < 13*pi^2/(4L)
```

gives `Delta_*<[13*pi^2/(4w_0)]/L`. The note correctly calls this a different
sufficient pair, not a logically equivalent restatement of the window-mass
criterion.

The sampled observations -- including nonzero pole weight, bounded sampled
`M_-2/L^2`, and bounded sampled `L*Delta_act` -- are consistent with these
premises. They are not used as an all-`L` proof.

## 6. Claim ceiling

The following three results in the audited note pass:

```text
finite symmetric-probe visibility:  PROVED
native total first moment O(1/L):   PROVED
existence of some O(1/L) LSM state: PROVED
```

The following stronger result remains open:

```text
uniform probe-visible all-L z=1 response: OPEN
```

In particular, the audit does not promote finite-size numerics, the f-sum,
Perron--Frobenius positivity, or the off-momentum LSM excitation into the
missing uniform response theorem. It also does not turn the conditional
same-model Luttinger-liquid closure into a repository-internal theorem.

Within this claim ceiling, the route is mathematically consistent and stays on
the native proof surface.
