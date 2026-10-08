# Native photon-source pathway: exact spectral constraints

2026-09-29. Analytical continuation of the continuous-CMB source screen.
No new state propagation, physical photon law, temperature fit or observational
test is reported. The original formed vectors and Hamiltonians remain intact.

## Result

The next source test can use the existing native state rather than choosing
a radiation law to fit a blackbody.

- Coupling a weak photon probe only to the held **record count R** has
  exactly zero nonzero-frequency native transition support. A finite-time
  switching signal is possible, but its energy is not extracted from the
  conserved held network Hamiltonian.
- Coupling instead to **link occupation n** permits energy exchange. The
  inherited 16-state cell fixes five distinct positive transition gaps and
  their matrix elements exactly. Actual prepared populations determine
  absorption versus emission; no passive or thermal replacement is justified.
- A stationary, energy-dephased diagnostic and the actual nonstationary
  source are different experiments. Both have inexpensive exact checks.
  Neither a five-line cell nor an assumed thermal ratio already supplies
  the smooth Planck-preserving opacity in the preceding CMB note.

This identifies a concrete native-to-radiation calculation, while retaining
the photon/interface assumptions and complete source-energy debit.

## 1. Minimal adopted probe, not a photon derivation

Adopt one positive-frequency bosonic probe,

\[
 H_\gamma=\hbar\omega a^\dagger a,\qquad
 H_{int}(t)=g(t)O(a+a^\dagger),\qquad O=O^\dagger,
 \quad\omega>0.
 \tag{1}
\]

O is an owned dimensionless native operator; g has energy units. An
electromagnetic interpretation additionally needs a spatial coupling,
polarization, mode measure and calibrated physical clock/energy scale.
None follows just by calling this oscillator a photon. A collection of
probes can later carry those specifications; continuum cutoffs and any
counterterms must be owned rather than silently discarded.

