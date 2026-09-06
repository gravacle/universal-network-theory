# Frozen record-first hydrodynamic criticality pre-screen

## Scope and stop boundary

This packet searches for a finite-size **candidate** carrier-density interval
on the already audited degree-three two-rail prism.  It neither assumes nor
defines a continuum, physical metric, equilibrium ensemble, grid, Ward law,
graviton, gravity, or macroscopic phase.

The calculation has two gates:

1. an exact-through-L8 sector spectral seed screen, followed only on a seed by
   sparse L10/L12 confirmation; and
2. only on a confirmed interval, three automatically authorized response
   tracks: predictive macroscopic closure, long-wave mode universality, and
   two-cluster connected response.

If the first gate returns `NO_CANDIDATE` or `UNRESOLVED`, the three response
tracks do not run.  If it returns `CANDIDATE_INTERVAL`, they run without a
routine approval pause.  Every promotion requires an implementation frozen
independently of the target result.

## Frozen parent and exact density bookkeeping

For even `L` in `(4,6,8,10,12)`, use the previously audited connected prism
with sites `(a,i)`, `a in {0,1}`, `i in Z/LZ`, rail owners
`(a,i)--(a,i+1)`, and shifted connector owners
`(0,i)--(1,i+1)`.  Every edge is owned once.  The source-off carrier parent is

```text
H_L = - sum_(e in E_L) T_e,
Q   = sum_v n_v,
[H_L,Q] = 0.
```

`H_L` is independent of accumulated-write count.  No object may be called an
`H(N)` spectrum.  In the exact carrier-number sector `q`, define

```text
rho_q = q/(2L),      dim H_(L,q) = binomial(2L,q).
```

For `N` distinct authenticated `pi/4` writes, each with `W_R=1/2`, the
source-prepared state has

```text
p(q|N)    = 2^(-N) binomial(N,q),
mean rho  = N/(4L),
var(rho)  = N/(16 L^2).
```

Thus write count, mean carrier density, and sharp sector density remain
separate records.  Sector projection below is an adopted analytical
diagnostic and is not an authenticated post-selected accumulation history.
The exact common mean-density grid supplied by the fixed authenticated writes
across all five sizes is `{0,1/8,1/4,3/8,1/2}`.  A later equal-density
`L4+L4 -> L8` history must obey `N8=2*N4`; an off-grid candidate is bracketed,
not reached by changing the authenticated write angle.

## Structural anti-false-positive screen

Before any density result, verify independently:

1. topology, degree, owner-once edge census, and `[H_L,Q]=0`;
2. particle-hole sector equivalence `q <-> 2L-q`;
3. the exact one-carrier bands

   ```text
   epsilon_(m,+/-) = -2 cos(2 pi m/L) +/- 1;
   ```

4. their independence from `N`; and
5. bipartite/chiral `E <-> -E` symmetry of each configuration graph.

Zero energy, energy multiplicity, or the smallest generic many-body level
spacing is forbidden as a criticality diagnostic.  In particular, exact
one-carrier zeros at `L=6,12` are commensurability, and configuration-sublattice
imbalance forces many exact mid-spectrum zeros in even-`q` sectors.  These are
controls, not candidate roots.

## Response-active sector spectrum

For `0 < q <= L`, let `E_(L,q,0)` and `|0>` be the unique
Perron--Frobenius ground energy and state of `H_(L,q)`.  Put
`k_L=2*pi/L` and define the total-rail carrier-density mode

```text
n_k = sum_i exp(i k_L i) [n_(0,i)+n_(1,i)].
```

Group degenerate excited eigenvectors by their basis-independent spectral
projector `Pi_a`.  For every distinct positive excitation energy
`omega_a=E_a-E_0`, retain

```text
w_a = || Pi_a n_k |0> ||^2.
```

The numerical response-active gap, response-timescale moment, and lowest-pole
residue are

```text
Delta_act(L,q) = min { omega_a>0 : w_a > w_floor },
chi_tau(L,q)   = sqrt[ sum_a w_a/omega_a^2 / sum_a w_a ],
R_low(L,q)     = w_(Delta_act) / sum_a w_a.
```

