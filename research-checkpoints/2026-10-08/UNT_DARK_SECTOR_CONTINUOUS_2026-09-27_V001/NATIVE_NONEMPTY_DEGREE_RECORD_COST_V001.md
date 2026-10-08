# Native nonempty degree phases and complete record cost

2026-09-27. Analytical parameter-domain result only; no numerical run, new microscopic term, adopted parameter change, or ground-preparation claim.

## 1. Parent, regime, and energy being compared

The resident recovered_sources/BS_MICRO_ACTION.md was checked for flags and its relevant action and stability sections read: BS06, BS10–11, BS13–14. Source SHA256: 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec. Keep the native h_N = Ω/N with Ω fixed, one complete bipartite slab, no carriers, formation off, no graph-dependent ports, U = U_d > 0, λ = λ_R ≥ 0, and Δ − 2λ ≥ δ > 0. The bare record cost ε = ε_r is strictly positive. Unused spectator energies are zero; a nonzero common spectator constant would have to be retained separately.

For a fixed binary record pattern q_v, the complete graph-and-record Hamiltonian is

\[
 H=\sum_v\{f_{q_v}(d_v)+\epsilon q_v\}
      -\frac{\Omega}{N}\sum_eX_e,
 \qquad f_q(d)=U(d-d_*)^2+(\Delta/2-\lambda q)d.       \tag{1}
\]

Define m_q = min_{d ≥ 0, integer} f_q(d). The native sparse-limit proof in NATIVE_SPARSE_THERMODYNAMIC_BOUND_V001.md shows that the flip contribution changes conditional ground energy by at most O(√N), while the diagonal minimum supplies its leading energy. For uniform q it is exactly 2N(m_q + εq) before the quantum correction. For balanced binary patterns whose minimizing degree lists are feasible, NATIVE_BALANCED_RECORD_LEADING_ENERGY_V001.md gives

\[
 E_0=2Nm_0+D\mu+O(\sqrt N),\quad
 D=\sum_vq_v,\quad \mu=\epsilon+m_1-m_0.             \tag{2}
\]

Thus μ is the complete leading balanced-population excess per occupied register. It is not automatically the energy of one finite-N insertion, a dynamical chemical potential, or an inertial/gravitational mass. No energy reference is reset between record sectors.

## 2. Exact degree-transition intervals, including multiple steps

Put

\[
 x=d_*-\frac{\Delta}{4U},\qquad r=\frac{\lambda}{2U}.
\]

The q = 0 and q = 1 quadratic centers are x and x+r. Define the open nearest-integer cells

\[
 I_0=(-\infty,1/2),\qquad
 I_k=(k-1/2,k+1/2)\quad(k\ge1).                       \tag{3}
\]

For unique preferred degrees k at q = 0 and l = k+j at q = 1, the exact condition is

\[
 x\in I_k\cap(I_{k+j}-r),\qquad j\in\mathbb Z_{\ge0}.
                                                               \tag{4}
\]

Any independently declared range of d_* must also be intersected with (4). The absence of a lower endpoint for I_0 is essential: negative centers saturate at degree zero rather than creating negative degrees.

For k ≥ 1 the interval becomes

\[
 \frac{\Delta}{4U}+k-\frac12+\max(0,j-r)
 <d_*<
 \frac{\Delta}{4U}+k+\frac12+\min(0,j-r),              \tag{5}
\]

and is nonempty exactly when |j−r| < 1. Away from degree-zero saturation, an integer r produces exactly j = r; a noninteger r permits j = floor(r) or ceil(r), on the appropriate intervals. For k = 0 and j ≥ 1, the corresponding interval is

\[
 \frac{\Delta}{4U}+j-\frac12-r<d_*<
 \frac{\Delta}{4U}+\min(1/2,j+1/2-r).                 \tag{6}
\]

The k = j = 0 region is x+r < 1/2. At cell boundaries use the full minimizing sets, not a unique-degree assertion; the minimum energy remains continuous.

In the especially relevant adjacent-step regime 0 < λ ≤ 2U, (4) reduces, for every k ≥ 0, to

\[
 k+\frac12+\frac{\Delta}{4U}-\frac{\lambda}{2U}
 <d_*<k+\frac12+\frac{\Delta}{4U}.                   \tag{7}
\]

These are exact intervals for the diagonal/leading-large-N preferred degrees. A finite-N quantum ground state has fluctuating degrees; this is not a hard degree constraint or a finite-N classical-state claim.

## 3. Complete excess energy and the required storage gap

Within a unique k → k+j interval,

\[
 \mu=\epsilon+Uj(2k+j-2d_*)
           +\frac{\Delta}{2}j-\lambda(k+j).           \tag{8}
\]

For j = 0 this is exactly μ = ε−λk. For j > 0 it decreases with d_* at slope −2Uj. The necessary and sufficient leading positive-cost condition is

\[
 \epsilon>m_0-m_1
 =\lambda(k+j)-j[U(2k+j-2d_*)+\Delta/2].             \tag{9}
\]

It must be imposed jointly with (4), rather than inferred from ε > 0. Comparing each minimizer against the other's trial degree gives

\[
 -\lambda(k+j)\le m_1-m_0\le-\lambda k.             \tag{10}
\]

