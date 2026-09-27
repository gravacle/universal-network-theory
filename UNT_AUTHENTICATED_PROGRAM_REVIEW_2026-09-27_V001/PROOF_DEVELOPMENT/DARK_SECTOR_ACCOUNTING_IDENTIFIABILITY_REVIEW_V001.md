# Dark-sector energy accounting: an identifiability proposition

Date: 2026-09-27. Status: independent mathematical review and constructive
proof target. This note derives consequences of explicitly supplied effective-
fluid assumptions; it does not claim that UNT currently derives those assumptions,
dark matter, dark energy, a physical component split, or observational values.
No empirical data, parameter fitting, or numerical physics was used.

## Assumptions and exact identity

Work in units c=1 on a homogeneous FRW interval. Let a(t)>0 be differentiable,
H=dot(a)/a nonzero, and V(t)=V0 a(t)^3 with fixed V0>0 a comoving-cell volume
normalization. For each component take N_i(t)>0 and epsilon_i(t)>0, with
physical energy E_i=epsilon_i N_i and physical energy density rho_i=E_i/V.
Thus N_i denotes an inventory in the comoving cell, not a density; changing
that interpretation changes the accounting formula. Define p_i=w_i rho_i.

Fix the exchange sign convention by

```text
dot(rho_i) + 3 H (rho_i + p_i) = Q_i.
```

Positive Q_i supplies energy to component i per physical volume per unit time.
If these components exhaust a conserved total stress tensor, sum_i Q_i=0.
The background identity below needs this continuity equation, not the separate
Einstein field equations. Assuming GR does not independently derive E_i=epsilon_i N_i.

Differentiating rho_i gives

```text
dot(rho_i)/rho_i = dot(E_i)/E_i - 3 H.
```

Substitution into continuity yields exactly

```text
w_i = Q_i/(3 H rho_i) - (1/3) d ln(epsilon_i N_i)/d ln a.
```

The proposed formula therefore has the correct sign and factor. The logarithmic
derivative means H^(-1) d/dt along the specified trajectory. For H=0 one must
use the undivided identity `rho_i dot(ln E_i)+3H p_i=Q_i`; the formula is not
defined at a turnaround. Components of zero density also require separate
treatment rather than division by zero.

Equivalently, the comoving first-law statement is

```text
dot(E_i) = -p_i dot(V) + Q_i V,
p_i = -dE_i/dV + Q_i/(3H),
```

where dE_i/dV is along the evolving background, not an independently derived
microscopic equation of state. Inferring pressure from that path derivative
after assuming continuity is an accounting identity until the energy, exchange,
and physical volume laws are fixed independently.

## Proposition: counts alone do not identify the background pressure

Let a range over any positive interval, and let a prescribed count history
N_i(a)>0 be continuously differentiable. For any continuous target function
w_i(a) and normalization C_i>0, choose

```text
Q_i(a) = 0,
E_i(a) = C_i exp[-3 integral_(a*)^a w_i(u) d ln u],
epsilon_i(a) = E_i(a)/N_i(a),
rho_i(a) = E_i(a)/(V0 a^3).
```

These positive quantities satisfy the component continuity equation exactly
with that w_i(a). Proof: logarithmic differentiation gives
`d ln E_i/d ln a=-3w_i`, which inserted above gives Q_i=0. QED.

Thus an arbitrary specified count history admits different pressure histories
unless an independent rule fixes energy per counted item. Component density
ratios are also undetermined because the positive C_i remain free.

This is a mathematical nonidentifiability result, not a claim that every chosen
w_i has a healthy microscopic realization. The conclusion already holds for
the ordinary formal examples w=0 and w=-1: the same N(a) can accompany
epsilon=C/N or epsilon=C a^3/N, respectively, after absorbing reference-scale
constants into C. The first gives rho proportional to a^(-3), and the second
constant rho.

For a finite set of such positive components, a flat expanding GR background
with no additional cosmological constant can also be constructed locally:
define H(a)^2=(8 pi G/3) sum_i rho_i(a), G>0, and integrate
`dt/da=1/(aH(a))`. The continuity equations then imply the compatible
acceleration equation. Different choices generally produce different expansion
histories. This establishes background consistency of the counterconstruction;
it supplies no microscopic stress law, perturbation stability, or empirical fit.

## Even fixed per-item energy needs an exchange law

With epsilon constant and Q=0, count scaling N proportional to a^s gives
w=-s/3. In particular fixed inventory gives w=0, and growth proportional to
physical volume gives w=-1. These are consequences of the entire assumed
accounting package, not properties of the words active or maintenance.

If N grows as a^3 with fixed epsilon but receives Q=3Hrho, exactly the same
constant density instead has p=0, w=0. Its energy increase is supplied by
exchange, not negative-pressure work. A conserved total requires a compensating
negative Q in another component. Counting newly supplied energy both inside
dot(N) and as unexplained negative pressure would misidentify the mechanism.

More generally, continuity determines only

```text
w_eff = w - Q/(3Hrho) = -(1/3)d ln E/d ln a.
```

Separating intrinsic pressure from exchange requires further physical structure.
A component called dark energy needs an earned stress interpretation; a
component with a constant background density is not by that fact a cosmological
constant. Likewise, w near zero alone does not establish dark-matter-like
clustering or observational viability.

