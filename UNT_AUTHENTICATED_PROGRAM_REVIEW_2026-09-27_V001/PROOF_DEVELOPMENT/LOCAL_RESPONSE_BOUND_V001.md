# A local witness route to size-uniform response at a fixed short time

Status: newly derived finite-dimensional mathematical lemma; independent
project-internal analytic review passed at the stated conditional scope.
This is not external peer review or an assertion that the UNT family satisfies
its hypotheses. No claim of mathematical novelty or physical discovery is made.

## Exact finite statement

Let `rho` and `sigma` be density operators on a finite-dimensional joint
space `H_S tensor H_C`, with the same reduced carrier state. Write
`Delta=rho-sigma`, so `Tr_S Delta=0`. Fix a self-adjoint Hamiltonian `H`,
`U(t)=exp(-itH)`, and a self-adjoint carrier observable `O` with spectral
diameter `w=lambda_max(O)-lambda_min(O)>0`. Define

```text
Otilde = I_S tensor O,
d(t) = Tr[Otilde U(t) Delta U(t)^dagger],
a = i Tr([H,Otilde] Delta),
b = ||[H,[H,Otilde]]||_infinity,
M = ||Delta||_1 <= 2,
D_C(t) = (1/2) ||Tr_S[U(t) Delta U(t)^dagger]||_1.
```

Then, for every real t,

```text
|d(t) - t a| <= (t^2/2) b M,
D_C(t) >= max(0, |t| |a| - (t^2/2) b M) / w.
```

The scalar `a` is real. A subsequent common carrier unitary preserves
`D_C(t)`; its observable witness is transported by the corresponding unitary
conjugation. A subsequent general noisy carrier channel only gives a
contractivity upper bound and must not be assumed to preserve this lower bound.

## Proof

In the Heisenberg picture,
`d(t)=Tr[U(t)^dagger Otilde U(t) Delta]`. The equal initial carrier marginals
give `d(0)=0`. Differentiating yields

```text
d'(0) = i Tr([H,Otilde] Delta) = a,
d''(s) = -Tr[U(s)^dagger [H,[H,Otilde]] U(s) Delta].
```

The trace norm/operator norm inequality and unitary invariance imply
`|d''(s)|<=b M` for every s. Taylor's integral remainder gives
`|d(t)-ta|<=t^2 b M/2`, also for negative t. Thus
`|d(t)|>=|t||a|-t^2 b M/2` whenever the right side is positive.

Let `X=Tr_S[U(t) Delta U(t)^dagger]`. It is Hermitian and has trace zero.
Subtracting the midpoint of O's spectral interval does not change `Tr(OX)`
and leaves operator norm `w/2`. Hence
`|d(t)|<= (w/2)||X||_1 = w D_C(t)`. This proves the bound. Reality follows
because `i[H,Otilde]` and Delta are Hermitian. Common output-unitary
invariance is the unitary invariance of the trace norm. QED.

## Conditional uniform-family corollary

For a specified family indexed by L, suppose independently proved constants
`a0>0`, `B>0`, `W>0` satisfy

```text
|a_L| >= a0,        b_L ||Delta_L||_1 <= B,
0 < spectral_diameter(O_L) <= W
```

for every admissible `L>=L0`. Then any fixed
`0<|t|<=a0/B` gives

```text
D_C,L(t) >= |t| a0/(2 W) > 0
```

uniformly in L. This is size-uniform response at one fixed short time, not
persistence for long times. If the second derivative is identically zero
for all real times (in particular if `b_L ||Delta_L||_1=0`), then `d_L(t)=t a_L`
is globally bounded in this finite-dimensional unitary setting, so `a_L=0`.
That degenerate case cannot satisfy `a0>0`; no division by zero is used.
This corollary is conditional: the difficult scientific/model work
is proving the uniform correlation pairing and remainder control, not
substituting assumed constants into the inequality.

## Why this may help, and where it does not apply yet

The double commutator is a more focused target than the coarse extensive
bound `4||H||^2||O||`. In a concrete local model one can inspect which
Hamiltonian terms actually enter its support. Locality, bounded degree, and
uniform coupling bounds must be established for that model, not presumed
from the word "network." A global trace norm `M<=2` is already uniform, but
does not make `a_L` nonzero or `b_L` bounded.

The present UNT result uses a frozen discrete admission/revisit followed by
carrier transport, and a sector-dephased joint/product comparison. Applying
this continuous-time lemma requires an explicitly justified Hamiltonian
interpolation on a common finite space and the actual correlated initial
states. It supplies no conclusion about a different interpolation, fixed
finite-time angle outside its bound, an all-event response, the thermodynamic
limit, or gravity. If symmetric sectors are used, first embed the direct sum
in the stated joint space and verify the reduced-state and generator
identifications. Those are open application obligations, not hidden steps
in the proof.

An observed nonzero L4 response need not have a nonzero first derivative at
the chosen interpolation origin: a higher-order term may be responsible.
Failure of the `a0` criterion would therefore defeat this sufficient route,
not prove that every response or persistence route is impossible.
