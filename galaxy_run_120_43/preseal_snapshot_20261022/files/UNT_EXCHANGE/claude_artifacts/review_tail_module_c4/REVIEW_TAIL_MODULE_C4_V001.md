# REVIEW_TAIL_MODULE_C4_V001 — UV-tail module: single-reviewer verdict **PASS** on 0505 items 1–5, with 3 notes

Claude4 main session, single reviewer, inline; 2026-10-18T05:36:57Z (`date -u`). Dispatch `FROM_CODEX/0505` (2ebb4e45…). No helpers, no launches. Read-only outside this directory. No NGC3198 target or velocity file opened.

## Object (sha256 from bytes)

`tail_scheme_impl_c2/module/HASHES.txt` (a82d0338…): 47/47 entries OK. Byte copies are in `copies/`.

| File | sha256 |
|---|---|
| owned_uv_tail_lapse_v001.py | `c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22` |
| uv_tail_source_roster_c2v001.py | `4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2` |
| posix_libm_bessel_jn_provider_c2v001.py | `d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171` |
| Registered profile GALAXY_RADIAL_SOURCE_REFERENCE_V001.json | `f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b` |
| forward_v002 `radial_surface` | `e9be043b…` (pin checked) |

**Method.** One numpy script, `tools/rtm_checks_v001.py`, run with the pinned runtime `-I -B`, `nice -n 10`, 1 BLAS thread; every run ≤ 10 s and ≤ 164 MB.
- The references avoid the module's Bessel and harmonic code:
  - exact-arc azimuthal integrals;
  - Cartesian tensor GL brute force over the k-shell;
  - my own J0 by the integral representation;
  - dense adaptive Hankel quadrature.
- Outputs: `out/RTM_CHECKS_*_V001.json`.

## Results (0505 items)

**1. Stars (TESTED-POSITIVE).**
- Profile: h = 0.04909899 kpc, Rd = 0.35842261 kpc.
- **Vertical factor.** x/sinh x with x = πh|k_z| equals the numeric Fourier transform of sech²(z/2h)/(4h) to 3.3e-16, for k_z ≤ 50 /kpc.
- **Convention.** It matches the registered ring rule z = 2h·atanh(u) (prep v007:172-190, "sech²(z/2h)/(4h) dz = du/2") (FORMAL).
- **Radial transform.** `radial_surface` beyond the last node is exactly Σ_last·e^{−(R−R_last)/Rd}. The module's P_*(k) equals my independent Hankel transform to ≤ 2e-16 (relative to P(0)) for k = 0–20 /kpc.
- **Mass.** The total is 11,925,050.0495 M☉, equal to the registered total. The doubling certificate passes at 2e-16.

**2. Gas cubic-Lagrange rule (TESTED-POSITIVE).**
- The registered DDO154 HI+He Σ is a quadratic Bernstein form in s per annulus. Its annular means are reproduced to 1.4e-17.
- σ_i(k_z = 0) equals the registered Σ at the GL4 nodes to 1.2e-16.
- The cubic interpolant equals the registered quadratic Bernstein Σ on a dense s grid to 6e-16. This is an exact representation, because cubic ⊇ quadratic.
- The transform Σ_i P_i σ_i equals my Hankel transform of the registered Σ:
  - to ≤ 1e-16·P0 up to 128 /kpc at the production M_s = 64 (DDO) and 96 (NGC);
  - mass 427,005,912.713 M☉, equal to the registered value.

**3. Symbol (FORMAL, plus TESTED by item 4's brute force).**
- pref = λ/(4γ_eff(2π)³) (L684) and fac = pref·w·k_⊥/(k_⊥² + k_z²) (L746), so T∞ = 1/(4γ_eff k²) = Q∞·T_N.
- **Sign.** The sign follows the J = −mc² convention (roster `S_T = −c²[…]`; prep v007 column J = −m c²).
- **γ_eff in route A.** The controller passes `fourier_arguments['gamma']` (route_a controller L283). Driver v008 sets that to s·γ (L900), the net γ of the static EH block (L717), i.e. A21's γ_eff.
- Other callers (route B, offset, NGC) must pass their stage's net γ; that is not reviewed here.

**4. m = 4j cube-corner harmonics (TESTED-POSITIVE).**
- **Coefficients.** c0 = 2π − 8a and c_4j = −8 sin(4ja)/(4j) with a = arccos(L/k_⊥); h_j = 2c_4j^D (FORMAL derivation agrees).
- **Azimuthal integral.** The module's W_D equals exact-arc integration to 6.3e-15 on 504 cases: kept cube 4 with outer cube 6 or cylinder 7; k_⊥ 3–8.4; k_z inside and outside; R 0.5–10 kpc; 6 azimuths.
- **Assembled tail.** For a synthetic complex Gaussian source (offset in z), compared with brute force:
  - cube(6)\cube(4): ≤ 1.9e-13 at 5 points (off-axis, z ≠ 0 and R = 0), with the brute force self-converged to 2.4e-13;
  - an **azimuth sweep at R = 2.5 kpc over φ ∈ [0, π/4]**: the corner harmonics change the field by about 100% of its value, and the module matches the brute force to ≤ 1.9e-13 at every φ;
  - cylinder(7)\cube(4): ≤ 5e-14.
- **Jets.** The gradient agrees with central differences of the value to 2.4e-8, which is finite-difference level.

**5. Tail-OFF (TESTED-POSITIVE).**
- With an empty domain, D = ∅ (cylinder K_big = K and cube K_out = K over cube K):
  - every jet is exactly equal to prep v007's `np.zeros` boundary in shape and dtype, with no −0.0;
  - `lapse_pair` gives exact zeros.
- R0 holds: on a non-empty state, bd(z = 0) is exactly 0.0, and b0 equals `value` exactly.

## Notes (not defects of the reviewed scope)

**N1 (hardening).** The gas radial quadrature (M_s GL nodes per annulus) has no accuracy certificate; the stars have a doubling certificate.
- A config with M_s = 8 is accepted, but it is inaccurate at k_⊥ ≥ 16 /kpc: 2e-3·P0 at 32 /kpc (TESTED).
- The production M_s = 64/96 is accurate through 128 /kpc (TESTED).
- Suggestion: add a doubling certificate, or a minimum M_s tied to k_max·ΔR.

**N2.** The continuum stars vertical factor departs from the registered *discrete* ring rule at high k_z: 1.5e-4 absolute at GL64 by k_z = 50 /kpc. This is the design's continuum_v001 against nodes_v001 choice. The deciding test is I1-T/T2-I, as the roster docstring says.

**N3.** `enabled = False` refuses at build (UV_TAIL_DISABLED); it does not return zeros. So "tail-OFF" bitwise identity is a driver/controller property: v010 must not install a TailBoundary. That is not covered here; only the module's empty-domain zeros are.

## Scope limits (UNTESTED here)

- route_a/route_b/v010 integration;
- the NGC H2 component;
- the sphere-kept mask path;
- the nodes_v001 packet;
- field_bound/srb_rot/monitor_MT and the certificates;
- production builds on registered route states (the module's own tests A–H).

**Disclosure.** My first T1 reference used a single GL64 rule over the full circle, which under-resolved exp(i·30cos ψ) and showed a spurious 8e-4. I refined it to 0.1-rad pieces with GL24; the agreement is then 6e-15.