`chi_tau` is a finite spectral response-timescale statistic.  It is not a
thermodynamic/Kubo susceptibility and cannot diverge at finite `L`.
Separately report the ground-energy charge curvature

```text
Delta_Q(L,q) = E_0(q+1)+E_0(q-1)-2E_0(q)
```

only as an adopted sector-energy diagnostic, not a compressibility.

For L4/L6/L8, diagonalize complete fixed-`q` sectors sequentially and retain
complete eigenvalue spectra; eigenvectors sufficient for every declared
weight are retained one sector at a time.  Group energies at absolute
tolerance `1e-10`.  Set

```text
w_floor = max(1e-12 * sum_a w_a,
              100 * eigen_residual_max^2 * ||n_k|0>||^2).
```

Every promoted active pole must have eigenpair residual at most `1e-10` and
remain active under thresholds `w_floor/10`, `w_floor`, and `10*w_floor`.
Otherwise that row is `UNRESOLVED`.

L10/L12 may use a real-symmetric matrix-free or sparse restarted Lanczos
method, expanding the requested Ritz space `16 -> 32 -> 64 -> 128` until the
first active pole and its residue are stable.  Target residual and independent
solver disagreement must both be at most `1e-9`; otherwise the candidate is
`UNRESOLVED`.  Dense conversion or shift-invert at L10/L12 is forbidden.

## Seed and confirmed candidate rules

Associate sector `q` with its finite density-resolution cell

```text
I_(L,q) = [(q-1/2)/(2L), (q+1/2)/(2L)] intersect [0,1/2].
```

A sector is a seed only if:

1. `Delta_act` is a strict local density minimum beyond its numerical error;
2. `chi_tau` is a coincident strict local maximum;
3. `R_low >= 1e-6` and remains above that floor under the threshold screen;
4. the same `m=1`, total-rail density mode is used; and
5. neither an energy degeneracy nor a threshold/mode-identity switch creates
   the extremum.

An L<=8 seed interval exists only if one connected component of the
intersection of seed-cell unions for `L=4,6,8` is nonempty and, on an
overlapping triplet, `Delta_act` decreases while `chi_tau` increases with L.
No seed gives `NO_CANDIDATE_L4_L8` and stops all larger work.

On a seed, run only L10/L12 sectors whose cells intersect that seed.  A
confirmed finite-size candidate interval is

```text
I_c = intersection_(L in {8,10,12}) union_(admissible q) I_(L,q).
```

It must be one connected nonempty interval with the same tracked mode,
nonvanishing residue, decreasing gap, and increasing `chi_tau`.  Fit the five
size rows to the predeclared gapless family `a L^(-z)`, with
`a>0`, `1/4<=z<=4`, and to the positive-gap family
`Delta_inf+a L^(-z)`, with `Delta_inf>0` and the same bounds.  Use
leave-one-size-out prediction.  `CANDIDATE_INTERVAL` requires the gapless
family to have smaller total held-out squared relative error.  Otherwise the
result is `NO_CANDIDATE`, or `UNRESOLVED` if numerical/error or competing-cell
ambiguity controls the decision.

This is a candidate-selection rule, not proof that `Delta=0` or that
`chi_tau` diverges.

## Automatically authorized follow-up on a candidate

Freeze `I_c`, all bracketing authenticated mean-density rows, histories,
windows, solvers, and error thresholds before evaluating any follow-up.

### A. Spatial response

For a localized authenticated probe, retain the complete differential
occupation/current history against both a maximally distributed and compact
conditional background placement at the same authenticated mean density.
Use graph edge shells

```text
r(e;s) = min[d(s,u),d(s,v)] for e=(u,v).
```

Report signed shell current, shell L1, per-edge mean absolute current, RMS
current, and graph second-moment length.  Compare `A exp(-r/xi)` against
`A r^(-p)` only on expanding bulk windows `2<=r<L/2`, using leave-one-size-out
prediction and solver-error weights.  An algebraic candidate requires better
held-out prediction at every eligible larger size, stable `p`, and fitted
`1/xi_L` trending toward zero.  Pattern disagreement is a conditioned
crossover, not density-only criticality.

