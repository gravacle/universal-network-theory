# Repository-internal z=1 theorem route

Date: 2026-09-16

Status: `EXACT_PARTIAL_RESULTS__ONE_UNIFORM_RESPONSE_THEOREM_MISSING`

## 1. Surface restriction

This note asks what can be proved from the following objects alone:

1. the periodic two-leg hard-core-boson Hamiltonian defined in this packet;
2. its translation and rail-exchange symmetries;
3. the native density probe at `k_L=2 pi/L`; and
4. standard linear algebra and variational identities re-derived for that
   Hamiltonian.

It imports no earlier gate, adjudicator, fit rule, disposition label, URM or
gravity criterion, alpha argument, or theorem about a different Hamiltonian.
It also does not treat the same-model Luttinger-liquid literature premise as an
internal mathematical theorem.

The purpose is to locate the exact remaining obligation, not to promote an
incomplete route into a proof.

## 2. Exact finite-volume visibility

Fix even `L>=4` and `0<q<2L`. The `q`-token graph of the connected prism graph is connected.
In the occupation basis the Hamiltonian is minus its adjacency matrix. The
Perron--Frobenius theorem therefore gives a unique ground state whose
coefficients may all be chosen strictly positive and real.

Uniqueness makes that state invariant under translation and rail exchange. Put

```text
n_s(k) = n_0(k)+n_1(k),
O_+(k) = [(1+exp(i k))/2] n_s(k).
```

For every sector in the density interval `I=[7/48,13/48)`, one has `0<q<L`.
Consider the basis configuration with `q` consecutive occupied sites on one
rail. On that configuration,

```text
|n_s(k_L)| = |sin(pi q/L)/sin(pi/L)| > 0.
```

The positive ground state assigns nonzero probability to this configuration,
so

```text
||n_s(k_L)|0>|| > 0.
```

Because `k_L` is nonzero, translation symmetry makes this vector orthogonal to
the zero-momentum ground state. Hence the rail-even part of the native probe
has strictly positive, positive-frequency spectral support at every finite
`(L,q)` in the block.

This is an exact finite-volume visibility theorem. It supplies neither a
uniform lower bound on the weight nor an energy scale for the visible support.

## 3. Exact first-moment bound

The direct double-commutator calculation in
[`EXACT_RESPONSE_SUMRULE_BOUND.md`](EXACT_RESPONSE_SUMRULE_BOUND.md) proves for
the native total-density mode that, uniformly on `I`,

```text
245/(48L) <= m_1(L,q) < 13 pi^2/(4L).
```

Rail parity splits the spectral measure into nonnegative even and odd parts.
Consequently the even part relevant to `O_+` inherits the upper bound

```text
m_(1,+)(L,q) < 13 pi^2/(4L).
```

The total lower bound does not by itself become an even-channel lower bound.
The `O(1/L)` first moment is compatible with several mutually different
spectral arrangements, including vanishing residue or weight moving to energy
scales below `1/L`. It does not prove `z=1` alone.

## 4. Exact LSM variational state, and why it does not close the proof

Define the rung-number operator `N_x=n_(0,x)+n_(1,x)` and the twist

```text
U = exp[(2 pi i/L) sum_x x N_x].
```

Rung hopping is unchanged by `U`; leg hopping acquires the uniform twist.
Since the ground state is real, the sine term has zero expectation. The
variational excitation obeys

```text
<0|U^dagger H U|0>-E_0
  = (1-cos(2 pi/L))(-E_leg)
  <= 4 pi^2/L.
```

Here `E_leg` is the ground-state expectation of the leg-hopping part of `H`.
Each token has at most two leg moves, so `-E_leg<=2q<2L`; combining this with
`1-cos(2 pi/L)<=2 pi^2/L^2` gives the displayed bound. Translation changes the
state by momentum `+/- 2 pi q/L`, with the sign set by the translation
convention. For `0<q<L` this is nontrivial, so `U|0>` is orthogonal to the
ground state. Thus an exact `O(1/L)` excitation exists throughout the block.

The obstruction is decisive: its momentum is `2 pi q/L`, whereas the native
probe has momentum `2 pi/L`. LSM therefore proves a low state but not a low
state visible to this probe. It also permits translation-breaking towers and
dispersions with `z>1`.

## 5. Why the apparent shortcuts do not transfer

- A rung-order Jordan--Wigner transformation keeps rung hopping quadratic but
  puts an order-one density string on leg hopping. The result is a
  correlated-hopping two-orbital fermion chain, not the free XX chain.
- Perron--Frobenius positivity proves strict finite weight, not a uniform
  thermodynamic residue.
- The f-sum fixes a moment, not the location or concentration of its spectral
  measure.
- Locality and Lieb--Robinson bounds do not rule out quadratic low modes.
- Exclusion-process or token-graph Laplacian theorems apply to `D-A`; the
  present Hamiltonian is `-A`, and the configuration degree `D` is not
  constant.
- Results for other weakly coupled one-dimensional fermion models are not
  results for this order-one correlated-hopping ladder.

These are mathematical obstructions, not workflow failures. Importing a result
across any of these boundaries would change the proof surface.

## 6. A sufficient missing theorem

Let `mu_(L,q,+)` be the positive-frequency spectral measure of `O_+`, and put

```text
S_+(L,q) = ||O_+|0>||^2.
```

A sufficient, fully internal uniform response theorem is the existence of
constants `s_0>0` and `c>0`, independent of `L` and of every sector with
`q/(2L) in I`, such that

```text
S_+(L,q) >= s_0,
supp(mu_(L,q,+)) subset [c/L, infinity).
```

Together with `m_(1,+)<=C_1/L`, choose `C_2=2C_1/s_0`. Markov's inequality for
the spectral measure then forces at least `s_0/2` weight into

```text
[c/L, C_2/L].
```

That would establish a uniformly visible acoustic response and hence the
probe-visible response exponent `z=1` sought here. It is not, by itself, a
claim about every possible excitation channel of the full system.

If the project instead insists on the exact first-support pole group, a
different sufficient pair tailored to that definition is to define the group
without residual-dependent thresholds and prove constants `w_0,C>0`
satisfying

```text
w_*(L,q) >= w_0,
M_(-2)(L,q) = sum_j w_j/omega_j^2 <= C L^2.
```

The exact f-sum and these two bounds would give

```text
sqrt(w_0/C)/L <= Delta_*(L,q)
Delta_*(L,q) <= [13 pi^2/(4w_0)]/L.
```

The finite data strongly support the first inequality's residue premise, but
finite observations are not substituted for its required all-`L` proof.

## 7. Current conclusion

The repository-internal route reaches three exact results:

```text
finite symmetric-probe visibility:  PROVED
native first moment O(1/L):         PROVED
existence of some O(1/L) LSM state: PROVED
probe-visible all-L z=1 response:   OPEN
```

The open line is supplied by the sufficient uniform response theorem in
section 6. Necessity or mathematical minimality is not claimed. The
conditional same-model Luttinger theorem remains the present physical closure;
it is documented separately and is not smuggled into this internal route.
