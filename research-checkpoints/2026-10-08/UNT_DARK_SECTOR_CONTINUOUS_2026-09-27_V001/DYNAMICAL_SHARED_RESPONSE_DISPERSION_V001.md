# Shared internal response with finite rate and range

2026-09-27. Analytical continuation of
`UNIFIED_INTERNAL_RESPONSE_ENERGY_SCREEN_V001`; this is a conditional
completion to test, not a newly adopted native construct or fitted dark
sector. No numerical run, parameter selection or historical-source edit.

The predecessor was read in full after its resident flag check, at SHA256
`24ac7bd01de85a9e2aee6ee96cb4413d74f3b519f98ba323b70dea1588fdf124`.
It derived local relaxed curvature epsilon_nn−epsilon_nchi²/epsilon_chichi
and explicitly left finite-rate/gradient response open. This note retains
that response and determines the resulting linear modes exactly.

## 1. One conditional local dynamical system

Use an explicitly declared flat physical rest-frame patch and clock, c=1,
with a conserved fluid density n_0>0. Freeze all coefficients at a uniform
stationary background with epsilon_chi=0 and

    mu = epsilon_n > 0,   A = epsilon_nn,
    B = epsilon_nchi,     D = epsilon_chichi > 0,
    Z_t > 0,             Z_s > 0.                              (1)

The retained fluctuation is zeta = delta chi. Its quadratic kinetic and
gradient energy are normalized by Z_t and Z_s. These coefficients and the
physical density, three-space and clock are additional inputs to earn from
the network; none is identified with an uncalibrated graph variable.

For clarity an explicit conservative realization uses a fluid displacement
xi, delta n = −n_0 div xi and v = dot xi, with quadratic Lagrangian density

    L_2 = (n_0 mu/2)|dot xi|² + (Z_t/2) dot zeta²
          −(A/2)(delta n)² − B delta n zeta
          −(D/2)zeta² −(Z_s/2)|grad zeta|².                 (2)

The constant energy and the integral of the linear mu delta n term do not
affect these fixed-total-number perturbations; they are not erased from the
background stress ledger. Positive n_0 mu and Z_t make these kinetic terms
positive. We omit metric perturbations, self-gravity, expansion/damping,
viscosity, sources and coefficient drift only for this local test. This is
not an analysis of all modes of a cosmological or elastic network.

The exact linear equations for this quadratic completion are

    dot(delta n) + n_0 div v = 0,
    mu dot v + grad(A delta n + B zeta) = 0,
    Z_t ddot zeta − Z_s laplacian zeta + D zeta + B delta n = 0. (3)

The SAME B appears in the fluid chemical response and internal force. It
is the shared-energy reciprocity from the predecessor, not two adjustable
couplings for two desired effects.

## 2. Exact longitudinal dispersion and stability

For exp[i(k·x−omega t)], set alpha=n_0/mu>0, K=D+Z_s k²,
and c_n²=alpha A. Eliminating the two longitudinal amplitudes gives

    [omega²−alpha A k²][D+Z_s k²−Z_t omega²]
                         + alpha B² k² = 0.                 (4)

No quasi-static elimination was used. The two exact squared frequencies are

    omega²_± = (1/2){c_n² k² + K/Z_t
                ± sqrt[(c_n² k²−K/Z_t)²+4alpha B²k²/Z_t]}.   (5)

They are real, although a negative squared frequency describes exponential
growth/decay. At k=0 they are 0 and D/Z_t; the uniform density zero mode is
removed if the finite domain's total number is fixed. Transverse ideal-fluid
displacements are neutral in (2), not tested shear waves.

For k>0, both squared frequencies are nonnegative if and only if

    A(D+Z_s k²) >= B².                                     (6)

Indeed their product is alpha k²[A K−B²]/Z_t. If it is nonnegative,
A>=0 and their sum is positive, giving both roots nonnegative. Conversely
two nonnegative roots require that product condition. Consequently:

- All wavelengths of this mathematical continuum are linearly non-growing
  exactly when A D >= B². This includes the neutral A=B=0 case.
- If A>0 but A D<B², precisely the finite band
  0<k²<k_crit²=(B²/A−D)/Z_s is unstable. The boundary is marginal;
  larger k are stable.
- A<0 already has negative intrinsic fluid stiffness and remains unstable
  at every k>0, with an unbounded large-k negative acoustic branch. Adding
  a healthy internal oscillator does not repair that bare-fluid defect.

The small-k fluid branch recovers the prior result:

    omega²_- = alpha(A−B²/D) k² + O(k⁴).                    (7)

At the boundary AD=B², with A>0, the leading term is instead
omega²_- = alpha A Z_s k⁴/D + O(k⁶), nonnegative. At large k the two
principal squared propagation speeds tend to

    {c_n², Z_s/Z_t}.                                       (8)

They may coincide; mode mixing then affects subleading terms, not these
limits. Positive omega² is a linear stability statement, not a causality
proof. A claimed common physical cone separately requires these principal
speeds to be nonnegative and at most one, within a justified high-frequency
continuum regime. No network cutoff or cone has been inferred here.

## 3. Pure mass response: growing modes, but a finite growth ceiling

