# Conserved-scalar PRIMAT route: exact action current, prescribed neutrino history

2026-09-29. Additive source/physics review and implementation design. No external
source was imported or executed here; no compilation, nuclear integration,
abundance scoring, installation or new state preparation was performed.
This is a concrete repair of the *scalar-density* proxy identified in
`PRIMAT_2026_INTERFACE_AUDIT_V001.md`, not a claim that altered neutrino
decoupling is now solved. The hot ordinary history is an explicitly imported
comparison, not a derived UNT thermal origin or a Big Bang/inflation premise.

## 1. Bound source and the usable interface

The primary source is [PRIMAT commit
4bf97d5082eee54b9df50d88f43182bb651fea80](https://github.com/CyrilPitrou/primat/tree/4bf97d5082eee54b9df50d88f43182bb651fea80).
Read-only snapshots live in `bbn_inputs_v001/primat_c_reference_v001/`.
`SOURCE_REVIEW_CENSUS_V001.json` inventories 27 headers and 26 C files
(827,648 bytes), initially with only five documentation/interface snapshots.
The additional receipts bind actual implementation bytes:

| Receipt | SHA256 | Newly read implementation |
| --- | --- | --- |
| `IMPLEMENTATION_READ_RECEIPT_V001.json` | `8bc4bec741948148086132cd2e193fd5970358b498bbc886ba88434dabd322b0` | background, neutrino history, API |
| `IMPLEMENTATION_READ_RECEIPT_V002.json` | `92405267e0856cd62d8f35593c52678ea07126736bd5c3ce49f52083a746803b` | config, config/neutrino/constants headers |
| `IMPLEMENTATION_READ_RECEIPT_V003.json` | `839ce03523c227f067d1239e25db2d8c70c5b8a002ad0644fa420c75a37ed295` | constants implementation |

All eight receipt members (244,520 bytes) were independently checked against
their byte counts, SHA256 and pinned Git-blob SHA1. Full background, neutrino
history, API and constants implementations were read; configuration defaults,
validation, units and cache/path sections were read directly. No conclusion
about an unread dependency is inferred from a function name.

The load-bearing interface is `cpr_bg_Hubble(bg,Tg,Tnue,Tnumu,Tnutau,a)` in
`background.c`. Temperatures are MeV, energy densities are MeV^4 and the
returned H is s^-1. Its default two-dimensional ODE evolves

    x = ln(a T),       t_rel,
    dx/d ln T = 1 + d ln a/d ln T,
    dt_rel/d ln T = (d ln a/d ln T)/H(T,a),
    a = exp(x-ln T).                                      (1)

The actual evolving a is therefore available at every H evaluation: no
temperature-to-scale-factor power-law substitution or inverse lookup is
required. The standard branch then constructs the ordinary weak-rate tables
using the imported NEVO temperature and spectral histories.

Do **not** use `custom_background` to provide the new H: `config_validate`
explicitly forces `incomplete_decoupling=False` and
`spectral_distortions=False` for that branch. That would change the weak-rate
physics while ostensibly changing only expansion. `external_scale_factor`
is also unnecessary; the default entropy/current ODE (1) is the desired
declared fixed-heating comparison.

## 2. The exact same-state insertion

Use the already owned finite-gap scalar-fluid constitutive function e_R(I),
not a constant DeltaNeff fluid, and preserve each inherited state label:

    I(a)=I1/a^3,
    rho_H(a)=rho_H1 e_R(I1/a^3)/e_R(I1),
    p_H(a)=rho_H1 [I omega_R(I)-e_R(I)]/e_R(I1),
    d rho_H/d ln a = -3(rho_H+p_H).                       (2)

Here rho and p are energy density and pressure in the same natural units.
The current identity is exact in the separately adopted scalar macro-action;
it does not require an unprovided microscopic fast-clock calibration. The
ordinary nuclear/thermal history and validity of that macro-action at these
temperatures remain adopted inputs.

The clean candidate patch is a **replacement**, not an extra amplitude:

    old matter term:  rhocdm_a3 / a^3
    candidate term:   rhocdm_a3 * e_R(I1/a^3)/e_R(I1).     (3)

Keep `cfg.Omegach2=Omega_exc*h_cal^2` as an explicitly relabelled present
density normalization, not as a second CDM population. This both satisfies
the upstream positive-value validation and preserves its setup identity

    rho_H1 = Omega_exc*h_cal^2*rho_crit,100,
    rho_Lambda = (h_cal^2-omega_b-Omega_exc*h_cal^2)
                  *rho_crit,100.                         (4)

For the existing Omega_Lambda=1-Omega_m reference families, (4) is the
already matched vacuum. Simply setting Omegach2 to zero would instead move
its density into Lambda and is wrong. Any future family with a separately
specified vacuum must set its exact retained value explicitly. Do not add
DeltaU again on top of rho_Lambda. H_cal remains the inherited critical-density
scale: adding ordinary radiation does not authorize renormalizing it to the
actual present H or rematching the vacuum.

Set `DeltaNeff=0`, extra_rho absent, EDE absent, chemical potentials zero and
analytic neutrino distortions absent in this candidate branch. The ordinary
three-flavour NEVO history remains present. An output named upstream `Neff`
describes that ordinary neutrino sector; it must not be relabelled as the
scalar energy density. Report scalar rho, p, w and current separately.

A minimal derived-source implementation can add a borrowed, immutable
material context to the standard background initializer, with a separate
candidate entry point; the ordinary initializer remains identical. No
process-global mutable state is needed. The candidate branch changes only
the matter term in H and propagates invalid/nonpositive density or H as an
explicit failed invocation. The adapter can call the existing setup stages
directly, as `api.c` does, retaining background arrays before freeing them.
No adapter or patch is authored by this note.

## 3. Physical units and endpoint normalization

The source defines `cpr_MeV4_to_gcmm3()` explicitly. Thus a saved SI mass
density maps to natural energy density as

    rho[MeV^4] = 1e-3 rho_mass[kg/m^3]
                    /cpr_MeV4_to_gcmm3().                 (5)

Equivalently, (4) uses the source's own G and H100 conversion and must agree
with (5), subject to explicitly reported inherited Mpc/constant conventions.
Do not multiply by c^2 a second time after this mass-density conversion.
Temperature overrides use the config setter so eta and relevant cache
fingerprints are recomputed. The old table used T0=2.7255 K; current
same-state photon normalization uses its separately pinned value. Preserve
these labels and compare candidate and its ordinary control at the *same*
chosen T0, rather than silently mixing them.

An apparent scale-factor problem is resolved by the actual implementation:
`cpr_s0bar()` is **4 pi^2/45**, the photon entropy coefficient, despite the
header/background comments describing a high-temperature limit. Therefore

    a_end = (T0/T_end)[sigma_end/(4 pi^2/45)]^(-1/3)       (6)

has the desired photon normalization when the residual electron/QED/heating
tail is negligible. There is no hidden (11/4)^(1/3) rescaling to repair.
Finite-endpoint entropy and heating remainders must still be reported or
bounded. `t_ini=1/(2H_start)` is the source's additive time-origin convention;
it is not a proved age for an arbitrary changed background. Autonomous
reaction evolution depends on elapsed time; any explicit-age observable
would need this convention qualified separately.

The inspected H implementation omits baryon rest energy, although the
reaction network uses `rhoB_BBN=ma*n_gamma0*eta0b/a^3` in g/cm^3. This reaction
mass convention is not an additional cosmic density. A same-background
candidate should explicitly retain rho_b,1/a^3 in H or report its omission
bound, alongside a matched ordinary control isolating that change. The
small correction from evolving mean nuclear mass/binding energy is separate
from scalar conservation and can be bounded by number conservation and the
largest/minimum included mass per baryon; do not call ma*nB the exact
composition-dependent gravitational energy.

## 4. What the fixed reheating approximation actually asserts

Write sigma=s_em/T^3 and C_src=T^-2(ds_em/dT)_supplied, matching the exact
functions used by the background RHS. It uses

    d ln a/d ln T = -C_src/(3sigma+N),
    Tdot = -H T(3sigma+N)/C_src.                          (7)

Both the NEVO temperature ratios and N(T) are imported functions independent
of the altered H. Negative numerical N tail samples are clipped by the
upstream source, and N is zero outside the table domain. Preserve those
source conventions and raw signed inputs in the receipt.

For the actual interpolated neutrino density, the *implied*, not collision-
predicted, exchange is

    Q_nu = dot rho_nu +4H rho_nu
         = H[4rho_nu-T(3sigma+N)rho_nu,T/C_src].           (8)

Consequently the prescribed history fixes Q_nu/H, not Q_nu's response to a
changed expansion from the neutrino collision operator. For the EM sector,
compute the actual interpolant derivative and report

    Q_em/H=3(rho_em+p_em)
                 -T(3sigma+N)rho_em,T/C_src.             (9)

With exact thermodynamic derivatives, rho_em+p_em=T^4 sigma and
rho_em,T=T^3 C_src, so (9) reduces to -N T^4. Otherwise retain the supplied-
versus-interpolated derivative residual, as in the earlier source audit.
Q_em+Q_nu is a useful ordinary-energy consistency diagnostic. Even a small
value does not demonstrate that the prescribed collision transfer is correct
for the new H. The scalar part (2) has zero exchange identically.

This calculation would remove the known proxy's nonconserved scalar source
and can directly measure its abundance effect at unchanged state/baryon
parameters. It does **not** turn the fixed NEVO approximation into a solved
decoupling response. A small change in H alone cannot be promoted to a small
abundance-error bound without a transport/sensitivity bound. Instantaneous
decoupling can be a separately labelled sensitivity calculation, not an
undocumented substitute or guaranteed bracket. A fully qualified reheating
upgrade needs ordinary neutrino energy/spectral transport evaluated with this
same H; the inspected C history module only reads tables.

## 5. Bounded executable route and unresolved data enumeration

The pinned Makefile uses C11, libm and pthread, with no external numerical
package. Its stock main/CLI, Python extension, MC, tests, fuzzing and clean
targets are unnecessary and must not be invoked. A future root-owned build
can use explicit serial compiler arguments over the transitive library
sources and a stdout-only adapter in a separate derived directory; upstream
snapshots remain immutable. GPL-3.0-or-later notices/license must accompany
the bounded receipt. Actual license texts and the exact small-network data
closure still need enumeration; neither the 53-source inventory nor a README
tree diagram is itself a complete executable receipt.

Config defaults are **not** read-only: cache_dir is a writable overlay,
weak/plasma cache misses may generate tables, and save_nTOp defaults on.
All result-file flags must be off (or the explicitly checked in-memory-only
path used), no data-location autodiscovery/overlays allowed, and a cache miss
must fail rather than silently regenerate thermal Monte Carlo tables.
The next bounded source read requested from the already pinned manifest is:

| Source | Bytes | Purpose |
| --- | ---: | --- |
| plasma.c | 35,097 | exact cache names, thermodynamic derivative and regeneration branches |
| weak_rates.c | 70,171 | cache identity, NEVO weak corrections and miss behavior |
| cache.c | 25,680 | writes/fingerprints and contained read-only route |
| network_data.c | 74,068 | exact small reaction list and transitive data files |
| nuclear_network.c | 48,666 | output suppression, finite-history initialization and solver contract |

These 253,682 bytes are requested for source review, not a full-tree download
or execution. After this read, enumerate only required nuclide/reaction,
NEVO, electron/QED and matching weak-cache tables at the same commit, with
byte/Git/SHA identities. Missing/mismatched tables stay explicit failed
prerequisites, not permission to fetch a repository archive or generate data.

The first scientific qualification should be an unchanged ordinary baseline,
then a dust-mode replacement identity, followed by the fixed first existing
finite-gap state and its matched proxy/control. Verify (2), (4)--(9), state
anchors, density positivity, background/network resolution and original
ordinary weak-rate settings before using abundance residuals. At the finite
nuclear initial slice, inherited equilibrium abundances require a rate/H and
initial-relaxation check; neither a 40 MeV background start nor the words
"standard initial data" prove it for every altered history. No candidate
selection or fitting is performed here. The previously frozen marginal
D/H/helium products, reuse/exposure statements and absence of joint theory
covariance remain unchanged.