## Constructive proof program

The useful next theorem is a same-parent energy/stress closure, followed by a
perturbation closure. It should earn the following linked objects:

1. **Inventory and energy map.** Define active/maintenance classes by physical
   projectors, histories, or operations independently of desired cosmological
   behavior. Derive the energy carried by each class and its normalization from
   the same Hamiltonian/action. Operation counts or maintenance costs are not
   automatically stored gravitating energy. Include interaction, controller,
   bath, and boundary energy once; identify when E_i=epsilon_i N_i is valid and
   when correlation terms prevent it.
2. **Physical work and pressure.** Establish what physical deformation changes
   the volume and derive its conjugate stress or work response. A controlled
   finite precursor could determine energy and work under independently
   calibrated strain, including all support and boundary terms. In a covariant
   completion use the common physical metric and complete stress variation;
   do not insert a metric or pressure law solely to obtain a desired w.
3. **Exchange and conservation.** Derive energy currents and creation/removal
   terms, identify Q_i with a fixed sign convention, and prove total conservation.
   This determines whether an increasing inventory receives imported energy,
   performs negative-pressure work, or changes energy per item. Freeze the
   component split before comparison; a mere relabeling must not create a new
   total stress prediction.
4. **Background consequence.** Only after the first three steps, derive N_i(a),
   epsilon_i(a), and Q_i(a), then apply the exact identity to obtain w_i(a).
   A dark-sector ratio requires the same independently earned normalizations;
   it cannot be inferred from a count ratio alone.
5. **Perturbations and discrimination.** Derive the response to inhomogeneous
   density/velocity disturbances: rest-frame pressure response, nonadiabatic
   terms, anisotropic stress, and perturbations of energy/momentum exchange.
   These laws control clustering and stability. A background w(a) supplies
   none of them by itself; dot(p)/dot(rho) is not generally the rest-frame
   propagation speed and may be undefined for constant density.

A useful first finite target is a closed energy-and-work ledger for one frozen
active/maintenance rule under controlled volume/strain and exchange operations,
including a proof that the classifications and energy map are independent of
the desired equation of state. Success would produce model-derived pressure
and exchange quantities that can enter a later FRW bridge. A negative result
would identify whether the count split fails to carry additive energy or a
distinct physical stress. Either result would sharpen the theory beyond a
purely named bookkeeping split.

The proposition above supplies a concrete theorem about what extra structure
is logically necessary for a prediction. The next positive result must derive
that structure; selecting epsilon, Q, or pressure to reproduce a desired w
would merely instantiate the demonstrated nonidentifiability.

## Independent review of the construction laboratory

Reviewed companion: `DARK_SECTOR_CONSTRUCTION_LAB_V001.md`, final SHA-256
`6a17bd76328d2e586b4e11ff5e069f633a847e14208ac0c40d6786c57488f736`.
Verdict: **PASS at conditional construction/accounting scope after repair**.
This is project-internal independent analytic review, not external peer review
or validation of an actual UNT microscopic law or cosmological phenomenon.

The review checked the signs and units of A0.3, pressure/exchange transformation
A0.5, finite-donor depletion A0.6, abundance-ratio equation A0.8, and the complete
four-component work balance A0.10–A0.12. The nonnegative-pressure construction
cannot accelerate under its explicit Einstein-FRW assumptions (A0.13). The
linear two-rate population law (A0.14) has the claimed formal fixed ratio and
finite-time initial-data dependence. The ratio is freely placed by the rates;
the formal asymptotic limit is not earned beyond the finite donor's lifetime.

The material review correction concerned finite stochastic resources. An
accepted maintenance event has intensity `nu n_M 1(E_D>=e_kick)` and transfers
equal energy out of the donor and into the bath. Thus the exact mean power
contains the donor-acceptance indicator inside the expectation. It cannot in
general be replaced by an unconditioned mean maintained count. The revised
laboratory retains this indicator and explicitly separates its stipulated
deterministic fluid equations from an unproved stochastic moment closure.
It also makes `N_star>0` explicit and identifies alpha/beta as transition rates,
unrelated to the electromagnetic fine-structure constant.

The companion `verify_dark_sector_construction_toy.py` has SHA-256
`7a12aef7a57e48cc7979eb61cca305ea6b46d572d226b1dd20b58414b323f667`.
An independent local run using

```sh
python3 -B UNT_AUTHENTICATED_PROGRAM_REVIEW_2026-09-27_V001/PROOF_DEVELOPMENT/verify_dark_sector_construction_toy.py
```

completed with exit 0 and **33 exact rational checks PASS**; measured in-process
wall time was 0.000289375 seconds, excluding interpreter startup. These checks
exercise explicit toy identities and counterexamples; they do not prove a
microscopic realization, stochastic closure, perturbation law, or dark-sector
prediction. The analytical propositions carry the general quantifiers; the
finite examples check implementation and exhibit specific failed inferences.

The constructive value of the laboratory is to expose a precise alternative
target: a native record generator and independently earned energy, stress, and
exchange law must restrict the freely adjustable constitutive and abundance
parameters. The paid-through maintenance toy does not meet that target, but
its failure is analytically informative and does not require fitting data.