The standard weak-probe relation between unsymmetrized noise, absorption,
emission and detailed balance is the explicitly imported quantum-probe
framework, not a theorem that the native network is a thermal bath. See
[Clerk et al., quantum noise review](https://arxiv.org/abs/0810.4729).
The native matrix identities and state restrictions below are derived
directly from the resident Hamiltonian.

In inherited units the held 16-state Hamiltonian is

\[
 H_N=3I+R-X_a+(\tfrac94I-\lambda_R R-\tfrac12X_C)n,
 \qquad R=Q_L+Q_R,
 \tag{2}
\]

with native `lambda_R=1/2`, incidence flip h=1 and copy couplings zero.
`[H_N,R]=[H_N,X_C]=0`, but `[H_N,n]` is nonzero. The original three
preparations and five retained ages are available in
`RECORD_ADDITION_RESULTS.json`; their complete complex vectors, source
switch work and all bands must remain in the ledger.

## 2. Record-count coupling: exact held null and switching exception

Take O=R. Since R(t)=R, for any initial native density matrix,

\[
 \langle R(t)R(t')\rangle=\langle R^2\rangle,\qquad
 \chi^R_{RR}(t,t')=0.
 \tag{3}
\]

The stationary raw spectrum is `2 pi <R^2> delta(omega)`; subtracting
the mean replaces `<R^2>` by `Var(R)`. There is no positive or negative
nonzero-frequency line. Equivalently,
`P_E R P_F=0` whenever E differs from F. A phase advancing between record
sectors does not change this selection rule for the count operator.

More strongly, `[H_N,H_N+H_gamma+g(t)R(a+a^dagger)]=0`, even with a
time-dependent g. The native held energy is exactly constant. To see why
this does not forbid every finite-time photon signal, abruptly switch a
constant g on at time zero with factorized photon vacuum. The exactly
forced oscillator obeys

\[
 a(t)=e^{-i\omega t}a(0)
 -\frac{gR}{\hbar\omega}(1-e^{-i\omega t}),
\]
\[
 \langle N_\gamma(t)\rangle
 =\frac{4g^2\langle R^2\rangle}{\hbar^2\omega^2}
    \sin^2(\omega t/2),\qquad
 \langle H_{int}(t)\rangle=-\hbar\omega\langle N_\gamma(t)\rangle.
 \tag{4}
\]

Removing the coupling at that time costs
`-<H_int>=hbar omega <N_gamma>`. This finite coherent dressing/switching
signal is not sustained extraction of record-storage energy. A dressed
static state likewise does not define an outgoing free-photon flux by its
bare oscillator occupation alone. Initial interaction energy or an external
drive must not be omitted.

During formation, record-target copies do not commute with R and can
give finite-frequency response; their actual dynamics and energy source
must then be included. A different phase/writer operator is also a different
coupling, not an exception to the held-count result.

## 3. Link occupation: complete exact native gap census

Fix `R=0,1,2` and carrier eigenvalue `s=+/-1`. Set

\[
 x_{Rs}=\tfrac94-\tfrac12R-\tfrac12s,\qquad
 d_{Rs}=\sqrt{x_{Rs}^2+4},\qquad
 E_{Rs\beta}=3+R+\frac{x_{Rs}+\beta d_{Rs}}2.
 \tag{5}
\]

The endpoint-record multiplicities are `m_R=(1,2,1)`. Since n preserves
both R and s, its only nonzero gaps connect the two link bands in the
same block:

| R | s | x | positive gap d | record multiplicity |
|---:|---:|---:|---:|---:|
| 0 | +1 | 7/4 | sqrt(113)/4 | 1 |
| 0 | -1 | 11/4 | sqrt(185)/4 | 1 |
| 1 | +1 | 5/4 | sqrt(89)/4 | 2 |
| 1 | -1 | 9/4 | sqrt(145)/4 | 2 |
| 2 | +1 | 3/4 | sqrt(73)/4 | 1 |
| 2 | -1 | 7/4 | sqrt(113)/4 | 1 |

Thus there are exactly **five distinct positive operator gaps**, their
negative partners, and a zero-frequency diagonal contribution. Counting
orthogonal degenerate record channels, the positive-gap multiplicities
ordered by radicand 73,89,113,145,185 are 1,2,2,2,1. These are allowed
operator channels, not an assertion that every chosen state populates them.

The band projectors give independently

\[
 n_{\beta\beta}=\frac{1+\beta x/d}{2},\qquad
 |n_{+-}|^2=\frac1{d^2},\qquad
 \langle X_a\rangle_\beta=-\frac{2\beta}{d}.
 \tag{6}
\]

For the feedback-off Hamiltonian x does not depend on R, leaving only
`sqrt(113)/4` and `sqrt(185)/4`. The copying-off state has R=0 exactly;
although its full held operator retains five allowed gaps, its populated
n-spectrum is restricted to those same two. No energy from a missing
record population may be assigned to it.

These gaps are in the inherited microscopic energy units. Assigning
physical microwave frequencies requires the missing physical energy/clock
calibration, not a choice of plotting units.

## 4. A separately labelled stationary spectral diagnostic

For a stationary density matrix rho_s, define the raw unsymmetrized
spectrum with this fixed Fourier convention:

\[
 S_O(\omega)=\int_{-\infty}^{\infty}d\tau\,
 e^{i\omega\tau}\operatorname{Tr}[\rho_s O(\tau)O(0)].
 \tag{7}
\]

Its positive-frequency weight is native **absorption** (upward native
energy); its negative-frequency weight is native **emission**. Subtracting
the stationary mean affects only the zero-frequency line. Positivity
follows from the energy-projector transition probabilities, not from a
presumed ground state.

A reproducible diagnostic for the saved formed vector rho_0 is
`rho_bar=sum_E P_E rho_0 P_E`, retaining all exactly degenerate subspaces.
This dephasing preserves band populations and mean held energy. It changes
the state, generally removes its advancing record phase, and is **not**
silently substituted for actual formation/hold evolution. The infinite
time average of the isolated density is a mathematical interpretation of
this diagnostic, not a demonstrated physical equilibration process.

Let `w_Rs,beta=Tr(rho_bar P_Rs,beta)`, including record multiplicity in
the trace. For n,

\[
 S_n(\omega)=2\pi Z_0\delta(\omega)
 +2\pi\sum_{R,s}\frac{1}{d_{Rs}^2}
 \left[w_{Rs,-}\delta(\omega-d_{Rs}/\hbar)
       +w_{Rs,+}\delta(\omega+d_{Rs}/\hbar)\right],
 \tag{8}
\]

where `Z0=sum_(R,s,beta) w_Rs,beta*n_beta,beta^2` for the raw spectrum.
For connected noise subtract `<n>_bar^2` from Z0. Identical gaps, including
the two sqrt(113)/4 blocks, must be summed before forming a measured
line ratio. No arbitrary basis choice within the R=1 degeneracy is needed.

Useful exact checks are

\[
 \int\frac{d\omega}{2\pi}S_n(\omega)=\langle n\rangle_{\bar\rho},
 \quad
 2\sum_{d>0}d(W_{abs,d}-W_{em,d})=\langle X_a\rangle_{\bar\rho}.
 \tag{9}
\]

Here W denotes the coefficient after dividing the line weight by `2 pi`.
The first equality uses the raw spectrum and `n^2=n`. The second follows
from `[n,[H_N,n]]=X_a`. It must use the dephased `<X_a>`, not the
age-dependent coherence of the actual saved state.

## 5. Actual formed-state probe: two times and positive finite windows

The actual state at an old held age w is
`rho_w=exp(-i H_N w/hbar) rho_0 exp(+i H_N w/hbar)`. Its owned correlation
and response are

\[
 C_O(w+\tau,w)=\operatorname{Tr}[\rho_w O(\tau)O(0)],
 \quad
 \chi^R_{OO}(w+\tau,w)=\frac{i}{\hbar}\theta(\tau)
   \operatorname{Tr}[\rho_w[O(\tau),O(0)]].
 \tag{10}
\]

For n, the exact initial retarded slope is
`partial_tau chi|0+=<X_a>_rho_w/hbar^2`; for R it is zero and the full
retarded kernel vanishes. An energy-projector expansion of (10) retains
the actual coherence terms. They cannot generally be represented by one
positive stationary noise spectrum or a single bath temperature.

For an initially vacuum probe over a fixed window T, its leading creation
probability has an especially clean positive form. Define, using rho_w,

\[
 F_{\omega,T}=\int_0^T ds\,e^{+i\omega s}O(s),\qquad
 P_{create}^{(2)}=\frac{g^2}{\hbar^2}
                \operatorname{Tr}(\rho_w F^\dagger F)\ge0.
 \tag{11}
\]

Equivalently use rho_0 and `O(w+s)` inside F, but do not apply both age
shifts. The raw correlation includes any coherent mean drive. Equation
(11) is the second-order weak-coupling coefficient, not an exact probability
at arbitrary g,T. It remains meaningful when a time-local rate or Wigner
spectrum would not be positive. For R it reduces to the bounded switching
coefficient in (4), whose rate divided by T tends to zero at fixed omega.

In an additional stationary weak-coupling, energy-resolving reservoir limit,
the oscillator birth and death coefficients are formally

\[
 A_\omega=\frac{g_\omega^2}{\hbar^2}S_O(-\omega),\qquad
 B_\omega=\frac{g_\omega^2}{\hbar^2}S_O(+\omega),\qquad
 \dot f=A_\omega(1+f)-B_\omega f.
 \tag{12}
\]

A finite isolated cell has discrete spectral measures and recurrences,
not automatically a maintained Markov bath. A resonance of one isolated
probe can have coherent, rather than constant-rate, evolution. Therefore
use (8) as line strengths unless broadening, reservoir renewal and the
relevant time limit have actually been derived. The finite-window (11)
does not require that replacement.

## 6. Detailed balance and the earlier inverse opacity

A thermal stationary bath satisfies the KMS/detailed-balance condition

\[
 S_O(-\omega)=e^{-\beta_N\hbar\omega}S_O(+\omega).
 \tag{13}
\]

For the five-line n diagnostic, a necessary common positive-temperature
condition is that `log(W_abs,d/W_em,d)/d` have one positive value at every
occupied line. Zero weights, absent lines and inversion must be reported
explicitly, not repaired with an arbitrary floor. This is a test of the
coupled n-channel only. Since n preserves R and carrier s, unrelated
sector weights can remain unconstrained even if this test passes; it is
not proof of a full Gibbs state or KMS relations for every native operator.

If detailed balance holds, `kappa=B-A>=0` and (12) becomes
`kappa*(f_P(T_N)-f)`. Actual inverted populations can instead give gain;
their response must not be replaced by a passive spectrum merely to
obtain positive opacity.

The earlier exact-Planck net-injection source requires, with `r=T_N/T>1`,
`u=T_dot/T+H>0` and `G(x)=x exp(x)/(exp(x)-1)^2`,

\[
 \kappa_{req}(\omega)
 =\frac{uG(x)}{f_P(x/r)-f_P(x)},\qquad
 x=\hbar\omega/(k_BT).
 \tag{14}
\]

Both the emission/absorption ratio and the frequency dependence must now
come from the same native coupling and state. KMS fixes a ratio, not the
spectral density or (14). The isolated held cell's five delta lines cannot
equal the positive smooth opacity (14) across a continuous frequency band.
Repeating identical independent cells multiplies strengths, not gap support.
A larger network, a derived distribution of environments or radiative
broadening could change the support, but each needs its own dynamics and
energy ledger. Freely fitting one width, occupation or coupling per frequency
would not establish native prediction.

For balanced maintenance `u=0`, a pre-existing Planck spectrum need not
change. Vanishing net injection does not mean zero microscopic replacement,
but a line-limited bath neither demonstrates broadband replacement nor
generates a Planck distribution in uncoupled modes. No conclusion about all
network-CMB mechanisms follows from this single-cell support result.

## 7. Exact energy debit and the smallest numerical discriminator

For the complete probe Hamiltonian (1),

\[
 \frac{d}{dt}\langle H_N+H_\gamma+H_{int}\rangle
       =\dot g\langle O(a+a^\dagger)\rangle.
 \tag{15}
\]

Native, photon and interaction energy currents are their actual commutators.
At constant g their sum is zero. Only in a justified stationary weak-coupling
exchange limit can the averaged interaction storage be neglected so that
`Q_N=-Q_gamma`, with
`Q_gamma=sum_modes hbar*omega*[A(1+f)-B*f]`. A finite donor's populations
then deplete or change; resetting/replenishing them requires owned work.
Cosmological use must also retain both sectors' physical pressure and
expansion work, as in the preceding CMB note. Record retention does not by
itself authorize a continuing heat budget.

The smallest prospective test uses the existing three formed vectors and
their unchanged held Hamiltonians, without a new formation run:

1. Verify R's commutator and all off-energy-block matrix elements vanish.
2. Check (5)--(8) with the full numerical projectors, including the exact
   degeneracies, duplicate gap, zero line and actual weights. Label the
   energy-dephased diagnostic explicitly; preserve the actual vectors.
3. Report every populated absorption/emission strength and line ratio.
   Test (9) and actual two-time (10) at the retained ages; do not use a
   thermal fit or a shared-temperature success requirement as a numerical
   correctness check.
4. If a finite-window probe is added, use (11) with an independent
   spectral-integral check and a counted switching/interaction ledger.
   That is a separate explicitly adopted probe experiment, not a microwave
   background calculation.

The root alone owns execution. No numerical census has been produced by
this analytical note. The conserved-count/switching result, spectral
conventions and five-gap census received an independent analytical check
from the CMB-source author; no second worker was run.

## Reviewed input identities

SHA-256 identities of resident inputs read for this derivation:

- `CMB_CONTINUOUS_SOURCE_ANALYSIS_V001.md`:
  `b4cb12de9a11767f91b6441d860711e09f4f8e64ec7d1517c5065e7ffbe50ad4`.
- `record_addition_compute.py`:
  `4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10`.
- `RECORD_ADDITION_RESULTS.json`:
  `2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a`.
- `NATIVE_TEMPORAL_KERNEL.md`:
  `ad3b095e8a687e76bc7581d79cbb125e92f8b5a61a75e9c8f785a2ebe00fc534`.

The existing record-addition protocol/report were also read. Hash custody
identifies the sources; it does not turn the added photon-probe premises
into a native physical derivation.