### B. Predictive macroscopic closure

One-time values of `tau_bulk` and `J_eff` are forbidden as a closure test.
Let authenticated pasts `p` span the frozen equal-density block preparations,
and futures `f` span joined probe/read continuations sufficient to reproduce
the complete target-occupation and connector-current time traces.  Form the
past/future pairing

```text
K_(p,f) = Tr(rho_p F_f).
```

`D_macro=rank(K)` is the minimum exact linear predictive-record dimension
modulo the annihilator of every frozen future macro read.  Report exact or
certified interval rank and, separately, empirical `D_macro(epsilon)` at a
frozen tolerance.  Held-out past/future compositions must be predicted; a
rank computed from the training histories alone does not close.

### C. Mode universality

Use translation modes `k_m=2*pi*m/L` and both rail-band/internal
polarizations with equal envelope, norm, source weight, and target-amplitude
floor.  Track the same response peak or transfer-function branch.  Report

```text
f_(sigma,m,L) = [tau_loaded(sigma,m,L)-tau_0(sigma,m,L)]/tau_0(sigma,m,L).
```

A finite universality candidate requires the spread across authenticated
internal modes to decrease with L at fixed small `m` (`k -> 0`).  Within-band
and cross-band conclusions remain separate.  Exact equality at finite L is
not required or called an equivalence principle.

### D. Two-cluster connected response

For every frozen cluster separation/orbit, compute four complete probe
response histories and

```text
C_AB O = O_AB - O_A - O_B + O_0.
```

Retain the complete connected current field, connected latency, and

```text
eta_J = ||C_AB J||_1 / (||delta_A J||_1+||delta_B J||_1).
```

For probes at multiple vertices, report the graph latency field
`phi_C(v)=tau_C(v)-tau_0(v)` and oriented graph gradient
`g_C(u->v)=phi_C(v)-phi_C(u)`.  Zero connected response means additive
routing; nonzero means nonlinear routing, not attraction.  Exponential and
power fits, including an external `1/r` comparator, remain graph-response
classifications.  The sealed conserved interaction energy is contact-only;
no operational long-range latency response may be relabeled a conserved
potential.

## Resource and claim guards

- Run at most one L10/L12 spectral job at a time.
- L8: abort above 12 GiB RSS or 45 minutes for any sector.
- L10: abort above 8 GiB RSS, 2,000 matvecs, or three aggregate hours.
- L12: abort above 16 GiB RSS, 2,000 matvecs, or ten aggregate hours.
- Keep at most 128 real Krylov vectors (or the equivalent complex-memory
  bound), release each sector before the next, and preserve raw telemetry.
- Record raw norm, number, energy, eigen-residual, and owner-once ledger
  controls.  Numerical remainders are not called defects before ownership
  classification.
- No result above L8 is authorized without an L<=8 seed.
- No result is promoted without an independent hostile implementation frozen
  before target inspection.

**Proved inputs:** finite topology/owner census, `[H,Q]=0`, authenticated
single-write ledger, binomial sector weights, and the structural spectrum and
symmetry identities when reconstructed exactly.

**Adopted:** sector projection as an analytical diagnostic, the total-rail
`m=1` response channel, density cells, extrema/fit rules, placement controls,
and predictive-record observable family.

**Conditional:** support, source placement, phase, clock, finite solver,
readout, and all later composition histories.

**Empirical:** every finite spectrum, active pole/residue, response time,
spatial profile, fitted interval/exponent, predictive rank, mode comparison,
and two-cluster field unless separately exact-certified.

**Open:** existence or uniqueness of `rho_c`, any thermodynamic or continuum
limit, autonomous placement/state selection, physical distance/dimension,
macroscopic closure, universal coupling, noncontact energy, attraction,
Ward behavior, graviton, emergence, and gravity.