For the predecessor's epsilon=n m(chi)+V(chi), A=0, B=m', mu=m and
D=n_0 m''+V''. For B!=0, the negative branch occurs at every k>0 in
this frozen continuum. Write omega²_- = −gamma². Exactly,

    gamma² = [sqrt(K²+4Z_t alpha B²k²)−K]/(2Z_t)
           = 2alpha B²k²/[K+sqrt(K²+4Z_t alpha B²k²)],
    0 < gamma² < alpha B²/Z_s,
    lim_(k→infinity) gamma² = alpha B²/Z_s.                 (9)

This ceiling is a supremum, not a maximum at a finite k. A direct proof
without an asymptotic expansion uses

    gamma²(K+Z_t gamma²) = alpha B²k²,
    d(gamma²)/d(k²)
      = [alpha B²−Z_s gamma²]/[D+Z_s k²+2Z_t gamma²] > 0.    (10)

For any unstable branch with A>=0 the same upper bound follows from
(gamma²+alpha A k²)(K+Z_t gamma²)=alpha B²k². In the finite-band case
the growth rate is zero at both band endpoints and its finite maximum is
strictly below that ceiling.

Thus the instantaneous, zero-gradient extrapolation gamma proportional to
k is not the full dynamical prediction. Finite gradient stiffness regulates
that extrapolation; retaining dynamics does not remove the attractive
growing mode. This is not a claim that every wavelength of an actual native
network is unstable: only wavelengths and frequencies inside the fluid and
gradient-expansion domains are admissible. Nor does a finite ceiling alone
make the growth slow enough, establish nonlinear stability, or predict an
acceptable cosmological structure history.

## 4. The same coefficients give a finite-range attractive response

Solving (3) for the driven internal response gives

    zeta(k,omega) = −B delta n(k,omega)/[K−Z_t omega²].      (11)

For a causal driven solution use the retarded prescription and the owned
initial state. Where Z_t|omega²| << K, its slow/quasi-static limit yields

    omega² ≈ alpha k²[A−B²/(D+Z_s k²)].                     (12)

The internal response time and range are distinct linked quantities:
omega_chi,0=sqrt(D/Z_t), c_chi=sqrt(Z_s/Z_t), and
ell_chi=sqrt(Z_s/D)=c_chi/omega_chi,0. Equation (12) still retains finite
range; the purely local adiabatic limit also needs k ell_chi << 1.

The exact STATIC energy minimization over zeta gives

    E_stat^(2) = (A/2) integral (delta n)² d³x
      −(B²/2) integral delta n (D−Z_s laplacian)^(-1)delta n d³x. (13)

On an explicitly adopted infinite flat three-space with a decaying boundary
condition, the inverse kernel is

    G(r) = exp(−r/ell_chi)/(4pi Z_s r),    r>0.             (14)

This follows directly from (D−Z_s laplacian)G=delta^(3).
For two nonnegative weak, nonoverlapping excess-density profiles, the
cross energy is −B² integral delta n_1 G delta n_2. For small localized
profiles it approaches −B² Q_1 Q_2 G(r), favoring smaller separation.
Self terms require smooth profiles or an explicit microscopic regulator;
no point-particle divergent self-energy is silently discarded.

Equations (9), (12) and (14) describe different limits of ONE response
using the SAME B,D,Z_t,Z_s. This is a candidate finite-range attraction,
not a separately fitted force law. In the mass/background ansatz the same
chi also contributes the background potential V and its vacuum-form stress
when its gradients and kinetic energy are negligible. Neither its absolute
V nor an observational force amplitude/range has been derived here.

Interpreting growing modes as attractive, Jeans-like clustering rather than
only as a local negative-pressure response is familiar in
[Bean, Flanagan and Trodden (2008), sections III–IV](https://arxiv.org/html/0709.1128v2).
That primary analysis also stresses approximation domains and growth scales.
Its physical model is not imported as UNT; equations (2)–(14) are the explicit
conditional two-variable calculation here. Since ordinary gravity was
omitted from (2), “Jeans-like” is an analogy to interaction-driven density
growth, not a calculation of the gravitational Jeans scale.

## 5. One mechanics, one ledger, still an unearned physical realization

The constructive next input is the same-parent derivation of a conserved
physical n, an internal chi, complete epsilon(n,chi), and the kinetic/gradient
coefficients Z_t,Z_s with their clock and distance units. The same state and
source convention must determine A,B,D and satisfy mixed-derivative
reciprocity. This fixes attraction, response range, internal frequency,
density stiffness and growth rates jointly, rather than fitting a galaxy
force and an expansion law independently.

The full stress and background action must retain V, all reference/matching
terms and derivative energies exactly once. Adding a constant to epsilon
leaves (4) and (13) unchanged but changes the homogeneous accelerating stress;
these perturbation data do not fix that constant. Physical metric/volume
variation can detect it. Likewise local dispersion does not select initial
abundance or the state reached during formation.

Once these microscopic inputs exist, compare the allowed instability band
and growth rates with the actual dynamical/observational domain, including
gravity, expansion, preparation and nonlinear evolution where needed.
No galaxy rotation curve, light-propagation relation, cosmic expansion,
primary A/M abundance, native three-dimensional geometry or complete
unification is claimed by this conditional screen.