Both inequalities are strict when j > 0 and both minima are unique. Hence a necessary condition for μ > 0 in that case is ε > λk; ε ≥ λ(k+j) is sufficient, but not necessary. For adjacent transitions in (7), μ sweeps the entire open interval

\[
 \epsilon-\lambda(k+1)<\mu<\epsilon-\lambda k.       \tag{11}
\]

Three distinct requirements must not be conflated:

- BS13 requires a positive **bare** ε and an extensive total lower bound. It does not require ε ≥ λN.
- A positive optimized **bulk excess** is the coefficient test (9).
- A nonnegative instantaneous local insertion cost on **every possible graph state** requires ε−λd_v ≥ 0 for all 0 ≤ d_v ≤ N, namely ε ≥ λN. This stronger condition is not part of BS13 and cannot hold at all N with fixed finite ε and fixed λ > 0. It is not needed for an extensive lower bound.

The O(√N) error in (2) does not certify a single-record finite-N cost. That needs a separately specified insertion state or spectral comparison.

## 4. Prospective d_* windows at the inherited remaining coefficients

Keep U = 1, Δ = 4, λ = 1/2, ε = 1, with fixed Ω (Ω = 2 matches the existing N = 2 value h_2 = 1). Only d_* is treated as a prospective parameter, not changed in an existing mission or adopted by this note. The native extensive domain remains satisfied throughout this scan: Δ−2λ = 3 > 0 and d_* is N-independent.

For the adjacent transition k → k+1,

\[
 k+5/4<d_*<k+3/2,\qquad
 \mu=7/2+(3/2)k-2d_*,\qquad
 (1-k)/2<\mu<1-k/2.                                 \tag{12}
\]

| Unique degrees q=0 → q=1 | Open prospective d_* interval | Complete μ | Sign inside |
| --- | --- | --- | --- |
| 0 → 1 | (5/4, 3/2) | 7/2 − 2d_* | positive: (1/2, 1) |
| 1 → 2 | (9/4, 5/2) | 5 − 2d_* | positive: (0, 1/2) |
| 2 → 3 | (13/4, 7/2) | 13/2 − 2d_* | negative: (−1/2, 0) |

Thus there is an open native parameter region with nonempty preferred degrees on both record backgrounds, an increased preferred degree when occupied, and strictly positive leading record excess, without changing the inherited U, Δ, λ or ε. This establishes compatibility with the stated extensive stability domain—not dynamical stability, locality, or a viable geometric phase—and does not choose a point in that region.

The 2 → 3 window instead has negative μ in its entire interior. μ = 0 at its lower endpoint is a degree tie. A further useful distinction is that for 5/2 < d_* < 13/4 both backgrounds uniquely prefer degree two, so μ = ε−2λ = 0 throughout that interval. At its endpoints the degrees can tie, while μ remains zero. The inherited current value d_* = 1 lies in neither nonempty window; both preferred degrees there are zero.

Negative μ does not mean unbounded energy or uncontrolled growth of degree. All record occupations are binary, the native edge margin stays positive, the penalty controls degrees, and H ≥ δM + εD − ΩN in this sector. It means that the optimized graph-plus-feedback contribution lowers energy enough to overcome the bare storage difference relative to the compared blank-record ground sector. That blank sector is then not the lower-energy reference among those conditional ground sectors.

## 5. What this energy law can—and cannot—select

The leading balanced-population law (2) is affine in D. It does not by itself select an interior occupation fraction. There is an exact stronger conditional statement if one additionally asks for the absolute ground state across all record sectors, instead of keeping the actually prepared q distribution.

Let m_* = min(m_0, ε+m_1). For μ > 0 define Q_unfav = D; for μ < 0 define Q_unfav = 2N−D. The diagonal operator, for arbitrary binary patterns and not just balanced ones, satisfies

\[
 H_{\rm diag}\ge2Nm_*+|\mu|Q_{\rm unfav}.            \tag{13}
\]

A uniform favorable record pattern with a minimizing regular graph attains 2Nm_* once N is at least its fixed preferred degree. The same empty-trial/native-margin argument as before bounds ground incidence by CN, where C = (2Ud_*²+Ω)/δ. Applying the all-state flip bound |⟨V_N⟩| ≤ 2Ω√⟨M⟩ then yields

\[
 \frac{\langle Q_{\rm unfav}\rangle_0}{2N}
 \le\frac{\Omega\sqrt C}{|\mu|\sqrt N}.              \tag{14}
\]

Accordingly, **under this additional global-ground-selection comparison**, the occupied fraction tends to zero for positive μ and to one for negative μ. At μ = 0 the leading energy does not choose the fraction; subleading quantum terms, constraints, entropy or specified nonequilibrium history would need their own analysis. This is not a claimed abundance law, dynamical process or thermal calculation.

In the actual source-off native hold, each q_v commutes with H: unitary evolution does not redistribute weight between record sectors. Turning on the owned formation terms can change occupations, but does not by itself cool the system into the global ground sector; its donors, controller work and resulting state remain in the ledger. A positive-cost, record-sensitive degree phase is therefore a genuine prospective regime condition, not an explanation of why that regime or a particular record abundance is realized.

Next discriminating input: a physically owned preparation/sector-selection rule for a declared native parameter point. Enlarging N or minimizing over q without that rule cannot select the sought history. No physical volume, pressure, dark abundance, or gravity law has been imported here.
